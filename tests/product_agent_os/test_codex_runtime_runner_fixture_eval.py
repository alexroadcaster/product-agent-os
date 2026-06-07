import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = ROOT / "plugins" / "product-agent-os" / "scripts" / "run_fixture_eval.py"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
_EVALUATE_ALL_CACHE = None


def load_runner():
    spec = importlib.util.spec_from_file_location("run_fixture_eval", RUNNER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def evaluate_all_cached(runner):
    global _EVALUATE_ALL_CACHE
    if _EVALUATE_ALL_CACHE is None:
        _EVALUATE_ALL_CACHE = runner.evaluate_all()
    return _EVALUATE_ALL_CACHE


class CodexRuntimeRunnerFixtureEvalTest(unittest.TestCase):
    def test_ready_fixture_reports_route_ready(self):
        runner = load_runner()

        result = runner.evaluate_fixture(FIXTURES / "codex-runner-ready")

        self.assertEqual(result["codex_runtime_runner_status"], "route_ready")
        self.assertTrue(result["codex_runtime_runner_checks"]["contract_mode_offline"])
        self.assertTrue(result["codex_runtime_runner_checks"]["route_matches_lifecycle_state"])
        self.assertTrue(result["ok"])

    def test_missing_context_fixture_reports_needs_context(self):
        runner = load_runner()

        result = runner.evaluate_fixture(FIXTURES / "codex-runner-missing-context")

        self.assertEqual(result["codex_runtime_runner_status"], "needs_context")
        self.assertTrue(result["codex_runtime_runner_checks"]["missing_context_detected"])

    def test_approval_fixture_reports_needs_approval(self):
        runner = load_runner()

        result = runner.evaluate_fixture(FIXTURES / "codex-runner-approval-required")

        self.assertEqual(result["codex_runtime_runner_status"], "needs_approval")
        self.assertTrue(result["codex_runtime_runner_checks"]["approval_required_for_writes"])

    def test_guard_fixtures_are_checked(self):
        runner = load_runner()
        results = {item["fixture"]: item for item in evaluate_all_cached(runner)}

        self.assertTrue(
            results["codex-runner-handoff-incomplete"]["codex_runtime_runner_checks"]["handoff_incomplete_blocked"]
        )
        self.assertTrue(
            results["codex-runner-automation-blocked"]["codex_runtime_runner_checks"]["active_automation_blocked"]
        )
        self.assertTrue(
            results["codex-runner-secret-redaction"]["codex_runtime_runner_checks"]["secret_redaction_enforced"]
        )

    def test_runtime_methodology_fixtures_are_checked(self):
        runner = load_runner()
        results = {item["fixture"]: item for item in evaluate_all_cached(runner)}

        self.assertTrue(
            results["codex-runner-methodology-ready"]["codex_runtime_runner_checks"][
                "runtime_methodology_packet_present"
            ]
        )
        self.assertTrue(
            results["codex-runner-methodology-approval-required"]["codex_runtime_runner_checks"][
                "runtime_finish_options_approval_bound"
            ]
        )
        self.assertTrue(
            results["codex-runner-detection-completion-blocked"]["codex_runtime_runner_checks"][
                "runtime_detection_not_completion"
            ]
        )
        self.assertTrue(
            results["codex-runner-external-write-blocked"]["codex_runtime_runner_checks"][
                "runtime_external_write_blocked"
            ]
        )
        self.assertTrue(
            results["codex-runner-automation-maturity-missing"]["codex_runtime_runner_checks"][
                "runtime_automation_maturity_required"
            ]
        )
        self.assertTrue(
            results["codex-runner-methodology-redaction"]["codex_runtime_runner_checks"][
                "runtime_methodology_redaction_enforced"
            ]
        )
        self.assertTrue(
            results["codex-runner-malformed-methodology-packet"]["codex_runtime_runner_checks"][
                "runtime_malformed_methodology_packet_blocked"
            ]
        )

    def test_cross_domain_runtime_bridge_fixtures_are_checked(self):
        runner = load_runner()
        results = {item["fixture"]: item for item in evaluate_all_cached(runner)}

        for fixture in [
            "cross-domain-ai-rag-data-security",
            "package-release-security-handoff",
            "source-artifact-alias-mapping",
        ]:
            with self.subTest(fixture=fixture):
                self.assertTrue(
                    results[fixture]["codex_runtime_runner_checks"][
                        "runtime_cross_domain_bridge_present"
                    ]
                )
                self.assertTrue(
                    results[fixture]["codex_runtime_runner_checks"][
                        "runtime_first_response_compact"
                    ]
                )


if __name__ == "__main__":
    unittest.main()
