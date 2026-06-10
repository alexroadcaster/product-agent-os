"""Read-only agent and skill metrics-loop foundation for Product-Agent OS."""

from __future__ import annotations

import json
import math
import re
from datetime import date
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import redact_payload, validate_redaction


METRICS_PACKET_LIMITS = {
    "targets": 20,
    "evidence_records": 80,
    "questions": 8,
    "update_candidates": 12,
    "embedded_json_bytes": 12_000,
}

_SOURCE_OF_TRUTH = [
    "control_plane",
    "run_record",
    "trace_packet",
    "eval_packet",
    "accepted_gap",
]
_GENERATED_REVIEW_ONLY = [
    "status_dashboard_html",
    "metrics_report_html",
    "generated_report_html",
]
_REJECTED_SOURCES = [
    "memory",
    "raw_chat_log",
    "unsupported_community_claim",
]
_CONTROL_PLANE_FILES = {"AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"}
_EVAL_HINTS = ("fixture eval", "transcript eval", "eval summary", "eval-run-report")
_DATE_PATTERN = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
_KEY_VALUE_PATTERN = re.compile(r"^\s*([A-Za-z0-9_-]+)\s*[:=]\s*\"?([^\"\r\n]+)\"?\s*$")
_SUPPORTED_TRACE_SOURCE_TYPES = {"agents_sdk", "opentelemetry_genai", "tool_report", "accepted_gap"}
_TRACE_REQUIRED_SPAN_TYPES = ["model", "tool", "handoff", "final_response"]
_RAW_PROMPT_KEYS = {"prompt", "raw_prompt", "system_prompt", "user_prompt"}
_RAW_TOOL_OUTPUT_KEYS = {"tool_output", "raw_tool_output", "tool_outputs", "raw_tool_outputs"}
_BLOCKED_REDACTION_OPERATIONS = [
    "dataset_builder",
    "ledger",
    "report_rendering",
    "scoring",
    "update_candidates",
]


def source_priority_policy() -> dict[str, Any]:
    """Return the source-priority contract for metrics-loop evidence."""

    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "source_of_truth": list(_SOURCE_OF_TRUTH),
        "generated_review_only": list(_GENERATED_REVIEW_ONLY),
        "rejected": list(_REJECTED_SOURCES),
        "generated_view_success_claim_policy": "never",
        "notes": [
            "HTML dashboards and reports are generated review views only.",
            "Memory and raw chat logs are recall material, not evidence.",
            "Community claims require verification before evidence use.",
        ],
    }


def collect_target_registry(workspace: str | Path) -> dict[str, Any]:
    """Collect local agentic targets without external calls or workspace writes."""

    root = Path(workspace)
    targets: list[dict[str, Any]] = []
    targets.extend(_agent_targets(root))
    targets.extend(_skill_targets(root))
    targets.extend(_artifact_policy_targets(root))
    targets.extend(_automation_candidate_targets(root))
    targets.extend(_config_targets(root))
    targets.extend(_harness_targets(root))
    targets = _dedupe_targets(targets)
    targets = _bounded_list(targets, "target_id", METRICS_PACKET_LIMITS["targets"])
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "policy": source_priority_policy(),
        "targets": targets,
        "summary": {
            "total": len(targets),
            "by_type": _counts(targets, "target_type"),
            "no_data": sum(1 for target in targets if target.get("no_data_status") != "metrics_data_present"),
        },
        "warnings": [],
    }
    return _redacted_dict(packet)


def build_evidence_packet(
    workspace: str | Path,
    *,
    as_of_date: str = "",
    max_records: int | None = None,
    evidence_max_age_days: int = 14,
) -> dict[str, Any]:
    """Build a bounded evidence packet from explicit project artifacts only."""

    root = Path(workspace)
    records: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    for path in _evidence_candidate_paths(root):
        relative = _relative_path(root, path)
        excluded_type = _excluded_source_type(relative)
        if excluded_type:
            excluded.append(_excluded_record(relative, excluded_type))
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        records.extend(_records_from_text(relative, text, as_of_date, evidence_max_age_days))

    limit = max_records or METRICS_PACKET_LIMITS["evidence_records"]
    bounded, warnings = _trim_records(records, limit, "evidence_records")
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "as_of_date": as_of_date,
        "policy": source_priority_policy(),
        "evidence_records": bounded,
        "excluded_records": sorted(excluded, key=lambda item: (item["source_type"], item["source_path"])),
        "summary": {
            "total": len(bounded),
            "by_source_type": _counts(bounded, "source_type"),
            "excluded": len(excluded),
        },
        "warnings": warnings,
    }
    return _redacted_dict(packet)


def build_metrics_packet(
    *,
    targets: list[dict[str, Any]] | None = None,
    evidence_records: list[dict[str, Any]] | None = None,
    questions: list[dict[str, Any]] | None = None,
    update_candidates: list[dict[str, Any]] | None = None,
    embedded_json: Any | None = None,
) -> dict[str, Any]:
    """Build a bounded metrics-loop packet safe for later routing or rendering."""

    warnings: list[str] = []
    bounded_targets, target_warnings = _trim_items(
        targets or [],
        METRICS_PACKET_LIMITS["targets"],
        "targets",
    )
    bounded_evidence, evidence_warnings = _trim_items(
        evidence_records or [],
        METRICS_PACKET_LIMITS["evidence_records"],
        "evidence_records",
    )
    bounded_questions, question_warnings = _trim_items(
        questions or [],
        METRICS_PACKET_LIMITS["questions"],
        "questions",
    )
    bounded_candidates, candidate_warnings = _trim_items(
        update_candidates or [],
        METRICS_PACKET_LIMITS["update_candidates"],
        "update_candidates",
    )
    warnings.extend(target_warnings)
    warnings.extend(evidence_warnings)
    warnings.extend(question_warnings)
    warnings.extend(candidate_warnings)
    embedded, embedded_warnings = _bounded_embedded_json(embedded_json)
    warnings.extend(embedded_warnings)

    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "limits": dict(METRICS_PACKET_LIMITS),
        "policy": source_priority_policy(),
        "targets": bounded_targets,
        "evidence_records": bounded_evidence,
        "questions": bounded_questions,
        "update_candidates": bounded_candidates,
        "embedded_json": embedded,
        "warnings": sorted(set(warnings)),
    }
    return _redacted_dict(packet)


def build_trace_packet(
    *,
    trace_sources: list[dict[str, Any]] | None = None,
    max_traces: int | None = None,
) -> dict[str, Any]:
    """Normalize supported trace evidence into a portable read-only packet."""

    warnings: list[str] = []
    traces: list[dict[str, Any]] = []
    for index, source in enumerate(trace_sources or []):
        trace, trace_warnings = _normalize_trace_source(source, index)
        traces.append(trace)
        warnings.extend(trace_warnings)

    limit = max_traces or METRICS_PACKET_LIMITS["evidence_records"]
    bounded, trim_warnings = _trim_items(traces, limit, "traces")
    warnings.extend(trim_warnings)
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "policy": source_priority_policy(),
        "traces": bounded,
        "summary": {
            "total": len(bounded),
            "by_status": _counts(bounded, "status"),
            "by_trace_source_type": _counts(bounded, "trace_source_type"),
            "replayable": sum(
                1 for trace in bounded if trace.get("replayability", {}).get("status") == "replayable"
            ),
        },
        "warnings": sorted(set(warnings)),
    }
    return _redacted_dict(packet)


def enforce_metrics_redaction_gate(packet: dict[str, Any]) -> dict[str, Any]:
    """Redact unsafe metrics-loop payloads and block downstream use when needed."""

    _preflight_redacted, preflight_report = redact_payload(packet)
    sanitized, raw_report = _sanitize_raw_metrics_payload(packet)
    redacted, report = redact_payload(sanitized)
    rendered = json.dumps(redacted, sort_keys=True, default=str)
    validation_errors = validate_redaction(rendered)
    categories = set(str(item) for item in report.get("categories", []))
    categories.update(str(item) for item in preflight_report.get("categories", []))
    categories.update(str(item) for item in raw_report["categories"])
    categories.update(error.split(":", 1)[-1] for error in validation_errors)
    redaction_count = int(preflight_report.get("count", 0)) + int(report.get("count", 0)) + int(raw_report["count"])
    blocked_operations = list(_BLOCKED_REDACTION_OPERATIONS) if categories or validation_errors else []
    safety_status = "blocked_pending_review" if blocked_operations else "ready"
    result = {
        "schema_version": 1,
        "write_policy": "read_only",
        "safety_status": safety_status,
        "redacted_packet": redacted,
        "redaction_summary": {
            "count": redaction_count,
            "categories": sorted(categories),
            "validation_errors": sorted(set(validation_errors)),
        },
        "blocked_operations": blocked_operations,
    }
    final, final_report = redact_payload(result)
    if isinstance(final, dict) and final_report.get("count"):
        final["final_redaction_summary"] = final_report
    return final if isinstance(final, dict) else result


