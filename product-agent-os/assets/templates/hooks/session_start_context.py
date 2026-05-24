from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    root = Path.cwd()
    files = ["AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
    payload = {
        "hook": "session_start_context",
        "workspace": str(root),
        "present": [name for name in files if (root / name).exists()],
        "missing": [name for name in files if not (root / name).exists()],
    }
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
