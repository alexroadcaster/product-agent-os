import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
SKILLS = ROOT / "plugins" / "product-agent-os" / "skills"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.contracts import LIFECYCLE_STATES  # noqa: E402


SKILL_NAMES = [
    "project-lifecycle-orchestrator",
    "workspace-discovery-auditor",
    "requirements-author",
    "implementation-planner",
    "agent-team-designer",
    "test-eval-designer",
    "risk-reviewer",
    "docs-maintainer",
    "pr-release-operator",
    "learning-loop-maintainer",
    "automation-promoter",
]

REQUIRED_HEADINGS = [
    "## Trigger",
    "## Boundaries",
    "## Inputs",
    "## Process",
    "## Outputs",
    "## Verification",
    "## Failure Modes",
    "## Final Response Contract",
]

REFERENCES = [
    "lifecycle-states.md",
    "handoff-contract.md",
    "source-policy.md",
    "complexity-routing.md",
]

REFERENCE_TERMS = {
    "lifecycle-states.md": [
        "uninitialized",
        "maintenance",
        "Do not skip",
    ],
    "handoff-contract.md": [
        "verification_evidence",
        "unsupported_claims",
        "stop_reason",
    ],
    "source-policy.md": [
        "Official OpenAI documentation",
        "Context7",
        "Do not store secrets",
    ],
    "complexity-routing.md": [
        "guided-small",
        "enterprise-governed",
        "autonomous-maintenance",
    ],
}

REQUIRED_SKILL_LINKS = [
    "../references/lifecycle-states.md",
    "../references/handoff-contract.md",
    "../references/source-policy.md",
    "../references/complexity-routing.md",
]

ROUTING = {
    "uninitialized": "workspace-discovery-auditor",
    "infrastructure_planned": "requirements-author",
    "requirements_ready": "implementation-planner",
    "plan_ready": "agent-team-designer",
    "team_ready": "test-eval-designer",
    "build_active": "risk-reviewer",
    "quality_gate": "risk-reviewer",
    "review_ready": "pr-release-operator",
    "release_ready": "learning-loop-maintainer",
    "learning_ready": "automation-promoter",
    "maintenance": "project-lifecycle-orchestrator",
}

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\((?:<)?([^)>]+)(?:>)?\)")
REFERENCE_LINK_RE = re.compile(r"^\.\./references/[^/]+\.md$")

PERMISSIVE_PREFIX = r"(?:can|may|should|allowed to|is permitted to|will|must)"
FORBIDDEN_PERMISSIVE_PATTERNS = [
    rf"\b{PERMISSIVE_PREFIX}\s+(?:create|write)\s+\.codex/agents\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:install|enable)\s+hooks\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:create|activate|start)\s+"
    r"(?:active\s+)?automation\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:create|activate|start)\s+recurring\s+automation\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:mutate|change|modify|edit)\s+"
    r"(?:global\s+)?(?:codex\s+)?config\b",
    rf"\b{PERMISSIVE_PREFIX}\s+store\s+secrets\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:create|write|generate|modify)\s+"
    r"project\s+templates\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:create|write|generate|modify)\s+workflow\s+files\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:create|run|call|connect to|use)\s+mcp\s+servers\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:create|run|use)\s+(?:an?\s+)?agents\s+sdk\s+runner\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:run|execute|perform)\s+destructive\s+commands\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:write|store|modify|use)\s+user-level\s+memory\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:call|modify|write to|connect to|use)\s+"
    r"external\s+systems\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:perform|make|do)\s+external\s+writes\b",
    rf"\b{PERMISSIVE_PREFIX}\s+install\s+external\s+dependencies\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:use\s+)?network\s+access\b",
]

NEGATIVE_PREFIX = r"(?:do not|never|must not|cannot|forbidden to|not permitted to)"

SECRET_BOUNDARY_PATTERNS = [
    rf"\b{NEGATIVE_PREFIX}\s+store\s+secrets\b",
]

AUTOMATION_BOUNDARY_PATTERNS = [
    rf"\b{NEGATIVE_PREFIX}\s+(?:create|activate|start)\s+"
    r"(?:active\s+)?automation\b",
]

CONFIG_BOUNDARY_PATTERNS = [
    rf"\b{NEGATIVE_PREFIX}\s+(?:mutate|change)\s+global\s+config\b",
    rf"\b{NEGATIVE_PREFIX}\s+modify\s+config\b",
    rf"\b{NEGATIVE_PREFIX}\s+edit\s+project\s+config\b",
    rf"\b{NEGATIVE_PREFIX}\s+change\s+global\s+codex\s+config\b",
]

EVIDENCE_BOUNDARY_PATTERNS = [
    rf"\b{NEGATIVE_PREFIX}\s+claim\b",
    r"\bwithout\s+evidence\b",
]


