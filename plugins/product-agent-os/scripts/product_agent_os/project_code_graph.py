"""Read-only project code graph foundation for Product-Agent OS."""

from __future__ import annotations

import json
import hashlib
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
        "structured_overlay_summary": structured_overlay["metadata"]["structured_overlay_summary"],
        "python_scanner": language_overlay["metadata"]["python_scanner"],
        "line_count_policy": f"capped_at_{LINE_COUNT_LIMIT}",
        "manifest": manifest,
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
    language = str(item.get("language") or "unknown")
    if language in {"typescript", "javascript"}:
        return "unsupported"
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
        elif language in {"markdown", "yaml", "json", "sql", "dbml"}:
            summary[language] = "structured_overlay_supported"
        elif language in {"typescript", "javascript"}:
            summary[language] = "file_only"
        else:
            summary[language] = "file_only"
    return dict(sorted(summary.items()))


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


def _safe_id(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-") or "item"


def _edge_id(edge_type: str, source: str, target: str) -> str:
    seed = json.dumps({"type": edge_type, "source": source, "target": target}, sort_keys=True)
    return "edge:" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24]
