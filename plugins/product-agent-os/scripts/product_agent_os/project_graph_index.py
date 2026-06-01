"""Offline static search index for Product-Agent OS project graphs."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any

from product_agent_os.project_graph_sanitization import safe_relative_path_text, sanitize_graph_text


STATIC_SEARCH_INDEX_TARGET = ".codex/product-agent-os/project-code-graph-search-index.json"
DEFAULT_MAX_RESULTS = 25
DEFAULT_MAX_TOKENS = 4_000
MAX_QUERY_TEXT_LENGTH = 120


def graph_content_fingerprint(graph: dict[str, Any]) -> str:
    """Return a stable fingerprint for the redacted graph artifact payload."""

    return "sha256:" + hashlib.sha256(
        json.dumps(graph, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def build_static_search_index(graph: dict[str, Any], *, cache_status: str = "built") -> dict[str, Any]:
    """Build a deterministic local search index from graph JSON/JSONL content only."""

    observations = {
        str(item.get("id")): item
        for item in graph.get("observations", [])
        if isinstance(item, dict) and item.get("id")
    }
    aliases_by_node = _aliases_by_node(graph)
    records = [
        _record_for_node(node, observations=observations, aliases=aliases_by_node.get(str(node.get("id") or ""), []))
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and node.get("id")
    ]
    records = sorted(records, key=lambda item: item["node_id"])
    metadata = graph.get("metadata", {}) if isinstance(graph.get("metadata"), dict) else {}
    index = {
        "schema_version": 1,
        "write_policy": "read_only",
        "artifact_kind": "project_graph_static_search_index",
        "source_boundary": "graph_artifact_only_raw_source_excluded",
        "generated_view_policy": "static_search_index_is_generated_cache_not_source_of_truth",
        "approval_boundary": "batch19_explicit_offline_static_index_no_live_backend_model_or_database",
        "graph_fingerprint": graph_content_fingerprint(graph),
        "metadata": {
            "scan_id": sanitize_graph_text(metadata.get("scan_id") or ""),
            "node_count": int(metadata.get("node_count") or len(graph.get("nodes", []))),
            "edge_count": int(metadata.get("edge_count") or len(graph.get("edges", []))),
            "index_record_count": len(records),
            "manifest_fingerprint": sanitize_graph_text(
                (metadata.get("manifest") or {}).get("root_fingerprint")
                if isinstance(metadata.get("manifest"), dict)
                else ""
            ),
        },
        "cache_policy": {
            "cache_status": cache_status,
            "fingerprint_scope": "canonical_redacted_graph_artifact",
            "stale_policy": "block_if_graph_fingerprint_mismatch",
            "cache_storage": "explicit_stage_root_only",
        },
        "query_policy": {
            "offline_only": True,
            "no_live_database_or_server": True,
            "no_llm_embedding_or_cross_encoder": True,
            "default_max_results": DEFAULT_MAX_RESULTS,
            "default_max_tokens": DEFAULT_MAX_TOKENS,
        },
        "eval_policy": {
            "explicit_thresholds_required": True,
            "minimum_symbol_recall": 1.0,
            "minimum_top_k_mrr": 1.0,
            "maximum_false_positive_rate": 0.0,
        },
        "rollback": {
            "disable_path": f"delete {STATIC_SEARCH_INDEX_TARGET}",
            "fallback": "graph_only_search_packets",
            "deletion_scope": "stage_root_generated_cache_only",
        },
        "records": records,
    }
    index["validation"] = validate_static_search_index(index)
    return index


def load_static_search_index(path: str | Path) -> dict[str, Any]:
    """Load a static index artifact without reading workspace source files."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("static search index artifact must be a JSON object")
    return payload


