import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOOKS = ROOT / "plugins" / "product-agent-os" / "assets" / "templates" / "hooks"
LOCAL_HOOKS = ROOT / ".codex" / "hooks"
ACTIVE_HOOKS_JSON = ROOT / ".codex" / "hooks.json"


def run_hook(script: Path, payload: dict[str, object] | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps(payload or {}),
        cwd=str(cwd) if cwd is not None else str(ROOT),
        check=False,
        capture_output=True,
        text=True,
    )


class LifecycleHooksTest(unittest.TestCase):
    def test_project_local_hooks_are_installed_with_codex_hooks_shape(self):
        hooks_json = ACTIVE_HOOKS_JSON
        self.assertTrue(hooks_json.exists())

        data = json.loads(hooks_json.read_text(encoding="utf-8"))
        hooks = data["hooks"]
        for event in ["SessionStart", "PreToolUse", "PermissionRequest", "PostToolUse", "Stop"]:
            with self.subTest(event=event):
                self.assertIn(event, hooks)
                self.assertTrue(hooks[event])
                handler = hooks[event][0]["hooks"][0]
                self.assertEqual(handler["type"], "command")
                self.assertTrue(handler["command"].startswith("python "))
                self.assertIn("/.codex/hooks/", handler["command"])
                self.assertIn("statusMessage", handler)

    def test_project_local_hook_scripts_are_installed(self):
        self.assertTrue((LOCAL_HOOKS / "hooks.json").exists())
        for name in [
            "session_start_context.py",
            "pre_tool_use_policy.py",
            "permission_request_summary.py",
            "post_tool_use_evidence.py",
            "stop_runlog_reminder.py",
        ]:
            with self.subTest(name=name):
                self.assertTrue((LOCAL_HOOKS / name).exists())

    def test_session_start_reports_lifecycle_contract_files(self):
        result = run_hook(HOOKS / "session_start_context.py")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["hook"], "session_start_context")
        self.assertEqual(payload["lifecycle"]["state_marker"], ".codex/product-agent-os/lifecycle-state.json")
        self.assertIn("Task Brief", " ".join(payload["reminders"]))
        self.assertIn("control-plane sync", " ".join(payload["reminders"]))

    def test_pre_tool_use_allows_read_only_discovery_without_lifecycle_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_hook(
                HOOKS / "pre_tool_use_policy.py",
                {
                    "tool_name": "functions.shell_command",
                    "tool_input": {"command": "Get-Content PLAN.md | Select-Object -First 20"},
                },
                Path(tmp),
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "observe")
        self.assertFalse(payload["mutating_command_detected"])

    def test_pre_tool_use_blocks_mutating_command_without_lifecycle_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_hook(
                HOOKS / "pre_tool_use_policy.py",
                {
                    "tool_name": "functions.shell_command",
                    "tool_input": {"command": "Set-Content PLAN.md 'updated'"},
                },
                Path(tmp),
            )

        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "block")
        self.assertTrue(payload["mutating_command_detected"])
        self.assertIn("missing_lifecycle_marker", {item["kind"] for item in payload["findings"]})

    def test_pre_tool_use_allows_mutating_command_after_lifecycle_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / ".codex" / "product-agent-os" / "lifecycle-state.json"
            state.parent.mkdir(parents=True)
            state.write_text(
                json.dumps(
                    {
                        "task_start_brief_shown": True,
                        "task_id": "DOC-LIFECYCLE-HOOKS-A01",
                        "scope": "local hook test",
                        "updated_at": "2026-06-20T00:00:00+03:00",
                        "approval_boundary": "local workspace only",
                    }
                ),
                encoding="utf-8",
            )

            result = run_hook(
                HOOKS / "pre_tool_use_policy.py",
                {
                    "tool_name": "functions.shell_command",
                    "tool_input": {"command": "Set-Content PLAN.md 'updated'"},
                },
                root,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "observe")
        self.assertTrue(payload["lifecycle_marker"]["ok"])

    def test_pre_tool_use_allows_lifecycle_marker_write_without_existing_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_hook(
                HOOKS / "pre_tool_use_policy.py",
                {
                    "tool_name": "functions.shell_command",
                    "tool_input": {
                        "command": "Set-Content .codex/product-agent-os/lifecycle-state.json '{\"task_start_brief_shown\": true}'"
                    },
                },
                Path(tmp),
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "observe")
        self.assertTrue(payload["lifecycle_marker"]["marker_write_allowed"])

    def test_stop_hook_reminds_completion_brief_and_control_plane_sync(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_hook(HOOKS / "stop_runlog_reminder.py", cwd=Path(tmp))

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["hook"], "stop_runlog_reminder")
        reminders = " ".join(payload["reminders"])
        self.assertIn("Completion Brief", reminders)
        self.assertIn("control-plane sync", reminders)


if __name__ == "__main__":
    unittest.main()
