from __future__ import annotations

import json
import sys


def main() -> int:
    event = sys.stdin.read()
    payload = {
        "hook": "post_tool_use_evidence",
        "decision": "record_evidence",
        "input_bytes": len(event.encode("utf-8")),
        "reminder": "Record command, exit code, and relevant output in RUNLOG.md when useful.",
    }
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
