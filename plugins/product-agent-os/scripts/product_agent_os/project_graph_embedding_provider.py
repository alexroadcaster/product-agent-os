"""External embedding provider gate for Product-Agent OS project graphs.

Batch 26 defines an approval-bound external embedding adapter contract and
eval baseline. It does not call external providers or enable provider results
by default.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import redact_payload, validate_redaction
from product_agent_os.project_graph_index import graph_content_fingerprint
from product_agent_os.project_graph_live_governance import validate_live_governance_packet
from product_agent_os.project_graph_queries import load_graph_artifact
from product_agent_os.project_graph_sanitization import safe_relative_path_text, sanitize_graph_text
from product_agent_os.project_graph_semantic import (
    evaluate_semantic_retrieval_quality,
    load_semantic_retrieval_index,
)


EMBEDDING_PROVIDER_TARGET = ".codex/product-agent-os/project-code-graph-embedding-provider.json"
EMBEDDING_PROVIDER_CACHE_TARGET = ".codex/product-agent-os/project-code-graph-embedding-provider-cache.json"
_APPROVAL_FIELDS = {
    "explicit_approval",
    "owner",
    "allowed_surfaces",
    "provider",
    "data_classification",
    "redaction_policy",
    "cache_policy",
    "budget_policy",
    "eval_threshold",
    "failure_handling",
    "rollback_path",
    "residual_risks",
}
_BATCH26_ALLOWED_SURFACES = {"external_embedding_adapter", "embedding_eval_baseline"}
_FORBIDDEN_INPUTS = {"raw_source_bodies", "secrets", "absolute_local_paths"}
_WINDOWS_PATH_PATTERN = re.compile(r"\b[A-Za-z]:[\\/][^\s\"'<>]+")
_POSIX_PATH_PATTERN = re.compile(r"(^|\s)/(Users|home|private|Volumes|mnt|tmp|var)/[^\s\"'<>]+")
_SECRET_FIELD_NAMES = {
    "access_token",
    "api_key",
    "apikey",
    "client_secret",
    "credential",
    "credential_value",
    "key",
    "password",
    "private_key",
    "refresh_token",
    "secret",
    "secret_value",
    "token",
}
_SECRET_VALUE_PATTERN = re.compile(
    r"(?i)\b(?:sk-[a-z0-9_-]{8,}|api[_-]?key\s*=\s*[^\s\"'<>]+|token\s*=\s*[^\s\"'<>]+)"
)


def validate_embedding_provider_approval(
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Validate the explicit Batch 26 provider-gate approval packet."""

    if not isinstance(approval, dict):
        return _validation(False, ["embedding_provider_approval:missing"], "embedding_provider_approval")
    errors: list[str] = []
    missing = sorted(field for field in _APPROVAL_FIELDS if field not in approval)
    errors.extend(f"embedding_provider_approval:{field}:missing" for field in missing)
    if approval.get("explicit_approval") is not True:
        errors.append("embedding_provider_approval:explicit_approval")
    if not sanitize_graph_text(approval.get("owner") or ""):
        errors.append("embedding_provider_approval:owner")

    allowed_surfaces = {str(item) for item in approval.get("allowed_surfaces", []) if isinstance(item, str)}
    for required in sorted(_BATCH26_ALLOWED_SURFACES):
        if required not in allowed_surfaces:
            errors.append(f"embedding_provider_approval:allowed_surfaces:{required}:missing")
    for surface in sorted(allowed_surfaces - _BATCH26_ALLOWED_SURFACES):
        errors.append(f"embedding_provider_approval:allowed_surfaces:{surface}")

    errors.extend(_validate_governance_prerequisite(governance_packet))
    errors.extend(_validate_provider_policy(approval.get("provider")))
    errors.extend(_validate_data_classification(approval.get("data_classification")))
    errors.extend(_validate_redaction_policy(approval.get("redaction_policy")))
    errors.extend(_validate_cache_policy(approval.get("cache_policy")))
    errors.extend(_validate_budget_policy(approval.get("budget_policy")))
    errors.extend(_validate_eval_threshold(approval.get("eval_threshold")))
    errors.extend(_validate_failure_handling(approval.get("failure_handling")))
    if approval.get("rollback_path") != f"delete {EMBEDDING_PROVIDER_TARGET}":
        errors.append("embedding_provider_approval:rollback_path")
    if not isinstance(approval.get("residual_risks"), list):
        errors.append("embedding_provider_approval:residual_risks")
    if _has_unsafe_text(approval):
        errors.append("embedding_provider_approval:unsafe_text")
    return _validation(not errors, errors, "embedding_provider_approval")


