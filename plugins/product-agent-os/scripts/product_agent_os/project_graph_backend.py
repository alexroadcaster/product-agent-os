"""Local query backend gate for Product-Agent OS project graphs.

This module implements a generated local file-store contract. It does not
start a server or create a live database; server activation remains an
explicit future operation outside default Batch 20 behavior.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import redact_payload
from product_agent_os.project_graph_index import (
    build_static_search_index,
    graph_content_fingerprint,
    validate_static_search_index,
)
from product_agent_os.project_graph_queries import load_graph_artifact, query_project_graph
from product_agent_os.project_graph_sanitization import safe_relative_path_text, sanitize_graph_text


LOCAL_BACKEND_TARGET = ".codex/product-agent-os/project-code-graph-backend.json"
DEFAULT_BACKEND_LOG_PATH = ".codex/product-agent-os/project-code-graph-backend.log"
DEFAULT_BACKEND_PID_PATH = ".codex/product-agent-os/project-code-graph-backend.pid"
MAX_BACKEND_STORE_BYTES = 5_000_000
DEFAULT_MAX_QUERY_MS = 250
DEFAULT_MAX_PAYLOAD_TOKENS = 4_000

_APPROVAL_FIELDS = {
    "explicit_approval",
    "storage_path",
    "port_policy",
    "process_lifecycle",
    "auth_boundary",
    "cleanup",
    "logging",
    "performance_threshold",
    "rollback_path",
}


def validate_backend_approval(approval: dict[str, Any] | None) -> dict[str, Any]:
    """Validate the explicit approval packet required before staging a local backend store."""

    errors: list[str] = []
    if not isinstance(approval, dict):
        return _validation(False, ["backend_approval:missing"], "backend_approval")
    missing = sorted(field for field in _APPROVAL_FIELDS if field not in approval)
    errors.extend(f"backend_approval:{field}:missing" for field in missing)
    if approval.get("explicit_approval") is not True:
        errors.append("backend_approval:explicit_approval")
    if safe_relative_path_text(approval.get("storage_path") or "") != LOCAL_BACKEND_TARGET:
        errors.append("backend_approval:storage_path")

    port_policy = approval.get("port_policy") if isinstance(approval.get("port_policy"), dict) else {}
    if port_policy.get("host") != "127.0.0.1":
        errors.append("backend_approval:port_policy:host")
    try:
        port = int(port_policy.get("port") or 0)
    except (TypeError, ValueError):
        port = -1
    if port != 0:
        errors.append("backend_approval:port_policy:disabled_port")
    if port_policy.get("mode") != "disabled_by_default":
        errors.append("backend_approval:port_policy:mode")

    lifecycle = approval.get("process_lifecycle") if isinstance(approval.get("process_lifecycle"), dict) else {}
    if lifecycle.get("server_enabled_by_default") is not False:
        errors.append("backend_approval:process_lifecycle:default")
    if lifecycle.get("start_requires_explicit_command") is not True:
        errors.append("backend_approval:process_lifecycle:start")
    if safe_relative_path_text(lifecycle.get("pid_path") or "") != lifecycle.get("pid_path"):
        errors.append("backend_approval:process_lifecycle:pid_path")

    auth = approval.get("auth_boundary") if isinstance(approval.get("auth_boundary"), dict) else {}
    if auth.get("local_only") is not True:
        errors.append("backend_approval:auth_boundary:local_only")
    if auth.get("write_controls") is not False:
        errors.append("backend_approval:auth_boundary:write_controls")

    cleanup = approval.get("cleanup") if isinstance(approval.get("cleanup"), dict) else {}
    if cleanup.get("delete_generated_store") is not True:
        errors.append("backend_approval:cleanup")

    logging = approval.get("logging") if isinstance(approval.get("logging"), dict) else {}
    if safe_relative_path_text(logging.get("log_path") or "") != logging.get("log_path"):
        errors.append("backend_approval:logging:log_path")
    if logging.get("redacted") is not True:
        errors.append("backend_approval:logging:redacted")

    thresholds = approval.get("performance_threshold") if isinstance(approval.get("performance_threshold"), dict) else {}
    if _positive_int(thresholds.get("max_query_ms"), 0) <= 0:
        errors.append("backend_approval:performance_threshold:max_query_ms")
    if _positive_int(thresholds.get("max_payload_tokens"), 0) <= 0:
        errors.append("backend_approval:performance_threshold:max_payload_tokens")

    if approval.get("rollback_path") != f"delete {LOCAL_BACKEND_TARGET}":
        errors.append("backend_approval:rollback_path")
    return _validation(not errors, errors, "backend_approval")


def build_local_query_backend_store(
    graph: dict[str, Any],
    *,
    static_index: dict[str, Any] | None = None,
    approval: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a generated local file-store contract from graph/index artifacts only."""

    approval_validation = validate_backend_approval(approval)
    if approval_validation["ok"] is not True:
        return _approval_required_store(approval_validation)

    safe_graph = _redacted_dict(graph)
    index = static_index if isinstance(static_index, dict) else build_static_search_index(safe_graph)
    safe_index = _redacted_dict(index)
    metadata = safe_graph.get("metadata", {}) if isinstance(safe_graph.get("metadata"), dict) else {}
    thresholds = approval.get("performance_threshold", {}) if isinstance(approval, dict) else {}
    store = {
        "schema_version": 1,
        "artifact_kind": "project_graph_local_query_backend",
        "write_policy": "read_only",
        "status": "ready",
        "source_boundary": "graph_and_static_index_artifacts_only_raw_source_excluded",
        "generated_view_policy": "local_backend_store_is_generated_cache_not_source_of_truth",
        "approval_boundary": "batch20_explicit_local_backend_gate_no_active_server_default",
        "graph_fingerprint": graph_content_fingerprint(safe_graph),
        "storage": {
            "storage_kind": "local_file_store",
            "storage_path": LOCAL_BACKEND_TARGET,
            "schema_version": 1,
            "migration_guard": "schema_version_must_match_before_reuse",
            "max_store_bytes": MAX_BACKEND_STORE_BYTES,
            "backup_target": ".codex/product-agent-os/project-code-graph-backend.previous.json",
            "cleanup_command": f"delete {LOCAL_BACKEND_TARGET}",
        },
        "server_lifecycle": {
            "server_status": "disabled_by_default",
            "active_process": False,
            "host": "127.0.0.1",
            "port": 0,
            "start_requires_explicit_command": True,
            "pid_path": safe_relative_path_text(
                approval.get("process_lifecycle", {}).get("pid_path") or DEFAULT_BACKEND_PID_PATH
            ),
            "log_path": safe_relative_path_text(approval.get("logging", {}).get("log_path") or DEFAULT_BACKEND_LOG_PATH),
            "process_lifecycle_policy": "no_start_in_batch20_default_path",
        },
        "api_contract": {
            "endpoints": [
                {"method": "GET", "path": "/status", "write_policy": "read_only"},
                {"method": "POST", "path": "/query", "write_policy": "read_only"},
            ],
            "forbidden_controls": ["write", "edit", "delete_node", "browser_file_edit"],
            "request_id_required": True,
            "stable_json_errors": True,
            "external_network_dependency": False,
        },
        "performance_threshold": {
            "max_query_ms": _positive_int(thresholds.get("max_query_ms"), DEFAULT_MAX_QUERY_MS),
            "max_payload_tokens": _positive_int(thresholds.get("max_payload_tokens"), DEFAULT_MAX_PAYLOAD_TOKENS),
            "concurrency_policy": "deterministic_read_only",
        },
        "rollback": {
            "disable_path": f"delete {LOCAL_BACKEND_TARGET}",
            "fallback": "graph_only_query_mode",
            "deletion_scope": "stage_root_generated_backend_store_only",
        },
        "metadata": {
            "scan_id": sanitize_graph_text(metadata.get("scan_id") or ""),
            "node_count": int(metadata.get("node_count") or len(safe_graph.get("nodes", []))),
            "edge_count": int(metadata.get("edge_count") or len(safe_graph.get("edges", []))),
        },
        "graph": safe_graph,
        "static_index": safe_index,
    }
    store["validation"] = validate_local_query_backend_store(store)
    return store


