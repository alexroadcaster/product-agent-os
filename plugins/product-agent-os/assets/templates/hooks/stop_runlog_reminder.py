from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


LIFECYCLE_STATE_REL = Path(".codex/product-agent-os/lifecycle-state.json")
TERMINAL_STATUSES = {"ready_for_completion_brief", "blocked", "stopped_repair_required"}
WORKSPACE_ROOT_ENV = "CODEX_HOOK_WORKSPACE_ROOT"
COMPLETION_BRIEF_FIELDS = [
    "Task ID:",
    "Result status:",
    "What was done:",
    "Files / artifacts changed:",
    "Verification evidence:",
    "Residual risks / accepted gaps:",
    "Follow-up:",
]
REMINDER = (
    "Before stopping, finish implementation, verification, task-plan update and control-plane sync. Then set the "
    "lifecycle marker to ready_for_completion_brief, blocked, or stopped_repair_required and send one terminal Completion Brief as the final response."
)


def _read_payload() -> dict[str, Any]:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _workspace_root(payload: dict[str, Any]) -> Path:
    override = os.environ.get(WORKSPACE_ROOT_ENV)
    if override:
        return Path(override).resolve()
    payload_cwd = payload.get("cwd")
    current = Path(payload_cwd).resolve() if isinstance(payload_cwd, str) and payload_cwd.strip() else Path.cwd()
    for candidate in [current, *current.parents]:
        if (candidate / ".codex").exists():
            return candidate
    return current


def _completion_ready(root: Path) -> bool:
    try:
        marker = json.loads((root / LIFECYCLE_STATE_REL).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return (
        isinstance(marker, dict)
        and marker.get("completion_ready") is True
        and marker.get("status") in TERMINAL_STATUSES
    )


def _brief_complete(message: Any) -> bool:
    if not isinstance(message, str) or "Completion Brief" not in message:
        return False
    return all(field in message for field in COMPLETION_BRIEF_FIELDS)


def main() -> int:
    """Allow a valid terminal brief, or request at most one corrective continuation."""
    payload = _read_payload()
    if not _completion_ready(_workspace_root(payload)):
        print(json.dumps({"systemMessage": REMINDER}, sort_keys=True))
        return 0
    if _brief_complete(payload.get("last_assistant_message")):
        return 0
    if payload.get("stop_hook_active") is True:
        print(
            json.dumps(
                {"systemMessage": "Completion Brief is incomplete; continuation was already requested, so stop to avoid a loop."},
                sort_keys=True,
            )
        )
        return 0
    print(
        json.dumps(
            {
                "decision": "block",
                "reason": (
                    "Replace the draft with one terminal Completion Brief containing: "
                    + ", ".join(COMPLETION_BRIEF_FIELDS)
                    + " Do not call tools after that response."
                ),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
