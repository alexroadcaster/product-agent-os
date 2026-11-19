"""Compose the scoped methodology decision and formation ownership in one DAG."""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any

from product_agent_os.methodology_synthesis import classify_source_artifact
from product_agent_os.project_formation import formation_plan
from product_agent_os.task_routing import fingerprint


def build_delivery_plan(
    root: Path, audit: dict[str, Any], task: dict[str, Any], decision: dict[str, Any], assignment: dict[str, Any],
) -> dict[str, Any]:
    """Build a proposal from observed domains. Callers must review gaps before staging."""
    facts = decision["facts"]
    branches = {row["method"]: row for row in decision["decisions"] if row["applicability"] != "not_applicable"}
    domains = []
    if "fsd" in branches:
        domains.append("architecture")
    if task.get("evals_required"):
        domains.append("ai")
    contract_files = {PurePosixPath(path).name.lower() for path in assignment["planned_paths"]}
    if contract_files.intersection({"openapi.json", "openapi.yaml", "openapi.yml"}):
        domains.append("api")
    if "schema.sql" in contract_files:
        domains.append("data")
    formation_task = {**task, "explicit_full_packet": True}
    formation = formation_plan(root, {"schema_version": 1, "task": formation_task, "domains": domains}, audit)["plan"]
    synthesis = audit.get("methodology_intelligence", {}).get("methodology_synthesis", {})
    grouped: dict[str, list[str]] = {}
    for row in synthesis.get("recommendation_groups", []):
        artifact = classify_source_artifact(row["artifact"])
        target = artifact["target"]
        if target:
            grouped.setdefault(PurePosixPath(target).name.casefold(), []).extend(row.get("reasons", []))
    artifacts = {}
    for owner, path in formation["owners"].items():
        reasons = [formation["selection_reasons"].get(path, "canonical_information_owner")]
        for name in {PurePosixPath(owner).name.casefold(), PurePosixPath(path).name.casefold()}:
            reasons.extend(grouped.get(name, []))
        artifacts[owner] = {"path": path, "reasons": sorted(set(reasons)),
                            "disposition": "reuse" if path in formation["source_snapshot"] else "proposal"}

    slices = []

    def add(name: str, owner: str, inputs: list[str], output: str, depends_on: list[str], *, checks: bool = False) -> None:
        slices.append({"id": name, "owner": owner, "inputs": inputs, "output": output, "depends_on": depends_on,
                       "criteria": assignment["criteria"], "checks": assignment["checks"] if checks else [],
                       "stop": "Review stale inputs, missing evidence or authority before continuing"})

    add("specification", "requirements-author", ["task", "workspace"], "criterion trace", [])
    before_build = []
    if "design_driven" in branches:
        add("design", branches["design_driven"]["owner"], ["criterion trace"], "journey and UI states", ["specification"])
        before_build.append("design")
    if "fsd" in branches:
        add("architecture", branches["fsd"]["owner"], ["criterion trace", "workspace"], "imports and ownership evidence", ["specification"])
        before_build.append("architecture")
    if "tdd" in branches:
        add("red", branches["tdd"]["owner"], ["criterion trace"], "observed failing regression", ["specification"], checks=True)
        before_build.append("red")
    if facts["change_mode"] == "no_op":
        add("verification", "test-eval-designer", ["criterion trace"], "observations", ["specification"], checks=True)
    else:
        add("implementation", assignment["owner"], assignment["planned_paths"], "scoped change",
            before_build or ["specification"])
        add("verification", "test-eval-designer", ["scoped change"], "observations", ["implementation"], checks=True)
    gaps = sorted(set(formation["gaps"] + formation["implementation_gaps"] + decision["plan"]["gaps"]))
    if "design" in before_build:
        gaps.append("Attach current journey and visual acceptance scenarios before implementation")
    if "architecture" in before_build:
        gaps.append("Review observed imports and public boundaries before selecting an FSD migration")
    plan = {
        "schema_version": "paos_methodology_delivery_v1", "scope": decision["scope"],
        "input_digest": assignment["input_digest"], "formation_digest": formation["digest"],
        "authority": "read_only", "status": "review_required" if gaps else "proposed",
        "slices": slices, "artifacts": artifacts, "gaps": gaps,
        "next_action": "Resolve the listed gaps with their owners" if gaps else "Review the specification and checks",
    }
    return {**plan, "digest": fingerprint(plan)}