def validate_local_query_backend_store(store: dict[str, Any]) -> dict[str, Any]:
    """Validate the generated backend store and live-server gate invariants."""

    errors: list[str] = []
    if store.get("schema_version") != 1:
        errors.append("schema_version")
    if store.get("artifact_kind") != "project_graph_local_query_backend":
        errors.append("artifact_kind")
    if store.get("write_policy") != "read_only":
        errors.append("write_policy")
    if store.get("source_boundary") != "graph_and_static_index_artifacts_only_raw_source_excluded":
        errors.append("source_boundary")
    if not str(store.get("graph_fingerprint") or "").startswith("sha256:"):
        errors.append("graph_fingerprint")
    lifecycle = store.get("server_lifecycle") if isinstance(store.get("server_lifecycle"), dict) else {}
    if lifecycle.get("server_status") != "disabled_by_default" or lifecycle.get("active_process") is not False:
        errors.append("server_lifecycle:default_disabled")
    if lifecycle.get("host") != "127.0.0.1" or int(lifecycle.get("port") or 0) != 0:
        errors.append("server_lifecycle:port_policy")
    storage = store.get("storage") if isinstance(store.get("storage"), dict) else {}
    if storage.get("storage_path") != LOCAL_BACKEND_TARGET:
        errors.append("storage:path")
    api = store.get("api_contract") if isinstance(store.get("api_contract"), dict) else {}
    if api.get("external_network_dependency") is not False:
        errors.append("api_contract:external_network")
    if _has_unsafe_text(store):
        errors.append("source_boundary:unsafe_text")
    static_index = store.get("static_index") if isinstance(store.get("static_index"), dict) else {}
    if static_index:
        index_validation = static_index.get("validation") or validate_static_search_index(static_index)
        if index_validation.get("ok") is not True:
            errors.append("static_index:invalid")
        if static_index.get("graph_fingerprint") != store.get("graph_fingerprint"):
            errors.append("static_index:stale")
    return _validation(not errors, errors, "local_query_backend_store")


