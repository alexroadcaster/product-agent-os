import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.batch39_m21_plugin_skill_pilot import (
    M21_ATTEMPT_SCHEMA_VERSION,
    M21_ROLLUP_SCHEMA_VERSION,
    build_m21_attempt_summary,
    build_m21_three_target_rollup,
    validate_m21_attempt_summary,
    validate_m21_three_target_rollup,
    write_m21_evidence_pack,
)
from product_agent_os.first_run_analysis import (
    run_first_project_analysis,
)


FIXTURE = ROOT / "tests" / "fixtures" / "product_agent_os" / "batch39-m21-plugin-skill-fixture"


class Batch39M21PluginSkillPilotTests(unittest.TestCase):
    maxDiff = None

    def test_three_attempt_rollup_preserves_expected_boundaries(self):
        attempts = [
            build_m21_attempt_summary(
                attempt_id="B39-TEST-M21-A01",
                target_label="synthetic_plugin_skill_fixture",
                target_kind="synthetic_fixture",
                mode="synthetic_local",
                source_policy_status="verified_synthetic",
                first_run_packet=run_first_project_analysis(
                    FIXTURE,
                    generated_at="2026-06-18T00:00:00Z",
                    write=False,
                ),
                rendered_artifact={
                    "status": "rendered_in_temp_copy",
                    "page_count": 11,
                    "manifest_ref": "tmp-analysis/analysis-manifest.json",
                    "packet_ref": "tmp-analysis/first-run-analysis-packet.json",
                },
            ),
            build_m21_attempt_summary(
                attempt_id="B39-TEST-M21-A02",
                target_label="Neural Flow",
                target_kind="approved_read_only_target",
                mode="read_only_comparative",
                source_policy_status="present_unverified",
                first_run_packet={"workspace": {"detected_archetypes": ["docs", "plugin_skill"]}},
            ),
            build_m21_attempt_summary(
                attempt_id="B39-TEST-M21-A03",
                target_label="SOL",
                target_kind="approved_read_only_target",
                mode="read_only_real_target",
                source_policy_status="present_unverified",
                first_run_packet={"workspace": {"detected_archetypes": ["web_frontend", "backend_api"]}},
            ),
        ]

        for attempt in attempts:
            validate_m21_attempt_summary(attempt)
            self.assertEqual(attempt["schema_version"], M21_ATTEMPT_SCHEMA_VERSION)
            self.assertEqual(attempt["approval_boundary"]["target_workspace_mutation"], "not_performed")
            self.assertEqual(attempt["generated_view_policy"], "orientation_only_not_proof")

        self.assertEqual(attempts[0]["summary_status"], "passed_contract_guardrail")
        self.assertEqual(attempts[0]["plugin_skill_contract"]["status"], "passed")
        self.assertEqual(attempts[0]["first_run_artifact"]["page_count"], 11)
        self.assertEqual(attempts[0]["synthetic_write_status"], "allowed_generated_analysis_only")

        self.assertEqual(attempts[1]["summary_status"], "blocked_expected_source_policy")
        self.assertIn("release_readiness", attempts[1]["unsupported_claims"])
        self.assertEqual(attempts[1]["comparison_role"], "expected_block_behavior")

        self.assertEqual(attempts[2]["summary_status"], "inspection_only_real_target_value")
        self.assertEqual(
            attempts[2]["first_run_artifact_usefulness"]["status"],
            "usefulness_signal_recorded",
        )

        rollup = build_m21_three_target_rollup(
            attempts,
            generated_at="2026-06-18T00:00:00Z",
        )
        validate_m21_three_target_rollup(rollup)
        self.assertEqual(rollup["schema_version"], M21_ROLLUP_SCHEMA_VERSION)
        self.assertEqual(rollup["attempt_count"], 3)
        self.assertEqual(rollup["rollup_status"], "accepted_risk_three_target_evidence")
        self.assertFalse(rollup["release_readiness_supported"])
        self.assertFalse(rollup["target_mutation_performed"])
        self.assertEqual(rollup["next_route"], "B39-S3")

    def test_evidence_pack_writer_has_stable_file_names_and_no_absolute_path_leaks(self):
        attempt = build_m21_attempt_summary(
            attempt_id="B39-TEST-M21-A01",
            target_label="synthetic_plugin_skill_fixture",
            target_kind="synthetic_fixture",
            mode="synthetic_local",
            source_policy_status="verified_synthetic",
            first_run_packet=run_first_project_analysis(
                FIXTURE,
                generated_at="2026-06-18T00:00:00Z",
                write=False,
            ),
            rendered_artifact={"status": "rendered_in_temp_copy", "page_count": 11},
        )
        rollup = build_m21_three_target_rollup([attempt], generated_at="2026-06-18T00:00:00Z")

        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            written = write_m21_evidence_pack(output_dir, [attempt], rollup)

            self.assertEqual(
                set(written),
                {
                    "batch39-m21-synthetic-plugin-skill-summary.json",
                    "batch39-m21-three-target-rollup.json",
                },
            )
            payload = (output_dir / "batch39-m21-synthetic-plugin-skill-summary.json").read_text(
                encoding="utf-8"
            )
            self.assertNotIn(str(FIXTURE), payload)
            self.assertNotIn(str(ROOT), payload)
            self.assertEqual(json.loads(payload)["attempt_id"], "B39-TEST-M21-A01")

    def test_cli_generates_evidence_without_mutating_real_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "specs"
            target_copy = Path(tmp) / "synthetic-copy"
            shutil.copytree(FIXTURE, target_copy)

            command = [
                sys.executable,
                str(ROOT / "plugins" / "product-agent-os" / "scripts" / "create_batch39_m21_evidence_pack.py"),
                "--output-dir",
                str(output_dir),
                "--synthetic-target",
                str(target_copy),
                "--neural-flow-target",
                str(target_copy),
                "--sol-target",
                str(target_copy),
                "--generated-at",
                "2026-06-18T00:00:00Z",
            ]
            result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((target_copy / ".codex" / "product-agent-os" / "analysis").exists())
            expected_files = {
                "batch39-m21-synthetic-plugin-skill-summary.json",
                "batch39-m21-neural-flow-readonly-summary.json",
                "batch39-m21-sol-readonly-summary.json",
                "batch39-m21-three-target-rollup.json",
            }
            self.assertEqual({path.name for path in output_dir.iterdir()}, expected_files)
            combined = "\n".join(path.read_text(encoding="utf-8") for path in output_dir.iterdir())
            self.assertNotIn(str(target_copy), combined)
            self.assertNotIn(str(output_dir), combined)
            self.assertIn("target_workspace_mutation", combined)


if __name__ == "__main__":
    unittest.main()
