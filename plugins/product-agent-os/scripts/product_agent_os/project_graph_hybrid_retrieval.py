"""Hybrid retrieval pipeline for Product-Agent OS project graphs.

Batch 27 combines graph-only, static-index and semantic retrieval signals into
bounded explainable search packets. External reranker calls remain disabled by
default and can only be represented as offline eval evidence.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import redact_payload, validate_redaction
from product_agent_os.project_graph_index import (
    graph_content_fingerprint,
    load_static_search_index,
    query_static_search_index,
    validate_static_search_index,
)
from product_agent_os.project_graph_queries import load_graph_artifact, query_project_graph
from product_agent_os.project_graph_reranker_provider import (
    RERANKER_PROVIDER_TARGET,
    validate_reranker_provider_gate,
)
from product_agent_os.project_graph_sanitization import safe_relative_path_text, sanitize_graph_text
from product_agent_os.project_graph_semantic import (
    load_semantic_retrieval_index,
    query_semantic_retrieval,
    validate_semantic_retrieval_index,
)


HYBRID_RETRIEVAL_TARGET = ".codex/product-agent-os/project-code-graph-hybrid-retrieval.json"
DEFAULT_MAX_RESULTS = 25
DEFAULT_MAX_TOKENS = 4_000
MAX_QUERY_TEXT_LENGTH = 120
_WINDOWS_PATH_PATTERN = re.compile(r"\b[A-Za-z]:[\\/][^\s\"'<>]+")
_POSIX_PATH_PATTERN = re.compile(r"(^|\s)/(Users|home|private|Volumes|mnt|tmp|var)/[^\s\"'<>]+")
_SECRET_VALUE_PATTERN = re.compile(
    r"(?i)\b(?:sk-[a-z0-9_-]{8,}|api[_-]?key\s*=\s*[^\s\"'<>]+|token\s*=\s*[^\s\"'<>]+)"
)


def build_hybrid_retrieval_pipeline(
    graph: dict[str, Any],
    *,
    static_index: dict[str, Any] | None,
    semantic_index: dict[str, Any] | None,
    reranker_gate: dict[str, Any] | None,
    approval: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build the Batch 27 hybrid retrieval contract from generated artifacts."""

    approval_validation = _validate_hybrid_approval(approval)
    gate_validation = (
        validate_reranker_provider_gate(reranker_gate)
        if isinstance(reranker_gate, dict)
        else _validation(False, ["reranker_gate:missing"], "hybrid_retrieval_pipeline")
    )
    static_validation = (
        validate_static_search_index(static_index)
        if isinstance(static_index, dict)
        else {"ok": False, "errors": ["static_index:missing"]}
    )
    semantic_validation = (
        validate_semantic_retrieval_index(semantic_index)
        if isinstance(semantic_index, dict)
        else _validation(False, ["semantic_index:missing"], "semantic_retrieval_index")
    )
    validation = _merge_validation(approval_validation, gate_validation, static_validation, semantic_validation)
    if validation["ok"] is not True:
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_hybrid_retrieval_pipeline",
            "status": "approval_required",
            "write_policy": "read_only",
            "approval_boundary": "batch27_external_reranker_and_hybrid_retrieval",
            "fallback": "semantic_retrieval_or_graph_only",
            "validation": validation,
            "safe_next_action": "Provide Batch 27 approval plus valid static, semantic and reranker gate artifacts.",
        }
    approval = approval if isinstance(approval, dict) else {}
    provider = reranker_gate.get("provider_policy", {}) if isinstance(reranker_gate, dict) else {}
    thresholds = approval.get("eval_threshold", {}) if isinstance(approval.get("eval_threshold"), dict) else {}
    pipeline = {
        "schema_version": 1,
        "artifact_kind": "project_graph_hybrid_retrieval_pipeline",
        "status": "ready",
        "write_policy": "read_only",
        "approval_boundary": "batch27_external_reranker_and_hybrid_retrieval",
        "source_boundary": "graph_static_semantic_and_reranker_gate_redacted_only",
        "generated_view_policy": "hybrid_retrieval_packets_are_generated_orientation_evidence_not_source_of_truth",
        "fusion_policy": {
            "candidate_sources": ["graph_scan", "static_index", "semantic_retrieval"],
            "ranking": "weighted_static_semantic_graph_fusion_external_reranker_disabled_by_default",
            "max_candidates": _positive_int(
                provider.get("candidate_policy", {}).get("max_candidates")
                if isinstance(provider.get("candidate_policy"), dict)
                else None,
                20,
            ),
            "component_scores_required": True,
            "fusion_explanation_required": True,
            "source_backed_results_required": True,
            "confidence": "present_unverified",
            "no_completion_claims_from_matches_alone": True,
        },
        "provider_policy": {
            "provider": "external_reranker",
            "provider_call_allowed": False,
            "external_call_performed": False,
            "provider_enabled": False,
            "provider_enabled_by_default": False,
            "fallback": "semantic_retrieval_or_graph_only",
        },
        "blocked_surfaces": [
            "external_provider_call_without_runtime_invocation_approval",
            "secret_storage",
            "raw_source_payload",
            "canonical_graph_mutation",
            "production_server",
            "git_action",
        ],
        "graph_fingerprint": graph_content_fingerprint(_redacted_dict(graph)),
        "static_index_fingerprint": _artifact_fingerprint(static_index or {}, record_key="records"),
        "semantic_index_fingerprint": _artifact_fingerprint(semantic_index or {}, record_key="corpus_records"),
        "reranker_gate_fingerprint": _artifact_fingerprint(reranker_gate or {}, record_key="allowed_surfaces"),
        "eval_policy": {
            "hybrid_retrieval_eval_suite": True,
            "min_precision_at_k": _float_value(thresholds.get("min_precision_at_k"), 0.0),
            "min_mrr": _float_value(thresholds.get("min_mrr"), 0.0),
            "min_ndcg_at_k": _float_value(thresholds.get("min_ndcg_at_k"), 0.0),
            "max_false_positive_rate": _float_value(thresholds.get("max_false_positive_rate"), 1.0),
            "max_query_ms": _positive_int(thresholds.get("max_query_ms"), 250),
            "max_payload_tokens": _positive_int(thresholds.get("max_payload_tokens"), 1200),
        },
        "fallback": "semantic_retrieval_or_graph_only",
        "rollback": {
            "disable_path": f"delete {HYBRID_RETRIEVAL_TARGET}",
            "fallback": "semantic_retrieval_or_graph_only",
            "deletion_scope": "stage_root_generated_hybrid_retrieval_pipeline_only",
        },
        "safe_next_action": (
            "Use hybrid results as source-backed orientation evidence only; read source before edits or completion "
            "claims, and keep external reranker calls disabled unless eval evidence passes."
        ),
    }
    safe_pipeline, report = redact_payload(pipeline)
    if isinstance(safe_pipeline, dict):
        safe_pipeline["redaction_summary"] = report
        safe_pipeline["validation"] = _merge_validation(validation, validate_hybrid_retrieval_pipeline(safe_pipeline))
        if safe_pipeline["validation"]["ok"] is not True:
            safe_pipeline["status"] = "blocked"
        return safe_pipeline
    pipeline["validation"] = validate_hybrid_retrieval_pipeline(pipeline)
    return pipeline


