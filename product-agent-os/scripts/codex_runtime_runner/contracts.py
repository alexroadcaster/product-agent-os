from __future__ import annotations

from typing import Any


ALLOWED_RUNNER_STATUSES = ["route_ready", "needs_context", "needs_approval", "blocked", "completed", "failed"]
ALLOWED_RUNTIME_SURFACES = ["Codex App", "CLI", "IDE extension", "codex exec", "subagent", "skill"]
ALLOWED_WRITE_POLICIES = ["read_only", "staged_only", "approved_write", "blocked"]
ALLOWED_APPROVAL_STATUSES = ["not_required", "required", "approved", "rejected", "stale"]
ALLOWED_LIFECYCLE_STATES = [
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
REQUIRED_RESULT_FIELDS = [
    "schema_version",
    "status",
    "workspace",
    "lifecycle_state",
    "route_packet",
    "handoffs",
    "files_touched",
    "files_proposed",
    "verification_evidence",
    "source_policy_status",
    "approval_status",
    "redactions",
    "errors",
    "warnings",
    "next_action",
]


def validate_runner_request(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("schema_version") != 1:
        errors.append("schema_version:must_be_1")
    if not _non_empty_string(payload.get("workspace")):
        errors.append("workspace:required")

    task = payload.get("task")
    routing = payload.get("routing")
    approval = payload.get("approval")
    if not isinstance(task, dict):
        errors.append("task:required")
        task = {}
    if not isinstance(routing, dict):
        errors.append("routing:required")
        routing = {}
    if not isinstance(approval, dict):
        errors.append("approval:required")
        approval = {}

    state = task.get("lifecycle_state")
    if state not in ("", None) and state not in ALLOWED_LIFECYCLE_STATES:
        errors.append("task.lifecycle_state:unknown")
    for field in ["constraints", "allowed_sources", "expected_artifacts"]:
        if field in task and not isinstance(task[field], list):
            errors.append(f"task.{field}:invalid")

    surface = routing.get("preferred_surface")
    if surface not in ALLOWED_RUNTIME_SURFACES:
        errors.append("routing.preferred_surface:unknown")
    if not isinstance(routing.get("allow_subagents"), bool):
        errors.append("routing.allow_subagents:invalid")
    if not isinstance(routing.get("allow_workspace_writes"), bool):
        errors.append("routing.allow_workspace_writes:invalid")

    approval_status = approval.get("approval_status")
    if approval_status not in ALLOWED_APPROVAL_STATUSES:
        errors.append("approval.approval_status:unknown")
    if routing.get("allow_workspace_writes") and approval_status != "approved":
        errors.append("routing.allow_workspace_writes:approval_required")
    return errors


def build_result(
    *,
    status: str,
    workspace: str,
    lifecycle_state: str,
    route_packet: dict[str, Any],
    source_policy_status: str,
    approval_status: str,
    next_action: str,
    handoffs: list[dict[str, Any]] | None = None,
    files_touched: list[str] | None = None,
    files_proposed: list[str] | None = None,
    verification_evidence: list[str] | None = None,
    redactions: dict[str, Any] | None = None,
    errors: list[str] | None = None,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "status": status,
        "workspace": workspace,
        "lifecycle_state": lifecycle_state,
        "route_packet": route_packet,
        "handoffs": handoffs or [],
        "files_touched": files_touched or [],
        "files_proposed": files_proposed or [],
        "verification_evidence": verification_evidence or [],
        "source_policy_status": source_policy_status,
        "approval_status": approval_status,
        "redactions": redactions or {"count": 0, "categories": []},
        "errors": errors or [],
        "warnings": warnings or [],
        "next_action": next_action,
    }


def validate_runner_result(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if list(payload.keys()) != REQUIRED_RESULT_FIELDS:
        errors.append("result:field_order_or_shape")
    if payload.get("schema_version") != 1:
        errors.append("schema_version:must_be_1")
    if payload.get("status") not in ALLOWED_RUNNER_STATUSES:
        errors.append("status:unknown")
    if payload.get("lifecycle_state") not in ALLOWED_LIFECYCLE_STATES:
        errors.append("lifecycle_state:unknown")
    if not isinstance(payload.get("route_packet"), dict):
        errors.append("route_packet:invalid")

    for field in ["handoffs", "files_touched", "files_proposed", "verification_evidence", "errors", "warnings"]:
        if not isinstance(payload.get(field), list):
            errors.append(f"{field}:invalid")

    redactions = payload.get("redactions")
    if not isinstance(redactions, dict) or not isinstance(redactions.get("count"), int):
        errors.append("redactions:invalid")
    if payload.get("status") == "completed" and not payload.get("verification_evidence"):
        errors.append("verification_evidence:required_for_completed")
    return errors


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())
