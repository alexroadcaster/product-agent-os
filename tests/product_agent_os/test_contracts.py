import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.contracts import (  # noqa: E402
    COMPLEXITY_PROFILES,
    LIFECYCLE_STATES,
    REQUIRED_HANDOFF_FIELDS,
    validate_handoff,
)


class ContractsTest(unittest.TestCase):
    def test_lifecycle_states_are_ordered(self):
        self.assertEqual(LIFECYCLE_STATES[0], "uninitialized")
        self.assertEqual(LIFECYCLE_STATES[-1], "maintenance")
        self.assertIn("quality_gate", LIFECYCLE_STATES)

    def test_complexity_profiles_cover_production_modes(self):
        self.assertIn("guided-small", COMPLEXITY_PROFILES)
        self.assertIn("production-team", COMPLEXITY_PROFILES)
        self.assertIn("enterprise-governed", COMPLEXITY_PROFILES)

    def test_handoff_requires_evidence_and_constraints(self):
        missing = validate_handoff({"goal": "ship feature"})
        self.assertIn("constraints", missing)
        self.assertIn("verification_evidence", missing)

    def test_handoff_rejects_empty_constraints_and_verification_evidence(self):
        payload = self._valid_handoff()
        payload["constraints"] = []
        payload["verification_evidence"] = []

        errors = validate_handoff(payload)

        self.assertIn("constraints:empty", errors)
        self.assertIn("verification_evidence:empty", errors)

    def test_handoff_requires_files_touched_or_files_proposed(self):
        payload = self._valid_handoff()
        payload["files_touched"] = []
        payload["files_proposed"] = []

        self.assertIn("files:empty", validate_handoff(payload))

    def test_valid_handoff_has_no_missing_fields(self):
        payload = self._valid_handoff()
        self.assertEqual(validate_handoff(payload), [])

    def _valid_handoff(self):
        return {
            "lifecycle_state": "plan_ready",
            "goal": "ship feature",
            "constraints": ["Do not store secrets."],
            "allowed_sources": [],
            "inputs_used": [],
            "verified_claims": [],
            "unsupported_claims": [],
            "files_touched": ["PLAN.md"],
            "files_proposed": [],
            "commands_run": [],
            "verification_evidence": ["python -m unittest tests.product_agent_os.test_contracts -v"],
            "risks": [],
            "next_agent_task": "",
            "stop_reason": "",
        }


if __name__ == "__main__":
    unittest.main()
