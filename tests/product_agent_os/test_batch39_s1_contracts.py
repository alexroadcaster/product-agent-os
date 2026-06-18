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


from product_agent_os.batch39_failure_taxonomy import (  # noqa: E402
    REQUIRED_FAILURE_CLASSES,
    build_failure_taxonomy,
    validate_failure_taxonomy,
)
from product_agent_os.batch39_redaction import (  # noqa: E402
    build_redaction_report,
    validate_redaction_report,
)
from product_agent_os.batch39_rollup import (  # noqa: E402
    build_batch39_rollup,
    validate_batch39_rollup,
)
from product_agent_os.batch39_scorecard import (  # noqa: E402
    build_graph_usefulness_scorecard,
    build_scorecard_gates,
    validate_graph_usefulness_scorecard,
    validate_scorecard_gates,
)
from product_agent_os.batch39_session_visibility import (  # noqa: E402
    build_session_visibility_report,
    validate_session_visibility_report,
)
from product_agent_os.status_dashboard import render_status_dashboard  # noqa: E402
from product_agent_os.status_snapshot import build_status_snapshot  # noqa: E402


class Batch39S1ContractsTests(unittest.TestCase):
    def test_m05_redaction_report_scrubs_paths_secrets_private_logs_and_raw_bodies(self) -> None:
        report = build_redaction_report(
            test_id="B39-TEST-M05",
            attempt_id="B39-TEST-M05-A01",
            artifact_refs=[
                "docs/superpowers/specs/doubt-verification-packet.example.json",
                "C:\\Users\\person\\private\\raw.log",
            ],
            sample_payload={
                "doubt_verification_packet": {
                    "path": "C:\\Users\\person\\project\\RUNLOG.md",
                    "token": "OPENAI_API_KEY=sk-test-secret",
                    "raw_private_log": "raw private chat log",
                    "raw_body": "must not be retained",
                },
                "safe": "relative/ref.md",
            },
            generated_at="2026-06-11T00:00:00+00:00",
        )

        encoded = json.dumps(report, ensure_ascii=False, sort_keys=True)

        self.assertEqual(report["schema_version"], "redaction_report_v1")
        self.assertEqual(report["verdict"], "passed_redacted_local_paths")
        self.assertIn("absolute_path", report["redaction_summary"]["categories"])
        self.assertIn("secret", report["redaction_summary"]["categories"])
        self.assertIn("private_data", report["redaction_summary"]["categories"])
        self.assertFalse(report["policy"]["raw_file_bodies_stored"])
        self.assertFalse(report["policy"]["raw_private_logs_stored"])
        self.assertNotIn("C:\\Users\\person", encoded)
        self.assertNotIn("sk-test-secret", encoded)
        self.assertNotIn("raw private chat log", encoded)
        self.assertNotIn("raw_body", encoded)
        self.assertEqual(validate_redaction_report(report), [])

    def test_m05_cli_writes_redaction_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "redaction-report.example.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "create_redaction_report.py"),
                    "--output",
                    str(output),
                    "--test-id",
                    "B39-TEST-M05",
                    "--attempt-id",
                    "B39-TEST-M05-A01",
                    "--artifact-ref",
                    "docs/superpowers/specs/doubt-verification-packet.example.json",
                    "--sample-json",
                    json.dumps({"path": "C:\\Users\\person\\project", "secret": "TOKEN=fixture-secret"}),
                    "--generated-at",
                    "2026-06-11T00:00:00+00:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(validate_redaction_report(payload), [])
            self.assertIn('"status": "ok"', result.stdout)

    def test_m06_session_visibility_requires_install_update_uninstall_and_visible_session(self) -> None:
        report = build_session_visibility_report(
            test_id="B39-TEST-M06",
            attempt_id="B39-TEST-M06-A01",
            generated_at="2026-06-11T00:00:00+00:00",
            package_ref="product-agent-os@0.1.0",
            events=[
                {"operation": "install", "status": "observed", "artifact": "plugin-cache"},
                {"operation": "update", "status": "observed", "artifact": "plugin-cache"},
                {"operation": "session_visible", "status": "observed", "artifact": "Codex App skills list"},
                {"operation": "uninstall", "status": "observed", "artifact": "staged removal check"},
            ],
        )

        self.assertEqual(report["schema_version"], "session_visibility_report_v1")
        self.assertEqual(report["verdict"], "session_visibility_verified")
        self.assertEqual(report["coverage"]["install"], "observed")
        self.assertEqual(report["coverage"]["update"], "observed")
        self.assertEqual(report["coverage"]["uninstall"], "observed")
        self.assertEqual(report["coverage"]["session_visible"], "observed")
        self.assertEqual(report["approval_boundary"]["cache_mutation"], "not_performed")
        self.assertEqual(validate_session_visibility_report(report), [])

        missing = build_session_visibility_report(
            test_id="B39-TEST-M06",
            attempt_id="B39-TEST-M06-A01",
            package_ref="product-agent-os@0.1.0",
            events=[{"operation": "install", "status": "observed", "artifact": "plugin-cache"}],
        )
        self.assertIn("missing required operation: update", validate_session_visibility_report(missing))
        self.assertEqual(missing["verdict"], "session_visibility_incomplete")

    def test_m07_rollup_aggregates_attempts_without_treating_generated_view_as_proof(self) -> None:
        rollup = build_batch39_rollup(
            test_id="B39-TEST-M07",
            attempt_id="B39-TEST-M07-A01",
            generated_at="2026-06-11T00:00:00+00:00",
            task_rows=[
                {"test_id": "B39-TEST-M05", "status": "passed", "attempts": 1, "evidence_refs": ["redaction-report"]},
                {"test_id": "B39-TEST-M06", "status": "passed", "attempts": 1, "evidence_refs": ["session-report"]},
                {"test_id": "B39-TEST-M10", "status": "planned", "attempts": 0, "evidence_refs": []},
            ],
        )

        self.assertEqual(rollup["schema_version"], "batch39_rollup_v1")
        self.assertEqual(rollup["counts"]["passed"], 2)
        self.assertEqual(rollup["counts"]["planned"], 1)
        self.assertEqual(rollup["safe_next_action"], "continue_pending_tests")
        self.assertEqual(rollup["generated_view_policy"], "orientation_only_not_proof")
        self.assertEqual(validate_batch39_rollup(rollup), [])

    def test_m08_dashboard_projects_pilot_evidence_rollup_as_generated_view_only(self) -> None:
        rollup = build_batch39_rollup(
            test_id="B39-TEST-M08",
            attempt_id="B39-TEST-M08-A01",
            generated_at="2026-06-11T00:00:00+00:00",
            task_rows=[
                {"test_id": "B39-TEST-M05", "status": "passed", "attempts": 1, "evidence_refs": ["redaction"]},
                {"test_id": "B39-TEST-M06", "status": "blocked", "attempts": 1, "evidence_refs": ["session"]},
            ],
        )
        snapshot = build_status_snapshot(
            runtime_result={
                "status": "route_ready",
                "workspace": "C:\\Users\\person\\pilot-dashboard",
                "route_packet": {"pilot_evidence_rollup": rollup},
            },
            generated_at="2026-06-11T00:00:00+00:00",
        )
        dashboard = render_status_dashboard(snapshot)
        rendered = dashboard["html"] + dashboard["json"]

        self.assertEqual(snapshot["pilot_evidence_rollup"]["source_policy"], "generated view is not proof")
        self.assertIn('id="section-pilot-evidence"', dashboard["html"])
        self.assertIn("Pilot Evidence", dashboard["html"])
        self.assertIn("generated view is not proof", rendered)
        self.assertIn("blocked", rendered)
        self.assertNotIn("C:\\Users\\person", rendered)
        self.assertEqual(dashboard["validation"]["errors"], [])

    def test_m20_7_status_and_rollup_reference_first_run_analysis_without_proof_claims(self) -> None:
        analysis_ref = {
            "kind": "generated_analysis_pack",
            "path": ".codex/product-agent-os/analysis/analysis-manifest.json",
            "digest": "sha256:" + "5" * 64,
            "page_count": 11,
            "freshness": "current",
            "unsupported_claim_count": 3,
        }
        rollup = build_batch39_rollup(
            test_id="B39-TEST-M20",
            attempt_id="B39-FRIA-M20.7-A01",
            generated_at="2026-06-18T18:00:00+00:00",
            task_rows=[
                {
                    "test_id": "B39-TEST-M20",
                    "status": "in_progress",
                    "attempts": 7,
                    "evidence_refs": ["prod_test.md"],
                    "first_run_analysis_ref": analysis_ref,
                }
            ],
        )
        snapshot = build_status_snapshot(
            runtime_result={
                "status": "route_ready",
                "workspace": "C:\\Users\\person\\first-run-rollup",
                "route_packet": {
                    "pilot_evidence_rollup": rollup,
                    "first_run_analysis_ref": analysis_ref,
                },
            },
            generated_at="2026-06-18T18:00:00+00:00",
        )
        dashboard = render_status_dashboard(snapshot)
        rendered = dashboard["html"] + dashboard["json"]

        self.assertEqual(rollup["task_rows"][0]["first_run_analysis_ref"]["path"], analysis_ref["path"])
        self.assertEqual(snapshot["first_run_analysis"]["manifest_digest"], analysis_ref["digest"])
        self.assertEqual(snapshot["first_run_analysis"]["page_count"], 11)
        self.assertEqual(snapshot["first_run_analysis"]["freshness"], "current")
        self.assertEqual(snapshot["first_run_analysis"]["unsupported_claim_count"], 3)
        self.assertEqual(snapshot["first_run_analysis"]["generated_view_policy"], "orientation_only_not_proof")
        self.assertIn("First Run Analysis", dashboard["html"])
        self.assertIn("orientation_only_not_proof", rendered)
        self.assertNotIn("C:\\Users\\person", rendered)
        self.assertEqual(dashboard["validation"]["errors"], [])

    def test_m09_failure_taxonomy_contains_required_completion_skeptic_classes(self) -> None:
        taxonomy = build_failure_taxonomy(
            test_id="B39-TEST-M09",
            attempt_id="B39-TEST-M09-A01",
            generated_at="2026-06-11T00:00:00+00:00",
        )

        self.assertEqual(taxonomy["schema_version"], "pilot_failure_taxonomy_v1")
        self.assertTrue(REQUIRED_FAILURE_CLASSES.issubset(set(taxonomy["classes"])))
        self.assertIn("generated_view_not_proof", taxonomy["classes"])
        self.assertEqual(validate_failure_taxonomy(taxonomy), [])

        taxonomy["classes"].remove("fake_evidence_rejected")
        self.assertIn("missing required failure class: fake_evidence_rejected", validate_failure_taxonomy(taxonomy))

    def test_m10_scorecard_blocks_synthetic_only_promotion_and_separates_gate_groups(self) -> None:
        scorecard = build_scorecard_gates(
            test_id="B39-TEST-M10",
            attempt_id="B39-TEST-M10-A01",
            generated_at="2026-06-11T00:00:00+00:00",
            gate_results=[
                {"gate": "pilot_current_evidence", "group": "pilot", "status": "passed"},
                {"gate": "product_usability_value", "group": "product_usability", "status": "passed"},
                {"gate": "real_project_evidence", "group": "promotion", "status": "blocked", "reason": "synthetic_only_boundary"},
            ],
        )

        self.assertEqual(scorecard["schema_version"], "pilot_product_usability_scorecard_v1")
        self.assertEqual(scorecard["promotion_decision"], "not_promoted")
        self.assertEqual(scorecard["groups"]["pilot"]["passed"], 1)
        self.assertEqual(scorecard["groups"]["product_usability"]["passed"], 1)
        self.assertEqual(scorecard["groups"]["promotion"]["blocked"], 1)
        self.assertIn("synthetic_only_boundary", scorecard["blocking_reasons"])
        self.assertEqual(validate_scorecard_gates(scorecard), [])

    def test_m20_8_first_run_artifact_scorecard_keeps_operator_review_and_synthetic_boundary(self) -> None:
        from product_agent_os.batch39_scorecard import (  # noqa: PLC0415
            build_first_run_artifact_scorecard,
            validate_first_run_artifact_scorecard,
        )

        scorecard = build_first_run_artifact_scorecard(
            test_id="B39-TEST-M20",
            attempt_id="B39-FRIA-M20.8-A01",
            generated_at="2026-06-18T19:00:00+00:00",
            artifact_summary={
                "page_count": 11,
                "source_artifact_count": 3,
                "unsupported_claim_count": 4,
                "manifest_digest": "sha256:" + "6" * 64,
                "freshness": "current",
                "redaction_status": "passed_redacted",
                "source_policy_status": "approval_required",
                "safe_next_action_present": True,
                "navigation_status": "complete",
            },
            owner_review_status="pending_owner_review",
        )

        self.assertEqual(scorecard["schema_version"], "first_run_artifact_scorecard_v1")
        self.assertEqual(scorecard["raw_counts"]["page_count"], 11)
        self.assertEqual(scorecard["raw_counts"]["unsupported_claim_count"], 4)
        self.assertEqual(scorecard["owner_review"]["status"], "pending_owner_review")
        self.assertEqual(scorecard["boundary_status"], "synthetic_only_boundary")
        self.assertEqual(scorecard["promotion_decision"], "not_promoted")
        self.assertEqual(scorecard["generated_view_policy"], "orientation_only_not_proof")
        self.assertIn("clarity", scorecard["scores"])
        self.assertIn("artifact_navigation", scorecard["scores"])
        self.assertGreaterEqual(scorecard["operator_usability_score"], 0.0)
        self.assertLessEqual(scorecard["operator_usability_score"], 1.0)
        self.assertEqual(validate_first_run_artifact_scorecard(scorecard), [])

    def test_graph_depth_scorecard_calibrates_fixture_usefulness_without_promotion_claim(self) -> None:
        scorecard = build_graph_usefulness_scorecard(
            test_id="B39-S4-GRAPH-DEPTH-06",
            attempt_id="B39-S4-GD-S6-SCORECARD-A01",
            generated_at="2026-06-18T20:30:00+00:00",
            metric_summary={
                "symbol_queries_total": 4,
                "symbol_queries_hit": 4,
                "top_k_hits": 3,
                "affected_tests_expected": 2,
                "affected_tests_matched": 2,
                "affected_tests_false_positive": 0,
                "baseline_read_files": 12,
                "packet_read_files": 4,
                "unsupported_language_count": 1,
                "language_count": 6,
                "stale_block_behavior": True,
                "safe_next_action_present": True,
                "real_target_comparison_present": False,
                "target_comparison_delta": None,
            },
        )

        self.assertEqual(scorecard["schema_version"], "graph_usefulness_scorecard_v1")
        self.assertEqual(scorecard["task_ids"], ["B39-S4-GRAPH-DEPTH-06", "B39-S4-GRAPH-DEPTH-14"])
        self.assertEqual(scorecard["fixture_evaluation_status"], "fixture_thresholds_passed")
        self.assertEqual(scorecard["promotion_decision"], "not_promoted")
        self.assertEqual(scorecard["promotion_boundary"], "manual_only_not_promoted")
        self.assertEqual(scorecard["target_comparison"]["status"], "missing")
        self.assertEqual(scorecard["generated_view_policy"], "orientation_only_not_proof")
        self.assertEqual(scorecard["source_boundary"], "graph_artifact_only_raw_source_excluded")
        self.assertEqual(scorecard["metrics"]["symbol_recall"], 1.0)
        self.assertEqual(scorecard["metrics"]["top_k_relevance"], 0.75)
        self.assertEqual(scorecard["metrics"]["affected_test_precision"], 1.0)
        self.assertEqual(scorecard["metrics"]["false_positive_rate"], 0.0)
        self.assertGreaterEqual(scorecard["metrics"]["reading_scope_reduction"], 0.6)
        self.assertLessEqual(scorecard["metrics"]["unsupported_language_rate"], 0.2)
        self.assertIn("real_target_comparison_missing", scorecard["blocking_reasons"])
        self.assertIn("release_readiness", scorecard["unsupported_claims"])
        self.assertEqual(validate_graph_usefulness_scorecard(scorecard), [])

    def test_graph_depth_scorecard_validation_blocks_overclaim_and_missing_metrics(self) -> None:
        scorecard = build_graph_usefulness_scorecard(
            test_id="B39-S4-GRAPH-DEPTH-14",
            attempt_id="B39-S4-GD-S6-SCORECARD-A01",
            metric_summary={
                "symbol_queries_total": 2,
                "symbol_queries_hit": 1,
                "top_k_hits": 1,
                "affected_tests_expected": 2,
                "affected_tests_matched": 1,
                "affected_tests_false_positive": 2,
                "baseline_read_files": 4,
                "packet_read_files": 4,
                "unsupported_language_count": 3,
                "language_count": 4,
                "stale_block_behavior": False,
                "safe_next_action_present": False,
                "real_target_comparison_present": True,
                "target_comparison_delta": {"time_to_first_safe_action_delta": -0.2},
            },
        )

        self.assertEqual(scorecard["fixture_evaluation_status"], "fixture_thresholds_failed")
        self.assertEqual(scorecard["promotion_decision"], "not_promoted")
        self.assertIn("symbol_recall_below_threshold", scorecard["blocking_reasons"])
        self.assertIn("stale_block_behavior_missing", scorecard["blocking_reasons"])

        scorecard["promotion_decision"] = "owner_review_required"
        scorecard["metrics"].pop("symbol_recall")

        errors = validate_graph_usefulness_scorecard(scorecard)

        self.assertIn("promotion_decision must be not_promoted", errors)
        self.assertIn("metrics.symbol_recall must be between 0 and 1", errors)


if __name__ == "__main__":
    unittest.main()
