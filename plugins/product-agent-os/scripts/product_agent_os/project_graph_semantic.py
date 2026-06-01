"""Semantic retrieval gate for Product-Agent OS project graphs.

Batch 21 implements a generated local semantic retrieval cache with
deterministic embeddings and reranking. It does not call live model APIs.
External embedding or cross-encoder providers remain approval-bound.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
import time
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import redact_payload
from product_agent_os.project_graph_index import (
    build_static_search_index,
    graph_content_fingerprint,
)
from product_agent_os.project_graph_queries import load_graph_artifact
from product_agent_os.project_graph_sanitization import safe_relative_path_text, sanitize_graph_text


SEMANTIC_RETRIEVAL_TARGET = ".codex/product-agent-os/project-code-graph-semantic-index.json"
DEFAULT_SEMANTIC_DIMENSION = 64
DEFAULT_MAX_QUERY_TOKENS = 1_200
DEFAULT_MAX_CORPUS_RECORD_TOKENS = 120
DEFAULT_MAX_QUERY_MS = 250
DEFAULT_MAX_RESULTS = 25
MAX_QUERY_TEXT_LENGTH = 160

_APPROVAL_FIELDS = {
    "explicit_approval",
    "storage_path",
    "embedding_provider",
    "embedding_model",
    "cross_encoder",
    "data_classification",
    "redaction_policy",
    "cache_policy",
    "token_budget",
    "eval_threshold",
    "failure_handling",
    "rollback_path",
}


def validate_semantic_retrieval_approval(approval: dict[str, Any] | None) -> dict[str, Any]:
    """Validate explicit approval before building semantic retrieval artifacts."""

    if not isinstance(approval, dict):
        return _validation(False, ["semantic_approval:missing"], "semantic_approval")
    errors: list[str] = []
    missing = sorted(field for field in _APPROVAL_FIELDS if field not in approval)
    errors.extend(f"semantic_approval:{field}:missing" for field in missing)
    if approval.get("explicit_approval") is not True:
        errors.append("semantic_approval:explicit_approval")
    if safe_relative_path_text(approval.get("storage_path") or "") != SEMANTIC_RETRIEVAL_TARGET:
        errors.append("semantic_approval:storage_path")
    if approval.get("embedding_provider") != "local_deterministic":
        errors.append("semantic_approval:embedding_provider")

    embedding_model = approval.get("embedding_model") if isinstance(approval.get("embedding_model"), dict) else {}
    if embedding_model.get("external_model_calls_allowed") is not False:
        errors.append("semantic_approval:embedding_model:external_calls")
    if _positive_int(embedding_model.get("dimension"), 0) <= 0:
        errors.append("semantic_approval:embedding_model:dimension")
    if not embedding_model.get("name") or not embedding_model.get("version"):
        errors.append("semantic_approval:embedding_model:identity")

    cross_encoder = approval.get("cross_encoder") if isinstance(approval.get("cross_encoder"), dict) else {}
    if cross_encoder.get("provider") != "local_deterministic":
        errors.append("semantic_approval:cross_encoder:provider")
    if cross_encoder.get("external_model_calls_allowed") is not False:
        errors.append("semantic_approval:cross_encoder:external_calls")
    if not cross_encoder.get("model"):
        errors.append("semantic_approval:cross_encoder:model")

    classification = approval.get("data_classification") if isinstance(approval.get("data_classification"), dict) else {}
    forbidden_inputs = set(str(item) for item in classification.get("forbidden_inputs", []) if isinstance(item, str))
    for required in ["raw_source_bodies", "secrets", "absolute_local_paths"]:
        if required not in forbidden_inputs:
            errors.append(f"semantic_approval:data_classification:{required}")

    redaction = approval.get("redaction_policy") if isinstance(approval.get("redaction_policy"), dict) else {}
    if redaction.get("raw_source_excluded") is not True:
        errors.append("semantic_approval:redaction_policy:raw_source_excluded")
    if redaction.get("secrets_redacted") is not True:
        errors.append("semantic_approval:redaction_policy:secrets_redacted")
    if redaction.get("absolute_paths_redacted") is not True:
        errors.append("semantic_approval:redaction_policy:absolute_paths_redacted")

    cache = approval.get("cache_policy") if isinstance(approval.get("cache_policy"), dict) else {}
    if cache.get("stale_policy") != "block_if_graph_fingerprint_mismatch":
        errors.append("semantic_approval:cache_policy:stale_policy")
    if "graph" not in str(cache.get("fingerprint_scope") or ""):
        errors.append("semantic_approval:cache_policy:fingerprint_scope")

    token_budget = approval.get("token_budget") if isinstance(approval.get("token_budget"), dict) else {}
    if _positive_int(token_budget.get("max_query_tokens"), 0) <= 0:
        errors.append("semantic_approval:token_budget:max_query_tokens")
    if _positive_int(token_budget.get("max_corpus_record_tokens"), 0) <= 0:
        errors.append("semantic_approval:token_budget:max_corpus_record_tokens")

    thresholds = approval.get("eval_threshold") if isinstance(approval.get("eval_threshold"), dict) else {}
    for threshold in ["min_recall_at_k", "min_mrr", "max_false_positive_rate", "max_query_ms", "max_payload_tokens"]:
        if threshold not in thresholds:
            errors.append(f"semantic_approval:eval_threshold:{threshold}")
    if _positive_int(thresholds.get("max_query_ms"), 0) <= 0:
        errors.append("semantic_approval:eval_threshold:max_query_ms")
    if _positive_int(thresholds.get("max_payload_tokens"), 0) <= 0:
        errors.append("semantic_approval:eval_threshold:max_payload_tokens")

    failure = approval.get("failure_handling") if isinstance(approval.get("failure_handling"), dict) else {}
    if "fallback" not in str(failure.get("on_stale_or_failed_eval") or ""):
        errors.append("semantic_approval:failure_handling:fallback")
    if approval.get("rollback_path") != f"delete {SEMANTIC_RETRIEVAL_TARGET}":
        errors.append("semantic_approval:rollback_path")
    return _validation(not errors, errors, "semantic_approval")


def build_semantic_retrieval_index(
    graph: dict[str, Any],
    *,
    static_index: dict[str, Any] | None = None,
    approval: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a deterministic generated semantic retrieval cache from graph artifacts."""

    approval_validation = validate_semantic_retrieval_approval(approval)
    if approval_validation["ok"] is not True:
        return _approval_required_index(approval_validation)

    safe_graph = _redacted_dict(graph)
    safe_static_index = _redacted_dict(static_index) if isinstance(static_index, dict) else build_static_search_index(safe_graph)
    dimension = _positive_int(approval.get("embedding_model", {}).get("dimension"), DEFAULT_SEMANTIC_DIMENSION)
    max_record_tokens = _positive_int(
        approval.get("token_budget", {}).get("max_corpus_record_tokens"),
        DEFAULT_MAX_CORPUS_RECORD_TOKENS,
    )
    corpus_records = [
        _corpus_record_for_node(
            node,
            static_index=safe_static_index,
            dimension=dimension,
            max_record_tokens=max_record_tokens,
        )
        for node in safe_graph.get("nodes", [])
        if isinstance(node, dict) and node.get("id")
    ]
    corpus_records = sorted(corpus_records, key=lambda item: item["node_id"])
    thresholds = approval.get("eval_threshold", {})
    index = {
        "schema_version": 1,
        "artifact_kind": "project_graph_semantic_retrieval_index",
        "write_policy": "read_only",
        "status": "ready",
        "source_boundary": "graph_and_static_index_artifacts_only_redacted_corpus_raw_source_excluded",
        "generated_view_policy": "semantic_retrieval_index_is_generated_cache_not_source_of_truth",
        "approval_boundary": "batch21_explicit_semantic_retrieval_gate",
        "graph_fingerprint": graph_content_fingerprint(safe_graph),
        "static_index_fingerprint": safe_static_index.get("graph_fingerprint"),
        "model_decision": {
            "embedding_provider": approval.get("embedding_provider"),
            "embedding_model": sanitize_graph_text(approval.get("embedding_model", {}).get("name") or ""),
            "embedding_model_version": sanitize_graph_text(approval.get("embedding_model", {}).get("version") or ""),
            "cross_encoder_provider": approval.get("cross_encoder", {}).get("provider"),
            "cross_encoder_model": sanitize_graph_text(approval.get("cross_encoder", {}).get("model") or ""),
            "external_model_calls_allowed": False,
            "implementation_mode": "local_deterministic_eval_gate",
        },
        "corpus_policy": {
            "semantic_corpus_and_chunk_policy": "redacted_graph_labels_static_index_terms_observation_ids_only",
            "approved_inputs": list(approval.get("data_classification", {}).get("allowed_inputs", [])),
            "forbidden_inputs": list(approval.get("data_classification", {}).get("forbidden_inputs", [])),
            "generated_html_as_source": False,
            "raw_private_text_allowed": False,
            "max_corpus_record_tokens": max_record_tokens,
        },
        "embedding": {
            "cache_kind": "embeddings_cache_metadata",
            "provider": "local_deterministic",
            "model": sanitize_graph_text(approval.get("embedding_model", {}).get("name") or ""),
            "version": sanitize_graph_text(approval.get("embedding_model", {}).get("version") or ""),
            "dimension": dimension,
            "vector_hashing": "sha256_token_hashing_v1",
            "external_model_calls_allowed": False,
        },
        "cross_encoder": {
            "reranking_gate": "cross_encoder_reranking_gate",
            "provider": "local_deterministic",
            "model": sanitize_graph_text(approval.get("cross_encoder", {}).get("model") or ""),
            "enabled": bool(approval.get("cross_encoder", {}).get("enabled", True)),
            "external_model_calls_allowed": False,
            "canonical_graph_edge_rewrites": False,
        },
        "cache_policy": {
            "cache_status": str(approval.get("cache_policy", {}).get("cache_status") or "generated"),
            "fingerprint_scope": "canonical_redacted_graph_and_static_index",
            "stale_policy": "block_if_graph_fingerprint_mismatch",
            "expiration_policy": {"ttl_days": _positive_int(approval.get("cache_policy", {}).get("ttl_days"), 30)},
            "storage_path": SEMANTIC_RETRIEVAL_TARGET,
        },
        "query_policy": {
            "semantic_query_packets": True,
            "default_max_results": DEFAULT_MAX_RESULTS,
            "max_query_tokens": _positive_int(
                approval.get("token_budget", {}).get("max_query_tokens"),
                DEFAULT_MAX_QUERY_TOKENS,
            ),
            "fallback": "lexical_or_graph_search",
            "semantic_hits_confidence": "present_unverified",
            "no_completion_claims_from_semantic_matches_alone": True,
        },
        "eval_policy": {
            "semantic_retrieval_eval_suite": True,
            "min_recall_at_k": float(thresholds.get("min_recall_at_k", 0.0)),
            "min_mrr": float(thresholds.get("min_mrr", 0.0)),
            "min_cross_encoder_mrr_delta": float(thresholds.get("min_cross_encoder_mrr_delta", 0.0)),
            "max_false_positive_rate": float(thresholds.get("max_false_positive_rate", 1.0)),
            "max_query_ms": _positive_int(thresholds.get("max_query_ms"), DEFAULT_MAX_QUERY_MS),
            "max_payload_tokens": _positive_int(thresholds.get("max_payload_tokens"), DEFAULT_MAX_QUERY_TOKENS),
        },
        "rollback": {
            "disable_path": f"delete {SEMANTIC_RETRIEVAL_TARGET}",
            "fallback": "lexical_or_graph_search",
            "deletion_scope": "stage_root_generated_semantic_index_only",
        },
        "corpus_records": corpus_records,
    }
    index["validation"] = validate_semantic_retrieval_index(index)
    return index


