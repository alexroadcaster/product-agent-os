import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.guards import (  # noqa: E402
    validate_approval_boundary,
    validate_automation_boundary,
    validate_codex_handoff,
    validate_route_packet,
)
from codex_runtime_runner.redaction import redact_text, validate_redaction  # noqa: E402


class CodexRuntimeRunnerGuardsTest(unittest.TestCase):
    def test_approved_write_route_requires_approval(self):
        route = {"write_policy": "approved_write", "approval_requirements": ["approval required"]}

        errors = validate_approval_boundary(route, {"approval_status": "required"})

        self.assertIn("approval:required_for_write", errors)

    def test_read_only_route_does_not_require_approval(self):
        route = {"write_policy": "read_only", "approval_requirements": []}

        self.assertEqual(validate_approval_boundary(route, {"approval_status": "not_required"}), [])

    def test_route_packet_rejects_unknown_skill_for_state(self):
        route = {
            "lifecycle_state": "quality_gate",
            "recommended_skill": "requirements-author",
            "recommended_subagent_role": "",
            "write_policy": "read_only",
        }

        errors = validate_route_packet(route)

        self.assertIn("route:unexpected_skill_for_state", errors)

    def test_handoff_requires_constraints_and_evidence(self):
        handoff = {
            "lifecycle_state": "quality_gate",
            "role": "risk-reviewer",
            "goal": "Review release risk.",
            "constraints": [],
            "sources_used": [],
            "assumptions": [],
            "verified_claims": [],
            "unsupported_claims": [],
            "files_touched": [],
            "files_proposed": ["RUNLOG.md"],
            "commands_run": [],
            "verification_evidence": [],
            "approval_requirements": [],
            "open_risks": [],
            "recommended_next_role": "",
            "stop_reason": "",
        }

        errors = validate_codex_handoff(handoff)

        self.assertIn("constraints:empty", errors)
        self.assertIn("verification_evidence:empty", errors)

    def test_active_automation_request_is_blocked(self):
        text = "Create active recurring automation after this run."

        self.assertIn("automation:active_request_blocked", validate_automation_boundary(text))

    def test_redaction_removes_secret_like_and_absolute_path_values(self):
        text = "TOKEN=fixture-secret\nPath C:\\Users\\person\\project\\file.txt\nraw private chat log"

        redacted, report = redact_text(text)

        self.assertNotIn("fixture-secret", redacted)
        self.assertNotIn("C:\\Users\\person", redacted)
        self.assertIn("secret", report["categories"])
        self.assertIn("absolute_path", report["categories"])
        self.assertEqual(validate_redaction(redacted), [])


if __name__ == "__main__":
    unittest.main()
