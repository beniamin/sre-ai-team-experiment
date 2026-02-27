import redis
import json
import uuid
import sys
import threading
from datetime import datetime
import os

# Configuration
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = 6379
CHANNEL = "agent_channel"
HISTORY_KEY = "chat_history"

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
LOG_FILE = os.path.join(LOG_DIR, f"conversation_{timestamp}.log")

def log_to_file(text):
    with open(LOG_FILE, "a") as f:
        f.write(text + "\n")

def listen_for_messages(pubsub, my_id):
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            sender = data.get("sender")
            content = data.get("content")
            
            # Don't print own messages
            if sender == my_id:
                continue
                
            print(f"\n[{sender}]: {content}")
            log_to_file(f"[{sender}]: {content}")
            print(f"[{my_id}]: ", end="", flush=True)

def main():
    # Attempt to connect to Redis
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping()
    except redis.ConnectionError:
        print(f"Could not connect to Redis at {REDIS_HOST}:{REDIS_PORT}. Is it running?")
        sys.exit(1)

    my_id = "User"
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL)

    print(f"Connected to A2A Network as {my_id}.")
    print("Commands: STOP (halt agents) | CLEAR (reset session) | exit/quit")
    print("---------------------------------------------------------------")

    # Start listener thread
    listener = threading.Thread(target=listen_for_messages, args=(pubsub, my_id), daemon=True)
    listener.start()

    try:
        while True:
            user_input = input(f"[{my_id}]: ")
            if user_input.lower() in ["exit", "quit"]:
                break
                
            if not user_input.strip():
                continue

            # Handle CLEAR command — broadcast to agents and wipe history
            if user_input.strip().upper() == "CLEAR":
                clear_msg = {
                    "sender": my_id,
                    "content": "CLEAR",
                    "timestamp": datetime.now().isoformat()
                }
                msg_json = json.dumps(clear_msg)
                r.publish(CHANNEL, msg_json)
                r.delete(HISTORY_KEY)
                print("[System]: CLEAR sent. All agent activity aborted. Session wiped.")
                log_to_file("[System]: CLEAR command sent. Session wiped.")
                continue

            # Handle STOP command — broadcast to all agents
            if user_input.strip().upper() == "STOP":
                stop_msg = {
                    "sender": my_id,
                    "content": "STOP",
                    "timestamp": datetime.now().isoformat()
                }
                msg_json = json.dumps(stop_msg)
                r.rpush(HISTORY_KEY, msg_json)
                r.publish(CHANNEL, msg_json)
                print("[System]: STOP command sent to all agents.")
                log_to_file("[System]: STOP command sent.")
                continue

            log_to_file(f"[{my_id}]: {user_input}")

            message = {
                "sender": my_id,
                "content": user_input,
                "timestamp": datetime.now().isoformat()
            }
            
            # Publish and Save to History
            msg_json = json.dumps(message)
            r.rpush(HISTORY_KEY, msg_json)
            r.publish(CHANNEL, msg_json)
            
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
