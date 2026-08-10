from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from .promotion_contract import QuarantinedPrimaryResult, ValidatedPrimaryResult, parse_primary_result
from .redaction import validate_redaction


FINAL_JSON_MARKER = "FINAL_JSON:"

LIVE_RUN_STATUS_VALUES = [
    "completed",
    "timeout",
    "no_op",
    "invalid_json",
    "wrapper_failure_before_model_call",
    "aborted_by_policy",
    "not_run_due_stop_rule",
]
LIVE_RUN_REQUIRED_FIELDS = [
    "task_id",
    "arm",
    "pair_id",
    "attempt_id",
    "status",
    "timed_out",
    "final_json_parse_ok",
    "changed_file_count",
    "sanitized_changed_files",
    "behavior_score",
    "raw_output_hashes",
    "retention_status",
]
PAIR_REQUIRED_FIELDS = [
    "pair_id",
    "task_id",
    "baseline_status",
    "treatment_status",
    "pair_valid_for_scoring",
    "invalid_reason",
    "treatment_equal_or_better",
    "reviewer_required",
]
AGGREGATE_REQUIRED_FIELDS = [
    "valid_pair_count",
    "invalid_pair_count",
    "timeout_count",
    "no_op_count",
    "invalid_json_count",
    "treatment_equal_or_better_count",
    "reviewer_decision",
    "promotion_threshold_met",
    "m26_reversed",
    "m35_reversed",
]
PAIR_INVALID_REASONS = [
    "baseline_timeout",
    "treatment_timeout",
    "baseline_no_op",
    "treatment_no_op",
    "baseline_invalid_json",
    "treatment_invalid_json",
    "baseline_wrapper_failure_before_model_call",
    "treatment_wrapper_failure_before_model_call",
    "baseline_aborted_by_policy",
    "treatment_aborted_by_policy",
    "baseline_not_run_due_stop_rule",
    "treatment_not_run_due_stop_rule",
]
HASH_FIELD_PATTERN = re.compile(r"^[A-Fa-f0-9]{64}$")
RAW_OUTPUT_FIELD_PATTERN = re.compile(
    r"(?i)(?:^|_)(stdout|stderr|prompt|provider_payload|raw_output|raw_body|final_summary)$"
)
IGNORED_CHANGE_PATTERNS = (
    re.compile(r"(^|/|\\)__pycache__($|/|\\)"),
    re.compile(r"\.pyc$", re.IGNORECASE),
    re.compile(r"(^|/|\\)tmp_root_write_check\.txt$", re.IGNORECASE),
    re.compile(r"(^|/|\\)(?:copy|setup|watchdog|process)[-_]?(?:log|probe)(?:\.txt|\.json)?$", re.IGNORECASE),
)


@dataclass(frozen=True)
class ExtractionResult:
    payload: Any | None
    error: str | None

    @property
    def ok(self) -> bool:
        return self.error is None


@dataclass(frozen=True)
class RunClassification:
    status: str
    final_json_parse_ok: bool
    changed_file_count: int
    sanitized_changed_files: list[dict[str, str]]
    material_changed_file_count: int
    errors: list[str]


def extract_strict_json(text: str, *, marker: str = FINAL_JSON_MARKER) -> ExtractionResult:
    if marker:
        marker_count = text.count(marker)
        if marker_count == 0:
            return ExtractionResult(None, "final_json:marker_missing")
        if marker_count > 1:
            return ExtractionResult(None, "final_json:multiple_markers")
        json_section = text.split(marker, 1)[1].lstrip()
    else:
        json_section = text.lstrip()

    if not json_section:
        return ExtractionResult(None, "final_json:empty")

    try:
        payload, end_index = json.JSONDecoder().raw_decode(json_section)
    except json.JSONDecodeError:
        return ExtractionResult(None, "final_json:invalid_json")

    if json_section[end_index:].strip():
        return ExtractionResult(None, "final_json:trailing_content")
    if not isinstance(payload, dict):
        return ExtractionResult(None, "final_json:not_object")
    return ExtractionResult(payload, None)


def extract_promotion_result(
    text: str, *, material_change_required: bool = True
) -> ValidatedPrimaryResult | QuarantinedPrimaryResult:
    """Extract FINAL_JSON and quarantine every extraction failure consistently."""
    extracted = extract_strict_json(text)
    if extracted.ok:
        return parse_primary_result(extracted.payload, material_change_required)
    return QuarantinedPrimaryResult("invalid_json", (str(extracted.error),), ())


