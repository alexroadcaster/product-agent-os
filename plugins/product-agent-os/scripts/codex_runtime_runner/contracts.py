from __future__ import annotations

import re
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
REQUIRED_METHODOLOGY_PACKET_KEYS = [
    "methodology_domains",
    "methodology_recommendations",
    "recommendation_groups",
    "questions_for_owner",
    "safe_next_action",
    "semantic_evidence_sufficiency",
    "source_artifact_ledger",
    "write_policy",
    "status",
]
METHODOLOGY_PACKET_LIMITS = {
    "methodology_domains": 12,
    "methodology_recommendations": 12,
    "recommendation_groups": 8,
    "questions_for_owner": 8,
    "source_artifact_ledger": 12,
}
DETECTION_ONLY_METHODOLOGY_STATUSES = {
    "applicable_missing",
    "evidence_required",
    "present_unverified",
}
APPROVAL_BOUND_ACTION_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bpublish(?:ing)?\b",
        r"\bdeploy(?:ing|ment)?\b",
        r"\btag\b",
        r"\brelease[_ -]?create\b",
        r"\brelease creation\b",
        r"\bcreate (?:a )?release\b",
        r"\bpr/push\b",
        r"\bpull request\b",
        r"\bpush(?:ing)?\b",
        r"\bpackage registry\b",
        r"\bregistry mutation\b",
        r"\bmarketplace\b",
        r"\bstore submission\b",
        r"\bsecurity scan\b",
        r"\bproduction data\b",
        r"\bproduction db\b",
        r"\bdb migration\b",
        r"\bdatabase migration\b",
        r"\bexternal-system mutation\b",
        r"\bexternal system mutation\b",
        r"\bexternal write\b",
    ]
]
AUTOMATION_ACTION_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bautomation\b",
        r"\bautomation-promoter\b",
        r"\bautomation-candidate\.md\b",
    ]
]
AUTOMATION_MATURITY_EVIDENCE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\btwo manual runs\b",
        r"\bmanual stability evidence\b",
        r"\bworkflow value evidence\b",
        r"\bmaturity evidence\b",
        r"\bmanual run evidence\b",
    ]
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


def build_methodology_packet(methodology_intelligence: dict[str, Any] | None = None) -> dict[str, Any]:
    intelligence = methodology_intelligence if isinstance(methodology_intelligence, dict) else {}
    synthesis = intelligence.get("methodology_synthesis")
    if not isinstance(synthesis, dict):
        synthesis = {}

    safe_next_action = (
        _non_empty_or_empty(intelligence.get("safe_next_action"))
        or _non_empty_or_empty(synthesis.get("safe_next_action"))
        or "Record methodology synthesis output and proceed only with evidence-backed planning."
    )
    questions = intelligence.get("questions_for_owner")
    if not isinstance(questions, list):
        questions = synthesis.get("owner_questions", [])
    semantic_evidence = synthesis.get(
        "semantic_evidence_sufficiency",
        intelligence.get("semantic_evidence_sufficiency", {}),
    )
    if not isinstance(semantic_evidence, dict):
        semantic_evidence = {}

    return {
        "methodology_domains": _bounded_list(
            intelligence.get("methodology_domains", []),
            METHODOLOGY_PACKET_LIMITS["methodology_domains"],
        ),
        "methodology_recommendations": _bounded_list(
            intelligence.get("recommendations", []),
            METHODOLOGY_PACKET_LIMITS["methodology_recommendations"],
        ),
        "recommendation_groups": _bounded_list(
            intelligence.get("recommendation_groups", synthesis.get("recommendation_groups", [])),
            METHODOLOGY_PACKET_LIMITS["recommendation_groups"],
        ),
        "questions_for_owner": _bounded_list(
            questions,
            METHODOLOGY_PACKET_LIMITS["questions_for_owner"],
        ),
        "safe_next_action": safe_next_action,
        "semantic_evidence_sufficiency": semantic_evidence,
        "source_artifact_ledger": _bounded_list(
            synthesis.get("source_artifact_ledger", intelligence.get("source_artifact_ledger", [])),
            METHODOLOGY_PACKET_LIMITS["source_artifact_ledger"],
        ),
        "write_policy": "read_only",
        "status": _methodology_packet_status(intelligence),
    }


