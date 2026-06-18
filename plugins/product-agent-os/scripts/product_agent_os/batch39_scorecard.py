from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from product_agent_os.stage_manifest import canonical_json, content_digest


SCORECARD_SCHEMA_VERSION = "pilot_product_usability_scorecard_v1"
FIRST_RUN_ARTIFACT_SCORECARD_SCHEMA_VERSION = "first_run_artifact_scorecard_v1"
GRAPH_USEFULNESS_SCORECARD_SCHEMA_VERSION = "graph_usefulness_scorecard_v1"
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
GRAPH_USEFULNESS_METRIC_KEYS = (
    "symbol_recall",
    "top_k_relevance",
    "affected_test_precision",
    "false_positive_rate",
    "reading_scope_reduction",
    "unsupported_language_rate",
    "stale_block_behavior",
    "first_safe_action",
)
GRAPH_USEFULNESS_THRESHOLDS = {
    "min_symbol_recall": 0.8,
    "min_top_k_relevance": 0.75,
    "min_affected_test_precision": 0.8,
    "max_false_positive_rate": 0.1,
    "min_reading_scope_reduction": 0.4,
    "max_unsupported_language_rate": 0.25,
    "require_stale_block_behavior": True,
    "require_first_safe_action": True,
    "require_real_target_comparison_for_promotion": True,
}


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


def build_graph_usefulness_scorecard(
    *,
    test_id: str,
    attempt_id: str,
    metric_summary: dict[str, Any],
    generated_at: str | None = None,
) -> dict[str, Any]:
    summary = metric_summary if isinstance(metric_summary, dict) else {}
    raw_counts = {
        "symbol_queries_total": _int(summary.get("symbol_queries_total")),
        "symbol_queries_hit": _int(summary.get("symbol_queries_hit")),
        "top_k_hits": _int(summary.get("top_k_hits")),
        "affected_tests_expected": _int(summary.get("affected_tests_expected")),
        "affected_tests_matched": _int(summary.get("affected_tests_matched")),
        "affected_tests_false_positive": _int(summary.get("affected_tests_false_positive")),
        "baseline_read_files": _int(summary.get("baseline_read_files")),
        "packet_read_files": _int(summary.get("packet_read_files")),
        "unsupported_language_count": _int(summary.get("unsupported_language_count")),
        "language_count": _int(summary.get("language_count")),
    }
    affected_returned = raw_counts["affected_tests_matched"] + raw_counts["affected_tests_false_positive"]
    metrics = {
        "symbol_recall": _rate(raw_counts["symbol_queries_hit"], raw_counts["symbol_queries_total"]),
        "top_k_relevance": _rate(raw_counts["top_k_hits"], raw_counts["symbol_queries_total"]),
        "affected_test_precision": _rate(raw_counts["affected_tests_matched"], affected_returned),
        "false_positive_rate": _rate(raw_counts["affected_tests_false_positive"], affected_returned),
        "reading_scope_reduction": _scope_reduction(raw_counts["baseline_read_files"], raw_counts["packet_read_files"]),
        "unsupported_language_rate": _rate(raw_counts["unsupported_language_count"], raw_counts["language_count"]),
        "stale_block_behavior": _score_bool(summary.get("stale_block_behavior") is True),
        "first_safe_action": _score_bool(summary.get("safe_next_action_present") is True),
    }
    threshold_results = _graph_threshold_results(metrics)
    metric_blockers = [item["blocker"] for item in threshold_results if item["status"] == "failed"]
    real_target_comparison_present = summary.get("real_target_comparison_present") is True
    blocking_reasons = list(metric_blockers)
    if not real_target_comparison_present:
        blocking_reasons.append("real_target_comparison_missing")
    fixture_status = "fixture_thresholds_passed" if not metric_blockers else "fixture_thresholds_failed"
    scorecard = {
        "schema_version": GRAPH_USEFULNESS_SCORECARD_SCHEMA_VERSION,
        "batch": "B39",
        "task_ids": ["B39-S4-GRAPH-DEPTH-06", "B39-S4-GRAPH-DEPTH-14"],
        "test_id": test_id,
        "attempt_id": attempt_id,
        "generated_at": generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "raw_counts": raw_counts,
        "metrics": metrics,
        "thresholds": GRAPH_USEFULNESS_THRESHOLDS,
        "threshold_results": threshold_results,
        "fixture_evaluation_status": fixture_status,
        "target_comparison": {
            "status": "available" if real_target_comparison_present else "missing",
            "delta": summary.get("target_comparison_delta") if real_target_comparison_present else None,
            "required_for_promotion": True,
        },
        "blocking_reasons": sorted(set(blocking_reasons)),
        "accepted_gaps": [
            "fixture_metrics_are_local_calibration_only",
            "small_target_sets_do_not_prove_broad_semantic_usefulness",
        ],
        "unsupported_claims": [
            "release_readiness",
            "production_readiness",
            "broad_agent_navigation_usefulness",
            "real_target_improvement_without_comparison",
        ],
        "decision_status": "manual_only",
        "promotion_decision": "not_promoted",
        "promotion_boundary": "manual_only_not_promoted",
        "generated_view_policy": "orientation_only_not_proof",
        "source_boundary": "graph_artifact_only_raw_source_excluded",
        "source_policy": "graph scorecard is local calibration evidence, not readiness proof",
    }
    scorecard["scorecard_digest"] = content_digest(canonical_json(scorecard))
    return scorecard


