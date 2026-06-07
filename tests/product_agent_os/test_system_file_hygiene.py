import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
WRAPPER = SCRIPTS / "validate_system_file_hygiene.py"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.system_file_hygiene import (  # noqa: E402
    TRIGGER_POLICY,
    build_system_file_hygiene_audit,
    system_file_class_records,
    validate_system_file_hygiene_audit,
)


class SystemFileHygieneTest(unittest.TestCase):
    def test_trigger_policy_is_hybrid_and_candidate_only(self):
        self.assertEqual(TRIGGER_POLICY["schedule_status"], "not_created")
        self.assertEqual(TRIGGER_POLICY["write_policy"], "read_only")

        rendered = json.dumps(TRIGGER_POLICY, sort_keys=True)
        for expected in [
            "weekly_full_system_file_hygiene",
            "monthly_deep_ownership_review",
            "after changes to AGENTS.md",
            "soft_size_review",
            "hard_size_compaction_required",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, rendered)

    def test_system_file_classes_cover_project_control_surfaces(self):
        classes = {item["key"]: item for item in system_file_class_records()}

        for expected in [
            "root_control_plane",
            "project_entrypoint",
            "nested_agents_md",
            "codex_config",
            "codex_agents",
            "codex_skills",
            "codex_workflows",
            "artifact_templates",
            "automation_candidates",
            "hooks",
            "evals",
            "pr_release_packets",
            "docs_source_control",
            "external_automation_policy",
            "plugin_package_control",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, classes)

        self.assertIn(".codex/agents/*.toml", classes["codex_agents"]["patterns"])
        self.assertIn(".codex/skills/**/SKILL.md", classes["codex_skills"]["patterns"])
        self.assertIn(".github/workflows/*", classes["external_automation_policy"]["patterns"])

    def test_clean_minimal_workspace_returns_ok_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root)
            (root / "README.md").write_text("# Project\n\nOperator entrypoint.\n", encoding="utf-8")
            (root / ".codex" / "agents").mkdir(parents=True)
            (root / ".codex" / "agents" / "builder.toml").write_text(
                'name = "builder"\n'
                'description = "Builds scoped slices."\n'
                'developer_instructions = "Follow PLAN.md."\n'
                'ownership = "implementation"\n'
                'inputs = "PLAN.md"\n'
                'outputs = "patch and evidence"\n'
                'stop_conditions = "missing plan"\n'
                'model_policy = "default"\n'
                'handoff_requirements = "files, checks, risks"\n',
                encoding="utf-8",
            )
            (root / ".codex" / "skills" / "cleanup").mkdir(parents=True)
            (root / ".codex" / "skills" / "cleanup" / "SKILL.md").write_text(
                "# Cleanup Skill\n\n## Trigger\n\nRepeated cleanup.\n\n## Verification\n\nRun audit.\n",
                encoding="utf-8",
            )

            packet = build_system_file_hygiene_audit(root)

        self.assertEqual(packet["status"], "ok")
        self.assertEqual(packet["write_policy"], "read_only")
        self.assertEqual(packet["schedule_status"], "not_created")
        self.assertEqual(validate_system_file_hygiene_audit(packet), [])
        self.assertGreaterEqual(packet["summary"]["files_scanned"], 8)

    def test_size_ledger_and_active_schedule_findings_require_review_or_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root)
            (root / "REQUIREMENTS.md").write_text("# REQUIREMENTS.md\n\n" + ("x" * 51000), encoding="utf-8")
            (root / "README.md").write_text("# Project\n\nTask 1 Batch 1 implementation log.\n", encoding="utf-8")
            candidate_dir = root / ".codex" / "automation-candidates"
            candidate_dir.mkdir(parents=True)
            (candidate_dir / "system-file-hygiene-audit.md").write_text(
                "# Candidate\n\n"
                "## Owner\n\n- Accountable owner: Ops\n\n"
                "## Cadence\n\n- Trigger: manual\n\n"
                "## Stable Inputs\n\n- Inputs: system files\n\n"
                "## Stable Outputs\n\n- Outputs: report\n\n"
                "## Verification\n\n- Deterministic checks: python validate_system_file_hygiene.py .\n\n"
                "## Failure Modes\n\n- Known failure: stale evidence\n\n"
                "## Rollback Or Disable Path\n\n- Disable path: remove candidate\n\n"
                "## Explicit Write Policy\n\n- Allowed write targets: staged reports only\n\n"
                "## Explicit Approval\n\n- Approval status: not requested\n\n"
                "Cron: 0 9 * * *\n",
                encoding="utf-8",
            )

            packet = build_system_file_hygiene_audit(root)
            cli = subprocess.run(
                [sys.executable, str(WRAPPER), str(root)],
                check=False,
                capture_output=True,
                text=True,
            )

        codes = {finding["code"] for finding in packet["findings"]}
        self.assertEqual(packet["status"], "blocked")
        self.assertIn("hard_size_limit_exceeded", codes)
        self.assertIn("historical_ledger_density", codes)
        self.assertIn("active_schedule_in_candidate", codes)
        self.assertEqual(cli.returncode, 1)
        self.assertIn('"status": "blocked"', cli.stdout)


def _write_minimal_control_plane(root: Path) -> None:
    for name in ["AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]:
        (root / name).write_text(f"# {name}\n\nCurrent contract only.\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
