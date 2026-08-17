"""Offline agent and skill metrics report renderer for Product-Agent OS."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path, PureWindowsPath
from typing import Any

from product_agent_os.offline_artifact_safety import (
    GENERATED_VIEW_ONLY_TEXT,
    EMBEDDED_JSON_BYTE_LIMIT,
    escape_html,
    prepare_offline_payload,
    validate_offline_artifact,
)
from product_agent_os.offline_artifact_export import build_html_export_contract
from product_agent_os.stage_manifest import (
    MANIFEST_NAME,
    build_stage_manifest,
    content_digest,
    file_digest,
    load_stage_manifest,
    write_stage_manifest,
)


METRICS_REPORT_TARGET = ".codex/eval-reports/agent-skill-evaluation-report.html"
METRICS_REPORT_ARCHIVE_DIR = ".codex/eval-reports/archive"
RENDERER_VERSION = "0.1.0"


class AgentSkillMetricsReportError(RuntimeError):
    pass


def build_agent_skill_metrics_report_manifest(
    *,
    report_id: str,
    generated_at: str,
    project_id: str,
    eval_window: dict[str, Any],
    cadence: dict[str, Any],
    source_datasets: list[str] | None = None,
    trace_sources: list[str] | None = None,
    redaction_status: str = "unknown",
    archive: bool = False,
) -> dict[str, Any]:
    """Build a redacted report manifest for staged metrics review."""

    safe = prepare_offline_payload(
        {
            "schema_version": 1,
            "write_policy": "read_only",
            "report_id": str(report_id),
            "generated_at": str(generated_at),
            "project_id": str(project_id),
            "eval_window": eval_window,
            "cadence": cadence,
            "source_datasets": sorted(str(item) for item in source_datasets or []),
            "trace_sources": sorted(str(item) for item in trace_sources or []),
            "redaction_status": redaction_status,
            "current_report_path": METRICS_REPORT_TARGET,
            "archive_policy": _archive_policy(str(report_id), archive),
        }
    )
    payload = safe["payload"]
    payload["redaction_summary"] = safe["redaction_summary"]
    return payload


def render_agent_skill_metrics_report(report_packet: dict[str, Any]) -> dict[str, Any]:
    """Render a self-contained offline metrics report with embedded redacted JSON."""

    if not isinstance(report_packet, dict):
        raise AgentSkillMetricsReportError("report packet must be an object")
    manifest = build_agent_skill_metrics_report_manifest(
        report_id=str(report_packet.get("report_id") or _default_report_id()),
        generated_at=str(report_packet.get("generated_at") or _generated_at()),
        project_id=str(report_packet.get("project_id") or "unassigned"),
        eval_window=_dict(report_packet.get("eval_window")),
        cadence=_dict(report_packet.get("cadence")),
        source_datasets=[str(item) for item in report_packet.get("source_datasets", [])],
        trace_sources=[str(item) for item in _dict(report_packet.get("trace_evidence")).get("trace_sources", [])],
        redaction_status=str(report_packet.get("redaction_status") or "unknown"),
    )
    packet = dict(report_packet)
    packet["manifest"] = manifest
    prepared = prepare_offline_payload(packet, max_json_bytes=EMBEDDED_JSON_BYTE_LIMIT)
    safe_packet = prepared["payload"]
    html_text = _render_html(safe_packet, prepared["json_for_html"])
    validation = validate_offline_artifact(
        html_text=html_text,
        embedded_json=prepared["json"],
        payload=safe_packet if isinstance(safe_packet, dict) else {},
        max_json_bytes=EMBEDDED_JSON_BYTE_LIMIT,
    )
    return {
        "status": "ready" if validation["ok"] else "blocked",
        "html": html_text,
        "json": prepared["json"],
        "report": safe_packet,
        "manifest": manifest,
        "embedded_json_bytes": prepared["embedded_json_bytes"],
        "redaction_summary": prepared["redaction_summary"],
        "validation": validation,
    }


def render_agent_skill_metrics_report_plan(
    workspace: str | Path,
    report_packet: dict[str, Any],
    *,
    archive: bool = False,
) -> dict[str, Any]:
    """Build a read-only metrics report staging plan without writing files."""

    return _report_renderer_result(Path(workspace).resolve(), report_packet, None, write_files=False, archive=archive)


def stage_agent_skill_metrics_report(
    workspace: str | Path,
    output_dir: str | Path,
    report_packet: dict[str, Any],
    *,
    archive: bool = False,
) -> dict[str, Any]:
    """Stage report files and a standard Product-Agent OS stage manifest."""

    workspace_path = Path(workspace).resolve()
    stage_root = Path(output_dir).resolve()
    if stage_root == workspace_path or stage_root.is_relative_to(workspace_path):
        raise AgentSkillMetricsReportError("stage output directory must be outside workspace")
    if stage_root.exists() and not stage_root.is_dir():
        raise AgentSkillMetricsReportError(f"stage output path is not a directory: {stage_root}")
    return _report_renderer_result(workspace_path, report_packet, stage_root, write_files=True, archive=archive)


def validate_agent_skill_metrics_report_manifest(stage_root: str | Path) -> list[str]:
    """Validate report stage manifest paths and staged file digests."""

    stage_path = Path(stage_root).resolve()
    try:
        manifest = load_stage_manifest(stage_path)
    except ValueError as exc:
        return [str(exc)]

    errors: list[str] = []
    entries = [item for item in manifest.get("files", []) if isinstance(item, dict)]
    targets = {str(item.get("target_path", "")) for item in entries}
    if METRICS_REPORT_TARGET not in targets:
        errors.append(f"metrics report target missing from manifest: {METRICS_REPORT_TARGET}")
    for item in entries:
        target_path = str(item.get("target_path", ""))
        if target_path != METRICS_REPORT_TARGET and not target_path.startswith(METRICS_REPORT_ARCHIVE_DIR + "/"):
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
        if str(item.get("digest", "")) != file_digest(staged_path):
            errors.append(f"{target_path}: staged digest does not match manifest")
    return errors


def _report_renderer_result(
    workspace: Path,
    report_packet: dict[str, Any],
    stage_root: Path | None,
    *,
    write_files: bool,
    archive: bool,
) -> dict[str, Any]:
    rendered = render_agent_skill_metrics_report(report_packet)
    report_id = str(rendered["manifest"].get("report_id") or _default_report_id())
    contents = {METRICS_REPORT_TARGET: rendered["html"]}
    if archive:
        contents[f"{METRICS_REPORT_ARCHIVE_DIR}/{_slug(report_id)}.html"] = rendered["html"]

    files: list[dict[str, Any]] = []
    warnings: list[str] = []
    blocked: list[str] = []
    action_summary = {"create": [], "update": [], "leave_unchanged": [], "blocked": []}
    for target_path, content in contents.items():
        _validate_report_target(target_path)
        action, write_policy, file_warnings, file_blocked = _plan_report_file(workspace / target_path, target_path)
        warnings.extend(file_warnings)
        blocked.extend(file_blocked)
        action_summary[action].append(target_path)
        staged_path = _staged_path(stage_root, target_path, action)
        if write_files and action in {"create", "update", "leave_unchanged"}:
            _write_inside_root(stage_root, Path(staged_path), content)
        files.append(
            {
                "key": _slug(Path(target_path).stem),
                "category": "metrics-report",
                "target_path": target_path,
                "action": action,
                "write_policy": write_policy,
                "staged_path": staged_path,
                "digest": content_digest(content) if action != "blocked" else "",
            }
        )

    validation_errors: dict[str, list[str]] = {}
    if not rendered["validation"]["ok"]:
        validation_errors[METRICS_REPORT_TARGET] = rendered["validation"]["errors"]
    status = "blocked" if blocked or validation_errors else "needs_approval"
    result = {
        "infrastructure_plan": {
            "status": status,
            "workspace": str(workspace),
            "profile": "metrics-report",
            "detected_stack": [],
            "create": action_summary["create"],
            "update": action_summary["update"],
            "leave_unchanged": action_summary["leave_unchanged"],
            "approval_required": ["explicit approval required before applying staged metrics report"],
            "warnings": _unique(warnings),
            "blocked": _unique(blocked),
            "questions": [],
        },
        "rendered_artifacts": {
            "mode": "stage" if write_files else "dry-run",
            "root": str(stage_root if stage_root is not None else Path(".product-agent-os") / "agent-skill-report"),
            "output_dir": str(stage_root) if stage_root is not None else "",
            "final_export_contract": build_html_export_contract(
                workspace,
                artifact_id="agent-skill-evaluation-report",
                default_relative_path=METRICS_REPORT_TARGET,
            ),
            "files": files,
            "managed_sections": [],
            "validation": {
                "ok": not validation_errors,
                "checks": rendered["validation"]["checks"],
                "errors": validation_errors,
            },
            "report_manifest": rendered["manifest"],
        },
    }
    if write_files and stage_root is not None:
        manifest = build_stage_manifest(
            workspace=workspace,
            stage_root=stage_root,
            renderer_result=result,
            renderer_version=RENDERER_VERSION,
        )
        manifest_path = write_stage_manifest(stage_root, manifest)
        result["rendered_artifacts"]["manifest_path"] = str(manifest_path)
    return result


def _render_html(packet: dict[str, Any], json_for_html: str) -> str:
    title = "Agent Skill Metrics Report"
    manifest = _dict(packet.get("manifest"))
    sections = "\n".join(
        [
            _summary_section(packet),
            _targets_section(packet),
            _metrics_section(packet),
            _execution_loop_section(packet),
            _version_section(packet),
            _candidates_section(packet),
            _appendix_section(packet),
        ]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape_html(title)}</title>
  <style>
    :root {{ color-scheme: light; --bg: #f7f8fa; --panel: #ffffff; --text: #1d2733; --muted: #5f6b7a; --border: #d9e0e8; --accent: #126d60; --accent-2: #2f6fb0; --warning-bg: #fff4d6; --warning-border: #e0a92f; --danger: #a33a2a; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--text); font-family: Arial, Helvetica, sans-serif; line-height: 1.5; }}
    main {{ width: min(1180px, calc(100% - 32px)); margin: 0 auto; padding: 28px 0 44px; }}
    header {{ margin-bottom: 18px; }}
    h1, h2 {{ letter-spacing: 0; }}
    h1 {{ margin: 0; font-size: 30px; line-height: 1.2; }}
    h2 {{ margin: 0 0 12px; font-size: 18px; line-height: 1.25; }}
    .eyebrow {{ margin: 0 0 6px; color: var(--accent); font-size: 12px; font-weight: 700; letter-spacing: 0; text-transform: uppercase; }}
    .generated-view-policy, .muted {{ color: var(--muted); }}
    .summary-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin: 18px 0; }}
    .summary-card, section {{ background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 16px; min-width: 0; }}
    .summary-card strong {{ display: block; font-size: 12px; color: var(--muted); margin-bottom: 4px; text-transform: uppercase; }}
    section {{ margin: 14px 0; }}
    table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
    th, td {{ border-bottom: 1px solid #edf0f4; padding: 8px; text-align: left; vertical-align: top; overflow-wrap: anywhere; }}
    th {{ color: var(--text); }}
    .banner {{ border: 1px solid var(--warning-border); background: var(--warning-bg); border-radius: 8px; padding: 12px 14px; margin: 0 0 12px; color: var(--danger); }}
    code {{ background: #edf2f7; padding: 2px 4px; border-radius: 4px; overflow-wrap: anywhere; }}
    pre {{ max-height: 320px; overflow: auto; border: 1px solid var(--border); border-radius: 8px; padding: 12px; background: #fbfcfe; }}
    @media (max-width: 760px) {{ main {{ width: min(100% - 20px, 1180px); padding-top: 20px; }} .summary-grid {{ grid-template-columns: 1fr; }} table {{ font-size: 13px; }} }}
  </style>
</head>
<body>
  <main>
    <header>
      <p class="eyebrow">Product-Agent OS</p>
      <h1>{escape_html(title)}</h1>
      <p class="muted">Generated {escape_html(packet.get("generated_at", ""))}</p>
      <p class="generated-view-policy">{escape_html(GENERATED_VIEW_ONLY_TEXT)}</p>
      <div class="summary-grid" aria-label="Report summary">
        <div class="summary-card"><strong>Report</strong><code>{escape_html(manifest.get("report_id", "unassigned"))}</code></div>
        <div class="summary-card"><strong>Project</strong><code>{escape_html(manifest.get("project_id", "unassigned"))}</code></div>
        <div class="summary-card"><strong>Redaction</strong><code>{escape_html(manifest.get("redaction_status", "unknown"))}</code></div>
      </div>
    </header>
{sections}
  </main>
  <script type="application/json" id="agent-skill-report-data">{json_for_html}</script>
</body>
</html>
"""


