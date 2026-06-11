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


from product_agent_os.batch39_pilot_manifest import (  # noqa: E402
    PILOT_RUN_MANIFEST_SCHEMA,
    build_pilot_run_manifest,
    validate_pilot_run_manifest,
)


class Batch39PilotManifestTests(unittest.TestCase):
    def test_builds_manifest_with_completion_skeptic_and_approval_boundaries(self) -> None:
        manifest = build_pilot_run_manifest(
            test_id="B39-TEST-M02",
            attempt_id="B39-TEST-M02-A01",
            slice_id="B39-S1",
            pilot_id="synthetic-docs-pilot",
            archetype="docs_research",
            target_ref="docs/superpowers/specs",
            source_inventory_ref="docs/superpowers/specs/batch39-m01-inventory.json",
            generated_at="2026-06-11T00:00:00+00:00",
            commands_planned=["python -m unittest tests.product_agent_os.test_batch39_pilot_manifest -v"],
            evidence_artifacts=["docs/superpowers/specs/pilot-run-manifest.example.json"],
        )

        self.assertEqual(manifest["schema_version"], "pilot_run_manifest_v1")
        self.assertEqual(manifest["test_id"], "B39-TEST-M02")
        self.assertEqual(manifest["attempt_id"], "B39-TEST-M02-A01")
        self.assertEqual(manifest["completion_skeptic"]["verdict"], "not_run")
        self.assertEqual(manifest["completion_skeptic"]["promotion_boundary"], "manual_only_not_promoted")
        self.assertEqual(manifest["completion_skeptic"]["failure_classes"], [])
        self.assertEqual(manifest["approval_boundary"]["target_workspace_mutation"], "not_performed")
        self.assertEqual(manifest["approval_boundary"]["provider_or_api_calls"], "not_performed")
        self.assertEqual(manifest["redaction"]["raw_private_logs_stored"], False)
        self.assertEqual(manifest["status"]["overall"], "ready_for_planned_pilot")
        self.assertTrue(manifest["manifest_digest"].startswith("sha256:"))
        self.assertEqual(validate_pilot_run_manifest(manifest), [])

    def test_schema_declares_required_manifest_fields(self) -> None:
        required = set(PILOT_RUN_MANIFEST_SCHEMA["required"])

        for field in [
            "schema_version",
            "test_id",
            "attempt_id",
            "slice",
            "pilot",
            "source_inventory_ref",
            "approval_boundary",
            "execution_plan",
            "completion_skeptic",
            "redaction",
            "status",
            "manifest_digest",
        ]:
            self.assertIn(field, required)

        completion_required = set(
            PILOT_RUN_MANIFEST_SCHEMA["properties"]["completion_skeptic"]["required"]
        )
        for field in [
            "doubt_packet_ref",
            "verdict",
            "trigger",
            "failure_classes",
            "accepted_gap_refs",
            "scorecard_ref",
            "promotion_boundary",
        ]:
            self.assertIn(field, completion_required)

    def test_validation_rejects_missing_completion_skeptic_fields_and_path_leaks(self) -> None:
        manifest = build_pilot_run_manifest(
            test_id="B39-TEST-M02",
            attempt_id="B39-TEST-M02-A01",
            slice_id="B39-S1",
            pilot_id="synthetic-docs-pilot",
            archetype="docs_research",
            target_ref="docs/superpowers/specs",
            source_inventory_ref="docs/superpowers/specs/batch39-m01-inventory.json",
            generated_at="2026-06-11T00:00:00+00:00",
        )
        manifest["completion_skeptic"].pop("promotion_boundary")
        manifest["target"] = r"C:\Users\user\secret-project"

        errors = validate_pilot_run_manifest(manifest)

        self.assertIn("completion_skeptic.promotion_boundary is required", errors)
        self.assertIn("local absolute path leaked", errors)

    def test_cli_writes_manifest_and_schema_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "pilot-run-manifest.example.json"
            schema_output = Path(tmp) / "pilot-run-manifest.schema.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "create_pilot_run_manifest.py"),
                    "--output",
                    str(output),
                    "--schema-output",
                    str(schema_output),
                    "--test-id",
                    "B39-TEST-M02",
                    "--attempt-id",
                    "B39-TEST-M02-A01",
                    "--slice",
                    "B39-S1",
                    "--pilot-id",
                    "synthetic-docs-pilot",
                    "--archetype",
                    "docs_research",
                    "--target-ref",
                    "docs/superpowers/specs",
                    "--source-inventory-ref",
                    "docs/superpowers/specs/batch39-m01-inventory.json",
                    "--command-planned",
                    "python -m unittest tests.product_agent_os.test_batch39_pilot_manifest -v",
                    "--evidence-artifact",
                    "docs/superpowers/specs/pilot-run-manifest.example.json",
                    "--generated-at",
                    "2026-06-11T00:00:00+00:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            manifest = json.loads(output.read_text(encoding="utf-8"))
            schema = json.loads(schema_output.read_text(encoding="utf-8"))
            self.assertEqual(validate_pilot_run_manifest(manifest), [])
            self.assertEqual(schema["title"], "Batch 39 Pilot Run Manifest")
            self.assertIn('"status": "ok"', result.stdout)


if __name__ == "__main__":
    unittest.main()
