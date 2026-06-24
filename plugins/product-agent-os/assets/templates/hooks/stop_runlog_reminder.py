from __future__ import annotations

import json
import subprocess
from pathlib import Path


LIFECYCLE_STATE_REL = Path(".codex/product-agent-os/lifecycle-state.json")


def _workspace_root() -> Path:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        result = ""
    if result and result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip())
    current = Path.cwd()
    for candidate in [current, *current.parents]:
        if (candidate / ".codex").exists():
            return candidate
    return current


def _marker_summary() -> dict[str, object]:
    lifecycle_state = _workspace_root() / LIFECYCLE_STATE_REL
    if not lifecycle_state.exists():
        return {"path": str(LIFECYCLE_STATE_REL), "exists": False}
    try:
        data = json.loads(lifecycle_state.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"path": str(LIFECYCLE_STATE_REL), "exists": True, "valid_json": False}
    return {
        "path": str(LIFECYCLE_STATE_REL),
        "exists": True,
        "valid_json": isinstance(data, dict),
        "task_id": data.get("task_id") if isinstance(data, dict) else "",
        "task_start_brief_shown": data.get("task_start_brief_shown") if isinstance(data, dict) else False,
        "brief_schema_version": data.get("brief_schema_version") if isinstance(data, dict) else "",
        "brief_fields_count": len(data.get("brief_fields_present", []))
        if isinstance(data, dict) and isinstance(data.get("brief_fields_present"), list)
        else 0,
    }


def main() -> int:
    root = _workspace_root()
    payload = {
        "hook": "stop_runlog_reminder",
        "runlog_exists": (root / "RUNLOG.md").exists(),
        "lifecycle_marker": _marker_summary(),
        "reminders": [
            "Before closing a work cycle, record files changed, checks run, result, and open risks.",
            "Show a user-visible Completion Brief after execution, verification, or blocked handoff.",
            "If the Task Start Brief was compact or incomplete, record the accepted gap instead of treating the marker as proof.",
            "Run control-plane sync before the Completion Brief when Product-Agent OS scope, plan, tests, evals, runlog, or evidence state changed.",
        ],
    }
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
