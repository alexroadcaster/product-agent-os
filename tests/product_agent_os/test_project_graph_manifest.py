import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_graph_manifest import (  # noqa: E402
    build_project_graph_manifest,
    collect_project_files,
)


class ProjectGraphManifestTest(unittest.TestCase):
    def test_manifest_records_stable_fingerprints_and_changed_sets_without_absolute_path_leak(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            (workspace / "app.py").write_text("print('v1')\n", encoding="utf-8")
            (workspace / "generated.lock").write_text("generated lock\n", encoding="utf-8")

            first_files = collect_project_files(workspace)
            first = build_project_graph_manifest(workspace, first_files)
            second = build_project_graph_manifest(workspace, collect_project_files(workspace), previous_manifest=first)
            (workspace / "app.py").write_text("print('v2')\n", encoding="utf-8")
            (workspace / "new.py").write_text("print('new')\n", encoding="utf-8")
            (workspace / "generated.lock").unlink()
            third = build_project_graph_manifest(workspace, collect_project_files(workspace), previous_manifest=first)

            self.assertEqual(first["schema_version"], 1)
            self.assertEqual(first["write_policy"], "read_only")
            self.assertEqual(first["root_fingerprint"], second["root_fingerprint"])
            self.assertEqual(second["changes"]["unchanged"], ["app.py", "generated.lock"])
            self.assertEqual(second["freshness"]["status"], "current")
            self.assertEqual(third["changes"]["changed"], ["app.py"])
            self.assertEqual(third["changes"]["added"], ["new.py"])
            self.assertEqual(third["changes"]["deleted"], ["generated.lock"])
            self.assertEqual(third["freshness"]["status"], "changed")
            self.assertEqual(third["workspace"]["name"], "workspace")
            self.assertNotIn(str(workspace), str(third))

    def test_collect_project_files_ignores_low_value_directories_and_classifies_generated_files(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            (workspace / "src").mkdir(parents=True)
            (workspace / "node_modules" / "pkg").mkdir(parents=True)
            (workspace / ".git").mkdir()
            (workspace / "dist").mkdir()
            (workspace / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")
            (workspace / "node_modules" / "pkg" / "index.js").write_text("ignored\n", encoding="utf-8")
            (workspace / "dist" / "bundle.js").write_text("compiled\n", encoding="utf-8")
            (workspace / "openapi.generated.yaml").write_text("openapi: 3.0.0\n", encoding="utf-8")

            files = collect_project_files(workspace)
            by_path = {item["relative_path"]: item for item in files}

            self.assertIn("src/app.py", by_path)
            self.assertNotIn("node_modules/pkg/index.js", by_path)
            self.assertNotIn(".git", by_path)
            self.assertTrue(by_path["openapi.generated.yaml"]["generated"])
            self.assertEqual(by_path["src/app.py"]["language"], "python")

    def test_collect_project_files_skips_symlink_escape_without_crashing(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            outside = Path(tmp) / "outside"
            workspace.mkdir()
            outside.write_text("outside\n", encoding="utf-8")
            link = workspace / "escape.py"
            try:
                link.symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            (workspace / "inside.py").write_text("print('inside')\n", encoding="utf-8")

            files = collect_project_files(workspace)

            paths = {item["relative_path"] for item in files}
            self.assertIn("inside.py", paths)
            self.assertNotIn("escape.py", paths)

    def test_collect_project_files_honors_max_files_without_materializing_everything(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            for index in range(5):
                (workspace / f"file_{index}.py").write_text(f"print({index})\n", encoding="utf-8")

            files = collect_project_files(workspace, max_files=2)
            manifest = build_project_graph_manifest(workspace, files)

            self.assertEqual(len(files), 2)
            self.assertTrue(manifest["summary"]["truncated"])
            self.assertEqual(manifest["summary"]["omitted_count"], 3)

    def test_manifest_reads_git_provenance_when_available_and_records_build_metadata(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            git = workspace / ".git"
            (git / "refs" / "heads").mkdir(parents=True)
            commit = "a" * 40
            (git / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
            (git / "refs" / "heads" / "main").write_text(commit + "\n", encoding="utf-8")
            (workspace / "app.py").write_text("print('ok')\n", encoding="utf-8")

            manifest = build_project_graph_manifest(workspace, collect_project_files(workspace))

            self.assertEqual(manifest["provenance"]["branch"], "main")
            self.assertEqual(manifest["provenance"]["commit"], commit)
            self.assertEqual(manifest["provenance"]["worktree"], "present")
            self.assertEqual(manifest["build_metadata"]["builder"], "product-agent-os-project-code-graph")
            self.assertEqual(manifest["build_metadata"]["schema_version"], 1)

    def test_manifest_reads_linked_git_worktree_provenance_when_git_is_file(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            actual_git = Path(tmp) / "actual-git"
            workspace.mkdir()
            (actual_git / "refs" / "heads").mkdir(parents=True)
            commit = "b" * 40
            (workspace / ".git").write_text(f"gitdir: {actual_git}\n", encoding="utf-8")
            (actual_git / "HEAD").write_text("ref: refs/heads/worktree-branch\n", encoding="utf-8")
            (actual_git / "refs" / "heads" / "worktree-branch").write_text(commit + "\n", encoding="utf-8")
            (workspace / "app.py").write_text("print('ok')\n", encoding="utf-8")

            manifest = build_project_graph_manifest(workspace, collect_project_files(workspace))

            self.assertEqual(manifest["provenance"]["branch"], "worktree-branch")
            self.assertEqual(manifest["provenance"]["commit"], commit)
            self.assertEqual(manifest["provenance"]["worktree"], "linked")


if __name__ == "__main__":
    unittest.main()
