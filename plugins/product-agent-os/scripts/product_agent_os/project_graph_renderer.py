"""Offline HTML cockpit renderer for Product-Agent OS project graphs."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path, PureWindowsPath
from typing import Any

from codex_runtime_runner.redaction import redact_payload, validate_redaction
from product_agent_os.offline_artifact_safety import (
    GENERATED_VIEW_ONLY_TEXT,
    escape_html,
    json_for_html_text,
    prepare_offline_payload,
    validate_offline_artifact,
)
from product_agent_os.project_cockpit_model import build_project_cockpit_model
from product_agent_os.project_graph_sanitization import safe_relative_path_text, sanitize_graph_text
from product_agent_os.project_graph_visual_model import build_project_graph_visual_model
from product_agent_os.stage_manifest import (
    MANIFEST_NAME,
    build_stage_manifest,
    content_digest,
    file_digest,
    load_stage_manifest,
    write_stage_manifest,
)


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = PLUGIN_ROOT / "assets" / "templates" / "project-graph"
PROJECT_COCKPIT_HTML_TARGET = ".codex/product-agent-os/project-cockpit.html"
PROJECT_COCKPIT_JSON_TARGET = ".codex/product-agent-os/project-cockpit.json"
PROJECT_COCKPIT_TARGETS = (PROJECT_COCKPIT_HTML_TARGET, PROJECT_COCKPIT_JSON_TARGET)
PROJECT_COCKPIT_MANIFEST_NAME = MANIFEST_NAME
PROJECT_COCKPIT_JSON_BYTE_LIMIT = 120_000
RENDERER_VERSION = "0.1.0"


class ProjectGraphRendererError(RuntimeError):
    pass


def render_project_graph_cockpit(
    graph: dict[str, Any],
    *,
    analysis: dict[str, Any] | None = None,
    query_packets: list[dict[str, Any]] | None = None,
    selected_node_id: str = "",
    active_page: str = "overview",
    section_anchor: str = "",
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Render an offline project graph cockpit without writing files."""

    if not isinstance(graph, dict):
        raise ProjectGraphRendererError("project graph must be an object")
    generated_at_value = generated_at or datetime.now(UTC).replace(microsecond=0).isoformat()
    model = build_project_cockpit_model(
        graph,
        analysis=analysis,
        query_packets=query_packets or [],
        active_page=active_page,
        section_anchor=section_anchor,
    )
    visual_projection = build_project_graph_visual_model(graph, selected_node_id=selected_node_id)
    payload = {
        "schema_version": 1,
        "write_policy": "read_only",
        "generated_at": generated_at_value,
        "generated_view_policy": GENERATED_VIEW_ONLY_TEXT,
        "source_policy": "generated HTML is review output only; graph JSON and source files are evidence",
        "cockpit": model,
        "visual_projection": visual_projection,
        "analysis": _analysis_payload(analysis),
        "query_packets": _query_packets_payload(query_packets or []),
        "visual_qa": _visual_qa_packet(model, visual_projection),
    }
    payload = _neutralize_script_breakouts(payload)
    prepared = prepare_offline_payload(payload, max_json_bytes=PROJECT_COCKPIT_JSON_BYTE_LIMIT)
    safe_payload = prepared["payload"]
    cockpit = safe_payload.get("cockpit") if isinstance(safe_payload.get("cockpit"), dict) else model
    projection = (
        safe_payload.get("visual_projection")
        if isinstance(safe_payload.get("visual_projection"), dict)
        else visual_projection
    )
    html_text = _render_html(cockpit, projection, safe_payload, prepared["json_for_html"])
    validation = _validate_cockpit_content(html_text, prepared["json"], safe_payload)
    return {
        "status": "ready" if validation["ok"] else "blocked",
        "html": html_text,
        "json": prepared["json"],
        "cockpit": cockpit,
        "visual_projection": projection,
        "redaction_summary": prepared["redaction_summary"],
        "validation": validation,
    }


def render_project_graph_cockpit_plan(
    workspace: str | Path,
    graph: dict[str, Any],
    *,
    analysis: dict[str, Any] | None = None,
    query_packets: list[dict[str, Any]] | None = None,
    selected_node_id: str = "",
    active_page: str = "overview",
    section_anchor: str = "",
) -> dict[str, Any]:
    """Build a staged-only cockpit render plan without writing files."""

    return _cockpit_renderer_result(
        Path(workspace).resolve(),
        graph,
        None,
        analysis=analysis,
        query_packets=query_packets or [],
        selected_node_id=selected_node_id,
        active_page=active_page,
        section_anchor=section_anchor,
        write_files=False,
    )


