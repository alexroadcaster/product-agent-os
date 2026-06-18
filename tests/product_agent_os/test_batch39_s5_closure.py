from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


class Batch39S5ClosureTests(unittest.TestCase):
    def test_s5_closure_packet_closes_m34_m36_without_release_claim(self) -> None:
        from product_agent_os.batch39_s5_closure import build_b39_s5_closure_packet  # noqa: PLC0415

        packet = build_b39_s5_closure_packet(
            generated_at="2026-06-18T22:30:00+03:00",
            s4_closure_matrix={
                "closure_status": "not_release_ready_expected_blocks_recorded",
                "blocked_expected_tasks": ["B39-TEST-M37", "B39-TEST-M42"],
                "approval_required_tasks": ["B39-TEST-M46", "B39-TEST-M54"],
                "task_counts": {"total": 16, "partial": 11, "blocked_expected": 2, "approval_required": 2},
            },
            verification_evidence={
                "full_unittest": "983 OK / 1 skipped",
                "fixture_eval": "ok",
                "transcript_eval": "26/26",
                "codex_compatibility": "compatible",
                "docs_check": "ok",
                "diff_check": "ok",
            },
        )

        self.assertEqual(packet["schema_version"], "batch39_s5_closure_packet_v1")
        self.assertEqual(packet["attempt_id"], "B39-S5-CLOSURE-A01")
        self.assertEqual(packet["slice"], "B39-S5")
        self.assertEqual(packet["slice_status"], "closed_for_owner_feedback_testing_not_release_ready")
        self.assertEqual(set(packet["covered_tasks"]), {"B39-TEST-M34", "B39-TEST-M35", "B39-TEST-M36"})
        self.assertEqual(packet["tasks"]["B39-TEST-M34"]["status"], "passed_source_docs_sync")
        self.assertEqual(packet["tasks"]["B39-TEST-M35"]["decision"], "conditional_go_owner_feedback_testing")
        self.assertFalse(packet["tasks"]["B39-TEST-M35"]["release_go"])
        self.assertTrue(packet["tasks"]["B39-TEST-M35"]["owner_feedback_testing_go"])
        self.assertEqual(packet["tasks"]["B39-TEST-M36"]["status"], "passed_no_unapproved_actions_proof")
        self.assertFalse(packet["actions_performed"]["target_workspace_mutation"])
        self.assertFalse(packet["actions_performed"]["release_deploy_publish"])
        self.assertIn("release readiness is not claimed", " ".join(packet["unsupported_claims"]))

    def test_s5_owner_feedback_plan_is_manual_and_evidence_bound(self) -> None:
        from product_agent_os.batch39_s5_closure import build_owner_feedback_test_plan  # noqa: PLC0415

        plan = build_owner_feedback_test_plan()

        self.assertEqual(plan["schema_version"], "batch39_s5_owner_feedback_test_plan_v1")
        self.assertEqual(plan["status"], "ready_for_manual_owner_feedback_testing")
        self.assertEqual(plan["promotion_status"], "manual_only_not_promoted")
        self.assertGreaterEqual(len(plan["scenarios"]), 5)
        for scenario in plan["scenarios"]:
            with self.subTest(scenario=scenario["id"]):
                self.assertTrue(scenario["question_for_owner"])
                self.assertTrue(scenario["evidence_to_collect"])
                self.assertEqual(scenario["external_action_required"], False)
        self.assertIn("runtime/browser pilot", " ".join(plan["approval_required_followups"]))

    def test_s5_packet_is_json_safe_and_preserves_no_action_boundaries(self) -> None:
        from product_agent_os.batch39_s5_closure import build_b39_s5_closure_packet  # noqa: PLC0415

        packet = build_b39_s5_closure_packet(
            generated_at="2026-06-18T22:30:00+03:00",
            s4_closure_matrix={},
            verification_evidence={},
        )
        encoded = json.dumps(packet, ensure_ascii=False, sort_keys=True)

        self.assertNotIn("C:\\Users\\user", encoded)
        self.assertNotIn("sk-", encoded)
        for name, value in packet["actions_performed"].items():
            with self.subTest(action=name):
                self.assertFalse(value)
        self.assertEqual(packet["go_no_go"]["release"], "no_go")
        self.assertEqual(packet["go_no_go"]["owner_feedback_testing"], "conditional_go")

    def test_s5_runner_writes_expected_artifacts(self) -> None:
        output_dir = ROOT / "docs" / "superpowers" / "specs"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "run_batch39_s5_closure.py"), "--generated-at", "2026-06-18T22:30:00+03:00"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "closed_for_owner_feedback_testing_not_release_ready")
        self.assertTrue((output_dir / "batch39-s5-closure-summary.json").exists())
        self.assertTrue((output_dir / "batch39-s5-go-no-go-decision-packet.json").exists())
        self.assertTrue((output_dir / "batch39-s5-no-unapproved-actions-proof.json").exists())
        self.assertTrue((output_dir / "batch39-s5-owner-feedback-test-plan.json").exists())


if __name__ == "__main__":
    unittest.main()
