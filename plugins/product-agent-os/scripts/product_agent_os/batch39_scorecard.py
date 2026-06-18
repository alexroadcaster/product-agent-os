from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from product_agent_os.stage_manifest import canonical_json, content_digest


SCORECARD_SCHEMA_VERSION = "pilot_product_usability_scorecard_v1"
FIRST_RUN_ARTIFACT_SCORECARD_SCHEMA_VERSION = "first_run_artifact_scorecard_v1"
GATE_GROUPS = ("pilot", "product_usability", "promotion")
GATE_STATUSES = ("passed", "failed", "blocked", "accepted_gap")
FIRST_RUN_SCORE_KEYS = (
    "clarity",
    "completeness",
    "actionability",
    "missing_evidence_visibility",
    "first_safe_action",
    "approval_boundary_clarity",
    "onboarding_time",
    "artifact_navigation",
)


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


def build_first_run_artifact_scorecard(
    *,
    test_id: str,
    attempt_id: str,
    artifact_summary: dict[str, Any],
    owner_review_status: str,
    generated_at: str | None = None,
) -> dict[str, Any]:
    summary = artifact_summary if isinstance(artifact_summary, dict) else {}
    raw_counts = {
        "page_count": _int(summary.get("page_count")),
        "source_artifact_count": _int(summary.get("source_artifact_count")),
        "unsupported_claim_count": _int(summary.get("unsupported_claim_count")),
    }
    scores = {
        "clarity": _score_bool(raw_counts["page_count"] >= 8),
        "completeness": _score_bool(raw_counts["source_artifact_count"] > 0 and summary.get("manifest_digest")),
        "actionability": _score_bool(summary.get("safe_next_action_present") is True),
        "missing_evidence_visibility": _score_bool(raw_counts["unsupported_claim_count"] >= 0),
        "first_safe_action": _score_bool(summary.get("safe_next_action_present") is True),
        "approval_boundary_clarity": _score_bool(str(summary.get("source_policy_status", "")) in {"approval_required", "current", "blocked"}),
        "onboarding_time": _score_bool(raw_counts["page_count"] <= 12),
        "artifact_navigation": _score_bool(summary.get("navigation_status") == "complete"),
    }
    operator_score = round(sum(scores.values()) / len(FIRST_RUN_SCORE_KEYS), 3)
    blockers = []
    if summary.get("redaction_status") != "passed_redacted":
        blockers.append("redaction_not_passed")
    if owner_review_status != "owner_reviewed":
        blockers.append("owner_review_pending")
    scorecard = {
        "schema_version": FIRST_RUN_ARTIFACT_SCORECARD_SCHEMA_VERSION,
        "batch": "B39",
        "test_id": test_id,
        "attempt_id": attempt_id,
        "generated_at": generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "artifact_ref": {
            "kind": "generated_analysis_pack",
            "manifest_digest": str(summary.get("manifest_digest", "")),
            "freshness": str(summary.get("freshness", "not_available")),
        },
        "raw_counts": raw_counts,
        "scores": scores,
        "thresholds": {
            "minimum_operator_usability_score": 0.75,
            "owner_review_required": True,
            "redaction_required": True,
        },
        "operator_usability_score": operator_score,
        "owner_review": {
            "status": owner_review_status,
            "required": True,
        },
        "blocking_reasons": sorted(set(blockers)),
        "boundary_status": "synthetic_only_boundary",
        "promotion_decision": "not_promoted",
        "promotion_boundary": "manual_only_not_promoted",
        "generated_view_policy": "orientation_only_not_proof",
        "source_policy": "first-run scorecard is operator review guidance, not release approval",
    }
    scorecard["scorecard_digest"] = content_digest(canonical_json(scorecard))
    return scorecard


def validate_first_run_artifact_scorecard(scorecard: dict[str, Any]) -> list[str]:
    if not isinstance(scorecard, dict):
        return ["first-run artifact scorecard must be an object"]
    errors: list[str] = []
    if scorecard.get("schema_version") != FIRST_RUN_ARTIFACT_SCORECARD_SCHEMA_VERSION:
        errors.append(f"schema_version must be {FIRST_RUN_ARTIFACT_SCORECARD_SCHEMA_VERSION}")
    if scorecard.get("boundary_status") != "synthetic_only_boundary":
        errors.append("boundary_status must be synthetic_only_boundary")
    if scorecard.get("promotion_decision") != "not_promoted":
        errors.append("promotion_decision must be not_promoted")
    if scorecard.get("generated_view_policy") != "orientation_only_not_proof":
        errors.append("generated_view_policy must be orientation_only_not_proof")
    scores = scorecard.get("scores")
    if not isinstance(scores, dict):
        errors.append("scores must be an object")
        scores = {}
    for key in FIRST_RUN_SCORE_KEYS:
        value = scores.get(key)
        if not isinstance(value, (int, float)) or value < 0 or value > 1:
            errors.append(f"scores.{key} must be between 0 and 1")
    raw_counts = scorecard.get("raw_counts")
    if not isinstance(raw_counts, dict):
        errors.append("raw_counts must be an object")
    owner_review = scorecard.get("owner_review")
    if not isinstance(owner_review, dict) or owner_review.get("required") is not True:
        errors.append("owner_review.required must be true")
    if not str(scorecard.get("scorecard_digest", "")).startswith("sha256:"):
        errors.append("scorecard_digest must be a sha256 digest")
    return errors


def _score_bool(value: Any) -> float:
    return 1.0 if bool(value) else 0.0


def _int(value: Any) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


__all__ = [
    "FIRST_RUN_ARTIFACT_SCORECARD_SCHEMA_VERSION",
    "GATE_GROUPS",
    "build_first_run_artifact_scorecard",
    "build_scorecard_gates",
    "validate_first_run_artifact_scorecard",
    "validate_scorecard_gates",
]
