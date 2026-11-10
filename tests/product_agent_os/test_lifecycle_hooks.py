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
    # Synthetic fixtures must not inherit the parent repository via git discovery.
    hook_env = os.environ.copy()
    hook_env.update(env or {})
    if cwd is not None and (env is None or "CODEX_HOOK_WORKSPACE_ROOT" not in env):
        hook_env["CODEX_HOOK_WORKSPACE_ROOT"] = str(cwd)
    return subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps(payload or {}),
        cwd=str(cwd) if cwd is not None else str(ROOT),
        env=hook_env,
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
    def test_terminal_local_validation_commands_keep_exact_scope(self):
        commands = [
            ("python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/tasks.md", {}, False),
            ("python -B plugins/product-agent-os/scripts/validate_task_state_consistency.py .", {}, False),
            ("git -c core.safecrlf=false diff --check", {}, False),
            ("python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/tasks.md", {"workdir": "other"}, True),
            ("python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/tasks.md", {"shell": "custom-shell"}, True),
            ("python -B plugins/product-agent-os/scripts/validate_task_matrix.py --write", {}, True),
            ("python -B plugins/product-agent-os/scripts/validate_task_matrix.py ../tasks.md", {}, True),
            ("python -B plugins/product-agent-os/scripts/validate_task_matrix.py tasks.md extra", {}, True),
            ("python plugins/product-agent-os/scripts/validate_task_matrix.py tasks.md", {}, True),
            ("python -B other/validate_task_matrix.py tasks.md", {}, True),
            ("python -B plugins/product-agent-os/scripts/sync_task_documents.py apply", {}, True),
            ("python -c 'write()'", {}, True),
            ("python -B plugins/product-agent-os/scripts/validate_task_matrix.py tasks.md; Set-Content other x", {}, True),
            ("git -c core.safecrlf=false diff --check --output=other", {}, True),
            ("git -c core.pager=other diff --check", {}, True),
            ("git -c core.safecrlf=false apply patch", {}, True),
        ]
        for script in (HOOKS, LOCAL_HOOKS):
            module = load_hook_module(script / "pre_tool_use_policy.py")
            for command, extra, denied in commands:
                with self.subTest(script=script, command=command, extra=extra):
                    payload = {"tool_name": "functions.exec_command", "cwd": str(ROOT),
                               "tool_input": {"cmd": command, **extra}}
                    output = io.StringIO()
                    with mock.patch.object(module, "_read_payload", return_value=(payload, "")), \
                         mock.patch.object(module, "_workspace_root", return_value=ROOT), \
                         mock.patch.object(module, "_lifecycle_marker_ok", return_value=(False, "terminal")), \
                         mock.patch("sys.stdout", output):
                        self.assertEqual(module.main([]), 0)
                    self.assertEqual(bool(output.getvalue()), denied, output.getvalue())

    def test_g7_terminal_wire_allows_only_literal_default_shell_reads(self):
        for script in (HOOKS, LOCAL_HOOKS):
            module = load_hook_module(script / 'pre_tool_use_policy.py')
            for command, extra, denied in [
                ("rg -n 'a|b' README.md", {}, False),
                ("Get-Content README.md | Select-String -SimpleMatch 'a'", {}, False),
                ("rg pattern README.md", {'shell': 'custom-shell'}, True),
                ("rg pattern README.md|Set-Content other x", {}, True),
                ("Get-Content README.md\nSet-Content other x", {}, True),
                ("rg -n 'x\" --pre placeholder \"suffix with more' file", {}, True),
                (r"rg \--pre placeholder file", {}, True),
            ]:
                payload = {'tool_name': 'functions.exec_command', 'tool_input': {'cmd': command, **extra}}
                output = io.StringIO()
                with mock.patch.object(module, '_read_payload', return_value=(payload, '')), \
                     mock.patch.object(module, '_workspace_root', return_value=ROOT), \
                     mock.patch.object(module, '_lifecycle_marker_ok', return_value=(False, 'terminal')), \
                     mock.patch('sys.stdout', output):
                    self.assertEqual(module.main([]), 0)
                self.assertEqual(bool(output.getvalue()), denied, (command, output.getvalue()))

    def test_g7_literal_read_classifier_preserves_mutation_boundary(self):
        allowed = [
            "Get-Content PLAN.md; Get-Content TEST.md",
            "rg -n 'status; planned' PLAN.md | Select-Object -First 3",
            "rg -n 'PAOS-AUD-G7|planned' PLAN.md",
            "rg -F '|' PLAN.md",
            "Get-Content PLAN.md | Select-String -SimpleMatch '|'",
            "Get-Content PLAN.md | Select-String -SimpleMatch 'PAOS-AUD-G7'",
            "Get-Content PLAN.md | Select-Object -Skip 2 -First 4",
        ]
        denied = [
            "Get-Content PLAN.md; python -c 'write()'",
            "Get-Content PLAN.md;; Get-Content TEST.md",
            "rg-evil pattern file", "Get-Content-Evil file",
            "rg --pre script pattern file", "rg --p're' script pattern file",
            'rg "$(Write-Output bad)" file', "rg 'unterminated file",
            "Get-Content file | Out-File other", "Get-Content file > other",
            "Get-Content file; Set-Content other x", "rg --% pattern file",
            "rg pattern file|Set-Content other x",
            "rg -n @probeArgs file",
            "Get-Content '/etc/passwd' | Select-String root",
        ]
        for script in (HOOKS, LOCAL_HOOKS):
            module = load_hook_module(script / "pre_tool_use_policy.py")
            for command in allowed:
                with self.subTest(script=script.name, command=command):
                    self.assertTrue(module._is_read_only(command))
            for command in denied:
                with self.subTest(script=script.name, command=command):
                    self.assertFalse(module._is_read_only(command))

    def test_command_payload_excludes_tool_metadata_and_unknown_tools_need_scope(self):
        module = load_hook_module(HOOKS / "pre_tool_use_policy.py")
        payload = {"tool_name": "functions.exec_command", "tool_input": {
            "cmd": "Get-Content README.md", "workdir": "project", "justification": "read source"}}
        self.assertEqual("Get-Content README.md", module._command_text(payload, ""))
        self.assertTrue(module._is_mutating("unknown_write_tool", "Get-Content README.md"))


    def test_patch_prose_is_not_an_executable_command(self):
        module = load_hook_module(HOOKS / "pre_tool_use_policy.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_marker(root, valid_marker())
            for path, denied in (("report.md", False), ("../outside.md", True), (".env", True)):
                patch = f"*** Begin Patch\n*** Add File: {path}\n+Never execute git reset --hard or rm -rf.\n*** End Patch"
                payload = {"tool_name": "apply_patch", "tool_input": patch}
                self.assertEqual(denied, bool(module._safety_reasons(root, payload, patch)))
            self.assertTrue(module._safety_reasons(root,
                {"tool_name": "exec_command", "tool_input": {"cmd": "git reset --hard"}}, ""))
            self.assertFalse(module._safety_reasons(root,
                {"tool_name": "exec_command", "tool_input": {"cmd": "rg 'git reset --hard' docs"}}, ""))

    def test_pinned_authoring_updates_exact_report_and_rejects_conflicts(self):
        module = load_hook_module(HOOKS / "pre_tool_use_policy.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            session = "author-chat"
            payload = {"tool_name": "functions.exec", "session_id": session}
            marker_path = module.lifecycle_marker_path(root, payload)
            marker_path.parent.mkdir(parents=True)
            marker = valid_marker(session_id=session, brief_schema_version="task_scope_note_v1",
                brief_format="concise", brief_fields_present=["Scope", "Evidence", "Limits"],
                scope_note_shown=True, lifecycle_scope={"work_type": "report_authoring", "size": "bounded",
                "risk": "low", "financially_material": False, "release_or_readiness": False,
                "explicit_packet_request": False, "reason": "Explicit one-report authoring"})
            marker_path.write_text(json.dumps(marker), encoding="utf-8")
            now = datetime.now(timezone.utc)
            grant = {"schema_version": 2, "task_id": marker["task_id"], "session_id": session,
                "workspace_sha256": hashlib.sha256(os.path.normcase(str(root)).encode()).hexdigest(),
                "marker_sha256": hashlib.sha256(marker_path.read_bytes()).hexdigest(),
                "output_path": "report.md", "issued_at": now.isoformat(),
                "expires_at": (now + timedelta(hours=1)).isoformat()}
            authority = root / "authority.json"
            def check(patch, previous="absent", change=None, owner=session):
                authority.write_text(json.dumps({**grant, **(change or {})}), encoding="utf-8")
                pin = hashlib.sha256(authority.read_bytes()).hexdigest()
                code = "// paos-report-previous-sha256: " + previous + "\nawait tools.apply_patch(" + json.dumps(patch) + ");"
                return module._report_authoring_action_ok(root,
                    {**payload, "session_id": owner, "tool_input": code}, authority, pin)
            add = "*** Begin Patch\n*** Add File: report.md\n+first\n*** End Patch"
            self.assertEqual((True, "ok"), check(add))
            report = root / "report.md"
            report.write_bytes(b"first\n")
            update = "*** Begin Patch\n*** Update File: report.md\n@@\n-first\n+second\n*** End of File\n*** End Patch"
            previous = hashlib.sha256(report.read_bytes()).hexdigest()
            self.assertEqual((True, "ok"), check(update, previous))
            report.write_bytes(b"second\n")
            self.assertFalse(check(update, previous)[0], "concurrent edit must conflict")
            update2 = update.replace("-first", "-second").replace("+second", "+third")
            previous = hashlib.sha256(report.read_bytes()).hexdigest()
            self.assertEqual((True, "ok"), check(update2, previous))
            for bad in (update2.replace("report.md", "neighbor.md"),
                        update2.replace("report.md", "./report.md"),
                        update2.replace("*** End Patch", "*** Add File: other.md\n+x\n*** End Patch")):
                self.assertFalse(check(bad, previous)[0])
            self.assertFalse(check(update2, previous, owner="foreign-chat")[0])
            self.assertFalse(check(update2, previous, {"expires_at": now.isoformat()})[0])
            self.assertFalse(check(update2, previous, {"schema_version": 1})[0])
            self.assertFalse(check(update2, previous, {"marker_sha256": "0" * 64})[0])
            with mock.patch.object(Path, "is_symlink", return_value=True):
                self.assertFalse(check(update2, previous)[0])
            with mock.patch.object(Path, "is_junction", return_value=True, create=True):
                self.assertFalse(check(update2, previous)[0])
            # Exercise trusted flag dispatch as well as the contract function.
            code = "// paos-report-previous-sha256: " + previous + "\nawait tools.apply_patch(" + json.dumps(update2) + ");"
            authority.write_text(json.dumps(grant), encoding="utf-8")
            pin = hashlib.sha256(authority.read_bytes()).hexdigest()
            wire_payload = {**payload, "tool_input": code}
            with mock.patch.object(module, "_read_payload", return_value=(wire_payload, "")), \
                 mock.patch.object(module, "_workspace_root", return_value=root), \
                 mock.patch("sys.stdout", new_callable=io.StringIO) as output:
                module.main(["--report-authoring", str(authority), "--report-authoring-sha256", pin])
                self.assertEqual("", output.getvalue())
            self.assertFalse(module._lifecycle_marker_ok(marker_path, expected_session_id=session)[0])
            marker.update(completion_ready=True)
            marker_path.write_text(json.dumps(marker), encoding="utf-8")
            grant["marker_sha256"] = hashlib.sha256(marker_path.read_bytes()).hexdigest()
            self.assertFalse(check(update2, previous)[0])

    def test_read_classification_rejects_compound_and_unknown_writes(self):
        module = load_hook_module(HOOKS / "pre_tool_use_policy.py")
        for command in ("Get-Content README.md; Set-Content result.txt x",
                        "rg example . > result.txt", "git diff --output=result.txt",
                        "python -c \"open('result.txt', 'w').write('x')\"",
                        "Get-Content $(Set-Content result.txt x)", "unknown-writer result.txt"):
            with self.subTest(command=command):
                self.assertFalse(module._is_read_only(command))
                self.assertTrue(module._is_mutating("exec_command", command))
        self.assertTrue(module._is_read_only("Get-Content README.md"))

    def test_session_markers_isolate_parallel_chats_and_ignore_shared_terminal(self):
        for hooks in (HOOKS, LOCAL_HOOKS):
            with self.subTest(hooks=hooks), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                write_marker(root, valid_marker(completion_ready=True))
                for session, terminal in (("chat-a", False), ("chat-b", True)):
                    path = root / ".codex/product-agent-os" / (
                        "lifecycle-state." + hashlib.sha256(session.encode()).hexdigest() + ".json"
                    )
                    path.write_text(json.dumps(valid_marker(
                        session_id=session, completion_ready=terminal
                    )), encoding="utf-8")
                for session, allowed in (("chat-a", True), ("chat-b", False), ("chat-c", False)):
                    result = run_hook(hooks / "pre_tool_use_policy.py", {
                        "session_id": session, "cwd": str(root), "tool_name": "apply_patch",
                        "tool_input": {"command": "*** Begin Patch\n*** Add File: report.md\n+hello\n*** End Patch"}
                    }, root)
                    self.assertEqual(0, result.returncode, result.stderr)
                    if allowed:
                        self.assertEqual("", result.stdout)
                    else:
                        self.assertEqual("deny", json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"])

    def test_session_identity_cannot_be_spoofed_from_tool_input_or_foreign_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_marker(root, valid_marker())
            session = "chat-a"
            path = root / ".codex/product-agent-os" / (
                "lifecycle-state." + hashlib.sha256(session.encode()).hexdigest() + ".json"
            )
            path.write_text(json.dumps(valid_marker(session_id="chat-b")), encoding="utf-8")
            for supplied in (session, "../escape", "", None, 123):
                with self.subTest(session=supplied):
                    result = run_hook(HOOKS / "pre_tool_use_policy.py", {
                        "session_id": supplied, "cwd": str(root), "tool_name": "apply_patch",
                        "tool_input": {"command": "*** Begin Patch\n*** Add File: report.md\n+hello\n*** End Patch",
                                       "session_id": "chat-b"}
                    }, root)
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertTrue(result.stdout, "Invalid or foreign session identity must produce a denial")
                    self.assertEqual("deny", json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"])

    def test_session_start_and_stop_use_the_same_session_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_marker(root, valid_marker(task_id="FOREIGN", completion_ready=True))
            session = "chat-a"
            filename = "lifecycle-state." + hashlib.sha256(session.encode()).hexdigest() + ".json"
            path = root / ".codex/product-agent-os" / filename
            path.write_text(json.dumps(valid_marker(task_id="OWN", session_id=session)), encoding="utf-8")
            env = os.environ.copy()
            env["CODEX_HOOK_WORKSPACE_ROOT"] = str(root)
            for hooks in (HOOKS, LOCAL_HOOKS):
                start = run_hook(hooks / "session_start_context.py", {"session_id": session}, root, env)
                self.assertEqual(0, start.returncode, start.stderr)
                context = json.loads(start.stdout)["hookSpecificOutput"]["additionalContext"]
                self.assertIn(filename, context)
                self.assertIn("task_id=OWN", context)
                self.assertNotIn("task_id=FOREIGN", context)
                stop = run_hook(hooks / "stop_runlog_reminder.py", {"session_id": session}, root, env)
                self.assertIn("systemMessage", json.loads(stop.stdout))
            path.write_text(json.dumps(valid_marker(
                task_id="OWN", session_id=session, completion_ready=True, status="ready_for_completion_brief"
            )), encoding="utf-8")
            stop = run_hook(HOOKS / "stop_runlog_reminder.py", {"session_id": session}, root, env)
            self.assertEqual("", stop.stdout)

    def test_marker_bootstrap_is_exact_and_session_bound(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            own = ".codex/product-agent-os/lifecycle-state." + hashlib.sha256(b"chat-a").hexdigest() + ".json"
            other = ".codex/product-agent-os/lifecycle-state." + hashlib.sha256(b"chat-b").hexdigest() + ".json"
            patches = [
                (f"*** Begin Patch\n*** Add File: {own}\n+{{\"scope_note_shown\": true}}\n*** End Patch", True),
                (f"*** Begin Patch\n*** Add File: {other}\n+{{\"scope_note_shown\": true}}\n*** End Patch", False),
                (f"*** Begin Patch\n*** Add File: report.md\n+.codex/product-agent-os/lifecycle-state.json scope_note_shown\n*** End Patch", False),
                (f"*** Begin Patch\n*** Add File: {own}\n+{{\"scope_note_shown\": true}}\n*** Add File: report.md\n+hello\n*** End Patch", False),
            ]
            for patch, allowed in patches:
                with self.subTest(allowed=allowed, patch=patch):
                    result = run_hook(HOOKS / "pre_tool_use_policy.py", {
                        "session_id": "chat-a", "cwd": str(root), "tool_name": "apply_patch",
                        "tool_input": {"command": patch}
                    }, root)
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertEqual(not allowed, bool(result.stdout), result.stdout)

            # An active own marker must not authorize patches to another chat's state.
            write_marker(root, valid_marker(completion_ready=True))
            (root / own).write_text(json.dumps(valid_marker(session_id="chat-a")), encoding="utf-8")
            for patch, _ in patches[1::2]:
                result = run_hook(HOOKS / "pre_tool_use_policy.py", {
                    "session_id": "chat-a", "cwd": str(root), "tool_name": "apply_patch",
                    "tool_input": {"command": patch}
                }, root)
                self.assertIn("only this session", result.stdout)
            if os.name == "nt":
                result = run_hook(HOOKS / "pre_tool_use_policy.py", {
                    "session_id": "chat-a", "cwd": str(root), "tool_name": "apply_patch",
                    "tool_input": {"command": patches[1][0].replace(other, other.upper())}
                }, root)
                self.assertIn("only this session", result.stdout)

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
            session_payload = {**direct, "session_id": "report-chat"}
            session_marker = module.lifecycle_marker_path(root, session_payload)
            session_marker.write_text(json.dumps({**marker, "session_id": "report-chat"}), encoding="utf-8")
            session_grant = {**grant, "marker_sha256": hashlib.sha256(session_marker.read_bytes()).hexdigest()}
            session_authority = root / "session-authority.json"
            session_authority.write_text(json.dumps(session_grant), encoding="utf-8")
            session_pin = hashlib.sha256(session_authority.read_bytes()).hexdigest()
            self.assertEqual(module._report_action_ok(root, session_payload, session_authority, session_pin), (True, "ok"))
            self.assertFalse(module._report_action_ok(root, {**session_payload, "session_id": "another-chat"}, session_authority, session_pin)[0])
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