def stage_project_graph_search_index(
    graph_artifact: str | Path,
    stage_root: str | Path,
    *,
    workspace: str | Path,
) -> dict[str, Any]:
    """Stage or reuse a static search index under an explicit stage root."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    if stage_path == workspace_path or stage_path.is_relative_to(workspace_path):
        raise ValueError("stage output directory must be outside workspace")
    if stage_path.exists() and not stage_path.is_dir():
        raise ValueError("stage output path is not a directory")

    graph = _load_graph_artifact(graph_artifact)
    fingerprint = graph_content_fingerprint(graph)
    target = stage_path / STATIC_SEARCH_INDEX_TARGET
    previous = _load_existing_index(target)
    if previous and previous.get("graph_fingerprint") == fingerprint and previous.get("validation", {}).get("ok") is True:
        return _stage_result("ready", "hit", "leave_unchanged")

    cache_status = "miss_invalidated" if previous else "miss"
    if previous:
        _backup_existing(target, target.with_name("project-code-graph-search-index.previous.json"))
    index = build_static_search_index(graph, cache_status=cache_status)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(index, indent=2, sort_keys=True), encoding="utf-8")
    return _stage_result("ready" if index["validation"]["ok"] else "blocked", cache_status, "create")


def query_static_search_index(index: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    """Run a deterministic bounded search against a static index."""

    errors = _validate_query(index, request)
    if errors:
        return _packet(index, request, status="blocked", nodes=[], errors=errors)
    query_text = sanitize_graph_text(request.get("text") or "")
    query_terms = _terms(query_text)
    records = [
        (record, _score_record(record, query_terms))
        for record in index.get("records", [])
        if isinstance(record, dict) and _record_matches_filters(record, request)
    ]
    if query_terms:
        records = [(record, score) for record, score in records if score > 0]
    ranked = sorted(records, key=lambda item: (-item[1], item[0]["node_id"]))
    return _packet(index, request, status="ok", nodes=[_compact_record(record) for record, _score in ranked])


def validate_static_search_index(index: dict[str, Any]) -> dict[str, Any]:
    """Validate static index schema and source-boundary invariants."""

    errors: list[str] = []
    if index.get("schema_version") != 1:
        errors.append("schema_version")
    if index.get("write_policy") != "read_only":
        errors.append("write_policy")
    if index.get("artifact_kind") != "project_graph_static_search_index":
        errors.append("artifact_kind")
    if index.get("source_boundary") != "graph_artifact_only_raw_source_excluded":
        errors.append("source_boundary")
    if not str(index.get("graph_fingerprint") or "").startswith("sha256:"):
        errors.append("graph_fingerprint")
    records = index.get("records")
    if not isinstance(records, list):
        errors.append("records")
        records = []
    for record in records:
        if not isinstance(record, dict):
            errors.append("record:shape")
            continue
        if not record.get("node_id"):
            errors.append("record:node_id")
        if _has_unsafe_text(record):
            errors.append("record:unsafe_text")
        path = str(record.get("path") or "")
        if path and safe_relative_path_text(path) != path:
            errors.append("record:path")
    return {
        "ok": not errors,
        "checks": [
            "schema_v1",
            "read_only",
            "graph_fingerprint",
            "source_free_records",
            "stage_cache_policy",
        ],
        "errors": sorted(set(errors)),
    }


def _record_for_node(
    node: dict[str, Any],
    *,
    observations: dict[str, dict[str, Any]],
    aliases: list[str],
) -> dict[str, Any]:
    node_id = _safe_review_text(node.get("id") or "")
    label = _safe_review_text(node.get("label") or "")
    path = safe_relative_path_text(node.get("path") or "")
    observation_ids = [_safe_review_text(item) for item in node.get("observation_ids", []) if item]
    confidence = _confidence(observation_ids, observations)
    alias_values = sorted(set(_safe_review_text(item) for item in aliases if item))
    partitions = _partitions(path)
    searchable_values = [
        node_id,
        label,
        path,
        _safe_review_text(node.get("type") or ""),
        _safe_review_text(node.get("language") or ""),
        *alias_values,
    ]
    terms = sorted(set(term for value in searchable_values for term in _terms(value)))
    return {
        "node_id": node_id,
        "type": _safe_review_text(node.get("type") or ""),
        "label": label[:120],
        "language": _safe_review_text(node.get("language") or ""),
        "path": path,
        "aliases": alias_values[:10],
        "partitions": partitions,
        "confidence": confidence,
        "stale_status": _safe_review_text(node.get("status") or ""),
        "observation_ids": observation_ids[:5],
        "terms": terms[:80],
    }


def _aliases_by_node(graph: dict[str, Any]) -> dict[str, list[str]]:
    metadata = graph.get("metadata", {}) if isinstance(graph.get("metadata"), dict) else {}
    ledger = metadata.get("alias_ledger") if isinstance(metadata.get("alias_ledger"), dict) else {}
    aliases: dict[str, list[str]] = {}
    for item in ledger.get("aliases", []) if isinstance(ledger.get("aliases"), list) else []:
        if not isinstance(item, dict):
            continue
        canonical_id = str(item.get("canonical_id") or "")
        alias = str(item.get("alias") or "")
        if canonical_id and alias:
            aliases.setdefault(canonical_id, []).append(alias)
    return aliases


def _confidence(observation_ids: list[str], observations: dict[str, dict[str, Any]]) -> str:
    levels = [
        str(observations[item].get("confidence") or "")
        for item in observation_ids
        if item in observations
    ]
    if "verified" in levels:
        return "verified"
    if "high" in levels:
        return "high"
    if "medium" in levels:
        return "medium"
    if "low" in levels:
        return "low"
    return "present_unverified"


def _partitions(path: str) -> list[str]:
    partitions = ["workspace"]
    if path:
        first = path.split("/", 1)[0] or "root"
        partitions.append(first)
    else:
        partitions.append("root")
    return sorted(set(partitions))


def _terms(value: Any) -> list[str]:
    text = _safe_review_text(value).lower().replace("\\", "/")
    return [term for term in re.split(r"[^a-z0-9]+", text) if term]


def _score_record(record: dict[str, Any], query_terms: list[str]) -> int:
    terms = set(str(item) for item in record.get("terms", []) if item)
    haystack = " ".join(
        str(record.get(key) or "").lower()
        for key in ["node_id", "label", "path", "type", "language"]
    )
    score = 0
    for term in query_terms:
        if term in terms:
            score += 10
        elif term in haystack:
            score += 3
    if str(record.get("type")) in {"function", "method", "class"}:
        score += 4
    if "/tests/" not in f"/{record.get('path', '')}" and not str(record.get("path") or "").startswith("tests/"):
        score += 2
    else:
        score -= 15
    if str(record.get("stale_status")) == "current":
        score += 1
    return score


def _record_matches_filters(record: dict[str, Any], request: dict[str, Any]) -> bool:
    node_types = set(str(item) for item in request.get("node_types", []) if isinstance(item, str))
    path_prefixes = [str(item) for item in request.get("path_prefixes", []) if isinstance(item, str)]
    if node_types and record.get("type") not in node_types:
        return False
    if path_prefixes and not any(str(record.get("path") or "").startswith(prefix) for prefix in path_prefixes):
        return False
    return True


def _compact_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(record.get("node_id") or ""),
        "type": str(record.get("type") or ""),
        "label": str(record.get("label") or "")[:120],
        "status": str(record.get("stale_status") or ""),
        "language": str(record.get("language") or ""),
        "path": str(record.get("path") or ""),
    }


def _validate_query(index: dict[str, Any], request: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    validation = index.get("validation") if isinstance(index.get("validation"), dict) else validate_static_search_index(index)
    if validation.get("ok") is not True:
        errors.append("static_index:invalid")
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
    index: dict[str, Any],
    request: dict[str, Any],
    *,
    status: str,
    nodes: list[dict[str, Any]],
    errors: list[str] | None = None,
) -> dict[str, Any]:
    max_results = _positive_int(request.get("max_results"), DEFAULT_MAX_RESULTS)
    max_tokens = _positive_int(request.get("max_tokens"), DEFAULT_MAX_TOKENS)
    omitted = max(0, len(nodes) - max_results)
    compact_nodes = nodes[:max_results]
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "status": status,
        "result_kind": "search",
        "search_backend": "static_index",
        "query_id": _query_id(request),
        "as_of_scan": str((index.get("metadata") or {}).get("scan_id") or ""),
        "source_boundary": "graph_artifact_only_raw_source_excluded",
        "generated_view_policy": "static_search_index_is_generated_cache_not_source_of_truth",
        "nodes": compact_nodes,
        "edges": [],
        "errors": errors or [],
        "filters": {
            key: request[key]
            for key in ["node_types", "path_prefixes"]
            if key in request
        },
        "budget": {
            "max_results": max_results,
            "max_tokens": max_tokens,
            "estimated_tokens": 0,
            "truncated": omitted > 0,
            "omitted_count": omitted,
            "truncation_reasons": ["max_results"] if omitted > 0 else [],
        },
        "safe_next_action": "Use static index as generated orientation cache only; read source before edits or completion claims.",
    }
    _enforce_budget(packet)
    return packet


def _enforce_budget(packet: dict[str, Any]) -> None:
    budget = packet["budget"]
    max_tokens = _positive_int(budget.get("max_tokens"), DEFAULT_MAX_TOKENS)
    while _estimated_tokens(packet) > max_tokens and packet.get("nodes"):
        packet["nodes"].pop()
        budget["truncated"] = True
        budget["omitted_count"] = int(budget.get("omitted_count") or 0) + 1
        budget["truncation_reasons"] = sorted(set(list(budget.get("truncation_reasons") or []) + ["token_budget"]))
    budget["estimated_tokens"] = _estimated_tokens(packet)


def _stage_result(status: str, cache_status: str, action: str) -> dict[str, Any]:
    return {
        "rendered_artifacts": {
            "status": status,
            "mode": "build-index",
            "root_status": "redacted",
            "cache_status": cache_status,
            "source_boundary": "graph_artifact_only_raw_source_excluded",
            "rollback": {"disable_path": f"delete {STATIC_SEARCH_INDEX_TARGET}"},
            "files": [
                {
                    "target_path": STATIC_SEARCH_INDEX_TARGET,
                    "action": action,
                    "write_policy": "staged_only",
                    "staged_path": STATIC_SEARCH_INDEX_TARGET,
                }
            ],
        }
    }


def _load_graph_artifact(path: str | Path) -> dict[str, Any]:
    graph_path = Path(path)
    text = graph_path.read_text(encoding="utf-8")
    if graph_path.suffix.lower() == ".jsonl":
        graph: dict[str, Any] = {
            "schema_version": 1,
            "write_policy": "read_only",
            "metadata": {},
            "nodes": [],
            "edges": [],
            "observations": [],
        }
        for line in text.splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            kind = record.get("record_kind")
            payload = record.get("payload")
            if kind == "metadata" and isinstance(payload, dict):
                graph["metadata"] = payload
            elif kind == "node" and isinstance(payload, dict):
                graph["nodes"].append(payload)
            elif kind == "edge" and isinstance(payload, dict):
                graph["edges"].append(payload)
            elif kind == "observation" and isinstance(payload, dict):
                graph["observations"].append(payload)
        return graph
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError("graph artifact must be a JSON object")
    return payload


def _load_existing_index(path: Path) -> dict[str, Any] | None:
    if not path.exists() or not path.is_file():
        return None
    try:
        return load_static_search_index(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return None


def _backup_existing(target: Path, backup_target: Path) -> None:
    if not target.exists() or not target.is_file():
        return
    backup_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(target, backup_target)


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


def _query_id(request: dict[str, Any]) -> str:
    return "index-query:" + hashlib.sha256(json.dumps(request, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def _estimated_tokens(packet: dict[str, Any]) -> int:
    return max(1, len(json.dumps(packet, sort_keys=True)) // 4)


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default
