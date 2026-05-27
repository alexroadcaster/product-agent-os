import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.status_snapshot import build_status_snapshot  # noqa: E402


class StatusSnapshotTest(unittest.TestCase):
    def test_status_snapshot_summarizes_runtime_renderer_manifest_and_ledgers_without_raw_paths(self):
        runtime_result = {
            "status": "needs_approval",
            "workspace": "C:\\Users\\person\\private-project",
            "lifecycle_state": "quality_gate",
            "route_packet": {
                "write_policy": "read_only",
                "usage_mode": {"primary": "security_sensitive_change", "confidence": "high"},
                "question_queue": {
                    "summary": {"total": 3, "blocking": 1, "recommended": 2, "optional": 0, "remaining": 2},
                    "next_blocking_question": {
                        "id": "q_approval_synthetic",
                        "text": "Who approves the external write?",
                        "priority": "blocking",
                    },
                },
                "first_response_contract": {
                    "safe_next_action": "Stage approval-record.md before external mutation.",
                    "next_blocking_question": {"id": "q_approval_synthetic"},
                    "question_counts": {"total": 3, "blocking": 1, "recommended": 2, "optional": 0, "remaining": 2},
                    "question_summary": ["1 blocking question", "2 recommended questions", "0 optional questions"],
                },
                "methodology_packet": self._methodology_packet(),
            },
            "approval_status": "required",
            "verification_evidence": [],
            "redactions": {"count": 0, "categories": []},
        }
        renderer_result = {
            "infrastructure_plan": {"status": "needs_approval"},
            "rendered_artifacts": {
                "mode": "stage",
                "files": [
                    {
                        "target_path": "AGENTS.md",
                        "staged_path": "C:\\Users\\person\\stage\\AGENTS.md",
                        "action": "create",
                    },
                    {
                        "target_path": ".codex/artifact-templates/question-ledger.md",
                        "staged_path": "C:\\Users\\person\\stage\\.codex\\artifact-templates\\question-ledger.md",
                        "action": "create",
                    },
                ],
                "validation": {"ok": True, "errors": {}},
            },
        }
        stage_manifest = {
            "workspace": "C:\\Users\\person\\private-project",
            "workspace_audit_digest": "sha256:" + "a" * 64,
            "infrastructure_plan_digest": "sha256:" + "b" * 64,
            "files": [
                {
                    "target_path": "AGENTS.md",
                    "staged_path": "C:\\Users\\person\\stage\\AGENTS.md",
                    "digest": "sha256:" + "c" * 64,
                }
            ],
        }
        question_ledger = {
            "summary": {"accepted": 1, "blocked": 0, "unanswered": 2, "total": 3},
            "artifact_updates": [{"artifact": "approval-record.md", "question_ids": ["q_approval_synthetic"]}],
        }

        snapshot = build_status_snapshot(
            runtime_result=runtime_result,
            renderer_result=renderer_result,
            stage_manifest=stage_manifest,
            question_ledger=question_ledger,
            generated_at="2026-05-28T10:00:00+00:00",
        )
        serialized = json.dumps(snapshot, sort_keys=True)

        self.assertEqual(snapshot["schema_version"], 1)
        self.assertEqual(snapshot["write_policy"], "read_only")
        self.assertEqual(snapshot["generated_at"], "2026-05-28T10:00:00+00:00")
        self.assertEqual(snapshot["workspace"], "[REDACTED_LOCAL_PATH]")
        self.assertEqual(snapshot["lifecycle_state"], "quality_gate")
        self.assertEqual(snapshot["usage_mode"]["primary"], "security_sensitive_change")
        self.assertEqual(snapshot["question_summary"]["blocking"], 1)
        self.assertEqual(snapshot["readiness_summary"]["status"], "needs_approval")
        self.assertEqual(snapshot["evidence_summary"]["freshness"], "missing")
        self.assertEqual(snapshot["next_safe_action"], "Stage approval-record.md before external mutation.")
        self.assertEqual(snapshot["dashboard_policy"]["source_of_truth"], "underlying_artifacts")
        self.assertEqual(snapshot["dashboard_policy"]["write_policy"], "read_only")
        self.assertEqual(snapshot["renderer_file_count"], 2)
        self.assertEqual(
            snapshot["manifest_digests"]["workspace_audit_digest"],
            "sha256:" + "a" * 64,
        )
        self.assertEqual(snapshot["manifest_digests"]["file_count"], 1)
        self.assertEqual(
            snapshot["source_artifact_ledger"],
            [{"artifact": "approval-record.md", "decision": "canonical_template"}],
        )
        self.assertEqual(
            snapshot["semantic_evidence_sufficiency"]["status"],
            "present_unverified",
        )
        self.assertEqual(snapshot["question_ledger_summary"]["accepted"], 1)
        self.assertIn("absolute_path", snapshot["redaction_summary"]["categories"])
        self.assertNotIn("C:\\Users\\person", serialized)
        self.assertNotIn("private-project", serialized)
        self.assertNotIn("staged_path", serialized)

    def test_snapshot_marks_inspection_only_and_stale_evidence_without_success_claims(self):
        runtime_result = {
            "status": "completed",
            "workspace": "C:\\Users\\person\\inspection-only",
            "lifecycle_state": "maintenance",
            "route_packet": {
                "usage_mode": {"primary": "inspection_only", "confidence": "high"},
                "question_queue": {
                    "summary": {"total": 0, "blocking": 0, "recommended": 0, "optional": 0, "remaining": 0},
                    "next_blocking_question": None,
                },
                "first_response_contract": {
                    "safe_next_action": "Record read-only audit findings.",
                    "question_counts": {"total": 0, "blocking": 0, "recommended": 0, "optional": 0, "remaining": 0},
                    "question_summary": ["0 blocking questions", "0 recommended questions", "0 optional questions"],
                },
                "methodology_packet": self._methodology_packet(status="present_unverified"),
            },
            "verification_evidence": [
                {"command": "python -m unittest", "status": "ok", "recorded_at": "2026-04-01T00:00:00+00:00"}
            ],
            "approval_status": "not_required",
        }

        snapshot = build_status_snapshot(
            runtime_result=runtime_result,
            generated_at="2026-05-28T10:00:00+00:00",
            evidence_max_age_days=14,
        )
        serialized = json.dumps(snapshot, sort_keys=True).lower()

        self.assertEqual(snapshot["usage_mode"]["primary"], "inspection_only")
        self.assertTrue(snapshot["usage_mode"]["inspection_only"])
        self.assertEqual(snapshot["evidence_summary"]["freshness"], "stale")
        self.assertEqual(snapshot["readiness_summary"]["success_claim"], "not_claimed")
        self.assertEqual(snapshot["readiness_summary"]["status"], "inspection_only")
        self.assertIn("stale evidence", snapshot["readiness_summary"]["warnings"])
        self.assertIn("inspection-only evidence cannot prove completion", snapshot["readiness_summary"]["warnings"])
        self.assertNotIn("tests pass", serialized)
        self.assertNotIn("checks passed", serialized)
        self.assertNotIn("success", snapshot["readiness_summary"]["status"])

    def test_snapshot_redacts_secret_and_private_data_from_nested_packets(self):
        runtime_result = {
            "status": "route_ready",
            "workspace": "C:\\Users\\person\\project",
            "lifecycle_state": "quality_gate",
            "route_packet": {
                "usage_mode": {"primary": "standard_feature", "confidence": "medium"},
                "question_queue": {
                    "summary": {"total": 1, "blocking": 1, "recommended": 0, "optional": 0, "remaining": 0},
                    "next_blocking_question": {"id": "q_secret", "text": "TOKEN=fixture-secret"},
                },
                "first_response_contract": {
                    "safe_next_action": "Inspect C:\\Users\\person\\project and raw private chat log.",
                    "question_counts": {"total": 1, "blocking": 1, "recommended": 0, "optional": 0, "remaining": 0},
                    "question_summary": ["1 blocking question"],
                },
            },
            "verification_evidence": ["TOKEN=fixture-secret"],
        }

        snapshot = build_status_snapshot(
            runtime_result=runtime_result,
            generated_at="2026-05-28T10:00:00+00:00",
        )
        serialized = json.dumps(snapshot, sort_keys=True)

        self.assertNotIn("fixture-secret", serialized)
        self.assertNotIn("raw private chat log", serialized)
        self.assertNotIn("C:\\Users\\person", serialized)
        self.assertIn("secret", snapshot["redaction_summary"]["categories"])
        self.assertIn("private_data", snapshot["redaction_summary"]["categories"])
        self.assertIn("absolute_path", snapshot["redaction_summary"]["categories"])

    def _methodology_packet(self, *, status="present_unverified"):
        return {
            "safe_next_action": "Stage approval-record.md before external mutation.",
            "status": status,
            "semantic_evidence_sufficiency": {
                "status": "present_unverified",
                "required_evidence": ["owner-reviewed evidence"],
            },
            "source_artifact_ledger": [
                {"artifact": "approval-record.md", "decision": "canonical_template"}
            ],
        }


if __name__ == "__main__":
    unittest.main()
