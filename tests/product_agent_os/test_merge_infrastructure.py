import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
WRAPPER = SCRIPTS / "merge_infrastructure.py"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.merge_infrastructure import (  # noqa: E402
    ROLLBACK_MANIFEST_NAME,
    MergeInfrastructureError,
    apply_merge_plan,
    build_merge_plan,
    rollback_merge,
)
from product_agent_os.stage_manifest import (  # noqa: E402
    APPROVAL_TEMPLATE_NAME,
    MANIFEST_NAME,
    content_digest,
)


class MergeInfrastructureTest(unittest.TestCase):
    def test_plan_is_read_only_and_needs_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            before = _relative_files(workspace)

            plan = build_merge_plan(workspace, stage_root)

            self.assertEqual(_relative_files(workspace), before)
            self.assertEqual(plan["status"], "needs_approval")
            self.assertRegex(plan["id"], r"^merge-plan-sha256:[0-9a-f]{64}$")
            self.assertEqual(plan["blocked"], [])
            self.assertEqual(plan["decisions"][0]["action"], "create_file")
            self.assertTrue(plan["decisions"][0]["approval_required"])
            self.assertEqual(plan["approval_template_path"], str(stage_root / APPROVAL_TEMPLATE_NAME))
            self.assertTrue((stage_root / APPROVAL_TEMPLATE_NAME).exists())

    def test_missing_stage_manifest_raises_clean_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)

            with self.assertRaises(MergeInfrastructureError) as error:
                build_merge_plan(workspace, stage_root)

            self.assertIn("stage manifest", str(error.exception))

    def test_path_traversal_staged_manifest_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, "AGENTS.md", "content\n")
            _write_raw_manifest(stage_root, [_entry("../AGENTS.md", "AGENTS.md")])

            with self.assertRaises(MergeInfrastructureError) as error:
                build_merge_plan(workspace, stage_root)

            self.assertIn("escapes", str(error.exception))

    def test_plan_blocks_stage_manifest_for_different_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_a = Path(tmp) / "workspace-a"
            workspace_b = Path(tmp) / "workspace-b"
            stage_root = Path(tmp) / "stage"
            workspace_a.mkdir()
            workspace_b.mkdir()
            stage_root.mkdir()
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(
                stage_root,
                [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")],
                workspace=workspace_a,
            )

            plan = build_merge_plan(workspace_b, stage_root)

            self.assertEqual(plan["status"], "blocked")
            self.assertIn("workspace", " ".join(plan["blocked"]))
            self.assertFalse(plan["decisions"][0]["approval_required"])

    def test_plan_blocks_stale_workspace_audit_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            (workspace / "AGENTS.md").write_text("# Added after staging\n", encoding="utf-8")

            plan = build_merge_plan(workspace, stage_root)

            self.assertEqual(plan["status"], "blocked")
            self.assertIn("workspace audit digest", " ".join(plan["blocked"]))
            self.assertFalse(plan["decisions"][0]["approval_required"])

    @unittest.skipIf(not hasattr(os, "symlink"), "symlink unsupported")
    def test_symlink_escape_blocked_where_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            outside = Path(tmp) / "outside.md"
            outside.write_text("outside\n", encoding="utf-8")
            try:
                os.symlink(outside, workspace / "AGENTS.md")
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink creation unsupported: {exc}")
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])

            plan = build_merge_plan(workspace, stage_root)

            self.assertEqual(plan["status"], "blocked")
            self.assertEqual(plan["decisions"][0]["action"], "blocked")
            self.assertIn("symlink", " ".join(plan["blocked"]))

    @unittest.skipIf(not hasattr(os, "symlink"), "symlink unsupported")
    def test_broken_target_symlink_blocks_plan_and_apply_without_writing_outside(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            outside = Path(tmp) / "missing-outside.md"
            try:
                os.symlink(outside, workspace / "AGENTS.md")
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink creation unsupported: {exc}")
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            approval = _approval_file(stage_root, "blocked-plan", [], [])

            plan = build_merge_plan(workspace, stage_root)
            with self.assertRaises(MergeInfrastructureError) as error:
                apply_merge_plan(workspace, stage_root, approval)

            self.assertEqual(plan["status"], "blocked")
            self.assertEqual(plan["decisions"][0]["action"], "blocked")
            self.assertIn("symlink", " ".join(plan["blocked"]))
            self.assertIn("symlink", str(error.exception))
            self.assertFalse(outside.exists())
            self.assertTrue((workspace / "AGENTS.md").is_symlink())

    def test_apply_rejects_missing_approval_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])

            with self.assertRaises(MergeInfrastructureError) as error:
                apply_merge_plan(workspace, stage_root, stage_root / "missing-approval.json")

            self.assertIn("approval file", str(error.exception))

    def test_apply_rejects_bare_plan_id_and_mismatched_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            plan = build_merge_plan(workspace, stage_root)
            bare = stage_root / "bare.json"
            bare.write_text(json.dumps(plan["id"]), encoding="utf-8")
            mismatched = _approval_file(stage_root, "wrong-plan", ["AGENTS.md"], ["create_file"])

            with self.assertRaises(MergeInfrastructureError) as bare_error:
                apply_merge_plan(workspace, stage_root, bare)
            with self.assertRaises(MergeInfrastructureError) as mismatch_error:
                apply_merge_plan(workspace, stage_root, mismatched)

            self.assertIn("approval record", str(bare_error.exception))
            self.assertIn("does not match", str(mismatch_error.exception))

    def test_apply_creates_approved_greenfield_files_and_rollback_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(stage_root, plan["id"], ["AGENTS.md"], ["create_file"])

            result = apply_merge_plan(workspace, stage_root, approval)

            self.assertEqual(result["status"], "applied")
            self.assertTrue((workspace / "AGENTS.md").exists())
            self.assertIn("Generated rules.", (workspace / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertEqual(result["rollback_manifest"], str(stage_root / ROLLBACK_MANIFEST_NAME))
            self.assertTrue((stage_root / ROLLBACK_MANIFEST_NAME).exists())

    def test_apply_rejects_parent_child_target_conflict_before_any_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, "_staged/parent-file", "parent file\n")
            _stage_file(stage_root, "_staged/child-file", "child file\n")
            _write_manifest(
                stage_root,
                [
                    _entry("parent", "_staged/parent-file"),
                    _entry("parent/child.md", "_staged/child-file"),
                ],
            )
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(
                stage_root,
                plan["id"],
                ["parent", "parent/child.md"],
                ["create_file"],
            )

            with self.assertRaises(MergeInfrastructureError) as error:
                apply_merge_plan(workspace, stage_root, approval)

            self.assertIn("target conflict", str(error.exception))
            self.assertFalse((workspace / "parent").exists())

    def test_apply_rejects_windows_case_only_target_conflict_before_any_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, "_staged/Foo.md", "upper\n")
            _stage_file(stage_root, "_staged/foo.md", "lower\n")
            _write_manifest(
                stage_root,
                [
                    _entry("Foo.md", "_staged/Foo.md"),
                    _entry("foo.md", "_staged/foo.md"),
                ],
            )
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(
                stage_root,
                plan["id"],
                ["Foo.md", "foo.md"],
                ["create_file"],
            )

            with self.assertRaises(MergeInfrastructureError) as error:
                apply_merge_plan(workspace, stage_root, approval)

            self.assertIn("target conflict", str(error.exception))
            self.assertFalse((workspace / "Foo.md").exists())
            self.assertFalse((workspace / "foo.md").exists())

    def test_cli_apply_rollback_manifest_path_directory_returns_json_error_before_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(stage_root, plan["id"], ["AGENTS.md"], ["create_file"])
            (stage_root / ROLLBACK_MANIFEST_NAME).mkdir()

            result = subprocess.run(
                [
                    sys.executable,
                    str(WRAPPER),
                    str(workspace),
                    str(stage_root),
                    "--apply",
                    "--approval-file",
                    str(approval),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stderr, "")
            self.assertNotIn("Traceback", result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn("rollback manifest", payload["error"])
            self.assertFalse((workspace / "AGENTS.md").exists())

    def test_failed_multi_target_apply_leaves_rollback_manifest_rollbackable(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            (workspace / "AGENTS.md").write_text("# Local rules\n", encoding="utf-8")
            _stage_file(stage_root, "README.md", "# Created first\n")
            staged_agents = (
                "# Generated\n\n"
                "<!-- product-agent-os:start project-rules -->\n"
                "Generated rules.\n"
                "<!-- product-agent-os:start project-rules -->\n"
                "Nested marker.\n"
                "<!-- product-agent-os:end project-rules -->\n"
                "<!-- product-agent-os:end project-rules -->\n"
            )
            _stage_file(stage_root, "AGENTS.md", staged_agents)
            _write_manifest(
                stage_root,
                [
                    _entry("README.md", "README.md"),
                    _entry("AGENTS.md", "AGENTS.md", managed_section="project-rules"),
                ],
            )
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(
                stage_root,
                plan["id"],
                ["README.md", "AGENTS.md"],
                ["append_managed_section", "create_file"],
            )

            with self.assertRaises(MergeInfrastructureError):
                apply_merge_plan(workspace, stage_root, approval)

            rollback_path = stage_root / ROLLBACK_MANIFEST_NAME
            manifest = json.loads(rollback_path.read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["entries"]), 1)
            self.assertEqual(manifest["entries"][0]["target_path"], "README.md")
            self.assertRegex(manifest["entries"][0]["digest_after"], r"^sha256:[0-9a-f]{64}$")
            rollback_merge(workspace, rollback_path)
            self.assertFalse((workspace / "README.md").exists())
            self.assertEqual((workspace / "AGENTS.md").read_text(encoding="utf-8"), "# Local rules\n")

    def test_cli_apply_corrupt_rollback_backup_root_returns_json_error_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            (workspace / "AGENTS.md").write_text("# Local rules\n", encoding="utf-8")
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(stage_root, plan["id"], ["AGENTS.md"], ["append_managed_section"])
            (stage_root / "_rollback").write_text("not a directory\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(WRAPPER),
                    str(workspace),
                    str(stage_root),
                    "--apply",
                    "--approval-file",
                    str(approval),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stderr, "")
            self.assertNotIn("Traceback", result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn("backup", payload["error"])
            self.assertEqual((workspace / "AGENTS.md").read_text(encoding="utf-8"), "# Local rules\n")

    def test_stale_target_digest_blocks_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            (workspace / "AGENTS.md").write_text("# Existing\n", encoding="utf-8")
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(stage_root, plan["id"], ["AGENTS.md"], ["append_managed_section"])
            (workspace / "AGENTS.md").write_text("# Existing\n\nChanged.\n", encoding="utf-8")

            with self.assertRaises(MergeInfrastructureError) as error:
                apply_merge_plan(workspace, stage_root, approval)

            self.assertIn("stale", str(error.exception))

    def test_apply_rejects_approval_when_current_plan_id_changed_by_stage_manifest_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            old_plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(stage_root, old_plan["id"], ["AGENTS.md"], ["create_file"])

            _stage_file(stage_root, "README.md", "# Companion proposal\n")
            _write_manifest(
                stage_root,
                [
                    _entry("AGENTS.md", "AGENTS.md", managed_section="project-rules"),
                    _entry("README.md", "README.md"),
                ],
            )

            with self.assertRaises(MergeInfrastructureError) as error:
                apply_merge_plan(workspace, stage_root, approval)

            self.assertIn("merge_plan_id", str(error.exception))

    def test_existing_agents_without_marker_appends_managed_section_preserving_user_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            original = "# Local rules\n\nDo not delete this.\n"
            (workspace / "AGENTS.md").write_text(original, encoding="utf-8")
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(stage_root, plan["id"], ["AGENTS.md"], ["append_managed_section"])

            apply_merge_plan(workspace, stage_root, approval)

            updated = (workspace / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn(original.strip(), updated)
            self.assertIn("<!-- product-agent-os:start project-rules -->", updated)
            self.assertIn("Generated rules.", updated)

    def test_existing_config_toml_remains_companion_only_and_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            original = 'model = "user-choice"\n'
            (workspace / ".codex").mkdir()
            (workspace / ".codex" / "config.toml").write_text(original, encoding="utf-8")
            _stage_file(stage_root, "_proposals/.codex__config.toml.product-agent-os-proposal", 'model = "generated"\n')
            _write_manifest(
                stage_root,
                [_entry(".codex/config.toml", "_proposals/.codex__config.toml.product-agent-os-proposal")],
            )

            plan = build_merge_plan(workspace, stage_root)
            result = apply_merge_plan(workspace, stage_root, _approval_file(stage_root, plan["id"], [], []))

            self.assertEqual(plan["decisions"][0]["action"], "companion_only")
            self.assertEqual(result["status"], "applied")
            self.assertEqual((workspace / ".codex" / "config.toml").read_text(encoding="utf-8"), original)

    def test_unapproved_hooks_json_remains_companion_only_and_not_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, ".codex/hooks/hooks.json", "{}\n")
            _write_manifest(stage_root, [_entry(".codex/hooks/hooks.json", ".codex/hooks/hooks.json")])
            plan = build_merge_plan(workspace, stage_root)
            result = apply_merge_plan(workspace, stage_root, _approval_file(stage_root, plan["id"], [], []))

            self.assertEqual(plan["decisions"][0]["action"], "companion_only")
            self.assertEqual(result["status"], "applied")
            self.assertFalse((workspace / ".codex" / "hooks" / "hooks.json").exists())

    def test_enable_hooks_true_writes_hooks_json_only_when_target_absent_and_approved(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, ".codex/hooks/hooks.json", '{"SessionStart": []}\n')
            _write_manifest(stage_root, [_entry(".codex/hooks/hooks.json", ".codex/hooks/hooks.json")])
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(
                stage_root,
                plan["id"],
                [".codex/hooks/hooks.json"],
                ["create_file"],
                enable_hooks=True,
                approved_hook_events=["SessionStart"],
            )

            result = apply_merge_plan(workspace, stage_root, approval)

            self.assertEqual(result["status"], "applied")
            self.assertTrue((workspace / ".codex" / "hooks" / "hooks.json").exists())

    def test_enable_hooks_true_requires_full_hook_approval_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, ".codex/hooks/hooks.json", "{}\n")
            _write_manifest(stage_root, [_entry(".codex/hooks/hooks.json", ".codex/hooks/hooks.json")])
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(
                stage_root,
                plan["id"],
                [".codex/hooks/hooks.json"],
                ["create_file"],
                enable_hooks=True,
                approved_hook_events=["SessionStart"],
                blocking_hooks=[],
                hook_rollback="",
            )

            with self.assertRaises(MergeInfrastructureError) as error:
                apply_merge_plan(workspace, stage_root, approval)

            self.assertIn("hook_rollback", str(error.exception))
            self.assertFalse((workspace / ".codex" / "hooks" / "hooks.json").exists())

    def test_enable_hooks_true_rejects_unknown_hook_events(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, ".codex/hooks/hooks.json", "{}\n")
            _write_manifest(stage_root, [_entry(".codex/hooks/hooks.json", ".codex/hooks/hooks.json")])
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(
                stage_root,
                plan["id"],
                [".codex/hooks/hooks.json"],
                ["create_file"],
                enable_hooks=True,
                approved_hook_events=["NotARealHook"],
            )

            with self.assertRaises(MergeInfrastructureError) as error:
                apply_merge_plan(workspace, stage_root, approval)

            self.assertIn("approved_hook_events", str(error.exception))
            self.assertFalse((workspace / ".codex" / "hooks" / "hooks.json").exists())

    def test_enable_hooks_true_blocks_existing_hooks_json_instead_of_empty_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            hooks_path = workspace / ".codex" / "hooks" / "hooks.json"
            hooks_path.parent.mkdir(parents=True)
            hooks_path.write_text('{"SessionStart": []}\n', encoding="utf-8")
            _stage_file(stage_root, ".codex/hooks/hooks.json", '{"SessionStart": ["generated"]}\n')
            _write_manifest(stage_root, [_entry(".codex/hooks/hooks.json", ".codex/hooks/hooks.json")])
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(
                stage_root,
                plan["id"],
                [],
                [],
                enable_hooks=True,
                approved_hook_events=["SessionStart"],
            )

            with self.assertRaises(MergeInfrastructureError) as error:
                apply_merge_plan(workspace, stage_root, approval)

            self.assertIn("hooks.json", str(error.exception))
            self.assertIn("blocked", str(error.exception))
            self.assertEqual(hooks_path.read_text(encoding="utf-8"), '{"SessionStart": []}\n')

    def test_rollback_removes_created_file_after_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            plan = build_merge_plan(workspace, stage_root)
            result = apply_merge_plan(workspace, stage_root, _approval_file(stage_root, plan["id"], ["AGENTS.md"], ["create_file"]))

            rollback = rollback_merge(workspace, result["rollback_manifest"])

            self.assertEqual(rollback["status"], "rolled_back")
            self.assertFalse((workspace / "AGENTS.md").exists())

    def test_rollback_manifest_workspace_binding_prevents_cross_workspace_restore(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_a = Path(tmp) / "workspace-a"
            workspace_b = Path(tmp) / "workspace-b"
            stage_root = Path(tmp) / "stage"
            workspace_a.mkdir()
            workspace_b.mkdir()
            stage_root.mkdir()
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(
                stage_root,
                [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")],
                workspace=workspace_a,
            )
            plan = build_merge_plan(workspace_a, stage_root)
            result = apply_merge_plan(
                workspace_a,
                stage_root,
                _approval_file(stage_root, plan["id"], ["AGENTS.md"], ["create_file"]),
            )
            applied = (workspace_a / "AGENTS.md").read_text(encoding="utf-8")
            (workspace_b / "AGENTS.md").write_text(applied, encoding="utf-8")

            with self.assertRaises(MergeInfrastructureError) as error:
                rollback_merge(workspace_b, result["rollback_manifest"])

            self.assertIn("workspace", str(error.exception))
            self.assertEqual((workspace_b / "AGENTS.md").read_text(encoding="utf-8"), applied)

    def test_rollback_restores_updated_file_after_append(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            original = "# Local rules\n\nDo not delete this.\n"
            (workspace / "AGENTS.md").write_text(original, encoding="utf-8")
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            plan = build_merge_plan(workspace, stage_root)
            result = apply_merge_plan(
                workspace,
                stage_root,
                _approval_file(stage_root, plan["id"], ["AGENTS.md"], ["append_managed_section"]),
            )

            rollback_merge(workspace, result["rollback_manifest"])

            self.assertEqual((workspace / "AGENTS.md").read_text(encoding="utf-8"), original)

    def test_rollback_refuses_when_file_changed_post_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            plan = build_merge_plan(workspace, stage_root)
            result = apply_merge_plan(workspace, stage_root, _approval_file(stage_root, plan["id"], ["AGENTS.md"], ["create_file"]))
            (workspace / "AGENTS.md").write_text("changed after apply\n", encoding="utf-8")

            with self.assertRaises(MergeInfrastructureError) as error:
                rollback_merge(workspace, result["rollback_manifest"])

            self.assertIn("changed after apply", str(error.exception))

    @unittest.skipIf(not hasattr(os, "symlink"), "symlink unsupported")
    def test_rollback_refuses_target_symlink_escape_without_touching_outside(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            outside = Path(tmp) / "outside.md"
            outside.write_text(_managed_doc("project-rules", "Generated rules."), encoding="utf-8")
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            plan = build_merge_plan(workspace, stage_root)
            result = apply_merge_plan(workspace, stage_root, _approval_file(stage_root, plan["id"], ["AGENTS.md"], ["create_file"]))
            (workspace / "AGENTS.md").unlink()
            try:
                os.symlink(outside, workspace / "AGENTS.md")
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink creation unsupported: {exc}")

            with self.assertRaises(MergeInfrastructureError) as error:
                rollback_merge(workspace, result["rollback_manifest"])

            self.assertIn("symlink", str(error.exception))
            self.assertTrue(outside.exists())
            self.assertEqual(outside.read_text(encoding="utf-8"), _managed_doc("project-rules", "Generated rules."))

    @unittest.skipIf(not hasattr(os, "symlink"), "symlink unsupported")
    def test_rollback_refuses_parent_symlink_escape_without_touching_outside(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            outside_dir = Path(tmp) / "outside"
            outside_dir.mkdir()
            outside_file = outside_dir / "hooks.json"
            outside_file.write_text("{}\n", encoding="utf-8")
            _stage_file(stage_root, ".codex/hooks/hooks.json", '{"SessionStart": []}\n')
            _write_manifest(stage_root, [_entry(".codex/hooks/hooks.json", ".codex/hooks/hooks.json")])
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(
                stage_root,
                plan["id"],
                [".codex/hooks/hooks.json"],
                ["create_file"],
                enable_hooks=True,
                approved_hook_events=["SessionStart"],
            )
            result = apply_merge_plan(workspace, stage_root, approval)
            (workspace / ".codex" / "hooks" / "hooks.json").unlink()
            (workspace / ".codex" / "hooks").rmdir()
            try:
                os.symlink(outside_dir, workspace / ".codex" / "hooks")
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink creation unsupported: {exc}")

            with self.assertRaises(MergeInfrastructureError) as error:
                rollback_merge(workspace, result["rollback_manifest"])

            self.assertIn("symlink", str(error.exception))
            self.assertTrue(outside_file.exists())
            self.assertEqual(outside_file.read_text(encoding="utf-8"), "{}\n")

    def test_cli_plan_and_apply_print_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])

            plan_result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), str(stage_root), "--plan"],
                check=False,
                capture_output=True,
                text=True,
            )
            plan = json.loads(plan_result.stdout)
            approval = _approval_file(stage_root, plan["id"], ["AGENTS.md"], ["create_file"])
            apply_result = subprocess.run(
                [
                    sys.executable,
                    str(WRAPPER),
                    str(workspace),
                    str(stage_root),
                    "--apply",
                    "--approval-file",
                    str(approval),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(plan_result.returncode, 0, plan_result.stderr)
            self.assertEqual(apply_result.returncode, 0, apply_result.stderr)
            self.assertEqual(json.loads(apply_result.stdout)["status"], "applied")

    def test_cli_apply_invalid_managed_section_returns_json_error_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            (workspace / "AGENTS.md").write_text("# Local rules\n", encoding="utf-8")
            _stage_file(stage_root, "AGENTS.md", _managed_doc("bad section", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="bad section")])
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(stage_root, plan["id"], ["AGENTS.md"], ["append_managed_section"])

            result = subprocess.run(
                [
                    sys.executable,
                    str(WRAPPER),
                    str(workspace),
                    str(stage_root),
                    "--apply",
                    "--approval-file",
                    str(approval),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stderr, "")
            self.assertNotIn("Traceback", result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn("section", payload["error"])

    def test_cli_apply_nested_same_section_marker_returns_json_error_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            (workspace / "AGENTS.md").write_text("# Local rules\n", encoding="utf-8")
            staged = (
                "# Generated\n\n"
                "<!-- product-agent-os:start project-rules -->\n"
                "Generated rules.\n"
                "<!-- product-agent-os:start project-rules -->\n"
                "Nested marker.\n"
                "<!-- product-agent-os:end project-rules -->\n"
                "<!-- product-agent-os:end project-rules -->\n"
            )
            _stage_file(stage_root, "AGENTS.md", staged)
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            plan = build_merge_plan(workspace, stage_root)
            approval = _approval_file(stage_root, plan["id"], ["AGENTS.md"], ["append_managed_section"])

            result = subprocess.run(
                [
                    sys.executable,
                    str(WRAPPER),
                    str(workspace),
                    str(stage_root),
                    "--apply",
                    "--approval-file",
                    str(approval),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stderr, "")
            self.assertNotIn("Traceback", result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn("managed", payload["error"])

    def test_cli_rollback_missing_backup_returns_json_error_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            target = workspace / "AGENTS.md"
            target.write_text("# Applied\n", encoding="utf-8")
            manifest = stage_root / "rollback.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "workspace": str(workspace),
                        "entries": [
                            {
                                "target_path": "AGENTS.md",
                                "action": "updated",
                                "existed_before": True,
                                "digest_before": "sha256:" + "0" * 64,
                                "digest_after": content_digest(target.read_bytes()),
                                "backup_path": "_rollback/missing.backup",
                                "verification": {},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), str(stage_root), "--rollback", str(manifest)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stderr, "")
            self.assertNotIn("Traceback", result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn("backup", payload["error"])

    def test_cli_rollback_target_directory_returns_json_error_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace, stage_root = _workspace_and_stage(tmp)
            _stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
            _write_manifest(stage_root, [_entry("AGENTS.md", "AGENTS.md", managed_section="project-rules")])
            plan = build_merge_plan(workspace, stage_root)
            result = apply_merge_plan(
                workspace,
                stage_root,
                _approval_file(stage_root, plan["id"], ["AGENTS.md"], ["create_file"]),
            )
            (workspace / "AGENTS.md").unlink()
            (workspace / "AGENTS.md").mkdir()

            cli_result = subprocess.run(
                [sys.executable, str(WRAPPER), str(workspace), str(stage_root), "--rollback", result["rollback_manifest"]],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(cli_result.returncode, 0)
            self.assertEqual(cli_result.stderr, "")
            self.assertNotIn("Traceback", cli_result.stderr)
            payload = json.loads(cli_result.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn("not a file", payload["error"])


def _workspace_and_stage(tmp):
    workspace = Path(tmp) / "workspace"
    stage_root = Path(tmp) / "stage"
    workspace.mkdir()
    stage_root.mkdir()
    return workspace, stage_root


def _stage_file(stage_root, relative_path, content):
    path = stage_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _write_manifest(stage_root, files, *, workspace=None):
    for item in files:
        staged = stage_root / item["staged_path"]
        if item["action"] != "blocked":
            item["digest"] = content_digest(staged.read_bytes())
    _write_raw_manifest(stage_root, files, workspace=workspace)


def _write_raw_manifest(stage_root, files, *, workspace=None):
    workspace_path = workspace if workspace is not None else stage_root.parent / "workspace"
    workspace_path = Path(workspace_path).resolve()
    manifest = {
        "schema_version": 1,
        "renderer": "product-agent-os",
        "renderer_version": "0.1.0",
        "workspace": str(workspace_path),
        "generated_at": "2026-05-14T00:00:00+00:00",
        "workspace_audit_digest": _workspace_audit_digest(workspace_path, files),
        "infrastructure_plan_digest": "sha256:" + "2" * 64,
        "validation": {"ok": True, "checks": [], "errors": {}},
        "files": files,
    }
    (stage_root / MANIFEST_NAME).write_text(json.dumps(manifest), encoding="utf-8")


def _entry(target_path, staged_path, action="create", write_policy="staged_only", managed_section=""):
    return {
        "target_path": target_path,
        "staged_path": staged_path,
        "action": action,
        "write_policy": write_policy,
        "digest": "sha256:" + "0" * 64,
        "managed_section": managed_section,
    }


def _approval_file(
    stage_root,
    plan_id,
    targets,
    actions,
    *,
    enable_hooks=False,
    approved_hook_events=None,
    blocking_hooks=None,
    hook_rollback=None,
):
    path = stage_root / "approval.json"
    if enable_hooks and blocking_hooks is None:
        blocking_hooks = ["PreToolUse"]
    if enable_hooks and hook_rollback is None:
        hook_rollback = "remove hooks.json when rollback digest matches"
    payload = {
        "approval": {
            "schema_version": 1,
            "merge_plan_id": plan_id,
            "approved_by": "test-user",
            "approved_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "approved_targets": targets,
            "approved_actions": actions,
            "accepted_risks": ["fixture workspace write"],
            "denied_targets": [],
            "notes": "test approval",
            "enable_hooks": enable_hooks,
            "approved_hook_events": approved_hook_events or [],
            "blocking_hooks": blocking_hooks or [],
            "hook_rollback": hook_rollback or "",
        }
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _managed_doc(section_id, body):
    return (
        "# Generated\n\n"
        f"<!-- product-agent-os:start {section_id} -->\n"
        f"{body}\n"
        f"<!-- product-agent-os:end {section_id} -->\n"
    )


def _relative_files(root):
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())


def _workspace_audit_digest(workspace, files):
    snapshot = []
    for target_path in sorted({item["target_path"] for item in files if isinstance(item.get("target_path"), str)}):
        path = workspace / target_path
        entry = {
            "target_path": target_path,
            "exists": path.exists(),
            "is_file": path.is_file(),
            "is_symlink": path.is_symlink(),
        }
        if path.is_symlink():
            entry["kind"] = "symlink"
        elif path.is_file():
            entry["digest"] = content_digest(path.read_bytes())
            entry["kind"] = "file"
        elif path.exists():
            entry["kind"] = "other"
        else:
            entry["kind"] = "missing"
        snapshot.append(entry)
    payload = json.dumps(snapshot, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return content_digest(payload)


if __name__ == "__main__":
    unittest.main()
