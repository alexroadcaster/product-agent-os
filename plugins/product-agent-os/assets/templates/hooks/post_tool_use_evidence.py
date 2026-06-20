from __future__ import annotations

import json
import sys


def main() -> int:
    event = sys.stdin.read()
    payload = {
        "hook": "post_tool_use_evidence",
        "decision": "record_evidence",
        "input_bytes": len(event.encode("utf-8")),
        "reminders": [
            "Record command, exit code, and relevant output in RUNLOG.md when useful.",
            "Keep verification claims tied to current command/runtime evidence or an explicit accepted gap.",
            "Do not treat hook output alone as completion proof.",
        ],
    }
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
