from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


LIFECYCLE_STATE_REL = Path(".codex/product-agent-os/lifecycle-state.json")
TERMINAL_STATUSES = {"ready_for_completion_brief", "ready_for_completion_ledger", "blocked", "stopped_repair_required"}
WORKSPACE_ROOT_ENV = "CODEX_HOOK_WORKSPACE_ROOT"
REMINDER = (
    "Finish applicable verification and control-plane sync before closing. Use Task Start Brief / "
    "Completion Ledger for the configured packet scope; ordinary work may use concise results, evidence "
    "and limits. Report missing gates honestly. This reminder does not validate chat or prove completion."
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


def main() -> int:
    """Remind about open work; never reject a closing answer by its format."""
    payload = _read_payload()
    if payload.get("stop_hook_active") is True:
        return 0
    # The marker is workflow metadata, not proof that chat was delivered or reviewed.
    if not _completion_ready(_workspace_root(payload)):
        print(json.dumps({"systemMessage": REMINDER}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