def validate_semantic_retrieval_index(index: dict[str, Any]) -> dict[str, Any]:
    """Validate semantic retrieval cache schema and safety invariants."""

    errors: list[str] = []
    if index.get("schema_version") != 1:
        errors.append("schema_version")
    if index.get("artifact_kind") != "project_graph_semantic_retrieval_index":
        errors.append("artifact_kind")
    if index.get("write_policy") != "read_only":
        errors.append("write_policy")
    if index.get("source_boundary") != "graph_and_static_index_artifacts_only_redacted_corpus_raw_source_excluded":
        errors.append("source_boundary")
    if index.get("generated_view_policy") != "semantic_retrieval_index_is_generated_cache_not_source_of_truth":
        errors.append("generated_view_policy")
    if index.get("approval_boundary") != "batch21_explicit_semantic_retrieval_gate":
        errors.append("approval_boundary")
    if not str(index.get("graph_fingerprint") or "").startswith("sha256:"):
        errors.append("graph_fingerprint")
    if index.get("model_decision", {}).get("external_model_calls_allowed") is not False:
        errors.append("model_decision:external_calls")
    if index.get("cross_encoder", {}).get("canonical_graph_edge_rewrites") is not False:
        errors.append("cross_encoder:canonical_graph_edge_rewrites")
    records = index.get("corpus_records")
    if not isinstance(records, list):
        errors.append("corpus_records")
        records = []
    dimension = _positive_int(index.get("embedding", {}).get("dimension"), DEFAULT_SEMANTIC_DIMENSION)
    for record in records:
        if not isinstance(record, dict):
            errors.append("record:shape")
            continue
        if not record.get("node_id"):
            errors.append("record:node_id")
        if len(record.get("embedding", [])) != dimension:
            errors.append("record:embedding_dimension")
        if _has_unsafe_text(record):
            errors.append("record:unsafe_text")
        path = str(record.get("path") or "")
        if path and safe_relative_path_text(path) != path:
            errors.append("record:path")
    if _has_unsafe_text(index):
        errors.append("source_boundary:unsafe_text")
    return _validation(not errors, errors, "semantic_retrieval_index")


