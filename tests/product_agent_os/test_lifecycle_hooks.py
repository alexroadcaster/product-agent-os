import json
import hashlib
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
HOOKS = ROOT / "plugins" / "product-agent-os" / "assets" / "templates" / "hooks"
LOCAL_HOOKS = ROOT / ".codex" / "hooks"
ACTIVE_HOOKS_JSON = ROOT / ".codex" / "hooks.json"
MIRROR_HOOKS_JSON = LOCAL_HOOKS / "hooks.json"
TEMPLATE_HOOKS_JSON = HOOKS / "hooks.json"
REQUIRED_BRIEF_FIELDS = [
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
]


def run_hook(
    script: Path,
    payload: dict[str, object] | None = None,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps(payload or {}),
        cwd=str(cwd) if cwd is not None else str(ROOT),
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def valid_marker(**overrides: object) -> dict[str, object]:
    marker: dict[str, object] = {
        "task_start_brief_shown": True,
        "completion_brief_shown": False,
        "status": "in_progress",
        "task_id": "DOC-LIFECYCLE-HOOKS-A01",
        "scope": "local hook test",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "approval_boundary": "local workspace only",
        "brief_schema_version": "task_start_brief_v1",
        "brief_format": "field_list",
        "brief_digest": "sha256:" + "0" * 64,
        "brief_fields_present": REQUIRED_BRIEF_FIELDS,
    }
    marker.update(overrides)
    return marker


def write_marker(root: Path, marker: dict[str, object]) -> None:
    state = root / ".codex" / "product-agent-os" / "lifecycle-state.json"
    state.parent.mkdir(parents=True, exist_ok=True)
    state.write_text(json.dumps(marker), encoding="utf-8")


def load_hook_module(script: Path):
    spec = importlib.util.spec_from_file_location(f"test_{script.stem}", script)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load hook module: {script.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LifecycleHooksTest(unittest.TestCase):
    def test_read_only_report_requires_pinned_authority_and_exact_patch(self):
        module = load_hook_module(HOOKS / "pre_tool_use_policy.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = valid_marker(brief_schema_version="task_scope_note_v1", brief_format="concise",
                brief_fields_present=["Scope", "Evidence", "Limits"], scope_note_shown=True,
                previous_task_id="OLD-TASK", lifecycle_scope={"work_type": "research", "size": "bounded", "risk": "low",
                "financially_material": False, "release_or_readiness": False, "explicit_packet_request": False, "reason": "Read-only analysis with exact report"})
            write_marker(root, marker)
            now = datetime.now(timezone.utc)
            grant = {"schema_version": 1, "task_id": marker["task_id"], "previous_task_id": "OLD-TASK",
                "workspace_sha256": hashlib.sha256(os.path.normcase(str(root.resolve())).encode()).hexdigest(),
                "marker_sha256": hashlib.sha256((root / module.LIFECYCLE_STATE_REL).read_bytes()).hexdigest(),
                "output_path": "reports/result.md", "issued_at": now.isoformat(), "expires_at": (now + timedelta(hours=1)).isoformat()}
            authority = root / "authority.json"; authority.write_text(json.dumps(grant), encoding="utf-8")
            digest = hashlib.sha256(authority.read_bytes()).hexdigest()
            patch = "*** Begin Patch\n*** Add File: reports/result.md\n+Observed result\n*** End Patch"
            direct = {"tool_name": "functions.apply_patch", "tool_input": patch}
            nested = {"tool_name": "functions.exec", "tool_input": {"code": "text(await tools.apply_patch(" + json.dumps(patch) + "));"}}
            for payload in (direct, nested):
                self.assertEqual(module._report_action_ok(root, payload, authority, digest), (True, "ok"))
            args = ["--report-authority", str(authority), "--report-authority-sha256", digest]
            env = dict(os.environ, CODEX_HOOK_WORKSPACE_ROOT=str(root))
            def wire(payload, flags=args):
                result = subprocess.run([sys.executable, str(HOOKS / "pre_tool_use_policy.py"), *flags],
                    input=json.dumps(payload), cwd=root, env=env, capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, 0, result.stderr)
                return json.loads(result.stdout) if result.stdout else {}
            for payload in (direct, nested):
                self.assertEqual(wire(payload), {})
            denied = wire({**direct, "report_authority": grant}, [])
            self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")
            for cmd in ("git diff --output reports/neighbor.md", "rg --pre malware pattern", "Get-Content -LiteralPath 'x'; write y"):
                denied = wire({"tool_name": "functions.exec_command", "tool_input": {"cmd": cmd, "login": False}})
                self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")
            read = {"tool_name": "functions.exec_command", "tool_input": {"cmd": "Get-Content -LiteralPath 'README.md'", "login": False}}
            self.assertEqual(wire(read), {})
            self.assertFalse(module._report_read_only({**read, "tool_input": {**read["tool_input"], "shell": "untrusted"}}))
            self.assertFalse(module._report_action_ok(root, direct, authority, "0" * 64)[0])
            for name in ("reports/neighbor.md", "src/code.py", ".codex/config.toml", ".codex/hooks/policy.py", "../result.md", "reports/../reports/result.md", "reports/result.md:stream", "reports/RESULT~1.md"):
                bad = {**direct, "tool_input": patch.replace("reports/result.md", name)}
                self.assertFalse(module._report_action_ok(root, bad, authority, digest)[0], name)
            for code in ('await tools.exec_command({"cmd":"python -c write_target"});', nested["tool_input"]["code"] + ' await tools.exec_command({"cmd":"write"});'):
                self.assertFalse(module._report_action_ok(root, {"tool_name": "functions.exec", "tool_input": {"code": code}}, authority, digest)[0])
            (root / "reports").mkdir(); (root / "reports/result.md").write_text("user content", encoding="utf-8")
            self.assertFalse(module._report_action_ok(root, direct, authority, digest)[0])
            (root / "reports/result.md").unlink()
            for change in ({"status": "ready_for_completion_ledger"}, {"updated_at": (now - timedelta(days=3)).isoformat()}, {"previous_task_id": "WRONG"}):
                write_marker(root, {**marker, **change})
                grant["marker_sha256"] = hashlib.sha256((root / module.LIFECYCLE_STATE_REL).read_bytes()).hexdigest()
                authority.write_text(json.dumps(grant), encoding="utf-8")
                digest = hashlib.sha256(authority.read_bytes()).hexdigest()
                self.assertFalse(module._report_action_ok(root, direct, authority, digest)[0])
            write_marker(root, marker)
            grant["marker_sha256"] = hashlib.sha256((root / module.LIFECYCLE_STATE_REL).read_bytes()).hexdigest()
            for change in ({"expires_at": (now - timedelta(seconds=1)).isoformat()}, {"workspace_sha256": "0" * 64}, {"output_path": "PLAN.md"}):
                authority.write_text(json.dumps({**grant, **change}), encoding="utf-8")
                pin = hashlib.sha256(authority.read_bytes()).hexdigest()
                self.assertFalse(module._report_action_ok(root, direct, authority, pin)[0])

    def test_report_options_do_not_slow_normal_read_only_path(self):
        module = load_hook_module(HOOKS / "pre_tool_use_policy.py")
        payload = {"tool_name": "functions.exec_command", "tool_input": {"cmd": "git status --short"}}
        with mock.patch.object(module, "_read_payload", return_value=(payload, json.dumps(payload))), mock.patch.object(module, "_workspace_root", side_effect=AssertionError("normal read must not resolve workspace")):
            self.assertEqual(module.main([]), 0)

    def test_pre_tool_use_accepts_trade_shaped_start_and_scoped_concise_note(self):
        module = load_hook_module(HOOKS / "pre_tool_use_policy.py")
        scope = {"work_type": "implementation", "size": "large", "risk": "high",
                 "financially_material": False, "release_or_readiness": False,
                 "explicit_packet_request": False, "reason": "Material instruction migration"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = valid_marker(brief_schema_version="task_start_brief_v2", brief_format="bold_fields",
                                  brief_fields_present=["Request", "Goal", "Context", "Scope", "Value", "Execution", "Acceptance", "Risks / approvals", "Next step"],
                                  lifecycle_scope=scope)
            write_marker(root, marker)
            self.assertEqual(module._lifecycle_marker_ok(root / module.LIFECYCLE_STATE_REL), (True, "ok"))
            scope.update(work_type="fix", size="bounded", risk="low", reason="Small local correction")
            marker.update(brief_schema_version="task_scope_note_v1", brief_format="concise",
                          brief_fields_present=["Scope", "Evidence", "Limits"],
                          task_start_brief_shown=False, scope_note_shown=True)
            write_marker(root, marker)
            self.assertEqual(module._lifecycle_marker_ok(root / module.LIFECYCLE_STATE_REL), (True, "ok"))
            for key, value in (("risk", "high"), ("size", "large"), ("explicit_packet_request", True),
                               ("financially_material", True), ("release_or_readiness", True),
                               ("work_type", "review"), ("work_type", "research"), ("work_type", "planning")):
                with self.subTest(key=key, value=value):
                    unsafe = dict(scope, **{key: value})
                    write_marker(root, dict(marker, lifecycle_scope=unsafe))
                    self.assertFalse(module._lifecycle_marker_ok(root / module.LIFECYCLE_STATE_REL)[0])

    def test_stop_does_not_reject_a_complete_answer_for_missing_legacy_heading(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_marker(root, valid_marker(status="ready_for_completion_brief", completion_ready=True))
            env = dict(os.environ, CODEX_HOOK_WORKSPACE_ROOT=str(root))
            result = run_hook(HOOKS / "stop_runlog_reminder.py", {"last_assistant_message": "Task ID: example\nResult status: partial\nWhat was done: inspected\nFiles / artifacts changed: none\nVerification evidence: source read\nResidual risks / accepted gaps: runtime unavailable\nFollow-up: bounded check"}, ROOT, env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_stop_is_advisory_for_ordinary_and_incomplete_reports(self):
        for ready in (False, True):
            with self.subTest(ready=ready), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                write_marker(root, valid_marker(status="ready_for_completion_brief" if ready else "in_progress", completion_ready=ready))
                env = dict(os.environ, CODEX_HOOK_WORKSPACE_ROOT=str(root))
                result = run_hook(HOOKS / "stop_runlog_reminder.py", {"last_assistant_message": "Concise result with evidence and limits."}, ROOT, env)
                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(result.stdout) if result.stdout else {}
                self.assertNotIn("decision", payload)

    def test_project_local_hooks_use_official_codex_shape_and_match_packaged_template(self):
        active = json.loads(ACTIVE_HOOKS_JSON.read_text(encoding="utf-8"))
        self.assertEqual(active, json.loads(MIRROR_HOOKS_JSON.read_text(encoding="utf-8")))
        self.assertEqual(active, json.loads(TEMPLATE_HOOKS_JSON.read_text(encoding="utf-8")))

        hooks = active["hooks"]
        for event in ["SessionStart", "PreToolUse", "PermissionRequest", "PostToolUse", "Stop"]:
            with self.subTest(event=event):
                self.assertIn(event, hooks)
                self.assertTrue(hooks[event])
                for group in hooks[event]:
                    for handler in group["hooks"]:
                        self.assertEqual(handler["type"], "command")
                        self.assertTrue(handler["command"].startswith("python "))
                        self.assertIn("/.codex/hooks/", handler["command"])
                        self.assertEqual(handler["command"], handler["commandWindows"])
                        self.assertGreater(handler["timeout"], 0)
                        self.assertLessEqual(handler["timeout"], 5)
                        self.assertIn("statusMessage", handler)

        self.assertEqual("startup|resume|clear|compact", hooks["SessionStart"][0]["matcher"])
        self.assertIn("apply_patch", hooks["PreToolUse"][0]["matcher"])
        self.assertNotIn("Bash", hooks["PostToolUse"][0]["matcher"])
        self.assertNotIn("matcher", hooks["Stop"][0])

    def test_project_local_hook_scripts_match_packaged_templates(self):
        names = [
            "comment_sufficiency_advisory.py",
            "session_start_context.py",
            "pre_tool_use_policy.py",
            "permission_request_summary.py",
            "post_tool_use_evidence.py",
            "stop_runlog_reminder.py",
        ]
        for name in names:
            with self.subTest(name=name):
                self.assertTrue((LOCAL_HOOKS / name).exists())
                self.assertEqual(
                    (HOOKS / name).read_text(encoding="utf-8"),
                    (LOCAL_HOOKS / name).read_text(encoding="utf-8"),
                )

    def test_project_local_post_tool_use_routes_both_evidence_and_comment_advisory(self):
        data = json.loads(ACTIVE_HOOKS_JSON.read_text(encoding="utf-8"))
        commands = [
            handler["command"]
            for group in data["hooks"]["PostToolUse"]
            for handler in group["hooks"]
        ]
        self.assertIn("post_tool_use_evidence.py", " ".join(commands))
        self.assertIn("comment_sufficiency_advisory.py", " ".join(commands))

    def test_comment_sufficiency_advisory_warns_without_blocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
            (root / "complex_case.py").write_text(
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
            env["CODEX_COMMENT_ADVISORY_ROOT"] = str(root)
            result = run_hook(
                LOCAL_HOOKS / "comment_sufficiency_advisory.py",
                {
                    "tool_name": "apply_patch",
                    "tool_input": {"command": "*** Update File: complex_case.py"},
                },
                ROOT,
                env,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        output = payload["hookSpecificOutput"]
        self.assertEqual("PostToolUse", output["hookEventName"])
        self.assertIn("1 reviewer-only warning", output["additionalContext"])
        self.assertIn("complex_case.py", output["additionalContext"])
        self.assertNotIn(str(root), result.stdout)
        self.assertNotIn("decision", result.stdout)

    def test_comment_sufficiency_advisory_scans_only_current_patch_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
            (root / "simple.py").write_text("def simple():\n    return 1\n", encoding="utf-8")
            (root / "unrelated_complex.py").write_text(
                "def unrelated_complex(value):\n"
                "    total = 0\n"
                "    for item in value:\n"
                "        if item:\n"
                "            total += 1\n"
                "        elif item == 0:\n"
                "            total -= 1\n"
                "    try:\n"
                "        if total > 10 and value:\n"
                "            return total\n"
                "    except TypeError:\n"
                "        return -1\n"
                "    while total < 0:\n"
                "        total += 1\n"
                "    return total\n",
                encoding="utf-8",
            )
            env = os.environ.copy()
            env["CODEX_COMMENT_ADVISORY_ROOT"] = str(root)
            result = run_hook(
                LOCAL_HOOKS / "comment_sufficiency_advisory.py",
                {
                    "tool_name": "apply_patch",
                    "tool_input": {"command": "*** Update File: simple.py"},
                },
                ROOT,
                env,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual("", result.stdout)

    def test_comment_sufficiency_advisory_scans_typescript_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
            (root / "policy.tsx").write_text(
                "export const evaluateAccess = async (value: unknown): Promise<boolean> => {\n"
                "  return Boolean(value);\n"
                "};\n",
                encoding="utf-8",
            )
            env = os.environ.copy()
            env["CODEX_COMMENT_ADVISORY_ROOT"] = str(root)
            result = run_hook(LOCAL_HOOKS / "comment_sufficiency_advisory.py", cwd=ROOT, env=env)

        self.assertEqual(result.returncode, 0, result.stderr)
        message = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("policy.tsx:1 (evaluateAccess)", message)
        self.assertNotIn(str(root), result.stdout)

    def test_comment_sufficiency_no_warning_emits_no_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
            (root / "simple.py").write_text("def simple():\n    return 1\n", encoding="utf-8")
            env = os.environ.copy()
            env["CODEX_COMMENT_ADVISORY_ROOT"] = str(root)
            result = run_hook(LOCAL_HOOKS / "comment_sufficiency_advisory.py", cwd=ROOT, env=env)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual("", result.stdout)

    def test_comment_sufficiency_invalid_root_fails_open_without_absolute_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing_root = Path(tmp) / "missing-workspace"
            env = os.environ.copy()
            env["CODEX_COMMENT_ADVISORY_ROOT"] = str(missing_root)
            result = run_hook(LOCAL_HOOKS / "comment_sufficiency_advisory.py", cwd=ROOT, env=env)

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("failed open", payload["systemMessage"])
        self.assertNotIn(str(missing_root), result.stdout)

    def test_comment_sufficiency_validator_error_fails_open_without_absolute_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
            (root / "broken.py").write_text("def broken(:\n    return 1\n", encoding="utf-8")
            env = os.environ.copy()
            env["CODEX_COMMENT_ADVISORY_ROOT"] = str(root)
            result = run_hook(LOCAL_HOOKS / "comment_sufficiency_advisory.py", cwd=ROOT, env=env)

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("SyntaxError", payload["systemMessage"])
        self.assertNotIn(str(root), result.stdout)

    def test_session_start_uses_official_additional_context_shape(self):
        result = run_hook(HOOKS / "session_start_context.py")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual("SessionStart", payload["hookEventName"])
        context = payload["additionalContext"]
        self.assertIn(".codex/product-agent-os/lifecycle-state.json", context)
        self.assertIn("task_start_brief_v2", context)
        self.assertIn("Risks / approvals", context)
        self.assertIn("Stop is advisory", context)
        self.assertIn("control-plane sync", context)
        self.assertIn("canonical_skill_source=plugins/product-agent-os/skills", context)
        self.assertIn("mixed_source=forbidden", context)
        self.assertIn("sha256=", context)
        self.assertNotIn(str(ROOT), result.stdout)
        self.assertNotIn(".codex/hooks/hooks.json", context)

    def test_permission_request_preserves_normal_approval_prompt(self):
        result = run_hook(HOOKS / "permission_request_summary.py")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("Approval remains undecided", payload["systemMessage"])
        self.assertNotIn("decision", payload)
        self.assertNotIn("hookSpecificOutput", payload)

    def test_post_tool_use_uses_official_additional_context_shape(self):
        result = run_hook(HOOKS / "post_tool_use_evidence.py")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual("PostToolUse", payload["hookEventName"])
        self.assertIn("current-run evidence", payload["additionalContext"])
        self.assertNotIn("decision", payload)

    def test_pre_tool_use_allows_read_only_discovery_without_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_hook(
                HOOKS / "pre_tool_use_policy.py",
                {
                    "tool_name": "shell_command",
                    "tool_input": {"command": "Get-Content PLAN.md | Select-Object -First 20"},
                },
                Path(tmp),
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual("", result.stdout)

    def test_pre_tool_use_read_only_fast_path_skips_workspace_resolution(self):
        module = load_hook_module(LOCAL_HOOKS / "pre_tool_use_policy.py")
        payload = {
            "tool_name": "Bash",
            "tool_input": {"command": "Get-Content PLAN.md | Select-Object -First 20"},
        }
        stdout = io.StringIO()
        with (
            mock.patch.object(module, "_workspace_root", side_effect=AssertionError("workspace lookup is not needed")),
            mock.patch("sys.stdin", io.StringIO(json.dumps(payload))),
            mock.patch("sys.stdout", stdout),
        ):
            result = module.main()

        self.assertEqual(0, result)
        self.assertEqual("", stdout.getvalue())

    def test_pre_tool_use_denies_mutation_without_marker_using_official_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_hook(
                HOOKS / "pre_tool_use_policy.py",
                {
                    "tool_name": "shell_command",
                    "tool_input": {"command": "Set-Content PLAN.md 'updated'"},
                },
                Path(tmp),
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual("PreToolUse", output["hookEventName"])
        self.assertEqual("deny", output["permissionDecision"])
        self.assertIn("missing lifecycle marker", output["permissionDecisionReason"])

    def test_pre_tool_use_allows_mutation_after_current_marker_without_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_marker(root, valid_marker())
            result = run_hook(
                HOOKS / "pre_tool_use_policy.py",
                {
                    "tool_name": "shell_command",
                    "tool_input": {"command": "Set-Content PLAN.md 'updated'"},
                },
                root,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual("", result.stdout)

    def test_pre_tool_use_denies_legacy_marker_without_full_task_brief_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_marker(
                root,
                {
                    "task_start_brief_shown": True,
                    "task_id": "DOC-LIFECYCLE-HOOKS-A01",
                    "scope": "local hook test",
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                    "approval_boundary": "local workspace only",
                },
            )
            result = run_hook(
                LOCAL_HOOKS / "pre_tool_use_policy.py",
                {"tool_name": "shell_command", "tool_input": {"command": "Set-Content PLAN.md 'updated'"}},
                root,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        reason = json.loads(result.stdout)["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("status must be in_progress", reason)

    def test_pre_tool_use_denies_stale_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_marker(root, valid_marker(updated_at=(datetime.now(timezone.utc) - timedelta(hours=49)).isoformat()))
            result = run_hook(
                HOOKS / "pre_tool_use_policy.py",
                {"tool_name": "shell_command", "tool_input": {"command": "Set-Content PLAN.md 'updated'"}},
                root,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        reason = json.loads(result.stdout)["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("stale", reason)

    def test_session_start_marks_stale_in_progress_state_as_recovery_not_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_marker(root, valid_marker(updated_at=(datetime.now(timezone.utc) - timedelta(hours=49)).isoformat()))
            env = os.environ.copy()
            env["CODEX_HOOK_WORKSPACE_ROOT"] = str(root)
            result = run_hook(HOOKS / "session_start_context.py", cwd=ROOT, env=env)

        self.assertEqual(result.returncode, 0, result.stderr)
        context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("lifecycle_state=stale_in_progress", context)
        self.assertIn("action=stop_and_recover_not_resume", context)

    def test_pre_tool_use_denies_completed_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_marker(root, valid_marker(completion_brief_shown=True, status="completed"))
            result = run_hook(
                HOOKS / "pre_tool_use_policy.py",
                {"tool_name": "shell_command", "tool_input": {"command": "Set-Content PLAN.md 'updated'"}},
                root,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        reason = json.loads(result.stdout)["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("completed task", reason)

    def test_pre_tool_use_allows_lifecycle_marker_write_without_existing_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_hook(
                HOOKS / "pre_tool_use_policy.py",
                {
                    "tool_name": "shell_command",
                    "tool_input": {
                        "command": "Set-Content .codex/product-agent-os/lifecycle-state.json '{\"task_start_brief_shown\": true}'"
                    },
                },
                Path(tmp),
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual("", result.stdout)

    def test_concise_marker_bootstrap_and_terminal_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bootstrap = run_hook(HOOKS / "pre_tool_use_policy.py", {
                "tool_name": "shell_command", "tool_input": {
                    "command": 'Set-Content .codex/product-agent-os/lifecycle-state.json \'{"scope_note_shown": true}\''
                }}, root)
            self.assertEqual("", bootstrap.stdout)
            write_marker(root, valid_marker(completion_ready=True))
            result = run_hook(HOOKS / "pre_tool_use_policy.py", {
                "tool_name": "shell_command", "tool_input": {"command": "Set-Content output.txt value"}}, root)
            self.assertEqual("deny", json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"])

    def test_stop_hook_accepts_terminal_completion_brief_without_continuation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = valid_marker(
                status="ready_for_completion_brief",
                completion_status="implemented",
                completion_ready=True,
            )
            write_marker(root, marker)
            env = os.environ.copy()
            env["CODEX_HOOK_WORKSPACE_ROOT"] = str(root)
            result = run_hook(
                HOOKS / "stop_runlog_reminder.py",
                {
                    "stop_hook_active": False,
                    "last_assistant_message": (
                        "Completion Brief\nTask ID: B45-S9-H01\nResult status: implemented\n"
                        "What was done: hooks optimized\nFiles / artifacts changed: hooks and workflow\n"
                        "Verification evidence: focused tests passed\nResidual risks / accepted gaps: trust review pending\n"
                        "Follow-up: review hooks in a fresh session"
                    ),
                },
                ROOT,
                env,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual("", result.stdout)

    def test_stop_hook_never_requests_format_correction_for_a_ready_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_marker(root, valid_marker(status="ready_for_completion_brief", completion_ready=True))
            env = os.environ.copy()
            env["CODEX_HOOK_WORKSPACE_ROOT"] = str(root)
            result = run_hook(
                HOOKS / "stop_runlog_reminder.py",
                {"stop_hook_active": False, "last_assistant_message": "Work finished."},
                ROOT,
                env,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_stop_hook_accepts_blocked_terminal_brief_without_continuation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_marker(root, valid_marker(status="blocked", completion_ready=True))
            env = os.environ.copy()
            env["CODEX_HOOK_WORKSPACE_ROOT"] = str(root)
            result = run_hook(
                HOOKS / "stop_runlog_reminder.py",
                {
                    "stop_hook_active": False,
                    "last_assistant_message": (
                        "Completion Brief\nTask ID: blocked-case\nResult status: blocked\n"
                        "What was done: stopped safely\nFiles / artifacts changed: none\n"
                        "Verification evidence: blocker reproduced\nResidual risks / accepted gaps: unresolved input\n"
                        "Follow-up: owner decision"
                    ),
                },
                ROOT,
                env,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual("", result.stdout)

    def test_stop_hook_does_not_loop_after_continuation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_marker(root, valid_marker(status="ready_for_completion_brief", completion_ready=True))
            env = os.environ.copy()
            env["CODEX_HOOK_WORKSPACE_ROOT"] = str(root)
            result = run_hook(
                HOOKS / "stop_runlog_reminder.py",
                {"stop_hook_active": True, "last_assistant_message": "Still incomplete."},
                ROOT,
                env,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
