import json
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
TEMPLATE_ROOT = ROOT / "plugins" / "product-agent-os" / "assets" / "templates"
PLUGIN_ROOT = ROOT / "plugins" / "product-agent-os"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.templates import (  # noqa: E402
    AI_RAG_TEMPLATE_ALIASES,
    DELIVERY_TEMPLATE_ALIASES,
    SECURITY_TEMPLATE_ALIASES,
    required_templates,
    render_template,
)
from product_agent_os.validators import validate_agent_file, validate_hook_file  # noqa: E402


REQUIRED_TARGETS = {
    "AGENTS.md",
    "REQUIREMENTS.md",
    "PLAN.md",
    "TEST.md",
    "EVALS.md",
    "RUNLOG.md",
    ".codex/config.toml",
    ".codex/agents/product-manager.toml",
    ".codex/agents/architect.toml",
    ".codex/agents/explorer.toml",
    ".codex/agents/builder.toml",
    ".codex/agents/tester.toml",
    ".codex/agents/reviewer.toml",
    ".codex/agents/docs-maintainer.toml",
    ".codex/agents/release-operator.toml",
    ".codex/hooks/hooks.json",
    ".codex/hooks/session_start_context.py",
    ".codex/hooks/pre_tool_use_policy.py",
    ".codex/hooks/permission_request_summary.py",
    ".codex/hooks/post_tool_use_evidence.py",
    ".codex/hooks/stop_runlog_reminder.py",
    ".codex/workflows/source-context-pack.md",
    ".codex/workflows/worktree-ownership.md",
    ".codex/workflows/build-slice.md",
    ".codex/workflows/review-slice.md",
    ".codex/workflows/release-packet.md",
    ".codex/workflows/runlog-compaction.md",
    ".codex/workflows/development-standards.md",
    ".codex/workflows/documentation-system.md",
    ".codex/workflows/first-run-intake.md",
    ".codex/workflows/bug-rescue.md",
    ".codex/workflows/greenfield-idea-to-plan.md",
    ".codex/workflows/complex-system-acceleration.md",
    ".codex/workflows/pr-review-readiness.md",
    ".codex/workflows/legacy-onboarding.md",
    ".codex/workflows/api-migration.md",
    ".codex/workflows/ai-eval-regression.md",
    ".codex/workflows/native-mobile-feature.md",
    ".codex/workflows/desktop-local-first.md",
    ".codex/workflows/data-migration.md",
    ".codex/workflows/security-sensitive-change.md",
    ".codex/workflows/ci-stabilization.md",
    ".codex/workflows/release-packaging.md",
    ".codex/artifact-templates/adr.md",
    ".codex/artifact-templates/architecture-overview.md",
    ".codex/artifact-templates/architecture-review-record.md",
    ".codex/artifact-templates/architecture-fitness-functions.md",
    ".codex/artifact-templates/trust-boundary-map.md",
    ".codex/artifact-templates/architecture-docs-tooling-decision.md",
    ".codex/artifact-templates/domain-modeling.md",
    ".codex/artifact-templates/metric-spec.md",
    ".codex/artifact-templates/product-brief.md",
    ".codex/artifact-templates/value-proposition.md",
    ".codex/artifact-templates/opportunity-tree.md",
    ".codex/artifact-templates/experiment-plan.md",
    ".codex/artifact-templates/tracking-plan.md",
    ".codex/artifact-templates/api-contract-review.md",
    ".codex/artifact-templates/api-inventory.md",
    ".codex/artifact-templates/api-error-catalog.md",
    ".codex/artifact-templates/api-auth-authorization-matrix.md",
    ".codex/artifact-templates/api-consumer-map.md",
    ".codex/artifact-templates/api-compatibility-record.md",
    ".codex/artifact-templates/api-contract-test-matrix.md",
    ".codex/artifact-templates/generated-sdk-manifest.md",
    ".codex/artifact-templates/webhook-event-contract.md",
    ".codex/artifact-templates/external-integration-approval.md",
    ".codex/artifact-templates/api-style-guide.md",
    ".codex/artifact-templates/component-card.md",
    ".codex/artifact-templates/database-inventory.md",
    ".codex/artifact-templates/database-dictionary.md",
    ".codex/artifact-templates/database-migration-plan.md",
    ".codex/artifact-templates/database-expand-contract-record.md",
    ".codex/artifact-templates/database-backfill-runbook.md",
    ".codex/artifact-templates/database-rollback-feasibility.md",
    ".codex/artifact-templates/database-backup-restore-evidence.md",
    ".codex/artifact-templates/database-data-classification-matrix.md",
    ".codex/artifact-templates/database-data-quality-checks.md",
    ".codex/artifact-templates/database-data-contract.md",
    ".codex/artifact-templates/database-lineage-map.md",
    ".codex/artifact-templates/database-query-performance-review.md",
    ".codex/artifact-templates/database-retention-deletion-policy.md",
    ".codex/artifact-templates/database-synthetic-fixtures-policy.md",
    ".codex/artifact-templates/database-production-access-approval.md",
    ".codex/artifact-templates/agent-task-packet.md",
    ".codex/artifact-templates/behavioral-eval-case.md",
    ".codex/artifact-templates/plan-quality-check.md",
    ".codex/artifact-templates/codex-compatibility-report.md",
    ".codex/artifact-templates/bug-rescue-report.md",
    ".codex/artifact-templates/greenfield-idea-brief.md",
    ".codex/artifact-templates/acceptance-scenarios.md",
    ".codex/artifact-templates/requirement-registry.md",
    ".codex/artifact-templates/stakeholder-owner-map.md",
    ".codex/artifact-templates/story-slice-map.md",
    ".codex/artifact-templates/requirements-traceability-matrix.md",
    ".codex/artifact-templates/business-rules.md",
    ".codex/artifact-templates/example-map.md",
    ".codex/artifact-templates/requirement-change-impact.md",
    ".codex/artifact-templates/domain-review-record.md",
    ".codex/artifact-templates/docs-tooling-decision.md",
    ".codex/artifact-templates/governance-proposal.md",
    ".codex/artifact-templates/integration-catalog.md",
    ".codex/artifact-templates/pr-risk-review.md",
    ".codex/artifact-templates/onboarding-map.md",
    ".codex/artifact-templates/migration-plan.md",
    ".codex/artifact-templates/ai-eval-spec.md",
    ".codex/artifact-templates/ai-behavior-spec.md",
    ".codex/artifact-templates/prompt-contract.md",
    ".codex/artifact-templates/model-decision-record.md",
    ".codex/artifact-templates/eval-run-report.md",
    ".codex/artifact-templates/ai-dataset-manifest.md",
    ".codex/artifact-templates/structured-output-schema.md",
    ".codex/artifact-templates/ai-tool-contract.md",
    ".codex/artifact-templates/rag-source-inventory.md",
    ".codex/artifact-templates/rag-retrieval-config.md",
    ".codex/artifact-templates/rag-eval-report.md",
    ".codex/artifact-templates/grounding-rubric.md",
    ".codex/artifact-templates/agent-workflow-map.md",
    ".codex/artifact-templates/guardrail-matrix.md",
    ".codex/artifact-templates/trace-evidence-packet.md",
    ".codex/artifact-templates/ai-cost-latency-budget.md",
    ".codex/artifact-templates/security-risk-review.md",
    ".codex/artifact-templates/threat-surface.md",
    ".codex/artifact-templates/asvs-ssdf-mapping.md",
    ".codex/artifact-templates/authz-negative-test-matrix.md",
    ".codex/artifact-templates/secrets-policy.md",
    ".codex/artifact-templates/data-classification-register.md",
    ".codex/artifact-templates/privacy-impact-record.md",
    ".codex/artifact-templates/api-security-review.md",
    ".codex/artifact-templates/abuse-rate-limit-plan.md",
    ".codex/artifact-templates/supply-chain-review.md",
    ".codex/artifact-templates/sbom-manifest.md",
    ".codex/artifact-templates/ci-permissions-review.md",
    ".codex/artifact-templates/audit-logging-review.md",
    ".codex/artifact-templates/ai-security-review.md",
    ".codex/artifact-templates/compliance-overlay.md",
    ".codex/artifact-templates/vulnerability-response-record.md",
    ".codex/artifact-templates/approval-record.md",
    ".codex/artifact-templates/ci-stabilization-report.md",
    ".codex/artifact-templates/release-readiness.md",
    ".codex/artifact-templates/versioning-policy.md",
    ".codex/artifact-templates/release-artifact-manifest.md",
    ".codex/artifact-templates/rollout-plan.md",
    ".codex/artifact-templates/rollback-recovery-plan.md",
    ".codex/artifact-templates/environment-matrix.md",
    ".codex/artifact-templates/deployment-plan.md",
    ".codex/artifact-templates/ci-cd-workflow-inventory.md",
    ".codex/artifact-templates/observability-map.md",
    ".codex/artifact-templates/slo-spec.md",
    ".codex/artifact-templates/operations-runbook.md",
    ".codex/artifact-templates/incident-record.md",
    ".codex/artifact-templates/postmortem.md",
    ".codex/artifact-templates/post-release-review.md",
    ".codex/artifact-templates/test-eval-matrix.md",
    ".codex/artifact-templates/quality-strategy.md",
    ".codex/artifact-templates/ci-evidence-record.md",
    ".codex/artifact-templates/flaky-test-policy.md",
    ".codex/artifact-templates/manual-qa-evidence.md",
    ".codex/artifact-templates/model-reasoning-policy.md",
    ".codex/artifact-templates/mcp-permission-review.md",
    ".codex/artifact-templates/hook-governance.md",
    ".codex/artifact-templates/skill-promotion-record.md",
    ".codex/artifact-templates/agent-eval-workflow.md",
    ".codex/artifact-templates/frontend-flow-spec.md",
    ".codex/artifact-templates/frontend-state-matrix.md",
    ".codex/artifact-templates/frontend-visual-qa.md",
    ".codex/artifact-templates/frontend-accessibility-review.md",
    ".codex/artifact-templates/frontend-performance-budget.md",
    ".codex/artifact-templates/backend-service-overview.md",
    ".codex/artifact-templates/backend-runtime-behavior.md",
    ".codex/artifact-templates/backend-dependency-failure-matrix.md",
    ".codex/artifact-templates/backend-observability-map.md",
    ".codex/artifact-templates/backend-slo-sheet.md",
    ".codex/artifact-templates/backend-health-check-contract.md",
    ".codex/artifact-templates/backend-job-queue-contract.md",
    ".codex/artifact-templates/backend-data-consistency-record.md",
    ".codex/artifact-templates/backend-config-secrets-manifest.md",
    ".codex/artifact-templates/backend-release-rollback-notes.md",
    ".codex/artifact-templates/backend-operational-runbook.md",
    ".codex/runlogs/archive/README.md",
    ".codex/evals/project-readiness.json",
    ".codex/evals/handoff-completeness.json",
    ".codex/evals/renderer-fixtures.json",
    ".codex/evals/behavioral-workflows.json",
    ".codex/automation-candidates/automation-candidate.md",
    ".codex/pr/pr-body.md",
    ".codex/pr/release-notes.md",
}

FORBIDDEN_TEXT = [
    "sk-",
    "BEGIN PRIVATE KEY",
    "PASSWORD=",
    "API_KEY=",
    "TOKEN=",
    "recurring schedule is active",
    "checks passed",
    "tests pass",
    "global ~/.codex/config.toml",
]

SCENARIO_HANDOFF_TERMS = [
    "scenario handoff",
    "sources/context used",
    "assumptions",
    "files touched",
    "files proposed",
    "verification evidence",
    "open risks",
    "recommended next role",
    "stop reason",
]


