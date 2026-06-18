from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from product_agent_os.first_run_analysis import GENERATED_VIEW_POLICY
from product_agent_os.stage_manifest import canonical_json, content_digest


M21_ATTEMPT_SCHEMA_VERSION = "batch39_m21_attempt_summary_v1"
M21_ROLLUP_SCHEMA_VERSION = "batch39_m21_three_target_rollup_v1"
M21_ATTEMPT_IDS = {
    "B39-TEST-M21-A01",
    "B39-TEST-M21-A02",
    "B39-TEST-M21-A03",
}
M21_FILENAMES = {
    "B39-TEST-M21-A01": "batch39-m21-synthetic-plugin-skill-summary.json",
    "B39-TEST-M21-A02": "batch39-m21-neural-flow-readonly-summary.json",
    "B39-TEST-M21-A03": "batch39-m21-sol-readonly-summary.json",
}
M21_ROLLUP_FILENAME = "batch39-m21-three-target-rollup.json"
_LOCAL_ABSOLUTE_PATH_RE = re.compile(r"(?:[A-Za-z]:[\\/]|\\\\|/Users/|/home/|/tmp/)")


def build_m21_attempt_summary(
    *,
    attempt_id: str,
    target_label: str,
    target_kind: str,
    mode: str,
    source_policy_status: str,
    first_run_packet: dict[str, Any],
    rendered_artifact: dict[str, Any] | None = None,
    generated_at: str = "2026-06-18T00:00:00Z",
) -> dict[str, Any]:
    """Build one Batch 39 M21 attempt summary without retaining target-local paths."""

    packet = _packet_payload(first_run_packet)
    target_label_text = str(target_label).strip()
    artifact = rendered_artifact or {}
    archetypes = _detected_archetypes(packet)
    summary_status = _summary_status(attempt_id, source_policy_status)
    summary = {
        "schema_version": M21_ATTEMPT_SCHEMA_VERSION,
        "batch": "B39",
        "test_id": "B39-TEST-M21",
        "attempt_id": attempt_id,
        "generated_at": generated_at,
        "target": {
            "label": target_label_text,
            "kind": str(target_kind).strip(),
            "location_ref": _target_location_ref(target_kind),
        },
        "mode": str(mode).strip(),
        "summary_status": summary_status,
        "source_policy_status": str(source_policy_status).strip(),
        "comparison_role": _comparison_role(attempt_id),
        "first_run_artifact": {
            "status": str(artifact.get("status", "packet_only_dry_run")),
            "page_count": int(artifact.get("page_count", 0) or 0),
            "manifest_ref": str(artifact.get("manifest_ref", "not_rendered")),
            "packet_ref": str(artifact.get("packet_ref", "packet_digest_only")),
            "packet_digest": str(_packet_digest(packet)),
            "detected_archetypes": archetypes,
        },
        "plugin_skill_contract": _plugin_skill_contract(attempt_id, archetypes, artifact),
        "first_run_artifact_usefulness": _artifact_usefulness(attempt_id, artifact, packet),
        "synthetic_write_status": _synthetic_write_status(attempt_id, artifact),
        "generated_view_policy": GENERATED_VIEW_POLICY,
        "unsupported_claims": _unsupported_claims(attempt_id),
        "approval_boundary": _approval_boundary(),
        "next_action": _next_action(attempt_id),
    }
    summary["attempt_digest"] = content_digest(canonical_json(summary))
    errors = validate_m21_attempt_summary(summary)
    if errors:
        raise ValueError("; ".join(errors))
    return summary


def build_m21_three_target_rollup(
    attempts: list[dict[str, Any]],
    *,
    generated_at: str,
) -> dict[str, Any]:
    """Build the three-target M21 rollup from validated attempt summaries."""

    for attempt in attempts:
        errors = validate_m21_attempt_summary(attempt)
        if errors:
            raise ValueError("; ".join(errors))
    attempt_ids = [str(attempt.get("attempt_id", "")) for attempt in attempts]
    rollup = {
        "schema_version": M21_ROLLUP_SCHEMA_VERSION,
        "batch": "B39",
        "test_id": "B39-TEST-M21",
        "generated_at": generated_at,
        "attempt_count": len(attempts),
        "attempt_ids": attempt_ids,
        "rollup_status": "accepted_risk_three_target_evidence",
        "release_readiness_supported": False,
        "target_mutation_performed": any(
            attempt.get("approval_boundary", {}).get("target_workspace_mutation") != "not_performed"
            for attempt in attempts
        ),
        "provider_or_external_actions_performed": False,
        "generated_view_policy": GENERATED_VIEW_POLICY,
        "evidence_refs": [
            {"attempt_id": attempt_id, "path": M21_FILENAMES[attempt_id]}
            for attempt_id in attempt_ids
            if attempt_id in M21_FILENAMES
        ],
        "control_plane_ref": "prod_test.md#B39-TEST-M21",
        "next_route": "B39-S3",
        "next_action": "Continue Batch 39 through B39-S3 route accuracy only after recording accepted M21 evidence gaps.",
        "accepted_gaps": [
            "real target runtime/browser/provider checks not performed",
            "generated views remain orientation evidence, not proof",
            "source-policy positive apply remains unsupported for read-only targets",
        ],
    }
    rollup["rollup_digest"] = content_digest(canonical_json(rollup))
    errors = validate_m21_three_target_rollup(rollup)
    if errors:
        raise ValueError("; ".join(errors))
    return rollup


