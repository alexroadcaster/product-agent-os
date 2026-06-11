from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from product_agent_os.stage_manifest import canonical_json, content_digest


SCORECARD_SCHEMA_VERSION = "pilot_product_usability_scorecard_v1"
GATE_GROUPS = ("pilot", "product_usability", "promotion")
GATE_STATUSES = ("passed", "failed", "blocked", "accepted_gap")


def build_scorecard_gates(
    *,
    test_id: str,
    attempt_id: str,
    gate_results: list[dict[str, Any]],
    generated_at: str | None = None,
) -> dict[str, Any]:
    groups = {group: {status: 0 for status in GATE_STATUSES} for group in GATE_GROUPS}
    safe_results = []
    blocking_reasons: list[str] = []
    for item in gate_results:
        group = str(item.get("group", "pilot"))
        status = str(item.get("status", "blocked"))
        if group not in groups:
            group = "pilot"
        if status not in GATE_STATUSES:
            status = "blocked"
        reason = str(item.get("reason", "")).strip()
        groups[group][status] += 1
        if status in {"blocked", "failed"} and reason:
            blocking_reasons.append(reason)
        safe_results.append({"gate": str(item.get("gate", "")).strip(), "group": group, "status": status, "reason": reason})
    scorecard = {
        "schema_version": SCORECARD_SCHEMA_VERSION,
        "batch": "B39",
        "test_id": test_id,
        "attempt_id": attempt_id,
        "generated_at": generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "gate_results": safe_results,
        "groups": groups,
        "blocking_reasons": sorted(set(blocking_reasons)),
        "promotion_decision": "not_promoted" if blocking_reasons or groups["promotion"]["blocked"] else "owner_review_required",
        "promotion_boundary": "manual_only_not_promoted",
        "source_policy": "scorecard is a gate ledger, not proof by itself",
    }
    scorecard["scorecard_digest"] = content_digest(canonical_json(scorecard))
    return scorecard


def validate_scorecard_gates(scorecard: dict[str, Any]) -> list[str]:
    if not isinstance(scorecard, dict):
        return ["scorecard must be an object"]
    errors: list[str] = []
    if scorecard.get("schema_version") != SCORECARD_SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCORECARD_SCHEMA_VERSION}")
    if scorecard.get("promotion_decision") not in {"not_promoted", "owner_review_required"}:
        errors.append("promotion_decision missing or invalid")
    if scorecard.get("promotion_boundary") != "manual_only_not_promoted":
        errors.append("promotion_boundary must be manual_only_not_promoted")
    groups = scorecard.get("groups")
    if not isinstance(groups, dict):
        errors.append("groups must be an object")
        groups = {}
    for group in GATE_GROUPS:
        if group not in groups:
            errors.append(f"missing group: {group}")
    if not str(scorecard.get("scorecard_digest", "")).startswith("sha256:"):
        errors.append("scorecard_digest must be a sha256 digest")
    return errors


__all__ = [
    "GATE_GROUPS",
    "build_scorecard_gates",
    "validate_scorecard_gates",
]
