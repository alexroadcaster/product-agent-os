from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    payload = {
        "hook": "stop_runlog_reminder",
        "runlog_exists": Path("RUNLOG.md").exists(),
        "reminder": "Before closing a work cycle, record files changed, checks run, result, and open risks.",
    }
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