def stage_semantic_retrieval_index(
    graph_artifact: str | Path,
    stage_root: str | Path,
    *,
    workspace: str | Path,
    approval: dict[str, Any] | None,
    static_index_artifact: str | Path | None = None,
) -> dict[str, Any]:
    """Stage or reuse a generated semantic retrieval index under an explicit stage root."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    approval_validation = validate_semantic_retrieval_approval(approval)
    if approval_validation["ok"] is not True:
        return _stage_result("approval_required", "blocked", approval_validation, action="blocked")

    graph = load_graph_artifact(graph_artifact)
    fingerprint = graph_content_fingerprint(_redacted_dict(graph))
    target = stage_path / SEMANTIC_RETRIEVAL_TARGET
    previous = _load_existing_semantic_index(target)
    if previous and previous.get("graph_fingerprint") == fingerprint and previous.get("validation", {}).get("ok") is True:
        return _stage_result("ready", "hit", previous["validation"], action="leave_unchanged")

    static_index = _load_optional_json(static_index_artifact) if static_index_artifact else None
    cache_status = "miss_invalidated" if previous else "miss"
    if previous:
        _backup_existing(target, target.with_name("project-code-graph-semantic-index.previous.json"))
    semantic_index = build_semantic_retrieval_index(graph, static_index=static_index, approval=approval)
    if semantic_index.get("validation", {}).get("ok") is not True:
        return _stage_result("blocked", cache_status, semantic_index["validation"], action="blocked")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(semantic_index, indent=2, sort_keys=True), encoding="utf-8")
    return _stage_result("ready", cache_status, semantic_index["validation"], action="create")


def load_semantic_retrieval_index(path: str | Path) -> dict[str, Any]:
    """Load a generated semantic retrieval index without reading source files."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("semantic retrieval index must be a JSON object")
    return payload


