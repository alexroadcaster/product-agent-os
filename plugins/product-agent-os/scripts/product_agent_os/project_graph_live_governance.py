"""Live semantic runtime governance for Product-Agent OS project graphs.

Batch 24 defines approval, classification, redaction, credential, cache and
budget gates. It does not start a server, call providers or mutate canonical
graph facts.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import redact_payload, validate_redaction
from product_agent_os.project_graph_sanitization import safe_relative_path_text, sanitize_graph_text


LIVE_GOVERNANCE_TARGET = ".codex/product-agent-os/project-code-graph-live-governance.json"
LIVE_CACHE_TARGET = ".codex/product-agent-os/project-code-graph-live-cache.json"
_APPROVAL_FIELDS = {
    "explicit_approval",
    "owner",
    "allowed_surfaces",
    "data_classification",
    "redaction_boundary",
    "provider_policy",
    "credential_policy",
    "cache_policy",
    "budget_policy",
    "rollback_path",
    "residual_risks",
}
_BATCH24_ALLOWED_SURFACES = {
    "approval_packet",
    "data_classification",
    "redaction_pipeline",
    "credential_boundary",
    "cache_policy",
    "budget_policy",
}
_BLOCKED_INPUTS = {"absolute_local_paths", "raw_source_bodies", "secrets"}
_SECRET_KEY_TERMS = ("secret", "token", "password", "api_key", "apikey", "private_key", "credential_value")
_SECRET_VALUE_PATTERN = re.compile(
    r"(?i)\b(?:sk-[a-z0-9_-]{8,}|api[_-]?key\s*=\s*[^\s\"'<>]+|token\s*=\s*[^\s\"'<>]+)"
)
_WINDOWS_PATH_PATTERN = re.compile(r"\b[A-Za-z]:[\\/][^\s\"'<>]+")
_POSIX_PATH_PATTERN = re.compile(r"(^|\s)/(Users|home|private|Volumes|mnt|tmp|var)/[^\s\"'<>]+")


def validate_live_runtime_approval(approval: dict[str, Any] | None) -> dict[str, Any]:
    """Validate the explicit Batch 24 governance approval packet."""

    if not isinstance(approval, dict):
        return _validation(False, ["live_governance_approval:missing"], "live_governance_approval")
    errors: list[str] = []
    missing = sorted(field for field in _APPROVAL_FIELDS if field not in approval)
    errors.extend(f"live_governance_approval:{field}:missing" for field in missing)
    if approval.get("explicit_approval") is not True:
        errors.append("live_governance_approval:explicit_approval")
    if not sanitize_graph_text(approval.get("owner") or ""):
        errors.append("live_governance_approval:owner")

    allowed_surfaces = {str(item) for item in approval.get("allowed_surfaces", []) if isinstance(item, str)}
    for required in sorted(_BATCH24_ALLOWED_SURFACES):
        if required not in allowed_surfaces:
            errors.append(f"live_governance_approval:allowed_surfaces:{required}:missing")
    for surface in sorted(allowed_surfaces - _BATCH24_ALLOWED_SURFACES):
        errors.append(f"live_governance_approval:allowed_surfaces:{surface}")

    errors.extend(_validate_data_classification(approval.get("data_classification")))
    errors.extend(_validate_redaction_boundary(approval.get("redaction_boundary")))
    errors.extend(_validate_provider_policy(approval.get("provider_policy")))
    errors.extend(_validate_credential_policy(approval.get("credential_policy")))
    errors.extend(_validate_cache_policy(approval.get("cache_policy")))
    errors.extend(_validate_budget_policy(approval.get("budget_policy")))
    if approval.get("rollback_path") != f"delete {LIVE_GOVERNANCE_TARGET}":
        errors.append("live_governance_approval:rollback_path")
    if not isinstance(approval.get("residual_risks"), list):
        errors.append("live_governance_approval:residual_risks")
    if _has_unsafe_text(approval):
        errors.append("live_governance_approval:unsafe_text")
    return _validation(not errors, errors, "live_governance_approval")


def build_live_governance_packet(approval: dict[str, Any] | None) -> dict[str, Any]:
    """Build a source-free governance packet for Task 26 Batch 24."""

    validation = validate_live_runtime_approval(approval)
    approval = approval if isinstance(approval, dict) else {}
    status = "ready" if validation["ok"] else ("blocked" if approval.get("explicit_approval") is True else "approval_required")
    packet = {
        "schema_version": 1,
        "artifact_kind": "project_graph_live_governance",
        "write_policy": "read_only",
        "status": status,
        "approval_boundary": "batch24_live_governance_only_no_live_calls",
        "source_boundary": "approval_policy_metadata_only_no_raw_source_or_secret_material",
        "generated_view_policy": "live_governance_packet_is_policy_evidence_not_source_of_truth",
        "owner": sanitize_graph_text(approval.get("owner") or ""),
        "allowed_surfaces": sorted(
            surface
            for surface in (str(item) for item in approval.get("allowed_surfaces", []) if isinstance(item, str))
            if surface in _BATCH24_ALLOWED_SURFACES
        ),
        "blocked_surfaces": [
            "live_server_start",
            "external_provider_call",
            "canonical_graph_mutation",
            "external_write",
            "git_action",
        ],
        "data_classification": _data_classification_packet(approval.get("data_classification")),
        "redaction_guard": _redaction_guard_packet(approval.get("redaction_boundary")),
        "provider_policy": _provider_policy_packet(approval.get("provider_policy")),
        "credential_policy": _credential_policy_packet(approval.get("credential_policy")),
        "cache_policy": _cache_policy_packet(approval),
        "budget_policy": _budget_policy_packet(approval.get("budget_policy")),
        "rollback": {
            "disable_path": f"delete {LIVE_GOVERNANCE_TARGET}",
            "delete_generated_cache_path": f"delete {LIVE_CACHE_TARGET}",
            "fallback": "graph_only_query_mode",
            "deletion_scope": "stage_root_generated_live_governance_and_cache_only",
        },
        "residual_risks": [
            sanitize_graph_text(item)
            for item in approval.get("residual_risks", [])
            if isinstance(item, str)
        ][:10],
        "safe_next_action": (
            "Use Batch 24 governance as prerequisite evidence only; live/provider/mutation work remains disabled."
        ),
        "validation": validation,
    }
    safe_packet, report = redact_payload(packet)
    if isinstance(safe_packet, dict):
        safe_packet["redaction_summary"] = report
        safe_packet["validation"] = _merge_validation(
            safe_packet.get("validation", validation),
            validate_live_governance_packet(safe_packet),
        )
        if safe_packet["validation"]["ok"] is not True and safe_packet.get("status") == "ready":
            safe_packet["status"] = "blocked"
        return safe_packet
    return packet


def validate_live_governance_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate Batch 24 governance packet schema and safety invariants."""

    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("schema_version")
    if packet.get("artifact_kind") != "project_graph_live_governance":
        errors.append("artifact_kind")
    if packet.get("write_policy") != "read_only":
        errors.append("write_policy")
    if packet.get("approval_boundary") != "batch24_live_governance_only_no_live_calls":
        errors.append("approval_boundary")
    provider_policy = packet.get("provider_policy") if isinstance(packet.get("provider_policy"), dict) else {}
    if provider_policy.get("external_provider_calls_allowed") is not False:
        errors.append("provider_policy:external_calls")
    credential_policy = packet.get("credential_policy") if isinstance(packet.get("credential_policy"), dict) else {}
    if credential_policy.get("secret_material_stored") is not False:
        errors.append("credential_policy:secret_material")
    cache_policy = packet.get("cache_policy") if isinstance(packet.get("cache_policy"), dict) else {}
    if cache_policy.get("deletion_proof_required") is not True:
        errors.append("cache_policy:deletion_proof")
    budget_policy = packet.get("budget_policy") if isinstance(packet.get("budget_policy"), dict) else {}
    if _positive_int(budget_policy.get("max_mutation_tokens"), -1) != 0:
        errors.append("budget_policy:max_mutation_tokens")
    if _positive_int(budget_policy.get("max_cost_units"), -1) != 0:
        errors.append("budget_policy:max_cost_units")
    if _has_unsafe_text(packet):
        errors.append("source_boundary:unsafe_text")
    redacted_render = json.dumps(packet, sort_keys=True, default=str)
    errors.extend(f"redaction:{error}" for error in validate_redaction(redacted_render))
    return _validation(not errors, errors, "live_governance_packet")


