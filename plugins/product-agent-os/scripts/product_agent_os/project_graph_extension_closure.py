"""Future extension verification and rollback closure for project graph artifacts.

Batch 23 is a closure layer over approved Batch 19-22 generated artifacts.
It does not enable live servers, external model/API calls or canonical graph
mutation. It records verification evidence, rollback/data deletion proof and
graph-only fallback status.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from product_agent_os.project_graph_backend import (
    DEFAULT_BACKEND_LOG_PATH,
    DEFAULT_BACKEND_PID_PATH,
    LOCAL_BACKEND_TARGET,
    validate_local_query_backend_store,
)
from product_agent_os.project_graph_index import (
    STATIC_SEARCH_INDEX_TARGET,
    validate_static_search_index,
)
from product_agent_os.project_graph_llm_extraction import (
    LLM_EXTRACTION_TARGET,
    validate_llm_extraction_proposals,
)
from product_agent_os.project_graph_queries import load_graph_artifact, query_project_graph
from product_agent_os.project_graph_sanitization import sanitize_graph_text
from product_agent_os.project_graph_semantic import (
    SEMANTIC_RETRIEVAL_TARGET,
    validate_semantic_retrieval_index,
)


EXTENSION_CLOSURE_TARGET = ".codex/product-agent-os/project-code-graph-extension-closure.json"
APPROVED_EXTENSION_SURFACES = {
    "static_index": STATIC_SEARCH_INDEX_TARGET,
    "backend": LOCAL_BACKEND_TARGET,
    "semantic": SEMANTIC_RETRIEVAL_TARGET,
    "llm_proposals": LLM_EXTRACTION_TARGET,
}
_DELETION_TARGETS = (
    STATIC_SEARCH_INDEX_TARGET,
    ".codex/product-agent-os/project-code-graph-search-index.previous.json",
    LOCAL_BACKEND_TARGET,
    ".codex/product-agent-os/project-code-graph-backend.previous.json",
    DEFAULT_BACKEND_LOG_PATH,
    DEFAULT_BACKEND_PID_PATH,
    SEMANTIC_RETRIEVAL_TARGET,
    ".codex/product-agent-os/project-code-graph-semantic-index.previous.json",
    LLM_EXTRACTION_TARGET,
    ".codex/product-agent-os/project-code-graph-llm-proposals.previous.json",
    EXTENSION_CLOSURE_TARGET,
)
_DEFERRED_SURFACES = (
    "live_database_server",
    "production_query_backend",
    "live_external_embedding_provider",
    "live_external_cross_encoder",
    "live_external_llm_semantic_extraction",
    "canonical_graph_mutation_from_generated_proposals",
    "external_network_requests",
)


def build_future_extension_closure_packet(
    *,
    workspace: str | Path,
    stage_root: str | Path,
    graph: dict[str, Any] | None = None,
    artifacts: dict[str, dict[str, Any]] | None = None,
    verification_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a source-free closure packet for approved project graph extensions."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    evidence_validation = _validate_verification_evidence(verification_evidence)
    loaded_artifacts = artifacts if artifacts is not None else _load_stage_artifacts(stage_path)
    surface_packets, surface_errors = _surface_packets(loaded_artifacts)
    runtime_visual_qa = _runtime_visual_qa(loaded_artifacts)
    fallback = _graph_only_fallback(graph)
    errors = [*surface_errors, *evidence_validation["errors"]]
    status = "verification_required" if evidence_validation["ok"] is not True else "ready"
    if evidence_validation["ok"] is True and surface_errors:
        status = "blocked"
    packet = {
        "schema_version": 1,
        "artifact_kind": "project_graph_future_extension_closure",
        "write_policy": "read_only",
        "status": status,
        "approval_boundary": "batch23_future_extension_verification_rollback_closure",
        "source_boundary": "approved_generated_extension_artifacts_only_no_raw_source_or_private_data",
        "generated_view_policy": "closure_report_is_generated_evidence_not_source_of_truth",
        "approved_surfaces": surface_packets,
        "deferred_surface_status": {
            surface: "blocked_without_new_explicit_approval"
            for surface in _DEFERRED_SURFACES
        },
        "runtime_visual_qa": runtime_visual_qa,
        "rollback_data_deletion": {
            "rollback_data_deletion_proof_required": True,
            "disable_command": "scan_project_code_graph.py --disable-extensions --stage <stage-root>",
            "targets_checked": list(_DELETION_TARGETS),
            "deletion_scope": "stage_root_generated_extension_artifacts_only",
            "graph_only_fallback_required": True,
        },
        "graph_only_fallback": fallback,
        "full_verification_contract": {
            "timeout_ms": 1_200_000,
            "focused_suites_required": [
                "project_graph_index",
                "project_graph_backend",
                "project_graph_semantic",
                "project_graph_llm_extraction",
                "project_graph_extension_closure",
                "project_graph_cli",
            ],
            "full_commands_required": [
                "python -m unittest discover -s tests -p \"test_*.py\" -v",
                "python plugins\\product-agent-os\\scripts\\run_fixture_eval.py",
                "python plugins\\product-agent-os\\scripts\\run_transcript_eval.py plugins\\product-agent-os\\assets\\eval-fixtures\\transcripts\\product-agent-os-synthetic-sessions.json",
                "python plugins\\product-agent-os\\scripts\\validate_codex_compatibility.py",
                "python tools\\check_docs.py",
                "python -m mkdocs build --strict --site-dir .mkdocs_task25_batch23_site",
                "git diff --check",
            ],
            "verification_evidence": _compact_evidence(verification_evidence),
        },
        "git_boundary": "explicit_only",
        "canonical_graph_mutation": "forbidden",
        "safe_next_action": (
            "Use Batch 23 closure as rollback/evidence packet only; generated extension artifacts remain non-source-of-truth."
            if status == "ready"
            else "Disable generated extension artifacts and rerun graph-only verification."
        ),
    }
    packet["validation"] = validate_future_extension_closure_packet(packet, extra_errors=errors)
    if packet["validation"]["ok"] is not True and status == "ready":
        packet["status"] = "blocked"
    return packet


def validate_future_extension_closure_packet(
    packet: dict[str, Any],
    *,
    extra_errors: list[str] | None = None,
) -> dict[str, Any]:
    """Validate Batch 23 closure schema, surface gates and source boundaries."""

    errors = list(extra_errors or [])
    if packet.get("schema_version") != 1:
        errors.append("schema_version")
    if packet.get("artifact_kind") != "project_graph_future_extension_closure":
        errors.append("artifact_kind")
    if packet.get("write_policy") != "read_only":
        errors.append("write_policy")
    if packet.get("approval_boundary") != "batch23_future_extension_verification_rollback_closure":
        errors.append("approval_boundary")
    if packet.get("canonical_graph_mutation") != "forbidden":
        errors.append("canonical_graph_mutation")
    if packet.get("git_boundary") != "explicit_only":
        errors.append("git_boundary")
    if packet.get("full_verification_contract", {}).get("timeout_ms") != 1_200_000:
        errors.append("full_verification_contract:timeout_ms")
    deferred = packet.get("deferred_surface_status") if isinstance(packet.get("deferred_surface_status"), dict) else {}
    for surface in _DEFERRED_SURFACES:
        if deferred.get(surface) != "blocked_without_new_explicit_approval":
            errors.append(f"deferred_surface:{surface}")
    if _has_unsafe_text(packet):
        errors.append("source_boundary:unsafe_text")
    return {"ok": not errors, "checks": ["batch23_future_extension_closure"], "errors": sorted(set(errors))}


def stage_future_extension_closure(
    stage_root: str | Path,
    *,
    workspace: str | Path,
    graph_artifact: str | Path | None = None,
    artifacts: dict[str, dict[str, Any]] | None = None,
    verification_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Stage the Batch 23 closure report under an explicit stage root."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    graph = load_graph_artifact(graph_artifact) if graph_artifact else None
    packet = build_future_extension_closure_packet(
        workspace=workspace_path,
        stage_root=stage_path,
        graph=graph,
        artifacts=artifacts,
        verification_evidence=verification_evidence,
    )
    target = stage_path / EXTENSION_CLOSURE_TARGET
    action = "blocked"
    if packet.get("status") == "ready" and packet.get("validation", {}).get("ok") is True:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
        action = "create"
    return {
        "rendered_artifacts": {
            "status": packet.get("status"),
            "mode": "verify-extensions",
            "root_status": "redacted",
            "source_boundary": packet.get("source_boundary"),
            "fallback": packet.get("graph_only_fallback", {}).get("fallback", "graph_only_query_mode"),
            "files": [
                {
                    "target_path": EXTENSION_CLOSURE_TARGET,
                    "action": action,
                    "write_policy": "staged_only" if action == "create" else "blocked",
                    "staged_path": EXTENSION_CLOSURE_TARGET,
                }
            ],
            "validation": packet.get("validation"),
        }
    }


def disable_future_extensions(
    stage_root: str | Path,
    *,
    workspace: str | Path,
    graph: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Delete generated extension artifacts under stage root and report proof."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    deleted: list[str] = []
    remaining: list[str] = []
    for relative in _DELETION_TARGETS:
        target = stage_path / relative
        if target.exists() and target.is_file():
            target.unlink()
            deleted.append(relative)
        if target.exists():
            remaining.append(relative)
    fallback = _graph_only_fallback(graph)
    return {
        "rendered_artifacts": {
            "status": "disabled" if not remaining else "blocked",
            "mode": "disable-extensions",
            "root_status": "redacted",
            "fallback": "graph_only_query_mode",
            "deletion_proof": {
                "targets_checked": list(_DELETION_TARGETS),
                "deleted": deleted,
                "remaining": remaining,
                "deletion_scope": "stage_root_generated_extension_artifacts_only",
            },
            "graph_only_fallback": fallback,
            "files": [
                {
                    "target_path": relative,
                    "action": "delete_if_present",
                    "write_policy": "stage_generated_file_only",
                    "staged_path": relative,
                }
                for relative in _DELETION_TARGETS
            ],
            "rollback": {"disable_path": "delete generated Batch 19-23 extension artifacts under stage root"},
        }
    }


def _surface_packets(artifacts: dict[str, dict[str, Any]] | None) -> tuple[list[dict[str, Any]], list[str]]:
    artifacts = artifacts or {}
    packets: list[dict[str, Any]] = []
    errors: list[str] = []
    for surface, target in APPROVED_EXTENSION_SURFACES.items():
        artifact = artifacts.get(surface)
        if not isinstance(artifact, dict):
            packets.append(_surface_packet(surface, target, "missing_stage_artifact", ["artifact_missing"]))
            errors.append(f"{surface}:artifact_missing")
            continue
        validation = _validate_surface(surface, artifact)
        surface_errors = list(validation.get("errors", []))
        status = "verified" if validation.get("ok") is True else "blocked"
        errors.extend(f"{surface}:{error}" for error in surface_errors)
        packets.append(_surface_packet(surface, target, status, surface_errors, artifact=artifact))
    return packets, errors


def _validate_surface(surface: str, artifact: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if surface == "static_index":
        validation = validate_static_search_index(artifact)
        errors.extend(validation.get("errors", []))
        query_policy = artifact.get("query_policy") if isinstance(artifact.get("query_policy"), dict) else {}
        if query_policy.get("no_live_database_or_server") is not True:
            errors.append("live_database_or_server")
        if query_policy.get("no_llm_embedding_or_cross_encoder") is not True:
            errors.append("llm_embedding_or_cross_encoder")
    elif surface == "backend":
        validation = validate_local_query_backend_store(artifact)
        errors.extend(validation.get("errors", []))
        lifecycle = artifact.get("server_lifecycle") if isinstance(artifact.get("server_lifecycle"), dict) else {}
        if lifecycle.get("active_process") is not False or lifecycle.get("server_status") != "disabled_by_default":
            errors.append("live_server_active")
        if int(lifecycle.get("port") or 0) != 0:
            errors.append("live_port_active")
    elif surface == "semantic":
        validation = validate_semantic_retrieval_index(artifact)
        errors.extend(validation.get("errors", []))
        if artifact.get("model_decision", {}).get("external_model_calls_allowed") is not False:
            errors.append("external_model_calls")
        if artifact.get("cross_encoder", {}).get("canonical_graph_edge_rewrites") is not False:
            errors.append("canonical_graph_edge_rewrites")
    elif surface == "llm_proposals":
        validation = validate_llm_extraction_proposals(artifact)
        errors.extend(validation.get("errors", []))
        if artifact.get("model_policy", {}).get("external_model_calls_allowed") is not False:
            errors.append("external_model_calls")
        if artifact.get("canonical_graph_mutation") != "forbidden":
            errors.append("canonical_graph_mutation")
    else:
        errors.append("unknown_surface")
    if _has_unsafe_text(artifact):
        errors.append("unsafe_text")
    return {"ok": not errors, "errors": sorted(set(errors))}


def _surface_packet(
    surface: str,
    target: str,
    status: str,
    errors: list[str],
    *,
    artifact: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rollback = artifact.get("rollback", {}) if isinstance(artifact, dict) else {}
    return {
        "surface": surface,
        "status": status,
        "artifact_target": target,
        "source_boundary": sanitize_graph_text((artifact or {}).get("source_boundary") or "generated_artifact_only"),
        "generated_view_policy": sanitize_graph_text((artifact or {}).get("generated_view_policy") or "generated_not_source_of_truth"),
        "rollback": {
            "disable_path": sanitize_graph_text(rollback.get("disable_path") or f"delete {target}"),
            "fallback": sanitize_graph_text(rollback.get("fallback") or "graph_only_query_mode"),
        },
        "validation": {"ok": not errors, "errors": sorted(set(errors))},
    }


def _runtime_visual_qa(artifacts: dict[str, dict[str, Any]] | None) -> dict[str, Any]:
    backend = (artifacts or {}).get("backend") if isinstance(artifacts, dict) else None
    lifecycle = backend.get("server_lifecycle") if isinstance(backend, dict) and isinstance(backend.get("server_lifecycle"), dict) else {}
    return {
        "runtime_browser_surface": "contract_only_no_browser_required_for_batch23",
        "backend_server_status": sanitize_graph_text(lifecycle.get("server_status") or "not_present"),
        "live_server_started": lifecycle.get("active_process") is True,
        "external_requests_allowed": False,
        "generated_view_source_boundary_labels_required": True,
    }


def _graph_only_fallback(graph: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(graph, dict):
        return {"status": "not_checked", "fallback": "graph_only_query_mode"}
    packet = query_project_graph(graph, {"query": "search", "text": "run", "max_results": 5})
    return {
        "status": sanitize_graph_text(packet.get("status") or "unknown"),
        "query_backend": sanitize_graph_text(packet.get("search_backend") or packet.get("query_backend") or "graph_only"),
        "fallback": "graph_only_query_mode",
        "node_count": len(packet.get("nodes", [])) if isinstance(packet.get("nodes"), list) else 0,
    }


def _load_stage_artifacts(stage_path: Path) -> dict[str, dict[str, Any]]:
    artifacts: dict[str, dict[str, Any]] = {}
    for surface, target in APPROVED_EXTENSION_SURFACES.items():
        path = stage_path / target
        if not path.exists() or not path.is_file():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict):
            artifacts[surface] = payload
    return artifacts


def _validate_verification_evidence(evidence: dict[str, Any] | None) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(evidence, dict):
        return {"ok": False, "errors": ["verification_evidence:missing"]}
    focused = evidence.get("focused_suites") if isinstance(evidence.get("focused_suites"), dict) else {}
    for surface in APPROVED_EXTENSION_SURFACES:
        if focused.get(surface) != "passed":
            errors.append(f"verification_evidence:focused_suites:{surface}")
    if evidence.get("full_verification_required") is not True:
        errors.append("verification_evidence:full_verification_required")
    if evidence.get("timeout_ms") != 1_200_000:
        errors.append("verification_evidence:timeout_ms")
    for key in ["docs_check_required", "strict_mkdocs_required", "diff_hygiene_required"]:
        if evidence.get(key) is not True:
            errors.append(f"verification_evidence:{key}")
    return {"ok": not errors, "errors": sorted(set(errors))}


def _compact_evidence(evidence: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(evidence, dict):
        return {"status": "verification_required"}
    return {
        "focused_suites": evidence.get("focused_suites", {}),
        "full_verification_required": evidence.get("full_verification_required") is True,
        "timeout_ms": evidence.get("timeout_ms"),
        "docs_check_required": evidence.get("docs_check_required") is True,
        "strict_mkdocs_required": evidence.get("strict_mkdocs_required") is True,
        "diff_hygiene_required": evidence.get("diff_hygiene_required") is True,
    }


def _validate_stage_boundary(stage_path: Path, workspace_path: Path) -> None:
    if stage_path == workspace_path or stage_path.is_relative_to(workspace_path):
        raise ValueError("stage output directory must be outside workspace")
    if stage_path.exists() and not stage_path.is_dir():
        raise ValueError("stage output path is not a directory")


def _has_unsafe_text(value: Any) -> bool:
    serialized = json.dumps(value, sort_keys=True).lower()
    forbidden = ["fixture-secret", "http://", "https://", "c:\\users\\", "/users/", "/home/", "/tmp/"]
    return any(item in serialized for item in forbidden)
