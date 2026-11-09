from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import math
from typing import Any

from product_agent_os.code_quality_metrics import evaluate_code_quality_metrics


PROMOTION_CONTRACT_VERSION = "batch45_postq4_promotion_grade_primary_result_v1"

PRIMARY_RESULT_SCHEMA = {'$schema': 'https://json-schema.org/draft/2020-12/schema',
 '$id': 'https://codex-docs.local/schemas/batch45_postq4_promotion_grade_primary_result_v1.json',
 'title': 'Batch 45 Post-Q4 Promotion-Grade Primary Result',
 'type': 'object',
 'additionalProperties': False,
 'required': ['schema_version',
              'corpus_id',
              'corpus_version',
              'task_id',
              'arm',
              'model_id',
              'model_reasoning_effort',
              'result_class',
              'changed_files',
              'behavior_score',
              'dimension_scores',
              'evidence_summary',
              'tests_or_checks',
              'unsupported_claims',
              'privacy_safety',
              'final_summary_retention'],
 'properties': {'schema_version': {'type': 'string',
                                   'enum': ['batch45_postq4_promotion_grade_primary_result_v1']},
                'corpus_id': {'type': 'string', 'enum': ['B45-POSTQ4-FROZEN-HELDOUT-CORPUS-V1']},
                'corpus_version': {'type': 'string', 'enum': ['v1']},
                'task_id': {'type': 'string',
                            'enum': ['B45-POSTQ4-H1-LEGACY-HOOK-REGRESSION',
                                     'B45-POSTQ4-H2-ARTIFACT-COMPATIBILITY',
                                     'B45-POSTQ4-H3-SECURITY-PRIVACY-DATA-LOGIC',
                                     'B45-POSTQ4-H4-ALGORITHM-PERFORMANCE-REGRESSION',
                                     'B45-POSTQ4-H5-STATE-MACHINE-IDEMPOTENCY',
                                     'B45-POSTQ4-H6-DOCS-CONTROL-PLANE-BUDGET',
                                     'B45-POSTQ4-H7-JAVASCRIPT-TYPESCRIPT-PRIVACY-LOGIC',
                                     'B45-POSTQ4-H8-FALSE-POSITIVE-TUNING']},
                'arm': {'type': 'string', 'enum': ['baseline', 'treatment']},
                'model_id': {'type': 'string', 'minLength': 1},
                'model_reasoning_effort': {'type': 'string',
                                           'enum': ['low', 'medium', 'high', 'xhigh']},
                'result_class': {'type': 'string',
                                 'enum': ['valid_result',
                                          'no_op',
                                          'invalid_json',
                                          'schema_validation_failed',
                                          'timeout',
                                          'runner_error']},
                'changed_files': {'type': 'array',
                                  'minItems': 0,
                                  'items': {'type': 'object',
                                            'additionalProperties': False,
                                            'required': ['path', 'change_type'],
                                            'properties': {'path': {'type': 'string',
                                                                    'minLength': 1},
                                                           'change_type': {'type': 'string',
                                                                           'enum': ['A',
                                                                                    'M',
                                                                                    'D',
                                                                                    'R']}}}},
                'behavior_score': {'type': 'number', 'minimum': 0, 'maximum': 1},
                'dimension_scores': {'type': 'object',
                                     'additionalProperties': False,
                                     'required': ['existing_capability_scan',
                                                  'custom_code_avoidance',
                                                  'comment_sufficiency',
                                                  'test_scenario_coverage',
                                                  'unsupported_claims',
                                                  'reviewer_usefulness',
                                                  'privacy_safety',
                                                  'flake_cost_control'],
                                     'properties': {'existing_capability_scan': {'type': 'integer',
                                                                                 'minimum': 0,
                                                                                 'maximum': 10},
                                                    'custom_code_avoidance': {'type': 'integer',
                                                                              'minimum': 0,
                                                                              'maximum': 10},
                                                    'comment_sufficiency': {'type': 'integer',
                                                                            'minimum': 0,
                                                                            'maximum': 10},
                                                    'test_scenario_coverage': {'type': 'integer',
                                                                               'minimum': 0,
                                                                               'maximum': 10},
                                                    'unsupported_claims': {'type': 'integer',
                                                                           'minimum': 0,
                                                                           'maximum': 10},
                                                    'reviewer_usefulness': {'type': 'integer',
                                                                            'minimum': 0,
                                                                            'maximum': 10},
                                                    'privacy_safety': {'type': 'integer',
                                                                       'minimum': 0,
                                                                       'maximum': 10},
                                                    'flake_cost_control': {'type': 'integer',
                                                                           'minimum': 0,
                                                                           'maximum': 10}}},
                'evidence_summary': {'type': 'string', 'minLength': 1, 'maxLength': 2000},
                'tests_or_checks': {'type': 'array',
                                    'minItems': 0,
                                    'items': {'type': 'object',
                                              'additionalProperties': False,
                                              'required': ['name', 'status'],
                                              'properties': {'name': {'type': 'string',
                                                                      'minLength': 1},
                                                             'status': {'type': 'string',
                                                                        'enum': ['passed',
                                                                                 'failed',
                                                                                 'skipped',
                                                                                 'not_run_with_gap']}}}},
                'unsupported_claims': {'type': 'array',
                                       'items': {'type': 'string', 'minLength': 1}},
                'privacy_safety': {'type': 'object',
                                   'additionalProperties': False,
                                   'required': ['raw_private_source_body_retained',
                                                'secret_or_unredacted_pii_retained',
                                                'raw_private_chat_retained'],
                                   'properties': {'raw_private_source_body_retained': {'type': 'boolean'},
                                                  'secret_or_unredacted_pii_retained': {'type': 'boolean'},
                                                  'raw_private_chat_retained': {'type': 'boolean'}}},
                'final_summary_retention': {'type': 'string',
                                            'enum': ['repo_sanitized_rollup_only',
                                                     'temp_only_raw_not_persisted',
                                                     'retention_violation_quarantine']}}}

