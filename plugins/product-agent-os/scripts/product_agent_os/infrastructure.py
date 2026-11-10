from __future__ import annotations

import json
import hashlib
import re
import tempfile
import tomllib
from pathlib import Path
from typing import Any

from product_agent_os.discovery import analyze_workspace
from product_agent_os.stage_manifest import build_stage_manifest, write_stage_manifest
from product_agent_os.status_dashboard import StatusDashboardError
from product_agent_os.status_dashboard import render_status_dashboard_plan as _render_status_dashboard_plan
from product_agent_os.status_dashboard import stage_status_dashboard as _stage_status_dashboard
from product_agent_os.templates import TemplateSpec, render_template, required_templates, selected_templates
from product_agent_os.task_routing import build_task_routing, intake_receipt
from product_agent_os.validators import validate_agent_file, validate_agent_project_config, validate_hook_file
from product_agent_os.control_plane_documents import DOCUMENT_CONTRACTS, scoped_document, document_readiness


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


def render_infrastructure_plan(
    workspace: str | Path, *, task_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    workspace_path = _workspace_path(workspace)
    audit = _analyze(workspace_path)
    return _build_result(workspace_path, audit, None, write_files=False, task_context=task_context)


def render_infrastructure_from_audit(
    workspace: str | Path,
    audit: dict[str, Any],
    *,
    lifecycle_packets: dict[str, Any] | list[dict[str, Any]] | None = None,
    task_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    workspace_path = _workspace_path(workspace)
    return _build_result(
        workspace_path,
        audit,
        None,
        write_files=False,
        lifecycle_packets=lifecycle_packets,
        task_context=task_context,
    )


def stage_infrastructure(
    workspace: str | Path, output_dir: str | Path, *, task_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    workspace_path = _workspace_path(workspace)
    stage_root = Path(output_dir).resolve()
    if stage_root == workspace_path or stage_root.is_relative_to(workspace_path):
        raise InfrastructureError("stage output directory must be outside workspace")
    if stage_root.exists() and not stage_root.is_dir():
        raise InfrastructureError(f"stage output path is not a directory: {stage_root}")
    audit = _analyze(workspace_path)
    try:
        return _build_result(workspace_path, audit, stage_root, write_files=True, task_context=task_context)
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
    task_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    context = _template_context(workspace, audit)
    warnings = _profile_warnings(workspace, audit)
    approval_required = ["explicit approval required before applying staged infrastructure to workspace"]
    blocked: list[str] = []
    files: list[dict[str, Any]] = []
    proposed_content: dict[str, str] = {}
    managed_sections: list[dict[str, str]] = []
    validation_errors: dict[str, list[str]] = {}
    action_summary: dict[str, list[str]] = {
        "create": [],
        "update": [],
        "leave_unchanged": [],
        "blocked": [],
    }

    selection = None
    templates = required_templates()
    if task_context is not None:
        decision = build_task_routing(workspace, audit, task_context)
        templates, selection = selected_templates(
            decision, set(audit.get("detected_files", [])),
            evals_applicable=bool(task_context.get("evals_required") or "EVALS.md" in task_context.get("documents", {})),
        )
        selection["dependency_policy"] = "scoped documents use inline contracts; no implicit config/hooks/workflow activation"
        # Inspection can show proposals while gaps remain, but no incomplete
        # task context is allowed to produce a staged merge input.
        if write_files and decision["gaps"]:
            raise InfrastructureError("task context gaps must be resolved before staging")
    for item in templates:
        _validate_template_target(item)
        rendered = render_template(item, context)
        if task_context and item.target_path in DOCUMENT_CONTRACTS:
            rendered = scoped_document(item.target_path, item.managed_section, task_context)
        if selection is not None:
            dependencies = selection.setdefault('document_dependencies', [])
            selected_paths = {spec.target_path for spec in templates}
            for reference in sorted(set(re.findall(r'`(\.codex/[\w./-]+\.(?:md|toml|json))`', rendered))):
                status = ('existing' if (workspace / reference).is_file() else
                          'staged_proposal' if reference in selected_paths else 'gap_not_staged')
                dependencies.append({'from': item.target_path, 'path': reference, 'status': status,
                                     'claim': 'reference_only; no activation or authority'})
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
        if staged_content is not None:
            proposed_content[item.target_path] = staged_content
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
                "preserve_existing": any("managed_content_preserved" in warning for warning in file_warnings),
                "staged_path": staged_path,
                "bytes": len(staged_content.encode("utf-8")) if staged_content is not None else None,
                "content_digest": hashlib.sha256(staged_content.encode("utf-8")).hexdigest() if staged_content is not None else None,
            }
        )

    validation_errors.update(_validate_generated_files(files, stage_root, write_files, proposed_content))
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
    result["infrastructure_plan"]["intake"] = intake_receipt(task_context)
    if selection is not None:
        result["infrastructure_plan"]["template_selection"] = selection
    result["rendered_artifacts"]["document_readiness"] = {
        name: document_readiness(name, content) for name, content in proposed_content.items()
        if name in DOCUMENT_CONTRACTS
    }
    if write_files and stage_root is not None:
        # An ordinary task may reuse every file; its empty proposal still needs
        # a manifest directory, created only after the task-context gate passes.
        stage_root.mkdir(parents=True, exist_ok=True)
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
    destination.write_bytes(content.encode("utf-8"))


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
        # Rendering is a proposal, not an execution receipt. Wall clock belongs
        # in the stage manifest, otherwise unchanged input creates new diffs.
        "generated_at": "not_recorded; see stage manifest",
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
            # Managed does not mean disposable: no ancestor/template baseline
            # proves which values belong to the user. Offer a companion proposal
            # and leave the entire target byte-for-byte untouched.
            warnings.append(f"{item.target_path}: managed_content_preserved; explicit reviewed merge required")
            return "leave_unchanged", "staged_only", warnings, blocked, rendered

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
        return path.read_bytes().decode("utf-8")
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
    proposed_content: dict[str, str],
) -> dict[str, list[str]]:
    errors: dict[str, list[str]] = {}
    specs = {item.target_path: item for item in required_templates()}
    available_prompt_paths = {file["target_path"] for file in files if file["action"] != "blocked"}
    with tempfile.TemporaryDirectory(prefix="product-agent-os-render-") as tmp:
        tmp_root = Path(tmp)
        for file in files:
            if file["action"] == "blocked":
                continue
            spec = specs[file["target_path"]]
            _validate_template_target(spec)
            path = Path(file["staged_path"]) if write_files else tmp_root / spec.target_path
            if not write_files:
                _write_inside_root(tmp_root, path, proposed_content[spec.target_path])
            elif stage_root is not None and not path.resolve().is_relative_to(stage_root.resolve()):
                errors[spec.target_path] = ["staged path escapes output directory"]
                continue
            file_errors = _validate_file(
                spec,
                path,
                available_prompt_paths=available_prompt_paths,
            )
            if file_errors:
                errors[spec.target_path] = file_errors
    return errors


def _validate_file(
    spec: TemplateSpec,
    path: Path,
    *,
    available_prompt_paths: set[str] | None = None,
) -> list[str]:
    text = _read_validation_text(path)
    if text is None:
        return ["unable to read rendered file"]
    marker_errors = _unresolved_marker_errors(text)
    if spec.validation_kind == "agent":
        return marker_errors + validate_agent_file(
            path,
            available_prompt_paths=available_prompt_paths,
        )
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
        if spec.key == "config":
            return marker_errors + validate_agent_project_config(path)
    return marker_errors


def _read_validation_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _unresolved_marker_errors(text: str) -> list[str]:
    # Supplied document facts are data, not template expressions. Parse before
    # excluding the block so malformed/duplicated delimiters still fail closed.
    from product_agent_os.control_plane_documents import read_document_data, DATA_START, DATA_END
    try:
        if read_document_data(text):
            start, end = text.index(DATA_START), text.index(DATA_END) + len(DATA_END)
            text = text[:start] + text[end:]
    except ValueError as exc:
        return [str(exc)]
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