def _summary_section(packet: dict[str, Any]) -> str:
    manifest = _dict(packet.get("manifest"))
    return (
        '    <section id="report-summary">\n'
        "      <h2>Executive Verdict</h2>\n"
        f"      <p>{escape_html(GENERATED_VIEW_ONLY_TEXT)}</p>\n"
        f"      <p>Report id: <code>{escape_html(manifest.get('report_id', 'unassigned'))}</code></p>\n"
        f"      <p>Cadence: <code>{escape_html(_compact_json(manifest.get('cadence', {})))}</code></p>\n"
        "    </section>"
    )


def _targets_section(packet: dict[str, Any]) -> str:
    targets = packet.get("target_inventory") if isinstance(packet.get("target_inventory"), list) else []
    rows = []
    for target in targets:
        if not isinstance(target, dict):
            continue
        target_id = str(target.get("target_id") or "target")
        rows.append(
            f'        <tr id="target-{_slug(target_id)}">'
            f"<th>{escape_html(target_id)}</th>"
            f"<td>{escape_html(target.get('target_type', 'unknown'))}</td>"
            f"<td>{escape_html(target.get('version', 'unversioned'))}</td></tr>"
        )
    return (
        '    <section id="target-inventory">\n'
        "      <h2>Target Inventory</h2>\n"
        "      <table><thead><tr><th>Target</th><th>Type</th><th>Version</th></tr></thead><tbody>\n"
        + "\n".join(rows)
        + "\n      </tbody></table>\n"
        "    </section>"
    )


