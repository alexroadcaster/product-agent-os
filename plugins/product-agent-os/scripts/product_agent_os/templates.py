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


AI_RAG_TEMPLATE_ALIASES = {
    "ai-prompt-contract.md": "prompt-contract.md",
    "ai-model-decision-record.md": "model-decision-record.md",
    "rag-grounding-eval.md": "rag-eval-report.md",
    "agent-handoff-contract.md": "agent-task-packet.md",
}

SECURITY_TEMPLATE_ALIASES = {
    "threat-model.md": "threat-surface.md",
    "asvs-mapping.md": "asvs-ssdf-mapping.md",
    "secrets-inventory.md": "secrets-policy.md",
    "authz-matrix.md": "authz-negative-test-matrix.md",
    "audit-log-policy.md": "audit-logging-review.md",
    "compliance-applicability-matrix.md": "compliance-overlay.md",
}

DELIVERY_TEMPLATE_ALIASES = {
    "release-scope.md": "release-readiness.md",
    "version-impact-record.md": "versioning-policy.md",
    "artifact-manifest.md": "release-artifact-manifest.md",
    "rollout-strategy.md": "rollout-plan.md",
    "ci-cd-governance.md": "ci-cd-workflow-inventory.md",
    "incident-response-path.md": "incident-record.md",
    "post-release-measurement.md": "post-release-review.md",
}

CODEX_TEMPLATE_ALIASES = {
    "agent-eval-case.md": "agent-eval-workflow.md",
    "agentic-workflow-readiness.md": "project-readiness.json",
    "context-memory-policy.md": "model-reasoning-policy.md",
    "hook-activation-record.md": "hook-governance.md",
    "skill-candidate.md": "skill-promotion-record.md",
    "skill-failure-log.md": "skill-promotion-record.md",
}

FRONTEND_TEMPLATE_ALIASES = {
    "accessibility-review.md": "frontend-accessibility-review.md",
    "component-state-matrix.md": "frontend-state-matrix.md",
    "design-system-inventory.md": "component-card.md",
    "design-tokens-reference.md": "component-card.md",
    "frontend-api-dependency-map.md": "frontend-flow-spec.md",
    "frontend-boundary-map.md": "component-card.md",
    "frontend-browser-support-matrix.md": "frontend-visual-qa.md",
    "frontend-content-i18n-record.md": "frontend-flow-spec.md",
    "frontend-interaction-test-matrix.md": "frontend-flow-spec.md",
    "fsd-boundary-record.md": "component-card.md",
    "keyboard-focus-map.md": "frontend-accessibility-review.md",
    "responsive-viewport-matrix.md": "frontend-visual-qa.md",
    "route-page-inventory.md": "frontend-flow-spec.md",
    "storybook-story-map.md": "component-card.md",
    "ui-flow-spec.md": "frontend-flow-spec.md",
    "visual-evidence-packet.md": "frontend-visual-qa.md",
}

QUALITY_TEMPLATE_ALIASES = {
    "bug-reproduction.md": "bug-rescue-report.md",
    "ci-quality-gates.md": "ci-evidence-record.md",
    "contract-test-map.md": "api-contract-review.md",
    "coverage-policy.md": "quality-strategy.md",
    "evidence-packet.md": "RUNLOG.md",
    "flaky-test-ledger.md": "flaky-test-policy.md",
    "manual-qa-charter.md": "manual-qa-evidence.md",
    "mutation-test-report.md": "test-eval-matrix.md",
    "property-test-spec.md": "test-eval-matrix.md",
    "red-green-refactor-log.md": "test-eval-matrix.md",
    "regression-impact-map.md": "test-eval-matrix.md",
    "risk-based-test-plan.md": "quality-strategy.md",
    "runtime-evidence.md": "manual-qa-evidence.md",
    "visual-a11y-evidence.md": "manual-qa-evidence.md",
}