def build_evidence_dataset(
    *,
    implemented_tasks: list[dict[str, Any]] | None = None,
    trace_packet: dict[str, Any] | None = None,
    prior_failures: list[dict[str, Any]] | None = None,
    critical_slices: list[dict[str, Any]] | None = None,
    edge_cases: list[dict[str, Any]] | None = None,
    holdout_cases: list[dict[str, Any]] | None = None,
    synthetic_regression_cases: list[dict[str, Any]] | None = None,
    known_flaky_cases: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a stratified local evidence dataset without mixing holdout labels."""

    records: list[dict[str, Any]] = []
    records.extend(_dataset_records(implemented_tasks or [], "implemented_task", "implemented_task"))
    records.extend(_trace_dataset_records((trace_packet or {}).get("traces", [])))
    records.extend(_dataset_records(prior_failures or [], "prior_failure", "prior_failure"))
    records.extend(_dataset_records(critical_slices or [], "critical_slice", "critical"))
    records.extend(_dataset_records(edge_cases or [], "edge_adversarial", "edge_adversarial"))
    records.extend(_dataset_records(holdout_cases or [], "holdout", "holdout"))
    records.extend(
        _dataset_records(
            synthetic_regression_cases or [],
            "synthetic_regression",
            "synthetic_regression",
            synthetic_default=True,
        )
    )
    records.extend(_dataset_records(known_flaky_cases or [], "known_flaky", "flaky"))
    records = sorted(records, key=lambda item: (str(item.get("sample_id")), str(item.get("split")), str(item.get("group"))))
    duplicate_sample_ids = _duplicate_sample_ids(records)
    leakage_sample_ids = _leakage_sample_ids(records)
    total = len(records)
    duplicate_rate = len(duplicate_sample_ids) / total if total else 0.0
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "records": records,
        "source_counts": _counts(records, "group"),
        "split_summary": _counts(records, "split"),
        "dataset_duplicate_rate": round(duplicate_rate, 4),
        "duplicate_sample_ids": duplicate_sample_ids,
        "leakage_status": "leakage_detected" if leakage_sample_ids else "no_leakage_detected",
        "leakage_sample_ids": leakage_sample_ids,
        "holdout_policy": "separate_from_training_and_prior_failure_labels",
        "prior_failure_policy": "kept_as_prior_failure_split_not_holdout_success",
    }
    return _redacted_dict(packet)


def evaluate_dataset_quality(
    dataset_packet: dict[str, Any],
    *,
    min_samples: int = 8,
    min_real_trace_samples: int = 1,
    max_duplicate_rate: float = 0.1,
) -> dict[str, Any]:
    """Evaluate dataset sufficiency before confident metrics-loop decisions."""

    records = list(dataset_packet.get("records", []))
    coverage = _counts(records, "group")
    expected_splits = [
        "implemented_task",
        "real_trace_sample",
        "prior_failure",
        "critical_slice",
        "holdout",
        "synthetic_regression",
    ]
    missing_expected_splits = [split for split in expected_splits if coverage.get(split, 0) == 0]
    duplicate_rate = float(dataset_packet.get("dataset_duplicate_rate") or 0.0)
    leakage_status = str(dataset_packet.get("leakage_status") or "unknown")
    low_real_trace_coverage = coverage.get("real_trace_sample", 0) < min_real_trace_samples
    insufficient_sample = len(records) < min_samples
    blockers = []
    if missing_expected_splits:
        blockers.append("missing_expected_splits")
    if duplicate_rate > max_duplicate_rate:
        blockers.append("duplicate_rate_exceeded")
    if leakage_status == "leakage_detected":
        blockers.append("leakage_detected")
    if low_real_trace_coverage:
        blockers.append("low_real_trace_coverage")
    if insufficient_sample:
        blockers.append("insufficient_sample")
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "decision_status": "blocked_insufficient_dataset" if blockers else "ready",
        "blockers": blockers,
        "dataset_coverage": coverage,
        "dataset_duplicate_rate": duplicate_rate,
        "leakage_status": leakage_status,
        "missing_expected_splits": missing_expected_splits,
        "low_real_trace_coverage": low_real_trace_coverage,
        "insufficient_sample": insufficient_sample,
        "sample_size": len(records),
        "thresholds": {
            "min_samples": min_samples,
            "min_real_trace_samples": min_real_trace_samples,
            "max_duplicate_rate": max_duplicate_rate,
        },
    }
    return _redacted_dict(packet)


def build_grader_run_summary(
    *,
    metric_graders: list[dict[str, Any]] | None = None,
    trace_graders: list[dict[str, Any]] | None = None,
    human_audits: list[dict[str, Any]] | None = None,
    llm_judges: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Summarize local grader outputs and metadata-only judge contracts."""

    graders: list[dict[str, Any]] = []
    graders.extend(_grader_records(metric_graders or [], "metric"))
    graders.extend(_grader_records(trace_graders or [], "trace"))
    graders.extend(_human_audit_records(human_audits or []))
    unsupported_gaps: list[str] = []
    for judge in llm_judges or []:
        mode = str(judge.get("mode") or "metadata_only")
        if mode == "live_model_call":
            unsupported_gaps.append("unsupported_live_judge")
            continue
        graders.append(
            _grader_record(
                "llm_as_judge_metadata",
                str(judge.get("rubric_id") or "unassigned"),
                int(judge.get("sample_size") or 0),
                source_status="metadata_only_no_live_call",
            )
        )
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "external_calls": "not_performed",
        "graders": sorted(graders, key=lambda item: (item["grader_type"], item["rubric_id"])),
        "summary": {
            "total": len(graders),
            "by_grader_type": _counts(graders, "grader_type"),
            "sample_size": sum(int(grader.get("sample_size") or 0) for grader in graders),
        },
        "unsupported_gaps": sorted(set(unsupported_gaps)),
    }
    return _redacted_dict(packet)


def build_judge_calibration_summary(
    *,
    judge_labels: list[str] | None = None,
    human_labels: list[str] | None = None,
    min_sample_size: int = 20,
    min_precision: float = 0.8,
    min_recall: float = 0.8,
    min_kappa: float = 0.6,
) -> dict[str, Any]:
    """Compute judge calibration metrics and block approvals when not calibrated."""

    pairs = list(zip(judge_labels or [], human_labels or []))
    counts = _binary_label_counts(pairs)
    sample_size = len(pairs)
    agreement = _safe_ratio(counts["tp"] + counts["tn"], sample_size)
    precision = _safe_ratio(counts["tp"], counts["tp"] + counts["fp"])
    recall = _safe_ratio(counts["tp"], counts["tp"] + counts["fn"])
    kappa = _cohen_kappa(counts, sample_size, agreement)
    calibrated = (
        sample_size >= min_sample_size
        and precision >= min_precision
        and recall >= min_recall
        and kappa >= min_kappa
    )
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "status": "calibrated" if calibrated else "judge_not_calibrated",
        "blocks_candidate_approval": not calibrated,
        "judge_derived_metrics_policy": "may_support_review" if calibrated else "reportable_gap_only",
        "sample_size": sample_size,
        "min_sample_size": min_sample_size,
        "judge_human_agreement": round(agreement, 4),
        "judge_precision": round(precision, 4),
        "judge_recall": round(recall, 4),
        "cohen_kappa": round(kappa, 4),
        "confusion_matrix": counts,
        "thresholds": {
            "min_precision": min_precision,
            "min_recall": min_recall,
            "min_kappa": min_kappa,
        },
    }
    return _redacted_dict(packet)


