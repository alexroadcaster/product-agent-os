from __future__ import annotations

import json
import re
from typing import Any

from codex_runtime_runner.redaction import validate_redaction
from product_agent_os.question_protocol import (
    MAX_TOTAL_QUESTIONS,
    QUESTION_ANSWER_TYPES,
    QUESTION_CATEGORIES,
    QUESTION_PRIORITIES,
)
from product_agent_os.doubt_verification import validate_completion_skeptic_recommendation_packet


ALLOWED_RUNNER_STATUSES = ["route_ready", "needs_context", "needs_approval", "blocked", "completed", "failed"]
ALLOWED_RUNTIME_SURFACES = ["Codex App", "CLI", "IDE extension", "codex exec", "subagent", "skill"]
ALLOWED_WRITE_POLICIES = ["read_only", "staged_only", "approved_write", "blocked"]
ALLOWED_APPROVAL_STATUSES = ["not_required", "required", "approved", "rejected", "stale"]
ALLOWED_FINISH_OPTIONS = [
    "read_only_audit",
    "ask_owner",
    "stage_proposal",
    "stage_metrics_report",
    "request_owner_review",
    "block_automation_promotion",
    "keep_current",
    "investigate_regression",
    "request_approval",
    "run_verification",
    "stop_blocked",
]
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
QUESTION_QUEUE_LIMITS = {
    "questions": MAX_TOTAL_QUESTIONS,
}
AGENT_SKILL_METRICS_LOOP_LIMITS = {
    "report_refs": 4,
    "top_candidates": 5,
}
PROJECT_GRAPH_STATUS_LIMITS = {
    "artifact_refs": 4,
    "top_gaps": 5,
    "unsupported_languages": 8,
}
DETECTION_ONLY_METHODOLOGY_STATUSES = {
    "applicable_missing",
    "evidence_required",
    "present_unverified",
}
METHODOLOGY_HIGH_RISK_ACTIONS = [
    "live_runtime",
    "browser_automation",
    "provider_api_call",
    "git_action",
    "publish",
    "deploy",
    "tag",
    "release_create",
    "pr_or_push",
    "package_registry_mutation",
    "marketplace_submission",
    "security_scan",
    "production_data_access",
    "db_migration",
    "automation_activation",
    "external_system_mutation",
]
HIGH_RISK_ACTION_PATTERNS = {
    "live_runtime": [
        re.compile(r"\blive server\b", re.IGNORECASE),
        re.compile(r"\bstart (?:a )?(?:dev |local )?server\b", re.IGNORECASE),
        re.compile(r"\brun(?:ning)? (?:the )?(?:app|runtime|server)\b", re.IGNORECASE),
        re.compile(r"\bruntime execution\b", re.IGNORECASE),
    ],
    "browser_automation": [
        re.compile(r"\bbrowser automation\b", re.IGNORECASE),
        re.compile(r"\bplaywright\b", re.IGNORECASE),
        re.compile(r"\bselenium\b", re.IGNORECASE),
        re.compile(r"\bin-app browser\b", re.IGNORECASE),
    ],
    "provider_api_call": [
        re.compile(r"\bprovider api\b", re.IGNORECASE),
        re.compile(r"\bapi call\b", re.IGNORECASE),
        re.compile(r"\bmodel call\b", re.IGNORECASE),
        re.compile(r"\bexternal provider\b", re.IGNORECASE),
        re.compile(r"\bcall provider\b", re.IGNORECASE),
    ],
    "git_action": [
        re.compile(r"\bgit (?:push|commit|tag|checkout|merge|rebase|reset)\b", re.IGNORECASE),
        re.compile(r"\bcreate (?:a )?branch\b", re.IGNORECASE),
        re.compile(r"\bstage files\b", re.IGNORECASE),
    ],
    "publish": [re.compile(r"\bpublish(?:ing)?\b", re.IGNORECASE)],
    "deploy": [re.compile(r"\bdeploy(?:ing|ed)?\b", re.IGNORECASE)],
    "tag": [re.compile(r"\btag\b", re.IGNORECASE)],
    "release_create": [
        re.compile(r"\brelease[_ -]?create\b", re.IGNORECASE),
        re.compile(r"\brelease creation\b", re.IGNORECASE),
        re.compile(r"\bcreate (?:a )?release\b", re.IGNORECASE),
    ],
    "pr_or_push": [
        re.compile(r"\bpr/push\b", re.IGNORECASE),
        re.compile(r"\bpull request\b", re.IGNORECASE),
        re.compile(r"\bpush(?:ing)?\b", re.IGNORECASE),
    ],
    "package_registry_mutation": [
        re.compile(r"\bpackage registry\b", re.IGNORECASE),
        re.compile(r"\bregistry mutation\b", re.IGNORECASE),
    ],
    "marketplace_submission": [
        re.compile(r"\bmarketplace\b", re.IGNORECASE),
        re.compile(r"\bstore submission\b", re.IGNORECASE),
    ],
    "security_scan": [re.compile(r"\bsecurity scan\b", re.IGNORECASE)],
    "production_data_access": [
        re.compile(r"\bproduction data\b", re.IGNORECASE),
        re.compile(r"\bproduction db\b", re.IGNORECASE),
    ],
    "db_migration": [
        re.compile(r"\bdb migration\b", re.IGNORECASE),
        re.compile(r"\bdatabase migration\b", re.IGNORECASE),
    ],
    "automation_activation": [
        re.compile(r"\bactive automation\b", re.IGNORECASE),
        re.compile(r"\bactivate automation\b", re.IGNORECASE),
        re.compile(r"\bscheduled automation\b", re.IGNORECASE),
    ],
    "external_system_mutation": [
        re.compile(r"\bexternal-system mutation\b", re.IGNORECASE),
        re.compile(r"\bexternal system mutation\b", re.IGNORECASE),
        re.compile(r"\bexternal write\b", re.IGNORECASE),
    ],
}
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
    return bool(classify_methodology_high_risk_actions(packet))


