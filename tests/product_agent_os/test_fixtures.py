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
            "ai-prompt-model-change",
            "ai-tool-approval",
            "ai-structured-output",
            "ai-agent-trace",
            "ai-latency-cost-budget",
            "native-mobile-permissions",
            "desktop-local-indexer",
            "data-migration-pii",
            "security-auth-payment",
            "security-docs-only-mention",
            "security-compliance-claim",
            "security-ci-sbom",
            "ci-flaky-tests",
            "package-release",
            "release-docs-only-note",
            "release-ci-only-workflow",
            "release-deployment-manifest-only",
            "release-feature-flag-no-owner",
            "release-gitops-no-approval",
            "package-release-approval",
            "release-mobile-signing-only",
            "release-dora-individual-quota",
            "release-tooling-only",
            "backend-no-fsd",
            "native-no-fsd",
            "simple-crud-no-ddd",
            "docs-light-no-portal",
            "hosted-docs-approval",
            "frontend-ui-app",
            "backend-service-app",
            "api-external-write-approval",
            "swagger-ui-only-api-docs",
            "graphql-grpc-style-choice",
            "database-schema-only",
            "database-destructive-migration",
            "database-production-access-approval",
            "database-lineage-rag-overlap",
            "security-docs-only-mention",
            "security-compliance-claim",
            "security-ci-sbom",
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
            "frontend-ui-app",
            "api-external-write-approval",
            "swagger-ui-only-api-docs",
            "graphql-grpc-style-choice",
            "database-schema-only",
            "database-destructive-migration",
            "database-production-access-approval",
            "database-lineage-rag-overlap",
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

    def test_security_methodology_fixtures_are_synthetic_and_secret_free(self):
        expected_terms = {
            "security-auth-payment": ["Synthetic", "payment", "authorization", "permissions"],
            "security-docs-only-mention": ["Synthetic", "docs-only", "security article"],
            "security-compliance-claim": ["Synthetic", "compliance", "unsupported claim"],
            "security-ci-sbom": ["Synthetic", "SBOM", "CI permissions", "supply chain"],
        }

        for name, terms in expected_terms.items():
            with self.subTest(name=name):
                text = "\n".join(
                    path.read_text(encoding="utf-8")
                    for path in (FIXTURES / name).rglob("*")
                    if path.is_file()
                )
                for expected in terms:
                    self.assertIn(expected, text)
                lowered = text.lower()
                self.assertNotIn("private customer", lowered)
                self.assertNotIn("raw pii", lowered)
                self.assertNotIn("payment data", lowered)
                self.assertNotIn("token=", lowered)
                self.assertNotIn("api_key", lowered)
                self.assertNotIn("sk-", lowered)

    def test_ai_rag_methodology_fixtures_are_synthetic_and_secret_free(self):
        expected_terms = {
            "rag-quality-regression": ["Synthetic", "RAG", "grounding", "baseline"],
            "ai-prompt-model-change": ["Synthetic", "prompt", "model", "baseline"],
            "ai-tool-approval": ["Synthetic", "tool", "approval", "side effects"],
            "ai-structured-output": ["Synthetic", "structured output", "schema", "fallback"],
            "ai-agent-trace": ["Synthetic", "agent", "trace", "handoff"],
            "ai-latency-cost-budget": ["Synthetic", "latency", "cost", "budget"],
        }

        for name, terms in expected_terms.items():
            with self.subTest(name=name):
                text = "\n".join(
                    path.read_text(encoding="utf-8")
                    for path in (FIXTURES / name).rglob("*")
                    if path.is_file()
                )
                for expected in terms:
                    self.assertIn(expected, text)
                lowered = text.lower()
                self.assertNotIn("private customer", lowered)
                self.assertNotIn("raw private chat", lowered)
                self.assertNotIn("token=", lowered)
                self.assertNotIn("api_key", lowered)
                self.assertNotIn("sk-", lowered)

    def test_delivery_release_operations_fixtures_are_synthetic_and_secret_free(self):
        expected_terms = {
            "release-docs-only-note": ["Synthetic", "docs-only", "release note"],
            "release-ci-only-workflow": ["Synthetic", "CI-only", "workflow"],
            "release-deployment-manifest-only": ["Synthetic", "deployment manifest", "without execution"],
            "release-feature-flag-no-owner": ["Synthetic", "feature flag", "no owner"],
            "release-gitops-no-approval": ["Synthetic", "GitOps", "no approval path"],
            "package-release-approval": ["Synthetic", "package release", "approval_required"],
            "release-mobile-signing-only": ["Synthetic", "mobile signing", "without platform owner evidence"],
            "release-dora-individual-quota": ["Synthetic", "DORA", "individual quota"],
            "release-tooling-only": ["Synthetic", "release tooling", "without owner evidence"],
        }

        for name, terms in expected_terms.items():
            with self.subTest(name=name):
                text = "\n".join(
                    path.read_text(encoding="utf-8")
                    for path in (FIXTURES / name).rglob("*")
                    if path.is_file()
                )
                for expected in terms:
                    self.assertIn(expected, text)
                lowered = text.lower()
                self.assertNotIn("private customer", lowered)
                self.assertNotIn("raw private chat", lowered)
                self.assertNotIn("raw pii", lowered)
                self.assertNotIn("token=", lowered)
                self.assertNotIn("api_key", lowered)
                self.assertNotIn("sk-", lowered)

    def test_backend_service_fixture_is_synthetic_and_secret_free(self):
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (FIXTURES / "backend-service-app").rglob("*")
            if path.is_file()
        )
        for expected in [
            "Synthetic",
            "backend",
            "health",
            "queue",
            "worker",
            "observability",
            "runbook",
        ]:
            self.assertIn(expected, text)
        self.assertNotIn("private customer", text.lower())
        self.assertNotIn("token=", text.lower())
        self.assertNotIn("api_key", text.lower())


if __name__ == "__main__":
    unittest.main()