REQUIREMENTS_TEMPLATE_ALIASES = {
    "context-map.md": "architecture-overview.md",
    "event-catalog.md": "requirements-traceability-matrix.md",
    "glossary.md": "domain-modeling.md",
    "ubiquitous-language.md": "domain-modeling.md",
}

ARCHITECTURE_TEMPLATE_ALIASES = {
    "architecture.md": "architecture-overview.md",
    "architecture-tradeoff-record.md": "adr.md",
    "boundary-responsibility-map.md": "architecture-review-record.md",
    "dependency-rules.md": "architecture-fitness-functions.md",
    "docs-tooling-decision.md": "architecture-docs-tooling-decision.md",
    "quality-attribute-scenarios.md": "architecture-fitness-functions.md",
    "runtime-topology.md": "architecture-overview.md",
}

DELIVERY_SOURCE_TEMPLATE_ALIASES = {
    "runbook.md": "operations-runbook.md",
    "slo.md": "slo-spec.md",
}

SOURCE_ARTIFACT_TEMPLATE_ALIASES = {
    **AI_RAG_TEMPLATE_ALIASES,
    **SECURITY_TEMPLATE_ALIASES,
    **DELIVERY_TEMPLATE_ALIASES,
    **CODEX_TEMPLATE_ALIASES,
    **FRONTEND_TEMPLATE_ALIASES,
    **QUALITY_TEMPLATE_ALIASES,
    **REQUIREMENTS_TEMPLATE_ALIASES,
    **ARCHITECTURE_TEMPLATE_ALIASES,
    **DELIVERY_SOURCE_TEMPLATE_ALIASES,
}


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
    _spec("artifact-task-start-brief", "artifact-templates", "artifact-templates/task-start-brief.md", ".codex/artifact-templates/task-start-brief.md"),
    _spec("artifact-completion-ledger", "artifact-templates", "artifact-templates/completion-ledger.md", ".codex/artifact-templates/completion-ledger.md"),
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
    _spec(
        "workflow-task-plan-lifecycle",
        "workflows",
        "workflows/task-plan-lifecycle.md",
        ".codex/workflows/task-plan-lifecycle.md",
    ),
    _spec(
        "workflow-control-plane-sync",
        "workflows",
        "workflows/control-plane-sync.md",
        ".codex/workflows/control-plane-sync.md",
    ),
    _spec("workflow-review-slice", "workflows", "workflows/review-slice.md", ".codex/workflows/review-slice.md"),
    _spec("workflow-release-packet", "workflows", "workflows/release-packet.md", ".codex/workflows/release-packet.md"),
    _spec("workflow-runlog-compaction", "workflows", "workflows/runlog-compaction.md", ".codex/workflows/runlog-compaction.md"),
    _spec(
        "workflow-system-file-hygiene-audit",
        "workflows",
        "workflows/system-file-hygiene-audit.md",
        ".codex/workflows/system-file-hygiene-audit.md",
    ),
    _spec(
        "workflow-development-standards",
        "workflows",
        "workflows/development-standards.md",
        ".codex/workflows/development-standards.md",
    ),
    _spec(
        "workflow-coding-standards",
        "workflows",
        "workflows/coding-standards.md",
        ".codex/workflows/coding-standards.md",
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
        "workflow-project-formation",
        "workflows",
        "workflows/project-formation.md",
        ".codex/workflows/project-formation.md",
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
        "artifact-question-ledger",
        "artifact-templates",
        "artifact-templates/question-ledger.md",
        ".codex/artifact-templates/question-ledger.md",
    ),
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
        "artifact-api-inventory",
        "artifact-templates",
        "artifact-templates/api-inventory.md",
        ".codex/artifact-templates/api-inventory.md",
    ),
    _spec(
        "artifact-api-error-catalog",
        "artifact-templates",
        "artifact-templates/api-error-catalog.md",
        ".codex/artifact-templates/api-error-catalog.md",
    ),
    _spec(
        "artifact-api-auth-authorization-matrix",
        "artifact-templates",
        "artifact-templates/api-auth-authorization-matrix.md",
        ".codex/artifact-templates/api-auth-authorization-matrix.md",
    ),
    _spec(
        "artifact-api-consumer-map",
        "artifact-templates",
        "artifact-templates/api-consumer-map.md",
        ".codex/artifact-templates/api-consumer-map.md",
    ),
    _spec(
        "artifact-api-compatibility-record",
        "artifact-templates",
        "artifact-templates/api-compatibility-record.md",
        ".codex/artifact-templates/api-compatibility-record.md",
    ),
    _spec(
        "artifact-api-contract-test-matrix",
        "artifact-templates",
        "artifact-templates/api-contract-test-matrix.md",
        ".codex/artifact-templates/api-contract-test-matrix.md",
    ),
    _spec(
        "artifact-generated-sdk-manifest",
        "artifact-templates",
        "artifact-templates/generated-sdk-manifest.md",
        ".codex/artifact-templates/generated-sdk-manifest.md",
    ),
    _spec(
        "artifact-webhook-event-contract",
        "artifact-templates",
        "artifact-templates/webhook-event-contract.md",
        ".codex/artifact-templates/webhook-event-contract.md",
    ),
    _spec(
        "artifact-external-integration-approval",
        "artifact-templates",
        "artifact-templates/external-integration-approval.md",
        ".codex/artifact-templates/external-integration-approval.md",
    ),
    _spec(
        "artifact-api-style-guide",
        "artifact-templates",
        "artifact-templates/api-style-guide.md",
        ".codex/artifact-templates/api-style-guide.md",
    ),
    _spec(
        "artifact-component-card",
        "artifact-templates",
        "artifact-templates/component-card.md",
        ".codex/artifact-templates/component-card.md",
    ),
    _spec(
        "artifact-database-inventory",
        "artifact-templates",
        "artifact-templates/database-inventory.md",
        ".codex/artifact-templates/database-inventory.md",
    ),
    _spec(
        "artifact-database-dictionary",
        "artifact-templates",
        "artifact-templates/database-dictionary.md",
        ".codex/artifact-templates/database-dictionary.md",
    ),
    _spec(
        "artifact-database-migration-plan",
        "artifact-templates",
        "artifact-templates/database-migration-plan.md",
        ".codex/artifact-templates/database-migration-plan.md",
    ),
    _spec(
        "artifact-database-expand-contract-record",
        "artifact-templates",
        "artifact-templates/database-expand-contract-record.md",
        ".codex/artifact-templates/database-expand-contract-record.md",
    ),
    _spec(
        "artifact-database-backfill-runbook",
        "artifact-templates",
        "artifact-templates/database-backfill-runbook.md",
        ".codex/artifact-templates/database-backfill-runbook.md",
    ),
    _spec(
        "artifact-database-rollback-feasibility",
        "artifact-templates",
        "artifact-templates/database-rollback-feasibility.md",
        ".codex/artifact-templates/database-rollback-feasibility.md",
    ),
    _spec(
        "artifact-database-backup-restore-evidence",
        "artifact-templates",
        "artifact-templates/database-backup-restore-evidence.md",
        ".codex/artifact-templates/database-backup-restore-evidence.md",
    ),
    _spec(
        "artifact-database-data-classification-matrix",
        "artifact-templates",
        "artifact-templates/database-data-classification-matrix.md",
        ".codex/artifact-templates/database-data-classification-matrix.md",
    ),
    _spec(
        "artifact-database-data-quality-checks",
        "artifact-templates",
        "artifact-templates/database-data-quality-checks.md",
        ".codex/artifact-templates/database-data-quality-checks.md",
    ),
    _spec(
        "artifact-database-data-contract",
        "artifact-templates",
        "artifact-templates/database-data-contract.md",
        ".codex/artifact-templates/database-data-contract.md",
    ),
    _spec(
        "artifact-database-lineage-map",
        "artifact-templates",
        "artifact-templates/database-lineage-map.md",
        ".codex/artifact-templates/database-lineage-map.md",
    ),
    _spec(
        "artifact-database-query-performance-review",
        "artifact-templates",
        "artifact-templates/database-query-performance-review.md",
        ".codex/artifact-templates/database-query-performance-review.md",
    ),
    _spec(
        "artifact-database-retention-deletion-policy",
        "artifact-templates",
        "artifact-templates/database-retention-deletion-policy.md",
        ".codex/artifact-templates/database-retention-deletion-policy.md",
    ),
    _spec(
        "artifact-database-synthetic-fixtures-policy",
        "artifact-templates",
        "artifact-templates/database-synthetic-fixtures-policy.md",
        ".codex/artifact-templates/database-synthetic-fixtures-policy.md",
    ),
    _spec(
        "artifact-database-production-access-approval",
        "artifact-templates",
        "artifact-templates/database-production-access-approval.md",
        ".codex/artifact-templates/database-production-access-approval.md",
    ),
    _spec(
        "artifact-agent-task-packet",
        "artifact-templates",
        "artifact-templates/agent-task-packet.md",
        ".codex/artifact-templates/agent-task-packet.md",
    ),
    _spec(
        "artifact-code-change-contract",
        "artifact-templates",
        "artifact-templates/code-change-contract.md",
        ".codex/artifact-templates/code-change-contract.md",
    ),
    _spec(
        "artifact-code-quality-profile",
        "artifact-templates",
        "artifact-templates/code-quality-profile.md",
        ".codex/artifact-templates/code-quality-profile.md",
    ),
    _spec(
        "artifact-coding-standard-checklist",
        "artifact-templates",
        "artifact-templates/coding-standard-checklist.md",
        ".codex/artifact-templates/coding-standard-checklist.md",
    ),
    _spec(
        "artifact-subagent-context-packet",
        "artifact-templates",
        "artifact-templates/subagent-context-packet.md",
        ".codex/artifact-templates/subagent-context-packet.md",
    ),
    _spec(
        "artifact-subagent-result-packet",
        "artifact-templates",
        "artifact-templates/subagent-result-packet.md",
        ".codex/artifact-templates/subagent-result-packet.md",
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
        "artifact-task-matrix-plan",
        "artifact-templates",
        "artifact-templates/task-matrix-plan.md",
        ".codex/artifact-templates/task-matrix-plan.md",
    ),
    _spec(
        "artifact-doubt-verification-packet",
        "artifact-templates",
        "artifact-templates/doubt-verification-packet.md",
        ".codex/artifact-templates/doubt-verification-packet.md",
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
        "artifact-ai-behavior-spec",
        "artifact-templates",
        "artifact-templates/ai-behavior-spec.md",
        ".codex/artifact-templates/ai-behavior-spec.md",
    ),
    _spec(
        "artifact-prompt-contract",
        "artifact-templates",
        "artifact-templates/prompt-contract.md",
        ".codex/artifact-templates/prompt-contract.md",
    ),
    _spec(
        "artifact-model-decision-record",
        "artifact-templates",
        "artifact-templates/model-decision-record.md",
        ".codex/artifact-templates/model-decision-record.md",
    ),
    _spec(
        "artifact-eval-run-report",
        "artifact-templates",
        "artifact-templates/eval-run-report.md",
        ".codex/artifact-templates/eval-run-report.md",
    ),
    _spec(
        "artifact-agent-skill-scorecard-ledger",
        "artifact-templates",
        "artifact-templates/agent-skill-scorecard-ledger.md",
        ".codex/artifact-templates/agent-skill-scorecard-ledger.md",
    ),
    _spec(
        "artifact-agent-skill-daily-eval-report",
        "artifact-templates",
        "artifact-templates/agent-skill-daily-eval-report.md",
        ".codex/artifact-templates/agent-skill-daily-eval-report.md",
    ),
    _spec(
        "artifact-agent-skill-weekly-verification",
        "artifact-templates",
        "artifact-templates/agent-skill-weekly-verification.md",
        ".codex/artifact-templates/agent-skill-weekly-verification.md",
    ),
    _spec(
        "artifact-agent-skill-update-candidate",
        "artifact-templates",
        "artifact-templates/agent-skill-update-candidate.md",
        ".codex/artifact-templates/agent-skill-update-candidate.md",
    ),
    _spec(
        "artifact-system-file-hygiene-report",
        "artifact-templates",
        "artifact-templates/system-file-hygiene-report.md",
        ".codex/artifact-templates/system-file-hygiene-report.md",
    ),
    _spec(
        "artifact-ai-dataset-manifest",
        "artifact-templates",
        "artifact-templates/ai-dataset-manifest.md",
        ".codex/artifact-templates/ai-dataset-manifest.md",
    ),
    _spec(
        "artifact-structured-output-schema",
        "artifact-templates",
        "artifact-templates/structured-output-schema.md",
        ".codex/artifact-templates/structured-output-schema.md",
    ),
    _spec(
        "artifact-ai-tool-contract",
        "artifact-templates",
        "artifact-templates/ai-tool-contract.md",
        ".codex/artifact-templates/ai-tool-contract.md",
    ),
    _spec(
        "artifact-rag-source-inventory",
        "artifact-templates",
        "artifact-templates/rag-source-inventory.md",
        ".codex/artifact-templates/rag-source-inventory.md",
    ),
    _spec(
        "artifact-rag-retrieval-config",
        "artifact-templates",
        "artifact-templates/rag-retrieval-config.md",
        ".codex/artifact-templates/rag-retrieval-config.md",
    ),
    _spec(
        "artifact-rag-eval-report",
        "artifact-templates",
        "artifact-templates/rag-eval-report.md",
        ".codex/artifact-templates/rag-eval-report.md",
    ),
    _spec(
        "artifact-grounding-rubric",
        "artifact-templates",
        "artifact-templates/grounding-rubric.md",
        ".codex/artifact-templates/grounding-rubric.md",
    ),
    _spec(
        "artifact-agent-workflow-map",
        "artifact-templates",
        "artifact-templates/agent-workflow-map.md",
        ".codex/artifact-templates/agent-workflow-map.md",
    ),
    _spec(
        "artifact-guardrail-matrix",
        "artifact-templates",
        "artifact-templates/guardrail-matrix.md",
        ".codex/artifact-templates/guardrail-matrix.md",
    ),
    _spec(
        "artifact-trace-evidence-packet",
        "artifact-templates",
        "artifact-templates/trace-evidence-packet.md",
        ".codex/artifact-templates/trace-evidence-packet.md",
    ),
    _spec(
        "artifact-ai-cost-latency-budget",
        "artifact-templates",
        "artifact-templates/ai-cost-latency-budget.md",
        ".codex/artifact-templates/ai-cost-latency-budget.md",
    ),
    _spec(
        "artifact-security-risk-review",
        "artifact-templates",
        "artifact-templates/security-risk-review.md",
        ".codex/artifact-templates/security-risk-review.md",
    ),
    _spec(
        "artifact-threat-surface",
        "artifact-templates",
        "artifact-templates/threat-surface.md",
        ".codex/artifact-templates/threat-surface.md",
    ),
    _spec(
        "artifact-asvs-ssdf-mapping",
        "artifact-templates",
        "artifact-templates/asvs-ssdf-mapping.md",
        ".codex/artifact-templates/asvs-ssdf-mapping.md",
    ),
    _spec(
        "artifact-authz-negative-test-matrix",
        "artifact-templates",
        "artifact-templates/authz-negative-test-matrix.md",
        ".codex/artifact-templates/authz-negative-test-matrix.md",
    ),
    _spec(
        "artifact-secrets-policy",
        "artifact-templates",
        "artifact-templates/secrets-policy.md",
        ".codex/artifact-templates/secrets-policy.md",
    ),
    _spec(
        "artifact-data-classification-register",
        "artifact-templates",
        "artifact-templates/data-classification-register.md",
        ".codex/artifact-templates/data-classification-register.md",
    ),
    _spec(
        "artifact-privacy-impact-record",
        "artifact-templates",
        "artifact-templates/privacy-impact-record.md",
        ".codex/artifact-templates/privacy-impact-record.md",
    ),
    _spec(
        "artifact-api-security-review",
        "artifact-templates",
        "artifact-templates/api-security-review.md",
        ".codex/artifact-templates/api-security-review.md",
    ),
    _spec(
        "artifact-abuse-rate-limit-plan",
        "artifact-templates",
        "artifact-templates/abuse-rate-limit-plan.md",
        ".codex/artifact-templates/abuse-rate-limit-plan.md",
    ),
    _spec(
        "artifact-supply-chain-review",
        "artifact-templates",
        "artifact-templates/supply-chain-review.md",
        ".codex/artifact-templates/supply-chain-review.md",
    ),
    _spec(
        "artifact-sbom-manifest",
        "artifact-templates",
        "artifact-templates/sbom-manifest.md",
        ".codex/artifact-templates/sbom-manifest.md",
    ),
    _spec(
        "artifact-ci-permissions-review",
        "artifact-templates",
        "artifact-templates/ci-permissions-review.md",
        ".codex/artifact-templates/ci-permissions-review.md",
    ),
    _spec(
        "artifact-audit-logging-review",
        "artifact-templates",
        "artifact-templates/audit-logging-review.md",
        ".codex/artifact-templates/audit-logging-review.md",
    ),
    _spec(
        "artifact-ai-security-review",
        "artifact-templates",
        "artifact-templates/ai-security-review.md",
        ".codex/artifact-templates/ai-security-review.md",
    ),
    _spec(
        "artifact-compliance-overlay",
        "artifact-templates",
        "artifact-templates/compliance-overlay.md",
        ".codex/artifact-templates/compliance-overlay.md",
    ),
    _spec(
        "artifact-vulnerability-response-record",
        "artifact-templates",
        "artifact-templates/vulnerability-response-record.md",
        ".codex/artifact-templates/vulnerability-response-record.md",
    ),
    _spec(
        "artifact-approval-record",
        "artifact-templates",
        "artifact-templates/approval-record.md",
        ".codex/artifact-templates/approval-record.md",
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
        "artifact-versioning-policy",
        "artifact-templates",
        "artifact-templates/versioning-policy.md",
        ".codex/artifact-templates/versioning-policy.md",
    ),
    _spec(
        "artifact-release-artifact-manifest",
        "artifact-templates",
        "artifact-templates/release-artifact-manifest.md",
        ".codex/artifact-templates/release-artifact-manifest.md",
    ),
    _spec(
        "artifact-rollout-plan",
        "artifact-templates",
        "artifact-templates/rollout-plan.md",
        ".codex/artifact-templates/rollout-plan.md",
    ),
    _spec(
        "artifact-rollback-recovery-plan",
        "artifact-templates",
        "artifact-templates/rollback-recovery-plan.md",
        ".codex/artifact-templates/rollback-recovery-plan.md",
    ),
    _spec(
        "artifact-environment-matrix",
        "artifact-templates",
        "artifact-templates/environment-matrix.md",
        ".codex/artifact-templates/environment-matrix.md",
    ),
    _spec(
        "artifact-deployment-plan",
        "artifact-templates",
        "artifact-templates/deployment-plan.md",
        ".codex/artifact-templates/deployment-plan.md",
    ),
    _spec(
        "artifact-ci-cd-workflow-inventory",
        "artifact-templates",
        "artifact-templates/ci-cd-workflow-inventory.md",
        ".codex/artifact-templates/ci-cd-workflow-inventory.md",
    ),
    _spec(
        "artifact-observability-map",
        "artifact-templates",
        "artifact-templates/observability-map.md",
        ".codex/artifact-templates/observability-map.md",
    ),
    _spec(
        "artifact-slo-spec",
        "artifact-templates",
        "artifact-templates/slo-spec.md",
        ".codex/artifact-templates/slo-spec.md",
    ),
    _spec(
        "artifact-operations-runbook",
        "artifact-templates",
        "artifact-templates/operations-runbook.md",
        ".codex/artifact-templates/operations-runbook.md",
    ),
    _spec(
        "artifact-incident-record",
        "artifact-templates",
        "artifact-templates/incident-record.md",
        ".codex/artifact-templates/incident-record.md",
    ),
    _spec(
        "artifact-postmortem",
        "artifact-templates",
        "artifact-templates/postmortem.md",
        ".codex/artifact-templates/postmortem.md",
    ),
    _spec(
        "artifact-post-release-review",
        "artifact-templates",
        "artifact-templates/post-release-review.md",
        ".codex/artifact-templates/post-release-review.md",
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
    _spec(
        "artifact-frontend-flow-spec",
        "artifact-templates",
        "artifact-templates/frontend-flow-spec.md",
        ".codex/artifact-templates/frontend-flow-spec.md",
    ),
    _spec(
        "artifact-frontend-state-matrix",
        "artifact-templates",
        "artifact-templates/frontend-state-matrix.md",
        ".codex/artifact-templates/frontend-state-matrix.md",
    ),
    _spec(
        "artifact-frontend-visual-qa",
        "artifact-templates",
        "artifact-templates/frontend-visual-qa.md",
        ".codex/artifact-templates/frontend-visual-qa.md",
    ),
    _spec(
        "artifact-frontend-accessibility-review",
        "artifact-templates",
        "artifact-templates/frontend-accessibility-review.md",
        ".codex/artifact-templates/frontend-accessibility-review.md",
    ),
    _spec(
        "artifact-frontend-performance-budget",
        "artifact-templates",
        "artifact-templates/frontend-performance-budget.md",
        ".codex/artifact-templates/frontend-performance-budget.md",
    ),
    _spec(
        "artifact-backend-service-overview",
        "artifact-templates",
        "artifact-templates/backend-service-overview.md",
        ".codex/artifact-templates/backend-service-overview.md",
    ),
    _spec(
        "artifact-backend-runtime-behavior",
        "artifact-templates",
        "artifact-templates/backend-runtime-behavior.md",
        ".codex/artifact-templates/backend-runtime-behavior.md",
    ),
    _spec(
        "artifact-backend-dependency-failure-matrix",
        "artifact-templates",
        "artifact-templates/backend-dependency-failure-matrix.md",
        ".codex/artifact-templates/backend-dependency-failure-matrix.md",
    ),
    _spec(
        "artifact-backend-observability-map",
        "artifact-templates",
        "artifact-templates/backend-observability-map.md",
        ".codex/artifact-templates/backend-observability-map.md",
    ),
    _spec(
        "artifact-backend-slo-sheet",
        "artifact-templates",
        "artifact-templates/backend-slo-sheet.md",
        ".codex/artifact-templates/backend-slo-sheet.md",
    ),
    _spec(
        "artifact-backend-health-check-contract",
        "artifact-templates",
        "artifact-templates/backend-health-check-contract.md",
        ".codex/artifact-templates/backend-health-check-contract.md",
    ),
    _spec(
        "artifact-backend-job-queue-contract",
        "artifact-templates",
        "artifact-templates/backend-job-queue-contract.md",
        ".codex/artifact-templates/backend-job-queue-contract.md",
    ),
    _spec(
        "artifact-backend-data-consistency-record",
        "artifact-templates",
        "artifact-templates/backend-data-consistency-record.md",
        ".codex/artifact-templates/backend-data-consistency-record.md",
    ),
    _spec(
        "artifact-backend-config-secrets-manifest",
        "artifact-templates",
        "artifact-templates/backend-config-secrets-manifest.md",
        ".codex/artifact-templates/backend-config-secrets-manifest.md",
    ),
    _spec(
        "artifact-backend-release-rollback-notes",
        "artifact-templates",
        "artifact-templates/backend-release-rollback-notes.md",
        ".codex/artifact-templates/backend-release-rollback-notes.md",
    ),
    _spec(
        "artifact-backend-operational-runbook",
        "artifact-templates",
        "artifact-templates/backend-operational-runbook.md",
        ".codex/artifact-templates/backend-operational-runbook.md",
    ),
    _spec("runlog-archive-readme", "runlogs", "runlogs/archive/README.md", ".codex/runlogs/archive/README.md"),
    _spec("eval-project-readiness", "evals", "evals/project-readiness.json", ".codex/evals/project-readiness.json", "eval_json"),
    _spec("eval-agent-context-contract", "evals", "evals/agent-context-contract.json", ".codex/evals/agent-context-contract.json", "eval_json"),
    _spec("eval-handoff-completeness", "evals", "evals/handoff-completeness.json", ".codex/evals/handoff-completeness.json", "eval_json"),
    _spec("eval-renderer-fixtures", "evals", "evals/renderer-fixtures.json", ".codex/evals/renderer-fixtures.json", "eval_json"),
    _spec("eval-behavioral-workflows", "evals", "evals/behavioral-workflows.json", ".codex/evals/behavioral-workflows.json", "eval_json"),
    _spec("automation-candidate", "automations", "automations/automation-candidate.md", ".codex/automation-candidates/automation-candidate.md"),
    _spec(
        "automation-system-file-hygiene-audit",
        "automations",
        "automations/system-file-hygiene-audit.md",
        ".codex/automation-candidates/system-file-hygiene-audit.md",
    ),
    _spec(
        "automation-completion-skeptic-stop-reminder",
        "automations",
        "automations/completion-skeptic-stop-reminder.md",
        ".codex/automation-candidates/completion-skeptic-stop-reminder.md",
    ),
    _spec("pr-body", "pr", "pr/pr-body.md", ".codex/pr/pr-body.md"),
    _spec("release-notes", "pr", "pr/release-notes.md", ".codex/pr/release-notes.md"),
)


