#!/usr/bin/env python3
"""PostToolUse hook: remind to run /team-verify after TeamDelete.

Fires after every tool use. Only acts when:
1. tool_name == "TeamDelete"
2. VERIFICATION_PLAN.md exists in current working directory

Injects a systemMessage prompting the agent to call Skill("team-verify").
"""

import json
import os
import sys


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        print("{}")
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")

    # Only care about TeamDelete
    if tool_name != "TeamDelete":
        print("{}")
        sys.exit(0)

    # Check if VERIFICATION_PLAN.md exists in project root
    if os.path.isfile("./VERIFICATION_PLAN.md"):
        result = {
            "systemMessage": (
                "\n⚠️ VERIFICATION_PLAN.md detected in project root.\n"
                "Run automated verification NOW:\n\n"
                'Skill("team-verify", args="./VERIFICATION_PLAN.md")\n\n'
                "This is MANDATORY — do not skip."
            )
        }
        print(json.dumps(result))
    else:
        print("{}")

    sys.exit(0)


if __name__ == "__main__":
    main()