def sanitize_live_provider_payload(payload: dict[str, Any], *, approval: dict[str, Any] | None) -> dict[str, Any]:
    """Sanitize a would-be provider payload and block unsafe inputs before any live call."""

    approval_validation = validate_live_runtime_approval(approval)
    if approval_validation["ok"] is not True:
        return {
            "schema_version": 1,
            "status": "approval_required",
            "provider_call_allowed": False,
            "sanitized_payload": {},
            "validation": approval_validation,
        }
    errors = sorted(set(_blocked_payload_errors(payload)))
    sanitized = _sanitize_payload(payload)
    redacted, report = redact_payload(sanitized)
    if not isinstance(redacted, dict):
        redacted = {}
    rendered = json.dumps(redacted, sort_keys=True, default=str)
    errors.extend(f"redaction:{error}" for error in validate_redaction(rendered))
    status = "ready" if not errors else "blocked"
    return {
        "schema_version": 1,
        "status": status,
        "provider_payload_status": status,
        "provider_call_allowed": False,
        "live_action_boundary": "provider_call_still_disabled_until_later_task26_batch",
        "sanitized_payload": redacted if not errors else {},
        "redaction_summary": report,
        "validation": _validation(not errors, errors, "live_provider_payload_redaction_guard"),
    }


def enforce_live_budget(request: dict[str, Any], budget_policy: dict[str, Any]) -> dict[str, Any]:
    """Check a proposed live/provider action against Batch 24 hard budget limits."""

    errors: list[str] = []
    estimated_tokens = _positive_int(request.get("estimated_tokens"), 0)
    estimated_query_tokens = _positive_int(request.get("estimated_query_tokens"), estimated_tokens)
    estimated_mutation_tokens = _positive_int(request.get("estimated_mutation_tokens"), 0)
    estimated_cost_units = _positive_int(request.get("estimated_cost_units"), 0)
    estimated_latency_ms = _positive_int(request.get("estimated_latency_ms"), 0)
    if estimated_tokens > _positive_int(budget_policy.get("max_run_tokens"), 0):
        errors.append("budget:estimated_tokens")
    if estimated_query_tokens > _positive_int(budget_policy.get("max_query_tokens"), 0):
        errors.append("budget:estimated_query_tokens")
    if estimated_mutation_tokens > _positive_int(budget_policy.get("max_mutation_tokens"), 0):
        errors.append("budget:estimated_mutation_tokens")
    if estimated_cost_units > _positive_int(budget_policy.get("max_cost_units"), 0):
        errors.append("budget:estimated_cost_units")
    if estimated_latency_ms > _positive_int(budget_policy.get("max_latency_ms"), 0):
        errors.append("budget:estimated_latency_ms")
    return {
        "schema_version": 1,
        "status": "ready" if not errors else "blocked",
        "degraded_mode": "graph_only" if errors else "not_required",
        "errors": errors,
        "budget_policy": _budget_policy_packet(budget_policy),
    }