def _metrics_section(packet: dict[str, Any]) -> str:
    metrics = []
    sections = _dict(_dict(packet.get("metrics")).get("sections"))
    for section in sections.values():
        if not isinstance(section, dict):
            continue
        for metric in _dict(section.get("metrics")).values():
            if isinstance(metric, dict):
                metrics.append(metric)
    rows = []
    banner = ""
    for metric in metrics:
        metric_id = str(metric.get("metric_id") or "metric")
        numerator = metric.get("numerator", 0)
        denominator = metric.get("denominator", 0)
        status = str(metric.get("status") or "unknown")
        if status == "insufficient_data":
            banner = '      <div class="banner">Insufficient data: at least one metric cannot support approval.</div>\n'
        rows.append(
            f'        <tr id="metric-{escape_html(metric_id)}">'
            f"<th>{escape_html(metric_id)}</th>"
            f"<td>{escape_html(numerator)} / {escape_html(denominator)}</td>"
            f"<td>{escape_html(metric.get('value', ''))}</td>"
            f"<td>{escape_html(status)}</td></tr>"
        )
    return (
        '    <section id="metrics">\n'
        "      <h2>Metrics</h2>\n"
        f"{banner}"
        "      <table><thead><tr><th>Metric</th><th>Raw Count</th><th>Value</th><th>Status</th></tr></thead><tbody>\n"
        + "\n".join(rows)
        + "\n      </tbody></table>\n"
        "    </section>"
    )


