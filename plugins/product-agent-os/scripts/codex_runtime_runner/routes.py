from __future__ import annotations

from typing import Any

from codex_runtime_runner.contracts import (
    build_methodology_packet,
    methodology_requires_approval,
    methodology_requires_automation_maturity,
)


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
) -> dict[str, Any]:
    skill, subagent, write_policy, action = ROUTES[lifecycle_state]
    if subagent and not allow_subagents:
        skill = "project-lifecycle-orchestrator"
        subagent = ""
    approval_requirements = ["explicit approval record required before workspace writes"] if write_policy == "approved_write" else []
    usage_mode = usage_mode or _default_usage_mode()
    methodology_packet = build_methodology_packet(methodology_intelligence)
    methodology_approval_required = methodology_requires_approval(methodology_packet)
    automation_maturity_required = (
        lifecycle_state == "learning_ready"
        and methodology_requires_automation_maturity(methodology_packet)
    )
    if automation_maturity_required:
        skill = "learning-loop-maintainer"
        subagent = ""
        action = "Record manual stability and workflow value evidence before automation promotion."
    if methodology_approval_required:
        approval_requirements.append("explicit approval required before methodology-recommended external or irreversible action")
    if automation_maturity_required:
        approval_requirements.append("manual stability and workflow value evidence required before automation promotion")
    finish_options = _finish_options(
        write_policy,
        methodology_approval_required=methodology_approval_required,
        automation_maturity_required=automation_maturity_required,
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
        ],
    }
    route["usage_mode"] = usage_mode
    route["behavioral_route_inputs"] = behavioral_route_inputs or _default_behavioral_route_inputs()
    route["methodology_packet"] = methodology_packet
    route["finish_options"] = finish_options
    route["first_response_contract"] = {
        "mode": usage_mode["primary"],
        "confidence": usage_mode["confidence"],
        "next_smallest_action": action,
        "safe_next_action": methodology_packet["safe_next_action"],
        "required_fields": usage_mode["first_response_contract"],
        "minimum_artifacts": usage_mode["minimum_artifacts"],
        "evidence_gaps": [],
        "approval_boundary": write_policy,
        "finish_options": finish_options,
    }
    return route


def _finish_options(
    write_policy: str,
    *,
    methodology_approval_required: bool = False,
    automation_maturity_required: bool = False,
) -> list[str]:
    options = ["read_only_audit", "ask_owner"]
    if write_policy == "staged_only" and not automation_maturity_required:
        options.append("stage_proposal")
    if write_policy == "approved_write" or methodology_approval_required:
        options.append("request_approval")
    options.append("run_verification")
    options.append("stop_blocked")
    return options


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