def classify_promotion_pair(
    baseline: ValidatedPrimaryResult | QuarantinedPrimaryResult,
    treatment: ValidatedPrimaryResult | QuarantinedPrimaryResult,
) -> dict[str, bool | str | float | None]:
    """Score only revalidated, comparable primary-result gateway values."""
    gateway_types = (ValidatedPrimaryResult, QuarantinedPrimaryResult)
    if not isinstance(baseline, gateway_types) or not isinstance(treatment, gateway_types):
        raise TypeError("promotion pair inputs must use the parsed-result gateway")
    if isinstance(baseline, QuarantinedPrimaryResult):
        return _quarantined_promotion_pair(f"baseline_{baseline.reason}")
    if isinstance(treatment, QuarantinedPrimaryResult):
        return _quarantined_promotion_pair(f"treatment_{treatment.reason}")

    # Reparse here to defeat forged dataclasses and post-parse payload mutation.
    baseline_payload = baseline.payload
    treatment_payload = treatment.payload
    baseline = parse_primary_result(baseline_payload)
    treatment = parse_primary_result(treatment_payload)
    for field in ("task_id", "corpus_id", "corpus_version", "model_id", "model_reasoning_effort"):
        if (
            field in baseline_payload
            and field in treatment_payload
            and baseline_payload[field] != treatment_payload[field]
        ):
            return _quarantined_promotion_pair(f"{field}_mismatch")
    if isinstance(baseline, QuarantinedPrimaryResult):
        return _quarantined_promotion_pair(f"baseline_{baseline.reason}")
    if isinstance(treatment, QuarantinedPrimaryResult):
        return _quarantined_promotion_pair(f"treatment_{treatment.reason}")
    if baseline.payload["arm"] != "baseline":
        return _quarantined_promotion_pair("baseline_arm_mismatch")
    if treatment.payload["arm"] != "treatment":
        return _quarantined_promotion_pair("treatment_arm_mismatch")
    return {
        "pair_valid_for_scoring": True,
        "invalid_reason": None,
        "score_delta": treatment.payload["behavior_score"] - baseline.payload["behavior_score"],
        "reviewer_required": True,
    }


def _quarantined_promotion_pair(reason: str) -> dict[str, bool | str | float | None]:
    return {
        "pair_valid_for_scoring": False,
        "invalid_reason": reason,
        "score_delta": None,
        "reviewer_required": False,
    }


def material_changed_files(changed_files: Any) -> list[dict[str, str]]:
    if not isinstance(changed_files, list):
        return []

    material: list[dict[str, str]] = []
    for item in changed_files:
        if not isinstance(item, dict):
            continue
        path = item.get("path")
        if not isinstance(path, str) or not path.strip():
            continue
        normalized = path.replace("\\", "/")
        if any(pattern.search(normalized) for pattern in IGNORED_CHANGE_PATTERNS):
            continue
        material.append(
            {
                str(key): str(value)
                for key, value in item.items()
                if isinstance(value, (str, int, float, bool))
            }
        )
    return material


def classify_live_run(
    payload: Any,
    *,
    timed_out: bool = False,
    exit_code: int | None = None,
    material_change_required: bool = True,
) -> RunClassification:
    if timed_out:
        return RunClassification("timeout", False, 0, [], 0, [])
    if not isinstance(payload, dict):
        return RunClassification("invalid_json", False, 0, [], 0, ["run:payload_not_object"])

    changed_files = payload.get("sanitized_changed_files", [])
    material_files = material_changed_files(changed_files)
    declared_count = len(material_files)
    errors = validate_live_run_payload(payload)
    status = str(payload.get("status", "invalid_json"))

    if errors:
        status = "invalid_json"
    elif status == "completed" and material_change_required and declared_count == 0:
        status = "no_op"
    elif exit_code not in (None, 0) and status == "completed":
        status = "wrapper_failure_before_model_call"

    return RunClassification(
        status=status,
        final_json_parse_ok=status not in {"invalid_json", "timeout", "wrapper_failure_before_model_call"},
        changed_file_count=declared_count,
        sanitized_changed_files=material_files,
        material_changed_file_count=declared_count,
        errors=errors,
    )


def classify_pair(baseline: dict[str, Any], treatment: dict[str, Any]) -> dict[str, Any]:
    pair_id = str(
        baseline.get("pair_id")
        or baseline.get("task_id")
        or treatment.get("pair_id")
        or treatment.get("task_id")
    )
    baseline_status = str(baseline.get("status"))
    treatment_status = str(treatment.get("status"))
    invalid_reason = _pair_invalid_reason(baseline_status, treatment_status)
    pair_valid = invalid_reason is None
    score_delta = None
    treatment_equal_or_better = False

    if pair_valid:
        baseline_score = baseline.get("behavior_score")
        treatment_score = treatment.get("behavior_score")
        if isinstance(baseline_score, (int, float)) and isinstance(treatment_score, (int, float)):
            score_delta = treatment_score - baseline_score
            treatment_equal_or_better = treatment_score >= baseline_score

    return {
        "pair_id": pair_id,
        "task_id": pair_id,
        "baseline_status": baseline_status,
        "treatment_status": treatment_status,
        "pair_valid_for_scoring": pair_valid,
        "invalid_reason": invalid_reason,
        "score_delta": score_delta,
        "treatment_equal_or_better": treatment_equal_or_better,
        "reviewer_required": pair_valid,
    }