def stage_project_graph_cockpit(
    workspace: str | Path,
    output_dir: str | Path,
    graph: dict[str, Any],
    *,
    analysis: dict[str, Any] | None = None,
    query_packets: list[dict[str, Any]] | None = None,
    selected_node_id: str = "",
    active_page: str = "overview",
    section_anchor: str = "",
) -> dict[str, Any]:
    """Stage cockpit HTML/JSON files under an explicit output directory."""

    workspace_path = Path(workspace).resolve()
    stage_root = Path(output_dir).resolve()
    if stage_root == workspace_path or stage_root.is_relative_to(workspace_path):
        raise ProjectGraphRendererError("stage output directory must be outside workspace")
    if stage_root.exists() and not stage_root.is_dir():
        raise ProjectGraphRendererError("stage output path is not a directory")
    return _cockpit_renderer_result(
        workspace_path,
        graph,
        stage_root,
        analysis=analysis,
        query_packets=query_packets or [],
        selected_node_id=selected_node_id,
        active_page=active_page,
        section_anchor=section_anchor,
        write_files=True,
    )


def validate_project_graph_cockpit_manifest(stage_root: str | Path) -> list[str]:
    """Validate cockpit stage manifest paths and staged file digests."""

    stage_path = Path(stage_root).resolve()
    try:
        manifest = load_stage_manifest(stage_path)
    except ValueError as exc:
        return [str(exc)]

    errors: list[str] = []
    entries = [item for item in manifest.get("files", []) if isinstance(item, dict)]
    targets = {str(item.get("target_path", "")) for item in entries}
    for target in PROJECT_COCKPIT_TARGETS:
        if target not in targets:
            errors.append(f"cockpit target missing from manifest: {target}")
    for item in entries:
        target_path = str(item.get("target_path", ""))
        if target_path not in PROJECT_COCKPIT_TARGETS:
            errors.append(f"unexpected target in cockpit manifest: {target_path}")
            continue
        if item.get("action") == "blocked":
            continue
        staged_path_value = str(item.get("staged_path", ""))
        if _unsafe_relative_path(staged_path_value):
            errors.append(f"staged path escapes stage root: {staged_path_value}")
            continue
        staged_path = (stage_path / Path(staged_path_value)).resolve()
        if not staged_path.is_relative_to(stage_path):
            errors.append(f"staged path escapes stage root: {staged_path_value}")
            continue
        if not staged_path.exists() or not staged_path.is_file():
            errors.append(f"{target_path}: staged file is missing or not a file")
            continue
        expected_digest = str(item.get("digest", ""))
        actual_digest = file_digest(staged_path)
        if expected_digest != actual_digest:
            errors.append(f"{target_path}: staged digest does not match manifest")
    return errors


