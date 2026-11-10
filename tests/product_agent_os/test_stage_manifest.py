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

from product_agent_os.infrastructure import stage_infrastructure  # noqa: E402
from product_agent_os.stage_manifest import (  # noqa: E402
    APPROVAL_TEMPLATE_NAME,
    MANIFEST_NAME,
    build_approval_template,
    content_digest,
    load_stage_manifest,
    validate_approval_record,
    validate_stage_manifest,
)


class StageManifestTest(unittest.TestCase):
    def test_stage_mode_writes_manifest_with_file_digests(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)

            result = stage_infrastructure(workspace, stage_root, legacy_catalog=True)
            manifest_path = stage_root / MANIFEST_NAME
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

            self.assertTrue(manifest_path.exists())
            self.assertEqual(manifest["schema_version"], 1)
            self.assertEqual(manifest["renderer"], "product-agent-os")
            self.assertTrue(manifest["renderer_version"])
            self.assertEqual(manifest["workspace"], str(workspace.resolve()))
            self.assertIn("generated_at", manifest)
            self.assertRegex(manifest["workspace_audit_digest"], r"^sha256:[0-9a-f]{64}$")
            self.assertRegex(manifest["infrastructure_plan_digest"], r"^sha256:[0-9a-f]{64}$")
            self.assertEqual(manifest["validation"]["ok"], True)
            self.assertEqual(result["rendered_artifacts"]["manifest_path"], str(manifest_path))
            self.assertTrue(any(item["target_path"] == "AGENTS.md" for item in manifest["files"]))
            for item in manifest["files"]:
                if item["action"] == "blocked":
                    continue
                self.assertRegex(item["digest"], r"^sha256:[0-9a-f]{64}$")

    def test_workspace_audit_digest_changes_when_workspace_target_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            first_stage = Path(tmp) / "stage-1"
            second_stage = Path(tmp) / "stage-2"
            shutil.copytree(FIXTURES / "empty-repo", workspace)

            stage_infrastructure(workspace, first_stage, legacy_catalog=True)
            first_manifest = load_stage_manifest(first_stage)
            (workspace / "AGENTS.md").write_text("# Existing rules\n\nUser-authored content.\n", encoding="utf-8")
            stage_infrastructure(workspace, second_stage, legacy_catalog=True)
            second_manifest = load_stage_manifest(second_stage)

        self.assertNotEqual(
            first_manifest["workspace_audit_digest"],
            second_manifest["workspace_audit_digest"],
        )

    def test_load_stage_manifest_rejects_missing_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError) as error:
                load_stage_manifest(Path(tmp))

        self.assertIn("stage manifest does not exist", str(error.exception))

    def test_load_stage_manifest_rejects_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            stage_root = Path(tmp)
            (stage_root / MANIFEST_NAME).write_text("{", encoding="utf-8")

            with self.assertRaises(ValueError) as error:
                load_stage_manifest(stage_root)

        self.assertIn("invalid stage manifest json", str(error.exception))

    def test_load_stage_manifest_rejects_non_utf8_manifest_as_value_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            stage_root = Path(tmp)
            (stage_root / MANIFEST_NAME).write_bytes(b"\xff\xfe\xfa")

            with self.assertRaises(ValueError) as error:
                load_stage_manifest(stage_root)

        self.assertIn("unable to read stage manifest", str(error.exception))

    def test_load_stage_manifest_rejects_unsafe_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            stage_root = Path(tmp)
            manifest = _valid_manifest()
            manifest["files"] = [_file_entry(target_path="../AGENTS.md")]
            (stage_root / MANIFEST_NAME).write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaises(ValueError) as error:
                load_stage_manifest(stage_root)

        self.assertIn("target path escapes workspace: ../AGENTS.md", str(error.exception))

    def test_load_stage_manifest_rejects_invalid_file_entry_from_disk(self):
        with tempfile.TemporaryDirectory() as tmp:
            stage_root = Path(tmp)
            manifest = _valid_manifest()
            manifest["files"] = [_file_entry(action="rewrite")]
            (stage_root / MANIFEST_NAME).write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaises(ValueError) as error:
                load_stage_manifest(stage_root)

        self.assertIn("invalid action for staged file AGENTS.md: rewrite", str(error.exception))

    def test_load_stage_manifest_rejects_missing_required_top_level_fields(self):
        for field in ["generated_at", "workspace_audit_digest", "infrastructure_plan_digest"]:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp:
                    stage_root = Path(tmp)
                    manifest = _valid_manifest()
                    del manifest[field]
                    (stage_root / MANIFEST_NAME).write_text(json.dumps(manifest), encoding="utf-8")

                    with self.assertRaises(ValueError) as error:
                        load_stage_manifest(stage_root)

                self.assertIn(f"{field} is required", str(error.exception))

    def test_load_stage_manifest_rejects_invalid_generated_at_values(self):
        for value in [
            "",
            "not-a-date",
            "2026-05-14",
            "2026-05-14T12:00:00",
            "2026-99-99T99:99:99+00:00",
        ]:
            with self.subTest(value=value):
                with tempfile.TemporaryDirectory() as tmp:
                    stage_root = Path(tmp)
                    manifest = _valid_manifest()
                    manifest["generated_at"] = value
                    (stage_root / MANIFEST_NAME).write_text(json.dumps(manifest), encoding="utf-8")

                    with self.assertRaises(ValueError) as error:
                        load_stage_manifest(stage_root)

                self.assertIn("generated_at must be a valid ISO datetime", str(error.exception))

    def test_validate_stage_manifest_rejects_unsafe_paths(self):
        manifest = _valid_manifest()
        manifest["files"] = [
            _file_entry(target_path=""),
            _file_entry(target_path="C:/workspace/AGENTS.md"),
            _file_entry(target_path="/tmp/AGENTS.md"),
            _file_entry(target_path="\\tmp\\AGENTS.md"),
            _file_entry(target_path="../AGENTS.md"),
            _file_entry(staged_path=""),
            _file_entry(staged_path="C:/stage/AGENTS.md"),
            _file_entry(staged_path="/tmp/AGENTS.md"),
            _file_entry(staged_path="\\tmp\\AGENTS.md"),
            _file_entry(staged_path="../AGENTS.md"),
        ]

        errors = validate_stage_manifest(manifest)

        self.assertIn("target path escapes workspace: ", errors)
        self.assertIn("target path escapes workspace: C:/workspace/AGENTS.md", errors)
        self.assertIn("target path escapes workspace: /tmp/AGENTS.md", errors)
        self.assertIn("target path escapes workspace: \\tmp\\AGENTS.md", errors)
        self.assertIn("target path escapes workspace: ../AGENTS.md", errors)
        self.assertIn("staged path escapes stage root: ", errors)
        self.assertIn("staged path escapes stage root: C:/stage/AGENTS.md", errors)
        self.assertIn("staged path escapes stage root: /tmp/AGENTS.md", errors)
        self.assertIn("staged path escapes stage root: \\tmp\\AGENTS.md", errors)
        self.assertIn("staged path escapes stage root: ../AGENTS.md", errors)

    def test_validate_stage_manifest_rejects_missing_required_file_entry_fields(self):
        missing_action = _file_entry()
        del missing_action["action"]
        missing_write_policy = _file_entry()
        del missing_write_policy["write_policy"]
        missing_managed_section = _file_entry()
        del missing_managed_section["managed_section"]
        manifest = _valid_manifest()
        manifest["files"] = [missing_action, missing_write_policy, missing_managed_section]

        errors = validate_stage_manifest(manifest)

        self.assertIn("missing file entry field for AGENTS.md: action", errors)
        self.assertIn("missing file entry field for AGENTS.md: write_policy", errors)
        self.assertIn("missing file entry field for AGENTS.md: managed_section", errors)

    def test_validate_stage_manifest_rejects_invalid_action_and_write_policy_values(self):
        manifest = _valid_manifest()
        manifest["files"] = [
            _file_entry(action="rewrite"),
            _file_entry(write_policy="direct_write"),
        ]

        errors = validate_stage_manifest(manifest)

        self.assertIn("invalid action for staged file AGENTS.md: rewrite", errors)
        self.assertIn("invalid write_policy for staged file AGENTS.md: direct_write", errors)

    def test_validate_stage_manifest_returns_errors_for_malformed_file_entry_types(self):
        manifest = _valid_manifest()
        manifest["files"] = [
            _file_entry(target_path=123),
            _file_entry(staged_path=123),
            _file_entry(managed_section=123),
            _file_entry(action=[]),
            _file_entry(write_policy=[]),
        ]

        errors = validate_stage_manifest(manifest)

        self.assertIn("target_path must be a string", errors)
        self.assertIn("staged_path must be a string", errors)
        self.assertIn("managed_section must be a string for AGENTS.md", errors)
        self.assertIn("action must be a string for staged file AGENTS.md", errors)
        self.assertIn("write_policy must be a string for staged file AGENTS.md", errors)

    def test_approval_template_is_not_an_approval_record(self):
        merge_plan = {
            "id": "merge-plan-abc",
            "decisions": [
                {"target_path": "AGENTS.md", "action": "create_file", "approval_required": True}
            ],
        }

        template = build_approval_template(merge_plan)
        errors = validate_approval_record(template, "merge-plan-abc", ["AGENTS.md"], ["create_file"])

        self.assertEqual(template["approval"]["schema_version"], 1)
        self.assertEqual(template["approval"]["merge_plan_id"], "merge-plan-abc")
        self.assertEqual(template["approval"]["approved_by"], "")
        self.assertIn("approved_by is required", errors)

    def test_completed_approval_record_must_match_plan_targets_and_actions(self):
        approval = {
            "approval": {
                "schema_version": 1,
                "merge_plan_id": "merge-plan-abc",
                "approved_by": "user",
                "approved_at": "2026-05-14T12:00:00+00:00",
                "approved_targets": ["AGENTS.md"],
                "approved_actions": ["create_file"],
                "accepted_risks": ["local workspace write"],
                "denied_targets": [],
                "notes": "Approved for fixture apply.",
                "enable_hooks": False,
                "approved_hook_events": [],
                "blocking_hooks": [],
                "hook_rollback": "",
            }
        }

        errors = validate_approval_record(approval, "merge-plan-abc", ["AGENTS.md"], ["create_file"])

        self.assertEqual(errors, [])

    def test_completed_approval_record_rejects_bare_plan_id(self):
        errors = validate_approval_record("merge-plan-abc", "merge-plan-abc", ["AGENTS.md"], ["create_file"])

        self.assertIn("approval record must be an object", errors)

    def test_approval_record_rejects_invalid_approved_at_values(self):
        for value in ["not-a-date", "2026-05-14", "2026-05-14T12:00:00"]:
            with self.subTest(value=value):
                approval = _valid_approval_record()
                approval["approval"]["approved_at"] = value

                errors = validate_approval_record(approval, "merge-plan-abc", ["AGENTS.md"], ["create_file"])

                self.assertIn("approved_at must be a valid ISO datetime with timezone", errors)

    def test_approval_record_rejects_missing_full_contract_fields(self):
        for field in [
            "denied_targets",
            "notes",
            "enable_hooks",
            "approved_hook_events",
            "blocking_hooks",
            "hook_rollback",
        ]:
            with self.subTest(field=field):
                approval = _valid_approval_record()
                del approval["approval"][field]

                errors = validate_approval_record(approval, "merge-plan-abc", ["AGENTS.md"], ["create_file"])

                self.assertIn(f"{field} is required", errors)

    def test_approval_record_rejects_wrong_type_full_contract_fields(self):
        invalid_values = {
            "denied_targets": "AGENTS.md",
            "notes": [],
            "enable_hooks": "false",
            "approved_hook_events": "SessionStart",
            "blocking_hooks": "PreToolUse",
            "hook_rollback": [],
        }
        for field, value in invalid_values.items():
            with self.subTest(field=field):
                approval = _valid_approval_record()
                approval["approval"][field] = value

                errors = validate_approval_record(approval, "merge-plan-abc", ["AGENTS.md"], ["create_file"])

                self.assertIn(f"{field} has invalid type", errors)

    def test_approval_record_rejects_target_and_action_lists_with_non_string_items(self):
        invalid_values = {
            "approved_targets": ["AGENTS.md", 1],
            "approved_actions": ["create_file", {"action": "update"}],
        }
        for field, value in invalid_values.items():
            with self.subTest(field=field):
                approval = _valid_approval_record()
                approval["approval"][field] = value

                errors = validate_approval_record(approval, "merge-plan-abc", ["AGENTS.md"], ["create_file"])

                self.assertIn(f"{field} must contain only strings", errors)

    def test_approval_record_rejects_hook_lists_with_non_string_items(self):
        invalid_values = {
            "approved_hook_events": [1],
            "blocking_hooks": [{"event": "PreToolUse"}],
        }
        for field, value in invalid_values.items():
            with self.subTest(field=field):
                approval = _valid_approval_record()
                approval["approval"][field] = value

                errors = validate_approval_record(approval, "merge-plan-abc", ["AGENTS.md"], ["create_file"])

                self.assertIn(f"{field} must contain only strings", errors)

    def test_approval_record_rejects_risk_and_denied_target_lists_with_non_string_items(self):
        invalid_values = {
            "accepted_risks": ["local workspace write", 1],
            "denied_targets": ["AGENTS.md", {"target": "PLAN.md"}],
        }
        for field, value in invalid_values.items():
            with self.subTest(field=field):
                approval = _valid_approval_record()
                approval["approval"][field] = value

                errors = validate_approval_record(approval, "merge-plan-abc", ["AGENTS.md"], ["create_file"])

                self.assertIn(f"{field} must contain only strings", errors)

    def test_content_digest_is_stable_sha256(self):
        self.assertEqual(
            content_digest("Product-Agent OS\n"),
            "sha256:6f316a8ae91c7998521da8286e88cae5ac6eac803ff45a8aa76a91b71a2e22be",
        )

    def test_approval_template_name_is_stable(self):
        self.assertEqual(APPROVAL_TEMPLATE_NAME, "product-agent-os-approval-template.json")


