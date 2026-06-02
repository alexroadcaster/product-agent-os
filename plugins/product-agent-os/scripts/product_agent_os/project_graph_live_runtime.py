"""Local read-only runtime contract for Product-Agent OS project graphs.

Batch 25 defines a disabled-by-default local runtime contract, lifecycle
controls, local auth policy and graph-only fallback. It does not start a
network server, call providers or mutate canonical graph facts.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import redact_payload, validate_redaction
from product_agent_os.project_graph_index import graph_content_fingerprint
from product_agent_os.project_graph_live_governance import validate_live_governance_packet
from product_agent_os.project_graph_queries import load_graph_artifact, query_project_graph
from product_agent_os.project_graph_sanitization import safe_relative_path_text, sanitize_graph_text


LIVE_RUNTIME_TARGET = ".codex/product-agent-os/project-code-graph-live-runtime.json"
LIVE_RUNTIME_PID_TARGET = ".codex/product-agent-os/project-code-graph-live-runtime.pid"
LIVE_RUNTIME_LOG_TARGET = ".codex/product-agent-os/project-code-graph-live-runtime.log"
_APPROVAL_FIELDS = {
    "explicit_approval",
    "owner",
    "allowed_surfaces",
    "server_contract",
    "lifecycle_controls",
    "auth_policy",
    "fallback_policy",
    "rollback_path",
    "residual_risks",
}
_BATCH25_ALLOWED_SURFACES = {
    "local_read_only_runtime",
    "server_lifecycle",
    "local_auth_policy",
    "graph_only_fallback",
}
_LOCAL_HOSTS = {"127.0.0.1", "localhost"}
_WINDOWS_PATH_PATTERN = re.compile(r"\b[A-Za-z]:[\\/][^\s\"'<>]+")
_POSIX_PATH_PATTERN = re.compile(r"(^|\s)/(Users|home|private|Volumes|mnt|tmp|var)/[^\s\"'<>]+")


def validate_live_runtime_contract_approval(
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Validate the explicit Batch 25 runtime approval and Batch 24 prerequisite."""

    errors: list[str] = []
    if not isinstance(approval, dict):
        return _validation(False, ["live_runtime_approval:missing"], "live_runtime_approval")
    missing = sorted(field for field in _APPROVAL_FIELDS if field not in approval)
    errors.extend(f"live_runtime_approval:{field}:missing" for field in missing)
    if approval.get("explicit_approval") is not True:
        errors.append("live_runtime_approval:explicit_approval")
    if not sanitize_graph_text(approval.get("owner") or ""):
        errors.append("live_runtime_approval:owner")

    allowed_surfaces = {str(item) for item in approval.get("allowed_surfaces", []) if isinstance(item, str)}
    for required in sorted(_BATCH25_ALLOWED_SURFACES):
        if required not in allowed_surfaces:
            errors.append(f"live_runtime_approval:allowed_surfaces:{required}:missing")
    for surface in sorted(allowed_surfaces - _BATCH25_ALLOWED_SURFACES):
        errors.append(f"live_runtime_approval:allowed_surfaces:{surface}")

    errors.extend(_validate_governance_prerequisite(governance_packet))
    errors.extend(_validate_server_contract(approval.get("server_contract")))
    errors.extend(_validate_lifecycle_controls(approval.get("lifecycle_controls")))
    errors.extend(_validate_auth_policy(approval.get("auth_policy")))
    errors.extend(_validate_fallback_policy(approval.get("fallback_policy")))
    if approval.get("rollback_path") != f"delete {LIVE_RUNTIME_TARGET}":
        errors.append("live_runtime_approval:rollback_path")
    if not isinstance(approval.get("residual_risks"), list):
        errors.append("live_runtime_approval:residual_risks")
    if _has_unsafe_text(approval):
        errors.append("live_runtime_approval:unsafe_text")
    return _validation(not errors, errors, "live_runtime_approval")


