import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
PRODUCT_AGENT_OS = DOCS / "product-agent-os"
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
TEMPLATE_ROOT = ROOT / "plugins" / "product-agent-os" / "assets" / "templates"
SUMMARY = (
    DOCS
    / "superpowers"
    / "specs"
    / "batch45-professional-code-s4-public-docs-closure-summary.json"
)
S5_SUMMARY = (
    DOCS
    / "superpowers"
    / "specs"
    / "batch45-professional-code-s5-learning-automation-summary.json"
)
M26_RESULTS = DOCS / "superpowers" / "specs" / "batch45-agent-behavior-eval-results.json"
M26_PLAN = DOCS / "superpowers" / "specs" / "batch45-agent-behavior-eval-plan.json"
M27_DECISION = DOCS / "superpowers" / "specs" / "batch45-comment-policy-promotion-decision.json"
M33_COMPARISON = DOCS / "superpowers" / "specs" / "batch45-real-project-refactor-comparison.json"
M34_SCORECARD = DOCS / "superpowers" / "specs" / "batch45-real-project-scorecard.json"
M35_DECISION = DOCS / "superpowers" / "specs" / "batch45-real-project-decision-packet.json"
M37_REMEDIATION = DOCS / "superpowers" / "specs" / "batch45-review-remediation-summary.json"
RETEST_PROTOCOL = DOCS / "superpowers" / "specs" / "batch45-quality-retest-protocol.json"
RETEST_Q3_SUMMARY = DOCS / "superpowers" / "specs" / "batch45-quality-retest-fixture-static-summary.json"
RETEST_Q4_SUMMARY = DOCS / "superpowers" / "specs" / "batch45-quality-retest-project-slices-static-summary.json"
POST_Q4_NEXT_TASKS = DOCS / "superpowers" / "specs" / "batch45-post-q4-next-tasks.json"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.templates import required_templates, template_by_target  # noqa: E402