def validate_hybrid_retrieval_pipeline(pipeline: dict[str, Any]) -> dict[str, Any]:
    """Validate Batch 27 hybrid retrieval schema and safety invariants."""

    errors: list[str] = []
    if pipeline.get("schema_version") != 1:
        errors.append("schema_version")
    if pipeline.get("artifact_kind") != "project_graph_hybrid_retrieval_pipeline":
        errors.append("artifact_kind")
    if pipeline.get("write_policy") != "read_only":
        errors.append("write_policy")
    if pipeline.get("approval_boundary") != "batch27_external_reranker_and_hybrid_retrieval":
        errors.append("approval_boundary")
    if pipeline.get("source_boundary") != "graph_static_semantic_and_reranker_gate_redacted_only":
        errors.append("source_boundary")
    fusion = pipeline.get("fusion_policy") if isinstance(pipeline.get("fusion_policy"), dict) else {}
    for required in ["graph_scan", "static_index", "semantic_retrieval"]:
        if required not in fusion.get("candidate_sources", []):
            errors.append(f"fusion_policy:candidate_sources:{required}")
    for field in [
        "component_scores_required",
        "fusion_explanation_required",
        "source_backed_results_required",
        "no_completion_claims_from_matches_alone",
    ]:
        if fusion.get(field) is not True:
            errors.append(f"fusion_policy:{field}")
    provider = pipeline.get("provider_policy") if isinstance(pipeline.get("provider_policy"), dict) else {}
    if provider.get("provider_call_allowed") is not False:
        errors.append("provider_policy:provider_call_allowed")
    if provider.get("external_call_performed") is not False:
        errors.append("provider_policy:external_call_performed")
    if provider.get("provider_enabled_by_default") is not False:
        errors.append("provider_policy:provider_enabled_by_default")
    if pipeline.get("fallback") != "semantic_retrieval_or_graph_only":
        errors.append("fallback")
    if "canonical_graph_mutation" not in pipeline.get("blocked_surfaces", []):
        errors.append("blocked_surfaces:canonical_graph_mutation")
    if _has_unsafe_text(pipeline):
        errors.append("source_boundary:unsafe_text")
    rendered = json.dumps(pipeline, sort_keys=True, default=str)
    errors.extend(f"redaction:{error}" for error in validate_redaction(rendered))
    return _validation(not errors, sorted(set(errors)), "hybrid_retrieval_pipeline")


