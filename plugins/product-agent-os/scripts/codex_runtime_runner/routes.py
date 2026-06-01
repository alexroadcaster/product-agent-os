from __future__ import annotations

from copy import deepcopy
from typing import Any

from codex_runtime_runner.contracts import (
    build_methodology_packet,
    methodology_has_ownership_conflict,
    methodology_requires_approval,
    methodology_requires_automation_maturity,
)
from product_agent_os.question_protocol import build_question_queue


ROUTES = {
    "uninitialized": ("workspace-discovery-auditor", "", "read_only", "Audit workspace readiness."),
    "infrastructure_planned": ("requirements-author", "", "staged_only", "Draft requirements packet."),
    "requirements_ready": ("implementation-planner", "", "staged_only", "Draft implementation plan."),
    "plan_ready": ("agent-team-designer", "", "staged_only", "Design ownership and handoffs."),
    "team_ready": ("test-eval-designer", "", "staged_only", "Define quality gates."),
    "build_active": ("", "builder", "approved_write", "Execute one approved build slice."),
    "quality_gate": ("risk-reviewer", "", "read_only", "Review risks and verification evidence."),
    "review_ready": ("pr-release-operator", "", "staged_only", "Prepare PR or release packet."),
    "release_ready": ("learning-loop-maintainer", "", "staged_only", "Capture learnings and failures."),
    "learning_ready": ("automation-promoter", "", "staged_only", "Evaluate candidate-only automation."),
    "maintenance": ("project-lifecycle-orchestrator", "", "read_only", "Route maintenance work."),
}


