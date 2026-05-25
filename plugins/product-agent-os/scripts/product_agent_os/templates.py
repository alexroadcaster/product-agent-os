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
    _spec(
        "workflow-development-standards",
        "workflows",
        "workflows/development-standards.md",
        ".codex/workflows/development-standards.md",
    ),
    _spec(
        "workflow-documentation-system",
        "workflows",
        "workflows/documentation-system.md",
        ".codex/workflows/documentation-system.md",
    ),
    _spec(
        "workflow-first-run-intake",
        "workflows",
        "workflows/first-run-intake.md",
        ".codex/workflows/first-run-intake.md",
    ),
    _spec(
        "workflow-bug-rescue",
        "workflows",
        "workflows/bug-rescue.md",
        ".codex/workflows/bug-rescue.md",
    ),
    _spec(
        "workflow-greenfield-idea-to-plan",
        "workflows",
        "workflows/greenfield-idea-to-plan.md",
        ".codex/workflows/greenfield-idea-to-plan.md",
    ),
    _spec(
        "workflow-complex-system-acceleration",
        "workflows",
        "workflows/complex-system-acceleration.md",
        ".codex/workflows/complex-system-acceleration.md",
    ),
    _spec(
        "workflow-pr-review-readiness",
        "workflows",
        "workflows/pr-review-readiness.md",
        ".codex/workflows/pr-review-readiness.md",
    ),
    _spec(
        "workflow-legacy-onboarding",
        "workflows",
        "workflows/legacy-onboarding.md",
        ".codex/workflows/legacy-onboarding.md",
    ),
    _spec(
        "workflow-api-migration",
        "workflows",
        "workflows/api-migration.md",
        ".codex/workflows/api-migration.md",
    ),
    _spec(
        "workflow-ai-eval-regression",
        "workflows",
        "workflows/ai-eval-regression.md",
        ".codex/workflows/ai-eval-regression.md",
    ),
    _spec(
        "workflow-native-mobile-feature",
        "workflows",
        "workflows/native-mobile-feature.md",
        ".codex/workflows/native-mobile-feature.md",
    ),
    _spec(
        "workflow-desktop-local-first",
        "workflows",
        "workflows/desktop-local-first.md",
        ".codex/workflows/desktop-local-first.md",
    ),
    _spec(
        "workflow-data-migration",
        "workflows",
        "workflows/data-migration.md",
        ".codex/workflows/data-migration.md",
    ),
    _spec(
        "workflow-security-sensitive-change",
        "workflows",
        "workflows/security-sensitive-change.md",
        ".codex/workflows/security-sensitive-change.md",
    ),
    _spec(
        "workflow-ci-stabilization",
        "workflows",
        "workflows/ci-stabilization.md",
        ".codex/workflows/ci-stabilization.md",
    ),
    _spec(
        "workflow-release-packaging",
        "workflows",
        "workflows/release-packaging.md",
        ".codex/workflows/release-packaging.md",
    ),
    _spec("artifact-adr", "artifact-templates", "artifact-templates/adr.md", ".codex/artifact-templates/adr.md"),
    _spec(
        "artifact-architecture-overview",
        "artifact-templates",
        "artifact-templates/architecture-overview.md",
        ".codex/artifact-templates/architecture-overview.md",
    ),
    _spec(
        "artifact-architecture-review-record",
        "artifact-templates",
        "artifact-templates/architecture-review-record.md",
        ".codex/artifact-templates/architecture-review-record.md",
    ),
    _spec(
        "artifact-architecture-fitness-functions",
        "artifact-templates",
        "artifact-templates/architecture-fitness-functions.md",
        ".codex/artifact-templates/architecture-fitness-functions.md",
    ),
    _spec(
        "artifact-trust-boundary-map",
        "artifact-templates",
        "artifact-templates/trust-boundary-map.md",
        ".codex/artifact-templates/trust-boundary-map.md",
    ),
    _spec(
        "artifact-architecture-docs-tooling-decision",
        "artifact-templates",
        "artifact-templates/architecture-docs-tooling-decision.md",
        ".codex/artifact-templates/architecture-docs-tooling-decision.md",
    ),
    _spec(
        "artifact-domain-modeling",
        "artifact-templates",
        "artifact-templates/domain-modeling.md",
        ".codex/artifact-templates/domain-modeling.md",
    ),
    _spec(
        "artifact-metric-spec",
        "artifact-templates",
        "artifact-templates/metric-spec.md",
        ".codex/artifact-templates/metric-spec.md",
    ),
    _spec(
        "artifact-product-brief",
        "artifact-templates",
        "artifact-templates/product-brief.md",
        ".codex/artifact-templates/product-brief.md",
    ),
    _spec(
        "artifact-value-proposition",
        "artifact-templates",
        "artifact-templates/value-proposition.md",
        ".codex/artifact-templates/value-proposition.md",
    ),
    _spec(
        "artifact-opportunity-tree",
        "artifact-templates",
        "artifact-templates/opportunity-tree.md",
        ".codex/artifact-templates/opportunity-tree.md",
    ),
    _spec(
        "artifact-experiment-plan",
        "artifact-templates",
        "artifact-templates/experiment-plan.md",
        ".codex/artifact-templates/experiment-plan.md",
    ),
    _spec(
        "artifact-tracking-plan",
        "artifact-templates",
        "artifact-templates/tracking-plan.md",
        ".codex/artifact-templates/tracking-plan.md",
    ),
    _spec(
        "artifact-api-contract-review",
        "artifact-templates",
        "artifact-templates/api-contract-review.md",
        ".codex/artifact-templates/api-contract-review.md",
    ),
    _spec(
        "artifact-component-card",
        "artifact-templates",
        "artifact-templates/component-card.md",
        ".codex/artifact-templates/component-card.md",
    ),
    _spec(
        "artifact-database-dictionary",
        "artifact-templates",
        "artifact-templates/database-dictionary.md",
        ".codex/artifact-templates/database-dictionary.md",
    ),
    _spec(
        "artifact-agent-task-packet",
        "artifact-templates",
        "artifact-templates/agent-task-packet.md",
        ".codex/artifact-templates/agent-task-packet.md",
    ),
    _spec(
        "artifact-behavioral-eval-case",
        "artifact-templates",
        "artifact-templates/behavioral-eval-case.md",
        ".codex/artifact-templates/behavioral-eval-case.md",
    ),
    _spec(
        "artifact-plan-quality-check",
        "artifact-templates",
        "artifact-templates/plan-quality-check.md",
        ".codex/artifact-templates/plan-quality-check.md",
    ),
    _spec(
        "artifact-codex-compatibility-report",
        "artifact-templates",
        "artifact-templates/codex-compatibility-report.md",
        ".codex/artifact-templates/codex-compatibility-report.md",
    ),
    _spec(
        "artifact-bug-rescue-report",
        "artifact-templates",
        "artifact-templates/bug-rescue-report.md",
        ".codex/artifact-templates/bug-rescue-report.md",
    ),
    _spec(
        "artifact-greenfield-idea-brief",
        "artifact-templates",
        "artifact-templates/greenfield-idea-brief.md",
        ".codex/artifact-templates/greenfield-idea-brief.md",
    ),
    _spec(
        "artifact-acceptance-scenarios",
        "artifact-templates",
        "artifact-templates/acceptance-scenarios.md",
        ".codex/artifact-templates/acceptance-scenarios.md",
    ),
    _spec(
        "artifact-requirement-registry",
        "artifact-templates",
        "artifact-templates/requirement-registry.md",
        ".codex/artifact-templates/requirement-registry.md",
    ),
    _spec(
        "artifact-stakeholder-owner-map",
        "artifact-templates",
        "artifact-templates/stakeholder-owner-map.md",
        ".codex/artifact-templates/stakeholder-owner-map.md",
    ),
    _spec(
        "artifact-story-slice-map",
        "artifact-templates",
        "artifact-templates/story-slice-map.md",
        ".codex/artifact-templates/story-slice-map.md",
    ),
    _spec(
        "artifact-requirements-traceability-matrix",
        "artifact-templates",
        "artifact-templates/requirements-traceability-matrix.md",
        ".codex/artifact-templates/requirements-traceability-matrix.md",
    ),
    _spec(
        "artifact-business-rules",
        "artifact-templates",
        "artifact-templates/business-rules.md",
        ".codex/artifact-templates/business-rules.md",
    ),
    _spec(
        "artifact-example-map",
        "artifact-templates",
        "artifact-templates/example-map.md",
        ".codex/artifact-templates/example-map.md",
    ),
    _spec(
        "artifact-requirement-change-impact",
        "artifact-templates",
        "artifact-templates/requirement-change-impact.md",
        ".codex/artifact-templates/requirement-change-impact.md",
    ),
    _spec(
        "artifact-domain-review-record",
        "artifact-templates",
        "artifact-templates/domain-review-record.md",
        ".codex/artifact-templates/domain-review-record.md",
    ),
    _spec(
        "artifact-docs-tooling-decision",
        "artifact-templates",
        "artifact-templates/docs-tooling-decision.md",
        ".codex/artifact-templates/docs-tooling-decision.md",
    ),
    _spec(
        "artifact-governance-proposal",
        "artifact-templates",
        "artifact-templates/governance-proposal.md",
        ".codex/artifact-templates/governance-proposal.md",
    ),
    _spec(
        "artifact-integration-catalog",
        "artifact-templates",
        "artifact-templates/integration-catalog.md",
        ".codex/artifact-templates/integration-catalog.md",
    ),
    _spec(
        "artifact-pr-risk-review",
        "artifact-templates",
        "artifact-templates/pr-risk-review.md",
        ".codex/artifact-templates/pr-risk-review.md",
    ),
    _spec(
        "artifact-onboarding-map",
        "artifact-templates",
        "artifact-templates/onboarding-map.md",
        ".codex/artifact-templates/onboarding-map.md",
    ),
    _spec(
        "artifact-migration-plan",
        "artifact-templates",
        "artifact-templates/migration-plan.md",
        ".codex/artifact-templates/migration-plan.md",
    ),
    _spec(
        "artifact-ai-eval-spec",
        "artifact-templates",
        "artifact-templates/ai-eval-spec.md",
        ".codex/artifact-templates/ai-eval-spec.md",
    ),
    _spec(
        "artifact-security-risk-review",
        "artifact-templates",
        "artifact-templates/security-risk-review.md",
        ".codex/artifact-templates/security-risk-review.md",
    ),
    _spec(
        "artifact-ci-stabilization-report",
        "artifact-templates",
        "artifact-templates/ci-stabilization-report.md",
        ".codex/artifact-templates/ci-stabilization-report.md",
    ),
    _spec(
        "artifact-release-readiness",
        "artifact-templates",
        "artifact-templates/release-readiness.md",
        ".codex/artifact-templates/release-readiness.md",
    ),
    _spec(
        "artifact-test-eval-matrix",
        "artifact-templates",
        "artifact-templates/test-eval-matrix.md",
        ".codex/artifact-templates/test-eval-matrix.md",
    ),
    _spec(
        "artifact-quality-strategy",
        "artifact-templates",
        "artifact-templates/quality-strategy.md",
        ".codex/artifact-templates/quality-strategy.md",
    ),
    _spec(
        "artifact-ci-evidence-record",
        "artifact-templates",
        "artifact-templates/ci-evidence-record.md",
        ".codex/artifact-templates/ci-evidence-record.md",
    ),
    _spec(
        "artifact-flaky-test-policy",
        "artifact-templates",
        "artifact-templates/flaky-test-policy.md",
        ".codex/artifact-templates/flaky-test-policy.md",
    ),
    _spec(
        "artifact-manual-qa-evidence",
        "artifact-templates",
        "artifact-templates/manual-qa-evidence.md",
        ".codex/artifact-templates/manual-qa-evidence.md",
    ),
    _spec(
        "artifact-model-reasoning-policy",
        "artifact-templates",
        "artifact-templates/model-reasoning-policy.md",
        ".codex/artifact-templates/model-reasoning-policy.md",
    ),
    _spec(
        "artifact-mcp-permission-review",
        "artifact-templates",
        "artifact-templates/mcp-permission-review.md",
        ".codex/artifact-templates/mcp-permission-review.md",
    ),
    _spec(
        "artifact-hook-governance",
        "artifact-templates",
        "artifact-templates/hook-governance.md",
        ".codex/artifact-templates/hook-governance.md",
    ),
    _spec(
        "artifact-skill-promotion-record",
        "artifact-templates",
        "artifact-templates/skill-promotion-record.md",
        ".codex/artifact-templates/skill-promotion-record.md",
    ),
    _spec(
        "artifact-agent-eval-workflow",
        "artifact-templates",
        "artifact-templates/agent-eval-workflow.md",
        ".codex/artifact-templates/agent-eval-workflow.md",
    ),
    _spec("runlog-archive-readme", "runlogs", "runlogs/archive/README.md", ".codex/runlogs/archive/README.md"),
    _spec("eval-project-readiness", "evals", "evals/project-readiness.json", ".codex/evals/project-readiness.json", "eval_json"),
    _spec("eval-handoff-completeness", "evals", "evals/handoff-completeness.json", ".codex/evals/handoff-completeness.json", "eval_json"),
    _spec("eval-renderer-fixtures", "evals", "evals/renderer-fixtures.json", ".codex/evals/renderer-fixtures.json", "eval_json"),
    _spec("eval-behavioral-workflows", "evals", "evals/behavioral-workflows.json", ".codex/evals/behavioral-workflows.json", "eval_json"),
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
