"""Methodology catalog loading and validation for Product-Agent OS Track 9."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


READINESS_STATUSES = [
    "not_applicable",
    "applicable_missing",
    "present_unverified",
    "present_verified",
    "proposal_staged",
    "explicit_gap_accepted",
    "approval_required",
]

RECOMMENDATION_PRIORITIES = [
    "P0_blocker",
    "P1_high_risk",
    "P2_recommended",
    "P3_optional_maturity",
    "not_applicable",
]

MATURITY_LEVELS = ["baseline", "team", "production", "regulated"]
COMPLEXITY_PROFILES = ["simple", "standard", "complex", "high_risk"]

DOMAIN_KEYS = {
    "id",
    "title",
    "source_file",
    "purpose",
    "applies_when",
    "not_applicable_when",
    "maturity_impact",
    "complexity_impact",
    "track8_scenarios",
    "decision_horizons",
    "artifacts",
    "gates",
    "eval_fields",
    "overlaps",
}

SYNTHESIS_KEYS = {
    "schema_version",
    "output_packet_keys",
    "supported_non_catalog_targets",
    "shared_gates",
    "artifact_owners",
    "artifact_aliases",
    "source_artifact_decisions",
    "priority_tie_breakers",
    "conflict_rules",
    "false_positive_rules",
    "semantic_evidence_sufficiency",
    "owner_question_dedupe",
}


def _plugin_root() -> Path:
    return Path(__file__).resolve().parents[2]


def catalog_path() -> Path:
    return _plugin_root() / "assets" / "methodology" / "methodology-catalog.json"


def load_methodology_catalog(path: str | Path | None = None) -> dict[str, Any]:
    catalog_file = Path(path) if path is not None else catalog_path()
    data = json.loads(catalog_file.read_text(encoding="utf-8"))
    errors = validate_methodology_catalog(data)
    if errors:
        raise ValueError("; ".join(errors))
    return data


def validate_methodology_catalog(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("version") != 1:
        errors.append("version must be 1")
    if data.get("readiness_statuses") != READINESS_STATUSES:
        errors.append("readiness_statuses mismatch")
    if data.get("recommendation_priorities") != RECOMMENDATION_PRIORITIES:
        errors.append("recommendation_priorities mismatch")
    if data.get("maturity_levels") != MATURITY_LEVELS:
        errors.append("maturity_levels mismatch")
    if data.get("complexity_profiles") != COMPLEXITY_PROFILES:
        errors.append("complexity_profiles mismatch")
    domains = data.get("domains")
    if not isinstance(domains, list) or not domains:
        errors.append("domains must be a non-empty list")
        return errors
    seen: set[str] = set()
    all_gates: set[str] = set()
    all_artifacts: set[str] = set()
    for index, domain in enumerate(domains):
        if not isinstance(domain, dict):
            errors.append(f"domains[{index}] must be an object")
            continue
        domain_id = str(domain.get("id", f"index-{index}"))
        if domain_id in seen:
            errors.append(f"duplicate domain id: {domain_id}")
        seen.add(domain_id)
        if set(domain) != DOMAIN_KEYS:
            errors.append(f"{domain_id} keys mismatch")
        for field in [
            "applies_when",
            "not_applicable_when",
            "maturity_impact",
            "complexity_impact",
            "track8_scenarios",
            "decision_horizons",
            "artifacts",
            "gates",
            "eval_fields",
            "overlaps",
        ]:
            if not isinstance(domain.get(field), list):
                errors.append(f"{domain_id}.{field} must be a list")
        if isinstance(domain.get("gates"), list):
            all_gates.update(str(item) for item in domain["gates"])
        if isinstance(domain.get("artifacts"), list):
            all_artifacts.update(str(item) for item in domain["artifacts"])
    errors.extend(_validate_synthesis(data.get("synthesis"), seen, all_gates, all_artifacts))
    return errors


def _validate_synthesis(
    synthesis: Any,
    domain_ids: set[str],
    all_gates: set[str],
    all_artifacts: set[str],
) -> list[str]:
    errors: list[str] = []
    if not isinstance(synthesis, dict):
        errors.append("synthesis must be an object")
        return errors
    if set(synthesis) != SYNTHESIS_KEYS:
        errors.append("synthesis keys mismatch")
    if synthesis.get("schema_version") != 1:
        errors.append("synthesis.schema_version must be 1")
    for field in ["output_packet_keys", "supported_non_catalog_targets", "priority_tie_breakers", "conflict_rules", "false_positive_rules"]:
        if not isinstance(synthesis.get(field), list):
            errors.append(f"synthesis.{field} must be a list")
    for field in ["shared_gates", "artifact_owners", "artifact_aliases", "source_artifact_decisions", "semantic_evidence_sufficiency", "owner_question_dedupe"]:
        if not isinstance(synthesis.get(field), dict):
            errors.append(f"synthesis.{field} must be an object")

    supported_targets = {
        str(item)
        for item in synthesis.get("supported_non_catalog_targets", [])
        if isinstance(item, str)
    }
    known_artifacts = set(all_artifacts) | set(synthesis.get("artifact_owners", {})) | supported_targets

    for gate, record in synthesis.get("shared_gates", {}).items():
        if gate not in all_gates:
            errors.append(f"unknown synthesis shared gate: {gate}")
        if isinstance(record, dict):
            _validate_domain_reference(errors, record.get("owner_domain"), domain_ids, "owner")
            _validate_domain_list(errors, record.get("consumer_domains"), domain_ids, "consumer")
        else:
            errors.append(f"synthesis.shared_gates.{gate} must be an object")

    for artifact, record in synthesis.get("artifact_owners", {}).items():
        if artifact not in all_artifacts:
            errors.append(f"unknown synthesis artifact owner: {artifact}")
        if isinstance(record, dict):
            _validate_domain_reference(errors, record.get("owner_domain"), domain_ids, "owner")
            _validate_domain_list(errors, record.get("consumer_domains"), domain_ids, "consumer")
        else:
            errors.append(f"synthesis.artifact_owners.{artifact} must be an object")

    for source_name, record in synthesis.get("artifact_aliases", {}).items():
        if not isinstance(record, dict):
            errors.append(f"synthesis.artifact_aliases.{source_name} must be an object")
            continue
        _validate_domain_reference(errors, record.get("owner_domain"), domain_ids, "owner")
        target = record.get("target")
        if not isinstance(target, str) or target not in known_artifacts:
            errors.append(f"unknown synthesis artifact target: {target}")

    for source_name, record in synthesis.get("source_artifact_decisions", {}).items():
        if not isinstance(record, dict):
            errors.append(f"synthesis.source_artifact_decisions.{source_name} must be an object")
            continue
        _validate_domain_reference(errors, record.get("owner_domain"), domain_ids, "owner")
        if record.get("decision") not in {"existing_non_template", "deferred"}:
            errors.append(f"unknown source artifact decision: {record.get('decision')}")

    for item in synthesis.get("priority_tie_breakers", []):
        if not isinstance(item, dict):
            errors.append("synthesis.priority_tie_breakers entries must be objects")
            continue
        artifact = item.get("artifact")
        if not isinstance(artifact, str) or artifact not in known_artifacts:
            errors.append(f"unknown synthesis priority artifact: {artifact}")
        if not isinstance(item.get("risk_rank"), int):
            errors.append(f"synthesis priority risk_rank must be int: {item.get('id')}")

    semantic = synthesis.get("semantic_evidence_sufficiency", {})
    if isinstance(semantic, dict):
        _validate_domain_reference(errors, semantic.get("owner_domain"), domain_ids, "owner")
        _validate_domain_list(errors, semantic.get("consumer_domains"), domain_ids, "consumer")
        if not isinstance(semantic.get("accepted_gap_required_fields"), list):
            errors.append("synthesis.semantic_evidence_sufficiency.accepted_gap_required_fields must be a list")

    return errors


def _validate_domain_reference(
    errors: list[str],
    domain: Any,
    domain_ids: set[str],
    role: str,
) -> None:
    if not isinstance(domain, str) or domain not in domain_ids:
        errors.append(f"unknown synthesis {role} domain: {domain}")


def _validate_domain_list(
    errors: list[str],
    domains: Any,
    domain_ids: set[str],
    role: str,
) -> None:
    if not isinstance(domains, list):
        errors.append(f"synthesis {role} domains must be a list")
        return
    for domain in domains:
        if not isinstance(domain, str) or domain not in domain_ids:
            errors.append(f"unknown synthesis {role} domain: {domain}")
