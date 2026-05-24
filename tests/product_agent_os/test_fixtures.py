import json
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"


class FixtureCompletenessTest(unittest.TestCase):
    def test_required_fixture_projects_exist(self):
        for name in [
            "empty-repo",
            "node-app",
            "python-app",
            "monorepo",
            "docs-repo",
            "existing-codex-config",
            "duplicate-managed-section",
            "docs-source-conflict",
            "failed-verification",
            "unsafe-write-request",
            "stale-merge-plan",
            "path-traversal-stage",
            "symlink-escape",
            "hook-activation-unapproved",
            "hook-activation-approved",
            "source-policy-conflict",
            "automation-candidate-valid",
            "automation-candidate-invalid",
            "rollback-required",
            "failure-log-regression",
            "codex-runner-ready",
            "codex-runner-missing-context",
            "codex-runner-handoff-incomplete",
            "codex-runner-approval-required",
            "codex-runner-automation-blocked",
            "codex-runner-secret-redaction",
            "legacy-undocumented-repo",
            "api-migration-repo",
            "rag-quality-regression",
            "native-mobile-permissions",
            "desktop-local-indexer",
            "data-migration-pii",
            "security-auth-payment",
            "ci-flaky-tests",
            "package-release",
            "backend-no-fsd",
            "native-no-fsd",
            "simple-crud-no-ddd",
            "docs-light-no-portal",
            "hosted-docs-approval",
        ]:
            with self.subTest(name=name):
                self.assertTrue((FIXTURES / name).is_dir())

    def test_node_fixture_has_package_json(self):
        self.assertTrue((FIXTURES / "node-app" / "package.json").exists())

    def test_existing_codex_fixture_has_project_config(self):
        self.assertTrue((FIXTURES / "existing-codex-config" / ".codex" / "config.toml").exists())

    def test_json_fixtures_are_valid(self):
        for path in [
            FIXTURES / "node-app" / "package.json",
            FIXTURES / "monorepo" / "package.json",
            FIXTURES / "monorepo" / "packages" / "api" / "package.json",
        ]:
            with self.subTest(path=path):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertIn("name", data)

    def test_node_fixture_is_explicit_esm(self):
        data = json.loads((FIXTURES / "node-app" / "package.json").read_text(encoding="utf-8"))
        self.assertEqual(data["type"], "module")

    def test_toml_fixtures_are_valid(self):
        for path in [
            FIXTURES / "python-app" / "pyproject.toml",
            FIXTURES / "existing-codex-config" / ".codex" / "config.toml",
        ]:
            with self.subTest(path=path):
                tomllib.loads(path.read_text(encoding="utf-8"))

    def test_docs_fixture_has_docs_dir(self):
        mkdocs_config = (FIXTURES / "docs-repo" / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertIn("docs_dir: docs", mkdocs_config)
        self.assertTrue((FIXTURES / "docs-repo" / "docs").is_dir())

    def test_duplicate_managed_section_fixture_has_two_markers(self):
        text = (FIXTURES / "duplicate-managed-section" / "AGENTS.md").read_text(encoding="utf-8")

        self.assertEqual(text.count("<!-- product-agent-os:start project-rules -->"), 2)

    def test_docs_source_conflict_fixture_has_source_registry(self):
        self.assertTrue((FIXTURES / "docs-source-conflict" / "docs" / "sources" / "registry.md").exists())
        text = (FIXTURES / "docs-source-conflict" / "mkdocs.yml").read_text(encoding="utf-8")

        self.assertIn("docs_dir: docs", text)

    def test_failed_verification_fixture_records_failure_without_success_claim(self):
        text = (FIXTURES / "failed-verification" / "RUNLOG.md").read_text(encoding="utf-8")

        self.assertIn("exit_code: 1", text)
        self.assertIn("verification failed", text)
        self.assertNotIn("checks passed", text.lower())

    def test_unsafe_write_request_fixture_has_existing_codex_config(self):
        self.assertTrue((FIXTURES / "unsafe-write-request" / ".codex" / "config.toml").exists())
        text = (FIXTURES / "unsafe-write-request" / "AGENTS.md").read_text(encoding="utf-8")

        self.assertIn("Do not write outside this workspace", text)

    def test_track_four_automation_candidate_fixtures_have_candidate_packets(self):
        for name in ["automation-candidate-valid", "automation-candidate-invalid"]:
            with self.subTest(name=name):
                self.assertTrue(
                    (
                        FIXTURES
                        / name
                        / ".codex"
                        / "automation-candidates"
                        / "automation-candidate.md"
                    ).exists()
                )

    def test_failure_log_regression_fixture_records_expected_check(self):
        text = (FIXTURES / "failure-log-regression" / "RUNLOG.md").read_text(encoding="utf-8")

        self.assertIn("expected_regression_fixture:", text)
        self.assertIn("expected_check:", text)

    def test_symlink_escape_fixture_documents_portable_metadata(self):
        text = (FIXTURES / "symlink-escape" / "README.md").read_text(encoding="utf-8")

        self.assertIn("portable metadata", text)

    def test_codex_runner_fixtures_are_synthetic(self):
        for name in [
            "codex-runner-ready",
            "codex-runner-missing-context",
            "codex-runner-handoff-incomplete",
            "codex-runner-approval-required",
            "codex-runner-automation-blocked",
            "codex-runner-secret-redaction",
        ]:
            with self.subTest(name=name):
                text = "\n".join(
                    path.read_text(encoding="utf-8")
                    for path in (FIXTURES / name).rglob("*")
                    if path.is_file()
                )
                self.assertIn("Synthetic", text)
                self.assertNotIn("private customer", text.lower())

    def test_false_positive_scenario_fixtures_are_synthetic_and_secret_free(self):
        for name in [
            "backend-no-fsd",
            "native-no-fsd",
            "simple-crud-no-ddd",
            "docs-light-no-portal",
            "hosted-docs-approval",
        ]:
            with self.subTest(name=name):
                text = "\n".join(
                    path.read_text(encoding="utf-8")
                    for path in (FIXTURES / name).rglob("*")
                    if path.is_file()
                )
                self.assertIn("Synthetic", text)
                self.assertNotIn("private customer", text.lower())
                self.assertNotIn("token=", text.lower())
                self.assertNotIn("api_key", text.lower())


if __name__ == "__main__":
    unittest.main()