def classify_methodology_high_risk_actions(packet: dict[str, Any]) -> list[str]:
    text = _methodology_action_text(packet)
    return [
        action
        for action in METHODOLOGY_HIGH_RISK_ACTIONS
        if _matches_any(text, HIGH_RISK_ACTION_PATTERNS[action])
    ]


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
        if "finish_options" in route_packet:
            errors.extend(_validate_finish_options(route_packet["finish_options"], "route_packet.finish_options"))
        if "question_queue" in route_packet:
            errors.extend(validate_question_queue(route_packet["question_queue"], "route_packet.question_queue"))
        if "status_snapshot_ref" in route_packet:
            errors.extend(_validate_status_snapshot_ref(route_packet["status_snapshot_ref"]))
        if "agent_skill_metrics_loop" in route_packet:
            errors.extend(validate_agent_skill_metrics_loop_packet(route_packet["agent_skill_metrics_loop"]))
        if "project_graph_status" in route_packet:
            errors.extend(validate_project_graph_status_packet(route_packet["project_graph_status"]))
        if "completion_skeptic_recommendation" in route_packet:
            errors.extend(
                validate_completion_skeptic_recommendation_packet(
                    route_packet["completion_skeptic_recommendation"]
                )
            )
        first_response = route_packet.get("first_response_contract")
        if first_response is not None:
            if not isinstance(first_response, dict):
                errors.append("route_packet.first_response_contract:invalid")
            elif "finish_options" in first_response:
                errors.extend(
                    _validate_finish_options(
                        first_response["finish_options"],
                        "route_packet.first_response_contract.finish_options",
                    )
                )
            if isinstance(first_response, dict):
                if "questions" in first_response:
                    errors.append("route_packet.first_response_contract.questions:forbidden")
                if "question_queue" in route_packet:
                    for field in ["next_blocking_question", "question_counts", "question_summary"]:
                        if field not in first_response:
                            errors.append(f"route_packet.first_response_contract.{field}:required")

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