def stage_local_query_backend(
    graph_artifact: str | Path,
    stage_root: str | Path,
    *,
    workspace: str | Path,
    approval: dict[str, Any] | None,
    static_index_artifact: str | Path | None = None,
) -> dict[str, Any]:
    """Stage a generated local backend store under an explicit stage root."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    approval_validation = validate_backend_approval(approval)
    if approval_validation["ok"] is not True:
        return _stage_result("approval_required", "blocked", approval_validation, action="blocked")

    graph = load_graph_artifact(graph_artifact)
    static_index = _load_optional_json(static_index_artifact) if static_index_artifact else None
    store = build_local_query_backend_store(graph, static_index=static_index, approval=approval)
    target = stage_path / LOCAL_BACKEND_TARGET
    if store.get("validation", {}).get("ok") is not True:
        return _stage_result("blocked", "blocked", store["validation"], action="blocked")
    serialized = json.dumps(store, indent=2, sort_keys=True)
    if len(serialized.encode("utf-8")) > MAX_BACKEND_STORE_BYTES:
        return _stage_result("blocked", "blocked", _validation(False, ["storage:size_cap"], "local_query_backend_store"), action="blocked")
    _backup_existing(target, target.with_name("project-code-graph-backend.previous.json"))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(serialized, encoding="utf-8")
    return _stage_result("ready", "ready", store["validation"], action="create")


def load_local_query_backend_store(path: str | Path) -> dict[str, Any]:
    """Load a generated local backend store without reading workspace source files."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("local query backend store must be a JSON object")
    return payload