def query_hybrid_retrieval(
    pipeline: dict[str, Any],
    request: dict[str, Any],
    *,
    graph: dict[str, Any],
    static_index: dict[str, Any],
    semantic_index: dict[str, Any],
) -> dict[str, Any]:
    """Run bounded hybrid search over generated local artifacts only."""

    errors = _validate_query(pipeline, request, graph, static_index, semantic_index)
    if errors:
        return _packet(pipeline, request, [], status="blocked", errors=errors, duration_ms=0.0)
    started = time.perf_counter()
    request = {key: value for key, value in request.items() if value not in (None, [], "")}
    max_candidates = _positive_int(pipeline.get("fusion_policy", {}).get("max_candidates"), 20)
    static_packet = query_static_search_index(static_index, {**request, "max_results": max_candidates})
    semantic_packet = query_semantic_retrieval(semantic_index, {**request, "max_results": max_candidates}, graph=graph)
    graph_packet = query_project_graph(graph, {**request, "max_results": max_candidates})
    node_index = _graph_node_index(graph)
    candidates: dict[str, dict[str, Any]] = {}
    _merge_component(candidates, static_packet.get("nodes", []), "static", node_index)
    _merge_component(candidates, semantic_packet.get("nodes", []), "semantic", node_index)
    _merge_component(candidates, graph_packet.get("nodes", []), "graph", node_index)
    ranked = sorted(
        (_explain_candidate(candidate) for candidate in candidates.values()),
        key=lambda item: (-float(item.get("fused_score") or 0.0), item["id"]),
    )
    duration_ms = (time.perf_counter() - started) * 1000
    return _packet(pipeline, request, ranked, status="ok", errors=[], duration_ms=duration_ms)