def build_metric_aggregation(
    *,
    outcome_records: list[dict[str, Any]] | None = None,
    trajectory_records: list[dict[str, Any]] | None = None,
    reliability_records: list[dict[str, Any]] | None = None,
    skill_records: list[dict[str, Any]] | None = None,
    cost_latency_records: list[dict[str, Any]] | None = None,
    safety_records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Aggregate raw metrics into bounded sections with numerator and denominator evidence."""

    outcome = outcome_records or []
    trajectory = trajectory_records or []
    reliability = reliability_records or []
    skills = skill_records or []
    cost_latency = cost_latency_records or []
    safety = safety_records or []
    sections = {
        "outcome": _metric_section(
            "outcome",
            [
                _boolean_rate_metric("task_success_rate", outcome, "task_success"),
                _boolean_rate_metric("regression_free_success_rate", outcome, "regression_free"),
                _boolean_rate_metric("final_state_accuracy", outcome, "final_state_correct"),
                _boolean_rate_metric("false_pass_rate", outcome, "false_pass", higher_is_better=False),
                _boolean_rate_metric("false_fail_rate", outcome, "false_fail", higher_is_better=False),
            ],
        ),
        "trajectory": _metric_section(
            "trajectory",
            [
                _boolean_rate_metric("tool_selection_accuracy", trajectory, "tool_selection_correct"),
                _boolean_rate_metric("tool_argument_accuracy", trajectory, "tool_argument_correct"),
                _boolean_rate_metric("trace_completeness", trajectory, "trace_complete"),
                _boolean_rate_metric("replayable_trace_rate", trajectory, "replayable_trace"),
            ],
        ),
        "harness_reliability": _metric_section(
            "harness_reliability",
            [
                _boolean_rate_metric("flake_rate", reliability, "flake", higher_is_better=False),
                _boolean_rate_metric("replay_success_rate", reliability, "replay_success"),
                _boolean_rate_metric(
                    "repeated_run_instability",
                    reliability,
                    "repeated_run_instability",
                    higher_is_better=False,
                ),
            ],
        ),
        "harness_optimizer": _metric_section(
            "harness_optimizer",
            [
                _cost_regression_metric(cost_latency),
                _latency_regression_metric(cost_latency),
                _cost_improvement_metric(cost_latency),
            ],
        ),
        "skill": _metric_section(
            "skill",
            [
                _skill_trigger_recall(skills),
                _skill_trigger_precision(skills),
                _boolean_rate_metric("skill_adherence_rate", skills, "skill_adhered"),
            ],
        ),
        "cost_latency": _metric_section(
            "cost_latency",
            [
                _sum_metric("total_cost_usd", cost_latency, "cost_usd"),
                _average_metric("average_cost_usd", cost_latency, "cost_usd"),
                _average_metric("average_latency_ms", cost_latency, "latency_ms"),
                _percentile_metric("p95_latency_ms", cost_latency, "latency_ms", 0.95),
            ],
        ),
        "safety": _metric_section(
            "safety",
            [
                _boolean_rate_metric("instruction_violation_rate", safety, "instruction_violation", higher_is_better=False),
                _boolean_rate_metric("approval_violation_rate", safety, "approval_violation", higher_is_better=False),
                _boolean_rate_metric("private_data_leak_rate", safety, "private_data_leak", higher_is_better=False),
                _any_safety_violation_metric(safety),
            ],
        ),
    }
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "sections": sections,
        "summary": {
            "section_count": len(sections),
            "ready_metrics": sum(
                1
                for section in sections.values()
                for metric in section["metrics"].values()
                if metric["status"] == "ready"
            ),
            "insufficient_metrics": sum(
                1
                for section in sections.values()
                for metric in section["metrics"].values()
                if metric["status"] == "insufficient_data"
            ),
        },
    }
    return _redacted_dict(packet)


def calculate_repeatability_metrics(
    *,
    replay_cases: list[dict[str, Any]] | None = None,
    k: int = 3,
) -> dict[str, Any]:
    """Calculate repeatability metrics only from replayable repeated-run evidence."""

    cases = replay_cases or []
    eligible_cases: list[dict[str, Any]] = []
    single_success_cases: list[str] = []
    total_replay_runs = 0
    successful_replay_runs = 0
    for case in cases:
        runs = case.get("runs") if isinstance(case.get("runs"), list) else []
        if len(runs) == 1 and bool(runs[0].get("passed")):
            single_success_cases.append(str(case.get("case_id") or "case"))
        if len(runs) < 2:
            continue
        bounded_runs = runs[: max(1, k)]
        total_replay_runs += len(bounded_runs)
        successful_replay_runs += sum(1 for run in bounded_runs if bool(run.get("replay_success")))
        eligible_cases.append({"case_id": str(case.get("case_id") or "case"), "runs": bounded_runs})

    pass_at_k = sum(1 for case in eligible_cases if any(bool(run.get("passed")) for run in case["runs"]))
    pass_power_k = sum(1 for case in eligible_cases if all(bool(run.get("passed")) for run in case["runs"]))
    unstable = sum(1 for case in eligible_cases if _case_has_instability(case["runs"]))
    denominator = len(eligible_cases)
    insufficient_reasons: list[str] = []
    if not cases:
        insufficient_reasons.append("no_replay_evidence")
    if not eligible_cases:
        insufficient_reasons.append("insufficient_repeated_runs")
    if single_success_cases:
        insufficient_reasons.append("single_lucky_run")
    status = "ready" if eligible_cases else "insufficient_replay_evidence"
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "status": status,
        "k": k,
        "metrics": {
            "pass_at_k": _ratio_metric("pass_at_k", pass_at_k, denominator),
            "pass_power_k": _ratio_metric("pass_power_k", pass_power_k, denominator),
            "replay_success_rate": _ratio_metric("replay_success_rate", successful_replay_runs, total_replay_runs),
            "repeated_run_instability": _ratio_metric(
                "repeated_run_instability",
                unstable,
                denominator,
                higher_is_better=False,
            ),
        },
        "insufficient_reasons": sorted(set(insufficient_reasons)),
        "promotion_policy": {
            "single_success_promotion": "blocked",
            "decision": "blocked_single_lucky_run" if single_success_cases and not eligible_cases else "repeatability_required",
        },
    }
    return _redacted_dict(packet)


def calculate_scorecards(
    *,
    metric_packet: dict[str, Any],
    weights: dict[str, dict[str, float]] | None = None,
) -> dict[str, Any]:
    """Calculate scorecards while surfacing guardrail blockers separately from headline scores."""

    scorecard_weights = weights or _default_scorecard_weights()
    scorecards = {
        scorecard_id: _scorecard(scorecard_id, metric_packet, component_weights)
        for scorecard_id, component_weights in scorecard_weights.items()
    }
    guardrail_metrics = _guardrail_metrics(metric_packet)
    guardrail_blockers = _guardrail_blockers(guardrail_metrics)
    all_missing = all(scorecard["status"] == "insufficient_data" for scorecard in scorecards.values())
    if guardrail_blockers:
        overall_status = "blocked_by_guardrail"
    elif all_missing:
        overall_status = "insufficient_data"
    else:
        overall_status = "ready"
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "scorecards": scorecards,
        "overall_status": overall_status,
        "guardrail_blockers": guardrail_blockers,
        "guardrail_metrics": guardrail_metrics,
        "headline_policy": "headline_scores_cannot_override_guardrails",
    }
    return _redacted_dict(packet)


def evaluate_confidence_and_decision_gates(
    *,
    current_metric_packet: dict[str, Any],
    baseline_metric_packet: dict[str, Any] | None = None,
    owner_review_status: str = "",
    critical_regressions: list[str] | None = None,
    thresholds: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Evaluate weekly acceptance confidence and guardrail gates."""

    active_thresholds = {
        "min_sample_size": 30.0,
        "min_wilson_lower_bound": 0.75,
        "max_false_pass_rate": 0.02,
        "max_flake_rate": 0.02,
        "min_trace_completeness": 0.95,
        "max_cost_regression_rate": 0.05,
        "max_safety_violation_rate": 0.0,
    }
    active_thresholds.update(thresholds or {})
    task_success = _metric_lookup(current_metric_packet, "task_success_rate")
    baseline_success = _metric_lookup(baseline_metric_packet or {}, "task_success_rate")
    sample_size = int(task_success.get("denominator") or 0)
    success_count = int(task_success.get("numerator") or 0)
    wilson_lower = _wilson_lower_bound(success_count, sample_size)
    delta = _metric_value(task_success) - _metric_value(baseline_success) if baseline_success else 0.0
    metrics = {
        "task_success_rate": {
            "numerator": success_count,
            "denominator": sample_size,
            "wilson_lower_bound": round(wilson_lower, 4),
            "delta_vs_baseline": round(delta, 4),
        }
    }
    blockers: list[str] = []
    if sample_size < int(active_thresholds["min_sample_size"]):
        blockers.append("insufficient_sample")
    if wilson_lower < active_thresholds["min_wilson_lower_bound"]:
        blockers.append("confidence_lower_bound_below_threshold")
    if critical_regressions:
        blockers.append("critical_regression")
    if _metric_value(_metric_lookup(current_metric_packet, "false_pass_rate")) > active_thresholds["max_false_pass_rate"]:
        blockers.append("false_pass_threshold_exceeded")
    if _metric_value(_metric_lookup(current_metric_packet, "flake_rate")) > active_thresholds["max_flake_rate"]:
        blockers.append("flake_threshold_exceeded")
    if _metric_value(_metric_lookup(current_metric_packet, "trace_completeness")) < active_thresholds["min_trace_completeness"]:
        blockers.append("trace_completeness_below_threshold")
    if _metric_value(_metric_lookup(current_metric_packet, "cost_regression_rate")) > active_thresholds["max_cost_regression_rate"]:
        blockers.append("cost_regression_threshold_exceeded")
    if _metric_value(_metric_lookup(current_metric_packet, "safety_violation_rate")) > active_thresholds["max_safety_violation_rate"]:
        blockers.append("safety_violation")
    if owner_review_status not in {"owner_reviewed", "accepted_gap"}:
        blockers.append("owner_review_or_gap_missing")
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "decision_status": "blocked_by_gate" if blockers else "weekly_acceptance_ready",
        "blockers": sorted(set(blockers)),
        "critical_regressions": critical_regressions or [],
        "owner_review_status": owner_review_status or "missing",
        "statistical_evidence": metrics,
        "thresholds": active_thresholds,
        "weekly_acceptance_policy": {
            "requires_confidence_evidence": True,
            "requires_zero_critical_regressions": True,
            "requires_owner_review_or_gap": True,
        },
    }
    return _redacted_dict(packet)


def recommend_metrics_cadence(
    *,
    target: dict[str, Any],
    metrics_summary: dict[str, Any] | None = None,
    owner_override: str = "",
) -> dict[str, Any]:
    """Recommend a metrics cadence as policy guidance without creating active schedules."""

    metrics = metrics_summary or {}
    reasons: list[str] = []
    level = "L0"
    risk = str(target.get("risk_level") or "unknown").lower()
    usage = str(target.get("usage_volume") or "unknown").lower()
    permission = str(target.get("tool_permission_level") or "unknown").lower()
    production_impact = bool(target.get("production_impact"))
    target_type = str(target.get("target_type") or "")
    flake_rate = float(metrics.get("flake_rate") or 0.0)
    trace_completeness = float(metrics.get("trace_completeness") or 1.0)
    if risk == "high" or usage == "high" or permission in {"approval_bound", "write", "workspace_tools"}:
        level = "L2"
        reasons.append("elevated_target_risk_or_permissions")
    if production_impact or target_type == "automation_candidate" or flake_rate > 0.1 or trace_completeness < 0.8:
        level = "L3"
        reasons.append("production_or_reliability_risk")
    elif level == "L0" and (risk == "medium" or usage == "medium" or flake_rate > 0.03 or trace_completeness < 0.95):
        level = "L1"
        reasons.append("periodic_review_needed")
    if owner_override in {"L0", "L1", "L2", "L3"}:
        level = owner_override
        reasons.append("owner_override")
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "target": _json_ready(target),
        "cadence_level": level,
        "recommended_cadence": _cadence_for_level(level),
        "reasons": sorted(set(reasons)) or ["low_risk_on_change_only"],
        "schedule_policy": "suggested_only",
        "active_schedule_status": "approval_required",
        "automation_boundary": "candidate_only_until_owner_approval",
    }
    return _redacted_dict(packet)


def build_metrics_run_record(
    *,
    run_id: str,
    generated_at: str,
    cadence: dict[str, Any],
    window: dict[str, Any],
    dataset_split: str,
    target: dict[str, Any],
    versions: dict[str, Any],
    model: str,
    reasoning_effort: str,
    repo_sha: str = "",
    repo_sha_gap: dict[str, Any] | None = None,
    environment: dict[str, Any] | None = None,
    trace_metadata: dict[str, Any] | None = None,
    artifacts: list[dict[str, Any]] | None = None,
    scores: dict[str, Any] | None = None,
    statistical_evidence: dict[str, Any] | None = None,
    cost_latency: dict[str, Any] | None = None,
    update_decision: dict[str, Any] | None = None,
    review: dict[str, Any] | None = None,
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic JSON-ready run record for staged metrics review."""

    accepted_artifacts, excluded_artifacts = _partition_run_artifacts(artifacts or [])
    redaction_gate = enforce_metrics_redaction_gate(evidence or {})
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "run_id": str(run_id),
        "generated_at": str(generated_at),
        "cadence": _json_ready(cadence),
        "window": _json_ready(window),
        "dataset_split": str(dataset_split),
        "target": _json_ready(target),
        "versions": _json_ready(versions),
        "model": str(model),
        "reasoning_effort": str(reasoning_effort),
        "repo": _repo_record(repo_sha, repo_sha_gap or {}),
        "environment": _json_ready(environment or {}),
        "trace_metadata": _json_ready(trace_metadata or {}),
        "artifacts": accepted_artifacts,
        "excluded_artifacts": excluded_artifacts,
        "artifact_policy": {
            "dashboard_as_source_claim": "rejected",
            "generated_views": list(_GENERATED_REVIEW_ONLY),
            "source_of_truth": list(_SOURCE_OF_TRUTH),
        },
        "scores": _json_ready(scores or {}),
        "statistical_evidence": _json_ready(statistical_evidence or {}),
        "cost_latency": _json_ready(cost_latency or {}),
        "update_decision": _json_ready(update_decision or {}),
        "review": _json_ready(review or {}),
        "evidence": redaction_gate.get("redacted_packet", {}),
        "evidence_safety_status": redaction_gate.get("safety_status", "ready"),
        "evidence_redaction_summary": redaction_gate.get("redaction_summary", {}),
    }
    return _redacted_dict(packet)


def enforce_trace_data_classification_gate(
    trace_packet: dict[str, Any],
    *,
    data_classification_register_present: bool = False,
    secrets_policy_present: bool = False,
    accepted_gap: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Block real trace ingestion unless data classification, secrets policy or gap exists."""

    traces = trace_packet.get("traces") if isinstance(trace_packet.get("traces"), list) else []
    real_traces = [
        trace
        for trace in traces
        if isinstance(trace, dict) and not bool(trace.get("synthetic")) and trace.get("trace_source_type") != "accepted_gap"
    ]
    policy_present = data_classification_register_present or secrets_policy_present
    gap_present = isinstance(accepted_gap, dict) and bool(accepted_gap.get("owner")) and bool(accepted_gap.get("reason"))
    blocked_trace_ids = [] if policy_present or gap_present else [_trace_id(trace) for trace in real_traces]
    allowed_trace_ids = [
        _trace_id(trace)
        for trace in traces
        if isinstance(trace, dict) and _trace_id(trace) not in set(blocked_trace_ids)
    ]
    blockers = ["real_trace_requires_data_classification_or_gap"] if blocked_trace_ids else []
    status = "blocked" if blocked_trace_ids else "accepted_gap" if gap_present and real_traces else "ready"
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "status": status,
        "blockers": blockers,
        "blocked_trace_ids": blocked_trace_ids,
        "allowed_trace_ids": allowed_trace_ids,
        "required_artifacts": ["data-classification-register.md", "secrets-policy.md"],
        "policy": {
            "real_trace_requires_data_classification": True,
            "synthetic_fixtures_allowed_when_marked": True,
            "data_classification_register_present": bool(data_classification_register_present),
            "secrets_policy_present": bool(secrets_policy_present),
            "accepted_gap": _json_ready(accepted_gap or {}) if gap_present else {},
        },
    }
    return _redacted_dict(packet)