def disable_local_query_backend(stage_root: str | Path, *, workspace: str | Path) -> dict[str, Any]:
    """Disable the generated backend by deleting only its stage-root store file."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    target = stage_path / LOCAL_BACKEND_TARGET
    if target.exists() and target.is_file():
        target.unlink()
    for relative in [DEFAULT_BACKEND_LOG_PATH, DEFAULT_BACKEND_PID_PATH]:
        candidate = stage_path / relative
        if candidate.exists() and candidate.is_file():
            candidate.unlink()
    return {
        "rendered_artifacts": {
            "status": "disabled",
            "mode": "disable-backend",
            "root_status": "redacted",
            "fallback": "graph_only_query_mode",
            "files": [
                {
                    "target_path": LOCAL_BACKEND_TARGET,
                    "action": "delete_if_present",
                    "write_policy": "stage_generated_file_only",
                    "staged_path": LOCAL_BACKEND_TARGET,
                }
            ],
            "rollback": {"disable_path": f"delete {LOCAL_BACKEND_TARGET}"},
        }
    }


def handle_backend_api_request(store: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    """Handle the local backend read-only JSON API contract without a live server."""

    method = sanitize_graph_text(request.get("method") or "").upper()
    path = sanitize_graph_text(request.get("path") or "")
    request_id = _backend_request_id(request)
    validation = validate_local_query_backend_store(store)
    if validation["ok"] is not True:
        return _api_error("backend_store:invalid", request_id=request_id)
    if not _safe_api_path(path):
        return _api_error("backend_api:path_invalid", request_id=request_id)
    if method == "GET" and path == "/status":
        return {
            "schema_version": 1,
            "write_policy": "read_only",
            "status": "ok",
            "request_id": request_id,
            "query_backend": "local_file_store",
            "backend_status": {
                "server_status": store["server_lifecycle"]["server_status"],
                "active_process": False,
                "storage_path": LOCAL_BACKEND_TARGET,
                "source_boundary": store["source_boundary"],
            },
            "errors": [],
        }
    if method == "POST" and path == "/query":
        body = request.get("body") if isinstance(request.get("body"), dict) else {}
        packet = query_local_backend(store, body)
        packet["request_id"] = request_id
        return packet
    if method in {"POST", "PUT", "PATCH", "DELETE"}:
        return _api_error("backend_api:read_only", request_id=request_id)
    return _api_error("backend_api:not_found", request_id=request_id)


def query_local_backend(store: dict[str, Any], query: dict[str, Any]) -> dict[str, Any]:
    """Run a bounded read-only query against the generated local backend store."""

    validation = validate_local_query_backend_store(store)
    if validation["ok"] is not True:
        return _api_error("backend_store:invalid", request_id=_backend_request_id(query))
    graph = store.get("graph") if isinstance(store.get("graph"), dict) else {}
    static_index = store.get("static_index") if isinstance(store.get("static_index"), dict) else None
    packet = query_project_graph(graph, query, static_index=static_index)
    packet["query_backend"] = "local_file_store"
    packet["server_status"] = "disabled_by_default"
    packet["approval_boundary"] = "batch20_explicit_local_backend_gate_no_active_server_default"
    packet["safe_next_action"] = (
        "Use local backend store as generated orientation cache only; graph-only mode remains available."
    )
    return packet


def evaluate_backend_query_contract(
    store: dict[str, Any],
    queries: list[dict[str, Any]],
    *,
    thresholds: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate deterministic local backend query behavior against explicit thresholds."""

    thresholds = thresholds or {}
    max_query_ms = _positive_int(thresholds.get("max_query_ms"), DEFAULT_MAX_QUERY_MS)
    max_payload_tokens = _positive_int(thresholds.get("max_payload_tokens"), DEFAULT_MAX_PAYLOAD_TOKENS)
    durations: list[float] = []
    packets: list[dict[str, Any]] = []
    for query in queries:
        started = time.perf_counter()
        packet = query_local_backend(store, query)
        durations.append((time.perf_counter() - started) * 1000)
        packets.append(packet)
    deterministic = _deterministic_under_parallel_reads(store, queries)
    max_duration = round(max(durations or [0.0]), 3)
    max_tokens = max((_estimated_tokens(packet) for packet in packets), default=0)
    errors: list[str] = []
    if max_duration > max_query_ms:
        errors.append("performance:max_query_ms")
    if max_tokens > max_payload_tokens:
        errors.append("performance:max_payload_tokens")
    if not deterministic:
        errors.append("concurrency:non_deterministic")
    return {
        "schema_version": 1,
        "status": "ok" if not errors else "blocked",
        "write_policy": "read_only",
        "query_backend": "local_file_store",
        "approval_boundary": "batch20_explicit_local_backend_gate_no_active_server_default",
        "performance": {
            "max_query_ms": max_duration,
            "threshold_max_query_ms": max_query_ms,
            "max_payload_tokens": max_tokens,
            "threshold_max_payload_tokens": max_payload_tokens,
        },
        "concurrency": {"deterministic_read_results": deterministic},
        "rollback": {"fallback": "graph_only_query_mode", "disable_path": f"delete {LOCAL_BACKEND_TARGET}"},
        "errors": errors,
    }