def stage_live_governance(
    stage_root: str | Path,
    *,
    workspace: str | Path,
    approval: dict[str, Any] | None,
) -> dict[str, Any]:
    """Stage Batch 24 live governance under an explicit stage root."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    packet = build_live_governance_packet(approval)
    target = stage_path / LIVE_GOVERNANCE_TARGET
    action = "blocked"
    if packet.get("status") == "ready" and packet.get("validation", {}).get("ok") is True:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
        action = "create"
    return {
        "rendered_artifacts": {
            "status": packet.get("status"),
            "mode": "validate-live-governance",
            "root_status": "redacted",
            "source_boundary": packet.get("source_boundary"),
            "provider_calls": "not_performed",
            "server_started": False,
            "canonical_graph_mutation": "not_performed",
            "files": [
                {
                    "target_path": LIVE_GOVERNANCE_TARGET,
                    "action": action,
                    "write_policy": "staged_only" if action == "create" else "blocked",
                    "staged_path": LIVE_GOVERNANCE_TARGET,
                }
            ],
            "validation": packet.get("validation"),
            "rollback": packet.get("rollback"),
        }
    }


def disable_live_governance(stage_root: str | Path, *, workspace: str | Path) -> dict[str, Any]:
    """Delete generated Batch 24 governance/cache artifacts from stage root only."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    deleted: list[str] = []
    for relative in [LIVE_GOVERNANCE_TARGET, LIVE_CACHE_TARGET]:
        target = stage_path / relative
        if target.exists() and target.is_file():
            target.unlink()
            deleted.append(relative)
    return {
        "rendered_artifacts": {
            "status": "disabled",
            "mode": "disable-live-governance",
            "root_status": "redacted",
            "fallback": "graph_only_query_mode",
            "deletion_proof": {
                "targets_checked": [LIVE_GOVERNANCE_TARGET, LIVE_CACHE_TARGET],
                "deleted": deleted,
                "deletion_scope": "stage_root_generated_live_governance_and_cache_only",
            },
            "files": [
                {
                    "target_path": relative,
                    "action": "delete_if_present",
                    "write_policy": "stage_generated_file_only",
                    "staged_path": relative,
                }
                for relative in [LIVE_GOVERNANCE_TARGET, LIVE_CACHE_TARGET]
            ],
            "rollback": {"disable_path": f"delete {LIVE_GOVERNANCE_TARGET}"},
        }
    }


