import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
WRAPPER = SCRIPTS / "validate_automation_candidate.py"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.automation_policy import validate_automation_candidate  # noqa: E402


class AutomationPolicyTest(unittest.TestCase):
    def test_valid_candidate_is_ready_for_manual_approval(self):
        candidate = (
            FIXTURES
            / "automation-candidate-valid"
            / ".codex"
            / "automation-candidates"
            / "automation-candidate.md"
        )

        report = validate_automation_candidate(candidate)

        self.assertEqual(report["status"], "ready_for_manual_approval")
        self.assertEqual(report["automation_promotion_report"]["status"], "ready_for_manual_approval")
        self.assertEqual(report["manual_success_count"], 2)
        self.assertTrue(report["owner_present"])
        self.assertEqual(report["errors"], [])

    def test_invalid_candidate_is_blocked(self):
        candidate = (
            FIXTURES
            / "automation-candidate-invalid"
            / ".codex"
            / "automation-candidates"
            / "automation-candidate.md"
        )

        report = validate_automation_candidate(candidate)

        self.assertEqual(report["status"], "blocked")
        self.assertIn("owner is required", report["errors"])
        self.assertIn("verification is required", report["errors"])
        self.assertIn("rollback or disable path is required", report["errors"])
        self.assertIn("write policy is required", report["errors"])

    def test_candidate_only_without_two_runs_is_not_ready(self):
        text = (
            "# Automation Candidate\n\n"
            "Readiness: candidate_only\n\n"
            "## Owner\n\n"
            "- Accountable owner: Ops\n\n"
            "## Cadence\n\n"
            "- Trigger: manual\n\n"
            "## Verification\n\n"
            "- Deterministic checks: python tools/check_docs.py\n\n"
            "## Failure Modes\n\n"
            "- Known failure: missing docs source status\n\n"
            "## Rollback Or Disable Path\n\n"
            "- Disable path: remove candidate packet\n\n"
            "## Explicit Write Policy\n\n"
            "- Allowed write targets: docs only\n\n"
            "## Explicit Approval\n\n"
            "- Approval status: not requested\n"
        )

        report = validate_automation_candidate.from_text(text, "inline.md")

        self.assertEqual(report["status"], "candidate_only")
        self.assertIn("manual success count is below 2", report["warnings"])

    def test_two_manual_runs_do_not_make_incomplete_candidate_ready(self):
        text = (
            "# Automation Candidate\n\n"
            "Readiness: candidate_only\n\n"
            "## Owner\n\n"
            "- Accountable owner: Ops\n\n"
            "## Verification\n\n"
            "- Deterministic checks: python tools/check_docs.py\n"
            "- Successful manual workflow runs: 2\n\n"
            "## Rollback Or Disable Path\n\n"
            "- Disable path: remove candidate packet\n\n"
            "## Explicit Write Policy\n\n"
            "- Allowed write targets: none\n"
        )

        report = validate_automation_candidate.from_text(text, "inline.md")

        self.assertEqual(report["status"], "candidate_only")
        self.assertIn("stable inputs are not documented", report["warnings"])
        self.assertIn("stable outputs are not documented", report["warnings"])
        self.assertIn("cadence is not documented", report["warnings"])
        self.assertIn("failure modes are not documented", report["warnings"])
        self.assertIn("explicit approval section is not documented", report["warnings"])

    def test_secret_like_literal_blocks_candidate(self):
        text = (
            "# Automation Candidate\n\n"
            "## Owner\n\n"
            "- Accountable owner: Ops\n\n"
            "## Verification\n\n"
            "- Deterministic checks: python tools/check_docs.py\n\n"
            "## Rollback Or Disable Path\n\n"
            "- Disable path: remove candidate packet\n\n"
            "## Explicit Write Policy\n\n"
            "- Allowed write targets: docs only\n\n"
            "OPENAI_API_KEY = \"sk-synthetic-test\"\n"
        )

        report = validate_automation_candidate.from_text(text, "inline.md")

        self.assertEqual(report["status"], "blocked")
        self.assertIn("secret-like literal is forbidden", report["errors"])

    def test_cli_exits_zero_for_candidate_only_and_one_for_blocked(self):
        candidate = (
            FIXTURES
            / "automation-candidate-invalid"
            / ".codex"
            / "automation-candidates"
            / "automation-candidate.md"
        )

        result = subprocess.run(
            [sys.executable, str(WRAPPER), str(candidate)],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assertIn('"status": "blocked"', result.stdout)


if __name__ == "__main__":
    unittest.main()
