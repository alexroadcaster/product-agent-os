from __future__ import annotations

from typing import Any


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
) -> dict[str, Any]:
    skill, subagent, write_policy, action = ROUTES[lifecycle_state]
    if subagent and not allow_subagents:
        skill = "project-lifecycle-orchestrator"
        subagent = ""
    approval_requirements = ["explicit approval record required before workspace writes"] if write_policy == "approved_write" else []
    usage_mode = usage_mode or _default_usage_mode()
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
        ],
    }
    route["usage_mode"] = usage_mode
    route["behavioral_route_inputs"] = behavioral_route_inputs or _default_behavioral_route_inputs()
    route["first_response_contract"] = {
        "mode": usage_mode["primary"],
        "confidence": usage_mode["confidence"],
        "next_smallest_action": action,
        "required_fields": usage_mode["first_response_contract"],
        "minimum_artifacts": usage_mode["minimum_artifacts"],
        "evidence_gaps": [],
        "approval_boundary": write_policy,
    }
    return route


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
