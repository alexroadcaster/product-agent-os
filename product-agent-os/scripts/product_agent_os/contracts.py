from __future__ import annotations

from typing import Any


LIFECYCLE_STATES = [
    "uninitialized",
    "infrastructure_planned",
    "requirements_ready",
    "plan_ready",
    "team_ready",
    "build_active",
    "quality_gate",
    "review_ready",
    "release_ready",
    "learning_ready",
    "maintenance",
]

COMPLEXITY_PROFILES = [
    "guided-small",
    "standard-product",
    "production-team",
    "ai-product",
    "enterprise-governed",
    "autonomous-maintenance",
]

CONTROL_PLANE_FILES = [
    "AGENTS.md",
    "REQUIREMENTS.md",
    "PLAN.md",
    "TEST.md",
    "EVALS.md",
    "RUNLOG.md",
]

REQUIRED_HANDOFF_FIELDS = [
    "lifecycle_state",
    "goal",
    "constraints",
    "allowed_sources",
    "inputs_used",
    "verified_claims",
    "unsupported_claims",
    "files_touched",
    "files_proposed",
    "commands_run",
    "verification_evidence",
    "risks",
    "next_agent_task",
    "stop_reason",
]


def validate_handoff(payload: dict[str, Any]) -> list[str]:
    """Return missing or invalid handoff fields."""
    missing: list[str] = []
    for field in REQUIRED_HANDOFF_FIELDS:
        if field not in payload:
            missing.append(field)

    state = payload.get("lifecycle_state")
    if state is not None and (not isinstance(state, str) or not state.strip()):
        missing.append("lifecycle_state:empty")
    elif state is not None and state not in LIFECYCLE_STATES:
        missing.append("lifecycle_state:unknown")

    goal = payload.get("goal")
    if goal is not None and (not isinstance(goal, str) or not goal.strip()):
        missing.append("goal:empty")

    for field in [
        "allowed_sources",
        "inputs_used",
        "verified_claims",
        "unsupported_claims",
        "commands_run",
        "risks",
    ]:
        value = payload.get(field)
        if value is not None and not isinstance(value, list):
            missing.append(f"{field}:invalid")

    for field in ["constraints", "verification_evidence"]:
        value = payload.get(field)
        if value is not None and not isinstance(value, list):
            missing.append(f"{field}:invalid")
        elif value is not None and not value:
            missing.append(f"{field}:empty")

    files_touched = payload.get("files_touched")
    files_proposed = payload.get("files_proposed")
    for field, value in [
        ("files_touched", files_touched),
        ("files_proposed", files_proposed),
    ]:
        if value is not None and not isinstance(value, list):
            missing.append(f"{field}:invalid")

    if (
        isinstance(files_touched, list)
        and isinstance(files_proposed, list)
        and not files_touched
        and not files_proposed
    ):
        missing.append("files:empty")

    for field in ["next_agent_task", "stop_reason"]:
        value = payload.get(field)
        if value is not None and not isinstance(value, str):
            missing.append(f"{field}:invalid")

    return missing
