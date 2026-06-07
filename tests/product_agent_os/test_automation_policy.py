import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
TEMPLATE_ROOT = ROOT / "plugins" / "product-agent-os" / "assets" / "templates"
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

    def test_metrics_automation_candidate_remains_candidate_only_with_manual_stability(self):
        text = _metrics_automation_candidate_text()

        report = validate_automation_candidate.from_text(text, "daily-agent-skill-metrics.md")

        self.assertEqual(report["status"], "candidate_only")
        self.assertTrue(report["metrics_automation_candidate"])
        self.assertEqual(report["manual_success_count"], 2)
        self.assertEqual(report["active_schedule_status"], "not_created")
        self.assertEqual(report["errors"], [])
        self.assertNotIn("manual success count is below 2", report["warnings"])

    def test_metrics_automation_candidate_blocks_active_schedules_and_external_workflows(self):
        text = (
            _metrics_automation_candidate_text()
            + "\n"
            + "## Active Schedule\n\n"
            + "- Cron: 0 9 * * *\n"
            + "- GitHub Actions workflow: active\n"
            + "- Codex App automation: active\n"
        )

        report = validate_automation_candidate.from_text(text, "weekly-agent-skill-metrics.md")

        self.assertEqual(report["status"], "blocked")
        self.assertTrue(report["metrics_automation_candidate"])
        self.assertIn("active automation is forbidden", report["errors"])
        self.assertIn("active metrics automation is forbidden", report["errors"])
        self.assertIn("external workflow creation is forbidden", report["errors"])

    def test_system_file_hygiene_candidate_remains_candidate_only_and_blocks_active_schedule(self):
        text = (
            "# System File Hygiene Audit Automation Candidate\n\n"
            "Automation type: system-file-hygiene\n"
            "Readiness: candidate_only\n\n"
            "## Owner\n\n"
            "- Accountable owner: Project operator\n\n"
            "## Cadence\n\n"
            "- Trigger: manual only until explicit approval\n"
            "- Frequency: weekly candidate packet\n\n"
            "## Stable Inputs\n\n"
            "- Inputs: AGENTS.md, REQUIREMENTS.md, PLAN.md, TEST.md, EVALS.md, RUNLOG.md, .codex/agents, .codex/skills\n\n"
            "## Stable Outputs\n\n"
            "- Outputs: staged system-file-hygiene-report.md\n\n"
            "## Verification\n\n"
            "- Deterministic checks: python plugins\\product-agent-os\\scripts\\validate_system_file_hygiene.py <workspace>\n"
            "- Successful manual workflow runs: 0\n\n"
            "## Failure Modes\n\n"
            "- Known failure: hard size limit crossed\n\n"
            "## Rollback Or Disable Path\n\n"
            "- Disable path: remove candidate packet\n\n"
            "## Explicit Write Policy\n\n"
            "- Allowed write targets: staged artifacts only\n\n"
            "## Explicit Approval\n\n"
            "- Approval status: not requested\n"
        )
        active = text + "\nCron: 0 9 * * *\n"

        report = validate_automation_candidate.from_text(text, "system-file-hygiene-audit.md")
        active_report = validate_automation_candidate.from_text(active, "system-file-hygiene-audit.md")

        self.assertEqual(report["status"], "candidate_only")
        self.assertIn("manual success count is below 2", report["warnings"])
        self.assertEqual(active_report["status"], "blocked")
        self.assertIn("active automation is forbidden", active_report["errors"])

    def test_bundled_system_file_hygiene_candidate_has_no_active_schedule(self):
        candidate = TEMPLATE_ROOT / "automations" / "system-file-hygiene-audit.md"

        report = validate_automation_candidate(candidate)
        text = candidate.read_text(encoding="utf-8").lower()

        self.assertEqual(report["status"], "candidate_only")
        self.assertEqual(report["manual_success_count"], 0)
        self.assertEqual(report["active_schedule_status"], "not_created")
        self.assertEqual(report["errors"], [])
        self.assertIn("manual success count is below 2", report["warnings"])
        self.assertIn("candidate_only", text)
        self.assertNotIn("github actions workflow: active", text)
        self.assertNotIn("codex app automation: active", text)
        active_schedule_prefixes = ("cron:", "- cron:", "rrule:", "- rrule:")
        self.assertFalse(any(line.strip().startswith(active_schedule_prefixes) for line in text.splitlines()))

    def test_non_metrics_candidate_blocks_schedule_field_as_active_schedule(self):
        text = _activation_candidate_text() + "\nSchedule: weekly every Monday\n"

        report = validate_automation_candidate.from_text(text, "docs-maintenance.md")

        self.assertEqual(report["status"], "blocked")
        self.assertEqual(report["active_schedule_status"], "detected")
        self.assertIn("active automation is forbidden", report["errors"])

    def test_activation_gate_requires_owner_approval_and_accepted_residual_risks(self):
        text = _activation_candidate_text()

        report = validate_automation_candidate.from_text(text, "docs-maintenance.md")
        gate = report["activation_gate"]

        self.assertEqual(report["status"], "ready_for_manual_approval")
        self.assertEqual(gate["status"], "blocked_without_owner_approval")
        self.assertFalse(gate["activation_requirements_met"])
        self.assertTrue(gate["manual_stability_present"])
        self.assertTrue(gate["deterministic_command_evidence_present"])
        self.assertTrue(gate["rollback_or_disable_present"])
        self.assertFalse(gate["owner_approval_present"])
        self.assertFalse(gate["accepted_residual_risks_present"])
        self.assertIn("owner approval is required before activation", report["warnings"])
        self.assertIn("accepted residual risks are required before activation", report["warnings"])

    def test_approved_candidate_still_requires_future_activation_slice_without_creating_schedule(self):
        text = _activation_candidate_text(
            approval_status="approved by Project operator for future activation review",
            accepted_residual_risks=True,
        )

        report = validate_automation_candidate.from_text(text, "docs-maintenance.md")
        gate = report["activation_gate"]

        self.assertEqual(report["status"], "ready_for_manual_approval")
        self.assertEqual(report["active_schedule_status"], "not_created")
        self.assertEqual(gate["status"], "ready_for_separate_activation_slice")
        self.assertTrue(gate["activation_requirements_met"])
        self.assertTrue(gate["future_activation_handoff_required"])
        self.assertFalse(gate["github_actions_active"])
        self.assertFalse(gate["codex_app_automation_active"])
        self.assertFalse(gate["hook_activation_active"])
        self.assertFalse(gate["external_write_active"])

    def test_future_activation_handoff_blocks_hook_activation_and_external_write_markers(self):
        text = _activation_candidate_text(
            approval_status="approved by Project operator for future activation review",
            accepted_residual_risks=True,
        )
        text += "\nHook activation: active\nExternal write: active\n"

        report = validate_automation_candidate.from_text(text, "docs-maintenance.md")
        gate = report["activation_gate"]

        self.assertEqual(report["status"], "blocked")
        self.assertEqual(gate["status"], "blocked_active_runtime_marker_detected")
        self.assertTrue(gate["hook_activation_active"])
        self.assertTrue(gate["external_write_active"])
        self.assertIn("hook activation is forbidden", report["errors"])
        self.assertIn("external write is forbidden", report["errors"])

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

    def test_cli_reports_activation_gate_for_blocked_runtime_markers(self):
        text = _activation_candidate_text(
            approval_status="approved by Project operator for future activation review",
            accepted_residual_risks=True,
        )
        text += "\nSchedule: weekly\n"

        with tempfile.TemporaryDirectory() as tmp:
            candidate = Path(tmp) / "automation-candidate.md"
            candidate.write_text(text, encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(candidate)],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["activation_gate"]["status"], "blocked_active_runtime_marker_detected")
        self.assertEqual(payload["active_schedule_status"], "detected")

