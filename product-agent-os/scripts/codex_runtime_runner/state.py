from __future__ import annotations

from pathlib import Path
from typing import Any

from codex_runtime_runner.contracts import ALLOWED_LIFECYCLE_STATES


def infer_lifecycle_state(context: dict[str, Any], request: dict[str, Any]) -> str:
    requested = request.get("task", {}).get("lifecycle_state") if isinstance(request.get("task"), dict) else ""
    if requested in ALLOWED_LIFECYCLE_STATES:
        return str(requested)

    files = context.get("files", {})
    if not files.get("AGENTS.md", {}).get("exists"):
        return "uninitialized"

    requirements = files.get("REQUIREMENTS.md", {}).get("text", "")
    if not requirements or "Acceptance Criteria" not in requirements:
        return "infrastructure_planned"

    plan = files.get("PLAN.md", {}).get("text", "")
    if not plan or "Verification" not in plan:
        return "requirements_ready"

    if not _has_agent_config(context):
        return "plan_ready"

    test_text = files.get("TEST.md", {}).get("text", "")
    evals_text = files.get("EVALS.md", {}).get("text", "")
    if "Quality gates" not in test_text or "Quality gates" not in evals_text:
        return "team_ready"

    runlog = files.get("RUNLOG.md", {}).get("text", "")
    for state in ["build_active", "quality_gate", "review_ready", "release_ready", "learning_ready"]:
        if f"lifecycle_state: {state}" in runlog:
            return state
    return "maintenance"


def _has_agent_config(context: dict[str, Any]) -> bool:
    workspace = str(context.get("workspace", ""))
    if not workspace:
        return False
    return (Path(workspace) / ".codex" / "agents" / "builder.toml").exists()
