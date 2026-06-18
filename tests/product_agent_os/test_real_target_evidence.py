import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


class RealTargetEvidenceContractTest(unittest.TestCase):
    def test_nested_detector_and_first_run_outputs_normalize_to_flat_route_fields(self):
        from product_agent_os.real_target_evidence import normalize_real_target_evidence

        summary = normalize_real_target_evidence(
            target_label="SOL 0.6",
            detect_project_output={
                "usage_mode": {
                    "primary": "desktop_local_first",
                    "confidence": "high",
                    "reasons": ["workspace has desktop or local-first runtime signals"],
                },
                "detected_stack": ["node"],
                "existing_control_plane": ["PLAN.md"],
                "missing_control_plane": ["AGENTS.md"],
                "risks": ["missing durable project instructions"],
            },
            first_run_dry_run_output={
                "status": "ok",
                "mode": "dry_run",
                "packet": {
                    "schema_version": "first_run_analysis_packet_v1",
                    "packet_digest": "sha256:" + "0" * 64,
                    "generated_view_policy": "orientation_only_not_proof",
                    "write_policy": "read_only_generated_analysis_only",
                    "generated_pages": [{"page_id": "overview"}, {"page_id": "graph"}],
                    "safe_next_action": "Review first-run packet.",
                },
                "written_files": [],
            },
        )

        self.assertEqual(summary["schema_version"], "real_target_evidence_summary_v1")
        self.assertEqual(summary["detect_project_summary"]["usage_mode_primary"], "desktop_local_first")
        self.assertEqual(summary["detect_project_summary"]["usage_mode_confidence"], "high")
        self.assertEqual(summary["first_run_dry_run_summary"]["status"], "ok")
        self.assertEqual(summary["first_run_dry_run_summary"]["mode"], "dry_run")
        self.assertEqual(summary["first_run_dry_run_summary"]["schema_version"], "first_run_analysis_packet_v1")
        self.assertEqual(summary["first_run_dry_run_summary"]["first_run_page_count"], 2)
        self.assertEqual(summary["first_run_dry_run_summary"]["generated_view_policy"], "orientation_only_not_proof")
        self.assertEqual(summary["first_run_dry_run_summary"]["written_file_count"], 0)
        self.assertIsNotNone(summary["summary_digest"])

    def test_runtime_route_packet_and_graph_validation_are_normalized(self):
        from product_agent_os.real_target_evidence import normalize_real_target_evidence

        summary = normalize_real_target_evidence(
            target_label="Neural Flow",
            runtime_contract_output={
                "status": "blocked",
                "route_packet": {
                    "usage_mode": {
                        "primary": "ai_eval_regression",
                        "reasons": ["workspace has AI or RAG eval regression signals"],
                    }
                },
                "source_policy_status": "blocked",
                "errors": ["source_policy:blocked"],
            },
            project_graph_output={
                "validation": {"ok": True, "errors": []},
                "nodes": [{"id": "file:README.md"}],
                "edges": [],
                "observations": [],
                "metadata": {
                    "scope_policy": {
                        "status": "excluded_prefixes_reported",
                        "excluded_prefixes": ["antigravity-awesome-skills-main"],
                    }
                },
            },
        )

        self.assertEqual(summary["runtime_contract_summary"]["usage_mode_primary"], "ai_eval_regression")
        self.assertEqual(summary["runtime_contract_summary"]["source_policy_status"], "blocked")
        self.assertEqual(summary["project_graph_summary"]["status"], "ok")
        self.assertTrue(summary["project_graph_summary"]["validation_ok"])
        self.assertEqual(summary["project_graph_summary"]["excluded_prefixes"], ["antigravity-awesome-skills-main"])


if __name__ == "__main__":
    unittest.main()