def build_scorecard_ledger_record(
    *,
    ledger_id: str,
    generated_at: str,
    baseline_version: dict[str, Any] | None = None,
    current_version: dict[str, Any] | None = None,
    candidate_version: dict[str, Any] | None = None,
    run_record_ids: list[str] | None = None,
    raw_counts: dict[str, Any] | None = None,
    confidence_intervals: dict[str, Any] | None = None,
    cost_latency: dict[str, Any] | None = None,
    evidence_links: list[str] | None = None,
    redaction_status: str = "unknown",
    report_anchors: list[str] | None = None,
) -> dict[str, Any]:
    """Build a deterministic append-only scorecard ledger entry."""

    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "ledger_id": str(ledger_id),
        "generated_at": str(generated_at),
        "ledger_policy": "append_only",
        "baseline_version": _json_ready(baseline_version or {}),
        "current_version": _json_ready(current_version or {}),
        "candidate_version": _json_ready(candidate_version or {}),
        "run_record_ids": sorted(str(item) for item in run_record_ids or []),
        "raw_counts": _json_ready(raw_counts or {}),
        "confidence_intervals": _json_ready(confidence_intervals or {}),
        "cost_latency": _json_ready(cost_latency or {}),
        "evidence_links": sorted(str(item) for item in evidence_links or []),
        "redaction_status": str(redaction_status or "unknown"),
        "report_anchors": sorted(str(item) for item in report_anchors or []),
        "no_secrets_policy": "no raw secrets, private customer data, raw prompts, or raw tool outputs",
    }
    return _redacted_dict(packet)


def build_completion_skeptic_metrics_loop_record(
    *,
    generated_at: str,
    pilot_ledger: dict[str, Any],
    scorecard_calibration: dict[str, Any],
    closure_packet: dict[str, Any],
    evidence_links: list[str] | None = None,
) -> dict[str, Any]:
    """Adapt completion-skeptic calibration evidence into the append-only metrics ledger."""

    metric_evidence = scorecard_calibration.get("metric_evidence")
    raw_counts = _json_ready(metric_evidence if isinstance(metric_evidence, dict) else {})
    record = build_scorecard_ledger_record(
        ledger_id="completion_skeptic_scorecard_calibration",
        generated_at=generated_at,
        baseline_version={"completion-skeptic": "manual-loop"},
        current_version={"completion-skeptic": "b40-s5"},
        candidate_version={"completion-skeptic": "manual-only"},
        run_record_ids=[
            str(pilot_ledger.get("ledger_id") or "completion_skeptic_manual_pilot_ledger"),
            str(scorecard_calibration.get("calibration_id") or "completion_skeptic_scorecard_calibration"),
            str(closure_packet.get("packet_id") or "completion_skeptic_go_no_go_closure"),
        ],
        raw_counts=raw_counts,
        evidence_links=evidence_links or [],
        redaction_status="ready",
        report_anchors=["#completion-skeptic-b40-s5"],
    )
    record.update(
        {
            "target": {
                "target_id": "skill:completion-skeptic",
                "target_type": "manual_verifier_loop",
                "pilot_scope": str(pilot_ledger.get("pilot_scope") or "unknown"),
            },
            "decision_status": str(closure_packet.get("decision_status") or "manual_only"),
            "promotion_status": str(closure_packet.get("promotion_status") or "not_promoted"),
            "pilot_denominators": {
                "sample_size": int(pilot_ledger.get("sample_size") or 0),
                "scenario_mix": _json_ready(pilot_ledger.get("archetype_counts") or {}),
                "owner_review_status": str(scorecard_calibration.get("owner_review_status") or "missing"),
                "no_unapproved_actions": bool(pilot_ledger.get("no_unapproved_actions")),
            },
            "blocked_promotions": [
                "automation",
                "MCP",
                "Agents SDK runner",
                "provider_call",
                "browser_automation",
                "target_apply",
                "canonical_mutation",
                "git_release",
            ],
            "next_approval_needs": sorted(str(item) for item in closure_packet.get("next_approval_needs", [])),
            "update_policy": "staged_evidence_only_no_auto_apply",
            "source_policy": "append_only_metrics_evidence_not_source_of_truth",
        }
    )
    return _redacted_dict(record)


def render_scorecard_ledger_markdown(record: dict[str, Any]) -> str:
    """Render a scorecard ledger entry as Markdown suitable for append-only storage."""

    lines = [
        f"# Agent Skill Scorecard Ledger: {record.get('ledger_id', 'ledger')}",
        "",
        "Append-only policy: append new records; do not rewrite prior evidence.",
        f"Generated at: {record.get('generated_at', '')}",
        f"Redaction status: {record.get('redaction_status', 'unknown')}",
        "",
        "## Versions",
        f"- Baseline version: {_compact_json(record.get('baseline_version', {}))}",
        f"- Current version: {_compact_json(record.get('current_version', {}))}",
        f"- Candidate version: {_compact_json(record.get('candidate_version', {}))}",
        "",
        "## Evidence",
        f"- Run record ids: {_join_or_none(record.get('run_record_ids', []))}",
        f"- Evidence links: {_join_or_none(record.get('evidence_links', []))}",
        f"- Report anchors: {_join_or_none(record.get('report_anchors', []))}",
        "",
        "## Metrics",
        f"- Raw counts: {_compact_json(record.get('raw_counts', {}))}",
        f"- Confidence intervals: {_compact_json(record.get('confidence_intervals', {}))}",
        f"- Cost and latency: {_compact_json(record.get('cost_latency', {}))}",
        "",
        "No-secrets policy: no raw secrets, private customer data, raw prompts, or raw tool outputs.",
    ]
    return "\n".join(lines) + "\n"


def build_daily_metrics_report(
    *,
    generated_at: str,
    evidence_window: dict[str, Any],
    target_reports: list[dict[str, Any]] | None = None,
    trace_source_mix: dict[str, int] | None = None,
    changed_versions: list[str] | None = None,
    failure_groups: list[str] | None = None,
    evidence_gaps: list[str] | None = None,
) -> dict[str, Any]:
    """Summarize daily metrics status and conservative next actions."""

    reports = [_json_ready(item) for item in target_reports or []]
    recommendations = [_daily_recommendation(item) for item in reports]
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "generated_at": str(generated_at),
        "evidence_window": _json_ready(evidence_window),
        "target_inventory": [item.get("target", {}) for item in reports],
        "trace_source_mix": dict(sorted((trace_source_mix or {}).items())),
        "changed_versions": sorted(str(item) for item in changed_versions or []),
        "failure_groups": sorted(str(item) for item in failure_groups or []),
        "evidence_gaps": sorted(set(str(item) for item in evidence_gaps or [])),
        "confidence_status": _daily_confidence_status(reports),
        "target_recommendations": recommendations,
        "next_safe_action": _daily_next_safe_action(recommendations),
        "auto_fix_policy": "never_from_one_noisy_run",
    }
    return _redacted_dict(packet)


def build_weekly_verification_packet(
    *,
    generated_at: str,
    rolling_window: dict[str, Any],
    baseline: dict[str, Any],
    previous_week: dict[str, Any],
    holdout: dict[str, Any],
    regression_findings: list[dict[str, Any]] | None = None,
    update_candidates: list[dict[str, Any]] | None = None,
    rollback_target: str = "",
    owner_review_status: str = "",
    false_pass_audit_status: str = "",
    flake_replay_status: str = "",
    cost_regression_check_status: str = "",
) -> dict[str, Any]:
    """Build a weekly verification packet that blocks unsafe update acceptance."""

    blockers: list[str] = []
    if not rollback_target:
        blockers.append("rollback_target_missing")
    if owner_review_status not in {"owner_reviewed", "accepted_gap"}:
        blockers.append("owner_review_missing")
    if str(holdout.get("status") or "") not in {"present", "passed", "checked"}:
        blockers.append("holdout_check_missing")
    if false_pass_audit_status not in {"passed", "reviewed", "accepted_gap"}:
        blockers.append("false_pass_audit_missing")
    if flake_replay_status not in {"passed", "reviewed", "accepted_gap"}:
        blockers.append("flake_replay_missing")
    if cost_regression_check_status not in {"passed", "reviewed", "accepted_gap"}:
        blockers.append("cost_regression_check_missing")
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "generated_at": str(generated_at),
        "status": "blocked" if blockers else "weekly_verification_ready",
        "blockers": sorted(set(blockers)),
        "rolling_window": _json_ready(rolling_window),
        "baseline": _json_ready(baseline),
        "previous_week": _json_ready(previous_week),
        "holdout": _json_ready(holdout),
        "false_pass_audit_status": false_pass_audit_status or "missing",
        "flake_replay_status": flake_replay_status or "missing",
        "cost_regression_check_status": cost_regression_check_status or "missing",
        "rollback_target": rollback_target,
        "owner_review_status": owner_review_status or "missing",
        "regression_findings": [_json_ready(item) for item in regression_findings or []],
        "update_candidates": [_json_ready(item) for item in update_candidates or []],
        "acceptance_policy": "rollback_owner_holdout_false_pass_flake_and_cost_evidence_required",
    }
    return _redacted_dict(packet)