def evaluate_hybrid_retrieval_quality(
    pipeline: dict[str, Any],
    *,
    graph: dict[str, Any],
    static_index: dict[str, Any],
    semantic_index: dict[str, Any],
    cases: list[dict[str, Any]],
    thresholds: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate hybrid retrieval quality without provider calls."""

    applied = {**_default_thresholds(pipeline), **(thresholds or {})}
    evaluated_cases: list[dict[str, Any]] = []
    durations: list[float] = []
    payload_tokens: list[int] = []
    for case in cases:
        if not isinstance(case, dict):
            continue
        top_k = _positive_int(case.get("top_k"), 5)
        started = time.perf_counter()
        packet = query_hybrid_retrieval(
            pipeline,
            {"query": "search", "text": case.get("text") or "", "max_results": top_k, "max_tokens": applied["max_payload_tokens"]},
            graph=graph,
            static_index=static_index,
            semantic_index=semantic_index,
        )
        durations.append((time.perf_counter() - started) * 1000)
        payload_tokens.append(_estimated_tokens(packet))
        result_ids = [str(node.get("id")) for node in packet.get("nodes", []) if isinstance(node, dict)]
        expected_ids = [str(item) for item in case.get("expected_node_ids", []) if item]
        unexpected_ids = [str(item) for item in case.get("unexpected_node_ids", []) if item]
        top_results = result_ids[:top_k]
        hits = [item for item in expected_ids if item in top_results]
        false_hits = [item for item in unexpected_ids if item in top_results]
        first_rank = _first_rank(result_ids, expected_ids)
        evaluated_cases.append(
            {
                "id": sanitize_graph_text(case.get("id") or "unnamed-hybrid-case")[:80],
                "status": "passed" if expected_ids and len(hits) == len(expected_ids) and not false_hits else "failed",
                "result_status": packet.get("status"),
                "top_k": top_k,
                "returned_count": len(top_results),
                "expected_node_count": len(expected_ids),
                "hit_count": len(hits),
                "false_positive_count": len(false_hits),
                "first_relevant_rank": first_rank,
                "reciprocal_rank": 0.0 if first_rank == 0 else 1.0 / first_rank,
                "ndcg": _ndcg(top_results, expected_ids),
            }
        )
    metrics = _quality_metrics(evaluated_cases)
    metrics["max_query_ms"] = round(max(durations or [0.0]), 3)
    metrics["max_payload_tokens"] = max(payload_tokens or [0])
    failed = _failed_thresholds(metrics, applied)
    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "decision_status": "passed" if evaluated_cases and not failed else "disabled_fallback",
        "search_backend": "hybrid_retrieval",
        "approval_boundary": pipeline.get("approval_boundary"),
        "source_boundary": pipeline.get("source_boundary"),
        "quality_metrics": metrics,
        "thresholds": applied,
        "failed_thresholds": failed,
        "cases": evaluated_cases,
        "fallback": "semantic_retrieval_or_graph_only",
        "rollback": pipeline.get("rollback", {}),
        "safe_next_action": "Use hybrid hits as present_unverified orientation evidence until source reads or owner review.",
    }


def stage_hybrid_retrieval_pipeline(
    graph_artifact: str | Path,
    static_index_artifact: str | Path,
    semantic_index_artifact: str | Path,
    stage_root: str | Path,
    *,
    workspace: str | Path,
    approval: dict[str, Any] | None,
    reranker_gate_artifact: str | Path | None,
) -> dict[str, Any]:
    """Stage the Batch 27 hybrid retrieval pipeline under an explicit stage root."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    graph = load_graph_artifact(graph_artifact)
    static_index = load_static_search_index(static_index_artifact)
    semantic_index = load_semantic_retrieval_index(semantic_index_artifact)
    reranker_gate = _load_json_file(reranker_gate_artifact) if reranker_gate_artifact else None
    pipeline = build_hybrid_retrieval_pipeline(
        graph,
        static_index=static_index,
        semantic_index=semantic_index,
        reranker_gate=reranker_gate,
        approval=approval,
    )
    target = stage_path / HYBRID_RETRIEVAL_TARGET
    action = "blocked"
    if pipeline.get("status") == "ready" and pipeline.get("validation", {}).get("ok") is True:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(pipeline, indent=2, sort_keys=True), encoding="utf-8")
        action = "create"
    return {
        "rendered_artifacts": {
            "status": pipeline.get("status"),
            "mode": "build-hybrid-retrieval",
            "root_status": "redacted",
            "source_boundary": pipeline.get("source_boundary", "graph_static_semantic_and_reranker_gate_redacted_only"),
            "provider_call_allowed": False,
            "provider_enabled_by_default": False,
            "fallback": "semantic_retrieval_or_graph_only",
            "files": [
                {
                    "target_path": HYBRID_RETRIEVAL_TARGET,
                    "action": action,
                    "write_policy": "staged_only" if action == "create" else "blocked",
                    "staged_path": HYBRID_RETRIEVAL_TARGET,
                }
            ],
            "rollback": {"disable_path": f"delete {HYBRID_RETRIEVAL_TARGET}"},
            "validation": pipeline.get("validation"),
        }
    }


