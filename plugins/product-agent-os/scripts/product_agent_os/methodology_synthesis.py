"""Pure cross-domain methodology synthesis helpers for Product-Agent OS."""

from __future__ import annotations

import re
from typing import Any

from product_agent_os.methodology_catalog import load_methodology_catalog
from product_agent_os.templates import required_templates


PRIORITY_ORDER = {
    "P0_blocker": 0,
    "P1_high_risk": 1,
    "P2_recommended": 2,
    "P3_optional_maturity": 3,
    "not_applicable": 4,
}

CANONICAL_TEMPLATE_OWNERS = {
    "task-matrix-plan.md": "codex_agentic_workflow",
}


def build_methodology_synthesis(
    recommendations: list[dict[str, Any]],
    *,
    owner_questions: list[str] | None = None,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a deterministic grouped synthesis packet without workspace side effects."""

    active_catalog = catalog if catalog is not None else load_methodology_catalog()
    synthesis = active_catalog["synthesis"]
    groups = group_recommendations(recommendations, catalog=active_catalog)
    ordered_groups = sorted(groups, key=_group_sort_key)
    return {
        "status": "ok",
        "write_policy": "read_only",
        "recommendation_groups": ordered_groups,
        "source_artifact_ledger": source_artifact_ledger(catalog=active_catalog),
        "semantic_evidence_sufficiency": synthesis["semantic_evidence_sufficiency"],
        "owner_questions": dedupe_owner_questions(owner_questions or []),
        "safe_next_action": _safe_next_action(ordered_groups),
    }


def group_recommendations(
    recommendations: list[dict[str, Any]],
    *,
    catalog: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Group recommendation packets by artifact while preserving source evidence."""

    active_catalog = catalog if catalog is not None else load_methodology_catalog()
    synthesis = active_catalog["synthesis"]
    groups: dict[str, dict[str, Any]] = {}
    for recommendation in recommendations:
        artifact = str(recommendation.get("artifact", ""))
        if not artifact:
            continue
        group = groups.setdefault(artifact, _empty_group(artifact, synthesis))
        priority = str(recommendation.get("priority", "not_applicable"))
        if _priority_index(priority) < _priority_index(group["priority"]):
            group["priority"] = priority
            group["safe_next_action"] = str(recommendation.get("safe_next_action", ""))
        group["risk_rank"] = max(group["risk_rank"], _risk_rank(artifact, synthesis))
        _append_unique(group["source_domains"], str(recommendation.get("domain", "")))
        _append_unique(group["gates"], str(recommendation.get("gate", "")))
        _append_unique(group["reasons"], str(recommendation.get("reason", "")))
        for evidence in recommendation.get("evidence_required", []):
            _append_unique(group["evidence_required"], str(evidence))
    return list(groups.values())


def classify_source_artifact(
    artifact: str,
    *,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Classify an artifact mention from docs/methodologies as canonical, alias or deferred."""

    active_catalog = catalog if catalog is not None else load_methodology_catalog()
    synthesis = active_catalog["synthesis"]
    canonical_artifact = _canonical_artifact_name(artifact)
    aliases = synthesis["artifact_aliases"]
    if artifact in aliases:
        record = aliases[artifact]
        return {
            "artifact": artifact,
            "decision": "alias",
            "target": record["target"],
            "owner_domain": record["owner_domain"],
            "reason": record.get("reason", "source-era name maps to canonical packaged artifact"),
        }
    decisions = synthesis["source_artifact_decisions"]
    if artifact in decisions:
        record = decisions[artifact]
        return {
            "artifact": artifact,
            "decision": record["decision"],
            "target": record.get("target", ""),
            "owner_domain": record["owner_domain"],
            "reason": record["reason"],
        }
    if canonical_artifact in _canonical_artifacts(active_catalog):
        return {
            "artifact": artifact,
            "decision": "canonical_template",
            "target": canonical_artifact,
            "owner_domain": _artifact_owner(canonical_artifact, synthesis),
            "reason": "artifact is already represented by the catalog or packaged templates",
        }
    return {
        "artifact": artifact,
        "decision": "deferred",
        "target": "",
        "owner_domain": "quality_testing_evals",
        "reason": "source artifact mention is not yet represented by a canonical template or explicit alias",
    }


def source_artifact_ledger(*, catalog: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Return explicit source artifact alias and non-template decisions from the catalog."""

    active_catalog = catalog if catalog is not None else load_methodology_catalog()
    synthesis = active_catalog["synthesis"]
    artifacts = sorted(set(synthesis["artifact_aliases"]) | set(synthesis["source_artifact_decisions"]))
    return [classify_source_artifact(artifact, catalog=active_catalog) for artifact in artifacts]


def dedupe_owner_questions(questions: list[str]) -> list[str]:
    """Dedupe semantically identical owner questions while preserving first wording."""

    seen: set[str] = set()
    result: list[str] = []
    for question in questions:
        key = _question_key(question)
        if key in seen:
            continue
        seen.add(key)
        result.append(question)
    return result


def _empty_group(artifact: str, synthesis: dict[str, Any]) -> dict[str, Any]:
    owner_record = synthesis["artifact_owners"].get(artifact, {})
    return {
        "artifact": artifact,
        "priority": "not_applicable",
        "owner_domain": owner_record.get("owner_domain", ""),
        "consumer_domains": list(owner_record.get("consumer_domains", [])),
        "source_domains": [],
        "gates": [],
        "reasons": [],
        "evidence_required": [],
        "safe_next_action": "",
        "risk_rank": _risk_rank(artifact, synthesis),
    }


def _safe_next_action(groups: list[dict[str, Any]]) -> str:
    for group in groups:
        if group.get("safe_next_action"):
            return str(group["safe_next_action"])
    return "Record methodology synthesis output and proceed only with evidence-backed planning."


def _risk_rank(artifact: str, synthesis: dict[str, Any]) -> int:
    ranks = {
        str(item.get("artifact")): int(item.get("risk_rank", 0))
        for item in synthesis.get("priority_tie_breakers", [])
        if isinstance(item, dict)
    }
    return ranks.get(artifact, 0)


def _group_sort_key(group: dict[str, Any]) -> tuple[int, int, int, str]:
    artifact = str(group.get("artifact", ""))
    priority_index = _priority_index(str(group.get("priority", "not_applicable")))
    risk_rank = int(group.get("risk_rank", 0))
    risk_specific_before_generic = 0 if risk_rank >= 80 and priority_index <= 1 else 1
    return (risk_specific_before_generic, priority_index, -risk_rank, artifact)


def _artifact_owner(artifact: str, synthesis: dict[str, Any]) -> str:
    record = synthesis.get("artifact_owners", {}).get(artifact, {})
    return str(record.get("owner_domain", "") or CANONICAL_TEMPLATE_OWNERS.get(artifact, ""))


def _canonical_artifact_name(artifact: str) -> str:
    return artifact.replace("\\", "/").rsplit("/", 1)[-1]


def _canonical_artifacts(catalog: dict[str, Any]) -> set[str]:
    artifacts: set[str] = set()
    for domain in catalog["domains"]:
        artifacts.update(str(item) for item in domain["artifacts"])
    artifacts.update(item.target_path.rsplit("/", 1)[-1] for item in required_templates())
    artifacts.update(str(item) for item in catalog["synthesis"].get("supported_non_catalog_targets", []))
    return artifacts


def _priority_index(priority: str) -> int:
    return PRIORITY_ORDER.get(priority, 99)


def _append_unique(items: list[str], value: str) -> None:
    if value and value not in items:
        items.append(value)


def _question_key(question: str) -> str:
    normalized = question.lower().replace("highest priority", "highest-priority")
    normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
    return " ".join(normalized.split())