def write_m21_evidence_pack(
    output_dir: str | Path,
    attempts: list[dict[str, Any]],
    rollup: dict[str, Any],
) -> dict[str, str]:
    """Write M21 evidence JSON files with stable names."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    written: dict[str, str] = {}
    for attempt in attempts:
        attempt_id = str(attempt.get("attempt_id", ""))
        filename = M21_FILENAMES.get(attempt_id)
        if not filename:
            raise ValueError(f"unsupported attempt id: {attempt_id}")
        _write_json(output_path / filename, attempt)
        written[filename] = filename
    _write_json(output_path / M21_ROLLUP_FILENAME, rollup)
    written[M21_ROLLUP_FILENAME] = M21_ROLLUP_FILENAME
    return written


def validate_m21_attempt_summary(summary: Any) -> list[str]:
    if not isinstance(summary, dict):
        return ["attempt summary must be an object"]
    errors: list[str] = []
    for field in [
        "schema_version",
        "batch",
        "test_id",
        "attempt_id",
        "target",
        "mode",
        "summary_status",
        "source_policy_status",
        "first_run_artifact",
        "generated_view_policy",
        "unsupported_claims",
        "approval_boundary",
        "attempt_digest",
    ]:
        if field not in summary:
            errors.append(f"{field} is required")
    if summary.get("schema_version") != M21_ATTEMPT_SCHEMA_VERSION:
        errors.append(f"schema_version must be {M21_ATTEMPT_SCHEMA_VERSION}")
    if summary.get("batch") != "B39":
        errors.append("batch must be B39")
    if summary.get("test_id") != "B39-TEST-M21":
        errors.append("test_id must be B39-TEST-M21")
    if summary.get("attempt_id") not in M21_ATTEMPT_IDS:
        errors.append("attempt_id is not a known M21 attempt")
    if summary.get("generated_view_policy") != GENERATED_VIEW_POLICY:
        errors.append(f"generated_view_policy must be {GENERATED_VIEW_POLICY}")
    if not isinstance(summary.get("unsupported_claims"), list):
        errors.append("unsupported_claims must be list")
    errors.extend(_validate_boundary(summary.get("approval_boundary")))
    encoded = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    if _LOCAL_ABSOLUTE_PATH_RE.search(encoded.replace("\\\\", "\\")):
        errors.append("local absolute path leaked")
    if any(raw_key in encoded for raw_key in ['"raw_source"', '"raw_body"', '"raw_file_body"', '"raw_private_log"']):
        errors.append("raw source field retained")
    if not str(summary.get("attempt_digest", "")).startswith("sha256:"):
        errors.append("attempt_digest must be a sha256 digest")
    return errors


def validate_m21_three_target_rollup(rollup: Any) -> list[str]:
    if not isinstance(rollup, dict):
        return ["rollup must be an object"]
    errors: list[str] = []
    for field in [
        "schema_version",
        "batch",
        "test_id",
        "attempt_count",
        "attempt_ids",
        "rollup_status",
        "release_readiness_supported",
        "target_mutation_performed",
        "next_route",
        "rollup_digest",
    ]:
        if field not in rollup:
            errors.append(f"{field} is required")
    if rollup.get("schema_version") != M21_ROLLUP_SCHEMA_VERSION:
        errors.append(f"schema_version must be {M21_ROLLUP_SCHEMA_VERSION}")
    if rollup.get("batch") != "B39":
        errors.append("batch must be B39")
    if rollup.get("test_id") != "B39-TEST-M21":
        errors.append("test_id must be B39-TEST-M21")
    if rollup.get("release_readiness_supported") is not False:
        errors.append("release_readiness_supported must be false")
    if rollup.get("target_mutation_performed") is not False:
        errors.append("target_mutation_performed must be false")
    if not str(rollup.get("rollup_digest", "")).startswith("sha256:"):
        errors.append("rollup_digest must be a sha256 digest")
    encoded = json.dumps(rollup, ensure_ascii=False, sort_keys=True)
    if _LOCAL_ABSOLUTE_PATH_RE.search(encoded.replace("\\\\", "\\")):
        errors.append("local absolute path leaked")
    return errors


def _packet_payload(first_run_packet: dict[str, Any]) -> dict[str, Any]:
    if isinstance(first_run_packet, dict) and isinstance(first_run_packet.get("packet"), dict):
        return first_run_packet["packet"]
    return first_run_packet


def _detected_archetypes(packet: dict[str, Any]) -> list[str]:
    workspace = packet.get("workspace") if isinstance(packet, dict) else {}
    archetypes = workspace.get("detected_archetypes") if isinstance(workspace, dict) else None
    if isinstance(archetypes, list) and archetypes:
        return sorted(str(item) for item in archetypes)
    target = packet.get("target", {}) if isinstance(packet, dict) else {}
    label = str(target.get("label", "") if isinstance(target, dict) else "")
    if "plugin" in label.lower() or "skill" in label.lower():
        return ["plugin_skill"]
    return ["unknown"]


def _packet_digest(packet: dict[str, Any]) -> str:
    digest = packet.get("packet_digest") if isinstance(packet, dict) else None
    if isinstance(digest, str) and digest.startswith("sha256:"):
        return digest
    return content_digest(canonical_json(packet))


def _target_location_ref(target_kind: str) -> str:
    if str(target_kind) == "synthetic_fixture":
        return "workspace_fixture:batch39-m21-plugin-skill-fixture"
    return "approved_read_only_target:redacted"


def _summary_status(attempt_id: str, source_policy_status: str) -> str:
    if attempt_id == "B39-TEST-M21-A01":
        return "passed_contract_guardrail"
    if attempt_id == "B39-TEST-M21-A02":
        return "blocked_expected_source_policy"
    if attempt_id == "B39-TEST-M21-A03":
        return "inspection_only_real_target_value"
    return str(source_policy_status)


def _comparison_role(attempt_id: str) -> str:
    return {
        "B39-TEST-M21-A01": "primary_pass_fail_contract",
        "B39-TEST-M21-A02": "expected_block_behavior",
        "B39-TEST-M21-A03": "first_run_artifact_usefulness",
    }.get(attempt_id, "unknown")


def _plugin_skill_contract(
    attempt_id: str,
    archetypes: list[str],
    artifact: dict[str, Any],
) -> dict[str, Any]:
    if attempt_id != "B39-TEST-M21-A01":
        return {"status": "not_applicable", "required": False}
    passed = "plugin_skill" in archetypes and int(artifact.get("page_count", 0) or 0) == 11
    return {
        "status": "passed" if passed else "failed",
        "required": True,
        "required_archetype": "plugin_skill",
        "required_page_count": 11,
    }


def _artifact_usefulness(
    attempt_id: str,
    artifact: dict[str, Any],
    packet: dict[str, Any],
) -> dict[str, Any]:
    if attempt_id == "B39-TEST-M21-A03":
        return {
            "status": "usefulness_signal_recorded",
            "signal_basis": "first-run dry-run packet classified target shape without target mutation",
            "packet_digest": _packet_digest(packet),
        }
    if artifact:
        return {"status": "rendered_artifact_available", "page_count": int(artifact.get("page_count", 0) or 0)}
    return {"status": "packet_only", "packet_digest": _packet_digest(packet)}


def _synthetic_write_status(attempt_id: str, artifact: dict[str, Any]) -> str:
    if attempt_id != "B39-TEST-M21-A01":
        return "not_applicable_read_only"
    if artifact.get("status") == "rendered_in_temp_copy":
        return "allowed_generated_analysis_only"
    return "packet_only_no_target_write"


def _unsupported_claims(attempt_id: str) -> list[str]:
    common = [
        "live_runtime",
        "browser_ui",
        "provider_calls",
        "target_apply",
        "git_release",
        "automation_activation",
        "release_readiness",
    ]
    if attempt_id == "B39-TEST-M21-A01":
        return [claim for claim in common if claim != "target_apply"]
    return common + ["clean_positive_source_policy"]


def _approval_boundary() -> dict[str, str]:
    return {
        "target_workspace_mutation": "not_performed",
        "provider_or_api_calls": "not_performed",
        "browser_automation": "not_performed",
        "live_server": "not_performed",
        "external_actions": "not_performed",
        "git_actions": "not_performed",
        "automation_activation": "not_performed",
        "local_evidence_artifact_write": "allowed_workspace_output_only",
    }


def _next_action(attempt_id: str) -> str:
    if attempt_id == "B39-TEST-M21-A01":
        return "Use synthetic pass/fail result as the M21 baseline contract."
    if attempt_id == "B39-TEST-M21-A02":
        return "Record Neural Flow expected-block behavior; do not infer apply readiness."
    return "Use SOL first-run usefulness signal to tune B39-S3 route accuracy questions."


def _validate_boundary(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["approval_boundary must be an object"]
    errors: list[str] = []
    for field, expected in _approval_boundary().items():
        if value.get(field) != expected:
            errors.append(f"approval_boundary.{field} must be {expected}")
    return errors


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


__all__ = [
    "M21_ATTEMPT_SCHEMA_VERSION",
    "M21_ROLLUP_SCHEMA_VERSION",
    "build_m21_attempt_summary",
    "build_m21_three_target_rollup",
    "validate_m21_attempt_summary",
    "validate_m21_three_target_rollup",
    "write_m21_evidence_pack",
]