def _cockpit_renderer_result(
    workspace: Path,
    graph: dict[str, Any],
    stage_root: Path | None,
    *,
    analysis: dict[str, Any] | None,
    query_packets: list[dict[str, Any]],
    selected_node_id: str,
    active_page: str,
    section_anchor: str,
    write_files: bool,
) -> dict[str, Any]:
    rendered = render_project_graph_cockpit(
        graph,
        analysis=analysis,
        query_packets=query_packets,
        selected_node_id=selected_node_id,
        active_page=active_page,
        section_anchor=section_anchor,
    )
    contents = {
        PROJECT_COCKPIT_HTML_TARGET: rendered["html"],
        PROJECT_COCKPIT_JSON_TARGET: rendered["json"] + "\n",
    }
    validation_errors = list(rendered["validation"]["errors"])
    files: list[dict[str, Any]] = []
    warnings: list[str] = []
    blocked: list[str] = []
    action_summary: dict[str, list[str]] = {
        "create": [],
        "update": [],
        "leave_unchanged": [],
        "blocked": [],
    }

    for target_path, content in contents.items():
        _validate_cockpit_target(target_path)
        action, write_policy, file_warnings, file_blocked = _plan_cockpit_file(workspace / Path(target_path), target_path)
        warnings.extend(file_warnings)
        blocked.extend(file_blocked)
        action_summary[action].append(target_path)
        staged_path = _staged_path(stage_root, target_path, action)
        if write_files and action in {"create", "leave_unchanged"}:
            _write_inside_root(stage_root, Path(staged_path), content)
        entry: dict[str, Any] = {
            "key": "project-cockpit-html" if target_path == PROJECT_COCKPIT_HTML_TARGET else "project-cockpit-json",
            "category": "project-graph-cockpit",
            "target_path": target_path,
            "action": action,
            "write_policy": write_policy,
            "staged_path": staged_path,
            "digest": content_digest(content),
        }
        if not write_files:
            entry["content"] = content
        files.append(entry)

    if validation_errors:
        blocked.extend(f"cockpit validation failed: {error}" for error in validation_errors)
    validation_ok = not validation_errors and not blocked
    approval_required = (
        ["explicit approval required before applying staged project graph cockpit to workspace"]
        if any(item["action"] == "create" for item in files)
        else []
    )
    status = "blocked" if not validation_ok else "needs_approval" if approval_required else "ready"
    result = {
        "project_graph_cockpit": {
            "status": status,
            "write_policy": "staged_only",
            "source_of_truth": "project_code_graph_json_and_source_files",
            "targets": list(PROJECT_COCKPIT_TARGETS),
            "warnings": _unique(warnings),
            "blocked": _unique(blocked),
            "redaction_summary": rendered["redaction_summary"],
        },
        "infrastructure_plan": {
            "status": status,
            "workspace": str(workspace),
            "profile": "project-graph-cockpit",
            "detected_stack": [],
            "create": action_summary["create"],
            "update": action_summary["update"],
            "leave_unchanged": action_summary["leave_unchanged"],
            "approval_required": approval_required,
            "warnings": _unique(warnings),
            "blocked": _unique(blocked),
            "questions": [],
        },
        "rendered_artifacts": {
            "mode": "stage" if write_files else "dry-run",
            "root": str(stage_root if stage_root is not None else Path(".product-agent-os") / "project-graph-cockpit"),
            "output_dir": str(stage_root) if stage_root is not None else "",
            "files": files,
            "managed_sections": [],
            "validation": {
                "ok": validation_ok,
                "checks": _validation_checks(),
                "errors": validation_errors,
            },
        },
    }
    if write_files and stage_root is not None:
        manifest = build_stage_manifest(
            workspace=workspace,
            stage_root=stage_root,
            renderer_result=result,
            renderer_version=_renderer_version(),
        )
        manifest_path = write_stage_manifest(stage_root, manifest)
        result["rendered_artifacts"]["manifest_path"] = str(manifest_path)
        manifest_errors = validate_project_graph_cockpit_manifest(stage_root)
        if manifest_errors:
            result["rendered_artifacts"]["validation"]["ok"] = False
            result["rendered_artifacts"]["validation"]["errors"].extend(manifest_errors)
            result["project_graph_cockpit"]["status"] = "blocked"
            result["infrastructure_plan"]["status"] = "blocked"
    return result


def _render_html(
    cockpit: dict[str, Any],
    projection: dict[str, Any],
    payload: dict[str, Any],
    embedded_json: str,
) -> str:
    template = (TEMPLATE_ROOT / "project-cockpit.html").read_text(encoding="utf-8")
    css = (TEMPLATE_ROOT / "project-graph.css").read_text(encoding="utf-8")
    graph_section = _render_graph_section(cockpit, projection)
    code_flow = _render_code_flow(cockpit)
    values = {
        "title": "Product-Agent OS Project Cockpit",
        "generated_at": _text(payload.get("generated_at") or "not available"),
        "generated_view_policy": _text(GENERATED_VIEW_ONLY_TEXT),
        "css": css.rstrip(),
        "nav": _render_nav(cockpit),
        "pages": _render_pages(cockpit, graph_section, code_flow),
        "project_cockpit_json": embedded_json,
    }
    html_text = template
    for key, value in values.items():
        html_text = html_text.replace("{{" + key + "}}", value)
    return html_text


def _render_nav(cockpit: dict[str, Any]) -> str:
    pages = cockpit.get("pages") if isinstance(cockpit.get("pages"), list) else []
    active = str(cockpit.get("active_page") or "overview")
    items = []
    for page in pages:
        if not isinstance(page, dict):
            continue
        page_id = str(page.get("id") or "")
        label = _text(page.get("label") or page_id)
        active_attr = ' aria-current="page"' if page_id == active else ""
        items.append(f'        <a href="#page-{_attr(page_id)}"{active_attr}>{label}</a>')
    return "\n".join(items)