def _validate_data_classification(value: Any) -> list[str]:
    errors: list[str] = []
    data = value if isinstance(value, dict) else {}
    blocked = {str(item) for item in data.get("blocked_fields", []) if isinstance(item, str)}
    for required in sorted(_BLOCKED_INPUTS):
        if required not in blocked:
            errors.append(f"live_governance_approval:data_classification:{required}")
    if not data.get("allowed_fields"):
        errors.append("live_governance_approval:data_classification:allowed_fields")
    return errors


def _validate_redaction_boundary(value: Any) -> list[str]:
    redaction = value if isinstance(value, dict) else {}
    errors = []
    for key in [
        "raw_source_excluded",
        "absolute_paths_redacted",
        "secrets_redacted",
        "provider_payload_validation_required",
    ]:
        if redaction.get(key) is not True:
            errors.append(f"live_governance_approval:redaction_boundary:{key}")
    return errors


def _validate_provider_policy(value: Any) -> list[str]:
    policy = value if isinstance(value, dict) else {}
    errors: list[str] = []
    if policy.get("external_provider_calls_allowed") is not False:
        errors.append("live_governance_approval:provider_policy:external_calls")
    if policy.get("requires_batch_specific_approval") is not True:
        errors.append("live_governance_approval:provider_policy:batch_specific_approval")
    if not isinstance(policy.get("approved_providers"), list):
        errors.append("live_governance_approval:provider_policy:approved_providers")
    return errors


def _validate_credential_policy(value: Any) -> list[str]:
    policy = value if isinstance(value, dict) else {}
    errors: list[str] = []
    if policy.get("storage") != "environment_only":
        errors.append("live_governance_approval:credential_policy:storage")
    if policy.get("secret_material_stored") is not False:
        errors.append("live_governance_approval:credential_policy:secret_material")
    providers = policy.get("providers") if isinstance(policy.get("providers"), list) else []
    if not providers:
        errors.append("live_governance_approval:credential_policy:providers")
    for index, provider in enumerate(providers):
        if not isinstance(provider, dict):
            errors.append(f"live_governance_approval:credential_policy:providers[{index}]")
            continue
        if provider.get("credential_source") != "environment":
            errors.append(f"live_governance_approval:credential_policy:providers[{index}]:source")
        env_var = str(provider.get("env_var") or "")
        if not re.fullmatch(r"[A-Z][A-Z0-9_]{3,}", env_var):
            errors.append(f"live_governance_approval:credential_policy:providers[{index}]:env_var")
        if any(key in provider for key in ["credential_value", "api_key", "token", "secret"]):
            errors.append("credential_policy:stored_secret")
    return errors


