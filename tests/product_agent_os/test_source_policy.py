import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
WRAPPER = SCRIPTS / "validate_source_policy.py"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.source_policy import validate_source_policy  # noqa: E402


class SourcePolicyTest(unittest.TestCase):
    def test_missing_source_status_blocks_docs_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            docs = workspace / "docs"
            docs.mkdir()
            (docs / "guide.md").write_text("# Guide\n\nOpenAI Codex behavior claim.\n", encoding="utf-8")

            report = validate_source_policy(workspace)

        self.assertEqual(report["status"], "blocked")
        self.assertIn("source_policy_report", report)
        self.assertIn("docs/guide.md", {item["path"] for item in report["files"]})
        self.assertIn("missing Source status", report["errors"])

    def test_openai_behavior_without_source_hint_needs_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            docs = workspace / "docs"
            docs.mkdir()
            (docs / "guide.md").write_text(
                "# Guide\n\n"
                "Source status: `official`\n\n"
                "Codex approvals and MCP hooks always run with the latest model behavior.\n",
                encoding="utf-8",
            )

            report = validate_source_policy(workspace)

        self.assertEqual(report["status"], "needs_review")
        file_report = report["files"][0]
        self.assertIn("official source hint is required for OpenAI behavior claim", file_report["missing_context"])
        self.assertTrue(file_report["freshness_risks"])

    def test_secret_like_literal_blocks_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            docs = workspace / "docs"
            docs.mkdir()
            (docs / "guide.md").write_text(
                "# Guide\n\nSource status: `experiment`\n\nOPENAI_API_KEY = \"sk-synthetic-test\"\n",
                encoding="utf-8",
            )

            report = validate_source_policy(workspace)

        self.assertEqual(report["status"], "blocked")
        self.assertTrue(report["secret_findings"])

    def test_community_claim_without_trust_metadata_needs_review(self):
        workspace = FIXTURES / "source-policy-conflict"

        report = validate_source_policy(workspace)

        self.assertEqual(report["status"], "needs_review")
        self.assertTrue(any(item["unsupported_claims"] for item in report["files"]))

    def test_repo_root_status_is_not_blocked_by_source_policy(self):
        report = validate_source_policy(ROOT)

        self.assertIn(report["status"], {"ok", "needs_review"})
        self.assertEqual(report["secret_findings"], [])

    def test_copied_repo_fixture_without_secrets_is_not_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            shutil.copytree(FIXTURES / "docs-repo", workspace)

            report = validate_source_policy(workspace)

        self.assertIn(report["status"], {"ok", "needs_review"})
        self.assertEqual(report["secret_findings"], [])

    def test_cli_exits_nonzero_for_needs_review_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            docs = workspace / "docs"
            docs.mkdir()
            (docs / "guide.md").write_text(
                "# Guide\n\n"
                "Source status: `official`\n\n"
                "Codex approvals and MCP hooks always run with the latest model behavior.\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace)],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assertEqual(payload["status"], "needs_review")
        self.assertNotIn("Traceback", result.stdout)


if __name__ == "__main__":
    unittest.main()
