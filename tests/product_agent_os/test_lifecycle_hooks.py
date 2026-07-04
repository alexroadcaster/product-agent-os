import json
import os
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
            "comment_sufficiency_advisory.py",
            "session_start_context.py",
            "pre_tool_use_policy.py",
            "permission_request_summary.py",
            "post_tool_use_evidence.py",
            "stop_runlog_reminder.py",
        ]:
            with self.subTest(name=name):
                self.assertTrue((LOCAL_HOOKS / name).exists())

    def test_comment_sufficiency_active_hook_matches_packaged_template(self):
        self.assertEqual(
            (HOOKS / "comment_sufficiency_advisory.py").read_text(encoding="utf-8"),
            (LOCAL_HOOKS / "comment_sufficiency_advisory.py").read_text(encoding="utf-8"),
        )

    def test_project_local_post_tool_use_runs_comment_sufficiency_advisory(self):
        data = json.loads(ACTIVE_HOOKS_JSON.read_text(encoding="utf-8"))
        commands = data["hooks"]["PostToolUse"][0]["hooks"]

        self.assertIn(
            "comment_sufficiency_advisory.py",
            " ".join(command["command"] for command in commands),
        )

    def test_comment_sufficiency_advisory_warns_without_blocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
            path = root / "complex_case.py"
            path.write_text(
                "\n".join(
                    [
                        "def complex_case(value):",
                        "    total = 0",
                        "    for item in value:",
                        "        if item:",
                        "            total += 1",
                        "        elif item == 0:",
                        "            total -= 1",
                        "    try:",
                        "        if total > 10 and value:",
                        "            return total",
                        "    except TypeError:",
                        "        return -1",
                        "    while total < 0:",
                        "        total += 1",
                        "    return total",
                    ]
                ),
                encoding="utf-8",
            )
            env = os.environ.copy()
            env["B45_COMMENT_ADVISORY_ROOT"] = str(root)
            result = subprocess.run(
                [sys.executable, str(LOCAL_HOOKS / "comment_sufficiency_advisory.py")],
                input=json.dumps({"tool_name": "functions.apply_patch"}),
                cwd=ROOT,
                env=env,
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("comment_sufficiency_advisory", payload["hook"])
        self.assertEqual("observe", payload["decision"])
        self.assertFalse(payload["blocking"])
        self.assertEqual("advisory_complete", payload["status"])
        self.assertEqual(1, payload["validator"]["warning_count"])
        self.assertEqual("advisory", payload["validator"]["warnings"][0]["severity"])
        self.assertIn(payload["validator_source_ref"], {"workspace_plugin", "packaged_plugin"})
        self.assertFalse(payload["raw_workspace_path_included"])
        self.assertNotIn("workspace_root", payload)
        self.assertNotIn(str(root), result.stdout)

    def test_comment_sufficiency_advisory_scans_typescript_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
            path = root / "policy.tsx"
            path.write_text(
                "export const evaluateAccess = async (value: unknown): Promise<boolean> => {\n"
                "  return Boolean(value);\n"
                "};\n",
                encoding="utf-8",
            )
            env = os.environ.copy()
            env["B45_COMMENT_ADVISORY_ROOT"] = str(root)
            result = subprocess.run(
                [sys.executable, str(LOCAL_HOOKS / "comment_sufficiency_advisory.py")],
                input=json.dumps({"tool_name": "functions.apply_patch"}),
                cwd=ROOT,
                env=env,
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("advisory_complete", payload["status"])
        self.assertEqual(["policy.tsx"], payload["scanned_paths"])
        self.assertEqual(["evaluateAccess"], [warning["symbol"] for warning in payload["validator"]["warnings"]])
        self.assertNotIn(str(root), result.stdout)

    def test_comment_sufficiency_invalid_root_fails_open_without_absolute_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing_root = Path(tmp) / "missing-workspace"
            env = os.environ.copy()
            env["B45_COMMENT_ADVISORY_ROOT"] = str(missing_root)
            result = subprocess.run(
                [sys.executable, str(LOCAL_HOOKS / "comment_sufficiency_advisory.py")],
                input=json.dumps({"tool_name": "functions.apply_patch"}),
                cwd=ROOT,
                env=env,
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("invalid_workspace_root_fail_open", payload["status"])
        self.assertFalse(payload["blocking"])
        self.assertEqual("unresolved", payload["workspace_ref"])
        self.assertNotIn(str(missing_root), result.stdout)

    def test_comment_sufficiency_validator_error_fails_open_without_absolute_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
            path = root / "broken.py"
            path.write_text("def broken(:\n    return 1\n", encoding="utf-8")
            env = os.environ.copy()
            env["B45_COMMENT_ADVISORY_ROOT"] = str(root)
            result = subprocess.run(
                [sys.executable, str(LOCAL_HOOKS / "comment_sufficiency_advisory.py")],
                input=json.dumps({"tool_name": "functions.apply_patch"}),
                cwd=ROOT,
                env=env,
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("validator_error_fail_open", payload["status"])
        self.assertFalse(payload["blocking"])
        self.assertEqual("SyntaxError", payload["error_type"])
        self.assertNotIn(str(root), result.stdout)

    def test_session_start_reports_lifecycle_contract_files(self):
        result = run_hook(HOOKS / "session_start_context.py")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["hook"], "session_start_context")
        self.assertEqual(payload["lifecycle"]["state_marker"], ".codex/product-agent-os/lifecycle-state.json")
        self.assertEqual(payload["lifecycle"]["task_start_brief_schema_version"], "task_start_brief_v1")
        self.assertIn("Product value", payload["lifecycle"]["task_start_brief_required_fields"])
        self.assertIn("Next action", payload["lifecycle"]["task_start_brief_required_fields"])
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
                        "brief_schema_version": "task_start_brief_v1",
                        "brief_format": "field_list",
                        "brief_digest": "sha256:0123456789abcdef",
                        "brief_fields_present": [
                            "Task ID",
                            "Product value",
                            "Technical value",
                            "Source / trigger",
                            "Scope",
                            "Non-goals",
                            "Agents and skills",
                            "Files / artifacts expected",
                            "Verification gate",
                            "Approval boundary / risks",
                            "Complexity",
                            "Estimated execution time",
                            "Next action",
                        ],
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

    def test_pre_tool_use_blocks_legacy_marker_without_full_task_brief_fields(self):
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

        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "block")
        self.assertFalse(payload["lifecycle_marker"]["ok"])
        self.assertIn("brief_schema_version", payload["lifecycle_marker"]["reason"])

    def test_project_local_pre_tool_use_blocks_legacy_marker_without_full_task_brief_fields(self):
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
                LOCAL_HOOKS / "pre_tool_use_policy.py",
                {
                    "tool_name": "functions.shell_command",
                    "tool_input": {"command": "Set-Content PLAN.md 'updated'"},
                },
                root,
            )

        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["decision"], "block")
        self.assertFalse(payload["lifecycle_marker"]["ok"])
        self.assertIn("brief_schema_version", payload["lifecycle_marker"]["reason"])

    def test_pre_tool_use_allows_full_task_brief_marker_with_required_fields(self):
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
                        "brief_schema_version": "task_start_brief_v1",
                        "brief_format": "field_list",
                        "brief_digest": "sha256:0123456789abcdef",
                        "brief_fields_present": [
                            "Task ID",
                            "Product value",
                            "Technical value",
                            "Source / trigger",
                            "Scope",
                            "Non-goals",
                            "Agents and skills",
                            "Files / artifacts expected",
                            "Verification gate",
                            "Approval boundary / risks",
                            "Complexity",
                            "Estimated execution time",
                            "Next action",
                        ],
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
        self.assertEqual(payload["lifecycle_marker"]["brief_schema_version"], "task_start_brief_v1")

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
        self.assertIn("compact or incomplete", reminders)
        self.assertIn("control-plane sync", reminders)


if __name__ == "__main__":
    unittest.main()