def build_embedding_provider_gate(
    graph: dict[str, Any],
    *,
    semantic_index: dict[str, Any] | None,
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a source-free external embedding provider gate packet."""

    validation = validate_embedding_provider_approval(approval, governance_packet)
    if validation["ok"] is not True:
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_external_embedding_provider_gate",
            "status": "approval_required",
            "write_policy": "read_only",
            "approval_boundary": "batch26_external_embedding_provider_gate_and_eval",
            "provider_enabled": False,
            "fallback": "semantic_retrieval_or_graph_only",
            "validation": validation,
            "safe_next_action": "Provide Batch 26 approval, Batch 24 governance and Batch 21 semantic index evidence.",
        }
    approval = approval if isinstance(approval, dict) else {}
    semantic_index = semantic_index if isinstance(semantic_index, dict) else {}
    provider = approval.get("provider") if isinstance(approval.get("provider"), dict) else {}
    gate = {
        "schema_version": 1,
        "artifact_kind": "project_graph_external_embedding_provider_gate",
        "status": "ready",
        "write_policy": "read_only",
        "approval_boundary": "batch26_external_embedding_provider_gate_and_eval",
        "source_boundary": "redacted_graph_and_semantic_index_only_no_raw_source",
        "generated_view_policy": "embedding_provider_gate_is_generated_evidence_not_source_of_truth",
        "owner": sanitize_graph_text(approval.get("owner") or ""),
        "allowed_surfaces": sorted(_BATCH26_ALLOWED_SURFACES),
        "blocked_surfaces": [
            "external_provider_call_without_runtime_invocation_approval",
            "secret_storage",
            "raw_source_payload",
            "canonical_graph_mutation",
            "production_server",
            "git_action",
        ],
        "governance": {
            "artifact_kind": "project_graph_live_governance",
            "status": "ready",
            "approval_boundary": "batch24_live_governance_only_no_live_calls",
        },
        "provider_policy": {
            "provider": sanitize_graph_text(provider.get("provider") or ""),
            "model": sanitize_graph_text(provider.get("model") or ""),
            "credential_source": sanitize_graph_text(provider.get("credential_source") or ""),
            "credential_env_var": sanitize_graph_text(provider.get("credential_env_var") or ""),
            "secret_material_stored": False,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "batching": _batching_packet(provider.get("batching")),
        },
        "data_classification": _classification_packet(approval.get("data_classification")),
        "redaction_policy": _redaction_policy_packet(approval.get("redaction_policy")),
        "cache_policy": _cache_policy_packet(approval.get("cache_policy")),
        "budget_policy": _budget_policy_packet(approval.get("budget_policy")),
        "eval_policy": _eval_policy_packet(approval.get("eval_threshold")),
        "failure_handling": _failure_handling_packet(approval.get("failure_handling")),
        "graph_fingerprint": graph_content_fingerprint(_redacted_dict(graph)),
        "semantic_index_fingerprint": _semantic_fingerprint(semantic_index),
        "provider_payload_contract": _provider_payload_contract(semantic_index, provider.get("batching")),
        "provider_enabled_by_default": False,
        "provider_enabled": False,
        "fallback": "semantic_retrieval_or_graph_only",
        "rollback": {
            "disable_path": f"delete {EMBEDDING_PROVIDER_TARGET}",
            "delete_cache_path": f"delete {EMBEDDING_PROVIDER_CACHE_TARGET}",
            "fallback": "semantic_retrieval_or_graph_only",
            "deletion_scope": "stage_root_generated_embedding_provider_gate_and_cache_only",
        },
        "residual_risks": [
            sanitize_graph_text(item)
            for item in approval.get("residual_risks", [])
            if isinstance(item, str)
        ][:10],
        "safe_next_action": (
            "Run the Batch 26 eval baseline with approved provider result evidence; keep provider disabled if it "
            "does not beat thresholds."
        ),
    }
    safe_gate, report = redact_payload(gate)
    if isinstance(safe_gate, dict):
        safe_gate["redaction_summary"] = report
        safe_gate["validation"] = _merge_validation(validation, validate_embedding_provider_gate(safe_gate))
        if safe_gate["validation"]["ok"] is not True:
            safe_gate["status"] = "blocked"
        return safe_gate
    gate["validation"] = validate_embedding_provider_gate(gate)
    return gate


def validate_embedding_provider_gate(gate: dict[str, Any]) -> dict[str, Any]:
    """Validate Batch 26 provider gate schema and safety invariants."""

    errors: list[str] = []
    if gate.get("schema_version") != 1:
        errors.append("schema_version")
    if gate.get("artifact_kind") != "project_graph_external_embedding_provider_gate":
        errors.append("artifact_kind")
    if gate.get("write_policy") != "read_only":
        errors.append("write_policy")
    if gate.get("approval_boundary") != "batch26_external_embedding_provider_gate_and_eval":
        errors.append("approval_boundary")
    if gate.get("source_boundary") != "redacted_graph_and_semantic_index_only_no_raw_source":
        errors.append("source_boundary")
    provider = gate.get("provider_policy") if isinstance(gate.get("provider_policy"), dict) else {}
    if provider.get("provider") != "external_embedding":
        errors.append("provider_policy:provider")
    if provider.get("credential_source") != "environment":
        errors.append("provider_policy:credential_source")
    if provider.get("secret_material_stored") is not False:
        errors.append("provider_policy:secret_material")
    if provider.get("provider_call_allowed") is not False:
        errors.append("provider_policy:provider_call_allowed")
    if provider.get("external_call_performed") is not False:
        errors.append("provider_policy:external_call_performed")
    redaction = gate.get("redaction_policy") if isinstance(gate.get("redaction_policy"), dict) else {}
    for field in ["raw_source_excluded", "secrets_redacted", "absolute_paths_redacted", "provider_payload_validation_required"]:
        if redaction.get(field) is not True:
            errors.append(f"redaction_policy:{field}")
    cache = gate.get("cache_policy") if isinstance(gate.get("cache_policy"), dict) else {}
    if cache.get("storage_path") != EMBEDDING_PROVIDER_TARGET:
        errors.append("cache_policy:storage_path")
    if cache.get("cache_target") != EMBEDDING_PROVIDER_CACHE_TARGET:
        errors.append("cache_policy:cache_target")
    if cache.get("deletion_proof_required") is not True:
        errors.append("cache_policy:deletion_proof")
    budget = gate.get("budget_policy") if isinstance(gate.get("budget_policy"), dict) else {}
    if _positive_int(budget.get("max_cost_units"), -1) != 0:
        errors.append("budget_policy:max_cost_units")
    if gate.get("provider_enabled_by_default") is not False:
        errors.append("provider_enabled_by_default")
    if gate.get("fallback") != "semantic_retrieval_or_graph_only":
        errors.append("fallback")
    if "canonical_graph_mutation" not in gate.get("blocked_surfaces", []):
        errors.append("blocked_surfaces:canonical_graph_mutation")
    if _has_unsafe_text(gate):
        errors.append("source_boundary:unsafe_text")
    rendered = json.dumps(gate, sort_keys=True, default=str)
    errors.extend(f"redaction:{error}" for error in validate_redaction(rendered))
    return _validation(not errors, errors, "embedding_provider_gate")


def evaluate_embedding_provider_baseline(
    gate: dict[str, Any],
    *,
    semantic_index: dict[str, Any],
    graph: dict[str, Any],
    cases: list[dict[str, Any]],
    provider_results: dict[str, dict[str, Any]] | None,
) -> dict[str, Any]:
    """Compare approved provider result evidence against the local semantic baseline."""

    gate_validation = validate_embedding_provider_gate(gate)
    thresholds = gate.get("eval_policy", {}) if isinstance(gate.get("eval_policy"), dict) else {}
    baseline = evaluate_semantic_retrieval_quality(
        semantic_index,
        graph=graph,
        cases=cases,
        thresholds={
            "min_recall_at_k": float(thresholds.get("min_recall_at_k", 0.0)),
            "min_mrr": float(thresholds.get("min_mrr", 0.0)),
            "max_false_positive_rate": float(thresholds.get("max_false_positive_rate", 1.0)),
            "max_query_ms": _positive_int(thresholds.get("max_query_ms"), 250),
            "max_payload_tokens": _positive_int(thresholds.get("max_payload_tokens"), 1200),
        },
    )
    provider_metrics = _provider_quality_metrics(cases, provider_results or {})
    failed = [] if gate_validation.get("ok") is True else ["embedding_provider_gate:invalid"]
    if not provider_results:
        failed.append("provider_eval:missing")
    failed.extend(_provider_failed_thresholds(provider_metrics, baseline.get("quality_metrics", {}), thresholds))
    decision = "passed" if not failed else "disabled_fallback"
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "decision_status": decision,
        "provider_enabled": False,
        "provider_enabled_by_default": False,
        "external_call_performed": False,
        "approval_boundary": gate.get("approval_boundary"),
        "source_boundary": gate.get("source_boundary"),
        "search_backend": "external_embedding_provider_eval",
        "baseline_backend": "semantic_retrieval",
        "baseline_quality_metrics": baseline.get("quality_metrics", {}),
        "provider_quality_metrics": provider_metrics,
        "thresholds": thresholds,
        "failed_thresholds": failed,
        "fallback": "semantic_retrieval_or_graph_only",
        "rollback": gate.get("rollback", {}),
        "safe_next_action": (
            "Keep provider disabled unless approved provider evidence beats thresholds; semantic retrieval or graph "
            "query remains the fallback."
        ),
    }
    return _redacted_dict(packet)


def stage_embedding_provider_gate(
    graph_artifact: str | Path,
    semantic_index_artifact: str | Path,
    stage_root: str | Path,
    *,
    workspace: str | Path,
    approval: dict[str, Any] | None,
    governance_artifact: str | Path | None,
) -> dict[str, Any]:
    """Stage the Batch 26 provider gate under an explicit stage root."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    graph = load_graph_artifact(graph_artifact)
    semantic_index = load_semantic_retrieval_index(semantic_index_artifact)
    governance = _load_json_file(governance_artifact) if governance_artifact else None
    gate = build_embedding_provider_gate(
        graph,
        semantic_index=semantic_index,
        approval=approval,
        governance_packet=governance,
    )
    target = stage_path / EMBEDDING_PROVIDER_TARGET
    action = "blocked"
    if gate.get("status") == "ready" and gate.get("validation", {}).get("ok") is True:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(gate, indent=2, sort_keys=True), encoding="utf-8")
        action = "create"
    return {
        "rendered_artifacts": {
            "status": gate.get("status"),
            "mode": "validate-embedding-provider",
            "root_status": "redacted",
            "source_boundary": gate.get("source_boundary", "redacted_graph_and_semantic_index_only_no_raw_source"),
            "provider_call_allowed": False,
            "provider_enabled_by_default": False,
            "fallback": "semantic_retrieval_or_graph_only",
            "files": [
                {
                    "target_path": EMBEDDING_PROVIDER_TARGET,
                    "action": action,
                    "write_policy": "staged_only" if action == "create" else "blocked",
                    "staged_path": EMBEDDING_PROVIDER_TARGET,
                }
            ],
            "rollback": {"disable_path": f"delete {EMBEDDING_PROVIDER_TARGET}"},
            "validation": gate.get("validation"),
        }
    }


