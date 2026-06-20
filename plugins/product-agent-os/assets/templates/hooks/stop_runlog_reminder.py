from __future__ import annotations

import json
from pathlib import Path


LIFECYCLE_STATE = Path(".codex/product-agent-os/lifecycle-state.json")


def _marker_summary() -> dict[str, object]:
    if not LIFECYCLE_STATE.exists():
        return {"path": str(LIFECYCLE_STATE), "exists": False}
    try:
        data = json.loads(LIFECYCLE_STATE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"path": str(LIFECYCLE_STATE), "exists": True, "valid_json": False}
    return {
        "path": str(LIFECYCLE_STATE),
        "exists": True,
        "valid_json": isinstance(data, dict),
        "task_id": data.get("task_id") if isinstance(data, dict) else "",
        "task_start_brief_shown": data.get("task_start_brief_shown") if isinstance(data, dict) else False,
    }


def main() -> int:
    payload = {
        "hook": "stop_runlog_reminder",
        "runlog_exists": Path("RUNLOG.md").exists(),
        "lifecycle_marker": _marker_summary(),
        "reminders": [
            "Before closing a work cycle, record files changed, checks run, result, and open risks.",
            "Show a user-visible Completion Brief after execution, verification, or blocked handoff.",
            "Run control-plane sync before the Completion Brief when Product-Agent OS scope, plan, tests, evals, runlog, or evidence state changed.",
        ],
    }
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
