"""Project only the requirements and criterion trace for the selected task."""

from __future__ import annotations

from typing import Any

from product_agent_os.methodology_profile import scoped_paths


def project_requirements(
    task: dict[str, Any], route: dict[str, Any], step: dict[str, Any],
) -> dict[str, Any]:
    """Map a single criterion to the proposed check; keep unresolved mappings explicit."""
    criteria = task["acceptance"]
    linked = len(criteria) == 1 and step["target"] is not None
    full = route["mode"] == "full"
    evidence_owner = (
        "requirements-author" if step["kind"] == "check_source" else "test-eval-designer"
    )
    return {
        "owner": "requirements-author",
        "depth": "full" if full else "compact",
        "changed_paths": scoped_paths(task["changed_paths"]),
        "invariants": route["invariants"],
        "non_goals": ["Changes outside the declared task scope", "Applying this proposal"],
        "criteria": [
            {
                "id": f"AC-{index}",
                "criterion": criterion,
                "scenario": (
                    "Use the proposed verification and compare the observation with this criterion"
                    if linked else "Identify an observable check for this criterion"
                ),
                "owner": evidence_owner if linked else "requirements-author",
                "trace": "proposed" if linked else "gap",
                "check": "plan.next_step" if linked else None,
                "evidence_refs": list(dict.fromkeys(["task", *step["evidence_refs"]])) if linked else ["task"],
            }
            for index, criterion in enumerate(criteria, 1)
        ],
    }
