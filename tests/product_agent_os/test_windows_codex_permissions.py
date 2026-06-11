import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
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


class WindowsCodexPermissionsTest(unittest.TestCase):
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
        self.assertEqual(payload["status"], "unsupported")


if __name__ == "__main__":
    unittest.main()
