from __future__ import annotations

from pathlib import Path
import hashlib
import json
from typing import Any

from codex_runtime_runner.contracts import ALLOWED_LIFECYCLE_STATES
from product_agent_os.task_routing import TaskContextError, workspace_path


def resolve_task_state(context: dict[str, Any], task: dict[str, Any]) -> dict[str, Any]:
    """Separate structural observations from task-bound state; never infer from headings."""
    files = context.get("files", {})
    structural = {
        "present": sorted(name for name, entry in files.items() if entry.get("exists")),
        "missing": list(context.get("missing", [])),
        "custom_builder_present": _has_agent_config(context),
    }
    result = {
        "structural_readiness": structural,
        "task_state": None,
        "recommendation": "maintenance" if structural["present"] else "uninitialized",
        "provenance": "task_scope_recommendation_not_authoritative_state",
        "gaps": [],
    }
    state = task.get("state")
    if state is None:
        return result
    if not isinstance(state, dict) or set(state) != {"value", "source", "sha256"}:
        result["gaps"].append("Task state requires value, source and sha256")
        return result
    try:
        path = workspace_path(Path(context["workspace"]).resolve(), state["source"])
        if path.stat().st_size > 1024 * 1024:
            raise ValueError("state source too large")
        raw = path.read_bytes()
        record = json.loads(raw.decode("utf-8-sig"))
        valid = (
            state["value"] in ALLOWED_LIFECYCLE_STATES
            and isinstance(record, dict)
            and record.get("task_id") == task["task_id"]
            and record.get("lifecycle_state") == state["value"]
            and hashlib.sha256(raw).hexdigest() == state["sha256"]
        )
    except (OSError, ValueError, TypeError, TaskContextError):
        valid = False
    if not valid:
        result["gaps"].append("Task state is invalid, stale or belongs to another task")
        return result
    result.update(task_state=state["value"], recommendation=state["value"],
                  provenance={"source": state["source"], "sha256": state["sha256"],
                              "authority": "task_state_only_not_write_permission"})
    return result


def infer_lifecycle_state(context: dict[str, Any], request: dict[str, Any]) -> str:
    requested = request.get("task", {}).get("lifecycle_state") if isinstance(request.get("task"), dict) else ""
    if requested in ALLOWED_LIFECYCLE_STATES:
        return str(requested)

    files = context.get("files", {})
    if not files.get("AGENTS.md", {}).get("exists"):
        return "uninitialized"

    # Legacy headings/config presence are observations, never readiness proof.
    # Explicit requested routes above remain caller intent, not acceptance.
    task = request.get("task", {})
    if isinstance(task, dict) and task.get("task_id") and task.get("state"):
        return str(resolve_task_state(context, task)["recommendation"])
    return "maintenance"


def _has_agent_config(context: dict[str, Any]) -> bool:
    workspace = str(context.get("workspace", ""))
    if not workspace:
        return False
    return (Path(workspace) / ".codex" / "agents" / "builder.toml").exists()
