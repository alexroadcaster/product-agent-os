from __future__ import annotations

import json
import sys


def main() -> int:
    event = sys.stdin.read()
    payload = {
        "hook": "permission_request_summary",
        "decision": "summarize",
        "input_bytes": len(event.encode("utf-8")),
        "required_fields": ["purpose", "scope", "risk", "rollback"],
    }
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
