from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


class Batch41S6ClosureTests(unittest.TestCase):
    def test_synthetic_e2e_summary_requires_dry_run_stage_questions_and_no_write(self) -> None:
        from product_agent_os.batch41_s6_closure import build_synthetic_e2e_summary  # noqa: PLC0415

        summary = build_synthetic_e2e_summary(
            generated_at="2026-06-18T00:40:00+03:00",
            full_dry_run_payload={
                "status": "ok",
                "mode": "full_dry_run",
                "first_response": {
                    "schema_version": "first_run_guided_response_v1",
                    "blocking_question_count": 1,
                    "route_options": [{"id": "static_read_only_analysis"}],
                },
                "packet": {
                    "schema_version": "first_run_analysis_packet_v1",
                    "question_queue": {"summary": {"total": 3, "blocking": 1}},
                    "generated_view_policy": "orientation_only_not_proof",
                },
                "written_files": [],
                "actions_performed": {"target_workspace_mutation": False},
            },
            stage_payload={
                "status": "ok",
                "mode": "stage",
                "written_files": [
                    "first-run-analysis-packet.json",
                    "answer-ledger-template.json",
                    "index.html",
                    "analysis-manifest.json",
                ],
                "render_result": {"page_count": 11},
                "baseline_comparison": {"status": "missing"},
                "actions_performed": {"target_workspace_mutation": False},
            },
            target_snapshot_before={"fingerprint": "sha256:before", "file_count": 2},
            target_snapshot_after={"fingerprint": "sha256:before", "file_count": 2},
        )

        self.assertEqual(summary["schema_version"], "batch41_s6_synthetic_e2e_summary_v1")
        self.assertEqual(summary["status"], "passed_synthetic_e2e")
        self.assertEqual(summary["task_id"], "B41-S6-M24")
        self.assertEqual(summary["dry_run"]["mode"], "full_dry_run")
        self.assertEqual(summary["stage"]["html_page_count"], 11)
        self.assertTrue(summary["guided_question_output"]["one_blocking_question_max"])
        self.assertTrue(summary["answer_ledger_template_present"])
        self.assertFalse(summary["target_mutation"]["changed"])
        self.assertEqual(summary["completion_claim"], "not_claimed")

    def test_real_target_pilot_summary_redacts_path_and_preserves_mutation_boundary(self) -> None:
        from product_agent_os.batch41_s6_closure import build_real_target_pilot_summary  # noqa: PLC0415

        summary = build_real_target_pilot_summary(
            task_id="B41-S6-M25",
            target_label="Neural_Flow",
            target_kind="docs_research_expected_block",
            generated_at="2026-06-18T00:45:00+03:00",
            target_access_status="readable",
            full_dry_run_payload={
                "status": "ok",
                "mode": "full_dry_run",
                "first_response": {"blocking_question_count": 1, "route_options": [{"id": "fix_source_policy"}]},
                "packet": {
                    "source_policy_summary": {"status": "blocked"},
                    "methodology_audit_summary": {"status": "current"},
                    "runtime_browser_boundary": {"status": "not_available"},
                    "generated_view_policy": "orientation_only_not_proof",
                },
                "actions_performed": {"target_workspace_mutation": False},
            },
            stage_payload={"status": "ok", "mode": "stage", "render_result": {"page_count": 11}},
            target_snapshot_before={"fingerprint": "sha256:same", "file_count": 12},
            target_snapshot_after={"fingerprint": "sha256:same", "file_count": 12},
        )
        encoded = json.dumps(summary, sort_keys=True)

        self.assertEqual(summary["schema_version"], "batch41_s6_real_target_pilot_summary_v1")
        self.assertEqual(summary["status"], "passed_read_only_expected_block")
        self.assertEqual(summary["source_policy_status"], "blocked")
        self.assertEqual(summary["html_artifact_status"], "rendered_orientation_only")
        self.assertFalse(summary["target_mutation"]["changed"])
        self.assertNotIn("C:\\Users\\user", encoded)
        self.assertEqual(summary["unsupported_claims"][0], "real-target pilot is read-only orientation evidence only")

    def test_closure_packet_keeps_release_no_go_when_plugin_cache_is_not_ready(self) -> None:
        from product_agent_os.batch41_s6_closure import (
            build_batch41_s6_closure_packet,
            build_plugin_cache_readiness,
            build_usefulness_scorecard,
        )  # noqa: PLC0415

        synthetic = {"status": "passed_synthetic_e2e", "task_id": "B41-S6-M24"}
        pilots = [
            {"task_id": "B41-S6-M25", "status": "passed_read_only_expected_block", "target_label": "Neural_Flow"},
            {"task_id": "B41-S6-M26", "status": "passed_read_only_static_boundary", "target_label": "SOL 0.6"},
        ]
        scorecard = build_usefulness_scorecard(
            generated_at="2026-06-18T00:50:00+03:00",
            synthetic_e2e_summary=synthetic,
            real_target_pilots=pilots,
        )
        plugin_cache = build_plugin_cache_readiness(
            generated_at="2026-06-18T00:55:00+03:00",
            source_markers={"first_run_guided_response": True, "answer_ledger_template": True},
            cache_markers={"first_run_guided_response": False, "answer_ledger_template": False},
        )
        packet = build_batch41_s6_closure_packet(
            generated_at="2026-06-18T01:00:00+03:00",
            synthetic_e2e_summary=synthetic,
            real_target_pilots=pilots,
            usefulness_scorecard=scorecard,
            verification_evidence={"full_unittest": "1005 OK / 1 skipped"},
            plugin_cache_readiness=plugin_cache,
        )

        self.assertEqual(packet["schema_version"], "batch41_s6_closure_packet_v1")
        self.assertEqual(packet["attempt_id"], "B41-S6-CLOSURE-A01")
        self.assertEqual(set(packet["covered_tasks"]), {f"B41-S6-M{index}" for index in range(24, 31)})
        self.assertEqual(packet["tasks"]["B41-S6-M24"]["status"], "implemented")
        self.assertEqual(packet["tasks"]["B41-S6-M29"]["status"], "blocked_expected_approval_required")
        self.assertEqual(packet["go_no_go"]["release"], "no_go")
        self.assertEqual(packet["go_no_go"]["owner_feedback_testing"], "conditional_go")
        self.assertEqual(packet["go_no_go"]["plugin_cache_readiness"], "approval_required")
        self.assertFalse(packet["actions_performed"]["release_deploy_publish"])
        self.assertIn("release readiness is not claimed", " ".join(packet["unsupported_claims"]))

    def test_s6_runner_writes_closure_artifacts_without_target_arguments(self) -> None:
        output_dir = ROOT / "docs" / "superpowers" / "specs"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "run_batch41_s6_closure.py"),
                "--generated-at",
                "2026-06-18T01:10:00+03:00",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "closed_conditional_go_not_release_ready")
        self.assertTrue((output_dir / "batch41-s6-closure-summary.json").exists())
        self.assertTrue((output_dir / "batch41-s6-synthetic-e2e-summary.json").exists())
        self.assertTrue((output_dir / "batch41-s6-real-target-pilots-summary.json").exists())
        self.assertTrue((output_dir / "batch41-s6-usefulness-scorecard.json").exists())
        self.assertTrue((output_dir / "batch41-s6-go-no-go-decision-packet.json").exists())
        self.assertTrue((output_dir / "batch41-s6-no-unapproved-actions-proof.json").exists())
        self.assertTrue((output_dir / "batch41-s6-plugin-cache-readiness.json").exists())


if __name__ == "__main__":
    unittest.main()
