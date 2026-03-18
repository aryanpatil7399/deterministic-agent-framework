import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from agent.deterministic_agent import DeterministicAgent

def print_result(title, result):
    print(f"\n{'='*20} {title} {'='*20}")
    print("Execution Flow:")
    print("  -> Input Received")
    print("  -> Validation against Schema")
    print("  -> Registry Lookup for Tool")
    print("  -> Tool Execution")
    print("  -> Output Validation against Schema")
    print("\nResult:")
    print(json.dumps(result, indent=2))

def main():
    agent = DeterministicAgent()
    print("Agent initialized successfully!")

    # 1. ECHO Task
    r1 = agent.process({
        "user_id": "demo_user",
        "task_type": "ECHO",
        "payload": {"message": "Hello World!"}
    })
    print_result("ECHO Task", r1)

    # 2. SUM_NUMBERS Task
    r2 = agent.process({
        "user_id": "demo_user",
        "task_type": "SUM_NUMBERS",
        "payload": {"numbers": [1, 2, 3]}
    })
    print_result("SUM_NUMBERS Task", r2)

    # 3. UPPERCASE_TEXT Task
    r3 = agent.process({
        "user_id": "text_user",
        "task_type": "UPPERCASE_TEXT",
        "payload": {"text": "hello deterministic agent"}
    })
    print_result("UPPERCASE_TEXT Task", r3)

    # 4. Invalid Input (extra field)
    r4 = agent.process({
        "user_id": "hacker",
        "task_type": "ECHO",
        "payload": {},
        "extra_field": "not allowed"
    })
    print_result("Invalid Input (extra field schema violation)", r4)

    # 5. Unsupported Task Type
    r5 = agent.process({
        "user_id": "confused_user",
        "task_type": "UNKNOWN_TASK",
        "payload": {}
    })
    print_result("Unsupported Task Type", r5)

if __name__ == "__main__":
    main()
