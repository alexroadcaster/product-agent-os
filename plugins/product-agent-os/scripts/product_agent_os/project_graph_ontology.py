"""Controlled ontology and validation for Product-Agent OS project graphs."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path, PureWindowsPath
from typing import Any

from codex_runtime_runner.redaction import validate_redaction


GRAPH_LIMITS = {
    "max_nodes": 10_000,
    "max_edges": 25_000,
    "max_label_chars": 160,
    "max_observations": 30_000,
}

_NODE_TYPES = [
    "workspace",
    "package",
    "module",
    "file",
    "class",
    "function",
    "method",
    "test",
    "fixture",
    "template",
    "generated_artifact",
    "markdown_page",
    "mkdocs_page",
    "contract",
    "schema",
    "diagram",
    "control_plane",
]
_EDGE_TYPES = [
    "contains",
    "imports",
    "calls",
    "exports",
    "tests",
    "verifies",
    "documents",
    "renders",
    "generates",
    "configures",
    "owns",
    "references",
    "impacts",
]
_CONFIDENCE_LEVELS = ["verified", "inferred", "heuristic", "unsupported", "accepted_gap"]
_STATUS_VALUES = ["current", "stale", "generated", "unsupported", "invalidated", "superseded", "accepted_gap"]
_LANGUAGE_SUPPORT = {
    "python": "supported",
    "markdown": "structured_overlay_pending",
    "yaml": "structured_overlay_pending",
    "json": "structured_overlay_pending",
    "sql": "structured_overlay_pending",
    "dbml": "structured_overlay_pending",
    "toml": "file_only",
    "typescript": "supported_conservative_stdlib",
    "javascript": "supported_conservative_stdlib",
    "plantuml": "structured_overlay_pending",
    "text": "file_only",
    "unknown": "file_only",
}
_DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
_FORBIDDEN_SOURCE_KEYS = {"raw_source", "source_body", "raw_body", "content", "raw_prompt", "raw_tool_output"}


def default_ontology() -> dict[str, Any]:
    """Return the baseline controlled ontology for Task 25 project graphs."""

    return {
        "schema_version": 1,
        "node_types": list(_NODE_TYPES),
        "edge_types": list(_EDGE_TYPES),
        "confidence_levels": list(_CONFIDENCE_LEVELS),
        "status_values": list(_STATUS_VALUES),
        "language_support": dict(_LANGUAGE_SUPPORT),
        "limits": dict(GRAPH_LIMITS),
        "extension_status": "core",
    }


def register_ontology_extension(
    ontology: dict[str, Any],
    *,
    node_types: list[str] | None = None,
    edge_types: list[str] | None = None,
) -> dict[str, Any]:
    """Return a copy of the ontology with explicit extension terms registered."""

    extended = deepcopy(ontology)
    for key, values in [("node_types", node_types or []), ("edge_types", edge_types or [])]:
        current = {str(item) for item in extended.get(key, [])}
        current.update(str(item) for item in values if str(item).strip())
        extended[key] = sorted(current)
    extended["extension_status"] = "registered"
    return extended


def validate_graph_schema(graph: Any, ontology: dict[str, Any] | None = None) -> dict[str, Any]:
    """Validate a project graph packet without treating it as source of truth."""

    ontology = ontology or default_ontology()
    errors: list[str] = []
    if not isinstance(graph, dict):
        return {"ok": False, "errors": ["graph:must_be_object"], "checks": _checks()}

    if graph.get("schema_version") != 1:
        errors.append("schema_version:must_be_1")
    if graph.get("write_policy") != "read_only":
        errors.append("write_policy:must_be_read_only")

    metadata = graph.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("metadata:must_be_object")
    else:
        if metadata.get("source_boundary") != "raw_source_bodies_excluded":
            errors.append("metadata.source_boundary:raw_source_bodies_excluded_required")
        if metadata.get("generated_view_policy") != "html_is_review_only":
            errors.append("metadata.generated_view_policy:html_is_review_only_required")

    nodes = graph.get("nodes")
    edges = graph.get("edges")
    observations = graph.get("observations", [])
    if not isinstance(nodes, list):
        errors.append("nodes:must_be_list")
        nodes = []
    if not isinstance(edges, list):
        errors.append("edges:must_be_list")
        edges = []
    if not isinstance(observations, list):
        errors.append("observations:must_be_list")
        observations = []

    if len(nodes) > GRAPH_LIMITS["max_nodes"]:
        errors.append("nodes:count_limit_exceeded")
    if len(edges) > GRAPH_LIMITS["max_edges"]:
        errors.append("edges:count_limit_exceeded")
    if len(observations) > GRAPH_LIMITS["max_observations"]:
        errors.append("observations:count_limit_exceeded")

    _reject_nested_forbidden_keys(graph, "", errors)
    observation_ids = _validate_observations(observations, ontology, errors)
    node_ids = _validate_nodes(nodes, ontology, observation_ids, errors)
    _validate_edges(edges, node_ids, ontology, observation_ids, errors)
    errors.extend(validate_redaction(json.dumps(graph, sort_keys=True)))

    return {"ok": not errors, "errors": _unique(errors), "checks": _checks()}


def _validate_nodes(
    nodes: list[Any],
    ontology: dict[str, Any],
    observation_ids: set[str],
    errors: list[str],
) -> set[str]:
    allowed_types = set(str(item) for item in ontology.get("node_types", []))
    allowed_status = set(str(item) for item in ontology.get("status_values", []))
    language_support = ontology.get("language_support") if isinstance(ontology.get("language_support"), dict) else {}
    ids: set[str] = set()
    for index, node in enumerate(nodes):
        label = f"nodes[{index}]"
        if not isinstance(node, dict):
            errors.append("node:must_be_object")
            continue
        _reject_forbidden_keys(node, "node", errors)
        node_id = _string(node.get("id"))
        if not node_id:
            errors.append("node.id:required")
        elif node_id in ids:
            errors.append("node.id:duplicate")
        else:
            ids.add(node_id)
        if _string(node.get("type")) not in allowed_types:
            errors.append("node.type:unknown")
        if _string(node.get("status") or "current") not in allowed_status:
            errors.append("node.status:unknown")
        if len(_string(node.get("label"))) > GRAPH_LIMITS["max_label_chars"]:
            errors.append("node.label:too_long")
        language = _string(node.get("language") or "unknown")
        if language not in language_support:
            errors.append("node.language:unknown")
        path = _string(node.get("path"))
        if path and _unsafe_relative_path(path):
            errors.append("node.path:unsafe")
        spans = node.get("source_spans", [])
        if spans and not isinstance(spans, list):
            errors.append("node.source_spans:must_be_list")
        for span in spans if isinstance(spans, list) else []:
            _validate_source_span(span, errors)
        node_observations = node.get("observation_ids", [])
        if not isinstance(node_observations, list):
            errors.append(f"{label}.observation_ids:must_be_list")
        else:
            for observation_id in node_observations:
                if observation_id not in observation_ids:
                    errors.append("node.observation_ids:unknown_observation")
    return ids


def _validate_edges(
    edges: list[Any],
    node_ids: set[str],
    ontology: dict[str, Any],
    observation_ids: set[str],
    errors: list[str],
) -> None:
    allowed_types = set(str(item) for item in ontology.get("edge_types", []))
    allowed_confidence = set(str(item) for item in ontology.get("confidence_levels", []))
    allowed_status = set(str(item) for item in ontology.get("status_values", []))
    ids: set[str] = set()
    for edge in edges:
        if not isinstance(edge, dict):
            errors.append("edge:must_be_object")
            continue
        _reject_forbidden_keys(edge, "edge", errors)
        edge_id = _string(edge.get("id"))
        if not edge_id:
            errors.append("edge.id:required")
        elif edge_id in ids:
            errors.append("edge.id:duplicate")
        else:
            ids.add(edge_id)
        if _string(edge.get("type")) not in allowed_types:
            errors.append("edge.type:unknown")
        if _string(edge.get("confidence") or "unsupported") not in allowed_confidence:
            errors.append("edge.confidence:unknown")
        if _string(edge.get("status") or "current") not in allowed_status:
            errors.append("edge.status:unknown")
        if edge.get("source") not in node_ids:
            errors.append("edge.source:unknown_node")
        if edge.get("target") not in node_ids:
            errors.append("edge.target:unknown_node")
        edge_observations = edge.get("observation_ids", [])
        if not isinstance(edge_observations, list):
            errors.append("edge.observation_ids:must_be_list")
        else:
            for observation_id in edge_observations:
                if observation_id not in observation_ids:
                    errors.append("edge.observation_ids:unknown_observation")


def _validate_observations(observations: list[Any], ontology: dict[str, Any], errors: list[str]) -> set[str]:
    allowed_confidence = set(str(item) for item in ontology.get("confidence_levels", []))
    ids: set[str] = set()
    for observation in observations:
        if not isinstance(observation, dict):
            errors.append("observation:must_be_object")
            continue
        _reject_forbidden_keys(observation, "observation", errors)
        observation_id = _string(observation.get("id"))
        if not observation_id:
            errors.append("observation.id:required")
        elif observation_id in ids:
            errors.append("observation.id:duplicate")
        else:
            ids.add(observation_id)
        if _unsafe_relative_path(_string(observation.get("relative_path"))):
            errors.append("observation.relative_path:unsafe")
        fingerprint = _string(observation.get("fingerprint"))
        if fingerprint and not _DIGEST_PATTERN.match(fingerprint):
            errors.append("observation.fingerprint:invalid")
        span = observation.get("span")
        if span is not None:
            _validate_span(span, errors, "observation.span")
        for key in ["scan_id", "subject_id", "extractor", "confidence", "redaction_status"]:
            if not _string(observation.get(key)):
                errors.append(f"observation.{key}:required")
        if _string(observation.get("confidence")) and _string(observation.get("confidence")) not in allowed_confidence:
            errors.append("observation.confidence:unknown")
        if observation.get("raw_source_status") != "excluded":
            errors.append("observation.raw_source_status:must_be_excluded")
    return ids


def _validate_source_span(span: Any, errors: list[str]) -> None:
    if not isinstance(span, dict):
        errors.append("source_span:must_be_object")
        return
    if _unsafe_relative_path(_string(span.get("relative_path"))):
        errors.append("source_span.relative_path:unsafe")
    fingerprint = _string(span.get("fingerprint"))
    if fingerprint and not _DIGEST_PATTERN.match(fingerprint):
        errors.append("source_span.fingerprint:invalid")
    _validate_span(span, errors, "source_span")


def _validate_span(span: Any, errors: list[str], label: str) -> None:
    if not isinstance(span, dict):
        errors.append(f"{label}:must_be_object")
        return
    start = span.get("start_line")
    end = span.get("end_line")
    if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start:
        errors.append(f"{label}:invalid_lines")


def _reject_forbidden_keys(value: dict[str, Any], prefix: str, errors: list[str]) -> None:
    for key in _FORBIDDEN_SOURCE_KEYS:
        if key in value:
            errors.append(f"{prefix}.{key}:forbidden")
            errors.extend(validate_redaction(str(value.get(key))))
    if "raw_source" in value:
        errors.append("node.raw_source:forbidden")


def _reject_nested_forbidden_keys(value: Any, path: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            next_path = f"{path}.{key}" if path else str(key)
            if key in _FORBIDDEN_SOURCE_KEYS:
                errors.append(f"{next_path}:forbidden")
                errors.extend(validate_redaction(str(item)))
            _reject_nested_forbidden_keys(item, next_path, errors)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_nested_forbidden_keys(item, f"{path}[{index}]", errors)


def _unsafe_relative_path(value: str) -> bool:
    if not value:
        return True
    path = Path(value)
    windows_path = PureWindowsPath(value)
    return (
        path.is_absolute()
        or bool(path.drive)
        or bool(path.root)
        or windows_path.is_absolute()
        or bool(windows_path.drive)
        or bool(windows_path.root)
        or ".." in path.parts
        or ".." in windows_path.parts
    )


def _checks() -> list[str]:
    return [
        "schema version is stable",
        "write policy is read-only",
        "controlled ontology terms validate",
        "node and edge bounds validate",
        "relative paths validate",
        "raw source bodies are forbidden",
        "redaction validates",
    ]


def _string(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _unique(items: list[str]) -> list[str]:
    return sorted(set(items))
