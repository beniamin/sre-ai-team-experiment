import os
import redis
import json
import time
import re
import threading
from typing import List, Dict, Any, Optional
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage


class DistributedAgent:
    # Number of consecutive tool errors before forcing escalation
    MAX_CONSECUTIVE_ERRORS = 3
    # Directory for per-agent execution logs
    EXECUTION_LOG_DIR = "/app/docs"
    # LLM retry settings for transient errors (rate limits, server errors)
    LLM_MAX_RETRIES = 5
    LLM_RETRY_BASE_DELAY = 2  # seconds; doubles each retry: 2, 4, 8, 16, 32

    def __init__(self, role: str, redis_host: str = "redis-broker", redis_port: int = 6379, tools=None):
        self.role = role
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.pubsub = self.redis_client.pubsub()
        self.channel = "agent_channel"
        self.chat_history_key = "chat_history"
        self.tools = tools or []
        self.stopped = False
        self._respond_thread = None
        self._execution_log_path = os.path.join(
            self.EXECUTION_LOG_DIR, f"execution_log_{self.role}.md"
        )
        # Recent tool calls kept in memory for richer escalation messages
        self._recent_tool_calls: List[Dict[str, str]] = []

        # Initialize LLM
        base_llm = ChatOpenAI(
            model=os.environ.get("LLM_MODEL", "gpt-5-mini"),
            temperature=0.1,
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1"),
            reasoning_effort="low",
            max_tokens=16384
        )

        if self.tools:
            self.llm = base_llm.bind_tools(self.tools)
        else:
            self.llm = base_llm

        self.system_prompt = self._get_system_prompt()
        print(f"[{self.role}] Agent initialized.")

    def _get_system_prompt(self) -> str:
        return os.environ.get("SYSTEM_PROMPT", f"You are {self.role}.")

    def _log_tool_execution(self, tool_name: str, tool_args: dict, result: str, is_error: bool):
        """Append a tool execution entry to the per-agent log file on disk.
        This file can be read by Architect_Zero via read_file for debugging."""
        timestamp = datetime.now().isoformat()
        status = "ERROR" if is_error else "OK"
        # Truncate large results for the log (keep full output readable but bounded)
        result_truncated = result[:2000] + ("... [truncated]" if len(result) > 2000 else "")
        args_str = json.dumps(tool_args)[:500]

        entry = (
            f"\n### [{timestamp}] {tool_name} — {status}\n"
            f"**Args:** `{args_str}`\n"
            f"**Result:**\n```\n{result_truncated}\n```\n"
        )

        # Also keep in memory for escalation context
        self._recent_tool_calls.append({
            "tool": tool_name,
            "args": args_str,
            "status": status,
            "result_short": result[:300],
            "timestamp": timestamp,
        })
        # Keep only last 10 in memory
        if len(self._recent_tool_calls) > 10:
            self._recent_tool_calls = self._recent_tool_calls[-10:]

        try:
            os.makedirs(self.EXECUTION_LOG_DIR, exist_ok=True)
            with open(self._execution_log_path, "a") as f:
                f.write(entry)
        except Exception as e:
            print(f"[{self.role}] Warning: could not write execution log: {e}")

    def _format_escalation_context(self) -> str:
        """Build a summary of recent tool calls for escalation messages."""
        if not self._recent_tool_calls:
            return "No recent tool calls recorded."
        lines = ["Recent tool execution history:"]
        for call in self._recent_tool_calls[-5:]:
            lines.append(
                f"- [{call['timestamp']}] {call['tool']}({call['args'][:100]}) "
                f"→ {call['status']}: {call['result_short'][:150]}"
            )
        lines.append(
            f"\nFull execution log available at: {self._execution_log_path}"
        )
        return "\n".join(lines)

    @staticmethod
    def _is_retryable_error(exc: Exception) -> bool:
        """Return True if the exception is a transient error worth retrying."""
        exc_type = type(exc).__name__
        exc_str = str(exc).lower()
        # OpenAI / httpx rate-limit and server errors
        if exc_type in ("RateLimitError", "APIStatusError", "APITimeoutError"):
            return True
        for keyword in ("rate limit", "429", "500", "502", "503", "server error", "timeout", "overloaded"):
            if keyword in exc_str:
                return True
        return False

    def _invoke_llm_with_retry(self, messages):
        """Call self.llm.invoke with exponential backoff on transient errors.
        Returns the LLM response or raises on fatal / exhausted retries."""
        last_exc = None
        for attempt in range(1, self.LLM_MAX_RETRIES + 1):
            try:
                return self.llm.invoke(messages)
            except Exception as exc:
                last_exc = exc
                if not self._is_retryable_error(exc):
                    raise  # fatal — don't retry auth failures, bad requests, etc.
                delay = self.LLM_RETRY_BASE_DELAY * (2 ** (attempt - 1))
                self._think(
                    f"Transient LLM error (attempt {attempt}/{self.LLM_MAX_RETRIES}): "
                    f"{type(exc).__name__}: {str(exc)[:200]}. Retrying in {delay}s..."
                )
                time.sleep(delay)
                if self.stopped:
                    raise
        # All retries exhausted
        raise last_exc

    def listen(self):
        """Subscribes to the Redis channel and listens for messages."""
        self.pubsub.subscribe(self.channel)
        print(f"[{self.role}] Listening on {self.channel}...")

        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                self._process_message(data)

    def _get_memory(self, limit: int = 80) -> List[Dict[str, Any]]:
        """Retrieves the last 'limit' messages from Redis history,
        filtering out ::think and tool-result messages to keep context clean."""
        messages = self.redis_client.lrange(self.chat_history_key, 0, -1)
        history = [json.loads(m) for m in messages]

        # Filter out internal noise: thinking messages and raw tool results
        filtered = []
        for msg in history:
            sender = msg.get("sender", "")
            content = msg.get("content", "")
            # Skip thinking messages
            if "::think" in sender:
                continue
            # Skip raw tool result broadcasts (they start with "Tool Result (")
            if content.startswith("Tool Result ("):
                continue
            filtered.append(msg)

        return filtered[-limit:]

    def _process_message(self, data: Dict[str, Any]):
        sender = data.get("sender")
        content = data.get("content")
        timestamp = data.get("timestamp")

        # Don't reply to yourself or your own thinking
        if sender == self.role or (sender and sender.startswith(f"{self.role}::")):
            return

        # Handle STOP command from User
        if sender == "User" and content.strip().upper() == "STOP":
            self.stopped = True
            print(f"[{self.role}] Received STOP command. Halting.")
            return

        # Handle CLEAR command from User — abort everything and reset
        if sender == "User" and content.strip().upper() == "CLEAR":
            self.stopped = True
            print(f"[{self.role}] Received CLEAR command. Aborting all activity.")
            return

        # Handle [DONE] signal from Architect_Zero — team work is complete
        if sender == "Architect_Zero" and "[DONE]" in content:
            self.stopped = True
            print(f"[{self.role}] Job complete. Waiting for new User instructions.")
            return

        # Handle [AWAITING_INPUT] signal from Architect_Zero — need user input
        if sender == "Architect_Zero" and "[AWAITING_INPUT]" in content:
            self.stopped = True
            print(f"[{self.role}] Awaiting user input. Paused.")
            return

        # If stopped, ignore all messages until a new User message resets
        if sender == "User" and content.strip().upper() not in ["STOP", "CLEAR"]:
            self.stopped = False

        if getattr(self, 'stopped', False):
            print(f"[{self.role}] Ignoring message (stopped).")
            return

        print(f"[{self.role}] Received from {sender}: {content[:50]}...")

        should_respond = False

        # Trigger logic
        if f"@{self.role}" in content:
            should_respond = True
        elif self.role == "Architect_Zero" and sender == "User":
            should_respond = True

        if should_respond:
            # Run _respond in a background thread so the listener stays
            # responsive to STOP/CLEAR even during long LLM calls
            if self._respond_thread and self._respond_thread.is_alive():
                print(f"[{self.role}] Already processing a request, skipping.")
                return
            self._respond_thread = threading.Thread(
                target=self._respond,
                args=(content, sender),
                daemon=True
            )
            self._respond_thread.start()

    def _respond(self, user_content: str, sender: str):
        self._think(f"Processing message from {sender}...")

        # Construct prompt with memory
        memory = self._get_memory()

        messages = [SystemMessage(content=self.system_prompt)]

        context_str = "Chat History:\n"
        for msg in memory:
            context_str += f"{msg['sender']}: {msg['content']}\n"

        full_prompt = f"""
        {context_str}

        Current Message from {sender}:
        {user_content}

        Respond as {self.role}. If you need to perform actions, output the tool calls or plan.
        """

        messages.append(HumanMessage(content=full_prompt))

        # Track consecutive tool errors for escalation
        consecutive_errors = 0

        try:
            # ReAct loop for tool execution
            MAX_STEPS = 100
            for step in range(MAX_STEPS):
                step_warning = ""
                if step >= MAX_STEPS - 3:
                    step_warning = " WARNING: You are approaching the maximum execution steps. You MUST ask for help or explicitly tag @Architect_Zero to brainstorm a solution."

                step_msg = SystemMessage(content=f"[SYSTEM] Current thinking step: {step + 1} of {MAX_STEPS}.{step_warning}")

                self._think(f"Thinking step {step + 1}/{MAX_STEPS}...")

                # Check if stopped/cleared mid-loop
                if self.stopped:
                    self._think("Execution aborted by user.")
                    return

                response = self.llm.invoke(messages + [step_msg])

                if response.tool_calls:
                    messages.append(response)

                    for tool_call in response.tool_calls:
                        if self.stopped:
                            self._think("Execution aborted by user.")
                            return

                        tool_name = tool_call["name"]
                        tool_args = tool_call["args"]
                        tool_id = tool_call.get("id", "")

                        self._think(f"Calling tool: {tool_name}({json.dumps(tool_args)[:200]})")

                        tool_instance = next((t for t in self.tools if t.name == tool_name), None)
                        if tool_instance:
                            try:
                                result = tool_instance.invoke(tool_args)
                                result_str = str(result)

                                # Check if the tool returned an error
                                is_error = any(
                                    result_str.startswith(prefix)
                                    for prefix in ("Error", "Access denied", "STDERR")
                                ) or "Error:" in result_str[:50]

                                # Log to execution file (readable by Architect_Zero)
                                self._log_tool_execution(tool_name, tool_args, result_str, is_error)

                                if is_error:
                                    consecutive_errors += 1
                                    self._think(f"Tool error ({consecutive_errors}/{self.MAX_CONSECUTIVE_ERRORS}): {result_str[:200]}")
                                else:
                                    consecutive_errors = 0

                                messages.append(ToolMessage(content=result_str, tool_call_id=tool_id))

                                # Force escalation after too many consecutive errors
                                if consecutive_errors >= self.MAX_CONSECUTIVE_ERRORS:
                                    context = self._format_escalation_context()
                                    escalation_msg = (
                                        f"I have hit {consecutive_errors} consecutive tool errors and need help.\n\n"
                                        f"{context}\n\n"
                                        f"@Architect_Zero — please read {self._execution_log_path} "
                                        f"for full details and help me diagnose this issue."
                                    )
                                    self.speak(escalation_msg)
                                    return

                            except Exception as e:
                                error_msg = f"Tool Error ({tool_name}): {str(e)}"
                                self._log_tool_execution(tool_name, tool_args, error_msg, True)
                                consecutive_errors += 1
                                self._think(f"Tool exception ({consecutive_errors}/{self.MAX_CONSECUTIVE_ERRORS}): {error_msg[:200]}")
                                messages.append(ToolMessage(content=error_msg, tool_call_id=tool_id))

                                if consecutive_errors >= self.MAX_CONSECUTIVE_ERRORS:
                                    context = self._format_escalation_context()
                                    escalation_msg = (
                                        f"I have hit {consecutive_errors} consecutive tool errors and need help.\n\n"
                                        f"{context}\n\n"
                                        f"@Architect_Zero — please read {self._execution_log_path} "
                                        f"for full details and help me diagnose this issue."
                                    )
                                    self.speak(escalation_msg)
                                    return
                        else:
                            error_msg = f"Error: I do not have a tool named '{tool_name}'."
                            self.speak(error_msg)
                            messages.append(ToolMessage(content=error_msg, tool_call_id=tool_id))

                    if self.stopped:
                        self._think("Execution aborted by user.")
                        return

                    continue
                else:
                    content_doc = response.content
                    # Extract text from list-based responses
                    if isinstance(content_doc, list):
                        text_parts = []
                        for item in content_doc:
                            if isinstance(item, dict) and item.get("type") == "text" and "text" in item:
                                text_parts.append(item["text"])
                            elif isinstance(item, str):
                                text_parts.append(item)
                        final_text = "".join(text_parts) if text_parts else str(content_doc)
                    else:
                        final_text = str(content_doc)

                    # Extract and publish <think> blocks
                    think_matches = re.findall(r'<think>(.*?)</think>', final_text, re.DOTALL)
                    for think_block in think_matches:
                        cleaned = think_block.strip()
                        if cleaned:
                            self._think(f"Internal reasoning:\n{cleaned}")

                    # Remove <think> blocks from the final spoken output
                    clean_text = re.sub(r'<think>.*?</think>', '', final_text, flags=re.DOTALL).strip()

                    if clean_text:
                        self.speak(clean_text)
                        # Self-halt if this agent just sent [DONE] or [AWAITING_INPUT]
                        if "[DONE]" in clean_text or "[AWAITING_INPUT]" in clean_text:
                            self.stopped = True
                            print(f"[{self.role}] Self-halting after signal.")

                    break

        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(f"[{self.role}] {error_msg}")
            self._think(f"{error_msg}")
            self.speak(error_msg)

    def _think(self, content: str):
        """Publishes a thinking/internal process message to Redis for logging."""
        message = {
            "sender": f"{self.role}::think",
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        msg_json = json.dumps(message)
        # Save to history so it appears in the log
        self.redis_client.rpush(self.chat_history_key, msg_json)
        # Publish to channel so the console can display it
        self.redis_client.publish(self.channel, msg_json)
        print(f"[{self.role}::think] {content}")

    def speak(self, content: str):
        """Publishes a message to Redis and saves it to history."""
        message = {
            "sender": self.role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }

        msg_json = json.dumps(message)

        # 1. Save to history
        self.redis_client.rpush(self.chat_history_key, msg_json)

        # 2. Publish to channel
        self.redis_client.publish(self.channel, msg_json)
        print(f"[{self.role}] Sent message.")
