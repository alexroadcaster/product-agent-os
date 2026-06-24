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
        self.assertIn("run_self_learning_loop.py", payload["manual_run_command"])
        self.assertEqual(payload["manual_run_command_status"], "available_manual_only")

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

    def test_manual_runner_dry_run_reports_progress_without_workspace_writes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    ".codex/product-agent-os/lifecycle-state.json": "{}\n",
                    ".codex/product-agent-os/self-learning-state.json": json.dumps(
                        {
                            "schema_version": "self_learning_state_v1",
                            "plugin_id": "product-agent-os",
                            "plugin_version": "0.1.0",
                            "installed_at": "2026-06-01T00:00:00+00:00",
                            "last_analysis_at": None,
                            "last_success_at": None,
                            "last_failure_at": None,
                            "next_due_at": None,
                            "cadence_level": "manual_only",
                            "last_report_id": None,
                            "last_metrics_digest": None,
                            "approval_state": "manual_only",
                            "disable_reason": None,
                        },
                        sort_keys=True,
                    )
                    + "\n",
                    "PLAN.md": "# Plan\n",
                    "TEST.md": "# Test\n",
                },
            )
            before = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_self_learning_loop.py"),
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
        self.assertEqual(payload["schema_version"], "self_learning_run_packet_v1")
        self.assertEqual(payload["mode"], "dry_run")
        self.assertEqual(payload["status"], "ready_for_owner_review")
        self.assertTrue(payload["product_agent_os_scope"]["eligible"])
        self.assertEqual(payload["due_check"]["status"], "due")
        self.assertEqual(payload["progress"]["status"], "ready_for_owner_review")
        self.assertIn("scope_check", [event["phase"] for event in payload["progress"]["events"]])
        self.assertFalse(payload["analysis_executed"])
        self.assertFalse(payload["state_written"])
        self.assertEqual(payload["auto_apply"]["status"], "not_enabled")
        self.assertEqual(payload["rendered_artifacts"]["mode"], "dry_run")
        self.assertIn(
            ".codex/product-agent-os/self-learning/self-learning-progress.html",
            payload["rendered_artifacts"]["targets"],
        )
        self.assertEqual(before, after)
        self.assertNotIn(str(workspace), result.stdout)

    def test_manual_runner_stage_writes_progress_and_html_only_under_stage_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir, tempfile.TemporaryDirectory() as stagedir:
            workspace = Path(tmpdir) / "workspace"
            workspace.mkdir()
            stage = Path(stagedir) / "stage"
            self._write_files(
                workspace,
                {
                    ".codex/product-agent-os/lifecycle-state.json": "{}\n",
                    ".codex/product-agent-os/self-learning-state.json": json.dumps(
                        {
                            "schema_version": "self_learning_state_v1",
                            "plugin_id": "product-agent-os",
                            "plugin_version": "0.1.0",
                            "installed_at": "2026-06-01T00:00:00+00:00",
                            "last_analysis_at": None,
                            "last_success_at": None,
                            "last_failure_at": None,
                            "next_due_at": None,
                            "cadence_level": "manual_only",
                            "last_report_id": None,
                            "last_metrics_digest": None,
                            "approval_state": "manual_only",
                            "disable_reason": None,
                        },
                        sort_keys=True,
                    )
                    + "\n",
                },
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_self_learning_loop.py"),
                    str(workspace),
                    "--now",
                    "2026-06-09T00:00:00+00:00",
                    "--stage",
                    str(stage),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            workspace_files = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())
            stage_files = sorted(path.relative_to(stage).as_posix() for path in stage.rglob("*") if path.is_file())
            html = (stage / ".codex/product-agent-os/self-learning/self-learning-progress.html").read_text(encoding="utf-8")
            manifest = (stage / "product-agent-os-stage-manifest.json").read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], "stage")
        self.assertEqual(payload["rendered_artifacts"]["mode"], "stage")
        self.assertIn(".codex/product-agent-os/self-learning/progress.jsonl", stage_files)
        self.assertIn(".codex/product-agent-os/self-learning/self-learning-progress.html", stage_files)
        run_progress = [
            path
            for path in stage_files
            if path.startswith(".codex/product-agent-os/self-learning/runs/") and path.endswith("/progress.json")
        ]
        self.assertEqual(len(run_progress), 1)
        self.assertIn("Generated review view only", html)
        self.assertIn("Self-Learning Loop Progress", html)
        self.assertNotIn("http://", html)
        self.assertNotIn("https://", html)
        self.assertNotIn(str(workspace), html)
        self.assertNotIn(str(workspace), manifest)
        manifest_payload = json.loads(manifest)
        self.assertEqual(manifest_payload["schema_version"], "self_learning_stage_manifest_v1")
        self.assertFalse(manifest_payload["raw_workspace_path_included"])
        self.assertIn("workspace_ref", manifest_payload)
        self.assertEqual(
            workspace_files,
            [
                ".codex/product-agent-os/lifecycle-state.json",
                ".codex/product-agent-os/self-learning-state.json",
            ],
        )

    def test_manual_runner_blocks_disabled_state_without_collecting_later_phases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    ".codex/product-agent-os/lifecycle-state.json": "{}\n",
                    ".codex/product-agent-os/self-learning-state.json": json.dumps(
                        {
                            "schema_version": "self_learning_state_v1",
                            "plugin_id": "product-agent-os",
                            "plugin_version": "0.1.0",
                            "installed_at": "2026-06-01T00:00:00+00:00",
                            "last_analysis_at": None,
                            "last_success_at": None,
                            "last_failure_at": None,
                            "next_due_at": None,
                            "cadence_level": "disabled",
                            "last_report_id": None,
                            "last_metrics_digest": None,
                            "approval_state": "disabled",
                            "disable_reason": "owner disabled",
                        },
                        sort_keys=True,
                    )
                    + "\n",
                },
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_self_learning_loop.py"),
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

        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("self-learning loop is disabled", payload["blockers"])
        phases = [event["phase"] for event in payload["progress"]["events"]]
        self.assertIn("scope_check", phases)
        self.assertIn("due_check", phases)
        self.assertIn("blocked", phases)
        self.assertNotIn("evidence_collect", phases)
        self.assertFalse(payload["analysis_executed"])
        self.assertFalse(payload["state_written"])

    def test_manual_runner_missing_state_does_not_create_state_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    ".codex/product-agent-os/lifecycle-state.json": "{}\n",
                },
            )
            before = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_self_learning_loop.py"),
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

        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("self-learning state is invalid", payload["blockers"])
        self.assertEqual(before, after)
        self.assertNotIn(str(workspace), result.stdout)

    def test_manual_runner_fails_closed_for_out_of_scope_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": '{"name":"regular-app"}\n',
                    "src/app.ts": "export const app = true;\n",
                },
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_self_learning_loop.py"),
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

        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "blocked")
        self.assertFalse(payload["product_agent_os_scope"]["eligible"])
        self.assertIn("scope_check", [event["phase"] for event in payload["progress"]["events"]])
        self.assertIn("Product-Agent OS scope is not eligible", payload["blockers"])
        self.assertFalse(payload["analysis_executed"])
        self.assertFalse(payload["state_written"])
        self.assertNotIn(str(workspace), result.stdout)

    def test_due_check_cli_now_exposes_b44_s2_manual_runner_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    ".codex/product-agent-os/self-learning-state.json": json.dumps(
                        {
                            "schema_version": "self_learning_state_v1",
                            "plugin_id": "product-agent-os",
                            "plugin_version": "0.1.0",
                            "installed_at": "2026-06-01T00:00:00+00:00",
                            "last_analysis_at": None,
                            "last_success_at": None,
                            "last_failure_at": None,
                            "next_due_at": None,
                            "cadence_level": "manual_only",
                            "last_report_id": None,
                            "last_metrics_digest": None,
                            "approval_state": "manual_only",
                            "disable_reason": None,
                        },
                        sort_keys=True,
                    )
                    + "\n",
                },
            )

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

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertIn("run_self_learning_loop.py", payload["manual_run_command"])
        self.assertEqual(payload["manual_run_command_status"], "available_manual_only")
        self.assertNotIn("future_manual_runner", payload)

    def _write_files(self, workspace: Path, files: dict[str, str]) -> None:
        for relative, text in files.items():
            path = workspace / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
