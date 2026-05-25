import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.discovery import analyze_workspace, discover_workspace  # noqa: E402


class DiscoveryTest(unittest.TestCase):
    def test_node_app_detection(self):
        result = analyze_workspace(FIXTURES / "node-app")

        self.assertIn("node", result["detected_stack"])
        self.assertIn("package.json", result["detected_files"])
        self.assertEqual(result["complexity_profile"]["name"], "guided-small")
        self.assertEqual(result["usage_mode"]["primary"], "standard_feature")
        self.assertIn("workspace audit packet", result["usage_mode"]["minimum_artifacts"])

    def test_discovery_includes_methodology_intelligence_packet(self):
        result = discover_workspace(FIXTURES / "node-app")

        self.assertIn("methodology_intelligence", result)
        packet = result["methodology_intelligence"]
        self.assertIn("maturity_level", packet)
        self.assertIn("complexity_profile", packet)
        self.assertIn("delivery_map", packet)
        self.assertIn("recommendations", packet)
        self.assertEqual(packet["write_policy"], "read_only")

    def test_docs_repo_detection(self):
        result = analyze_workspace(FIXTURES / "docs-repo")

        self.assertIn("docs", result["detected_stack"])
        self.assertIn("mkdocs.yml", result["detected_files"])
        self.assertEqual(result["usage_mode"]["primary"], "docs_only")
        self.assertIn("docs tooling decision", result["usage_mode"]["minimum_artifacts"])

    def test_existing_control_plane_detection(self):
        result = analyze_workspace(FIXTURES / "existing-codex-config")

        self.assertIn("AGENTS.md", result["existing_control_plane"])
        self.assertIn(".codex/config.toml", result["existing_codex_assets"])
        self.assertIn("first_response_contract", result["usage_mode"])
        self.assertEqual(result["usage_mode"]["primary"], "maintenance")
        self.assertIn("first-run-existing-control-plane", result["usage_mode"]["behavioral_eval_cases"])

    def test_greenfield_usage_mode_for_empty_or_idea_workspace(self):
        result = analyze_workspace(FIXTURES / "empty-repo")

        usage_mode = result["usage_mode"]
        self.assertEqual(usage_mode["primary"], "greenfield_idea")
        self.assertEqual(usage_mode["confidence"], "high")
        self.assertEqual(usage_mode["fallback"], "standard_feature")
        self.assertIn("greenfield idea brief", usage_mode["minimum_artifacts"])
        self.assertIn("approval before scaffold", usage_mode["minimum_artifacts"])
        self.assertIn("greenfield-no-scaffold-before-approval", usage_mode["behavioral_eval_cases"])
        self.assertIn("greenfield-lightweight-mode", usage_mode["behavioral_eval_cases"])
        self.assertIn("first-run-empty-greenfield", usage_mode["behavioral_eval_cases"])
        self.assertIn("approval boundary", usage_mode["first_response_contract"])
        self.assertIn("minimum artifacts", usage_mode["first_response_contract"])
        self.assertIn("evidence gaps", usage_mode["first_response_contract"])

    def test_bug_rescue_usage_mode_from_failed_verification(self):
        result = analyze_workspace(FIXTURES / "failed-verification")

        usage_mode = result["usage_mode"]
        self.assertEqual(usage_mode["primary"], "bug_rescue")
        self.assertIn("failed verification evidence", " ".join(usage_mode["reasons"]))
        self.assertIn("bug rescue report", usage_mode["minimum_artifacts"])
        self.assertIn("bug-rescue-root-cause", usage_mode["behavioral_eval_cases"])
        self.assertIn("first-run-broken-bug-rescue", usage_mode["behavioral_eval_cases"])

        reproduction = result["bug_reproduction_signals"]
        self.assertTrue(reproduction["present"])
        self.assertIn("RUNLOG.md", reproduction["evidence_files"])
        self.assertEqual(reproduction["verification_status"], "possible_evidence")
        self.assertIn("not verified truth", reproduction["note"])

    def test_bug_reproduction_signals_detect_candidate_logs_without_claiming_truth(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            (workspace / "package.json").write_text("{}", encoding="utf-8")
            (workspace / "logs").mkdir()
            (workspace / "logs" / "pytest.log").write_text(
                "FAILED tests/test_checkout.py::test_total\nexit_code: 1\n",
                encoding="utf-8",
            )

            result = analyze_workspace(workspace)

        reproduction = result["bug_reproduction_signals"]
        self.assertTrue(reproduction["present"])
        self.assertEqual(reproduction["verification_status"], "possible_evidence")
        self.assertEqual(reproduction["evidence_files"], ["logs/pytest.log"])
        self.assertIn("rerun required", reproduction["note"])
        self.assertEqual(result["usage_mode"]["primary"], "bug_rescue")

    def test_bug_reproduction_signals_avoid_false_positive_from_regular_docs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            (workspace / "package.json").write_text("{}", encoding="utf-8")
            (workspace / "docs").mkdir()
            (workspace / "docs" / "failure-analysis.md").write_text(
                "# Failure analysis\nA historical failed test is described here.\n",
                encoding="utf-8",
            )

            result = analyze_workspace(workspace)

        reproduction = result["bug_reproduction_signals"]
        self.assertFalse(reproduction["present"])
        self.assertEqual(reproduction["verification_status"], "not_found")
        self.assertEqual(reproduction["evidence_files"], [])
        self.assertEqual(result["usage_mode"]["primary"], "standard_feature")

    def test_complex_system_acceleration_usage_mode_for_monorepo(self):
        result = analyze_workspace(FIXTURES / "monorepo")

        usage_mode = result["usage_mode"]
        self.assertEqual(usage_mode["primary"], "complex_system_acceleration")
        self.assertIn("integration catalog", usage_mode["minimum_artifacts"])
        self.assertIn("ownership split", usage_mode["minimum_artifacts"])
        self.assertIn("release gates", usage_mode["minimum_artifacts"])
        self.assertIn("fresh-context-handoff", usage_mode["behavioral_eval_cases"])
        self.assertIn("complex-ownership-split", usage_mode["behavioral_eval_cases"])
        self.assertIn("complex-no-overparallelization", usage_mode["behavioral_eval_cases"])
        self.assertIn("first-run-complex-system", usage_mode["behavioral_eval_cases"])

    def test_prompt_intent_can_route_pr_review_without_workspace_writes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            (workspace / "package.json").write_text("{}", encoding="utf-8")

            result = analyze_workspace(workspace, intent_hint="Please review this PR diff before merge")

        usage_mode = result["usage_mode"]
        self.assertEqual(usage_mode["primary"], "pr_review")
        self.assertIn("prompt requests PR or diff review", usage_mode["reasons"])
        self.assertIn("pr review readiness", usage_mode["minimum_artifacts"])
        self.assertIn("pr risk review", usage_mode["minimum_artifacts"])
        self.assertIn("pr-review-readiness", usage_mode["behavioral_eval_cases"])

    def test_diff_surface_routes_pr_review_and_reports_pr_route_inputs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": '{"name": "fixture-pr-review"}\n',
                    "diff.patch": "diff --git a/api/openapi.yaml b/api/openapi.yaml\n",
                    ".codex/pr/changed-files.md": "- openapi/public.yaml\n- migrations/202605230001_add_users.sql\n",
                    "openapi/public.yaml": "openapi: 3.2.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                    "migrations/202605230001_add_users.sql": "alter table users add column email text;\n",
                },
            )

            result = analyze_workspace(workspace)

        usage_mode = result["usage_mode"]
        self.assertEqual(usage_mode["primary"], "pr_review")
        self.assertIn("workspace has PR diff or changed-files review signals", usage_mode["reasons"])
        self.assertIn("pr review readiness", usage_mode["minimum_artifacts"])
        self.assertIn("pr_review_surface", result["route_inputs"]["workspace_signals"]["active_surfaces"])
        self.assertIn("api_migration", usage_mode["secondary"])
        self.assertIn("data_migration", usage_mode["secondary"])

    def test_undocumented_run_script_repo_routes_legacy_with_unverified_statuses(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "src/app.py": "print('synthetic undocumented app')\n",
                    "scripts/run.sh": "#!/bin/sh\npython src/app.py\n",
                },
            )

            result = analyze_workspace(workspace)

        usage_mode = result["usage_mode"]
        self.assertEqual(usage_mode["primary"], "legacy_onboarding")
        self.assertIn("workspace has legacy or undocumented repository signals", usage_mode["reasons"])
        self.assertIn("onboarding map", usage_mode["minimum_artifacts"])
        self.assertIn("legacy-onboarding-map", usage_mode["behavioral_eval_cases"])
        self.assertIn("legacy_docs_debt_surface", result["route_inputs"]["workspace_signals"]["active_surfaces"])

        signals = result["legacy_onboarding_signals"]
        self.assertEqual(signals["entry_points_status"], "present_unverified")
        self.assertEqual(signals["run_commands_status"], "present_unverified")
        self.assertEqual(signals["documentation_status"], "applicable_missing")
        self.assertEqual(signals["architecture_status"], "applicable_missing")
        self.assertIn("present_unverified until commands run", signals["note"])

    def test_api_contract_repo_routes_migration_with_unverified_contract_signals(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": '{"name": "fixture-api-migration", "version": "2.0.0"}\n',
                    "openapi/public.yaml": (
                        "openapi: 3.2.0\n"
                        "info:\n  title: Public API\n  version: 2.0.0\n"
                        "paths: {}\n"
                    ),
                    "asyncapi/events.yaml": (
                        "asyncapi: 3.0.0\n"
                        "info:\n  title: Events\n  version: 2.0.0\n"
                        "channels: {}\n"
                    ),
                    "clients/generated/README.md": "# Generated clients\n",
                    "docs/deprecations/v1.md": "# Deprecated v1 endpoints\n",
                    "docs/api-migration-v2.md": "# API migration\n",
                    "CHANGELOG.md": "# Changelog\n",
                },
            )

            result = analyze_workspace(workspace)

        usage_mode = result["usage_mode"]
        self.assertEqual(usage_mode["primary"], "api_migration")
        self.assertIn("workspace has API contract migration signals", usage_mode["reasons"])
        self.assertIn("migration plan", usage_mode["minimum_artifacts"])
        self.assertIn("api contract review", usage_mode["minimum_artifacts"])
        self.assertIn("api-migration-plan", usage_mode["behavioral_eval_cases"])
        self.assertIn("api_contract_surface", result["route_inputs"]["workspace_signals"]["active_surfaces"])

        signals = result["api_migration_signals"]
        self.assertEqual(signals["contract_sources_status"], "present_unverified")
        self.assertEqual(signals["consumer_impact_status"], "present_unverified")
        self.assertEqual(signals["generated_clients_status"], "present_unverified")
        self.assertEqual(signals["deprecation_status"], "present_unverified")
        self.assertEqual(signals["release_impact_status"], "present_unverified")
        self.assertEqual(signals["verification_status"], "applicable_missing")
        self.assertIn("present_unverified until contract lint", signals["note"])

    def test_api_integration_signals_record_contract_depth_without_execution(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "openapi/public.yaml": "openapi: 3.2.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                    "asyncapi/events.yaml": "asyncapi: 3.1.0\ninfo:\n  title: Events\n  version: 1.0.0\nchannels: {}\n",
                    "graphql/schema.graphql": "type Query { order(id: ID!): Order }\n",
                    "proto/orders.proto": "syntax = 'proto3';\n",
                    "schemas/order.schema.json": (
                        '{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}\n'
                    ),
                    "pacts/order-consumer.json": "{}\n",
                    "clients/generated/orders/README.md": "# generated client\n",
                    "webhooks/order-created.md": "# webhook\n",
                    "integrations/payment-provider.md": "# external provider\n",
                    "docs/api-compatibility.md": "# compatibility and deprecation\n",
                    "docs/oauth-scopes.md": "# OAuth scopes token rate limit errors\n",
                },
            )

            result = analyze_workspace(workspace)

        signals = result["route_inputs"]["workspace_signals"]["api_integration_signals"]
        expected_sources = {
            "contract_sources": "openapi/public.yaml",
            "event_contract_sources": "asyncapi/events.yaml",
            "graphql_sources": "graphql/schema.graphql",
            "protobuf_sources": "proto/orders.proto",
            "json_schema_sources": "schemas/order.schema.json",
            "pact_sources": "pacts/order-consumer.json",
            "generated_client_sources": "clients/generated/orders/README.md",
            "webhook_event_sources": "webhooks/order-created.md",
            "external_provider_sources": "integrations/payment-provider.md",
            "security_auth_sources": "docs/oauth-scopes.md",
            "compatibility_sources": "docs/api-compatibility.md",
        }
        for category, source in expected_sources.items():
            with self.subTest(category=category):
                packet = signals[category]
                self.assertEqual(packet["status"], "present_unverified")
                self.assertIn(source, packet["sources"])
        self.assertIn("without executing API tools", signals["note"])
        self.assertIn("external writes", signals["note"])
        self.assertIn("approval_required", signals["note"])
        self.assertIn("api_contract_surface", result["route_inputs"]["workspace_signals"]["active_surfaces"])

    def test_swagger_ui_only_does_not_create_api_contract_surface(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "docs/swagger-ui.html": "<html>Swagger UI rendered output</html>\n",
                    "docs/api/index.html": "<html>Rendered API docs</html>\n",
                },
            )

            result = analyze_workspace(workspace)

        self.assertNotIn("api_contract_surface", result["route_inputs"]["workspace_signals"]["active_surfaces"])
        signals = result["route_inputs"]["workspace_signals"]["api_integration_signals"]
        self.assertEqual(signals["contract_sources"]["status"], "applicable_missing")

    def test_ai_eval_repo_routes_regression_with_unverified_eval_signals(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": '{"name": "fixture-rag-quality"}\n',
                    "evals/rag-regression.json": '{"cases": [], "metric": "grounding"}\n',
                    "evals/baseline-result.json": '{"score": 0.72}\n',
                    "evals/thresholds/quality.json": '{"grounding": 0.90}\n',
                    "datasets/synthetic-rag.jsonl": '{"question": "synthetic"}\n',
                    "prompts/retrieval.md": "# Retrieval prompt\n",
                    "docs/eval-rubric.md": "# Judge rubric\n",
                    "reports/latency-cost.md": "# Latency and cost\n",
                    "reports/failure-examples.md": "# Failure examples\n",
                    "scripts/run-evals.js": "console.log('synthetic eval runner');\n",
                },
            )

            result = analyze_workspace(workspace)

        usage_mode = result["usage_mode"]
        self.assertEqual(usage_mode["primary"], "ai_eval_regression")
        self.assertIn("workspace has AI or RAG eval regression signals", usage_mode["reasons"])
        self.assertIn("ai eval spec", usage_mode["minimum_artifacts"])
        self.assertIn("baseline result", usage_mode["minimum_artifacts"])
        self.assertIn("ai-eval-regression-plan", usage_mode["behavioral_eval_cases"])
        self.assertIn("ai_eval_surface", result["route_inputs"]["workspace_signals"]["active_surfaces"])

        signals = result["ai_eval_signals"]
        self.assertEqual(signals["baseline_status"], "present_unverified")
        self.assertEqual(signals["dataset_status"], "present_unverified")
        self.assertEqual(signals["prompt_context_status"], "present_unverified")
        self.assertEqual(signals["retrieval_status"], "present_unverified")
        self.assertEqual(signals["judge_rubric_status"], "present_unverified")
        self.assertEqual(signals["threshold_status"], "present_unverified")
        self.assertEqual(signals["latency_cost_status"], "present_unverified")
        self.assertEqual(signals["failure_examples_status"], "present_unverified")
        self.assertEqual(signals["verification_status"], "applicable_missing")
        self.assertIn("present_unverified until eval rerun", signals["note"])

    def test_native_mobile_repo_routes_feature_with_unverified_platform_signals(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "android/settings.gradle": 'pluginManagement { repositories { google() } }\n',
                    "android/app/build.gradle": "plugins { id 'com.android.application' }\n",
                    "android/app/src/main/AndroidManifest.xml": (
                        "<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\">\n"
                        "  <uses-permission android:name=\"android.permission.CAMERA\" />\n"
                        "</manifest>\n"
                    ),
                    "ios/App.xcodeproj/project.pbxproj": "// synthetic xcode project\n",
                    "ios/App/App.entitlements": "<plist />\n",
                    "docs/mobile-permissions.md": "# Mobile permissions\n",
                    "docs/offline-sync.md": "# Offline sync\n",
                    "reports/android-emulator-log.txt": "emulator booted in synthetic fixture\n",
                    "reports/screenshots/home.png": "synthetic screenshot placeholder\n",
                },
            )

            result = analyze_workspace(workspace)

        usage_mode = result["usage_mode"]
        self.assertEqual(usage_mode["primary"], "native_mobile_feature")
        self.assertIn("workspace has native or mobile runtime signals", usage_mode["reasons"])
        self.assertIn("platform runtime check", usage_mode["minimum_artifacts"])
        self.assertIn("acceptance scenarios", usage_mode["minimum_artifacts"])
        self.assertIn("native-mobile-runtime-plan", usage_mode["behavioral_eval_cases"])
        self.assertIn("native_mobile_surface", result["route_inputs"]["workspace_signals"]["active_surfaces"])

        signals = result["native_mobile_signals"]
        self.assertEqual(signals["platform_status"], "present_unverified")
        self.assertEqual(signals["permission_status"], "present_unverified")
        self.assertEqual(signals["offline_status"], "present_unverified")
        self.assertEqual(signals["simulator_emulator_status"], "present_unverified")
        self.assertEqual(signals["build_command_status"], "present_unverified")
        self.assertEqual(signals["logs_status"], "present_unverified")
        self.assertEqual(signals["screenshot_status"], "present_unverified")
        self.assertEqual(signals["verification_status"], "applicable_missing")
        self.assertIn("present_unverified until platform build/run", signals["note"])

    def test_desktop_local_repo_routes_feature_with_unverified_local_runtime_signals(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": '{"name": "fixture-desktop-local", "scripts": {"tauri:build": "tauri build"}}\n',
                    "src-tauri/tauri.conf.json": '{"productName": "Synthetic Desktop"}\n',
                    "src/main.ts": "export const app = true;\n",
                    "src/background/indexer.ts": "export const indexer = true;\n",
                    "db/app.sqlite": "synthetic sqlite placeholder\n",
                    "docs/local-data.md": "# Local data and filesystem permissions\n",
                    "docs/privacy.md": "# Privacy and retention\n",
                    "docs/recovery.md": "# Recovery path\n",
                    "reports/app.log": "synthetic desktop app log\n",
                    "reports/screenshots/desktop-home.png": "synthetic screenshot placeholder\n",
                },
            )

            result = analyze_workspace(workspace)

        usage_mode = result["usage_mode"]
        self.assertEqual(usage_mode["primary"], "desktop_local_first")
        self.assertIn("workspace has desktop or local-first runtime signals", usage_mode["reasons"])
        self.assertIn("local data risk note", usage_mode["minimum_artifacts"])
        self.assertIn("runtime log check", usage_mode["minimum_artifacts"])
        self.assertIn("desktop-local-runtime-plan", usage_mode["behavioral_eval_cases"])
        self.assertIn("desktop_local_surface", result["route_inputs"]["workspace_signals"]["active_surfaces"])

        signals = result["desktop_local_signals"]
        self.assertEqual(signals["platform_status"], "present_unverified")
        self.assertEqual(signals["filesystem_status"], "present_unverified")
        self.assertEqual(signals["local_data_status"], "present_unverified")
        self.assertEqual(signals["background_job_status"], "present_unverified")
        self.assertEqual(signals["privacy_status"], "present_unverified")
        self.assertEqual(signals["build_command_status"], "present_unverified")
        self.assertEqual(signals["runtime_log_status"], "present_unverified")
        self.assertEqual(signals["screenshot_status"], "present_unverified")
        self.assertEqual(signals["recovery_status"], "present_unverified")
        self.assertEqual(signals["verification_status"], "applicable_missing")
        self.assertIn("present_unverified until desktop build/run", signals["note"])

    def test_data_migration_repo_routes_with_unverified_database_safety_signals(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": '{"name": "fixture-data-migration", "scripts": {"migrate:dry-run": "node scripts/dry-run.js"}}\n',
                    "migrations/202605230001_add_users.sql": "alter table users add column email text;\n",
                    "migrations/202605230002_backfill_users.sql": "-- backfill users\n",
                    "db/schema.dbml": "Table users { id integer email varchar }\n",
                    "docs/pii-retention.md": "# PII and retention\n",
                    "docs/data-quality.md": "# Data quality validation\n",
                    "docs/rollback.md": "# Rollback and backup plan\n",
                    "reports/migration-dry-run.txt": "synthetic dry run result\n",
                    "reports/row-counts.csv": "table,count\nusers,10\n",
                },
            )

            result = analyze_workspace(workspace)

        usage_mode = result["usage_mode"]
        self.assertEqual(usage_mode["primary"], "data_migration")
        self.assertIn("workspace has database or migration documentation signals", usage_mode["reasons"])
        self.assertIn("migration plan", usage_mode["minimum_artifacts"])
        self.assertIn("database dictionary", usage_mode["minimum_artifacts"])
        self.assertIn("data-migration-plan", usage_mode["behavioral_eval_cases"])
        self.assertIn("data_migration_surface", result["route_inputs"]["workspace_signals"]["active_surfaces"])

        signals = result["data_migration_signals"]
        self.assertEqual(signals["schema_status"], "present_unverified")
        self.assertEqual(signals["backfill_status"], "present_unverified")
        self.assertEqual(signals["sensitive_data_status"], "present_unverified")
        self.assertEqual(signals["retention_status"], "present_unverified")
        self.assertEqual(signals["rollback_status"], "present_unverified")
        self.assertEqual(signals["validation_status"], "present_unverified")
        self.assertEqual(signals["dry_run_status"], "present_unverified")
        self.assertEqual(signals["database_dictionary_status"], "present_unverified")
        self.assertEqual(signals["verification_status"], "applicable_missing")
        self.assertIn("present_unverified until migration dry run", signals["note"])

    def test_security_sensitive_repo_routes_with_unverified_security_signals(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": '{"name": "fixture-security-sensitive"}\n',
                    "src/auth/oauth.ts": "export const authn = true;\n",
                    "src/auth/permissions.ts": "export const authz = true;\n",
                    "src/payments/checkout.ts": "export const checkout = true;\n",
                    "docs/secrets-policy.md": "# Secrets policy\n",
                    "docs/pii-handling.md": "# PII and sensitive data handling\n",
                    "docs/abuse-rate-limits.md": "# Abuse controls and rate limit\n",
                    "docs/audit-logging.md": "# Audit logging\n",
                    "docs/security-rollback.md": "# Security rollback plan\n",
                    "docs/security-approval.md": "# Owner review and approval\n",
                    "tests/authz.test.ts": "test('synthetic authz test', () => {});\n",
                },
            )

            result = analyze_workspace(workspace)

        usage_mode = result["usage_mode"]
        self.assertEqual(usage_mode["primary"], "security_sensitive_change")
        self.assertIn("workspace has auth, permission, payment or sensitive-data signals", usage_mode["reasons"])
        self.assertIn("security risk review", usage_mode["minimum_artifacts"])
        self.assertIn("approval boundary", usage_mode["minimum_artifacts"])
        self.assertIn("security-sensitive-change-plan", usage_mode["behavioral_eval_cases"])
        self.assertIn("security_sensitive_surface", result["route_inputs"]["workspace_signals"]["active_surfaces"])

        signals = result["security_sensitive_signals"]
        self.assertEqual(signals["authn_status"], "present_unverified")
        self.assertEqual(signals["authz_status"], "present_unverified")
        self.assertEqual(signals["permission_status"], "present_unverified")
        self.assertEqual(signals["payment_status"], "present_unverified")
        self.assertEqual(signals["secret_status"], "present_unverified")
        self.assertEqual(signals["sensitive_data_status"], "present_unverified")
        self.assertEqual(signals["abuse_control_status"], "present_unverified")
        self.assertEqual(signals["audit_logging_status"], "present_unverified")
        self.assertEqual(signals["test_status"], "present_unverified")
        self.assertEqual(signals["rollback_status"], "present_unverified")
        self.assertEqual(signals["approval_status"], "present_unverified")
        self.assertEqual(signals["verification_status"], "applicable_missing")
        self.assertIn("present_unverified until security tests", signals["note"])
        self.assertEqual(
            result["route_inputs"]["workspace_signals"]["security_sensitive_signals"],
            signals,
        )

    def test_extended_usage_mode_matrix_from_workspace_surfaces(self):
        cases = {
            "legacy_onboarding": (
                {
                    "legacy/service.py": "print('synthetic legacy app')\n",
                    "scripts/run.sh": "#!/bin/sh\npython legacy/service.py\n",
                },
                "onboarding map",
                "legacy_docs_debt_surface",
            ),
            "api_migration": (
                {
                    "package.json": '{"name": "fixture-api-migration"}\n',
                    "openapi/public.yaml": "openapi: 3.1.0\ninfo:\n  title: API\n  version: 2.0.0\npaths: {}\n",
                    "docs/api-migration-v2.md": "# API migration\n",
                },
                "migration plan",
                "api_contract_surface",
            ),
            "ai_eval_regression": (
                {
                    "package.json": '{"name": "fixture-rag"}\n',
                    "evals/rag-regression.json": '{"cases": []}\n',
                    "prompts/retrieval.md": "# Retrieval prompt\n",
                },
                "ai eval spec",
                "ai_eval_surface",
            ),
            "native_mobile_feature": (
                {
                    "android/settings.gradle": 'pluginManagement { repositories { google() } }\n',
                    "android/app/build.gradle": "plugins { id 'com.android.application' }\n",
                    "android/app/src/main/AndroidManifest.xml": "<manifest />\n",
                },
                "platform runtime check",
                "native_mobile_surface",
            ),
            "desktop_local_first": (
                {
                    "package.json": '{"name": "fixture-desktop"}\n',
                    "src-tauri/tauri.conf.json": '{"productName": "Synthetic Desktop"}\n',
                    "src/index.ts": "export const app = true;\n",
                },
                "runtime log check",
                "desktop_local_surface",
            ),
            "data_migration": (
                {
                    "package.json": '{"name": "fixture-data"}\n',
                    "migrations/202605230001_add_users.sql": "create table users(id integer);\n",
                    "db/schema.dbml": "Table users { id integer }\n",
                },
                "database dictionary",
                "data_migration_surface",
            ),
            "security_sensitive_change": (
                {
                    "package.json": '{"name": "fixture-security"}\n',
                    "src/auth/permissions.ts": "export const permission = 'synthetic';\n",
                    "docs/payments.md": "# Payment approval notes\n",
                },
                "security risk review",
                "security_sensitive_surface",
            ),
            "ci_stabilization": (
                {
                    "package.json": '{"name": "fixture-ci"}\n',
                    ".github/workflows/ci.yml": "name: CI\non: [push]\njobs: {}\n",
                    "ci/failure.log": "github actions job failed on ubuntu-latest\n",
                },
                "ci stabilization report",
                "ci_failure_surface",
            ),
            "release_packaging": (
                {
                    "package.json": '{"name": "fixture-release", "version": "1.0.0"}\n',
                    "CHANGELOG.md": "# Changelog\n",
                    "docs/release.md": "# Release checklist\n",
                },
                "release readiness",
                "distribution_surface",
            ),
        }

        for expected_mode, (files, expected_artifact, expected_surface) in cases.items():
            with self.subTest(expected_mode=expected_mode):
                with tempfile.TemporaryDirectory() as tmpdir:
                    workspace = Path(tmpdir)
                    self._write_files(workspace, files)

                    result = analyze_workspace(workspace)

                usage_mode = result["usage_mode"]
                self.assertEqual(usage_mode["primary"], expected_mode)
                self.assertIn(expected_artifact, usage_mode["minimum_artifacts"])
                self.assertIn(expected_surface, result["route_inputs"]["workspace_signals"]["active_surfaces"])
                self.assertFalse(result["route_inputs"]["intent_hint_present"])

    def test_behavioral_route_inputs_keep_intent_workspace_and_control_plane_separate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "AGENTS.md": "# Synthetic rules\n",
                    "package.json": '{"name": "fixture-ci"}\n',
                    ".github/workflows/ci.yml": "name: CI\non: [push]\njobs: {}\n",
                    "ci/failure.log": "github actions job failed on ubuntu-latest\n",
                },
            )

            result = analyze_workspace(workspace, intent_hint="Please stabilize the CI failure")

        self.assertEqual(result["usage_mode"]["primary"], "ci_stabilization")
        route_inputs = result["route_inputs"]
        self.assertTrue(route_inputs["intent_hint_present"])
        self.assertEqual(route_inputs["control_plane_state"]["existing_control_plane_files"], ["AGENTS.md"])
        self.assertIn("ci_failure_surface", route_inputs["workspace_signals"]["active_surfaces"])
        self.assertIn("node", route_inputs["workspace_signals"]["stack"])

    def test_ci_stabilization_repo_routes_with_unverified_ci_signals(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": '{"name": "fixture-ci"}\n',
                    ".github/workflows/ci.yml": "name: CI\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - run: npm test\n",
                    "ci/failure.log": "github actions job test failed on ubuntu-latest\n",
                    "ci/flaky-history.md": "# Flaky test history\n",
                    "ci/test-result.xml": "<testsuite failures=\"1\"></testsuite>\n",
                    "docs/ci-environment.md": "# CI environment: ubuntu-latest, node 20\n",
                    "docs/ci-local-reproduction.md": "# Local reproduction command\nnpm test\n",
                    "docs/ci-rerun-evidence.md": "# Rerun evidence pending approval\n",
                    "docs/ci-approval.md": "# Remote CI approval boundary\n",
                    "scripts/test-ci.sh": "npm test\n",
                    "tests/example.test.ts": "test('synthetic', () => {})\n",
                },
            )

            result = analyze_workspace(workspace)

        usage_mode = result["usage_mode"]
        self.assertEqual(usage_mode["primary"], "ci_stabilization")
        self.assertIn("workspace has CI failure evidence signals", usage_mode["reasons"])
        self.assertIn("ci stabilization report", usage_mode["minimum_artifacts"])
        self.assertIn("failure evidence", usage_mode["minimum_artifacts"])
        self.assertIn("ci-stabilization-plan", usage_mode["behavioral_eval_cases"])
        self.assertIn("ci_failure_surface", result["route_inputs"]["workspace_signals"]["active_surfaces"])

        signals = result["ci_stabilization_signals"]
        for key in [
            "workflow_status",
            "failure_log_status",
            "job_status",
            "command_status",
            "environment_status",
            "test_result_status",
            "flaky_status",
            "local_reproduction_status",
            "rerun_status",
            "approval_status",
        ]:
            self.assertEqual(signals[key], "present_unverified", key)
        self.assertEqual(signals["verification_status"], "applicable_missing")
        self.assertIn("present_unverified until local reproduction", signals["note"])
        self.assertEqual(
            result["route_inputs"]["workspace_signals"]["ci_stabilization_signals"],
            signals,
        )

    def test_release_packaging_repo_routes_with_unverified_release_signals(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": (
                        '{"name": "fixture-release", "version": "1.2.0", '
                        '"scripts": {"build": "npm run bundle", "test": "npm test"}}\n'
                    ),
                    "CHANGELOG.md": "# Changelog\n",
                    "docs/release.md": "# Release checklist\n",
                    "docs/release-security.md": "# Security notes\n",
                    "LICENSE": "Synthetic license placeholder\n",
                    "dist/package.tgz": "synthetic artifact placeholder\n",
                    "docs/release-rollback.md": "# Rollback plan\n",
                    "docs/publish-approval.md": "# Publish approval\n",
                    ".github/workflows/release.yml": "name: Release\njobs: {}\n",
                    "tests/release.test.ts": "test('synthetic release', () => {})\n",
                },
            )

            result = analyze_workspace(workspace)

        usage_mode = result["usage_mode"]
        self.assertEqual(usage_mode["primary"], "release_packaging")
        self.assertIn("workspace has package or release distribution signals", usage_mode["reasons"])
        self.assertIn("release readiness", usage_mode["minimum_artifacts"])
        self.assertIn("finish options", usage_mode["minimum_artifacts"])
        self.assertIn("release-packaging-readiness", usage_mode["behavioral_eval_cases"])
        self.assertIn("finish-options", usage_mode["behavioral_eval_cases"])
        self.assertIn("distribution_surface", result["route_inputs"]["workspace_signals"]["active_surfaces"])

        signals = result["release_packaging_signals"]
        for key in [
            "package_metadata_status",
            "version_status",
            "changelog_status",
            "build_status",
            "test_status",
            "docs_status",
            "security_status",
            "license_status",
            "artifact_status",
            "rollback_status",
            "approval_status",
        ]:
            self.assertEqual(signals[key], "present_unverified", key)
        self.assertEqual(signals["verification_status"], "applicable_missing")
        self.assertIn("present_unverified until release evidence", signals["note"])
        self.assertEqual(
            result["route_inputs"]["workspace_signals"]["release_packaging_signals"],
            signals,
        )

    def test_missing_workspace_raises_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            analyze_workspace(FIXTURES / "does-not-exist")

    def test_file_workspace_raises_not_a_directory(self):
        with tempfile.NamedTemporaryFile() as handle:
            with self.assertRaises(NotADirectoryError):
                analyze_workspace(handle.name)

    def test_generated_directories_are_ignored(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            (workspace / "package.json").write_text("{}", encoding="utf-8")
            ignored_files = {
                ".git/config",
                ".cache/tool/state.json",
                ".next/server/app.js",
                ".nox/unit/log.txt",
                ".tox/py312/log.txt",
                ".turbo/cache/state.json",
                "coverage/lcov.info",
                "node_modules/pkg/index.js",
                "site/index.html",
                "target/debug/app",
                "vendor/module/file.go",
            }
            for relative_file in ignored_files:
                path = workspace / relative_file
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("", encoding="utf-8")
            (workspace / "src").mkdir()
            (workspace / "src" / "app.js").write_text("", encoding="utf-8")

            result = analyze_workspace(workspace)

        self.assertIn("package.json", result["detected_files"])
        self.assertIn("src/app.js", result["detected_files"])
        for relative_file in ignored_files:
            self.assertNotIn(relative_file, result["detected_files"])

    def test_methodology_signals_are_detected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            files = {
                "package.json": "{}",
                "docs/architecture/overview.md": "# Architecture",
                "docs/adr/0001-api-contract.md": "# ADR-0001",
                "openapi/public.yaml": "openapi: 3.2.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                "asyncapi/events.yaml": "asyncapi: 3.0.0\ninfo:\n  title: Events\n  version: 1.0.0\n",
                ".storybook/main.ts": "export default {};",
                "db/schema.dbml": "Table users { id integer }",
                "docs/domain/glossary.md": "# Ubiquitous language\n",
                "docs/domain/context-map.md": "# Bounded contexts\n",
                "CODEOWNERS": "docs/** @docs-team",
                "EVALS.md": "# Evals",
                "analytics/metrics.md": "# Metrics",
            }
            for relative, text in files.items():
                path = workspace / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")

            result = analyze_workspace(workspace)

        signals = result["methodology_signals"]
        self.assertTrue(signals["architecture_docs"])
        self.assertTrue(signals["adr"])
        self.assertTrue(signals["openapi"])
        self.assertTrue(signals["asyncapi"])
        self.assertTrue(signals["storybook"])
        self.assertTrue(signals["database_docs"])
        self.assertTrue(signals["domain_model"])
        self.assertTrue(signals["codeowners"])
        self.assertTrue(signals["evals"])
        self.assertTrue(signals["metrics"])
        self.assertEqual(result["methodology_gaps"], [])

    def test_quality_testing_evals_signals_are_present_unverified(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": '{"dependencies":{"vitest":"latest","@playwright/test":"latest"}}\n',
                    "tests/test_app.py": "def test_app():\n    assert True\n",
                    "spec/cart.spec.ts": "test('cart', () => {})\n",
                    "e2e/checkout.spec.ts": "test('checkout', () => {})\n",
                    "playwright/smoke.spec.ts": "test('smoke', () => {})\n",
                    "cypress/e2e/login.cy.ts": "describe('login', () => {})\n",
                    "fixtures/user.json": "{}\n",
                    "__tests__/button.test.tsx": "test('button', () => {})\n",
                    "snapshots/home.snap": "snapshot\n",
                    ".github/workflows/ci.yml": "name: ci\n",
                    "TEST.md": "# Test plan\n",
                    "EVALS.md": "# Evals\n",
                    "RUNLOG.md": "# Runlog\n",
                    "pytest.ini": "[pytest]\n",
                    "tox.ini": "[tox]\n",
                    "vitest.config.ts": "export default {}\n",
                    "jest.config.js": "module.exports = {}\n",
                    "playwright.config.ts": "export default {}\n",
                    "coverage-summary.json": "{}\n",
                    "promptfoo.yaml": "providers: []\n",
                    "pact/consumer.json": "{}\n",
                    "openapi.yaml": "openapi: 3.1.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                    "asyncapi.yaml": "asyncapi: 3.0.0\ninfo:\n  title: Events\n  version: 1.0.0\n",
                    "docs/testing.md": (
                        "pytest unittest JUnit Jest Vitest Playwright Testing Library Storybook Pact "
                        "Stryker Hypothesis Promptfoo Ragas Codecov GitHub Actions flaky retry\n"
                    ),
                },
            )

            result = analyze_workspace(workspace)

        signals = result["methodology_signals"]
        self.assertTrue(signals["quality_testing_evals"])
        self.assertIn(
            "quality_testing_evals",
            result["route_inputs"]["workspace_signals"]["methodology_signals"],
        )
        applicability = result["methodology_applicability"]["test_eval_first_evidence"]
        self.assertEqual(applicability["status"], "present_unverified")
        self.assertNotEqual(applicability["status"], "present_verified")
        self.assertIn("detection alone does not prove quality evidence", applicability["residual_risk"])

    def test_codex_agentic_workflow_signals_are_present_unverified(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "AGENTS.md": "# Agents\n",
                    ".codex/config.toml": "model = 'gpt-5'\n",
                    ".codex/agents/builder.toml": "name = 'builder'\n",
                    ".codex/workflows/build-slice.md": "# Build slice\n",
                    ".codex/artifact-templates/agent-task-packet.md": "# Task packet\n",
                    ".agents/skills/review/SKILL.md": "# Skill\n",
                    ".agents/plugins/demo/.codex-plugin/plugin.json": '{"name":"demo"}\n',
                    ".mcp.json": '{"servers":{"docs":{"command":"node"}}}\n',
                    "hooks.json": '{"hooks":{"PreToolUse":[]}}\n',
                    "automation.toml": "name = 'candidate'\n",
                    "docs/playbooks/use-case-to-plugin.md": "# Plugin playbook\n",
                    "docs/runtime/codex.md": (
                        "Codex App CLI IDE extension subagents skills MCP hooks plugin automation "
                        "approval boundary external write worktree handoff eval evidence\n"
                    ),
                },
            )

            result = analyze_workspace(workspace)

        signals = result["methodology_signals"]
        self.assertTrue(signals["codex_agentic_workflow"])
        self.assertIn(
            "codex_agentic_workflow",
            result["route_inputs"]["workspace_signals"]["methodology_signals"],
        )
        applicability = result["methodology_applicability"]["codex_agentic_workflow"]
        self.assertEqual(applicability["status"], "present_unverified")
        self.assertIn("Codex workflow signal exists", applicability["reason"])
        self.assertIn("detection alone does not prove safe activation", applicability["residual_risk"])

    def test_frontend_methodology_signals_are_present_unverified(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": (
                        '{"dependencies":{"react":"latest","@storybook/react":"latest",'
                        '"@playwright/test":"latest","@testing-library/react":"latest","axe-core":"latest"}}\n'
                    ),
                    "vite.config.ts": "export default {};\n",
                    "components.json": "{}\n",
                    "tokens/colors.json": "{}\n",
                    "src/pages/home/HomePage.tsx": "export const HomePage = () => null;\n",
                    "src/widgets/header/Header.tsx": "export const Header = () => null;\n",
                    "src/features/search/SearchBox.tsx": "export const SearchBox = () => null;\n",
                    "src/shared/ui/Button.stories.tsx": "export default {};\n",
                    ".storybook/main.ts": "export default {};\n",
                    "playwright.config.ts": "export default {};\n",
                    "docs/frontend-qa.md": (
                        "Synthetic frontend route component Storybook visual regression screenshot "
                        "viewport accessibility WCAG keyboard focus responsive Core Web Vitals LCP INP CLS\n"
                    ),
                },
            )

            result = analyze_workspace(workspace)

        signals = result["methodology_signals"]
        self.assertTrue(signals["frontend"])
        self.assertIn(
            "frontend",
            result["route_inputs"]["workspace_signals"]["methodology_signals"],
        )
        applicability = result["methodology_applicability"]["frontend_methodology"]
        self.assertEqual(applicability["status"], "present_unverified")
        self.assertIn("frontend signal exists", applicability["reason"])
        self.assertIn("browser/runtime evidence", applicability["required_evidence"])
        self.assertIn("detection alone does not prove UI completion", applicability["residual_risk"])

    def test_backend_methodology_signals_are_present_unverified(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "pyproject.toml": "[project]\nname = 'orders-api'\n",
                    "requirements.txt": "fastapi\ncelery\nredis\npsycopg\n",
                    "server/app.py": "def app():\n    return None\n",
                    "services/orders/service.py": "def handle():\n    return None\n",
                    "workers/email_worker.py": "def run():\n    return None\n",
                    "jobs/nightly.py": "def run():\n    return None\n",
                    "queues/orders.py": "QUEUE = 'orders'\n",
                    "adapters/payment_client.py": "class PaymentClient:\n    pass\n",
                    "repositories/order_repository.py": "class OrderRepository:\n    pass\n",
                    "migrations/001_init.sql": "create table orders(id text);\n",
                    "Dockerfile": "FROM python:3.12\n",
                    "docker-compose.yml": "services: {}\n",
                    "k8s/deployment.yaml": "apiVersion: apps/v1\n",
                    "openapi.yaml": "openapi: 3.1.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                    "asyncapi.yaml": "asyncapi: 3.0.0\ninfo:\n  title: Events\n  version: 1.0.0\n",
                    "proto/orders.proto": "syntax = 'proto3';\n",
                    "docs/backend-runtime.md": (
                        "retry timeout idempotency circuit breaker health check readiness liveness "
                        "SLO runbook observability traces metrics logs correlation\n"
                    ),
                },
            )

            result = analyze_workspace(workspace)

        signals = result["methodology_signals"]
        self.assertTrue(signals["backend"])
        self.assertIn(
            "backend",
            result["route_inputs"]["workspace_signals"]["methodology_signals"],
        )
        applicability = result["methodology_applicability"]["backend_methodology"]
        self.assertEqual(applicability["status"], "present_unverified")
        self.assertIn("backend signal exists", applicability["reason"])
        self.assertIn("backend-service-overview.md", applicability["required_evidence"])
        self.assertIn("runtime/failure evidence", applicability["required_evidence"])
        self.assertIn("detection alone does not prove backend runtime safety", applicability["residual_risk"])

    def test_backend_dependency_signals_distinguish_categories_as_present_unverified(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "requirements.txt": "psycopg\nredis\nkafka-python\nstripe\nboto3\nelasticsearch\nhttpx\n",
                    "server/app.py": "def app():\n    return None\n",
                    "repositories/order_repository.py": "class OrderRepository:\n    pass\n",
                    "queues/order_consumer.py": "QUEUE = 'orders'\n",
                    "cache/redis_client.py": "class RedisClient:\n    pass\n",
                    "adapters/payment_client.py": "class PaymentClient:\n    pass\n",
                    "adapters/email_sender.py": "class EmailSender:\n    pass\n",
                    "storage/blob_store.py": "class BlobStore:\n    pass\n",
                    "search/index_client.py": "class SearchClient:\n    pass\n",
                    "integrations/provider_client.py": "class ProviderClient:\n    pass\n",
                },
            )

            result = analyze_workspace(workspace)

        self.assertIn("backend_dependency_signals", result)
        dependencies = result["backend_dependency_signals"]
        expected = {
            "database": "repositories/order_repository.py",
            "message_broker": "queues/order_consumer.py",
            "cache": "cache/redis_client.py",
            "payment": "adapters/payment_client.py",
            "email": "adapters/email_sender.py",
            "storage": "storage/blob_store.py",
            "search": "search/index_client.py",
            "third_party_http_provider": "integrations/provider_client.py",
        }
        for category, source in expected.items():
            with self.subTest(category=category):
                packet = dependencies[category]
                self.assertEqual(packet["status"], "present_unverified")
                self.assertIn(source, packet["sources"])
        self.assertIn("present_unverified until owner review", dependencies["note"])

    def test_backend_delivery_signals_record_commands_ci_deploy_without_execution(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "pyproject.toml": "[project]\nname = 'orders-api'\n",
                    "server/app.py": "def app():\n    return None\n",
                    "workers/order_worker.py": "def run():\n    return None\n",
                    "queues/orders.py": "QUEUE = 'orders'\n",
                    "db/schema.sql": "create table orders(id text);\n",
                    "openapi/orders.yaml": "openapi: 3.2.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                    "scripts/start-api.sh": "#!/bin/sh\npython -m server.app\n",
                    ".github/workflows/deploy.yml": "name: deploy\n",
                    "Dockerfile": "FROM python:3.12\n",
                    "k8s/deployment.yaml": "apiVersion: apps/v1\nkind: Deployment\n",
                    "security/authz.py": "def authorize():\n    return True\n",
                },
            )

            result = analyze_workspace(workspace)

        self.assertIn("backend_delivery_signals", result)
        delivery = result["backend_delivery_signals"]
        expected_sources = {
            "backend_stack": "pyproject.toml",
            "commands": "scripts/start-api.sh",
            "ci": ".github/workflows/deploy.yml",
            "api_contracts": "openapi/orders.yaml",
            "database": "db/schema.sql",
            "queues": "queues/orders.py",
            "workers": "workers/order_worker.py",
            "deployment_manifests": "Dockerfile",
            "security": "security/authz.py",
        }
        for category, source in expected_sources.items():
            with self.subTest(category=category):
                packet = delivery[category]
                self.assertEqual(packet["status"], "present_unverified")
                self.assertIn(source, packet["sources"])
        self.assertIn("without executing deployments", delivery["note"])
        self.assertIn("external writes", delivery["note"])
        self.assertIn("approval_required", delivery["note"])
        self.assertIn(
            "backend_delivery_signals",
            result["route_inputs"]["workspace_signals"],
        )

    def test_backend_resilience_signals_are_lightweight_present_unverified(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "server/app.py": "def app():\n    return None\n",
                    "services/retry_policy.py": "MAX_ATTEMPTS = 3\n",
                    "services/idempotency_keys.py": "KEY = 'synthetic'\n",
                    "jobs/order_retry_worker.py": "def run():\n    return None\n",
                    "integrations/payment_provider_client.py": "class Client:\n    pass\n",
                },
            )

            result = analyze_workspace(workspace)

        self.assertIn("backend_resilience_signals", result)
        resilience = result["backend_resilience_signals"]
        self.assertEqual(resilience["retry_idempotency_terms"]["status"], "present_unverified")
        self.assertIn("services/retry_policy.py", resilience["retry_idempotency_terms"]["sources"])
        self.assertIn("services/idempotency_keys.py", resilience["retry_idempotency_terms"]["sources"])
        self.assertEqual(resilience["job_context"]["status"], "present_unverified")
        self.assertIn("jobs/order_retry_worker.py", resilience["job_context"]["sources"])
        self.assertEqual(resilience["dependency_context"]["status"], "present_unverified")
        self.assertIn("integrations/payment_provider_client.py", resilience["dependency_context"]["sources"])
        self.assertIn("lightweight read-only signals", resilience["note"])
        self.assertIn("deeper static analysis deferred", resilience["note"])
        self.assertIn("avoid false positives", resilience["note"])
        self.assertIn(
            "backend_resilience_signals",
            result["route_inputs"]["workspace_signals"],
        )

    def test_backend_service_fixture_routes_backend_methodology(self):
        workspace = FIXTURES / "backend-service-app"

        result = analyze_workspace(workspace)

        self.assertTrue(result["methodology_signals"]["backend"])
        dependencies = result["backend_dependency_signals"]
        for category in [
            "database",
            "message_broker",
            "cache",
            "payment",
            "email",
            "storage",
            "search",
            "third_party_http_provider",
        ]:
            with self.subTest(category=category):
                self.assertEqual(dependencies[category]["status"], "present_unverified")
        self.assertIn(
            "backend",
            result["route_inputs"]["workspace_signals"]["methodology_signals"],
        )
        applicability = result["methodology_applicability"]["backend_methodology"]
        self.assertEqual(applicability["status"], "present_unverified")
        for expected in [
            "backend-service-overview.md",
            "backend-runtime-behavior.md",
            "runtime/failure evidence",
            "observability/SLO/health evidence or accepted explicit gap",
        ]:
            self.assertIn(expected, applicability["required_evidence"])

    def test_methodology_applicability_reports_status_packets(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": "{}",
                    "docs/architecture/overview.md": "# Architecture",
                    "EVALS.md": "# Evals",
                    "CODEOWNERS": "docs/** @docs-team",
                    "analytics/metrics.md": "# Metrics",
                },
            )

            result = analyze_workspace(workspace)

        applicability = result["methodology_applicability"]
        expected_keys = {
            "architecture_boundary",
            "test_eval_first_evidence",
            "docs_as_code_ownership",
            "product_measurement",
            "domain_model_when_complex_domain",
            "fsd_structure_when_ui_architecture_applies",
            "frontend_methodology",
            "backend_methodology",
            "docs_tooling_decision",
            "standards_trigger_policy",
            "codex_agentic_workflow",
        }
        self.assertEqual(set(applicability), expected_keys)
        for gate, packet in applicability.items():
            with self.subTest(gate=gate):
                self.assertEqual(
                    set(packet),
                    {
                        "status",
                        "applies_when",
                        "reason",
                        "evidence",
                        "required_evidence",
                        "owner",
                        "residual_risk",
                    },
                )
                self.assertIsInstance(packet["evidence"], list)
                self.assertIsInstance(packet["required_evidence"], list)
                self.assertIn(
                    packet["status"],
                    {
                        "not_applicable",
                        "applicable_missing",
                        "present_unverified",
                        "present_verified",
                        "proposal_staged",
                        "explicit_gap_accepted",
                        "approval_required",
                    },
                )
        self.assertEqual(applicability["architecture_boundary"]["status"], "present_unverified")
        self.assertEqual(applicability["test_eval_first_evidence"]["status"], "present_unverified")
        self.assertEqual(applicability["docs_as_code_ownership"]["status"], "present_unverified")
        self.assertEqual(applicability["product_measurement"]["status"], "present_unverified")
        self.assertEqual(applicability["domain_model_when_complex_domain"]["status"], "not_applicable")

    def test_methodology_applicability_reports_status_transitions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "packages/orders/package.json": "{}",
                    "packages/billing/package.json": "{}",
                    "packages/orders/src/workflow.ts": "export const workflow = true;\n",
                    "src/pages/orders/ui/OrdersPage.tsx": "export const OrdersPage = () => null;\n",
                    "src/widgets/order-list/ui/OrderList.tsx": "export const OrderList = () => null;\n",
                    "src/features/orders/model/orders.ts": "export const orders = [];\n",
                    "src/entities/order/model/order.ts": "export const order = {};\n",
                    "src/shared/ui/Button.tsx": "export const Button = () => null;\n",
                    ".readthedocs.yaml": "version: 2\n",
                    "schemaspy.properties": "schemaspy.t=pgsql\n",
                    "openapi/public.yaml": "openapi: 3.2.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                },
            )

            result = analyze_workspace(workspace)

        applicability = result["methodology_applicability"]
        self.assertEqual(
            applicability["domain_model_when_complex_domain"]["status"],
            "applicable_missing",
        )
        self.assertEqual(
            applicability["fsd_structure_when_ui_architecture_applies"]["status"],
            "present_unverified",
        )
        self.assertEqual(applicability["docs_tooling_decision"]["status"], "approval_required")
        self.assertEqual(applicability["standards_trigger_policy"]["status"], "present_unverified")
        self.assertIn(
            "missing domain model for complex domain",
            applicability["domain_model_when_complex_domain"]["reason"],
        )

    def test_fsd_structure_signal_detects_frontend_layer_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": '{"dependencies":{"@vitejs/plugin-react":"latest"}}',
                    "src/app/providers/index.tsx": "export const AppProviders = () => null;\n",
                    "src/pages/home/ui/HomePage.tsx": "export const HomePage = () => null;\n",
                    "src/widgets/header/ui/Header.tsx": "export const Header = () => null;\n",
                    "src/features/auth/model/session.ts": "export const session = {};\n",
                    "src/entities/user/model/user.ts": "export const user = {};\n",
                    "src/shared/ui/Button.tsx": "export const Button = () => null;\n",
                },
            )

            result = analyze_workspace(workspace)

        self.assertTrue(result["methodology_signals"]["fsd_structure"])
        self.assertIn(
            "fsd_structure",
            result["route_inputs"]["workspace_signals"]["methodology_signals"],
        )

    def test_fsd_structure_signal_avoids_backend_native_and_simple_false_positives(self):
        cases = {
            "backend_named_folders": {
                "pyproject.toml": "[project]\nname = 'api'\n",
                "app/features/reporting.py": "def run():\n    return None\n",
                "app/entities/user.py": "class User:\n    pass\n",
                "app/shared/database.py": "DATABASE_URL = 'sqlite://'\n",
            },
            "native_flow_modules": {
                "package.json": '{"dependencies":{"react-native":"latest"}}',
                "android/app/build.gradle": "plugins {}\n",
                "ios/AppDelegate.swift": "import UIKit\n",
                "src/features/profile/ProfileScreen.tsx": "export const ProfileScreen = () => null;\n",
                "src/shared/ui/Button.tsx": "export const Button = () => null;\n",
            },
            "simple_crud_frontend": {
                "package.json": '{"dependencies":{"react":"latest"}}',
                "src/app.tsx": "export const App = () => null;\n",
                "src/pages/users.tsx": "export const UsersPage = () => null;\n",
                "src/shared/api.ts": "export const api = {};\n",
            },
        }

        for name, files in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmpdir:
                workspace = Path(tmpdir)
                self._write_files(workspace, files)

                result = analyze_workspace(workspace)

                self.assertFalse(result["methodology_signals"]["fsd_structure"])
                self.assertNotIn(
                    "fsd_structure",
                    result["route_inputs"]["workspace_signals"]["methodology_signals"],
                )

    def test_domain_model_gate_is_required_for_complex_domain_workspaces(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "packages/orders/package.json": "{}",
                    "packages/billing/package.json": "{}",
                    "packages/orders/src/workflow.ts": "export const workflow = true;\n",
                    "docs/architecture/overview.md": "# Architecture\n",
                    "EVALS.md": "# Evals\n",
                    ".github/workflows/ci.yml": "name: ci\n",
                    "analytics/metrics.md": "# Metrics\n",
                },
            )

            result = analyze_workspace(workspace)

        self.assertEqual(result["complexity_profile"]["name"], "production-team")
        self.assertFalse(result["methodology_signals"]["domain_model"])
        self.assertIn("missing domain model for complex domain", result["methodology_gaps"])

    def test_domain_model_signal_detects_context_map_in_architecture_docs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": "{}",
                    "docs/architecture/context-map.md": "# Bounded context map\n",
                    "docs/architecture/overview.md": "# Architecture\n",
                },
            )

            result = analyze_workspace(workspace)

        self.assertTrue(result["methodology_signals"]["architecture_docs"])
        self.assertTrue(result["methodology_signals"]["domain_model"])

    def test_domain_model_signal_does_not_treat_plain_domain_folder_as_ddd_proof(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": "{}",
                    "src/domain/order.ts": "export const order = true;\n",
                    "src/domain/customer.ts": "export const customer = true;\n",
                },
            )

            result = analyze_workspace(workspace)

        self.assertFalse(result["methodology_signals"]["domain_model"])
        self.assertNotIn("missing domain model for complex domain", result["methodology_gaps"])

    def test_missing_methodology_signals_are_reported_as_gaps(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            (workspace / "package.json").write_text("{}", encoding="utf-8")

            result = analyze_workspace(workspace)

        self.assertFalse(result["methodology_signals"]["architecture_docs"])
        self.assertIn("missing architecture documentation signals", result["methodology_gaps"])
        self.assertIn("missing test or eval signals", result["methodology_gaps"])
        self.assertIn("missing docs-as-code ownership or CI signals", result["methodology_gaps"])

    def test_docs_tooling_decision_detects_existing_stack_tools(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "mkdocs.yml": "site_name: Docs\n",
                    "docs/index.md": "# Docs\n",
                    "package.json": '{"scripts":{"build-storybook":"storybook build"}}\n',
                    ".storybook/main.ts": "export default {};\n",
                    "src/Button.stories.tsx": "export default {};\n",
                    "openapi/public.yaml": "openapi: 3.1.0\ninfo:\n  title: API\n  version: '1.0'\n",
                    "schema.dbml": "Table users { id integer }\n",
                },
            )

            result = analyze_workspace(workspace)

        decision = result["docs_tooling_decision"]
        self.assertEqual(decision["docs_as_code_impact"]["status"], "present_unverified")
        self.assertIn("MkDocs", decision["selected_tools"])
        self.assertIn("Storybook", decision["selected_tools"])
        self.assertIn("OpenAPI tooling", decision["selected_tools"])
        self.assertIn("DBML/dbdocs", decision["selected_tools"])
        self.assertIn("mkdocs build --strict", decision["commands"])
        self.assertIn("npm run build-storybook", decision["commands"])
        self.assertEqual(decision["tool_statuses"]["docs_portal"]["status"], "present_unverified")
        self.assertEqual(decision["tool_statuses"]["ui_component_docs"]["status"], "present_unverified")
        self.assertEqual(decision["tool_statuses"]["api_docs"]["status"], "present_unverified")
        self.assertEqual(decision["tool_statuses"]["database_docs"]["status"], "present_unverified")
        self.assertIn(
            "docs_tooling_decision",
            result["route_inputs"]["workspace_signals"]["methodology_signals"],
        )

    def test_docs_tooling_decision_routes_architecture_diagram_tools(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "docs/architecture.md": "```mermaid\nflowchart LR\n  A --> B\n```\n",
                    "architecture/workspace.dsl": "workspace { model { } views { } }\n",
                    "diagrams/checkout.puml": "@startuml\nA -> B\n@enduml\n",
                },
            )

            result = analyze_workspace(workspace)

        decision = result["docs_tooling_decision"]
        self.assertEqual(decision["tool_statuses"]["architecture_diagrams"]["status"], "present_unverified")
        self.assertIn("Mermaid", decision["selected_tools"])
        self.assertIn("Structurizr DSL", decision["selected_tools"])
        self.assertIn("PlantUML", decision["selected_tools"])
        self.assertIn("docs build/render check", decision["commands"])
        self.assertIn("structurizr validate", decision["commands"])
        self.assertIn("plantuml", decision["commands"])

    def test_docs_tooling_decision_avoids_heavy_portal_for_docs_light_project(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": "{}\n",
                    "src/index.ts": "export const ok = true;\n",
                },
            )

            result = analyze_workspace(workspace)

        decision = result["docs_tooling_decision"]
        self.assertEqual(decision["docs_as_code_impact"]["status"], "not_applicable")
        self.assertEqual(decision["tool_statuses"]["docs_portal"]["status"], "not_applicable")
        self.assertNotIn("MkDocs", decision["selected_tools"])
        self.assertNotIn("Docusaurus", decision["selected_tools"])
        self.assertNotIn("Sphinx", decision["selected_tools"])
        self.assertNotIn("Antora", decision["selected_tools"])
        self.assertEqual(decision["approval_required"], [])

    def test_docs_tooling_decision_marks_external_docs_actions_as_approval_required(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    ".readthedocs.yaml": "version: 2\n",
                    "docs/conf.py": "project = 'Example'\n",
                    "schemaspy.properties": "schemaspy.t=pgsql\n",
                },
            )

            result = analyze_workspace(workspace)

        decision = result["docs_tooling_decision"]
        self.assertIn("hosted docs", decision["approval_required"])
        self.assertIn("db introspection", decision["approval_required"])
        self.assertEqual(decision["tool_statuses"]["hosted_docs"]["status"], "approval_required")
        self.assertEqual(decision["tool_statuses"]["db_introspection"]["status"], "approval_required")

    def _write_files(self, workspace: Path, files: dict[str, str]) -> None:
        for relative, text in files.items():
            path = workspace / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
