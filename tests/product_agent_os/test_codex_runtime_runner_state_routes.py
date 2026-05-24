import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.context_loader import load_control_plane_context  # noqa: E402
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

    def test_build_active_uses_builder_subagent_and_requires_approval(self):
        route = plan_route("build_active", allow_subagents=True)

        self.assertEqual(route["recommended_skill"], "")
        self.assertEqual(route["recommended_subagent_role"], "builder")
        self.assertEqual(route["write_policy"], "approved_write")
        self.assertTrue(route["approval_requirements"])

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