def _render_pages(cockpit: dict[str, Any], graph_section: str, code_flow: str) -> str:
    pages = cockpit.get("pages") if isinstance(cockpit.get("pages"), list) else []
    rendered = []
    for page in pages:
        if not isinstance(page, dict):
            continue
        page_id = str(page.get("id") or "")
        sections_html = "\n".join(_render_section(section, page, graph_section, code_flow) for section in page.get("sections", []))
        rendered.append(
            "      <section class=\"cockpit-page\" "
            f"id=\"page-{_attr(page_id)}\" data-page=\"{_attr(page_id)}\">\n"
            f"        <h2>{_text(page.get('label'))}</h2>\n"
            f"        <p class=\"page-role\">{_text(page.get('role'))}</p>\n"
            f"{_render_page_meta(page)}\n"
            f"{sections_html}\n"
            "      </section>"
        )
    return "\n".join(rendered)


def _render_section(section: dict[str, Any], page: dict[str, Any], graph_section: str, code_flow: str) -> str:
    section_id = str(section.get("id") or "")
    label = _text(section.get("label") or section_id)
    if section_id == "visual-projection":
        body = graph_section
    elif section_id == "code-flow":
        body = code_flow
    elif section_id == "selected-node-evidence":
        body = '<div id="selected-node-evidence" class="evidence-panel" aria-live="polite">Select a node in the Project Map table.</div>'
    elif section_id in {"graph-filters", "fallback-static-view"}:
        body = "<p>Project Map controls and fallback table are available in the Visual Projection section.</p>"
    else:
        body = _section_summary(section_id, page)
    return (
        f"        <section class=\"cockpit-section\" id=\"section-{_attr(section_id)}\">\n"
        f"          <h3>{label}</h3>\n"
        f"          {body}\n"
        "        </section>"
    )


def _render_page_meta(page: dict[str, Any]) -> str:
    boundaries = page.get("approval_boundaries") if isinstance(page.get("approval_boundaries"), list) else []
    actions = page.get("action_surfaces") if isinstance(page.get("action_surfaces"), list) else []
    return (
        "        <div class=\"page-meta\">\n"
        f"          <p><strong>Boundary:</strong> {_text('; '.join(str(item) for item in boundaries[:2]))}</p>\n"
        f"          <p><strong>Actions:</strong> {_text('; '.join(str(item) for item in actions[:5]))}</p>\n"
        "        </div>"
    )


def _section_summary(section_id: str, page: dict[str, Any]) -> str:
    packets = page.get("graph_packets") if isinstance(page.get("graph_packets"), list) else []
    links = page.get("source_links") if isinstance(page.get("source_links"), list) else []
    flags = page.get("stale_flags") if isinstance(page.get("stale_flags"), list) else []
    rows = [
        ("Section source", "graph artifacts and compact generated packets"),
        ("Graph packets", ", ".join(str(packet.get("result_kind", "")) for packet in packets) or "not available"),
        ("Source links", ", ".join(str(link.get("path", "")) for link in links) or "not available"),
        ("Flags", ", ".join(str(flag) for flag in flags) or "none"),
    ]
    row_html = "\n".join(
        f"              <tr><th scope=\"row\">{_text(label)}</th><td>{_text(value)}</td></tr>"
        for label, value in rows
    )
    return (
        f"<table class=\"compact-table\" data-section=\"{_attr(section_id)}\"><tbody>\n"
        f"{row_html}\n"
        "</tbody></table>"
    )


def _render_graph_section(cockpit: dict[str, Any], projection: dict[str, Any]) -> str:
    template = (TEMPLATE_ROOT / "project-graph.html").read_text(encoding="utf-8")
    selected = projection.get("focused_subgraph") if isinstance(projection.get("focused_subgraph"), dict) else {}
    values = {
        "filter_controls": _filter_controls(projection),
        "graph_svg": _render_static_svg(projection),
        "fallback_table": _fallback_table(projection),
        "selected_summary": _selected_summary(selected),
        "performance_summary": _performance_summary(projection),
    }
    html_text = template
    for key, value in values.items():
        html_text = html_text.replace("{{" + key + "}}", value)
    return html_text


