"""Static offline status dashboard renderer for Product-Agent OS."""

from __future__ import annotations

import html
import json
import re
from datetime import UTC, datetime
from pathlib import Path, PureWindowsPath
from typing import Any

from codex_runtime_runner.redaction import redact_payload, validate_redaction
from product_agent_os.stage_manifest import (
    MANIFEST_NAME,
    build_stage_manifest,
    content_digest,
    file_digest,
    load_stage_manifest,
    write_stage_manifest,
)


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = PLUGIN_ROOT / "assets" / "templates" / "status-dashboard"
STATUS_HTML_TARGET = ".codex/product-agent-os/status.html"
STATUS_JSON_TARGET = ".codex/product-agent-os/status.json"
DASHBOARD_TARGETS = (STATUS_HTML_TARGET, STATUS_JSON_TARGET)
DASHBOARD_MANIFEST_NAME = MANIFEST_NAME
RENDERER_VERSION = "0.1.0"
EXTERNAL_URL_PATTERN = re.compile(r"https?://", re.IGNORECASE)
SCRIPT_SRC_PATTERN = re.compile(r"<script\s+[^>]*\bsrc\s*=", re.IGNORECASE)


class StatusDashboardError(RuntimeError):
    pass


def render_status_dashboard(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Render a status snapshot into offline HTML and JSON dashboard artifacts."""

    if not isinstance(snapshot, dict):
        raise StatusDashboardError("status snapshot must be an object")
    safe_snapshot, redaction_summary = _redacted_snapshot(snapshot)
    snapshot_json = _json_text(safe_snapshot)
    html_text = _render_html(safe_snapshot)
    validation = _validate_dashboard_content(html_text, snapshot_json, safe_snapshot)
    return {
        "status": "ready" if validation["ok"] else "blocked",
        "html": html_text,
        "json": snapshot_json,
        "snapshot": safe_snapshot,
        "redaction_summary": redaction_summary,
        "validation": validation,
    }


def render_status_dashboard_plan(
    workspace: str | Path,
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    """Build a read-only dashboard render plan without writing files."""

    return _dashboard_renderer_result(Path(workspace).resolve(), snapshot, None, write_files=False)


def stage_status_dashboard(
    workspace: str | Path,
    output_dir: str | Path,
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    """Stage dashboard files and a standard Product-Agent OS stage manifest."""

    workspace_path = Path(workspace).resolve()
    stage_root = Path(output_dir).resolve()
    if stage_root == workspace_path or stage_root.is_relative_to(workspace_path):
        raise StatusDashboardError("stage output directory must be outside workspace")
    if stage_root.exists() and not stage_root.is_dir():
        raise StatusDashboardError(f"stage output path is not a directory: {stage_root}")
    return _dashboard_renderer_result(workspace_path, snapshot, stage_root, write_files=True)


def validate_status_dashboard_manifest(stage_root: str | Path) -> list[str]:
    """Validate dashboard stage manifest paths and staged file digests."""

    stage_path = Path(stage_root).resolve()
    try:
        manifest = load_stage_manifest(stage_path)
    except ValueError as exc:
        return [str(exc)]

    errors: list[str] = []
    entries = [item for item in manifest.get("files", []) if isinstance(item, dict)]
    targets = {str(item.get("target_path", "")) for item in entries}
    for target in DASHBOARD_TARGETS:
        if target not in targets:
            errors.append(f"dashboard target missing from manifest: {target}")

    for item in entries:
        target_path = str(item.get("target_path", ""))
        if target_path not in DASHBOARD_TARGETS:
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


def _dashboard_renderer_result(
    workspace: Path,
    snapshot: dict[str, Any],
    stage_root: Path | None,
    *,
    write_files: bool,
) -> dict[str, Any]:
    rendered = render_status_dashboard(snapshot)
    contents = {
        STATUS_HTML_TARGET: rendered["html"],
        STATUS_JSON_TARGET: rendered["json"] + "\n",
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
        _validate_dashboard_target(target_path)
        action, write_policy, file_warnings, file_blocked = _plan_dashboard_file(workspace / Path(target_path), target_path)
        warnings.extend(file_warnings)
        blocked.extend(file_blocked)
        action_summary[action].append(target_path)
        staged_path = _staged_path(stage_root, target_path, action)
        if write_files and action in {"create", "leave_unchanged"}:
            _write_inside_root(stage_root, Path(staged_path), content)
        entry: dict[str, Any] = {
            "key": "status-dashboard-html" if target_path == STATUS_HTML_TARGET else "status-dashboard-json",
            "category": "status-dashboard",
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
        blocked.extend(f"dashboard validation failed: {error}" for error in validation_errors)
    validation_ok = not validation_errors and not blocked
    approval_required = (
        ["explicit approval required before applying staged status dashboard to workspace"]
        if any(item["action"] == "create" for item in files)
        else []
    )
    status = "blocked" if not validation_ok else "needs_approval" if approval_required else "ready"
    result = {
        "status_dashboard": {
            "status": status,
            "write_policy": "staged_only",
            "source_of_truth": "status_snapshot",
            "targets": list(DASHBOARD_TARGETS),
            "warnings": _unique(warnings),
            "blocked": _unique(blocked),
            "redaction_summary": rendered["redaction_summary"],
        },
        "infrastructure_plan": {
            "status": status,
            "workspace": str(workspace),
            "profile": "status-dashboard",
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
            "root": str(stage_root if stage_root is not None else Path(".product-agent-os") / "status-dashboard"),
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
        manifest_errors = validate_status_dashboard_manifest(stage_root)
        if manifest_errors:
            result["rendered_artifacts"]["validation"]["ok"] = False
            result["rendered_artifacts"]["validation"]["errors"].extend(manifest_errors)
            result["status_dashboard"]["status"] = "blocked"
            result["infrastructure_plan"]["status"] = "blocked"
    return result


def _redacted_snapshot(snapshot: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    redacted, report = redact_payload(snapshot)
    if not isinstance(redacted, dict):
        raise StatusDashboardError("status snapshot redaction failed")
    existing = redacted.get("redaction_summary")
    categories = set(str(item) for item in report.get("categories", []))
    count = int(report.get("count", 0))
    if isinstance(existing, dict):
        categories.update(str(item) for item in existing.get("categories", []) if isinstance(item, str))
        try:
            count += int(existing.get("count", 0))
        except (TypeError, ValueError):
            pass
    summary = {"count": count, "categories": sorted(categories)}
    redacted["redaction_summary"] = summary
    return redacted, summary


def _render_html(snapshot: dict[str, Any]) -> str:
    template = (TEMPLATE_ROOT / "status.html").read_text(encoding="utf-8")
    css = (TEMPLATE_ROOT / "status.css").read_text(encoding="utf-8")
    values = {
        "title": "Product-Agent OS Status",
        "generated_at": _text(snapshot.get("generated_at") or "not available"),
        "css": css.rstrip(),
        "banner": _status_banner(snapshot),
        "sections": _sections(snapshot),
        "snapshot_json": _json_for_html(snapshot),
    }
    html_text = template
    for key, value in values.items():
        html_text = html_text.replace("{{" + key + "}}", value)
    return html_text


def _sections(snapshot: dict[str, Any]) -> str:
    usage = _dict(snapshot.get("usage_mode"))
    questions = _dict(snapshot.get("question_summary"))
    readiness = _dict(snapshot.get("readiness_summary"))
    evidence = _dict(snapshot.get("evidence_summary"))
    approvals = _dict(snapshot.get("approval_summary"))
    dashboard_policy = _dict(snapshot.get("dashboard_policy"))
    staged = _dict(snapshot.get("staged_artifacts"))
    manifest = _dict(snapshot.get("manifest_digests"))

    sections = [
        _section(
            "section-lifecycle",
            "Lifecycle",
            [
                ("Lifecycle state", snapshot.get("lifecycle_state")),
                ("Workspace", snapshot.get("workspace")),
                ("Generated at", snapshot.get("generated_at")),
                ("Write policy", snapshot.get("write_policy")),
            ],
        ),
        _section(
            "section-usage-mode",
            "Usage Mode",
            [
                ("Primary", usage.get("primary")),
                ("Confidence", usage.get("confidence")),
                ("Inspection only", usage.get("inspection_only")),
                ("Minimum artifacts", usage.get("minimum_artifacts")),
            ],
        ),
        _section(
            "section-questions",
            "Questions",
            [
                ("Total", questions.get("total")),
                ("Blocking", questions.get("blocking")),
                ("Recommended", questions.get("recommended")),
                ("Optional", questions.get("optional")),
                ("Remaining", questions.get("remaining")),
                ("Next blocking question", _next_question_text(questions.get("next_blocking_question"))),
                ("First response summary", questions.get("first_response_summary")),
            ],
        ),
        _section(
            "section-readiness",
            "Readiness",
            [
                ("Status", readiness.get("status")),
                ("Runtime status", readiness.get("runtime_status")),
                ("Success claim", readiness.get("success_claim")),
                ("Warnings", readiness.get("warnings")),
            ],
        ),
        _section(
            "section-evidence",
            "Evidence",
            [
                ("Freshness", evidence.get("freshness")),
                ("Evidence count", evidence.get("evidence_count")),
                ("Stale count", evidence.get("stale_count")),
                ("Max age days", evidence.get("max_age_days")),
                ("Staged mode", staged.get("mode")),
                ("Manifest files", manifest.get("file_count")),
            ],
        ),
        _section(
            "section-approvals",
            "Approvals",
            [
                ("Status", approvals.get("status")),
                ("Requirements", approvals.get("requirements")),
            ],
        ),
        _section(
            "section-next-action",
            "Next Action",
            [
                ("Next safe action", snapshot.get("next_safe_action")),
                ("Dashboard source", dashboard_policy.get("source_of_truth")),
                ("Dashboard write policy", dashboard_policy.get("write_policy")),
                ("Success claim policy", dashboard_policy.get("success_claim_policy")),
            ],
        ),
    ]
    return "\n".join(sections)


def _section(section_id: str, title: str, rows: list[tuple[str, Any]]) -> str:
    table_rows = "\n".join(
        f"          <tr><th scope=\"row\">{_text(label)}</th><td>{_value(value)}</td></tr>"
        for label, value in rows
    )
    return (
        f"      <section class=\"status-section\" id=\"{section_id}\">\n"
        f"        <h2>{_text(title)}</h2>\n"
        "        <table class=\"status-table\">\n"
        "          <tbody>\n"
        f"{table_rows}\n"
        "          </tbody>\n"
        "        </table>\n"
        "      </section>"
    )


def _status_banner(snapshot: dict[str, Any]) -> str:
    usage = _dict(snapshot.get("usage_mode"))
    evidence = _dict(snapshot.get("evidence_summary"))
    readiness = _dict(snapshot.get("readiness_summary"))
    warnings = readiness.get("warnings") if isinstance(readiness.get("warnings"), list) else []
    needs_review = (
        bool(usage.get("inspection_only"))
        or evidence.get("freshness") == "stale"
        or "stale evidence" in warnings
        or "inspection-only evidence cannot prove completion" in warnings
    )
    if not needs_review:
        return ""
    return (
        "    <section class=\"status-banner\" role=\"status\">\n"
        "      <strong>Evidence requires review</strong>\n"
        "      <p>Inspection-only or stale evidence cannot prove completion; use underlying artifacts before claiming work is done.</p>\n"
        "    </section>"
    )


def _value(value: Any) -> str:
    if value in (None, ""):
        return "<span class=\"muted\">not available</span>"
    if isinstance(value, bool):
        return _text("yes" if value else "no")
    if isinstance(value, list):
        if not value:
            return "<span class=\"muted\">none</span>"
        items = "".join(f"<li>{_value(item)}</li>" for item in value)
        return f"<ul class=\"status-list\">{items}</ul>"
    if isinstance(value, dict):
        compact = json.dumps(value, ensure_ascii=False, sort_keys=True)
        return f"<code>{_text(compact)}</code>"
    return _text(value)


def _next_question_text(value: Any) -> Any:
    if isinstance(value, dict):
        return value.get("text") or value.get("id") or value
    return value


def _text(value: Any) -> str:
    text = str(value)
    text = EXTERNAL_URL_PATTERN.sub("[EXTERNAL_URL_REDACTED]", text)
    return html.escape(text, quote=True)


def _json_text(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def _json_for_html(payload: Any) -> str:
    text = _json_text(payload)
    return (
        text.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("http://", "http:\\/\\/")
        .replace("https://", "https:\\/\\/")
    )


def _validate_dashboard_content(html_text: str, snapshot_json: str, snapshot: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    lower_html = html_text.lower()
    if not lower_html.startswith("<!doctype html>"):
        errors.append("html:doctype_missing")
    if '<meta name="viewport"' not in lower_html:
        errors.append("html:viewport_missing")
    if EXTERNAL_URL_PATTERN.search(html_text):
        errors.append("html:external_url_forbidden")
    if SCRIPT_SRC_PATTERN.search(html_text):
        errors.append("html:script_src_forbidden")
    if snapshot.get("schema_version") != 1:
        errors.append("snapshot.schema_version:must_be_1")
    if snapshot.get("write_policy") != "read_only":
        errors.append("snapshot.write_policy:must_be_read_only")
    errors.extend(validate_redaction(html_text))
    errors.extend(validate_redaction(snapshot_json))
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
        "snapshot redaction validated",
        "status snapshot schema validates",
    ]


def _plan_dashboard_file(target: Path, target_path: str) -> tuple[str, str, list[str], list[str]]:
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
    root = stage_root if stage_root is not None else Path(".product-agent-os") / "status-dashboard"
    if action == "leave_unchanged":
        safe = target_path.replace("/", "__").replace("\\", "__")
        return str(root / "_proposals" / f"{safe}.product-agent-os-proposal")
    if action == "blocked":
        return ""
    return str(root / Path(target_path))


def _write_inside_root(root: Path | None, destination: Path, content: str) -> None:
    if root is None:
        raise StatusDashboardError("internal error: write root is required")
    resolved_root = root.resolve()
    resolved_destination = destination.resolve()
    if not resolved_destination.is_relative_to(resolved_root):
        raise StatusDashboardError(f"staged path escapes output directory: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def _validate_dashboard_target(target_path: str) -> None:
    if _unsafe_relative_path(target_path):
        raise StatusDashboardError(f"invalid dashboard target_path: {target_path}")


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


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _unique(items: list[str]) -> list[str]:
    unique: list[str] = []
    for item in items:
        if item not in unique:
            unique.append(item)
    return unique
