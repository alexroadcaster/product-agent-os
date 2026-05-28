"""Read-only agent and skill metrics-loop foundation for Product-Agent OS."""

from __future__ import annotations

import json
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