def _version_section(packet: dict[str, Any]) -> str:
    comparison = _dict(packet.get("version_comparison"))
    rows = [
        f"<tr><th>{escape_html(name)}</th><td><code>{escape_html(_compact_json(value))}</code></td></tr>"
        for name, value in comparison.items()
    ]
    return (
        '    <section id="version-comparison">\n'
        "      <h2>Version Comparison</h2>\n"
        "      <table><tbody>\n"
        + "\n".join(rows)
        + "\n      </tbody></table>\n"
        "    </section>"
    )


def _execution_loop_section(packet: dict[str, Any]) -> str:
    loop = _dict(packet.get("execution_loop_metrics"))
    triggers = loop.get("stop_triggers") if isinstance(loop.get("stop_triggers"), list) else []
    recommendations = loop.get("recommendations") if isinstance(loop.get("recommendations"), list) else []
    trigger_items = "".join(f"<li><code>{escape_html(item)}</code></li>" for item in triggers)
    recommendation_items = "".join(f"<li>{escape_html(item)}</li>" for item in recommendations)
    return (
        '    <section id="execution-loop-metrics">\n'
        "      <h2>Execution Loop Diagnostics</h2>\n"
        f"      <p>Status: <code>{escape_html(loop.get('status', 'not_collected'))}</code></p>\n"
        f"      <p>Evidence ceiling: <code>{escape_html(loop.get('evidence_ceiling', 'manual_local_diagnostic_only'))}</code></p>\n"
        f"      <ul>{trigger_items}</ul>\n"
        f"      <ol>{recommendation_items}</ol>\n"
        "    </section>"
    )