def validate_live_run_payload(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["run:payload_not_object"]

    for field in LIVE_RUN_REQUIRED_FIELDS:
        if field not in payload:
            errors.append(f"run.{field}:missing")

    status = payload.get("status")
    if status not in LIVE_RUN_STATUS_VALUES:
        errors.append("run.status:unknown")
    if payload.get("arm") not in {"baseline", "treatment"}:
        errors.append("run.arm:unknown")
    if not isinstance(payload.get("timed_out"), bool):
        errors.append("run.timed_out:not_bool")
    if not isinstance(payload.get("final_json_parse_ok"), bool):
        errors.append("run.final_json_parse_ok:not_bool")
    if not isinstance(payload.get("changed_file_count"), int) or payload.get("changed_file_count", -1) < 0:
        errors.append("run.changed_file_count:invalid")
    if not isinstance(payload.get("sanitized_changed_files"), list):
        errors.append("run.sanitized_changed_files:not_list")
    else:
        for index, item in enumerate(payload["sanitized_changed_files"]):
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                errors.append(f"run.sanitized_changed_files[{index}]:invalid")
    if payload.get("retention_status") != "raw_temp_only_repo_sanitized_rollup":
        errors.append("run.retention_status:invalid")
    _validate_hashes(payload.get("raw_output_hashes"), errors, "run.raw_output_hashes")

    if status == "completed" and payload.get("final_json_parse_ok") is not True:
        errors.append("run.final_json:completed_requires_parse_ok")
    if status == "invalid_json" and payload.get("final_json_parse_ok") is not False:
        errors.append("run.final_json:invalid_json_requires_parse_false")
    if status == "timeout" and payload.get("timed_out") is not True:
        errors.append("run.timeout:timed_out_required")
    if status == "no_op" and material_changed_files(payload.get("sanitized_changed_files", [])):
        errors.append("run.changed_files:no_op_has_material_files")

    return errors


def validate_paired_live_eval_result(packet: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(packet, dict):
        return ["packet:payload_not_object"]

    serialized = json.dumps(packet, ensure_ascii=False, sort_keys=True)
    errors.extend(validate_redaction(serialized))
    _validate_no_raw_output_fields(packet, errors, "packet")

    per_task = packet.get("per_task_results")
    pairs = packet.get("pairs")
    aggregate = packet.get("aggregate_result")
    summary = packet.get("execution_summary")
    retention = packet.get("cost_and_retention")

    if not isinstance(per_task, list):
        errors.append("per_task_results:not_list")
        per_task = []
    if not isinstance(pairs, list):
        errors.append("pairs:not_list")
        pairs = []
    if not isinstance(aggregate, dict):
        errors.append("aggregate_result:not_object")
        aggregate = {}
    if not isinstance(summary, dict):
        errors.append("execution_summary:not_object")
        summary = {}

    run_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for index, run in enumerate(per_task):
        run_errors = validate_live_run_payload(run)
        errors.extend(f"per_task_results[{index}].{error}" for error in run_errors)
        if isinstance(run, dict):
            key = (str(run.get("pair_id") or run.get("task_id")), str(run.get("arm")))
            if key in run_by_key:
                errors.append(f"per_task_results[{index}]:duplicate_pair_arm")
            run_by_key[key] = run

    recomputed = {
        "valid_pair_count": 0,
        "invalid_pair_count": 0,
        "timeout_count": sum(1 for run in per_task if isinstance(run, dict) and run.get("status") == "timeout"),
        "no_op_count": sum(1 for run in per_task if isinstance(run, dict) and run.get("status") == "no_op"),
        "invalid_json_count": sum(
            1 for run in per_task if isinstance(run, dict) and run.get("status") == "invalid_json"
        ),
        "treatment_equal_or_better_count": 0,
    }

    seen_pairs: set[str] = set()
    for index, pair in enumerate(pairs):
        if not isinstance(pair, dict):
            errors.append(f"pairs[{index}]:not_object")
            continue
        for field in PAIR_REQUIRED_FIELDS:
            if field not in pair:
                errors.append(f"pairs[{index}].{field}:missing")
        pair_id = str(pair.get("pair_id") or pair.get("task_id"))
        if pair_id in seen_pairs:
            errors.append(f"pairs[{index}].pair_id:duplicate")
        seen_pairs.add(pair_id)

        baseline = run_by_key.get((pair_id, "baseline"))
        treatment = run_by_key.get((pair_id, "treatment"))
        if baseline is None:
            errors.append(f"pairs[{index}].baseline_run:missing")
        if treatment is None:
            errors.append(f"pairs[{index}].treatment_run:missing")
        expected_reason = _pair_invalid_reason(str(pair.get("baseline_status")), str(pair.get("treatment_status")))
        if expected_reason is None:
            recomputed["valid_pair_count"] += 1
            if pair.get("invalid_reason") is not None:
                errors.append(f"pairs[{index}].invalid_reason:must_be_null_for_valid_pair")
        else:
            recomputed["invalid_pair_count"] += 1
            if pair.get("invalid_reason") != expected_reason:
                errors.append(f"pairs[{index}].invalid_reason:expected_{expected_reason}")
            if pair.get("pair_valid_for_scoring") is not False:
                errors.append(f"pairs[{index}].pair_valid_for_scoring:invalid_pair_must_be_false")
        if pair.get("treatment_equal_or_better") is True and expected_reason is None:
            recomputed["treatment_equal_or_better_count"] += 1

    for field in AGGREGATE_REQUIRED_FIELDS:
        if field not in aggregate:
            errors.append(f"aggregate_result.{field}:missing")
    for field, value in recomputed.items():
        if aggregate.get(field) != value:
            errors.append(f"aggregate_result.{field}:expected_{value}")
        if summary.get(field) not in {None, value}:
            errors.append(f"execution_summary.{field}:expected_{value}")

    if recomputed["valid_pair_count"] < len(pairs):
        if summary.get("reviewer_calls_started") not in {None, 0}:
            errors.append("execution_summary.reviewer_calls_started:must_be_zero_when_invalid_pairs")
        if summary.get("reviewer_status") != "not_run_due_invalid_pair_count":
            errors.append("execution_summary.reviewer_status:expected_not_run_due_invalid_pair_count")
        if aggregate.get("promotion_threshold_met") is not False:
            errors.append("aggregate_result.promotion_threshold_met:must_be_false_when_invalid_pairs")
        if aggregate.get("m26_reversed") is not False:
            errors.append("aggregate_result.m26_reversed:must_be_false_when_invalid_pairs")
        if aggregate.get("m35_reversed") is not False:
            errors.append("aggregate_result.m35_reversed:must_be_false_when_invalid_pairs")

    if isinstance(retention, dict):
        if retention.get("raw_outputs_in_repo") is not False:
            errors.append("cost_and_retention.raw_outputs_in_repo:must_be_false")
        if retention.get("raw_outputs_retained_in_temp_only") is not True:
            errors.append("cost_and_retention.raw_outputs_retained_in_temp_only:must_be_true")
        temp_root = retention.get("temp_root_pattern")
        if isinstance(temp_root, str) and temp_root.startswith("C:\\"):
            errors.append("cost_and_retention.temp_root_pattern:concrete_path_forbidden")
    else:
        errors.append("cost_and_retention:not_object")

    no_unapproved = packet.get("no_unapproved_actions")
    if isinstance(no_unapproved, dict):
        for key, value in no_unapproved.items():
            if value is not False:
                errors.append(f"no_unapproved_actions.{key}:must_be_false")
    else:
        errors.append("no_unapproved_actions:not_object")

    return errors


def _validate_hashes(value: Any, errors: list[str], prefix: str) -> None:
    if not isinstance(value, dict):
        errors.append(f"{prefix}:not_object")
        return
    for field in ["prompt_sha256", "stdout_sha256", "stderr_sha256"]:
        item = value.get(field)
        if not isinstance(item, str) or not HASH_FIELD_PATTERN.fullmatch(item):
            errors.append(f"{prefix}.{field}:invalid_sha256")
    for key, item in value.items():
        if str(key).endswith("_length_bytes") and (not isinstance(item, int) or item < 0):
            errors.append(f"{prefix}.{key}:invalid_length")


def _validate_no_raw_output_fields(value: Any, errors: list[str], path: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            next_path = f"{path}.{key_text}"
            if RAW_OUTPUT_FIELD_PATTERN.search(key_text) and not key_text.endswith(("_sha256", "_length_bytes")):
                errors.append(f"{next_path}:raw_output_field_forbidden")
            if validate_redaction(key_text):
                errors.append(f"{next_path}:sensitive_key_forbidden")
            _validate_no_raw_output_fields(item, errors, next_path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _validate_no_raw_output_fields(item, errors, f"{path}[{index}]")


def _pair_invalid_reason(baseline_status: str, treatment_status: str) -> str | None:
    if baseline_status != "completed":
        return f"baseline_{baseline_status}"
    if treatment_status != "completed":
        return f"treatment_{treatment_status}"
    return None