def _filter_controls(projection: dict[str, Any]) -> str:
    filters = projection.get("available_filters") if isinstance(projection.get("available_filters"), list) else []
    options = _filter_options(projection)
    controls = [
        '<label class="filter-control">Text <input id="graph-filter-text" data-filter="text" type="search" placeholder="node or edge"></label>'
    ]
    for filter_name in filters:
        if filter_name == "text":
            continue
        option_html = '<option value="">All</option>' + "".join(
            f'<option value="{_attr(option)}">{_text(option)}</option>'
            for option in options.get(str(filter_name), [])
        )
        controls.append(
            f'<label class="filter-control">{_text(str(filter_name).replace("_", " ").title())} '
            f'<select data-filter="{_attr(str(filter_name))}" id="graph-filter-{_attr(str(filter_name).replace("_", "-"))}">'
            f"{option_html}</select></label>"
        )
    commands = "".join(
        f'<button type="button" data-command="{_attr(command)}">{_text(command.title())}</button>'
        for command in projection.get("navigation_commands", [])
        if isinstance(command, str)
    )
    return (
        '<div class="graph-controls" aria-label="Graph filters">'
        + "".join(controls)
        + f'<div class="graph-commands">{commands}</div>'
        + "</div>"
    )


def _filter_options(projection: dict[str, Any]) -> dict[str, list[str]]:
    options: dict[str, set[str]] = {
        "node_type": set(),
        "edge_type": set(),
        "confidence": set(),
        "language": set(),
        "artifact": set(),
        "partition": set(),
        "stale": set(),
    }
    for node in projection.get("nodes", []):
        if not isinstance(node, dict):
            continue
        attrs = node.get("attributes") if isinstance(node.get("attributes"), dict) else {}
        _add_option(options, "node_type", attrs.get("type"))
        _add_option(options, "language", attrs.get("language"))
        _add_option(options, "artifact", attrs.get("path"))
        _add_option(options, "partition", attrs.get("community"))
        _add_option(options, "stale", attrs.get("status"))
    for edge in projection.get("edges", []):
        if not isinstance(edge, dict):
            continue
        attrs = edge.get("attributes") if isinstance(edge.get("attributes"), dict) else {}
        _add_option(options, "edge_type", attrs.get("type"))
        _add_option(options, "confidence", attrs.get("confidence"))
        _add_option(options, "stale", attrs.get("status"))
    return {key: sorted(values)[:50] for key, values in options.items()}


def _add_option(options: dict[str, set[str]], key: str, value: Any) -> None:
    text = str(value or "").strip()
    if text:
        options.setdefault(key, set()).add(text)


def _render_static_svg(projection: dict[str, Any]) -> str:
    nodes = projection.get("nodes") if isinstance(projection.get("nodes"), list) else []
    edges = projection.get("edges") if isinstance(projection.get("edges"), list) else []
    by_id = {str(node.get("key")): node.get("attributes", {}) for node in nodes if isinstance(node, dict)}
    edge_parts = []
    for edge in edges[:300]:
        if not isinstance(edge, dict):
            continue
        source = by_id.get(str(edge.get("source")))
        target = by_id.get(str(edge.get("target")))
        if not isinstance(source, dict) or not isinstance(target, dict):
            continue
        attrs = edge.get("attributes") if isinstance(edge.get("attributes"), dict) else {}
        edge_parts.append(
            f'<line class="graph-edge" data-edge-type="{_attr(attrs.get("type"))}" '
            f'data-confidence="{_attr(attrs.get("confidence"))}" '
            f'data-stale="{_attr(attrs.get("status"))}" data-text="{_attr(edge.get("key"))} {_attr(attrs.get("type"))}" '
            f'x1="{_coord(source.get("x"))}" y1="{_coord(source.get("y"))}" '
            f'x2="{_coord(target.get("x"))}" y2="{_coord(target.get("y"))}" />'
        )
    node_parts = []
    for node in nodes:
        if not isinstance(node, dict):
            continue
        attrs = node.get("attributes") if isinstance(node.get("attributes"), dict) else {}
        node_parts.append(
            f'<g class="graph-node" data-node-id="{_attr(node.get("key"))}" '
            f'data-node-type="{_attr(attrs.get("type"))}" data-language="{_attr(attrs.get("language"))}" '
            f'data-stale="{_attr(attrs.get("status"))}" data-artifact="{_attr(attrs.get("path"))}" '
            f'data-partition="{_attr(attrs.get("community"))}" data-text="{_attr(attrs.get("label"))} {_attr(node.get("key"))}">'
            f'<circle cx="{_coord(attrs.get("x"))}" cy="{_coord(attrs.get("y"))}" '
            f'r="{_radius(attrs.get("size"))}" fill="{_attr(attrs.get("color"))}"></circle>'
            f'<text x="{_coord(float(attrs.get("x") or 0) + 3)}" y="{_coord(float(attrs.get("y") or 0) - 3)}">'
            f'{_text(attrs.get("label"))}</text></g>'
        )
    return (
        '<svg id="graph-canvas-fallback" class="graph-canvas" viewBox="-70 -70 140 140" '
        'role="img" aria-label="Static project graph projection">'
        + "".join(edge_parts)
        + "".join(node_parts)
        + "</svg>"
    )


