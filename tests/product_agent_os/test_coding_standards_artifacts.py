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
POST_Q4_T01_T04_SUMMARY = DOCS / "superpowers" / "specs" / "batch45-postq4-t01-t04-execution-summary.json"
POST_Q4_T04_APPROVAL = DOCS / "superpowers" / "specs" / "batch45-postq4-live-model-rerun-approval-packet.json"
POST_Q4_T05_RESULTS = DOCS / "superpowers" / "specs" / "batch45-postq4-t05-live-model-rerun-results.json"
POST_Q4_T05B_APPROVAL = DOCS / "superpowers" / "specs" / "batch45-postq4-t05b-rerun-approval-packet.json"
POST_Q4_T06_DECISION = DOCS / "superpowers" / "specs" / "batch45-postq4-t06-promotion-decision.json"
POST_Q4_T08_ARCHITECTURE = DOCS / "superpowers" / "specs" / "batch45-postq4-architecture-next-actions.json"
POST_Q4_T10_HARNESS = DOCS / "superpowers" / "specs" / "batch45-postq4-t10-live-eval-harness-redesign-packet.json"
POST_Q4_T11_DESIGN = DOCS / "superpowers" / "specs" / "batch45-postq4-t11-treatment-v3-source-design.json"
POST_Q4_T12_APPROVAL = (
    DOCS
    / "superpowers"
    / "specs"
    / "batch45-postq4-t12-paired-live-model-rerun-exact-approval-packet.json"
)
POST_Q4_T12_RESULTS = DOCS / "superpowers" / "specs" / "batch45-postq4-t12-paired-live-model-rerun-results.json"
POST_Q4_T13_HARDENING = (
    DOCS
    / "superpowers"
    / "specs"
    / "batch45-postq4-t13-strict-output-schema-and-harness-hardening.json"
)
POST_Q4_T14_APPROVAL = (
    DOCS
    / "superpowers"
    / "specs"
    / "batch45-postq4-t14-strict-rerun-approval-packet.json"
)
POST_Q4_T14_RESULTS = DOCS / "superpowers" / "specs" / "batch45-postq4-t14-strict-rerun-results.json"
POST_Q4_T15_DECISION = DOCS / "superpowers" / "specs" / "batch45-postq4-t15-model-change-decision-packet.json"
POST_Q4_T16_T22_TASK_GROUP = (
    DOCS
    / "superpowers"
    / "specs"
    / "batch45-postq4-t16-t22-promotion-grade-eval-task-group.json"
)
POST_Q4_T17_FROZEN_HELDOUT_CORPUS = (
    DOCS
    / "superpowers"
    / "specs"
    / "batch45-postq4-t17-frozen-heldout-corpus.json"
)
POST_Q4_T18_EVAL_DESIGN = (
    DOCS
    / "superpowers"
    / "specs"
    / "batch45-postq4-t18-promotion-grade-eval-design.json"
)
POST_Q4_T19_POLICY = (
    DOCS
    / "superpowers"
    / "specs"
    / "batch45-postq4-t19-cost-timeout-retention-policy.json"
)
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.model_output import (  # noqa: E402
    AGGREGATE_REQUIRED_FIELDS,
    LIVE_RUN_REQUIRED_FIELDS,
    LIVE_RUN_STATUS_VALUES,
    PAIR_REQUIRED_FIELDS,
    validate_paired_live_eval_result,
)
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
            "they do not prove that ai agents now write enterprise-quality code in real projects",
            "m26 records a live behavior-eval no-go",
            "m27 keeps the m25 advisory local/non-blocking",
            "m35 keeps s7 fixture-local/source-only",
            "m37 records local hook/validator hardening plus review remediation docs/control-plane sync only",
            "t17 freezes the metadata-only held-out corpus manifest",
            "t18 defines the same-model promotion-grade eval design and strict schema",
            "t19 defines the cost/timeout/raw-temp-only retention policy",
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
            "B45-POSTQ4-T05B-RERUN-PACKET-REVISION",
            "B45-POSTQ4-T06-PROMOTION-DECISION",
            "B45-POSTQ4-T07-RUNTIME-BROWSER-PACKET",
            "B45-POSTQ4-T08-ARCHITECTURE-NEXT-ACTIONS",
            "B45-POSTQ4-T09-CLOSURE-ADVISORY-ONLY",
            "B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET",
            "B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN",
            "B45-POSTQ4-T12-PAIRED-LIVE-MODEL-RERUN-EXACT-APPROVAL-PACKET",
            "B45-POSTQ4-T13-STRICT_OUTPUT_SCHEMA_AND_HARNESS_HARDENING",
            "B45-POSTQ4-T14-STRICT-RERUN-APPROVAL-PACKET",
            "B45-POSTQ4-T15-DECISION-PACKET-MODEL-CHANGE-INTERPRETATION",
            "B45-POSTQ4-T16-T22-PROMOTION-GRADE-EVAL-TASK-GROUP",
        }
        self.assertEqual(expected_tasks, {task["task_id"] for task in packet["task_queue"]})
        self.assertEqual(17, len(packet["task_queue"]))

        approval_required = {
            task["task_id"]: task["status"]
            for task in packet["task_queue"]
            if "approval_required" in task["route"]
        }
        self.assertEqual(
            {
                "B45-POSTQ4-T05-LIVE-MODEL-RERUN": "attempted_approved_live_eval_stopped_on_timeout_no_go",
            },
            approval_required,
        )
        self.assertIn("approval_required_not_run", serialized)
        self.assertIn("B45-PCA-M36".lower(), serialized)
        self.assertIn("promotion_requires_live_eval_evidence", serialized)
        self.assertIn("targeted_static_repair_then_delta_verify", serialized)
        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t01-t04-execution-summary.json",
            packet["execution_update"]["latest_evidence"],
        )
        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-architecture-next-actions.json",
            packet["execution_update"]["latest_t08_architecture_next_actions"],
        )
        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t10-live-eval-harness-redesign-packet.json",
            packet["execution_update"]["latest_t10_harness_redesign"],
        )
        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json",
            packet["execution_update"]["latest_t11_design"],
        )
        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t12-paired-live-model-rerun-exact-approval-packet.json",
            packet["execution_update"]["latest_t12_exact_approval_packet"],
        )
        self.assertEqual(0, packet["execution_update"]["warning_delta"]["post_t03_warning_count"])
        self.assertEqual(-14, packet["execution_update"]["warning_delta"]["delta"])
        self.assertEqual(
            "stopped_on_timeout_inconclusive_no_go",
            packet["execution_update"]["t05_live_eval_result"]["status"],
        )
        self.assertEqual(1, packet["execution_update"]["t05_live_eval_result"]["completed_primary_task_runs"])
        self.assertEqual(1, packet["execution_update"]["t05_live_eval_result"]["timeout_primary_task_runs"])
        self.assertEqual(14, packet["execution_update"]["t05_live_eval_result"]["not_run_due_stop_rule"])
        self.assertIn("B45-POSTQ4-T05-LIVE-MODEL-RERUN", packet["execution_update"]["executed_task_ids"])
        self.assertIn("B45-POSTQ4-T08-ARCHITECTURE-NEXT-ACTIONS", packet["execution_update"]["executed_task_ids"])
        self.assertIn("B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET", packet["execution_update"]["executed_task_ids"])
        self.assertIn("B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN", packet["execution_update"]["executed_task_ids"])
        self.assertIn(
            "B45-POSTQ4-T12-PAIRED-LIVE-MODEL-RERUN-EXACT-APPROVAL-PACKET",
            packet["execution_update"]["executed_task_ids"],
        )
        self.assertIn(
            "B45-POSTQ4-T12-PAIRED-LIVE-MODEL-RERUN",
            packet["execution_update"]["executed_task_ids"],
        )
        self.assertIn(
            "B45-POSTQ4-T15-DECISION-PACKET-MODEL-CHANGE-INTERPRETATION",
            packet["execution_update"]["executed_task_ids"],
        )
        self.assertEqual(
            18,
            packet["execution_update"]["approved_actions_performed"][
                "approved_codex_exec_live_model_task_calls_started"
            ],
        )
        self.assertEqual(
            16,
            packet["execution_update"]["approved_actions_performed"]["approved_t12_codex_exec_primary_calls_started"],
        )
        self.assertEqual(6, packet["execution_update"]["t12_live_eval_result"]["valid_pair_count"])
        self.assertEqual("not_run_due_invalid_pair_count", packet["execution_update"]["t12_live_eval_result"]["reviewer_status"])
        self.assertEqual(
            {
                "B45-POSTQ4-T09-CLOSURE-ADVISORY-ONLY",
                "B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET",
                "B45-POSTQ4-T07-RUNTIME-BROWSER-PACKET",
                "B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN",
                "B45-POSTQ4-T13-STRICT_OUTPUT_SCHEMA_AND_HARNESS_HARDENING",
                "B45-POSTQ4-T14-STRICT-RERUN-APPROVAL-PACKET",
                "B45-POSTQ4-T16-T22-PROMOTION-GRADE-EVAL-TASK-GROUP",
            },
            set(packet["execution_update"]["post_t06_recommended_next_routes"]),
        )

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

    def test_b45_postq4_t01_t04_execution_summary_and_approval_packet_are_bounded(self):
        summary = json.loads(POST_Q4_T01_T04_SUMMARY.read_text(encoding="utf-8"))
        approval = json.loads(POST_Q4_T04_APPROVAL.read_text(encoding="utf-8"))
        t05 = json.loads(POST_Q4_T05_RESULTS.read_text(encoding="utf-8"))
        t05b = json.loads(POST_Q4_T05B_APPROVAL.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
        serialized = (
            json.dumps(summary, sort_keys=True).lower()
            + json.dumps(approval, sort_keys=True).lower()
            + json.dumps(t05, sort_keys=True).lower()
            + json.dumps(t05b, sort_keys=True).lower()
        )
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

        self.assertEqual("batch45_postq4_t01_t04_execution_summary_v1", summary["schema_version"])
        self.assertEqual("B45-POSTQ4-T01-T04", summary["task_id"])
        self.assertEqual("B45-POSTQ4-T01-T04-A01", summary["evidence_id"])
        self.assertEqual("implemented_local_static_delta_and_approval_packet_with_gaps", summary["status"])
        self.assertEqual(11, summary["implemented_tasks"]["B45-POSTQ4-T01-SOL-ROLE-STATIC-FIX"]["warning_count_before"])
        self.assertEqual(0, summary["implemented_tasks"]["B45-POSTQ4-T01-SOL-ROLE-STATIC-FIX"]["warning_count_after"])
        self.assertEqual(3, summary["implemented_tasks"]["B45-POSTQ4-T02-MP-CRM-STATIC-FIX"]["warning_count_before"])
        self.assertEqual(0, summary["implemented_tasks"]["B45-POSTQ4-T02-MP-CRM-STATIC-FIX"]["warning_count_after"])
        self.assertEqual(14, summary["implemented_tasks"]["B45-POSTQ4-T03-STATIC-DELTA-VERIFY"]["q4_baseline_warning_count"])
        self.assertEqual(0, summary["implemented_tasks"]["B45-POSTQ4-T03-STATIC-DELTA-VERIFY"]["post_fix_warning_count"])
        self.assertEqual(-14, summary["implemented_tasks"]["B45-POSTQ4-T03-STATIC-DELTA-VERIFY"]["warning_delta"])
        self.assertEqual(0, summary["implemented_tasks"]["B45-POSTQ4-T03-STATIC-DELTA-VERIFY"]["secret_pattern_matches"])
        self.assertEqual("implemented_approval_packet_only_not_run", summary["implemented_tasks"]["B45-POSTQ4-T04-LIVE-MODEL-RERUN-PACKET"]["status"])
        self.assertEqual(13, summary["implemented_tasks"]["B45-POSTQ4-T03-STATIC-DELTA-VERIFY"]["diff_numstat"]["files_changed"])
        self.assertEqual(15, summary["implemented_tasks"]["B45-POSTQ4-T03-STATIC-DELTA-VERIFY"]["diff_numstat"]["lines_added"])
        self.assertEqual(0, summary["implemented_tasks"]["B45-POSTQ4-T03-STATIC-DELTA-VERIFY"]["diff_numstat"]["lines_deleted"])

        self.assertEqual("batch45_postq4_live_model_rerun_approval_packet_v1", approval["schema_version"])
        self.assertEqual("B45-POSTQ4-T04-LIVE-MODEL-RERUN-PACKET", approval["task_id"])
        self.assertEqual("B45-POSTQ4-T04-A01", approval["evidence_id"])
        self.assertEqual("approval_packet_only_not_run", approval["status"])
        self.assertFalse(approval["current_claim_ceiling"]["promotion_allowed"])
        self.assertFalse(approval["current_claim_ceiling"]["static_warning_delta_can_promote"])
        self.assertEqual("owner_selected_provider_required", approval["approval_required_before_any_run"]["provider"])
        self.assertEqual("owner_fill_required", approval["approval_required_before_any_run"]["max_cost_usd"])
        self.assertEqual(8, len(approval["task_set"]["task_ids"]))
        self.assertEqual("disabled", approval["arms"]["baseline"]["advisory_signal"])
        self.assertIn("M25/comment-sufficiency", approval["arms"]["treatment"]["advisory_signal"])
        self.assertIn("raw private prompts", approval["privacy_boundary"]["retain_forbidden"])
        self.assertIn("provider/model not exactly approved", approval["abort_conditions"])
        self.assertEqual("stopped_on_timeout_inconclusive_no_go", approval["execution_follow_up"]["result_status"])

        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json",
            next_tasks["execution_update"]["latest_t05_evidence"],
        )
        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json",
            next_tasks["execution_update"]["latest_t05b_packet"],
        )
        self.assertEqual(0, next_tasks["execution_update"]["warning_delta"]["unresolved_advisory_warnings"])
        self.assertIn("B45-POSTQ4-T04-LIVE-MODEL-RERUN-PACKET", next_tasks["execution_update"]["executed_task_ids"])
        self.assertIn("B45-POSTQ4-T05-LIVE-MODEL-RERUN", next_tasks["execution_update"]["executed_task_ids"])
        self.assertIn("B45-POSTQ4-T05B-RERUN-PACKET-REVISION", next_tasks["execution_update"]["executed_task_ids"])

        self.assertEqual("batch45_postq4_t05_live_model_rerun_results_v1", t05["schema_version"])
        self.assertEqual("B45-POSTQ4-T05-LIVE-MODEL-RERUN", t05["task_id"])
        self.assertEqual("B45-POSTQ4-T05-A01", t05["evidence_id"])
        self.assertEqual("stopped_on_timeout_inconclusive_no_go", t05["status"])
        self.assertEqual(16, t05["execution_summary"]["planned_primary_task_runs"])
        self.assertEqual(2, t05["execution_summary"]["approved_primary_task_model_calls_started"])
        self.assertEqual(1, t05["execution_summary"]["completed_primary_task_runs"])
        self.assertEqual(1, t05["execution_summary"]["timeout_primary_task_runs"])
        self.assertEqual(14, t05["execution_summary"]["not_run_due_stop_rule"])
        self.assertEqual(0, t05["execution_summary"]["reviewer_calls_started"])
        self.assertEqual("no_go_stopped_on_timeout", t05["decision"]["state"])
        self.assertFalse(t05["decision"]["promotion_allowed"])
        self.assertFalse(t05["decision"]["m26_reversed"])
        self.assertEqual("not_comparable_due_early_timeout", t05["comparison_to_previous_m26"]["delta_assessment"])
        self.assertFalse(t05["cost_and_retention"]["raw_outputs_in_repo"])
        self.assertTrue(t05["cost_and_retention"]["raw_outputs_retained_in_temp_only"])

        self.assertEqual("batch45_postq4_t05b_rerun_approval_packet_v1", t05b["schema_version"])
        self.assertEqual("B45-POSTQ4-T05B-RERUN-PACKET-REVISION", t05b["task_id"])
        self.assertEqual("B45-POSTQ4-T05B-A01", t05b["evidence_id"])
        self.assertEqual("approval_packet_only_not_run", t05b["status"])
        self.assertEqual("stopped_on_timeout_inconclusive_no_go", t05b["basis"]["t05_result_status"])
        self.assertEqual(0, t05b["required_exact_approval_before_any_run"]["run_count"]["setup_or_smoke_model_calls"])
        self.assertTrue(t05b["watchdog_contract"]["process_tree_kill_on_timeout"])
        self.assertFalse(t05b["retention_policy"]["raw_outputs_in_repo_allowed"])
        self.assertFalse(t05b["promotion_threshold"]["static_warning_delta_can_promote"])
        self.assertIn("No new exact owner approval for T05B.", t05b["abort_conditions"])

        for packet in [summary, approval, t05, t05b]:
            for action, performed in packet["no_unapproved_actions"].items():
                with self.subTest(action=action):
                    self.assertFalse(performed)

        for expected in [
            "real_ai_agent_behavior_improvement",
            "target_runtime_behavior",
            "provider_or_live_api_behavior",
            "M26_no_go_reversed".lower(),
            "approval_required",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected.lower(), serialized)

        for registry in [registry_ru, registry_en]:
            with self.subTest(registry="source_registry"):
                self.assertIn("B45-POSTQ4-T01-T04", registry)
                self.assertIn("B45-POSTQ4-T01-T04-A01", registry)
                self.assertIn("docs/superpowers/specs/batch45-postq4-t01-t04-execution-summary.json", registry)
                self.assertIn("B45-POSTQ4-T04-A01", registry)
                self.assertIn("docs/superpowers/specs/batch45-postq4-live-model-rerun-approval-packet.json", registry)
                self.assertIn("B45-POSTQ4-T05-A01", registry)
                self.assertIn("docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json", registry)
                self.assertIn("B45-POSTQ4-T05B-A01", registry)
                self.assertIn("docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json", registry)

        for control_plane in [plan, evals, test_plan, track11]:
            with self.subTest(control_plane="compact_pointer"):
                self.assertIn("B45-POSTQ4-T01-T04-A01", control_plane)
                self.assertIn("B45-POSTQ4-T05-A01", control_plane)
                self.assertIn("B45-POSTQ4-T05B-A01", control_plane)

        self.assertIn("| `B45-POSTQ4-T05` |", track11)
        self.assertIn("| `B45-POSTQ4-T05B` |", track11)

    def test_b45_postq4_t06_promotion_decision_keeps_advisory_only(self):
        packet = json.loads(POST_Q4_T06_DECISION.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
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

        self.assertEqual("batch45_postq4_t06_promotion_decision_v1", packet["schema_version"])
        self.assertEqual("B45-POSTQ4-T06-PROMOTION-DECISION", packet["task_id"])
        self.assertEqual("B45-POSTQ4-T06-A01", packet["evidence_id"])
        self.assertEqual("implemented_promotion_no_go_keep_advisory_only", packet["status"])
        self.assertEqual(
            "keep_advisory_only_no_go_after_static_delta_and_t05_timeout",
            packet["decision"]["state"],
        )
        self.assertTrue(packet["decision"]["keep_m25_local_non_blocking_advisory"])
        self.assertFalse(packet["decision"]["promote_stronger_advisory"])
        self.assertFalse(packet["decision"]["promote_ci_workflow"])
        self.assertFalse(packet["decision"]["promote_blocker_enforcement"])
        self.assertFalse(packet["decision"]["promote_active_automation"])
        self.assertFalse(packet["decision"]["claim_real_ai_agent_behavior_improvement"])
        self.assertFalse(packet["decision"]["claim_runtime_browser_or_target_readiness"])

        self.assertEqual("cannot_promote", packet["decision_matrix"]["static_warning_delta"]["promotion_effect"])
        self.assertEqual("blocks_promotion", packet["decision_matrix"]["live_behavior_evidence"]["promotion_effect"])
        self.assertEqual("optional_new_exact_approval_required", packet["decision_matrix"]["t05b_rerun_option"]["decision"])
        self.assertEqual(
            "forbidden_without_new_approval_and_evidence",
            packet["decision_matrix"]["ci_blocker_automation"]["promotion_effect"],
        )
        self.assertIn("no_comparable_t05_baseline_treatment_result", {gap["gap"] for gap in packet["accepted_gaps_for_t06_only"]})
        self.assertIn("B45-POSTQ4-T07-RUNTIME-BROWSER-PACKET", {route["task_id"] for route in packet["next_routes"]})

        for review in packet["sidecar_agent_reviews"]:
            with self.subTest(report=review["report"]):
                self.assertEqual("completed", review["status"])
                self.assertTrue(ROOT.joinpath(review["report"]).exists())

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for expected in [
            "real_ai_agent_behavior_improvement",
            "ci_workflow_readiness",
            "blocker_enforcement_readiness",
            "M26_no_go_reversed".lower(),
            "M35_no_go_reversed".lower(),
            "static warning delta is useful maintenance evidence, but it is not behavior proof",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected.lower(), serialized)

        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t06-promotion-decision.json",
            next_tasks["execution_update"]["latest_t06_decision"],
        )
        self.assertIn("B45-POSTQ4-T06-PROMOTION-DECISION", next_tasks["execution_update"]["executed_task_ids"])
        self.assertEqual(
            "implemented_promotion_no_go_keep_advisory_only",
            next_tasks["execution_update"]["status_by_task"]["B45-POSTQ4-T06-PROMOTION-DECISION"],
        )

        for registry in [registry_ru, registry_en]:
            with self.subTest(registry="source_registry"):
                self.assertIn("B45-POSTQ4-T06-PROMOTION-DECISION", registry)
                self.assertIn("B45-POSTQ4-T06-A01", registry)
                self.assertIn("docs/superpowers/specs/batch45-postq4-t06-promotion-decision.json", registry)

        for control_plane in [plan, evals, test_plan, track11]:
            with self.subTest(control_plane="compact_pointer"):
                self.assertIn("B45-POSTQ4-T06-A01", control_plane)

        self.assertIn("| `B45-POSTQ4-T06` |", track11)

    def test_b45_postq4_t08_architecture_next_actions_routes_without_promotion(self):
        packet = json.loads(POST_Q4_T08_ARCHITECTURE.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
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

        self.assertEqual("batch45_postq4_architecture_next_actions_v1", packet["schema_version"])
        self.assertEqual("B45-POSTQ4-T08-ARCHITECTURE-NEXT-ACTIONS", packet["task_id"])
        self.assertEqual("B45-POSTQ4-T08-A01", packet["evidence_id"])
        self.assertEqual("implemented_source_owned_architecture_next_actions_after_t06", packet["status"])
        self.assertEqual(
            "advisory_only_no_go_with_local_static_quality_improvement",
            packet["current_state_summary"]["claim_ceiling"],
        )
        self.assertEqual(
            {
                "advisory_layer",
                "eval_layer",
                "runtime_layer",
                "control_plane_layer",
            },
            set(packet["technical_architecture_analysis"]),
        )
        self.assertEqual(
            {
                "B45-POSTQ4-AD-01",
                "B45-POSTQ4-AD-02",
                "B45-POSTQ4-AD-03",
            },
            {decision["decision_id"] for decision in packet["architecture_decisions"]},
        )
        self.assertEqual(
            [
                "B45-POSTQ4-T09-CLOSURE-ADVISORY-ONLY",
                "B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET",
                "B45-POSTQ4-T07-RUNTIME-BROWSER-PACKET",
                "B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN",
            ],
            [task["task_id"] for task in packet["recommended_next_tasks"]],
        )
        self.assertEqual("approval_packet_only", packet["recommended_next_tasks"][1]["route"])
        self.assertEqual("source_only_design", packet["recommended_next_tasks"][3]["route"])

        for unsupported in [
            "ci_workflow_readiness",
            "M26_no_go_reversed".lower(),
            "T05_timeout_reversed".lower(),
        ]:
            self.assertIn(unsupported.lower(), serialized)

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-architecture-next-actions.json",
            next_tasks["execution_update"]["latest_t08_architecture_next_actions"],
        )
        self.assertIn("B45-POSTQ4-T08-ARCHITECTURE-NEXT-ACTIONS", next_tasks["execution_update"]["executed_task_ids"])
        self.assertEqual(
            "implemented_source_owned_architecture_next_actions_after_t06",
            next_tasks["execution_update"]["status_by_task"]["B45-POSTQ4-T08-ARCHITECTURE-NEXT-ACTIONS"],
        )

        for registry in [registry_ru, registry_en]:
            with self.subTest(registry="source_registry"):
                self.assertIn("B45-POSTQ4-T08-ARCHITECTURE-NEXT-ACTIONS", registry)
                self.assertIn("B45-POSTQ4-T08-A01", registry)
                self.assertIn("docs/superpowers/specs/batch45-postq4-architecture-next-actions.json", registry)

        for control_plane in [plan, evals, test_plan, track11]:
            with self.subTest(control_plane="compact_pointer"):
                self.assertIn("B45-POSTQ4-T08-A01", control_plane)

        self.assertIn("| `B45-POSTQ4-T08` |", track11)

    def test_b45_postq4_t10_live_eval_harness_redesign_is_approval_packet_only(self):
        packet = json.loads(POST_Q4_T10_HARNESS.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
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

        self.assertEqual("batch45_postq4_t10_live_eval_harness_redesign_packet_v1", packet["schema_version"])
        self.assertEqual("B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET", packet["task_id"])
        self.assertEqual("B45-POSTQ4-T10-A01", packet["evidence_id"])
        self.assertEqual("implemented_approval_packet_only_not_run", packet["status"])
        self.assertEqual("approval_packet_only", packet["route"])
        self.assertEqual("paired_by_task", packet["redesign_contract"]["default_run_order"])
        self.assertEqual(0, packet["redesign_contract"]["setup_or_smoke_model_calls"])
        self.assertEqual(
            {
                "strict_stop_on_first_timeout",
                "paired_continue_with_invalid_pair_quarantine",
                "single_task_timeout_diagnostic",
            },
            {option["id"] for option in packet["timeout_policy_options"]},
        )
        self.assertIn("timeout", packet["result_schema_contract"]["run_status_values"])
        self.assertIn("no_op", packet["result_schema_contract"]["run_status_values"])
        self.assertIn("baseline_timeout", packet["result_schema_contract"]["pair_invalid_reasons"])
        self.assertEqual("after_primary_pairs_complete_and_schema_valid", packet["reviewer_route"]["default_timing"])
        self.assertTrue(packet["reviewer_route"]["reviewer_no_go_blocks_promotion"])
        self.assertFalse(packet["promotion_gate_candidate"]["static_warning_delta_can_promote"])
        self.assertTrue(packet["promotion_gate_candidate"]["m26_reversed_only_if_all_thresholds_met"])
        self.assertFalse(packet["promotion_gate_candidate"]["m35_reversed_only_if_runtime_or_owner_decision_packet_later_allows"])
        self.assertFalse(packet["privacy_and_retention"]["raw_outputs_in_repo_allowed"])
        self.assertEqual("owner_fill_required", packet["required_exact_approval_packet_fields"]["provider_surface"])
        self.assertEqual("owner_fill_required", packet["required_exact_approval_packet_fields"]["model"])
        self.assertEqual(8, packet["required_exact_approval_packet_fields"]["run_count"]["baseline"])
        self.assertEqual(8, packet["required_exact_approval_packet_fields"]["run_count"]["treatment"])
        self.assertEqual(1, packet["required_exact_approval_packet_fields"]["run_count"]["reviewer"])
        self.assertEqual(0, packet["required_exact_approval_packet_fields"]["run_count"]["setup_or_smoke_model_calls"])

        self.assertEqual("approval_packet_ready_for_owner_review_not_run", packet["decision"]["state"])
        for flag in [
            "m26_reversed",
            "m35_reversed",
            "t05_timeout_reversed",
            "t11_behavior_proven",
            "promotion_allowed",
            "live_model_rerun_allowed_without_new_approval",
            "runtime_browser_or_target_claim_allowed",
        ]:
            with self.subTest(flag=flag):
                self.assertFalse(packet["decision"][flag])

        self.assertEqual(5, len(packet["sidecar_agent_reviews"]))
        for review in packet["sidecar_agent_reviews"]:
            with self.subTest(report=review["report"]):
                self.assertEqual("completed", review["status"])
                self.assertTrue(ROOT.joinpath(review["report"]).exists())

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for expected in [
            "M26_no_go_reversed".lower(),
            "T05_timeout_reversed".lower(),
            "provider_or_live_api_behavior",
            "runtime_browser_readiness",
            "ci_workflow_readiness",
            "raw outputs only in temp",
        ]:
            self.assertIn(expected.lower(), serialized)

        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t10-live-eval-harness-redesign-packet.json",
            next_tasks["execution_update"]["latest_t10_harness_redesign"],
        )
        self.assertIn("B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET", next_tasks["execution_update"]["executed_task_ids"])
        self.assertEqual(
            "implemented_approval_packet_only_not_run",
            next_tasks["execution_update"]["status_by_task"]["B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET"],
        )

        for registry in [registry_ru, registry_en]:
            with self.subTest(registry="source_registry"):
                self.assertIn("B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET", registry)
                self.assertIn("B45-POSTQ4-T10-A01", registry)
                self.assertIn("docs/superpowers/specs/batch45-postq4-t10-live-eval-harness-redesign-packet.json", registry)

        for control_plane in [plan, evals, test_plan, track11]:
            with self.subTest(control_plane="compact_pointer"):
                self.assertIn("B45-POSTQ4-T10-A01", control_plane)

        self.assertIn("| `B45-POSTQ4-T10` |", track11)

    def test_b45_postq4_t11_treatment_v3_source_design_is_source_only(self):
        packet = json.loads(POST_Q4_T11_DESIGN.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
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

        self.assertEqual("batch45_postq4_t11_treatment_v3_source_design_v1", packet["schema_version"])
        self.assertEqual("B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN", packet["task_id"])
        self.assertEqual("B45-POSTQ4-T11-A01", packet["evidence_id"])
        self.assertEqual("implemented_source_only_treatment_v3_design_not_run", packet["status"])
        self.assertEqual("source_only_design", packet["route"])
        self.assertEqual(
            "source_design_ready_for_review_only_no_behavior_or_runtime_claim",
            packet["decision"]["state"],
        )
        for flag in [
            "m26_reversed",
            "m35_reversed",
            "t05_timeout_reversed",
            "promotion_allowed",
            "ci_blocker_automation_allowed",
            "live_model_rerun_allowed_without_new_approval",
            "runtime_browser_or_target_claim_allowed",
        ]:
            with self.subTest(flag=flag):
                self.assertFalse(packet["decision"][flag])

        self.assertTrue(packet["future_eval_update_required"]["required"])
        self.assertEqual(
            "B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET before any approved rerun",
            packet["future_eval_update_required"]["recommended_route"],
        )
        self.assertFalse(
            packet["future_eval_update_required"]["promotion_threshold_candidate"][
                "static_warning_delta_can_promote"
            ]
        )
        self.assertEqual(
            {
                "enterprise_leverage_check",
                "existing_capability_scan",
                "one_line_candidate",
                "negative_dependency_rule",
                "deep_module_check",
                "legacy_seam_check",
                "comment_policy",
                "cleverness_budget",
            },
            {item["standard"] for item in packet["standards_to_behaviors_map"]},
        )
        self.assertGreaterEqual(len(packet["negative_examples"]), 5)
        self.assertEqual(5, len(packet["sidecar_agent_reviews"]))
        for review in packet["sidecar_agent_reviews"]:
            with self.subTest(report=review["report"]):
                self.assertEqual("completed", review["status"])
                self.assertTrue(ROOT.joinpath(review["report"]).exists())

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for unsupported in [
            "treatment_v3_behavior_proven",
            "M26_no_go_reversed".lower(),
            "M35_no_go_reversed".lower(),
            "runtime_browser_readiness",
            "ci_workflow_readiness",
        ]:
            self.assertIn(unsupported.lower(), serialized)

        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json",
            next_tasks["execution_update"]["latest_t11_design"],
        )
        self.assertIn("B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN", next_tasks["execution_update"]["executed_task_ids"])
        self.assertEqual(
            "implemented_source_only_treatment_v3_design_not_run",
            next_tasks["execution_update"]["status_by_task"]["B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN"],
        )

        for registry in [registry_ru, registry_en]:
            with self.subTest(registry="source_registry"):
                self.assertIn("B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN", registry)
                self.assertIn("B45-POSTQ4-T11-A01", registry)
                self.assertIn("docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json", registry)

        for control_plane in [plan, evals, test_plan, track11]:
            with self.subTest(control_plane="compact_pointer"):
                self.assertIn("B45-POSTQ4-T11-A01", control_plane)

        self.assertIn("| `B45-POSTQ4-T11` |", track11)

    def test_b45_postq4_t12_exact_paired_rerun_packet_is_not_owner_confirmation(self):
        packet = json.loads(POST_Q4_T12_APPROVAL.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
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

        self.assertEqual("batch45_postq4_t12_paired_live_model_rerun_exact_approval_packet_v1", packet["schema_version"])
        self.assertEqual("B45-POSTQ4-T12-PAIRED-LIVE-MODEL-RERUN-EXACT-APPROVAL-PACKET", packet["task_id"])
        self.assertEqual("B45-POSTQ4-T12-A01", packet["evidence_id"])
        self.assertEqual("exact_approval_packet_draft_not_owner_confirmed_not_run", packet["status"])
        self.assertEqual("exact_approval_packet_only", packet["route"])
        self.assertFalse(packet["approval_state"]["owner_confirmed"])
        self.assertFalse(packet["approval_state"]["run_authorized_by_this_artifact"])
        self.assertTrue(packet["approval_state"]["requires_next_user_message"])
        self.assertEqual("Codex CLI/OpenAI via codex exec", packet["approved_if_owner_confirms_exact_text"]["provider_surface"])
        self.assertEqual("gpt-5.3-codex-spark", packet["approved_if_owner_confirms_exact_text"]["model"])
        self.assertEqual(8, packet["approved_if_owner_confirms_exact_text"]["primary_model_call_cap"]["baseline"])
        self.assertEqual(8, packet["approved_if_owner_confirms_exact_text"]["primary_model_call_cap"]["treatment"])
        self.assertEqual(1, packet["approved_if_owner_confirms_exact_text"]["reviewer_call_cap"])
        self.assertEqual(0, packet["approved_if_owner_confirms_exact_text"]["setup_or_smoke_model_calls"])
        self.assertEqual("paired_by_task", packet["run_design"]["run_order"])
        self.assertEqual("paired_continue_with_invalid_pair_quarantine", packet["run_design"]["timeout_policy"])
        self.assertTrue(packet["run_design"]["timeout_effect"]["continue_remaining_pairs"])
        self.assertFalse(packet["run_design"]["timeout_effect"]["promotion_possible_after_any_timeout"])
        self.assertEqual(8, packet["promotion_gate"]["minimum_valid_pairs"])
        self.assertFalse(packet["promotion_gate"]["static_warning_delta_can_promote"])
        self.assertFalse(packet["privacy_and_retention"]["raw_outputs_in_repo_allowed"])
        self.assertTrue(packet["privacy_and_retention"]["raw_outputs_temp_only"])
        self.assertEqual(
            "1DD5CE891B8674B4FC1BA4BF96235A554EF4169EA55F08B5B0FEED300EF102B8",
            packet["source_freeze"]["t10_harness_contract"]["sha256"],
        )
        self.assertEqual(
            "FF17C9580B0A823D1F0BA4CEEE393231E13F6502819C122148376F87367E5787",
            packet["source_freeze"]["t11_treatment_v3_source_design"]["sha256"],
        )

        confirmation_text = "\n".join(packet["exact_approval_text_for_owner_confirmation"])
        for expected in [
            "provider/surface: Codex CLI/OpenAI via codex exec",
            "model: gpt-5.3-codex-spark",
            "run count: max 8 baseline + 8 treatment paired primary calls + max 1 reviewer",
            "timeout policy: paired_continue_with_invalid_pair_quarantine",
            "retention: raw outputs only in temp; repo stores sanitized rollup only",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, confirmation_text)

        self.assertEqual("exact_approval_packet_ready_for_owner_confirmation_not_run", packet["decision"]["state"])
        for flag in [
            "m26_reversed",
            "m35_reversed",
            "t05_timeout_reversed",
            "t11_behavior_proven",
            "promotion_allowed",
            "live_model_rerun_allowed_without_next_owner_confirmation",
            "runtime_browser_or_target_claim_allowed",
        ]:
            with self.subTest(flag=flag):
                self.assertFalse(packet["decision"][flag])

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for expected in [
            "provider_or_live_api_behavior_from_this_packet",
            "M26_no_go_reversed".lower(),
            "owner has not restated the exact approval text",
        ]:
            self.assertIn(expected.lower(), serialized)

        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t12-paired-live-model-rerun-exact-approval-packet.json",
            next_tasks["execution_update"]["latest_t12_exact_approval_packet"],
        )
        self.assertIn("B45-POSTQ4-T12-PAIRED-LIVE-MODEL-RERUN-EXACT-APPROVAL-PACKET", next_tasks["execution_update"]["executed_task_ids"])
        self.assertEqual(
            "exact_approval_packet_draft_not_owner_confirmed_not_run",
            next_tasks["execution_update"]["status_by_task"]["B45-POSTQ4-T12-PAIRED-LIVE-MODEL-RERUN-EXACT-APPROVAL-PACKET"],
        )

        for registry in [registry_ru, registry_en]:
            with self.subTest(registry="source_registry"):
                self.assertIn("B45-POSTQ4-T12-PAIRED-LIVE-MODEL-RERUN-EXACT-APPROVAL-PACKET", registry)
                self.assertIn("B45-POSTQ4-T12-A01", registry)
                self.assertIn("docs/superpowers/specs/batch45-postq4-t12-paired-live-model-rerun-exact-approval-packet.json", registry)

        self.assertIn("| `B45-POSTQ4-T12` |", track11)
        self.assertIn("batch45-postq4-t12-paired-live-model-rerun-exact-approval-packet.json", track11)

    def test_b45_postq4_t12_paired_live_model_rerun_results_preserve_no_go(self):
        result = json.loads(POST_Q4_T12_RESULTS.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
        registry_ru = (DOCS / "sources" / "registry.md").read_text(encoding="utf-8")
        registry_en = (DOCS / "sources" / "registry.en.md").read_text(encoding="utf-8")
        lifecycle = json.loads((ROOT / ".codex" / "product-agent-os" / "lifecycle-state.json").read_text(encoding="utf-8"))
        plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        evals = (ROOT / "EVALS.md").read_text(encoding="utf-8")
        test_plan = (ROOT / "TEST.md").read_text(encoding="utf-8")
        track11 = (
            DOCS
            / "superpowers"
            / "plans"
            / "2026-06-20-track-11-documentation-architecture-refresh.md"
        ).read_text(encoding="utf-8")

        self.assertEqual("batch45_postq4_t12_paired_live_model_rerun_results_v1", result["schema_version"])
        self.assertEqual("B45-POSTQ4-T12-PAIRED-LIVE-MODEL-RERUN", result["task_id"])
        self.assertEqual("B45-POSTQ4-T12-RUN-A01", result["evidence_id"])
        self.assertEqual("executed_paired_live_model_rerun_no_go_invalid_pair", result["status"])
        self.assertTrue(result["approval_confirmation_observed"])
        self.assertEqual(16, result["execution_summary"]["approved_primary_task_model_calls_started"])
        self.assertEqual(14, result["execution_summary"]["completed_primary_task_runs"])
        self.assertEqual(1, result["execution_summary"]["no_op_primary_task_runs"])
        self.assertEqual(1, result["execution_summary"]["invalid_json_primary_task_runs"])
        self.assertEqual(0, result["execution_summary"]["timeout_primary_task_runs"])
        self.assertEqual(6, result["execution_summary"]["valid_pair_count"])
        self.assertEqual(2, result["execution_summary"]["invalid_pair_count"])
        self.assertEqual(0, result["execution_summary"]["reviewer_calls_started"])
        self.assertEqual("not_run_due_invalid_pair_count", result["execution_summary"]["reviewer_status"])
        self.assertFalse(result["aggregate_result"]["promotion_threshold_met"])
        self.assertFalse(result["aggregate_result"]["m26_reversed"])
        self.assertFalse(result["aggregate_result"]["m35_reversed"])
        self.assertFalse(result["cost_and_retention"]["raw_outputs_in_repo"])
        self.assertTrue(result["cost_and_retention"]["raw_outputs_retained_in_temp_only"])
        self.assertEqual("%TEMP%\\codex-b45-postq4-t12-*", result["cost_and_retention"]["temp_root_pattern"])
        self.assertTrue(result["cost_and_retention"]["temp_root_redacted_in_repo"])
        self.assertNotIn("C:\\Users", json.dumps(result))

        invalid_pairs = {pair["task_id"]: pair["invalid_reason"] for pair in result["pairs"] if not pair["pair_valid_for_scoring"]}
        self.assertEqual("treatment_invalid_json", invalid_pairs["B45-HELDOUT-01"])
        self.assertEqual("treatment_no_op", invalid_pairs["B45-HELDOUT-07"])
        self.assertEqual(8, len(result["pairs"]))
        self.assertEqual(16, len(result["per_task_results"]))

        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t12-paired-live-model-rerun-results.json",
            next_tasks["execution_update"]["latest_t12_run_results"],
        )
        self.assertIn("B45-POSTQ4-T12-PAIRED-LIVE-MODEL-RERUN", next_tasks["execution_update"]["executed_task_ids"])
        self.assertEqual(
            "executed_paired_live_model_rerun_no_go_invalid_pair",
            next_tasks["execution_update"]["status_by_task"]["B45-POSTQ4-T12-PAIRED-LIVE-MODEL-RERUN"],
        )
        self.assertEqual(16, next_tasks["execution_update"]["t12_live_eval_result"]["approved_primary_task_model_calls_started"])
        self.assertEqual(6, next_tasks["execution_update"]["t12_live_eval_result"]["valid_pair_count"])
        self.assertEqual("not_run_due_invalid_pair_count", next_tasks["execution_update"]["t12_live_eval_result"]["reviewer_status"])

        for registry in [registry_ru, registry_en]:
            self.assertIn("B45-POSTQ4-T12-RUN-A01", registry)
            self.assertIn("docs/superpowers/specs/batch45-postq4-t12-paired-live-model-rerun-results.json", registry)
            self.assertIn("valid_pair_count=6", registry)

        for control_plane in [plan, evals, test_plan, track11]:
            self.assertIn("B45-POSTQ4-T12-RUN-A01", control_plane)

        self.assertIn(lifecycle["task_id"], {
            "B45-POSTQ4-T12-PAIRED-LIVE-MODEL-RERUN",
            "B45-POSTQ4-T13-STRICT_OUTPUT_SCHEMA_AND_HARNESS_HARDENING",
            "B45-POSTQ4-T14-STRICT-RERUN-APPROVAL-PACKET",
            "B45-POSTQ4-T14-STRICT-RERUN",
            "B45-POSTQ4-T15-DECISION-PACKET-MODEL-CHANGE-INTERPRETATION",
            "B45-POSTQ4-T16-T22-PROMOTION-GRADE-EVAL-TASK-GROUP",
            "B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS",
            "B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA",
            "B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY",
        })

    def test_b45_postq4_t13_strict_output_schema_and_harness_hardening(self):
        packet = json.loads(POST_Q4_T13_HARDENING.read_text(encoding="utf-8"))
        t12_result = json.loads(POST_Q4_T12_RESULTS.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
        registry_ru = (DOCS / "sources" / "registry.md").read_text(encoding="utf-8")
        registry_en = (DOCS / "sources" / "registry.en.md").read_text(encoding="utf-8")
        lifecycle = json.loads((ROOT / ".codex" / "product-agent-os" / "lifecycle-state.json").read_text(encoding="utf-8"))
        plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        evals = (ROOT / "EVALS.md").read_text(encoding="utf-8")
        test_plan = (ROOT / "TEST.md").read_text(encoding="utf-8")
        track11 = (
            DOCS
            / "superpowers"
            / "plans"
            / "2026-06-20-track-11-documentation-architecture-refresh.md"
        ).read_text(encoding="utf-8")

        self.assertEqual("batch45_postq4_t13_strict_output_schema_and_harness_hardening_v1", packet["schema_version"])
        self.assertEqual("B45-POSTQ4-T13-STRICT_OUTPUT_SCHEMA_AND_HARNESS_HARDENING", packet["task_id"])
        self.assertEqual("B45-POSTQ4-T13-A01", packet["evidence_id"])
        self.assertEqual("implemented_local_schema_no_op_hardening_no_live_calls", packet["status"])
        self.assertEqual(6, packet["basis"]["t12_failure_classes"]["valid_pair_count"])
        self.assertEqual(1, packet["basis"]["t12_failure_classes"]["invalid_json_primary_task_runs"])
        self.assertEqual(1, packet["basis"]["t12_failure_classes"]["no_op_primary_task_runs"])
        self.assertIn("plugins/product-agent-os/scripts/codex_runtime_runner/model_output.py", packet["implemented_hardening"]["module"])
        self.assertIn("treatment_invalid_json", packet["implemented_hardening"]["pair_gate_contract"]["supported_t12_reasons"])
        self.assertIn("treatment_no_op", packet["implemented_hardening"]["pair_gate_contract"]["supported_t12_reasons"])
        self.assertFalse(packet["decision"]["promotion_allowed"])
        self.assertTrue(packet["decision"]["next_rerun_requires_fresh_exact_approval"])
        self.assertFalse(packet["no_unapproved_actions"]["live_model_or_provider_api_called_without_approval"])
        self.assertFalse(packet["no_unapproved_actions"]["raw_outputs_written_to_repo"])

        self.assertEqual([], validate_paired_live_eval_result(t12_result))
        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t13-strict-output-schema-and-harness-hardening.json",
            next_tasks["execution_update"]["latest_t13_hardening"],
        )
        self.assertIn("B45-POSTQ4-T13-STRICT_OUTPUT_SCHEMA_AND_HARNESS_HARDENING", next_tasks["execution_update"]["executed_task_ids"])
        self.assertEqual(
            "implemented_local_schema_no_op_hardening_no_live_calls",
            next_tasks["execution_update"]["status_by_task"]["B45-POSTQ4-T13-STRICT_OUTPUT_SCHEMA_AND_HARNESS_HARDENING"],
        )

        for registry in [registry_ru, registry_en]:
            self.assertIn("B45-POSTQ4-T13-A01", registry)
            self.assertIn("docs/superpowers/specs/batch45-postq4-t13-strict-output-schema-and-harness-hardening.json", registry)
            self.assertIn("local schema/no-op harness hardening", registry)

        for control_plane in [plan, evals, test_plan, track11]:
            self.assertIn("B45-POSTQ4-T13-A01", control_plane)

        self.assertIn(lifecycle["task_id"], {
            "B45-POSTQ4-T13-STRICT_OUTPUT_SCHEMA_AND_HARNESS_HARDENING",
            "B45-POSTQ4-T14-STRICT-RERUN-APPROVAL-PACKET",
            "B45-POSTQ4-T14-STRICT-RERUN",
            "B45-POSTQ4-T15-DECISION-PACKET-MODEL-CHANGE-INTERPRETATION",
            "B45-POSTQ4-T16-T22-PROMOTION-GRADE-EVAL-TASK-GROUP",
            "B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS",
            "B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA",
            "B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY",
        })
        if lifecycle["task_id"] == "B45-POSTQ4-T13-STRICT_OUTPUT_SCHEMA_AND_HARNESS_HARDENING":
            self.assertEqual("synthetic_green_after_local_tests_only", lifecycle["closure_level"])
        elif lifecycle["task_id"] == "B45-POSTQ4-T14-STRICT-RERUN":
            self.assertEqual("live_dependency_aligned", lifecycle["closure_level"])
        elif lifecycle["task_id"] == "B45-POSTQ4-T15-DECISION-PACKET-MODEL-CHANGE-INTERPRETATION":
            self.assertEqual("docs_contract_ready", lifecycle["closure_level"])
        elif lifecycle["task_id"] in {
            "B45-POSTQ4-T16-T22-PROMOTION-GRADE-EVAL-TASK-GROUP",
            "B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS",
            "B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA",
            "B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY",
        }:
            self.assertEqual("docs_contract_ready", lifecycle["closure_level"])
        else:
            self.assertEqual("approval_packet_only_not_run", lifecycle["closure_level"])

    def test_b45_postq4_t14_strict_rerun_approval_packet_is_not_owner_confirmation(self):
        packet = json.loads(POST_Q4_T14_APPROVAL.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
        registry_ru = (DOCS / "sources" / "registry.md").read_text(encoding="utf-8")
        registry_en = (DOCS / "sources" / "registry.en.md").read_text(encoding="utf-8")
        lifecycle = json.loads((ROOT / ".codex" / "product-agent-os" / "lifecycle-state.json").read_text(encoding="utf-8"))
        plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        evals = (ROOT / "EVALS.md").read_text(encoding="utf-8")
        test_plan = (ROOT / "TEST.md").read_text(encoding="utf-8")
        track11 = (
            DOCS
            / "superpowers"
            / "plans"
            / "2026-06-20-track-11-documentation-architecture-refresh.md"
        ).read_text(encoding="utf-8")

        self.assertEqual("batch45_postq4_t14_strict_rerun_approval_packet_v1", packet["schema_version"])
        self.assertEqual("B45-POSTQ4-T14-STRICT-RERUN-APPROVAL-PACKET", packet["task_id"])
        self.assertEqual("B45-POSTQ4-T14-A01", packet["evidence_id"])
        self.assertEqual(
            "exact_approval_packet_draft_revised_for_gpt55_high_not_owner_confirmed_not_run",
            packet["status"],
        )
        self.assertFalse(packet["approval_state"]["owner_confirmed"])
        self.assertFalse(packet["approval_state"]["run_authorized_by_this_artifact"])
        self.assertTrue(packet["approval_state"]["requires_next_user_message"])
        self.assertIn("Подтверждаю B45-POSTQ4-T14 exact approval:", packet["exact_approval_text_for_owner_confirmation"])
        self.assertIn("model: gpt-5.5", packet["exact_approval_text_for_owner_confirmation"])
        self.assertIn("model reasoning effort: high", packet["exact_approval_text_for_owner_confirmation"])
        self.assertIn(
            "result detail level: detailed run/pair/aggregate evidence with per-dimension rubric scores, failure taxonomy, changed-file metadata, static warning deltas, invalid-pair reasons, reviewer-ready summaries and unsupported-claim ledger",
            packet["exact_approval_text_for_owner_confirmation"],
        )
        self.assertEqual("gpt-5.5", packet["approved_if_owner_confirms_exact_text"]["model"])
        self.assertEqual("high", packet["approved_if_owner_confirms_exact_text"]["model_reasoning_effort"])
        self.assertEqual("detailed", packet["approved_if_owner_confirms_exact_text"]["result_detail_level"])
        self.assertEqual(
            "current_best_quality_rerun_not_same_model_comparability",
            packet["approved_if_owner_confirms_exact_text"]["comparison_mode"],
        )
        self.assertIn("model_change_effect", packet["approval_state"])
        self.assertTrue(packet["promotion_gate"]["model_change_requires_decision_packet"])
        self.assertIn("dimension_scores", packet["result_schema_contract"]["required_run_fields"])
        self.assertIn("failure_taxonomy", packet["result_schema_contract"]["required_run_fields"])
        self.assertIn("same_model_comparability_with_m26_t05_t12", packet["result_schema_contract"]["required_aggregate_fields"])
        self.assertIn("model_change_interpretation_required", packet["result_schema_contract"]["required_aggregate_fields"])
        self.assertGreaterEqual(len(packet["model_selection_source_matrix"]), 3)
        self.assertIn("plugins/product-agent-os/scripts/codex_runtime_runner/model_output.py", packet["basis"])
        self.assertEqual(
            "plugins/product-agent-os/scripts/codex_runtime_runner/model_output.py",
            packet["run_design"]["strict_output_validator"],
        )
        self.assertTrue(packet["t13_harness_gate"]["pre_reviewer_validation_required"])
        self.assertFalse(packet["promotion_gate"]["static_warning_delta_can_promote"])
        self.assertFalse(packet["no_unapproved_actions"]["live_model_or_provider_api_called"])
        self.assertFalse(packet["no_unapproved_actions"]["reviewer_model_call_started"])
        self.assertFalse(packet["decision"]["new_live_model_rerun_performed"])
        self.assertFalse(packet["decision"]["promotion_allowed"])

        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t14-strict-rerun-approval-packet.json",
            next_tasks["execution_update"]["latest_t14_approval_packet"],
        )
        self.assertIn("B45-POSTQ4-T14-STRICT-RERUN-APPROVAL-PACKET", next_tasks["execution_update"]["executed_task_ids"])
        self.assertEqual(
            "exact_approval_packet_consumed_by_t14_run_gpt55_high",
            next_tasks["execution_update"]["status_by_task"]["B45-POSTQ4-T14-STRICT-RERUN-APPROVAL-PACKET"],
        )
        self.assertEqual("gpt-5.5", next_tasks["execution_update"]["t14_approval_packet_result"]["model"])
        self.assertEqual("high", next_tasks["execution_update"]["t14_approval_packet_result"]["model_reasoning_effort"])
        self.assertEqual("detailed", next_tasks["execution_update"]["t14_approval_packet_result"]["result_detail_level"])

        for registry in [registry_ru, registry_en]:
            self.assertIn("B45-POSTQ4-T14-A01", registry)
            self.assertIn("docs/superpowers/specs/batch45-postq4-t14-strict-rerun-approval-packet.json", registry)

        for control_plane in [plan, evals, test_plan, track11]:
            self.assertIn("B45-POSTQ4-T14-A01", control_plane)

        self.assertIn(
            lifecycle["task_id"],
            {
                "B45-POSTQ4-T14-STRICT-RERUN-APPROVAL-PACKET",
                "B45-POSTQ4-T14-STRICT-RERUN",
                "B45-POSTQ4-T15-DECISION-PACKET-MODEL-CHANGE-INTERPRETATION",
                "B45-POSTQ4-T16-T22-PROMOTION-GRADE-EVAL-TASK-GROUP",
                "B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS",
                "B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA",
                "B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY",
            },
        )

    def test_b45_postq4_t14_strict_rerun_results_preserve_model_change_no_promotion(self):
        result = json.loads(POST_Q4_T14_RESULTS.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
        registry_ru = (DOCS / "sources" / "registry.md").read_text(encoding="utf-8")
        registry_en = (DOCS / "sources" / "registry.en.md").read_text(encoding="utf-8")
        lifecycle = json.loads((ROOT / ".codex" / "product-agent-os" / "lifecycle-state.json").read_text(encoding="utf-8"))

        self.assertEqual("batch45_postq4_t14_strict_rerun_results_v1", result["schema_version"])
        self.assertEqual("B45-POSTQ4-T14-STRICT-RERUN", result["task_id"])
        self.assertEqual("B45-POSTQ4-T14-RUN-A01", result["evidence_id"])
        self.assertEqual("executed_current_best_quality_rerun_no_promotion", result["status"])
        self.assertTrue(result["approval_confirmation_observed"])
        self.assertEqual("gpt-5.5", result["approval_used"]["model"])
        self.assertEqual("high", result["approval_used"]["model_reasoning_effort"])
        self.assertEqual("current_best_quality_rerun_not_same_model_comparability", result["approval_used"]["comparison_mode"])

        summary = result["execution_summary"]
        aggregate = result["aggregate_result"]
        self.assertEqual(16, summary["approved_primary_task_model_calls_started"])
        self.assertEqual(16, summary["completed_primary_task_runs"])
        self.assertEqual(8, summary["valid_pair_count"])
        self.assertEqual(0, summary["invalid_pair_count"])
        self.assertEqual(0, summary["timeout_primary_task_runs"])
        self.assertEqual(0, summary["no_op_primary_task_runs"])
        self.assertEqual(0, summary["invalid_json_primary_task_runs"])
        self.assertEqual("not_run_due_runner_contract_manual_gap", summary["reviewer_status"])
        self.assertEqual(0, summary["reviewer_calls_started"])
        self.assertEqual(8, aggregate["valid_pair_count"])
        self.assertEqual(0, aggregate["invalid_pair_count"])
        self.assertEqual(3.27, aggregate["average_score_delta_percent"])
        self.assertEqual(6, aggregate["treatment_equal_or_better_count"])
        self.assertFalse(aggregate["promotion_threshold_met"])
        self.assertFalse(aggregate["m26_reversed"])
        self.assertFalse(aggregate["m35_reversed"])
        self.assertFalse(aggregate["same_model_comparability_with_m26_t05_t12"])
        self.assertTrue(aggregate["model_change_interpretation_required"])
        self.assertEqual([], validate_paired_live_eval_result(result))

        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t14-strict-rerun-results.json",
            next_tasks["execution_update"]["latest_t14_run_results"],
        )
        self.assertEqual(
            "executed_current_best_quality_rerun_no_promotion",
            next_tasks["execution_update"]["t14_live_eval_result"]["status"],
        )
        self.assertEqual(8, next_tasks["execution_update"]["t14_live_eval_result"]["valid_pair_count"])
        self.assertEqual(0, next_tasks["execution_update"]["t14_live_eval_result"]["invalid_pair_count"])
        self.assertEqual("not_run_due_runner_contract_manual_gap", next_tasks["execution_update"]["t14_live_eval_result"]["reviewer_status"])

        for registry in [registry_ru, registry_en]:
            self.assertIn("B45-POSTQ4-T14-RUN-A01", registry)
            self.assertIn("docs/superpowers/specs/batch45-postq4-t14-strict-rerun-results.json", registry)

        self.assertIn(
            lifecycle["task_id"],
            {
                "B45-POSTQ4-T14-STRICT-RERUN",
                "B45-POSTQ4-T15-DECISION-PACKET-MODEL-CHANGE-INTERPRETATION",
                "B45-POSTQ4-T16-T22-PROMOTION-GRADE-EVAL-TASK-GROUP",
                "B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS",
                "B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA",
                "B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY",
            },
        )
        if lifecycle["task_id"] == "B45-POSTQ4-T14-STRICT-RERUN":
            self.assertEqual("live_dependency_aligned", lifecycle["closure_level"])
        else:
            self.assertEqual("docs_contract_ready", lifecycle["closure_level"])

    def test_b45_postq4_t15_model_change_decision_keeps_no_promotion(self):
        packet = json.loads(POST_Q4_T15_DECISION.read_text(encoding="utf-8"))
        t14_result = json.loads(POST_Q4_T14_RESULTS.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
        registry_ru = (DOCS / "sources" / "registry.md").read_text(encoding="utf-8")
        registry_en = (DOCS / "sources" / "registry.en.md").read_text(encoding="utf-8")
        lifecycle = json.loads((ROOT / ".codex" / "product-agent-os" / "lifecycle-state.json").read_text(encoding="utf-8"))
        plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        evals = (ROOT / "EVALS.md").read_text(encoding="utf-8")
        test_plan = (ROOT / "TEST.md").read_text(encoding="utf-8")
        track11 = (
            DOCS
            / "superpowers"
            / "plans"
            / "2026-06-20-track-11-documentation-architecture-refresh.md"
        ).read_text(encoding="utf-8")

        self.assertEqual("batch45_postq4_t15_model_change_decision_packet_v1", packet["schema_version"])
        self.assertEqual("B45-POSTQ4-T15-DECISION-PACKET-MODEL-CHANGE-INTERPRETATION", packet["task_id"])
        self.assertEqual("B45-POSTQ4-T15-A01", packet["evidence_id"])
        self.assertEqual("implemented_model_change_interpretation_keep_advisory_only_no_go", packet["status"])
        self.assertEqual(
            "keep_advisory_only_no_go_after_model_change_rerun",
            packet["decision"]["state"],
        )
        self.assertTrue(packet["decision"]["t14_is_useful_quality_signal"])
        self.assertFalse(packet["decision"]["t14_can_reverse_m26"])
        self.assertFalse(packet["decision"]["t14_can_reverse_m35"])
        self.assertFalse(packet["decision"]["promotion_allowed"])
        self.assertEqual(
            "blocks_direct_same_model_comparison",
            packet["interpretation_matrix"]["model_change"]["decision"],
        )
        self.assertEqual("not_satisfied", packet["interpretation_matrix"]["promotion_threshold"]["decision"])
        self.assertEqual("not_satisfied", packet["interpretation_matrix"]["reviewer_gate"]["decision"])
        self.assertFalse(packet["promotion_gate_after_t15"]["promotion_allowed_now"])
        self.assertEqual(3.27, packet["promotion_gate_after_t15"]["t14_average_score_delta_percent"])
        self.assertFalse(packet["promotion_gate_after_t15"]["minimum_behavior_quality_improvement_met"])
        self.assertEqual(3.27, t14_result["aggregate_result"]["average_score_delta_percent"])
        self.assertFalse(t14_result["aggregate_result"]["same_model_comparability_with_m26_t05_t12"])

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for unsupported in [
            "M26_no_go_reversed",
            "M35_no_go_reversed",
            "strict_same_model_comparability_with_spark_runs",
            "promotion_ready",
        ]:
            self.assertIn(unsupported, packet["unsupported_claims"])

        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t15-model-change-decision-packet.json",
            next_tasks["execution_update"]["latest_t15_model_change_decision"],
        )
        self.assertEqual(
            "implemented_model_change_interpretation_keep_advisory_only_no_go",
            next_tasks["execution_update"]["status_by_task"][
                "B45-POSTQ4-T15-DECISION-PACKET-MODEL-CHANGE-INTERPRETATION"
            ],
        )
        self.assertEqual(
            "keep_advisory_only_no_go_after_model_change_rerun",
            next_tasks["execution_update"]["t15_model_change_decision"]["decision"],
        )
        self.assertFalse(next_tasks["execution_update"]["t15_model_change_decision"]["promotion_allowed"])

        for registry in [registry_ru, registry_en]:
            self.assertIn("B45-POSTQ4-T15-A01", registry)
            self.assertIn("docs/superpowers/specs/batch45-postq4-t15-model-change-decision-packet.json", registry)
            self.assertIn("same-model comparability=false", registry)

        for control_plane in [plan, evals, test_plan, track11]:
            self.assertIn("B45-POSTQ4-T15-A01", control_plane)

        self.assertIn(
            lifecycle["task_id"],
            {
                "B45-POSTQ4-T16-T22-PROMOTION-GRADE-EVAL-TASK-GROUP",
                "B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS",
                "B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA",
                "B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY",
            },
        )
        self.assertEqual("docs_contract_ready", lifecycle["closure_level"])

    def test_b45_postq4_t16_t22_promotion_grade_eval_task_group_is_design_only(self):
        packet = json.loads(POST_Q4_T16_T22_TASK_GROUP.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
        registry_ru = (DOCS / "sources" / "registry.md").read_text(encoding="utf-8")
        registry_en = (DOCS / "sources" / "registry.en.md").read_text(encoding="utf-8")
        lifecycle = json.loads((ROOT / ".codex" / "product-agent-os" / "lifecycle-state.json").read_text(encoding="utf-8"))
        plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        runlog = (ROOT / "RUNLOG.md").read_text(encoding="utf-8")
        evals = (ROOT / "EVALS.md").read_text(encoding="utf-8")
        test_plan = (ROOT / "TEST.md").read_text(encoding="utf-8")
        current_state = (DOCS / "product-agent-os" / "control-plane-current-state.md").read_text(encoding="utf-8")
        track11 = (
            DOCS
            / "superpowers"
            / "plans"
            / "2026-06-20-track-11-documentation-architecture-refresh.md"
        ).read_text(encoding="utf-8")

        self.assertEqual("batch45_postq4_t16_t22_promotion_grade_eval_task_group_v1", packet["schema_version"])
        self.assertEqual("B45-POSTQ4-T16-T22-PROMOTION-GRADE-EVAL-TASK-GROUP", packet["task_id"])
        self.assertEqual("B45-POSTQ4-T16-T22-A01", packet["evidence_id"])
        self.assertEqual("implemented_task_group_design_no_run", packet["status"])
        self.assertEqual("B45-S8-PROMOTION-GRADE-EVAL", packet["task_group"]["group_id"])
        self.assertFalse(packet["task_group"]["promotion_allowed_now"])
        self.assertTrue(packet["task_group"]["execution_requires_later_exact_approval"])
        self.assertEqual("same_model_baseline_treatment", packet["comparability_policy"]["preferred_mode"])
        self.assertIn("explicit_current_model_comparison", packet["comparability_policy"]["allowed_modes"])
        self.assertTrue(packet["promotion_gate"]["reviewer_gate_required"])
        self.assertTrue(packet["promotion_gate"]["raw_temp_only_retention_required"])
        self.assertTrue(packet["promotion_gate"]["no_unapproved_actions_proof_required"])

        task_ids = {task["task_id"] for task in packet["task_rows"]}
        for required_task in [
            "B45-POSTQ4-T16-PROMOTION-GRADE-EVAL-TASK-GROUP",
            "B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS",
            "B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA",
            "B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY",
            "B45-POSTQ4-T20-EXACT-APPROVAL-PACKET",
            "B45-POSTQ4-T21-APPROVED-PROMOTION-GRADE-EVAL-RUN",
            "B45-POSTQ4-T22-REVIEWER-GATE-AND-DECISION",
        ]:
            with self.subTest(required_task=required_task):
                self.assertIn(required_task, task_ids)

        task_status = {task["task_id"]: task["status"] for task in packet["task_rows"]}
        self.assertEqual("approval_required_not_started", task_status["B45-POSTQ4-T21-APPROVED-PROMOTION-GRADE-EVAL-RUN"])
        self.assertEqual("blocked_until_t21_result", task_status["B45-POSTQ4-T22-REVIEWER-GATE-AND-DECISION"])

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for unsupported in [
            "promotion_grade_eval_result_exists",
            "M26_no_go_reversed",
            "M35_no_go_reversed",
            "T15_no_go_reversed",
            "same_model_promotion_run_evidence_exists",
            "promotion_ready",
        ]:
            self.assertIn(unsupported, packet["unsupported_claims"])
        self.assertNotIn("same_model_comparability_selected_for_future_run", packet["unsupported_claims"])

        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t16-t22-promotion-grade-eval-task-group.json",
            next_tasks["execution_update"]["latest_t16_t22_promotion_grade_eval_task_group"],
        )
        self.assertEqual(
            "implemented_task_group_design_no_run",
            next_tasks["execution_update"]["status_by_task"][
                "B45-POSTQ4-T16-T22-PROMOTION-GRADE-EVAL-TASK-GROUP"
            ],
        )
        self.assertEqual(
            "B45-POSTQ4-T16-T22-PROMOTION-GRADE-EVAL-TASK-GROUP",
            next_tasks["execution_update"]["t15_model_change_decision"]["next_recommended_route"],
        )
        self.assertFalse(next_tasks["execution_update"]["t16_t22_promotion_grade_eval_task_group"]["promotion_allowed"])
        self.assertTrue(
            next_tasks["execution_update"]["t16_t22_promotion_grade_eval_task_group"][
                "future_exact_approval_required_before_run"
            ]
        )

        for registry in [registry_ru, registry_en]:
            self.assertIn("B45-POSTQ4-T16-T22-A01", registry)
            self.assertIn("docs/superpowers/specs/batch45-postq4-t16-t22-promotion-grade-eval-task-group.json", registry)

        for control_plane in [plan, runlog, evals, test_plan, current_state, track11]:
            self.assertIn("B45-POSTQ4-T16-T22-A01", control_plane)

        self.assertIn(
            lifecycle["task_id"],
            {
                "B45-POSTQ4-T16-T22-PROMOTION-GRADE-EVAL-TASK-GROUP",
                "B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS",
                "B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA",
                "B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY",
            },
        )
        self.assertIn(
            lifecycle["evidence_id"],
            {
                "B45-POSTQ4-T16-T22-A01",
                "B45-POSTQ4-T17-A01",
                "B45-POSTQ4-T18-A01",
                "B45-POSTQ4-T19-A01",
            },
        )
        self.assertIn(
            lifecycle["status"],
            {
                "implemented_task_group_design_no_run",
                "implemented_frozen_heldout_corpus_manifest_no_run",
                "implemented_eval_design_strict_schema_no_run",
                "implemented_cost_timeout_retention_policy_no_run",
            },
        )
        self.assertEqual("docs_contract_ready", lifecycle["closure_level"])

    def test_b45_postq4_t17_frozen_heldout_corpus_manifest_is_no_run(self):
        packet = json.loads(POST_Q4_T17_FROZEN_HELDOUT_CORPUS.read_text(encoding="utf-8"))
        parent = json.loads(POST_Q4_T16_T22_TASK_GROUP.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
        registry_ru = (DOCS / "sources" / "registry.md").read_text(encoding="utf-8")
        registry_en = (DOCS / "sources" / "registry.en.md").read_text(encoding="utf-8")
        lifecycle = json.loads((ROOT / ".codex" / "product-agent-os" / "lifecycle-state.json").read_text(encoding="utf-8"))
        plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        runlog = (ROOT / "RUNLOG.md").read_text(encoding="utf-8")
        evals = (ROOT / "EVALS.md").read_text(encoding="utf-8")
        test_plan = (ROOT / "TEST.md").read_text(encoding="utf-8")
        current_state = (DOCS / "product-agent-os" / "control-plane-current-state.md").read_text(encoding="utf-8")
        coding_ru = (DOCS / "product-agent-os" / "coding-standards.md").read_text(encoding="utf-8")
        coding_en = (DOCS / "product-agent-os" / "coding-standards.en.md").read_text(encoding="utf-8")
        behavioral_ru = (DOCS / "product-agent-os" / "behavioral-evals.md").read_text(encoding="utf-8")
        behavioral_en = (DOCS / "product-agent-os" / "behavioral-evals.en.md").read_text(encoding="utf-8")
        track11 = (
            DOCS
            / "superpowers"
            / "plans"
            / "2026-06-20-track-11-documentation-architecture-refresh.md"
        ).read_text(encoding="utf-8")

        serialized = json.dumps(packet, sort_keys=True)
        self.assertEqual("batch45_postq4_t17_frozen_heldout_corpus_v1", packet["schema_version"])
        self.assertEqual("B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS", packet["task_id"])
        self.assertEqual("B45-POSTQ4-T17-A01", packet["evidence_id"])
        self.assertEqual("implemented_frozen_heldout_corpus_manifest_no_run", packet["status"])
        self.assertEqual("docs_contract_ready", packet["closure_level"])

        corpus = packet["corpus"]
        self.assertEqual("B45-POSTQ4-FROZEN-HELDOUT-CORPUS-V1", corpus["corpus_id"])
        self.assertEqual("v1", corpus["corpus_version"])
        self.assertEqual("frozen_before_any_baseline_or_treatment_execution", corpus["status"])
        self.assertEqual(8, corpus["task_count"])
        self.assertEqual(8, len(corpus["task_ids"]))
        self.assertEqual(8, len(set(corpus["task_ids"])))
        self.assertEqual("sha256", corpus["hash_algorithm"])
        self.assertTrue(corpus["corpus_manifest_hash"].startswith("sha256:"))
        self.assertEqual(71, len(corpus["corpus_manifest_hash"]))

        self.assertFalse(packet["change_control"]["baseline_started"])
        self.assertFalse(packet["change_control"]["treatment_started"])
        self.assertIn("new corpus_version", packet["change_control"]["edit_after_baseline_starts"])
        self.assertEqual("stop_condition_forbidden", packet["change_control"]["tuning_after_result_inspection"])

        entries = packet["entries"]
        self.assertEqual(8, len(entries))
        self.assertEqual(set(corpus["task_ids"]), {entry["task_id"] for entry in entries})
        self.assertEqual({f"H{i}" for i in range(1, 9)}, {entry["slot"] for entry in entries})
        for entry in entries:
            with self.subTest(entry=entry["task_id"]):
                self.assertIn(entry["difficulty"], {"low", "medium", "high"})
                self.assertEqual(
                    "project-authored task metadata from batch45-quality-retest-protocol held_out_tasks_v2",
                    entry["source_class"],
                )
                self.assertEqual("metadata_only_no_raw_private_source", entry["privacy_class"])
                self.assertTrue(entry["expected_evidence"])
                self.assertTrue(entry["allowed_evidence"])
                self.assertTrue(entry["blocked_claims"])
                self.assertTrue(entry["source_refs"])
                self.assertTrue(entry["metadata_hash"].startswith("sha256:"))
                self.assertEqual(71, len(entry["metadata_hash"]))
                for source_ref in entry["source_refs"]:
                    self.assertFalse(source_ref.startswith("/"))
                    self.assertNotIn("..", source_ref)
                    self.assertNotIn("C:", source_ref)

        self.assertEqual("metadata_only_passed_current_run", packet["privacy_review"]["result"])
        self.assertIn("raw private source bodies", packet["privacy_review"]["forbidden_retained_data_classes"])
        self.assertIn("secrets_or_credentials", packet["privacy_review"]["forbidden_retained_data_classes"])
        self.assertFalse(packet["approval_and_execution_boundary"]["packet_authorizes_future_run"])
        self.assertFalse(packet["approval_and_execution_boundary"]["baseline_or_treatment_run_started"])
        self.assertFalse(packet["approval_and_execution_boundary"]["reviewer_gate_satisfied"])
        self.assertEqual(
            "B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA",
            packet["approval_and_execution_boundary"]["next_required_task"],
        )

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        for unsupported in [
            "promotion_grade_eval_result_exists",
            "baseline_treatment_execution_started",
            "reviewer_gate_satisfied",
            "M26_no_go_reversed",
            "M35_no_go_reversed",
            "T15_no_go_reversed",
            "promotion_ready",
        ]:
            self.assertIn(unsupported, packet["unsupported_claims"])

        for forbidden_path_fragment in ["C:\\Users", "C:/Users", "\\Users\\"]:
            self.assertNotIn(forbidden_path_fragment, serialized)

        parent_rows = {task["task_id"]: task for task in parent["task_rows"]}
        self.assertEqual(
            "implemented_frozen_heldout_corpus_manifest_no_run",
            parent_rows["B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS"]["status"],
        )
        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t17-frozen-heldout-corpus.json",
            parent_rows["B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS"]["evidence_owner"],
        )

        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t17-frozen-heldout-corpus.json",
            next_tasks["execution_update"]["latest_t17_frozen_heldout_corpus"],
        )
        self.assertIn("B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS", next_tasks["execution_update"]["executed_task_ids"])
        self.assertEqual(
            "implemented_frozen_heldout_corpus_manifest_no_run",
            next_tasks["execution_update"]["status_by_task"]["B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS"],
        )
        self.assertFalse(next_tasks["execution_update"]["t17_frozen_heldout_corpus"]["promotion_allowed"])
        self.assertFalse(next_tasks["execution_update"]["t17_frozen_heldout_corpus"]["baseline_started"])
        self.assertFalse(next_tasks["execution_update"]["t17_frozen_heldout_corpus"]["treatment_started"])

        for registry in [registry_ru, registry_en]:
            self.assertIn("B45-POSTQ4-T17-A01", registry)
            self.assertIn("docs/superpowers/specs/batch45-postq4-t17-frozen-heldout-corpus.json", registry)
            self.assertIn("metadata-only frozen held-out corpus", registry)

        for control_plane in [
            plan,
            runlog,
            evals,
            test_plan,
            current_state,
            coding_ru,
            coding_en,
            track11,
        ]:
            self.assertIn("B45-POSTQ4-T17-A01", control_plane)

        for source_owner in [
            plan,
            test_plan,
            current_state,
            coding_ru,
            coding_en,
            behavioral_ru,
            behavioral_en,
            track11,
        ]:
            self.assertIn("batch45-postq4-t17-frozen-heldout-corpus.json", source_owner)

        self.assertIn(
            lifecycle["task_id"],
            {
                "B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS",
                "B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA",
                "B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY",
            },
        )
        self.assertIn(lifecycle["evidence_id"], {"B45-POSTQ4-T17-A01", "B45-POSTQ4-T18-A01", "B45-POSTQ4-T19-A01"})
        self.assertIn(
            lifecycle["status"],
            {
                "implemented_frozen_heldout_corpus_manifest_no_run",
                "implemented_eval_design_strict_schema_no_run",
                "implemented_cost_timeout_retention_policy_no_run",
            },
        )
        self.assertEqual("docs_contract_ready", lifecycle["closure_level"])

    def test_b45_postq4_t18_eval_design_and_strict_schema_is_no_run(self):
        packet = json.loads(POST_Q4_T18_EVAL_DESIGN.read_text(encoding="utf-8"))
        parent = json.loads(POST_Q4_T16_T22_TASK_GROUP.read_text(encoding="utf-8"))
        frozen = json.loads(POST_Q4_T17_FROZEN_HELDOUT_CORPUS.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
        registry_ru = (DOCS / "sources" / "registry.md").read_text(encoding="utf-8")
        registry_en = (DOCS / "sources" / "registry.en.md").read_text(encoding="utf-8")
        lifecycle = json.loads((ROOT / ".codex" / "product-agent-os" / "lifecycle-state.json").read_text(encoding="utf-8"))
        plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        runlog = (ROOT / "RUNLOG.md").read_text(encoding="utf-8")
        evals = (ROOT / "EVALS.md").read_text(encoding="utf-8")
        test_plan = (ROOT / "TEST.md").read_text(encoding="utf-8")
        current_state = (DOCS / "product-agent-os" / "control-plane-current-state.md").read_text(encoding="utf-8")
        coding_ru = (DOCS / "product-agent-os" / "coding-standards.md").read_text(encoding="utf-8")
        coding_en = (DOCS / "product-agent-os" / "coding-standards.en.md").read_text(encoding="utf-8")
        behavioral_ru = (DOCS / "product-agent-os" / "behavioral-evals.md").read_text(encoding="utf-8")
        behavioral_en = (DOCS / "product-agent-os" / "behavioral-evals.en.md").read_text(encoding="utf-8")
        track11 = (
            DOCS
            / "superpowers"
            / "plans"
            / "2026-06-20-track-11-documentation-architecture-refresh.md"
        ).read_text(encoding="utf-8")

        serialized = json.dumps(packet, sort_keys=True)
        self.assertEqual("batch45_postq4_t18_promotion_grade_eval_design_v1", packet["schema_version"])
        self.assertEqual("B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA", packet["task_id"])
        self.assertEqual("B45-POSTQ4-T18-A01", packet["evidence_id"])
        self.assertEqual("implemented_eval_design_strict_schema_no_run", packet["status"])
        self.assertEqual("docs_contract_ready", packet["closure_level"])
        self.assertIn("Context7 /websites/json-schema_understanding-json-schema", packet["basis"]["json_schema_reference"])
        self.assertTrue(packet["sidecar_agent_use"]["agent_outputs_are_supporting_review_only"])
        self.assertTrue(packet["sidecar_agent_use"]["source_artifacts_remain_authoritative"])

        comparison = packet["comparison_design"]
        self.assertEqual("same_model_baseline_treatment", comparison["selected_promotion_grade_comparison_mode"])
        self.assertTrue(comparison["promotion_grade_model_policy"]["same_model_required_for_baseline_and_treatment"])
        self.assertTrue(comparison["promotion_grade_model_policy"]["same_reasoning_effort_required_for_baseline_and_treatment"])
        self.assertTrue(comparison["promotion_grade_model_policy"]["same_tooling_and_runner_required_for_baseline_and_treatment"])
        self.assertEqual(
            "advisory_current_quality_signal_only_not_promotion_grade",
            comparison["promotion_grade_model_policy"]["allowed_current_model_comparison"],
        )
        self.assertEqual(frozen["corpus"]["corpus_id"], comparison["corpus_binding"]["corpus_id"])
        self.assertEqual(frozen["corpus"]["corpus_version"], comparison["corpus_binding"]["corpus_version"])
        self.assertEqual(8, comparison["corpus_binding"]["task_count"])
        self.assertTrue(comparison["corpus_binding"]["all_tasks_required_for_primary_promotion_decision"])

        strict_schema = packet["strict_output_schema"]
        self.assertEqual("batch45_postq4_promotion_grade_primary_result_v1", strict_schema["schema_id"])
        self.assertEqual("https://json-schema.org/draft/2020-12/schema", strict_schema["json_schema_dialect"])
        for keyword in ["type", "properties", "required", "enum", "minimum", "maximum", "items", "additionalProperties"]:
            self.assertIn(keyword, strict_schema["context7_keywords_used"])

        root_schema = strict_schema["root_schema"]
        self.assertEqual("object", root_schema["type"])
        self.assertFalse(root_schema["additionalProperties"])
        for required in [
            "schema_version",
            "corpus_id",
            "corpus_version",
            "task_id",
            "arm",
            "model_id",
            "model_reasoning_effort",
            "result_class",
            "changed_files",
            "behavior_score",
            "dimension_scores",
            "evidence_summary",
            "tests_or_checks",
            "unsupported_claims",
            "privacy_safety",
            "final_summary_retention",
        ]:
            self.assertIn(required, root_schema["required"])
        self.assertFalse(root_schema["properties"]["changed_files"]["items"]["additionalProperties"])
        self.assertFalse(root_schema["properties"]["dimension_scores"]["additionalProperties"])
        self.assertFalse(root_schema["properties"]["tests_or_checks"]["items"]["additionalProperties"])
        self.assertFalse(root_schema["properties"]["privacy_safety"]["additionalProperties"])

        runner_alignment = packet["runner_contract_alignment"]
        self.assertEqual("plugins/product-agent-os/scripts/codex_runtime_runner/model_output.py", runner_alignment["source"])
        self.assertEqual(LIVE_RUN_STATUS_VALUES, runner_alignment["live_run_status_values"])
        self.assertEqual(LIVE_RUN_REQUIRED_FIELDS, runner_alignment["live_run_required_fields"])
        self.assertEqual(PAIR_REQUIRED_FIELDS, runner_alignment["pair_required_fields"])
        self.assertEqual(AGGREGATE_REQUIRED_FIELDS, runner_alignment["aggregate_required_fields"])
        for forbidden_raw_field in [
            "stdout",
            "stderr",
            "prompt",
            "provider_payload",
            "raw_output",
            "raw_body",
            "final_summary",
        ]:
            self.assertIn(
                forbidden_raw_field,
                runner_alignment["raw_output_like_fields_forbidden_unless_hash_or_length_metadata"],
            )

        invalid_handling = packet["invalid_output_handling"]
        self.assertTrue(invalid_handling["deterministic_quarantine"])
        self.assertIn("schema_validation_failed", invalid_handling["invalid_classes"])
        self.assertTrue(invalid_handling["pair_policy"]["one_invalid_arm_invalidates_pair"])
        self.assertTrue(invalid_handling["pair_policy"]["invalid_pair_count_must_be_zero_for_promotion"])
        self.assertTrue(invalid_handling["pair_policy"]["reviewer_not_called_for_invalid_pairs"])

        for negative_case in [
            "missing_required_field",
            "unknown_additional_property",
            "invalid_status_enum",
            "final_json_marker_missing",
            "raw_output_like_field_present_without_hash_or_length_suffix",
            "absolute_user_specific_path_present",
            "reviewer_calls_started_with_invalid_pairs",
            "promotion_threshold_met_with_invalid_pairs",
        ]:
            self.assertIn(negative_case, packet["strict_schema_negative_cases"])

        threshold = packet["scoring_rubric"]["promotion_threshold"]
        self.assertEqual(20, threshold["minimum_average_score_delta_percent"])
        self.assertEqual(8, threshold["valid_pair_count_required"])
        self.assertEqual(0, threshold["invalid_pair_count_required"])
        self.assertEqual(0, threshold["timeout_count_required"])
        self.assertTrue(threshold["reviewer_gate_required"])
        self.assertTrue(threshold["same_model_comparability_required"])
        self.assertFalse(threshold["critical_privacy_or_unsupported_claim_failures_allowed"])
        self.assertEqual(8, len(packet["scoring_rubric"]["dimension_weights"]))

        reviewer = packet["reviewer_rubric"]
        self.assertTrue(reviewer["reviewer_gate_required_for_promotion"])
        self.assertEqual(["promotion_go", "no_go", "needs_rerun"], reviewer["reviewer_decision_enum"])
        self.assertEqual("promotion_go", reviewer["promotion_requires_reviewer_decision"])
        self.assertIn("raw reviewer traces", reviewer["reviewer_inputs_forbidden_in_repo"])

        privacy = packet["privacy_and_retention_design"]
        for forbidden_class in [
            "raw private source bodies",
            "secrets_or_credentials",
            "raw_model_outputs_or_provider_traces",
            "raw reviewer traces",
            "absolute_user_specific_paths",
            "raw prompts",
            "provider responses",
            "customer_user_data",
        ]:
            self.assertIn(forbidden_class, privacy["repo_forbidden_data_classes"])
        self.assertIn("hashes and byte lengths", privacy["repo_allowed_future_result_data"])

        result_contract = packet["future_result_contract"]
        self.assertEqual(
            "future docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-results.json",
            result_contract["result_packet_path"],
        )
        self.assertIn("no_unapproved_actions", result_contract["required_top_level_sections"])
        self.assertTrue(result_contract["t21_result_cannot_self_promote"])

        boundary = packet["approval_and_execution_boundary"]
        self.assertFalse(boundary["packet_authorizes_future_run"])
        self.assertFalse(boundary["baseline_or_treatment_run_started"])
        self.assertFalse(boundary["reviewer_gate_satisfied"])
        self.assertFalse(boundary["concrete_model_approved"])
        self.assertFalse(boundary["cost_timeout_retention_policy_ready"])
        self.assertEqual("B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY", boundary["next_required_task"])
        self.assertTrue(boundary["future_approval_required_before_T21"])
        self.assertIn("reviewer/model/provider calls", boundary["does_not_authorize"])

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)
        self.assertFalse(packet["no_unapproved_actions"]["raw_outputs_written_to_repo"])

        for unsupported in [
            "promotion_grade_eval_result_exists",
            "baseline_treatment_execution_started",
            "reviewer_gate_satisfied",
            "concrete_model_or_provider_approved",
            "cost_timeout_retention_policy_ready",
            "M26_no_go_reversed",
            "M35_no_go_reversed",
            "T15_no_go_reversed",
            "promotion_ready",
        ]:
            self.assertIn(unsupported, packet["unsupported_claims"])

        for forbidden_path_fragment in ["C:\\Users", "C:/Users", "\\Users\\"]:
            self.assertNotIn(forbidden_path_fragment, serialized)

        parent_rows = {task["task_id"]: task for task in parent["task_rows"]}
        self.assertEqual(
            "implemented_eval_design_strict_schema_no_run",
            parent_rows["B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA"]["status"],
        )
        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t18-promotion-grade-eval-design.json",
            parent_rows["B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA"]["evidence_owner"],
        )
        self.assertIn(
            parent["task_group"]["group_status"],
            {
                "t18_eval_design_strict_schema_ready_next_t19",
                "t19_cost_timeout_retention_ready_next_t20",
            },
        )

        update = next_tasks["execution_update"]
        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t18-promotion-grade-eval-design.json",
            update["latest_t18_eval_design"],
        )
        self.assertIn("B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA", update["executed_task_ids"])
        self.assertEqual(
            "implemented_eval_design_strict_schema_no_run",
            update["status_by_task"]["B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA"],
        )
        self.assertEqual("B45-POSTQ4-T18-A01", update["t18_eval_design"]["evidence_id"])
        self.assertEqual(
            "same_model_baseline_treatment",
            update["t18_eval_design"]["selected_promotion_grade_comparison_mode"],
        )
        self.assertEqual("batch45_postq4_promotion_grade_primary_result_v1", update["t18_eval_design"]["schema_id"])
        self.assertEqual(8, update["t18_eval_design"]["valid_pair_count_required"])
        self.assertEqual(0, update["t18_eval_design"]["invalid_pair_count_required"])
        self.assertEqual(20, update["t18_eval_design"]["minimum_average_score_delta_percent"])
        self.assertTrue(update["t18_eval_design"]["reviewer_gate_required"])
        self.assertFalse(update["t18_eval_design"]["promotion_allowed"])
        self.assertFalse(update["t18_eval_design"]["baseline_started"])
        self.assertFalse(update["t18_eval_design"]["treatment_started"])
        self.assertEqual("B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY", update["t18_eval_design"]["next_required_task"])

        for registry in [registry_ru, registry_en]:
            self.assertIn("B45-POSTQ4-T18-A01", registry)
            self.assertIn("docs/superpowers/specs/batch45-postq4-t18-promotion-grade-eval-design.json", registry)
            self.assertIn("same-model baseline/treatment", registry)
            self.assertIn("Context7 JSON Schema", registry)

        for control_plane in [
            plan,
            runlog,
            evals,
            test_plan,
            current_state,
            coding_ru,
            coding_en,
            track11,
        ]:
            self.assertIn("B45-POSTQ4-T18-A01", control_plane)

        for source_owner in [
            plan,
            test_plan,
            current_state,
            coding_ru,
            coding_en,
            behavioral_ru,
            behavioral_en,
            track11,
        ]:
            self.assertIn("batch45-postq4-t18-promotion-grade-eval-design.json", source_owner)

        self.assertNotIn("B45-POSTQ4-T18-A01", behavioral_ru)
        self.assertNotIn("B45-POSTQ4-T18-A01", behavioral_en)

        self.assertIn(
            lifecycle["task_id"],
            {
                "B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA",
                "B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY",
            },
        )
        self.assertIn(lifecycle["evidence_id"], {"B45-POSTQ4-T18-A01", "B45-POSTQ4-T19-A01"})
        self.assertIn(
            lifecycle["status"],
            {
                "implemented_eval_design_strict_schema_no_run",
                "implemented_cost_timeout_retention_policy_no_run",
            },
        )
        self.assertEqual("docs_contract_ready", lifecycle["closure_level"])

    def test_b45_postq4_t19_cost_timeout_retention_policy_is_no_run(self):
        packet = json.loads(POST_Q4_T19_POLICY.read_text(encoding="utf-8"))
        parent = json.loads(POST_Q4_T16_T22_TASK_GROUP.read_text(encoding="utf-8"))
        next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
        registry_ru = (DOCS / "sources" / "registry.md").read_text(encoding="utf-8")
        registry_en = (DOCS / "sources" / "registry.en.md").read_text(encoding="utf-8")
        lifecycle = json.loads((ROOT / ".codex" / "product-agent-os" / "lifecycle-state.json").read_text(encoding="utf-8"))
        plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        runlog = (ROOT / "RUNLOG.md").read_text(encoding="utf-8")
        evals = (ROOT / "EVALS.md").read_text(encoding="utf-8")
        test_plan = (ROOT / "TEST.md").read_text(encoding="utf-8")
        current_state = (DOCS / "product-agent-os" / "control-plane-current-state.md").read_text(encoding="utf-8")
        coding_ru = (DOCS / "product-agent-os" / "coding-standards.md").read_text(encoding="utf-8")
        coding_en = (DOCS / "product-agent-os" / "coding-standards.en.md").read_text(encoding="utf-8")
        behavioral_ru = (DOCS / "product-agent-os" / "behavioral-evals.md").read_text(encoding="utf-8")
        behavioral_en = (DOCS / "product-agent-os" / "behavioral-evals.en.md").read_text(encoding="utf-8")
        track11 = (
            DOCS
            / "superpowers"
            / "plans"
            / "2026-06-20-track-11-documentation-architecture-refresh.md"
        ).read_text(encoding="utf-8")

        serialized = json.dumps(packet, sort_keys=True)
        self.assertEqual("batch45_postq4_t19_cost_timeout_retention_policy_v1", packet["schema_version"])
        self.assertEqual("B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY", packet["task_id"])
        self.assertEqual("B45-POSTQ4-T19-A01", packet["evidence_id"])
        self.assertEqual("implemented_cost_timeout_retention_policy_no_run", packet["status"])
        self.assertEqual("docs_contract_ready", packet["closure_level"])
        self.assertIn("Context7 /websites/json-schema_understanding-json-schema", packet["basis"]["json_schema_reference"])
        self.assertTrue(packet["sidecar_agent_use"]["agent_outputs_are_supporting_review_only"])
        self.assertTrue(packet["sidecar_agent_use"]["source_artifacts_remain_authoritative"])

        budget = packet["run_budget_policy"]
        self.assertEqual(8, budget["max_baseline_primary_calls"])
        self.assertEqual(8, budget["max_treatment_primary_calls"])
        self.assertEqual(16, budget["max_primary_model_calls"])
        self.assertEqual(1, budget["max_reviewer_calls_after_valid_pairs"])
        self.assertEqual(17, budget["max_total_model_or_reviewer_calls"])
        self.assertEqual(0, budget["max_setup_or_smoke_calls"])
        self.assertEqual(0, budget["max_total_retries"])
        self.assertTrue(budget["no_implicit_retry_budget"])

        timeout = packet["timeout_policy"]
        self.assertEqual(600, timeout["per_primary_call_timeout_seconds"])
        self.assertEqual(600, timeout["per_reviewer_call_timeout_seconds"])
        self.assertEqual(12000, timeout["max_total_wall_clock_seconds"])
        self.assertTrue(timeout["stop_on_first_primary_timeout"])
        self.assertEqual(0, timeout["timeout_count_required_for_promotion"])
        self.assertFalse(timeout["timed_out_pair_valid_for_scoring"])

        cost = packet["cost_policy"]
        self.assertEqual("owner_fill_required_in_T20_exact_approval", cost["concrete_usd_cap_status"])
        self.assertTrue(cost["approval_not_executable_without_usd_cap"])
        self.assertTrue(cost["current_pricing_lookup_required_in_T20"])
        self.assertTrue(cost["abort_when_cost_unknown"])
        self.assertTrue(cost["cost_cap_breach_blocks_promotion"])

        retry_abort = packet["retry_and_abort_policy"]
        self.assertFalse(retry_abort["automatic_retries_allowed"])
        self.assertTrue(retry_abort["manual_rerun_requires_new_exact_approval"])
        self.assertEqual([], retry_abort["retryable_classes_under_this_policy"])
        for abort_condition in [
            "first_primary_timeout",
            "cost_unknown_before_or_after_call",
            "estimated_cost_cap_would_be_exceeded",
            "raw_output_retention_violation",
            "secret_or_unredacted_pii_detected",
        ]:
            self.assertIn(abort_condition, retry_abort["abort_conditions"])
        self.assertTrue(retry_abort["aborted_run_cannot_support_promotion"])

        retention = packet["raw_temp_only_retention_policy"]
        self.assertFalse(retention["raw_outputs_repo_retention_allowed"])
        self.assertTrue(retention["raw_outputs_temp_only"])
        self.assertEqual(0, retention["repo_raw_retention_bytes_allowed"])
        self.assertTrue(retention["concrete_temp_root_in_repo_artifact_forbidden"])
        self.assertEqual(24, retention["raw_retention_max_hours"])
        self.assertTrue(retention["delete_raw_on_success"])
        self.assertTrue(retention["delete_raw_on_abort"])
        for forbidden in [
            "raw stdout",
            "raw stderr",
            "raw prompts",
            "provider response bodies",
            "raw model outputs",
            "raw reviewer traces",
            "absolute_user_specific_paths",
        ]:
            self.assertIn(forbidden, retention["forbidden_repo_retention"])
        self.assertIn("hashes and byte lengths", retention["allowed_repo_retention"])

        rollup = packet["sanitized_rollup_contract"]
        self.assertIn("cost_timeout_retention", rollup["result_section_name"])
        for required in [
            "policy_evidence_id",
            "call_budget",
            "timeout_policy",
            "cost_policy",
            "retention_policy",
        ]:
            self.assertIn(required, rollup["strict_policy_schema"]["required"])
        self.assertFalse(rollup["strict_policy_schema"]["additionalProperties"])
        for forbidden_raw_field in ["stdout", "stderr", "prompt", "provider_payload", "raw_output", "raw_body"]:
            self.assertIn(forbidden_raw_field, rollup["forbidden_raw_field_names"])

        approval = packet["t20_exact_approval_requirements"]
        self.assertEqual("B45-POSTQ4-T20-EXACT-APPROVAL-PACKET", approval["next_required_task"])
        for required_approval_field in [
            "model_id",
            "model_reasoning_effort",
            "usd_cost_cap",
            "pricing_source_checked_at",
            "raw_temp_only_retention_policy",
            "abort_conditions",
        ]:
            self.assertIn(required_approval_field, approval["owner_confirmation_must_name"])
        self.assertTrue(approval["approval_packet_cannot_run_by_itself"])
        self.assertFalse(approval["approval_reuse_after_consumed_or_aborted_run_allowed"])

        boundary = packet["approval_and_execution_boundary"]
        self.assertFalse(boundary["packet_authorizes_future_run"])
        self.assertFalse(boundary["baseline_or_treatment_run_started"])
        self.assertFalse(boundary["reviewer_gate_satisfied"])
        self.assertFalse(boundary["concrete_model_approved"])
        self.assertFalse(boundary["concrete_usd_cost_cap_approved"])
        self.assertTrue(boundary["cost_timeout_retention_policy_ready"])
        self.assertEqual("B45-POSTQ4-T20-EXACT-APPROVAL-PACKET", boundary["next_required_task"])

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)
        self.assertFalse(packet["no_unapproved_actions"]["raw_outputs_written_to_repo"])

        for unsupported in [
            "promotion_grade_eval_result_exists",
            "baseline_treatment_execution_started",
            "reviewer_gate_satisfied",
            "concrete_model_or_provider_approved",
            "concrete_usd_cost_cap_approved",
            "M26_no_go_reversed",
            "M35_no_go_reversed",
            "T15_no_go_reversed",
            "promotion_ready",
        ]:
            self.assertIn(unsupported, packet["unsupported_claims"])

        for forbidden_path_fragment in ["C:\\Users", "C:/Users", "\\Users\\"]:
            self.assertNotIn(forbidden_path_fragment, serialized)

        parent_rows = {task["task_id"]: task for task in parent["task_rows"]}
        self.assertEqual(
            "implemented_cost_timeout_retention_policy_no_run",
            parent_rows["B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY"]["status"],
        )
        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t19-cost-timeout-retention-policy.json",
            parent_rows["B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY"]["evidence_owner"],
        )
        self.assertEqual("t19_cost_timeout_retention_ready_next_t20", parent["task_group"]["group_status"])

        update = next_tasks["execution_update"]
        self.assertEqual(
            "docs/superpowers/specs/batch45-postq4-t19-cost-timeout-retention-policy.json",
            update["latest_t19_cost_timeout_retention_policy"],
        )
        self.assertIn("B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY", update["executed_task_ids"])
        self.assertEqual(
            "implemented_cost_timeout_retention_policy_no_run",
            update["status_by_task"]["B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY"],
        )
        t19_rollup = update["t19_cost_timeout_retention_policy"]
        self.assertEqual("B45-POSTQ4-T19-A01", t19_rollup["evidence_id"])
        self.assertEqual(17, t19_rollup["max_total_model_or_reviewer_calls"])
        self.assertEqual(0, t19_rollup["max_total_retries"])
        self.assertEqual(600, t19_rollup["per_primary_call_timeout_seconds"])
        self.assertTrue(t19_rollup["raw_temp_only_retention_required"])
        self.assertTrue(t19_rollup["cost_timeout_retention_policy_ready"])
        self.assertFalse(t19_rollup["promotion_allowed"])
        self.assertFalse(t19_rollup["baseline_started"])
        self.assertFalse(t19_rollup["treatment_started"])
        self.assertEqual("B45-POSTQ4-T20-EXACT-APPROVAL-PACKET", t19_rollup["next_required_task"])

        for registry in [registry_ru, registry_en]:
            self.assertIn("B45-POSTQ4-T19-A01", registry)
            self.assertIn("docs/superpowers/specs/batch45-postq4-t19-cost-timeout-retention-policy.json", registry)
            self.assertIn("raw-temp-only retention", registry)

        for control_plane in [
            plan,
            runlog,
            evals,
            test_plan,
            current_state,
            coding_ru,
            coding_en,
            track11,
        ]:
            self.assertIn("B45-POSTQ4-T19-A01", control_plane)

        for source_owner in [
            plan,
            test_plan,
            current_state,
            coding_ru,
            coding_en,
            behavioral_ru,
            behavioral_en,
            track11,
        ]:
            self.assertIn("batch45-postq4-t19-cost-timeout-retention-policy.json", source_owner)

        self.assertNotIn("B45-POSTQ4-T19-A01", behavioral_ru)
        self.assertNotIn("B45-POSTQ4-T19-A01", behavioral_en)

        self.assertEqual("B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY", lifecycle["task_id"])
        self.assertEqual("B45-POSTQ4-T19-A01", lifecycle["evidence_id"])
        self.assertEqual("implemented_cost_timeout_retention_policy_no_run", lifecycle["status"])
        self.assertEqual("docs_contract_ready", lifecycle["closure_level"])

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
