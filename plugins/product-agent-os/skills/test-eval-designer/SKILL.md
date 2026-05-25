---
name: test-eval-designer
description: Use when a Product-Agent OS plan needs deterministic tests, manual checks, eval gates, or test gap documentation before implementation or review.
---

# Test Eval Designer

## Trigger

Use this skill when a Product-Agent OS project needs test commands, eval criteria, quality gates, or explicit verification evidence requirements before implementation, review, or handoff.

## Boundaries

This is a Track 2 skill. Produce a staged `test_eval_packet` only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not write `TEST.md` or `EVALS.md` directly, edit code, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim test coverage, eval quality, command success, runtime behavior, or readiness without evidence from the current run.
Ask for approval before any write, external action, expanded scope, dependency installation, or operation outside the allowed workspace.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- `requirements_packet` with acceptance criteria, constraints, risks, and open questions.
- `implementation_plan_packet` with slices, proposed gates, rollback notes, and ownership boundaries.
- `workspace_audit` or stack summary with available build, lint, test, docs, visual, and eval commands.
- Known test, lint, build, docs, browser, native, API, visual, or eval commands and their limits.
- Risk profile, approval limits, acceptance criteria, and required verification evidence.
- Acceptance scenario packet when behavior changes: `.codex/artifact-templates/acceptance-scenarios.md`, ATDD, BDD, `requirement -> scenario -> check -> evidence owner`, Given, When, Then, equivalent behavior format, business rule, edge case, non-goal, explicit gap, and evidence owner.
- Business/Product methodology packet when product, MVP, user value, analytics, release measurement, or workflow promotion claims are present: `product_hypothesis_present`, `value_proposition_evidence_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, `metric_scope_classified`, `.codex/artifact-templates/tracking-plan.md`, metric evidence, feedback evidence, release measurement evidence, and accepted gap status.

## Process

1. Validate that requirements and implementation plan packets are staged and the lifecycle state is `team_ready` or equivalent pre-build handoff.
2. Map every acceptance criterion to at least one deterministic check when a suitable command exists.
3. For behavior changes, require acceptance scenarios or an explicit gap before implementation; block implementation before acceptance scenarios when no gap is accepted.
4. Verify ATDD or BDD traceability as `requirement -> scenario -> check -> evidence owner`.
5. Accept Given, When, Then or an equivalent behavior format when it names the business rule, edge case, non-goal, explicit gap, and evidence owner.
6. For product, MVP, value, analytics, release measurement, or workflow promotion claims, map `product_hypothesis_present`, `value_proposition_evidence_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, and `metric_scope_classified` to deterministic checks, eval gates, manual evidence, or explicit gaps.
7. For product analytics, require `.codex/artifact-templates/tracking-plan.md` checks for event taxonomy, property definitions, validation evidence, dashboard/report evidence, owner, and privacy classification.
8. Prefer test-first or eval-first gates before implementation for behavior changes, contract changes, AI/RAG changes, product measurement changes, and documentation quality changes.
9. Add manual checks only when runtime, visual, UX, device, owner review, qualitative feedback, or external-environment verification cannot be automated in the available workspace.
10. Add eval gates for AI behavior, UX judgment, documentation quality, product outcome claims, subjective acceptance, or long-horizon quality criteria.
11. Add documentation checks for architecture docs, API/event contracts, UI component docs, database docs, tracking plans, metrics, and release/user-facing docs when those artifacts are impacted.
12. Mark missing, unavailable, unknown, or approval-gated commands as test gaps instead of inventing evidence.
13. Define thresholds, pass criteria, failure signals, artifacts to inspect, and evidence required for each check or eval gate.
14. For conditional readiness gates, test applicable/missing/not-applicable/accepted-gap transitions with `readiness_statuses`: `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`.
15. Detection alone can only support `present_unverified`; `present_verified` requires current command evidence, owner evidence, or verified artifact evidence, and each gate must name owner, applicability reason, and residual risk.
16. Keep proposed artifacts staged as `TEST.md` and `EVALS.md`; do not write them directly.
17. Return `build_active` only when deterministic checks, manual checks, eval gates, docs checks, thresholds, evidence, gaps, and conditional readiness gates are explicit.