def validate_graph_usefulness_scorecard(scorecard: dict[str, Any]) -> list[str]:
    if not isinstance(scorecard, dict):
        return ["graph usefulness scorecard must be an object"]
    errors: list[str] = []
    if scorecard.get("schema_version") != GRAPH_USEFULNESS_SCORECARD_SCHEMA_VERSION:
        errors.append(f"schema_version must be {GRAPH_USEFULNESS_SCORECARD_SCHEMA_VERSION}")
    if scorecard.get("promotion_decision") != "not_promoted":
        errors.append("promotion_decision must be not_promoted")
    if scorecard.get("promotion_boundary") != "manual_only_not_promoted":
        errors.append("promotion_boundary must be manual_only_not_promoted")
    if scorecard.get("decision_status") != "manual_only":
        errors.append("decision_status must be manual_only")
    if scorecard.get("generated_view_policy") != "orientation_only_not_proof":
        errors.append("generated_view_policy must be orientation_only_not_proof")
    if scorecard.get("source_boundary") != "graph_artifact_only_raw_source_excluded":
        errors.append("source_boundary must be graph_artifact_only_raw_source_excluded")
    metrics = scorecard.get("metrics")
    if not isinstance(metrics, dict):
        errors.append("metrics must be an object")
        metrics = {}
    for key in GRAPH_USEFULNESS_METRIC_KEYS:
        value = metrics.get(key)
        if not isinstance(value, (int, float)) or value < 0 or value > 1:
            errors.append(f"metrics.{key} must be between 0 and 1")
    thresholds = scorecard.get("thresholds")
    if not isinstance(thresholds, dict):
        errors.append("thresholds must be an object")
    target_comparison = scorecard.get("target_comparison")
    if not isinstance(target_comparison, dict) or target_comparison.get("required_for_promotion") is not True:
        errors.append("target_comparison.required_for_promotion must be true")
    if "release_readiness" not in set(scorecard.get("unsupported_claims", [])):
        errors.append("unsupported_claims must include release_readiness")
    if not str(scorecard.get("scorecard_digest", "")).startswith("sha256:"):
        errors.append("scorecard_digest must be a sha256 digest")
    return errors


def _graph_threshold_results(metrics: dict[str, float]) -> list[dict[str, Any]]:
    threshold_checks = [
        ("symbol_recall", ">=", GRAPH_USEFULNESS_THRESHOLDS["min_symbol_recall"], "symbol_recall_below_threshold"),
        ("top_k_relevance", ">=", GRAPH_USEFULNESS_THRESHOLDS["min_top_k_relevance"], "top_k_relevance_below_threshold"),
        (
            "affected_test_precision",
            ">=",
            GRAPH_USEFULNESS_THRESHOLDS["min_affected_test_precision"],
            "affected_test_precision_below_threshold",
        ),
        ("false_positive_rate", "<=", GRAPH_USEFULNESS_THRESHOLDS["max_false_positive_rate"], "false_positive_rate_above_threshold"),
        (
            "reading_scope_reduction",
            ">=",
            GRAPH_USEFULNESS_THRESHOLDS["min_reading_scope_reduction"],
            "reading_scope_reduction_below_threshold",
        ),
        (
            "unsupported_language_rate",
            "<=",
            GRAPH_USEFULNESS_THRESHOLDS["max_unsupported_language_rate"],
            "unsupported_language_rate_above_threshold",
        ),
        ("stale_block_behavior", ">=", 1.0, "stale_block_behavior_missing"),
        ("first_safe_action", ">=", 1.0, "first_safe_action_missing"),
    ]
    results = []
    for metric, operator, threshold, blocker in threshold_checks:
        value = metrics.get(metric, 0.0)
        passed = value >= threshold if operator == ">=" else value <= threshold
        results.append(
            {
                "metric": metric,
                "operator": operator,
                "threshold": threshold,
                "value": value,
                "status": "passed" if passed else "failed",
                "blocker": "" if passed else blocker,
            }
        )
    return results


def _score_bool(value: Any) -> float:
    return 1.0 if bool(value) else 0.0


def _rate(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(max(0.0, min(1.0, numerator / denominator)), 3)


def _scope_reduction(baseline: int, packet: int) -> float:
    if baseline <= 0:
        return 0.0
    return round(max(0.0, min(1.0, (baseline - packet) / baseline)), 3)


def _int(value: Any) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


__all__ = [
    "FIRST_RUN_ARTIFACT_SCORECARD_SCHEMA_VERSION",
    "GATE_GROUPS",
    "GRAPH_USEFULNESS_SCORECARD_SCHEMA_VERSION",
    "build_first_run_artifact_scorecard",
    "build_graph_usefulness_scorecard",
    "build_scorecard_gates",
    "validate_first_run_artifact_scorecard",
    "validate_graph_usefulness_scorecard",
    "validate_scorecard_gates",
]
