import json
from datetime import UTC, datetime
import os
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
    def test_detailed_planning_matrix_size_exception_does_not_exempt_navigation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root)
            (root / 'docs/planning/feature').mkdir(parents=True)
            matrix = '### Task `P-01`\n- ID: P-01\n- Status: planned\n- Acceptance criteria: retained\n' + 'Detail.\n' * 6000
            for name in ('docs/planning/feature/tasks.md', 'docs/planning/index.md', 'PLAN.md'):
                (root / name).write_bytes(matrix.encode())
            result = build_system_file_hygiene_audit(root)
            records = {r['path']: r for r in result['inventory']}
            self.assertIn('docs/planning/feature/tasks.md', records)
            self.assertTrue(records['docs/planning/feature/tasks.md']['size_exempt'])
            self.assertFalse(records['docs/planning/index.md']['size_exempt'])
            self.assertFalse(records['PLAN.md']['size_exempt'])
            hard = {f['path'] for f in result['findings'] if f['code'] == 'hard_size_limit_exceeded'}
            self.assertNotIn('docs/planning/feature/tasks.md', hard)
            self.assertTrue({'PLAN.md', 'docs/planning/index.md'} <= hard)
            self.assertEqual((root / 'docs/planning/feature/tasks.md').read_bytes(), matrix.encode())
            from product_agent_os.document_navigation import check_local_links
            with (root / 'docs/planning/feature/tasks.md').open('ab') as handle:
                handle.write(b'\n[Evidence](missing.md)\n## Repeated\n## Repeated\n')
            self.assertTrue(check_local_links(root, ['docs/planning/feature/tasks.md']))
            content_check = build_system_file_hygiene_audit(root)
            self.assertTrue(any(f['path'] == 'docs/planning/feature/tasks.md' and f['code'] == 'duplicate_markdown_headings'
                                for f in content_check['findings']))
            (root / '.codex').mkdir()
            (root / '.codex/config.toml').write_text(
                '[product_agent_os.documents.limits]\n"docs/planning/feature/tasks.md" = 20000\n', encoding='utf-8')
            strict = build_system_file_hygiene_audit(root)
            self.assertTrue(any(f['code'] == 'hard_size_limit_exceeded' and f['path'] == 'docs/planning/feature/tasks.md'
                                for f in strict['findings']))

    def test_utf8_budget_is_bytes_and_exact_hard_boundary_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root)
            for size, prefix in ((size, prefix) for size in (39999, 40000, 40001, 39999, 40001)
                                 for prefix in (b'', '\ufeffRU/EN Я🙂\r\n'.encode('utf-8'))):
                with self.subTest(size=size, prefix=prefix):
                    remaining = size - len(prefix)
                    content = prefix + ('Я' * (remaining // 2)).encode() + b'x' * (remaining % 2)
                    (root / 'PLAN.md').write_bytes(content)
                    result = build_system_file_hygiene_audit(root)
                    codes = [f['code'] for f in result['findings'] if f['path'] == 'PLAN.md']
                    self.assertEqual('hard_size_limit_exceeded' in codes, size > 40000)
                    record = next(r for r in result['inventory'] if r['path'] == 'PLAN.md')
                    self.assertEqual(record['bytes'], size)

    def test_stricter_project_byte_budget_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root)
            (root / '.codex').mkdir(exist_ok=True)
            (root / '.codex/config.toml').write_text(
                '[product_agent_os.documents.limits]\n"PLAN.md" = 20000\n', encoding='utf-8')
            (root / 'PLAN.md').write_bytes(b'x' * 20001)
            report = build_system_file_hygiene_audit(root)
            self.assertTrue(any(f['code'] == 'hard_size_limit_exceeded' and f['path'] == 'PLAN.md'
                                for f in report['findings']))

    def test_archive_exemption_requires_index_and_cannot_hide_open_task_matrix(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root)
            (root / '.codex').mkdir()
            (root / 'docs/plans').mkdir(parents=True)
            (root / 'docs/index.md').write_text('[History](plans/history.md)', encoding='utf-8')
            (root / 'docs/plans/history.md').write_bytes(b'closed evidence\n' * 4000)
            (root / '.codex/config.toml').write_text(
                '[product_agent_os.documents.classifications."docs/plans/history.md"]\n'
                'kind="history"\nowner="maintainer"\nreason="closed cycle"\nindex="docs/index.md"\n', encoding='utf-8')
            result = build_system_file_hygiene_audit(root)
            self.assertTrue(next(r for r in result['inventory'] if r['path'] == 'docs/plans/history.md')['size_exempt'])
            with (root / 'docs/plans/history.md').open('ab') as handle:
                handle.write(b'\n- Status: planned\n')
            result = build_system_file_hygiene_audit(root)
            self.assertTrue(any(f['code'] == 'document_budget_invalid' for f in result['findings']))

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
        self.assertIn(".codex/artifact-templates/*.md", classes["artifact_templates"]["patterns"])
        self.assertIn("docs/superpowers/plans/*task-matrix*.md", classes["docs_source_control"]["patterns"])

    def test_task_matrix_hygiene_uses_existing_template_and_docs_source_ownership_without_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root)
            template_path = root / ".codex" / "artifact-templates" / "task-matrix-plan.md"
            docs_plan_path = root / "docs" / "superpowers" / "plans" / "2026-06-08-task-matrix-plan.md"
            template_path.parent.mkdir(parents=True)
            docs_plan_path.parent.mkdir(parents=True)
            template_path.write_text(
                "# Task Matrix Template\n\nSchema version: task_matrix_plan_v1\n",
                encoding="utf-8",
            )
            docs_plan_path.write_text(
                "# Task Matrix Plan\n\nSource status: generated planning evidence, not completion evidence.\n",
                encoding="utf-8",
            )
            fixed_mtime = datetime(2026, 5, 1, 12, 0, 0, tzinfo=UTC).timestamp()
            os.utime(docs_plan_path, (fixed_mtime, fixed_mtime))
            before = _workspace_files(root)

            packet = build_system_file_hygiene_audit(
                root,
                audit_trigger="soft_size_review",
                audit_started_at="2026-06-08T12:00:00+00:00",
            )
            after = _workspace_files(root)

        statuses = {item["path"]: item for item in packet["file_statuses"]}
        findings = json.dumps(packet["findings"], sort_keys=True)

        self.assertEqual(before, after)
        self.assertEqual(statuses[".codex/artifact-templates/task-matrix-plan.md"]["class"], "artifact_templates")
        self.assertEqual(statuses[".codex/artifact-templates/task-matrix-plan.md"]["owner"], "docs maintainer")
        self.assertEqual(statuses["docs/superpowers/plans/2026-06-08-task-matrix-plan.md"]["class"], "docs_source_control")
        self.assertEqual(statuses["docs/superpowers/plans/2026-06-08-task-matrix-plan.md"]["owner"], "docs maintainer")
        self.assertEqual(statuses["docs/superpowers/plans/2026-06-08-task-matrix-plan.md"]["state"], "stale")
        self.assertEqual(
            statuses["docs/superpowers/plans/2026-06-08-task-matrix-plan.md"]["top_finding"],
            "mtime_older_than_30_days",
        )
        self.assertEqual(packet["summary"]["no_secrets_status"], "passed")
        self.assertNotIn("secret_like_literal", findings)
        self.assertEqual(validate_system_file_hygiene_audit(packet), [])

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

    def test_batch36e_file_status_projection_is_bounded_secret_free_and_relative(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root)
            plan = root / "PLAN.md"
            plan_text = "# PLAN.md\n\nOPENAI_API_KEY = \"sk-test\"\n"
            plan.write_text(plan_text, encoding="utf-8")
            written_plan_text = plan.read_bytes().decode("utf-8")
            fixed_mtime = datetime(2026, 6, 5, 12, 0, 0, tzinfo=UTC).timestamp()
            os.utime(plan, (fixed_mtime, fixed_mtime))
            packet = build_system_file_hygiene_audit(
                root,
                audit_trigger="soft_size_review",
                audit_started_at="2026-06-07T12:00:00+00:00",
            )

        statuses = {item["path"]: item for item in packet["file_statuses"]}
        serialized = json.dumps(packet, sort_keys=True)
        plan_status = statuses["PLAN.md"]

        self.assertEqual(packet["last_audit_at"], "2026-06-07T12:00:00+00:00")
        self.assertEqual(plan_status["path"], "PLAN.md")
        self.assertEqual(plan_status["class"], "root_control_plane")
        self.assertEqual(plan_status["owner"], "project root")
        self.assertEqual(plan_status["state"], "blocked")
        self.assertEqual(plan_status["severity"], "error")
        self.assertEqual(plan_status["finding_count"], 1)
        self.assertEqual(plan_status["size"], len(written_plan_text))
        self.assertEqual(plan_status["line_count"], written_plan_text.count("\n") + 1)
        self.assertEqual(plan_status["mtime_utc"], "2026-06-05T12:00:00+00:00")
        self.assertEqual(plan_status["age_days"], 2)
        self.assertRegex(plan_status["content_digest"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(plan_status["last_audit_at"], "2026-06-07T12:00:00+00:00")
        self.assertNotIn(str(root), serialized)
        self.assertNotIn("sk-test", serialized)
        self.assertNotIn("OPENAI_API_KEY =", serialized)
        self.assertEqual(validate_system_file_hygiene_audit(packet), [])

        invalid_packet = json.loads(json.dumps(packet))
        invalid_packet["file_statuses"][0]["path"] = str(root / "PLAN.md")
        self.assertIn("file_statuses:invalid", validate_system_file_hygiene_audit(invalid_packet))

    def test_batch36f_file_status_projection_includes_missing_and_unreadable_dashboard_states(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_control_plane(root, omit={"EVALS.md"})
            broken_skill = root / ".codex" / "skills" / "broken" / "SKILL.md"
            broken_skill.parent.mkdir(parents=True)
            broken_skill.write_bytes(b"\xff\xfe\x00")

            packet = build_system_file_hygiene_audit(
                root,
                audit_trigger="status_dashboard_projection",
                audit_started_at="2026-06-07T12:00:00+00:00",
            )

        statuses = {item["path"]: item for item in packet["file_statuses"]}

        self.assertEqual(statuses["EVALS.md"]["state"], "missing")
        self.assertEqual(statuses["EVALS.md"]["severity"], "warning")
        self.assertEqual(statuses["EVALS.md"]["class"], "root_control_plane")
        self.assertEqual(statuses["EVALS.md"]["top_finding"], "missing_control_plane_file")
        self.assertEqual(statuses[".codex/skills/broken/SKILL.md"]["state"], "unreadable")
        self.assertEqual(statuses[".codex/skills/broken/SKILL.md"]["severity"], "error")
        self.assertEqual(statuses[".codex/skills/broken/SKILL.md"]["class"], "codex_skills")
        self.assertEqual(statuses[".codex/skills/broken/SKILL.md"]["top_finding"], "unreadable_utf8")
        self.assertEqual(validate_system_file_hygiene_audit(packet), [])

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
            (root / "REQUIREMENTS.md").write_text("# REQUIREMENTS.md\n\n" + ("x" * 33000), encoding="utf-8")
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