def _validate_cache_policy(value: Any) -> list[str]:
    cache = value if isinstance(value, dict) else {}
    errors: list[str] = []
    if safe_relative_path_text(cache.get("storage_path") or "") != LIVE_CACHE_TARGET:
        errors.append("live_governance_approval:cache_policy:storage_path")
    if _positive_int(cache.get("ttl_days"), 0) <= 0:
        errors.append("live_governance_approval:cache_policy:ttl_days")
    if cache.get("fingerprint_scope") != "redacted_graph_and_live_governance_policy":
        errors.append("live_governance_approval:cache_policy:fingerprint_scope")
    if cache.get("stale_policy") != "block_if_graph_or_policy_fingerprint_mismatch":
        errors.append("live_governance_approval:cache_policy:stale_policy")
    if cache.get("deletion_proof_required") is not True:
        errors.append("live_governance_approval:cache_policy:deletion_proof")
    return errors


def _validate_budget_policy(value: Any) -> list[str]:
    budget = value if isinstance(value, dict) else {}
    errors: list[str] = []
    for key in ["max_run_tokens", "max_query_tokens", "max_latency_ms"]:
        if _positive_int(budget.get(key), 0) <= 0:
            errors.append(f"live_governance_approval:budget_policy:{key}")
    if _positive_int(budget.get("max_mutation_tokens"), -1) != 0:
        errors.append("live_governance_approval:budget_policy:max_mutation_tokens")
    if _positive_int(budget.get("max_cost_units"), -1) != 0:
        errors.append("live_governance_approval:budget_policy:max_cost_units")
    if budget.get("on_exceed") != "blocked_or_degraded_graph_only":
        errors.append("live_governance_approval:budget_policy:on_exceed")
    return errors


def _data_classification_packet(value: Any) -> dict[str, Any]:
    data = value if isinstance(value, dict) else {}
    return {
        "allowed_fields": _sorted_sanitized_list(data.get("allowed_fields")),
        "redacted_fields": _sorted_sanitized_list(data.get("redacted_fields")),
        "blocked_fields": _sorted_sanitized_list(data.get("blocked_fields")),
        "raw_source_bodies": "blocked",
        "absolute_local_paths": "blocked",
        "secrets": "blocked",
    }


def _redaction_guard_packet(value: Any) -> dict[str, Any]:
    redaction = value if isinstance(value, dict) else {}
    return {
        "raw_source_excluded": redaction.get("raw_source_excluded") is True,
        "absolute_paths_redacted": redaction.get("absolute_paths_redacted") is True,
        "secrets_redacted": redaction.get("secrets_redacted") is True,
        "provider_payload_validation_required": redaction.get("provider_payload_validation_required") is True,
        "provider_call_without_sanitizer": "blocked",
    }


def _provider_policy_packet(value: Any) -> dict[str, Any]:
    policy = value if isinstance(value, dict) else {}
    return {
        "external_provider_calls_allowed": False,
        "approved_providers": _sorted_sanitized_list(policy.get("approved_providers")),
        "requires_batch_specific_approval": policy.get("requires_batch_specific_approval") is True,
        "live_call_status": "blocked_until_later_task26_batch",
    }


def _credential_policy_packet(value: Any) -> dict[str, Any]:
    policy = value if isinstance(value, dict) else {}
    providers = []
    for provider in policy.get("providers", []) if isinstance(policy.get("providers"), list) else []:
        if not isinstance(provider, dict):
            continue
        providers.append(
            {
                "provider": sanitize_graph_text(provider.get("provider") or ""),
                "credential_source": "environment",
                "env_var": sanitize_graph_text(provider.get("env_var") or ""),
                "credential_value": "[REDACTED_SECRET]" if "credential_value" in provider else None,
            }
        )
    return {
        "storage": "environment_only",
        "secret_material_stored": False,
        "audit_safe_errors": True,
        "providers": providers,
    }


def _cache_policy_packet(approval: dict[str, Any]) -> dict[str, Any]:
    cache = approval.get("cache_policy") if isinstance(approval.get("cache_policy"), dict) else approval
    return {
        "storage_path": safe_relative_path_text(cache.get("storage_path") or LIVE_CACHE_TARGET),
        "ttl_days": _positive_int(cache.get("ttl_days"), 0),
        "fingerprint_scope": sanitize_graph_text(cache.get("fingerprint_scope") or ""),
        "policy_fingerprint": _fingerprint(
            {
                "data_classification": approval.get("data_classification"),
                "redaction_boundary": approval.get("redaction_boundary"),
                "provider_policy": approval.get("provider_policy"),
                "budget_policy": approval.get("budget_policy"),
            }
        ),
        "stale_policy": sanitize_graph_text(cache.get("stale_policy") or ""),
        "deletion_proof_required": cache.get("deletion_proof_required") is True,
        "delete_generated_cache_path": f"delete {LIVE_CACHE_TARGET}",
        "cache_can_be_deleted_without_graph_loss": True,
    }


