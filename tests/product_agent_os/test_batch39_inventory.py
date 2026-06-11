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


from product_agent_os.batch39_inventory import (  # noqa: E402
    build_batch39_inventory,
    validate_batch39_inventory,
)


class Batch39InventoryTests(unittest.TestCase):
    def test_builds_redacted_source_cache_package_session_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            plugin_root = workspace / "plugins" / "product-agent-os"
            cache_root = Path(tmp) / "cache" / "product-agent-os" / "0.1.0"
            _write_fixture_workspace(workspace, plugin_root, cache_root)

            packet = build_batch39_inventory(
                workspace=workspace,
                plugin_root=plugin_root,
                cache_roots=[cache_root],
                generated_at="2026-06-11T00:00:00+00:00",
            )

            self.assertEqual(packet["schema_version"], "batch39_inventory_v1")
            self.assertEqual(set(packet["inventory"].keys()), {"source", "cache", "package", "session"})
            self.assertEqual(packet["inventory"]["source"]["skill_count"], 1)
            self.assertEqual(packet["inventory"]["package"]["manifest"]["name"], "product-agent-os")
            self.assertEqual(packet["inventory"]["package"]["manifest"]["version"], "0.1.0")
            self.assertEqual(packet["inventory"]["cache"]["roots"][0]["status"], "present")
            self.assertEqual(packet["inventory"]["cache"]["roots"][0]["skill_count"], 1)
            self.assertEqual(packet["inventory"]["session"]["agent_count"], 1)
            self.assertEqual(packet["inventory"]["session"]["workflow_count"], 1)
            self.assertEqual(packet["approval_boundary"]["external_actions"], "not_performed")
            self.assertEqual(packet["generated_view_policy"], "orientation_only_not_proof")

            encoded = json.dumps(packet, ensure_ascii=False)
            self.assertNotIn(str(workspace), encoded)
            self.assertNotIn(str(cache_root), encoded)
            self.assertEqual(validate_batch39_inventory(packet), [])

    def test_validation_rejects_missing_categories_and_local_paths(self) -> None:
        packet = {
            "schema_version": "batch39_inventory_v1",
            "inventory": {"source": {}, "cache": {}, "package": {}},
            "leak": r"D:\Projects\secret\repo",
        }

        errors = validate_batch39_inventory(packet)

        self.assertIn("missing inventory category: session", errors)
        self.assertIn("source.status missing or invalid", errors)
        self.assertIn("cache.status missing or invalid", errors)
        self.assertIn("package.manifest_present must be boolean", errors)
        self.assertIn("local absolute path leaked", errors)

    def test_cache_inventory_digest_distinguishes_same_file_count_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            plugin_root = workspace / "plugins" / "product-agent-os"
            cache_root = Path(tmp) / "cache" / "product-agent-os" / "0.1.0"
            other_cache_root = Path(tmp) / "cache" / "product-agent-os" / "0.1.1"
            _write_fixture_workspace(workspace, plugin_root, cache_root)
            _write_fixture_workspace(workspace, plugin_root, other_cache_root)
            (other_cache_root / "skills" / "explorer" / "SKILL.md").write_text(
                "---\nname: explorer\nversion: changed\n---\n",
                encoding="utf-8",
            )

            packet = build_batch39_inventory(
                workspace=workspace,
                plugin_root=plugin_root,
                cache_roots=[cache_root, other_cache_root],
                generated_at="2026-06-11T00:00:00+00:00",
            )

            digests = [root["inventory_digest"] for root in packet["inventory"]["cache"]["roots"]]
            self.assertEqual(2, len(set(digests)))

    def test_cli_writes_inventory_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            plugin_root = workspace / "plugins" / "product-agent-os"
            cache_root = Path(tmp) / "cache" / "product-agent-os" / "0.1.0"
            output = workspace / "docs" / "superpowers" / "specs" / "inventory.json"
            _write_fixture_workspace(workspace, plugin_root, cache_root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "collect_batch39_inventory.py"),
                    "--workspace",
                    str(workspace),
                    "--plugin-root",
                    str(plugin_root),
                    "--cache-root",
                    str(cache_root),
                    "--output",
                    str(output),
                    "--generated-at",
                    "2026-06-11T00:00:00+00:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            packet = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(validate_batch39_inventory(packet), [])
            self.assertIn('"status": "ok"', result.stdout)


def _write_fixture_workspace(workspace: Path, plugin_root: Path, cache_root: Path) -> None:
    for path in [
        plugin_root / ".codex-plugin",
        plugin_root / "skills" / "explorer",
        plugin_root / "assets" / "templates" / "workflows",
        plugin_root / "assets" / "templates" / "agents",
        workspace / ".codex" / "agents",
        workspace / ".codex" / "workflows",
        workspace / "docs" / "superpowers" / "specs",
        cache_root / ".codex-plugin",
        cache_root / "skills" / "explorer",
    ]:
        path.mkdir(parents=True, exist_ok=True)

    manifest = {
        "name": "product-agent-os",
        "version": "0.1.0",
        "skills": "./skills",
        "mcpServers": "./.mcp.json",
    }
    (plugin_root / ".codex-plugin" / "plugin.json").write_text(json.dumps(manifest), encoding="utf-8")
    (plugin_root / ".mcp.json").write_text('{"mcpServers":{"context7":{}}}', encoding="utf-8")
    (plugin_root / "skills" / "explorer" / "SKILL.md").write_text("---\nname: explorer\n---\n", encoding="utf-8")
    (plugin_root / "assets" / "templates" / "workflows" / "source-context-pack.md").write_text(
        "# Source Context Pack\n",
        encoding="utf-8",
    )
    (plugin_root / "assets" / "templates" / "agents" / "explorer.toml").write_text(
        'name = "explorer"\n',
        encoding="utf-8",
    )
    (workspace / ".codex" / "agents" / "explorer.toml").write_text('name = "explorer"\n', encoding="utf-8")
    (workspace / ".codex" / "workflows" / "source-context-pack.md").write_text(
        "# Source Context Pack\n",
        encoding="utf-8",
    )
    (workspace / ".codex" / "config.toml").write_text("[project]\n", encoding="utf-8")
    (workspace / ".rules").write_text("allow read\n", encoding="utf-8")
    (cache_root / ".codex-plugin" / "plugin.json").write_text(json.dumps(manifest), encoding="utf-8")
    (cache_root / ".mcp.json").write_text('{"mcpServers":{"context7":{}}}', encoding="utf-8")
    (cache_root / "skills" / "explorer" / "SKILL.md").write_text("---\nname: explorer\n---\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