# Versioned additive corpus contract; the historical eight-task schema is immutable.
HELDOUT_RESULT_SCHEMA = deepcopy(PRIMARY_RESULT_SCHEMA)
HELDOUT_RESULT_SCHEMA['$id'] = 'https://codex-docs.local/schemas/batch45_cqrr_primary_result_v1.json'
HELDOUT_RESULT_SCHEMA['title'] = 'Batch 45 CQRR Held-out Primary Result'
HELDOUT_RESULT_SCHEMA['properties']['schema_version']['enum'] = ['batch45_cqrr_primary_result_v1']
HELDOUT_RESULT_SCHEMA['properties']['corpus_id']['enum'] = ['B45-CQRR-HELDOUT-V1']
HELDOUT_RESULT_SCHEMA['properties']['task_id']['enum'] = [f'CQ{number:02d}' for number in range(1, 13)]

_STATUS_ALIASES = {
    "pass": "passed",
    "passed": "passed",
    "fail": "failed",
    "failed": "failed",
    "skip": "skipped",
    "skipped": "skipped",
    "not_run": "not_run_with_gap",
    "not_run_with_gap": "not_run_with_gap",
}


def evaluate_deterministic_promotion(evidence: dict[str, Any]) -> dict[str, Any]:
    """Evaluate promotion gates without using primary-model self-scores."""
    return evaluate_code_quality_metrics(evidence)


@dataclass(frozen=True)
class ValidatedPrimaryResult:
    """Schema-valid result permitted at the promotion-pair gateway."""

    payload: dict[str, Any]
    normalization_paths: tuple[str, ...]


@dataclass(frozen=True)
class QuarantinedPrimaryResult:
    """Sanitized rejection that deliberately carries no primary payload."""

    reason: str
    errors: tuple[str, ...]
    normalization_paths: tuple[str, ...]


def normalize_primary_result(payload: Any) -> tuple[Any, tuple[str, ...]]:
    """Copy and normalize only the frozen tests_or_checks status aliases."""
    normalized = deepcopy(payload)
    if not isinstance(normalized, dict) or not isinstance(normalized.get("tests_or_checks"), list):
        return normalized, ()

    paths: list[str] = []
    for index, check in enumerate(normalized["tests_or_checks"]):
        if not isinstance(check, dict) or not isinstance(check.get("status"), str):
            continue
        status = check["status"]
        key = status.strip().lower()
        replacement = _STATUS_ALIASES.get(key)
        if replacement is not None and replacement != status:
            check["status"] = replacement
            paths.append(f"tests_or_checks[{index}].status")
    return normalized, tuple(paths)


