from __future__ import annotations

import json
import re
import tempfile
import tomllib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from product_agent_os.discovery import analyze_workspace
from product_agent_os.merge_markdown import merge_section
from product_agent_os.stage_manifest import build_stage_manifest, write_stage_manifest
from product_agent_os.status_dashboard import StatusDashboardError
from product_agent_os.status_dashboard import render_status_dashboard_plan as _render_status_dashboard_plan
from product_agent_os.status_dashboard import stage_status_dashboard as _stage_status_dashboard
from product_agent_os.templates import TemplateSpec, render_template, required_templates
from product_agent_os.validators import validate_agent_file, validate_hook_file


OWNER = "product-agent-os"
RENDERER_VERSION = "0.1.0"
PLACEHOLDER_PATTERN = re.compile(r"\{[A-Za-z0-9_]+\}")
REQUIRED_HOOK_EVENTS = [
    "SessionStart",
    "PreToolUse",
    "PermissionRequest",
    "PostToolUse",
    "Stop",
]
CONTROL_PLANE_TARGETS = {
    "AGENTS.md",
    "REQUIREMENTS.md",
    "PLAN.md",
    "TEST.md",
    "EVALS.md",
    "RUNLOG.md",
}


class InfrastructureError(RuntimeError):
    pass


def render_infrastructure_plan(workspace: str | Path) -> dict[str, Any]:
    workspace_path = _workspace_path(workspace)
    audit = _analyze(workspace_path)
    return _build_result(workspace_path, audit, None, write_files=False)


