import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
WRAPPER = SCRIPTS / "run_codex_runtime_runner.py"
VALIDATOR = SCRIPTS / "validate_codex_runtime_runner.py"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner import cli as runtime_cli  # noqa: E402
from codex_runtime_runner.contracts import build_result  # noqa: E402


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

    def test_contract_run_redacts_methodology_route_payload_before_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, "lifecycle_state: quality_gate")
            audit = self._audit(
                methodology_intelligence=self._methodology_intelligence(
                    safe_next_action="TOKEN=fixture-secret\nInspect C:\\Users\\person\\project\nraw private chat log",
                    question="Can C:\\Users\\person\\project be inspected?",
                )
            )
            with patch.object(runtime_cli, "analyze_workspace", return_value=audit):
                payload = runtime_cli.run_contract(workspace)

        text = json.dumps(payload, sort_keys=True)
        self.assertNotIn("fixture-secret", text)
        self.assertNotIn("C:\\Users\\person", text)
        self.assertNotIn("raw private chat log", text)
        self.assertIn("secret", payload["redactions"]["categories"])
        self.assertNotIn("redaction:secret_retained", payload["errors"])

    def test_validator_rejects_malformed_methodology_packet_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "result.json"
            payload = build_result(
                status="route_ready",
                workspace="C:/workspace/synthetic",
                lifecycle_state="quality_gate",
                route_packet={
                    "write_policy": "read_only",
                    "methodology_packet": {"write_policy": "staged_only"},
                },
                source_policy_status="ok",
                approval_status="not_required",
                next_action="Run risk-reviewer.",
            )
            output.write_text(json.dumps(payload), encoding="utf-8")
            validate_result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(output)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(validate_result.returncode, 1)
        self.assertIn("methodology_packet.safe_next_action:required", validate_result.stdout)
        self.assertNotIn("Traceback", validate_result.stdout + validate_result.stderr)

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

    def _audit(self, *, methodology_intelligence: dict):
        return {
            "usage_mode": {
                "primary": "maintenance",
                "secondary": [],
                "confidence": "medium",
                "reasons": ["synthetic patched audit"],
                "fallback": "standard_feature",
                "first_response_contract": [
                    "mode",
                    "confidence",
                    "next smallest action",
                    "minimum artifacts",
                    "evidence gaps",
                    "approval boundary",
                ],
                "minimum_artifacts": ["workspace audit packet"],
                "behavioral_eval_cases": ["route-selection"],
            },
            "route_inputs": {
                "intent_hint_present": False,
                "workspace_signals": {
                    "stack": [],
                    "active_surfaces": [],
                    "methodology_signals": [],
                },
                "control_plane_state": {
                    "existing_control_plane_files": [],
                    "has_codex_assets": False,
                },
            },
            "methodology_intelligence": methodology_intelligence,
        }

    def _methodology_intelligence(self, *, safe_next_action: str, question: str = "Who owns the decision?"):
        return {
            "status": "present_unverified",
            "write_policy": "read_only",
            "methodology_domains": [{"id": "security", "status": "applicable_missing"}],
            "recommendations": [
                {
                    "domain": "security",
                    "artifact": "security-risk-review.md",
                    "priority": "P1_high_risk",
                    "safe_next_action": safe_next_action,
                }
            ],
            "recommendation_groups": [
                {
                    "artifact": "security-risk-review.md",
                    "owner_domain": "security",
                    "consumer_domains": ["quality_testing_evals"],
                    "priority": "P1_high_risk",
                    "safe_next_action": safe_next_action,
                }
            ],
            "questions_for_owner": [question],
            "methodology_synthesis": {
                "safe_next_action": safe_next_action,
                "semantic_evidence_sufficiency": {"status": "present_unverified"},
                "source_artifact_ledger": [
                    {"artifact": "security-risk-review.md", "decision": "canonical_template"}
                ],
            },
        }


if __name__ == "__main__":
    unittest.main()