def validate_project_graph_status_packet(packet: Any) -> list[str]:
    if not isinstance(packet, dict):
        return ["project_graph_status:invalid"]
    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("project_graph_status.schema_version:must_be_1")
    if packet.get("write_policy") != "read_only":
        errors.append("project_graph_status.write_policy:must_be_read_only")
    if packet.get("status") not in {"current", "stale", "ambiguous", "unsupported", "not_available"}:
        errors.append("project_graph_status.status:invalid")
    if packet.get("source_policy") != "generated graph is not source of truth":
        errors.append("project_graph_status.source_policy:invalid")
    for field in ["freshness", "counts"]:
        if not isinstance(packet.get(field), dict):
            errors.append(f"project_graph_status.{field}:invalid")
    if not _non_empty_string(packet.get("safe_next_action")):
        errors.append("project_graph_status.safe_next_action:required")

    artifact_refs = packet.get("artifact_refs")
    if not isinstance(artifact_refs, list):
        errors.append("project_graph_status.artifact_refs:invalid")
        artifact_refs = []
    elif len(artifact_refs) > PROJECT_GRAPH_STATUS_LIMITS["artifact_refs"]:
        errors.append("project_graph_status.artifact_refs:too_many")
    errors.extend(_validate_project_graph_refs(artifact_refs, "project_graph_status.artifact_refs"))

    analysis_ref = packet.get("analysis_ref")
    if analysis_ref not in (None, ""):
        if not isinstance(analysis_ref, dict):
            errors.append("project_graph_status.analysis_ref:invalid")
        else:
            errors.extend(_validate_project_graph_refs([analysis_ref], "project_graph_status.analysis_ref"))

    unsupported_languages = packet.get("unsupported_languages")
    if not isinstance(unsupported_languages, list):
        errors.append("project_graph_status.unsupported_languages:invalid")
    elif len(unsupported_languages) > PROJECT_GRAPH_STATUS_LIMITS["unsupported_languages"]:
        errors.append("project_graph_status.unsupported_languages:too_many")
    if isinstance(unsupported_languages, list):
        errors.extend(_validate_project_graph_unsupported_languages(unsupported_languages))

    top_gaps = packet.get("top_gaps")
    if not isinstance(top_gaps, list):
        errors.append("project_graph_status.top_gaps:invalid")
    elif len(top_gaps) > PROJECT_GRAPH_STATUS_LIMITS["top_gaps"]:
        errors.append("project_graph_status.top_gaps:too_many")

    rendered = json.dumps(packet, sort_keys=True)
    if validate_redaction(rendered) or re.search(r"[A-Za-z]:[/\\]Users[/\\]", rendered):
        errors.append("project_graph_status:contains_local_path")
    return errors


