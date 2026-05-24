from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = PLUGIN_ROOT / "assets" / "templates"

SUPPORTED_PLACEHOLDERS = {
    "project_name",
    "workspace_path",
    "profile_name",
    "detected_stack",
    "detected_stack_text",
    "existing_control_plane",
    "missing_control_plane",
    "existing_codex_assets",
    "risk_text",
    "generated_at",
}
PLACEHOLDER_PATTERN = re.compile(r"\{([a-zA-Z0-9_]+)\}")


@dataclass(frozen=True)
class TemplateSpec:
    key: str
    category: str
    source_path: Path
    target_path: str
    validation_kind: str = "text"
    managed_section: str = ""


def _spec(
    key: str,
    category: str,
    source: str,
    target: str,
    validation_kind: str = "text",
    managed_section: str = "",
) -> TemplateSpec:
    return TemplateSpec(
        key=key,
        category=category,
        source_path=TEMPLATE_ROOT / source,
        target_path=target,
        validation_kind=validation_kind,
        managed_section=managed_section,
    )


_TEMPLATES: tuple[TemplateSpec, ...] = (
    _spec("agents-md", "control-plane", "control-plane/AGENTS.md", "AGENTS.md", managed_section="project-rules"),
    _spec("requirements", "control-plane", "control-plane/REQUIREMENTS.md", "REQUIREMENTS.md", managed_section="requirements"),
    _spec("plan", "control-plane", "control-plane/PLAN.md", "PLAN.md", managed_section="plan"),
    _spec("test", "control-plane", "control-plane/TEST.md", "TEST.md", managed_section="test-plan"),
    _spec("evals", "control-plane", "control-plane/EVALS.md", "EVALS.md", managed_section="evals"),
    _spec("runlog", "control-plane", "control-plane/RUNLOG.md", "RUNLOG.md", managed_section="runlog"),
    _spec("config", "config", "config/config.toml", ".codex/config.toml", "toml"),
    _spec("agent-product-manager", "agents", "agents/product-manager.toml", ".codex/agents/product-manager.toml", "agent"),
    _spec("agent-architect", "agents", "agents/architect.toml", ".codex/agents/architect.toml", "agent"),
    _spec("agent-explorer", "agents", "agents/explorer.toml", ".codex/agents/explorer.toml", "agent"),
    _spec("agent-builder", "agents", "agents/builder.toml", ".codex/agents/builder.toml", "agent"),
    _spec("agent-tester", "agents", "agents/tester.toml", ".codex/agents/tester.toml", "agent"),
    _spec("agent-reviewer", "agents", "agents/reviewer.toml", ".codex/agents/reviewer.toml", "agent"),
    _spec("agent-docs-maintainer", "agents", "agents/docs-maintainer.toml", ".codex/agents/docs-maintainer.toml", "agent"),
    _spec("agent-release-operator", "agents", "agents/release-operator.toml", ".codex/agents/release-operator.toml", "agent"),
    _spec("hooks-json", "hooks", "hooks/hooks.json", ".codex/hooks/hooks.json", "hook_json"),
    _spec("hook-session-start", "hooks", "hooks/session_start_context.py", ".codex/hooks/session_start_context.py", "hook"),
    _spec("hook-pre-tool-use", "hooks", "hooks/pre_tool_use_policy.py", ".codex/hooks/pre_tool_use_policy.py", "hook"),
    _spec("hook-permission-request", "hooks", "hooks/permission_request_summary.py", ".codex/hooks/permission_request_summary.py", "hook"),
    _spec("hook-post-tool-use", "hooks", "hooks/post_tool_use_evidence.py", ".codex/hooks/post_tool_use_evidence.py", "hook"),
    _spec("hook-stop", "hooks", "hooks/stop_runlog_reminder.py", ".codex/hooks/stop_runlog_reminder.py", "hook"),
    _spec("workflow-source-context-pack", "workflows", "workflows/source-context-pack.md", ".codex/workflows/source-context-pack.md"),
    _spec("workflow-worktree-ownership", "workflows", "workflows/worktree-ownership.md", ".codex/workflows/worktree-ownership.md"),
    _spec("workflow-build-slice", "workflows", "workflows/build-slice.md", ".codex/workflows/build-slice.md"),
    _spec("workflow-review-slice", "workflows", "workflows/review-slice.md", ".codex/workflows/review-slice.md"),
    _spec("workflow-release-packet", "workflows", "workflows/release-packet.md", ".codex/workflows/release-packet.md"),
    _spec("workflow-runlog-compaction", "workflows", "workflows/runlog-compaction.md", ".codex/workflows/runlog-compaction.md"),
    _spec("runlog-archive-readme", "runlogs", "runlogs/archive/README.md", ".codex/runlogs/archive/README.md"),
    _spec("eval-project-readiness", "evals", "evals/project-readiness.json", ".codex/evals/project-readiness.json", "eval_json"),
    _spec("eval-handoff-completeness", "evals", "evals/handoff-completeness.json", ".codex/evals/handoff-completeness.json", "eval_json"),
    _spec("eval-renderer-fixtures", "evals", "evals/renderer-fixtures.json", ".codex/evals/renderer-fixtures.json", "eval_json"),
    _spec("automation-candidate", "automations", "automations/automation-candidate.md", ".codex/automation-candidates/automation-candidate.md"),
    _spec("pr-body", "pr", "pr/pr-body.md", ".codex/pr/pr-body.md"),
    _spec("release-notes", "pr", "pr/release-notes.md", ".codex/pr/release-notes.md"),
)


def required_templates() -> tuple[TemplateSpec, ...]:
    return _TEMPLATES


def template_by_target(target_path: str) -> TemplateSpec:
    normalized = target_path.replace("\\", "/")
    for item in _TEMPLATES:
        if item.target_path == normalized:
            return item
    raise KeyError(target_path)


def render_template(item: TemplateSpec, context: dict[str, Any]) -> str:
    text = item.source_path.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in SUPPORTED_PLACEHOLDERS:
            return match.group(0)
        if key not in context:
            raise KeyError(key)
        return _render_value(context[key])

    return PLACEHOLDER_PATTERN.sub(replace, text)


def _render_value(value: Any) -> str:
    if isinstance(value, set):
        items = sorted((_render_string(item) for item in value), key=str)
        return "none" if not items else ", ".join(items)
    if isinstance(value, (list, tuple)):
        items = [_render_string(item) for item in value]
        return "none" if not items else ", ".join(items)
    return _render_string(value)


def _render_string(value: Any) -> str:
    return str(value).replace("\\", "\\\\").replace('"', '\\"')