def _candidates_section(packet: dict[str, Any]) -> str:
    candidates = packet.get("update_candidates") if isinstance(packet.get("update_candidates"), list) else []
    items = "\n".join(
        f"        <li><code>{escape_html(_dict(item).get('candidate_id', 'candidate'))}</code> - {escape_html(_dict(item).get('approval_state', 'not_requested'))}</li>"
        for item in candidates
    )
    return (
        '    <section id="update-candidates">\n'
        "      <h2>Update Candidates</h2>\n"
        f"      <ul>{items}</ul>\n"
        "    </section>"
    )


def _appendix_section(packet: dict[str, Any]) -> str:
    return (
        '    <section id="raw-redacted-appendix">\n'
        "      <h2>Raw Redacted Appendix</h2>\n"
        f"      <pre>{escape_html(_compact_json(packet.get('raw_appendix', {})))}</pre>\n"
        "    </section>"
    )


def _archive_policy(report_id: str, archive: bool) -> dict[str, Any]:
    if not archive:
        return {"status": "disabled", "archive_report_path": ""}
    return {"status": "enabled", "archive_report_path": f"{METRICS_REPORT_ARCHIVE_DIR}/{_slug(report_id)}.html"}


def _plan_report_file(target: Path, target_path: str) -> tuple[str, str, list[str], list[str]]:
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
    root = stage_root if stage_root is not None else Path(".product-agent-os") / "agent-skill-report"
    if action == "leave_unchanged":
        safe = target_path.replace("/", "__").replace("\\", "__")
        return str(root / "_proposals" / f"{safe}.product-agent-os-proposal")
    if action == "blocked":
        return ""
    return str(root / Path(target_path))


def _write_inside_root(root: Path | None, destination: Path, content: str) -> None:
    if root is None:
        raise AgentSkillMetricsReportError("internal error: write root is required")
    resolved_root = root.resolve()
    resolved_destination = destination.resolve()
    if not resolved_destination.is_relative_to(resolved_root):
        raise AgentSkillMetricsReportError(f"staged path escapes output directory: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def _validate_report_target(target_path: str) -> None:
    if _unsafe_relative_path(target_path):
        raise AgentSkillMetricsReportError(f"invalid report target_path: {target_path}")


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
    )


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def _slug(value: str) -> str:
    import re

    slug = re.sub(r"[^a-zA-Z0-9]+", "-", str(value).strip().lower()).strip("-")
    return slug or "unknown"


def _default_report_id() -> str:
    return "agent-skill-report"


def _generated_at() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _unique(items: list[str]) -> list[str]:
    return sorted(set(items))
