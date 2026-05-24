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


def plan_route(lifecycle_state: str, *, allow_subagents: bool) -> dict[str, Any]:
    skill, subagent, write_policy, action = ROUTES[lifecycle_state]
    if subagent and not allow_subagents:
        skill = "project-lifecycle-orchestrator"
        subagent = ""
    approval_requirements = ["explicit approval record required before workspace writes"] if write_policy == "approved_write" else []
    return {
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