def prioritize_improvement_components(
    *,
    failure_taxonomy: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Rank improvement components by failure impact and evidence sufficiency."""

    priorities: list[dict[str, Any]] = []
    for item in failure_taxonomy or []:
        component = str(item.get("component") or "unknown")
        metrics = item.get("affected_metrics") if isinstance(item.get("affected_metrics"), dict) else {}
        failure_modes = [str(value) for value in item.get("failure_modes", []) if value]
        evidence_status = str(item.get("evidence_status") or "none")
        impact = sum(abs(float(value or 0.0)) for value in metrics.values())
        if evidence_status == "sufficient" and failure_modes and impact > 0:
            decision = "change"
        elif evidence_status in {"insufficient", "partial"} or (failure_modes and impact == 0):
            decision = "defer"
        else:
            decision = "leave_unchanged"
        priorities.append(
            {
                "component": component,
                "decision": decision,
                "impact_score": round(impact, 4),
                "evidence_status": evidence_status,
                "affected_metrics": _json_ready(metrics),
                "failure_modes": failure_modes,
                "reason": ", ".join(failure_modes) if failure_modes else "no source-backed failure mode",
            }
        )
    sorted_items = sorted(
        priorities,
        key=lambda item: (
            {"change": 0, "defer": 1, "leave_unchanged": 2}.get(item["decision"], 3),
            -float(item["impact_score"]),
            item["component"],
        ),
    )
    for index, item in enumerate(sorted_items, start=1):
        item["rank"] = index
    return _redacted_dict(
        {
            "schema_version": 1,
            "write_policy": "read_only",
            "priorities": sorted_items,
            "component_catalog": [
                "prompt",
                "skill",
                "agent_config",
                "router",
                "tool_policy",
                "memory_policy",
                "logging",
                "dataset",
                "grader",
                "harness",
                "approval_policy",
            ],
        }
    )


def generate_modernization_candidates(
    *,
    component_priorities: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Generate staged review candidates without applying patches or external writes."""

    candidates: list[dict[str, Any]] = []
    for item in component_priorities or []:
        component = str(item.get("component") or "unknown")
        metrics = item.get("affected_metrics") if isinstance(item.get("affected_metrics"), dict) else {}
        blockers: list[str] = []
        if item.get("decision") != "change":
            blockers.append("component_not_selected_for_change")
        if not metrics or item.get("evidence_status") != "sufficient":
            blockers.append("headline_only_or_insufficient_evidence")
        if not item.get("rollback_target"):
            blockers.append("rollback_target_missing")
        if not item.get("expected_impact"):
            blockers.append("expected_impact_missing")
        status = "blocked" if blockers else "staged_for_review"
        candidates.append(
            {
                "candidate_id": _stable_id("candidate", component, str(item.get("target_id") or "target")),
                "component": component,
                "target_id": str(item.get("target_id") or "unassigned"),
                "status": status,
                "reason": str(item.get("reason") or "unspecified"),
                "metric_deltas": _json_ready(metrics),
                "affected_targets": [str(item.get("target_id") or "unassigned")],
                "component_priority": str(item.get("decision") or "unknown"),
                "expected_impact": str(item.get("expected_impact") or ""),
                "risk": str(item.get("risk") or "unknown"),
                "approval_state": str(item.get("approval_state") or "not_requested"),
                "rollback_target": str(item.get("rollback_target") or ""),
                "external_write_action": "none",
                "blockers": sorted(set(blockers)),
            }
        )
    return _redacted_dict(
        {
            "schema_version": 1,
            "write_policy": "read_only",
            "candidates": candidates,
            "apply_policy": "cannot_apply_patches",
            "external_write_policy": "none",
        }
    )


def _metric_section(section_id: str, metrics: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "section_id": section_id,
        "metrics": {metric["metric_id"]: metric for metric in metrics},
    }


def _ratio_metric(
    metric_id: str,
    numerator: int | float,
    denominator: int | float,
    *,
    higher_is_better: bool = True,
) -> dict[str, Any]:
    value = _safe_ratio(float(numerator), float(denominator)) if denominator else None
    return {
        "metric_id": metric_id,
        "numerator": round(float(numerator), 4),
        "denominator": round(float(denominator), 4),
        "value": round(value, 4) if value is not None else None,
        "status": "ready" if denominator else "insufficient_data",
        "higher_is_better": higher_is_better,
    }


def _boolean_rate_metric(
    metric_id: str,
    records: list[dict[str, Any]],
    key: str,
    *,
    higher_is_better: bool = True,
) -> dict[str, Any]:
    present = [record for record in records if key in record]
    numerator = sum(1 for record in present if bool(record.get(key)))
    return _ratio_metric(metric_id, numerator, len(present), higher_is_better=higher_is_better)


def _numeric_values(records: list[dict[str, Any]], key: str) -> list[float]:
    values = []
    for record in records:
        if key not in record:
            continue
        try:
            values.append(float(record.get(key)))
        except (TypeError, ValueError):
            continue
    return values


def _sum_metric(metric_id: str, records: list[dict[str, Any]], key: str) -> dict[str, Any]:
    values = _numeric_values(records, key)
    total = sum(values)
    return {
        "metric_id": metric_id,
        "numerator": round(total, 4),
        "denominator": len(values),
        "value": round(total, 4) if values else None,
        "status": "ready" if values else "insufficient_data",
        "higher_is_better": False,
    }


def _average_metric(metric_id: str, records: list[dict[str, Any]], key: str) -> dict[str, Any]:
    values = _numeric_values(records, key)
    total = sum(values)
    value = total / len(values) if values else None
    return {
        "metric_id": metric_id,
        "numerator": round(total, 4),
        "denominator": len(values),
        "value": round(value, 4) if value is not None else None,
        "status": "ready" if values else "insufficient_data",
        "higher_is_better": False,
    }


def _percentile_metric(metric_id: str, records: list[dict[str, Any]], key: str, percentile: float) -> dict[str, Any]:
    values = sorted(_numeric_values(records, key))
    if not values:
        return {
            "metric_id": metric_id,
            "numerator": 0.0,
            "denominator": 0,
            "value": None,
            "status": "insufficient_data",
            "higher_is_better": False,
        }
    index = max(0, min(len(values) - 1, math.ceil(percentile * len(values)) - 1))
    value = values[index]
    return {
        "metric_id": metric_id,
        "numerator": round(value, 4),
        "denominator": len(values),
        "value": round(value, 4),
        "status": "ready",
        "higher_is_better": False,
    }


def _cost_regression_metric(records: list[dict[str, Any]]) -> dict[str, Any]:
    present = [record for record in records if "cost_usd" in record and "baseline_cost_usd" in record]
    numerator = sum(1 for record in present if float(record.get("cost_usd") or 0.0) > float(record.get("baseline_cost_usd") or 0.0))
    return _ratio_metric("cost_regression_rate", numerator, len(present), higher_is_better=False)


def _latency_regression_metric(records: list[dict[str, Any]]) -> dict[str, Any]:
    present = [record for record in records if "latency_ms" in record and "baseline_latency_ms" in record]
    numerator = sum(1 for record in present if float(record.get("latency_ms") or 0.0) > float(record.get("baseline_latency_ms") or 0.0))
    return _ratio_metric("latency_regression_rate", numerator, len(present), higher_is_better=False)


def _cost_improvement_metric(records: list[dict[str, Any]]) -> dict[str, Any]:
    present = [record for record in records if "cost_usd" in record and "baseline_cost_usd" in record]
    numerator = sum(1 for record in present if float(record.get("cost_usd") or 0.0) <= float(record.get("baseline_cost_usd") or 0.0))
    return _ratio_metric("cost_improvement_rate", numerator, len(present))


def _skill_trigger_recall(records: list[dict[str, Any]]) -> dict[str, Any]:
    expected = [record for record in records if bool(record.get("skill_expected"))]
    numerator = sum(1 for record in expected if bool(record.get("skill_triggered")))
    return _ratio_metric("skill_trigger_recall", numerator, len(expected))


def _skill_trigger_precision(records: list[dict[str, Any]]) -> dict[str, Any]:
    triggered = [record for record in records if bool(record.get("skill_triggered"))]
    numerator = sum(1 for record in triggered if bool(record.get("skill_expected")))
    return _ratio_metric("skill_trigger_precision", numerator, len(triggered))


def _any_safety_violation_metric(records: list[dict[str, Any]]) -> dict[str, Any]:
    keys = ["instruction_violation", "approval_violation", "private_data_leak"]
    present = [record for record in records if any(key in record for key in keys)]
    numerator = sum(1 for record in present if any(bool(record.get(key)) for key in keys))
    return _ratio_metric("safety_violation_rate", numerator, len(present), higher_is_better=False)


def _case_has_instability(runs: list[dict[str, Any]]) -> bool:
    outcomes = {bool(run.get("passed")) for run in runs}
    return len(outcomes) > 1


def _default_scorecard_weights() -> dict[str, dict[str, float]]:
    return {
        "harness_quality_score": {
            "trace_completeness": 0.25,
            "replay_success_rate": 0.25,
            "flake_rate": 0.25,
            "false_pass_rate": 0.25,
        },
        "agentic_task_score": {
            "task_success_rate": 0.25,
            "final_state_accuracy": 0.20,
            "tool_selection_accuracy": 0.20,
            "tool_argument_accuracy": 0.20,
            "instruction_violation_rate": 0.15,
        },
        "harness_optimization_score": {
            "regression_free_success_rate": 0.25,
            "cost_regression_rate": 0.25,
            "latency_regression_rate": 0.20,
            "skill_adherence_rate": 0.15,
            "replayable_trace_rate": 0.15,
        },
    }


def _scorecard(scorecard_id: str, metric_packet: dict[str, Any], weights: dict[str, float]) -> dict[str, Any]:
    component_scores: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    weighted_score = 0.0
    total_weight = 0.0
    for metric_id, weight in weights.items():
        metric = _metric_lookup(metric_packet, metric_id)
        if metric.get("status") != "ready":
            missing.append(metric_id)
            component_scores[metric_id] = {"score": None, "weight": weight, "status": "insufficient_data"}
            continue
        score = _component_score(metric)
        component_scores[metric_id] = {"score": score, "weight": weight, "status": "ready"}
        weighted_score += score * weight
        total_weight += weight
    status = "ready" if total_weight else "insufficient_data"
    return {
        "scorecard_id": scorecard_id,
        "score": round(weighted_score / total_weight, 4) if total_weight else 0.0,
        "status": status,
        "components": component_scores,
        "weights": dict(weights),
        "missing_data": missing,
    }


def _component_score(metric: dict[str, Any]) -> float:
    value = _metric_value(metric)
    if metric.get("higher_is_better") is False:
        value = 1.0 - value
    return round(max(0.0, min(1.0, value)), 4)


def _metric_lookup(metric_packet: dict[str, Any], metric_id: str) -> dict[str, Any]:
    sections = metric_packet.get("sections") if isinstance(metric_packet, dict) else {}
    if not isinstance(sections, dict):
        return {}
    for section in sections.values():
        if not isinstance(section, dict):
            continue
        metrics = section.get("metrics")
        if isinstance(metrics, dict) and metric_id in metrics:
            metric = metrics[metric_id]
            return metric if isinstance(metric, dict) else {}
    return {}


def _metric_value(metric: dict[str, Any]) -> float:
    try:
        return float(metric.get("value") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _guardrail_metrics(metric_packet: dict[str, Any]) -> dict[str, float | None]:
    metric_ids = [
        "instruction_violation_rate",
        "approval_violation_rate",
        "private_data_leak_rate",
        "safety_violation_rate",
        "false_pass_rate",
        "flake_rate",
        "trace_completeness",
        "cost_regression_rate",
    ]
    values: dict[str, float | None] = {}
    for metric_id in metric_ids:
        metric = _metric_lookup(metric_packet, metric_id)
        values[metric_id] = _metric_value(metric) if metric.get("status") == "ready" else None
    return values


def _guardrail_blockers(metrics: dict[str, float | None]) -> list[str]:
    blockers: list[str] = []
    if any((metrics.get(metric_id) or 0.0) > 0 for metric_id in [
        "instruction_violation_rate",
        "approval_violation_rate",
        "private_data_leak_rate",
        "safety_violation_rate",
    ]):
        blockers.append("safety_violation")
    if metrics.get("false_pass_rate") is not None and (metrics["false_pass_rate"] or 0.0) > 0.05:
        blockers.append("false_pass_regression")
    if metrics.get("flake_rate") is not None and (metrics["flake_rate"] or 0.0) > 0.1:
        blockers.append("flake_regression")
    if metrics.get("trace_completeness") is not None and (metrics["trace_completeness"] or 0.0) < 0.8:
        blockers.append("trace_incomplete")
    if metrics.get("cost_regression_rate") is not None and (metrics["cost_regression_rate"] or 0.0) > 0.2:
        blockers.append("cost_regression")
    return sorted(set(blockers))


def _wilson_lower_bound(successes: int, total: int, z: float = 1.96) -> float:
    if total == 0:
        return 0.0
    phat = successes / total
    denominator = 1 + (z * z / total)
    centre = phat + (z * z / (2 * total))
    margin = z * math.sqrt((phat * (1 - phat) + (z * z / (4 * total))) / total)
    return max(0.0, (centre - margin) / denominator)


def _cadence_for_level(level: str) -> list[str]:
    return {
        "L0": ["on_change"],
        "L1": ["weekly", "on_change"],
        "L2": ["daily", "weekly", "on_change"],
        "L3": ["daily", "weekly", "on_change", "incident_triggered"],
    }.get(level, ["on_change"])


def _partition_run_artifacts(artifacts: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    accepted: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    rejected_types = set(_GENERATED_REVIEW_ONLY + _REJECTED_SOURCES)
    for artifact in artifacts:
        source_type = str(artifact.get("source_type") or "")
        record = _json_ready(artifact)
        if source_type in rejected_types:
            record["reason"] = "not_source_of_truth"
            excluded.append(record)
        else:
            accepted.append(record)
    return (
        sorted(accepted, key=lambda item: str(item.get("artifact_id") or item.get("path") or "")),
        sorted(excluded, key=lambda item: str(item.get("artifact_id") or item.get("path") or "")),
    )


def _trace_id(trace: dict[str, Any]) -> str:
    return str(trace.get("trace_id") or trace.get("id") or trace.get("record_id") or "trace")


def _compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _join_or_none(values: Any) -> str:
    if not isinstance(values, list) or not values:
        return "none"
    return ", ".join(str(item) for item in values)


def _daily_recommendation(item: dict[str, Any]) -> dict[str, Any]:
    target = item.get("target") if isinstance(item.get("target"), dict) else {}
    target_id = str(target.get("target_id") or item.get("target_id") or "unassigned")
    blockers = [str(value) for value in item.get("blockers", []) if value]
    decision_status = str(item.get("decision_status") or "unknown")
    evidence_gaps = [str(value) for value in item.get("evidence_gaps", []) if value]
    update_candidates = item.get("update_candidates") if isinstance(item.get("update_candidates"), list) else []
    if blockers or decision_status == "blocked_by_gate":
        recommendation = "block_promotion"
    elif update_candidates:
        recommendation = "stage_candidate_for_review"
    elif decision_status == "insufficient_data" or evidence_gaps:
        recommendation = "request_human_audit"
    elif decision_status in {"weekly_acceptance_ready", "ready"}:
        recommendation = "no_op"
    else:
        recommendation = "investigate"
    return {
        "target_id": target_id,
        "recommendation": recommendation,
        "decision_status": decision_status,
        "blockers": blockers,
        "evidence_gaps": evidence_gaps,
    }


def _daily_confidence_status(reports: list[dict[str, Any]]) -> str:
    statuses = {str(item.get("confidence_status") or item.get("decision_status") or "unknown") for item in reports}
    if any(status in {"blocked", "blocked_by_gate"} for status in statuses):
        return "blocked"
    if any(status == "insufficient_data" for status in statuses):
        return "insufficient_data"
    return "ready" if reports else "no_data"


def _daily_next_safe_action(recommendations: list[dict[str, Any]]) -> str:
    actions = {item["recommendation"] for item in recommendations}
    if "block_promotion" in actions:
        return "review blockers before promotion"
    if "stage_candidate_for_review" in actions:
        return "stage candidate packet for owner review"
    if "request_human_audit" in actions:
        return "request human audit or accepted evidence gap"
    if "investigate" in actions:
        return "investigate changed evidence"
    return "record no-op decision"


def _repo_record(repo_sha: str, gap: dict[str, Any]) -> dict[str, Any]:
    if repo_sha:
        return {"repo_sha_status": "present", "repo_sha": str(repo_sha)}
    if gap:
        return {
            "repo_sha_status": "accepted_gap",
            "accepted_gap": {
                "owner": str(gap.get("owner") or "unassigned"),
                "reason": str(gap.get("reason") or "unspecified"),
            },
        }
    return {"repo_sha_status": "missing", "accepted_gap_required": True}


def _normalize_trace_source(source: dict[str, Any], index: int) -> tuple[dict[str, Any], list[str]]:
    source_type = _normalize_trace_source_type(str(source.get("trace_source_type") or source.get("source_type") or ""))
    trace_id = str(source.get("trace_id") or source.get("id") or f"trace-{index + 1}")
    group_id = str(source.get("group_id") or source.get("task_id") or "")
    warnings: list[str] = []
    if source_type not in _SUPPORTED_TRACE_SOURCE_TYPES:
        warnings.append("unsupported_trace_source")
        return (
            {
                "trace_id": trace_id,
                "group_id": group_id,
                "trace_source_type": source_type or "unsupported",
                "status": "unsupported",
                "required_span_types": list(_TRACE_REQUIRED_SPAN_TYPES),
                "present_span_types": [],
                "missing_span_types": list(_TRACE_REQUIRED_SPAN_TYPES),
                "replayability": {"status": "not_replayable", "fields": []},
            },
            warnings,
        )
    if source_type == "accepted_gap":
        gap = source.get("accepted_gap") if isinstance(source.get("accepted_gap"), dict) else {}
        return (
            {
                "trace_id": trace_id,
                "group_id": group_id,
                "trace_source_type": source_type,
                "status": "accepted_gap",
                "required_span_types": [],
                "present_span_types": [],
                "missing_span_types": [],
                "accepted_gap": {
                    "owner": str(gap.get("owner") or "unassigned"),
                    "reason": str(gap.get("reason") or "unspecified"),
                },
                "replayability": {"status": "accepted_gap", "fields": []},
            },
            warnings,
        )

    present = _trace_span_types(source, source_type)
    missing = [span_type for span_type in _TRACE_REQUIRED_SPAN_TYPES if span_type not in present]
    replayability = _trace_replayability(source)
    status = "complete" if not missing else "incomplete"
    return (
        {
            "trace_id": trace_id,
            "group_id": group_id,
            "trace_source_type": source_type,
            "status": status,
            "required_span_types": list(_TRACE_REQUIRED_SPAN_TYPES),
            "present_span_types": present,
            "missing_span_types": missing,
            "replayability": replayability,
        },
        warnings,
    )


def _normalize_trace_source_type(value: str) -> str:
    normalized = _slug(value).replace("-", "_")
    aliases = {
        "agents_sdk_trace": "agents_sdk",
        "openai_agents_sdk": "agents_sdk",
        "otel_genai": "opentelemetry_genai",
        "open_telemetry_genai": "opentelemetry_genai",
        "tool_specific_report": "tool_report",
    }
    return aliases.get(normalized, normalized)


def _trace_span_types(source: dict[str, Any], source_type: str) -> list[str]:
    span_types: set[str] = set()
    spans = source.get("spans")
    if isinstance(spans, list):
        for span in spans:
            if isinstance(span, dict):
                span_types.update(_span_types_from_mapping(span, source_type))
    if source.get("tool_calls"):
        span_types.add("tool")
    for key, span_type in [
        ("model_calls", "model"),
        ("handoffs", "handoff"),
        ("state", "state"),
        ("final_response", "final_response"),
        ("result", "final_response"),
    ]:
        if source.get(key):
            span_types.add(span_type)
    return sorted(span_types)


def _span_types_from_mapping(span: dict[str, Any], source_type: str) -> set[str]:
    values = [
        str(span.get("span_type") or ""),
        str(span.get("type") or ""),
        str(span.get("name") or ""),
    ]
    attributes = span.get("attributes")
    if isinstance(attributes, dict):
        values.extend(str(value) for value in attributes.values())
    joined = " ".join(values).lower()
    span_types: set[str] = set()
    if "handoff" in joined:
        span_types.add("handoff")
    if "tool" in joined or "function" in joined:
        span_types.add("tool")
    if "final" in joined or "response" in joined or "output" in joined:
        span_types.add("final_response")
    if "model" in joined or "chat" in joined or "completion" in joined or "gen_ai" in joined:
        span_types.add("model")
    if source_type == "opentelemetry_genai" and ("chat" in joined or "gen_ai" in joined):
        span_types.add("model")
    return span_types


def _trace_replayability(source: dict[str, Any]) -> dict[str, Any]:
    replay = source.get("replay")
    fields: list[str] = []
    if isinstance(replay, dict):
        fields = sorted(str(key) for key, value in replay.items() if value)
    for key in ["fixture", "command", "seed", "dataset", "run_record"]:
        if source.get(key) and key not in fields:
            fields.append(key)
    return {
        "status": "replayable" if fields else "not_replayable",
        "fields": sorted(fields),
    }


def _sanitize_raw_metrics_payload(value: Any, key: str = "") -> tuple[Any, dict[str, Any]]:
    categories: set[str] = set()
    count = 0

    def visit(item: Any, current_key: str = "") -> Any:
        nonlocal count
        normalized_key = _slug(current_key).replace("-", "_")
        if isinstance(item, dict):
            return {nested_key: visit(nested_value, str(nested_key)) for nested_key, nested_value in item.items()}
        if isinstance(item, list):
            return [visit(nested_value, current_key) for nested_value in item]
        if isinstance(item, str):
            if normalized_key in _RAW_PROMPT_KEYS:
                categories.add("raw_prompt")
                count += 1
                return "[REDACTED_RAW_PROMPT]"
            if normalized_key in _RAW_TOOL_OUTPUT_KEYS:
                categories.add("raw_tool_output")
                count += 1
                return "[REDACTED_RAW_TOOL_OUTPUT]"
        return item

    sanitized = visit(value, key)
    return sanitized, {"count": count, "categories": sorted(categories)}


def _dataset_records(
    samples: list[dict[str, Any]],
    group: str,
    split: str,
    *,
    synthetic_default: bool = False,
) -> list[dict[str, Any]]:
    return [_dataset_record(sample, group, split, synthetic_default=synthetic_default) for sample in samples]


def _trace_dataset_records(traces: Any) -> list[dict[str, Any]]:
    if not isinstance(traces, list):
        return []
    records = []
    for trace in traces:
        if not isinstance(trace, dict):
            continue
        records.append(
            {
                "sample_id": str(trace.get("trace_id") or trace.get("record_id") or "trace"),
                "group": "real_trace_sample",
                "split": "real_trace",
                "source_type": "trace_packet",
                "trace_source_type": str(trace.get("trace_source_type") or "unknown"),
                "status": str(trace.get("status") or "present_unverified"),
                "synthetic": bool(trace.get("synthetic", False)),
            }
        )
    return records


def _dataset_record(
    sample: dict[str, Any],
    group: str,
    split: str,
    *,
    synthetic_default: bool = False,
) -> dict[str, Any]:
    sample_id = str(sample.get("sample_id") or sample.get("id") or sample.get("record_id") or _stable_id(group, split))
    return {
        "sample_id": sample_id,
        "group": group,
        "split": split,
        "source_type": str(sample.get("source_type") or group),
        "status": str(sample.get("status") or "present_unverified"),
        "synthetic": bool(sample.get("synthetic", synthetic_default)),
    }


def _duplicate_sample_ids(records: list[dict[str, Any]]) -> list[str]:
    counts: dict[str, int] = {}
    for record in records:
        sample_id = str(record.get("sample_id") or "")
        counts[sample_id] = counts.get(sample_id, 0) + 1
    return sorted(sample_id for sample_id, count in counts.items() if sample_id and count > 1)


def _leakage_sample_ids(records: list[dict[str, Any]]) -> list[str]:
    splits_by_sample: dict[str, set[str]] = {}
    for record in records:
        sample_id = str(record.get("sample_id") or "")
        split = str(record.get("split") or "")
        if not sample_id:
            continue
        splits_by_sample.setdefault(sample_id, set()).add(split)
    return sorted(
        sample_id
        for sample_id, splits in splits_by_sample.items()
        if "holdout" in splits and len(splits - {"holdout"}) > 0
    )


def _grader_records(items: list[dict[str, Any]], grader_type: str) -> list[dict[str, Any]]:
    return [
        _grader_record(
            grader_type,
            str(item.get("rubric_id") or "unassigned"),
            int(item.get("sample_size") or 0),
            source_status=str(item.get("source_status") or "local_eval_output"),
            passed=int(item.get("passed") or 0),
            failed=int(item.get("failed") or 0),
        )
        for item in items
    ]


def _human_audit_records(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for item in items:
        labels = item.get("labels") if isinstance(item.get("labels"), list) else []
        records.append(
            _grader_record(
                "human_audit",
                str(item.get("rubric_id") or "owner-review"),
                int(item.get("sample_size") or len(labels)),
                source_status="manual_label_input",
            )
        )
    return records


def _grader_record(
    grader_type: str,
    rubric_id: str,
    sample_size: int,
    *,
    source_status: str,
    passed: int = 0,
    failed: int = 0,
) -> dict[str, Any]:
    return {
        "grader_type": grader_type,
        "rubric_id": rubric_id,
        "sample_size": sample_size,
        "source_status": source_status,
        "passed": passed,
        "failed": failed,
    }


def _binary_label_counts(pairs: list[tuple[str, str]]) -> dict[str, int]:
    counts = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    for judge_label, human_label in pairs:
        judge_positive = _positive_label(judge_label)
        human_positive = _positive_label(human_label)
        if judge_positive and human_positive:
            counts["tp"] += 1
        elif judge_positive and not human_positive:
            counts["fp"] += 1
        elif not judge_positive and human_positive:
            counts["fn"] += 1
        else:
            counts["tn"] += 1
    return counts


def _positive_label(value: str) -> bool:
    return str(value).strip().lower() in {"pass", "passed", "ok", "true", "1", "approve", "approved", "success"}


def _cohen_kappa(counts: dict[str, int], sample_size: int, agreement: float) -> float:
    if sample_size == 0:
        return 0.0
    judge_positive = counts["tp"] + counts["fp"]
    judge_negative = counts["fn"] + counts["tn"]
    human_positive = counts["tp"] + counts["fn"]
    human_negative = counts["fp"] + counts["tn"]
    expected = ((judge_positive * human_positive) + (judge_negative * human_negative)) / (sample_size * sample_size)
    if expected == 1.0:
        return 1.0 if agreement == 1.0 else 0.0
    return (agreement - expected) / (1.0 - expected)


def _safe_ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def _agent_targets(root: Path) -> list[dict[str, Any]]:
    targets = []
    agent_paths = sorted((root / ".codex" / "agents").glob("*.toml"))
    for path in agent_paths:
        text = _safe_read(path)
        name = _metadata_value(text, "name") or path.stem
        targets.append(
            _target(
                target_id=f"agent:{_slug(name)}",
                target_type="agent",
                name=name,
                source_path=_relative_path(root, path),
                owner=_metadata_value(text, "owner"),
                version=_metadata_value(text, "version"),
                risk_level=_metadata_value(text, "risk_level") or "medium",
                expected_artifacts=["agent-task-packet.md", "handoff-contract.md", "eval-run-report.md"],
                eval_suite=["agent_skill_metrics"],
                maturity_level="configured",
                tool_permission_level="workspace_tools",
            )
        )
    if len(agent_paths) > 1:
        targets.append(
            _target(
                target_id="subagent_team:codex-agents",
                target_type="subagent_team",
                name="codex-agents",
                source_path=".codex/agents",
                expected_artifacts=["worktree-ownership.md", "handoff-contract.md"],
                eval_suite=["handoff-completeness", "agent_skill_metrics"],
                maturity_level="configured",
                tool_permission_level="workspace_tools",
            )
        )
    return targets


def _skill_targets(root: Path) -> list[dict[str, Any]]:
    targets = []
    search_roots = [
        root / ".codex" / "skills",
        root / "skills",
        root / "plugins" / "product-agent-os" / "skills",
    ]
    for skill_root in search_roots:
        if not skill_root.exists():
            continue
        for path in sorted(skill_root.glob("*/SKILL.md")):
            text = _safe_read(path)
            name = _frontmatter_value(text, "name") or path.parent.name
            targets.append(
                _target(
                    target_id=f"skill:{_slug(name)}",
                    target_type="skill",
                    name=name,
                    source_path=_relative_path(root, path),
                    owner=_frontmatter_value(text, "owner"),
                    version=_frontmatter_value(text, "version"),
                    risk_level=_frontmatter_value(text, "risk_level") or "medium",
                    expected_artifacts=["skill-promotion-record.md", "agent-eval-workflow.md"],
                    eval_suite=["agent_skill_metrics", "transcript_session_eval"],
                    maturity_level="managed",
                    tool_permission_level="workspace_tools",
                )
            )
    return targets


def _artifact_policy_targets(root: Path) -> list[dict[str, Any]]:
    definitions = [
        ("prompt-contract.md", "prompt_pack", "prompt-contract", "prompt_contract"),
        ("model-reasoning-policy.md", "policy_pack", "model-reasoning-policy", "model_reasoning_policy"),
        ("mcp-permission-review.md", "policy_pack", "mcp-permission-review", "tool_permission_policy"),
        ("hook-governance.md", "policy_pack", "hook-governance", "hook_policy"),
        ("agent-workflow-map.md", "policy_pack", "agent-workflow-map", "agent_workflow_policy"),
    ]
    targets = []
    for filename, target_type, name, maturity in definitions:
        for path in _find_named_artifacts(root, filename):
            targets.append(
                _target(
                    target_id=f"{target_type}:{_slug(name)}",
                    target_type=target_type,
                    name=name,
                    source_path=_relative_path(root, path),
                    expected_artifacts=["eval-run-report.md", "trace-evidence-packet.md"],
                    eval_suite=["agent_skill_metrics"],
                    maturity_level=maturity,
                    tool_permission_level="policy_documented",
                )
            )
    return targets


def _automation_candidate_targets(root: Path) -> list[dict[str, Any]]:
    targets = []
    candidate_root = root / ".codex" / "automation-candidates"
    if not candidate_root.exists():
        return targets
    for path in sorted(candidate_root.glob("*.md")):
        name = path.stem
        targets.append(
            _target(
                target_id=f"automation_candidate:{_slug(name)}",
                target_type="automation_candidate",
                name=name,
                source_path=_relative_path(root, path),
                risk_level="high",
                expected_artifacts=["automation-candidate.md", "approval-record.md", "eval-run-report.md"],
                eval_suite=["automation_policy", "agent_skill_metrics"],
                maturity_level="candidate_only",
                tool_permission_level="approval_bound",
                production_impact=True,
            )
        )
    return targets


def _config_targets(root: Path) -> list[dict[str, Any]]:
    path = root / ".codex" / "config.toml"
    if not path.exists():
        return []
    return [
        _target(
            target_id="policy_pack:codex-config",
            target_type="policy_pack",
            name="codex-config",
            source_path=_relative_path(root, path),
            expected_artifacts=["model-reasoning-policy.md", "mcp-permission-review.md", "approval-record.md"],
            eval_suite=["agent_skill_metrics"],
            maturity_level="configured",
            tool_permission_level="codex_policy",
        )
    ]


def _harness_targets(root: Path) -> list[dict[str, Any]]:
    paths = [
        root / ".codex" / "product-agent-os" / "harness-version.json",
        root / ".codex" / "product-agent-os" / "status.json",
    ]
    targets = []
    for path in paths:
        if not path.exists():
            continue
        name = path.stem
        targets.append(
            _target(
                target_id=f"harness:{_slug(name)}",
                target_type="harness",
                name=name,
                source_path=_relative_path(root, path),
                expected_artifacts=["eval-run-report.md", "trace-evidence-packet.md"],
                eval_suite=["agent_skill_metrics"],
                maturity_level="detected",
                tool_permission_level="read_only",
            )
        )
    return targets


def _target(
    *,
    target_id: str,
    target_type: str,
    name: str,
    source_path: str,
    owner: str = "",
    version: str = "",
    risk_level: str = "unknown",
    expected_artifacts: list[str] | None = None,
    eval_suite: list[str] | None = None,
    maturity_level: str = "detected",
    usage_volume: str = "unknown",
    tool_permission_level: str = "unknown",
    production_impact: bool = False,
) -> dict[str, Any]:
    return {
        "target_id": target_id,
        "target_type": target_type,
        "name": name,
        "owner": owner or "unassigned",
        "version": version or "unversioned",
        "risk_level": risk_level if risk_level in {"low", "medium", "high", "unknown"} else "unknown",
        "expected_artifacts": expected_artifacts or [],
        "eval_suite": eval_suite or [],
        "source_artifacts": [source_path],
        "maturity_level": maturity_level,
        "usage_volume": usage_volume,
        "tool_permission_level": tool_permission_level,
        "production_impact": bool(production_impact),
        "no_data_status": "target_registered_no_metrics_yet",
    }


def _evidence_candidate_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for filename in _CONTROL_PLANE_FILES:
        path = root / filename
        if path.exists() and path.is_file():
            paths.append(path)
    for pattern in [
        ".codex/artifact-templates/trace-evidence-packet.md",
        ".codex/artifact-templates/eval-run-report.md",
        ".codex/evals/*.json",
        ".codex/eval-reports/*.json",
        ".codex/product-agent-os/status.html",
        ".codex/eval-reports/*.html",
        "memory.md",
        "raw-chat.log",
    ]:
        paths.extend(path for path in root.glob(pattern) if path.is_file())
    return sorted(set(paths), key=lambda item: item.as_posix())


def _records_from_text(relative: str, text: str, as_of_date: str, evidence_max_age_days: int) -> list[dict[str, Any]]:
    source_type = _source_type(relative, text)
    recorded_at = _first_date(text)
    records = [
        _evidence_record(
            source_path=relative,
            source_type=source_type,
            status=_status_from_text(text),
            recorded_at=recorded_at,
        )
    ]
    if Path(relative).name in _CONTROL_PLANE_FILES and source_type != "control_plane":
        records.append(
            _evidence_record(
                source_path=relative,
                source_type="control_plane",
                status=_status_from_text(text),
                recorded_at=recorded_at,
            )
        )
    lowered = text.lower()
    if "accepted gap" in lowered:
        records.append(
            _evidence_record(
                source_path=relative,
                source_type="accepted_gap",
                status="accepted_gap",
                recorded_at=recorded_at,
            )
        )
    if "failed verification" in lowered or "verification failed" in lowered or "fixture eval failed" in lowered:
        records.append(
            _evidence_record(
                source_path=relative,
                source_type="failed_verification",
                status="failed",
                recorded_at=recorded_at,
            )
        )
    if _is_stale(recorded_at, as_of_date, evidence_max_age_days):
        records.append(
            _evidence_record(
                source_path=relative,
                source_type="stale_evidence",
                status="stale",
                recorded_at=recorded_at,
            )
        )
    return records


def _source_type(relative: str, text: str) -> str:
    name = Path(relative).name
    lowered = f"{relative}\n{text}".lower()
    if name == "trace-evidence-packet.md":
        return "trace_packet"
    if name == "eval-run-report.md" or any(hint in lowered for hint in _EVAL_HINTS):
        return "eval_packet"
    if name in _CONTROL_PLANE_FILES:
        return "control_plane"
    if relative.endswith(".json"):
        return "run_record"
    return "control_plane"


def _excluded_source_type(relative: str) -> str:
    lowered = relative.lower()
    name = Path(relative).name.lower()
    if name == "status.html" or lowered.endswith("/status.html"):
        return "status_dashboard_html"
    if name == "agent-skill-evaluation-report.html":
        return "metrics_report_html"
    if name.endswith(".html"):
        return "generated_report_html"
    if name.startswith("memory"):
        return "memory"
    if "raw-chat" in name or "raw_chat" in name:
        return "raw_chat_log"
    return ""


def _evidence_record(*, source_path: str, source_type: str, status: str, recorded_at: str = "") -> dict[str, Any]:
    record_id = _stable_id(source_type, source_path, status, recorded_at)
    return {
        "record_id": record_id,
        "source_type": source_type,
        "source_path": source_path,
        "status": status,
        "recorded_at": recorded_at,
    }


def _excluded_record(source_path: str, source_type: str) -> dict[str, Any]:
    return {
        "record_id": _stable_id("excluded", source_type, source_path),
        "source_type": source_type,
        "source_path": source_path,
        "reason": "not_source_of_truth",
    }


def _status_from_text(text: str) -> str:
    lowered = text.lower()
    if "accepted gap" in lowered:
        return "accepted_gap_present"
    if "failed verification" in lowered or "verification failed" in lowered or "fixture eval failed" in lowered:
        return "failed"
    if "exited 0" in lowered or "0 failures" in lowered or " ok" in lowered:
        return "recorded"
    return "present_unverified"


def _first_date(text: str) -> str:
    match = _DATE_PATTERN.search(text)
    return match.group(1) if match else ""


def _is_stale(recorded_at: str, as_of_date: str, max_age_days: int) -> bool:
    try:
        recorded = date.fromisoformat(recorded_at)
        current = date.fromisoformat(as_of_date)
    except ValueError:
        return False
    return (current - recorded).days > max_age_days


def _trim_items(items: list[dict[str, Any]], limit: int, name: str) -> tuple[list[dict[str, Any]], list[str]]:
    sorted_items = sorted((_json_ready(item) for item in items), key=_item_sort_key)
    if len(sorted_items) <= limit:
        return sorted_items, []
    return sorted_items[:limit], [f"{name}_trimmed"]


def _trim_records(items: list[dict[str, Any]], limit: int, name: str) -> tuple[list[dict[str, Any]], list[str]]:
    unique: dict[str, dict[str, Any]] = {}
    for item in items:
        unique[str(item.get("record_id"))] = item
    return _trim_items(list(unique.values()), limit, name)


def _bounded_list(items: list[dict[str, Any]], key: str, limit: int) -> list[dict[str, Any]]:
    unique: dict[str, dict[str, Any]] = {}
    for item in items:
        unique[str(item.get(key))] = item
    return sorted(unique.values(), key=lambda item: str(item.get(key)))[:limit]


def _bounded_embedded_json(value: Any) -> tuple[dict[str, Any], list[str]]:
    if value is None:
        return {"status": "empty", "byte_size": 0, "data": None}, []
    rendered = json.dumps(value, sort_keys=True, separators=(",", ":"))
    byte_size = len(rendered.encode("utf-8"))
    limit = METRICS_PACKET_LIMITS["embedded_json_bytes"]
    if byte_size <= limit:
        return {"status": "included", "byte_size": byte_size, "data": value}, []
    return {
        "status": "trimmed",
        "byte_size": limit,
        "original_byte_size": byte_size,
        "data": None,
    }, ["embedded_json_trimmed"]


def _dedupe_targets(targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: dict[str, dict[str, Any]] = {}
    for target in targets:
        unique[str(target.get("target_id"))] = target
    return sorted(unique.values(), key=lambda item: str(item.get("target_id")))


def _find_named_artifacts(root: Path, filename: str) -> list[Path]:
    candidates = [
        root / filename,
        root / ".codex" / "artifact-templates" / filename,
        root / "plugins" / "product-agent-os" / "assets" / "templates" / "artifact-templates" / filename,
    ]
    return [path for path in candidates if path.exists() and path.is_file()]


def _metadata_value(text: str, key: str) -> str:
    for line in text.splitlines():
        match = _KEY_VALUE_PATTERN.match(line)
        if match and match.group(1).strip().lower() == key.lower():
            return match.group(2).strip()
    return ""


def _frontmatter_value(text: str, key: str) -> str:
    if not text.startswith("---"):
        return ""
    for line in text.splitlines()[1:]:
        if line.strip() == "---":
            break
        match = _KEY_VALUE_PATTERN.match(line)
        if match and match.group(1).strip().lower() == key.lower():
            return match.group(2).strip()
    return ""


def _safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _relative_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.name


def _item_sort_key(item: dict[str, Any]) -> tuple[str, str]:
    for key in ("target_id", "record_id", "id", "candidate_id", "source_path"):
        value = item.get(key)
        if value:
            return key, str(value)
    return "json", json.dumps(item, sort_keys=True)


def _json_ready(item: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(item, sort_keys=True, default=str))


def _stable_id(*parts: str) -> str:
    return "_".join(_slug(part) for part in parts if part)[:120] or "record"


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", str(value).strip().lower()).strip("-")
    return slug or "unknown"


def _counts(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(key) or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _redacted_dict(packet: dict[str, Any]) -> dict[str, Any]:
    redacted, report = redact_payload(packet)
    if not isinstance(redacted, dict):
        return {"schema_version": 1, "write_policy": "read_only", "redaction_summary": report}
    redacted["redaction_summary"] = report
    return redacted