def _valid_manifest():
    return {
        "schema_version": 1,
        "renderer": "product-agent-os",
        "renderer_version": "0.1.0",
        "workspace": "C:/workspace/project",
        "generated_at": "2026-05-14T00:00:00+00:00",
        "workspace_audit_digest": "sha256:" + "1" * 64,
        "infrastructure_plan_digest": "sha256:" + "2" * 64,
        "validation": {"ok": True, "checks": [], "errors": {}},
        "files": [_file_entry()],
    }


def _file_entry(
    target_path="AGENTS.md",
    staged_path="AGENTS.md",
    action="create",
    write_policy="staged_only",
    managed_section="project-rules",
):
    return {
        "target_path": target_path,
        "staged_path": staged_path,
        "action": action,
        "write_policy": write_policy,
        "digest": "sha256:" + "0" * 64,
        "managed_section": managed_section,
    }


def _valid_approval_record():
    return {
        "approval": {
            "schema_version": 1,
            "merge_plan_id": "merge-plan-abc",
            "approved_by": "user",
            "approved_at": "2026-05-14T12:00:00+00:00",
            "approved_targets": ["AGENTS.md"],
            "approved_actions": ["create_file"],
            "accepted_risks": ["local workspace write"],
            "denied_targets": [],
            "notes": "Approved for fixture apply.",
            "enable_hooks": False,
            "approved_hook_events": [],
            "blocking_hooks": [],
            "hook_rollback": "",
        }
    }


if __name__ == "__main__":
    unittest.main()
