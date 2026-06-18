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

    def test_project_graph_depth_signals_are_preserved_for_real_target_retest(self):
        from product_agent_os.real_target_evidence import normalize_real_target_evidence

        summary = normalize_real_target_evidence(
            target_label="SOL 0.6",
            first_run_dry_run_output={
                "status": "ok",
                "mode": "dry_run",
                "packet": {
                    "graph_depth_summary": {
                        "schema_version": "graph_depth_first_run_summary_v1",
                        "status": "current",
                        "coverage": {"status": "diagnostic_only"},
                        "freshness": {"status": "current", "blocks_action_claims": False},
                        "rejected_link_summary": {"total": 3, "by_reason": {"weak_name_similarity": 3}},
                        "framework_semantic_summary": {"total": 2, "frameworks": {"react": 2}},
                    },
                    "generated_pages": [],
                },
                "written_files": [],
            },
            project_graph_output={
                "validation": {"ok": True, "errors": []},
                "node_count": 12,
                "edge_count": 8,
                "observation_count": 20,
                "metadata": {
                    "coverage_map": {
                        "status": "diagnostic_only",
                        "supported_file_count": 5,
                        "partial_file_count": 2,
                        "unsupported_file_count": 1,
                        "unsupported_languages": {"css": 1},
                        "skipped_reasons": {"excluded_prefix": 1},
                        "recommended_next_parser_or_linker_action": "Add CSS selector overlay only after target need.",
                    },
                    "temporal_delta": {
                        "status": "not_available",
                        "changed_edge_count": 0,
                        "removed_edge_count": 0,
                    },
                    "conservative_linker": {
                        "rejected_link_count": 3,
                    },
                    "rejected_links": [
                        {"reason": "weak_name_similarity"},
                        {"reason": "weak_name_similarity"},
                        {"reason": "ambiguous_target"},
                    ],
                    "typescript_javascript_scanner": {
                        "framework_semantics": {
                            "framework_count": 2,
                            "frameworks": {"react": 2, "nextjs": 1},
                        }
                    },
                    "scope_policy": {
                        "status": "excluded_prefixes_reported",
                        "excluded_prefixes": ["antigravity-awesome-skills-main"],
                    },
                },
            },
        )

        graph_summary = summary["project_graph_summary"]
        self.assertEqual(graph_summary["coverage"]["status"], "diagnostic_only")
        self.assertEqual(graph_summary["coverage"]["unsupported_languages"], {"css": "1"})
        self.assertEqual(graph_summary["freshness"]["status"], "not_available")
        self.assertTrue(graph_summary["freshness"]["blocks_action_claims"])
        self.assertEqual(graph_summary["rejected_link_summary"]["total"], 3)
        self.assertEqual(graph_summary["rejected_link_summary"]["by_reason"]["weak_name_similarity"], 2)
        self.assertEqual(graph_summary["framework_semantic_summary"]["frameworks"]["react"], 2)
        self.assertEqual(
            summary["first_run_dry_run_summary"]["graph_depth_summary"]["rejected_link_summary"]["total"],
            3,
        )
        self.assertEqual(summary["first_run_dry_run_summary"]["written_file_count"], 0)


if __name__ == "__main__":
    unittest.main()
