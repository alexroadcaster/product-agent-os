"""Structured non-source-body overlays for project graph artifacts."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from product_agent_os.project_graph_observations import build_observation_record


MAX_STRUCTURED_CHUNKS_PER_FILE = 100
MAX_ALIAS_RECORDS = 100
MAX_OVERLAY_FILE_BYTES = 1_000_000
_FORBIDDEN_RAW_KEYS = {"raw_source", "source_body", "raw_body", "content", "raw_prompt", "raw_tool_output"}


def build_structured_chunks(
    relative_path: str,
    text: str,
    *,
    fingerprint: str,
    max_chunks: int = MAX_STRUCTURED_CHUNKS_PER_FILE,
) -> dict[str, Any]:
    """Extract bounded structural nodes from text without returning raw body content."""

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    lowered = relative_path.lower()
    if lowered.endswith((".md", ".markdown")):
        nodes.extend(_markdown_heading_nodes(relative_path, text, fingerprint))
        if not nodes and _markdown_reference_targets(text):
            nodes.append(
                _node(
                    f"chunk:{relative_path}:key:api",
                    node_type="markdown_page",
                    label="markdown references",
                    language="markdown",
                    path=relative_path,
                    source_kind="markdown_reference",
                    extractor="structured_markdown_reference",
                    span=_span(relative_path, 1, 1, fingerprint),
                )
            )
        nodes.extend(_diagram_nodes(relative_path, text, fingerprint))
    elif lowered.endswith((".plantuml", ".puml")):
        nodes.extend(_standalone_plantuml_nodes(relative_path, text, fingerprint))
    elif "openapi" in lowered or "swagger" in lowered:
        nodes.extend(_openapi_operation_nodes(relative_path, text, fingerprint))
    elif "asyncapi" in lowered:
        nodes.extend(_asyncapi_channel_nodes(relative_path, text, fingerprint))
    elif lowered.endswith(".dbml"):
        nodes.extend(_dbml_table_nodes(relative_path, text, fingerprint))
    elif lowered.endswith(".sql"):
        nodes.extend(_sql_table_nodes(relative_path, text, fingerprint))
    elif lowered.endswith((".json", ".yaml", ".yml")):
        nodes.extend(_top_level_key_nodes(relative_path, text, fingerprint))

    if lowered.endswith((".md", ".markdown")):
        node_ids = [node["id"] for node in nodes if node["id"].startswith(f"chunk:{relative_path}:")]
        reference_targets = _markdown_reference_targets(text)
        for source_id in node_ids[:1]:
            for target in reference_targets:
                edges.append(
                    {
                        "type": "references",
                        "source": source_id,
                        "target_path": target,
                        "line": 1,
                        "confidence": "verified",
                    }
                )

    visible_nodes = nodes[:max_chunks]
    return {
        "nodes": visible_nodes,
        "edges": edges,
        "truncated": len(nodes) > len(visible_nodes),
        "omitted_count": max(0, len(nodes) - len(visible_nodes)),
    }


def build_structured_overlays(
    root: Path,
    manifest_files: list[dict[str, Any]],
    *,
    scan_id: str,
) -> dict[str, Any]:
    """Build docs/contracts/schema/diagram overlay graph elements."""

    file_paths = {str(item["relative_path"]) for item in manifest_files}
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []
    summary = {
        "markdown_sections": 0,
        "diagrams": 0,
        "openapi_operations": 0,
        "asyncapi_channels": 0,
        "dbml_tables": 0,
        "sql_tables": 0,
        "config_keys": 0,
        "truncated_files": 0,
        "omitted_chunks": 0,
    }
    for item in sorted(manifest_files, key=lambda value: str(value["relative_path"])):
        relative_path = str(item["relative_path"])
        if not _overlay_candidate(relative_path) or int(item.get("size_bytes") or 0) > MAX_OVERLAY_FILE_BYTES:
            continue
        try:
            text = (root / relative_path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        chunks = build_structured_chunks(relative_path, text, fingerprint=str(item["fingerprint"]))
        if chunks["truncated"]:
            summary["truncated_files"] += 1
            summary["omitted_chunks"] += int(chunks["omitted_count"])
        for node in chunks["nodes"]:
            observation = _observation(
                scan_id,
                subject_id=node["id"],
                relative_path=relative_path,
                line=int(node["source_spans"][0]["start_line"]),
                fingerprint=str(item["fingerprint"]),
                extractor=str(node["metadata"]["extractor"]),
                confidence="verified" if node["status"] == "current" else "unsupported",
            )
            observations.append(observation)
            node["observation_ids"] = [observation["id"]]
            nodes.append(node)
            summary[_summary_key(node)] += 1
            edge, edge_observation = _edge(
                scan_id,
                edge_type="contains",
                source=f"file:{relative_path}",
                target=node["id"],
                relative_path=relative_path,
                line=int(node["source_spans"][0]["start_line"]),
                fingerprint=str(item["fingerprint"]),
                extractor=str(node["metadata"]["extractor"]),
                confidence="verified" if node["status"] == "current" else "unsupported",
            )
            edges.append(edge)
            observations.append(edge_observation)
        for reference in chunks["edges"]:
            target_path = _normalize_reference(relative_path, str(reference["target_path"]))
            if target_path not in file_paths:
                continue
            edge, observation = _edge(
                scan_id,
                edge_type="references",
                source=str(reference["source"]),
                target=f"file:{target_path}",
                relative_path=relative_path,
                line=int(reference["line"]),
                fingerprint=str(item["fingerprint"]),
                extractor="structured_markdown_reference",
                confidence=str(reference["confidence"]),
            )
            edges.append(edge)
            observations.append(observation)

    return {
        "nodes": nodes,
        "edges": edges,
        "observations": observations,
        "metadata": {
            "structured_overlay_summary": summary,
        },
    }


def build_partition_alias_readiness_metadata(manifest: dict[str, Any]) -> dict[str, Any]:
    """Build bounded partition, alias and readiness summaries for graph metadata."""

    files = manifest.get("files", []) if isinstance(manifest.get("files"), list) else []
    partitions = _partitions(files)
    aliases = _aliases(files)
    return {
        "partitions": partitions,
        "alias_ledger": {
            "policy": "canonical_ids_prevent_duplicate_context",
            "aliases": aliases[:MAX_ALIAS_RECORDS],
            "omitted_count": max(0, len(aliases) - MAX_ALIAS_RECORDS),
        },
        "readiness_summary": {
            "status": "present_unverified",
            "policy": "detection_only_does_not_verify_readiness",
            "methodology_gates": _methodology_gates(files)[:20],
            "accepted_gaps": [],
            "evidence_depth": "bounded",
        },
    }


def _markdown_heading_nodes(relative_path: str, text: str, fingerprint: str) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    seen: dict[str, int] = {}
    for index, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            continue
        title = match.group(2).strip()
        slug = _unique_slug(_safe_slug(title, fallback="redacted-heading"), seen)
        nodes.append(
            _node(
                f"chunk:{relative_path}:heading:{slug}",
                node_type="markdown_page",
                label=_safe_label(title, fallback=f"heading:{slug}"),
                language="markdown",
                path=relative_path,
                source_kind="markdown_heading",
                extractor="structured_markdown_heading",
                span=_span(relative_path, index, index, fingerprint),
            )
        )
    return nodes


def _diagram_nodes(relative_path: str, text: str, fingerprint: str) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    counters = {"mermaid": 0, "plantuml": 0}
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        fence = re.match(r"^```\s*(mermaid|plantuml)\s*$", lines[index].strip(), re.IGNORECASE)
        if not fence:
            index += 1
            continue
        kind = fence.group(1).lower()
        start = index + 1
        end = start
        cursor = index + 1
        while cursor < len(lines):
            if lines[cursor].strip().startswith("```"):
                end = cursor + 1
                break
            cursor += 1
        counters[kind] += 1
        nodes.append(
            _node(
                f"diagram:{relative_path}:{kind}:{counters[kind]}",
                node_type="diagram",
                label=f"{kind} diagram {counters[kind]}",
                language="markdown",
                path=relative_path,
                source_kind=f"{kind}_diagram",
                extractor=f"structured_{kind}_diagram",
                span=_span(relative_path, start, end, fingerprint),
            )
        )
        index = max(cursor + 1, index + 1)
    return nodes


def _standalone_plantuml_nodes(relative_path: str, text: str, fingerprint: str) -> list[dict[str, Any]]:
    stripped = text.lstrip()
    if not stripped.startswith("@startuml"):
        return []
    return [
        _node(
            f"diagram:{relative_path}:plantuml:1",
            node_type="diagram",
            label="plantuml diagram 1",
            language="plantuml",
            path=relative_path,
            source_kind="plantuml_diagram",
            extractor="structured_plantuml_diagram",
            span=_span(relative_path, 1, max(1, len(text.splitlines()) or 1), fingerprint),
        )
    ]


def _openapi_operation_nodes(relative_path: str, text: str, fingerprint: str) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.search(r"\boperationId:\s*['\"]?([A-Za-z0-9_.-]+)", line)
        if match:
            operation = match.group(1).strip("'\"")
            operation_slug = _safe_identifier(operation, fallback="openapi-operation")
            nodes.append(
                _node(
                    f"chunk:{relative_path}:operation:{operation_slug}",
                    node_type="contract",
                    label=_safe_label(operation, fallback="openapi_operation"),
                    language="yaml" if relative_path.endswith((".yaml", ".yml")) else "json",
                    path=relative_path,
                    source_kind="openapi_operation",
                    extractor="structured_openapi_operation",
                    span=_span(relative_path, line_number, line_number, fingerprint),
                )
            )
    if not nodes and relative_path.endswith(".json"):
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return nodes
        for path_item in (payload.get("paths") or {}).values():
            if not isinstance(path_item, dict):
                continue
            for operation in path_item.values():
                if isinstance(operation, dict) and isinstance(operation.get("operationId"), str):
                    operation_id = operation["operationId"]
                    operation_slug = _safe_identifier(operation_id, fallback="openapi-operation")
                    nodes.append(
                        _node(
                            f"chunk:{relative_path}:operation:{operation_slug}",
                            node_type="contract",
                            label=_safe_label(operation_id, fallback="openapi_operation"),
                            language="json",
                            path=relative_path,
                            source_kind="openapi_operation",
                            extractor="structured_openapi_operation",
                            span=_span(relative_path, 1, 1, fingerprint),
                        )
                    )
    return nodes


def _asyncapi_channel_nodes(relative_path: str, text: str, fingerprint: str) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    in_channels = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped == "channels:":
            in_channels = True
            continue
        if in_channels and re.match(r"^\s{2}[A-Za-z0-9_.-]+:\s*$", line):
            channel = stripped[:-1]
            channel_slug = _safe_slug(channel, fallback="asyncapi-channel")
            nodes.append(
                _node(
                    f"chunk:{relative_path}:channel:{channel_slug}",
                    node_type="contract",
                    label=_safe_label(channel, fallback="asyncapi_channel"),
                    language="yaml",
                    path=relative_path,
                    source_kind="asyncapi_channel",
                    extractor="structured_asyncapi_channel",
                    span=_span(relative_path, line_number, line_number, fingerprint),
                )
            )
    return nodes


def _dbml_table_nodes(relative_path: str, text: str, fingerprint: str) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^\s*Table\s+([A-Za-z0-9_.-]+)", line)
        if match:
            table = match.group(1)
            table_slug = _safe_slug(table, fallback="dbml-table")
            nodes.append(
                _node(
                    f"chunk:{relative_path}:table:{table_slug}",
                    node_type="schema",
                    label=_safe_label(table, fallback="dbml_table"),
                    language="dbml",
                    path=relative_path,
                    source_kind="dbml_table",
                    extractor="structured_dbml_table",
                    span=_span(relative_path, line_number, line_number, fingerprint),
                )
            )
    return nodes


def _sql_table_nodes(relative_path: str, text: str, fingerprint: str) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^\s*CREATE\s+TABLE\s+([A-Za-z0-9_.-]+)", line, re.IGNORECASE)
        if match:
            table = match.group(1)
            table_slug = _safe_slug(table, fallback="sql-table")
            nodes.append(
                _node(
                    f"chunk:{relative_path}:table:{table_slug}",
                    node_type="schema",
                    label=_safe_label(table, fallback="sql_table"),
                    language="sql",
                    path=relative_path,
                    source_kind="sql_table",
                    extractor="structured_sql_table",
                    span=_span(relative_path, line_number, line_number, fingerprint),
                )
            )
    return nodes


def _top_level_key_nodes(relative_path: str, text: str, fingerprint: str) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    if relative_path.endswith(".json"):
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return nodes
        if isinstance(payload, dict):
            for key in sorted(payload)[:MAX_STRUCTURED_CHUNKS_PER_FILE]:
                nodes.append(
                    _node(
                        f"chunk:{relative_path}:key:{_safe_slug(str(key), fallback='json-key')}",
                        node_type="schema",
                        label=_safe_label(str(key), fallback="json_key"),
                        language="json",
                        path=relative_path,
                        source_kind="json_key",
                        extractor="structured_json_key",
                        span=_span(relative_path, 1, 1, fingerprint),
                    )
                )
        return nodes
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^([A-Za-z0-9_.-]+):\s*", line)
        if not match:
            continue
        key = match.group(1)
        nodes.append(
            _node(
                f"chunk:{relative_path}:key:{_safe_slug(key, fallback='yaml-key')}",
                node_type="schema",
                label=_safe_label(key, fallback="yaml_key"),
                language="yaml",
                path=relative_path,
                source_kind="yaml_key",
                extractor="structured_yaml_key",
                span=_span(relative_path, line_number, line_number, fingerprint),
            )
        )
    return nodes


def _markdown_reference_targets(text: str) -> list[str]:
    targets: list[str] = []
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).replace("\\", "/").split("#", 1)[0].strip()
        if target and "://" not in target and not _contains_local_path(target):
            targets.append(target)
    return targets


def _normalize_reference(relative_path: str, target: str) -> str:
    target = target.replace("\\", "/")
    base = Path(relative_path).parent
    normalized = (base / target).as_posix()
    parts: list[str] = []
    for part in normalized.split("/"):
        if part in {"", "."}:
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return "/".join(parts)


def _partitions(files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[str, int] = {"workspace": 0, "worktree": 0}
    for item in files:
        scope = _partition_scope(str(item.get("relative_path") or ""), bool(item.get("generated")))
        counts[scope] = counts.get(scope, 0) + 1
        counts["workspace"] += 1
    return [
        {"id": f"partition:{scope}", "scope": scope, "file_count": count, "status": "present_unverified"}
        for scope, count in sorted(counts.items())
        if count or scope == "worktree"
    ]


def _aliases(files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    aliases: list[dict[str, Any]] = []
    canonical_names = {"openapi.yaml", "openapi.yml", "asyncapi.yaml", "asyncapi.yml", "schema.dbml"}
    for item in files:
        relative_path = str(item.get("relative_path") or "")
        name = Path(relative_path).name
        if name in canonical_names:
            aliases.append(
                {
                    "alias": name,
                    "canonical_id": f"file:{relative_path}",
                    "decision": "canonical",
                    "reason": "recognized structured project graph artifact",
                }
            )
    return aliases


def _methodology_gates(files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gates: dict[str, dict[str, Any]] = {}
    for item in files:
        relative_path = str(item.get("relative_path") or "")
        lowered = relative_path.lower()
        if "openapi" in lowered or "asyncapi" in lowered:
            gates["api_integrations"] = {
                "gate": "api_integrations_contract_present",
                "status": "present_unverified",
                "evidence": "contract artifact detected",
            }
        if lowered.endswith((".dbml", ".sql")):
            gates["database_data"] = {
                "gate": "database_data_contract_present",
                "status": "present_unverified",
                "evidence": "schema artifact detected",
            }
        if lowered.endswith((".md", ".markdown")):
            gates.setdefault(
                "docs_as_code",
                {
                    "gate": "docs_as_code_impact",
                    "status": "present_unverified",
                    "evidence": "documentation artifact detected",
                },
            )
    return [gates[key] for key in sorted(gates)]


def _overlay_candidate(relative_path: str) -> bool:
    lowered = relative_path.lower()
    return lowered.endswith((".md", ".markdown", ".yaml", ".yml", ".json", ".dbml", ".sql", ".plantuml", ".puml"))


def _summary_key(node: dict[str, Any]) -> str:
    source_kind = node.get("metadata", {}).get("source_kind")
    return {
        "markdown_heading": "markdown_sections",
        "mermaid_diagram": "diagrams",
        "plantuml_diagram": "diagrams",
        "openapi_operation": "openapi_operations",
        "asyncapi_channel": "asyncapi_channels",
        "dbml_table": "dbml_tables",
        "sql_table": "sql_tables",
        "json_key": "config_keys",
        "yaml_key": "config_keys",
    }.get(str(source_kind), "config_keys")


def _node(
    node_id: str,
    *,
    node_type: str,
    label: str,
    language: str,
    path: str,
    source_kind: str,
    extractor: str,
    span: dict[str, Any],
) -> dict[str, Any]:
    return {
        "id": node_id,
        "type": node_type,
        "label": label[:160],
        "status": "current",
        "language": language,
        "path": path,
        "source_spans": [span],
        "observation_ids": [],
        "metadata": {
            "source_kind": source_kind,
            "extractor": extractor,
            "parse_status": "structured",
            "raw_source_status": "excluded",
        },
    }


def _span(relative_path: str, start_line: int, end_line: int, fingerprint: str) -> dict[str, Any]:
    return {
        "relative_path": relative_path,
        "start_line": start_line,
        "end_line": max(start_line, end_line),
        "fingerprint": fingerprint,
    }


def _edge(
    scan_id: str,
    *,
    edge_type: str,
    source: str,
    target: str,
    relative_path: str,
    line: int,
    fingerprint: str,
    extractor: str,
    confidence: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    edge_id = _edge_id(edge_type, source, target, relative_path=relative_path, line=line)
    observation = _observation(
        scan_id,
        subject_id=edge_id,
        relative_path=relative_path,
        line=max(1, line),
        fingerprint=fingerprint,
        extractor=extractor,
        confidence=confidence,
    )
    return (
        {
            "id": edge_id,
            "type": edge_type,
            "source": source,
            "target": target,
            "confidence": confidence,
            "status": "current",
            "observation_ids": [observation["id"]],
            "fingerprint": fingerprint,
        },
        observation,
    )


def _observation(
    scan_id: str,
    *,
    subject_id: str,
    relative_path: str,
    line: int,
    fingerprint: str,
    extractor: str,
    confidence: str,
) -> dict[str, Any]:
    return build_observation_record(
        scan_id=scan_id,
        relative_path=relative_path,
        span={"start_line": line, "end_line": line},
        fingerprint=fingerprint,
        extractor=extractor,
        confidence=confidence,
        redaction_status="redacted",
        subject_id=subject_id,
    )


def _edge_id(edge_type: str, source: str, target: str, *, relative_path: str, line: int) -> str:
    seed = json.dumps(
        {"type": edge_type, "source": source, "target": target, "relative_path": relative_path, "line": line},
        sort_keys=True,
    )
    return "edge:" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24]


def _partition_scope(relative_path: str, generated: bool) -> str:
    if generated:
        return "artifact"
    lowered = relative_path.lower()
    if lowered.startswith(("docs/", "doc/")) or lowered.endswith((".md", ".markdown")):
        return "docs"
    if "openapi" in lowered or "asyncapi" in lowered:
        return "contracts"
    if lowered.endswith((".dbml", ".sql")):
        return "data"
    if lowered.startswith("packages/"):
        return "package:" + lowered.split("/")[1]
    return "repository"


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_.-]+", "-", value.strip().lower()).strip("-")
    return slug or "section"


def _unique_slug(slug: str, seen: dict[str, int]) -> str:
    count = seen.get(slug, 0) + 1
    seen[slug] = count
    return slug if count == 1 else f"{slug}-{count}"


def _safe_slug(value: str, *, fallback: str) -> str:
    if _label_needs_redaction(value):
        return fallback
    return _slug(value)


def _safe_identifier(value: str, *, fallback: str) -> str:
    if _label_needs_redaction(value):
        return fallback
    identifier = re.sub(r"[^a-zA-Z0-9_.-]+", "-", value.strip()).strip("-")
    return identifier or fallback


def _safe_label(value: str, *, fallback: str) -> str:
    if not value:
        return fallback
    if _label_needs_redaction(value):
        return fallback
    return value[:160]


def _label_needs_redaction(value: str) -> bool:
    if _contains_local_path(value):
        return True
    lowered = value.lower()
    if any(term in lowered for term in ["secret", "token", "password", "api_key", "apikey", "private key"]):
        return True
    if re.search(r"\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)[A-Z0-9_]*\b", value):
        return True
    return False


def _contains_local_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    if re.search(r"\b[A-Za-z]:/", normalized):
        return True
    if normalized.startswith(("//", "file:/")):
        return True
    return bool(re.search(r"(^|\s)/(Users|home|private|Volumes|mnt|tmp|var)/", normalized))
