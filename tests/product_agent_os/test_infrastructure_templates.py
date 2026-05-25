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

from product_agent_os.templates import required_templates, render_template  # noqa: E402
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
    ".codex/artifact-templates/component-card.md",
    ".codex/artifact-templates/database-dictionary.md",
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
    ".codex/artifact-templates/security-risk-review.md",
    ".codex/artifact-templates/ci-stabilization-report.md",
    ".codex/artifact-templates/release-readiness.md",
    ".codex/artifact-templates/test-eval-matrix.md",
    ".codex/artifact-templates/quality-strategy.md",
    ".codex/artifact-templates/ci-evidence-record.md",
    ".codex/artifact-templates/flaky-test-policy.md",
    ".codex/artifact-templates/manual-qa-evidence.md",
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
                "ci-stabilization-plan",
                "release-packaging-readiness",
                "no-placeholder-plan",
                "two-stage-review",
                "fresh-context-handoff",
                "evidence-before-completion",
                "quality-current-evidence-before-completion",
                "finish-options",
                "codex-only-compatibility",
                "cost-model-budget",
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
            "baseline",
            "dataset policy",
            "no-secrets",
            "prompt/context",
            "retrieval metrics",
            "judge rubric",
            "threshold",
            "latency",
            "cost",
            "grounding",
            "one-factor-at-a-time",
            "rerun command",
            "failure examples",
            "eval evidence",
            "do not change model",
            "do not claim quality",
            "approval",
        ]:
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
        self.assertIn("metric_hardening_when_product_behavior_changes", expected["methodology_gates"])
        self.assertIn("evidence_before_completion", expected["methodology_gates"])
        self.assertIn("test_eval_first_evidence", expected["methodology_gates"])
        self.assertIn("docs_as_code_impact", expected["methodology_gates"])
        self.assertIn("release_measurement", expected["methodology_gates"])
        self.assertIn("docs_tooling_selector", expected["methodology_gates"])
        self.assertIn("standards_trigger_policy", expected["methodology_gates"])
        self.assertIn("domain_model", expected["methodology_signals"])
        self.assertIn("fsd_structure", expected["methodology_signals"])
        self.assertIn("metric_spec", expected["methodology_signals"])
        self.assertIn("completion_evidence", expected["methodology_signals"])
        self.assertIn("docs_tooling_decision", expected["methodology_signals"])
        self.assertIn("governance_proposal", expected["methodology_signals"])
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
            "ai_eval_spec_when_ai_behavior_changes",
            "docs_tooling_decision",
            "contract_docs_when_api_or_event_changes",
            "db_docs_when_schema_changes",
            "release_version_impact_when_public_contract_changes",
            "reproduction_evidence_when_bug_rescue",
            "approval_before_greenfield_scaffold",
            "integration_catalog_when_external_systems_exist",
            "ownership_split_when_parallel_agents_used",
            "pr_risk_review_when_review_mode",
            "onboarding_map_when_legacy_repo",
            "migration_plan_when_contract_or_data_changes",
            "security_review_when_sensitive_surface",
            "platform_runtime_check_when_native_or_desktop",
            "ci_failure_evidence_when_ci_stabilization",
            "release_readiness_when_distribution_changes",
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
        }
        self.assertEqual(set(gates), required_gates)

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