def required_templates() -> tuple[TemplateSpec, ...]:
    return _TEMPLATES


def selected_templates(
    decision: dict[str, Any], existing_paths: set[str],
) -> tuple[tuple[TemplateSpec, ...], dict[str, Any]]:
    """Select staged proposals, never activate agents, hooks or automations implicitly."""
    targets: set[str] = set()
    if decision["mode"] == "full":
        targets.update({"AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"})
        targets.update({".codex/artifact-templates/code-change-contract.md",
                        ".codex/artifact-templates/quality-strategy.md"})
    elif not ({"AGENTS.md", "AGENTS.override.md"} & existing_paths):
        targets.update({"AGENTS.md", "REQUIREMENTS.md"})
    # Existing ordinary projects reuse their task/evidence sections, including
    # inline compact contracts; they do not need an extra file per decision.
    selected = tuple(item for item in _TEMPLATES if item.target_path in targets)
    report = {
        "mode": decision["mode"], "registry_count": len(_TEMPLATES),
        "selected": [item.target_path for item in selected],
        "omitted": [{"target_path": item.target_path,
                     "reason": "reuse_existing_task_context_or_not_applicable"}
                    for item in _TEMPLATES if item.target_path not in targets],
        "reason": "applicable_full_gates" if decision["mode"] == "full" else "ordinary_reuse_or_discovery",
        "gaps": decision["gaps"],
    }
    return selected, report


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
