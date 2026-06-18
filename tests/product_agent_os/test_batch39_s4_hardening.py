from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


class Batch39S4HardeningTests(unittest.TestCase):
    def test_m37_public_docs_classifies_first_run_pages_without_public_readiness_claim(self) -> None:
        from product_agent_os.batch39_s4_hardening import (  # noqa: PLC0415
            FIRST_RUN_GENERATED_PAGES,
            build_m37_public_docs_acceptance,
        )

        acceptance = build_m37_public_docs_acceptance(
            public_docs_scope="internal_control_plane_only",
            first_run_page_ids=FIRST_RUN_GENERATED_PAGES,
        )

        self.assertEqual(acceptance["task_id"], "B39-TEST-M37")
        self.assertEqual(acceptance["status"], "partial_pass_public_docs_internal_only")
        self.assertEqual(acceptance["public_readiness_claim"], "not_claimed")
        self.assertEqual(acceptance["first_run_generated_pages"]["classification"], "not_applicable_to_public_site")
        self.assertEqual(acceptance["first_run_generated_pages"]["page_count"], 11)
        self.assertIn("generated orientation evidence", " ".join(acceptance["unsupported_claims"]))

    def test_m38_offline_html_audit_blocks_external_urls_and_scripts(self) -> None:
        from product_agent_os.batch39_s4_hardening import audit_first_run_offline_html  # noqa: PLC0415

        safe_html = {
            "index.html": "<!doctype html><a href=\"inventory.html\">Inventory</a><code>generated-view-only</code>",
            "inventory.html": "<!doctype html><a href=\"#top\">Top</a>",
        }
        unsafe_html = {
            "index.html": "<script src=\"https://cdn.example/app.js\"></script>",
            "risks.html": "<a href=\"http://example.test\">external</a><script>alert(1)</script>",
        }

        safe = audit_first_run_offline_html(safe_html)
        unsafe = audit_first_run_offline_html(unsafe_html)

        self.assertEqual(safe["status"], "passed_no_external_url_or_script")
        self.assertEqual(safe["blocked_counts"]["external_url"], 0)
        self.assertEqual(safe["blocked_counts"]["script_tag"], 0)
        self.assertEqual(unsafe["status"], "blocked_external_url_or_script")
        self.assertEqual(unsafe["blocked_counts"]["external_url"], 2)
        self.assertEqual(unsafe["blocked_counts"]["script_tag"], 2)
        self.assertEqual(unsafe["violations"][0]["page"], "index.html")

    def test_m39_cli_contract_matrix_covers_required_modes_and_unsafe_packet_cases(self) -> None:
        from product_agent_os.batch39_s4_hardening import build_m39_cli_contract_matrix  # noqa: PLC0415

        matrix = build_m39_cli_contract_matrix()
        rows = {row["case_id"]: row for row in matrix["cases"]}

        self.assertEqual(matrix["task_id"], "B39-TEST-M39")
        self.assertEqual(matrix["status"], "partial_pass_cli_contract_matrix")
        self.assertEqual(
            set(rows),
            {
                "first_run_dry_run",
                "first_run_write",
                "first_run_ambiguous_mode_rejection",
                "first_run_stage_rejection",
                "unsafe_packet_rejection",
            },
        )
        self.assertEqual(rows["first_run_dry_run"]["write_scope"], "stdout_only")
        self.assertEqual(rows["first_run_write"]["write_scope"], ".codex/product-agent-os/analysis")
        self.assertEqual(rows["first_run_stage_rejection"]["expected_status"], "rejected")
        self.assertEqual(rows["unsafe_packet_rejection"]["guardrail"], "no_secret_no_raw_source_no_local_path")
        self.assertIn("target mutation", " ".join(matrix["unsupported_claims"]))

    def test_m37_m39_summary_is_json_safe_and_keeps_b39_s4_open(self) -> None:
        from product_agent_os.batch39_s4_hardening import build_m37_m39_hardening_summary  # noqa: PLC0415

        summary = build_m37_m39_hardening_summary(generated_at="2026-06-18T18:00:00+03:00")
        encoded = json.dumps(summary, ensure_ascii=False, sort_keys=True)

        self.assertEqual(summary["schema_version"], "batch39_s4_m37_m39_hardening_summary_v1")
        self.assertEqual(summary["attempt_id"], "B39-S4-M37-M39-A01")
        self.assertEqual(summary["slice_status"], "partial_pass_broader_b39_s4_still_open")
        self.assertEqual(sorted(summary["tasks"]), ["B39-TEST-M37", "B39-TEST-M38", "B39-TEST-M39"])
        self.assertNotIn("C:\\Users\\user", encoded)
        self.assertNotIn("sk-", encoded)
        self.assertIn("runtime/browser QA", " ".join(summary["unsupported_claims"]))

    def test_full_dependency_readiness_excludes_dependency_corpora_and_keeps_runtime_blocked(self) -> None:
        from product_agent_os.batch39_s4_hardening import build_target_dependency_readiness  # noqa: PLC0415

        sol = build_target_dependency_readiness(
            target_id="sol_0_6",
            target_kind="node_fullstack",
            file_refs=[
                "frontend/package.json",
                "frontend/package-lock.json",
                "frontend/node_modules/next/package.json",
                "frontend/.next/BUILD_ID",
                "backend/package.json",
                "backend/package-lock.json",
                "backend/node_modules/express/package.json",
                "antigravity-awesome-skills-main/package.json",
            ],
            runtime_write_risks=["frontend_next_cache", "backend_lancedb_data"],
            provider_risks=["backend_env_provider_credentials", "google_genai_dependency"],
        )
        neural = build_target_dependency_readiness(
            target_id="neural_flow",
            target_kind="docs_research_only",
            file_refs=["PLAN.md", "README.md", "research/source.md"],
            runtime_write_risks=[],
            provider_risks=[],
        )

        self.assertEqual(sol["status"], "partial_pass_static_dependency_inventory_runtime_blocked")
        self.assertEqual(sol["manifest_summary"]["product_manifest_count"], 4)
        self.assertIn("frontend/node_modules/next/package.json", sol["excluded_dependency_corpora"])
        self.assertIn("antigravity-awesome-skills-main/package.json", sol["excluded_dependency_corpora"])
        self.assertTrue(sol["runtime_guardrails"]["target_runtime_blocked"])
        self.assertTrue(sol["runtime_guardrails"]["provider_calls_blocked"])
        self.assertEqual(neural["status"], "not_applicable_docs_research_target_no_runtime_manifests")
        self.assertTrue(neural["runtime_guardrails"]["target_runtime_blocked"])

    def test_all_script_cli_matrix_rollup_keeps_help_gaps_visible(self) -> None:
        from product_agent_os.batch39_s4_hardening import summarize_cli_matrix  # noqa: PLC0415

        matrix = summarize_cli_matrix(
            [
                {"script": "run_first_project_analysis.py", "help_status": "passed", "exit_code": 0},
                {"script": "detect_project.py", "help_status": "failed", "exit_code": 1},
                {"script": "scan_project_code_graph.py", "help_status": "passed", "exit_code": 0},
            ]
        )

        self.assertEqual(matrix["task_id"], "B39-TEST-M39")
        self.assertEqual(matrix["status"], "partial_pass_all_script_cli_matrix_with_help_gaps")
        self.assertEqual(matrix["script_count"], 3)
        self.assertEqual(matrix["help_pass_count"], 2)
        self.assertEqual(matrix["help_gap_count"], 1)
        self.assertEqual(matrix["help_gaps"], ["detect_project.py"])
        self.assertIn("target mutation", " ".join(matrix["unsupported_claims"]))

    def test_runtime_browser_harness_records_blocked_and_non_mutating_status(self) -> None:
        from product_agent_os.batch39_s4_hardening import build_runtime_browser_harness_status  # noqa: PLC0415

        status = build_runtime_browser_harness_status(
            target_id="sol_0_6",
            runtime_entrypoints=["frontend:npm run dev", "backend:npm run dev"],
            browser_tool_status="blocked_playwright_unavailable",
            mutation_risks=["frontend .next cache", "backend .sol_data"],
            provider_risks=["backend /api/llm/test"],
            executed_runtime=False,
            executed_browser=False,
        )

        self.assertEqual(status["task_id"], "B39-TEST-M42")
        self.assertEqual(status["status"], "blocked_runtime_browser_requires_mutation_or_missing_tool")
        self.assertEqual(status["target_mutation_performed"], False)
        self.assertEqual(status["browser_automation_performed"], False)
        self.assertIn("frontend:npm run dev", status["runtime_entrypoints"])
        self.assertIn("provider/API calls were not performed", " ".join(status["unsupported_claims"]))

    def test_full_comparison_separates_previous_and_current_results(self) -> None:
        from product_agent_os.batch39_s4_hardening import build_target_comparison  # noqa: PLC0415

        comparison = build_target_comparison(
            target_id="sol_0_6",
            previous={
                "project_graph": {"nodes": 2830, "edges": 2914},
                "runtime_browser": {"status": "not_performed"},
            },
            current={
                "project_graph": {"nodes": 2830, "edges": 2914},
                "runtime_browser": {"status": "blocked_runtime_browser_requires_mutation_or_missing_tool"},
            },
        )

        self.assertEqual(comparison["target_id"], "sol_0_6")
        self.assertEqual(comparison["previous"]["project_graph"]["nodes"], 2830)
        self.assertEqual(comparison["current"]["runtime_browser"]["status"], "blocked_runtime_browser_requires_mutation_or_missing_tool")
        self.assertEqual(comparison["delta"]["project_graph_nodes"], 0)
        self.assertEqual(comparison["delta"]["runtime_browser_status"], "not_performed -> blocked_runtime_browser_requires_mutation_or_missing_tool")

    def test_remaining_top_level_scripts_expose_help_contracts(self) -> None:
        scripts = [
            "detect_project.py",
            "merge_markdown.py",
            "run_fixture_eval.py",
            "run_methodology_audit.py",
            "validate_agents.py",
            "validate_automation_candidate.py",
            "validate_codex_runtime_runner.py",
            "validate_control_plane.py",
            "validate_doubt_verification_packet.py",
            "validate_hooks.py",
            "validate_source_policy.py",
            "validate_task_matrix.py",
        ]

        for script in scripts:
            with self.subTest(script=script):
                result = subprocess.run(
                    [sys.executable, str(SCRIPTS / script), "--help"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    timeout=20,
                )
                combined = f"{result.stdout}\n{result.stderr}".lower()
                self.assertEqual(result.returncode, 0, combined[:500])
                self.assertIn("usage:", combined)

    def test_remaining_gates_summary_covers_m41_through_m54_without_live_claims(self) -> None:
        from product_agent_os.batch39_s4_remaining_gates import build_remaining_gates_summary  # noqa: PLC0415

        summary = build_remaining_gates_summary(
            generated_at="2026-06-18T21:30:00+03:00",
            cli_help_pass_count=31,
            cli_help_gap_count=0,
            mkdocs_available=False,
        )

        expected_tasks = {
            "B39-TEST-M41",
            "B39-TEST-M42",
            "B39-TEST-M43",
            "B39-TEST-M44",
            "B39-TEST-M45",
            "B39-TEST-M46",
            "B39-TEST-M47",
            "B39-TEST-M48",
            "B39-TEST-M49",
            "B39-TEST-M50",
            "B39-TEST-M51",
            "B39-TEST-M52",
            "B39-TEST-M53",
            "B39-TEST-M54",
        }

        self.assertTrue(expected_tasks.issubset(set(summary["tasks"])))
        self.assertEqual(summary["tasks"]["B39-TEST-M39"]["status"], "passed_all_script_cli_help_matrix")
        self.assertEqual(summary["tasks"]["B39-TEST-M37"]["status"], "blocked_expected_mkdocs_unavailable")
        self.assertEqual(summary["tasks"]["B39-TEST-M42"]["status"], "blocked_expected_runtime_browser_requires_approval")
        self.assertEqual(summary["slice_status"], "executed_remaining_s4_gates_with_expected_approval_blocks")
        self.assertFalse(summary["actions_performed"]["target_workspace_mutation"])
        self.assertFalse(summary["actions_performed"]["live_server"])
        self.assertFalse(summary["actions_performed"]["provider_api_call"])
        self.assertIn("runtime/browser pass is not claimed", " ".join(summary["unsupported_claims"]))

    def test_remaining_gate_records_are_json_safe_and_have_product_value(self) -> None:
        from product_agent_os.batch39_s4_remaining_gates import build_remaining_gates_summary  # noqa: PLC0415

        summary = build_remaining_gates_summary(
            generated_at="2026-06-18T21:30:00+03:00",
            cli_help_pass_count=31,
            cli_help_gap_count=0,
            mkdocs_available=False,
        )
        encoded = json.dumps(summary, ensure_ascii=False, sort_keys=True)

        for task_id, record in summary["tasks"].items():
            with self.subTest(task_id=task_id):
                self.assertTrue(record["technical_value"])
                self.assertTrue(record["product_value"])
                self.assertTrue(record["evidence_refs"])
                self.assertIn(record["status"], summary["allowed_statuses"])
        self.assertNotIn("C:\\Users\\user", encoded)
        self.assertNotIn("sk-", encoded)


if __name__ == "__main__":
    unittest.main()