def validate_agent_skill_metrics_loop_packet(packet: Any) -> list[str]:
    if not isinstance(packet, dict):
        return ["agent_skill_metrics_loop:invalid"]
    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("agent_skill_metrics_loop.schema_version:must_be_1")
    if packet.get("write_policy") != "read_only":
        errors.append("agent_skill_metrics_loop.write_policy:must_be_read_only")
    if not _non_empty_string(packet.get("status")):
        errors.append("agent_skill_metrics_loop.status:required")

    summary = packet.get("summary")
    if not isinstance(summary, dict):
        errors.append("agent_skill_metrics_loop.summary:invalid")
    report_refs = packet.get("report_refs")
    if not isinstance(report_refs, list):
        errors.append("agent_skill_metrics_loop.report_refs:invalid")
        report_refs = []
    elif len(report_refs) > AGENT_SKILL_METRICS_LOOP_LIMITS["report_refs"]:
        errors.append("agent_skill_metrics_loop.report_refs:too_many")
    for index, ref in enumerate(report_refs):
        if not isinstance(ref, dict):
            errors.append(f"agent_skill_metrics_loop.report_refs[{index}]:invalid")
            continue
        if ref.get("kind") == "external_ref":
            errors.append(f"agent_skill_metrics_loop.report_refs[{index}].kind:forbidden_external_ref")
        if not _non_empty_string(ref.get("path")):
            errors.append(f"agent_skill_metrics_loop.report_refs[{index}].path:required")
        path = str(ref.get("path", ""))
        if path.startswith(("http://", "https://")):
            errors.append(f"agent_skill_metrics_loop.report_refs[{index}].path:external_url_forbidden")

    candidate_summary = packet.get("update_candidate_summary")
    if not isinstance(candidate_summary, dict):
        errors.append("agent_skill_metrics_loop.update_candidate_summary:invalid")
        candidate_summary = {}
    top_candidates = candidate_summary.get("top_candidates")
    if not isinstance(top_candidates, list):
        top_candidates = []
    elif len(top_candidates) > AGENT_SKILL_METRICS_LOOP_LIMITS["top_candidates"]:
        errors.append("agent_skill_metrics_loop.update_candidate_summary.top_candidates:too_many")
    for index, candidate in enumerate(top_candidates):
        if not isinstance(candidate, dict):
            errors.append(f"agent_skill_metrics_loop.update_candidate_summary.top_candidates[{index}]:invalid")
            continue
        action = str(candidate.get("action", "")).lower()
        if action in {"apply", "apply_patch", "self_apply", "activate_automation"}:
            errors.append(
                f"agent_skill_metrics_loop.update_candidate_summary.top_candidates[{index}].action:apply_forbidden"
            )
        if candidate.get("requires_rollback") is not True:
            errors.append(
                f"agent_skill_metrics_loop.update_candidate_summary.top_candidates[{index}].requires_rollback:required"
            )
    if packet.get("automation_policy") not in {"candidate_only", "blocked", "not_applicable"}:
        errors.append("agent_skill_metrics_loop.automation_policy:invalid")
    if packet.get("source_policy") != "generated summaries are not source of truth":
        errors.append("agent_skill_metrics_loop.source_policy:invalid")
    return errors


def _validate_project_graph_refs(refs: list[Any], prefix: str) -> list[str]:
    errors: list[str] = []
    for index, ref in enumerate(refs):
        item_prefix = f"{prefix}[{index}]" if prefix.endswith("refs") else prefix
        if not isinstance(ref, dict):
            errors.append(f"{item_prefix}:invalid")
            continue
        if ref.get("kind") == "external_ref":
            errors.append(f"{item_prefix}.kind:forbidden_external_ref")
        kind = ref.get("kind")
        if kind not in {"staged_artifact", "not_available", "generated_artifact", "report"}:
            errors.append(f"{item_prefix}.kind:unknown")
        path = str(ref.get("path") or "")
        if kind != "not_available" and not path:
            errors.append(f"{item_prefix}.path:required")
        if path.startswith(("http://", "https://")):
            errors.append(f"{item_prefix}.path:external_url_forbidden")
        if path and kind != "not_available" and not _safe_project_graph_relative_path(path):
            errors.append(f"{item_prefix}.path:absolute_or_unsafe")
    return errors


def _validate_project_graph_unsupported_languages(items: list[Any]) -> list[str]:
    errors: list[str] = []
    allowed_keys = {"language", "file_count", "status"}
    allowed_statuses = {"file_only", "unsupported", "structured_overlay_pending", "supported", "unknown"}
    for index, item in enumerate(items):
        prefix = f"project_graph_status.unsupported_languages[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}:invalid")
            continue
        for key in sorted(set(item.keys()) - allowed_keys):
            errors.append(f"{prefix}.{key}:unknown")
        if not _non_empty_string(item.get("language")):
            errors.append(f"{prefix}.language:required")
        if item.get("status") not in allowed_statuses:
            errors.append(f"{prefix}.status:invalid")
        try:
            file_count = int(item.get("file_count"))
        except (TypeError, ValueError):
            errors.append(f"{prefix}.file_count:invalid")
        else:
            if file_count < 0:
                errors.append(f"{prefix}.file_count:invalid")
    return errors


