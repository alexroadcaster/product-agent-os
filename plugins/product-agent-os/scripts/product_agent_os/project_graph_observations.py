"""Observation lineage helpers for project code graph artifacts."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def build_observation_record(
    *,
    scan_id: str,
    relative_path: str,
    span: dict[str, int] | None,
    fingerprint: str,
    extractor: str,
    confidence: str,
    redaction_status: str,
    subject_id: str,
) -> dict[str, Any]:
    """Build a deterministic observation record without storing source bodies."""

    normalized_span = {
        "start_line": int((span or {}).get("start_line") or 1),
        "end_line": int((span or {}).get("end_line") or (span or {}).get("start_line") or 1),
    }
    seed = {
        "scan_id": scan_id,
        "relative_path": relative_path,
        "span": normalized_span,
        "fingerprint": fingerprint,
        "extractor": extractor,
        "confidence": confidence,
        "subject_id": subject_id,
    }
    return {
        "id": "obs:" + _digest(seed)[:24],
        "scan_id": scan_id,
        "subject_id": subject_id,
        "relative_path": relative_path,
        "span": normalized_span,
        "fingerprint": fingerprint,
        "extractor": extractor,
        "confidence": confidence,
        "redaction_status": redaction_status,
        "raw_source_status": "excluded",
    }


def diff_observation_lineage(
    previous_graph: dict[str, Any],
    current_graph: dict[str, Any],
    *,
    scan_id: str,
) -> dict[str, Any]:
    """Describe edge lineage changes without silently erasing removed edges."""

    previous_edges = _edge_map(previous_graph)
    current_edges = _edge_map(current_graph)
    invalidated: list[dict[str, Any]] = []
    superseded: list[dict[str, Any]] = []
    new_edges: list[dict[str, Any]] = []

    for edge_id in sorted(previous_edges):
        previous = previous_edges[edge_id]
        current = current_edges.get(edge_id)
        if current is None:
            invalidated.append(_edge_delta(edge_id, previous, scan_id, "invalidated"))
        elif _edge_fingerprint(previous) != _edge_fingerprint(current):
            superseded.append(_edge_delta(edge_id, previous, scan_id, "superseded", current_edge=current))

    for edge_id in sorted(current_edges):
        if edge_id not in previous_edges:
            new_edges.append(_edge_delta(edge_id, current_edges[edge_id], scan_id, "new"))

    status = "changed" if invalidated or superseded or new_edges else "unchanged"
    return {
        "schema_version": 1,
        "scan_id": scan_id,
        "status": status,
        "invalidated_edges": invalidated,
        "superseded_edges": superseded,
        "new_edges": new_edges,
    }


def _edge_map(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(edge.get("id")): edge
        for edge in graph.get("edges", [])
        if isinstance(edge, dict) and edge.get("id")
    }


def _edge_delta(
    edge_id: str,
    edge: dict[str, Any],
    scan_id: str,
    status: str,
    *,
    current_edge: dict[str, Any] | None = None,
) -> dict[str, Any]:
    item = {
        "edge_id": edge_id,
        "scan_id": scan_id,
        "status": status,
        "source": str(edge.get("source") or ""),
        "target": str(edge.get("target") or ""),
        "type": str(edge.get("type") or ""),
        "previous_observation_ids": list(edge.get("observation_ids") or []),
    }
    if current_edge is not None:
        item["current_observation_ids"] = list(current_edge.get("observation_ids") or [])
    return item


def _edge_fingerprint(edge: dict[str, Any]) -> str:
    explicit = edge.get("fingerprint")
    if isinstance(explicit, str) and explicit:
        return explicit
    return _digest(
        {
            "source": edge.get("source"),
            "target": edge.get("target"),
            "type": edge.get("type"),
            "confidence": edge.get("confidence"),
            "observation_ids": edge.get("observation_ids"),
        }
    )


def _digest(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