def load_hybrid_retrieval_pipeline(path: str | Path) -> dict[str, Any]:
    """Load a generated hybrid retrieval pipeline without reading source files."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("hybrid retrieval pipeline must be a JSON object")
    return payload


def disable_hybrid_retrieval_pipeline(stage_root: str | Path, *, workspace: str | Path) -> dict[str, Any]:
    """Disable Batch 27 hybrid retrieval by deleting only generated stage-root files."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    target = stage_path / HYBRID_RETRIEVAL_TARGET
    deleted: list[str] = []
    if target.exists() and target.is_file():
        target.unlink()
        deleted.append(HYBRID_RETRIEVAL_TARGET)
    return {
        "rendered_artifacts": {
            "status": "disabled",
            "mode": "disable-hybrid-retrieval",
            "root_status": "redacted",
            "fallback": "semantic_retrieval_or_graph_only",
            "deletion_proof": {
                "targets_checked": [HYBRID_RETRIEVAL_TARGET],
                "deleted": deleted,
                "remaining": [HYBRID_RETRIEVAL_TARGET] if target.exists() else [],
            },
            "files": [
                {
                    "target_path": HYBRID_RETRIEVAL_TARGET,
                    "action": "delete_if_present",
                    "write_policy": "stage_generated_file_only",
                    "staged_path": HYBRID_RETRIEVAL_TARGET,
                }
            ],
            "rollback": {"disable_path": f"delete {HYBRID_RETRIEVAL_TARGET}"},
        }
    }


