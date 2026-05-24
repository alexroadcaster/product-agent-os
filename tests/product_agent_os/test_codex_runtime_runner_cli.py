import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
WRAPPER = SCRIPTS / "run_codex_runtime_runner.py"
VALIDATOR = SCRIPTS / "validate_codex_runtime_runner.py"


class CodexRuntimeRunnerCliTest(unittest.TestCase):
    def test_contract_cli_returns_route_ready_for_quality_gate_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: quality_gate")
            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--contract"],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(payload["status"], "route_ready")
        self.assertEqual(payload["lifecycle_state"], "quality_gate")
        self.assertEqual(payload["route_packet"]["recommended_skill"], "risk-reviewer")
        self.assertEqual(payload["workspace"], "[REDACTED_LOCAL_PATH]")
        self.assertNotIn(str(workspace), result.stdout)

    def test_contract_cli_requires_contract_flag(self):
        result = subprocess.run(
            [sys.executable, str(WRAPPER), "."],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("choose --contract", result.stderr)

    def test_contract_cli_includes_first_run_usage_mode_for_empty_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            (workspace / "README.md").write_text("# Idea\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--contract"],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "route_ready")
        self.assertEqual(payload["lifecycle_state"], "uninitialized")
        self.assertEqual(payload["route_packet"]["usage_mode"]["primary"], "greenfield_idea")
        self.assertEqual(payload["route_packet"]["first_response_contract"]["mode"], "greenfield_idea")
        self.assertIn("greenfield idea brief", payload["route_packet"]["first_response_contract"]["minimum_artifacts"])
        self.assertIn("minimum artifacts", payload["route_packet"]["first_response_contract"]["required_fields"])
        self.assertIn("evidence gaps", payload["route_packet"]["first_response_contract"]["required_fields"])
        self.assertIn(
            "first-run-empty-greenfield",
            payload["route_packet"]["usage_mode"]["behavioral_eval_cases"],
        )

    def test_contract_cli_returns_needs_approval_for_build_active_without_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: build_active")
            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--contract", "--allow-subagents"],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload["status"], "needs_approval")
        self.assertEqual(payload["route_packet"]["write_policy"], "approved_write")

    def test_contract_cli_blocks_source_policy_blocked_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: quality_gate")
            docs = workspace / "docs"
            docs.mkdir()
            (docs / "guide.md").write_text("# Guide\n\nOpenAI Codex behavior claim.\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--contract"],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["source_policy_status"], "blocked")
        self.assertIn("source_policy:blocked", payload["errors"])

    def test_contract_cli_intent_hint_does_not_bypass_source_policy_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: quality_gate")
            docs = workspace / "docs"
            docs.mkdir()
            (docs / "guide.md").write_text("# Guide\n\nOpenAI Codex behavior claim.\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(WRAPPER),
                    str(workspace),
                    "--contract",
                    "--intent-hint",
                    "release this package now",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["source_policy_status"], "blocked")
        self.assertEqual(payload["route_packet"]["usage_mode"]["primary"], "release_packaging")
        self.assertTrue(payload["route_packet"]["behavioral_route_inputs"]["intent_hint_present"])
        self.assertIn("source_policy:blocked", payload["errors"])

    def test_validator_accepts_valid_result_json_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: quality_gate")
            output = Path(tmp) / "result.json"
            run_result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), "--contract", "--output", str(output)],
                check=False,
                capture_output=True,
                text=True,
            )
            validate_result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(output)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(run_result.returncode, 0)
        self.assertEqual(validate_result.returncode, 0, validate_result.stdout + validate_result.stderr)
        self.assertIn('"ok": true', validate_result.stdout)

    def _write_control_plane(self, workspace: Path, runlog_marker: str) -> None:
        (workspace / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
        (workspace / "REQUIREMENTS.md").write_text(
            "# Requirements\n\n## Acceptance Criteria\n\n- Synthetic.\n",
            encoding="utf-8",
        )
        (workspace / "PLAN.md").write_text("# Plan\n\n## Verification\n\n- Run tests.\n", encoding="utf-8")
        (workspace / "TEST.md").write_text("# Test\n\nQuality gates: unit tests.\n", encoding="utf-8")
        (workspace / "EVALS.md").write_text("# Evals\n\nQuality gates: fixture eval.\n", encoding="utf-8")
        (workspace / "RUNLOG.md").write_text(f"# Runlog\n\n{runlog_marker}\n", encoding="utf-8")
        agents = workspace / ".codex" / "agents"
        agents.mkdir(parents=True)
        (agents / "builder.toml").write_text('name = "builder"\n', encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