def _fallback_table(projection: dict[str, Any]) -> str:
    rows = []
    for node in projection.get("nodes", [])[:80]:
        if not isinstance(node, dict):
            continue
        attrs = node.get("attributes") if isinstance(node.get("attributes"), dict) else {}
        rows.append(
            '<tr class="node-row" '
            f'data-node-id="{_attr(node.get("key"))}" data-node-type="{_attr(attrs.get("type"))}" '
            f'data-language="{_attr(attrs.get("language"))}" data-stale="{_attr(attrs.get("status"))}" '
            f'data-artifact="{_attr(attrs.get("path"))}" data-partition="{_attr(attrs.get("community"))}" '
            f'data-text="{_attr(attrs.get("label"))} {_attr(node.get("key"))}">'
            f'<td><code>{_text(node.get("key"))}</code></td>'
            f'<td>{_text(attrs.get("type"))}</td>'
            f'<td>{_text(attrs.get("language"))}</td>'
            f'<td>{_text(attrs.get("status"))}</td>'
            "</tr>"
        )
    return (
        '<table class="graph-fallback-table" aria-label="Static graph node table">'
        "<thead><tr><th>Node</th><th>Type</th><th>Language</th><th>Status</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def _selected_summary(selected: dict[str, Any]) -> str:
    node = selected.get("selected_node") if isinstance(selected.get("selected_node"), dict) else {}
    if not node:
        return "No node selected. Use graph rows to inspect compact evidence."
    return (
        f"Selected {_text(node.get('id'))}; source path {_text(node.get('path') or 'not available')}; "
        "raw source bodies are excluded."
    )


def _performance_summary(projection: dict[str, Any]) -> str:
    budget = projection.get("performance_budget") if isinstance(projection.get("performance_budget"), dict) else {}
    return (
        f"{_text(budget.get('visible_node_count'))} visible nodes, "
        f"{_text(budget.get('visible_edge_count'))} visible edges, "
        f"{_text(budget.get('omitted_node_count'))} omitted nodes."
    )


def _render_code_flow(cockpit: dict[str, Any]) -> str:
    template = (TEMPLATE_ROOT / "project-code-flow.html").read_text(encoding="utf-8")
    code_flow = cockpit.get("code_flow") if isinstance(cockpit.get("code_flow"), dict) else {}
    rows = []
    for item in code_flow.get("module_flows", [])[:50]:
        if not isinstance(item, dict):
            continue
        source = item.get("source") if isinstance(item.get("source"), dict) else {}
        target = item.get("target") if isinstance(item.get("target"), dict) else {}
        rows.append(
            "<tr>"
            f"<td><code>{_text(source.get('id'))}</code></td>"
            f"<td>{_text(item.get('type'))}</td>"
            f"<td><code>{_text(target.get('id'))}</code></td>"
            f"<td>{_text(item.get('confidence'))}</td>"
            "</tr>"
        )
    table = (
        '<table class="compact-table code-flow-table">'
        "<thead><tr><th>Source</th><th>Flow</th><th>Target</th><th>Confidence</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )
    return template.replace("{{code_flow_table}}", table).replace(
        "{{code_flow_boundary}}",
        _text(code_flow.get("source_boundary") or "Code Flow is generated graph orientation only."),
    )


def _analysis_payload(analysis: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(analysis, dict):
        return {"status": "not_available"}
    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "graph_ref": _safe_graph_ref(analysis.get("graph_ref")),
        "hotspots": [_safe_analysis_record(item) for item in _list(analysis.get("hotspots"))[:20]],
        "ambiguous_edge_inventory": [
            _safe_analysis_record(item)
            for item in _list(analysis.get("ambiguous_edge_inventory"))[:20]
        ],
        "unsupported_language_summary": _safe_count_map(analysis.get("unsupported_language_summary")),
        "suggested_agent_questions": [
            _safe_question_record(item)
            for item in _list(analysis.get("suggested_agent_questions"))[:10]
        ],
        "budget": _safe_budget(analysis.get("budget")),
    }


def _safe_graph_ref(value: Any) -> dict[str, Any]:
    graph_ref = value if isinstance(value, dict) else {}
    return {
        "scan_id": sanitize_graph_text(graph_ref.get("scan_id")),
        "node_count": _int(graph_ref.get("node_count")),
        "edge_count": _int(graph_ref.get("edge_count")),
    }


def _safe_analysis_record(value: Any) -> dict[str, Any]:
    item = value if isinstance(value, dict) else {}
    safe = {
        "id": sanitize_graph_text(item.get("id")),
        "source": sanitize_graph_text(item.get("source")),
        "target": sanitize_graph_text(item.get("target")),
        "label": sanitize_graph_text(item.get("label")),
        "type": sanitize_graph_text(item.get("type")),
        "status": sanitize_graph_text(item.get("status")),
        "confidence": sanitize_graph_text(item.get("confidence")),
        "language": sanitize_graph_text(item.get("language")),
        "path": safe_relative_path_text(item.get("path")),
        "degree": _int(item.get("degree")),
        "source_domain": sanitize_graph_text(item.get("source_domain")),
        "target_domain": sanitize_graph_text(item.get("target_domain")),
        "call_name": sanitize_graph_text(item.get("call_name")),
        "safe_next_action": sanitize_graph_text(item.get("safe_next_action")),
    }
    return {key: val for key, val in safe.items() if val not in {"", 0}}


def _safe_question_record(value: Any) -> dict[str, str]:
    item = value if isinstance(value, dict) else {}
    return {
        "id": sanitize_graph_text(item.get("id"))[:120],
        "text": sanitize_graph_text(item.get("text"))[:240],
        "source": sanitize_graph_text(item.get("source"))[:120],
    }


def _safe_count_map(value: Any) -> dict[str, int]:
    source = value if isinstance(value, dict) else {}
    result: dict[str, int] = {}
    for key, count in source.items():
        safe_key = sanitize_graph_text(key)[:80]
        if safe_key:
            result[safe_key] = _int(count)
    return result


def _safe_budget(value: Any) -> dict[str, Any]:
    source = value if isinstance(value, dict) else {}
    allowed = {
        "max_items",
        "truncated",
        "omitted_count",
        "visible_node_count",
        "visible_edge_count",
    }
    result: dict[str, Any] = {}
    for key in allowed:
        if key in source:
            item = source[key]
            result[key] = item if isinstance(item, bool) else _int(item)
    return result


def _query_packets_payload(packets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    compact = []
    for packet in packets[:20]:
        if not isinstance(packet, dict):
            continue
        compact.append(
            {
                "schema_version": 1,
                "write_policy": "read_only",
                "result_kind": str(packet.get("result_kind") or ""),
                "status": str(packet.get("status") or ""),
                "query_id": str(packet.get("query_id") or ""),
                "budget": packet.get("budget", {}),
                "node_count": len(packet.get("nodes", [])) if isinstance(packet.get("nodes"), list) else 0,
                "edge_count": len(packet.get("edges", [])) if isinstance(packet.get("edges"), list) else 0,
            }
        )
    return compact


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _visual_qa_packet(cockpit: dict[str, Any], projection: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "ready",
        "checks": [
            "nonblank graph fallback",
            "no console/network dependency by design",
            "filters present",
            "selected panel present",
            "eight page grouping",
            "local section navigation",
            "desktop and mobile CSS present",
        ],
        "page_count": len(cockpit.get("pages", [])) if isinstance(cockpit.get("pages"), list) else 0,
        "visible_node_count": len(projection.get("nodes", [])) if isinstance(projection.get("nodes"), list) else 0,
    }


def _neutralize_script_breakouts(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _neutralize_script_breakouts(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_neutralize_script_breakouts(item) for item in value]
    if isinstance(value, tuple):
        return [_neutralize_script_breakouts(item) for item in value]
    if isinstance(value, str):
        return (
            value.replace("</script", "[SCRIPT_TAG_REDACTED]")
            .replace("</SCRIPT", "[SCRIPT_TAG_REDACTED]")
            .replace("<script", "[SCRIPT_TAG_REDACTED]")
            .replace("<SCRIPT", "[SCRIPT_TAG_REDACTED]")
        )
    return value


def _validate_cockpit_content(html_text: str, cockpit_json: str, payload: dict[str, Any]) -> dict[str, Any]:
    validation = validate_offline_artifact(
        html_text=html_text,
        embedded_json=cockpit_json,
        payload=payload,
        max_json_bytes=PROJECT_COCKPIT_JSON_BYTE_LIMIT,
    )
    errors: list[str] = list(validation["errors"])
    lower_html = html_text.lower()
    if payload.get("schema_version") != 1:
        errors.append("payload.schema_version:must_be_1")
    if payload.get("write_policy") != "read_only":
        errors.append("payload.write_policy:must_be_read_only")
    for required in [
        'id="page-overview"',
        'id="page-project-map"',
        'id="page-code-intelligence"',
        'id="section-code-flow"',
        'id="graph-canvas-fallback"',
        'id="selected-node-evidence"',
        'data-filter="node_type"',
    ]:
        if required not in html_text:
            errors.append(f"html:missing:{required}")
    for forbidden in ["fetch(", "xmlhttprequest", "import(", "contenteditable"]:
        if forbidden in lower_html:
            errors.append(f"html:forbidden:{forbidden}")
    errors.extend(validate_redaction(html_text))
    errors.extend(validate_redaction(cockpit_json))
    return {
        "ok": not errors,
        "checks": _validation_checks(),
        "errors": _unique(errors),
    }


def _validation_checks() -> list[str]:
    return [
        "offline html doctype present",
        "viewport meta present",
        "external urls absent",
        "external scripts absent",
        "embedded json escaped",
        "embedded json bounded",
        "generated view policy present",
        "eight page cockpit structure present",
        "graph controls present",
        "selected-node evidence panel present",
        "fallback static graph present",
        "Code Flow nested in Code Intelligence",
        "visual QA checks present",
        "mobile CSS present",
        "redaction validated",
    ]


def _plan_cockpit_file(target: Path, target_path: str) -> tuple[str, str, list[str], list[str]]:
    warnings: list[str] = []
    blocked: list[str] = []
    if not target.exists():
        return "create", "staged_only", warnings, blocked
    if not target.is_file():
        blocked.append(f"{target_path}: target exists and is not a file")
        return "blocked", "blocked", warnings, blocked
    warnings.append(f"preserved user-authored file: {target_path}")
    return "leave_unchanged", "staged_only", warnings, blocked


def _staged_path(stage_root: Path | None, target_path: str, action: str) -> str:
    root = stage_root if stage_root is not None else Path(".product-agent-os") / "project-graph-cockpit"
    if action == "leave_unchanged":
        safe = target_path.replace("/", "__").replace("\\", "__")
        return str(root / "_proposals" / f"{safe}.product-agent-os-proposal")
    if action == "blocked":
        return ""
    return str(root / Path(target_path))


def _write_inside_root(root: Path | None, destination: Path, content: str) -> None:
    if root is None:
        raise ProjectGraphRendererError("internal error: write root is required")
    resolved_root = root.resolve()
    resolved_destination = destination.resolve()
    if not resolved_destination.is_relative_to(resolved_root):
        raise ProjectGraphRendererError(f"staged path escapes output directory: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def _validate_cockpit_target(target_path: str) -> None:
    if _unsafe_relative_path(target_path):
        raise ProjectGraphRendererError(f"invalid cockpit target_path: {target_path}")


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


def _renderer_version() -> str:
    plugin_json = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
    try:
        payload = json.loads(plugin_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return RENDERER_VERSION
    version = payload.get("version")
    return version if isinstance(version, str) and version.strip() else RENDERER_VERSION


def _int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _coord(value: Any) -> str:
    try:
        return f"{float(value):.3f}"
    except (TypeError, ValueError):
        return "0"


def _radius(value: Any) -> str:
    try:
        return f"{max(2.0, min(float(value), 20.0)):.2f}"
    except (TypeError, ValueError):
        return "4.00"


def _attr(value: Any) -> str:
    return escape_html(value)


def _text(value: Any) -> str:
    return escape_html(value)


def _unique(items: list[str]) -> list[str]:
    unique: list[str] = []
    for item in items:
        if item not in unique:
            unique.append(item)
    return unique