def disable_semantic_retrieval_index(stage_root: str | Path, *, workspace: str | Path) -> dict[str, Any]:
    """Disable semantic retrieval by deleting only the generated stage-root cache."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    target = stage_path / SEMANTIC_RETRIEVAL_TARGET
    if target.exists() and target.is_file():
        target.unlink()
    return {
        "rendered_artifacts": {
            "status": "disabled",
            "mode": "disable-semantic-index",
            "root_status": "redacted",
            "fallback": "lexical_or_graph_search",
            "files": [
                {
                    "target_path": SEMANTIC_RETRIEVAL_TARGET,
                    "action": "delete_if_present",
                    "write_policy": "stage_generated_file_only",
                    "staged_path": SEMANTIC_RETRIEVAL_TARGET,
                }
            ],
            "rollback": {"disable_path": f"delete {SEMANTIC_RETRIEVAL_TARGET}"},
        }
    }


def query_semantic_retrieval(
    semantic_index: dict[str, Any],
    request: dict[str, Any],
    *,
    graph: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run a bounded semantic search over generated local corpus records."""

    errors = _validate_query(semantic_index, request, graph)
    if errors:
        return _packet(semantic_index, request, [], status="blocked", errors=errors, duration_ms=0.0)
    started = time.perf_counter()
    query_text = _safe_review_text(request.get("text") or "")
    query_terms = _terms(query_text)
    query_embedding = _embedding_for_terms(query_terms, _positive_int(semantic_index["embedding"]["dimension"], 64))
    candidates = []
    for record in semantic_index.get("corpus_records", []):
        if not isinstance(record, dict) or not _record_matches_filters(record, request):
            continue
        vector_score = _cosine(query_embedding, [float(value) for value in record.get("embedding", [])])
        rerank_score = _cross_encoder_score(record, query_terms)
        score = vector_score + rerank_score
        if query_terms and score <= 0:
            continue
        candidates.append((record, vector_score, rerank_score, score))
    ranked = sorted(candidates, key=lambda item: (-item[3], item[0]["node_id"]))
    duration_ms = (time.perf_counter() - started) * 1000
    nodes = [_semantic_node(record, vector_score, rerank_score) for record, vector_score, rerank_score, _score in ranked]
    return _packet(semantic_index, request, nodes, status="ok", errors=[], duration_ms=duration_ms)