def build_live_runtime_contract(
    graph: dict[str, Any],
    *,
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a source-free local read-only runtime contract for Batch 25."""

    validation = validate_live_runtime_contract_approval(approval, governance_packet)
    if validation["ok"] is not True:
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_live_runtime_contract",
            "status": "approval_required",
            "runtime_status": "blocked",
            "write_policy": "read_only",
            "validation": validation,
            "safe_next_action": "Provide Batch 25 approval and a ready Batch 24 governance packet.",
        }
    approval = approval if isinstance(approval, dict) else {}
    metadata = graph.get("metadata", {}) if isinstance(graph.get("metadata"), dict) else {}
    contract = {
        "schema_version": 1,
        "artifact_kind": "project_graph_live_runtime_contract",
        "status": "ready",
        "runtime_status": "disabled_by_default_not_started",
        "write_policy": "read_only",
        "approval_boundary": "batch25_local_read_only_runtime_auth_fallback",
        "source_boundary": "graph_artifact_only_no_raw_source_or_secret_material",
        "generated_view_policy": "live_runtime_contract_is_generated_evidence_not_source_of_truth",
        "owner": sanitize_graph_text(approval.get("owner") or ""),
        "allowed_surfaces": sorted(_BATCH25_ALLOWED_SURFACES),
        "blocked_surfaces": [
            "write_endpoint",
            "canonical_graph_mutation",
            "external_provider_call",
            "public_network_bind",
            "production_server",
            "git_action",
        ],
        "governance": {
            "artifact_kind": "project_graph_live_governance",
            "status": "ready",
            "approval_boundary": "batch24_live_governance_only_no_live_calls",
        },
        "server_contract": _server_contract_packet(approval.get("server_contract")),
        "server_lifecycle": _lifecycle_packet(approval.get("lifecycle_controls")),
        "auth_policy": _auth_policy_packet(approval.get("auth_policy")),
        "fallback_policy": _fallback_policy_packet(approval.get("fallback_policy")),
        "graph_fingerprint": graph_content_fingerprint(graph),
        "metadata": {
            "scan_id": sanitize_graph_text(metadata.get("scan_id") or ""),
            "node_count": int(metadata.get("node_count") or len(graph.get("nodes", []))),
            "edge_count": int(metadata.get("edge_count") or len(graph.get("edges", []))),
        },
        "graph": graph,
        "rollback": {
            "disable_path": f"delete {LIVE_RUNTIME_TARGET}",
            "delete_pid_path": f"delete {LIVE_RUNTIME_PID_TARGET}",
            "delete_log_path": f"delete {LIVE_RUNTIME_LOG_TARGET}",
            "fallback": "graph_only_query_mode",
            "deletion_scope": "stage_root_generated_live_runtime_artifacts_only",
        },
        "residual_risks": [
            sanitize_graph_text(item)
            for item in approval.get("residual_risks", [])
            if isinstance(item, str)
        ][:10],
        "safe_next_action": "Use this contract for local read-only graph navigation only; process startup remains explicit.",
    }
    safe_contract, report = redact_payload(contract)
    if isinstance(safe_contract, dict):
        safe_contract["redaction_summary"] = report
        safe_contract["validation"] = _merge_validation(validation, validate_live_runtime_contract(safe_contract))
        if safe_contract["validation"]["ok"] is not True:
            safe_contract["status"] = "blocked"
            safe_contract["runtime_status"] = "blocked"
        return safe_contract
    contract["validation"] = validate_live_runtime_contract(contract)
    return contract


def validate_live_runtime_contract(contract: dict[str, Any]) -> dict[str, Any]:
    """Validate Batch 25 runtime contract schema and safety invariants."""

    errors: list[str] = []
    if contract.get("schema_version") != 1:
        errors.append("schema_version")
    if contract.get("artifact_kind") != "project_graph_live_runtime_contract":
        errors.append("artifact_kind")
    if contract.get("write_policy") != "read_only":
        errors.append("write_policy")
    if contract.get("approval_boundary") != "batch25_local_read_only_runtime_auth_fallback":
        errors.append("approval_boundary")
    if contract.get("runtime_status") != "disabled_by_default_not_started":
        errors.append("runtime_status")
    server_contract = contract.get("server_contract") if isinstance(contract.get("server_contract"), dict) else {}
    if server_contract.get("write_endpoints") != []:
        errors.append("server_contract:write_endpoints")
    if server_contract.get("canonical_mutation_allowed") is not False:
        errors.append("server_contract:canonical_mutation")
    lifecycle = contract.get("server_lifecycle") if isinstance(contract.get("server_lifecycle"), dict) else {}
    if lifecycle.get("server_started") is not False:
        errors.append("server_lifecycle:server_started")
    if lifecycle.get("server_enabled_by_default") is not False:
        errors.append("server_lifecycle:default")
    auth = contract.get("auth_policy") if isinstance(contract.get("auth_policy"), dict) else {}
    if auth.get("bind_host") not in _LOCAL_HOSTS or auth.get("public_network") is not False:
        errors.append("auth_policy:local_only")
    if auth.get("token_source") != "environment":
        errors.append("auth_policy:token_source")
    fallback = contract.get("fallback_policy") if isinstance(contract.get("fallback_policy"), dict) else {}
    if fallback.get("fallback") != "graph_only_query_mode":
        errors.append("fallback_policy:fallback")
    if "canonical_graph_mutation" not in contract.get("blocked_surfaces", []):
        errors.append("blocked_surfaces:canonical_graph_mutation")
    if _has_unsafe_text(contract):
        errors.append("source_boundary:unsafe_text")
    rendered = json.dumps(contract, sort_keys=True, default=str)
    errors.extend(f"redaction:{error}" for error in validate_redaction(rendered))
    return _validation(not errors, errors, "live_runtime_contract")


def handle_live_runtime_request(contract: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    """Handle a contract-mode local runtime request without starting a server."""

    validation = validate_live_runtime_contract(contract)
    if validation["ok"] is not True:
        return _blocked_response(["live_runtime_contract:invalid"])
    auth_errors = _runtime_auth_errors(contract, request)
    if auth_errors:
        return _blocked_response(auth_errors)
    method = str(request.get("method") or "GET").upper()
    path = sanitize_graph_text(request.get("path") or "/")
    if method == "GET" and path == "/status":
        return {
            "schema_version": 1,
            "status": "ok",
            "runtime_backend": "local_read_only_contract",
            "server_status": contract.get("runtime_status"),
            "server_started": False,
            "fallback": "graph_only_query_mode",
            "write_policy": "read_only",
        }
    if method == "POST" and path == "/query":
        graph = contract.get("graph") if isinstance(contract.get("graph"), dict) else {}
        body = request.get("body") if isinstance(request.get("body"), dict) else {}
        packet = query_project_graph(graph, {key: value for key, value in body.items() if value not in (None, [], "")})
        packet["runtime_backend"] = "local_read_only_contract"
        packet["fallback"] = "graph_only_query_mode"
        packet["server_started"] = False
        return _redacted_dict(packet)
    return _blocked_response(["live_runtime_contract:read_only"])


def stage_live_runtime_contract(
    graph_artifact: str | Path,
    stage_root: str | Path,
    *,
    workspace: str | Path,
    approval: dict[str, Any] | None,
    governance_artifact: str | Path | None,
) -> dict[str, Any]:
    """Stage the Batch 25 local runtime contract under an explicit stage root."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    graph = load_graph_artifact(graph_artifact)
    governance = _load_json_file(governance_artifact) if governance_artifact else None
    contract = build_live_runtime_contract(graph, approval=approval, governance_packet=governance)
    target = stage_path / LIVE_RUNTIME_TARGET
    action = "blocked"
    if contract.get("status") == "ready" and contract.get("validation", {}).get("ok") is True:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(contract, indent=2, sort_keys=True), encoding="utf-8")
        action = "create"
    return {
        "rendered_artifacts": {
            "status": contract.get("status"),
            "mode": "validate-live-runtime",
            "root_status": "redacted",
            "server_started": False,
            "provider_calls": "not_performed",
            "canonical_graph_mutation": "not_performed",
            "fallback": "graph_only_query_mode",
            "files": [
                {
                    "target_path": LIVE_RUNTIME_TARGET,
                    "action": action,
                    "write_policy": "staged_only" if action == "create" else "blocked",
                    "staged_path": LIVE_RUNTIME_TARGET,
                }
            ],
            "validation": contract.get("validation"),
            "rollback": contract.get("rollback"),
        }
    }


