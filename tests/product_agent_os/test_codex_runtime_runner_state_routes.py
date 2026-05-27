import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.context_loader import load_control_plane_context  # noqa: E402
from codex_runtime_runner.cli import run_contract  # noqa: E402
from codex_runtime_runner.guards import validate_approval_boundary, validate_route_packet  # noqa: E402
from codex_runtime_runner.routes import plan_route  # noqa: E402
from codex_runtime_runner.state import infer_lifecycle_state  # noqa: E402


class CodexRuntimeRunnerStateRoutesTest(unittest.TestCase):
    def test_missing_agents_is_uninitialized(self):
        with tempfile.TemporaryDirectory() as tmp:
            context = load_control_plane_context(Path(tmp))

        self.assertEqual(infer_lifecycle_state(context, {}), "uninitialized")

    def test_missing_plan_after_requirements_is_requirements_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, omit={"PLAN.md"})
            context = load_control_plane_context(workspace)

        self.assertEqual(infer_lifecycle_state(context, {}), "requirements_ready")

    def test_request_lifecycle_override_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace)
            context = load_control_plane_context(workspace)

        self.assertEqual(
            infer_lifecycle_state(context, {"task": {"lifecycle_state": "quality_gate"}}),
            "quality_gate",
        )

    def test_route_maps_quality_gate_to_risk_reviewer(self):
        route = plan_route("quality_gate", allow_subagents=False)

        self.assertEqual(route["recommended_skill"], "risk-reviewer")
        self.assertEqual(route["recommended_subagent_role"], "")
        self.assertEqual(route["write_policy"], "read_only")
        self.assertIn("python", " ".join(route["verification"]))

    def test_route_can_carry_usage_mode_and_first_response_contract(self):
        usage_mode = {
            "primary": "greenfield_idea",
            "secondary": [],
            "confidence": "high",
            "reasons": ["workspace has no implementation files"],
            "fallback": "standard_feature",
            "first_response_contract": [
                "mode",
                "confidence",
                "next smallest action",
                "minimum artifacts",
                "evidence gaps",
                "approval boundary",
            ],
            "minimum_artifacts": ["greenfield idea brief"],
            "behavioral_eval_cases": ["first-run-response"],
        }

        route = plan_route("uninitialized", allow_subagents=False, usage_mode=usage_mode)

        self.assertEqual(route["usage_mode"]["primary"], "greenfield_idea")
        self.assertEqual(route["first_response_contract"]["mode"], "greenfield_idea")
        self.assertEqual(route["first_response_contract"]["minimum_artifacts"], ["greenfield idea brief"])
        self.assertEqual(route["first_response_contract"]["approval_boundary"], "read_only")
        self.assertEqual(route["first_response_contract"]["required_fields"], usage_mode["first_response_contract"])
        self.assertIn("evidence gaps", route["first_response_contract"]["required_fields"])

    def test_route_carries_compact_methodology_packet_and_finish_options(self):
        route = plan_route(
            "requirements_ready",
            allow_subagents=False,
            methodology_intelligence=self._methodology_intelligence(),
        )

        packet = route["methodology_packet"]
        self.assertEqual(packet["write_policy"], "read_only")
        self.assertEqual(packet["safe_next_action"], "Stage security-risk-review.md before implementation.")
        self.assertTrue(packet["recommendation_groups"])
        self.assertTrue(packet["questions_for_owner"])
        self.assertEqual(route["finish_options"], ["read_only_audit", "ask_owner", "stage_proposal", "run_verification", "stop_blocked"])
        self.assertEqual(route["first_response_contract"]["safe_next_action"], packet["safe_next_action"])
        self.assertEqual(route["first_response_contract"]["finish_options"], route["finish_options"])

    def test_read_only_route_does_not_stage_from_recommendation_only_methodology_packet(self):
        route = plan_route(
            "quality_gate",
            allow_subagents=False,
            methodology_intelligence=self._methodology_intelligence(),
        )

        self.assertEqual(route["write_policy"], "read_only")
        self.assertNotIn("stage_proposal", route["finish_options"])
        self.assertNotIn("security-risk-review.md", route["expected_outputs"])

    def test_high_risk_methodology_action_requires_approval_without_external_output(self):
        route = plan_route(
            "review_ready",
            allow_subagents=False,
            methodology_intelligence=self._methodology_intelligence(
                artifact="release-readiness.md",
                safe_next_action="Publish package to the package registry.",
            ),
        )

        approval_errors = validate_approval_boundary(route, {"approval_status": "not_required"})

        self.assertIn("request_approval", route["finish_options"])
        self.assertIn("approval:required_for_methodology_action", approval_errors)
        self.assertTrue(route["approval_requirements"])
        self.assertNotIn("publish", " ".join(route["expected_outputs"]).lower())

    def test_automation_maturity_blocks_automation_promoter_route(self):
        route = plan_route(
            "learning_ready",
            allow_subagents=False,
            methodology_intelligence=self._methodology_intelligence(
                artifact="automation-candidate.md",
                safe_next_action="Promote this workflow to an active automation.",
            ),
        )

        errors = validate_route_packet(route)

        self.assertEqual(route["recommended_skill"], "learning-loop-maintainer")
        self.assertNotIn("stage_proposal", route["finish_options"])
        self.assertIn("automation:maturity_evidence_required", errors)

    def test_run_contract_preserves_methodology_intelligence_from_workspace_discovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace)
            src = workspace / "src"
            src.mkdir()
            (src / "payment_api.py").write_text("def charge(): pass\n", encoding="utf-8")
            result = run_contract(
                workspace,
                intent_hint="security-sensitive payment release",
            )

        packet = result["route_packet"]["methodology_packet"]
        self.assertTrue(packet["methodology_domains"])
        self.assertTrue(packet["recommendation_groups"])
        self.assertTrue(packet["questions_for_owner"])
        self.assertTrue(packet["safe_next_action"])
        self.assertEqual(packet["write_policy"], "read_only")
        self.assertIn("finish_options", result["route_packet"])

    def test_build_active_uses_builder_subagent_and_requires_approval(self):
        route = plan_route("build_active", allow_subagents=True)

        self.assertEqual(route["recommended_skill"], "")
        self.assertEqual(route["recommended_subagent_role"], "builder")
        self.assertEqual(route["write_policy"], "approved_write")
        self.assertTrue(route["approval_requirements"])

    def _methodology_intelligence(
        self,
        *,
        artifact: str = "security-risk-review.md",
        safe_next_action: str = "Stage security-risk-review.md before implementation.",
    ):
        return {
            "status": "present_unverified",
            "write_policy": "read_only",
            "methodology_domains": [{"id": "security", "status": "applicable_missing"}],
            "recommendations": [
                {
                    "domain": "security",
                    "artifact": artifact,
                    "priority": "P1_high_risk",
                    "safe_next_action": safe_next_action,
                }
            ],
            "recommendation_groups": [
                {
                    "artifact": artifact,
                    "owner_domain": "security",
                    "consumer_domains": ["quality_testing_evals"],
                    "priority": "P1_high_risk",
                    "safe_next_action": safe_next_action,
                }
            ],
            "questions_for_owner": ["Who owns the security review?"],
            "methodology_synthesis": {
                "safe_next_action": safe_next_action,
                "semantic_evidence_sufficiency": {
                    "status": "present_unverified",
                    "required_evidence": ["owner-reviewed evidence"],
                },
                "source_artifact_ledger": [
                    {"artifact": artifact, "decision": "canonical_template"}
                ],
            },
        }

    def _write_control_plane(self, workspace: Path, omit: set[str] | None = None) -> None:
        omit = omit or set()
        content = {
            "AGENTS.md": "# Rules\n",
            "REQUIREMENTS.md": "# Requirements\n\n## Acceptance Criteria\n\n- Synthetic acceptance.\n",
            "PLAN.md": "# Plan\n\n## Verification\n\n- Run unit tests.\n",
            "TEST.md": "# Test\n\nQuality gates: unit tests.\n",
            "EVALS.md": "# Evals\n\nQuality gates: fixture eval.\n",
            "RUNLOG.md": "# Runlog\n\nNo active lifecycle marker.\n",
        }
        for name, text in content.items():
            if name not in omit:
                (workspace / name).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
