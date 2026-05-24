import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.contracts import (  # noqa: E402
    ALLOWED_RUNNER_STATUSES,
    ALLOWED_RUNTIME_SURFACES,
    ALLOWED_WRITE_POLICIES,
    REQUIRED_RESULT_FIELDS,
    build_result,
    validate_runner_request,
    validate_runner_result,
)


class CodexRuntimeRunnerContractsTest(unittest.TestCase):
    def test_contract_enums_are_codex_only(self):
        self.assertIn("Codex App", ALLOWED_RUNTIME_SURFACES)
        self.assertIn("CLI", ALLOWED_RUNTIME_SURFACES)
        self.assertIn("IDE extension", ALLOWED_RUNTIME_SURFACES)
        self.assertIn("subagent", ALLOWED_RUNTIME_SURFACES)
        self.assertIn("skill", ALLOWED_RUNTIME_SURFACES)
        self.assertNotIn("Agents SDK", ALLOWED_RUNTIME_SURFACES)
        self.assertNotIn("api", {item.lower() for item in ALLOWED_RUNTIME_SURFACES})
        self.assertEqual(ALLOWED_WRITE_POLICIES, ["read_only", "staged_only", "approved_write", "blocked"])
        self.assertIn("route_ready", ALLOWED_RUNNER_STATUSES)

    def test_valid_runner_request_passes(self):
        request = self._valid_request()

        self.assertEqual(validate_runner_request(request), [])

    def test_runner_request_rejects_unknown_surface_and_writes_without_approval(self):
        request = self._valid_request()
        request["routing"]["preferred_surface"] = "external service"
        request["routing"]["allow_workspace_writes"] = True
        request["approval"]["approval_status"] = "required"

        errors = validate_runner_request(request)

        self.assertIn("routing.preferred_surface:unknown", errors)
        self.assertIn("routing.allow_workspace_writes:approval_required", errors)

    def test_build_result_returns_complete_shape(self):
        result = build_result(
            status="route_ready",
            workspace="C:/workspace/synthetic",
            lifecycle_state="quality_gate",
            route_packet={"write_policy": "read_only"},
            source_policy_status="ok",
            approval_status="not_required",
            next_action="Run risk-reviewer.",
        )

        self.assertEqual(list(result.keys()), REQUIRED_RESULT_FIELDS)
        self.assertEqual(validate_runner_result(result), [])
        self.assertEqual(result["redactions"], {"count": 0, "categories": []})

    def test_result_rejects_completion_claim_without_evidence(self):
        result = build_result(
            status="completed",
            workspace="C:/workspace/synthetic",
            lifecycle_state="review_ready",
            route_packet={"write_policy": "staged_only"},
            source_policy_status="ok",
            approval_status="not_required",
            next_action="No action.",
        )

        errors = validate_runner_result(result)

        self.assertIn("verification_evidence:required_for_completed", errors)

    def _valid_request(self):
        return {
            "schema_version": 1,
            "workspace": "C:/workspace/synthetic",
            "task": {
                "goal": "Prepare next Product-Agent OS action.",
                "lifecycle_state": "quality_gate",
                "constraints": ["Do not write files."],
                "allowed_sources": ["official docs", "repo artifacts"],
                "expected_artifacts": ["codex_runner_result"],
            },
            "routing": {
                "preferred_surface": "CLI",
                "allow_subagents": False,
                "allow_workspace_writes": False,
            },
            "approval": {
                "required": False,
                "approval_file": "",
                "approval_status": "not_required",
            },
        }


if __name__ == "__main__":
    unittest.main()
