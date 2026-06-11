from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from product_agent_os.stage_manifest import canonical_json, content_digest


FAILURE_TAXONOMY_SCHEMA_VERSION = "pilot_failure_taxonomy_v1"
REQUIRED_FAILURE_CLASSES = {
    "false_pass_blocked",
    "false_rewrite_blocked",
    "fake_evidence_rejected",
    "missing_current_evidence",
    "generated_view_not_proof",
    "synthetic_only_boundary",
}


def build_failure_taxonomy(
    *,
    test_id: str,
    attempt_id: str,
    generated_at: str | None = None,
) -> dict[str, Any]:
    taxonomy = {
        "schema_version": FAILURE_TAXONOMY_SCHEMA_VERSION,
        "batch": "B39",
        "test_id": test_id,
        "attempt_id": attempt_id,
        "generated_at": generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "classes": sorted(REQUIRED_FAILURE_CLASSES),
        "class_definitions": {
            "false_pass_blocked": "Completion claim blocked when current evidence is absent or contradictory.",
            "false_rewrite_blocked": "Rewrite-from-scratch drift blocked when project context should be extended.",
            "fake_evidence_rejected": "Claimed or fabricated evidence cannot satisfy a verification gate.",
            "missing_current_evidence": "Only stale, generated, or claimed evidence is available.",
            "generated_view_not_proof": "Dashboard, rollup, report, or graph is orientation evidence only.",
            "synthetic_only_boundary": "Synthetic fixtures cannot promote a real-project or production claim.",
        },
        "promotion_boundary": "manual_only_not_promoted",
    }
    taxonomy["taxonomy_digest"] = content_digest(canonical_json(taxonomy))
    return taxonomy


def validate_failure_taxonomy(taxonomy: dict[str, Any]) -> list[str]:
    if not isinstance(taxonomy, dict):
        return ["failure taxonomy must be an object"]
    errors: list[str] = []
    if taxonomy.get("schema_version") != FAILURE_TAXONOMY_SCHEMA_VERSION:
        errors.append(f"schema_version must be {FAILURE_TAXONOMY_SCHEMA_VERSION}")
    classes = taxonomy.get("classes")
    if not isinstance(classes, list):
        return errors + ["classes must be list"]
    present = set(str(item) for item in classes)
    for required in sorted(REQUIRED_FAILURE_CLASSES):
        if required not in present:
            errors.append(f"missing required failure class: {required}")
    if taxonomy.get("promotion_boundary") != "manual_only_not_promoted":
        errors.append("promotion_boundary must be manual_only_not_promoted")
    if not str(taxonomy.get("taxonomy_digest", "")).startswith("sha256:"):
        errors.append("taxonomy_digest must be a sha256 digest")
    return errors


__all__ = [
    "REQUIRED_FAILURE_CLASSES",
    "build_failure_taxonomy",
    "validate_failure_taxonomy",
]
