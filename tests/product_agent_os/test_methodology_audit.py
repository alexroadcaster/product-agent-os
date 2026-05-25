import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


class MethodologyAuditContractTest(unittest.TestCase):
    def _domain_status(self, result, domain_id):
        domains = {domain["id"]: domain for domain in result["methodology_domains"]}
        return domains[domain_id]["status"]

    def _recommendation_by_gate(self, result, gate):
        for recommendation in result["recommendations"]:
            if recommendation["gate"] == gate:
                return recommendation
        self.fail(f"missing recommendation for gate {gate}")

    def test_empty_workspace_returns_baseline_simple_with_questions(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            result = build_methodology_audit(Path(tmp), intent_hint="new MVP idea")

        self.assertEqual(result["maturity_level"]["selected"], "baseline")
        self.assertEqual(result["complexity_profile"]["selected"], "simple")
        self.assertIn("delivery_map", result)
        self.assertIn("questions_for_owner", result)
        self.assertIn("safe_next_action", result)
        self.assertEqual(result["write_policy"], "read_only")

    def test_workspace_with_api_database_and_ci_routes_complex(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "openapi.yaml").write_text(
                "openapi: 3.1.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                encoding="utf-8",
            )
            (root / "migrations").mkdir()
            (root / "migrations" / "001_init.sql").write_text(
                "create table accounts(id text primary key);\n",
                encoding="utf-8",
            )
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
            result = build_methodology_audit(root, intent_hint="prepare for production API release")

        self.assertIn(result["maturity_level"]["selected"], ["team", "production"])
        self.assertIn(result["complexity_profile"]["selected"], ["complex", "high_risk"])
        domain_ids = [domain["id"] for domain in result["methodology_domains"] if domain["status"] != "not_applicable"]
        self.assertIn("api_integrations", domain_ids)
        self.assertIn("database_data", domain_ids)
        self.assertIn("delivery_release_operations", domain_ids)

    def test_recommendations_have_stable_shape(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"vitest"}}\n', encoding="utf-8")
            result = build_methodology_audit(root, intent_hint="ship frontend feature")

        required_keys = {
            "priority",
            "reason",
            "domain",
            "gate",
            "artifact",
            "evidence_required",
            "evidence_owner",
            "approval_boundary",
            "accepted_gap_option",
            "residual_risk",
            "safe_next_action",
        }
        self.assertGreaterEqual(len(result["recommendations"]), 1)
        for recommendation in result["recommendations"]:
            self.assertEqual(set(recommendation), required_keys)

    def test_business_product_intent_routes_domain_and_product_hypothesis_priority(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            discovery_result = build_methodology_audit(Path(tmp), intent_hint="new MVP idea")
            implementation_root = Path(tmp) / "implementation"
            implementation_root.mkdir()
            (implementation_root / "package.json").write_text('{"scripts":{"test":"vitest"}}\n', encoding="utf-8")
            implementation_result = build_methodology_audit(
                implementation_root,
                intent_hint="ship MVP product metric experiment",
            )

        self.assertNotEqual(self._domain_status(discovery_result, "business_product"), "not_applicable")
        self.assertNotEqual(self._domain_status(implementation_result, "business_product"), "not_applicable")
        self.assertEqual(
            self._recommendation_by_gate(discovery_result, "product_hypothesis_present")["priority"],
            "P2_recommended",
        )
        self.assertEqual(
            self._recommendation_by_gate(implementation_result, "product_hypothesis_present")["priority"],
            "P1_high_risk",
        )

    def test_business_product_metric_ai_analytics_and_release_claims_create_recommendations(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"vitest"}}\n', encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "ship AI product analytics dashboard with usage events and product success "
                    "metric after release without telemetry and workflow promotion"
                ),
            )

        expected = {
            "metric_hardening_when_product_behavior_changes": ("P1_high_risk", "metric-spec.md"),
            "ai_product_eval_when_ai_behavior_changes": ("P1_high_risk", "ai-eval-spec.md"),
            "analytics_tracking_plan_present": ("P1_high_risk", "tracking-plan.md"),
            "release_measurement_evidence_present": ("P1_high_risk", "RUNLOG.md"),
            "decision_horizon_present": ("P2_recommended", "product-brief.md"),
            "outcome_metric_level_separated": ("P2_recommended", "metric-spec.md"),
            "metric_scope_classified": ("P1_high_risk", "REQUIREMENTS.md"),
            "workflow_promotion_value_evidence_present": ("P2_recommended", "skill-promotion-record.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

    def test_business_product_false_positive_intents_are_not_applicable(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        for intent in [
            "typo-only docs edit",
            "formatting-only markdown cleanup",
            "dependency pin without behavior impact",
        ]:
            with self.subTest(intent=intent):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "README.md").write_text("# Demo\n", encoding="utf-8")
                    result = build_methodology_audit(root, intent_hint=intent)

                self.assertEqual(self._domain_status(result, "business_product"), "not_applicable")

    def test_requirements_domain_behavior_intent_routes_domain_and_blocks_missing_scenarios(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"vitest"}}\n', encoding="utf-8")
            result = build_methodology_audit(root, intent_hint="ship user behavior change")

        self.assertNotEqual(self._domain_status(result, "requirements_domain"), "not_applicable")
        recommendation = self._recommendation_by_gate(result, "acceptance_scenarios_when_behavior_changes")
        self.assertEqual(recommendation["priority"], "P0_blocker")
        self.assertEqual(recommendation["artifact"], "acceptance-scenarios.md")

    def test_requirements_domain_risky_public_contract_work_requires_ids_quality_and_constraints(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "openapi.yaml").write_text(
                "openapi: 3.1.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                encoding="utf-8",
            )
            result = build_methodology_audit(
                root,
                intent_hint="regulatory multi-slice public API requirement with privacy rollback constraints",
            )

        expected = {
            "requirement_quality_present": ("P1_high_risk", "requirement-registry.md"),
            "requirement_ids_present": ("P1_high_risk", "requirement-registry.md"),
            "constraints_traceability_present": ("P1_high_risk", "requirements-traceability-matrix.md"),
            "api_ui_data_traceability_present": ("P1_high_risk", "requirements-traceability-matrix.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

    def test_requirements_domain_story_domain_event_and_owner_review_recommendations(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"pytest"}}\n', encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "unclear large disputed user story with MVP deferred slices and business rule "
                    "for payment domain event across boundary from AI generated finance legal claim"
                ),
            )

        expected = {
            "stakeholder_owner_map_present": ("P2_recommended", "stakeholder-owner-map.md"),
            "story_slice_map_present": ("P2_recommended", "story-slice-map.md"),
            "example_mapping_when_unclear_story": ("P2_recommended", "example-map.md"),
            "business_rules_present": ("P1_high_risk", "business-rules.md"),
            "domain_event_contracts_present": ("P1_high_risk", "requirements-traceability-matrix.md"),
            "domain_expert_review_present": ("P1_high_risk", "domain-review-record.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

    def test_requirements_domain_change_impact_accepted_gap_and_declarative_scenario_recommendations(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"pytest"}}\n', encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "requirement changed after planning with accepted gap missing review date "
                    "and acceptance scenario using css selector database table function name test harness"
                ),
            )

        expected = {
            "requirement_change_impact_review_present": ("P1_high_risk", "requirement-change-impact.md"),
            "accepted_gap_recorded": ("P1_high_risk", "domain-review-record.md"),
            "declarative_acceptance_scenarios_present": ("P1_high_risk", "acceptance-scenarios.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

    def test_requirements_domain_false_positive_intents_are_not_applicable_for_readme_only_work(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        for intent in [
            "typo-only docs edit",
            "formatting-only markdown cleanup",
            "dependency metadata without behavior impact",
        ]:
            with self.subTest(intent=intent):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "README.md").write_text("# Demo\n", encoding="utf-8")
                    result = build_methodology_audit(root, intent_hint=intent)

                self.assertEqual(self._domain_status(result, "requirements_domain"), "not_applicable")

    def test_requirements_domain_rejects_unsupported_methodology_claims_as_evidence(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        unsupported_claims = [
            "BDD replaces testing",
            "Gherkin is mandatory",
            "user story template is complete requirement",
            "glossary is ubiquitous language",
            "OpenAPI is requirements source of truth",
        ]
        for claim in unsupported_claims:
            with self.subTest(claim=claim):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "package.json").write_text('{"scripts":{"test":"pytest"}}\n', encoding="utf-8")
                    result = build_methodology_audit(root, intent_hint=claim)

                recommendation = self._recommendation_by_gate(result, "unsupported_claims_rejected")
                self.assertEqual(recommendation["priority"], "P1_high_risk")
                self.assertEqual(recommendation["artifact"], "domain-review-record.md")

    def test_solution_architecture_recommends_boundary_decision_runtime_and_evidence_artifacts(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"vitest"}}\n', encoding="utf-8")
            (root / "openapi.yaml").write_text(
                "openapi: 3.1.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                encoding="utf-8",
            )
            (root / "migrations").mkdir()
            (root / "migrations" / "001_split_orders.sql").write_text("alter table orders add column region text;\n")
            (root / "docs").mkdir()
            (root / "docs" / "context.mmd").write_text("flowchart LR\n  A-->B\n", encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "ship multi-service public API service split with generated client, persistent data, "
                    "PII, trust boundary, observability, runtime topology, ADR, rollback and parallel agent ownership"
                ),
            )

        self.assertNotEqual(self._domain_status(result, "solution_architecture"), "not_applicable")
        expected = {
            "solution_architecture_scope_present": ("P1_high_risk", "architecture-overview.md"),
            "architecture_context_view_present": ("P1_high_risk", "architecture-overview.md"),
            "architecture_container_boundary_present": ("P1_high_risk", "architecture-overview.md"),
            "boundary_responsibility_owner_present": ("P1_high_risk", "architecture-review-record.md"),
            "public_contract_boundary_trace_present": ("P1_high_risk", "api-contract-review.md"),
            "data_ownership_boundary_present": ("P1_high_risk", "database-dictionary.md"),
            "trust_boundary_security_review_present": ("P1_high_risk", "trust-boundary-map.md"),
            "adr_for_architecture_decision": ("P1_high_risk", "adr.md"),
            "observability_architecture_present": ("P1_high_risk", "architecture-fitness-functions.md"),
            "migration_rollback_path_present": ("P1_high_risk", "migration-plan.md"),
            "diagram_render_check_present": ("P2_recommended", "architecture-docs-tooling-decision.md"),
            "architecture_fitness_function_present": ("P2_recommended", "architecture-fitness-functions.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

    def test_solution_architecture_false_positive_intents_are_not_applicable(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        for intent in [
            "typo-only docs edit",
            "formatting-only markdown cleanup",
            "docs-light prototype without reviewed/diffable diagrams",
            "non-cloud work without Well-Architected review",
        ]:
            with self.subTest(intent=intent):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "README.md").write_text("# Demo\n", encoding="utf-8")
                    result = build_methodology_audit(root, intent_hint=intent)

                self.assertEqual(self._domain_status(result, "solution_architecture"), "not_applicable")

    def test_solution_architecture_rejects_unsupported_methodology_claims_as_evidence(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        unsupported_claims = [
            "Architecture means diagrams",
            "rendered diagram proves correctness",
            "C4 code diagrams are always required",
            "ADR is bureaucracy",
            "Well-Architected review proves architecture quality",
            "Architecture-as-code is always required",
            "AI can design architecture from chat alone",
        ]
        for claim in unsupported_claims:
            with self.subTest(claim=claim):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "package.json").write_text('{"scripts":{"test":"pytest"}}\n', encoding="utf-8")
                    result = build_methodology_audit(root, intent_hint=claim)

                recommendation = self._recommendation_by_gate(result, "unsupported_architecture_claims_rejected")
                self.assertEqual(recommendation["priority"], "P1_high_risk")
                self.assertEqual(recommendation["artifact"], "architecture-review-record.md")

    def test_quality_testing_evals_recommends_gate_priority_and_artifact_mapping(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"name":"quality-fixture"}\n', encoding="utf-8")
            (root / "src").mkdir()
            (root / "src" / "checkout.py").write_text("def total():\n    return 0\n", encoding="utf-8")
            (root / "openapi.yaml").write_text(
                "openapi: 3.1.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                encoding="utf-8",
            )
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "ship risky broad constrained public UI API schema deterministic bugfix business rule "
                    "runtime behavior manual QA visual accessibility AI eval baseline rerun release shared branch "
                    "flaky retry coverage proves correctness 100 percent line coverage test data privacy "
                    "regression impact completion ready quality claim"
                ),
            )

        self.assertNotEqual(self._domain_status(result, "quality_testing_evals"), "not_applicable")
        expected = {
            "quality_strategy_present": ("P0_blocker", "quality-strategy.md"),
            "risk_based_scope_present": ("P1_high_risk", "quality-strategy.md"),
            "acceptance_traceability_present": ("P1_high_risk", "test-eval-matrix.md"),
            "test_first_or_gap_present": ("P1_high_risk", "test-eval-matrix.md"),
            "contract_check_present": ("P1_high_risk", "api-contract-review.md"),
            "runtime_evidence_present": ("P1_high_risk", "manual-qa-evidence.md"),
            "manual_qa_evidence_present": ("P2_recommended", "manual-qa-evidence.md"),
            "visual_a11y_evidence_present": ("P1_high_risk", "manual-qa-evidence.md"),
            "eval_spec_present": ("P1_high_risk", "ai-eval-spec.md"),
            "eval_rerun_evidence_present": ("P1_high_risk", "EVALS.md"),
            "ci_quality_gate_present": ("P1_high_risk", "ci-evidence-record.md"),
            "flaky_test_policy_present": ("P2_recommended", "flaky-test-policy.md"),
            "coverage_policy_present": ("P2_recommended", "quality-strategy.md"),
            "test_data_privacy_present": ("P1_high_risk", "quality-strategy.md"),
            "bug_reproduction_evidence_present": ("P0_blocker", "bug-rescue-report.md"),
            "regression_impact_present": ("P1_high_risk", "test-eval-matrix.md"),
            "current_evidence_before_completion": ("P0_blocker", "RUNLOG.md"),
            "unsupported_quality_claims_rejected": ("P1_high_risk", "quality-strategy.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

        flaky = self._recommendation_by_gate(result, "flaky_test_policy_present")
        self.assertIn("owner", " ".join(flaky["evidence_required"]).lower())
        self.assertIn("expiry", " ".join(flaky["evidence_required"]).lower())

    def test_quality_testing_evals_false_positive_intents_are_not_applicable(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        for intent in [
            "typo-only docs edit",
            "formatting-only markdown cleanup",
            "docs-only source cleanup",
            "dependency metadata without behavior impact",
        ]:
            with self.subTest(intent=intent):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "README.md").write_text("# Demo\n", encoding="utf-8")
                    result = build_methodology_audit(root, intent_hint=intent)

                self.assertEqual(self._domain_status(result, "quality_testing_evals"), "not_applicable")
                quality_recommendations = [
                    item for item in result["recommendations"] if item["domain"] == "quality_testing_evals"
                ]
                self.assertEqual(quality_recommendations, [])

    def test_quality_testing_evals_uses_lower_visual_priority_for_internal_ui(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"vitest"}}\n', encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint="internal UI layout change with visual accessibility evidence gap",
            )

        recommendation = self._recommendation_by_gate(result, "visual_a11y_evidence_present")
        self.assertEqual(recommendation["priority"], "P2_recommended")
        self.assertEqual(recommendation["artifact"], "manual-qa-evidence.md")

    def test_codex_agentic_workflow_recommends_gate_priority_and_artifact_mapping(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"pytest"}}\n', encoding="utf-8")
            (root / ".codex" / "agents").mkdir(parents=True)
            (root / ".codex" / "agents" / "builder.toml").write_text("name = 'builder'\n", encoding="utf-8")
            (root / ".mcp.json").write_text('{"servers":{"remote":{"command":"npx"}}}\n', encoding="utf-8")
            (root / "hooks.json").write_text('{"hooks":{"PreToolUse":[]}}\n', encoding="utf-8")
            (root / ".codex-plugin").mkdir()
            (root / ".codex-plugin" / "plugin.json").write_text('{"name":"demo"}\n', encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "Codex App CLI IDE extension subagents parallel worker overlap MCP side-effecting tool "
                    "remote MCP auth secrets hook activation blocking hook plugin packaging repeated workflow "
                    "skill promotion automation schedule external write production data model reasoning memory "
                    "is source of truth Agents SDK app orchestration tool call handoff correctness completion "
                    "ready inspection proves completion"
                ),
            )

        self.assertNotEqual(self._domain_status(result, "codex_agentic_workflow"), "not_applicable")
        expected = {
            "agentic_scope_classified": ("P1_high_risk", "PLAN.md"),
            "control_plane_present": ("P0_blocker", "AGENTS.md"),
            "source_of_truth_present": ("P0_blocker", "AGENTS.md"),
            "read_only_discovery_complete": ("P1_high_risk", "RUNLOG.md"),
            "model_reasoning_policy_present": ("P1_high_risk", "model-reasoning-policy.md"),
            "fresh_context_handoff_present": ("P1_high_risk", "agent-task-packet.md"),
            "ownership_split_present": ("P1_high_risk", "worktree-ownership.md"),
            "subagent_parallelism_safe": ("P1_high_risk", "worktree-ownership.md"),
            "approval_boundary_present": ("P0_blocker", "approval-record.md"),
            "mcp_permission_review_present": ("P1_high_risk", "mcp-permission-review.md"),
            "hook_activation_approval_present": ("P1_high_risk", "hook-governance.md"),
            "plugin_boundary_present": ("P2_recommended", "plugin-blueprint.md"),
            "skill_promotion_evidence_present": ("P2_recommended", "skill-promotion-record.md"),
            "automation_manual_stability_present": ("P1_high_risk", "automation-candidate.md"),
            "agent_eval_workflow_present": ("P1_high_risk", "agent-eval-workflow.md"),
            "memory_policy_present": ("P1_high_risk", "AGENTS.md"),
            "agentic_evidence_before_completion": ("P0_blocker", "RUNLOG.md"),
            "unsupported_agentic_claims_rejected": ("P1_high_risk", "model-reasoning-policy.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)
                self.assertIn("approval", recommendation["approval_boundary"].lower())

    def test_codex_agentic_workflow_false_positive_intents_are_not_applicable(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        for intent in [
            "typo-only docs edit without Codex workflow change",
            "single local deterministic command without agent delegation",
            "read-only research without staged artifacts or external writes",
        ]:
            with self.subTest(intent=intent):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "README.md").write_text("# Demo\n", encoding="utf-8")
                    result = build_methodology_audit(root, intent_hint=intent)

                self.assertEqual(self._domain_status(result, "codex_agentic_workflow"), "not_applicable")
                workflow_recommendations = [
                    item for item in result["recommendations"] if item["domain"] == "codex_agentic_workflow"
                ]
                self.assertEqual(workflow_recommendations, [])

    def test_codex_agentic_workflow_rejects_unsupported_claims_as_evidence(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        unsupported_claims = [
            "memory is project source of truth",
            "subagents are automatically faster",
            "MCP tools are safe because they are tools",
            "hooks are harmless convenience scripts",
            "repeated workflow should become automation immediately",
            "Agents SDK and Codex runtime are the same layer",
            "inspection proves completion",
        ]
        for claim in unsupported_claims:
            with self.subTest(claim=claim):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / ".codex" / "agents").mkdir(parents=True)
                    (root / ".codex" / "agents" / "builder.toml").write_text(
                        "name = 'builder'\n",
                        encoding="utf-8",
                    )
                    result = build_methodology_audit(root, intent_hint=claim)

                recommendation = self._recommendation_by_gate(result, "unsupported_agentic_claims_rejected")
                self.assertEqual(recommendation["priority"], "P1_high_risk")
                self.assertEqual(recommendation["artifact"], "model-reasoning-policy.md")

    def test_frontend_recommends_gate_priority_and_artifact_mapping(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text(
                '{"dependencies":{"react":"latest","@storybook/react":"latest","@playwright/test":"latest"}}\n',
                encoding="utf-8",
            )
            (root / ".storybook").mkdir()
            (root / ".storybook" / "main.ts").write_text("export default {};\n", encoding="utf-8")
            (root / "playwright.config.ts").write_text("export default {};\n", encoding="utf-8")
            (root / "src" / "pages" / "checkout").mkdir(parents=True)
            (root / "src" / "pages" / "checkout" / "CheckoutPage.tsx").write_text(
                "export const CheckoutPage = () => null;\n",
                encoding="utf-8",
            )
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "ship public frontend route page reusable component design-system primitive token variant "
                    "FSD API data contract accessibility keyboard focus responsive visual runtime console "
                    "interaction test performance browser support i18n long text state ownership ready"
                ),
            )

        self.assertNotEqual(self._domain_status(result, "frontend"), "not_applicable")
        expected = {
            "frontend_user_flow_acceptance_present": ("P0_blocker", "frontend-flow-spec.md"),
            "frontend_component_state_matrix_present": ("P1_high_risk", "frontend-state-matrix.md"),
            "frontend_component_docs_present": ("P1_high_risk", "component-card.md"),
            "frontend_design_system_boundary_present": ("P1_high_risk", "component-card.md"),
            "frontend_fsd_boundary_reviewed": ("P2_recommended", "component-card.md"),
            "frontend_api_contract_alignment_present": ("P1_high_risk", "frontend-flow-spec.md"),
            "frontend_accessibility_review_present": ("P1_high_risk", "frontend-accessibility-review.md"),
            "frontend_keyboard_focus_contract_present": ("P1_high_risk", "frontend-accessibility-review.md"),
            "frontend_responsive_viewport_matrix_present": ("P1_high_risk", "frontend-visual-qa.md"),
            "frontend_visual_evidence_present": ("P1_high_risk", "frontend-visual-qa.md"),
            "frontend_runtime_console_evidence_present": ("P0_blocker", "frontend-visual-qa.md"),
            "frontend_interaction_test_evidence_present": ("P1_high_risk", "test-eval-matrix.md"),
            "frontend_performance_budget_present": ("P1_high_risk", "frontend-performance-budget.md"),
            "frontend_browser_support_present": ("P2_recommended", "frontend-visual-qa.md"),
            "frontend_content_i18n_boundary_present": ("P2_recommended", "frontend-flow-spec.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

        runtime = self._recommendation_by_gate(result, "frontend_runtime_console_evidence_present")
        self.assertIn("console status", " ".join(runtime["evidence_required"]).lower())
        self.assertIn("trace", " ".join(runtime["evidence_required"]).lower())
        design = self._recommendation_by_gate(result, "frontend_design_system_boundary_present")
        self.assertIn("token owner", " ".join(design["evidence_required"]).lower())
        self.assertIn("migration", " ".join(design["evidence_required"]).lower())

    def test_frontend_false_positive_intents_are_not_applicable(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        cases = [
            ("backend-only service worker queue work", {"pyproject.toml": "[project]\nname='api'\n"}),
            ("data-only migration and backfill", {"migrations/001.sql": "create table users(id text);\n"}),
            ("CLI-only command parser", {"src/cli.py": "print('Synthetic')\n"}),
            ("docs-only markdown cleanup", {"README.md": "# Synthetic docs\n"}),
            ("native-only Android iOS feature", {"android/app/build.gradle": "plugins {}\n"}),
            ("dependency metadata without UI behavior impact", {"package.json": "{}\n"}),
            (
                "simple CRUD without non-trivial frontend state",
                {
                    "package.json": '{"dependencies":{"react":"latest"}}\n',
                    "src/App.tsx": "export const App = () => null;\n",
                },
            ),
        ]
        for intent, files in cases:
            with self.subTest(intent=intent), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                for relative, text in files.items():
                    path = root / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(text, encoding="utf-8")

                result = build_methodology_audit(root, intent_hint=intent)

                self.assertEqual(self._domain_status(result, "frontend"), "not_applicable")
                frontend_recommendations = [
                    item for item in result["recommendations"] if item["domain"] == "frontend"
                ]
                self.assertEqual(frontend_recommendations, [])

    def test_frontend_rejects_unsupported_claims_as_evidence(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        unsupported_claims = [
            "FSD should be mandatory for every frontend project",
            "Storybook proves UI quality by itself",
            "automated a11y addon output is enough",
            "a desktop screenshot proves responsive UI",
            "lab Web Vitals always represent production UX",
            "code inspection proves UI completion",
        ]
        for claim in unsupported_claims:
            with self.subTest(claim=claim), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "package.json").write_text('{"dependencies":{"react":"latest"}}\n', encoding="utf-8")
                result = build_methodology_audit(root, intent_hint=claim)

                recommendation = self._recommendation_by_gate(result, "unsupported_frontend_claims_rejected")
                self.assertEqual(recommendation["priority"], "P1_high_risk")
                self.assertEqual(recommendation["artifact"], "frontend-visual-qa.md")

    def test_backend_recommends_gate_priority_and_artifact_mapping(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pyproject.toml").write_text("[project]\nname='orders-api'\n", encoding="utf-8")
            (root / "server").mkdir()
            (root / "server" / "app.py").write_text("def app():\n    return None\n", encoding="utf-8")
            (root / "workers").mkdir()
            (root / "workers" / "email_worker.py").write_text("def run():\n    return None\n", encoding="utf-8")
            (root / "Dockerfile").write_text("FROM python:3.12\n", encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "ship production backend service worker queue scheduler remote dependency retry timeout "
                    "idempotency backpressure ordering replay observability traces metrics logs correlation "
                    "SLO health check readiness liveness config secret auth payment external write migration "
                    "rollback API event contract storage external adapter"
                ),
            )

        self.assertNotEqual(self._domain_status(result, "backend"), "not_applicable")
        expected = {
            "backend_service_boundary_present": ("P0_blocker", "backend-service-overview.md"),
            "backend_runtime_behavior_present": ("P0_blocker", "backend-runtime-behavior.md"),
            "backend_dependency_failure_matrix_present": ("P1_high_risk", "backend-dependency-failure-matrix.md"),
            "backend_observability_contract_present": ("P1_high_risk", "backend-observability-map.md"),
            "backend_slo_or_gap_present": ("P1_high_risk", "backend-slo-sheet.md"),
            "backend_health_probe_contract_present": ("P1_high_risk", "backend-health-check-contract.md"),
            "backend_job_queue_contract_present": ("P1_high_risk", "backend-job-queue-contract.md"),
            "backend_data_consistency_strategy_present": ("P1_high_risk", "backend-data-consistency-record.md"),
            "backend_config_secrets_boundary_present": ("P1_high_risk", "backend-config-secrets-manifest.md"),
            "backend_security_reviewed": ("P1_high_risk", "security-risk-review.md"),
            "backend_rollback_plan_present": ("P1_high_risk", "backend-release-rollback-notes.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

        boundary = self._recommendation_by_gate(result, "backend_service_boundary_present")
        self.assertIn("owner", " ".join(boundary["evidence_required"]).lower())
        self.assertIn("data ownership", " ".join(boundary["evidence_required"]).lower())
        runtime = self._recommendation_by_gate(result, "backend_runtime_behavior_present")
        self.assertIn("idempotency", " ".join(runtime["evidence_required"]).lower())
        self.assertIn("replay", " ".join(runtime["evidence_required"]).lower())
        quality = self._recommendation_by_gate(result, "backend_observability_contract_present")
        self.assertIn("correlation", " ".join(quality["evidence_required"]).lower())
        self.assertIn("redaction", " ".join(quality["evidence_required"]).lower())

    def test_backend_false_positive_intents_are_not_applicable(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        cases = [
            ("frontend-only route component", {"package.json": '{"dependencies":{"react":"latest"}}\n'}),
            ("docs-only backend architecture article", {"docs/backend-notes.md": "# Backend article\n"}),
            ("CLI-only command parser", {"src/cli.py": "print('Synthetic')\n"}),
            ("native-only Android iOS feature", {"android/app/build.gradle": "plugins {}\n"}),
            ("dependency metadata without backend runtime behavior", {"requirements.txt": "requests==2.0\n"}),
            ("package-name-only service folder without runtime evidence", {"services/README.md": "# Service docs\n"}),
        ]
        for intent, files in cases:
            with self.subTest(intent=intent), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                for relative, text in files.items():
                    path = root / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(text, encoding="utf-8")

                result = build_methodology_audit(root, intent_hint=intent)

                self.assertEqual(self._domain_status(result, "backend"), "not_applicable")
                backend_recommendations = [
                    item for item in result["recommendations"] if item["domain"] == "backend"
                ]
                self.assertEqual(backend_recommendations, [])

    def test_backend_rejects_unsupported_claims_as_evidence(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        unsupported_claims = [
            "Backend means only business logic files",
            "Microservices are the professional default",
            "Retries make systems reliable",
            "Health endpoint exists, so readiness is solved",
            "Logs are observability",
            "SLOs are only for large companies",
        ]
        for claim in unsupported_claims:
            with self.subTest(claim=claim), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "server").mkdir()
                (root / "server" / "app.py").write_text("def app():\n    return None\n", encoding="utf-8")
                result = build_methodology_audit(root, intent_hint=claim)

                recommendation = self._recommendation_by_gate(result, "unsupported_backend_claims_rejected")
                self.assertEqual(recommendation["priority"], "P1_high_risk")
                self.assertEqual(recommendation["artifact"], "backend-service-overview.md")


if __name__ == "__main__":
    unittest.main()