def _safe_project_graph_relative_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    if not normalized:
        return False
    if normalized.startswith(("/", "../", "~")):
        return False
    if ":/" in normalized:
        return False
    return ".." not in normalized.split("/")


def validate_question_queue(packet: Any, prefix: str = "question_queue") -> list[str]:
    if not isinstance(packet, dict):
        return [f"{prefix}:invalid"]
    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append(f"{prefix}.schema_version:must_be_1")
    if packet.get("write_policy") != "read_only":
        errors.append(f"{prefix}.write_policy:must_be_read_only")
    questions = packet.get("questions")
    if not isinstance(questions, list):
        errors.append(f"{prefix}.questions:invalid")
        questions = []
    elif len(questions) > QUESTION_QUEUE_LIMITS["questions"]:
        errors.append(f"{prefix}.questions:too_many")
    for index, question in enumerate(questions):
        if not isinstance(question, dict):
            errors.append(f"{prefix}.questions[{index}]:invalid")
            continue
        if not _non_empty_string(question.get("id")):
            errors.append(f"{prefix}.questions[{index}].id:required")
        if not _non_empty_string(question.get("text")):
            errors.append(f"{prefix}.questions[{index}].text:required")
        if question.get("priority") not in QUESTION_PRIORITIES:
            errors.append(f"{prefix}.questions[{index}].priority:unknown")
        if question.get("category") not in QUESTION_CATEGORIES:
            errors.append(f"{prefix}.questions[{index}].category:unknown")
        if question.get("answer_type") not in QUESTION_ANSWER_TYPES:
            errors.append(f"{prefix}.questions[{index}].answer_type:unknown")
        source = question.get("source")
        if not isinstance(source, dict) or not _non_empty_string(source.get("kind")) or not _non_empty_string(source.get("key")):
            errors.append(f"{prefix}.questions[{index}].source:invalid")
    next_blocking = packet.get("next_blocking_question")
    if next_blocking is not None and not isinstance(next_blocking, dict):
        errors.append(f"{prefix}.next_blocking_question:invalid")
    if not isinstance(packet.get("summary"), dict):
        errors.append(f"{prefix}.summary:invalid")
    return errors


def methodology_owner_domains(packet: dict[str, Any]) -> list[str]:
    owner_domains: list[str] = []
    for group in packet.get("recommendation_groups", []):
        if isinstance(group, dict) and _non_empty_string(group.get("owner_domain")):
            owner_domains.append(str(group["owner_domain"]))
    return owner_domains


def methodology_has_ownership_conflict(packet: dict[str, Any]) -> bool:
    owner_domains = {domain for domain in methodology_owner_domains(packet) if domain}
    if len(owner_domains) > 1:
        return True

    artifact_owners: dict[str, set[str]] = {}
    for group in packet.get("recommendation_groups", []):
        if not isinstance(group, dict):
            continue
        artifact = str(group.get("artifact", "")).strip()
        owner = str(group.get("owner_domain", "")).strip()
        if artifact and owner:
            artifact_owners.setdefault(artifact, set()).add(owner)
    return any(len(owners) > 1 for owners in artifact_owners.values())


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


def _validate_finish_options(value: Any, prefix: str) -> list[str]:
    if not isinstance(value, list):
        return [f"{prefix}:invalid"]
    errors: list[str] = []
    for item in value:
        if item not in ALLOWED_FINISH_OPTIONS:
            errors.append(f"{prefix}:unknown")
    return errors


def _validate_status_snapshot_ref(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["route_packet.status_snapshot_ref:invalid"]
    errors: list[str] = []
    if value.get("kind") not in {"staged_artifact", "external_ref", "not_available"}:
        errors.append("route_packet.status_snapshot_ref.kind:unknown")
    if value.get("kind") != "not_available" and not _non_empty_string(value.get("path")):
        errors.append("route_packet.status_snapshot_ref.path:required")
    digest = value.get("digest")
    if digest not in ("", None) and not _non_empty_string(digest):
        errors.append("route_packet.status_snapshot_ref.digest:invalid")
    return errors
