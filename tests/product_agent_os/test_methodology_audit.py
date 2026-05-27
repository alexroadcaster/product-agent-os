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

    def _recommendation_by_domain_gate(self, result, domain, gate):
        for recommendation in result["recommendations"]:
            if recommendation["domain"] == domain and recommendation["gate"] == gate:
                return recommendation
        self.fail(f"missing recommendation for domain {domain} gate {gate}")

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

    def test_backend_security_approval_and_secrets_policy_depth(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "server").mkdir()
            (root / "server" / "app.py").write_text("def app():\n    return None\n", encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "production backend auth tokens PII money movement privileged operations "
                    "external writes irreversible side effects secrets config"
                ),
            )

        security = self._recommendation_by_gate(result, "backend_security_reviewed")
        config = self._recommendation_by_gate(result, "backend_config_secrets_boundary_present")
        for expected in [
            "authn/authz",
            "tokens",
            "PII",
            "money movement",
            "privileged operations",
            "external writes",
            "irreversible side effects",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected.lower(), " ".join(security["evidence_required"]).lower())
        self.assertIn("private customer data", config["residual_risk"].lower())
        self.assertIn("docs, prompts, fixtures and logs", config["residual_risk"].lower())
        self.assertIn("approval_required", security["approval_boundary"])

    def test_backend_modular_ports_and_runtime_policy_recommendations(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "server").mkdir()
            (root / "server" / "app.py").write_text("def app():\n    return None\n", encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "production backend microservice ports adapters DDD retry timeout idempotency "
                    "backpressure ordering poison message replay"
                ),
            )

        boundary = self._recommendation_by_gate(result, "backend_service_boundary_present")
        runtime = self._recommendation_by_gate(result, "backend_runtime_behavior_present")
        boundary_evidence = " ".join(boundary["evidence_required"]).lower()
        runtime_evidence = " ".join(runtime["evidence_required"]).lower()
        for expected in [
            "modular monolith default",
            "microservice rationale",
            "independent deploy/scale/team/ownership evidence",
            "owner review",
            "adr",
            "ports/adapters boundary",
            "domain logic independent from http/db/queue/vendor sdk",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, boundary_evidence)
        for expected in [
            "timeout",
            "backoff/max attempts",
            "idempotency",
            "deduplication",
            "ordering",
            "backpressure",
            "poison message",
            "replay/recovery",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, runtime_evidence)

    def test_backend_resilience_ops_twelve_factor_and_owner_review_recommendations(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "server").mkdir()
            (root / "server" / "app.py").write_text("def app():\n    return None\n", encoding="utf-8")
            (root / "workers").mkdir()
            (root / "workers" / "sync_worker.py").write_text("def run():\n    return None\n", encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "production backend new changed responsibility remote dependency timeout retry backoff "
                    "max attempts circuit breaker fallback alert queue job DLQ dead-letter poison message "
                    "deduplication ordering backpressure payload idempotency replay local transaction outbox "
                    "saga compensation reconciliation migration impact observability traces metrics logs "
                    "correlation alert ownership no-private-payload logging SLI SLO explicit gap health "
                    "liveness readiness startup operational owner escalation rollback command manual procedure "
                    "data recovery irreversible side effects owner approval Twelve-Factor explicit dependencies "
                    "build-release-run process model admin tasks dev/prod parity logs-as-event-stream ADR "
                    "decision authority boundary rationale"
                ),
            )

        boundary = self._recommendation_by_gate(result, "backend_service_boundary_present")
        runtime = self._recommendation_by_gate(result, "backend_runtime_behavior_present")
        dependency = self._recommendation_by_gate(result, "backend_dependency_failure_matrix_present")
        observability = self._recommendation_by_gate(result, "backend_observability_contract_present")
        slo = self._recommendation_by_gate(result, "backend_slo_or_gap_present")
        health = self._recommendation_by_gate(result, "backend_health_probe_contract_present")
        queue = self._recommendation_by_gate(result, "backend_job_queue_contract_present")
        consistency = self._recommendation_by_gate(result, "backend_data_consistency_strategy_present")
        config = self._recommendation_by_gate(result, "backend_config_secrets_boundary_present")
        rollback = self._recommendation_by_gate(result, "backend_rollback_plan_present")

        expected_by_recommendation = {
            "boundary": (
                boundary,
                [
                    "changed backend responsibility",
                    "owner review",
                    "decision authority",
                    "boundary rationale",
                    "adr link or accepted gap",
                    "twelve-factor vocabulary",
                    "explicit dependencies",
                ],
            ),
            "runtime": (
                runtime,
                [
                    "process model",
                    "admin tasks",
                    "logs-as-event-stream",
                    "stateless process or accepted gap",
                ],
            ),
            "dependency": (
                dependency,
                [
                    "per dependency",
                    "timeout",
                    "retry/backoff/max attempts",
                    "circuit breaker non-applicability",
                    "fallback",
                    "alert owner",
                    "verification evidence",
                ],
            ),
            "observability": (
                observability,
                [
                    "traces",
                    "metrics",
                    "logs",
                    "correlation IDs",
                    "alert ownership",
                    "no-private-payload logging",
                    "logs alone are not accepted as observability",
                ],
            ),
            "slo": (
                slo,
                [
                    "SLI/SLO or explicit gap",
                    "user journey",
                    "user-relevant SLI",
                    "SLO target",
                    "no-telemetry or not-yet-production gap",
                ],
            ),
            "health": (
                health,
                [
                    "health endpoint semantics",
                    "liveness",
                    "readiness",
                    "startup",
                    "platform equivalent",
                    "test evidence or accepted gap",
                ],
            ),
            "queue": (
                queue,
                [
                    "payload contract",
                    "retry policy",
                    "dead-letter behavior",
                    "dead-letter queue",
                    "idempotency key",
                    "replay procedure",
                    "poison-message handling",
                ],
            ),
            "consistency": (
                consistency,
                [
                    "local transaction",
                    "outbox",
                    "saga",
                    "compensation",
                    "monitoring",
                    "reconciliation",
                    "migration impact",
                    "recovery path",
                ],
            ),
            "config": (
                config,
                [
                    "config/env keys without values",
                    "explicit dependencies",
                    "build-release-run boundary",
                    "dev/prod parity",
                    "secret source",
                ],
            ),
            "rollback": (
                rollback,
                [
                    "rollback trigger",
                    "rollback command or manual procedure",
                    "data recovery/replay",
                    "irreversible side effects",
                    "owner approval",
                    "residual risk",
                ],
            ),
        }
        for name, (recommendation, expected_terms) in expected_by_recommendation.items():
            evidence = " ".join(recommendation["evidence_required"]).lower()
            for expected in expected_terms:
                with self.subTest(recommendation=name, expected=expected):
                    self.assertIn(expected.lower(), evidence)

    def test_backend_intake_security_ops_contract_and_health_recommendations(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "server").mkdir()
            (root / "server" / "app.py").write_text("def app():\n    return None\n", encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "production backend service/user behavior affected backend unit dependencies data stores "
                    "runtime constraints operational assumptions explicit gaps security authn authz secrets "
                    "rate limits audit logging sensitive data abuse cases no-secrets evidence traces metrics "
                    "logs dashboards alerts semantic conventions collector instrumentation context propagation "
                    "redaction policy SLO user journey health platform-unavailable gap reason follow-up "
                    "runbook severity assumptions log query links rollback verification command feature flag "
                    "OpenAPI AsyncAPI Pact protobuf provider contracts external providers contract changes "
                    "synced with code and tests"
                ),
            )

        boundary = self._recommendation_by_gate(result, "backend_service_boundary_present")
        security = self._recommendation_by_gate(result, "backend_security_reviewed")
        observability = self._recommendation_by_gate(result, "backend_observability_contract_present")
        health = self._recommendation_by_gate(result, "backend_health_probe_contract_present")
        config = self._recommendation_by_gate(result, "backend_config_secrets_boundary_present")
        rollback = self._recommendation_by_gate(result, "backend_rollback_plan_present")

        expected_by_recommendation = {
            "boundary": (
                boundary,
                [
                    "service/user behavior",
                    "affected backend unit",
                    "data stores",
                    "operational assumptions",
                    "APIs/events/external providers",
                    "OpenAPI/AsyncAPI/Pact/protobuf/provider contracts where applicable",
                    "contract changes synced with code and tests",
                ],
            ),
            "security": (
                security,
                [
                    "authn/authz",
                    "secrets",
                    "rate limits",
                    "audit logging",
                    "sensitive data",
                    "abuse cases",
                    "privileged operations",
                    "no-secrets evidence",
                ],
            ),
            "observability": (
                observability,
                [
                    "semantic conventions or accepted gaps",
                    "collector/instrumentation notes",
                    "context propagation",
                    "redaction policy",
                ],
            ),
            "health": (
                health,
                [
                    "tested where platform/runtime is available",
                    "platform-unavailable gap owner",
                    "platform-unavailable gap reason",
                    "platform-unavailable follow-up",
                    "documentation alone is not sufficient",
                ],
            ),
            "config": (
                config,
                [
                    "required/optional status",
                    "no-secrets/no-private-data constraints",
                    "docs, prompts, fixtures, logs and examples",
                ],
            ),
            "rollback": (
                rollback,
                [
                    "feature flag",
                    "verification command",
                    "rollback/no-rollback rationale",
                    "contract changes synced with code/tests where applicable",
                ],
            ),
        }
        for name, (recommendation, expected_terms) in expected_by_recommendation.items():
            evidence = " ".join(recommendation["evidence_required"]).lower()
            for expected in expected_terms:
                with self.subTest(recommendation=name, expected=expected):
                    self.assertIn(expected.lower(), evidence)

    def test_backend_severity_policy_and_lightweight_retry_recommendations(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "server").mkdir()
            (root / "server" / "app.py").write_text("def app():\n    return None\n", encoding="utf-8")
            production_result = build_methodology_audit(
                root,
                intent_hint=(
                    "ship production backend service remote dependency retry idempotency observability "
                    "SLO health security rollback owner review"
                ),
            )
            accepted_gap_result = build_methodology_audit(
                root,
                intent_hint=(
                    "ship production backend SLO health observability explicit_gap_accepted owner reason "
                    "review date downstream risk follow-up condition"
                ),
            )
            local_result = build_methodology_audit(
                root,
                intent_hint="simple local/backend-light backend helper script without production users",
            )

        self.assertEqual(
            self._recommendation_by_gate(production_result, "backend_service_boundary_present")["priority"],
            "P0_blocker",
        )
        self.assertEqual(
            self._recommendation_by_gate(production_result, "backend_runtime_behavior_present")["priority"],
            "P0_blocker",
        )
        for gate in [
            "backend_security_reviewed",
            "backend_rollback_plan_present",
            "backend_observability_contract_present",
            "backend_slo_or_gap_present",
            "backend_health_probe_contract_present",
        ]:
            with self.subTest(gate=gate):
                self.assertEqual(
                    self._recommendation_by_gate(production_result, gate)["priority"],
                    "P1_high_risk",
                )

        for gate in [
            "backend_observability_contract_present",
            "backend_slo_or_gap_present",
            "backend_health_probe_contract_present",
        ]:
            with self.subTest(accepted_gap=gate):
                recommendation = self._recommendation_by_gate(accepted_gap_result, gate)
                self.assertEqual(recommendation["priority"], "P2_recommended")
                self.assertIn("accepted gap downgrade", recommendation["reason"].lower())

        local_priorities = {
            item["priority"]
            for item in local_result["recommendations"]
            if item["domain"] == "backend"
        }
        self.assertTrue(local_priorities)
        self.assertTrue(local_priorities.issubset({"P2_recommended", "P3_optional_maturity"}))

        runtime = self._recommendation_by_gate(production_result, "backend_runtime_behavior_present")
        runtime_evidence = " ".join(runtime["evidence_required"]).lower()
        for expected in [
            "lightweight read-only retry/idempotency signals",
            "dependency/job context",
            "deeper static analysis deferred",
            "avoid false positives",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, runtime_evidence)

    def test_backend_routes_semantic_evidence_sufficiency_to_owner_review_backlog(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "server").mkdir()
            (root / "server" / "app.py").write_text("def app():\n    return None\n", encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint="production backend completion evidence tests evals runtime real project risk",
            )

        recommendation = self._recommendation_by_gate(
            result,
            "backend_evidence_sufficiency_owner_reviewed",
        )
        self.assertEqual(recommendation["priority"], "P1_high_risk")
        self.assertEqual(recommendation["artifact"], "EVALS.md")
        evidence = " ".join(recommendation["evidence_required"]).lower()
        for expected in [
            "owner reviewed test/eval/runtime evidence sufficiency",
            "real project risk",
            "accepted gap owner",
            "accepted gap reason",
            "review date",
            "downstream risk",
            "follow-up",
            "t9-s",
            "cross-domain semantic sufficiency backlog",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, evidence)

    def test_api_integrations_recommends_contract_consumer_security_event_sdk_and_approval_gates(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "openapi").mkdir()
            (root / "openapi" / "public.yaml").write_text(
                "openapi: 3.2.0\ninfo:\n  title: Public API\n  version: 2.0.0\npaths: {}\n",
                encoding="utf-8",
            )
            (root / "asyncapi").mkdir()
            (root / "asyncapi" / "events.yaml").write_text(
                "asyncapi: 3.1.0\ninfo:\n  title: Events\n  version: 2.0.0\nchannels: {}\n",
                encoding="utf-8",
            )
            (root / "graphql").mkdir()
            (root / "graphql" / "schema.graphql").write_text("type Query { order(id: ID!): Order }\n", encoding="utf-8")
            (root / "proto").mkdir()
            (root / "proto" / "orders.proto").write_text("syntax = 'proto3';\n", encoding="utf-8")
            (root / "schemas").mkdir()
            (root / "schemas" / "order.schema.json").write_text(
                '{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}\n',
                encoding="utf-8",
            )
            (root / "pacts").mkdir()
            (root / "pacts" / "consumer-provider.json").write_text("{}\n", encoding="utf-8")
            (root / "clients" / "generated").mkdir(parents=True)
            (root / "clients" / "generated" / "orders-sdk.md").write_text("# generated SDK\n", encoding="utf-8")

            result = build_methodology_audit(
                root,
                intent_hint=(
                    "public partner mobile API migration breaking change with consumers generated SDK "
                    "GraphQL gRPC protobuf JSON Schema Pact webhook event external provider external write "
                    "auth scopes token claims object-level authorization rate limits sensitive fields "
                    "RFC 9457 problem details validation failure auth failure domain failure request id "
                    "correlation id latency metrics integration failure alert deprecation rollback"
                ),
            )

        self.assertNotEqual(self._domain_status(result, "api_integrations"), "not_applicable")
        expected = {
            "api_contract_source_present": ("P1_high_risk", "api-contract-review.md"),
            "api_consumer_map_present": ("P1_high_risk", "api-consumer-map.md"),
            "api_breaking_change_reviewed": ("P1_high_risk", "api-compatibility-record.md"),
            "api_security_reviewed": ("P1_high_risk", "api-auth-authorization-matrix.md"),
            "api_error_contract_present": ("P1_high_risk", "api-error-catalog.md"),
            "api_contract_test_matrix_present": ("P1_high_risk", "api-contract-test-matrix.md"),
            "event_delivery_contract_present": ("P1_high_risk", "webhook-event-contract.md"),
            "generated_client_manifest_present": ("P1_high_risk", "generated-sdk-manifest.md"),
            "external_write_approval_present": ("P0_blocker", "external-integration-approval.md"),
            "api_observability_contract_present": ("P1_high_risk", "integration-catalog.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

        contract = self._recommendation_by_gate(result, "api_contract_source_present")
        contract_evidence = " ".join(contract["evidence_required"]).lower()
        for expected_term in [
            "openapi",
            "asyncapi",
            "graphql schema",
            ".proto",
            "json schema dialect",
            "pact",
            "source of truth",
        ]:
            with self.subTest(contract_evidence=expected_term):
                self.assertIn(expected_term, contract_evidence)

    def test_api_integrations_severity_false_positives_and_unsupported_claims(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            swagger_root = Path(tmp) / "swagger_only"
            swagger_root.mkdir()
            (swagger_root / "docs").mkdir()
            (swagger_root / "docs" / "swagger-ui.html").write_text("<html>Swagger UI</html>\n", encoding="utf-8")
            swagger_result = build_methodology_audit(swagger_root, intent_hint="rendered swagger ui docs cleanup")

            openapi_root = Path(tmp) / "openapi_only"
            openapi_root.mkdir()
            (openapi_root / "openapi.yaml").write_text(
                "openapi: 3.2.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                encoding="utf-8",
            )
            openapi_result = build_methodology_audit(openapi_root, intent_hint="public API contract review")

            unsupported_root = Path(tmp) / "unsupported"
            unsupported_root.mkdir()
            (unsupported_root / "openapi.yaml").write_text(
                "openapi: 3.2.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                encoding="utf-8",
            )
            unsupported_result = build_methodology_audit(
                unsupported_root,
                intent_hint=(
                    "rendered API docs are enough; schema validation is the same as contract testing; "
                    "GraphQL is always more modern; OAuth exists, so API security is handled"
                ),
            )

            accepted_gap_root = Path(tmp) / "accepted_gap"
            accepted_gap_root.mkdir()
            (accepted_gap_root / "openapi.yaml").write_text(
                "openapi: 3.2.0\ninfo:\n  title: internal API\n  version: 1.0.0\npaths: {}\n",
                encoding="utf-8",
            )
            accepted_gap_result = build_methodology_audit(
                accepted_gap_root,
                intent_hint=(
                    "simple internal prototype API explicit_gap_accepted owner reason review date "
                    "downstream risk follow-up condition"
                ),
            )

        self.assertEqual(self._domain_status(swagger_result, "api_integrations"), "not_applicable")
        self.assertNotEqual(self._domain_status(openapi_result, "api_integrations"), "not_applicable")
        self.assertEqual(self._domain_status(openapi_result, "backend"), "not_applicable")

        unsupported = self._recommendation_by_gate(unsupported_result, "api_unsupported_claims_rejected")
        self.assertEqual(unsupported["priority"], "P1_high_risk")
        self.assertEqual(unsupported["artifact"], "api-contract-review.md")

        for gate in [
            "api_consumer_map_present",
            "api_breaking_change_reviewed",
            "api_security_reviewed",
            "api_error_contract_present",
            "api_observability_contract_present",
        ]:
            with self.subTest(accepted_gap=gate):
                recommendation = self._recommendation_by_gate(accepted_gap_result, gate)
                self.assertIn(recommendation["priority"], {"P2_recommended", "P3_optional_maturity"})
                self.assertIn("accepted gap", recommendation["reason"].lower())

    def test_api_integrations_contract_drift_security_examples_and_style_choice_depth(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "openapi.yaml").write_text(
                "openapi: 3.2.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                encoding="utf-8",
            )
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "API contract drift between source code and generated docs lifecycle stable deprecated removed "
                    "success example validation failure auth failure domain failure RFC 9457 problem details "
                    "OpenAPI security schemes GraphQL auth scopes token claims object-level authorization "
                    "rate limits abuse cases sensitive fields prose-only security notes request id correlation id "
                    "error counters latency rate-limit metrics integration failure alerts "
                    "generated SDK generator version config target languages regeneration command reviewable diff "
                    "SemVer impact release process multi-repo generated clients webhook signature verification replay "
                    "dead-letter CloudEvents GraphQL gRPC event-driven universal default Spectral Redocly"
                ),
            )

        expected_by_gate = {
            "api_contract_source_present": [
                "contract drift",
                "source, code and generated docs",
                "lifecycle state",
                "draft",
                "experimental",
                "stable",
                "deprecated",
                "removed",
            ],
            "api_error_contract_present": [
                "success example",
                "validation failure",
                "auth failure",
                "domain failure",
                "rfc 9457",
                "problem details",
            ],
            "api_security_reviewed": [
                "security schemes",
                "graphql auth",
                "scopes",
                "token claims",
                "object-level authorization",
                "rate limits",
                "abuse cases",
                "prose-only security notes are unsupported",
            ],
            "api_observability_contract_present": [
                "request ids",
                "correlation ids",
                "error counters",
                "latency",
                "rate-limit metrics",
                "integration failure alerts",
            ],
            "generated_client_manifest_present": [
                "generator",
                "version",
                "config",
                "target languages",
                "regeneration command",
                "reviewable diff",
                "semver impact",
                "multi-repository generated clients deferred",
            ],
            "event_delivery_contract_present": [
                "signature verification",
                "correlation id",
                "idempotency key",
                "retry policy",
                "ordering guarantee",
                "replay",
                "dead-letter",
                "cloudevents applicability",
            ],
            "api_style_choice_recorded": [
                "no universal default",
                "graphql",
                "grpc",
                "event-driven",
                "spectral",
                "redocly",
                "framework-native",
                "deferred with owner/reason",
            ],
        }
        for gate, expected_terms in expected_by_gate.items():
            recommendation = self._recommendation_by_gate(result, gate)
            evidence = " ".join(recommendation["evidence_required"]).lower()
            for expected in expected_terms:
                with self.subTest(gate=gate, expected=expected):
                    self.assertIn(expected, evidence)

    def test_database_data_recommends_inventory_migration_contract_privacy_and_approval_gates(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "db").mkdir()
            (root / "db" / "schema.dbml").write_text("Table orders { id integer user_email varchar }\n", encoding="utf-8")
            (root / "prisma").mkdir()
            (root / "prisma" / "schema.prisma").write_text("model Order { id String @id userEmail String }\n", encoding="utf-8")
            (root / "migrations").mkdir()
            (root / "migrations" / "001_add_orders.sql").write_text(
                "alter table orders add column user_email text;\n",
                encoding="utf-8",
            )
            (root / "migrations" / "002_backfill_orders.sql").write_text(
                "-- backfill production orders with synthetic dry run first\n",
                encoding="utf-8",
            )
            (root / "alembic.ini").write_text("[alembic]\nscript_location = migrations\n", encoding="utf-8")
            (root / "liquibase").mkdir()
            (root / "liquibase" / "changelog.xml").write_text(
                "<databaseChangeLog><changeSet id=\"1\" author=\"synthetic\"/></databaseChangeLog>\n",
                encoding="utf-8",
            )
            (root / "flyway.conf").write_text("flyway.locations=filesystem:migrations\n", encoding="utf-8")
            (root / "analytics").mkdir()
            (root / "analytics" / "orders.sql").write_text("select id, user_email from orders\n", encoding="utf-8")
            (root / "great_expectations.yml").write_text("config_version: 3\n", encoding="utf-8")
            (root / "lineage").mkdir()
            (root / "lineage" / "openlineage.json").write_text('{"eventType":"START"}\n', encoding="utf-8")
            (root / "pipelines").mkdir()
            (root / "pipelines" / "rag_ingest.py").write_text("def ingest():\n    return 'synthetic rag pipeline'\n", encoding="utf-8")
            (root / "reports").mkdir()
            (root / "reports" / "query-plan.txt").write_text("EXPLAIN SELECT * FROM orders;\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "production-data-access.md").write_text(
                "# Synthetic production data access approval\nPII retention backup restore rollback owner review\n",
                encoding="utf-8",
            )

            result = build_methodology_audit(
                root,
                intent_hint=(
                    "production database data migration backfill PII sensitive retention deletion privacy "
                    "schema source data contract lineage data quality query index performance backup restore "
                    "rollback transaction boundary expand contract production access approval RAG ingestion "
                    "dbt Great Expectations OpenLineage Alembic Liquibase Flyway Prisma"
                ),
            )

        self.assertNotEqual(self._domain_status(result, "database_data"), "not_applicable")
        expected = {
            "database_inventory_present": ("P1_high_risk", "database-inventory.md"),
            "database_dictionary_present": ("P1_high_risk", "database-dictionary.md"),
            "database_schema_source_present": ("P1_high_risk", "database-data-contract.md"),
            "database_migration_plan_present": ("P1_high_risk", "database-migration-plan.md"),
            "database_expand_contract_reviewed": ("P1_high_risk", "database-expand-contract-record.md"),
            "database_transaction_boundary_present": ("P1_high_risk", "database-data-contract.md"),
            "database_rollback_feasibility_present": ("P1_high_risk", "database-rollback-feasibility.md"),
            "database_backup_restore_evidence_present": ("P1_high_risk", "database-backup-restore-evidence.md"),
            "database_data_classification_present": ("P1_high_risk", "database-data-classification-matrix.md"),
            "database_data_quality_contract_present": ("P1_high_risk", "database-data-quality-checks.md"),
            "database_data_contract_present": ("P1_high_risk", "database-data-contract.md"),
            "database_lineage_present": ("P2_recommended", "database-lineage-map.md"),
            "database_performance_review_present": ("P2_recommended", "database-query-performance-review.md"),
            "database_retention_deletion_policy_present": ("P1_high_risk", "database-retention-deletion-policy.md"),
            "database_synthetic_fixture_policy_present": ("P2_recommended", "database-synthetic-fixtures-policy.md"),
            "database_production_access_approval_present": ("P0_blocker", "database-production-access-approval.md"),
            "database_constraints_integrity_review_present": ("P1_high_risk", "database-data-contract.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

        migration = self._recommendation_by_gate(result, "database_migration_plan_present")
        migration_evidence = " ".join(migration["evidence_required"]).lower()
        for expected_term in [
            "liquibase",
            "flyway",
            "alembic",
            "prisma",
            "rails/django",
            "expand-contract",
            "preconditions",
            "databasechangelog",
            "schema history",
            "versioned/repeatable",
            "no universal default",
            "schema-diff tooling deferred",
        ]:
            with self.subTest(migration_evidence=expected_term):
                self.assertIn(expected_term, migration_evidence)

        constraints = self._recommendation_by_gate(result, "database_constraints_integrity_review_present")
        constraints_evidence = " ".join(constraints["evidence_required"]).lower()
        for expected_term in ["constraints", "indexes", "foreign keys", "unique", "not null", "data drift"]:
            with self.subTest(constraints_evidence=expected_term):
                self.assertIn(expected_term, constraints_evidence)

        production_access = self._recommendation_by_gate(result, "database_production_access_approval_present")
        self.assertIn("approval_required", production_access["approval_boundary"])

    def test_database_data_false_positives_unsupported_claims_and_destructive_changes(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            readme_root = Path(tmp) / "readme_only"
            readme_root.mkdir()
            (readme_root / "README.md").write_text("# Synthetic database glossary cleanup\n", encoding="utf-8")
            readme_result = build_methodology_audit(
                readme_root,
                intent_hint="typo-only docs edit without schema data or query behavior change",
            )

            unsupported_root = Path(tmp) / "unsupported"
            unsupported_root.mkdir()
            (unsupported_root / "prisma").mkdir()
            (unsupported_root / "prisma" / "schema.prisma").write_text("model Account { id String @id }\n", encoding="utf-8")
            unsupported_result = build_methodology_audit(
                unsupported_root,
                intent_hint=(
                    "Prisma introspection proves database safety; ORM schema equals production schema; "
                    "EXPLAIN ANALYZE is safe on writes; dbdocs alone are enough; generated ERD proves constraints"
                ),
            )

            destructive_root = Path(tmp) / "destructive"
            destructive_root.mkdir()
            (destructive_root / "migrations").mkdir()
            (destructive_root / "migrations" / "003_destructive.sql").write_text(
                "DROP TABLE legacy_orders;\nTRUNCATE TABLE staging_orders;\nALTER TABLE orders RENAME TO orders_old;\n",
                encoding="utf-8",
            )
            destructive_result = build_methodology_audit(
                destructive_root,
                intent_hint="production database migration with drop truncate rename cleanup purge rollback",
            )

        self.assertEqual(self._domain_status(readme_result, "database_data"), "not_applicable")

        unsupported = self._recommendation_by_gate(unsupported_result, "database_unsupported_claims_rejected")
        self.assertEqual(unsupported["priority"], "P1_high_risk")
        self.assertEqual(unsupported["artifact"], "database-data-contract.md")

        migration = self._recommendation_by_gate(destructive_result, "database_migration_plan_present")
        evidence = " ".join(migration["evidence_required"]).lower()
        for expected_term in ["drop", "rename", "truncate", "cleanup", "purge", "destructive migration"]:
            with self.subTest(destructive_evidence=expected_term):
                self.assertIn(expected_term, evidence)
        approval = self._recommendation_by_gate(destructive_result, "database_production_access_approval_present")
        self.assertEqual(approval["priority"], "P0_blocker")

    def test_llm_ai_rag_recommends_baseline_rerun_prompt_model_tool_rag_safety_and_cost_gates(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "prompts").mkdir()
            (root / "prompts" / "support.prompt.md").write_text("You are a synthetic support assistant.\n", encoding="utf-8")
            (root / "rag").mkdir()
            (root / "rag" / "retrieval.py").write_text("def retrieve():\n    return []\n", encoding="utf-8")
            (root / "tools").mkdir()
            (root / "tools" / "refund_tool.py").write_text("def refund():\n    return 'synthetic'\n", encoding="utf-8")
            (root / "agents").mkdir()
            (root / "agents" / "triage_agent.py").write_text("AGENT = 'synthetic'\n", encoding="utf-8")
            (root / "schemas").mkdir()
            (root / "schemas" / "answer.schema.json").write_text('{"type":"object"}\n', encoding="utf-8")

            result = build_methodology_audit(
                root,
                intent_hint=(
                    "ship user-facing high-volume AI prompt model migration RAG retrieval vector embeddings "
                    "structured output schema tool function call MCP side-effecting approval agent routing "
                    "guardrail safety prompt injection private data eval regression latency cost grounding"
                ),
            )

        self.assertNotEqual(self._domain_status(result, "llm_ai_rag"), "not_applicable")
        expected = {
            "ai_behavior_spec_present": ("P1_high_risk", "ai-behavior-spec.md"),
            "ai_baseline_eval_present": ("P0_blocker", "ai-eval-spec.md"),
            "ai_eval_rerun_command_present": ("P1_high_risk", "eval-run-report.md"),
            "ai_dataset_governance_present": ("P1_high_risk", "ai-dataset-manifest.md"),
            "ai_prompt_contract_present": ("P1_high_risk", "prompt-contract.md"),
            "ai_model_decision_record_present": ("P1_high_risk", "model-decision-record.md"),
            "ai_structured_output_contract_present": ("P1_high_risk", "structured-output-schema.md"),
            "ai_tool_contract_present": ("P1_high_risk", "ai-tool-contract.md"),
            "ai_human_approval_boundary_present": ("P0_blocker", "guardrail-matrix.md"),
            "rag_source_inventory_present": ("P1_high_risk", "rag-source-inventory.md"),
            "rag_retrieval_config_present": ("P1_high_risk", "rag-retrieval-config.md"),
            "rag_grounding_eval_present": ("P1_high_risk", "rag-eval-report.md"),
            "agent_workflow_trace_present": ("P1_high_risk", "trace-evidence-packet.md"),
            "ai_safety_review_present": ("P1_high_risk", "guardrail-matrix.md"),
            "ai_cost_latency_budget_present": ("P1_high_risk", "ai-cost-latency-budget.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

        rerun = self._recommendation_by_gate(result, "ai_eval_rerun_command_present")
        rerun_evidence = " ".join(rerun["evidence_required"]).lower()
        for expected_term in ["rerun command", "threshold", "baseline/current comparison", "failed cases", "current-run evidence"]:
            with self.subTest(rerun_evidence=expected_term):
                self.assertIn(expected_term, rerun_evidence)

        prompt = self._recommendation_by_gate(result, "ai_prompt_contract_present")
        prompt_evidence = " ".join(prompt["evidence_required"]).lower()
        for expected_term in [
            "version",
            "role",
            "goal",
            "context",
            "variables",
            "constraints",
            "examples",
            "uncertainty",
            "refusal",
            "output format",
            "verification route",
        ]:
            with self.subTest(prompt_evidence=expected_term):
                self.assertIn(expected_term, prompt_evidence)

        dataset = self._recommendation_by_gate(result, "ai_dataset_governance_present")
        dataset_evidence = " ".join(dataset["evidence_required"]).lower()
        for expected_term in [
            "dataset source",
            "privacy class",
            "synthetic",
            "sanitized",
            "retention",
            "owner",
            "no secrets",
            "credentials",
            "private customer data",
            "raw private chat",
        ]:
            with self.subTest(dataset_evidence=expected_term):
                self.assertIn(expected_term, dataset_evidence)

        model = self._recommendation_by_gate(result, "ai_model_decision_record_present")
        model_evidence = " ".join(model["evidence_required"]).lower()
        for expected_term in [
            "snapshot/alias policy",
            "reasoning effort",
            "modality",
            "context window",
            "tool support",
            "latency",
            "cost",
            "fallback",
            "rollback",
            "migration note",
        ]:
            with self.subTest(model_evidence=expected_term):
                self.assertIn(expected_term, model_evidence)

        structured = self._recommendation_by_gate(result, "ai_structured_output_contract_present")
        structured_evidence = " ".join(structured["evidence_required"]).lower()
        for expected_term in ["schema", "typed contract", "strictness", "parser validation", "refusal", "fallback", "failure cases"]:
            with self.subTest(structured_evidence=expected_term):
                self.assertIn(expected_term, structured_evidence)

        tool = self._recommendation_by_gate(result, "ai_tool_contract_present")
        tool_evidence = " ".join(tool["evidence_required"]).lower()
        for expected_term in ["schema", "permissions", "side effects", "idempotency", "retries", "errors"]:
            with self.subTest(tool_evidence=expected_term):
                self.assertIn(expected_term, tool_evidence)

        approval = self._recommendation_by_gate(result, "ai_human_approval_boundary_present")
        approval_evidence = " ".join(approval["evidence_required"]).lower()
        for expected_term in ["writes", "shell", "money", "data exposure", "irreversible", "approval route"]:
            with self.subTest(approval_evidence=expected_term):
                self.assertIn(expected_term, approval_evidence)

        rag_source = self._recommendation_by_gate(result, "rag_source_inventory_present")
        rag_source_evidence = " ".join(rag_source["evidence_required"]).lower()
        for expected_term in ["corpus authority", "freshness", "owner", "ingestion path", "exclusions", "source policy", "unsupported-claim behavior"]:
            with self.subTest(rag_source_evidence=expected_term):
                self.assertIn(expected_term, rag_source_evidence)

        rag_config = self._recommendation_by_gate(result, "rag_retrieval_config_present")
        rag_config_evidence = " ".join(rag_config["evidence_required"]).lower()
        for expected_term in ["chunking", "embeddings", "vector store", "filters", "top-k", "reranking", "metadata"]:
            with self.subTest(rag_config_evidence=expected_term):
                self.assertIn(expected_term, rag_config_evidence)

        rag_eval = self._recommendation_by_gate(result, "rag_grounding_eval_present")
        rag_eval_evidence = " ".join(rag_eval["evidence_required"]).lower()
        for expected_term in ["context precision", "context recall", "faithfulness", "answer relevance", "grounding rubric", "failed queries", "source gaps"]:
            with self.subTest(rag_eval_evidence=expected_term):
                self.assertIn(expected_term, rag_eval_evidence)

        agent_trace = self._recommendation_by_gate(result, "agent_workflow_trace_present")
        agent_trace_evidence = " ".join(agent_trace["evidence_required"]).lower()
        for expected_term in ["smallest-useful workflow", "trace id", "tool calls", "handoffs", "state", "final-answer owner", "stop conditions"]:
            with self.subTest(agent_trace_evidence=expected_term):
                self.assertIn(expected_term, agent_trace_evidence)

        safety = self._recommendation_by_gate(result, "ai_safety_review_present")
        safety_evidence = " ".join(safety["evidence_required"]).lower()
        for expected_term in [
            "prompt injection",
            "private data",
            "risky tool actions",
            "minors",
            "cybersecurity",
            "finance",
            "healthcare",
            "legal",
            "support",
            "irreversible side effects",
            "red-team cases",
            "fallback",
        ]:
            with self.subTest(safety_evidence=expected_term):
                self.assertIn(expected_term, safety_evidence)

        budget = self._recommendation_by_gate(result, "ai_cost_latency_budget_present")
        budget_evidence = " ".join(budget["evidence_required"]).lower()
        for expected_term in ["timeout", "retry", "cache", "background/batch mode", "fallback", "token/cost budget", "measurement", "explicit unavailable gap"]:
            with self.subTest(budget_evidence=expected_term):
                self.assertIn(expected_term, budget_evidence)

    def test_llm_ai_rag_false_positives_and_unsupported_claims(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            readme_root = Path(tmp) / "readme_only"
            readme_root.mkdir()
            (readme_root / "README.md").write_text("# Synthetic AI glossary typo cleanup\n", encoding="utf-8")
            readme_result = build_methodology_audit(
                readme_root,
                intent_hint="typo-only docs edit without AI behavior change",
            )

            prompt_docs_root = Path(tmp) / "prompt_docs"
            prompt_docs_root.mkdir()
            (prompt_docs_root / "docs").mkdir()
            (prompt_docs_root / "docs" / "prompt-writing.md").write_text(
                "# Prompt writing editorial guide\n",
                encoding="utf-8",
            )
            prompt_docs_result = build_methodology_audit(
                prompt_docs_root,
                intent_hint="non-behavior prompt docs cleanup without AI behavior change",
            )

            unsupported_root = Path(tmp) / "unsupported"
            unsupported_root.mkdir()
            (unsupported_root / "prompts").mkdir()
            (unsupported_root / "prompts" / "answer.prompt.md").write_text("Synthetic prompt\n", encoding="utf-8")
            unsupported_result = build_methodology_audit(
                unsupported_root,
                intent_hint=(
                    "manual spot checks are enough for AI quality; citations alone prove RAG correctness; "
                    "a tool schema is enough for safe tool use; model upgrade automatically improves product quality"
                ),
            )

        self.assertEqual(self._domain_status(readme_result, "llm_ai_rag"), "not_applicable")
        self.assertEqual(
            [item for item in readme_result["recommendations"] if item["domain"] == "llm_ai_rag"],
            [],
        )
        self.assertEqual(self._domain_status(prompt_docs_result, "llm_ai_rag"), "not_applicable")
        self.assertEqual(
            [item for item in prompt_docs_result["recommendations"] if item["domain"] == "llm_ai_rag"],
            [],
        )

        unsupported = self._recommendation_by_gate(unsupported_result, "ai_unsupported_claims_rejected")
        self.assertEqual(unsupported["priority"], "P1_high_risk")
        self.assertEqual(unsupported["artifact"], "ai-eval-spec.md")
        evidence = " ".join(unsupported["evidence_required"]).lower()
        for expected_term in ["manual spot checks", "citations alone", "tool schema", "model upgrade"]:
            with self.subTest(unsupported_evidence=expected_term):
                self.assertIn(expected_term, evidence)

    def test_llm_ai_rag_final_batch_recommendations_cover_handoff_tooling_migration_lifecycle_diff_and_incident(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "prompts").mkdir()
            (root / "prompts" / "assistant.prompt.md").write_text("Synthetic prompt\n", encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "ship AI agent handoff with Promptfoo OpenAI Evals pytest Jest Ragas LangSmith "
                    "eval tooling selector deferred runner model migration snapshot alias prompt migration "
                    "minimum threshold sampling temperature rollback RAG corpus lifecycle deletion retention "
                    "privacy vector store lifecycle stale-source pruning diff changed files code config diff "
                    "failed eval hallucination report unsafe output tool misuse data exposure incident"
                ),
            )

        expected = {
            "ai_agent_handoff_contract_compatible": ("P1_high_risk", "agent-task-packet.md"),
            "ai_eval_tooling_selector_present": ("P2_recommended", "ai-eval-spec.md"),
            "ai_model_migration_policy_present": ("P1_high_risk", "model-decision-record.md"),
            "rag_corpus_lifecycle_privacy_present": ("P1_high_risk", "rag-source-inventory.md"),
            "ai_behavior_diff_signal_policy_present": ("P2_recommended", "RUNLOG.md"),
            "ai_incident_workflow_present": ("P1_high_risk", "guardrail-matrix.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

        handoff = self._recommendation_by_gate(result, "ai_agent_handoff_contract_compatible")
        for expected_term in ["handoff owner", "inputs", "output schema", "stop condition", "trace evidence"]:
            with self.subTest(handoff_evidence=expected_term):
                self.assertIn(expected_term, " ".join(handoff["evidence_required"]).lower())

        tooling = self._recommendation_by_gate(result, "ai_eval_tooling_selector_present")
        for expected_term in [
            "promptfoo",
            "openai evals",
            "pytest/jest",
            "ragas",
            "langsmith",
            "selected runner",
            "rejected runner",
            "deferred decision",
            "stack/privacy/ci fit",
        ]:
            with self.subTest(tooling_evidence=expected_term):
                self.assertIn(expected_term, " ".join(tooling["evidence_required"]).lower())
        self.assertIn("not defaults", tooling["reason"].lower())

        migration = self._recommendation_by_gate(result, "ai_model_migration_policy_present")
        for expected_term in [
            "snapshot or approved alias",
            "prompt migration impact",
            "compatibility checks",
            "rollback",
            "baseline/current eval comparison",
            "minimum threshold",
            "sampling parameter rationale",
        ]:
            with self.subTest(migration_evidence=expected_term):
                self.assertIn(expected_term, " ".join(migration["evidence_required"]).lower())

        lifecycle = self._recommendation_by_gate(result, "rag_corpus_lifecycle_privacy_present")
        for expected_term in [
            "deletion path",
            "retention",
            "source exclusion",
            "stale-source pruning",
            "privacy owner",
            "vector store lifecycle",
            "database/security overlap",
        ]:
            with self.subTest(lifecycle_evidence=expected_term):
                self.assertIn(expected_term, " ".join(lifecycle["evidence_required"]).lower())

        diff_policy = self._recommendation_by_gate(result, "ai_behavior_diff_signal_policy_present")
        self.assertIn("limited to workspace and intent signals", diff_policy["reason"].lower())
        for expected_term in ["no external branches", "no network", "filename changes alone are not certainty"]:
            with self.subTest(diff_policy_evidence=expected_term):
                self.assertIn(expected_term, " ".join(diff_policy["evidence_required"]).lower())

        incident = self._recommendation_by_gate(result, "ai_incident_workflow_present")
        for expected_term in [
            "owner",
            "severity",
            "evidence",
            "mitigation",
            "follow-up eval",
            "security/privacy handoff",
        ]:
            with self.subTest(incident_evidence=expected_term):
                self.assertIn(expected_term, " ".join(incident["evidence_required"]).lower())

    def test_security_privacy_compliance_recommends_gate_priority_and_artifact_mapping(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "auth").mkdir()
            (root / "auth" / "login.py").write_text("def login():\n    return None\n", encoding="utf-8")
            (root / "billing").mkdir()
            (root / "billing" / "stripe_checkout.py").write_text("def pay():\n    return None\n", encoding="utf-8")
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "deploy.yml").write_text("permissions: write-all\n", encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "ship production authn authz OAuth API with role scope resource ownership BOLA BFLA "
                    "object property authorization rate limit unsafe consumption payment billing secrets PII "
                    "privacy logs traces screenshots eval datasets audit logging supply chain SBOM provenance "
                    "CI permissions AI agent prompt injection tool misuse compliance finance healthcare minors "
                    "enterprise public sector marketplace legal regulatory contract external write production data "
                    "secret rotation vulnerability advisory leaked secret data exposure Codex Security scan"
                ),
            )

        self.assertNotEqual(self._domain_status(result, "security_privacy_compliance"), "not_applicable")
        expected = {
            "security_sensitive_classification_present": ("P1_high_risk", "security-risk-review.md"),
            "threat_surface_present": ("P1_high_risk", "threat-surface.md"),
            "security_risk_review_present": ("P1_high_risk", "security-risk-review.md"),
            "asvs_mapping_present": ("P1_high_risk", "asvs-ssdf-mapping.md"),
            "asvs_level_selection_present": ("P1_high_risk", "asvs-ssdf-mapping.md"),
            "secure_sdlc_ssdf_samm_present": ("P2_recommended", "asvs-ssdf-mapping.md"),
            "api_security_scheme_present": ("P1_high_risk", "api-security-review.md"),
            "authz_negative_tests_present": ("P1_high_risk", "authz-negative-test-matrix.md"),
            "secrets_policy_present": ("P0_blocker", "secrets-policy.md"),
            "data_classification_present": ("P1_high_risk", "data-classification-register.md"),
            "data_redaction_lifecycle_present": ("P1_high_risk", "data-classification-register.md"),
            "privacy_impact_record_present": ("P1_high_risk", "privacy-impact-record.md"),
            "external_write_approval_present": ("P0_blocker", "approval-record.md"),
            "abuse_rate_limit_review_present": ("P1_high_risk", "abuse-rate-limit-plan.md"),
            "audit_logging_review_present": ("P1_high_risk", "audit-logging-review.md"),
            "supply_chain_review_present": ("P1_high_risk", "supply-chain-review.md"),
            "sbom_provenance_decision_present": ("P1_high_risk", "sbom-manifest.md"),
            "ci_permission_review_present": ("P1_high_risk", "ci-permissions-review.md"),
            "ai_security_review_present": ("P1_high_risk", "ai-security-review.md"),
            "compliance_overlay_present": ("P1_high_risk", "compliance-overlay.md"),
            "compliance_overlay_taxonomy_present": ("P1_high_risk", "compliance-overlay.md"),
            "vulnerability_response_workflow_present": ("P1_high_risk", "vulnerability-response-record.md"),
            "codex_security_scan_status_present": ("P2_recommended", "security-risk-review.md"),
            "security_evidence_before_completion": ("P0_blocker", "RUNLOG.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_domain_gate(result, "security_privacy_compliance", gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

        authz = self._recommendation_by_domain_gate(result, "security_privacy_compliance", "authz_negative_tests_present")
        authz_evidence = " ".join(authz["evidence_required"]).lower()
        for expected_term in ["allowed behavior", "forbidden behavior", "bola", "bfla", "object property", "role", "scope", "resource ownership", "rate limits", "unsafe consumption"]:
            with self.subTest(authz_evidence=expected_term):
                self.assertIn(expected_term, authz_evidence)

        data = self._recommendation_by_domain_gate(result, "security_privacy_compliance", "data_redaction_lifecycle_present")
        data_evidence = " ".join(data["evidence_required"]).lower()
        for expected_term in ["prompts", "docs", "fixtures", "eval datasets", "logs", "traces", "screenshots", "redaction"]:
            with self.subTest(data_evidence=expected_term):
                self.assertIn(expected_term, data_evidence)

        compliance = self._recommendation_by_domain_gate(result, "security_privacy_compliance", "compliance_overlay_taxonomy_present")
        compliance_evidence = " ".join(compliance["evidence_required"]).lower()
        for expected_term in ["legal/regulatory", "customer contractual", "internal policy", "finance", "healthcare", "minors", "enterprise", "public sector", "marketplace", "ai agent tooling"]:
            with self.subTest(compliance_evidence=expected_term):
                self.assertIn(expected_term, compliance_evidence)

    def test_security_privacy_compliance_false_positives_and_unsupported_claims(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            docs_root = Path(tmp) / "docs_only"
            docs_root.mkdir()
            (docs_root / "docs").mkdir()
            (docs_root / "docs" / "security-article.md").write_text("# Security article\n", encoding="utf-8")
            docs_result = build_methodology_audit(
                docs_root,
                intent_hint="docs-only security article without code, data, CI, dependency or policy change",
            )

            unsupported_root = Path(tmp) / "unsupported"
            unsupported_root.mkdir()
            (unsupported_root / "auth").mkdir()
            (unsupported_root / "auth" / "oauth.py").write_text("def oauth():\n    return None\n", encoding="utf-8")
            unsupported_result = build_methodology_audit(
                unsupported_root,
                intent_hint=(
                    "security review can happen after coding; no secrets in code means safe; "
                    "ASVS OWASP proves compliance; SBOM once is enough; Codex Security scan is implied; "
                    "OAuth proves API security; privacy compliance is universal"
                ),
            )

        self.assertEqual(self._domain_status(docs_result, "security_privacy_compliance"), "not_applicable")
        self.assertEqual(
            [item for item in docs_result["recommendations"] if item["domain"] == "security_privacy_compliance"],
            [],
        )

        unsupported = self._recommendation_by_domain_gate(
            unsupported_result,
            "security_privacy_compliance",
            "security_unsupported_claims_rejected",
        )
        self.assertEqual(unsupported["priority"], "P1_high_risk")
        self.assertEqual(unsupported["artifact"], "security-risk-review.md")
        evidence = " ".join(unsupported["evidence_required"]).lower()
        for expected_term in [
            "security review after coding",
            "no-secrets-in-code",
            "asvs/owasp",
            "sbom once",
            "codex security scan is implied",
            "oauth proves api security",
            "privacy compliance is universal",
        ]:
            with self.subTest(unsupported_evidence=expected_term):
                self.assertIn(expected_term, evidence)

    def test_delivery_release_operations_recommends_initial_gate_priority_and_artifact_mapping(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text(
                '{"name":"synthetic-release","version":"1.2.0","scripts":{"build":"vite build","test":"vitest"}}\n',
                encoding="utf-8",
            )
            (root / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "release.yml").write_text("name: Release\n", encoding="utf-8")
            (root / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "publish production package release-ready deployed SemVer changelog release notes "
                    "migration deprecation compatibility external boundary owner current build test docs eval "
                    "runtime artifact evidence inspection-only"
                ),
            )

        self.assertNotEqual(self._domain_status(result, "delivery_release_operations"), "not_applicable")
        expected = {
            "release_scope_present": ("P1_high_risk", "release-readiness.md"),
            "version_impact_present": ("P1_high_risk", "versioning-policy.md"),
            "changelog_release_notes_present": ("P1_high_risk", "release-readiness.md"),
            "release_evidence_present": ("P0_blocker", "release-readiness.md"),
            "release_evidence_before_completion": ("P0_blocker", "release-packet.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_domain_gate(
                    result,
                    "delivery_release_operations",
                    gate,
                )
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

        scope = self._recommendation_by_domain_gate(result, "delivery_release_operations", "release_scope_present")
        scope_evidence = " ".join(scope["evidence_required"]).lower()
        for expected_term in ["release type", "target", "owner", "external boundary", "lifecycle stage", "docs-only/internal/production"]:
            with self.subTest(scope_evidence=expected_term):
                self.assertIn(expected_term, scope_evidence)

        version = self._recommendation_by_domain_gate(result, "delivery_release_operations", "version_impact_present")
        version_evidence = " ".join(version["evidence_required"]).lower()
        for expected_term in ["semver", "non-semver", "compatibility impact", "deprecation", "migration guidance", "generated client"]:
            with self.subTest(version_evidence=expected_term):
                self.assertIn(expected_term, version_evidence)

        evidence = self._recommendation_by_domain_gate(result, "delivery_release_operations", "release_evidence_before_completion")
        evidence_required = " ".join(evidence["evidence_required"]).lower()
        for expected_term in [
            "current build",
            "test",
            "docs",
            "eval",
            "runtime",
            "artifact",
            "owner evidence",
            "explicit gap",
            "inspection-only",
        ]:
            with self.subTest(release_evidence=expected_term):
                self.assertIn(expected_term, evidence_required)

    def test_delivery_release_operations_recommends_operational_gate_priority_and_artifact_mapping(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text(
                '{"name":"synthetic-release","version":"2.0.0","scripts":{"build":"vite build","test":"vitest"}}\n',
                encoding="utf-8",
            )
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "deploy.yml").write_text(
                "name: Deploy\non:\n  push:\n    tags: ['v*']\npermissions: write-all\n",
                encoding="utf-8",
            )
            (root / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")
            (root / "k8s").mkdir()
            (root / "k8s" / "deployment.yaml").write_text("kind: Deployment\n", encoding="utf-8")
            (root / "gitops").mkdir()
            (root / "gitops" / "app.yaml").write_text("kind: Application\n", encoding="utf-8")
            (root / "config").mkdir()
            (root / "config" / "feature-flags.yaml").write_text("new_checkout: false\n", encoding="utf-8")
            (root / "observability").mkdir()
            (root / "observability" / "dashboards.yaml").write_text("dashboards: []\n", encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "production deploy release artifact manifest canary blue-green staged rollout shadow traffic "
                    "manual promotion feature flag gitops desired state reconciliation drift rollback restore "
                    "unpublish yank environment approval github environments branch tag restrictions secrets "
                    "ci/cd governance required reviewers wait timers action pinning cache concurrency "
                    "observability logs metrics traces dashboard alert owner redaction sampling slo sli "
                    "operations runbook incident postmortem post-release dora support defects latency cost"
                ),
            )

        expected = {
            "artifact_manifest_present": ("P1_high_risk", "release-artifact-manifest.md"),
            "rollout_strategy_present": ("P1_high_risk", "rollout-plan.md"),
            "rollback_recovery_present": ("P1_high_risk", "rollback-recovery-plan.md"),
            "environment_approval_boundary_present": ("P1_high_risk", "environment-matrix.md"),
            "external_release_approval_present": ("P0_blocker", "approval-record.md"),
            "ci_cd_governance_present": ("P1_high_risk", "ci-cd-workflow-inventory.md"),
            "observability_release_evidence_present": ("P1_high_risk", "observability-map.md"),
            "slo_or_operational_gap_present": ("P1_high_risk", "slo-spec.md"),
            "operations_runbook_present": ("P1_high_risk", "operations-runbook.md"),
            "incident_response_path_present": ("P1_high_risk", "incident-record.md"),
            "post_release_measurement_present": ("P1_high_risk", "post-release-review.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_domain_gate(
                    result,
                    "delivery_release_operations",
                    gate,
                )
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

        evidence_terms = {
            "artifact_manifest_present": [
                "artifact names",
                "versions",
                "creation command",
                "storage location",
                "retention",
                "integrity notes",
                "checksums",
                "signatures",
                "sbom",
                "provenance",
            ],
            "rollout_strategy_present": [
                "immediate release",
                "release train",
                "staged rollout",
                "feature flag",
                "canary",
                "blue-green",
                "shadow traffic",
                "manual promotion",
                "cohorts/traffic",
                "promotion",
                "abort criteria",
                "blast radius",
            ],
            "rollback_recovery_present": [
                "revert",
                "redeploy previous artifact",
                "disable flag",
                "unpublish",
                "yank",
                "restore backup",
                "compensate data",
                "incident mitigation",
                "owner",
                "residual risk",
            ],
            "environment_approval_boundary_present": [
                "dev",
                "stage",
                "prod",
                "local",
                "mobile",
                "store",
                "registry",
                "branch/tag rules",
                "secret boundaries",
            ],
            "ci_cd_governance_present": [
                "workflow names",
                "triggers",
                "permissions",
                "secrets",
                "environments",
                "required reviewers",
                "branch/tag restrictions",
                "artifacts",
                "cache",
                "concurrency",
                "external action pinning",
            ],
            "observability_release_evidence_present": [
                "logs",
                "metrics",
                "traces",
                "dashboards",
                "alert owner",
                "redaction",
                "sampling",
            ],
            "slo_or_operational_gap_present": [
                "user journey",
                "sli",
                "slo",
                "measurement source",
                "alert policy",
                "accepted no-telemetry",
                "not-yet-production gap",
            ],
            "operations_runbook_present": [
                "deploy",
                "rollback",
                "first response",
                "escalation",
                "diagnostics",
            ],
            "incident_response_path_present": [
                "incident criteria",
                "owner",
                "communication path",
                "postmortem trigger",
            ],
            "post_release_measurement_present": [
                "metrics",
                "support signals",
                "defects",
                "latency/cost",
                "review date",
                "dora measurement source",
                "anti-goodhart",
                "product/reliability hypotheses",
            ],
        }
        for gate, terms in evidence_terms.items():
            recommendation = self._recommendation_by_domain_gate(result, "delivery_release_operations", gate)
            evidence = " ".join(recommendation["evidence_required"]).lower()
            for expected_term in terms:
                with self.subTest(gate=gate, evidence=expected_term):
                    self.assertIn(expected_term, evidence)

    def test_delivery_release_operations_gitops_flags_and_ci_claims_stay_unverified(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"version":"3.0.0"}\n', encoding="utf-8")
            (root / "gitops").mkdir()
            (root / "gitops" / "service.yaml").write_text("kind: Application\n", encoding="utf-8")
            (root / "config").mkdir()
            (root / "config" / "flags.yaml").write_text("new_checkout: false\n", encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "GitOps is automatically safe. Feature flags remove release risk. Rollback is just revert. "
                    "production deploy with gitops feature flag ci/cd governance and rollback"
                ),
            )

        unsupported = self._recommendation_by_domain_gate(
            result,
            "delivery_release_operations",
            "delivery_unsupported_claims_rejected",
        )
        unsupported_text = " ".join(unsupported["evidence_required"]).lower()
        for expected_term in [
            "gitops is automatically safe",
            "feature flags remove release risk",
            "rollback is just revert",
        ]:
            with self.subTest(unsupported_evidence=expected_term):
                self.assertIn(expected_term, unsupported_text)

        rollout = self._recommendation_by_domain_gate(result, "delivery_release_operations", "rollout_strategy_present")
        rollout_text = " ".join(rollout["evidence_required"]).lower()
        for expected_term in [
            "default value",
            "flag owner",
            "targeting rules",
            "cleanup date",
            "kill switch",
            "failure mode",
            "flag presence alone does not remove release risk",
        ]:
            with self.subTest(flag_evidence=expected_term):
                self.assertIn(expected_term, rollout_text)

        environment = self._recommendation_by_domain_gate(
            result,
            "delivery_release_operations",
            "environment_approval_boundary_present",
        )
        environment_text = " ".join(environment["evidence_required"]).lower()
        for expected_term in [
            "desired-state source",
            "reconciliation controller",
            "drift behavior",
            "approval path",
            "rollback/revert",
            "present_unverified",
        ]:
            with self.subTest(gitops_evidence=expected_term):
                self.assertIn(expected_term, environment_text)

        ci = self._recommendation_by_domain_gate(result, "delivery_release_operations", "ci_cd_governance_present")
        ci_text = " ".join(ci["evidence_required"]).lower()
        for expected_term in [
            "required reviewers",
            "wait timers",
            "branch/tag restrictions",
            "action pinning",
            "remote ci mutation approval",
        ]:
            with self.subTest(ci_evidence=expected_term):
                self.assertIn(expected_term, ci_text)

    def test_delivery_release_operations_false_positives_and_unsupported_claims(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            docs_root = Path(tmp) / "docs_only"
            docs_root.mkdir()
            (docs_root / "docs").mkdir()
            (docs_root / "docs" / "release-notes.md").write_text("# Release notes\n", encoding="utf-8")
            docs_result = build_methodology_audit(
                docs_root,
                intent_hint="docs-only release note edit without publish, package, runtime, CI/CD or user-impact claim",
            )

            unsupported_root = Path(tmp) / "unsupported"
            unsupported_root.mkdir()
            (unsupported_root / "package.json").write_text('{"version":"1.0.0"}\n', encoding="utf-8")
            unsupported_result = build_methodology_audit(
                unsupported_root,
                intent_hint=(
                    "CI green means release ready. Tests passed, so release is ready. "
                    "Rollback is just revert. Feature flags remove release risk. "
                    "GitOps is automatically safe. Generated changelog is enough for users. "
                    "DORA metrics prove individual performance. Automation is safer because it is repeatable."
                ),
            )

        docs_delivery_recommendations = [
            item for item in docs_result["recommendations"] if item["domain"] == "delivery_release_operations"
        ]
        self.assertNotIn(
            "release_evidence_present",
            {item["gate"] for item in docs_delivery_recommendations},
        )

        unsupported = self._recommendation_by_domain_gate(
            unsupported_result,
            "delivery_release_operations",
            "delivery_unsupported_claims_rejected",
        )
        self.assertEqual(unsupported["priority"], "P1_high_risk")
        self.assertEqual(unsupported["artifact"], "release-readiness.md")
        evidence = " ".join(unsupported["evidence_required"]).lower()
        for expected_term in [
            "ci green",
            "tests passed",
            "rollback is just revert",
            "feature flags remove release risk",
            "gitops is automatically safe",
            "generated changelog",
            "dora metrics prove individual performance",
            "automation is safer",
        ]:
            with self.subTest(unsupported_evidence=expected_term):
                self.assertIn(expected_term, evidence)

    def test_delivery_release_operations_recommends_automation_manual_stability_gate(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".codex" / "automation-candidates").mkdir(parents=True)
            (root / ".codex" / "automation-candidates" / "automation-candidate.md").write_text(
                "# Synthetic Automation Candidate\ncandidate_only: true\n",
                encoding="utf-8",
            )
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "promote recurring release operations workflow to automation; repeatable means safe; "
                    "manual success evidence stable inputs outputs owner verification approval requirements "
                    "value evidence rollback disable path active schedule"
                ),
            )

        recommendation = self._recommendation_by_domain_gate(
            result,
            "delivery_release_operations",
            "automation_manual_stability_present",
        )

        self.assertEqual(recommendation["priority"], "P1_high_risk")
        self.assertEqual(recommendation["artifact"], "automation-candidate.md")
        evidence = " ".join(recommendation["evidence_required"]).lower()
        for expected_term in [
            "manual success evidence",
            "stable inputs/outputs",
            "owner",
            "verification",
            "approval requirements",
            "value evidence",
            "rollback/disable path",
            "candidate-only",
            "active schedules remain out of scope",
        ]:
            with self.subTest(automation_evidence=expected_term):
                self.assertIn(expected_term, evidence)

    def test_delivery_release_operations_recommends_final_release_depth_gates(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text(
                '{"name":"synthetic-final-release","version":"4.0.0","scripts":{"build":"vite build"}}\n',
                encoding="utf-8",
            )
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "deploy.yml").write_text(
                "name: Deploy\non:\n  push:\n    tags: ['v*']\n",
                encoding="utf-8",
            )
            (root / ".github" / "environments").mkdir(parents=True)
            (root / ".github" / "environments" / "production.md").write_text(
                "# Production\n",
                encoding="utf-8",
            )
            (root / ".releaserc.json").write_text("{}\n", encoding="utf-8")
            (root / "release-please-config.json").write_text("{}\n", encoding="utf-8")
            (root / "observability").mkdir()
            (root / "observability" / "opentelemetry.yaml").write_text("service.name: fixture\n", encoding="utf-8")
            (root / "alerts").mkdir()
            (root / "alerts" / "pagerduty.yml").write_text("service: fixture\n", encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "production public release-ready deployed published release train continuous deployment "
                    "manual approval release candidate draft release cadence promotion trigger freeze cutoff "
                    "build release run immutable artifact release identifier runtime configuration boundary "
                    "environment-specific config injection accepted platform exception desktop installer mobile app "
                    "signing notarization app store review installer update path rollback yank phased rollout crash reporting "
                    "platform owner audience user impact support contact known issues migration deprecation release notes owner "
                    "conventional commits semantic-release release-please manual versioning selected rejected deferred "
                    "github environments required reviewers wait timers branch tag restrictions custom protection rules "
                    "environment secrets deployment targets dora change lead time deployment frequency failed deployment "
                    "recovery time change fail rate deployment rework rate trend review anti-goodhart team-only interpretation "
                    "incident severity timeline detection mitigation customer impact root causes contributing factors "
                    "action items blameless owner date opentelemetry prometheus grafana sentry datadog pagerduty opsgenie "
                    "manual monitoring no-tooling gap release signing vulnerability response license notice sbom provenance "
                    "package container integrity owner-reviewed release evidence sufficiency accepted gap stop condition"
                ),
            )

        expected = {
            "release_mode_policy_present": ("P1_high_risk", "release-readiness.md"),
            "build_release_run_boundary_present": ("P1_high_risk", "deployment-plan.md"),
            "platform_distribution_evidence_present": ("P1_high_risk", "release-readiness.md"),
            "release_communication_present": ("P1_high_risk", "release-readiness.md"),
            "versioning_tooling_decision_present": ("P1_high_risk", "versioning-policy.md"),
            "github_environment_controls_present": ("P1_high_risk", "environment-matrix.md"),
            "dora_measurement_design_present": ("P1_high_risk", "post-release-review.md"),
            "incident_postmortem_learning_present": ("P1_high_risk", "postmortem.md"),
            "observability_on_call_tooling_present": ("P1_high_risk", "observability-map.md"),
            "release_integrity_security_handoff_present": ("P1_high_risk", "release-artifact-manifest.md"),
            "release_evidence_sufficiency_owner_reviewed": ("P0_blocker", "release-readiness.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_domain_gate(result, "delivery_release_operations", gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

        evidence_terms = {
            "release_mode_policy_present": [
                "release train",
                "continuous deployment",
                "manual approval",
                "release candidate",
                "draft release",
                "cadence",
                "promotion trigger",
                "freeze/cutoff",
            ],
            "build_release_run_boundary_present": [
                "immutable artifact",
                "release identifier",
                "runtime configuration boundary",
                "environment-specific config injection",
                "accepted platform exception",
            ],
            "platform_distribution_evidence_present": [
                "signing",
                "notarization",
                "app store review",
                "installer/update path",
                "rollback/yank path",
                "phased rollout",
                "crash reporting",
                "platform owner evidence",
            ],
            "release_communication_present": [
                "audience",
                "user impact",
                "support contact",
                "known issues",
                "migration/deprecation note",
                "changelog link",
                "release-notes ownership",
            ],
            "versioning_tooling_decision_present": [
                "conventional commits",
                "semantic-release",
                "release-please",
                "manual versioning",
                "non-package policy",
                "selected/rejected/deferred",
                "no forced semver tooling",
            ],
            "github_environment_controls_present": [
                "required reviewers",
                "wait timers",
                "branch/tag restrictions",
                "custom protection rules",
                "environment secrets",
                "deployment targets",
                "approval_required mutation boundary",
            ],
            "dora_measurement_design_present": [
                "change lead time",
                "deployment frequency",
                "failed deployment recovery time",
                "change fail rate",
                "deployment rework rate",
                "data source",
                "trend review",
                "anti-goodhart",
                "team-only interpretation",
            ],
            "incident_postmortem_learning_present": [
                "severity",
                "timeline",
                "detection",
                "mitigation",
                "customer/user impact",
                "root causes",
                "contributing factors",
                "action items",
                "owner/date",
                "blameless",
            ],
            "observability_on_call_tooling_present": [
                "opentelemetry",
                "prometheus",
                "grafana",
                "sentry",
                "datadog",
                "pagerduty",
                "opsgenie",
                "manual monitoring",
                "selected/rejected/deferred",
                "accepted no-tooling gap",
            ],
            "release_integrity_security_handoff_present": [
                "release signing",
                "vulnerability response",
                "license/notice",
                "sbom/provenance",
                "package/container integrity",
                "satisfied",
                "not-applicable",
                "accepted gap",
                "security ownership",
            ],
            "release_evidence_sufficiency_owner_reviewed": [
                "owner acceptance",
                "sufficient for the real release risk",
                "accepted gap",
                "owner",
                "reason",
                "review date",
                "residual risk",
                "stop condition",
            ],
        }
        for gate, terms in evidence_terms.items():
            recommendation = self._recommendation_by_domain_gate(result, "delivery_release_operations", gate)
            evidence = " ".join(recommendation["evidence_required"]).lower()
            for expected_term in terms:
                with self.subTest(gate=gate, evidence=expected_term):
                    self.assertIn(expected_term, evidence)


if __name__ == "__main__":
    unittest.main()