def _approval_required_store(validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_kind": "project_graph_local_query_backend",
        "write_policy": "read_only",
        "status": "approval_required",
        "source_boundary": "graph_and_static_index_artifacts_only_raw_source_excluded",
        "approval_boundary": "batch20_explicit_local_backend_gate_no_active_server_default",
        "server_lifecycle": {"server_status": "disabled_by_default", "active_process": False},
        "rollback": {"disable_path": f"delete {LOCAL_BACKEND_TARGET}", "fallback": "graph_only_query_mode"},
        "validation": validation,
    }


def _stage_result(status: str, backend_status: str, validation: dict[str, Any], *, action: str) -> dict[str, Any]:
    return {
        "rendered_artifacts": {
            "status": status,
            "mode": "build-backend",
            "root_status": "redacted",
            "server_status": "disabled_by_default",
            "backend_status": backend_status,
            "source_boundary": "graph_and_static_index_artifacts_only_raw_source_excluded",
            "fallback": "graph_only_query_mode",
            "rollback": {"disable_path": f"delete {LOCAL_BACKEND_TARGET}"},
            "files": [
                {
                    "target_path": LOCAL_BACKEND_TARGET,
                    "action": action,
                    "write_policy": "staged_only" if action == "create" else "blocked",
                    "staged_path": LOCAL_BACKEND_TARGET,
                }
            ],
            "validation": validation,
        }
    }


def _validate_stage_boundary(stage_path: Path, workspace_path: Path) -> None:
    if stage_path == workspace_path or stage_path.is_relative_to(workspace_path):
        raise ValueError("stage output directory must be outside workspace")
    if stage_path.exists() and not stage_path.is_dir():
        raise ValueError("stage output path is not a directory")


def _backup_existing(target: Path, backup_target: Path) -> None:
    if not target.exists() or not target.is_file():
        return
    backup_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(target, backup_target)


def _load_optional_json(path: str | Path | None) -> dict[str, Any] | None:
    if not path:
        return None
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def _redacted_dict(payload: dict[str, Any]) -> dict[str, Any]:
    redacted, _report = redact_payload(payload)
    return redacted if isinstance(redacted, dict) else payload


def _api_error(error: str, *, request_id: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "status": "blocked",
        "request_id": request_id,
        "query_backend": "local_file_store",
        "server_status": "disabled_by_default",
        "errors": [error],
        "nodes": [],
        "edges": [],
    }


def _safe_api_path(path: str) -> bool:
    if path in {"/status", "/query", "/write"}:
        return True
    if path.startswith("/") and ".." not in path.split("/") and "://" not in path:
        return True
    return False


def _deterministic_under_parallel_reads(store: dict[str, Any], queries: list[dict[str, Any]]) -> bool:
    if not queries:
        return True
    with ThreadPoolExecutor(max_workers=min(4, len(queries) * 2)) as executor:
        first = list(executor.map(lambda query: json.dumps(query_local_backend(store, query), sort_keys=True), queries))
        second = list(executor.map(lambda query: json.dumps(query_local_backend(store, query), sort_keys=True), queries))
    return first == second


def _backend_request_id(request: dict[str, Any]) -> str:
    return "backend-request:" + hashlib.sha256(json.dumps(request, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def _estimated_tokens(packet: dict[str, Any]) -> int:
    return max(1, len(json.dumps(packet, sort_keys=True)) // 4)


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


def _validation(ok: bool, errors: list[str], check: str) -> dict[str, Any]:
    return {"ok": ok, "checks": [check], "errors": sorted(set(errors))}


def _has_unsafe_text(value: Any) -> bool:
    serialized = json.dumps(value, sort_keys=True).lower()
    forbidden = ["fixture-secret", "http://", "https://", "c:\\users\\", "/users/", "/home/", "/tmp/"]
    return any(item in serialized for item in forbidden)