def disable_embedding_provider_gate(stage_root: str | Path, *, workspace: str | Path) -> dict[str, Any]:
    """Disable Batch 26 provider artifacts by deleting generated stage-root files."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    targets = [EMBEDDING_PROVIDER_TARGET, EMBEDDING_PROVIDER_CACHE_TARGET]
    deleted: list[str] = []
    for relative in targets:
        target = stage_path / relative
        if target.exists() and target.is_file():
            target.unlink()
            deleted.append(relative)
    return {
        "rendered_artifacts": {
            "status": "disabled",
            "mode": "disable-embedding-provider",
            "root_status": "redacted",
            "fallback": "semantic_retrieval_or_graph_only",
            "deletion_proof": {
                "targets_checked": targets,
                "deleted": deleted,
                "remaining": [relative for relative in targets if (stage_path / relative).exists()],
            },
            "files": [
                {
                    "target_path": relative,
                    "action": "delete_if_present",
                    "write_policy": "stage_generated_file_only",
                    "staged_path": relative,
                }
                for relative in targets
            ],
            "rollback": {"disable_path": f"delete {EMBEDDING_PROVIDER_TARGET}"},
        }
    }


def _validate_governance_prerequisite(governance_packet: dict[str, Any] | None) -> list[str]:
    if not isinstance(governance_packet, dict):
        return ["embedding_provider_approval:governance_packet:missing"]
    errors: list[str] = []
    if governance_packet.get("status") != "ready":
        errors.append("embedding_provider_approval:governance_packet:not_ready")
    validation = validate_live_governance_packet(governance_packet)
    if validation.get("ok") is not True:
        errors.append("embedding_provider_approval:governance_packet:invalid")
    provider_policy = governance_packet.get("provider_policy") if isinstance(governance_packet.get("provider_policy"), dict) else {}
    if provider_policy.get("requires_batch_specific_approval") is not True:
        errors.append("embedding_provider_approval:governance_packet:batch_specific_approval")
    return errors


def _validate_provider_policy(provider: Any) -> list[str]:
    if not isinstance(provider, dict):
        return ["embedding_provider_approval:provider"]
    errors: list[str] = []
    if provider.get("provider") != "external_embedding":
        errors.append("embedding_provider_approval:provider:provider")
    if not sanitize_graph_text(provider.get("model") or ""):
        errors.append("embedding_provider_approval:provider:model")
    if provider.get("credential_source") != "environment":
        errors.append("embedding_provider_approval:provider:credential_source")
    if not sanitize_graph_text(provider.get("credential_env_var") or ""):
        errors.append("embedding_provider_approval:provider:credential_env_var")
    if provider.get("external_calls_allowed") is not False:
        errors.append("embedding_provider_approval:provider:external_calls_allowed")
    if any(key in provider for key in ["credential_value", "api_key", "token"]):
        errors.append("embedding_provider_approval:provider:stored_secret")
    batching = provider.get("batching") if isinstance(provider.get("batching"), dict) else {}
    if _positive_int(batching.get("max_batch_size"), 0) <= 0:
        errors.append("embedding_provider_approval:provider:max_batch_size")
    if _positive_int(batching.get("max_batch_tokens"), 0) <= 0:
        errors.append("embedding_provider_approval:provider:max_batch_tokens")
    return errors


def _validate_data_classification(classification: Any) -> list[str]:
    if not isinstance(classification, dict):
        return ["embedding_provider_approval:data_classification"]
    forbidden = {str(item) for item in classification.get("forbidden_inputs", []) if isinstance(item, str)}
    return [
        f"embedding_provider_approval:data_classification:{required}"
        for required in sorted(_FORBIDDEN_INPUTS - forbidden)
    ]


def _validate_redaction_policy(redaction: Any) -> list[str]:
    if not isinstance(redaction, dict):
        return ["embedding_provider_approval:redaction_policy"]
    errors: list[str] = []
    for field in ["raw_source_excluded", "secrets_redacted", "absolute_paths_redacted", "provider_payload_validation_required"]:
        if redaction.get(field) is not True:
            errors.append(f"embedding_provider_approval:redaction_policy:{field}")
    return errors


def _validate_cache_policy(cache: Any) -> list[str]:
    if not isinstance(cache, dict):
        return ["embedding_provider_approval:cache_policy"]
    errors: list[str] = []
    if safe_relative_path_text(cache.get("storage_path") or "") != EMBEDDING_PROVIDER_TARGET:
        errors.append("embedding_provider_approval:cache_policy:storage_path")
    if safe_relative_path_text(cache.get("cache_target") or "") != EMBEDDING_PROVIDER_CACHE_TARGET:
        errors.append("embedding_provider_approval:cache_policy:cache_target")
    if cache.get("stale_policy") != "block_if_graph_or_semantic_or_policy_fingerprint_mismatch":
        errors.append("embedding_provider_approval:cache_policy:stale_policy")
    if "semantic" not in str(cache.get("fingerprint_scope") or ""):
        errors.append("embedding_provider_approval:cache_policy:fingerprint_scope")
    if cache.get("deletion_proof_required") is not True:
        errors.append("embedding_provider_approval:cache_policy:deletion_proof_required")
    if _positive_int(cache.get("ttl_days"), 0) <= 0:
        errors.append("embedding_provider_approval:cache_policy:ttl_days")
    return errors


def _validate_budget_policy(budget: Any) -> list[str]:
    if not isinstance(budget, dict):
        return ["embedding_provider_approval:budget_policy"]
    errors: list[str] = []
    if _positive_int(budget.get("max_query_tokens"), 0) <= 0:
        errors.append("embedding_provider_approval:budget_policy:max_query_tokens")
    if _positive_int(budget.get("max_batch_tokens"), 0) <= 0:
        errors.append("embedding_provider_approval:budget_policy:max_batch_tokens")
    if _positive_int(budget.get("max_cost_units"), -1) != 0:
        errors.append("embedding_provider_approval:budget_policy:max_cost_units")
    if _positive_int(budget.get("max_latency_ms"), 0) <= 0:
        errors.append("embedding_provider_approval:budget_policy:max_latency_ms")
    if "fallback" not in str(budget.get("on_exceed") or ""):
        errors.append("embedding_provider_approval:budget_policy:on_exceed")
    return errors


def _validate_eval_threshold(thresholds: Any) -> list[str]:
    if not isinstance(thresholds, dict):
        return ["embedding_provider_approval:eval_threshold"]
    required = {
        "min_recall_at_k",
        "min_mrr",
        "min_provider_recall_delta",
        "min_provider_mrr_delta",
        "max_false_positive_rate",
        "max_query_ms",
        "max_payload_tokens",
    }
    errors = [f"embedding_provider_approval:eval_threshold:{field}" for field in sorted(required - set(thresholds))]
    if _positive_int(thresholds.get("max_query_ms"), 0) <= 0:
        errors.append("embedding_provider_approval:eval_threshold:max_query_ms")
    if _positive_int(thresholds.get("max_payload_tokens"), 0) <= 0:
        errors.append("embedding_provider_approval:eval_threshold:max_payload_tokens")
    return errors


def _validate_failure_handling(failure: Any) -> list[str]:
    if not isinstance(failure, dict):
        return ["embedding_provider_approval:failure_handling"]
    errors: list[str] = []
    for field in ["on_missing_provider_eval", "on_failed_eval"]:
        if "fallback" not in str(failure.get(field) or ""):
            errors.append(f"embedding_provider_approval:failure_handling:{field}")
    return errors


def _classification_packet(classification: Any) -> dict[str, Any]:
    classification = classification if isinstance(classification, dict) else {}
    return {
        "allowed_inputs": [
            sanitize_graph_text(item)
            for item in classification.get("allowed_inputs", [])
            if isinstance(item, str)
        ],
        "forbidden_inputs": [
            sanitize_graph_text(item)
            for item in classification.get("forbidden_inputs", [])
            if isinstance(item, str)
        ],
        "raw_source_bodies": "blocked",
        "absolute_local_paths": "blocked",
        "secrets": "blocked",
    }


def _redaction_policy_packet(redaction: Any) -> dict[str, Any]:
    redaction = redaction if isinstance(redaction, dict) else {}
    return {
        "raw_source_excluded": redaction.get("raw_source_excluded") is True,
        "secrets_redacted": redaction.get("secrets_redacted") is True,
        "absolute_paths_redacted": redaction.get("absolute_paths_redacted") is True,
        "provider_payload_validation_required": redaction.get("provider_payload_validation_required") is True,
    }


def _cache_policy_packet(cache: Any) -> dict[str, Any]:
    cache = cache if isinstance(cache, dict) else {}
    return {
        "storage_path": EMBEDDING_PROVIDER_TARGET,
        "cache_target": EMBEDDING_PROVIDER_CACHE_TARGET,
        "fingerprint_scope": "redacted_graph_semantic_index_provider_policy",
        "stale_policy": "block_if_graph_or_semantic_or_policy_fingerprint_mismatch",
        "ttl_days": _positive_int(cache.get("ttl_days"), 7),
        "deletion_proof_required": cache.get("deletion_proof_required") is True,
        "cache_can_be_deleted_without_graph_loss": True,
    }


def _budget_policy_packet(budget: Any) -> dict[str, Any]:
    budget = budget if isinstance(budget, dict) else {}
    return {
        "max_query_tokens": _positive_int(budget.get("max_query_tokens"), 0),
        "max_batch_tokens": _positive_int(budget.get("max_batch_tokens"), 0),
        "max_cost_units": _positive_int(budget.get("max_cost_units"), -1),
        "max_latency_ms": _positive_int(budget.get("max_latency_ms"), 0),
        "on_exceed": sanitize_graph_text(budget.get("on_exceed") or ""),
    }


def _eval_policy_packet(thresholds: Any) -> dict[str, Any]:
    thresholds = thresholds if isinstance(thresholds, dict) else {}
    return {
        "embedding_eval_baseline": True,
        "min_recall_at_k": _float_value(thresholds.get("min_recall_at_k"), 0.0),
        "min_mrr": _float_value(thresholds.get("min_mrr"), 0.0),
        "min_provider_recall_delta": _float_value(thresholds.get("min_provider_recall_delta"), 0.0),
        "min_provider_mrr_delta": _float_value(thresholds.get("min_provider_mrr_delta"), 0.0),
        "max_false_positive_rate": _float_value(thresholds.get("max_false_positive_rate"), 1.0),
        "max_query_ms": _positive_int(thresholds.get("max_query_ms"), 250),
        "max_payload_tokens": _positive_int(thresholds.get("max_payload_tokens"), 1200),
    }


def _failure_handling_packet(failure: Any) -> dict[str, Any]:
    failure = failure if isinstance(failure, dict) else {}
    return {
        "on_missing_provider_eval": sanitize_graph_text(
            failure.get("on_missing_provider_eval") or "disabled_fallback_to_semantic_or_graph"
        ),
        "on_failed_eval": sanitize_graph_text(
            failure.get("on_failed_eval") or "disabled_fallback_to_semantic_or_graph"
        ),
    }


def _batching_packet(batching: Any) -> dict[str, int]:
    batching = batching if isinstance(batching, dict) else {}
    return {
        "max_batch_size": _positive_int(batching.get("max_batch_size"), 0),
        "max_batch_tokens": _positive_int(batching.get("max_batch_tokens"), 0),
    }


def _provider_payload_contract(semantic_index: dict[str, Any], batching: Any) -> dict[str, Any]:
    records = semantic_index.get("corpus_records", []) if isinstance(semantic_index, dict) else []
    max_batch = _positive_int((batching or {}).get("max_batch_size") if isinstance(batching, dict) else None, 16)
    preview = []
    for record in records[:max_batch]:
        if not isinstance(record, dict):
            continue
        text = sanitize_graph_text(record.get("approved_text") or "")
        preview.append(
            {
                "record_id": sanitize_graph_text(record.get("record_id") or ""),
                "node_id": sanitize_graph_text(record.get("node_id") or ""),
                "approved_text_hash": "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "term_count": len(record.get("terms", [])) if isinstance(record.get("terms"), list) else 0,
                "observation_id_count": len(record.get("observation_ids", []))
                if isinstance(record.get("observation_ids"), list)
                else 0,
            }
        )
    return {
        "payload_kind": "embedding_request_contract",
        "approved_fields": ["record_id", "node_id", "approved_text_hash", "terms", "observation_id_count"],
        "raw_source_bodies_included": False,
        "absolute_local_paths_included": False,
        "secrets_included": False,
        "external_call_performed": False,
        "records_preview": preview,
        "omitted_record_count": max(0, len(records) - len(preview)),
    }


def _provider_quality_metrics(cases: list[dict[str, Any]], provider_results: dict[str, dict[str, Any]]) -> dict[str, float]:
    evaluated = []
    query_ms: list[float] = []
    payload_tokens: list[int] = []
    for case in cases:
        if not isinstance(case, dict):
            continue
        case_id = str(case.get("id") or "")
        result = provider_results.get(case_id, {}) if isinstance(provider_results, dict) else {}
        result_ids = [str(item) for item in result.get("result_node_ids", []) if item]
        expected_ids = [str(item) for item in case.get("expected_node_ids", []) if item]
        unexpected_ids = [str(item) for item in case.get("unexpected_node_ids", []) if item]
        top_k = _positive_int(case.get("top_k"), 5)
        hits = [item for item in expected_ids if item in result_ids[:top_k]]
        false_hits = [item for item in unexpected_ids if item in result_ids[:top_k]]
        first_rank = _first_rank(result_ids, expected_ids)
        query_ms.append(_float_value(result.get("query_ms"), 0.0))
        payload_tokens.append(_positive_int(result.get("payload_tokens"), 0))
        evaluated.append(
            {
                "expected_count": len(expected_ids),
                "hit_count": len(hits),
                "false_positive_count": len(false_hits),
                "top_k": top_k,
                "reciprocal_rank": 0.0 if first_rank == 0 else 1.0 / first_rank,
            }
        )
    total_expected = sum(item["expected_count"] for item in evaluated)
    total_hits = sum(item["hit_count"] for item in evaluated)
    total_returned = sum(item["top_k"] for item in evaluated)
    false_hits = sum(item["false_positive_count"] for item in evaluated)
    return {
        "recall_at_k": 1.0 if total_expected == 0 else round(total_hits / total_expected, 4),
        "mrr": _average(item["reciprocal_rank"] for item in evaluated),
        "false_positive_rate": 0.0 if total_returned == 0 else round(false_hits / total_returned, 4),
        "max_query_ms": round(max(query_ms or [0.0]), 3),
        "max_payload_tokens": max(payload_tokens or [0]),
    }


def _provider_failed_thresholds(
    provider_metrics: dict[str, float],
    baseline_metrics: dict[str, Any],
    thresholds: dict[str, Any],
) -> list[str]:
    failures: list[str] = []
    if _float_value(provider_metrics.get("recall_at_k"), 0.0) < _float_value(thresholds.get("min_recall_at_k"), 0.0):
        failures.append("provider_recall_at_k_below_threshold")
    if _float_value(provider_metrics.get("mrr"), 0.0) < _float_value(thresholds.get("min_mrr"), 0.0):
        failures.append("provider_mrr_below_threshold")
    recall_delta = _float_value(provider_metrics.get("recall_at_k"), 0.0) - _float_value(
        baseline_metrics.get("recall_at_k"),
        0.0,
    )
    if recall_delta < _float_value(thresholds.get("min_provider_recall_delta"), 0.0):
        failures.append("provider_recall_delta_below_threshold")
    mrr_delta = _float_value(provider_metrics.get("mrr"), 0.0) - _float_value(baseline_metrics.get("mrr"), 0.0)
    if mrr_delta < _float_value(thresholds.get("min_provider_mrr_delta"), 0.0):
        failures.append("provider_mrr_delta_below_threshold")
    if _float_value(provider_metrics.get("false_positive_rate"), 0.0) > _float_value(
        thresholds.get("max_false_positive_rate"),
        1.0,
    ):
        failures.append("provider_false_positive_rate_above_threshold")
    if _float_value(provider_metrics.get("max_query_ms"), 0.0) > _float_value(thresholds.get("max_query_ms"), 250.0):
        failures.append("provider_max_query_ms_above_threshold")
    if _float_value(provider_metrics.get("max_payload_tokens"), 0.0) > _float_value(
        thresholds.get("max_payload_tokens"),
        1200.0,
    ):
        failures.append("provider_max_payload_tokens_above_threshold")
    return failures


def _first_rank(result_ids: list[str], expected_ids: list[str]) -> int:
    for index, node_id in enumerate(result_ids, start=1):
        if node_id in expected_ids:
            return index
    return 0


def _semantic_fingerprint(semantic_index: dict[str, Any]) -> str:
    if semantic_index.get("graph_fingerprint"):
        payload = {
            "graph_fingerprint": semantic_index.get("graph_fingerprint"),
            "record_count": len(semantic_index.get("corpus_records", [])),
            "approval_boundary": semantic_index.get("approval_boundary"),
        }
        return "sha256:" + hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return "sha256:" + hashlib.sha256(json.dumps(_redacted_dict(semantic_index), sort_keys=True).encode("utf-8")).hexdigest()


def _redacted_dict(payload: dict[str, Any]) -> dict[str, Any]:
    safe, _report = redact_payload(payload)
    return safe if isinstance(safe, dict) else {}


def _load_json_file(path: str | Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def _validate_stage_boundary(stage_path: Path, workspace_path: Path) -> None:
    if stage_path == workspace_path or stage_path.is_relative_to(workspace_path):
        raise ValueError("stage output directory must be outside workspace")
    if stage_path.exists() and not stage_path.is_dir():
        raise ValueError("stage output path is not a directory")


def _has_unsafe_text(value: Any) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key).lower()
            if key_text in _SECRET_FIELD_NAMES and nested not in (None, "", False):
                if key_text in {"credential_env_var", "credential_source"}:
                    continue
                return True
            if _has_unsafe_text(nested):
                return True
        return False
    if isinstance(value, list):
        return any(_has_unsafe_text(item) for item in value)
    if isinstance(value, str):
        return bool(
            _SECRET_VALUE_PATTERN.search(value)
            or _WINDOWS_PATH_PATTERN.search(value)
            or _POSIX_PATH_PATTERN.search(value)
        )
    return False


def _merge_validation(*validations: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    for validation in validations:
        errors.extend(str(error) for error in validation.get("errors", []))
    return _validation(not errors, sorted(set(errors)), "embedding_provider_gate")


def _validation(ok: bool, errors: list[str], scope: str) -> dict[str, Any]:
    return {"ok": ok, "scope": scope, "errors": errors}


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed >= 0 else default


def _float_value(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _average(values: Any) -> float:
    items = list(values)
    if not items:
        return 0.0
    return round(sum(float(item) for item in items) / len(items), 4)