def plan_route(
    lifecycle_state: str,
    *,
    allow_subagents: bool,
    usage_mode: dict[str, Any] | None = None,
    behavioral_route_inputs: dict[str, Any] | None = None,
    methodology_intelligence: dict[str, Any] | None = None,
    question_queue: dict[str, Any] | None = None,
    status_snapshot_ref: dict[str, Any] | None = None,
    agent_skill_metrics_loop: dict[str, Any] | None = None,
    project_graph_status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    skill, subagent, write_policy, action = ROUTES[lifecycle_state]
    if subagent and not allow_subagents:
        skill = "project-lifecycle-orchestrator"
        subagent = ""
    approval_requirements = ["explicit approval record required before workspace writes"] if write_policy == "approved_write" else []
    usage_mode = usage_mode or _default_usage_mode()
    methodology_packet = build_methodology_packet(methodology_intelligence)
    question_queue = question_queue or _question_queue_from_methodology(
        methodology_intelligence,
        usage_mode,
        agent_skill_metrics_loop=agent_skill_metrics_loop,
    )
    methodology_approval_required = methodology_requires_approval(methodology_packet)
    automation_maturity_required = (
        lifecycle_state == "learning_ready"
        and methodology_requires_automation_maturity(methodology_packet)
    )
    ownership_parallelism_required = bool(subagent) and methodology_has_ownership_conflict(methodology_packet)
    if automation_maturity_required:
        skill = "learning-loop-maintainer"
        subagent = ""
        action = "Record manual stability and workflow value evidence before automation promotion."
    if ownership_parallelism_required:
        skill = "agent-team-designer"
        subagent = ""
        write_policy = "staged_only"
        action = "Resolve methodology ownership and fresh-context handoff before parallel build work."
    if methodology_approval_required:
        approval_requirements.append("explicit approval required before methodology-recommended external or irreversible action")
    if automation_maturity_required:
        approval_requirements.append("manual stability and workflow value evidence required before automation promotion")
    if ownership_parallelism_required:
        approval_requirements.append("fresh-context handoff and explicit file/artifact ownership required before parallel work")
    graph_blocks_readiness = _project_graph_blocks_readiness(project_graph_status)
    if graph_blocks_readiness:
        action = "Read source files before acting on stale, ambiguous, or unsupported project graph output."
    finish_options = _finish_options(
        write_policy,
        methodology_approval_required=methodology_approval_required,
        automation_maturity_required=automation_maturity_required,
        agent_skill_metrics_loop=agent_skill_metrics_loop,
    )
    route = {
        "lifecycle_state": lifecycle_state,
        "next_action": action,
        "recommended_skill": skill,
        "recommended_subagent_role": subagent,
        "runtime_surface": "subagent" if subagent else "skill",
        "write_policy": write_policy,
        "required_inputs": ["AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"],
        "expected_outputs": ["codex_runner_result", "handoff packet"],
        "verification": [
            'python -m unittest discover -s tests -p "test_*.py" -v',
            "python plugins\\product-agent-os\\scripts\\run_fixture_eval.py",
        ],
        "approval_requirements": approval_requirements,
        "stop_conditions": [
            "missing required control-plane context",
            "blocked source policy",
            "missing approval for approved_write route",
            "active automation request",
            "methodology action requires explicit approval",
            "automation promotion requires maturity evidence",
            "parallel work requires fresh-context handoff and explicit ownership",
            "metrics loop reports are staged evidence only",
            "project code graph is generated orientation evidence only",
        ],
    }
    if ownership_parallelism_required:
        route["required_inputs"].append("fresh_context_handoff")
        route["ownership_parallelism_guard"] = "fresh_context_handoff_required"
    route["usage_mode"] = usage_mode
    route["behavioral_route_inputs"] = behavioral_route_inputs or _default_behavioral_route_inputs()
    route["methodology_packet"] = methodology_packet
    route["question_queue"] = question_queue
    if status_snapshot_ref is not None:
        route["status_snapshot_ref"] = status_snapshot_ref
    if agent_skill_metrics_loop is not None:
        route["agent_skill_metrics_loop"] = agent_skill_metrics_loop
        route["expected_outputs"].append("staged metrics report")
        route["approval_requirements"].append(
            "owner review required before metrics-loop modernization, schedule activation or external eval calls"
        )
    if project_graph_status is not None:
        route["project_graph_status"] = project_graph_status
        route["expected_outputs"].append("project graph status packet")
        if graph_blocks_readiness:
            route["approval_requirements"].append("source file confirmation required before graph-backed readiness or impact claims")
    route["finish_options"] = finish_options
    evidence_gaps = _evidence_gaps(methodology_packet)
    if graph_blocks_readiness:
        evidence_gaps.append("source file confirmation for stale or ambiguous project graph")
    route["first_response_contract"] = {
        "mode": usage_mode["primary"],
        "confidence": usage_mode["confidence"],
        "next_smallest_action": action,
        "next_blocking_question": question_queue.get("next_blocking_question"),
        "question_counts": question_queue.get("summary", {}),
        "question_summary": _question_summary(question_queue),
        "safe_next_action": methodology_packet["safe_next_action"],
        "required_fields": usage_mode["first_response_contract"],
        "minimum_artifacts": usage_mode["minimum_artifacts"],
        "evidence_gaps": evidence_gaps,
        "approval_boundary": write_policy,
        "finish_options": finish_options,
    }
    if project_graph_status is not None:
        route["first_response_contract"]["project_graph_summary"] = _project_graph_summary(project_graph_status)
    return route


def apply_runner_status_to_route(route: dict[str, Any], status: str) -> dict[str, Any]:
    updated = deepcopy(route)
    finish_options = _finish_options_for_status(status, updated.get("finish_options", []))
    updated["finish_options"] = finish_options
    if status in STATUS_NEXT_ACTIONS:
        updated["next_action"] = STATUS_NEXT_ACTIONS[status]
        if isinstance(updated.get("first_response_contract"), dict):
            updated["first_response_contract"]["next_smallest_action"] = STATUS_NEXT_ACTIONS[status]
    if isinstance(updated.get("first_response_contract"), dict):
        updated["first_response_contract"]["finish_options"] = finish_options
    return updated


def _finish_options(
    write_policy: str,
    *,
    methodology_approval_required: bool = False,
    automation_maturity_required: bool = False,
    agent_skill_metrics_loop: dict[str, Any] | None = None,
) -> list[str]:
    options = ["read_only_audit", "ask_owner"]
    if write_policy == "staged_only" and not automation_maturity_required:
        options.append("stage_proposal")
    if isinstance(agent_skill_metrics_loop, dict):
        options.append("stage_metrics_report")
        options.append("request_owner_review")
        if str(agent_skill_metrics_loop.get("automation_policy", "")) == "candidate_only":
            options.append("block_automation_promotion")
        status = str(agent_skill_metrics_loop.get("status", ""))
        if status in {"regression_detected", "blocked_by_guardrail", "present_unverified"}:
            options.append("investigate_regression")
        else:
            options.append("keep_current")
    if write_policy == "approved_write" or methodology_approval_required:
        options.append("request_approval")
    options.append("run_verification")
    options.append("stop_blocked")
    return options


STATUS_FINISH_OPTIONS = {
    "route_ready": None,
    "needs_context": ["read_only_audit", "ask_owner", "stop_blocked"],
    "needs_approval": ["read_only_audit", "ask_owner", "request_approval", "stop_blocked"],
    "blocked": ["read_only_audit", "ask_owner", "stop_blocked"],
    "completed": ["run_verification", "stop_blocked"],
    "failed": ["read_only_audit", "ask_owner", "stop_blocked"],
}

STATUS_NEXT_ACTIONS = {
    "needs_context": "Collect missing control-plane context before staging proposals.",
    "needs_approval": "Request explicit owner approval before any write, stage, or external action.",
    "blocked": "Stop and resolve the blocking evidence, source-policy, approval, or ownership gap.",
    "completed": "Record current verification evidence and hand off the completed result.",
    "failed": "Record failure evidence and route to bug rescue or owner review.",
}


def _finish_options_for_status(status: str, current_options: Any) -> list[str]:
    status_options = STATUS_FINISH_OPTIONS.get(status)
    if status_options is not None:
        return list(status_options)
    if not isinstance(current_options, list):
        return ["read_only_audit", "ask_owner", "stop_blocked"]
    return [option for option in current_options if option in {
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
    }]


def _evidence_gaps(methodology_packet: dict[str, Any]) -> list[str]:
    semantic = methodology_packet.get("semantic_evidence_sufficiency")
    gaps: list[str] = []
    if isinstance(semantic, dict):
        required = semantic.get("required_evidence")
        if isinstance(required, list):
            gaps.extend(str(item) for item in required if str(item).strip())
        status = semantic.get("status")
        if status == "present_unverified" and not gaps:
            gaps.append("owner-reviewed methodology evidence")
    if methodology_packet.get("status") == "present_unverified" and not gaps:
        gaps.append("current verification evidence")
    return gaps


def _question_queue_from_methodology(
    methodology_intelligence: dict[str, Any] | None,
    usage_mode: dict[str, Any],
    *,
    agent_skill_metrics_loop: dict[str, Any] | None = None,
) -> dict[str, Any]:
    intelligence = methodology_intelligence if isinstance(methodology_intelligence, dict) else {}
    synthesis = intelligence.get("methodology_synthesis")
    if not isinstance(synthesis, dict):
        synthesis = {}
    owner_questions = intelligence.get("questions_for_owner")
    if not isinstance(owner_questions, list):
        owner_questions = synthesis.get("owner_questions", [])
    recommendation_groups = intelligence.get("recommendation_groups")
    if not isinstance(recommendation_groups, list):
        recommendation_groups = synthesis.get("recommendation_groups", [])
    unknowns = intelligence.get("unknowns")
    if not isinstance(unknowns, list):
        unknowns = []
    return build_question_queue(
        owner_questions=owner_questions,
        unknowns=unknowns,
        recommendation_groups=recommendation_groups if isinstance(recommendation_groups, list) else [],
        usage_mode=usage_mode,
        agent_skill_metrics_loop=agent_skill_metrics_loop,
        runtime_status="route_ready",
    )


def _question_summary(question_queue: dict[str, Any]) -> list[str]:
    summary = question_queue.get("summary", {})
    if not isinstance(summary, dict):
        return []
    labels = [
        ("blocking", "blocking question"),
        ("recommended", "recommended question"),
        ("optional", "optional question"),
    ]
    return [
        f"{int(summary.get(key, 0))} {label}{'' if int(summary.get(key, 0)) == 1 else 's'}"
        for key, label in labels
    ]


def _project_graph_blocks_readiness(project_graph_status: dict[str, Any] | None) -> bool:
    if not isinstance(project_graph_status, dict):
        return False
    if project_graph_status.get("status") in {"stale", "ambiguous", "unsupported"}:
        return True
    freshness = project_graph_status.get("freshness")
    if isinstance(freshness, dict) and freshness.get("status") in {"stale", "ambiguous"}:
        return True
    top_gaps = project_graph_status.get("top_gaps")
    if not isinstance(top_gaps, list):
        return False
    blocking_severities = {"high", "critical", "blocker", "blocking"}
    return any(
        isinstance(gap, dict) and str(gap.get("severity") or "").lower() in blocking_severities
        for gap in top_gaps
    )


def _project_graph_summary(project_graph_status: dict[str, Any]) -> dict[str, Any]:
    counts = project_graph_status.get("counts") if isinstance(project_graph_status.get("counts"), dict) else {}
    top_gaps = project_graph_status.get("top_gaps") if isinstance(project_graph_status.get("top_gaps"), list) else []
    return {
        "status": str(project_graph_status.get("status") or "not_available"),
        "counts": {
            "nodes": _int(counts.get("nodes")),
            "edges": _int(counts.get("edges")),
        },
        "top_gap_count": len(top_gaps),
        "safe_next_action": str(project_graph_status.get("safe_next_action") or "Read source files before graph-backed claims."),
    }


def _int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _default_usage_mode() -> dict[str, Any]:
    return {
        "primary": "maintenance",
        "secondary": [],
        "confidence": "low",
        "reasons": ["usage mode was not supplied by workspace discovery"],
        "fallback": "standard_feature",
        "first_response_contract": [
            "mode",
            "confidence",
            "next smallest action",
            "minimum artifacts",
            "evidence gaps",
            "approval boundary",
        ],
        "minimum_artifacts": ["workspace audit packet"],
        "behavioral_eval_cases": ["route-selection"],
    }


def _default_behavioral_route_inputs() -> dict[str, Any]:
    return {
        "intent_hint_present": False,
        "workspace_signals": {
            "stack": [],
            "active_surfaces": [],
            "methodology_signals": [],
        },
        "control_plane_state": {
            "existing_control_plane_files": [],
            "has_codex_assets": False,
        },
    }