def disable_live_runtime_contract(stage_root: str | Path, *, workspace: str | Path) -> dict[str, Any]:
    """Delete generated Batch 25 runtime artifacts from the stage root only."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    deleted: list[str] = []
    for relative in [LIVE_RUNTIME_TARGET, LIVE_RUNTIME_PID_TARGET, LIVE_RUNTIME_LOG_TARGET]:
        target = stage_path / relative
        if target.exists() and target.is_file():
            target.unlink()
            deleted.append(relative)
    return {
        "rendered_artifacts": {
            "status": "disabled",
            "mode": "disable-live-runtime",
            "root_status": "redacted",
            "server_started": False,
            "fallback": "graph_only_query_mode",
            "deletion_proof": {
                "targets_checked": [LIVE_RUNTIME_TARGET, LIVE_RUNTIME_PID_TARGET, LIVE_RUNTIME_LOG_TARGET],
                "deleted": deleted,
                "deletion_scope": "stage_root_generated_live_runtime_artifacts_only",
            },
            "files": [
                {
                    "target_path": relative,
                    "action": "delete_if_present",
                    "write_policy": "stage_generated_file_only",
                    "staged_path": relative,
                }
                for relative in [LIVE_RUNTIME_TARGET, LIVE_RUNTIME_PID_TARGET, LIVE_RUNTIME_LOG_TARGET]
            ],
            "rollback": {"disable_path": f"delete {LIVE_RUNTIME_TARGET}"},
        }
    }


def _validate_governance_prerequisite(governance_packet: Any) -> list[str]:
    if not isinstance(governance_packet, dict):
        return ["live_runtime_approval:governance_packet:missing"]
    errors: list[str] = []
    validation = validate_live_governance_packet(governance_packet)
    if validation.get("ok") is not True:
        errors.append("live_runtime_approval:governance_packet:invalid")
    if governance_packet.get("status") != "ready":
        errors.append("live_runtime_approval:governance_packet:not_ready")
    if governance_packet.get("artifact_kind") != "project_graph_live_governance":
        errors.append("live_runtime_approval:governance_packet:artifact_kind")
    return errors


def _validate_server_contract(value: Any) -> list[str]:
    contract = value if isinstance(value, dict) else {}
    errors: list[str] = []
    if contract.get("read_endpoints") != ["GET /status", "POST /query"]:
        errors.append("live_runtime_approval:server_contract:read_endpoints")
    if contract.get("write_endpoints") != []:
        errors.append("live_runtime_approval:server_contract:write_endpoints")
    if contract.get("canonical_mutation_allowed") is not False:
        errors.append("live_runtime_approval:server_contract:canonical_mutation")
    if contract.get("stable_json_errors") is not True:
        errors.append("live_runtime_approval:server_contract:stable_json_errors")
    if _positive_int(contract.get("max_payload_tokens"), 0) <= 0:
        errors.append("live_runtime_approval:server_contract:max_payload_tokens")
    return errors


def _validate_lifecycle_controls(value: Any) -> list[str]:
    lifecycle = value if isinstance(value, dict) else {}
    errors: list[str] = []
    for key in ["server_enabled_by_default", "server_started_in_batch"]:
        if lifecycle.get(key) is not False:
            errors.append(f"live_runtime_approval:lifecycle_controls:{key}")
    for key in ["start_requires_explicit_command", "cleanup_required", "shutdown_required"]:
        if lifecycle.get(key) is not True:
            errors.append(f"live_runtime_approval:lifecycle_controls:{key}")
    for key, expected in [("pid_path", LIVE_RUNTIME_PID_TARGET), ("log_path", LIVE_RUNTIME_LOG_TARGET)]:
        if safe_relative_path_text(lifecycle.get(key) or "") != expected:
            errors.append(f"live_runtime_approval:lifecycle_controls:{key}")
    return errors


def _validate_auth_policy(value: Any) -> list[str]:
    auth = value if isinstance(value, dict) else {}
    errors: list[str] = []
    if auth.get("bind_host") not in _LOCAL_HOSTS:
        errors.append("live_runtime_approval:auth_policy:bind_host")
    if auth.get("public_network") is not False:
        errors.append("live_runtime_approval:auth_policy:public_network")
    if auth.get("token_required") is not True:
        errors.append("live_runtime_approval:auth_policy:token_required")
    if auth.get("token_source") != "environment":
        errors.append("live_runtime_approval:auth_policy:token_source")
    if not re.fullmatch(r"[A-Z][A-Z0-9_]{3,}", str(auth.get("token_env_var") or "")):
        errors.append("live_runtime_approval:auth_policy:token_env_var")
    if "token_value" in auth or "api_key" in auth or "secret" in auth:
        errors.append("live_runtime_approval:auth_policy:stored_secret")
    if auth.get("cors_policy") != "local_only":
        errors.append("live_runtime_approval:auth_policy:cors")
    if auth.get("offline_assets_only") is not True:
        errors.append("live_runtime_approval:auth_policy:offline_assets")
    return errors


def _validate_fallback_policy(value: Any) -> list[str]:
    fallback = value if isinstance(value, dict) else {}
    errors: list[str] = []
    if fallback.get("fallback") != "graph_only_query_mode":
        errors.append("live_runtime_approval:fallback_policy:fallback")
    if fallback.get("disable_deletes_runtime_artifacts") is not True:
        errors.append("live_runtime_approval:fallback_policy:disable")
    return errors


def _server_contract_packet(value: Any) -> dict[str, Any]:
    contract = value if isinstance(value, dict) else {}
    return {
        "read_endpoints": _sorted_sanitized_list(contract.get("read_endpoints")),
        "write_endpoints": [],
        "canonical_mutation_allowed": False,
        "stable_json_errors": contract.get("stable_json_errors") is True,
        "max_payload_tokens": _positive_int(contract.get("max_payload_tokens"), 0),
        "external_network_dependency": False,
    }


def _lifecycle_packet(value: Any) -> dict[str, Any]:
    lifecycle = value if isinstance(value, dict) else {}
    return {
        "server_enabled_by_default": False,
        "start_requires_explicit_command": lifecycle.get("start_requires_explicit_command") is True,
        "server_started": False,
        "pid_path": safe_relative_path_text(lifecycle.get("pid_path") or LIVE_RUNTIME_PID_TARGET),
        "log_path": safe_relative_path_text(lifecycle.get("log_path") or LIVE_RUNTIME_LOG_TARGET),
        "cleanup_required": lifecycle.get("cleanup_required") is True,
        "shutdown_required": lifecycle.get("shutdown_required") is True,
        "health_check": "contract_only_no_process_started",
    }


def _auth_policy_packet(value: Any) -> dict[str, Any]:
    auth = value if isinstance(value, dict) else {}
    return {
        "bind_host": sanitize_graph_text(auth.get("bind_host") or ""),
        "public_network": False,
        "token_required": auth.get("token_required") is True,
        "token_source": "environment",
        "token_env_var": sanitize_graph_text(auth.get("token_env_var") or ""),
        "token_value_stored": False,
        "cors_policy": sanitize_graph_text(auth.get("cors_policy") or ""),
        "offline_assets_only": auth.get("offline_assets_only") is True,
    }


def _fallback_policy_packet(value: Any) -> dict[str, Any]:
    fallback = value if isinstance(value, dict) else {}
    return {
        "fallback": sanitize_graph_text(fallback.get("fallback") or ""),
        "disable_deletes_runtime_artifacts": fallback.get("disable_deletes_runtime_artifacts") is True,
        "fallback_available_after_disable": True,
    }


def _runtime_auth_errors(contract: dict[str, Any], request: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    host = sanitize_graph_text(request.get("host") or "127.0.0.1")
    if host not in _LOCAL_HOSTS:
        errors.append("live_runtime_auth:public_bind")
    auth = contract.get("auth_policy") if isinstance(contract.get("auth_policy"), dict) else {}
    headers = request.get("headers") if isinstance(request.get("headers"), dict) else {}
    token = headers.get("authorization") or headers.get("Authorization")
    if auth.get("token_required") is True and not token:
        errors.append("live_runtime_auth:unauthorized")
    return errors


def _blocked_response(errors: list[str]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "status": "blocked",
        "errors": sorted(set(errors)),
        "stable_json_error": True,
        "server_started": False,
        "fallback": "graph_only_query_mode",
    }


def _validate_stage_boundary(stage_path: Path, workspace_path: Path) -> None:
    if stage_path == workspace_path or stage_path.is_relative_to(workspace_path):
        raise ValueError("stage output directory must be outside workspace")
    if stage_path.exists() and not stage_path.is_dir():
        raise ValueError("stage output path is not a directory")


def _load_json_file(path: str | Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def _redacted_dict(payload: dict[str, Any]) -> dict[str, Any]:
    redacted, _report = redact_payload(payload)
    return redacted if isinstance(redacted, dict) else {}


def _has_unsafe_text(value: Any) -> bool:
    rendered = json.dumps(value, sort_keys=True, default=str)
    return bool(_WINDOWS_PATH_PATTERN.search(rendered) or _POSIX_PATH_PATTERN.search(rendered))


def _sorted_sanitized_list(value: Any) -> list[str]:
    return sorted(sanitize_graph_text(item) for item in value if isinstance(item, str)) if isinstance(value, list) else []


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed >= 0 else default


def _validation(ok: bool, errors: list[str], check: str) -> dict[str, Any]:
    return {"ok": ok, "checks": [check], "errors": sorted(set(errors))}


def _merge_validation(primary: dict[str, Any], secondary: dict[str, Any]) -> dict[str, Any]:
    return {
        "ok": primary.get("ok") is True and secondary.get("ok") is True,
        "checks": sorted(set(list(primary.get("checks", [])) + list(secondary.get("checks", [])))),
        "errors": sorted(set(list(primary.get("errors", [])) + list(secondary.get("errors", [])))),
    }
