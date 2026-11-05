import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
WRAPPER = SCRIPTS / "validate_source_policy.py"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.source_policy import validate_source_policy  # noqa: E402


class SourcePolicyTest(unittest.TestCase):
    def test_official_presence_is_not_semantic_or_freshness_verification(self):
        for host in ("learn.chatgpt.com", "platform.openai.com", "developers.openai.com"):
            with self.subTest(host=host), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); (root / "docs").mkdir()
                (root / "docs/guide.md").write_text("Source status: official\nCodex approvals.\nSources: https://" + host + "/docs\nChecked: 2026-11-05\n", encoding="utf-8")
                report = validate_source_policy(root, as_of=date(2026, 11, 5))
                evidence = report["files"][0]["source_evidence"]
                self.assertTrue(evidence["source_present"])
                self.assertEqual(evidence["claim_supported"], "not_verified")
                self.assertEqual(evidence["freshness"]["status"], "date_present_not_verified")
                self.assertEqual(report["status"], "ok")

    def test_empty_source_header_and_spoofed_urls_do_not_supply_evidence(self):
        for source in ("Sources:", "official docs", "https://developers.openai.com.evil.test/docs", "https://developers.openai.com@evil.test/docs", "https://evil.test/?next=https://developers.openai.com", "https://[broken", "https://github.com/openai-evil/repo"):
            with self.subTest(source=source), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); (root / "docs").mkdir()
                (root / "docs/guide.md").write_text("Source status: `official`\nCodex approvals.\n" + source, encoding="utf-8")
                report = validate_source_policy(root)
                self.assertEqual(report["status"], "needs_review")
                self.assertFalse(report["files"][0]["source_evidence"]["source_present"])

    def test_stale_invalid_and_missing_dates_remain_explicit(self):
        for marker, status in (("Checked: 2020-01-01", "stale"), ("Checked: 2026-99-99", "invalid"), ("", "missing")):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); (root / "docs").mkdir()
                (root / "docs/guide.md").write_text("Source status: `official`\nCodex MCP\nhttps://developers.openai.com/codex\n" + marker, encoding="utf-8")
                report = validate_source_policy(root, as_of=date(2026, 11, 5))
                self.assertEqual(report["files"][0]["source_evidence"]["freshness"]["status"], status)

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

    def test_sensitive_data_marker_literals_block_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            docs = workspace / "docs"
            docs.mkdir()
            (docs / "security-fixture.md").write_text(
                "# Fixture\n\n"
                "Source status: `experiment`\n\n"
                "raw_pii = \"Synthetic Person <synthetic@example.test>\"\n"
                "payment_data = \"4242 4242 4242 4242\"\n"
                "private_customer_data = \"synthetic customer text\"\n",
                encoding="utf-8",
            )

            report = validate_source_policy(workspace)

        self.assertEqual(report["status"], "blocked")
        findings = "\n".join(report["secret_findings"]).lower()
        self.assertIn("raw pii/private data/payment data marker is forbidden", findings)

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