def render_infrastructure_from_audit(
    workspace: str | Path,
    audit: dict[str, Any],
    *,
    lifecycle_packets: dict[str, Any] | list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    workspace_path = _workspace_path(workspace)
    return _build_result(
        workspace_path,
        audit,
        None,
        write_files=False,
        lifecycle_packets=lifecycle_packets,
    )


def stage_infrastructure(workspace: str | Path, output_dir: str | Path) -> dict[str, Any]:
    workspace_path = _workspace_path(workspace)
    stage_root = Path(output_dir).resolve()
    if stage_root == workspace_path or stage_root.is_relative_to(workspace_path):
        raise InfrastructureError("stage output directory must be outside workspace")
    if stage_root.exists() and not stage_root.is_dir():
        raise InfrastructureError(f"stage output path is not a directory: {stage_root}")
    audit = _analyze(workspace_path)
    try:
        return _build_result(workspace_path, audit, stage_root, write_files=True)
    except (OSError, ValueError) as exc:
        raise InfrastructureError(f"unable to write staged infrastructure: {exc}") from exc


def render_status_dashboard_plan(workspace: str | Path, status_snapshot: dict[str, Any]) -> dict[str, Any]:
    workspace_path = _workspace_path(workspace)
    try:
        return _render_status_dashboard_plan(workspace_path, status_snapshot)
    except StatusDashboardError as exc:
        raise InfrastructureError(f"unable to render status dashboard: {exc}") from exc


def stage_status_dashboard(
    workspace: str | Path,
    output_dir: str | Path,
    status_snapshot: dict[str, Any],
) -> dict[str, Any]:
    workspace_path = _workspace_path(workspace)
    stage_root = Path(output_dir).resolve()
    if stage_root == workspace_path or stage_root.is_relative_to(workspace_path):
        raise InfrastructureError("stage output directory must be outside workspace")
    if stage_root.exists() and not stage_root.is_dir():
        raise InfrastructureError(f"stage output path is not a directory: {stage_root}")
    try:
        return _stage_status_dashboard(workspace_path, stage_root, status_snapshot)
    except (OSError, ValueError, StatusDashboardError) as exc:
        raise InfrastructureError(f"unable to write staged status dashboard: {exc}") from exc


def _workspace_path(workspace: str | Path) -> Path:
    return Path(workspace).resolve()


def _analyze(workspace: Path) -> dict[str, Any]:
    try:
        return analyze_workspace(workspace)
    except FileNotFoundError as exc:
        raise InfrastructureError(f"workspace does not exist: {workspace}") from exc
    except NotADirectoryError as exc:
        raise InfrastructureError(f"workspace is not a directory: {workspace}") from exc
    except OSError as exc:
        raise InfrastructureError(f"unable to inspect workspace: {workspace}: {exc}") from exc


def _build_result(
    workspace: Path,
    audit: dict[str, Any],
    stage_root: Path | None,
    *,
    write_files: bool,
    lifecycle_packets: dict[str, Any] | list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    context = _template_context(workspace, audit)
    warnings = _profile_warnings(workspace, audit)
    approval_required = ["explicit approval required before applying staged infrastructure to workspace"]
    blocked: list[str] = []
    files: list[dict[str, Any]] = []
    managed_sections: list[dict[str, str]] = []
    validation_errors: dict[str, list[str]] = {}
    action_summary: dict[str, list[str]] = {
        "create": [],
        "update": [],
        "leave_unchanged": [],
        "blocked": [],
    }

    for item in required_templates():
        _validate_template_target(item)
        rendered = render_template(item, context)
        target = workspace / item.target_path
        action, write_policy, file_warnings, file_blocked, staged_content = _plan_file(item, target, rendered)
        warnings.extend(file_warnings)
        blocked.extend(file_blocked)
        action_summary[action].append(item.target_path)
        if item.managed_section and action != "blocked":
            managed_sections.append(
                {
                    "target_path": item.target_path,
                    "section_id": item.managed_section,
                    "action": action,
                }
            )

        staged_path = _staged_path(stage_root, item.target_path, action)
        if write_files and action in {"create", "update", "leave_unchanged"} and staged_content is not None:
            destination = Path(staged_path)
            _write_inside_root(stage_root, destination, staged_content)

        files.append(
            {
                "key": item.key,
                "category": item.category,
                "target_path": item.target_path,
                "action": action,
                "write_policy": write_policy,
                "staged_path": staged_path,
            }
        )

    validation_errors.update(_validate_generated_files(files, stage_root, write_files))
    for target_path in validation_errors:
        _block_validation_failed_file(files, managed_sections, action_summary, target_path)
        blocked.append(f"{target_path}: validation failed")
        if target_path not in action_summary["blocked"]:
            action_summary["blocked"].append(target_path)
    validation_ok = not validation_errors
    status = "blocked" if blocked or not validation_ok else "needs_approval" if approval_required else "ready"
    questions = _lifecycle_questions(lifecycle_packets)
    validation_checks = _validation_checks()
    result = {
        "infrastructure_plan": {
            "status": status,
            "workspace": str(workspace),
            "profile": context["profile_name"],
            "detected_stack": audit.get("detected_stack", []),
            "create": action_summary["create"],
            "update": action_summary["update"],
            "leave_unchanged": action_summary["leave_unchanged"],
            "approval_required": approval_required,
            "warnings": _unique(warnings),
            "blocked": _unique(blocked),
            "questions": questions,
        },
        "rendered_artifacts": {
            "mode": "stage" if write_files else "dry-run",
            "root": str(stage_root if stage_root is not None else Path(".product-agent-os") / "staged"),
            "output_dir": str(stage_root) if stage_root is not None else "",
            "files": files,
            "managed_sections": managed_sections,
            "validation": {
                "ok": validation_ok,
                "checks": validation_checks,
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
    return result


def _lifecycle_questions(lifecycle_packets: dict[str, Any] | list[dict[str, Any]] | None) -> list[str]:
    if lifecycle_packets is None:
        return []
    packets = lifecycle_packets if isinstance(lifecycle_packets, list) else [lifecycle_packets]
    questions: list[str] = []
    for packet in packets:
        if not isinstance(packet, dict):
            continue
        values = packet.get("questions", [])
        if isinstance(values, str):
            questions.append(values)
        elif isinstance(values, list):
            questions.extend(item for item in values if isinstance(item, str))
    return _unique(questions)


def _validation_checks() -> list[str]:
    return [
        "unresolved placeholders absent",
        "agent templates validate",
        "hook templates validate",
        "hook lifecycle config validates",
        "eval json validates",
        "staged config validates",
    ]


def _block_validation_failed_file(
    files: list[dict[str, Any]],
    managed_sections: list[dict[str, str]],
    action_summary: dict[str, list[str]],
    target_path: str,
) -> None:
    for file in files:
        if file["target_path"] != target_path:
            continue
        previous_action = file["action"]
        if previous_action in action_summary and target_path in action_summary[previous_action]:
            action_summary[previous_action].remove(target_path)
        file["action"] = "blocked"
        file["write_policy"] = "blocked"
        file["staged_path"] = ""
        break
    managed_sections[:] = [item for item in managed_sections if item["target_path"] != target_path]


def _renderer_version() -> str:
    plugin_json = Path(__file__).resolve().parents[2] / ".codex-plugin" / "plugin.json"
    try:
        payload = json.loads(plugin_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return RENDERER_VERSION
    version = payload.get("version")
    return version if isinstance(version, str) and version.strip() else RENDERER_VERSION


def _validate_template_target(item: TemplateSpec) -> None:
    target = Path(item.target_path)
    if target.is_absolute() or target.drive or target.root:
        raise InfrastructureError(f"invalid template target_path: {item.target_path}")
    if ".." in target.parts:
        raise InfrastructureError(f"invalid template target_path: {item.target_path}")


def _write_inside_root(root: Path | None, destination: Path, content: str) -> None:
    if root is None:
        raise InfrastructureError("internal error: write root is required")
    resolved_root = root.resolve()
    resolved_destination = destination.resolve()
    if not resolved_destination.is_relative_to(resolved_root):
        raise InfrastructureError(f"staged path escapes output directory: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def _template_context(workspace: Path, audit: dict[str, Any]) -> dict[str, Any]:
    stack = audit.get("detected_stack", [])
    risks = audit.get("risks", [])
    profile = audit.get("complexity_profile", {})
    profile_name = profile.get("name", "") if isinstance(profile, dict) else ""
    return {
        "project_name": workspace.name,
        "workspace_path": str(workspace),
        "profile_name": profile_name,
        "detected_stack": stack,
        "detected_stack_text": ", ".join(stack) if stack else "none",
        "existing_control_plane": audit.get("existing_control_plane", []),
        "missing_control_plane": audit.get("missing_control_plane", []),
        "existing_codex_assets": audit.get("existing_codex_assets", []),
        "risk_text": "; ".join(risks) if risks else "No initial risks detected.",
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    }


def _profile_warnings(workspace: Path, audit: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    stack = audit.get("detected_stack", [])
    profile = audit.get("complexity_profile", {})
    profile_name = profile.get("name", "") if isinstance(profile, dict) else ""
    files = set(audit.get("detected_files", []))
    if "monorepo" in stack or profile_name == "production-team":
        warnings.append("production-team or monorepo profile requires explicit worktree ownership")
    if "docs" in stack or "docs/sources/registry.md" in files:
        warnings.append("docs/source context detected; update the source registry when source-backed claims change")
    runlog = workspace / "RUNLOG.md"
    if runlog.exists() and runlog.is_file():
        try:
            text = runlog.read_text(encoding="utf-8").lower()
        except (OSError, UnicodeDecodeError):
            text = ""
        if "exit_code: 1" in text or "verification failed" in text:
            warnings.append("RUNLOG.md contains failed verification evidence")
    return warnings


def _plan_file(
    item: TemplateSpec,
    target: Path,
    rendered: str,
) -> tuple[str, str, list[str], list[str], str | None]:
    warnings: list[str] = []
    blocked: list[str] = []
    if not target.exists():
        return "create", "staged_only", warnings, blocked, rendered
    if not target.is_file():
        blocked.append(f"{item.target_path}: target exists and is not a file")
        return "blocked", "blocked", warnings, blocked, None

    existing = _read_text(target)
    if existing is None:
        warnings.append(f"preserved user-authored file: {item.target_path}")
        return "leave_unchanged", _write_policy(item), warnings, blocked, rendered

    if item.managed_section:
        start = f"<!-- {OWNER}:start {item.managed_section} -->"
        end = f"<!-- {OWNER}:end {item.managed_section} -->"
        marker_error = _managed_marker_error(existing, start, end)
        if marker_error:
            blocked.append(f"{item.target_path}: {marker_error}")
            return "blocked", "blocked", warnings, blocked, None
        if start in existing and end in existing:
            body = _managed_body(rendered, item.managed_section)
            try:
                staged = merge_section(existing, OWNER, item.managed_section, body)
            except ValueError as exc:
                blocked.append(f"{item.target_path}: {exc}")
                return "blocked", "blocked", warnings, blocked, None
            return "update", "staged_only", warnings, blocked, staged

    warnings.append(f"preserved user-authored file: {item.target_path}")
    if item.target_path == ".codex/config.toml":
        warnings.append("existing .codex/config.toml requires approved write before replacement")
    return "leave_unchanged", _write_policy(item), warnings, blocked, rendered


def _managed_marker_error(existing: str, start: str, end: str) -> str:
    start_positions = [match.start() for match in re.finditer(re.escape(start), existing)]
    end_positions = [match.start() for match in re.finditer(re.escape(end), existing)]
    if not start_positions and not end_positions:
        return ""
    if len(start_positions) > 1 or len(end_positions) > 1:
        return "duplicate managed section"
    if len(start_positions) != len(end_positions):
        return "unpaired managed section"
    if end_positions[0] < start_positions[0]:
        return "broken managed section marker order"
    return ""


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _managed_body(rendered: str, section_id: str) -> str:
    start = f"<!-- {OWNER}:start {section_id} -->"
    end = f"<!-- {OWNER}:end {section_id} -->"
    pattern = re.compile(re.escape(start) + r"\s*(.*?)\s*" + re.escape(end), re.DOTALL)
    match = pattern.search(rendered)
    if not match:
        return rendered
    return match.group(1).strip()


def _write_policy(item: TemplateSpec) -> str:
    if item.target_path == ".codex/config.toml":
        return "approved_write_required"
    return "staged_only"


def _staged_path(stage_root: Path | None, target_path: str, action: str) -> str:
    root = stage_root if stage_root is not None else Path(".product-agent-os") / "staged"
    if action == "leave_unchanged":
        safe = target_path.replace("/", "__").replace("\\", "__")
        return str(root / "_proposals" / f"{safe}.product-agent-os-proposal")
    if action == "blocked":
        return ""
    return str(root / Path(target_path))


def _validate_generated_files(
    files: list[dict[str, Any]],
    stage_root: Path | None,
    write_files: bool,
) -> dict[str, list[str]]:
    errors: dict[str, list[str]] = {}
    specs = {item.target_path: item for item in required_templates()}
    with tempfile.TemporaryDirectory(prefix="product-agent-os-render-") as tmp:
        tmp_root = Path(tmp)
        for file in files:
            if file["action"] == "blocked":
                continue
            spec = specs[file["target_path"]]
            _validate_template_target(spec)
            path = Path(file["staged_path"]) if write_files else tmp_root / spec.target_path
            if not write_files:
                _write_inside_root(tmp_root, path, render_template(spec, _validation_context()))
            elif stage_root is not None and not path.resolve().is_relative_to(stage_root.resolve()):
                errors[spec.target_path] = ["staged path escapes output directory"]
                continue
            file_errors = _validate_file(spec, path)
            if file_errors:
                errors[spec.target_path] = file_errors
    return errors


def _validation_context() -> dict[str, Any]:
    return {
        "project_name": "validation",
        "workspace_path": "validation",
        "profile_name": "guided-small",
        "detected_stack": [],
        "detected_stack_text": "none",
        "existing_control_plane": [],
        "missing_control_plane": [],
        "existing_codex_assets": [],
        "risk_text": "No initial risks detected.",
        "generated_at": "1970-01-01T00:00:00+00:00",
    }


def _validate_file(spec: TemplateSpec, path: Path) -> list[str]:
    text = _read_validation_text(path)
    if text is None:
        return ["unable to read rendered file"]
    marker_errors = _unresolved_marker_errors(text)
    if spec.validation_kind == "agent":
        return marker_errors + validate_agent_file(path)
    if spec.validation_kind == "hook":
        return marker_errors + validate_hook_file(path)
    if spec.validation_kind == "hook_json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            return marker_errors + [f"invalid json: {exc}"]
        errors = _validate_hook_json(data)
        return marker_errors + errors
    if spec.validation_kind == "eval_json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            return marker_errors + [f"invalid json: {exc}"]
        errors = []
        if not isinstance(data, dict):
            errors.append("eval json must be an object")
        elif not isinstance(data.get("cases"), list):
            errors.append("cases must be a list")
        return marker_errors + errors
    if spec.validation_kind == "toml":
        try:
            tomllib.loads(text)
        except tomllib.TOMLDecodeError as exc:
            return marker_errors + [f"invalid toml: {exc}"]
    return marker_errors


def _read_validation_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _unresolved_marker_errors(text: str) -> list[str]:
    markers = sorted(set(PLACEHOLDER_PATTERN.findall(text)))
    return [f"unresolved substitution marker: {marker}" for marker in markers]


def _validate_hook_json(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["hook json must be an object"]
    hook_events = data.get("hooks", data)
    if not isinstance(hook_events, dict):
        return ["hook json hooks must be an object"]
    errors: list[str] = []
    for event in REQUIRED_HOOK_EVENTS:
        value = hook_events.get(event)
        if value is None:
            errors.append(f"missing hook event: {event}")
        elif not isinstance(value, list):
            errors.append(f"hook event must be a list: {event}")
        else:
            for index, group in enumerate(value):
                if not isinstance(group, dict):
                    errors.append(f"hook event group must be an object: {event}[{index}]")
                    continue
                commands = group.get("hooks")
                if not isinstance(commands, list) or not commands:
                    errors.append(f"hook event group hooks must be a non-empty list: {event}[{index}]")
                    continue
                for hook_index, hook in enumerate(commands):
                    if not isinstance(hook, dict):
                        errors.append(f"hook command must be an object: {event}[{index}].hooks[{hook_index}]")
                        continue
                    if hook.get("type") != "command":
                        errors.append(f"hook command type must be command: {event}[{index}].hooks[{hook_index}]")
                    command = hook.get("command")
                    if not isinstance(command, str) or not command.strip():
                        errors.append(f"hook command must be a non-empty string: {event}[{index}].hooks[{hook_index}]")
    return errors


def _unique(items: list[str]) -> list[str]:
    unique: list[str] = []
    for item in items:
        if item not in unique:
            unique.append(item)
    return unique
