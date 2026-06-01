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

    def test_snapshot_includes_bounded_metrics_loop_summary_and_report_refs(self):
        runtime_result = {
            "status": "route_ready",
            "workspace": "C:\\Users\\person\\metrics-loop",
            "lifecycle_state": "quality_gate",
            "route_packet": {
                "usage_mode": {"primary": "maintenance", "confidence": "medium"},
                "agent_skill_metrics_loop": {
                    "status": "present_unverified",
                    "summary": {
                        "target_count": 12,
                        "overall_status": "blocked_by_guardrail",
                        "cadence_level": "L2",
                    },
                    "report_refs": [
                        {
                            "kind": "staged_artifact",
                            "path": ".codex/eval-reports/agent-skill-evaluation-report.html",
                            "digest": "sha256:" + "a" * 64,
                        },
                        {
                            "kind": "external_ref",
                            "path": "https://example.invalid/report.html",
                        },
                    ],
                    "update_candidate_summary": {
                        "candidate_count": 9,
                        "top_candidates": [
                            {"candidate_id": f"candidate-{index}", "requires_rollback": True}
                            for index in range(8)
                        ],
                    },
                    "unsafe_extra": "TOKEN=fixture-secret C:\\Users\\person\\metrics-loop",
                },
            },
            "verification_evidence": [],
        }

        snapshot = build_status_snapshot(
            runtime_result=runtime_result,
            generated_at="2026-05-28T10:00:00+00:00",
        )
        serialized = json.dumps(snapshot, sort_keys=True)

        summary = snapshot["agent_skill_metrics_loop"]
        self.assertEqual(summary["status"], "present_unverified")
        self.assertEqual(summary["summary"]["target_count"], 12)
        self.assertEqual(summary["summary"]["cadence_level"], "L2")
        self.assertEqual(summary["report_refs"][0]["path"], ".codex/eval-reports/agent-skill-evaluation-report.html")
        self.assertEqual(len(summary["report_refs"]), 1)
        self.assertEqual(len(summary["update_candidate_summary"]["top_candidates"]), 5)
        self.assertEqual(summary["source_policy"], "generated summaries are not source of truth")
        self.assertNotIn("fixture-secret", serialized)
        self.assertNotIn("C:\\Users\\person", serialized)
        self.assertNotIn("https://example.invalid", serialized)

    def test_snapshot_includes_bounded_project_graph_summary_and_never_claims_graph_as_truth(self):
        runtime_result = {
            "status": "route_ready",
            "workspace": "C:\\Users\\person\\graph-project",
            "lifecycle_state": "quality_gate",
            "route_packet": {
                "usage_mode": {"primary": "maintenance", "confidence": "medium"},
                "project_graph_status": {
                    "schema_version": 1,
                    "write_policy": "read_only",
                    "status": "stale",
                    "freshness": {"status": "stale", "scan_id": "scan-old", "as_of": "2026-05-01T00:00:00+00:00"},
                    "counts": {"nodes": 1000, "edges": 2000, "observations": 3000, "omitted_nodes": 750},
                    "unsupported_languages": [
                        {
                            "language": "typescript",
                            "file_count": 20,
                            "status": "file_only",
                            "raw_source": "def charge_card(): pass",
                        }
                    ],
                    "artifact_refs": [
                        {
                            "kind": "staged_artifact",
                            "path": ".codex/product-agent-os/project-code-graph.json",
                            "digest": "sha256:" + "a" * 64,
                        },
                        {"kind": "external_ref", "path": "https://example.invalid/graph.json"},
                        {"kind": "staged_artifact", "path": "D:/private/project/graph.json"},
                    ],
                    "top_gaps": [
                        {
                            "id": f"gap-{index}",
                            "severity": "medium",
                            "safe_next_action": "Read source files before acting.",
                        }
                        for index in range(10)
                    ],
                    "safe_next_action": "Use graph as orientation only; read source files before edits.",
                    "source_policy": "generated graph is not source of truth",
                    "nodes": [{"id": "file:C:\\Users\\person\\graph-project\\app.py"}],
                    "edges": [{"source": "a", "target": "b"}],
                },
            },
            "verification_evidence": [],
        }

        snapshot = build_status_snapshot(
            runtime_result=runtime_result,
            generated_at="2026-06-01T00:00:00+00:00",
        )
        serialized = json.dumps(snapshot, sort_keys=True)
        graph_summary = snapshot["project_graph_summary"]

        self.assertEqual(graph_summary["status"], "stale")
        self.assertEqual(graph_summary["counts"]["nodes"], 1000)
        self.assertEqual(graph_summary["unsupported_languages"][0]["language"], "typescript")
        self.assertNotIn("raw_source", graph_summary["unsupported_languages"][0])
        self.assertEqual(len(graph_summary["artifact_refs"]), 1)
        self.assertEqual(len(graph_summary["top_gaps"]), 5)
        self.assertEqual(graph_summary["source_policy"], "generated graph is not source of truth")
        self.assertIn("stale project graph", snapshot["readiness_summary"]["warnings"])
        self.assertNotIn("nodes", graph_summary)
        self.assertNotIn("edges", graph_summary)
        self.assertNotIn("https://example.invalid", serialized)
        self.assertNotIn("D:/private", serialized)
        self.assertNotIn("charge_card", serialized)
        self.assertNotIn("C:\\Users\\person", serialized)
        self.assertNotIn("graph-project", serialized)

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
