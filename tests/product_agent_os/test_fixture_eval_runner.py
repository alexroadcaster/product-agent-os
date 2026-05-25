import importlib.util
import io
import json
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = ROOT / "plugins" / "product-agent-os" / "scripts" / "run_fixture_eval.py"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"


def load_runner():
    spec = importlib.util.spec_from_file_location("run_fixture_eval", RUNNER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FixtureEvalRunnerTest(unittest.TestCase):
    def test_fixture_eval_returns_stable_named_results(self):
        runner = load_runner()

        results = runner.evaluate_all()

        names = [item["fixture"] for item in results]
        self.assertEqual(names, sorted(names))
        self.assertIn("node-app", names)
        for item in results:
            with self.subTest(fixture=item["fixture"]):
                self.assertEqual(
                    list(item.keys()),
                    [
                        "fixture",
                        "ok",
                        "profile",
                        "risks",
                        "renderer_status",
                        "merge_status",
                        "source_policy_status",
                        "automation_status",
                        "rollback_status",
                        "failure_log_regression_status",
                        "codex_runtime_runner_status",
                        "codex_runtime_runner_checks",
                        "methodology_domains",
                        "renderer_file_count",
                        "renderer_actions",
                        "expected_checks",
                        "evidence",
                    ],
                )
                self.assertIsInstance(item["ok"], bool)
                self.assertIsInstance(item["profile"], str)
                self.assertIsInstance(item["risks"], list)
                self.assertIsInstance(item["renderer_status"], str)
                self.assertIsInstance(item["merge_status"], str)
                self.assertIsInstance(item["source_policy_status"], str)
                self.assertIsInstance(item["automation_status"], str)
                self.assertIsInstance(item["rollback_status"], str)
                self.assertIsInstance(item["failure_log_regression_status"], str)
                self.assertIsInstance(item["codex_runtime_runner_status"], str)
                self.assertIsInstance(item["codex_runtime_runner_checks"], dict)
                self.assertIsInstance(item["methodology_domains"], list)
                self.assertIsInstance(item["renderer_file_count"], int)
                self.assertIsInstance(item["renderer_actions"], dict)
                self.assertIsInstance(item["expected_checks"], dict)
                self.assertIsInstance(item["evidence"], dict)

    def test_fixture_eval_checks_expected_renderer_behavior_by_fixture(self):
        runner = load_runner()

        results = {item["fixture"]: item for item in runner.evaluate_all()}

        self.assertTrue(results["existing-codex-config"]["expected_checks"]["config_leave_unchanged"])
        self.assertTrue(results["existing-codex-config"]["expected_checks"]["agents_md_leave_unchanged"])
        self.assertTrue(results["duplicate-managed-section"]["expected_checks"]["duplicate_markers_blocked"])
        self.assertTrue(results["monorepo"]["expected_checks"]["worktree_ownership_warning"])
        self.assertTrue(results["docs-source-conflict"]["expected_checks"]["source_registry_warning"])
        self.assertTrue(results["failed-verification"]["expected_checks"]["failed_verification_warning"])
        self.assertTrue(results["unsafe-write-request"]["expected_checks"]["config_leave_unchanged"])
        self.assertTrue(results["empty-repo"]["expected_checks"]["usage_mode_greenfield_idea"])
        self.assertTrue(results["failed-verification"]["expected_checks"]["usage_mode_bug_rescue"])
        self.assertTrue(results["monorepo"]["expected_checks"]["usage_mode_complex_system_acceleration"])
        self.assertTrue(results["docs-repo"]["expected_checks"]["usage_mode_docs_only"])
        self.assertTrue(results["node-app"]["expected_checks"]["usage_mode_standard_feature"])
        self.assertTrue(results["python-app"]["expected_checks"]["plan_quality_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["acceptance_scenarios_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["domain_model_gate_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["bounded_context_trace_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["ubiquitous_language_traceability_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["metric_hardening_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["completion_evidence_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["docs_tooling_selector_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["conditional_readiness_gates_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["transcript_session_eval_runner_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["standards_trigger_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["methodology_applicability_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["business_product_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["requirements_domain_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["solution_architecture_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["quality_testing_evals_contract_present"])
        self.assertTrue(results["python-app"]["expected_checks"]["codex_agentic_workflow_contract_present"])
        self.assertEqual(results["python-app"]["renderer_file_count"], 102)
        for check_name in [
            "methodology_catalog_contract_present",
            "methodology_intelligence_contract_present",
            "methodology_recommendations_prioritized",
            "methodology_audit_read_only",
        ]:
            with self.subTest(check_name=check_name):
                self.assertTrue(results["python-app"]["expected_checks"][check_name])
        expected_modes = {
            "legacy-undocumented-repo": "legacy_onboarding",
            "api-migration-repo": "api_migration",
            "rag-quality-regression": "ai_eval_regression",
            "native-mobile-permissions": "native_mobile_feature",
            "desktop-local-indexer": "desktop_local_first",
            "data-migration-pii": "data_migration",
            "security-auth-payment": "security_sensitive_change",
            "ci-flaky-tests": "ci_stabilization",
            "package-release": "release_packaging",
        }
        for fixture, mode in expected_modes.items():
            with self.subTest(fixture=fixture):
                self.assertIn(fixture, results)
                self.assertTrue(results[fixture]["expected_checks"][f"usage_mode_{mode}"])

    def test_fixture_eval_reports_applicable_methodology_domains_for_core_fixtures(self):
        runner = load_runner()

        results = {item["fixture"]: item for item in runner.evaluate_all()}

        for fixture in [
            "node-app",
            "python-app",
            "docs-repo",
            "api-migration-repo",
            "data-migration-pii",
            "rag-quality-regression",
            "security-auth-payment",
            "package-release",
        ]:
            with self.subTest(fixture=fixture):
                self.assertIn(fixture, results)
                self.assertGreaterEqual(len(results[fixture]["methodology_domains"]), 1)

    def test_fixture_eval_checks_false_positive_scenario_gates(self):
        runner = load_runner()

        results = {item["fixture"]: item for item in runner.evaluate_all()}

        expected_checks = {
            "backend-no-fsd": "fsd_structure_not_detected_for_backend",
            "native-no-fsd": "fsd_structure_not_detected_for_native",
            "simple-crud-no-ddd": "domain_model_not_forced_for_simple_crud",
            "docs-light-no-portal": "docs_light_does_not_select_heavy_portal",
            "hosted-docs-approval": "hosted_docs_and_db_introspection_require_approval",
        }
        for fixture, check_name in expected_checks.items():
            with self.subTest(fixture=fixture):
                self.assertIn(fixture, results)
                self.assertTrue(results[fixture]["expected_checks"][check_name])
                self.assertTrue(results[fixture]["ok"])

    def test_fixture_eval_includes_track_four_statuses(self):
        runner = load_runner()

        result = runner.evaluate_fixture(FIXTURES / "automation-candidate-valid")

        self.assertIn("merge_status", result)
        self.assertIn("source_policy_status", result)
        self.assertIn("automation_status", result)
        self.assertIn("rollback_status", result)
        self.assertIn("failure_log_regression_status", result)
        self.assertIn("evidence", result)

    def test_fixture_eval_checks_automation_candidate_behavior(self):
        runner = load_runner()

        results = {item["fixture"]: item for item in runner.evaluate_all()}

        self.assertEqual(results["automation-candidate-valid"]["automation_status"], "ready_for_manual_approval")
        self.assertEqual(results["automation-candidate-invalid"]["automation_status"], "blocked")
        self.assertTrue(results["failure-log-regression"]["expected_checks"]["failure_log_regression_visible"])

    def test_fixture_eval_encodes_expected_track_four_statuses(self):
        runner = load_runner()

        results = {item["fixture"]: item for item in runner.evaluate_all()}

        self.assertTrue(
            results["automation-candidate-valid"]["expected_checks"][
                "automation_status_ready_for_manual_approval"
            ]
        )
        self.assertTrue(results["automation-candidate-valid"]["ok"])
        self.assertTrue(results["automation-candidate-invalid"]["expected_checks"]["automation_status_blocked"])
        self.assertTrue(results["automation-candidate-invalid"]["ok"])
        self.assertTrue(results["source-policy-conflict"]["expected_checks"]["source_policy_status_needs_review"])
        self.assertTrue(results["failure-log-regression"]["expected_checks"]["failure_log_regression_status_ready"])
        self.assertTrue(results["rollback-required"]["expected_checks"]["rollback_status_required"])
        self.assertTrue(results["stale-merge-plan"]["expected_checks"]["stale_digest_blocked"])
        self.assertTrue(results["path-traversal-stage"]["expected_checks"]["path_traversal_blocked"])
        self.assertTrue(results["symlink-escape"]["expected_checks"]["symlink_escape_blocked"])
        self.assertTrue(results["hook-activation-unapproved"]["expected_checks"]["hooks_unapproved_companion_only"])
        self.assertTrue(results["hook-activation-approved"]["expected_checks"]["hooks_approved_apply"])
        self.assertTrue(results["hook-activation-approved"]["expected_checks"]["rollback_manifest_visible"])
        self.assertIn("build_merge_plan", results["stale-merge-plan"]["evidence"]["commands"])
        self.assertIn("apply_merge_plan", results["hook-activation-approved"]["evidence"]["commands"])

    def test_fixture_eval_fails_when_expected_track_four_status_regresses(self):
        runner = load_runner()
        original_validator = runner.validate_automation_candidate

        try:
            runner.validate_automation_candidate = lambda candidate: {"status": "candidate_only"}
            result = runner.evaluate_fixture(FIXTURES / "automation-candidate-invalid")
        finally:
            runner.validate_automation_candidate = original_validator

        self.assertEqual(result["automation_status"], "candidate_only")
        self.assertFalse(result["expected_checks"]["automation_status_blocked"])
        self.assertFalse(result["ok"])

    def test_cli_prints_json_and_exits_zero_when_all_fixtures_are_ok(self):
        result = subprocess.run(
            [sys.executable, str(RUNNER_PATH)],
            check=False,
            capture_output=True,
            text=True,
        )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertTrue(all(item["ok"] for item in payload))
        self.assertIn("node-app", {item["fixture"] for item in payload})

    def test_missing_fixture_root_returns_failed_json_shape(self):
        runner = load_runner()

        missing_root = ROOT / "does-not-exist-fixtures"
        results = runner.evaluate_all(missing_root)

        self.assertEqual(
            results,
            [
                {
                    "fixture": "does-not-exist-fixtures",
                    "ok": False,
                    "profile": "",
                    "risks": [f"fixture directory does not exist: {missing_root}"],
                    "renderer_status": "",
                    "merge_status": "",
                    "source_policy_status": "",
                    "automation_status": "",
                    "rollback_status": "",
                    "failure_log_regression_status": "",
                    "codex_runtime_runner_status": "",
                    "codex_runtime_runner_checks": {},
                    "methodology_domains": [],
                    "renderer_file_count": 0,
                    "renderer_actions": {},
                    "expected_checks": {},
                    "evidence": {},
                }
            ],
        )

    def test_discovery_exception_returns_failed_result_without_traceback(self):
        runner = load_runner()

        def fail_discovery(path):
            raise RuntimeError("synthetic discovery failure")

        runner.analyze_workspace = fail_discovery
        with TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "broken-fixture"
            fixture.mkdir()

            result = runner.evaluate_fixture(fixture)

        self.assertEqual(
            result,
            {
                "fixture": "broken-fixture",
                "ok": False,
                "profile": "",
                "risks": ["discovery failed: RuntimeError: synthetic discovery failure"],
                "renderer_status": "",
                "merge_status": "",
                "source_policy_status": "",
                "automation_status": "",
                "rollback_status": "",
                "failure_log_regression_status": "",
                "codex_runtime_runner_status": "",
                "codex_runtime_runner_checks": {},
                "methodology_domains": [],
                "renderer_file_count": 0,
                "renderer_actions": {},
                "expected_checks": {},
                "evidence": {},
            },
        )

    def test_main_exits_one_when_any_result_fails(self):
        runner = load_runner()
        runner.evaluate_all = lambda: [
            {
                "fixture": "ok-fixture",
                "ok": True,
                "profile": "simple",
                "risks": [],
                "renderer_status": "needs_approval",
                "merge_status": "not_exercised",
                "source_policy_status": "ok",
                "automation_status": "not_applicable",
                "rollback_status": "not_exercised",
                "failure_log_regression_status": "not_applicable",
                "codex_runtime_runner_status": "not_applicable",
                "codex_runtime_runner_checks": {},
                "methodology_domains": [],
                "renderer_file_count": 34,
                "renderer_actions": {},
                "expected_checks": {},
                "evidence": {},
            },
            {
                "fixture": "bad-fixture",
                "ok": False,
                "profile": "",
                "risks": ["discovery failed: RuntimeError: synthetic discovery failure"],
                "renderer_status": "",
                "merge_status": "",
                "source_policy_status": "",
                "automation_status": "",
                "rollback_status": "",
                "failure_log_regression_status": "",
                "codex_runtime_runner_status": "",
                "codex_runtime_runner_checks": {},
                "methodology_domains": [],
                "renderer_file_count": 0,
                "renderer_actions": {},
                "expected_checks": {},
                "evidence": {},
            },
        ]

        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = runner.main()

        payload = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 1)
        self.assertEqual(payload[1]["fixture"], "bad-fixture")
        self.assertFalse(payload[1]["ok"])


if __name__ == "__main__":
    unittest.main()
