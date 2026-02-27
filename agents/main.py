import os
import sys
import time
from pathlib import Path
from core import DistributedAgent
from tools import (
    AVAILABLE_TOOLS, save_file, append_file, read_file, read_env,
    run_shell, run_terraform, run_ansible, delete_file,
    fetch_webpage, run_ssh
)

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(role: str) -> str:
    """Load a system prompt from agents/prompts/{role}.md"""
    prompt_file = PROMPTS_DIR / f"{role}.md"
    if not prompt_file.exists():
        print(f"Warning: No prompt file found at {prompt_file}, using fallback.")
        return f"You are {role}."
    return prompt_file.read_text(encoding="utf-8")


def main():
    role = os.environ.get("AGENT_ROLE")
    if not role:
        print("Error: AGENT_ROLE environment variable not set.")
        sys.exit(1)

    print(f"Starting agent with role: {role}")

    # Load system prompt from .md file
    os.environ["SYSTEM_PROMPT"] = load_prompt(role)

    # Role-based tool filtering
    ROLE_TOOLS = {
        "Architect_Zero": [save_file, append_file, read_file],
        "DevOps_Builder": AVAILABLE_TOOLS,
        "Security_Sentinel": [read_file, read_env, run_shell],
        "QA_Tester": [run_shell, read_file, run_ssh, fetch_webpage],
    }
    tools = ROLE_TOOLS.get(role, [])
        
    # Initialize Agent
    agent = DistributedAgent(role=role, tools=tools)

    try:
        agent.listen()
    except KeyboardInterrupt:
        print("Agent stopping...")

if __name__ == "__main__":
    main()