## Outputs

Return a test and eval packet:

```yaml
test_eval_packet:
  deterministic_checks: []
  test_first_checks: []
  acceptance_scenario_checks:
    artifact: ".codex/artifact-templates/acceptance-scenarios.md"
    traceability: "requirement -> scenario -> check -> evidence owner"
    format: "Given/When/Then | equivalent behavior format | explicit gap"
    business_rule: ""
    edge_case: ""
    non_goal: ""
    evidence_owner: ""
  business_product_checks:
    gates:
      - "product_hypothesis_present"
      - "value_proposition_evidence_present"
      - "analytics_tracking_plan_present"
      - "qualitative_feedback_loop_present"
      - "release_measurement_evidence_present"
      - "decision_horizon_present"
      - "outcome_metric_level_separated"
      - "metric_scope_classified"
    tracking_plan_artifact: ".codex/artifact-templates/tracking-plan.md"
    deterministic_checks: []
    manual_feedback_checks: []
    eval_gates: []
    gaps: []
  manual_checks: []
  evals: []
  documentation_checks: []
  conditional_readiness_checks:
    readiness_statuses: "not_applicable | applicable_missing | present_unverified | present_verified | proposal_staged | explicit_gap_accepted | approval_required"
    applicable_missing_cases: []
    not_applicable_cases: []
    explicit_gap_accepted_cases: []
    present_verified_evidence: []
    owner: ""
    applicability_reason: ""
    residual_risk: ""
  thresholds: []
  evidence_required: []
  gaps: []
  assumptions: []
  files_proposed:
    - "TEST.md"
    - "EVALS.md"
  next_lifecycle_state: "build_active"
```

## Conditional Readiness Gates

Use conditional readiness gates to prove applicability and evidence transitions, not just artifact names. `readiness_statuses` are `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`. Detection alone can only produce `present_unverified`; tests/evals should fail if a route claims `present_verified` without command, owner, or artifact evidence. Record `not_applicable` with an applicability reason, `applicable_missing` when evidence is absent, and `explicit_gap_accepted` only with owner, residual risk, and follow-up condition.

## Docs Tooling Selector

Use `docs_tooling_selector` with `docs-tooling-decision.md` to close `docs_as_code_impact` without forcing a docs portal. Record `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, or `approval_required`; selected tools, rejected tools, evidence owner, maintenance owner, no forced install, no CI activation without approval, hosted docs approval, DB introspection approval, docs-light, and internal-only reasons.

## Requirements Domain Methodology

Map Requirements & Domain artifacts to checks and evals: `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, and `domain-review-record.md`. Test `requirements_traceability_present`, `requirement_quality_present`, `constraints_traceability_present`, `declarative_acceptance_scenarios_present`, `business_rules_present`, `domain_expert_review_present`, `requirement_change_impact_review_present`, `accepted_gap_recorded`, and `requirements_evidence_before_implementation` with deterministic checks, owner review, manual evidence, or explicit gaps. Reject scenarios with UI selectors, database internals, function names, or test harness details as business-facing acceptance evidence.

## Solution Architecture Methodology

Use Solution Architecture routing when a slice touches architecture boundary, public contract, data ownership, trust boundary, runtime topology, observability, rollback, or parallel agent ownership. Track `solution_architecture_scope_present`, `architecture_boundary_per_slice`, `boundary_responsibility_owner_present`, `adr_for_architecture_decision`, `diagram_render_check_present`, `runtime_deployment_topology_present`, `observability_architecture_present`, `migration_rollback_path_present`, and `architecture_fitness_function_present`.