class CodingStandardsArtifactsTest(unittest.TestCase):
    def test_public_docs_are_source_bound_and_nav_registered(self):
        ru = (PRODUCT_AGENT_OS / "coding-standards.md").read_text(encoding="utf-8")
        en = (PRODUCT_AGENT_OS / "coding-standards.en.md").read_text(encoding="utf-8")
        combined = (ru + "\n" + en).lower()

        for expected in [
            "source status:",
            "professional code authoring",
            "existing_capability_scan",
            "one_line_candidate",
            "negative_dependency_rule",
            "deep_module_check",
            "legacy_seam_check",
            "comment_policy",
            "cleverness_budget",
            "minimum_manual_successful_runs: 3",
            "candidate-only learning-loop/automation policy",
            "orientation_only_not_proof",
            "does not prove that ai agents now write enterprise-quality code in real projects",
            "m26 records a live behavior-eval no-go",
            "m27 keeps the m25 advisory local/non-blocking",
            "m35 keeps s7 fixture-local/source-only",
            "m37 records local hook/validator hardening plus review remediation docs/control-plane sync only",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, combined)

        forbidden_claims = [
            "hooks are active",
            "automation is active",
            "provider call performed",
            "browser verified",
            "plugin cache refreshed",
            "target workspace mutated",
            "release ready",
        ]
        for forbidden in forbidden_claims:
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, combined)

        mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        check_docs = (ROOT / "tools" / "check_docs.py").read_text(encoding="utf-8")
        self.assertIn("product-agent-os/coding-standards.md", mkdocs)
        self.assertIn("DOCS / \"product-agent-os\" / \"coding-standards.md\"", check_docs)
        self.assertIn("\"product-agent-os/coding-standards.md\"", check_docs)

    def test_cross_links_route_standards_from_public_docs(self):
        required_links = {
            "index.md": "coding-standards.md",
            "index.en.md": "coding-standards.md",
            "technical.md": "coding-standards.md",
            "technical.en.md": "coding-standards.md",
            "development-standards.md": "coding-standards.md",
            "development-standards.en.md": "coding-standards.md",
            "artifact-contracts.md": "coding-standards.md",
            "artifact-contracts.en.md": "coding-standards.md",
            "behavioral-evals.md": "coding-standards.md",
            "behavioral-evals.en.md": "coding-standards.md",
            "scenarios.md": "coding-standards.md",
            "scenarios.en.md": "coding-standards.md",
            "architecture.md": "coding-standards.md",
            "architecture.en.md": "coding-standards.md",
        }
        for filename, expected in required_links.items():
            with self.subTest(filename=filename):
                self.assertIn(expected, (PRODUCT_AGENT_OS / filename).read_text(encoding="utf-8"))

        for relative in ["code-review.md", "code-review.en.md"]:
            with self.subTest(playbook=relative):
                self.assertIn(
                    "../product-agent-os/coding-standards.md",
                    (DOCS / "playbooks" / relative).read_text(encoding="utf-8"),
                )

    def test_templates_and_eval_cases_remain_registered_without_stale_paths(self):
        expected_targets = {
            ".codex/workflows/coding-standards.md": "workflow-coding-standards",
            ".codex/artifact-templates/coding-standard-checklist.md": "artifact-coding-standard-checklist",
        }
        registered_targets = {template.target_path for template in required_templates()}
        for target, key in expected_targets.items():
            with self.subTest(target=target):
                self.assertIn(target, registered_targets)
                template = template_by_target(target)
                self.assertEqual(key, template.key)
                self.assertNotIn("assets/templates/artifacts", template.source_path.as_posix())

        behavioral = json.loads(
            (TEMPLATE_ROOT / "evals" / "behavioral-workflows.json").read_text(encoding="utf-8")
        )
        cases = {case["name"]: case for case in behavioral["cases"]}
        for case_name in [
            "professional-code-authoring-custom-code-bloat",
            "professional-code-authoring-unnecessary-dependency",
            "professional-code-authoring-missing-existing-capability-scan",
            "professional-code-authoring-comment-noise",
            "professional-code-authoring-shallow-wrapper",
            "professional-code-authoring-unsupported-legacy-rewrite",
        ]:
            with self.subTest(case=case_name):
                payload = json.dumps(cases[case_name], sort_keys=True).lower()
                self.assertIn("professional_code_authoring", payload)
                self.assertIn("coding-standard-checklist.md", payload)

    def test_s4_closure_packet_records_scope_and_claim_ceiling(self):
        packet = json.loads(SUMMARY.read_text(encoding="utf-8"))
        self.assertEqual("batch45_professional_code_s4_public_docs_closure_v1", packet["schema_version"])
        self.assertEqual("B45-S4-M12-M13-M19-M14-A01", packet["evidence_id"])
        self.assertEqual("implemented_s4_docs_contract_ready", packet["status"])

        self.assertEqual(
            {
                "B45-PCA-M12": "implemented_docs_contract_ready",
                "B45-PCA-M13": "implemented_docs_contract_ready",
                "B45-PCA-M19": "implemented_docs_contract_ready",
                "B45-PCA-M14": "closure_through_s4_pending_b45_pca_m23",
            },
            packet["row_status"],
        )
        self.assertEqual("planned_B45_S5", packet["remaining_rows"]["B45-PCA-M23"])
        self.assertIn("docs/product-agent-os/coding-standards.md", packet["source_docs"])
        self.assertIn("tests/product_agent_os/test_coding_standards_artifacts.py", packet["tests_added"])

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        self.assertIn("root_site_freshness_for_new_page_not_claimed", packet["accepted_gaps"])

    def test_m37_review_remediation_packet_links_public_docs_registry_and_control_plane(self):
        packet = json.loads(M37_REMEDIATION.read_text(encoding="utf-8"))
        serialized = json.dumps(packet, sort_keys=True).lower()
        ru = (PRODUCT_AGENT_OS / "coding-standards.md").read_text(encoding="utf-8").lower()
        en = (PRODUCT_AGENT_OS / "coding-standards.en.md").read_text(encoding="utf-8").lower()
        registry_ru = (DOCS / "sources" / "registry.md").read_text(encoding="utf-8")
        registry_en = (DOCS / "sources" / "registry.en.md").read_text(encoding="utf-8")
        plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        evals = (ROOT / "EVALS.md").read_text(encoding="utf-8")
        test_plan = (ROOT / "TEST.md").read_text(encoding="utf-8")
        track11 = (
            DOCS
            / "superpowers"
            / "plans"
            / "2026-06-20-track-11-documentation-architecture-refresh.md"
        ).read_text(encoding="utf-8")

        self.assertEqual("batch45_review_remediation_summary_v1", packet["schema_version"])
        self.assertEqual("B45-PCA-M37", packet["task_id"])
        self.assertEqual("B45-PCA-M37-A01", packet["evidence_id"])
        self.assertEqual("implemented_local_advisory_hardening_docs_sync_only", packet["status"])
        self.assertEqual(
            "reserved_for_optional_runtime_browser_approval_packet_not_used_by_this_remediation",
            packet["reserved_ids"]["B45-PCA-M36"],
        )
        self.assertEqual("no_go_advisory_only", packet["scope"]["promotion_state"])
        self.assertEqual(
            "local_synthetic_hardening_no_promotion_claim",
            packet["scope"]["closure_level"],
        )
        self.assertEqual(
            "handoff_required_due_runlog_budget",
            packet["control_plane_sync_decision"]["RUNLOG.md"],
        )

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        self.assertTrue(packet["local_remediation_actions"]["hook_or_code_files_changed_within_m37_scope"])
        self.assertTrue(packet["local_remediation_actions"]["comment_sufficiency_tests_changed_within_m37_scope"])
        self.assertTrue(packet["local_remediation_actions"]["active_and_packaged_hook_template_kept_in_parity"])

        for expected in [
            "b45-pca-m37-a01",
            "m36 remains reserved",
            "local hook/validator",
            "promotion remains no_go/advisory-only",
            "runtime/browser/provider/target/git/release/deploy/automation",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, serialized)

        for doc in [ru, en]:
            with self.subTest(doc="public_coding_standards"):
                self.assertIn("batch45-review-remediation-summary.json", doc)
                self.assertIn("m26 records a live behavior-eval no-go", doc)
                self.assertIn("m27 keeps the m25 advisory local/non-blocking", doc)
                self.assertIn("m35 keeps s7 fixture-local/source-only", doc)
                self.assertIn("m37 records local hook/validator hardening plus review remediation docs/control-plane sync only", doc)

        for registry in [registry_ru, registry_en]:
            with self.subTest(registry="source_registry"):
                self.assertIn("B45-PCA-M37", registry)
                self.assertIn("B45-PCA-M37-A01", registry)
                self.assertIn("docs/superpowers/specs/batch45-review-remediation-summary.json", registry)
                self.assertIn("M36 remains reserved", registry)

        self.assertIn("B45-PCA-M37-A01", plan)
        self.assertIn("B45-PCA-M37-A01", evals)
        self.assertIn("B45-PCA-M37-A01", test_plan)
        self.assertIn("| `B45-PCA-M37` |", track11)

    def test_b45_retest_q0_q2_protocol_links_sources_tasks_and_control_plane(self):
        packet = json.loads(RETEST_PROTOCOL.read_text(encoding="utf-8"))
        serialized = json.dumps(packet, sort_keys=True).lower()
        registry_ru = (DOCS / "sources" / "registry.md").read_text(encoding="utf-8")
        registry_en = (DOCS / "sources" / "registry.en.md").read_text(encoding="utf-8")
        plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        evals = (ROOT / "EVALS.md").read_text(encoding="utf-8")
        test_plan = (ROOT / "TEST.md").read_text(encoding="utf-8")
        track11 = (
            DOCS
            / "superpowers"
            / "plans"
            / "2026-06-20-track-11-documentation-architecture-refresh.md"
        ).read_text(encoding="utf-8")

        self.assertEqual("batch45_quality_retest_protocol_v1", packet["schema_version"])
        self.assertEqual("B45-RETEST-Q0-Q2", packet["task_id"])
        self.assertEqual("B45-RETEST-Q0-Q2-A01", packet["evidence_id"])
        self.assertEqual("implemented_source_only_protocol_harness_ready", packet["status"])
        self.assertEqual(
            "docs_contract_ready_for_local_static_retest_protocol",
            packet["scope"]["closure_level"],
        )
        self.assertEqual("approval_required_not_run", packet["scope"]["live_model_behavior_eval"])
        self.assertEqual("approval_required_not_run_B45_PCA_M36_reserved", packet["scope"]["runtime_browser_pilot"])

        self.assertEqual(
            {
                "B45-RETEST-Q0-SOURCE-FREEZE",
                "B45-RETEST-Q1-HELDOUT-V2",
                "B45-RETEST-Q2-HARNESS-DRY-RUN",
            },
            set(packet["queue_status"]),
        )
        self.assertEqual(8, len(packet["held_out_tasks_v2"]))
        self.assertEqual({f"H{i}" for i in range(1, 9)}, {task["slot"] for task in packet["held_out_tasks_v2"]})
        self.assertEqual(
            {"SOL-TS-STATIC-01", "MP-CRM-CHAR-01"},
            {canary["scenario_id"] for canary in packet["fixture_canaries"]},
        )

        blocker_ids = {blocker["id"] for blocker in packet["source_freeze"]["active_blockers"]}
        self.assertEqual({"B45-PCA-M26", "B45-PCA-M27", "B45-PCA-M35", "B45-PCA-M37-A01"}, blocker_ids)
        self.assertEqual(0.5, packet["thresholds"]["promotion_candidate_gate"]["treatment_delta_min"])
        self.assertEqual(0, packet["thresholds"]["promotion_candidate_gate"]["timeout_count_required"])
        self.assertIn("runtime_or_product_behavior_claim_from_local_static_evidence", packet["thresholds"]["automatic_no_go"])

        for action, performed in packet["privacy_and_approval_boundary"]["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for expected in [
            "real_ai_agent_behavior_improvement",
            "ci_or_blocker_enforcement_readiness",
            "target_runtime_behavior",
            "B45-RETEST-Q3-FIXTURE-STATIC".lower(),
            "comment_sufficiency.py <approved-corpus-paths>",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected.lower(), serialized)

        for registry in [registry_ru, registry_en]:
            with self.subTest(registry="source_registry"):
                self.assertIn("B45-RETEST-Q0-Q2", registry)
                self.assertIn("B45-RETEST-Q0-Q2-A01", registry)
                self.assertIn("docs/superpowers/specs/batch45-quality-retest-protocol.json", registry)

        for control_plane in [plan, evals, test_plan, track11]:
            with self.subTest(control_plane="compact_pointer"):
                self.assertIn("B45-RETEST-Q0-Q2-A01", control_plane)

        self.assertIn("| `B45-RETEST-Q0-Q2` |", track11)

    def test_b45_retest_q3_fixture_static_summary_records_local_static_replay_only(self):
        packet = json.loads(RETEST_Q3_SUMMARY.read_text(encoding="utf-8"))
        serialized = json.dumps(packet, sort_keys=True).lower()
        registry_ru = (DOCS / "sources" / "registry.md").read_text(encoding="utf-8")
        registry_en = (DOCS / "sources" / "registry.en.md").read_text(encoding="utf-8")
        plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        evals = (ROOT / "EVALS.md").read_text(encoding="utf-8")
        test_plan = (ROOT / "TEST.md").read_text(encoding="utf-8")
        track11 = (
            DOCS
            / "superpowers"
            / "plans"
            / "2026-06-20-track-11-documentation-architecture-refresh.md"
        ).read_text(encoding="utf-8")

        self.assertEqual("batch45_quality_retest_fixture_static_summary_v1", packet["schema_version"])
        self.assertEqual("B45-RETEST-Q3-FIXTURE-STATIC", packet["task_id"])
        self.assertEqual("B45-RETEST-Q3-FIXTURE-STATIC-A01", packet["evidence_id"])
        self.assertEqual("implemented_local_static_fixture_retest_with_gaps", packet["status"])
        self.assertEqual("local_static_retest_with_gaps", packet["scope"]["closure_level"])
        self.assertEqual("keep_advisory_only_no_go", packet["scope"]["promotion_state"])
        self.assertEqual("approval_required_not_run", packet["scope"]["live_model_behavior_eval"])
        self.assertEqual("approval_required_not_run_B45_PCA_M36_reserved", packet["scope"]["runtime_browser_pilot"])

        self.assertEqual(37, packet["approved_corpus"]["file_count"])
        self.assertEqual(14, packet["static_replay"]["warning_count"])
        self.assertFalse(packet["static_replay"]["blocking"])
        self.assertEqual(0, packet["static_replay"]["suppressed_warning_count"])
        self.assertEqual({"javascript": 12, "python": 2}, packet["static_replay"]["language_counts"])
        self.assertEqual({"mypartners": 3, "sol": 11}, packet["static_replay"]["fixture_counts"])
        self.assertEqual(14, len(packet["static_replay"]["warnings"]))
        self.assertEqual(0, packet["privacy_review"]["forbidden_artifact_file_count"]["fixtures"])
        self.assertEqual(0, packet["privacy_review"]["absolute_path_match_count"]["fixtures"])
        self.assertEqual(10, packet["privacy_review"]["provider_env_name_match_count"]["fixtures"])
        self.assertEqual(
            "static_provider_activation_risk_not_secret_value_leakage",
            packet["privacy_review"]["provider_env_name_classification"],
        )

        for check in packet["syntax_only_checks"]:
            with self.subTest(command=check["command"]):
                self.assertEqual(0, check["exit_code"])
                self.assertEqual("not_claimed", check["runtime_claim"])

        self.assertTrue(all(item["exit_code_interpretation"] == "diff_present_expected" for item in packet["refactor_numstat"]))
        self.assertEqual("continue_investigation_keep_advisory_only_no_go", packet["decision"]["status"])
        self.assertEqual("approval_required_not_run", packet["decision"]["next_queue_status"])
        self.assertEqual("approval_required_runtime_browser_packet_not_run", packet["decision"]["alternative_next_queue_status"])

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for expected in [
            "real_ai_agent_behavior_improvement",
            "treatment_v2_promotion_readiness",
            "target_runtime_behavior",
            "B45-PCA-M26".lower(),
            "B45-PCA-M27".lower(),
            "B45-PCA-M35".lower(),
            "B45-PCA-M37-A01".lower(),
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected.lower(), serialized)

        for registry in [registry_ru, registry_en]:
            with self.subTest(registry="source_registry"):
                self.assertIn("B45-RETEST-Q3-FIXTURE-STATIC", registry)
                self.assertIn("B45-RETEST-Q3-FIXTURE-STATIC-A01", registry)
                self.assertIn("docs/superpowers/specs/batch45-quality-retest-fixture-static-summary.json", registry)

        for control_plane in [plan, evals, test_plan, track11]:
            with self.subTest(control_plane="compact_pointer"):
                self.assertIn("B45-RETEST-Q3-FIXTURE-STATIC-A01", control_plane)

        self.assertIn("| `B45-RETEST-Q3-FIXTURE-STATIC` |", track11)

    def test_b45_retest_q4_project_slices_static_summary_records_static_only(self):
        packet = json.loads(RETEST_Q4_SUMMARY.read_text(encoding="utf-8"))
        serialized = json.dumps(packet, sort_keys=True).lower()
        registry_ru = (DOCS / "sources" / "registry.md").read_text(encoding="utf-8")
        registry_en = (DOCS / "sources" / "registry.en.md").read_text(encoding="utf-8")
        plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        evals = (ROOT / "EVALS.md").read_text(encoding="utf-8")
        test_plan = (ROOT / "TEST.md").read_text(encoding="utf-8")
        track11 = (
            DOCS
            / "superpowers"
            / "plans"
            / "2026-06-20-track-11-documentation-architecture-refresh.md"
        ).read_text(encoding="utf-8")

        self.assertEqual("batch45_quality_retest_project_slices_static_summary_v1", packet["schema_version"])
        self.assertEqual("B45-RETEST-Q4-PROJECT-SLICES-STATIC", packet["task_id"])
        self.assertEqual("B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01", packet["evidence_id"])
        self.assertEqual("implemented_local_static_project_slice_retest_with_gaps", packet["status"])
        self.assertEqual("local_static_project_slice_retest_with_gaps", packet["scope"]["closure_level"])
        self.assertEqual("keep_advisory_only_no_go", packet["scope"]["promotion_state"])
        self.assertEqual("approval_required_not_run", packet["scope"]["live_model_behavior_eval"])
        self.assertEqual("approval_required_not_run_B45_PCA_M36_reserved", packet["scope"]["runtime_browser_pilot"])

        slice_set = packet["slice_set"]
        self.assertEqual(5, slice_set["slice_count"])
        self.assertEqual(46, slice_set["total_files"])
        self.assertEqual(37, slice_set["code_files"])
        self.assertEqual(9, slice_set["config_doc_files"])
        self.assertEqual(
            {
                "Q4-SOL-01-BOOTSTRAP": 0,
                "Q4-SOL-02-ORCHESTRATION-CORE": 0,
                "Q4-SOL-03-AGENT-ROLES-TOOLS": 11,
                "Q4-MP-01-SERVER-CRM-CORE": 2,
                "Q4-MP-02-FRONTEND-CRM-TESTS": 1,
            },
            {
                item["slice_id"]: item["comment_sufficiency"]["warning_count"]
                for item in slice_set["slices"]
            },
        )
        self.assertTrue(all(not item["comment_sufficiency"]["blocking"] for item in slice_set["slices"]))
        self.assertTrue(all(item["comment_sufficiency"]["suppressed_warning_count"] == 0 for item in slice_set["slices"]))

        aggregate = packet["aggregate_static_replay"]
        self.assertEqual(14, aggregate["warning_count_total"])
        self.assertEqual(0, aggregate["blocking_slices"])
        self.assertEqual(0, aggregate["suppressed_warning_count_total"])
        self.assertEqual({"javascript": 12, "python": 2}, aggregate["language_counts"])
        self.assertEqual({"mypartners": 3, "sol": 11}, aggregate["fixture_counts"])

        privacy = packet["privacy_review"]
        self.assertEqual(0, privacy["forbidden_artifact_file_count"])
        self.assertEqual(0, privacy["secret_literal_match_count"])
        self.assertEqual(6, privacy["absolute_path_match_count"])
        self.assertEqual(2, privacy["provider_env_name_match_count"])
        self.assertEqual("static_env_lookup_name_not_secret_value_leakage", privacy["provider_env_name_classification"])

        self.assertEqual(1, len(packet["syntax_only_checks"]))
        self.assertEqual(0, packet["syntax_only_checks"][0]["exit_code"])
        self.assertEqual("not_claimed", packet["syntax_only_checks"][0]["runtime_claim"])
        self.assertEqual(
            "no_generated_pycache_directories_remain",
            packet["syntax_only_checks"][0]["generated_cache_cleanup"]["post_cleanup_status"],
        )
        self.assertTrue(all(item["exit_code_interpretation"] == "diff_present_expected" for item in packet["refactor_numstat"]))

        self.assertEqual("continue_investigation_keep_advisory_only_no_go", packet["decision"]["status"])
        self.assertEqual("approval_required_not_run", packet["decision"]["next_queue_status"])
        self.assertEqual("approval_required_runtime_browser_packet_not_run", packet["decision"]["alternative_next_queue_status"])
        self.assertEqual(
            "handoff_required_due_runlog_budget",
            packet["control_plane_sync_decision"]["RUNLOG.md"],
        )

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for expected in [
            "real_ai_agent_behavior_improvement",
            "treatment_v2_promotion_readiness",
            "target_runtime_behavior",
            "B45-PCA-M26".lower(),
            "B45-PCA-M27".lower(),
            "B45-PCA-M35".lower(),
            "B45-PCA-M37-A01".lower(),
            "B45-RETEST-Q5-LIVE-MODEL-RERUN".lower(),
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected.lower(), serialized)

        for registry in [registry_ru, registry_en]:
            with self.subTest(registry="source_registry"):
                self.assertIn("B45-RETEST-Q4-PROJECT-SLICES-STATIC", registry)
                self.assertIn("B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01", registry)
                self.assertIn("docs/superpowers/specs/batch45-quality-retest-project-slices-static-summary.json", registry)

        for control_plane in [plan, evals, test_plan, track11]:
            with self.subTest(control_plane="compact_pointer"):
                self.assertIn("B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01", control_plane)

        self.assertIn("| `B45-RETEST-Q4-PROJECT-SLICES-STATIC` |", track11)

    def test_b45_post_q4_next_tasks_records_followup_queue_without_promotion_claim(self):
        packet = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
        serialized = json.dumps(packet, sort_keys=True).lower()
        registry_ru = (DOCS / "sources" / "registry.md").read_text(encoding="utf-8")
        registry_en = (DOCS / "sources" / "registry.en.md").read_text(encoding="utf-8")
        plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        evals = (ROOT / "EVALS.md").read_text(encoding="utf-8")
        test_plan = (ROOT / "TEST.md").read_text(encoding="utf-8")
        track11 = (
            DOCS
            / "superpowers"
            / "plans"
            / "2026-06-20-track-11-documentation-architecture-refresh.md"
        ).read_text(encoding="utf-8")
        lifecycle = json.loads((ROOT / ".codex" / "product-agent-os" / "lifecycle-state.json").read_text(encoding="utf-8"))

        self.assertEqual("batch45_post_q4_next_tasks_v1", packet["schema_version"])
        self.assertEqual("B45-POST-Q4-NEXT-TASKS", packet["task_id"])
        self.assertEqual("B45-POST-Q4-NEXT-TASKS-A01", packet["evidence_id"])
        self.assertEqual("planned_source_owned_next_tasks_after_q4", packet["status"])
        self.assertEqual(14, packet["basis"]["q3_warning_count"])
        self.assertEqual(14, packet["basis"]["q4_warning_count"])
        self.assertEqual(5, packet["basis"]["q4_slice_count"])
        self.assertTrue(packet["basis"]["stable_signal"])
        self.assertEqual("Q4-SOL-03-AGENT-ROLES-TOOLS", packet["basis"]["main_static_hotspot"])
        self.assertTrue(packet["planning_decision"]["do_not_repeat_generic_static_replay"])
        self.assertEqual("keep_advisory_only_no_go", packet["planning_decision"]["promotion_state"])

        expected_tasks = {
            "B45-POSTQ4-T01-SOL-ROLE-STATIC-FIX",
            "B45-POSTQ4-T02-MP-CRM-STATIC-FIX",
            "B45-POSTQ4-T03-STATIC-DELTA-VERIFY",
            "B45-POSTQ4-T04-LIVE-MODEL-RERUN-PACKET",
            "B45-POSTQ4-T05-LIVE-MODEL-RERUN",
            "B45-POSTQ4-T06-PROMOTION-DECISION",
            "B45-POSTQ4-T07-RUNTIME-BROWSER-PACKET",
        }
        self.assertEqual(expected_tasks, {task["task_id"] for task in packet["task_queue"]})
        self.assertEqual(7, len(packet["task_queue"]))

        approval_required = {
            task["task_id"]: task["status"]
            for task in packet["task_queue"]
            if "approval_required" in task["route"]
        }
        self.assertEqual(
            {
                "B45-POSTQ4-T05-LIVE-MODEL-RERUN": "blocked_until_exact_owner_approval",
            },
            approval_required,
        )
        self.assertIn("approval_required_not_run", serialized)
        self.assertIn("B45-PCA-M36".lower(), serialized)
        self.assertIn("promotion_requires_live_eval_evidence", serialized)
        self.assertIn("targeted_static_repair_then_delta_verify", serialized)

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for registry in [registry_ru, registry_en]:
            with self.subTest(registry="source_registry"):
                self.assertIn("B45-POST-Q4-NEXT-TASKS", registry)
                self.assertIn("B45-POST-Q4-NEXT-TASKS-A01", registry)
                self.assertIn("docs/superpowers/specs/batch45-post-q4-next-tasks.json", registry)

        for control_plane in [plan, evals, test_plan, track11]:
            with self.subTest(control_plane="compact_pointer"):
                self.assertIn("B45-POST-Q4-NEXT-TASKS-A01", control_plane)

        self.assertIn("| `B45-POST-Q4-NEXT-TASKS` |", track11)
        self.assertEqual("B45-POST-Q4-NEXT-TASKS", lifecycle["task_id"])
        self.assertEqual("batch45_post_q4_next_tasks_planned_with_gaps", lifecycle["closure_level"])

    def test_s5_learning_automation_packet_closes_m23_without_activation(self):
        packet = json.loads(S5_SUMMARY.read_text(encoding="utf-8"))
        self.assertEqual(
            "batch45_professional_code_s5_learning_automation_summary_v1",
            packet["schema_version"],
        )
        self.assertEqual("B45-S5-M23-M14-A01", packet["evidence_id"])
        self.assertEqual("implemented_s5_synthetic_green", packet["status"])
        self.assertEqual(
            "implemented_candidate_only_synthetic_green",
            packet["row_status"]["B45-PCA-M23"],
        )
        self.assertEqual(
            "implemented_full_batch45_closure_after_m23",
            packet["row_status"]["B45-PCA-M14"],
        )
        self.assertEqual("candidate_only", packet["candidate_policy"]["status"])
        self.assertEqual(3, packet["candidate_policy"]["minimum_manual_successful_runs"])
        self.assertTrue(packet["candidate_policy"]["future_activation_handoff_required"])

        for required in [
            "owner_review",
            "rollback_or_disable_path",
            "false_positive_audit",
            "flake_replay",
            "cost_check",
            "no_hidden_telemetry_or_raw_private_chat",
        ]:
            self.assertIn(required, packet["candidate_policy"]["required_review_gates"])

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        self.assertIn("real_project_manual_pilot_not_run", packet["accepted_gaps"])

    def test_m26_agent_behavior_eval_records_live_no_go_without_promotion_claim(self):
        plan = json.dumps(json.loads(M26_PLAN.read_text(encoding="utf-8")), sort_keys=True)
        packet = json.loads(M26_RESULTS.read_text(encoding="utf-8"))

        self.assertEqual("B45-PCA-M26", packet["task_id"])
        self.assertEqual("executed_live_eval_no_go", packet["status"])
        self.assertEqual(
            "no_go_real_behavior_improvement_not_proven_after_live_eval",
            packet["decision"]["state"],
        )
        self.assertEqual(8, packet["local_readiness_checks"]["held_out_task_count"])
        self.assertTrue(packet["local_readiness_checks"]["no_manual_pilot_task_reuse"])
        self.assertEqual(8, packet["baseline_run"]["task_count"])
        self.assertEqual(8, packet["treatment_run"]["task_count"])
        self.assertTrue(packet["approval_boundary"]["live_provider_or_model_called"])
        self.assertFalse(packet["approval_boundary"]["raw_private_trace_captured_in_repo"])
        self.assertEqual(17, packet["provider_cost"]["primary_eval_model_calls"])
        self.assertEqual("no_go", packet["independent_reviewer_judgment"]["decision"])
        self.assertLess(
            packet["quantitative_result"]["treatment_average_local_score"],
            packet["quantitative_result"]["baseline_average_local_score"],
        )
        self.assertEqual(1, packet["quantitative_result"]["timeout_runs"])
        self.assertEqual(-14, packet["quantitative_result"]["advisory_warning_delta"])

        for task in packet["per_task_results"]:
            with self.subTest(task=task["task_id"]):
                self.assertIn(task["task_id"], plan)

        for dimension in [
            "existing_capability_scan",
            "custom_code_avoidance",
            "comment_sufficiency",
            "test_scenario_coverage",
            "unsupported_claims",
            "reviewer_usefulness",
            "privacy_safety",
            "flake_cost_control",
        ]:
            with self.subTest(dimension=dimension):
                self.assertIn(dimension, packet["local_readiness_checks"]["reviewer_rubric_dimensions"])
                self.assertIn(dimension, plan)

        self.assertIn("does not prove real ai-agent behavior improvement", json.dumps(packet, sort_keys=True).lower())

    def test_m27_promotion_decision_keeps_advisory_only_after_no_go(self):
        packet = json.loads(M27_DECISION.read_text(encoding="utf-8"))
        serialized = json.dumps(packet, sort_keys=True).lower()

        self.assertEqual("B45-PCA-M27", packet["task_id"])
        self.assertEqual("implemented_promotion_no_go_keep_advisory_only", packet["status"])
        self.assertEqual(
            "keep_advisory_only_no_go_for_blocker_or_ci",
            packet["decision"]["state"],
        )
        self.assertEqual(
            "local_non_blocking_post_tool_use_advisory",
            packet["decision"]["promoted_surface"],
        )
        self.assertFalse(packet["decision"]["stronger_advisory_promoted"])
        self.assertFalse(packet["decision"]["ci_wiring_promoted"])
        self.assertFalse(packet["decision"]["blocker_enforcement_promoted"])
        self.assertFalse(packet["decision"]["real_ai_agent_behavior_improvement_claimed"])
        self.assertEqual("keep_advisory_only", packet["future_reconsideration_gate"]["current_recommendation"])

        evidence_ids = {item["task_id"] for item in packet["evidence_used"]}
        for required in [
            "B45-PCA-M24-A01",
            "B45-PCA-M24-TUNING-A02",
            "B45-PCA-M25",
            "B45-PCA-M26",
        ]:
            with self.subTest(required=required):
                self.assertIn(required, evidence_ids)

        for action, performed in packet["approval_boundary"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for expected in [
            "no_go",
            "baseline average 4.22",
            "treatment average 3.88",
            "warnings 29 -> 15",
            "b45_comment_advisory_disabled=1",
            "does not approve ci workflow creation or blocker enforcement",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, serialized)

    def test_m33_real_project_refactor_comparison_is_fixture_local_and_bounded(self):
        packet = json.loads(M33_COMPARISON.read_text(encoding="utf-8"))
        serialized = json.dumps(packet, sort_keys=True).lower()

        self.assertEqual("batch45_real_project_refactor_comparison_v1", packet["schema_version"])
        self.assertEqual("B45-PCA-M33", packet["task_id"])
        self.assertEqual("B45-PCA-M33-A01", packet["evidence_id"])
        self.assertEqual("synthetic_green_fixture_local_with_accepted_gaps", packet["closure_level"])
        self.assertEqual(2, packet["scenario_count"])

        for artifact in packet["source_artifacts"]:
            with self.subTest(artifact=artifact):
                self.assertTrue(ROOT.joinpath(artifact).exists())

        scenarios = {scenario["scenario_id"]: scenario for scenario in packet["scenarios"]}
        self.assertEqual({"SOL-AGENT-ORCH-01", "MP-CRM-CHAT-OPEN-01"}, set(scenarios))

        sol_arms = {arm["arm_id"]: arm for arm in scenarios["SOL-AGENT-ORCH-01"]["arms"]}
        self.assertEqual("none", sol_arms["checklist-guided"]["code_change"])
        self.assertEqual("none", sol_arms["advisory-guided"]["code_change"])
        self.assertIn("churn prevention", scenarios["SOL-AGENT-ORCH-01"]["comparison_result"])

        mp_arms = {arm["arm_id"]: arm for arm in scenarios["MP-CRM-CHAT-OPEN-01"]["arms"]}
        self.assertEqual(2, mp_arms["original"]["comment_warning_count"])
        self.assertEqual(1, mp_arms["checklist-guided"]["comment_warning_count"])
        self.assertEqual(0, mp_arms["advisory-guided"]["comment_warning_count"])
        self.assertEqual(9, mp_arms["checklist-guided"]["diff_added_lines"])
        self.assertEqual(4, mp_arms["checklist-guided"]["diff_deleted_lines"])
        self.assertEqual(2, mp_arms["advisory-guided"]["diff_added_lines"])
        self.assertEqual([], mp_arms["checklist-guided"]["new_dependencies"])
        self.assertEqual([], mp_arms["advisory-guided"]["new_dependencies"])

        for action, performed in packet["approval_boundary"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for expected in [
            "fixture-local",
            "does not mutate sol 0.6 or mypartners",
            "target_behavior",
            "static_refactor_comparison_proves_real_ai_agent_behavior_improvement",
            "mp-crm-chat-open-01 advisory-guided",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, serialized)

    def test_m34_real_project_scorecard_keeps_promotion_blocked(self):
        packet = json.loads(M34_SCORECARD.read_text(encoding="utf-8"))
        serialized = json.dumps(packet, sort_keys=True).lower()

        self.assertEqual("batch45_real_project_scorecard_v1", packet["schema_version"])
        self.assertEqual("B45-PCA-M34", packet["task_id"])
        self.assertEqual("B45-PCA-M34-A01", packet["evidence_id"])
        self.assertEqual(
            "synthetic_green_scorecard_with_promotion_blocked",
            packet["closure_level"],
        )
        self.assertEqual(2, packet["scenario_count"])
        self.assertEqual(
            "blocked_static_fixture_only",
            packet["score_summary"]["promotion_state"],
        )

        for artifact in packet["input_sources"]:
            with self.subTest(artifact=artifact):
                self.assertTrue(ROOT.joinpath(artifact).exists())
        self.assertTrue(ROOT.joinpath(packet["reviewer_notes"]).exists())

        expected_dimensions = [
            "existing_capability_reuse",
            "custom_code_reduction",
            "dependency_avoidance",
            "comment_sufficiency",
            "tests",
            "unsupported_claims",
            "privacy_safety",
            "reviewer_usefulness",
            "runtime_gap",
            "flake_cost",
        ]
        self.assertEqual(expected_dimensions, packet["rubric"]["dimension_order"])
        self.assertTrue(packet["rubric"]["aggregate_score_is_not_promotion_gate"])
        self.assertTrue(packet["rubric"]["critical_blockers_override_average"])

        outcomes = {outcome["selected_outcome"]: outcome for outcome in packet["scored_outcomes"]}
        self.assertEqual(6.2, outcomes["no-code checklist/advisory"]["average_score"])
        self.assertEqual(6.8, outcomes["checklist-guided"]["average_score"])
        self.assertEqual(7.4, outcomes["advisory-guided"]["average_score"])
        self.assertEqual(
            "best_low_churn_static_arm_but_not_promotable",
            outcomes["advisory-guided"]["promotion_result"],
        )
        self.assertEqual(
            "blocked_until_characterization_or_runtime_evidence",
            outcomes["checklist-guided"]["promotion_result"],
        )

        for blocker in [
            "runtime_gap",
            "tests_gap",
            "type_script_advisory_gap_for_SOL",
            "owner_or_reviewer_weight_judgment_pending",
            "real_ai_agent_behavior_improvement_unproven",
        ]:
            with self.subTest(blocker=blocker):
                self.assertIn(blocker, packet["calibration_findings"]["critical_blockers"])

        self.assertEqual(
            "no_go_for_promotion_keep_fixture_local_static_only",
            packet["promotion_recommendation"]["state"],
        )
        self.assertEqual("B45-PCA-M35", packet["promotion_recommendation"]["next_task"])

        for action, performed in packet["approval_boundary"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for expected in [
            "critical_blockers_override_average",
            "mp-crm-chat-open-01 advisory-guided",
            "mp-crm-chat-open-01 checklist-guided",
            "sol-agent-orch-01",
            "target_behavior",
            "static_scorecard_proves_real_ai_agent_behavior_improvement",
            "m34_approves_ci_or_blocker_promotion",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, serialized)

    def test_m35_real_project_decision_packet_rejects_promotion_without_runtime_proof(self):
        packet = json.loads(M35_DECISION.read_text(encoding="utf-8"))
        serialized = json.dumps(packet, sort_keys=True).lower()

        self.assertEqual("batch45_real_project_decision_packet_v1", packet["schema_version"])
        self.assertEqual("B45-PCA-M35", packet["task_id"])
        self.assertEqual("B45-PCA-M35-A01", packet["evidence_id"])
        self.assertEqual("docs_contract_ready_decision_no_go", packet["closure_level"])
        self.assertEqual(
            "keep_advisory_only_no_go_for_treatment_v2_promotion",
            packet["decision"]["state"],
        )
        self.assertTrue(packet["decision"]["keep_advisory_only"])
        self.assertEqual(
            "allowed_as_source_only_future_design_not_implementation",
            packet["decision"]["design_smaller_treatment_v2"],
        )
        self.assertEqual(
            "approval_required_not_requested_or_executed",
            packet["decision"]["request_disposable_runtime_browser_pilot"],
        )
        self.assertFalse(packet["decision"]["reject_further_promotion_permanently"])

        evidence_ids = {item["task_id"] for item in packet["evidence_used"]}
        for required in [
            "B45-PCA-M27",
            "B45-PCA-M28-A01",
            "B45-PCA-M29-A01",
            "B45-PCA-M30-A01",
            "B45-PCA-M31-A01_A02",
            "B45-PCA-M32-A01_A02",
            "B45-PCA-M33-A01",
            "B45-PCA-M34-A01",
        ]:
            with self.subTest(required=required):
                self.assertIn(required, evidence_ids)

        for item in packet["evidence_used"]:
            with self.subTest(source=item["source"]):
                self.assertTrue(ROOT.joinpath(item["source"]).exists())

        self.assertEqual("rejected", packet["decision_matrix"]["promote_ci_or_blocker"]["decision"])
        self.assertEqual(
            "rejected",
            packet["decision_matrix"]["claim_real_ai_agent_behavior_improvement"]["decision"],
        )
        self.assertEqual(
            "approval_required",
            packet["decision_matrix"]["request_disposable_runtime_browser_pilot"]["decision"],
        )
        self.assertEqual("B45-PCA-M36", packet["next_approval_boundary"]["next_task"])
        self.assertEqual(
            "optional_approval_required_not_executed",
            packet["next_approval_boundary"]["status"],
        )

        for action, performed in packet["approval_boundary"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for expected in [
            "no-go decision only",
            "do not promote ci workflow creation or blocker enforcement",
            "m35_approves_target_apply",
            "m35_approves_disposable_runtime_browser_pilot",
            "m35_approves_ci_or_blocker_promotion",
            "m35_proves_real_ai_agent_behavior_improvement",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, serialized)


if __name__ == "__main__":
    unittest.main()
