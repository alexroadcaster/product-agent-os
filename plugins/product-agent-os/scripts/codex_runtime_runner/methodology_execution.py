"""Read-only assignment and capability routes for explicitly scoped tasks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from product_agent_os.plugin_components import resolve_plugin_components
from product_agent_os.task_routing import fingerprint

_METHOD_SKILLS = {
    "spec_driven": ("requirements-author", "Review the criterion and requirements owner"),
    "design_driven": ("implementation-planner", "Review the affected journey and states"),
    "tdd": ("test-eval-designer", "Review the source-backed check with the task owner"),
    "add": ("project-lifecycle-orchestrator", "Keep the assignment with the primary agent"),
    "fsd": ("risk-reviewer", "Inspect the affected imports before proposing a boundary change"),
}

_WORKFLOWS = {
    "spec_driven": "assets/templates/workflows/task-plan-lifecycle.md",
    "design_driven": "skills/implementation-planner/SKILL.md",
    "tdd": "skills/test-eval-designer/SKILL.md",
    "add": "assets/templates/workflows/task-plan-lifecycle.md",
    "fsd": "skills/risk-reviewer/SKILL.md",
}


def build_execution_assignment(
    decision: dict[str, Any], routing: dict[str, Any], *, parallel_requested: bool,
) -> dict[str, Any]:
    """Propose a single assignment; the offline runner has no agent/tool dispatch port."""
    plugin_root = Path(__file__).resolve().parents[2]
    components = resolve_plugin_components(plugin_root)
    skills = set(components["skills"]["names"])
    capabilities = []
    for method in decision["decisions"]:
        if method["applicability"] == "not_applicable":
            continue
        skill, manual_step = _METHOD_SKILLS[method["method"]]
        packaged = skill in skills
        workflow = _WORKFLOWS[method["method"]]
        capabilities.append({
            "method": method["method"], "skill": skill,
            "workflow": workflow if (plugin_root / workflow).is_file() else None,
            "tool": None, "tool_state": "not_exposed_in_contract_mode",
            "source": f"skills/{skill}/SKILL.md" if packaged else None,
            "availability": "packaged" if packaged else "missing",
            "installed": None, "staged": False, "exposed": None, "invoked": False,
            "evidence_refs": method["evidence_refs"],
            "gap": "HOST_EXPOSURE_UNOBSERVED" if packaged else "CANONICAL_SKILL_MISSING",
            "next_action": manual_step,
        })
    assignment = {
        "schema_version": "paos_methodology_assignment_v1",
        "format": "full" if routing["mode"] == "full" else "concise",
        "scope": decision["scope"], "input_digest": routing["input_digest"],
        "owner": "primary-agent", "goal": decision["plan"]["next_step"]["action"],
        "criteria": [row["id"] for row in decision["requirements"]["criteria"]],
        "planned_paths": decision["requirements"]["changed_paths"],
        "allowed_writes": [], "forbidden_effects": ["target_write", "external_write", "provider_call", "install_or_activate"],
        "checks": [{"id": fingerprint(check["command"]), "sources": check["sources"]}
                   for check in routing["checks"] if check["status"] != "blocked"],
        "parallelism": "serial", "delegation_limit": 0,
        "delegation_gap": "HOST_PARALLEL_CAPABILITY_UNOBSERVED" if parallel_requested else None,
        "runtime_policy": "inherited", "retry_limit": 0,
        "stop_conditions": ["scope_changed", "authority_missing", "partial_child", "timeout", "outcome_unknown"],
        "handoff": {"required": ["scope", "input_digest", "status", "evidence_refs"], "review_required": True},
        "capabilities": capabilities,
    }
    return assignment


def review_execution_handoff(assignment: dict[str, Any], handoff: dict[str, Any]) -> dict[str, str]:
    """Never infer completion, a retry, or a fallback from a child report."""
    if (not isinstance(handoff, dict) or set(handoff) != {"scope", "input_digest", "status", "evidence_refs"}
            or handoff["status"] not in ("reported_complete", "partial", "timeout", "failed", "outcome_unknown")
            or not isinstance(handoff["evidence_refs"], list) or len(handoff["evidence_refs"]) > 200
            or not all(isinstance(ref, str) and ref.strip() for ref in handoff["evidence_refs"])):
        return {"status": "invalid_handoff", "next_action": "Request a bounded result from the assigned owner"}
    if handoff["scope"] != assignment["scope"] or handoff["input_digest"] != assignment["input_digest"]:
        return {"status": "stale_handoff", "next_action": "Refresh sources and authority before continuing"}
    status = handoff["status"]
    if status == "reported_complete" and handoff["evidence_refs"]:
        return {"status": "review_required", "next_action": "Verify the referenced observations independently"}
    if status == "reported_complete":
        status = "partial"
    return {"status": status, "next_action": "Review the last observed result before dispatching further work"}


def project_criterion_evidence(decision: dict[str, Any], routing: dict[str, Any]) -> dict[str, Any]:
    """The offline runner can reconcile caller observations, never attest their execution."""
    next_step = decision["plan"]["next_step"]
    observed = [item for item in routing["check_observations"] if item["command"] == next_step["target"]]
    return {
        "schema_version": "paos_methodology_criterion_projection_v1", "scope": decision["scope"],
        "input_digest": routing["input_digest"], "technical": "not_evaluated", "human": "not_observed",
        "release": "not_evaluated",
        "criteria": [{
            "id": row["id"], "owner": row["owner"], "scenario": row["scenario"],
            "check": row["check"], "technical": "not_evaluated",
            "caller_observations": observed if row["check"] == "plan.next_step" else [],
        } for row in decision["requirements"]["criteria"]],
    }