class InfrastructureTemplateTest(unittest.TestCase):
    def test_required_template_targets_are_registered_once(self):
        templates = required_templates()
        targets = [item.target_path for item in templates]

        self.assertEqual(set(targets), REQUIRED_TARGETS)
        self.assertEqual(len(targets), len(set(targets)))

    def test_ai_rag_template_names_are_canonical_and_legacy_names_are_mapped(self):
        canonical_names = {
            "prompt-contract.md",
            "model-decision-record.md",
            "rag-eval-report.md",
        }
        legacy_aliases = {
            "ai-prompt-contract.md": "prompt-contract.md",
            "ai-model-decision-record.md": "model-decision-record.md",
            "rag-grounding-eval.md": "rag-eval-report.md",
            "agent-handoff-contract.md": "agent-task-packet.md",
        }
        targets = {item.target_path for item in required_templates()}
        catalog = json.loads(
            (PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json").read_text(
                encoding="utf-8"
            )
        )
        domains = {
            domain["id"]: domain
            for domain in catalog["domains"]
            if isinstance(domain, dict) and domain.get("id")
        }
        artifacts = set(domains["llm_ai_rag"]["artifacts"])

        for canonical in canonical_names:
            with self.subTest(canonical=canonical):
                self.assertIn(f".codex/artifact-templates/{canonical}", targets)
                self.assertIn(canonical, artifacts)

        self.assertEqual(AI_RAG_TEMPLATE_ALIASES, legacy_aliases)
        for legacy, canonical in legacy_aliases.items():
            with self.subTest(legacy=legacy):
                self.assertNotIn(f".codex/artifact-templates/{legacy}", targets)
                self.assertNotIn(legacy, artifacts)
                self.assertIn(canonical, artifacts)

    def test_security_template_names_are_canonical_and_source_names_are_mapped(self):
        canonical_names = {
            "threat-surface.md",
            "asvs-ssdf-mapping.md",
            "secrets-policy.md",
            "authz-negative-test-matrix.md",
            "audit-logging-review.md",
            "compliance-overlay.md",
        }
        source_aliases = {
            "threat-model.md": "threat-surface.md",
            "asvs-mapping.md": "asvs-ssdf-mapping.md",
            "secrets-inventory.md": "secrets-policy.md",
            "authz-matrix.md": "authz-negative-test-matrix.md",
            "audit-log-policy.md": "audit-logging-review.md",
            "compliance-applicability-matrix.md": "compliance-overlay.md",
        }
        targets = {item.target_path for item in required_templates()}
        catalog = json.loads(
            (PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json").read_text(
                encoding="utf-8"
            )
        )
        domains = {
            domain["id"]: domain
            for domain in catalog["domains"]
            if isinstance(domain, dict) and domain.get("id")
        }
        artifacts = set(domains["security_privacy_compliance"]["artifacts"])

        for canonical in canonical_names:
            with self.subTest(canonical=canonical):
                self.assertIn(f".codex/artifact-templates/{canonical}", targets)
                self.assertIn(canonical, artifacts)

        self.assertEqual(SECURITY_TEMPLATE_ALIASES, source_aliases)
        for source_name, canonical in source_aliases.items():
            with self.subTest(source_name=source_name):
                self.assertNotIn(f".codex/artifact-templates/{source_name}", targets)
                self.assertNotIn(source_name, artifacts)
                self.assertIn(canonical, artifacts)

    def test_delivery_template_names_are_canonical_and_plan_names_are_mapped(self):
        plan_aliases = {
            "release-scope.md": "release-readiness.md",
            "version-impact-record.md": "versioning-policy.md",
            "artifact-manifest.md": "release-artifact-manifest.md",
            "rollout-strategy.md": "rollout-plan.md",
            "ci-cd-governance.md": "ci-cd-workflow-inventory.md",
            "incident-response-path.md": "incident-record.md",
            "post-release-measurement.md": "post-release-review.md",
        }
        catalog = json.loads(
            (PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json").read_text(
                encoding="utf-8"
            )
        )
        domains = {
            domain["id"]: domain
            for domain in catalog["domains"]
            if isinstance(domain, dict) and domain.get("id")
        }
        artifacts = set(domains["delivery_release_operations"]["artifacts"])

        self.assertEqual(DELIVERY_TEMPLATE_ALIASES, plan_aliases)
        for plan_name, canonical in plan_aliases.items():
            with self.subTest(plan_name=plan_name):
                self.assertNotIn(plan_name, artifacts)
                self.assertIn(canonical, artifacts)

    def test_delivery_release_initial_templates_cover_scope_version_and_evidence(self):
        expected_terms = {
            "release-readiness.md": [
                "release type",
                "external boundary",
                "lifecycle stage",
                "docs-only/internal/production distinction",
                "current build/test/docs/eval/runtime/artifact evidence",
                "owner evidence",
                "explicit gap",
                "inspection-only",
            ],
            "release-packet.md": [
                "release_scope_present",
                "version_impact_present",
                "changelog_release_notes_present",
                "release_evidence_present",
                "release_evidence_before_completion",
            ],
            "versioning-policy.md": [
                "semver",
                "non-semver",
                "compatibility impact",
                "deprecation",
                "migration guidance",
                "generated client",
            ],
        }
        template_dirs = [TEMPLATE_ROOT / "artifact-templates", TEMPLATE_ROOT / "workflows"]
        for name, terms in expected_terms.items():
            with self.subTest(template=name):
                path = next((directory / name for directory in template_dirs if (directory / name).is_file()), None)
                self.assertIsNotNone(path, name)
                text = path.read_text(encoding="utf-8").lower()
                for term in terms:
                    with self.subTest(template=name, term=term):
                        self.assertIn(term, text)

    def test_delivery_release_operational_templates_cover_batch_two_gates(self):
        expected_terms = {
            "release-artifact-manifest.md": [
                "artifact names",
                "versions",
                "creation command",
                "storage location",
                "retention",
                "integrity notes",
                "checksums",
                "signatures",
                "sbom",
                "provenance",
                "docs-only/no build artifact",
            ],
            "rollout-plan.md": [
                "immediate release",
                "release train",
                "staged rollout",
                "feature flag",
                "canary",
                "blue-green",
                "shadow traffic",
                "manual promotion",
                "cohorts/traffic",
                "promotion",
                "abort criteria",
                "blast radius",
                "default value",
                "flag owner",
                "targeting rules",
                "cleanup date",
                "kill switch",
                "failure mode",
                "flag presence alone does not remove release risk",
            ],
            "rollback-recovery-plan.md": [
                "revert",
                "redeploy previous artifact",
                "disable flag",
                "unpublish",
                "yank",
                "restore backup",
                "compensate data",
                "incident mitigation",
                "command/manual procedure",
                "owner",
                "residual risk",
            ],
            "environment-matrix.md": [
                "dev",
                "stage",
                "prod",
                "local",
                "mobile",
                "store",
                "registry",
                "branch/tag rules",
                "secret boundaries",
                "desired-state source",
                "reconciliation controller",
                "drift behavior",
                "approval path",
                "rollback/revert",
                "present_unverified",
            ],
            "deployment-plan.md": [
                "target environment",
                "release candidate",
                "deploy command",
                "approval",
                "rollout window",
                "stop criteria",
                "desired-state source",
                "reconciliation controller",
                "drift behavior",
                "rollback/revert",
            ],
            "approval-record.md": [
                "publish",
                "tag",
                "github release",
                "artifact upload",
                "deployment",
                "pr creation",
                "branch push",
                "package registry",
                "marketplace",
                "store submission",
                "approval_required",
                "rollback/unpublish",
            ],
            "ci-cd-workflow-inventory.md": [
                "workflow names",
                "triggers",
                "permissions",
                "secrets",
                "environments",
                "required reviewers",
                "wait timers",
                "branch/tag restrictions",
                "artifacts",
                "cache",
                "concurrency",
                "external action pinning",
                "remote ci mutation approval",
            ],
            "ci-permissions-review.md": [
                "required reviewers",
                "wait timers",
                "branch/tag restrictions",
                "external action pinning",
                "remote ci mutation approval",
            ],
            "observability-map.md": [
                "logs",
                "metrics",
                "traces",
                "dashboards",
                "alert owner",
                "redaction",
                "sampling",
                "user journey",
            ],
            "slo-spec.md": [
                "user journey",
                "sli",
                "slo",
                "measurement source",
                "alert policy",
                "accepted no-telemetry",
                "not-yet-production gap",
            ],
            "operations-runbook.md": [
                "deploy",
                "rollback",
                "first response",
                "escalation",
                "diagnostics",
                "incident criteria",
            ],
            "incident-record.md": [
                "incident criteria",
                "owner",
                "communication path",
                "timeline",
                "mitigation",
                "postmortem trigger",
            ],
            "postmortem.md": [
                "impact",
                "detection",
                "root causes",
                "contributing factors",
                "action items",
                "review status",
                "quick rollback does not skip learning",
            ],
            "post-release-review.md": [
                "metrics",
                "support signals",
                "defects",
                "latency/cost",
                "review date",
                "dora measurement source",
                "anti-goodhart",
                "product/reliability hypotheses",
            ],
            "metric-spec.md": [
                "dora measurement source",
                "change lead time",
                "deployment frequency",
                "failed deployment recovery time",
                "change fail rate",
                "deployment rework rate",
                "anti-goodhart",
                "individual performance quota",
            ],
        }
        for name, terms in expected_terms.items():
            with self.subTest(template=name):
                path = TEMPLATE_ROOT / "artifact-templates" / name
                self.assertTrue(path.is_file(), name)
                text = path.read_text(encoding="utf-8").lower()
                for term in terms:
                    with self.subTest(template=name, term=term):
                        self.assertIn(term, text)

    def test_delivery_release_templates_control_plane_and_eval_contracts(self):
        targets = {item.target_path for item in required_templates()}
        rendered_targets = {
            ".codex/artifact-templates/versioning-policy.md",
            ".codex/artifact-templates/release-artifact-manifest.md",
            ".codex/artifact-templates/rollout-plan.md",
            ".codex/artifact-templates/rollback-recovery-plan.md",
            ".codex/artifact-templates/environment-matrix.md",
            ".codex/artifact-templates/deployment-plan.md",
            ".codex/artifact-templates/ci-cd-workflow-inventory.md",
            ".codex/artifact-templates/observability-map.md",
            ".codex/artifact-templates/slo-spec.md",
            ".codex/artifact-templates/operations-runbook.md",
            ".codex/artifact-templates/incident-record.md",
            ".codex/artifact-templates/postmortem.md",
            ".codex/artifact-templates/post-release-review.md",
        }
        self.assertTrue(rendered_targets.issubset(targets))

        payloads = {
            "control-plane": "\n".join(
                (TEMPLATE_ROOT / "control-plane" / name).read_text(encoding="utf-8").lower()
                for name in ["PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
            ),
            "project-readiness.json": (TEMPLATE_ROOT / "evals" / "project-readiness.json").read_text(
                encoding="utf-8"
            ).lower(),
            "behavioral-workflows.json": (
                TEMPLATE_ROOT / "evals" / "behavioral-workflows.json"
            ).read_text(encoding="utf-8").lower(),
        }
        shared_terms = [
            "delivery_release_operations",
            "release_scope_present",
            "version_impact_present",
            "artifact_manifest_present",
            "rollout_strategy_present",
            "rollback_recovery_present",
            "ci_cd_governance_present",
            "operations_runbook_present",
            "incident_response_path_present",
            "post_release_measurement_present",
            "automation_manual_stability_present",
            "automation-candidate.md",
            "approval_required",
            "explicit_gap_accepted",
            "release-ready",
            "feature flags remove release risk",
            "gitops is automatically safe",
            "automation is safer because it is repeatable",
            "delivery_release_operations_readiness_when_release_or_operations_changes",
            "publish without approval",
            "tag without approval",
            "deployment without approval",
            "active automation without manual stability",
        ]
        for name, text in payloads.items():
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_delivery_release_final_batch_templates_cover_deep_release_operations(self):
        expected_terms = {
            "release-readiness.md": [
                "release mode policy",
                "release train",
                "continuous deployment",
                "manual approval",
                "release candidate",
                "draft release",
                "cadence",
                "promotion trigger",
                "freeze/cutoff",
                "platform distribution evidence",
                "signing",
                "notarization",
                "app store review",
                "installer/update path",
                "crash reporting",
                "platform owner evidence",
                "release communication",
                "audience",
                "support contact",
                "known issues",
                "migration/deprecation note",
                "release-notes ownership",
                "release evidence sufficiency owner review",
                "sufficient for the real release risk",
                "stop condition",
            ],
            "deployment-plan.md": [
                "build-release-run boundary",
                "immutable artifact",
                "release identifier",
                "runtime configuration boundary",
                "environment-specific config injection",
                "accepted platform exception",
            ],
            "release-artifact-manifest.md": [
                "release signing",
                "license/notice",
                "sbom/provenance",
                "package/container integrity",
                "security ownership",
                "security handoff",
            ],
            "versioning-policy.md": [
                "conventional commits",
                "semantic-release",
                "release-please",
                "manual versioning",
                "selected/rejected/deferred",
                "no forced semver tooling",
            ],
            "environment-matrix.md": [
                "required reviewers",
                "wait timers",
                "custom protection rules",
                "environment secrets",
                "deployment targets",
                "approval_required mutation boundary",
            ],
            "post-release-review.md": [
                "trend review",
                "team-only interpretation",
                "deployment rework rate",
            ],
            "metric-spec.md": [
                "team-only interpretation",
                "deployment rework rate",
            ],
            "incident-record.md": [
                "severity",
                "user-visible degradation",
                "data loss",
                "manual intervention",
                "monitoring failure",
                "customer/user impact",
            ],
            "postmortem.md": [
                "blameless",
                "owner/date",
                "customer/user impact",
            ],
            "operations-runbook.md": [
                "opentelemetry",
                "pagerduty",
                "opsgenie",
                "manual monitoring",
                "selected/rejected/deferred",
            ],
            "observability-map.md": [
                "opentelemetry",
                "prometheus",
                "grafana",
                "sentry",
                "datadog",
                "pagerduty",
                "opsgenie",
                "manual monitoring",
                "accepted no-tooling gap",
            ],
            "slo-spec.md": [
                "selected/rejected/deferred",
                "accepted no-tooling gap",
            ],
        }

        for name, terms in expected_terms.items():
            path = TEMPLATE_ROOT / "artifact-templates" / name
            self.assertTrue(path.is_file(), name)
            text = path.read_text(encoding="utf-8").lower()
            for term in terms:
                with self.subTest(template=name, term=term):
                    self.assertIn(term, text)

    def test_security_privacy_compliance_templates_cover_source_artifact_set(self):
        expected_terms = {
            "security-risk-review.md": [
                "codex security scan status",
                "data classification register",
                "compliance overlay",
                "supply-chain review",
                "sbom/provenance decision",
            ],
            "threat-surface.md": ["actors", "assets", "entry points", "trust boundaries", "abuse cases"],
            "asvs-ssdf-mapping.md": ["asvs level 1", "asvs level 2", "asvs level 3", "ssdf", "samm"],
            "authz-negative-test-matrix.md": ["bola", "bfla", "object property authorization", "unsafe consumption"],
            "secrets-policy.md": ["storage", "rotation", "access scope", "scanning", "incident path"],
            "data-classification-register.md": ["prompts", "docs", "fixtures", "eval datasets", "logs", "traces", "screenshots"],
            "privacy-impact-record.md": ["purpose", "data minimization", "retention", "deletion/export", "legal owner"],
            "api-security-review.md": ["security scheme", "scopes", "error behavior", "negative examples", "object-level authorization"],
            "abuse-rate-limit-plan.md": ["abuse cases", "rate limits", "monitoring", "kill switch", "escalation"],
            "supply-chain-review.md": ["dependencies", "licenses", "vulnerabilities", "sbom", "provenance", "release signing"],
            "sbom-manifest.md": ["spdx", "cyclonedx", "generation command", "validation command", "provenance"],
            "ci-permissions-review.md": ["workflow triggers", "token permissions", "external actions", "action pinning", "approval boundary"],
            "audit-logging-review.md": ["event taxonomy", "redaction", "retention", "alerting", "investigation owner"],
            "ai-security-review.md": ["prompt injection", "data leakage", "tool misuse", "excessive agency", "red-team cases"],
            "compliance-overlay.md": ["legal/regulatory", "customer contractual", "internal policy", "finance", "healthcare", "ai agent tooling"],
            "vulnerability-response-record.md": ["triage", "severity", "containment", "fix evidence", "disclosure path", "post-incident lessons"],
            "approval-record.md": ["production data", "external write", "payment/billing", "secret rotation", "policy change"],
        }
        required_boundary_terms = [
            "Source status:",
            "Owner",
            "Current Evidence",
            "Accepted Gap",
            "Residual Risk",
            "raw secrets",
            "payment data",
            "raw PII",
            "private customer data",
        ]

        for filename, terms in expected_terms.items():
            text = (TEMPLATE_ROOT / "artifact-templates" / filename).read_text(encoding="utf-8")
            lowered = text.lower()
            with self.subTest(filename=filename):
                for term in required_boundary_terms:
                    self.assertIn(term.lower(), lowered)
                for term in terms:
                    self.assertIn(term.lower(), lowered)

    def test_llm_ai_rag_final_batch_templates_cover_handoff_tooling_migration_lifecycle_and_incidents(self):
        targets = {item.target_path for item in required_templates()}
        self.assertNotIn(".codex/artifact-templates/agent-handoff-contract.md", targets)
        self.assertIn(".codex/artifact-templates/agent-task-packet.md", targets)
        self.assertIn(".codex/artifact-templates/agent-workflow-map.md", targets)

        templates = {
            "agent-task-packet.md": (TEMPLATE_ROOT / "artifact-templates" / "agent-task-packet.md").read_text(
                encoding="utf-8"
            ).lower(),
            "agent-workflow-map.md": (TEMPLATE_ROOT / "artifact-templates" / "agent-workflow-map.md").read_text(
                encoding="utf-8"
            ).lower(),
            "trace-evidence-packet.md": (
                TEMPLATE_ROOT / "artifact-templates" / "trace-evidence-packet.md"
            ).read_text(encoding="utf-8").lower(),
            "ai-eval-spec.md": (TEMPLATE_ROOT / "artifact-templates" / "ai-eval-spec.md").read_text(
                encoding="utf-8"
            ).lower(),
            "model-decision-record.md": (
                TEMPLATE_ROOT / "artifact-templates" / "model-decision-record.md"
            ).read_text(encoding="utf-8").lower(),
            "eval-run-report.md": (TEMPLATE_ROOT / "artifact-templates" / "eval-run-report.md").read_text(
                encoding="utf-8"
            ).lower(),
            "rag-source-inventory.md": (
                TEMPLATE_ROOT / "artifact-templates" / "rag-source-inventory.md"
            ).read_text(encoding="utf-8").lower(),
            "rag-retrieval-config.md": (
                TEMPLATE_ROOT / "artifact-templates" / "rag-retrieval-config.md"
            ).read_text(encoding="utf-8").lower(),
            "ai-dataset-manifest.md": (
                TEMPLATE_ROOT / "artifact-templates" / "ai-dataset-manifest.md"
            ).read_text(encoding="utf-8").lower(),
            "guardrail-matrix.md": (TEMPLATE_ROOT / "artifact-templates" / "guardrail-matrix.md").read_text(
                encoding="utf-8"
            ).lower(),
            "control-plane-runlog.md": (TEMPLATE_ROOT / "control-plane" / "RUNLOG.md").read_text(
                encoding="utf-8"
            ).lower(),
        }

        expected_terms = {
            "agent-task-packet.md": [
                "agent-handoff-contract.md",
                "handoff owner",
                "inputs",
                "output schema",
                "trace evidence",
            ],
            "agent-workflow-map.md": [
                "handoff owner",
                "inputs",
                "output schema",
                "trace source",
                "sequential fallback",
            ],
            "trace-evidence-packet.md": [
                "trace source type",
                "agents sdk trace",
                "opentelemetry genai span",
                "tool-specific report",
                "redaction boundary",
            ],
            "ai-eval-spec.md": [
                "promptfoo",
                "openai evals",
                "pytest/jest",
                "ragas",
                "langsmith",
                "selected runner",
                "rejected runner",
                "deferred decision",
                "stack/privacy/ci fit",
                "no forced eval runner",
            ],
            "model-decision-record.md": [
                "snapshot or approved alias",
                "prompt migration impact",
                "compatibility checks",
                "minimum threshold",
                "sampling parameter rationale",
            ],
            "eval-run-report.md": [
                "model migration",
                "minimum threshold",
                "accepted regression",
                "ai incident",
                "follow-up eval",
            ],
            "rag-source-inventory.md": [
                "deletion path",
                "retention",
                "source exclusion",
                "stale-source pruning",
                "privacy owner",
            ],
            "rag-retrieval-config.md": [
                "vector store lifecycle",
                "deletion propagation",
                "privacy owner",
            ],
            "ai-dataset-manifest.md": [
                "deduplication",
                "stale-case pruning",
                "privacy review",
            ],
            "guardrail-matrix.md": [
                "ai incident",
                "hallucination report",
                "unsafe output",
                "tool misuse",
                "data exposure",
                "security/privacy handoff",
            ],
            "control-plane-runlog.md": [
                "ai incident boundary",
                "severity",
                "mitigation",
                "follow-up eval",
                "security/privacy handoff",
            ],
        }

        for filename, terms in expected_terms.items():
            with self.subTest(filename=filename):
                text = templates[filename]
                for term in terms:
                    self.assertIn(term, text)

    def test_template_source_files_exist(self):
        for item in required_templates():
            with self.subTest(key=item.key):
                self.assertTrue(item.source_path.exists(), item.source_path)
                self.assertTrue(item.source_path.is_file(), item.source_path)
                self.assertTrue(item.source_path.resolve().is_relative_to(TEMPLATE_ROOT.resolve()))

    def test_business_product_artifact_templates_have_operating_contracts(self):
        expected_templates = [
            "product-brief.md",
            "value-proposition.md",
            "opportunity-tree.md",
            "experiment-plan.md",
            "tracking-plan.md",
        ]
        required_terms = ["Source status:", "Owner", "Evidence", "Accepted Gap", "Residual Risk"]

        for filename in expected_templates:
            path = TEMPLATE_ROOT / "artifact-templates" / filename
            with self.subTest(filename=filename):
                self.assertTrue(path.exists(), path)
                text = path.read_text(encoding="utf-8")
                for term in required_terms:
                    self.assertIn(term, text)

    def test_requirements_domain_artifact_templates_have_operating_contracts(self):
        expected_templates = [
            "requirement-registry.md",
            "stakeholder-owner-map.md",
            "story-slice-map.md",
            "requirements-traceability-matrix.md",
            "business-rules.md",
            "example-map.md",
            "requirement-change-impact.md",
            "domain-review-record.md",
        ]
        required_terms = ["Source status:", "Owner", "Evidence", "Accepted Gap", "Residual Risk"]

        for filename in expected_templates:
            path = TEMPLATE_ROOT / "artifact-templates" / filename
            with self.subTest(filename=filename):
                self.assertTrue(path.exists(), path)
                text = path.read_text(encoding="utf-8")
                for term in required_terms:
                    self.assertIn(term, text)

    def test_quality_testing_evals_artifact_templates_have_operating_contracts(self):
        expected_templates = [
            "test-eval-matrix.md",
            "quality-strategy.md",
            "ci-evidence-record.md",
            "flaky-test-policy.md",
            "manual-qa-evidence.md",
        ]
        required_terms = [
            "Source status:",
            "Owner",
            "Current Evidence",
            "Accepted Gap",
            "Residual Risk",
            "Approval Boundary",
            "Verification",
            "Rollback",
            "test data privacy",
            "No Secrets",
        ]

        for filename in expected_templates:
            path = TEMPLATE_ROOT / "artifact-templates" / filename
            with self.subTest(filename=filename):
                self.assertTrue(path.exists(), path)
                text = path.read_text(encoding="utf-8")
                for term in required_terms:
                    self.assertIn(term, text)

    def test_codex_agentic_workflow_artifact_templates_have_operating_contracts(self):
        expected_templates = [
            "model-reasoning-policy.md",
            "mcp-permission-review.md",
            "hook-governance.md",
            "skill-promotion-record.md",
            "agent-eval-workflow.md",
        ]
        required_terms = [
            "Source status:",
            "Owner",
            "Evidence",
            "Accepted Gap",
            "Residual Risk",
            "Approval Boundary",
            "Verification",
            "Rollback",
            "No Secrets",
            "present_unverified",
            "approval_required",
        ]

        for filename in expected_templates:
            path = TEMPLATE_ROOT / "artifact-templates" / filename
            with self.subTest(filename=filename):
                self.assertTrue(path.exists(), path)
                text = path.read_text(encoding="utf-8")
                for term in required_terms:
                    self.assertIn(term, text)

    def test_llm_ai_rag_artifact_templates_have_operating_contracts(self):
        expected_terms = {
            "ai-behavior-spec.md": [
                "user-visible behavior promise",
                "accepted outputs",
                "refusal",
                "fallback",
            ],
            "prompt-contract.md": [
                "prompt version",
                "role",
                "goal",
                "variables",
                "examples",
                "verification route",
            ],
            "model-decision-record.md": [
                "snapshot/alias policy",
                "reasoning effort",
                "modality",
                "context window",
                "tool support",
                "rollback",
            ],
            "eval-run-report.md": [
                "baseline/current comparison",
                "failed cases",
                "current-run evidence",
                "inspection-only gap",
            ],
            "ai-dataset-manifest.md": [
                "dataset source",
                "privacy class",
                "synthetic/sanitized status",
                "retention",
                "raw private chat logs exclusion",
            ],
            "structured-output-schema.md": [
                "typed contract",
                "strictness",
                "parser validation",
                "refusal",
                "fallback",
            ],
            "ai-tool-contract.md": [
                "tool schema",
                "permissions",
                "side effects",
                "idempotency",
                "approval policy",
            ],
            "rag-source-inventory.md": [
                "corpus authority",
                "freshness",
                "ingestion path",
                "exclusions",
                "unsupported-claim behavior",
            ],
            "rag-retrieval-config.md": [
                "chunking",
                "embeddings",
                "vector store",
                "filters",
                "top-k",
                "reranking",
            ],
            "rag-eval-report.md": [
                "context precision",
                "context recall",
                "faithfulness",
                "answer relevance",
                "failed queries",
            ],
            "grounding-rubric.md": [
                "citation/source rules",
                "unsupported claim handling",
                "conflict handling",
                "abstention policy",
            ],
            "agent-workflow-map.md": [
                "smallest useful workflow",
                "handoffs",
                "state",
                "final-answer owner",
                "stop conditions",
            ],
            "guardrail-matrix.md": [
                "prompt injection",
                "private data",
                "risky tool actions",
                "human approvals",
                "red-team cases",
            ],
            "trace-evidence-packet.md": [
                "trace ids",
                "model/tool calls",
                "retrieved context",
                "latency",
                "cost",
                "redaction",
            ],
            "ai-cost-latency-budget.md": [
                "tokens",
                "cache strategy",
                "timeout",
                "retry",
                "batch/background mode",
                "fallback",
            ],
        }
        common_terms = [
            "Source status:",
            "Owner",
            "Evidence",
            "Accepted Gap",
            "Residual Risk",
            "Approval Boundary",
            "Verification",
            "No Secrets",
            "private customer data",
        ]

        for filename, specific_terms in expected_terms.items():
            path = TEMPLATE_ROOT / "artifact-templates" / filename
            with self.subTest(filename=filename):
                self.assertTrue(path.exists(), path)
                text = path.read_text(encoding="utf-8")
                lowered = text.lower()
                for term in common_terms:
                    self.assertIn(term, text)
                for term in specific_terms:
                    self.assertIn(term, lowered)

    def test_frontend_artifact_templates_have_operating_contracts(self):
        expected_templates = [
            "frontend-flow-spec.md",
            "frontend-state-matrix.md",
            "frontend-visual-qa.md",
            "frontend-accessibility-review.md",
            "frontend-performance-budget.md",
        ]
        required_terms = [
            "Source status:",
            "Owner",
            "Evidence",
            "Accepted Gap",
            "Residual Risk",
            "Approval Boundary",
            "Verification",
            "Rollback",
            "No Secrets",
            "frontend_user_flow_acceptance_present",
            "frontend_runtime_console_evidence_present",
        ]

        for filename in expected_templates:
            path = TEMPLATE_ROOT / "artifact-templates" / filename
            with self.subTest(filename=filename):
                self.assertTrue(path.exists(), path)
                text = path.read_text(encoding="utf-8")
                for term in required_terms:
                    self.assertIn(term, text)

    def test_frontend_templates_connect_control_plane_and_evals(self):
        payloads = {
            "frontend-flow-spec.md": (
                TEMPLATE_ROOT / "artifact-templates" / "frontend-flow-spec.md"
            ).read_text(encoding="utf-8").lower(),
            "frontend-state-matrix.md": (
                TEMPLATE_ROOT / "artifact-templates" / "frontend-state-matrix.md"
            ).read_text(encoding="utf-8").lower(),
            "frontend-visual-qa.md": (
                TEMPLATE_ROOT / "artifact-templates" / "frontend-visual-qa.md"
            ).read_text(encoding="utf-8").lower(),
            "frontend-accessibility-review.md": (
                TEMPLATE_ROOT / "artifact-templates" / "frontend-accessibility-review.md"
            ).read_text(encoding="utf-8").lower(),
            "frontend-performance-budget.md": (
                TEMPLATE_ROOT / "artifact-templates" / "frontend-performance-budget.md"
            ).read_text(encoding="utf-8").lower(),
            "component-card.md": (
                TEMPLATE_ROOT / "artifact-templates" / "component-card.md"
            ).read_text(encoding="utf-8").lower(),
            "control-plane": "\n".join(
                (TEMPLATE_ROOT / "control-plane" / name).read_text(encoding="utf-8").lower()
                for name in ["PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
            ),
            "project-readiness.json": (TEMPLATE_ROOT / "evals" / "project-readiness.json").read_text(
                encoding="utf-8"
            ).lower(),
            "behavioral-workflows.json": (
                TEMPLATE_ROOT / "evals" / "behavioral-workflows.json"
            ).read_text(encoding="utf-8").lower(),
        }

        shared_terms = [
            "frontend",
            "frontend-flow-spec.md",
            "frontend-state-matrix.md",
            "frontend-visual-qa.md",
            "frontend-accessibility-review.md",
            "frontend-performance-budget.md",
            "ui-flow-spec.md",
            "component-state-matrix.md",
            "accessibility-review.md",
            "route params",
            "auth/permission",
            "seo/meta",
            "token owner",
            "variant policy",
            "local state",
            "server-cache",
            "persisted state",
            "browser/runtime evidence",
            "console status",
            "playwright trace",
            "baseline owner",
            "reduced motion",
            "input modality",
            "wcag 2.2 aa",
            "external visual service approval",
            "storybook proves ui quality",
        ]
        for name, text in payloads.items():
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_backend_artifact_templates_have_operating_contracts(self):
        expected_templates = [
            "backend-service-overview.md",
            "backend-runtime-behavior.md",
            "backend-dependency-failure-matrix.md",
            "backend-observability-map.md",
            "backend-slo-sheet.md",
            "backend-health-check-contract.md",
            "backend-job-queue-contract.md",
            "backend-data-consistency-record.md",
            "backend-config-secrets-manifest.md",
            "backend-release-rollback-notes.md",
            "backend-operational-runbook.md",
        ]
        required_terms = [
            "Source status:",
            "Owner",
            "Evidence",
            "Accepted Gap",
            "Residual Risk",
            "Approval Boundary",
            "Verification",
            "Rollback",
            "No Secrets",
            "backend_service_boundary_present",
            "backend_runtime_behavior_present",
            "backend_rollback_plan_present",
        ]

        for filename in expected_templates:
            path = TEMPLATE_ROOT / "artifact-templates" / filename
            with self.subTest(filename=filename):
                self.assertTrue(path.exists(), path)
                text = path.read_text(encoding="utf-8")
                for term in required_terms:
                    self.assertIn(term, text)

    def test_backend_templates_connect_architecture_api_and_quality_evidence(self):
        filenames = [
            "backend-service-overview.md",
            "backend-runtime-behavior.md",
            "backend-dependency-failure-matrix.md",
            "backend-observability-map.md",
            "backend-job-queue-contract.md",
            "architecture-overview.md",
            "api-contract-review.md",
            "quality-strategy.md",
            "test-eval-matrix.md",
            "manual-qa-evidence.md",
        ]
        combined = "\n".join(
            (TEMPLATE_ROOT / "artifact-templates" / filename).read_text(encoding="utf-8").lower()
            for filename in filenames
        )

        for expected in [
            "backend-service-overview.md",
            "backend-runtime-behavior.md",
            "purpose",
            "owner",
            "inbound contracts",
            "outbound dependencies",
            "data ownership",
            "deployment/runtime shape",
            "openapi",
            "asyncapi",
            "pact",
            "protobuf",
            "unit",
            "integration",
            "contract",
            "runtime",
            "operational checks",
            "code inspection alone",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, combined)

    def test_backend_security_and_secrets_overlap_is_explicit(self):
        combined = "\n".join(
            (TEMPLATE_ROOT / "artifact-templates" / filename).read_text(encoding="utf-8").lower()
            for filename in [
                "security-risk-review.md",
                "backend-config-secrets-manifest.md",
            ]
        )

        for expected in [
            "authn/authz",
            "tokens",
            "pii",
            "money movement",
            "privileged operations",
            "external writes",
            "irreversible side effects",
            "docs, prompts, fixtures and logs",
            "private customer data",
            "approval_required",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, combined)

    def test_backend_control_plane_and_eval_templates_cover_readiness_gates(self):
        combined = "\n".join(
            (TEMPLATE_ROOT / relative).read_text(encoding="utf-8").lower()
            for relative in [
                "control-plane/PLAN.md",
                "control-plane/TEST.md",
                "control-plane/EVALS.md",
                "control-plane/RUNLOG.md",
                "evals/project-readiness.json",
                "evals/behavioral-workflows.json",
            ]
        )

        for expected in [
            "backend methodology (`backend`)",
            "backend_service_boundary_present",
            "backend_runtime_behavior_present",
            "backend_dependency_failure_matrix_present",
            "backend_observability_contract_present",
            "backend_slo_or_gap_present",
            "backend_health_probe_contract_present",
            "backend_job_queue_contract_present",
            "backend_data_consistency_strategy_present",
            "backend_config_secrets_boundary_present",
            "backend_security_reviewed",
            "backend_rollback_plan_present",
            "logs-only observability",
            "health-endpoint-only readiness",
            "package docs do not prove backend runtime safety",
            "accepted gap",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, combined)

    def test_backend_modular_ports_and_runtime_policy_depth(self):
        combined = "\n".join(
            (TEMPLATE_ROOT / "artifact-templates" / filename).read_text(encoding="utf-8").lower()
            for filename in [
                "backend-service-overview.md",
                "backend-runtime-behavior.md",
                "domain-modeling.md",
            ]
        )

        for expected in [
            "modular monolith is the default",
            "independent deploy/scale/team/ownership evidence",
            "microservices require explicit owner review",
            "migration/rollback notes",
            "domain logic independent from http/db/queue/vendor sdk",
            "ports/adapters boundary",
            "bounded context",
            "ubiquitous language",
            "timeout",
            "backoff",
            "max attempts",
            "idempotency",
            "deduplication",
            "ordering",
            "backpressure",
            "poison message",
            "explicit_gap_accepted",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, combined)

    def test_backend_resilience_operations_twelve_factor_and_owner_review_depth(self):
        artifact_terms = {
            "backend-dependency-failure-matrix.md": [
                "per dependency",
                "verification evidence",
                "backoff",
                "max attempts",
                "circuit breaker/non-applicability",
            ],
            "backend-job-queue-contract.md": [
                "dead-letter queue",
                "dead-letter behavior",
                "deduplication policy",
                "ordering guarantee",
                "backpressure",
                "poison-message handling",
            ],
            "backend-data-consistency-record.md": [
                "local transaction",
                "outbox",
                "saga",
                "compensation",
                "reconciliation",
                "migration impact",
            ],
            "backend-observability-map.md": [
                "logs alone are not accepted as observability",
                "alert ownership",
                "no-private-payload logging",
                "context propagation",
                "collector/exporter",
            ],
            "backend-slo-sheet.md": [
                "sli/slo or explicit gap",
                "user-relevant sli",
                "not-yet-production gap",
                "no-telemetry gap",
            ],
            "backend-health-check-contract.md": [
                "health endpoint semantics",
                "liveness",
                "readiness",
                "startup",
                "platform equivalent",
            ],
            "backend-operational-runbook.md": [
                "operational owner",
                "escalation path",
                "handoff to delivery/operations",
                "evidence freshness",
            ],
            "backend-release-rollback-notes.md": [
                "rollback command",
                "manual procedure",
                "irreversible side effects",
                "owner approval",
                "residual risk",
            ],
            "backend-service-overview.md": [
                "twelve-factor vocabulary",
                "explicit dependencies",
                "build-release-run",
                "process model",
                "admin tasks",
                "dev/prod parity",
                "owner review",
                "decision authority",
                "boundary rationale",
                "adr link or accepted gap",
            ],
            "backend-config-secrets-manifest.md": [
                "config/env keys",
                "build-release-run",
                "dev/prod parity",
                "secret source",
            ],
            "backend-runtime-behavior.md": [
                "logs-as-event-stream",
                "process model",
                "admin tasks",
                "stateless process",
            ],
            "migration-plan.md": [
                "data consistency",
                "outbox",
                "saga",
                "compensation",
                "reconciliation",
                "data recovery",
            ],
            "../workflows/release-packet.md": [
                "backend rollback",
                "rollback command",
                "manual procedure",
                "data recovery/replay",
                "irreversible side effects",
            ],
            "adr.md": [
                "service boundary change",
                "decision authority",
                "boundary rationale",
                "adr link",
                "owner review",
            ],
        }
        for filename, expected_terms in artifact_terms.items():
            root = TEMPLATE_ROOT / "artifact-templates"
            path = (root / filename).resolve() if filename.startswith("../") else root / filename
            text = path.read_text(encoding="utf-8").lower()
            for expected in expected_terms:
                with self.subTest(filename=filename, expected=expected):
                    self.assertIn(expected, text)

        readiness = json.loads((TEMPLATE_ROOT / "evals" / "project-readiness.json").read_text(encoding="utf-8"))
        gates = readiness["cases"][0]["expected"]["conditional_readiness_gates"]
        backend_gate = gates["backend_readiness_when_backend_changes"]
        required_evidence = "\n".join(backend_gate["required_evidence"]).lower()
        for expected in [
            "backend-dependency-failure-matrix.md",
            "backend-slo-sheet.md",
            "backend-health-check-contract.md",
            "backend-job-queue-contract.md",
            "backend-data-consistency-record.md",
            "backend-config-secrets-manifest.md",
            "backend-operational-runbook.md",
            "owner-reviewed evidence sufficiency",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, required_evidence)

    def test_backend_intake_security_ops_and_contract_depth(self):
        payloads = {
            "requirements-author": (PLUGIN_ROOT / "skills" / "requirements-author" / "SKILL.md")
            .read_text(encoding="utf-8")
            .lower(),
            "REQUIREMENTS.md": (TEMPLATE_ROOT / "control-plane" / "REQUIREMENTS.md").read_text(
                encoding="utf-8"
            ).lower(),
            "TEST.md": (TEMPLATE_ROOT / "control-plane" / "TEST.md").read_text(encoding="utf-8").lower(),
            "security-risk-review.md": (TEMPLATE_ROOT / "artifact-templates" / "security-risk-review.md").read_text(
                encoding="utf-8"
            ).lower(),
            "backend-observability-map.md": (
                TEMPLATE_ROOT / "artifact-templates" / "backend-observability-map.md"
            ).read_text(encoding="utf-8").lower(),
            "backend-health-check-contract.md": (
                TEMPLATE_ROOT / "artifact-templates" / "backend-health-check-contract.md"
            ).read_text(encoding="utf-8").lower(),
            "backend-operational-runbook.md": (
                TEMPLATE_ROOT / "artifact-templates" / "backend-operational-runbook.md"
            ).read_text(encoding="utf-8").lower(),
            "backend-config-secrets-manifest.md": (
                TEMPLATE_ROOT / "artifact-templates" / "backend-config-secrets-manifest.md"
            ).read_text(encoding="utf-8").lower(),
            "backend-release-rollback-notes.md": (
                TEMPLATE_ROOT / "artifact-templates" / "backend-release-rollback-notes.md"
            ).read_text(encoding="utf-8").lower(),
            "release-packet.md": (TEMPLATE_ROOT / "workflows" / "release-packet.md").read_text(
                encoding="utf-8"
            ).lower(),
            "backend-service-overview.md": (
                TEMPLATE_ROOT / "artifact-templates" / "backend-service-overview.md"
            ).read_text(encoding="utf-8").lower(),
            "api-contract-review.md": (
                TEMPLATE_ROOT / "artifact-templates" / "api-contract-review.md"
            ).read_text(encoding="utf-8").lower(),
            "backend-job-queue-contract.md": (
                TEMPLATE_ROOT / "artifact-templates" / "backend-job-queue-contract.md"
            ).read_text(encoding="utf-8").lower(),
        }
        expected_by_payload = {
            "requirements-author": [
                "service/user behavior",
                "affected backend unit",
                "dependencies",
                "data stores",
                "runtime constraints",
                "operational assumptions",
                "explicit gaps before implementation planning",
            ],
            "REQUIREMENTS.md": [
                "backend intake",
                "service/user behavior",
                "affected backend unit",
                "backend dependencies",
                "backend data stores",
                "operational assumptions",
                "explicit gaps before implementation planning",
            ],
            "TEST.md": [
                "health checks are tested where the platform/runtime is available",
                "platform-unavailable gap",
                "documentation alone is not sufficient",
            ],
            "security-risk-review.md": [
                "authn/authz",
                "rate limits",
                "audit logging",
                "sensitive data",
                "abuse cases",
                "no-secrets evidence",
            ],
            "backend-observability-map.md": [
                "semantic conventions or accepted gaps",
                "collector/instrumentation notes",
                "context propagation",
                "redaction policy",
            ],
            "backend-health-check-contract.md": [
                "platform-unavailable gap owner",
                "platform-unavailable gap reason",
                "platform-unavailable follow-up",
                "documentation alone is not sufficient",
            ],
            "backend-operational-runbook.md": [
                "common failures",
                "dashboard links",
                "log/query links or placeholders",
                "severity assumptions",
                "evidence freshness",
            ],
            "backend-config-secrets-manifest.md": [
                "required/optional status",
                "no-secrets/no-private-data constraints",
                "docs, prompts, fixtures, logs and examples",
            ],
            "backend-release-rollback-notes.md": [
                "verification command",
                "rollback/no-rollback rationale",
                "feature flag",
            ],
            "release-packet.md": [
                "backend rollback",
                "verification command",
                "rollback/no-rollback rationale",
                "feature flag",
            ],
            "backend-service-overview.md": [
                "apis/events/external providers",
                "contract changes synced with code and tests",
                "provider contracts",
            ],
            "api-contract-review.md": [
                "contract changes synced with code and tests",
                "external provider contract",
                "provider contract",
            ],
            "backend-job-queue-contract.md": [
                "asyncapi or provider contract",
                "contract changes synced with code and tests",
            ],
        }

        for name, expected_terms in expected_by_payload.items():
            text = payloads[name]
            for expected in expected_terms:
                with self.subTest(name=name, expected=expected):
                    self.assertIn(expected, text)

    def test_backend_framework_agnostic_and_evidence_sufficiency_policy(self):
        payloads = {
            "backend-service-overview.md": (
                TEMPLATE_ROOT / "artifact-templates" / "backend-service-overview.md"
            ).read_text(encoding="utf-8").lower(),
            "backend-runtime-behavior.md": (
                TEMPLATE_ROOT / "artifact-templates" / "backend-runtime-behavior.md"
            ).read_text(encoding="utf-8").lower(),
            "EVALS.md": (TEMPLATE_ROOT / "control-plane" / "EVALS.md").read_text(encoding="utf-8").lower(),
            "RUNLOG.md": (TEMPLATE_ROOT / "control-plane" / "RUNLOG.md").read_text(encoding="utf-8").lower(),
        }
        expected_by_payload = {
            "backend-service-overview.md": [
                "framework-agnostic",
                "stack-specific snippets deferred",
                "node.js, python, java, .net and go snippets",
                "owner, examples and verification",
            ],
            "backend-runtime-behavior.md": [
                "framework-agnostic",
                "stack-specific snippets deferred",
                "node.js, python, java, .net and go snippets",
                "deeper static analysis deferred",
                "avoid false positives",
            ],
            "EVALS.md": [
                "owner reviewed test/eval/runtime evidence sufficiency",
                "real project risk",
                "accepted gap owner",
                "accepted gap reason",
                "review date",
                "downstream risk",
                "follow-up",
                "t9-s",
            ],
            "RUNLOG.md": [
                "owner reviewed test/eval/runtime evidence sufficiency",
                "real project risk",
                "accepted gap owner",
                "accepted gap reason",
                "review date",
                "downstream risk",
                "follow-up",
                "t9-s",
            ],
        }

        for name, expected_terms in expected_by_payload.items():
            text = payloads[name]
            for expected in expected_terms:
                with self.subTest(name=name, expected=expected):
                    self.assertIn(expected, text)

        readiness = json.loads((TEMPLATE_ROOT / "evals" / "project-readiness.json").read_text(encoding="utf-8"))
        backend_gate = readiness["cases"][0]["expected"]["conditional_readiness_gates"][
            "backend_readiness_when_backend_changes"
        ]
        readiness_payload = json.dumps(backend_gate).lower()
        for expected in [
            "blocker/high-risk",
            "simple local/backend-light",
            "accepted gap downgrade",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, readiness_payload)

    def test_template_text_has_no_unsafe_literals(self):
        for item in required_templates():
            text = item.source_path.read_text(encoding="utf-8")
            with self.subTest(key=item.key):
                for forbidden in FORBIDDEN_TEXT:
                    self.assertNotIn(forbidden, text)
                self.assertNotRegex(text, re.compile(r"(?i)secret-value|private-customer|raw chat log"))

    def test_rendered_templates_have_no_unresolved_substitutions(self):
        context = {
            "project_name": "Synthetic Project",
            "workspace_path": "C:/workspace/synthetic-project",
            "profile_name": "standard-product",
            "detected_stack": ["python", "docs"],
            "detected_stack_text": "python, docs",
            "existing_control_plane": ["AGENTS.md"],
            "missing_control_plane": ["PLAN.md"],
            "existing_codex_assets": [".codex/config.toml"],
            "risk_text": "no detected test files or test configuration",
            "generated_at": "2026-05-14",
        }

        for item in required_templates():
            rendered = render_template(item, context)
            with self.subTest(key=item.key):
                self.assertNotRegex(rendered, re.compile(r"\{[a-zA-Z0-9_]+\}"))
                self.assertNotIn("None", rendered)

    def test_agent_templates_validate_after_render(self):
        context = self._context()
        for item in required_templates():
            if item.validation_kind != "agent":
                continue
            with self.subTest(key=item.key):
                path = self._render_temp_file(item, context)
                self.assertEqual(validate_agent_file(path), [])

    def test_hook_templates_validate_after_render(self):
        context = self._context()
        for item in required_templates():
            if item.validation_kind != "hook":
                continue
            with self.subTest(key=item.key):
                path = self._render_temp_file(item, context)
                self.assertEqual(validate_hook_file(path), [])

    def test_hook_lifecycle_config_is_template_only_and_complete(self):
        self.assertFalse((PLUGIN_ROOT / "hooks" / "hooks.json").exists())
        hooks_template = TEMPLATE_ROOT / "hooks" / "hooks.json"
        data = json.loads(hooks_template.read_text(encoding="utf-8"))

        for event in ["SessionStart", "PreToolUse", "PermissionRequest", "PostToolUse", "Stop"]:
            self.assertIn(event, data)

    def test_eval_templates_are_valid_json(self):
        for item in required_templates():
            if item.validation_kind != "eval_json":
                continue
            with self.subTest(key=item.key):
                data = json.loads(item.source_path.read_text(encoding="utf-8"))
                self.assertIn("name", data)
                self.assertIn("cases", data)
                self.assertIsInstance(data["cases"], list)

    def test_config_template_is_valid_toml(self):
        config = TEMPLATE_ROOT / "config" / "config.toml"
        data = tomllib.loads(config.read_text(encoding="utf-8"))

        self.assertIn("agents", data)
        self.assertIn("sandbox", data)
        self.assertIn("approvals", data)
        self.assertIn("product_agent_os", data)
        self.assertEqual(data["product_agent_os"]["runlog_archive_dir"], ".codex/runlogs/archive")
        self.assertNotIn("network_access", data)
        self.assertNotIn("secrets", data)

    def test_config_template_render_escapes_string_placeholders_for_toml(self):
        item = next(template for template in required_templates() if template.key == "config")
        context = self._context()
        context["profile_name"] = 'standard "quoted" \\ profile'

        rendered = render_template(item, context)
        data = tomllib.loads(rendered)

        self.assertEqual(data["profile"], context["profile_name"])

    def test_render_template_sorts_set_values_deterministically(self):
        item = next(template for template in required_templates() if template.key == "agents-md")
        context = self._context()
        context["existing_control_plane"] = {"zeta", "alpha", "Beta"}

        rendered_once = render_template(item, context)
        rendered_twice = render_template(item, context)

        self.assertEqual(rendered_once, rendered_twice)
        self.assertIn("Existing control-plane files: Beta, alpha, zeta", rendered_once)

    def test_automation_template_is_candidate_only(self):
        text = (TEMPLATE_ROOT / "automations" / "automation-candidate.md").read_text(encoding="utf-8")

        self.assertIn("candidate_only", text)
        self.assertIn("manual stability evidence", text)
        self.assertIn("at least two successful manual workflow runs", text)
        self.assertIn("explicit_gap_accepted", text)
        self.assertIn("explicit approval", text)
        self.assertNotIn("RRULE", text)
        self.assertNotIn("schedule:", text)

    def test_workflow_inventory_covers_context_and_ownership(self):
        names = {item.source_path.name for item in required_templates() if item.category == "workflows"}

        self.assertEqual(
            names,
            {
                "source-context-pack.md",
                "worktree-ownership.md",
                "build-slice.md",
                "review-slice.md",
                "release-packet.md",
                "runlog-compaction.md",
                "development-standards.md",
                "documentation-system.md",
                "first-run-intake.md",
                "bug-rescue.md",
                "greenfield-idea-to-plan.md",
                "complex-system-acceleration.md",
                "pr-review-readiness.md",
                "legacy-onboarding.md",
                "api-migration.md",
                "ai-eval-regression.md",
                "native-mobile-feature.md",
                "desktop-local-first.md",
                "data-migration.md",
                "security-sensitive-change.md",
                "ci-stabilization.md",
                "release-packaging.md",
            },
        )

    def test_methodology_workflows_cover_development_and_documentation_standards(self):
        development = (TEMPLATE_ROOT / "workflows" / "development-standards.md").read_text(encoding="utf-8")
        documentation = (TEMPLATE_ROOT / "workflows" / "documentation-system.md").read_text(encoding="utf-8")

        for expected in [
            "product hypothesis",
            "architecture boundary",
            "red-green-refactor",
            "test-first",
            "agentic implementation",
            "post-release measurement",
        ]:
            self.assertIn(expected, development.lower())

        for expected in [
            "architecture docs",
            "api contracts",
            "ui component docs",
            "database docs",
            "docs-as-code",
        ]:
            self.assertIn(expected, documentation.lower())

    def test_artifact_templates_cover_engineering_standards_gaps(self):
        templates = {
            path.name: path.read_text(encoding="utf-8").lower()
            for path in (TEMPLATE_ROOT / "artifact-templates").glob("*.md")
        }

        expected_templates = {
            "adr.md": [
                "source status:",
                "context",
                "decision",
                "consequences",
                "adr trigger policy",
                "tradeoff",
                "verification",
                "rollback",
                "no-rollback rationale",
                "accepted gap",
                "residual risk",
                "no secrets",
            ],
            "domain-modeling.md": [
                "bounded context",
                "bounded_context_architecture_boundary_trace",
                "context-to-boundary traceability",
                "architecture-overview.md",
                "architecture boundary",
                "boundary id",
                "ubiquitous language",
                "ubiquitous_language_traceability",
                "term-to-requirement",
                "api/event/contract",
                "ui label",
                "code module or owner",
                "domain expert review",
                "aggregate",
                "invariant",
                "domain_model_when_complex_domain",
                "complex backend",
                "workflow",
                "data-heavy",
                "accepted gap",
                "simple crud",
            ],
            "architecture-overview.md": [
                "source status:",
                "solution_architecture_scope_present",
                "c4",
                "c4 system context",
                "c4 container",
                "quality attributes",
                "risks",
                "mapped bounded context",
                "domain model",
                "context-to-boundary traceability",
                "boundary responsibility",
                "public contract",
                "data ownership",
                "trust boundary",
                "runtime topology",
                "observability",
                "render check",
                "architecture owner review",
                "accepted gap",
                "residual risk",
                "no secrets",
            ],
            "architecture-review-record.md": [
                "source status:",
                "architecture_owner_review_present",
                "boundary_responsibility_owner_present",
                "accepted_gap_recorded",
                "owner",
                "review outcome",
                "accepted gap",
                "residual risk",
                "approval boundary",
                "no secrets",
            ],
            "architecture-fitness-functions.md": [
                "source status:",
                "architecture_fitness_function_present",
                "dependency_rules_present",
                "observability_architecture_present",
                "fitness function",
                "dependency rule",
                "contract drift",
                "docs freshness",
                "verification command",
                "residual risk",
                "no secrets",
            ],
            "trust-boundary-map.md": [
                "source status:",
                "trust_boundary_security_review_present",
                "trust boundary",
                "data flow",
                "auth",
                "pii",
                "security risk review",
                "approval boundary",
                "residual risk",
                "no secrets",
            ],
            "architecture-docs-tooling-decision.md": [
                "source status:",
                "architecture_docs_as_code_present",
                "diagram_render_check_present",
                "architecture-as-code",
                "mermaid",
                "structurizr",
                "plantuml",
                "render check",
                "stale-doc detection",
                "accepted gap",
                "no secrets",
            ],
            "metric-spec.md": [
                "baseline",
                "guardrail",
                "goodhart",
                "privacy",
                "metric_hardening_when_product_behavior_changes",
                "north star",
                "input metric",
                "counter-metric",
                "proxy metric",
                "qualitative review",
                "privacy classification",
                "retention period",
                "data minimization",
                "owner signoff",
                "post-release review evidence",
            ],
            "product-brief.md": [
                "product_hypothesis_present",
                "target user segment",
                "decision horizon",
                "business outcome",
                "product outcome",
                "feature traction metric",
                "evidence",
                "accepted gap",
                "residual risk",
            ],
            "value-proposition.md": [
                "value_proposition_evidence_present",
                "target user segment",
                "job",
                "alternative",
                "evidence",
                "accepted gap",
                "residual risk",
            ],
            "opportunity-tree.md": [
                "opportunity_not_solution_present",
                "opportunity",
                "solution",
                "assumption",
                "evidence",
                "accepted gap",
                "residual risk",
            ],
            "experiment-plan.md": [
                "product_hypothesis_present",
                "decision horizon",
                "hypothesis",
                "primary metric",
                "guardrail",
                "evidence",
                "accepted gap",
                "residual risk",
            ],
            "tracking-plan.md": [
                "analytics_tracking_plan_present",
                "event",
                "properties",
                "privacy classification",
                "owner",
                "validation",
                "dashboard",
                "evidence",
                "accepted gap",
                "residual risk",
            ],
            "api-contract-review.md": ["openapi", "asyncapi", "auth", "errors"],
            "api-inventory.md": [
                "source status:",
                "provider",
                "consumers",
                "generated clients",
                "runtime environments",
                "contract drift",
                "accepted gap",
            ],
            "api-error-catalog.md": [
                "source status:",
                "rfc 9457",
                "success example",
                "validation failure",
                "auth failure",
                "domain failure",
            ],
            "api-auth-authorization-matrix.md": [
                "source status:",
                "openapi security schemes",
                "graphql auth",
                "scopes",
                "object-level authorization",
                "rate limits",
                "prose-only security notes",
            ],
            "api-consumer-map.md": [
                "source status:",
                "consumer",
                "owner",
                "generated client",
                "approval path",
                "multi-repository generated clients deferred",
            ],
            "api-compatibility-record.md": [
                "source status:",
                "breaking/non-breaking classification",
                "additive",
                "potentially breaking",
                "deprecation window",
                "rollback",
            ],
            "api-contract-test-matrix.md": [
                "source status:",
                "schema validation",
                "provider verification",
                "consumer-driven",
                "missing-tool gap",
                "framework-native",
            ],
            "generated-sdk-manifest.md": [
                "source status:",
                "generator config",
                "target languages",
                "regeneration command",
                "reviewable diff",
                "semver impact",
            ],
            "webhook-event-contract.md": [
                "source status:",
                "signature verification",
                "correlation id",
                "idempotency key",
                "retry policy",
                "dead-letter",
                "cloudevents",
            ],
            "external-integration-approval.md": [
                "source status:",
                "read capability",
                "write capability",
                "staged draft",
                "approval_required",
                "no secrets",
            ],
            "api-style-guide.md": [
                "source status:",
                "no universal default",
                "spectral/redocly/framework-native deferred",
                "api-only contract fixtures do not force backend blockers",
                "deferred with owner/reason",
            ],
            "component-card.md": [
                "states",
                "accessibility",
                "storybook",
                "fsd_structure",
                "feature-sliced design",
                "layer",
                "slice",
                "segment",
                "public api",
                "import rule",
                "not applicable",
                "backend",
                "native",
                "simple crud",
                "simple mvp",
            ],
            "database-dictionary.md": ["table", "pii", "retention", "migration"],
            "agent-task-packet.md": [
                "owned files",
                "forbidden files",
                "expected evidence",
                "stop conditions",
                "scenario handoff",
                "sources/context used",
                "assumptions",
                "files touched",
                "files proposed",
                "verification evidence",
                "open risks",
                "recommended next role",
                "stop reason",
            ],
            "behavioral-eval-case.md": ["prompt", "expected usage mode", "forbidden actions", "residual risk"],
            "plan-quality-check.md": ["exact files", "expected output", "rollback", "placeholder scan"],
            "codex-compatibility-report.md": ["codex app", "cli", "ide extension", "non-codex"],
            "bug-rescue-report.md": [
                "symptom",
                "expected behavior",
                "actual behavior",
                "reproduction",
                "root cause evidence",
                "regression test",
                "rollback",
                "unresolved risks",
            ],
            "greenfield-idea-brief.md": [
                "problem",
                "users",
                "options",
                "selected direction",
                "non-goals",
                "first vertical slice",
                "acceptance scenarios",
                "metrics",
                "approval gate",
                "docs/tooling decision",
            ],
            "acceptance-scenarios.md": [
                "atdd",
                "bdd",
                "requirement",
                "scenario",
                "check",
                "evidence owner",
                "given",
                "when",
                "then",
                "equivalent behavior format",
                "business rule",
                "edge case",
                "non-goal",
                "does not replace requirements",
                "unit tests",
                "integration tests",
                "contract tests",
                "evals",
                "declarative_acceptance_scenarios_present",
                "no ui selectors",
                "database internals",
                "function names",
                "test harness",
            ],
            "requirement-registry.md": [
                "requirement_ids_present",
                "requirement_quality_present",
                "requirement id",
                "type",
                "status",
                "source",
                "owner",
                "linked scenarios",
                "linked tests/evals",
                "change impact",
                "accepted gap",
                "residual risk",
            ],
            "stakeholder-owner-map.md": [
                "requirements_owner_present",
                "stakeholder",
                "domain expert",
                "technical owner",
                "decision authority",
                "escalation path",
                "unavailable owner gap",
                "review cadence",
                "accepted gap",
                "residual risk",
            ],
            "story-slice-map.md": [
                "story_slice_map_present",
                "user story",
                "value slice",
                "risk slice",
                "mvp boundary",
                "deferred slices",
                "non-goals",
                "acceptance scenario links",
                "accepted gap",
                "residual risk",
            ],
            "requirements-traceability-matrix.md": [
                "requirements_traceability_present",
                "api_ui_data_traceability_present",
                "requirement -> scenario -> implementation -> check/eval -> evidence owner",
                "api/event/schema",
                "ui label",
                "data field",
                "release/docs evidence",
                "accepted gap",
                "residual risk",
            ],
            "business-rules.md": [
                "business_rules_present",
                "rule",
                "source",
                "owner",
                "enforcement layer",
                "exceptions",
                "failure mode",
                "affected requirement ids",
                "tests/evals",
                "accepted gap",
                "residual risk",
            ],
            "example-map.md": [
                "example_mapping_when_unclear_story",
                "story",
                "rules",
                "examples",
                "questions",
                "deferred slices",
                "owner",
                "next action",
                "accepted gap",
                "residual risk",
            ],
            "requirement-change-impact.md": [
                "requirement_change_impact_review_present",
                "changed requirement",
                "affected tests/evals",
                "api",
                "db",
                "ui",
                "docs",
                "rollout",
                "rollback",
                "approval boundary",
                "accepted gap",
                "residual risk",
            ],
            "domain-review-record.md": [
                "domain_expert_review_present",
                "accepted_gap_recorded",
                "domain expert",
                "ai-generated claim",
                "unresolved conflicts",
                "downstream risk",
                "follow-up owner",
                "unsupported claims",
                "accepted gap",
                "residual risk",
            ],
            "docs-tooling-decision.md": [
                "docs_as_code_impact",
                "not_applicable",
                "present_unverified",
                "present_verified",
                "proposal_staged",
                "explicit_gap_accepted",
                "approval_required",
                "selected tools",
                "rejected tools",
                "mkdocs",
                "docusaurus",
                "sphinx",
                "antora",
                "storybook",
                "openapi",
                "asyncapi",
                "dbml",
                "typedoc",
                "jsdoc",
                "javadoc",
                "xml docs",
                "vale",
                "markdownlint",
                "no forced install",
                "no ci activation without approval",
                "hosted docs approval",
                "db introspection approval",
                "evidence owner",
                "maintenance owner",
            ],
            "governance-proposal.md": [
                "standards_trigger_policy",
                "governance proposal",
                "codeowners status",
                "present_verified",
                "proposal_staged",
                "approval_required",
                "not_applicable",
                "github actions",
                "least privilege",
                "workflow names",
                "commands",
                "permissions",
                "triggers",
                "owners",
                "no external activation without approval",
                "no forced external activation",
            ],
            "integration-catalog.md": [
                "external system",
                "system owner",
                "auth",
                "data exchanged",
                "rate limits",
                "retry",
                "idempotency",
                "webhook",
                "event contract",
                "observability",
                "rollback",
                "approval needs",
            ],
            "pr-risk-review.md": [
                "changed files",
                "spec compliance verdict",
                "quality/risk verdict",
                "behavior impact",
                "api impact",
                "database impact",
                "ui impact",
                "security impact",
                "docs impact",
                "release impact",
                "missing checks",
                "reviewer questions",
                "commands run",
                "residual risk",
                "external writes",
                "pr creation",
                "publish actions",
            ],
            "onboarding-map.md": [
                "source map",
                "entry points",
                "run commands",
                "architecture map",
                "docs debt",
                "verification status",
                "present_unverified",
                "first safe documentation slice",
                "without refactor",
                "assumptions",
                "open risks",
            ],
            "migration-plan.md": [
                "current state",
                "target state",
                "compatibility",
                "consumers",
                "generated clients",
                "deprecation",
                "rollout",
                "validation",
                "rollback",
                "release impact",
                "owner review",
            ],
            "ai-eval-spec.md": [
                "eval goal",
                "app path",
                "dataset",
                "no-secrets",
                "baseline",
                "rubric",
                "assertions",
                "judge policy",
                "threshold",
                "rerun command",
                "regression handling",
                "latency",
                "cost",
                "grounding",
                "failure examples",
                "residual risk",
            ],
            "ai-behavior-spec.md": [
                "source status:",
                "user-visible behavior promise",
                "accepted outputs",
                "refusal behavior",
                "fallback behavior",
                "approval boundary",
                "no secrets",
                "residual risk",
            ],
            "prompt-contract.md": [
                "source status:",
                "prompt version",
                "variables",
                "examples",
                "uncertainty policy",
                "refusal policy",
                "verification route",
                "no secrets",
                "residual risk",
            ],
            "model-decision-record.md": [
                "source status:",
                "snapshot/alias policy",
                "reasoning effort",
                "modality",
                "context window",
                "tool support",
                "migration note",
                "no secrets",
                "residual risk",
            ],
            "eval-run-report.md": [
                "source status:",
                "baseline/current comparison",
                "current-run evidence",
                "failed cases",
                "inspection-only gap",
                "approval boundary",
                "no secrets",
                "residual risk",
            ],
            "ai-dataset-manifest.md": [
                "source status:",
                "dataset source",
                "privacy class",
                "synthetic/sanitized status",
                "retention",
                "raw private chat logs exclusion",
                "no secrets",
                "residual risk",
            ],
            "structured-output-schema.md": [
                "source status:",
                "typed contract",
                "strictness",
                "parser validation",
                "refusal behavior",
                "fallback behavior",
                "failure cases",
                "no secrets",
                "residual risk",
            ],
            "ai-tool-contract.md": [
                "source status:",
                "tool schema",
                "permissions",
                "side effects",
                "idempotency",
                "approval policy",
                "approval boundary",
                "no secrets",
                "residual risk",
            ],
            "rag-source-inventory.md": [
                "source status:",
                "corpus authority",
                "freshness",
                "ingestion path",
                "exclusions",
                "source policy",
                "unsupported-claim behavior",
                "no secrets",
                "residual risk",
            ],
            "rag-retrieval-config.md": [
                "source status:",
                "chunking",
                "embeddings",
                "vector store",
                "filters",
                "top-k",
                "reranking",
                "no secrets",
                "residual risk",
            ],
            "rag-eval-report.md": [
                "source status:",
                "context precision",
                "context recall",
                "faithfulness",
                "answer relevance",
                "failed queries",
                "source gaps",
                "no secrets",
                "residual risk",
            ],
            "grounding-rubric.md": [
                "source status:",
                "citation/source rules",
                "unsupported claim handling",
                "conflict handling",
                "abstention policy",
                "no secrets",
                "residual risk",
            ],
            "agent-workflow-map.md": [
                "source status:",
                "smallest useful workflow",
                "handoffs",
                "state",
                "final-answer owner",
                "stop conditions",
                "no secrets",
                "residual risk",
            ],
            "guardrail-matrix.md": [
                "source status:",
                "prompt injection",
                "private data",
                "risky tool actions",
                "human approvals",
                "red-team cases",
                "no secrets",
                "residual risk",
            ],
            "trace-evidence-packet.md": [
                "source status:",
                "trace ids",
                "model/tool calls",
                "retrieved context",
                "latency",
                "cost",
                "redaction",
                "no secrets",
                "residual risk",
            ],
            "ai-cost-latency-budget.md": [
                "source status:",
                "tokens",
                "cache strategy",
                "timeout",
                "retry",
                "batch/background mode",
                "fallback",
                "no secrets",
                "residual risk",
            ],
            "security-risk-review.md": [
                "threat surface",
                "authn",
                "authz",
                "permissions",
                "payment",
                "billing",
                "secrets",
                "pii",
                "sensitive data",
                "abuse controls",
                "rate limit",
                "audit logging",
                "tests",
                "approval",
                "rollback",
                "residual risk",
            ],
            "threat-surface.md": [
                "source status:",
                "actors",
                "assets",
                "entry points",
                "trust boundaries",
                "abuse cases",
                "no secrets",
                "residual risk",
            ],
            "asvs-ssdf-mapping.md": [
                "source status:",
                "asvs level 1",
                "asvs level 2",
                "asvs level 3",
                "ssdf",
                "samm",
                "compliance",
                "residual risk",
            ],
            "authz-negative-test-matrix.md": [
                "source status:",
                "bola",
                "bfla",
                "object property authorization",
                "unsafe consumption",
                "abuse case",
                "residual risk",
            ],
            "secrets-policy.md": [
                "source status:",
                "storage",
                "rotation",
                "access scope",
                "scanning",
                "incident path",
                "no secrets",
                "residual risk",
            ],
            "data-classification-register.md": [
                "source status:",
                "prompts",
                "docs",
                "fixtures",
                "eval datasets",
                "logs",
                "traces",
                "screenshots",
                "redaction lifecycle",
                "residual risk",
            ],
            "privacy-impact-record.md": [
                "source status:",
                "purpose",
                "data minimization",
                "retention",
                "deletion/export",
                "legal owner",
                "not legal advice",
                "residual risk",
            ],
            "api-security-review.md": [
                "source status:",
                "security scheme",
                "scopes",
                "error behavior",
                "negative examples",
                "object-level authorization",
                "unsafe consumption",
                "residual risk",
            ],
            "abuse-rate-limit-plan.md": [
                "source status:",
                "abuse cases",
                "rate limits",
                "monitoring",
                "kill switch",
                "escalation",
                "residual risk",
            ],
            "supply-chain-review.md": [
                "source status:",
                "dependencies",
                "licenses",
                "vulnerabilities",
                "sbom",
                "provenance",
                "release signing",
                "residual risk",
            ],
            "sbom-manifest.md": [
                "source status:",
                "spdx",
                "cyclonedx",
                "generation command",
                "validation command",
                "provenance",
                "residual risk",
            ],
            "ci-permissions-review.md": [
                "source status:",
                "workflow triggers",
                "token permissions",
                "external actions",
                "action pinning",
                "approval boundary",
                "least privilege",
                "residual risk",
            ],
            "audit-logging-review.md": [
                "source status:",
                "event taxonomy",
                "redaction",
                "retention",
                "alerting",
                "investigation owner",
                "residual risk",
            ],
            "ai-security-review.md": [
                "source status:",
                "prompt injection",
                "data leakage",
                "tool misuse",
                "excessive agency",
                "red-team cases",
                "approval boundary",
                "residual risk",
            ],
            "compliance-overlay.md": [
                "source status:",
                "legal/regulatory",
                "customer contractual",
                "internal policy",
                "finance",
                "healthcare",
                "ai agent tooling",
                "not legal advice",
                "residual risk",
            ],
            "vulnerability-response-record.md": [
                "source status:",
                "triage",
                "severity",
                "containment",
                "fix evidence",
                "disclosure path",
                "post-incident lessons",
                "residual risk",
            ],
            "approval-record.md": [
                "source status:",
                "production data",
                "external write",
                "payment/billing",
                "secret rotation",
                "policy change",
                "approval_required",
                "residual risk",
            ],
            "ci-stabilization-report.md": [
                "failing job",
                "command",
                "logs",
                "environment",
                "deterministic",
                "flaky",
                "classification",
                "isolation plan",
                "local reproduction",
                "rerun evidence",
                "remote ci",
                "github actions",
                "approval",
                "residual risk",
            ],
            "test-eval-matrix.md": [
                "quality_testing_evals",
                "quality_strategy_present",
                "risk_based_scope_present",
                "acceptance_traceability_present",
                "contract_check_present",
                "current_evidence_before_completion",
                "explicit_gap_accepted",
                "approval_required",
                "test data privacy",
                "coverage is a signal, not proof",
                "no secrets",
                "residual risk",
            ],
            "quality-strategy.md": [
                "quality_testing_evals",
                "quality_strategy_present",
                "risk_based_scope_present",
                "test_first_or_gap_present",
                "coverage_policy_present",
                "test_data_privacy_present",
                "unsupported claims",
                "explicit_gap_accepted",
                "approval_required",
                "test data privacy",
                "coverage is a signal, not proof",
                "no secrets",
                "residual risk",
            ],
            "ci-evidence-record.md": [
                "quality_testing_evals",
                "ci_quality_gate_present",
                "current_evidence_before_completion",
                "least privilege",
                "present_unverified",
                "approval_required",
                "test data privacy",
                "coverage is a signal, not proof",
                "no secrets",
                "residual risk",
            ],
            "flaky-test-policy.md": [
                "quality_testing_evals",
                "flaky_test_policy_present",
                "present_unverified",
                "explicit_gap_accepted",
                "approval_required",
                "owner",
                "expiry",
                "test data privacy",
                "coverage is a signal, not proof",
                "no secrets",
                "residual risk",
            ],
            "manual-qa-evidence.md": [
                "quality_testing_evals",
                "runtime_evidence_present",
                "manual_qa_evidence_present",
                "visual_a11y_evidence_present",
                "present_unverified",
                "approval_required",
                "test data privacy",
                "coverage is a signal, not proof",
                "no secrets",
                "residual risk",
            ],
            "release-readiness.md": [
                "release scope",
                "package metadata",
                "version",
                "semver",
                "changelog",
                "build evidence",
                "test evidence",
                "docs evidence",
                "security notes",
                "license",
                "artifacts",
                "publish approval",
                "tag",
                "package registry",
                "rollback",
                "residual risk",
            ],
            "release-artifact-manifest.md": [
                "source status:",
                "artifact names",
                "versions",
                "creation command",
                "storage location",
                "retention",
                "integrity notes",
                "checksums",
                "signatures",
                "sbom",
                "provenance",
                "docs-only/no build artifact",
                "no secrets",
                "residual risk",
            ],
            "rollout-plan.md": [
                "source status:",
                "immediate release",
                "release train",
                "staged rollout",
                "feature flag",
                "canary",
                "blue-green",
                "shadow traffic",
                "manual promotion",
                "cohorts/traffic",
                "promotion",
                "abort criteria",
                "blast radius",
                "kill switch",
                "residual risk",
            ],
            "rollback-recovery-plan.md": [
                "source status:",
                "revert",
                "redeploy previous artifact",
                "disable flag",
                "unpublish",
                "yank",
                "restore backup",
                "compensate data",
                "incident mitigation",
                "command/manual procedure",
                "residual risk",
            ],
            "environment-matrix.md": [
                "source status:",
                "dev",
                "stage",
                "prod",
                "local",
                "mobile",
                "store",
                "registry",
                "branch/tag rules",
                "secret boundaries",
                "desired-state source",
                "reconciliation controller",
                "drift behavior",
                "present_unverified",
                "residual risk",
            ],
            "deployment-plan.md": [
                "source status:",
                "target environment",
                "release candidate",
                "deploy command",
                "approval",
                "rollout window",
                "stop criteria",
                "desired-state source",
                "reconciliation controller",
                "rollback/revert",
                "residual risk",
            ],
            "ci-cd-workflow-inventory.md": [
                "source status:",
                "workflow names",
                "triggers",
                "permissions",
                "secrets",
                "environments",
                "required reviewers",
                "branch/tag restrictions",
                "artifacts",
                "cache",
                "concurrency",
                "external action pinning",
                "residual risk",
            ],
            "observability-map.md": [
                "source status:",
                "logs",
                "metrics",
                "traces",
                "dashboards",
                "alert owner",
                "redaction",
                "sampling",
                "user journey",
                "residual risk",
            ],
            "slo-spec.md": [
                "source status:",
                "user journey",
                "sli",
                "slo",
                "measurement source",
                "alert policy",
                "accepted no-telemetry",
                "not-yet-production gap",
                "residual risk",
            ],
            "operations-runbook.md": [
                "source status:",
                "deploy",
                "rollback",
                "first response",
                "escalation",
                "diagnostics",
                "incident criteria",
                "residual risk",
            ],
            "incident-record.md": [
                "source status:",
                "incident criteria",
                "timeline",
                "impact",
                "mitigation",
                "communication path",
                "postmortem trigger",
                "residual risk",
            ],
            "postmortem.md": [
                "source status:",
                "impact",
                "detection",
                "root causes",
                "contributing factors",
                "action items",
                "review status",
                "quick rollback does not skip learning",
                "residual risk",
            ],
            "post-release-review.md": [
                "source status:",
                "metrics",
                "support signals",
                "defects",
                "latency/cost",
                "review date",
                "dora measurement source",
                "anti-goodhart",
                "product/reliability hypotheses",
                "residual risk",
            ],
            "database-inventory.md": [
                "datastore",
                "environment",
                "owner",
                "production access",
                "approval_required",
            ],
            "database-migration-plan.md": [
                "expand-contract",
                "transaction boundary",
                "destructive change",
                "liquibase",
                "flyway",
                "alembic",
                "prisma",
                "no universal default",
                "schema-diff tooling deferred",
            ],
            "database-expand-contract-record.md": [
                "expand phase",
                "contract phase",
                "backward compatibility",
                "consumer compatibility",
            ],
            "database-backfill-runbook.md": [
                "batch size",
                "idempotency",
                "resume",
                "dry run",
                "row counts",
            ],
            "database-rollback-feasibility.md": [
                "rollback feasibility",
                "restore",
                "irreversible",
                "accepted gap",
                "owner approval",
            ],
            "database-backup-restore-evidence.md": [
                "backup",
                "restore test",
                "restore point",
                "no production data in prompts",
            ],
            "database-data-classification-matrix.md": [
                "pii",
                "sensitive",
                "retention",
                "deletion",
                "access boundary",
            ],
            "database-data-quality-checks.md": [
                "great expectations",
                "dbt tests",
                "constraints",
                "row counts",
                "drift",
            ],
            "database-data-contract.md": [
                "producer",
                "consumer",
                "constraints",
                "indexes",
                "schema source",
                "compatibility",
            ],
            "database-lineage-map.md": [
                "lineage",
                "openlineage",
                "dbt",
                "upstream",
                "downstream",
            ],
            "database-query-performance-review.md": [
                "query plan",
                "index",
                "explain",
                "production load risk",
            ],
            "database-retention-deletion-policy.md": [
                "retention",
                "deletion",
                "legal hold",
                "audit evidence",
            ],
            "database-synthetic-fixtures-policy.md": [
                "synthetic",
                "no secrets",
                "no production data",
                "fixtures",
            ],
            "database-production-access-approval.md": [
                "production access",
                "approval_required",
                "read-only",
                "introspection",
                "least privilege",
            ],
            "model-reasoning-policy.md": [
                "codex_agentic_workflow",
                "model_reasoning_policy_present",
                "codex app",
                "cli",
                "ide extension",
                "codex exec",
                "github action",
                "mcp",
                "agents sdk",
                "automation",
                "memory as recall only",
                "no silent activation",
                "residual risk",
            ],
            "mcp-permission-review.md": [
                "codex_agentic_workflow",
                "mcp_permission_review_present",
                "tools/resources/prompts",
                "auth/secrets",
                "side effects",
                "approval_required",
                "no silent activation",
                "residual risk",
            ],
            "hook-governance.md": [
                "codex_agentic_workflow",
                "hook_activation_approval_present",
                "read-only validation hook",
                "blocking or side-effecting hook",
                "two-stage review",
                "approval_required",
                "no silent activation",
                "residual risk",
            ],
            "skill-promotion-record.md": [
                "codex_agentic_workflow",
                "skill_promotion_evidence_present",
                "trigger tests",
                "negative trigger tests",
                "missing-input behavior",
                "failure log",
                "automation_manual_stability_present",
                "no silent activation",
                "residual risk",
            ],
            "agent-eval-workflow.md": [
                "codex_agentic_workflow",
                "agent_eval_workflow_present",
                "trace-derived dataset",
                "tool-call correctness",
                "handoff correctness",
                "threshold",
                "privacy/no-secrets handling",
                "approval_required",
                "residual risk",
            ],
            "frontend-flow-spec.md": [
                "frontend_user_flow_acceptance_present",
                "ui-flow-spec.md",
                "route params",
                "auth/permission",
                "seo/meta",
                "frontend_runtime_console_evidence_present",
                "no secrets",
                "residual risk",
            ],
            "frontend-state-matrix.md": [
                "frontend_component_state_matrix_present",
                "component-state-matrix.md",
                "local state",
                "server-cache",
                "persisted state",
                "storybook proves ui quality",
                "no secrets",
                "residual risk",
            ],
            "frontend-visual-qa.md": [
                "frontend_visual_evidence_present",
                "frontend_runtime_console_evidence_present",
                "browser/runtime evidence",
                "console status",
                "playwright trace",
                "baseline owner",
                "external visual service approval",
                "no secrets",
            ],
            "frontend-accessibility-review.md": [
                "frontend_accessibility_review_present",
                "frontend_keyboard_focus_contract_present",
                "accessibility-review.md",
                "wcag 2.2 aa",
                "keyboard",
                "focus",
                "no secrets",
                "residual risk",
            ],
            "frontend-performance-budget.md": [
                "frontend_performance_budget_present",
                "lcp",
                "inp",
                "cls",
                "lab vs field/rum",
                "playwright trace",
                "no secrets",
                "residual risk",
            ],
            "backend-service-overview.md": [
                "backend_service_boundary_present",
                "backend_runtime_behavior_present",
                "purpose",
                "owner",
                "inbound contracts",
                "outbound dependencies",
                "data ownership",
                "deployment/runtime shape",
                "ports and adapters",
                "openapi",
                "no secrets",
                "residual risk",
            ],
            "backend-runtime-behavior.md": [
                "backend_runtime_behavior_present",
                "timeout",
                "retry",
                "backoff",
                "max attempts",
                "idempotency",
                "replay",
                "recovery",
                "code inspection alone",
                "no secrets",
                "residual risk",
            ],
            "backend-dependency-failure-matrix.md": [
                "backend_dependency_failure_matrix_present",
                "timeout",
                "retry",
                "circuit breaker",
                "fallback",
                "alert",
                "owner",
                "no secrets",
                "residual risk",
            ],
            "backend-observability-map.md": [
                "backend_observability_contract_present",
                "traces",
                "metrics",
                "logs",
                "dashboards",
                "alerts",
                "correlation ids",
                "redaction",
                "no secrets",
                "residual risk",
            ],
            "backend-slo-sheet.md": [
                "backend_slo_or_gap_present",
                "user journey",
                "sli",
                "slo target",
                "measurement window",
                "alert policy",
                "no secrets",
                "residual risk",
            ],
            "backend-health-check-contract.md": [
                "backend_health_probe_contract_present",
                "liveness",
                "readiness",
                "startup",
                "platform-unavailable gap",
                "no secrets",
                "residual risk",
            ],
            "backend-job-queue-contract.md": [
                "backend_job_queue_contract_present",
                "payload contract",
                "retry policy",
                "dead-letter behavior",
                "idempotency key",
                "replay",
                "no secrets",
                "residual risk",
            ],
            "backend-data-consistency-record.md": [
                "backend_data_consistency_strategy_present",
                "transaction boundary",
                "consistency model",
                "outbox",
                "saga",
                "compensation",
                "recovery path",
                "no secrets",
                "residual risk",
            ],
            "backend-config-secrets-manifest.md": [
                "backend_config_secrets_boundary_present",
                "env/config keys without values",
                "secret source",
                "rotation notes",
                "local/prod parity",
                "required/optional",
                "no secrets",
                "residual risk",
            ],
            "backend-release-rollback-notes.md": [
                "backend_rollback_plan_present",
                "migration",
                "feature flag",
                "rollback trigger",
                "replay",
                "data recovery",
                "no secrets",
                "residual risk",
            ],
            "backend-operational-runbook.md": [
                "backend_rollback_plan_present",
                "common failures",
                "dashboard links",
                "log links",
                "recovery steps",
                "escalation",
                "operational checks",
                "no secrets",
                "residual risk",
            ],
            "versioning-policy.md": [
                "source status:",
                "semver",
                "non-semver",
                "compatibility impact",
                "deprecation",
                "migration guidance",
                "generated client",
                "owner evidence",
                "explicit gap",
                "residual risk",
            ],
        }
        self.assertEqual(set(templates), set(expected_templates))
        for name, required_terms in expected_templates.items():
            with self.subTest(name=name):
                for term in required_terms:
                    self.assertIn(term, templates[name])

    def test_planning_templates_enforce_no_placeholder_quality_gate(self):
        plan = (TEMPLATE_ROOT / "control-plane" / "PLAN.md").read_text(encoding="utf-8").lower()
        build_slice = (TEMPLATE_ROOT / "workflows" / "build-slice.md").read_text(encoding="utf-8").lower()
        plan_quality = (TEMPLATE_ROOT / "artifact-templates" / "plan-quality-check.md").read_text(
            encoding="utf-8"
        ).lower()

        shared_terms = [
            "no-placeholder",
            "plan quality gate",
            "exact files",
            "owned files",
            "forbidden files",
            "exact commands",
            "expected outputs",
            "rollback",
            "evidence owner",
            "placeholder scan",
            "mechanical_change",
            "plan repair",
            "stop before build",
            "vague validation",
            "repeated-by-reference",
        ]
        for name, text in {
            "PLAN.md": plan,
            "build-slice.md": build_slice,
            "plan-quality-check.md": plan_quality,
        }.items():
            with self.subTest(name=name):
                for term in shared_terms:
                    self.assertIn(term, text)

        self.assertIn("mechanical_change reason", plan)
        self.assertIn("non-trivial slice", build_slice)
        self.assertIn("commands without expected outputs", plan_quality)

    def test_acceptance_scenarios_templates_map_requirements_to_checks(self):
        requirements = (TEMPLATE_ROOT / "control-plane" / "REQUIREMENTS.md").read_text(
            encoding="utf-8"
        ).lower()
        test_plan = (TEMPLATE_ROOT / "control-plane" / "TEST.md").read_text(encoding="utf-8").lower()
        evals = (TEMPLATE_ROOT / "control-plane" / "EVALS.md").read_text(encoding="utf-8").lower()
        development = (TEMPLATE_ROOT / "workflows" / "development-standards.md").read_text(
            encoding="utf-8"
        ).lower()
        acceptance = (TEMPLATE_ROOT / "artifact-templates" / "acceptance-scenarios.md").read_text(
            encoding="utf-8"
        ).lower()

        shared_terms = [
            "acceptance scenarios",
            "atdd",
            "bdd",
            "requirement -> scenario -> check -> evidence owner",
            "given",
            "when",
            "then",
            "equivalent behavior format",
            "business rule",
            "edge case",
            "non-goal",
            "evidence owner",
            "behavior changes",
            "explicit gap",
        ]
        for name, text in {
            "REQUIREMENTS.md": requirements,
            "TEST.md": test_plan,
            "EVALS.md": evals,
            "development-standards.md": development,
            "acceptance-scenarios.md": acceptance,
        }.items():
            with self.subTest(name=name):
                for term in shared_terms:
                    self.assertIn(term, text)

        for term in [
            "does not replace requirements",
            "does not replace unit tests",
            "does not replace integration tests",
            "does not replace contract tests",
            "does not replace evals",
        ]:
            self.assertIn(term, acceptance)

    def test_requirements_domain_templates_connect_control_plane_and_artifacts(self):
        control_plane = "\n".join(
            (TEMPLATE_ROOT / "control-plane" / name).read_text(encoding="utf-8").lower()
            for name in ["REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
        )
        artifacts = "\n".join(
            (TEMPLATE_ROOT / "artifact-templates" / name).read_text(encoding="utf-8").lower()
            for name in [
                "requirement-registry.md",
                "stakeholder-owner-map.md",
                "story-slice-map.md",
                "acceptance-scenarios.md",
                "requirements-traceability-matrix.md",
                "business-rules.md",
                "example-map.md",
                "domain-modeling.md",
                "requirement-change-impact.md",
                "domain-review-record.md",
            ]
        )
        payloads = {"control-plane": control_plane, "artifacts": artifacts}
        shared_terms = [
            "requirements_scope_present",
            "requirements_owner_present",
            "requirement_quality_present",
            "requirement_ids_present",
            "requirements_traceability_present",
            "business_rules_present",
            "non_goals_constraints_present",
            "constraints_traceability_present",
            "open_questions_recorded",
            "declarative_acceptance_scenarios_present",
            "domain_event_contracts_present",
            "api_ui_data_traceability_present",
            "domain_expert_review_present",
            "requirement_change_impact_review_present",
            "accepted_gap_recorded",
            "requirements_evidence_before_implementation",
        ]
        for name, text in payloads.items():
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_control_plane_templates_include_bounded_context_traceability(self):
        plan = (TEMPLATE_ROOT / "control-plane" / "PLAN.md").read_text(encoding="utf-8").lower()
        test_plan = (TEMPLATE_ROOT / "control-plane" / "TEST.md").read_text(encoding="utf-8").lower()
        evals = (TEMPLATE_ROOT / "control-plane" / "EVALS.md").read_text(encoding="utf-8").lower()
        runlog = (TEMPLATE_ROOT / "control-plane" / "RUNLOG.md").read_text(encoding="utf-8").lower()

        expected_terms = [
            "domain_model_when_complex_domain",
            "bounded_context_architecture_boundary_trace",
            "bounded context",
            "architecture boundary",
            "accepted gap",
        ]
        for name, text in {
            "PLAN.md": plan,
            "TEST.md": test_plan,
            "EVALS.md": evals,
            "RUNLOG.md": runlog,
        }.items():
            with self.subTest(name=name):
                for term in expected_terms:
                    self.assertIn(term, text)

    def test_control_plane_templates_include_ubiquitous_language_traceability(self):
        plan = (TEMPLATE_ROOT / "control-plane" / "PLAN.md").read_text(encoding="utf-8").lower()
        test_plan = (TEMPLATE_ROOT / "control-plane" / "TEST.md").read_text(encoding="utf-8").lower()
        evals = (TEMPLATE_ROOT / "control-plane" / "EVALS.md").read_text(encoding="utf-8").lower()
        runlog = (TEMPLATE_ROOT / "control-plane" / "RUNLOG.md").read_text(encoding="utf-8").lower()

        expected_terms = [
            "ubiquitous_language_traceability",
            "term-to-requirement",
            "api/event/contract",
            "ui label",
            "code module or owner",
            "accepted gap",
            "domain expert",
        ]
        for name, text in {
            "PLAN.md": plan,
            "TEST.md": test_plan,
            "EVALS.md": evals,
            "RUNLOG.md": runlog,
        }.items():
            with self.subTest(name=name):
                for term in expected_terms:
                    self.assertIn(term, text)

    def test_generalized_two_stage_review_templates_cover_risky_slices(self):
        review_slice = (TEMPLATE_ROOT / "workflows" / "review-slice.md").read_text(encoding="utf-8").lower()
        runlog = (TEMPLATE_ROOT / "control-plane" / "RUNLOG.md").read_text(encoding="utf-8").lower()
        pr_risk_review = (TEMPLATE_ROOT / "artifact-templates" / "pr-risk-review.md").read_text(
            encoding="utf-8"
        ).lower()

        shared_terms = [
            "generalized two-stage review",
            "stage 1: spec compliance",
            "stage 2: quality/risk",
            "spec compliance verdict",
            "quality/risk verdict",
            "acceptance criteria",
            "source constraints",
            "public contract",
            "migration",
            "security-sensitive",
            "data migration",
            "release packaging",
            "parallel work",
            "missing evidence",
            "do not collapse",
            "generic review only",
            "quality/risk before spec compliance",
            "ready verdict with missing evidence",
        ]
        for name, text in {
            "review-slice.md": review_slice,
            "RUNLOG.md": runlog,
            "pr-risk-review.md": pr_risk_review,
        }.items():
            with self.subTest(name=name):
                for term in shared_terms:
                    self.assertIn(term, text)

    def test_behavioral_workflow_eval_template_covers_route_and_guard_cases(self):
        data = json.loads((TEMPLATE_ROOT / "evals" / "behavioral-workflows.json").read_text(encoding="utf-8"))
        case_names = {case["name"] for case in data["cases"]}

        self.assertEqual(data["name"], "behavioral-workflows")
        self.assertTrue(data["codex_only"])
        self.assertEqual(
            case_names,
            {
                "route-selection",
                "methodology-intelligence-read-only-first",
                "first-run-response",
                "first-run-empty-greenfield",
                "first-run-broken-bug-rescue",
                "first-run-existing-control-plane",
                "first-run-complex-system",
                "explicit-invocation",
                "adversarial-shortcut",
                "bug-rescue-root-cause",
                "bug-rescue-no-broad-rewrite",
                "bug-rescue-no-repro-stop",
                "acceptance-scenarios-traceability",
                "greenfield-no-scaffold-before-approval",
                "greenfield-lightweight-mode",
                "complex-ownership-split",
                "complex-no-overparallelization",
                "scenario-handoff-completeness",
                "pr-review-readiness",
                "legacy-onboarding-map",
                "api-migration-plan",
                "ai-eval-regression-plan",
                "native-mobile-runtime-plan",
                "desktop-local-runtime-plan",
                "data-migration-plan",
                "security-sensitive-change-plan",
                "security-privacy-compliance-planning-first",
                "ci-stabilization-plan",
                "release-packaging-readiness",
                "no-placeholder-plan",
                "two-stage-review",
                "fresh-context-handoff",
                "evidence-before-completion",
                "quality-current-evidence-before-completion",
                "cross-domain-semantic-evidence-sufficiency",
                "cross-domain-synthesis-mixed-surface-routing",
                "frontend-evidence-before-completion",
                "backend-evidence-before-completion",
                "llm-ai-rag-evidence-before-completion",
                "api-integrations-evidence-before-completion",
                "finish-options",
                "codex-only-compatibility",
                "cost-model-budget",
                "codex-agentic-workflow",
            },
        )
        for case in data["cases"]:
            with self.subTest(case=case["name"]):
                self.assertIn("input", case)
                self.assertIn("expected", case)
                self.assertIn("forbidden", case)
                self.assertIn("residual_risk", case)
                self.assertIsInstance(case["forbidden"], list)
                self.assertTrue(case["forbidden"])

    def test_first_run_workflow_keeps_initial_response_small_and_approval_bound(self):
        text = (TEMPLATE_ROOT / "workflows" / "first-run-intake.md").read_text(encoding="utf-8").lower()

        for expected in [
            "usage_mode",
            "confidence",
            "next smallest action",
            "minimum artifacts",
            "evidence gaps",
            "approval boundary",
            "empty workspace",
            "failed verification",
            "existing control-plane",
            "complex system",
            "at most one blocking question",
            "do not scaffold",
            "do not fix",
            "do not regenerate",
            "do not parallelize",
            "do not dump every methodology gate",
        ]:
            self.assertIn(expected, text)

    def test_bug_rescue_workflow_requires_reproduction_and_stops_without_it(self):
        text = (TEMPLATE_ROOT / "workflows" / "bug-rescue.md").read_text(encoding="utf-8").lower()

        for expected in [
            "symptom",
            "expected behavior",
            "actual behavior",
            "reproduction command",
            "manual reproduction",
            "failing evidence",
            "suspect boundary",
            "files in scope",
            "files out of scope",
            "regression test",
            "rollback",
            "stop at diagnosis",
            "do not rewrite",
        ]:
            self.assertIn(expected, text)

    def test_greenfield_workflow_requires_direction_and_approval_before_scaffold(self):
        text = (TEMPLATE_ROOT / "workflows" / "greenfield-idea-to-plan.md").read_text(encoding="utf-8").lower()

        for expected in [
            "problem",
            "users",
            "options",
            "selected direction",
            "non-goals",
            "first vertical slice",
            "acceptance scenarios",
            "metrics",
            "docs/tooling decision",
            "approval boundary",
            "do not scaffold",
            "lightweight mode",
            "next smallest artifact",
        ]:
            self.assertIn(expected, text)

    def test_complex_system_workflow_requires_integration_catalog_and_ownership_gates(self):
        text = (TEMPLATE_ROOT / "workflows" / "complex-system-acceleration.md").read_text(encoding="utf-8").lower()

        for expected in [
            "web slice",
            "api slice",
            "integration slice",
            "database slice",
            "docs slice",
            "eval slice",
            "release slice",
            "integration catalog",
            "ownership boundaries",
            "parallelization rules",
            "openapi",
            "asyncapi",
            "db/docs",
            "release gates",
            "do not parallelize",
        ]:
            self.assertIn(expected, text)

    def test_legacy_onboarding_workflow_records_unverified_orientation_before_refactor(self):
        text = (TEMPLATE_ROOT / "workflows" / "legacy-onboarding.md").read_text(encoding="utf-8").lower()

        for expected in [
            "source map",
            "entry points",
            "run commands",
            "architecture/doc gaps",
            "docs debt map",
            "verification status",
            "present_unverified",
            "first safe documentation slice",
            "without refactor",
            "do not refactor",
            "do not infer",
            "stale docs",
            "read-only",
            "approval",
        ]:
            self.assertIn(expected, text)

    def test_api_migration_workflow_requires_contract_and_rollout_gates(self):
        text = (TEMPLATE_ROOT / "workflows" / "api-migration.md").read_text(encoding="utf-8").lower()

        for expected in [
            "openapi",
            "asyncapi",
            "consumers",
            "generated clients",
            "backwards compatibility",
            "deprecation",
            "examples",
            "rollout",
            "release impact",
            "migration plan",
            "owner review",
            "do not release",
            "do not implement",
            "contract check",
            "approval",
        ]:
            self.assertIn(expected, text)

    def test_ai_eval_regression_workflow_requires_baseline_and_eval_gates(self):
        text = (TEMPLATE_ROOT / "workflows" / "ai-eval-regression.md").read_text(encoding="utf-8").lower()

        for expected in [
            "app-backed path",
            "baseline",
            "baseline/current comparison",
            "dataset policy",
            "no-secrets",
            "prompt/context",
            "prompt/context inventory",
            "retrieval metrics",
            "judge rubric",
            "thresholds",
            "latency",
            "cost",
            "grounding",
            "one-factor-at-a-time",
            "rerun command",
            "failed cases",
            "failure examples",
            "eval evidence",
            "current eval evidence",
            "do not change model",
            "do not claim quality",
            "approval",
        ]:
            self.assertIn(expected, text)

    def test_ai_eval_spec_records_baseline_rerun_report_and_current_evidence_contract(self):
        text = (TEMPLATE_ROOT / "artifact-templates" / "ai-eval-spec.md").read_text(encoding="utf-8").lower()

        for expected in [
            "source status:",
            "app-backed path",
            "app path",
            "user-visible behavior promise",
            "prompt/context inventory",
            "baseline result",
            "current result",
            "baseline/current comparison",
            "rerun command",
            "thresholds",
            "retrieval metrics",
            "judge rubric",
            "latency",
            "cost",
            "grounding",
            "failed cases",
            "current-run evidence",
            "inspection-only gap",
            "dataset source",
            "privacy class",
            "no secrets",
            "private customer data",
            "raw private chat logs",
            "owner",
            "residual risk",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

    def test_llm_ai_rag_templates_connect_control_plane_and_evals(self):
        payloads = {
            "control-plane": "\n".join(
                (TEMPLATE_ROOT / "control-plane" / name).read_text(encoding="utf-8").lower()
                for name in ["PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
            ),
            "behavioral-workflows.json": (
                TEMPLATE_ROOT / "evals" / "behavioral-workflows.json"
            ).read_text(encoding="utf-8").lower(),
            "ai-eval-regression.md": (
                TEMPLATE_ROOT / "workflows" / "ai-eval-regression.md"
            ).read_text(encoding="utf-8").lower(),
        }
        shared_terms = [
            "llm_ai_rag",
            "llm_ai_rag_readiness_when_ai_behavior_changes",
            "ai behavior promise",
            "baseline eval",
            "eval rerun",
            "dataset governance",
            "prompt-contract.md",
            "model-decision-record.md",
            "structured-output-schema.md",
            "ai-tool-contract.md",
            "rag-source-inventory.md",
            "rag-retrieval-config.md",
            "rag-eval-report.md",
            "agent-workflow-map.md",
            "guardrail-matrix.md",
            "trace-evidence-packet.md",
            "ai-cost-latency-budget.md",
            "current-run evidence",
            "accepted-gap handling",
            "prompt inspection is enough",
            "ai quality claim without current eval evidence",
        ]

        for name, text in payloads.items():
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_native_mobile_feature_workflow_requires_platform_runtime_gates(self):
        text = (TEMPLATE_ROOT / "workflows" / "native-mobile-feature.md").read_text(encoding="utf-8").lower()

        for expected in [
            "platform assumptions",
            "ios",
            "android",
            "permissions",
            "offline state",
            "simulator",
            "emulator",
            "device",
            "logs",
            "screenshots",
            "build command",
            "manual device gap",
            "runtime evidence",
            "do not claim runtime behavior",
            "do not change permissions",
            "approval",
        ]:
            self.assertIn(expected, text)

    def test_desktop_local_first_workflow_requires_local_runtime_gates(self):
        text = (TEMPLATE_ROOT / "workflows" / "desktop-local-first.md").read_text(encoding="utf-8").lower()

        for expected in [
            "desktop platform assumptions",
            "filesystem permissions",
            "local data",
            "local db",
            "indexing",
            "background jobs",
            "privacy",
            "app logs",
            "runtime log check",
            "build command",
            "recovery path",
            "rollback",
            "runtime evidence",
            "manual os gap",
            "do not claim desktop runtime behavior",
            "do not change filesystem access",
            "approval",
        ]:
            self.assertIn(expected, text)

    def test_data_migration_workflow_requires_schema_backfill_and_privacy_gates(self):
        text = (TEMPLATE_ROOT / "workflows" / "data-migration.md").read_text(encoding="utf-8").lower()

        for expected in [
            "schema change",
            "backfill",
            "data quality",
            "pii",
            "sensitive fields",
            "retention",
            "rollback",
            "validation",
            "database dictionary",
            "migration plan",
            "production db",
            "dry run",
            "backup",
            "owner review",
            "do not access production data",
            "do not run migration",
            "approval",
        ]:
            self.assertIn(expected, text)

    def test_database_data_artifact_templates_cover_contract_safety_and_approval_depth(self):
        templates = {
            "database-inventory.md": [
                "datastore",
                "owner",
                "environment",
                "production access",
                "approval_required",
            ],
            "database-dictionary.md": [
                "business meaning",
                "owner",
                "classification",
                "retention",
                "source of truth",
            ],
            "database-migration-plan.md": [
                "expand-contract",
                "transaction boundary",
                "destructive change",
                "liquibase",
                "flyway",
                "alembic",
                "prisma",
                "no universal default",
                "schema-diff tooling deferred",
                "do not run migration",
            ],
            "database-expand-contract-record.md": [
                "expand phase",
                "contract phase",
                "backward compatibility",
                "consumer compatibility",
            ],
            "database-backfill-runbook.md": [
                "batch size",
                "idempotency",
                "resume",
                "dry run",
                "row counts",
            ],
            "database-rollback-feasibility.md": [
                "rollback feasibility",
                "restore",
                "irreversible",
                "accepted gap",
                "owner approval",
            ],
            "database-backup-restore-evidence.md": [
                "backup",
                "restore test",
                "restore point",
                "no production data in prompts",
            ],
            "database-data-classification-matrix.md": [
                "pii",
                "sensitive",
                "retention",
                "deletion",
                "access boundary",
            ],
            "database-data-quality-checks.md": [
                "great expectations",
                "dbt tests",
                "constraints",
                "row counts",
                "drift",
            ],
            "database-data-contract.md": [
                "producer",
                "consumer",
                "constraints",
                "indexes",
                "schema source",
                "compatibility",
            ],
            "database-lineage-map.md": [
                "lineage",
                "openlineage",
                "dbt",
                "upstream",
                "downstream",
            ],
            "database-query-performance-review.md": [
                "query plan",
                "index",
                "explain",
                "production load risk",
                "write-side EXPLAIN ANALYZE requires approval",
            ],
            "database-retention-deletion-policy.md": [
                "retention",
                "deletion",
                "legal hold",
                "audit evidence",
            ],
            "database-synthetic-fixtures-policy.md": [
                "synthetic",
                "no secrets",
                "no production data",
                "fixtures",
            ],
            "database-production-access-approval.md": [
                "production access",
                "approval_required",
                "read-only",
                "introspection",
                "least privilege",
                "do not access production data",
            ],
        }

        for filename, expected_terms in templates.items():
            with self.subTest(template=filename):
                text = (TEMPLATE_ROOT / "artifact-templates" / filename).read_text(encoding="utf-8").lower()
                for expected in expected_terms:
                    self.assertIn(expected.lower(), text)

    def test_security_sensitive_workflow_requires_risk_review_and_approval_gates(self):
        text = (TEMPLATE_ROOT / "workflows" / "security-sensitive-change.md").read_text(encoding="utf-8").lower()

        for expected in [
            "threat surface",
            "authn",
            "authz",
            "permissions",
            "payment",
            "billing",
            "secrets",
            "pii",
            "sensitive data",
            "abuse controls",
            "rate limit",
            "audit logging",
            "security risk review",
            "rollback",
            "tests",
            "owner review",
            "approval",
            "do not store secrets",
            "do not change auth",
            "do not process payments",
            "codex security",
            "explicitly requested",
        ]:
            self.assertIn(expected, text)

    def test_ci_stabilization_workflow_requires_failure_evidence_and_no_remote_mutation(self):
        text = (TEMPLATE_ROOT / "workflows" / "ci-stabilization.md").read_text(encoding="utf-8").lower()

        for expected in [
            "failing job",
            "command",
            "logs",
            "environment",
            "deterministic",
            "flaky",
            "classification",
            "failure evidence",
            "ci stabilization report",
            "isolation plan",
            "local reproduction",
            "rerun evidence",
            "remote ci",
            "github actions",
            "approval",
            "no remote mutation",
            "do not change ci settings",
            "do not rerun remote ci",
            "do not claim ci health",
            "residual risk",
        ]:
            self.assertIn(expected, text)

    def test_release_packaging_workflow_requires_readiness_and_publish_approval(self):
        text = (TEMPLATE_ROOT / "workflows" / "release-packaging.md").read_text(encoding="utf-8").lower()

        for expected in [
            "release scope",
            "package metadata",
            "version",
            "semver",
            "changelog",
            "build evidence",
            "test evidence",
            "docs evidence",
            "security notes",
            "license",
            "artifacts",
            "release readiness",
            "publish approval",
            "tag",
            "package registry",
            "rollback",
            "owner review",
            "approval",
            "do not publish",
            "do not tag",
            "do not create release",
            "do not upload artifacts",
            "residual risk",
        ]:
            self.assertIn(expected, text)

    def test_pr_review_workflow_maps_diff_risks_and_review_evidence(self):
        text = (TEMPLATE_ROOT / "workflows" / "pr-review-readiness.md").read_text(encoding="utf-8").lower()

        for expected in [
            "changed files map",
            "diff source",
            "behavior impact",
            "api impact",
            "database impact",
            "ui impact",
            "security impact",
            "docs impact",
            "release impact",
            "missing checks",
            "review evidence",
            "two-stage review",
            "spec compliance verdict",
            "quality/risk verdict",
            "do not create a pr",
            "do not push",
            "do not publish",
            "external writes",
            "approval",
        ]:
            self.assertIn(expected, text)

    def test_scenario_workflows_emit_standard_handoff_packet(self):
        for name in ["bug-rescue.md", "greenfield-idea-to-plan.md", "complex-system-acceleration.md"]:
            text = (TEMPLATE_ROOT / "workflows" / name).read_text(encoding="utf-8").lower()
            with self.subTest(name=name):
                for expected in SCENARIO_HANDOFF_TERMS:
                    self.assertIn(expected, text)
                self.assertIn("keep the handoff concise", text)

    def test_fresh_context_handoff_templates_cover_parallel_workers(self):
        agent_task_packet = (TEMPLATE_ROOT / "artifact-templates" / "agent-task-packet.md").read_text(
            encoding="utf-8"
        ).lower()
        worktree_ownership = (TEMPLATE_ROOT / "workflows" / "worktree-ownership.md").read_text(
            encoding="utf-8"
        ).lower()
        handoff_contract = (
            PLUGIN_ROOT / "skills" / "references" / "handoff-contract.md"
        ).read_text(encoding="utf-8").lower()

        shared_terms = [
            "fresh-context handoff",
            "complete task context",
            "source constraints",
            "allowed sources",
            "inputs used",
            "owned files",
            "forbidden files",
            "expected evidence",
            "handoff output schema",
            "stop conditions",
            "sequential fallback",
            "shared ownership ambiguity",
            "missing handoff schema",
            "do not advance to parallel work",
            "shared generated files",
            "contracts",
            "migrations",
            "read-only research",
        ]

        for name, text in {
            "agent-task-packet.md": agent_task_packet,
            "worktree-ownership.md": worktree_ownership,
            "handoff-contract.md": handoff_contract,
        }.items():
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_project_readiness_eval_checks_methodology_gates(self):
        data = json.loads((TEMPLATE_ROOT / "evals" / "project-readiness.json").read_text(encoding="utf-8"))
        expected = data["cases"][0]["expected"]

        self.assertIn("methodology_gates", expected)
        self.assertIn("product_hypothesis", expected["methodology_gates"])
        self.assertIn("architecture_boundary", expected["methodology_gates"])
        self.assertIn("acceptance_scenarios_when_behavior_changes", expected["methodology_gates"])
        self.assertIn("domain_model_when_complex_domain", expected["methodology_gates"])
        self.assertIn("bounded_context_architecture_boundary_trace", expected["methodology_gates"])
        self.assertIn("ubiquitous_language_traceability", expected["methodology_gates"])
        self.assertIn("fsd_structure_when_ui_architecture_applies", expected["methodology_gates"])
        self.assertIn("frontend_methodology", expected["methodology_gates"])
        self.assertIn("metric_hardening_when_product_behavior_changes", expected["methodology_gates"])
        self.assertIn("evidence_before_completion", expected["methodology_gates"])
        self.assertIn("test_eval_first_evidence", expected["methodology_gates"])
        self.assertIn("docs_as_code_impact", expected["methodology_gates"])
        self.assertIn("release_measurement", expected["methodology_gates"])
        self.assertIn("docs_tooling_selector", expected["methodology_gates"])
        self.assertIn("standards_trigger_policy", expected["methodology_gates"])
        self.assertIn("security_privacy_compliance", expected["methodology_gates"])
        self.assertIn("domain_model", expected["methodology_signals"])
        self.assertIn("fsd_structure", expected["methodology_signals"])
        self.assertIn("frontend", expected["methodology_signals"])
        self.assertIn("metric_spec", expected["methodology_signals"])
        self.assertIn("completion_evidence", expected["methodology_signals"])
        self.assertIn("docs_tooling_decision", expected["methodology_signals"])
        self.assertIn("governance_proposal", expected["methodology_signals"])
        self.assertIn("security_privacy_compliance", expected["methodology_signals"])
        self.assertIn("security_sensitive_surface", expected["methodology_signals"])
        self.assertIn("sbom_provenance", expected["methodology_signals"])
        self.assertIn("ci_permissions", expected["methodology_signals"])
        self.assertIn("docs_as_code_impact_statuses", expected)
        self.assertEqual(
            expected["docs_as_code_impact_statuses"],
            [
                "not_applicable",
                "present_unverified",
                "present_verified",
                "proposal_staged",
                "explicit_gap_accepted",
                "approval_required",
            ],
        )

    def test_project_readiness_eval_defines_conditional_readiness_contract(self):
        data = json.loads((TEMPLATE_ROOT / "evals" / "project-readiness.json").read_text(encoding="utf-8"))
        expected = data["cases"][0]["expected"]

        self.assertEqual(
            expected["readiness_statuses"],
            [
                "not_applicable",
                "applicable_missing",
                "present_unverified",
                "present_verified",
                "proposal_staged",
                "explicit_gap_accepted",
                "approval_required",
            ],
        )

        gates = expected["conditional_readiness_gates"]
        required_gates = {
            "acceptance_scenarios_when_behavior_changes",
            "domain_model_when_complex_domain",
            "fsd_boundary_when_ui_grows",
            "frontend_methodology",
            "ai_eval_spec_when_ai_behavior_changes",
            "llm_ai_rag_readiness_when_ai_behavior_changes",
            "docs_tooling_decision",
            "contract_docs_when_api_or_event_changes",
            "api_contract_readiness_when_api_or_integration_changes",
            "database_data_readiness_when_database_or_data_changes",
            "release_version_impact_when_public_contract_changes",
            "reproduction_evidence_when_bug_rescue",
            "approval_before_greenfield_scaffold",
            "integration_catalog_when_external_systems_exist",
            "ownership_split_when_parallel_agents_used",
            "pr_risk_review_when_review_mode",
            "onboarding_map_when_legacy_repo",
            "migration_plan_when_contract_or_data_changes",
            "security_review_when_sensitive_surface",
            "security_privacy_compliance_when_sensitive_surface",
            "backend_readiness_when_backend_changes",
            "platform_runtime_check_when_native_or_desktop",
            "ci_failure_evidence_when_ci_stabilization",
            "release_readiness_when_distribution_changes",
            "delivery_release_operations_readiness_when_release_or_operations_changes",
            "plugin_success_metric_for_major_workflow",
            "root_cause_before_bug_fix",
            "no_placeholder_plan_when_plan_ready",
            "two_stage_review_when_risky_or_parallel",
            "fresh_context_handoff_when_subagents_used",
            "behavioral_eval_when_new_route_added",
            "codex_only_compatibility_when_plugin_packaging_changes",
            "finish_options_when_release_ready",
            "standards_trigger_policy_when_architecture_api_release_or_governance_changes",
            "quality_testing_evals_when_non_trivial_change",
            "codex_agentic_workflow",
            "semantic_evidence_sufficiency",
        }
        self.assertEqual(set(gates), required_gates)
        self.assertNotIn("db_docs_when_schema_changes", gates)

        for gate_id, gate in gates.items():
            with self.subTest(gate=gate_id):
                self.assertEqual(
                    set(gate),
                    {
                        "applies_when",
                        "pass_condition",
                        "accepted_gap",
                        "required_evidence",
                        "owner",
                        "residual_risk",
                    },
                )
                self.assertIsInstance(gate["required_evidence"], list)
                self.assertGreater(len(gate["required_evidence"]), 0)
                self.assertIn("explicit_gap_accepted", gate["accepted_gap"])
                gate_payload = json.dumps(gate, sort_keys=True).lower()
                self.assertRegex(
                    gate_payload,
                    r"not_applicable|applicable_missing|present_unverified|present_verified|approval_required",
                )

        ai_rag_gate = gates["llm_ai_rag_readiness_when_ai_behavior_changes"]
        ai_rag_payload = json.dumps(ai_rag_gate, sort_keys=True).lower()
        for expected_term in [
            "ai-behavior-spec.md",
            "ai-eval-spec.md",
            "eval-run-report.md",
            "prompt-contract.md",
            "model-decision-record.md",
            "rag-source-inventory.md",
            "rag-retrieval-config.md",
            "grounding",
            "tool contract",
            "approval boundary",
            "cost",
            "latency",
            "present_unverified",
        ]:
            with self.subTest(ai_rag_gate=expected_term):
                self.assertIn(expected_term, ai_rag_payload)

        security_gate = gates["security_privacy_compliance_when_sensitive_surface"]
        security_payload = json.dumps(security_gate, sort_keys=True).lower()
        for expected_term in [
            "security_privacy_compliance",
            "threat-surface.md",
            "asvs-ssdf-mapping.md",
            "authz-negative-test-matrix.md",
            "data-classification-register.md",
            "privacy-impact-record.md",
            "sbom-manifest.md",
            "codex security scan status",
            "approval_required",
            "docs-only security articles",
        ]:
            with self.subTest(security_gate=expected_term):
                self.assertIn(expected_term, security_payload)

    def test_standards_trigger_templates_cover_architecture_api_release_and_governance(self):
        payloads = {
            "adr.md": (TEMPLATE_ROOT / "artifact-templates" / "adr.md").read_text(encoding="utf-8").lower(),
            "architecture-overview.md": (
                TEMPLATE_ROOT / "artifact-templates" / "architecture-overview.md"
            ).read_text(encoding="utf-8").lower(),
            "api-contract-review.md": (
                TEMPLATE_ROOT / "artifact-templates" / "api-contract-review.md"
            ).read_text(encoding="utf-8").lower(),
            "release-packet.md": (
                TEMPLATE_ROOT / "workflows" / "release-packet.md"
            ).read_text(encoding="utf-8").lower(),
            "documentation-system.md": (
                TEMPLATE_ROOT / "workflows" / "documentation-system.md"
            ).read_text(encoding="utf-8").lower(),
            "governance-proposal.md": (
                TEMPLATE_ROOT / "artifact-templates" / "governance-proposal.md"
            ).read_text(encoding="utf-8").lower(),
            "control-plane": "\n".join(
                (TEMPLATE_ROOT / "control-plane" / name).read_text(encoding="utf-8").lower()
                for name in ["PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
            ),
            "project-readiness.json": (TEMPLATE_ROOT / "evals" / "project-readiness.json").read_text(
                encoding="utf-8"
            ).lower(),
        }

        checks = {
            "adr.md": [
                "standards_trigger_policy",
                "adr trigger policy",
                "architecture boundary",
                "api contract",
                "storage",
                "auth/security",
                "irreversible migration",
                "automation activation",
                "not_applicable",
            ],
            "architecture-overview.md": [
                "standards_trigger_policy",
                "c4 system context",
                "c4 container",
                "component/code only when useful",
                "arc42",
                "architecture goals",
                "constraints",
                "quality attributes",
                "risks",
            ],
            "api-contract-review.md": [
                "standards_trigger_policy",
                "openapi source of truth",
                "swagger ui",
                "asyncapi",
                "channel",
                "message",
                "payload schema",
                "producer",
                "consumer",
                "ordering",
                "idempotency",
                "compatibility check",
            ],
            "release-packet.md": [
                "standards_trigger_policy",
                "semver impact",
                "major",
                "minor",
                "patch",
                "not_applicable",
                "keep a changelog",
                "added",
                "changed",
                "deprecated",
                "removed",
                "fixed",
                "security",
            ],
            "documentation-system.md": [
                "standards_trigger_policy",
                "adr trigger policy",
                "c4",
                "arc42",
                "openapi source of truth",
                "asyncapi",
                "semver impact",
                "keep a changelog",
                "governance-proposal.md",
                "codeowners status",
                "github actions",
                "least privilege",
                "no forced external activation",
            ],
            "governance-proposal.md": [
                "standards_trigger_policy",
                "codeowners status",
                "present_verified",
                "proposal_staged",
                "approval_required",
                "not_applicable",
                "github actions",
                "least privilege",
                "workflow names",
                "commands",
                "permissions",
                "triggers",
                "owners",
                "no external activation without approval",
                "no forced external activation",
            ],
            "control-plane": [
                "standards_trigger_policy",
                "adr trigger policy",
                "semver impact",
                "governance-proposal.md",
                "no forced external activation",
            ],
            "project-readiness.json": [
                "standards_trigger_policy_when_architecture_api_release_or_governance_changes",
                "governance-proposal.md",
                "codeowners",
                "github actions",
                "approval_required",
                "explicit_gap_accepted",
            ],
        }

        for name, terms in checks.items():
            with self.subTest(name=name):
                for term in terms:
                    self.assertIn(term, payloads[name])

    def test_docs_tooling_templates_close_t8_a11_applicability_gate(self):
        docs_tooling = (TEMPLATE_ROOT / "artifact-templates" / "docs-tooling-decision.md").read_text(
            encoding="utf-8"
        ).lower()
        documentation = (TEMPLATE_ROOT / "workflows" / "documentation-system.md").read_text(
            encoding="utf-8"
        ).lower()
        control_plane = "\n".join(
            (TEMPLATE_ROOT / "control-plane" / name).read_text(encoding="utf-8").lower()
            for name in ["PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
        )
        project_readiness = (TEMPLATE_ROOT / "evals" / "project-readiness.json").read_text(
            encoding="utf-8"
        ).lower()

        shared_terms = [
            "docs_tooling_selector",
            "docs-tooling-decision.md",
            "docs_as_code_impact",
            "not_applicable",
            "present_unverified",
            "present_verified",
            "proposal_staged",
            "explicit_gap_accepted",
            "approval_required",
            "selected tools",
            "rejected tools",
            "evidence owner",
            "maintenance owner",
            "no forced install",
            "no ci activation without approval",
            "hosted docs approval",
            "db introspection approval",
            "docs-light",
            "internal-only",
        ]
        for name, text in {
            "docs-tooling-decision.md": docs_tooling,
            "documentation-system.md": documentation,
            "control-plane": control_plane,
            "project-readiness.json": project_readiness,
        }.items():
            with self.subTest(name=name):
                for term in shared_terms:
                    self.assertIn(term, text)

    def test_metric_hardening_templates_connect_metrics_to_release_and_control_plane(self):
        metric_spec = (TEMPLATE_ROOT / "artifact-templates" / "metric-spec.md").read_text(
            encoding="utf-8"
        ).lower()
        release_packet = (TEMPLATE_ROOT / "workflows" / "release-packet.md").read_text(
            encoding="utf-8"
        ).lower()
        control_plane = "\n".join(
            (TEMPLATE_ROOT / "control-plane" / name).read_text(encoding="utf-8").lower()
            for name in ["REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
        )

        shared_terms = [
            "metric_hardening_when_product_behavior_changes",
            "north star",
            "input metric",
            "counter-metric",
            "proxy metric",
            "guardrail",
            "qualitative review",
            "privacy classification",
            "retention period",
            "data minimization",
            "owner signoff",
            "post-release review evidence",
            "do not claim success",
        ]
        for name, text in {
            "metric-spec.md": metric_spec,
            "release-packet.md": release_packet,
            "control-plane": control_plane,
        }.items():
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_completion_evidence_templates_generalize_finish_claims(self):
        release_packet = (TEMPLATE_ROOT / "workflows" / "release-packet.md").read_text(
            encoding="utf-8"
        ).lower()
        development = (TEMPLATE_ROOT / "workflows" / "development-standards.md").read_text(
            encoding="utf-8"
        ).lower()
        control_plane = "\n".join(
            (TEMPLATE_ROOT / "control-plane" / name).read_text(encoding="utf-8").lower()
            for name in ["AGENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
        )
        behavioral = (TEMPLATE_ROOT / "evals" / "behavioral-workflows.json").read_text(
            encoding="utf-8"
        ).lower()

        shared_terms = [
            "evidence_before_completion",
            "evidence-before-completion",
            "ready claim",
            "completed claim",
            "fixed claim",
            "works claim",
            "release claim",
            "current command evidence",
            "current eval evidence",
            "current runtime evidence",
            "inspection-only",
            "explicit test gap",
            "unsupported completion claim",
            "completion claim without current evidence",
        ]
        for name, text in {
            "release-packet.md": release_packet,
            "development-standards.md": development,
            "control-plane": control_plane,
            "behavioral-workflows.json": behavioral,
        }.items():
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_quality_testing_evals_templates_connect_control_plane_and_evals(self):
        payloads = {
            "quality-strategy.md": (
                TEMPLATE_ROOT / "artifact-templates" / "quality-strategy.md"
            ).read_text(encoding="utf-8").lower(),
            "test-eval-matrix.md": (
                TEMPLATE_ROOT / "artifact-templates" / "test-eval-matrix.md"
            ).read_text(encoding="utf-8").lower(),
            "ci-evidence-record.md": (
                TEMPLATE_ROOT / "artifact-templates" / "ci-evidence-record.md"
            ).read_text(encoding="utf-8").lower(),
            "flaky-test-policy.md": (
                TEMPLATE_ROOT / "artifact-templates" / "flaky-test-policy.md"
            ).read_text(encoding="utf-8").lower(),
            "manual-qa-evidence.md": (
                TEMPLATE_ROOT / "artifact-templates" / "manual-qa-evidence.md"
            ).read_text(encoding="utf-8").lower(),
            "control-plane": "\n".join(
                (TEMPLATE_ROOT / "control-plane" / name).read_text(encoding="utf-8").lower()
                for name in ["TEST.md", "EVALS.md", "RUNLOG.md"]
            ),
            "project-readiness.json": (TEMPLATE_ROOT / "evals" / "project-readiness.json").read_text(
                encoding="utf-8"
            ).lower(),
            "behavioral-workflows.json": (
                TEMPLATE_ROOT / "evals" / "behavioral-workflows.json"
            ).read_text(encoding="utf-8").lower(),
        }

        shared_terms = [
            "quality_testing_evals",
            "quality_strategy_present",
            "risk_based_scope_present",
            "test_first_or_gap_present",
            "acceptance_traceability_present",
            "contract_check_present",
            "runtime_evidence_present",
            "manual_qa_evidence_present",
            "visual_a11y_evidence_present",
            "eval_spec_present",
            "eval_rerun_evidence_present",
            "current_evidence_before_completion",
            "ci_quality_gate_present",
            "flaky_test_policy_present",
            "coverage_policy_present",
            "test_data_privacy_present",
            "bug_reproduction_evidence_present",
            "regression_impact_present",
            "coverage is a signal, not proof",
            "present_unverified",
            "explicit_gap_accepted",
            "approval_required",
        ]
        for name, text in payloads.items():
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_codex_agentic_workflow_templates_connect_control_plane_and_evals(self):
        payloads = {
            "model-reasoning-policy.md": (
                TEMPLATE_ROOT / "artifact-templates" / "model-reasoning-policy.md"
            ).read_text(encoding="utf-8").lower(),
            "mcp-permission-review.md": (
                TEMPLATE_ROOT / "artifact-templates" / "mcp-permission-review.md"
            ).read_text(encoding="utf-8").lower(),
            "hook-governance.md": (
                TEMPLATE_ROOT / "artifact-templates" / "hook-governance.md"
            ).read_text(encoding="utf-8").lower(),
            "skill-promotion-record.md": (
                TEMPLATE_ROOT / "artifact-templates" / "skill-promotion-record.md"
            ).read_text(encoding="utf-8").lower(),
            "agent-eval-workflow.md": (
                TEMPLATE_ROOT / "artifact-templates" / "agent-eval-workflow.md"
            ).read_text(encoding="utf-8").lower(),
            "AGENTS.md": (TEMPLATE_ROOT / "control-plane" / "AGENTS.md").read_text(
                encoding="utf-8"
            ).lower(),
            "config.toml": (TEMPLATE_ROOT / "config" / "config.toml").read_text(
                encoding="utf-8"
            ).lower(),
            "control-plane": "\n".join(
                (TEMPLATE_ROOT / "control-plane" / name).read_text(encoding="utf-8").lower()
                for name in ["PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
            ),
            "project-readiness.json": (TEMPLATE_ROOT / "evals" / "project-readiness.json").read_text(
                encoding="utf-8"
            ).lower(),
            "behavioral-workflows.json": (
                TEMPLATE_ROOT / "evals" / "behavioral-workflows.json"
            ).read_text(encoding="utf-8").lower(),
        }

        shared_terms = [
            "codex_agentic_workflow",
            "agentic_scope_classified",
            "control_plane_present",
            "source_of_truth_present",
            "read_only_discovery_complete",
            "model_reasoning_policy_present",
            "fresh_context_handoff_present",
            "ownership_split_present",
            "subagent_parallelism_safe",
            "approval_boundary_present",
            "mcp_permission_review_present",
            "hook_activation_approval_present",
            "plugin_boundary_present",
            "skill_promotion_evidence_present",
            "automation_manual_stability_present",
            "agent_eval_workflow_present",
            "memory_policy_present",
            "agentic_evidence_before_completion",
            "codex app",
            "ide extension",
            "codex exec",
            "github action",
            "mcp",
            "agents sdk",
            "automation",
            "present_unverified",
            "explicit_gap_accepted",
            "approval_required",
            "no silent activation",
            "memory as recall only",
        ]
        for name, text in payloads.items():
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_ui_fsd_structure_routing_is_conditional(self):
        component = (TEMPLATE_ROOT / "artifact-templates" / "component-card.md").read_text(
            encoding="utf-8"
        ).lower()
        development = (TEMPLATE_ROOT / "workflows" / "development-standards.md").read_text(
            encoding="utf-8"
        ).lower()
        control_plane = "\n".join(
            (TEMPLATE_ROOT / "control-plane" / name).read_text(encoding="utf-8").lower()
            for name in ["PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
        )

        shared_terms = [
            "fsd_structure",
            "feature-sliced design",
            "layer",
            "slice",
            "segment",
            "public api",
            "import rule",
            "not applicable",
            "backend",
            "native",
            "simple crud",
            "simple mvp",
        ]
        for name, text in {
            "component-card.md": component,
            "development-standards.md": development,
            "control-plane": control_plane,
        }.items():
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_archive_template_preserves_evidence_and_privacy_boundary(self):
        template = next(
            item for item in required_templates() if item.target_path == ".codex/runlogs/archive/README.md"
        )
        text = template.source_path.read_text(encoding="utf-8")

        self.assertIn("preserve evidence", text.lower())
        self.assertIn("do not store raw private chat logs", text.lower())
        self.assertIn("explicit approval", text.lower())

    def test_hook_pre_tool_use_blocks_destructive_command_and_observes_safe_command(self):
        hook = TEMPLATE_ROOT / "hooks" / "pre_tool_use_policy.py"
        destructive = subprocess.run(
            [sys.executable, str(hook)],
            input=json.dumps({"command": "git reset --hard HEAD"}),
            check=False,
            capture_output=True,
            text=True,
        )
        safe = subprocess.run(
            [sys.executable, str(hook)],
            input=json.dumps({"command": "python tools/check_docs.py"}),
            check=False,
            capture_output=True,
            text=True,
        )

        destructive_payload = json.loads(destructive.stdout)
        safe_payload = json.loads(safe.stdout)
        self.assertEqual(destructive.returncode, 1)
        self.assertEqual(destructive_payload["decision"], "block")
        self.assertEqual(safe.returncode, 0)
        self.assertEqual(safe_payload["decision"], "observe")

    def test_hook_permission_and_evidence_templates_emit_json(self):
        for name in ["permission_request_summary.py", "post_tool_use_evidence.py"]:
            with self.subTest(name=name):
                hook = TEMPLATE_ROOT / "hooks" / name
                result = subprocess.run(
                    [sys.executable, str(hook)],
                    input=json.dumps({"command": "python tools/check_docs.py"}),
                    check=False,
                    capture_output=True,
                    text=True,
                )
                payload = json.loads(result.stdout)
                self.assertEqual(result.returncode, 0)
                self.assertIn("hook", payload)

    def test_api_integration_templates_cover_contract_depth_and_deferrals(self):
        payloads = {
            name: (TEMPLATE_ROOT / "artifact-templates" / name).read_text(encoding="utf-8").lower()
            for name in [
                "api-inventory.md",
                "api-contract-review.md",
                "api-error-catalog.md",
                "api-auth-authorization-matrix.md",
                "api-consumer-map.md",
                "api-compatibility-record.md",
                "api-contract-test-matrix.md",
                "generated-sdk-manifest.md",
                "webhook-event-contract.md",
                "external-integration-approval.md",
                "api-style-guide.md",
                "integration-catalog.md",
                "migration-plan.md",
            ]
        }
        expected_terms = {
            "api-inventory.md": [
                "source status:",
                "provider",
                "consumers",
                "owners",
                "generated clients",
                "runtime environments",
                "draft",
                "experimental",
                "stable",
                "deprecated",
                "removed",
                "compatibility policy",
                "deprecation path",
                "accepted gap",
            ],
            "api-contract-review.md": [
                "source status:",
                "openapi",
                "asyncapi",
                "graphql",
                "grpc",
                "protobuf",
                "json schema",
                "dialect",
                "pact",
                "rfc 9457",
                "problem details",
                "security schemes",
                "contract drift",
                "request id",
                "correlation id",
                "swagger ui is not source of truth",
                "external write",
            ],
            "api-error-catalog.md": [
                "source status:",
                "success example",
                "validation failure",
                "auth failure",
                "domain failure",
                "status code",
                "error type",
                "extensions",
                "rfc 9457",
                "compatibility reason",
            ],
            "api-auth-authorization-matrix.md": [
                "source status:",
                "openapi security schemes",
                "graphql auth",
                "scopes",
                "token claims",
                "object-level authorization",
                "rate limits",
                "sensitive fields",
                "abuse cases",
                "prose-only security notes",
            ],
            "api-consumer-map.md": [
                "source status:",
                "consumer",
                "owner",
                "generated client",
                "approval path",
                "multi-repository generated clients deferred",
            ],
            "api-compatibility-record.md": [
                "source status:",
                "additive",
                "behavior-compatible",
                "potentially breaking",
                "breaking",
                "contract drift",
                "deprecation window",
                "rollback",
            ],
            "api-contract-test-matrix.md": [
                "source status:",
                "schema validation",
                "provider verification",
                "consumer-driven",
                "pact",
                "negative cases",
                "missing-tool gap",
                "no forced spectral",
                "framework-native",
            ],
            "generated-sdk-manifest.md": [
                "source status:",
                "generator",
                "version",
                "config",
                "target languages",
                "regeneration command",
                "reviewable diff",
                "semver impact",
                "release process",
            ],
            "webhook-event-contract.md": [
                "source status:",
                "schema",
                "headers",
                "signature verification",
                "correlation id",
                "idempotency key",
                "retry policy",
                "ordering guarantee",
                "replay",
                "dead-letter",
                "cloudevents",
            ],
            "external-integration-approval.md": [
                "source status:",
                "read capability",
                "write capability",
                "sandbox credentials",
                "staged draft",
                "approval_required",
                "rollback",
                "no secrets",
            ],
            "api-style-guide.md": [
                "source status:",
                "no universal default",
                "spectral",
                "redocly",
                "framework-native",
                "graphql",
                "grpc",
                "event-driven",
                "deferred with owner/reason",
            ],
            "integration-catalog.md": [
                "request id",
                "correlation id",
                "error counters",
                "latency",
                "rate-limit metrics",
                "integration failure alerts",
            ],
            "migration-plan.md": [
                "generated sdk",
                "semver impact",
                "external write approval",
                "contract check command",
                "release/rollback impact",
            ],
        }

        for name, terms in expected_terms.items():
            text = payloads[name]
            with self.subTest(template=name):
                for term in terms:
                    self.assertIn(term, text)

        readiness = (TEMPLATE_ROOT / "evals" / "project-readiness.json").read_text(encoding="utf-8").lower()
        for term in [
            "api_integrations",
            "api_contract_readiness_when_api_or_integration_changes",
            "api_contract_source_present",
            "api_consumer_map_present",
            "api_security_reviewed",
            "api_error_contract_present",
            "api_contract_test_matrix_present",
            "event_delivery_contract_present",
            "generated_client_manifest_present",
            "external_write_approval_present",
            "swagger ui is not source of truth",
        ]:
            with self.subTest(readiness=term):
                self.assertIn(term, readiness)

    def test_cross_domain_semantic_evidence_sufficiency_contract_is_shared(self):
        payloads = {
            "PLAN.md": (TEMPLATE_ROOT / "control-plane" / "PLAN.md").read_text(encoding="utf-8"),
            "TEST.md": (TEMPLATE_ROOT / "control-plane" / "TEST.md").read_text(encoding="utf-8"),
            "EVALS.md": (TEMPLATE_ROOT / "control-plane" / "EVALS.md").read_text(encoding="utf-8"),
            "RUNLOG.md": (TEMPLATE_ROOT / "control-plane" / "RUNLOG.md").read_text(encoding="utf-8"),
            "project-readiness.json": (TEMPLATE_ROOT / "evals" / "project-readiness.json").read_text(
                encoding="utf-8"
            ),
            "behavioral-workflows.json": (
                TEMPLATE_ROOT / "evals" / "behavioral-workflows.json"
            ).read_text(encoding="utf-8"),
        }
        joined = "\n".join(payloads.values()).lower()

        for expected in [
            "semantic_evidence_sufficiency",
            "owner_reviewed_evidence_sufficient_for_real_project_risk",
            "high-risk",
            "production",
            "release",
            "security-sensitive",
            "ai",
            "public-contract",
            "owner",
            "reason",
            "review_date",
            "downstream_risk",
            "follow_up_condition",
            "present_unverified",
            "explicit_gap_accepted",
            "approval_required",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, joined)

        readiness = json.loads(payloads["project-readiness.json"])
        gate = readiness["cases"][0]["expected"]["conditional_readiness_gates"]["semantic_evidence_sufficiency"]
        self.assertIn("owner_reviewed_evidence_sufficient_for_real_project_risk", gate["pass_condition"])
        self.assertEqual(
            gate["required_evidence"],
            [
                "current command/eval/runtime evidence",
                "owner_reviewed_evidence_sufficient_for_real_project_risk",
                "accepted gap owner",
                "accepted gap reason",
                "review_date",
                "downstream_risk",
                "follow_up_condition",
            ],
        )

        generated = "\n".join(
            (TEMPLATE_ROOT / relative).read_text(encoding="utf-8").lower()
            for relative in [
                "control-plane/PLAN.md",
                "control-plane/TEST.md",
                "control-plane/EVALS.md",
                "control-plane/RUNLOG.md",
                "evals/behavioral-workflows.json",
            ]
        )
        for term in [
            "api & integrations methodology (`api_integrations`)",
            "api_contract_source_present",
            "api_consumer_map_present",
            "api_security_reviewed",
            "api_error_contract_present",
            "api_contract_test_matrix_present",
            "event_delivery_contract_present",
            "generated_client_manifest_present",
            "external_write_approval_present",
            "swagger ui is not source of truth",
            "schema validation alone is not contract testing",
            "oauth alone is not complete security evidence",
            "graphql/grpc/events are not universal defaults",
        ]:
            with self.subTest(generated=term):
                self.assertIn(term, generated)

    def _context(self):
        return {
            "project_name": "Synthetic Project",
            "workspace_path": "C:/workspace/synthetic-project",
            "profile_name": "standard-product",
            "detected_stack": ["python"],
            "detected_stack_text": "python",
            "existing_control_plane": [],
            "missing_control_plane": ["AGENTS.md"],
            "existing_codex_assets": [],
            "risk_text": "no detected test files or test configuration",
            "generated_at": "2026-05-14",
        }

    def _render_temp_file(self, item, context):
        root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        path = root / item.target_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_template(item, context), encoding="utf-8")
        return path


if __name__ == "__main__":
    unittest.main()