def _metrics_automation_candidate_text() -> str:
    return (
        "# Daily Agent Skill Metrics Automation Candidate\n\n"
        "Automation type: metrics-loop\n"
        "Readiness: candidate_only\n\n"
        "## Owner\n\n"
        "- Accountable owner: Quality\n\n"
        "## Cadence\n\n"
        "- Trigger: manual only until explicit approval\n"
        "- Frequency: daily candidate packet\n\n"
        "## Stable Inputs\n\n"
        "- Inputs: RUNLOG.md, TEST.md, EVALS.md, trace-evidence-packet.md\n\n"
        "## Stable Outputs\n\n"
        "- Outputs: staged agent skill metrics report and candidate packet\n\n"
        "## Verification\n\n"
        "- Deterministic checks: python -m unittest tests.product_agent_os.test_agent_skill_metrics -v\n"
        "- Successful manual workflow runs: 2\n\n"
        "## Failure Modes\n\n"
        "- Known failure: missing trace classification register\n\n"
        "## Rollback Or Disable Path\n\n"
        "- Disable path: remove candidate packet and staged report proposal\n\n"
        "## Explicit Write Policy\n\n"
        "- Allowed write targets: staged artifacts only\n\n"
        "## Explicit Approval\n\n"
        "- Approval status: not requested\n"
    )


def _activation_candidate_text(
    *,
    approval_status: str = "not requested",
    accepted_residual_risks: bool = False,
) -> str:
    residual_risks = (
        "## Accepted Residual Risks\n\n"
        "- Accepted residual risks: low operational noise accepted by owner for future activation review\n\n"
        if accepted_residual_risks
        else ""
    )
    return (
        "# Docs Maintenance Automation Candidate\n\n"
        "Automation type: docs-maintenance\n"
        "Readiness: candidate_only\n\n"
        "## Owner\n\n"
        "- Accountable owner: Docs Maintainer\n\n"
        "## Cadence\n\n"
        "- Trigger: manual after docs changes until explicit approval\n"
        "- Frequency: on demand candidate packet\n\n"
        "## Stable Inputs\n\n"
        "- Inputs: changed Markdown files and source registry entries\n\n"
        "## Stable Outputs\n\n"
        "- Outputs: validation report only\n\n"
        "## Verification\n\n"
        "- Deterministic checks: python tools/check_docs.py\n"
        "- Successful manual workflow runs: 2\n\n"
        "## Failure Modes\n\n"
        "- Known failure: missing Source status\n\n"
        "## Rollback Or Disable Path\n\n"
        "- Disable path: pause or remove the candidate packet and stop invoking the command\n\n"
        "## Explicit Write Policy\n\n"
        "- Allowed write targets: none during candidate validation\n\n"
        "## Explicit Approval\n\n"
        f"- Approval status: {approval_status}\n\n"
        f"{residual_risks}"
    )


if __name__ == "__main__":
    unittest.main()
