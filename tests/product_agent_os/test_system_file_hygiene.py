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

    def test_trigger_policy_records_read_only_behavior_and_stop_conditions(self):
        trigger_groups = [
            *TRIGGER_POLICY["periodic_triggers"],
            *TRIGGER_POLICY["event_triggers"],
            *TRIGGER_POLICY["size_triggers"],
        ]

        for trigger in trigger_groups:
            with self.subTest(trigger=trigger["id"]):
                self.assertEqual(trigger["write_policy"], "read_only")
                self.assertIn("scope", trigger)
                self.assertIn("action", trigger)
                self.assertIsInstance(trigger["stop_conditions"], list)
                self.assertGreaterEqual(len(trigger["stop_conditions"]), 1)

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
        self.assertIn("plugins/*/skills/**/SKILL.md", classes["plugin_package_control"]["patterns"])
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

        invalid_packet = packet.copy()
        invalid_packet.pop("summary")
        self.assertIn("summary:required", validate_system_file_hygiene_audit(invalid_packet))

    def test_batch36b_validator_detects_required_safety_findings_with_report_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root, omit={"EVALS.md"})
            (root / "README.md").write_text("# Project\n\nTask 1 Batch 1 implementation log.\n", encoding="utf-8")
            (root / "PLAN.md").write_text(
                "# PLAN.md\n\n"
                "OPENAI_API_KEY = \"sk-test\"\n"
                "## Duplicate\n\nFirst.\n\n## Duplicate\n\nSecond.\n",
                encoding="utf-8",
            )
            (root / "REQUIREMENTS.md").write_text("# REQUIREMENTS.md\n\n" + ("x" * 41000), encoding="utf-8")
            (root / "TEST.md").write_bytes(b"\xef\xbb\xbf# TEST.md\n\nCurrent verification.\n")
            (root / ".codex" / "skills" / "broken").mkdir(parents=True)
            (root / ".codex" / "skills" / "broken" / "SKILL.md").write_bytes(b"\xff\xfe\x00")
            (root / ".codex" / "workflows").mkdir(parents=True)
            (root / ".codex" / "workflows" / "mojibake.md").write_text(
                "# Workflow\n\nPossible marker: Р Сњ.\n",
                encoding="utf-8",
            )
            candidate_dir = root / ".codex" / "automation-candidates"
            candidate_dir.mkdir(parents=True)
            (candidate_dir / "system-file-hygiene-audit.md").write_text(
                "# Candidate\n\n"
                "## Owner\n\n- Accountable owner: Ops\n\n"
                "## Cadence\n\n- Trigger: manual\n\n"
                "Cron: 0 9 * * *\n",
                encoding="utf-8",
            )

            packet = build_system_file_hygiene_audit(root, audit_trigger="weekly_full_system_file_hygiene")

        self.assertEqual(packet["audit_trigger"], "weekly_full_system_file_hygiene")
        codes = {finding["code"]: finding for finding in packet["findings"]}
        for expected in [
            "missing_control_plane_file",
            "unreadable_utf8",
            "utf8_bom_present",
            "mojibake_marker_present",
            "secret_like_literal",
            "duplicate_markdown_headings",
            "soft_size_limit_exceeded",
            "historical_ledger_density",
            "active_schedule_in_candidate",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, codes)
                self.assertIn("class", codes[expected])
                self.assertIn("owner", codes[expected])
                self.assertIn("finding_type", codes[expected])
                self.assertIn("compaction_decision", codes[expected])
                self.assertEqual(codes[expected]["approval_boundary"], "owner_approval_required_for_writes")

        self.assertEqual(packet["status"], "blocked")
        self.assertEqual(packet["summary"]["audit_trigger"], "weekly_full_system_file_hygiene")
        self.assertEqual(packet["summary"]["no_secrets_status"], "blocked")
        self.assertEqual(packet["summary"]["active_schedule_markers"], 1)
        self.assertEqual(validate_system_file_hygiene_audit(packet), [])

    def test_batch36b_cli_returns_json_exit_policy_and_does_not_write_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root, omit={"EVALS.md"})
            (root / "README.md").write_text("# Project\n\nOperator entrypoint.\n", encoding="utf-8")
            before = _workspace_files(root)

            cli = subprocess.run(
                [
                    sys.executable,
                    str(WRAPPER),
                    str(root),
                    "--trigger",
                    "soft_size_review",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            after = _workspace_files(root)

        self.assertEqual(cli.returncode, 0)
        payload = json.loads(cli.stdout)
        self.assertEqual(payload["status"], "review_required")
        self.assertEqual(payload["audit_trigger"], "soft_size_review")
        self.assertEqual(payload["write_policy"], "read_only")
        self.assertEqual(payload["schedule_status"], "not_created")
        self.assertEqual(before, after)

    def test_batch36b_no_secrets_status_blocks_when_secret_scan_is_unverifiable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root)
            (root / "README.md").write_text("# Project\n\nOperator entrypoint.\n", encoding="utf-8")
            (root / ".codex" / "skills" / "broken").mkdir(parents=True)
            (root / ".codex" / "skills" / "broken" / "SKILL.md").write_bytes(b"\xff\xfe\x00")

            packet = build_system_file_hygiene_audit(root)
            missing_workspace_packet = build_system_file_hygiene_audit(root / "missing")

        self.assertEqual(packet["status"], "blocked")
        self.assertEqual(packet["summary"]["no_secrets_status"], "blocked")
        self.assertEqual(packet["summary"]["secret_like_findings"], 0)
        self.assertIn("unreadable_utf8", {finding["code"] for finding in packet["findings"]})
        self.assertEqual(validate_system_file_hygiene_audit(packet), [])

        self.assertEqual(missing_workspace_packet["status"], "blocked")
        self.assertEqual(missing_workspace_packet["summary"]["no_secrets_status"], "blocked")
        self.assertIn("workspace_not_found", {finding["code"] for finding in missing_workspace_packet["findings"]})
        self.assertEqual(validate_system_file_hygiene_audit(missing_workspace_packet), [])

    def test_batch36b_validator_rejects_unapproved_finding_approval_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root, omit={"EVALS.md"})
            (root / "README.md").write_text("# Project\n\nOperator entrypoint.\n", encoding="utf-8")
            packet = build_system_file_hygiene_audit(root)

        invalid_packet = json.loads(json.dumps(packet))
        invalid_packet["findings"][0]["approval_boundary"] = "not_required"

        self.assertIn("findings:invalid", validate_system_file_hygiene_audit(invalid_packet))

    def test_batch36b_report_template_captures_required_report_fields(self):
        template = (
            ROOT
            / "plugins"
            / "product-agent-os"
            / "assets"
            / "templates"
            / "artifact-templates"
            / "system-file-hygiene-report.md"
        ).read_text(encoding="utf-8").lower()

        for expected in [
            "audit trigger",
            "system file class",
            "finding type",
            "owner",
            "compaction decision",
            "active schedule markers",
            "no-secrets status",
            "approval boundary",
            "owner-approved slice",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, template)

    def test_packet_validator_rejects_malformed_nested_contract_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root)
            (root / "README.md").write_text("# Project\n\nOperator entrypoint.\n", encoding="utf-8")
            packet = build_system_file_hygiene_audit(root)

        malformed_cases = [
            ("triggers:invalid", {"triggers": {"event_triggers": [{"id": "missing fields"}]}}),
            ("system_file_classes:invalid", {"system_file_classes": [{}]}),
            ("summary:status_required", {"summary": {"files_scanned": 1, "warnings": 0, "errors": 0}}),
            ("inventory:invalid", {"inventory": [{}]}),
            ("findings:invalid", {"findings": [{}], "status": "blocked", "summary": packet["summary"] | {"status": "blocked"}}),
        ]

        for expected_error, override in malformed_cases:
            with self.subTest(expected_error=expected_error):
                invalid_packet = packet | override
                self.assertIn(expected_error, validate_system_file_hygiene_audit(invalid_packet))

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

    def test_batch36d_blocks_schedule_text_hook_activation_and_external_write_in_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root)
            (root / "README.md").write_text("# Project\n\nOperator entrypoint.\n", encoding="utf-8")
            candidate_dir = root / ".codex" / "automation-candidates"
            candidate_dir.mkdir(parents=True)
            (candidate_dir / "docs-maintenance.md").write_text(
                "# Candidate\n\n"
                "## Owner\n\n- Accountable owner: Ops\n\n"
                "## Cadence\n\n- Trigger: manual\n\n"
                "## Verification\n\n- Deterministic checks: python tools/check_docs.py\n\n"
                "Schedule: weekly\n"
                "Hook activation: active\n"
                "External write: active\n",
                encoding="utf-8",
            )

            packet = build_system_file_hygiene_audit(root)

        findings = [finding for finding in packet["findings"] if finding["code"] == "active_schedule_in_candidate"]
        self.assertEqual(packet["status"], "blocked")
        self.assertEqual(packet["summary"]["active_schedule_markers"], 1)
        self.assertEqual(len(findings), 1)
        self.assertIn("active schedule", findings[0]["message"])


def _write_minimal_control_plane(root: Path, omit: set[str] | None = None) -> None:
    omitted = omit or set()
    for name in ["AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]:
        if name in omitted:
            continue
        (root / name).write_text(f"# {name}\n\nCurrent contract only.\n", encoding="utf-8")


def _workspace_files(root: Path) -> list[str]:
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())


if __name__ == "__main__":
    unittest.main()