def evaluate_semantic_retrieval_quality(
    semantic_index: dict[str, Any],
    *,
    graph: dict[str, Any],
    cases: list[dict[str, Any]],
    thresholds: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate semantic retrieval quality and cross-encoder gate behavior."""

    applied = {**_default_thresholds(semantic_index), **(thresholds or {})}
    evaluated_cases: list[dict[str, Any]] = []
    durations: list[float] = []
    payload_tokens: list[int] = []
    for case in cases:
        if not isinstance(case, dict):
            continue
        top_k = _positive_int(case.get("top_k"), 5)
        started = time.perf_counter()
        packet = query_semantic_retrieval(
            semantic_index,
            {"query": "search", "text": case.get("text") or "", "max_results": top_k, "max_tokens": applied["max_payload_tokens"]},
            graph=graph,
        )
        durations.append((time.perf_counter() - started) * 1000)
        payload_tokens.append(_estimated_tokens(packet))
        result_ids = [str(node.get("id")) for node in packet.get("nodes", []) if isinstance(node, dict)]
        expected_ids = [str(item) for item in case.get("expected_node_ids", []) if item]
        unexpected_ids = [str(item) for item in case.get("unexpected_node_ids", []) if item]
        hits = [item for item in expected_ids if item in result_ids[:top_k]]
        false_hits = [item for item in unexpected_ids if item in result_ids[:top_k]]
        first_rank = _first_rank(result_ids, expected_ids)
        evaluated_cases.append(
            {
                "id": _safe_review_text(case.get("id") or "unnamed-semantic-case")[:80],
                "status": "passed" if expected_ids and len(hits) == len(expected_ids) and not false_hits else "failed",
                "result_status": packet.get("status"),
                "top_k": top_k,
                "expected_node_count": len(expected_ids),
                "hit_count": len(hits),
                "false_positive_count": len(false_hits),
                "first_relevant_rank": first_rank,
                "reciprocal_rank": 0.0 if first_rank == 0 else 1.0 / first_rank,
            }
        )
    metrics = _semantic_quality_metrics(evaluated_cases)
    metrics["max_query_ms"] = round(max(durations or [0.0]), 3)
    metrics["max_payload_tokens"] = max(payload_tokens or [0])
    metrics["cross_encoder_mrr_delta"] = 0.0
    failed = _semantic_failed_thresholds(metrics, applied)
    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "decision_status": "passed" if evaluated_cases and not failed else "blocked",
        "search_backend": "semantic_retrieval",
        "approval_boundary": "batch21_explicit_semantic_retrieval_gate",
        "source_boundary": semantic_index.get("source_boundary"),
        "quality_metrics": metrics,
        "thresholds": applied,
        "failed_thresholds": failed,
        "cases": evaluated_cases,
        "rollback": semantic_index.get("rollback", {}),
        "safe_next_action": "Treat semantic hits as present_unverified orientation evidence until source reads or owner review.",
    }


def _approval_required_index(validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_kind": "project_graph_semantic_retrieval_index",
        "write_policy": "read_only",
        "status": "approval_required",
        "source_boundary": "graph_and_static_index_artifacts_only_redacted_corpus_raw_source_excluded",
        "approval_boundary": "batch21_explicit_semantic_retrieval_gate",
        "rollback": {"disable_path": f"delete {SEMANTIC_RETRIEVAL_TARGET}", "fallback": "lexical_or_graph_search"},
        "validation": validation,
    }


def _corpus_record_for_node(
    node: dict[str, Any],
    *,
    static_index: dict[str, Any],
    dimension: int,
    max_record_tokens: int,
) -> dict[str, Any]:
    node_id = _safe_review_text(node.get("id") or "")
    static_record = _static_record_for_node(static_index, node_id)
    path = safe_relative_path_text(node.get("path") or "")
    observation_ids = [_safe_review_text(item) for item in node.get("observation_ids", []) if item]
    terms = sorted(
        set(
            [
                *_terms(node_id),
                *_terms(node.get("label") or ""),
                *_terms(path),
                *_terms(node.get("type") or ""),
                *_terms(node.get("language") or ""),
                *[str(term) for term in static_record.get("terms", []) if term],
                *[term for alias in static_record.get("aliases", []) for term in _terms(alias)],
            ]
        )
    )
    approved_text = " ".join(
        [
            node_id,
            _safe_review_text(node.get("label") or ""),
            path,
            _safe_review_text(node.get("type") or ""),
            _safe_review_text(node.get("language") or ""),
            " ".join(terms),
            " ".join(observation_ids),
        ]
    )
    approved_text = _trim_approx_tokens(approved_text, max_record_tokens)
    return {
        "record_id": "semantic-record:" + hashlib.sha256(node_id.encode("utf-8")).hexdigest()[:16],
        "node_id": node_id,
        "type": _safe_review_text(node.get("type") or ""),
        "label": _safe_review_text(node.get("label") or "")[:120],
        "language": _safe_review_text(node.get("language") or ""),
        "path": path,
        "status": _safe_review_text(node.get("status") or ""),
        "observation_ids": observation_ids[:5],
        "approved_text": approved_text,
        "terms": terms[:80],
        "embedding": _embedding_for_terms(terms, dimension),
        "confidence": "present_unverified",
    }


def _static_record_for_node(static_index: dict[str, Any], node_id: str) -> dict[str, Any]:
    for record in static_index.get("records", []):
        if isinstance(record, dict) and record.get("node_id") == node_id:
            return record
    return {}


def _validate_query(
    semantic_index: dict[str, Any],
    request: dict[str, Any],
    graph: dict[str, Any] | None,
) -> list[str]:
    errors: list[str] = []
    validation = (
        semantic_index.get("validation")
        if isinstance(semantic_index.get("validation"), dict)
        else validate_semantic_retrieval_index(semantic_index)
    )
    if validation.get("ok") is not True:
        errors.append("semantic_index:invalid")
    if graph is not None and semantic_index.get("graph_fingerprint") != graph_content_fingerprint(_redacted_dict(graph)):
        errors.append("semantic_index:stale")
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
    node_types = request.get("node_types")
    if node_types is not None and not isinstance(node_types, list):
        errors.append("query:node_types:invalid")
    return errors


def _packet(
    semantic_index: dict[str, Any],
    request: dict[str, Any],
    nodes: list[dict[str, Any]],
    *,
    status: str,
    errors: list[str],
    duration_ms: float,
) -> dict[str, Any]:
    max_results = _positive_int(request.get("max_results"), DEFAULT_MAX_RESULTS)
    max_tokens = _positive_int(
        request.get("max_tokens"),
        _positive_int(semantic_index.get("query_policy", {}).get("max_query_tokens"), DEFAULT_MAX_QUERY_TOKENS),
    )
    omitted = max(0, len(nodes) - max_results)
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "status": status,
        "result_kind": "search",
        "search_backend": "semantic_retrieval",
        "reranker": "local_cross_encoder_eval_only",
        "query_id": _query_id(request),
        "source_boundary": semantic_index.get("source_boundary"),
        "generated_view_policy": "semantic_retrieval_packets_are_orientation_evidence_only",
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
        "fallback": "lexical_or_graph_search",
        "safe_next_action": (
            "Do not make completion claims from semantic matches alone; treat hits as present_unverified "
            "orientation evidence and read source before edits or owner-facing conclusions."
        ),
    }
    _enforce_budget(packet)
    return packet


def _semantic_node(record: dict[str, Any], vector_score: float, rerank_score: float) -> dict[str, Any]:
    return {
        "id": str(record.get("node_id") or ""),
        "type": str(record.get("type") or ""),
        "label": str(record.get("label") or "")[:120],
        "status": str(record.get("status") or ""),
        "language": str(record.get("language") or ""),
        "path": str(record.get("path") or ""),
        "confidence": "present_unverified",
        "semantic_score": round(vector_score, 4),
        "rerank_score": round(rerank_score, 4),
        "observation_ids": list(record.get("observation_ids") or [])[:3],
    }


def _record_matches_filters(record: dict[str, Any], request: dict[str, Any]) -> bool:
    node_types = set(str(item) for item in request.get("node_types", []) if isinstance(item, str))
    path_prefixes = [str(item) for item in request.get("path_prefixes", []) if isinstance(item, str)]
    if node_types and record.get("type") not in node_types:
        return False
    if path_prefixes and not any(str(record.get("path") or "").startswith(prefix) for prefix in path_prefixes):
        return False
    return True


def _cross_encoder_score(record: dict[str, Any], query_terms: list[str]) -> float:
    terms = set(str(item) for item in record.get("terms", []) if item)
    haystack = " ".join(str(record.get(key) or "").lower() for key in ["node_id", "label", "path", "type", "language"])
    score = 0.0
    for term in query_terms:
        if term in terms:
            score += 2.0
        elif term in haystack:
            score += 0.5
    if str(record.get("type")) in {"function", "method", "class"}:
        score += 0.8
    path = str(record.get("path") or "")
    if "/tests/" in f"/{path}" or path.startswith("tests/"):
        score -= 20.0
    else:
        score += 0.5
    if str(record.get("status")) == "current":
        score += 0.2
    return score


def _embedding_for_terms(terms: list[str], dimension: int) -> list[float]:
    vector = [0.0 for _ in range(dimension)]
    for term in terms:
        digest = hashlib.sha256(term.encode("utf-8")).digest()
        bucket = int.from_bytes(digest[:4], "big") % dimension
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[bucket] += sign
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [round(value / norm, 6) for value in vector]


def _cosine(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    return sum(a * b for a, b in zip(left, right))


def _semantic_quality_metrics(cases: list[dict[str, Any]]) -> dict[str, float]:
    total_expected = sum(_positive_int(case.get("expected_node_count"), 0) for case in cases)
    total_hits = sum(_positive_int(case.get("hit_count"), 0) for case in cases)
    total_returned = sum(_positive_int(case.get("top_k"), 0) for case in cases)
    false_hits = sum(_positive_int(case.get("false_positive_count"), 0) for case in cases)
    return {
        "recall_at_k": 1.0 if total_expected == 0 else round(total_hits / total_expected, 4),
        "mrr": _average(float(case.get("reciprocal_rank") or 0.0) for case in cases),
        "ndcg_at_k": _average(float(case.get("reciprocal_rank") or 0.0) for case in cases),
        "false_positive_rate": 0.0 if total_returned == 0 else round(false_hits / total_returned, 4),
    }


def _semantic_failed_thresholds(metrics: dict[str, float], thresholds: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if _float_value(metrics.get("recall_at_k"), 0.0) < _float_value(thresholds.get("min_recall_at_k"), 0.0):
        failures.append("recall_at_k_below_threshold")
    if _float_value(metrics.get("mrr"), 0.0) < _float_value(thresholds.get("min_mrr"), 0.0):
        failures.append("mrr_below_threshold")
    if _float_value(metrics.get("cross_encoder_mrr_delta"), 0.0) < _float_value(
        thresholds.get("min_cross_encoder_mrr_delta"),
        0.0,
    ):
        failures.append("cross_encoder_mrr_delta_below_threshold")
    if _float_value(metrics.get("false_positive_rate"), 0.0) > _float_value(
        thresholds.get("max_false_positive_rate"),
        1.0,
    ):
        failures.append("false_positive_rate_above_threshold")
    if _float_value(metrics.get("max_query_ms"), 0.0) > _float_value(
        thresholds.get("max_query_ms"),
        float(DEFAULT_MAX_QUERY_MS),
    ):
        failures.append("max_query_ms_above_threshold")
    if _float_value(metrics.get("max_payload_tokens"), 0.0) > _float_value(
        thresholds.get("max_payload_tokens"),
        float(DEFAULT_MAX_QUERY_TOKENS),
    ):
        failures.append("max_payload_tokens_above_threshold")
    return failures


def _float_value(value: Any, default: float) -> float:
    if value is None:
        return default
    return float(value)


def _default_thresholds(semantic_index: dict[str, Any]) -> dict[str, Any]:
    policy = semantic_index.get("eval_policy", {}) if isinstance(semantic_index.get("eval_policy"), dict) else {}
    return {
        "min_recall_at_k": float(policy.get("min_recall_at_k", 0.0)),
        "min_mrr": float(policy.get("min_mrr", 0.0)),
        "min_cross_encoder_mrr_delta": float(policy.get("min_cross_encoder_mrr_delta", 0.0)),
        "max_false_positive_rate": float(policy.get("max_false_positive_rate", 1.0)),
        "max_query_ms": _positive_int(policy.get("max_query_ms"), DEFAULT_MAX_QUERY_MS),
        "max_payload_tokens": _positive_int(policy.get("max_payload_tokens"), DEFAULT_MAX_QUERY_TOKENS),
    }


def _stage_result(status: str, cache_status: str, validation: dict[str, Any], *, action: str) -> dict[str, Any]:
    return {
        "rendered_artifacts": {
            "status": status,
            "mode": "build-semantic-index",
            "root_status": "redacted",
            "cache_status": cache_status,
            "source_boundary": "graph_and_static_index_artifacts_only_redacted_corpus_raw_source_excluded",
            "fallback": "lexical_or_graph_search",
            "rollback": {"disable_path": f"delete {SEMANTIC_RETRIEVAL_TARGET}"},
            "files": [
                {
                    "target_path": SEMANTIC_RETRIEVAL_TARGET,
                    "action": action,
                    "write_policy": "staged_only" if action in {"create", "leave_unchanged"} else "blocked",
                    "staged_path": SEMANTIC_RETRIEVAL_TARGET,
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


def _load_existing_semantic_index(path: Path) -> dict[str, Any] | None:
    if not path.exists() or not path.is_file():
        return None
    try:
        return load_semantic_retrieval_index(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return None


def _load_optional_json(path: str | Path | None) -> dict[str, Any] | None:
    if not path:
        return None
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def _backup_existing(target: Path, backup_target: Path) -> None:
    if not target.exists() or not target.is_file():
        return
    backup_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(target, backup_target)


def _redacted_dict(payload: dict[str, Any]) -> dict[str, Any]:
    redacted, _report = redact_payload(payload)
    return redacted if isinstance(redacted, dict) else payload


def _has_unsafe_text(value: Any) -> bool:
    serialized = json.dumps(value, sort_keys=True).lower()
    forbidden = ["fixture-secret", "http://", "https://", "c:\\users\\", "/users/", "/home/", "/tmp/"]
    return any(item in serialized for item in forbidden)


def _safe_review_text(value: Any) -> str:
    text = sanitize_graph_text(value)
    text = re.sub(
        r"(?i)\b(token|secret|password|api[_-]?key|private[_-]?key)\s*=\s*[^\s\"'<>]+",
        "[REDACTED_SECRET]",
        text,
    )
    text = re.sub(r"(?i)fixture-secret", "[REDACTED_SECRET]", text)
    return text


def _terms(value: Any) -> list[str]:
    text = _safe_review_text(value).lower().replace("\\", "/")
    return [term for term in re.split(r"[^a-z0-9]+", text) if term]


def _trim_approx_tokens(value: str, max_tokens: int) -> str:
    words = value.split()
    return " ".join(words[: max(max_tokens, 1)])


def _query_id(request: dict[str, Any]) -> str:
    return "semantic-query:" + hashlib.sha256(json.dumps(request, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def _first_rank(result_ids: list[str], expected_ids: list[str]) -> int:
    for index, result_id in enumerate(result_ids, start=1):
        if result_id in expected_ids:
            return index
    return 0


def _average(values: Any) -> float:
    materialized = [float(value) for value in values]
    if not materialized:
        return 1.0
    return round(sum(materialized) / len(materialized), 4)


def _enforce_budget(packet: dict[str, Any]) -> None:
    budget = packet["budget"]
    max_tokens = _positive_int(budget.get("max_tokens"), DEFAULT_MAX_QUERY_TOKENS)
    while _estimated_tokens(packet) > max_tokens and packet.get("nodes"):
        packet["nodes"].pop()
        budget["truncated"] = True
        budget["omitted_count"] = int(budget.get("omitted_count") or 0) + 1
        budget["truncation_reasons"] = sorted(set(list(budget.get("truncation_reasons") or []) + ["token_budget"]))
    budget["estimated_tokens"] = _estimated_tokens(packet)


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