Stage or request `.codex/artifact-templates/architecture-overview.md`, `.codex/artifact-templates/adr.md`, `.codex/artifact-templates/architecture-review-record.md`, `.codex/artifact-templates/architecture-fitness-functions.md`, `.codex/artifact-templates/trust-boundary-map.md`, and `.codex/artifact-templates/architecture-docs-tooling-decision.md` when the corresponding gate applies. C4/arc42 only when applicable; architecture-as-code is conditional; Well-Architected review is conditional. Use `not_applicable` or `explicit_gap_accepted` with owner, reason, residual risk and follow-up condition rather than forcing diagrams, cloud review or docs tooling.

## Track 9 Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.

## Quality Testing & Evals Methodology

Use `quality_testing_evals` when quality, test, eval, runtime, manual QA, visual/a11y, CI, flaky, coverage, test data privacy, bugfix, regression, release, readiness, or completion evidence applies. Stage or request `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md` when the corresponding gate applies.

Track `quality_strategy_present`, `risk_based_scope_present`, `test_first_or_gap_present`, `acceptance_traceability_present`, `contract_check_present`, `runtime_evidence_present`, `manual_qa_evidence_present`, `visual_a11y_evidence_present`, `eval_spec_present`, `eval_rerun_evidence_present`, `current_evidence_before_completion`, `ci_quality_gate_present`, `flaky_test_policy_present`, `coverage_policy_present`, `test_data_privacy_present`, `bug_reproduction_evidence_present`, and `regression_impact_present`. Coverage is a signal, not proof. Do not force TDD, do not force E2E, do not force coverage, and do not force AI evals when not applicable; use `not_applicable`, `present_unverified`, `explicit_gap_accepted`, or `approval_required` with owner, reason, residual risk and follow-up condition.

## Verification

Check that each acceptance criterion maps to a deterministic check, manual check, eval gate, or explicit gap. For behavior changes, check that acceptance scenarios map `requirement -> scenario -> check -> evidence owner`, use ATDD/BDD or equivalent behavior format, and name business rule, edge case, non-goal, explicit gap, and evidence owner. Check that conditional readiness gates exercise applicable_missing, not_applicable, explicit_gap_accepted, present_unverified, present_verified, and approval_required states where relevant. Check that thresholds are observable, evidence is named, approval needs are flagged, and every proposed artifact remains staged. Do not claim without evidence.

## Failure Modes

- If acceptance criteria are missing, stop and route to `requirements-author`.
- If behavior changes lack acceptance scenarios and no explicit gap is accepted, stop with `implementation before acceptance scenarios`.
- If Business/Product methodology applies and `product_hypothesis_present`, `value_proposition_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, or `metric_scope_classified` cannot be mapped to evidence or an accepted gap, stop before build.
- If analytics or telemetry claims lack `analytics_tracking_plan_present` or `.codex/artifact-templates/tracking-plan.md`, stop before build or record an explicit accepted gap.
- If qualitative feedback is required but `qualitative_feedback_loop_present` lacks a check or owner evidence, keep the packet out of `build_active`.
- If release success is claimed but `release_measurement_evidence_present` is missing, keep the packet out of `build_active`.
- If there is a scenario without requirement, scenario without check, or scenario without evidence owner, stop and route to `requirements-author`.
- If the packet implies `BDD replaces tests`, reject it and map the scenario to unit tests, integration tests, contract tests, manual checks, or evals.
- If implementation slices or ownership are missing, stop and route to `implementation-planner` or `agent-team-designer`.
- If commands are unknown, record test gaps and discovery needs.
- If eval criteria are subjective but unstated, return open questions and proposed rubric fields.
- If approval is needed, stop before writes, runtime actions, or external actions.

## Final Response Contract

Return status, lifecycle state, `test_eval_packet`, files proposed, commands proposed or already evidenced, verification evidence, unsupported claims, approval requirements, risks, and the next recommended skill.
