import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.validators import (  # noqa: E402
    validate_agent_file,
    validate_agent_project_config,
    validate_control_plane,
    validate_doubt_verification_packet_file,
    validate_hook_file,
    validate_task_matrix_file,
    validate_task_matrix_text,
)


class ValidatorsTest(unittest.TestCase):
    def test_lifecycle_packet_contracts_validate_content_and_closure_limits(self):
        from product_agent_os import validators
        validate = getattr(validators, "validate_lifecycle_packet_text", None)
        self.assertTrue(callable(validate), "lifecycle packet validation must be available")
        start_fields = ["Request", "Goal", "Context", "Scope", "Value", "Execution", "Acceptance", "Risks / approvals", "Next step"]
        start = "\n\n".join("**" + name + "**\nConcrete evidence and bounded task scope." for name in start_fields)
        self.assertEqual(validate(start, "start"), [])
        self.assertTrue(validate("# Task Start Brief", "start"))
        self.assertTrue(validate(start.replace("**Goal**\nConcrete evidence and bounded task scope.", "**Goal**"), "start"))
        self.assertTrue(validate("```text\n" + start + "\n```", "start"))
        fields = ["Result", "Scope", "Evidence", "Review", "Limits", "Tech debt", "Activation / fallback", "Docs impact", "Context integrity", "Runtime metrics", "Closure", "Next step", "Execution time"]
        values = {name: "N/A — no affected surface in this bounded task" for name in fields}
        values.update(Review="context_mode = self_review; tester_verdict = closed_allowed", Closure="closure_level = docs_static_verified", **{"Docs impact": "updated; docs/example.md; docs check exit 0"})
        ledger = "closure_contract: product-agent-os-completion-ledger-v2\n" + "\n".join("- " + name + ": " + values[name] for name in fields)
        self.assertEqual(validate(ledger, "completion"), [])
        bold = ledger
        for name in fields:
            bold = bold.replace("- " + name + ":", "- **" + name + ":**")
        self.assertEqual(validate(bold, "completion"), [])
        self.assertTrue(validate(bold.replace("closure_level = docs_static_verified", "docs_static_verified"), "completion"))
        self.assertTrue(validate(bold.replace("closed_allowed", "partial_only"), "completion"))
        self.assertTrue(validate(bold + "\n- Result: duplicate", "completion"))
        for invalid in (ledger.replace("- Evidence:", "Evidence:"), ledger.replace(values["Execution time"], "not_available"), ledger.replace("closed_allowed", "not_reviewed"), ledger.replace("updated; docs/example.md; docs check exit 0", "accepted_gap; owner: docs; next: review")):
            with self.subTest(invalid=invalid[:70]):
                self.assertTrue(validate(invalid, "completion"))
        self.assertTrue(validate(ledger.replace("product-agent-os-completion-ledger-v2", "trade-completion-ledger-v2"), "completion"))

    def test_control_plane_reports_missing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = validate_control_plane(Path(tmp))
        self.assertIn("AGENTS.md", result["missing"])
        self.assertFalse(result["ok"])

    def test_agent_file_accepts_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "reviewer.toml"
            path.write_text(
                'name = "reviewer"\n'
                'description = "Reviews correctness and missing tests."\n'
                'developer_instructions = "Ownership: review findings. Inputs: diff and verification evidence. '
                'Outputs: findings and risks. Stop conditions: stop when evidence is missing. '
                'Handoff: return files reviewed and open risks."\n',
                encoding="utf-8",
            )
            self.assertEqual(validate_agent_file(path), [])

    def test_agent_file_rejects_unsupported_runtime_policy_and_prompt_debt(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "reviewer.toml"
            path.write_text(
                'name = "reviewer"\n'
                'description = "Reviews changes."\n'
                'model = "gpt-5.5"\n'
                'model_reasoning_effort = "extreme"\n'
                'sandbox_mode = "danger-full-access"\n'
                'developer_instructions = "Ownership: review. Inputs: diff. Outputs: findings. '
                'Stop conditions: missing evidence. Handoff: risks. Track 9 routing."\n',
                encoding="utf-8",
            )

            errors = validate_agent_file(path)

        self.assertIn("unsupported agent model: gpt-5.5", errors)
        self.assertIn("unsupported model_reasoning_effort: extreme", errors)
        self.assertIn("parent-only agent setting: sandbox_mode", errors)
        self.assertIn("developer_instructions contain volatile phase identifier", errors)

    def test_agent_file_rejects_missing_skill_and_openai_docs_without_mcp(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            openai_docs = root / "openai-docs" / "SKILL.md"
            openai_docs.parent.mkdir(parents=True)
            openai_docs.write_text("# OpenAI Docs\n", encoding="utf-8")
            path = root / "research.toml"
            path.write_text(
                'name = "research"\n'
                'description = "Researches official sources."\n'
                'sandbox_mode = "read-only"\n'
                'mcp_servers = {}\n'
                'developer_instructions = "Ownership: sources. Inputs: question. Outputs: matrix. '
                'Stop conditions: missing source. Handoff: citations."\n'
                '[[skills.config]]\n'
                f'path = "{openai_docs.as_posix()}"\n'
                'enabled = true\n'
                '[[skills.config]]\n'
                f'path = "{(root / "missing" / "SKILL.md").as_posix()}"\n'
                'enabled = true\n',
                encoding="utf-8",
            )

            errors = validate_agent_file(path)

        self.assertIn("parent-only agent setting: mcp_servers", errors)
        self.assertIn("custom agent skills.config may only disable inherited skills", errors)

    def test_agent_file_rejects_workspace_write_without_skill_authority_and_missing_prompt_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            agents = root / ".codex" / "agents"
            skill = root / "plugins" / "product-agent-os" / "skills" / "staged" / "SKILL.md"
            agents.mkdir(parents=True)
            skill.parent.mkdir(parents=True)
            (root / "AGENTS.md").write_text("# Test project\n", encoding="utf-8")
            skill.write_text("Default output only. workspace_apply: forbidden\n", encoding="utf-8")
            path = agents / "builder.toml"
            path.write_text(
                'name = "builder"\n'
                'description = "Builds focused changes."\n'
                'model = "gpt-5.6-terra"\n'
                'model_reasoning_effort = "medium"\n'
                'sandbox_mode = "workspace-write"\n'
                'mcp_servers = {}\n'
                'developer_instructions = "Ownership: assigned files. Inputs: plan. Outputs: patch. '
                'Stop conditions: unsafe scope. Handoff: evidence. Read `docs/missing.md`."\n'
                '[[skills.config]]\n'
                f'path = "{skill.as_posix()}"\n'
                'enabled = true\n',
                encoding="utf-8",
            )

            errors = validate_agent_file(path)
            staged_errors = validate_agent_file(
                path,
                available_prompt_paths={"docs/missing.md"},
            )

        self.assertIn("parent-only agent setting: sandbox_mode", errors)
        self.assertIn("referenced prompt path does not exist: docs/missing.md", errors)
        self.assertNotIn("referenced prompt path does not exist: docs/missing.md", staged_errors)

    def test_project_config_rejects_permission_profile_sandbox_composition(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "config.toml"
            agent = root / "builder.toml"
            config.write_text(
                'default_permissions = ":workspace"\n'
                'sandbox_mode = "workspace-write"\n'
                '[permissions.workspace]\n'
                'extends = ":workspace"\n'
                '[agents]\n'
                'default_subagent_model = "gpt-5.6-terra"\n'
                'default_subagent_reasoning_effort = "medium"\n',
                encoding="utf-8",
            )
            agent.write_text('sandbox_mode = "workspace-write"\n', encoding="utf-8")

            errors = validate_agent_project_config(config, [agent])

        self.assertIn("permission profiles and legacy sandbox_mode must not be composed", errors)
        self.assertIn("builder.toml: parent-only agent setting: sandbox_mode", errors)

    def test_custom_agents_reject_parent_only_settings_even_empty_tables(self):
        settings = {
            "sandbox_mode": '"read-only"', "default_permissions": '":read-only"',
            "permissions": '{}', "sandbox_workspace_write": '{}',
            "approval_policy": '"never"', "approvals_reviewer": '"auto_review"',
            "model_provider": '"openai"', "mcp_servers": '{}',
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "agent.toml"
            for key, value in settings.items():
                with self.subTest(key=key):
                    path.write_text(f'{key} = {value}\n', encoding="utf-8")
                    self.assertIn(f"parent-only agent setting: {key}", validate_agent_file(path))

    def test_custom_agent_inherits_tools_and_accepts_gpt6_with_disabled_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "reviewer.toml"
            text = ('name = "reviewer"\ndescription = "Review"\n'
                    'model = "gpt-6.1-sol"\nmodel_reasoning_effort = "high"\n'
                    'developer_instructions = "Ownership: review. Inputs: diff. Outputs: findings. '
                    'Stop conditions: missing evidence. Handoff: risks."\n'
                    '[features]\napps = false\n'
                    '[[skills.config]]\nname = "unused-skill"\nenabled = false\n')
            path.write_text(text, encoding="utf-8")
            self.assertEqual(validate_agent_file(path), [])
            path.write_text(text.replace('apps = false', 'apps = true'), encoding="utf-8")
            self.assertIn("custom agent feature must disable a supported capability: apps", validate_agent_file(path))

    def test_project_contract_checks_inherited_mcp_and_parent_skill_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "plugins/product-agent-os/skills/docs-maintainer/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("workspace_apply: forbidden\n", encoding="utf-8")
            docs = root / "openai-docs/SKILL.md"
            docs.parent.mkdir()
            docs.write_text("# Docs", encoding="utf-8")
            config = root / "config.toml"
            text = ('default_permissions = ":workspace"\n'
                    '[agents]\ndefault_subagent_model = "gpt-6.1-sol"\n'
                    'default_subagent_reasoning_effort = "medium"\n'
                    f'[[skills.config]]\npath = "{skill.as_posix()}"\nenabled = true\n'
                    f'[[skills.config]]\npath = "{docs.as_posix()}"\nenabled = true\n')
            config.write_text(text, encoding="utf-8")
            errors = validate_agent_project_config(config)
            self.assertIn("parent openai-docs skill requires openaiDeveloperDocs MCP server", errors)
            self.assertIn("parent workspace skills lack explicit task write authority", errors)
            skill.write_text("workspace_apply: explicit_task_authority\n", encoding="utf-8")
            text += '\n[mcp_servers.openaiDeveloperDocs]\nurl = "https://developers.openai.com/mcp"\n'
            config.write_text(text, encoding="utf-8")
            self.assertEqual(validate_agent_project_config(config), [])
            skill.unlink()
            self.assertTrue(any(e.startswith("skill path does not exist:") for e in validate_agent_project_config(config)))

    def test_model_policy_rejects_unsupported_model_effort_pair(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "agent.toml"
            path.write_text('model = "gpt-6.1-sol"\nmodel_reasoning_effort = "none"\n', encoding="utf-8")
            self.assertIn("unsupported model_reasoning_effort for gpt-6.1-sol: none", validate_agent_file(path))

    def test_hook_file_rejects_secret_literal(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hook.py"
            path.write_text('TOKEN = "secret-value"\n', encoding="utf-8")
            errors = validate_hook_file(path)
        self.assertIn("contains forbidden secret-like literal", errors)

    def test_hook_file_rejects_supported_secret_assignment_styles(self):
        samples = [
            'TOKEN = "synthetic-secret"\n',
            'os.environ["API_KEY"] = "synthetic-secret"\n',
            'api_key: "synthetic-secret"\n',
            "PASSWORD=synthetic-secret\n",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            for index, text in enumerate(samples):
                path = Path(tmp) / f"hook-{index}.txt"
                path.write_text(text, encoding="utf-8")
                with self.subTest(text=text):
                    errors = validate_hook_file(path)
                self.assertIn("contains forbidden secret-like literal", errors)

    def test_hook_file_ignores_secret_mentions_in_prose_and_comments(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hook.py"
            path.write_text(
                "# TOKEN should be configured by the operator.\n"
                'print("PASSWORD must not be hardcoded")\n',
                encoding="utf-8",
            )
            self.assertEqual(validate_hook_file(path), [])

    def test_hook_file_allows_os_getenv_secret_name_lookup(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hook.py"
            path.write_text(
                'import os\nAPI_KEY = os.getenv("API_KEY")\n',
                encoding="utf-8",
            )
            self.assertEqual(validate_hook_file(path), [])

    def test_hook_file_allows_os_environ_get_secret_name_lookup(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hook.py"
            path.write_text(
                'TOKEN = os.environ.get("TOKEN")\n',
                encoding="utf-8",
            )
            self.assertEqual(validate_hook_file(path), [])

    def test_task_matrix_validator_accepts_planned_and_implemented_detailed_blocks(self):
        errors = validate_task_matrix_text(VALID_TASK_MATRIX)

        self.assertEqual(errors, [])

    def test_task_matrix_validator_rejects_summary_table_without_detailed_blocks(self):
        errors = validate_task_matrix_text(
            "# Task Matrix\n\n"
            "| Task | Status | Completion report |\n"
            "| --- | --- | --- |\n"
            "| `T10-PLAN-M06` | `implemented` | looked ok |\n"
        )

        self.assertIn("no detailed task blocks found", errors)

    def test_task_matrix_validator_rejects_fake_implemented_completion(self):
        invalid = VALID_TASK_MATRIX.replace(
            "- Date and time of task implementation: 07-06-2026 21:14",
            "- Date and time of task implementation: pending_execution_timestamp",
            1,
        ).replace(
            "- files touched / work locations: plugins/product-agent-os/scripts/product_agent_os/validators.py",
            "- files touched / work locations:",
            1,
        ).replace(
            "- verification evidence: python -m unittest tests.product_agent_os.test_validators -v",
            "- verification evidence: inspection-only review",
            1,
        )

        errors = validate_task_matrix_text(invalid)

        self.assertIn("T10-PLAN-M06: implemented requires actual DD-MM-YYYY HH:mm timestamp", errors)
        self.assertIn("T10-PLAN-M06: implemented requires files touched / work locations", errors)
        self.assertIn("T10-PLAN-M06: implemented cannot use inspection-only verification evidence", errors)

    def test_task_matrix_validator_rejects_planned_rows_with_fake_actual_completion_time(self):
        invalid = VALID_TASK_MATRIX.replace(
            "- actual implementation date and time: pending_execution_timestamp",
            "- actual implementation date and time: 07-06-2026 21:14",
            1,
        )

        errors = validate_task_matrix_text(invalid)

        self.assertIn(
            "T10-PLAN-M10: planned rows must not contain actual implementation date/time",
            errors,
        )

    def test_task_matrix_validator_rejects_unresolved_placeholders_and_missing_completion_report_fields(self):
        invalid = VALID_TASK_MATRIX.replace("Task `T10-PLAN-M10`", "Task `<task_id>`", 1).replace(
            "- residual risks: pending",
            "",
            1,
        )

        errors = validate_task_matrix_text(invalid)

        self.assertIn("<task_id>: unresolved placeholder in task block", errors)
        self.assertIn("<task_id>: missing completion report field: residual risks", errors)

    def test_task_matrix_file_and_cli_return_json_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            valid_path = Path(tmp) / "task-matrix.md"
            invalid_path = Path(tmp) / "invalid-task-matrix.md"
            valid_path.write_text(VALID_TASK_MATRIX, encoding="utf-8")
            invalid_path.write_text("# no tasks\n", encoding="utf-8")

            self.assertEqual(validate_task_matrix_file(valid_path), [])

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_task_matrix.py"),
                    str(invalid_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["errors"], ["no detailed task blocks found"])

    def test_doubt_verification_file_and_cli_return_json_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            valid_path = Path(tmp) / "doubt-packet.json"
            invalid_path = Path(tmp) / "invalid-doubt-packet.json"
            valid_path.write_text(json.dumps(VALID_DOUBT_PACKET), encoding="utf-8")
            invalid_path.write_text(json.dumps({"schema_version": "doubt_verification_packet_v1"}), encoding="utf-8")

            self.assertEqual(validate_doubt_verification_packet_file(valid_path), [])

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_doubt_verification_packet.py"),
                    str(invalid_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assertFalse(payload["ok"])
        self.assertIn("verdict:required", payload["errors"])

    def test_agent_file_reports_invalid_toml(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.toml"
            path.write_text('name = "reviewer"\n[broken\n', encoding="utf-8")
            errors = validate_agent_file(path)
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith("invalid toml: "))

    def test_agent_file_reports_missing_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "incomplete.toml"
            path.write_text('name = "reviewer"\n', encoding="utf-8")
            errors = validate_agent_file(path)
        self.assertEqual(
            errors,
            [
                "missing required field: description",
                "missing required field: developer_instructions",
            ],
        )

    def test_agent_file_reports_non_utf8_file_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.toml"
            path.write_bytes(b"\xff\xfe\x00")
            errors = validate_agent_file(path)
        self.assertEqual(errors, ["unable to read file as utf-8 text"])

    def test_hook_file_reports_non_utf8_file_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.py"
            path.write_bytes(b"\xff\xfe\x00")
            errors = validate_hook_file(path)
        self.assertEqual(errors, ["unable to read file as utf-8 text"])

    def test_agents_wrapper_fails_clearly_when_directory_is_missing(self):
        missing = FIXTURES / "empty-repo" / ".codex" / "agents"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "validate_agents.py"),
                str(missing),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["errors"], ["agent directory does not exist"])

    def test_agents_wrapper_returns_json_for_non_utf8_file_without_stderr(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bad.toml").write_bytes(b"\xff\xfe\x00")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_agents.py"),
                    str(root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assertFalse(payload["ok"])
        self.assertEqual(
            payload["file_errors"],
            {str(root / "bad.toml"): ["unable to read file as utf-8 text"]},
        )

    def test_agents_wrapper_returns_zero_for_valid_temp_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "reviewer.toml"
            path.write_text(
                'name = "reviewer"\n'
                'description = "Reviews correctness and missing tests."\n'
                'developer_instructions = "Ownership: review findings. Inputs: diff and verification evidence. '
                'Outputs: findings and risks. Stop conditions: stop when evidence is missing. '
                'Handoff: return files reviewed and open risks."\n',
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_agents.py"),
                    str(root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["file_errors"], {str(path): []})

    def test_hooks_wrapper_fails_clearly_when_directory_is_missing(self):
        missing = FIXTURES / "empty-repo" / ".codex" / "hooks"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "validate_hooks.py"),
                str(missing),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["errors"], ["hook directory does not exist"])

    def test_hooks_wrapper_returns_json_for_non_utf8_file_without_stderr(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bad.py").write_bytes(b"\xff\xfe\x00")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_hooks.py"),
                    str(root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assertFalse(payload["ok"])
        self.assertEqual(
            payload["file_errors"],
            {str(root / "bad.py"): ["unable to read file as utf-8 text"]},
        )

    def test_hooks_wrapper_validates_hooks_json_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hooks_json = root / "hooks.json"
            hooks_json.write_text(
                json.dumps(
                    {
                        "hooks": {
                            event: [
                                {
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": f"python .codex/hooks/{event}.py",
                                        }
                                    ]
                                }
                            ]
                            for event in ["SessionStart", "PreToolUse", "PermissionRequest", "PostToolUse", "Stop"]
                        }
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_hooks.py"),
                    str(root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["file_errors"], {str(hooks_json): []})

    def test_hooks_wrapper_accepts_single_hooks_json_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hooks_json = root / "hooks.json"
            hooks_json.write_text(
                json.dumps(
                    {
                        "hooks": {
                            event: [
                                {
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": f"python .codex/hooks/{event}.py",
                                        }
                                    ]
                                }
                            ]
                            for event in ["SessionStart", "PreToolUse", "PermissionRequest", "PostToolUse", "Stop"]
                        }
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_hooks.py"),
                    str(hooks_json),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["files"], [str(hooks_json)])

    def test_hooks_wrapper_rejects_incomplete_hooks_json_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hooks_json = root / "hooks.json"
            hooks_json.write_text('{"hooks":{"PreToolUse":[]}}\n', encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_hooks.py"),
                    str(root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(payload["ok"])
        self.assertIn("missing hook event: SessionStart", payload["file_errors"][str(hooks_json)])


VALID_TASK_MATRIX = """# Task Matrix

Source status: local implementation planning

### Task `T10-PLAN-M10`

- Task: T10-PLAN-M10
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: methodology-heavy eval guard
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: T10-PLAN-M04, T10-PLAN-M05, T10-PLAN-M06
- Blocks: T10-PLAN-M14
- Source: Batch 37 task matrix
- Short description: Add behavioral and fixture coverage.
- Technical value: Regression coverage for task-matrix behavior.
- Product value: Users can trust task reports are evidence-bound.
- Scope: Behavioral eval, fixture eval, transcript eval.
- Non-goals: No live model/API eval.
- Expected result: Synthetic evals cover task matrix behavior.
- Acceptance criteria: Detection-only is not completion evidence.
- Verification gates: python -m unittest tests.product_agent_os.test_behavioral_workflow_evals -v
- Risks / approval gates: Synthetic-only coverage.
- Complexity: medium
- Estimated execution time: 1h
- Agents: Tester
- Skills: test-driven-development, verification-before-completion
- Output artifacts: behavioral-workflows.json
- Next step: implement validator

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending

### Task `T10-PLAN-M06`

- Task: T10-PLAN-M06
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: methodology-heavy validator guard
- Validator target: detailed task blocks
- Date and time of task implementation: 07-06-2026 21:14
- Depends on: T10-PLAN-M01, T10-PLAN-M02, T10-PLAN-M04
- Blocks: T10-PLAN-M10, T10-PLAN-M13
- Source: Batch 37 task matrix
- Short description: Add deterministic task-matrix validator.
- Technical value: Enforce evidence-before-completion.
- Product value: Users get factual task reports.
- Scope: Validator and CLI.
- Non-goals: No discovery routing.
- Expected result: Invalid implemented rows fail.
- Acceptance criteria: Validator rejects fake completion.
- Verification gates: python -m unittest tests.product_agent_os.test_validators -v
- Risks / approval gates: Markdown parsing stays conservative.
- Complexity: medium
- Estimated execution time: 2h
- Agents: Builder, Tester
- Skills: test-driven-development, verification-before-completion
- Output artifacts: validate_task_matrix.py
- Next step: add eval guard

#### Completion Report

- status: implemented
- what was done: implemented deterministic validator
- files touched / work locations: plugins/product-agent-os/scripts/product_agent_os/validators.py
- technical value delivered: validator rejects fake completion
- product value delivered: task reports become reviewable
- actual implementation date and time: 07-06-2026 21:14
- verification evidence: python -m unittest tests.product_agent_os.test_validators -v
- residual risks: validator is conservative for Markdown
- follow-up: add behavioral eval guard
"""

VALID_DOUBT_PACKET = {
    "schema_version": "doubt_verification_packet_v1",
    "verdict": "pass",
    "artifact_under_review": {
        "kind": "task_row",
        "path": "docs/sources/product-agent-os-track-10-backlog.md",
        "label": "B40-S2",
    },
    "claim_ledger": [
        {
            "claim_id": "claim-current-evidence",
            "claim": "Focused validator tests ran in the current run.",
            "status": "supported",
            "provenance": {
                "kind": "command",
                "ref": "python -m unittest tests.product_agent_os.test_validators -v",
                "checked_at": "2026-06-09T12:00:00+03:00",
            },
        }
    ],
    "requirement_ledger": [
        {
            "requirement_id": "req-generated-view-boundary",
            "requirement": "Generated dashboards cannot be completion proof.",
            "status": "covered",
            "provenance": {
                "kind": "source",
                "ref": "AGENTS.md generated dashboard policy",
                "checked_at": "2026-06-09T12:00:00+03:00",
            },
        }
    ],
    "evidence_ledger": [
        {
            "evidence_id": "ev-current-unittest",
            "evidence_provider": "command",
            "evidence_role": "proof",
            "status": "available",
            "evidence_ref": "python -m unittest tests.product_agent_os.test_validators -v",
            "provenance": {
                "kind": "command",
                "ref": "focused unit test",
                "checked_at": "2026-06-09T12:00:00+03:00",
            },
        }
    ],
    "approval_boundary": {"status": "not_required", "hits": []},
    "gap_ledger": [],
    "handoff": {
        "verified_claims": ["claim-current-evidence"],
        "unsupported_claims": [],
        "verification_evidence": ["ev-current-unittest"],
        "stop_reason": "doubt_verification_passed",
        "recommended_next_role": "risk-reviewer",
    },
    "source_policy": "doubt verification packet is evidence ledger, not generated dashboard proof",
    "redaction_status": {"status": "clean", "categories": []},
}


if __name__ == "__main__":
    unittest.main()