def _budget_policy_packet(value: Any) -> dict[str, Any]:
    budget = value if isinstance(value, dict) else {}
    return {
        "max_run_tokens": _positive_int(budget.get("max_run_tokens"), 0),
        "max_query_tokens": _positive_int(budget.get("max_query_tokens"), 0),
        "max_mutation_tokens": _positive_int(budget.get("max_mutation_tokens"), 0),
        "max_cost_units": _positive_int(budget.get("max_cost_units"), 0),
        "max_latency_ms": _positive_int(budget.get("max_latency_ms"), 0),
        "on_exceed": sanitize_graph_text(budget.get("on_exceed") or ""),
    }


def _blocked_payload_errors(payload: Any) -> list[str]:
    errors: list[str] = []

    def visit(value: Any, key: str = "") -> None:
        lowered_key = key.lower()
        if lowered_key in {"raw_source", "raw_source_body", "source_body", "raw_body"}:
            errors.append("blocked_input:raw_source_bodies")
        if any(term in lowered_key for term in _SECRET_KEY_TERMS):
            errors.append("blocked_input:secrets")
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                visit(child_value, str(child_key))
        elif isinstance(value, list):
            for child in value:
                visit(child, key)
        else:
            text = str(value or "")
            if _SECRET_VALUE_PATTERN.search(text):
                errors.append("blocked_input:secrets")
            if _WINDOWS_PATH_PATTERN.search(text) or _POSIX_PATH_PATTERN.search(text):
                errors.append("blocked_input:absolute_local_paths")

    visit(payload)
    return errors


def _sanitize_payload(payload: Any) -> Any:
    if isinstance(payload, dict):
        result: dict[str, Any] = {}
        for key, value in payload.items():
            lowered = str(key).lower()
            if lowered in {"raw_source", "raw_source_body", "source_body", "raw_body"}:
                result[key] = "[REDACTED_RAW_SOURCE]"
            elif any(term in lowered for term in _SECRET_KEY_TERMS):
                result[key] = "[REDACTED_SECRET]"
            else:
                result[key] = _sanitize_payload(value)
        return result
    if isinstance(payload, list):
        return [_sanitize_payload(item) for item in payload]
    text = sanitize_graph_text(payload)
    text = _SECRET_VALUE_PATTERN.sub("[REDACTED_SECRET]", text)
    return text


def _validate_stage_boundary(stage_path: Path, workspace_path: Path) -> None:
    if stage_path == workspace_path or stage_path.is_relative_to(workspace_path):
        raise ValueError("stage output directory must be outside workspace")
    if stage_path.exists() and not stage_path.is_dir():
        raise ValueError("stage output path is not a directory")


def _has_unsafe_text(value: Any) -> bool:
    rendered = json.dumps(value, sort_keys=True, default=str)
    return bool(
        _SECRET_VALUE_PATTERN.search(rendered)
        or _WINDOWS_PATH_PATTERN.search(rendered)
        or _POSIX_PATH_PATTERN.search(rendered)
    )


def _sorted_sanitized_list(value: Any) -> list[str]:
    return sorted(sanitize_graph_text(item) for item in value if isinstance(item, str)) if isinstance(value, list) else []


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed >= 0 else default


def _fingerprint(payload: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _validation(ok: bool, errors: list[str], check: str) -> dict[str, Any]:
    return {"ok": ok, "checks": [check], "errors": sorted(set(errors))}


def _merge_validation(primary: dict[str, Any], secondary: dict[str, Any]) -> dict[str, Any]:
    return {
        "ok": primary.get("ok") is True and secondary.get("ok") is True,
        "checks": sorted(set(list(primary.get("checks", [])) + list(secondary.get("checks", [])))),
        "errors": sorted(set(list(primary.get("errors", [])) + list(secondary.get("errors", [])))),
    }