class LifecycleSkillsTest(unittest.TestCase):
    def test_required_skill_packages_exist(self):
        for name in SKILL_NAMES:
            with self.subTest(name=name):
                self.assertTrue(
                    (SKILLS / name / "SKILL.md").exists(),
                    f"{name} must include SKILL.md",
                )
                self.assertTrue(
                    (SKILLS / name / "agents" / "openai.yaml").exists(),
                    f"{name} must include agents/openai.yaml",
                )

    def test_skill_frontmatter_and_required_headings(self):
        for name in SKILL_NAMES:
            text = self._skill_text(name)
            with self.subTest(name=name):
                self._assert_frontmatter_has_only_name_and_description(name, text)
                self.assertRegex(
                    text,
                    r"^---\nname: "
                    + re.escape(name)
                    + r"\ndescription: .+\n---",
                )
                self.assertRegex(text, r"(?m)^# .+")
                for heading in REQUIRED_HEADINGS:
                    self.assertIn(heading, text)

    def test_skill_metadata_disables_implicit_invocation(self):
        for name in SKILL_NAMES:
            metadata = self._metadata_text(name)
            with self.subTest(name=name):
                self.assertIn("interface:", metadata)
                self.assertIn("display_name:", metadata)
                self.assertIn("short_description:", metadata)
                self.assertIn("default_prompt:", metadata)
                self.assertIn(f"Use ${name}", metadata)
                self.assertIn("allow_implicit_invocation: false", metadata)

    def test_reference_files_exist_and_are_linked(self):
        for reference in REFERENCES:
            with self.subTest(reference=reference):
                path = SKILLS / "references" / reference
                self.assertTrue(path.exists(), f"{reference} must exist")
                text = path.read_text(encoding="utf-8")
                self.assertIn("Product-Agent OS", text)
                for term in REFERENCE_TERMS[reference]:
                    self.assertIn(term, text)

        for name in SKILL_NAMES:
            text = self._skill_text(name)
            with self.subTest(name=name):
                for link in REQUIRED_SKILL_LINKS:
                    self.assertIn(link, text)
                self._assert_reference_links_resolve(name, text)

    def test_orchestrator_routing_covers_all_lifecycle_states(self):
        self.assertEqual(set(ROUTING), set(LIFECYCLE_STATES))
        text = self._skill_text("project-lifecycle-orchestrator")
        for state, skill in ROUTING.items():
            with self.subTest(state=state):
                self.assertIn(state, text)
                self.assertIn(skill, text)

    def test_bug_rescue_lifecycle_wording_is_evidence_first(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()
        discovery = self._skill_text("workspace-discovery-auditor").lower()

        for expected in [
            "usage_mode",
            "bug_rescue",
            "bug-rescue.md",
            "bug-rescue-report.md",
            "missing reproduction evidence",
        ]:
            self.assertIn(expected, orchestrator)

        for expected in [
            "bug_reproduction_signals",
            "possible evidence, not verified truth",
            "rerun required",
        ]:
            self.assertIn(expected, discovery)

    def test_greenfield_lifecycle_wording_blocks_scaffold_before_approval(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()

        for expected in [
            "greenfield_idea",
            "greenfield-idea-to-plan.md",
            "greenfield-idea-brief.md",
            "do not scaffold",
            "next smallest artifact",
            "at most one blocking question",
        ]:
            self.assertIn(expected, orchestrator)

    def test_complex_system_lifecycle_wording_requires_ownership_first(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()

        for expected in [
            "complex_system_acceleration",
            "complex-system-acceleration.md",
            "integration-catalog.md",
            "ownership-first",
            "fresh-context task packets",
            "do not parallelize",
            "overlapping files",
        ]:
            self.assertIn(expected, orchestrator)

    def test_first_run_lifecycle_wording_covers_core_entry_scenarios(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()
        discovery = self._skill_text("workspace-discovery-auditor").lower()

        for expected in [
            "first-run-intake.md",
            "first response contract",
            "empty workspace",
            "failed verification",
            "existing control-plane",
            "complex system",
            "mode",
            "confidence",
            "next smallest action",
            "minimum artifacts",
            "evidence gaps",
            "approval boundary",
            "at most one blocking question",
            "do not scaffold",
            "do not fix",
            "do not regenerate",
            "do not parallelize",
        ]:
            self.assertIn(expected, orchestrator)

        for expected in [
            "first_response_contract",
            "empty workspace",
            "failed verification",
            "existing control-plane",
            "complex system",
            "evidence gaps",
        ]:
            self.assertIn(expected, discovery)

    def test_scenario_handoff_wording_blocks_role_transition_without_packet(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()
        agent_team = self._skill_text("agent-team-designer").lower()

        for expected in [
            "scenario handoff",
            "sources/context used",
            "assumptions",
            "files touched",
            "files proposed",
            "verification evidence",
            "open risks",
            "recommended next role",
            "before role transition",
        ]:
            self.assertIn(expected, orchestrator)

        for expected in [
            "scenario handoff",
            "files touched",
            "files proposed",
            "keep handoffs concise",
            "do not advance to parallel work",
        ]:
            self.assertIn(expected, agent_team)

    def test_agent_team_designer_enforces_fresh_context_handoff_for_parallel_workers(self):
        agent_team = self._skill_text("agent-team-designer").lower()
        handoff_contract = (SKILLS / "references" / "handoff-contract.md").read_text(encoding="utf-8").lower()

        for expected in [
            "fresh-context handoff",
            "any subagent or parallel worker",
            "not only complex acceleration",
            "agent-task-packet.md",
            "handoff-contract.md",
            "worktree-ownership.md",
            "complete task context",
            "source constraints",
            "allowed sources",
            "inputs used",
            "owned files",
            "forbidden files",
            "expected evidence",
            "handoff output schema",
            "stop conditions",
            "sequential fallback",
            "shared ownership ambiguity",
            "missing handoff schema",
            "do not advance to parallel work",
        ]:
            self.assertIn(expected, agent_team)

        for expected in [
            "fresh-context handoff",
            "complete task context",
            "source constraints",
            "handoff output schema",
            "expected evidence",
            "sequential fallback",
        ]:
            self.assertIn(expected, handoff_contract)

    def test_pr_review_lifecycle_wording_routes_to_two_stage_read_only_review(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()
        risk_reviewer = self._skill_text("risk-reviewer").lower()

        for expected in [
            "pr_review",
            "pr-review-readiness.md",
            "pr-risk-review.md",
            "changed files map",
            "two-stage review",
            "spec compliance verdict",
            "quality/risk verdict",
            "missing checks",
            "do not create a pr",
            "do not push",
            "do not publish",
        ]:
            self.assertIn(expected, orchestrator)

        for expected in [
            "pr review",
            "changed files",
            "spec compliance verdict",
            "quality/risk verdict",
            "behavior impact",
            "api impact",
            "database impact",
            "ui impact",
            "security impact",
            "docs impact",
            "release impact",
            "external writes",
            "pr creation",
            "publish actions",
        ]:
            self.assertIn(expected, risk_reviewer)

    def test_acceptance_scenarios_are_required_before_behavior_changes(self):
        requirements_author = self._skill_text("requirements-author").lower()
        implementation_planner = self._skill_text("implementation-planner").lower()
        test_eval_designer = self._skill_text("test-eval-designer").lower()

        shared_terms = [
            "acceptance-scenarios.md",
            "atdd",
            "bdd",
            "requirement -> scenario -> check -> evidence owner",
            "given",
            "when",
            "then",
            "equivalent behavior format",
            "business rule",
            "edge case",
            "non-goal",
            "explicit gap",
            "evidence owner",
        ]
        for name, text in {
            "requirements-author": requirements_author,
            "implementation-planner": implementation_planner,
            "test-eval-designer": test_eval_designer,
        }.items():
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

        for expected in [
            "implementation before acceptance scenarios",
            "scenario without requirement",
            "scenario without check",
            "scenario without evidence owner",
            "bdd replaces tests",
        ]:
            self.assertIn(expected, test_eval_designer)

    def test_implementation_planner_enforces_conditional_domain_model_gate(self):
        implementation_planner = self._skill_text("implementation-planner").lower()

        for expected in [
            "domain_model_when_complex_domain",
            "domain-modeling.md",
            "complex backend",
            "workflow",
            "enterprise",
            "data-heavy",
            "bounded context",
            "bounded_context_architecture_boundary_trace",
            "architecture-overview.md",
            "architecture boundary",
            "context-to-boundary traceability",
            "every bounded context maps to architecture boundary",
            "ubiquitous language",
            "invariant",
            "accepted gap",
            "simple crud",
            "simple mvp",
            "do not force ddd",
            "missing domain model for complex domain",
            "missing bounded context architecture boundary trace",
            "stop before build",
        ]:
            self.assertIn(expected, implementation_planner)

    def test_implementation_planner_enforces_ubiquitous_language_traceability(self):
        implementation_planner = self._skill_text("implementation-planner").lower()

        for expected in [
            "ubiquitous_language_traceability",
            "term-to-requirement",
            "requirement or source",
            "api/event/contract",
            "ui label",
            "code module or owner",
            "domain expert review",
            "every ubiquitous language term",
            "missing ubiquitous language traceability",
            "accepted gap names the reason and evidence owner",
            "stop before build",
            "simple crud",
            "simple mvp",
            "do not force ddd",
        ]:
            self.assertIn(expected, implementation_planner)

    def test_implementation_planner_routes_fsd_structure_conditionally(self):
        discovery = self._skill_text("workspace-discovery-auditor").lower()
        planner = self._skill_text("implementation-planner").lower()

        for expected in [
            "fsd_structure",
            "feature-sliced design",
            "component-card.md",
            "layer",
            "slice",
            "segment",
            "public api",
            "import rule",
            "not applicable",
            "backend",
            "native",
            "simple crud",
            "simple mvp",
            "do not force fsd",
            "missing fsd structure boundary",
            "stop before build",
        ]:
            self.assertIn(expected, planner)

        for expected in [
            "fsd_structure",
            "feature-sliced design",
            "app",
            "pages",
            "widgets",
            "features",
            "entities",
            "shared",
            "do not claim architecture compliance",
        ]:
            self.assertIn(expected, discovery)

    def test_lifecycle_skills_enforce_metric_hardening_for_product_behavior(self):
        requirements_author = self._skill_text("requirements-author").lower()
        risk_reviewer = self._skill_text("risk-reviewer").lower()
        release_operator = self._skill_text("pr-release-operator").lower()

        shared_terms = [
            "metric_hardening_when_product_behavior_changes",
            "metric-spec.md",
            "north star",
            "input metric",
            "counter-metric",
            "proxy metric",
            "guardrail",
            "qualitative review",
            "privacy classification",
            "retention period",
            "data minimization",
            "owner signoff",
            "post-release review evidence",
            "do not claim success",
        ]
        for name, text in {
            "requirements-author": requirements_author,
            "risk-reviewer": risk_reviewer,
            "pr-release-operator": release_operator,
        }.items():
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_lifecycle_skills_enforce_business_product_methodology(self):
        shared_terms = [
            "product_hypothesis_present",
            "value_proposition_evidence_present",
            "analytics_tracking_plan_present",
            "qualitative_feedback_loop_present",
            "release_measurement_evidence_present",
            "decision_horizon_present",
            "outcome_metric_level_separated",
            "metric_scope_classified",
            "tracking-plan.md",
        ]
        skill_names = [
            "requirements-author",
            "implementation-planner",
            "test-eval-designer",
            "risk-reviewer",
            "learning-loop-maintainer",
            "automation-promoter",
        ]

        for name in skill_names:
            text = self._skill_text(name).lower()
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)
        self.assertIn("engineering time saved", self._skill_text("automation-promoter").lower())

    def test_lifecycle_skills_enforce_requirements_domain_methodology(self):
        shared_terms = [
            "requirement-registry.md",
            "stakeholder-owner-map.md",
            "story-slice-map.md",
            "requirements-traceability-matrix.md",
            "business-rules.md",
            "example-map.md",
            "requirement-change-impact.md",
            "domain-review-record.md",
            "requirements_traceability_present",
            "requirement_quality_present",
            "constraints_traceability_present",
            "declarative_acceptance_scenarios_present",
            "business_rules_present",
            "domain_expert_review_present",
            "requirement_change_impact_review_present",
            "accepted_gap_recorded",
            "requirements_evidence_before_implementation",
        ]
        skill_names = [
            "requirements-author",
            "implementation-planner",
            "agent-team-designer",
            "test-eval-designer",
            "risk-reviewer",
        ]

        for name in skill_names:
            text = self._skill_text(name).lower()
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

        docs_maintainer = self._skill_text("docs-maintainer").lower()
        for expected in [
            "requirement ids",
            "source registry",
            "glossary",
            "ubiquitous language",
            "traceability docs",
        ]:
            self.assertIn(expected, docs_maintainer)

    def test_lifecycle_skills_route_solution_architecture_methodology(self):
        shared_terms = [
            "solution_architecture_scope_present",
            "architecture_boundary_per_slice",
            "boundary_responsibility_owner_present",
            "adr_for_architecture_decision",
            "diagram_render_check_present",
            "runtime_deployment_topology_present",
            "observability_architecture_present",
            "migration_rollback_path_present",
            "architecture_fitness_function_present",
            "architecture-overview.md",
            "adr.md",
            "architecture-review-record.md",
            "architecture-fitness-functions.md",
            "trust-boundary-map.md",
            "architecture-docs-tooling-decision.md",
            "c4/arc42 only when applicable",
            "architecture-as-code is conditional",
            "well-architected review is conditional",
        ]
        skill_names = [
            "workspace-discovery-auditor",
            "requirements-author",
            "implementation-planner",
            "agent-team-designer",
            "test-eval-designer",
            "risk-reviewer",
            "docs-maintainer",
        ]

        for name in skill_names:
            text = self._skill_text(name).lower()
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_lifecycle_skills_generalize_evidence_before_completion(self):
        shared_terms = [
            "evidence-before-completion",
            "evidence_before_completion",
            "ready claim",
            "completed claim",
            "fixed claim",
            "works claim",
            "release claim",
            "current command evidence",
            "current eval evidence",
            "current runtime evidence",
            "inspection-only",
            "explicit test gap",
            "unsupported completion claim",
            "completion claim without current evidence",
        ]

        for name in SKILL_NAMES:
            text = self._skill_text(name).lower()
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_lifecycle_skills_route_docs_tooling_selector_and_t8_a11_statuses(self):
        shared_terms = [
            "docs_tooling_selector",
            "docs-tooling-decision.md",
            "docs_as_code_impact",
            "not_applicable",
            "present_unverified",
            "present_verified",
            "proposal_staged",
            "explicit_gap_accepted",
            "approval_required",
            "no forced install",
            "no ci activation without approval",
            "hosted docs approval",
            "db introspection approval",
        ]

        for name in [
            "workspace-discovery-auditor",
            "implementation-planner",
            "test-eval-designer",
            "risk-reviewer",
        ]:
            text = self._skill_text(name).lower()
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_lifecycle_skills_route_standards_trigger_policy(self):
        shared_terms = [
            "standards_trigger_policy",
            "governance-proposal.md",
            "adr trigger policy",
            "c4",
            "arc42",
            "openapi source of truth",
            "swagger ui",
            "asyncapi",
            "semver impact",
            "keep a changelog",
            "codeowners status",
            "github actions",
            "least privilege",
            "proposal_staged",
            "approval_required",
            "no external activation without approval",
            "no forced external activation",
        ]

        for name in [
            "workspace-discovery-auditor",
            "implementation-planner",
            "risk-reviewer",
            "pr-release-operator",
        ]:
            text = self._skill_text(name).lower()
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_lifecycle_skills_route_quality_testing_evals_methodology(self):
        shared_terms = [
            "quality_testing_evals",
            "quality-strategy.md",
            "test-eval-matrix.md",
            "ci-evidence-record.md",
            "flaky-test-policy.md",
            "manual-qa-evidence.md",
            "quality_strategy_present",
            "risk_based_scope_present",
            "test_first_or_gap_present",
            "acceptance_traceability_present",
            "contract_check_present",
            "runtime_evidence_present",
            "manual_qa_evidence_present",
            "visual_a11y_evidence_present",
            "eval_spec_present",
            "eval_rerun_evidence_present",
            "current_evidence_before_completion",
            "ci_quality_gate_present",
            "flaky_test_policy_present",
            "coverage_policy_present",
            "test_data_privacy_present",
            "bug_reproduction_evidence_present",
            "regression_impact_present",
            "coverage is a signal, not proof",
            "do not force tdd",
            "do not force e2e",
            "do not force coverage",
            "do not force ai evals",
        ]

        for name in [
            "workspace-discovery-auditor",
            "requirements-author",
            "implementation-planner",
            "test-eval-designer",
            "risk-reviewer",
            "docs-maintainer",
            "pr-release-operator",
        ]:
            text = self._skill_text(name).lower()
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_lifecycle_skills_route_codex_agentic_workflow_methodology(self):
        shared_terms = [
            "codex_agentic_workflow",
            "model-reasoning-policy.md",
            "mcp-permission-review.md",
            "hook-governance.md",
            "skill-promotion-record.md",
            "agent-eval-workflow.md",
            "agentic_scope_classified",
            "control_plane_present",
            "source_of_truth_present",
            "read_only_discovery_complete",
            "model_reasoning_policy_present",
            "fresh_context_handoff_present",
            "ownership_split_present",
            "subagent_parallelism_safe",
            "approval_boundary_present",
            "mcp_permission_review_present",
            "hook_activation_approval_present",
            "plugin_boundary_present",
            "skill_promotion_evidence_present",
            "automation_manual_stability_present",
            "agent_eval_workflow_present",
            "memory_policy_present",
            "agentic_evidence_before_completion",
            "memory as recall only",
            "no silent activation",
            "approval_required",
            "present_unverified",
        ]

        for name in [
            "project-lifecycle-orchestrator",
            "workspace-discovery-auditor",
            "requirements-author",
            "implementation-planner",
            "agent-team-designer",
            "test-eval-designer",
            "risk-reviewer",
            "docs-maintainer",
            "pr-release-operator",
            "learning-loop-maintainer",
            "automation-promoter",
        ]:
            text = self._skill_text(name).lower()
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_lifecycle_skills_route_frontend_methodology(self):
        shared_terms = [
            "frontend",
            "frontend-flow-spec.md",
            "frontend-state-matrix.md",
            "frontend-visual-qa.md",
            "frontend-accessibility-review.md",
            "frontend-performance-budget.md",
            "frontend_user_flow_acceptance_present",
            "frontend_component_state_matrix_present",
            "frontend_design_system_boundary_present",
            "frontend_api_contract_alignment_present",
            "frontend_runtime_console_evidence_present",
            "frontend_interaction_test_evidence_present",
            "storybook",
            "feature-sliced design",
            "wcag 2.2 aa",
            "browser/runtime evidence",
            "console status",
            "playwright trace",
            "no secrets",
            "approval_required",
            "present_unverified",
        ]

        for name in [
            "workspace-discovery-auditor",
            "requirements-author",
            "implementation-planner",
            "test-eval-designer",
            "risk-reviewer",
            "docs-maintainer",
            "pr-release-operator",
        ]:
            text = self._skill_text(name).lower()
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_lifecycle_skills_route_backend_methodology(self):
        shared_terms = [
            "track 9 backend methodology",
            "backend",
            "backend-service-overview.md",
            "backend-runtime-behavior.md",
            "backend-dependency-failure-matrix.md",
            "backend-observability-map.md",
            "backend-slo-sheet.md",
            "backend-health-check-contract.md",
            "backend-job-queue-contract.md",
            "backend-data-consistency-record.md",
            "backend-config-secrets-manifest.md",
            "backend-release-rollback-notes.md",
            "backend-operational-runbook.md",
            "backend_service_boundary_present",
            "backend_runtime_behavior_present",
            "backend_dependency_failure_matrix_present",
            "backend_observability_contract_present",
            "backend_slo_or_gap_present",
            "backend_health_probe_contract_present",
            "backend_job_queue_contract_present",
            "backend_data_consistency_strategy_present",
            "backend_config_secrets_boundary_present",
            "backend_security_reviewed",
            "backend_rollback_plan_present",
            "microservices conditional",
            "runtime/failure/observability/security/rollback evidence",
            "approval_required",
            "explicit_gap_accepted",
        ]

        for name in [
            "workspace-discovery-auditor",
            "requirements-author",
            "implementation-planner",
            "test-eval-designer",
            "risk-reviewer",
            "docs-maintainer",
            "pr-release-operator",
        ]:
            text = self._skill_text(name).lower()
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_workspace_discovery_records_backend_delivery_signals_without_execution(self):
        discovery = self._skill_text("workspace-discovery-auditor").lower()

        for expected in [
            "backend stack",
            "backend commands",
            "ci",
            "apis",
            "db",
            "queues",
            "workers",
            "deployment manifests",
            "security signals",
            "without executing deployments",
            "external writes",
            "approval_required",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, discovery)

    def test_lifecycle_skills_route_api_integrations_methodology(self):
        shared_terms = [
            "track 9 api & integrations methodology",
            "api-integrations",
            "api-inventory.md",
            "api-contract-review.md",
            "api-error-catalog.md",
            "api-auth-authorization-matrix.md",
            "api-consumer-map.md",
            "api-compatibility-record.md",
            "api-contract-test-matrix.md",
            "generated-sdk-manifest.md",
            "webhook-event-contract.md",
            "external-integration-approval.md",
            "api_contract_source_present",
            "api_consumer_map_present",
            "api_breaking_change_reviewed",
            "api_security_reviewed",
            "api_error_contract_present",
            "api_contract_test_matrix_present",
            "event_delivery_contract_present",
            "generated_client_manifest_present",
            "external_write_approval_present",
            "swagger ui is not source of truth",
            "contract drift blocks completion claims",
            "external writes are approval_required",
            "no universal graphql/grpc/event default",
            "present_unverified",
            "explicit_gap_accepted",
        ]

        for name in [
            "workspace-discovery-auditor",
            "implementation-planner",
            "test-eval-designer",
            "risk-reviewer",
            "docs-maintainer",
            "pr-release-operator",
        ]:
            text = self._skill_text(name).lower()
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_risk_reviewer_generalizes_two_stage_review_for_risky_slices(self):
        risk_reviewer = self._skill_text("risk-reviewer").lower()

        for expected in [
            "generalized two-stage review",
            "review-slice.md",
            "runlog.md",
            "stage 1: spec compliance",
            "stage 2: quality/risk",
            "acceptance criteria",
            "source constraints",
            "public contract",
            "migration",
            "security-sensitive",
            "data migration",
            "release packaging",
            "parallel work",
            "spec compliance verdict",
            "quality/risk verdict",
            "do not collapse",
            "generic review only",
            "quality/risk before spec compliance",
            "ready verdict with missing evidence",
        ]:
            self.assertIn(expected, risk_reviewer)

    def test_legacy_onboarding_lifecycle_wording_blocks_refactor_before_orientation(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()
        discovery = self._skill_text("workspace-discovery-auditor").lower()

        for expected in [
            "legacy_onboarding",
            "legacy-onboarding.md",
            "onboarding-map.md",
            "source map",
            "entry points",
            "run commands",
            "docs debt",
            "verification status",
            "present_unverified",
            "first safe documentation slice",
            "do not refactor",
        ]:
            self.assertIn(expected, orchestrator)

        for expected in [
            "legacy_onboarding_signals",
            "present_unverified",
            "docs debt",
            "run commands",
            "do not claim",
        ]:
            self.assertIn(expected, discovery)

    def test_api_migration_lifecycle_wording_requires_migration_plan_before_release(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()
        discovery = self._skill_text("workspace-discovery-auditor").lower()

        for expected in [
            "api_migration",
            "api-migration.md",
            "migration-plan.md",
            "openapi",
            "asyncapi",
            "consumers",
            "generated clients",
            "backwards compatibility",
            "deprecation",
            "examples",
            "rollout",
            "release impact",
            "owner review",
            "do not release",
            "do not implement",
        ]:
            self.assertIn(expected, orchestrator)

        for expected in [
            "api_migration_signals",
            "present_unverified",
            "contract sources",
            "generated clients",
            "do not claim compatibility",
        ]:
            self.assertIn(expected, discovery)

    def test_ai_eval_lifecycle_wording_requires_eval_spec_before_quality_claims(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()
        discovery = self._skill_text("workspace-discovery-auditor").lower()

        for expected in [
            "ai_eval_regression",
            "ai-eval-regression.md",
            "ai-eval-spec.md",
            "baseline",
            "dataset",
            "no-secrets",
            "rubric",
            "threshold",
            "rerun command",
            "prompt/context",
            "retrieval metrics",
            "judge policy",
            "latency",
            "cost",
            "grounding",
            "one-factor-at-a-time",
            "do not claim quality",
            "do not change model",
        ]:
            self.assertIn(expected, orchestrator)

        for expected in [
            "ai_eval_signals",
            "present_unverified",
            "baseline",
            "dataset",
            "judge rubric",
            "do not claim quality",
        ]:
            self.assertIn(expected, discovery)

    def test_lifecycle_skills_route_llm_ai_rag_methodology_without_forced_live_calls(self):
        shared_terms = [
            "llm_ai_rag",
            "ai behavior promise",
            "baseline eval",
            "eval rerun evidence",
            "app-backed eval path",
            "prompt-contract.md",
            "model-decision-record.md",
            "structured-output-schema.md",
            "ai-tool-contract.md",
            "rag-source-inventory.md",
            "rag-retrieval-config.md",
            "rag-eval-report.md",
            "agent-workflow-map.md",
            "guardrail-matrix.md",
            "trace-evidence-packet.md",
            "ai-cost-latency-budget.md",
            "safety evidence",
            "cost evidence",
            "do not force one eval runner",
            "do not force multi-agent architecture",
            "do not run live model calls",
            "approval_required",
        ]

        for name in [
            "workspace-discovery-auditor",
            "project-lifecycle-orchestrator",
            "requirements-author",
            "implementation-planner",
            "test-eval-designer",
            "risk-reviewer",
            "docs-maintainer",
            "learning-loop-maintainer",
        ]:
            text = self._skill_text(name).lower()
            with self.subTest(name=name):
                for expected in shared_terms:
                    self.assertIn(expected, text)

    def test_native_mobile_lifecycle_wording_requires_platform_runtime_evidence(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()
        discovery = self._skill_text("workspace-discovery-auditor").lower()

        for expected in [
            "native_mobile_feature",
            "native-mobile-feature.md",
            "platform assumptions",
            "ios",
            "android",
            "permissions",
            "offline state",
            "simulator",
            "emulator",
            "device",
            "logs",
            "screenshots",
            "build command",
            "manual device gap",
            "do not claim runtime behavior",
            "do not change permissions",
        ]:
            self.assertIn(expected, orchestrator)

        for expected in [
            "native_mobile_signals",
            "present_unverified",
            "permissions",
            "offline",
            "simulator/emulator",
            "screenshots",
            "do not claim runtime behavior",
        ]:
            self.assertIn(expected, discovery)

    def test_desktop_local_lifecycle_wording_requires_local_runtime_evidence(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()
        discovery = self._skill_text("workspace-discovery-auditor").lower()

        for expected in [
            "desktop_local_first",
            "desktop-local-first.md",
            "desktop platform assumptions",
            "filesystem permissions",
            "local data",
            "local db",
            "indexing",
            "background jobs",
            "privacy",
            "app logs",
            "runtime log check",
            "build command",
            "recovery path",
            "manual os gap",
            "do not claim desktop runtime behavior",
            "do not change filesystem access",
        ]:
            self.assertIn(expected, orchestrator)

        for expected in [
            "desktop_local_signals",
            "present_unverified",
            "filesystem permissions",
            "local db",
            "background jobs",
            "privacy",
            "app logs",
            "recovery path",
            "do not claim desktop runtime behavior",
        ]:
            self.assertIn(expected, discovery)

    def test_data_migration_lifecycle_wording_requires_database_safety_evidence(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()
        discovery = self._skill_text("workspace-discovery-auditor").lower()

        for expected in [
            "data_migration",
            "data-migration.md",
            "migration-plan.md",
            "database-dictionary.md",
            "schema change",
            "backfill",
            "data quality",
            "pii",
            "sensitive fields",
            "retention",
            "rollback",
            "validation",
            "production db",
            "dry run",
            "owner review",
            "do not access production data",
            "do not run migration",
        ]:
            self.assertIn(expected, orchestrator)

        for expected in [
            "data_migration_signals",
            "present_unverified",
            "schema",
            "backfill",
            "pii",
            "retention",
            "rollback",
            "validation",
            "dry run",
            "do not claim migration safety",
        ]:
            self.assertIn(expected, discovery)

    def test_database_data_lifecycle_wording_requires_full_methodology_contract(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()
        discovery = self._skill_text("workspace-discovery-auditor").lower()

        for expected in [
            "database_data",
            "database-inventory.md",
            "database-migration-plan.md",
            "database-data-contract.md",
            "database-backup-restore-evidence.md",
            "database-production-access-approval.md",
            "database_migration_plan_present",
            "database_backup_restore_evidence_present",
            "database_constraints_integrity_review_present",
            "database_production_access_approval_present",
            "approval_required",
            "no universal database tooling default",
            "do not access production data",
            "do not run destructive migration",
        ]:
            self.assertIn(expected, orchestrator)

        for expected in [
            "database_data_signals",
            "migration_tools",
            "destructive_change_sources",
            "production_access_sources",
            "pipeline_sources",
            "rag_ingestion_sources",
            "present_unverified",
            "approval_required",
            "do not claim database safety",
        ]:
            self.assertIn(expected, discovery)

    def test_security_sensitive_lifecycle_wording_requires_risk_review_and_approval(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()
        discovery = self._skill_text("workspace-discovery-auditor").lower()
        risk_reviewer = self._skill_text("risk-reviewer").lower()

        for expected in [
            "security_sensitive_change",
            "security-sensitive-change.md",
            "security-risk-review.md",
            "threat surface",
            "authn",
            "authz",
            "permissions",
            "payment",
            "billing",
            "secrets",
            "pii",
            "sensitive data",
            "abuse controls",
            "rate limit",
            "audit logging",
            "tests",
            "rollback",
            "owner review",
            "approval",
            "do not change auth",
            "do not process payments",
            "codex security",
            "explicitly requested",
        ]:
            self.assertIn(expected, orchestrator)

        for expected in [
            "security_sensitive_signals",
            "present_unverified",
            "authn",
            "authz",
            "permissions",
            "payment",
            "secrets",
            "pii",
            "abuse controls",
            "audit logging",
            "do not claim security safety",
        ]:
            self.assertIn(expected, discovery)

        for expected in [
            "security-sensitive",
            "security-risk-review.md",
            "threat surface",
            "authn",
            "authz",
            "payment",
            "secrets",
            "pii",
            "approval",
            "rollback",
        ]:
            self.assertIn(expected, risk_reviewer)

    def test_ci_stabilization_lifecycle_wording_requires_failure_evidence_and_no_remote_mutation(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()
        discovery = self._skill_text("workspace-discovery-auditor").lower()
        risk_reviewer = self._skill_text("risk-reviewer").lower()

        for expected in [
            "ci_stabilization",
            "ci-stabilization.md",
            "ci-stabilization-report.md",
            "failing job",
            "command",
            "logs",
            "environment",
            "deterministic",
            "flaky",
            "classification",
            "failure evidence",
            "isolation plan",
            "local reproduction",
            "rerun evidence",
            "remote ci",
            "github actions",
            "approval",
            "do not change ci settings",
            "do not rerun remote ci",
        ]:
            self.assertIn(expected, orchestrator)

        for expected in [
            "ci_stabilization_signals",
            "present_unverified",
            "workflow",
            "failure log",
            "failing job",
            "command",
            "environment",
            "test result",
            "flaky",
            "local reproduction",
            "rerun",
            "do not claim ci health",
        ]:
            self.assertIn(expected, discovery)

        for expected in [
            "ci stabilization",
            "ci-stabilization-report.md",
            "deterministic",
            "flaky",
            "remote ci",
            "approval",
            "residual risk",
        ]:
            self.assertIn(expected, risk_reviewer)

    def test_release_packaging_lifecycle_wording_requires_readiness_and_publish_approval(self):
        orchestrator = self._skill_text("project-lifecycle-orchestrator").lower()
        discovery = self._skill_text("workspace-discovery-auditor").lower()
        risk_reviewer = self._skill_text("risk-reviewer").lower()
        release_operator = self._skill_text("pr-release-operator").lower()

        for expected in [
            "release_packaging",
            "release-packaging.md",
            "release-readiness.md",
            "release scope",
            "package metadata",
            "version",
            "semver",
            "changelog",
            "build evidence",
            "test evidence",
            "docs evidence",
            "security notes",
            "license",
            "artifacts",
            "publish approval",
            "tag",
            "package registry",
            "rollback",
            "owner review",
            "residual risk",
            "do not publish",
            "do not tag",
            "do not create release",
            "do not upload artifacts",
        ]:
            self.assertIn(expected, orchestrator)

        for expected in [
            "release_packaging_signals",
            "present_unverified",
            "package metadata",
            "version",
            "semver",
            "changelog",
            "build evidence",
            "test evidence",
            "docs evidence",
            "security notes",
            "license",
            "artifacts",
            "rollback",
            "publish approval",
            "do not claim release readiness",
        ]:
            self.assertIn(expected, discovery)

        for expected in [
            "release packaging",
            "release-readiness.md",
            "semver",
            "changelog",
            "publish approval",
            "residual risk",
        ]:
            self.assertIn(expected, risk_reviewer)
            self.assertIn(expected, release_operator)

    def test_implementation_planner_enforces_no_placeholder_plan_quality(self):
        planner = self._skill_text("implementation-planner").lower()

        for expected in [
            "no-placeholder",
            "plan-quality-check.md",
            "plan_quality_check",
            "exact files",
            "owned files",
            "forbidden files",
            "exact commands",
            "expected outputs",
            "rollback",
            "evidence owner",
            "placeholder scan",
            "mechanical_change",
            "plan repair",
            "stop before build",
            "vague validation",
            "repeated-by-reference",
        ]:
            self.assertIn(expected, planner)

    def test_skills_state_track_two_boundaries(self):
        for name in SKILL_NAMES:
            text = self._skill_text(name).lower()
            with self.subTest(name=name):
                self.assertIn("track 2", text)
                self.assertIn("staged", text)
                self._assert_negative_boundary(
                    name, text, SECRET_BOUNDARY_PATTERNS, "secret storage"
                )
                self._assert_negative_boundary(
                    name,
                    text,
                    AUTOMATION_BOUNDARY_PATTERNS,
                    "active automation creation",
                )
                self._assert_negative_boundary(
                    name, text, CONFIG_BOUNDARY_PATTERNS, "config mutation"
                )
                self._assert_negative_boundary(
                    name,
                    text,
                    EVIDENCE_BOUNDARY_PATTERNS,
                    "verification evidence claims",
                )
                self.assertIn("approval", text)
                for pattern in FORBIDDEN_PERMISSIVE_PATTERNS:
                    self.assertNotRegex(text, pattern)

    def test_automation_skill_is_candidate_only(self):
        text = self._skill_text("automation-promoter").lower()
        self.assertIn("candidate_only", text)
        self.assertIn("manual stability evidence", text)

    def _skill_text(self, name: str) -> str:
        path = SKILLS / name / "SKILL.md"
        self.assertTrue(path.exists(), f"{name} must include SKILL.md")
        return path.read_text(encoding="utf-8")

    def _metadata_text(self, name: str) -> str:
        path = SKILLS / name / "agents" / "openai.yaml"
        self.assertTrue(path.exists(), f"{name} must include agents/openai.yaml")
        return path.read_text(encoding="utf-8")

    def _assert_frontmatter_has_only_name_and_description(
        self, name: str, text: str
    ) -> None:
        match = re.match(r"^---\n(?P<frontmatter>.*?)\n---", text, re.DOTALL)
        self.assertIsNotNone(match, f"{name} must start with frontmatter")
        lines = [
            line.strip()
            for line in match.group("frontmatter").splitlines()
            if line.strip()
        ]
        self.assertEqual(2, len(lines), f"{name} frontmatter must have only two keys")
        self.assertEqual(f"name: {name}", lines[0])
        self.assertRegex(lines[1], r"^description: .+$")

    def _assert_negative_boundary(
        self, name: str, text: str, patterns: list[str], boundary: str
    ) -> None:
        self.assertTrue(
            any(re.search(pattern, text) for pattern in patterns),
            f"{name} must include a negative boundary for {boundary}",
        )

    def _assert_reference_links_resolve(self, name: str, text: str) -> None:
        links = {
            match.group(1).strip()
            for match in MARKDOWN_LINK_RE.finditer(text)
            if REFERENCE_LINK_RE.match(match.group(1).strip())
        }
        self.assertEqual(set(REQUIRED_SKILL_LINKS), links)

        reference_root = (SKILLS / "references").resolve()
        for link in sorted(links):
            path = (SKILLS / name / link).resolve()
            self.assertTrue(
                path.is_relative_to(reference_root),
                f"{name} reference link escapes shared references: {link}",
            )
            self.assertTrue(path.exists(), f"{name} reference link must resolve: {link}")


if __name__ == "__main__":
    unittest.main()