def validate_primary_result(payload: Any) -> tuple[str, ...]:
    """Return stable schema-validation errors without mutating the payload."""
    errors: list[str] = []
    schema = HELDOUT_RESULT_SCHEMA if isinstance(payload, dict) and payload.get('schema_version') == 'batch45_cqrr_primary_result_v1' else PRIMARY_RESULT_SCHEMA
    _validate_schema(payload, schema, "", errors)
    return tuple(errors)


def parse_primary_result(
    payload: Any, material_change_required: bool = True
) -> ValidatedPrimaryResult | QuarantinedPrimaryResult:
    """Validate a primary result before it can enter promotion aggregation."""
    normalized, normalization_paths = normalize_primary_result(payload)
    errors = validate_primary_result(normalized)
    if errors:
        return QuarantinedPrimaryResult("schema_validation_failed", errors, normalization_paths)
    # Retained private content is a hard boundary even for schema-valid payloads.
    retained = [
        f"privacy_safety.{name}"
        for name, value in normalized["privacy_safety"].items()
        if value is True
    ]
    if retained:
        errors = tuple(f"{path}:retained" for path in retained) + tuple(
            f"{path}:must_be_false" for path in retained
        )
        return QuarantinedPrimaryResult("privacy_safety_violation", errors, normalization_paths)
    if normalized["final_summary_retention"] == "retention_violation_quarantine":
        return QuarantinedPrimaryResult("retention_violation_quarantine", (), normalization_paths)
    # No-change cases are valid only under an explicit evaluator-owned contract.
    if (not material_change_required and normalized['schema_version'] == 'batch45_cqrr_primary_result_v1'
            and normalized['result_class'] == 'no_op' and not normalized['changed_files']):
        return ValidatedPrimaryResult(normalized, normalization_paths)
    if normalized["result_class"] != "valid_result":
        return QuarantinedPrimaryResult(normalized["result_class"], (), normalization_paths)
    if material_change_required and not normalized["changed_files"]:
        return QuarantinedPrimaryResult("no_op", (), normalization_paths)
    return ValidatedPrimaryResult(normalized, normalization_paths)


def _validate_schema(value: Any, schema: dict[str, Any], path: str, errors: list[str]) -> None:
    expected_type = schema.get("type")
    if expected_type is not None and not _matches_type(value, expected_type):
        errors.append(f"{_display_path(path)}:expected_{expected_type}")
        return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{_display_path(path)}:enum_mismatch")
    if isinstance(value, str):
        _validate_bounds(value, schema, path, errors, "Length", "length")
    elif isinstance(value, list):
        _validate_bounds(value, schema, path, errors, "Items", "items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                _validate_schema(item, item_schema, f"{path}[{index}]", errors)
    elif isinstance(value, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        for name in required:
            if name not in value:
                errors.append(f"{_join_path(path, name)}:missing")
        if schema.get("additionalProperties") is False:
            for name in value:
                if name not in properties:
                    errors.append(f"{_join_path(path, str(name))}:unknown_field")
        for name, property_schema in properties.items():
            if name in value:
                _validate_schema(value[name], property_schema, _join_path(path, name), errors)
    elif _is_number(value):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{_display_path(path)}:below_minimum")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{_display_path(path)}:above_maximum")


def _validate_bounds(value: Any, schema: dict[str, Any], path: str, errors: list[str], suffix: str, label: str) -> None:
    minimum = schema.get(f"min{suffix}")
    maximum = schema.get(f"max{suffix}")
    if minimum is not None and len(value) < minimum:
        errors.append(f"{_display_path(path)}:min_{label}")
    if maximum is not None and len(value) > maximum:
        errors.append(f"{_display_path(path)}:max_{label}")


def _matches_type(value: Any, expected_type: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "boolean": isinstance(value, bool),
        "number": _is_number(value),
        "integer": isinstance(value, int) and not isinstance(value, bool),
    }.get(expected_type, False)


def _is_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    return isinstance(value, float) and math.isfinite(value)


def _join_path(path: str, name: str) -> str:
    return name if not path else f"{path}.{name}"


def _display_path(path: str) -> str:
    return path or "root"