def _validate_hybrid_approval(approval: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(approval, dict):
        return _validation(False, ["hybrid_retrieval_approval:missing"], "hybrid_retrieval_approval")
    errors: list[str] = []
    if approval.get("explicit_approval") is not True:
        errors.append("hybrid_retrieval_approval:explicit_approval")
    allowed_surfaces = {str(item) for item in approval.get("allowed_surfaces", []) if isinstance(item, str)}
    if "hybrid_retrieval_pipeline" not in allowed_surfaces:
        errors.append("hybrid_retrieval_approval:allowed_surfaces:hybrid_retrieval_pipeline")
    if _has_unsafe_text(approval):
        errors.append("hybrid_retrieval_approval:unsafe_text")
    return _validation(not errors, errors, "hybrid_retrieval_approval")


def _validate_query(
    pipeline: dict[str, Any],
    request: dict[str, Any],
    graph: dict[str, Any],
    static_index: dict[str, Any],
    semantic_index: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    validation = (
        pipeline.get("validation")
        if isinstance(pipeline.get("validation"), dict)
        else validate_hybrid_retrieval_pipeline(pipeline)
    )
    if validation.get("ok") is not True:
        errors.append("hybrid_pipeline:invalid")
    if request.get("query") not in {None, "search"}:
        errors.append("query:unknown")
    text = request.get("text")
    if isinstance(text, str) and len(text) > MAX_QUERY_TEXT_LENGTH:
        errors.append("query:text_too_long")
    value = request.get("path_prefixes")
    if value is not None and (
        not isinstance(value, list) or any(safe_relative_path_text(str(item)) != str(item) for item in value)
    ):
        errors.append("query:path_prefixes:invalid")
    if static_index.get("graph_fingerprint") != graph_content_fingerprint(_redacted_dict(graph)):
        errors.append("static_index:stale")
    if semantic_index.get("graph_fingerprint") != graph_content_fingerprint(_redacted_dict(graph)):
        errors.append("semantic_index:stale")
    return errors


def _merge_component(
    candidates: dict[str, dict[str, Any]],
    nodes: list[Any],
    component: str,
    node_index: dict[str, dict[str, Any]],
) -> None:
    for rank, node in enumerate(nodes, start=1):
        if not isinstance(node, dict) or not node.get("id"):
            continue
        node_id = sanitize_graph_text(node.get("id") or "")
        base = node_index.get(node_id, node)
        candidate = candidates.setdefault(node_id, _candidate_from_node(base))
        rank_score = round(1.0 / rank, 4)
        if component == "semantic":
            rank_score = round(rank_score + _float_value(node.get("semantic_score"), 0.0) + _float_value(node.get("rerank_score"), 0.0), 4)
        candidate["component_scores"][component] = rank_score
        if component == "semantic":
            candidate["component_scores"]["local_rerank"] = _float_value(node.get("rerank_score"), 0.0)


def _candidate_from_node(node: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": sanitize_graph_text(node.get("id") or ""),
        "type": sanitize_graph_text(node.get("type") or ""),
        "label": sanitize_graph_text(node.get("label") or "")[:120],
        "status": sanitize_graph_text(node.get("status") or ""),
        "language": sanitize_graph_text(node.get("language") or ""),
        "path": safe_relative_path_text(node.get("path") or ""),
        "confidence": "present_unverified",
        "observation_ids": [
            sanitize_graph_text(item)
            for item in node.get("observation_ids", [])
            if isinstance(item, str)
        ][:3],
        "component_scores": {},
    }


def _explain_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    scores = candidate.get("component_scores", {}) if isinstance(candidate.get("component_scores"), dict) else {}
    static_score = _float_value(scores.get("static"), 0.0)
    semantic_score = _float_value(scores.get("semantic"), 0.0)
    graph_score = _float_value(scores.get("graph"), 0.0)
    local_rerank_score = _float_value(scores.get("local_rerank"), 0.0)
    fused_score = round((static_score * 1.0) + (semantic_score * 1.5) + (graph_score * 0.5), 4)
    sources = sorted(key for key in ["static", "semantic", "graph"] if _float_value(scores.get(key), 0.0) > 0)
    return {
        **candidate,
        "component_scores": {
            "static": round(static_score, 4),
            "semantic": round(semantic_score, 4),
            "graph": round(graph_score, 4),
            "local_rerank": round(local_rerank_score, 4),
            "external_reranker": 0.0,
        },
        "fused_score": fused_score,
        "fusion_explanation": {
            "candidate_sources": sources,
            "ranking": "static + semantic + graph weighted fusion",
            "external_reranker_status": "disabled_no_provider_call",
            "source_backed": True,
            "no_completion_claims_from_match": True,
        },
        "evidence_refs": {
            "observation_ids": candidate.get("observation_ids", []),
            "source_boundary": "graph_static_semantic_and_reranker_gate_redacted_only",
        },
    }


def _packet(
    pipeline: dict[str, Any],
    request: dict[str, Any],
    nodes: list[dict[str, Any]],
    *,
    status: str,
    errors: list[str],
    duration_ms: float,
) -> dict[str, Any]:
    max_results = _positive_int(request.get("max_results"), DEFAULT_MAX_RESULTS)
    max_tokens = _positive_int(request.get("max_tokens"), DEFAULT_MAX_TOKENS)
    omitted = max(0, len(nodes) - max_results)
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "status": status,
        "result_kind": "search",
        "search_backend": "hybrid_retrieval",
        "query_id": _query_id(request),
        "source_boundary": pipeline.get("source_boundary"),
        "generated_view_policy": "hybrid_retrieval_packets_are_orientation_evidence_only",
        "nodes": nodes[:max_results],
        "edges": [],
        "errors": errors,
        "filters": {key: request[key] for key in ["node_types", "path_prefixes"] if key in request},
        "budget": {
            "max_results": max_results,
            "max_tokens": max_tokens,
            "estimated_tokens": 0,
            "truncated": omitted > 0,
            "omitted_count": omitted,
            "truncation_reasons": ["max_results"] if omitted > 0 else [],
        },
        "performance": {"query_ms": round(duration_ms, 3)},
        "provider_policy": pipeline.get("provider_policy", {}),
        "blocked_surfaces": pipeline.get("blocked_surfaces", []),
        "fallback": "semantic_retrieval_or_graph_only",
        "safe_next_action": (
            "Do not make completion claims from hybrid matches alone; treat hits as present_unverified "
            "orientation evidence and read source before edits or owner-facing conclusions."
        ),
    }
    _enforce_budget(packet)
    return packet


def _graph_node_index(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(node.get("id")): node
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and node.get("id")
    }


def _quality_metrics(cases: list[dict[str, Any]]) -> dict[str, float]:
    total_returned = sum(_positive_int(case.get("returned_count"), 0) for case in cases)
    total_hits = sum(_positive_int(case.get("hit_count"), 0) for case in cases)
    false_hits = sum(_positive_int(case.get("false_positive_count"), 0) for case in cases)
    return {
        "precision_at_k": 0.0 if total_returned == 0 else round(total_hits / total_returned, 4),
        "mrr": _average(float(case.get("reciprocal_rank") or 0.0) for case in cases),
        "ndcg_at_k": _average(float(case.get("ndcg") or 0.0) for case in cases),
        "false_positive_rate": 0.0 if total_returned == 0 else round(false_hits / total_returned, 4),
    }


def _failed_thresholds(metrics: dict[str, Any], thresholds: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if _float_value(metrics.get("precision_at_k"), 0.0) < _float_value(thresholds.get("min_precision_at_k"), 0.0):
        failures.append("hybrid_precision_at_k_below_threshold")
    if _float_value(metrics.get("mrr"), 0.0) < _float_value(thresholds.get("min_mrr"), 0.0):
        failures.append("hybrid_mrr_below_threshold")
    if _float_value(metrics.get("ndcg_at_k"), 0.0) < _float_value(thresholds.get("min_ndcg_at_k"), 0.0):
        failures.append("hybrid_ndcg_at_k_below_threshold")
    if _float_value(metrics.get("false_positive_rate"), 0.0) > _float_value(
        thresholds.get("max_false_positive_rate"),
        1.0,
    ):
        failures.append("hybrid_false_positive_rate_above_threshold")
    if _float_value(metrics.get("max_query_ms"), 0.0) > _float_value(thresholds.get("max_query_ms"), 250.0):
        failures.append("hybrid_max_query_ms_above_threshold")
    if _float_value(metrics.get("max_payload_tokens"), 0.0) > _float_value(thresholds.get("max_payload_tokens"), 1200.0):
        failures.append("hybrid_max_payload_tokens_above_threshold")
    return failures


def _default_thresholds(pipeline: dict[str, Any]) -> dict[str, Any]:
    policy = pipeline.get("eval_policy", {}) if isinstance(pipeline.get("eval_policy"), dict) else {}
    return {
        "min_precision_at_k": float(policy.get("min_precision_at_k", 0.0)),
        "min_mrr": float(policy.get("min_mrr", 0.0)),
        "min_ndcg_at_k": float(policy.get("min_ndcg_at_k", 0.0)),
        "max_false_positive_rate": float(policy.get("max_false_positive_rate", 1.0)),
        "max_query_ms": _positive_int(policy.get("max_query_ms"), 250),
        "max_payload_tokens": _positive_int(policy.get("max_payload_tokens"), 1200),
    }


def _artifact_fingerprint(artifact: dict[str, Any], *, record_key: str) -> str:
    payload = {
        "graph_fingerprint": artifact.get("graph_fingerprint"),
        "record_count": len(artifact.get(record_key, [])) if isinstance(artifact.get(record_key), list) else 0,
        "approval_boundary": artifact.get("approval_boundary"),
        "artifact_kind": artifact.get("artifact_kind"),
    }
    return "sha256:" + hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def _ndcg(result_ids: list[str], expected_ids: list[str]) -> float:
    if not expected_ids:
        return 1.0
    dcg = 0.0
    for index, result_id in enumerate(result_ids, start=1):
        if result_id in expected_ids:
            import math

            dcg += 1.0 / math.log2(index + 1)
    ideal_hits = min(len(expected_ids), len(result_ids))
    if ideal_hits == 0:
        return 0.0
    import math

    idcg = sum(1.0 / math.log2(index + 1) for index in range(1, ideal_hits + 1))
    return 0.0 if idcg == 0 else round(dcg / idcg, 4)


def _first_rank(result_ids: list[str], expected_ids: list[str]) -> int:
    for index, node_id in enumerate(result_ids, start=1):
        if node_id in expected_ids:
            return index
    return 0


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
        return any(_has_unsafe_text(key) or _has_unsafe_text(nested) for key, nested in value.items())
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
    return _validation(not errors, sorted(set(errors)), "hybrid_retrieval_pipeline")


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


def _query_id(request: dict[str, Any]) -> str:
    return "hybrid-query:" + hashlib.sha256(json.dumps(request, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def _estimated_tokens(payload: Any) -> int:
    return max(1, len(json.dumps(payload, sort_keys=True, default=str)) // 4)


def _enforce_budget(packet: dict[str, Any]) -> None:
    budget = packet["budget"]
    max_tokens = _positive_int(budget.get("max_tokens"), DEFAULT_MAX_TOKENS)
    while _estimated_tokens(packet) > max_tokens and packet.get("nodes"):
        packet["nodes"].pop()
        budget["omitted_count"] = int(budget.get("omitted_count") or 0) + 1
        budget["truncated"] = True
        budget["truncation_reasons"] = sorted(set(list(budget.get("truncation_reasons") or []) + ["token_budget"]))
    budget["estimated_tokens"] = _estimated_tokens(packet)