def validate_methodology_packet(packet: Any) -> list[str]:
    if not isinstance(packet, dict):
        return ["methodology_packet:invalid"]

    errors: list[str] = []
    keys = set(packet.keys())
    for key in REQUIRED_METHODOLOGY_PACKET_KEYS:
        if key not in keys:
            errors.append(f"methodology_packet.{key}:required")
    for key in sorted(keys - set(REQUIRED_METHODOLOGY_PACKET_KEYS)):
        errors.append(f"methodology_packet.{key}:unknown")

    for key, limit in METHODOLOGY_PACKET_LIMITS.items():
        value = packet.get(key)
        if not isinstance(value, list):
            errors.append(f"methodology_packet.{key}:invalid")
        elif len(value) > limit:
            errors.append(f"methodology_packet.{key}:too_many")

    if not _non_empty_string(packet.get("safe_next_action")):
        errors.append("methodology_packet.safe_next_action:invalid")
    if not isinstance(packet.get("semantic_evidence_sufficiency"), dict):
        errors.append("methodology_packet.semantic_evidence_sufficiency:invalid")
    if packet.get("write_policy") != "read_only":
        errors.append("methodology_packet.write_policy:must_be_read_only")
    if not _non_empty_string(packet.get("status")):
        errors.append("methodology_packet.status:invalid")
    return errors


def methodology_requires_approval(packet: dict[str, Any]) -> bool:
    return _matches_any(_methodology_action_text(packet), APPROVAL_BOUND_ACTION_PATTERNS)


def methodology_requires_automation_maturity(packet: dict[str, Any]) -> bool:
    text = _methodology_action_text(packet)
    return _matches_any(text, AUTOMATION_ACTION_PATTERNS) and not _matches_any(
        text,
        AUTOMATION_MATURITY_EVIDENCE_PATTERNS,
    )


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
        route_packet = {}
    else:
        route_packet = payload["route_packet"]
        if "methodology_packet" in route_packet:
            errors.extend(validate_methodology_packet(route_packet["methodology_packet"]))

    for field in ["handoffs", "files_touched", "files_proposed", "verification_evidence", "errors", "warnings"]:
        if not isinstance(payload.get(field), list):
            errors.append(f"{field}:invalid")

    redactions = payload.get("redactions")
    if not isinstance(redactions, dict) or not isinstance(redactions.get("count"), int):
        errors.append("redactions:invalid")
    if payload.get("status") == "completed" and not payload.get("verification_evidence"):
        errors.append("verification_evidence:required_for_completed")
        methodology_packet = route_packet.get("methodology_packet")
        if isinstance(methodology_packet, dict) and methodology_packet.get("status") in DETECTION_ONLY_METHODOLOGY_STATUSES:
            errors.append("methodology_packet:detection_not_completion")
    return errors


def _bounded_list(value: Any, limit: int) -> list[Any]:
    if not isinstance(value, list):
        return []
    return value[:limit]


def _methodology_packet_status(intelligence: dict[str, Any]) -> str:
    status = intelligence.get("status")
    if _non_empty_string(status):
        return str(status)
    return "not_applicable"


def _non_empty_or_empty(value: Any) -> str:
    return str(value).strip() if _non_empty_string(value) else ""


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _methodology_action_text(packet: dict[str, Any]) -> str:
    texts: list[str] = []
    if _non_empty_string(packet.get("safe_next_action")):
        texts.append(str(packet["safe_next_action"]))
    for collection_name in ("methodology_recommendations", "recommendation_groups"):
        collection = packet.get(collection_name, [])
        if not isinstance(collection, list):
            continue
        for item in collection:
            if not isinstance(item, dict):
                continue
            for key in ("artifact", "safe_next_action", "next_action", "action"):
                value = item.get(key)
                if _non_empty_string(value):
                    texts.append(str(value))
    return "\n".join(texts)


def _matches_any(text: str, patterns: list[re.Pattern[str]]) -> bool:
    return any(pattern.search(text) for pattern in patterns)
