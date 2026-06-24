from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


class SelfLearningStateTests(unittest.TestCase):
    def test_default_state_is_manual_only_and_due_without_running_analysis(self) -> None:
        from product_agent_os.self_learning_state import build_default_self_learning_state, evaluate_self_learning_due

        state = build_default_self_learning_state(
            plugin_version="0.1.0",
            installed_at="2026-06-01T00:00:00+00:00",
        )
        due = evaluate_self_learning_due(state, now="2026-06-08T00:00:00+00:00")

        self.assertEqual(state["schema_version"], "self_learning_state_v1")
        self.assertEqual(state["cadence_level"], "manual_only")
        self.assertEqual(state["approval_state"], "manual_only")
        self.assertEqual(due["status"], "due")
        self.assertEqual(due["action"], "manual_run_available")
        self.assertFalse(due["analysis_executed"])
        self.assertFalse(due["state_written"])
        self.assertEqual(due["trigger_policy"]["schedule_status"], "not_created")
        self.assertEqual(due["due_basis"], "manual_only")

    def test_weekly_state_is_not_due_before_next_due_at_and_uses_last_success(self) -> None:
        from product_agent_os.self_learning_state import build_default_self_learning_state, evaluate_self_learning_due

        state = build_default_self_learning_state(
            plugin_version="0.1.0",
            installed_at="2026-06-01T00:00:00+00:00",
            cadence_level="weekly",
        )
        state["last_success_at"] = "2026-06-10T10:00:00+03:00"

        due = evaluate_self_learning_due(state, now="2026-06-16T06:59:00+00:00")

        self.assertEqual(due["status"], "not_due")
        self.assertEqual(due["due_basis"], "last_success_at_plus_7_days")
        self.assertEqual(due["next_due_at"], "2026-06-17T07:00:00Z")

    def test_on_change_state_is_not_due_without_change_trigger(self) -> None:
        from product_agent_os.self_learning_state import build_default_self_learning_state, evaluate_self_learning_due

        state = build_default_self_learning_state(
            plugin_version="0.1.0",
            installed_at="2026-06-01T00:00:00+00:00",
            cadence_level="on_change",
        )

        due = evaluate_self_learning_due(state, now="2026-06-24T00:00:00+00:00")

        self.assertEqual(due["status"], "not_due")
        self.assertEqual(due["action"], "wait_for_product_agent_os_change")
        self.assertIsNone(due["next_due_at"])

    def test_disabled_state_is_not_due_and_names_disable_reason(self) -> None:
        from product_agent_os.self_learning_state import build_default_self_learning_state, evaluate_self_learning_due

        state = build_default_self_learning_state(
            plugin_version="0.1.0",
            installed_at="2026-06-01T00:00:00+00:00",
            approval_state="disabled",
            disable_reason="owner disabled during install",
        )
        due = evaluate_self_learning_due(state, now="2026-06-15T00:00:00+00:00")

        self.assertEqual(due["status"], "disabled")
        self.assertEqual(due["disable_reason"], "owner disabled during install")
        self.assertFalse(due["analysis_executed"])

    def test_malformed_state_returns_state_invalid(self) -> None:
        from product_agent_os.self_learning_state import evaluate_self_learning_due

        due = evaluate_self_learning_due({"schema_version": "wrong"}, now="2026-06-08T00:00:00+00:00")

        self.assertEqual(due["status"], "state_invalid")
        self.assertIn("schema_version:invalid", due["errors"])
        self.assertFalse(due["analysis_executed"])

    def test_due_check_cli_reads_state_without_writing_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            state_dir = workspace / ".codex" / "product-agent-os"
            state_dir.mkdir(parents=True)
            state_path = state_dir / "self-learning-state.json"
            state_path.write_text(
                json.dumps(
                    {
                        "schema_version": "self_learning_state_v1",
                        "plugin_id": "product-agent-os",
                        "plugin_version": "0.1.0",
                        "installed_at": "2026-06-01T00:00:00+00:00",
                        "last_analysis_at": None,
                        "last_success_at": None,
                        "last_failure_at": None,
                        "next_due_at": None,
                        "cadence_level": "weekly",
                        "last_report_id": None,
                        "last_metrics_digest": None,
                        "approval_state": "manual_only",
                        "disable_reason": None,
                    },
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            before = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "check_self_learning_due.py"),
                    str(workspace),
                    "--now",
                    "2026-06-09T00:00:00+00:00",
                    "--dry-run",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            after = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "due")
        self.assertEqual(payload["mode"], "dry_run")
        self.assertFalse(payload["analysis_executed"])
        self.assertFalse(payload["state_written"])
        self.assertEqual(before, after)
        self.assertNotIn(str(workspace), result.stdout)
        self.assertNotIn("run_self_learning_loop.py", payload["manual_run_command"])

    def test_due_check_cli_invalid_now_returns_bounded_json_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "check_self_learning_due.py"),
                    str(workspace),
                    "--now",
                    "not-a-date",
                    "--dry-run",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "state_invalid")
        self.assertIn("now:invalid_datetime", payload["errors"])
        self.assertNotIn("Traceback", result.stderr + result.stdout)
        self.assertNotIn(str(workspace), result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
