"""Read-only project code graph foundation for Product-Agent OS."""

from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path
from typing import Any

from product_agent_os.project_graph_adapters import build_language_overlays
from product_agent_os.project_graph_chunking import (
    build_partition_alias_readiness_metadata,
    build_structured_overlays,
)
from product_agent_os.project_graph_manifest import build_project_graph_manifest, collect_project_files
from product_agent_os.project_graph_observations import build_observation_record, diff_observation_lineage
from product_agent_os.project_graph_ontology import validate_graph_schema


PROJECT_GRAPH_TARGET = ".codex/product-agent-os/project-code-graph.json"
PROJECT_GRAPH_JSONL_TARGET = ".codex/product-agent-os/project-code-graph.jsonl"
MAX_SYNTHETIC_PROMPT_NODES = 250
LINE_COUNT_LIMIT = 10_000
GRAPH_DEPTH_DECISION_ARTIFACT = "docs/superpowers/specs/batch39-s4-graph-depth-s0-ontology-parser-decision.json"


def build_project_code_graph(
    workspace: str | Path,
    *,
    previous_manifest: dict[str, Any] | None = None,
    previous_graph: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic file-level project graph without mutating the workspace."""

    root = Path(workspace).resolve()
    project_files = collect_project_files(root)
    manifest = build_project_graph_manifest(root, project_files, previous_manifest=previous_manifest)
    scan_id = "scan-" + manifest["root_fingerprint"].removeprefix("sha256:")[:16]
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []

    workspace_id = f"workspace:{_safe_id(root.name)}"
    workspace_observation = build_observation_record(
        scan_id=scan_id,
        relative_path=".",
        span={"start_line": 1, "end_line": 1},
        fingerprint=manifest["root_fingerprint"],
        extractor="workspace_inventory",
        confidence="verified",
        redaction_status="redacted",
        subject_id=workspace_id,
    )
    observations.append(workspace_observation)
    nodes.append(
        {
            "id": workspace_id,
            "type": "workspace",
            "label": root.name,
            "status": "current",
            "language": "unknown",
            "observation_ids": [workspace_observation["id"]],
        }
    )

    for item in manifest["files"]:
        node_id = "file:" + item["relative_path"]
        status = _file_status(item)
        observation = build_observation_record(
            scan_id=scan_id,
            relative_path=item["relative_path"],
            span={"start_line": 1, "end_line": _line_count(root / item["relative_path"])},
            fingerprint=item["fingerprint"],
            extractor="file_inventory",
            confidence="verified",
            redaction_status="redacted",
            subject_id=node_id,
        )
        observations.append(observation)
        nodes.append(
            {
                "id": node_id,
                "type": _node_type_for_file(item["relative_path"], item["generated"]),
                "label": item["relative_path"],
                "status": status,
                "language": item["language"],
                "path": item["relative_path"],
                "source_spans": [
                    {
                        "relative_path": item["relative_path"],
                        "start_line": 1,
                        "end_line": observation["span"]["end_line"],
                        "fingerprint": item["fingerprint"],
                    }
                ],
                "observation_ids": [observation["id"]],
            }
        )
        edge_id = _edge_id("contains", workspace_id, node_id)
        edge_observation = build_observation_record(
            scan_id=scan_id,
            relative_path=item["relative_path"],
            span={"start_line": 1, "end_line": 1},
            fingerprint=item["fingerprint"],
            extractor="file_inventory",
            confidence="verified",
            redaction_status="redacted",
            subject_id=edge_id,
        )
        observations.append(edge_observation)
        edges.append(
            {
                "id": edge_id,
                "type": "contains",
                "source": workspace_id,
                "target": node_id,
                "confidence": "verified",
                "status": "current",
                "observation_ids": [edge_observation["id"]],
                "fingerprint": item["fingerprint"],
            }
        )

    language_overlay = build_language_overlays(root, manifest["files"], scan_id=scan_id, workspace_id=workspace_id)
    structured_overlay = build_structured_overlays(root, manifest["files"], scan_id=scan_id)
    nodes.extend(language_overlay["nodes"])
    nodes.extend(structured_overlay["nodes"])
    edges.extend(language_overlay["edges"])
    edges.extend(structured_overlay["edges"])
    observations.extend(language_overlay["observations"])
    observations.extend(structured_overlay["observations"])
    linker = _build_conservative_linker(nodes, scan_id=scan_id)
    edges.extend(linker["edges"])
    observations.extend(linker["observations"])
    partition_metadata = build_partition_alias_readiness_metadata(manifest)
    node_dedupe = _dedupe_by_id(nodes)
    edge_dedupe = _dedupe_by_id(edges)
    observation_dedupe = _dedupe_by_id(observations)
    metadata = {
        "scan_id": scan_id,
        "source_boundary": "raw_source_bodies_excluded",
        "generated_view_policy": "html_is_review_only",
        "node_count": len(node_dedupe["items"]),
        "edge_count": len(edge_dedupe["items"]),
        "observation_count": len(observation_dedupe["items"]),
        "dedupe_summary": {
            "dropped_nodes": node_dedupe["dropped_count"],
            "dropped_edges": edge_dedupe["dropped_count"],
            "dropped_observations": observation_dedupe["dropped_count"],
        },
        "language_support_summary": _language_support_summary(manifest["files"]),
        "adapter_summary": language_overlay["metadata"]["adapter_summary"],
        "graph_depth_decision": _graph_depth_decision_metadata(),
        "structured_overlay_summary": structured_overlay["metadata"]["structured_overlay_summary"],
        "coverage_map": _coverage_map(manifest, node_dedupe["items"], edge_dedupe["items"]),
        "python_scanner": language_overlay["metadata"]["python_scanner"],
        "typescript_javascript_scanner": language_overlay["metadata"]["typescript_javascript_scanner"],
        "conservative_linker": linker["metadata"],
        "rejected_links": linker["rejected_links"],
        "line_count_policy": f"capped_at_{LINE_COUNT_LIMIT}",
        "manifest": manifest,
        "scope_policy": manifest.get("scope_policy", {}),
        "temporal_delta": (
            diff_observation_lineage(previous_graph, {"edges": edge_dedupe["items"]}, scan_id=scan_id)
            if isinstance(previous_graph, dict)
            else {"schema_version": 1, "scan_id": scan_id, "status": "not_available"}
        ),
        **partition_metadata,
    }

    graph = {
        "schema_version": 1,
        "write_policy": "read_only",
        "artifact_targets": {
            "json": PROJECT_GRAPH_TARGET,
            "jsonl": PROJECT_GRAPH_JSONL_TARGET,
        },
        "metadata": metadata,
        "nodes": sorted(node_dedupe["items"], key=lambda item: item["id"]),
        "edges": sorted(edge_dedupe["items"], key=lambda item: item["id"]),
        "observations": sorted(observation_dedupe["items"], key=lambda item: item["id"]),
    }
    graph["validation"] = validate_graph_schema(graph)
    return graph


def graph_to_jsonl(graph: dict[str, Any]) -> str:
    """Serialize a graph into bounded JSONL records for agent consumption."""

    records = [{"record_kind": "metadata", "payload": graph.get("metadata", {})}]
    records.extend({"record_kind": "node", "payload": node} for node in graph.get("nodes", []))
    records.extend({"record_kind": "edge", "payload": edge} for edge in graph.get("edges", []))
    records.extend({"record_kind": "observation", "payload": obs} for obs in graph.get("observations", []))
    return "\n".join(json.dumps(record, sort_keys=True) for record in records)


def build_synthetic_project_graph(node_count: int) -> dict[str, Any]:
    """Build a bounded synthetic graph summary for scale fixture checks."""

    visible_count = min(node_count, MAX_SYNTHETIC_PROMPT_NODES)
    nodes = [
        {
            "id": f"file:synthetic/module_{index}.py",
            "type": "module",
            "label": f"synthetic/module_{index}.py",
            "status": "current",
            "language": "python",
            "path": f"synthetic/module_{index}.py",
            "observation_ids": [f"obs:synthetic:{index}"],
        }
        for index in range(visible_count)
    ]
    observations = [
        {
            "id": f"obs:synthetic:{index}",
            "scan_id": f"synthetic-{node_count}",
            "subject_id": f"file:synthetic/module_{index}.py",
            "relative_path": f"synthetic/module_{index}.py",
            "span": {"start_line": 1, "end_line": 1},
            "fingerprint": "sha256:" + f"{index:064x}"[-64:],
            "extractor": "synthetic_scale_fixture",
            "confidence": "verified",
            "redaction_status": "redacted",
            "raw_source_status": "excluded",
        }
        for index in range(visible_count)
    ]
    graph = {
        "schema_version": 1,
        "write_policy": "read_only",
        "artifact_targets": {"json": PROJECT_GRAPH_TARGET, "jsonl": PROJECT_GRAPH_JSONL_TARGET},
        "metadata": {
            "scan_id": f"synthetic-{node_count}",
            "source_boundary": "raw_source_bodies_excluded",
            "generated_view_policy": "html_is_review_only",
            "node_count": node_count,
            "visible_node_count": visible_count,
            "omitted_node_count": node_count - visible_count,
            "edge_count": 0,
            "observation_count": visible_count,
            "language_support_summary": {"python": "supported"},
            "scale_policy": "large_graph_payload_is_bounded",
        },
        "nodes": nodes,
        "edges": [],
        "observations": observations,
    }
    graph["validation"] = validate_graph_schema(graph)
    return graph


def build_synthetic_project_graph_from_fixture(fixture_path: str | Path) -> dict[str, Any]:
    """Build a bounded synthetic graph from a scale fixture directory."""

    path = Path(fixture_path) / "scale.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return build_synthetic_project_graph(node_count=int(payload["node_count"]))


def _node_type_for_file(relative_path: str, generated: bool) -> str:
    if generated:
        return "generated_artifact"
    path = Path(relative_path)
    lowered = relative_path.lower()
    if path.name.upper() in {"AGENTS.MD", "REQUIREMENTS.MD", "PLAN.MD", "TEST.MD", "EVALS.MD", "RUNLOG.MD"}:
        return "control_plane"
    if "/tests/" in f"/{lowered}" or path.name.startswith("test_"):
        return "test"
    if "/fixtures/" in f"/{lowered}" or "/eval-fixtures/" in f"/{lowered}":
        return "fixture"
    if lowered.endswith((".md", ".markdown")):
        return "markdown_page"
    if lowered.endswith((".yaml", ".yml", ".json")) and any(term in lowered for term in ["openapi", "swagger", "asyncapi"]):
        return "contract"
    if lowered.endswith((".sql", ".dbml")):
        return "schema"
    return "module"


def _file_status(item: dict[str, Any]) -> str:
    if item["generated"]:
        return "generated"
    return "current"


def _line_count(path: Path) -> int:
    count = 0
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                count += chunk.count(b"\n")
                if count >= LINE_COUNT_LIMIT:
                    return LINE_COUNT_LIMIT
    except OSError:
        return 1
    return max(1, count or 1)


def _language_support_summary(files: list[dict[str, Any]]) -> dict[str, str]:
    summary: dict[str, str] = {}
    for item in files:
        language = str(item.get("language") or "unknown")
        if language == "python":
            summary[language] = "supported"
        elif language in {"typescript", "javascript"}:
            summary[language] = "supported_conservative_stdlib"
        elif language in {"markdown", "yaml", "json", "sql", "dbml"}:
            summary[language] = "structured_overlay_supported"
        else:
            summary[language] = "file_only"
    return dict(sorted(summary.items()))


def _coverage_map(manifest: dict[str, Any], nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> dict[str, Any]:
    files = [item for item in manifest.get("files", []) if isinstance(item, dict)]
    language_support = _language_support_summary(files)
    unsupported_languages = {
        language: support
        for language, support in language_support.items()
        if support == "file_only"
    }
    partial_languages = {
        language: support
        for language, support in language_support.items()
        if support in {"supported_conservative_stdlib", "structured_overlay_supported"}
    }
    partial_file_count = sum(
        1
        for item in files
        if language_support.get(str(item.get("language") or "unknown")) in {"supported_conservative_stdlib", "structured_overlay_supported"}
    )
    scope_policy = manifest.get("scope_policy", {}) if isinstance(manifest.get("scope_policy"), dict) else {}
    omitted_count = int((manifest.get("summary") or {}).get("omitted_count") or 0)
    skipped_reasons = _coverage_skipped_reasons(scope_policy, omitted_count)
    return {
        "schema_version": 1,
        "status": "diagnostic_only",
        "source_boundary": "raw_source_bodies_excluded",
        "generated_view_policy": "coverage_is_not_semantic_correctness_proof",
        "files": {
            "total": len(files),
            "generated": sum(1 for item in files if bool(item.get("generated"))),
            "partial": partial_file_count,
            "skipped": sum(skipped_reasons.values()),
            "low_value": sum(1 for item in files if bool(item.get("low_value"))),
            "truncated": bool((manifest.get("summary") or {}).get("truncated")),
            "omitted_count": omitted_count,
        },
        "by_language": _count_by(files, "language"),
        "by_path_prefix": _path_prefix_counts(files),
        "by_file_type": _file_type_counts(files),
        "by_node_type": _count_by(nodes, "type"),
        "confidence_distribution": _count_by(edges, "confidence"),
        "unsupported_languages": unsupported_languages,
        "partial_languages": partial_languages,
        "skipped_reasons": skipped_reasons,
        "generated_vendor_imported_scope": scope_policy,
        "scope_policy": scope_policy,
        "recommended_next_parser_or_linker_action": _coverage_next_action(unsupported_languages, partial_languages),
    }


def _count_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(key) or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _path_prefix_counts(files: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in files:
        relative = str(item.get("relative_path") or "")
        prefix = relative.split("/", 1)[0] if "/" in relative else "."
        counts[prefix] = counts.get(prefix, 0) + 1
    return dict(sorted(counts.items()))


def _file_type_counts(files: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in files:
        relative = str(item.get("relative_path") or "")
        suffix = Path(relative).suffix.lower() or "no_extension"
        counts[suffix] = counts.get(suffix, 0) + 1
    return dict(sorted(counts.items()))


def _coverage_skipped_reasons(scope_policy: dict[str, Any], omitted_count: int) -> dict[str, int]:
    reasons: dict[str, int] = {}
    excluded_prefixes = scope_policy.get("excluded_prefixes")
    if isinstance(excluded_prefixes, list) and excluded_prefixes:
        reasons["excluded_prefix"] = len(excluded_prefixes)
    if omitted_count:
        reasons["skipped_or_omitted_file"] = omitted_count
    return dict(sorted(reasons.items()))


def _coverage_next_action(unsupported_languages: dict[str, str], partial_languages: dict[str, str]) -> str:
    if unsupported_languages:
        return "Review unsupported language inventory before graph-backed edits or impact claims."
    if partial_languages:
        return "Treat partial language and structured overlays as orientation; read source before claims."
    return "Use graph as orientation and read source before edits or completion claims."


def _build_conservative_linker(nodes: list[dict[str, Any]], *, scan_id: str) -> dict[str, Any]:
    operations = [
        node
        for node in nodes
        if isinstance(node, dict)
        and node.get("metadata", {}).get("source_kind") == "openapi_operation"
        and node.get("id")
    ]
    functions = [
        node
        for node in nodes
        if isinstance(node, dict)
        and node.get("type") in {"function", "method"}
        and node.get("id")
    ]
    edges: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []
    rejected_links: list[dict[str, Any]] = []
    seen_edges: set[tuple[str, str]] = set()
    seen_rejections: set[tuple[str, str, str]] = set()
    for function in functions:
        function_label = str(function.get("label") or "")
        function_norm = _link_name(function_label)
        function_tokens = _link_tokens(function_label)
        if not function_norm:
            continue
        for operation in operations:
            operation_label = str(operation.get("label") or "")
            operation_norm = _link_name(operation_label)
            operation_tokens = _link_tokens(operation_label)
            if not operation_norm:
                continue
            source_id = str(function["id"])
            target_id = str(operation["id"])
            if function_norm == operation_norm:
                if (source_id, target_id) in seen_edges:
                    continue
                seen_edges.add((source_id, target_id))
                edge, observation = _linker_edge(scan_id, function, operation)
                edges.append(edge)
                observations.append(observation)
                continue
            if _weak_link_candidate(function_norm, operation_norm, function_tokens, operation_tokens):
                key = (source_id, target_id, "weak_name_similarity")
                if key in seen_rejections:
                    continue
                seen_rejections.add(key)
                rejected_links.append(_rejected_link(function, operation, reason="weak_name_similarity"))
    return {
        "edges": edges,
        "observations": observations,
        "rejected_links": rejected_links[:100],
        "metadata": {
            "schema_version": 1,
            "policy": "exact_normalized_names_only_for_static_cross_language_links",
            "allowed_evidence_sources": ["function_label", "openapi_operation_id"],
            "edge_confidence": "inferred",
            "edge_type": "references",
            "link_count": len(edges),
            "rejected_link_count": len(rejected_links),
            "unsupported_claims": [
                "runtime_api_compatibility",
                "auth_or_data_flow_correctness",
                "production_behavior",
                "readiness",
            ],
        },
    }


def _linker_edge(scan_id: str, source_node: dict[str, Any], target_node: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    source_id = str(source_node["id"])
    target_id = str(target_node["id"])
    span = _first_source_span(source_node)
    edge_id = _edge_id("references", source_id, target_id)
    observation = build_observation_record(
        scan_id=scan_id,
        relative_path=span["relative_path"],
        span={"start_line": span["start_line"], "end_line": span["start_line"]},
        fingerprint=span["fingerprint"],
        extractor="conservative_static_linker",
        confidence="inferred",
        redaction_status="redacted",
        subject_id=edge_id,
    )
    return (
        {
            "id": edge_id,
            "type": "references",
            "source": source_id,
            "target": target_id,
            "confidence": "inferred",
            "status": "current",
            "observation_ids": [observation["id"]],
            "fingerprint": span["fingerprint"],
            "metadata": {
                "linker": "conservative_static_linker",
                "evidence": "exact_normalized_name_match",
                "source_read_required": True,
                "runtime_claims_supported": False,
            },
        },
        observation,
    )


def _rejected_link(source_node: dict[str, Any], target_node: dict[str, Any], *, reason: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "source": str(source_node.get("id") or ""),
        "target": str(target_node.get("id") or ""),
        "rule": "conservative_static_linker_exact_match_only",
        "reason": reason,
        "confidence": "unsupported",
        "source_read_required": True,
        "future_resolution": "explicit_route_or_contract_mapping_required",
        "unsupported_claims": ["hidden_dependency", "impact_proof", "runtime_api_compatibility"],
    }


def _first_source_span(node: dict[str, Any]) -> dict[str, Any]:
    spans = node.get("source_spans")
    if isinstance(spans, list) and spans and isinstance(spans[0], dict):
        return {
            "relative_path": str(spans[0].get("relative_path") or str(node.get("path") or ".")),
            "start_line": int(spans[0].get("start_line") or 1),
            "fingerprint": str(spans[0].get("fingerprint") or "sha256:" + "0" * 64),
        }
    return {
        "relative_path": str(node.get("path") or "."),
        "start_line": 1,
        "fingerprint": "sha256:" + "0" * 64,
    }


def _link_name(value: str) -> str:
    return "".join(_link_tokens(value))


def _link_tokens(value: str) -> list[str]:
    expanded = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    tokens = [token.lower() for token in re.split(r"[^A-Za-z0-9]+", expanded) if token]
    return [token[:-1] if len(token) > 3 and token.endswith("s") else token for token in tokens]


def _weak_link_candidate(source_norm: str, target_norm: str, source_tokens: list[str], target_tokens: list[str]) -> bool:
    if not source_norm or not target_norm:
        return False
    if source_norm.startswith(target_norm) or target_norm.startswith(source_norm):
        return True
    return len(set(source_tokens) & set(target_tokens)) >= 2


def _dedupe_by_id(items: list[dict[str, Any]]) -> dict[str, Any]:
    by_id: dict[str, dict[str, Any]] = {}
    dropped_count = 0
    for item in items:
        item_id = item.get("id")
        if isinstance(item_id, str) and item_id not in by_id:
            by_id[item_id] = item
        elif isinstance(item_id, str):
            dropped_count += 1
    return {"items": list(by_id.values()), "dropped_count": dropped_count}


def _graph_depth_decision_metadata() -> dict[str, Any]:
    return {
        "decision_id": "B39-S4-GD-S0-ONTOLOGY-PARSER-DECISION",
        "task_ids": ["B39-S4-GRAPH-DEPTH-00", "B39-S4-GRAPH-DEPTH-07"],
        "decision_artifact": GRAPH_DEPTH_DECISION_ARTIFACT,
        "ontology_profile": "core_terms_plus_framework_metadata",
        "parser_dependency_policy": "stdlib_regex_no_external_dependency",
        "core_node_types_added": [],
        "core_edge_types_added": [],
        "schema_migration_required": False,
        "framework_terms_policy": "metadata_only_until_registered",
        "readiness_policy": "orientation_evidence_only",
    }


def _safe_id(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-") or "item"


def _edge_id(edge_type: str, source: str, target: str) -> str:
    seed = json.dumps({"type": edge_type, "source": source, "target": target}, sort_keys=True)
    return "edge:" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24]
