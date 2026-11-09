import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
SCRIPT = SCRIPTS / "prepare_windows_codex_permissions.py"

sys.path.insert(0, str(SCRIPTS))

from product_agent_os.windows_codex_permissions import (  # noqa: E402
    PRODUCT_AGENT_OS_WRITABLE_CODEX_DIRS,
    SENSITIVE_CODEX_PATHS,
    build_permission_plan,
    check_permissions,
)
from product_agent_os import windows_codex_permissions as permissions


class WindowsCodexPermissionsTest(unittest.TestCase):
    def test_failed_repair_restores_snapshot_and_preserves_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / ".codex/runlogs"
            target.mkdir(parents=True)
            backup = root / "backup.txt"
            calls = []
            def run(path, *args):
                calls.append(args)
                if args[0] == "/save":
                    Path(args[1]).write_bytes(b"original ACL")
                if args[0] == "/remove:d":
                    raise subprocess.CalledProcessError(1, "synthetic icacls")
            with mock.patch.object(permissions, "IS_WINDOWS", True), \
                 mock.patch.object(permissions, "_acl_text", return_value="original ACL"), \
                 mock.patch.object(permissions, "_run_icacls", side_effect=run):
                plan = permissions.build_repair_plan(root, ".codex/runlogs", "S-1-5-21-123")
                result = permissions.apply_permissions(root, target=".codex/runlogs", sid="S-1-5-21-123",
                    plan_digest=plan["plan_digest"], backup=backup)
                self.assertEqual("blocked", result["status"])
                self.assertEqual("restored", result["rollback"]["status"])
                self.assertEqual(("/restore", str(backup)), calls[-1])
                self.assertEqual(b"original ACL", backup.read_bytes())
                with self.assertRaises(ValueError):
                    permissions.restore_permissions(root, ".codex/runlogs", backup, "0" * 64)

    def test_apply_without_exact_reviewed_plan_cannot_run_acl_commands(self):
        with mock.patch.object(permissions, "_run_icacls") as run:
            result = permissions.apply_permissions(ROOT)
        self.assertEqual(result["status"], "blocked")
        run.assert_not_called()

    def test_repair_plan_and_apply_bind_target_sid_acl_and_rollback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / ".codex/runlogs"
            target.mkdir(parents=True)
            sid = "S-1-5-21-123"
            calls = []
            def run(path, *args):
                calls.append((path, args))
                if args[0] == "/save":
                    Path(args[1]).write_bytes(b"synthetic ACL snapshot")
            with mock.patch.object(permissions, "_acl_text", return_value="other SID DENY; selected SID DENY"), \
                 mock.patch.object(permissions, "_run_icacls", side_effect=run), \
                 mock.patch.object(permissions, "IS_WINDOWS", True):
                plan = permissions.build_repair_plan(root, ".codex/runlogs", sid)
                backup = root / "acl-backup.txt"
                result = permissions.apply_permissions(root, target=".codex/runlogs", sid=sid,
                    plan_digest=plan["plan_digest"], backup=backup)
                self.assertEqual("applied", result["status"], result)
                self.assertEqual([(target, ("/save", str(backup))),
                                  (target, ("/inheritance:d",)),
                                  (target, ("/remove:d", "*" + sid))], calls)
                restored = permissions.restore_permissions(root, ".codex/runlogs", backup,
                    result["backup_sha256"])
                self.assertEqual("restored", restored["status"])
                self.assertEqual((target.parent, ("/restore", str(backup))), calls[-1])

    def test_repair_rejects_drift_unexpected_targets_and_reparse(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".codex/runlogs").mkdir(parents=True)
            with mock.patch.object(permissions, "_acl_text", return_value="ACL"), \
                 mock.patch.object(permissions, "_run_icacls") as run, \
                 mock.patch.object(permissions, "IS_WINDOWS", True):
                for target in (".codex/runlogs", ".codex/hooks", "../outside", ".codex/../runlogs"):
                    result = permissions.apply_permissions(root, target=target, sid="S-1-5-21-123",
                        plan_digest="0" * 64, backup=root / "snapshot")
                    self.assertEqual("blocked", result["status"])
                with mock.patch.object(Path, "is_symlink", return_value=True):
                    with self.assertRaises(ValueError):
                        permissions.build_repair_plan(root, ".codex/runlogs", "S-1-5-21-123")
                run.assert_not_called()
    def test_plan_names_scoped_product_agent_os_paths(self):
        plan = build_permission_plan(ROOT)

        self.assertEqual(plan["config_profile"], "product-agent-os-project")
        self.assertEqual(plan["config_entries"][".codex"], "read")
        for path in PRODUCT_AGENT_OS_WRITABLE_CODEX_DIRS:
            self.assertEqual(plan["config_entries"][path], "write")
        for path in SENSITIVE_CODEX_PATHS:
            self.assertIn(path, plan["not_opened_by_default"])

    def test_sensitive_paths_are_not_opened_by_default(self):
        opened = set(PRODUCT_AGENT_OS_WRITABLE_CODEX_DIRS)

        self.assertNotIn(".codex/config.toml", opened)
        self.assertNotIn(".codex/hooks", opened)
        self.assertNotIn(".codex/automations", opened)
        self.assertNotIn(".codex/plugins", opened)

    def test_check_is_read_only_and_reports_missing_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".codex").mkdir()

            result = check_permissions(root)

            self.assertEqual(result["status"], "checked")
            self.assertFalse((root / ".codex" / "agents").exists())
            by_path = {item["path"]: item for item in result["dirs"]}
            self.assertFalse(by_path[".codex/agents"]["exists"])

    def test_cli_check_prints_json(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(ROOT)],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "checked")
        self.assertIn(".codex/product-agent-os", payload["managed_write_dirs"])

    @unittest.skipIf(os.name == "nt", "non-Windows guard only")
    def test_apply_is_rejected_on_non_windows(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(ROOT), "--apply"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
