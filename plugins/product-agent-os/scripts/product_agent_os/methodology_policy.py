"""Task-level applicability using existing discovery and test selectors."""

from __future__ import annotations

from typing import Any

from product_agent_os.test_strategy_selector import TEST_FIRST_MODES


METHODS = ("spec_driven", "design_driven", "tdd", "add", "fsd")
OWNERS = ("requirements-author", "reviewer", "test-eval-designer", "implementation-planner", "architect")


def _choice(
    method: str, owner: str, applicability: str, depth: str, reason: str, next_action: str,
    *evidence_refs: str,
) -> dict[str, Any]:
    return {
        "method": method, "owner": owner, "applicability": applicability, "depth": depth,
        "reason": reason, "next_action": next_action, "evidence_refs": list(evidence_refs),
    }


def select_methodologies(
    profile: dict[str, Any], route: dict[str, Any], next_check: str,
) -> list[dict[str, Any]]:
    """Add task guidance without changing the repository audit or its domain statuses."""
    spec, design, test, agent, fsd = METHODS
    spec_owner, design_owner, test_owner, agent_owner, fsd_owner = OWNERS
    depth = "full" if route["mode"] == "full" else "compact"
    ui = profile["ui_scope"]
    cross_feature = profile["coupling"] in {"cross_surface", "multiple_frontend_areas"}
    spec_choice = _choice(
        spec, spec_owner, "applicable", depth, "Task intent and acceptance need an observable specification",
        "Review requirements and invariants" if depth == "full" else "Confirm the acceptance criterion",
        "task",
    )
    design_choice = (
        _choice(design, design_owner, "applicable", depth, "The task changes a detected UI surface",
                "Identify the affected journey and states", "task", "workspace")
        if ui else
        _choice(design, design_owner, "not_applicable", "none", "No UI change is evidenced in this scope",
                "Keep the check scoped to the changed surface", "task")
    )
    mode = profile["change_mode"]
    if mode not in TEST_FIRST_MODES or next_check == "review_evaluation":
        test_choice = _choice(test, test_owner, "not_applicable", "none",
                              "The declared change does not require a new failure-first test",
                              "Use a check suited to the change mode", "task")
    elif next_check == "run_regression":
        test_choice = _choice(test, test_owner, "applicable", depth,
                              "Behavior change and a declared, observed test seam",
                              "Identify the source-backed test for the intended failure", "task", "workspace")
    else:
        test_choice = _choice(test, test_owner, "needs_context", "none",
                              "An executable test seam has not been established",
                              "Identify a behavior check or record the missing test seam", "task", "workspace")
    agent_choice = _choice(
        agent, agent_owner, "applicable", depth,
        "The task has an explicit scope and a read-only verification boundary",
        "Review ownership and verification handoff" if depth == "full" else "Use the scoped next check", "task",
    )
    fsd_choice = (
        _choice(fsd, fsd_owner, "needs_context", "compact",
                "The change spans frontend areas or surfaces; paths alone do not establish coupling",
                "Inspect imports and responsibilities before deciding on a boundary change", "task", "workspace")
        if ui and cross_feature else
        _choice(fsd, fsd_owner, "not_applicable", "none", "No cross-feature frontend boundary change is evidenced",
                "Use the current component boundaries", "task", "workspace")
    )
    return [spec_choice, design_choice, test_choice, agent_choice, fsd_choice]
