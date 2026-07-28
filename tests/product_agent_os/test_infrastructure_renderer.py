import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

import product_agent_os.infrastructure as infrastructure  # noqa: E402
from product_agent_os.discovery import analyze_workspace  # noqa: E402
from product_agent_os.infrastructure import (  # noqa: E402
    InfrastructureError,
    render_infrastructure_plan,
    stage_infrastructure,
)
from product_agent_os.stage_manifest import MANIFEST_NAME  # noqa: E402
from product_agent_os.templates import TemplateSpec  # noqa: E402


class InfrastructureRendererTest(unittest.TestCase):
    def test_dry_run_returns_json_shape_without_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            shutil.copytree(FIXTURES / "node-app", workspace)
            before = self._relative_files(workspace)

            result = render_infrastructure_plan(workspace)
            after = self._relative_files(workspace)

        self.assertEqual(before, after)
        self.assertEqual(result["infrastructure_plan"]["status"], "needs_approval")
        self.assertEqual(result["infrastructure_plan"]["profile"], "guided-small")
        self.assertIn("rendered_artifacts", result)
        self.assertTrue(result["rendered_artifacts"]["validation"]["ok"])

    def test_plan_exposes_track_three_schema_summaries(self):
        result = render_infrastructure_plan(FIXTURES / "empty-repo")
        plan = result["infrastructure_plan"]
        artifacts = result["rendered_artifacts"]

        self.assertEqual(plan["status"], "needs_approval")
        for key in ["create", "update", "leave_unchanged", "blocked", "questions"]:
            self.assertIn(key, plan)
            self.assertIsInstance(plan[key], list)
        self.assertIn("AGENTS.md", plan["create"])
        self.assertEqual(plan["update"], [])
        self.assertEqual(plan["leave_unchanged"], [])
        self.assertEqual(plan["questions"], [])
        self.assertIn("root", artifacts)
        self.assertIn("managed_sections", artifacts)
        self.assertTrue(any(item["target_path"] == "AGENTS.md" for item in artifacts["managed_sections"]))
        self.assertIn("checks", artifacts["validation"])
        self.assertIn("agent templates validate", artifacts["validation"]["checks"])

    def test_render_from_precomputed_audit_uses_supplied_audit_and_lifecycle_packet(self):
        audit = analyze_workspace(FIXTURES / "node-app")
        audit["complexity_profile"]["name"] = "enterprise-governed"
        lifecycle_packets = {
            "questions": ["Confirm governed approval owner before applying staged files."]
        }

        result = infrastructure.render_infrastructure_from_audit(
            FIXTURES / "node-app",
            audit,
            lifecycle_packets=lifecycle_packets,
        )

        self.assertEqual(result["infrastructure_plan"]["profile"], "enterprise-governed")
        self.assertIn(
            "Confirm governed approval owner before applying staged files.",
            result["infrastructure_plan"]["questions"],
        )

    def test_greenfield_plan_creates_control_plane_and_codex_assets(self):
        result = render_infrastructure_plan(FIXTURES / "empty-repo")
        files = result["rendered_artifacts"]["files"]
        by_target = {item["target_path"]: item for item in files}

        self.assertEqual(by_target["AGENTS.md"]["action"], "create")
        self.assertEqual(by_target["REQUIREMENTS.md"]["action"], "create")
        self.assertEqual(by_target[".codex/config.toml"]["action"], "create")
        self.assertEqual(by_target[".codex/hooks/hooks.json"]["write_policy"], "staged_only")
        self.assertIn("explicit approval", " ".join(result["infrastructure_plan"]["approval_required"]))

    def test_lifecycle_hooks_are_staged_with_marker_guard(self):
        expected_targets = {
            ".codex/hooks/hooks.json",
            ".codex/hooks/session_start_context.py",
            ".codex/hooks/pre_tool_use_policy.py",
            ".codex/hooks/permission_request_summary.py",
            ".codex/hooks/post_tool_use_evidence.py",
            ".codex/hooks/stop_runlog_reminder.py",
        }

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)

            staged = stage_infrastructure(workspace, stage_root)

            staged_by_target = {
                item["target_path"]: Path(item["staged_path"])
                for item in staged["rendered_artifacts"]["files"]
                if item["target_path"] in expected_targets
            }
            manifest = json.loads(Path(staged["rendered_artifacts"]["manifest_path"]).read_text(encoding="utf-8"))
            manifest_targets = {item["target_path"] for item in manifest["files"]}

            self.assertEqual(set(staged_by_target), expected_targets)
            self.assertTrue(expected_targets.issubset(manifest_targets))
            for path in staged_by_target.values():
                self.assertTrue(path.resolve().is_relative_to(stage_root.resolve()), path)
                self.assertTrue(path.exists(), path)

            pre_tool = staged_by_target[".codex/hooks/pre_tool_use_policy.py"].read_text(encoding="utf-8")
            stop = staged_by_target[".codex/hooks/stop_runlog_reminder.py"].read_text(encoding="utf-8")
            self.assertIn(".codex/product-agent-os/lifecycle-state.json", pre_tool)
            self.assertIn("missing lifecycle marker", pre_tool)
            self.assertIn("task_start_brief_shown", pre_tool)
            self.assertIn("Completion Brief", stop)

    def test_stage_mode_writes_only_inside_output_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "python-app", workspace)

            result = stage_infrastructure(workspace, stage_root)

            staged_paths = [Path(item["staged_path"]).resolve() for item in result["rendered_artifacts"]["files"]]
            manifest_path = Path(result["rendered_artifacts"]["manifest_path"]).resolve()
            self.assertTrue(staged_paths)
            for path in staged_paths:
                self.assertTrue(path.is_relative_to(stage_root.resolve()), path)
                self.assertTrue(path.exists(), path)
            self.assertEqual(manifest_path, (stage_root / MANIFEST_NAME).resolve())
            self.assertTrue(manifest_path.is_relative_to(stage_root.resolve()), manifest_path)
            self.assertTrue(manifest_path.exists(), manifest_path)
            self.assertFalse((workspace / "AGENTS.md").exists())
            self.assertFalse((workspace / ".codex").exists())

    def test_system_file_hygiene_templates_are_staged_without_active_schedule(self):
        expected_targets = {
            ".codex/workflows/system-file-hygiene-audit.md",
            ".codex/artifact-templates/system-file-hygiene-report.md",
            ".codex/automation-candidates/system-file-hygiene-audit.md",
        }
        active_schedule_prefixes = ("cron:", "- cron:", "rrule:", "- rrule:")

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)

            dry_run = render_infrastructure_plan(workspace)
            staged = stage_infrastructure(workspace, stage_root)

            dry_run_targets = {
                item["target_path"]
                for item in dry_run["rendered_artifacts"]["files"]
                if item["target_path"] in expected_targets
            }
            dry_run_by_target = {
                item["target_path"]: item
                for item in dry_run["rendered_artifacts"]["files"]
                if item["target_path"] in expected_targets
            }
            staged_by_target = {
                item["target_path"]: Path(item["staged_path"])
                for item in staged["rendered_artifacts"]["files"]
                if item["target_path"] in expected_targets
            }
            manifest = json.loads(Path(staged["rendered_artifacts"]["manifest_path"]).read_text(encoding="utf-8"))
            manifest_targets = {
                item["target_path"]
                for item in manifest["files"]
                if item["target_path"] in expected_targets
            }

            self.assertEqual(dry_run_targets, expected_targets)
            self.assertEqual(set(staged_by_target), expected_targets)
            self.assertEqual(manifest_targets, expected_targets)
            for item in dry_run_by_target.values():
                self.assertEqual(item["action"], "create")
            for path in staged_by_target.values():
                self.assertTrue(path.resolve().is_relative_to(stage_root.resolve()), path)
                self.assertTrue(path.exists(), path)

            automation_text = staged_by_target[
                ".codex/automation-candidates/system-file-hygiene-audit.md"
            ].read_text(encoding="utf-8")
            self.assertIn("candidate_only", automation_text)

            combined_text = "\n".join(path.read_text(encoding="utf-8") for path in staged_by_target.values())
            lowered_lines = [line.strip().lower() for line in combined_text.splitlines()]
            self.assertFalse(any(line.startswith(active_schedule_prefixes) for line in lowered_lines))
            self.assertNotIn("codex app automation: active", combined_text.lower())
            self.assertNotIn("github actions workflow: active", combined_text.lower())

    def test_task_matrix_plan_template_is_staged_as_artifact(self):
        target = ".codex/artifact-templates/task-matrix-plan.md"

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)

            dry_run = render_infrastructure_plan(workspace)
            staged = stage_infrastructure(workspace, stage_root)

            dry_run_by_target = {
                item["target_path"]: item
                for item in dry_run["rendered_artifacts"]["files"]
                if item["target_path"] == target
            }
            staged_by_target = {
                item["target_path"]: Path(item["staged_path"])
                for item in staged["rendered_artifacts"]["files"]
                if item["target_path"] == target
            }
            manifest = json.loads(Path(staged["rendered_artifacts"]["manifest_path"]).read_text(encoding="utf-8"))
            manifest_targets = {item["target_path"] for item in manifest["files"]}

            self.assertIn(target, dry_run_by_target)
            self.assertIn(target, staged_by_target)
            self.assertIn(target, manifest_targets)
            self.assertEqual(dry_run_by_target[target]["action"], "create")
            staged_path = staged_by_target[target]
            self.assertTrue(staged_path.resolve().is_relative_to(stage_root.resolve()), staged_path)
            rendered = staged_path.read_text(encoding="utf-8")
            self.assertIn("task_matrix_plan_v1", rendered)
            self.assertIn("Validator target: detailed task blocks", rendered)
            self.assertIn("no git stage/commit/push/PR", rendered)

    def test_existing_agents_file_without_marker_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "existing-codex-config", workspace)
            original = (workspace / "AGENTS.md").read_text(encoding="utf-8")

            result = stage_infrastructure(workspace, stage_root)

            by_target = {item["target_path"]: item for item in result["rendered_artifacts"]["files"]}
            agents = by_target["AGENTS.md"]
            self.assertEqual(agents["action"], "leave_unchanged")
            self.assertIn("_proposals", agents["staged_path"])
            self.assertIn("preserved user-authored file", " ".join(result["infrastructure_plan"]["warnings"]))
            self.assertEqual((workspace / "AGENTS.md").read_text(encoding="utf-8"), original)

    def test_existing_project_config_without_marker_is_preserved(self):
        result = render_infrastructure_plan(FIXTURES / "existing-codex-config")
        by_target = {item["target_path"]: item for item in result["rendered_artifacts"]["files"]}

        self.assertEqual(by_target[".codex/config.toml"]["action"], "leave_unchanged")
        self.assertEqual(by_target[".codex/config.toml"]["write_policy"], "approved_write_required")
        self.assertIn(".codex/config.toml", " ".join(result["infrastructure_plan"]["warnings"]))

    def test_duplicate_managed_section_blocks_target(self):
        result = render_infrastructure_plan(FIXTURES / "duplicate-managed-section")
        by_target = {item["target_path"]: item for item in result["rendered_artifacts"]["files"]}

        self.assertEqual(result["infrastructure_plan"]["status"], "blocked")
        self.assertEqual(by_target["AGENTS.md"]["action"], "blocked")
        self.assertIn("duplicate managed section", " ".join(result["infrastructure_plan"]["blocked"]))

    def test_invalid_workspace_error_has_no_traceback_contract(self):
        with self.assertRaises(InfrastructureError) as error:
            render_infrastructure_plan(FIXTURES / "missing-workspace")

        self.assertIn("workspace does not exist", str(error.exception))

    def test_renderer_blocks_stage_directory_inside_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            shutil.copytree(FIXTURES / "node-app", workspace)

            with self.assertRaises(InfrastructureError) as error:
                stage_infrastructure(workspace, workspace / ".product-agent-os" / "staged")

        self.assertIn("outside workspace", str(error.exception))

    def test_rendered_control_plane_files_include_managed_markers(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)

            result = stage_infrastructure(workspace, stage_root)

            for item in result["rendered_artifacts"]["files"]:
                if item["target_path"] not in {
                    "AGENTS.md",
                    "REQUIREMENTS.md",
                    "PLAN.md",
                    "TEST.md",
                    "EVALS.md",
                    "RUNLOG.md",
                }:
                    continue
                text = Path(item["staged_path"]).read_text(encoding="utf-8")
                self.assertIn("<!-- product-agent-os:start", text)
                self.assertIn("<!-- product-agent-os:end", text)

    def test_monorepo_profile_warns_about_worktree_ownership(self):
        result = render_infrastructure_plan(FIXTURES / "monorepo")

        warnings = " ".join(result["infrastructure_plan"]["warnings"])
        self.assertIn("worktree ownership", warnings)

    def test_docs_source_context_warns_about_source_registry(self):
        result = render_infrastructure_plan(FIXTURES / "docs-source-conflict")

        warnings = " ".join(result["infrastructure_plan"]["warnings"])
        self.assertIn("source registry", warnings)

    def test_failed_verification_warns_without_checks_passed_claim(self):
        result = render_infrastructure_plan(FIXTURES / "failed-verification")

        warnings = " ".join(result["infrastructure_plan"]["warnings"])
        self.assertIn("failed verification evidence", warnings)
        self.assertNotIn("checks passed", json.dumps(result).lower())

    def test_unpaired_managed_marker_blocks_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            shutil.copytree(FIXTURES / "node-app", workspace)
            (workspace / "AGENTS.md").write_text(
                "# Rules\n\n<!-- product-agent-os:start project-rules -->\nUnclosed block.\n",
                encoding="utf-8",
            )

            result = render_infrastructure_plan(workspace)

        by_target = {item["target_path"]: item for item in result["rendered_artifacts"]["files"]}
        self.assertEqual(result["infrastructure_plan"]["status"], "blocked")
        self.assertEqual(by_target["AGENTS.md"]["action"], "blocked")
        self.assertIn("unpaired managed section", " ".join(result["infrastructure_plan"]["blocked"]))

    def test_reversed_managed_markers_block_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            shutil.copytree(FIXTURES / "node-app", workspace)
            (workspace / "AGENTS.md").write_text(
                "# Rules\n\n"
                "<!-- product-agent-os:end project-rules -->\n"
                "Broken block.\n"
                "<!-- product-agent-os:start project-rules -->\n",
                encoding="utf-8",
            )

            result = render_infrastructure_plan(workspace)

        by_target = {item["target_path"]: item for item in result["rendered_artifacts"]["files"]}
        blocked = " ".join(result["infrastructure_plan"]["blocked"])
        self.assertEqual(result["infrastructure_plan"]["status"], "blocked")
        self.assertEqual(by_target["AGENTS.md"]["action"], "blocked")
        self.assertRegex(blocked, r"broken managed section|managed marker")

    def test_unsafe_write_fixture_preserves_existing_project_files(self):
        agents_path = FIXTURES / "unsafe-write-request" / "AGENTS.md"
        config_path = FIXTURES / "unsafe-write-request" / ".codex" / "config.toml"
        before_files = self._relative_files(FIXTURES / "unsafe-write-request")
        before_agents = agents_path.read_text(encoding="utf-8")
        before_config = config_path.read_text(encoding="utf-8")

        dry_run = render_infrastructure_plan(FIXTURES / "unsafe-write-request")
        with tempfile.TemporaryDirectory() as tmp:
            stage_root = Path(tmp) / "stage"
            staged = stage_infrastructure(FIXTURES / "unsafe-write-request", stage_root)

            by_target = {item["target_path"]: item for item in staged["rendered_artifacts"]["files"]}
            config = by_target[".codex/config.toml"]
            agents = by_target["AGENTS.md"]
            warnings = " ".join(staged["infrastructure_plan"]["warnings"])

            self.assertEqual(config["action"], "leave_unchanged")
            self.assertEqual(config["write_policy"], "approved_write_required")
            self.assertIn("_proposals", config["staged_path"])
            self.assertFalse((stage_root / ".codex" / "config.toml").exists())
            self.assertEqual(agents["action"], "leave_unchanged")
            self.assertIn("_proposals", agents["staged_path"])
            self.assertFalse((stage_root / "AGENTS.md").exists())
            self.assertRegex(warnings, r"\.codex/config\.toml|approved write")

        dry_run_by_target = {item["target_path"]: item for item in dry_run["rendered_artifacts"]["files"]}
        self.assertEqual(dry_run_by_target[".codex/config.toml"]["action"], "leave_unchanged")
        self.assertEqual(before_files, self._relative_files(FIXTURES / "unsafe-write-request"))
        self.assertEqual(agents_path.read_text(encoding="utf-8"), before_agents)
        self.assertEqual(config_path.read_text(encoding="utf-8"), before_config)

    def test_validation_blocks_unresolved_substitution_markers(self):
        result = self._render_with_template(
            TemplateSpec("bad-text", "test", Path("unused"), "AGENTS.md"),
            "Project: {unresolved_marker}\n",
        )

        self.assertEqual(result["infrastructure_plan"]["status"], "blocked")
        self.assertFalse(result["rendered_artifacts"]["validation"]["ok"])
        self.assertIn("unresolved substitution marker", str(result["rendered_artifacts"]["validation"]["errors"]))

    def test_validation_requires_hook_json_events(self):
        result = self._render_with_template(
            TemplateSpec("bad-hooks", "hooks", Path("unused"), ".codex/hooks/hooks.json", "hook_json"),
            '{"SessionStart": []}',
        )

        self.assertEqual(result["infrastructure_plan"]["status"], "blocked")
        self.assertFalse(result["rendered_artifacts"]["validation"]["ok"])
        self.assertIn("missing hook event: PreToolUse", str(result["rendered_artifacts"]["validation"]["errors"]))

    def test_validation_requires_eval_json_cases_list(self):
        result = self._render_with_template(
            TemplateSpec("bad-eval", "evals", Path("unused"), ".codex/evals/bad.json", "eval_json"),
            '{"name": "bad", "cases": {}}',
        )

        self.assertEqual(result["infrastructure_plan"]["status"], "blocked")
        self.assertFalse(result["rendered_artifacts"]["validation"]["ok"])
        self.assertIn("cases must be a list", str(result["rendered_artifacts"]["validation"]["errors"]))

    def test_validation_still_uses_agent_and_hook_validators(self):
        agent_result = self._render_with_template(
            TemplateSpec("bad-agent", "agents", Path("unused"), ".codex/agents/bad.toml", "agent"),
            'name = "Bad Agent"\n',
        )
        hook_result = self._render_with_template(
            TemplateSpec("bad-hook", "hooks", Path("unused"), ".codex/hooks/bad.py", "hook"),
            'API_KEY = "secret"\n',
        )

        self.assertFalse(agent_result["rendered_artifacts"]["validation"]["ok"])
        self.assertIn("missing required field", str(agent_result["rendered_artifacts"]["validation"]["errors"]))
        self.assertFalse(hook_result["rendered_artifacts"]["validation"]["ok"])
        self.assertIn("forbidden secret-like literal", str(hook_result["rendered_artifacts"]["validation"]["errors"]))

    def test_stage_validation_failure_marks_file_entry_non_mergeable(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)

            result = self._stage_with_template(
                workspace,
                stage_root,
                TemplateSpec("bad-agent", "agents", Path("unused"), ".codex/agents/bad.toml", "agent"),
                'name = "Bad Agent"\n',
            )

        plan = result["infrastructure_plan"]
        by_target = {item["target_path"]: item for item in result["rendered_artifacts"]["files"]}
        bad_agent = by_target[".codex/agents/bad.toml"]
        self.assertEqual(result["infrastructure_plan"]["status"], "blocked")
        self.assertFalse(result["rendered_artifacts"]["validation"]["ok"])
        self.assertEqual(bad_agent["action"], "blocked")
        self.assertEqual(bad_agent["write_policy"], "blocked")
        self.assertEqual(bad_agent["staged_path"], "")
        self.assertNotIn(".codex/agents/bad.toml", plan["create"])
        self.assertNotIn(".codex/agents/bad.toml", plan["update"])
        self.assertNotIn(".codex/agents/bad.toml", plan["leave_unchanged"])
        self.assertIn(".codex/agents/bad.toml", " ".join(plan["blocked"]))

    def test_dry_run_rejects_absolute_template_target_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / "outside-dry-run.txt"
            try:
                with self.assertRaises(InfrastructureError):
                    self._render_with_template(
                        TemplateSpec("absolute-target", "test", Path("unused"), str(outside)),
                        "content\n",
                    )
                self.assertFalse(outside.exists())
            finally:
                outside.unlink(missing_ok=True)

    def test_stage_rejects_parent_template_target_without_writing_outside_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            outside = Path(tmp) / "escape.txt"
            shutil.copytree(FIXTURES / "empty-repo", workspace)
            spec = TemplateSpec("parent-target", "test", Path("unused"), "../escape.txt")

            original_required_templates = infrastructure.required_templates
            original_render_template = infrastructure.render_template
            infrastructure.required_templates = lambda: (spec,)
            infrastructure.render_template = lambda item, context: "content\n"
            try:
                with self.assertRaises(InfrastructureError):
                    stage_infrastructure(workspace, stage_root)
                self.assertFalse(outside.exists())
                if stage_root.exists():
                    for path in stage_root.rglob("*"):
                        self.assertTrue(path.resolve().is_relative_to(stage_root.resolve()), path)
            finally:
                infrastructure.required_templates = original_required_templates
                infrastructure.render_template = original_render_template
                outside.unlink(missing_ok=True)

    def _render_with_template(self, spec, content):
        original_required_templates = infrastructure.required_templates
        original_render_template = infrastructure.render_template
        infrastructure.required_templates = lambda: (spec,)
        infrastructure.render_template = lambda item, context: content
        try:
            return render_infrastructure_plan(FIXTURES / "empty-repo")
        finally:
            infrastructure.required_templates = original_required_templates
            infrastructure.render_template = original_render_template

    def _stage_with_template(self, workspace, stage_root, spec, content):
        original_required_templates = infrastructure.required_templates
        original_render_template = infrastructure.render_template
        infrastructure.required_templates = lambda: (spec,)
        infrastructure.render_template = lambda item, context: content
        try:
            return stage_infrastructure(workspace, stage_root)
        finally:
            infrastructure.required_templates = original_required_templates
            infrastructure.render_template = original_render_template

    def _relative_files(self, root):
        return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())


if __name__ == "__main__":
    unittest.main()
