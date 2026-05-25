---
name: implementation-planner
description: Use when staged requirements need implementation slices, verification gates, rollback, and ownership boundaries.
---

# Implementation Planner

## Trigger

Use this skill when requirements are staged and need implementation slices, verification gates, rollback, and ownership boundaries.

## Boundaries

This is a Track 2 skill. Produce a staged implementation plan packet only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not write `PLAN.md` or `TEST.md` directly, edit code, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim plan readiness, command success, test coverage, or runtime behavior without evidence from the current run.
Ask for approval before any write, external action, expanded scope, dependency installation, or operation outside the allowed workspace.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- `requirements_packet` with goal, scope, constraints, acceptance criteria, and open questions.
- `workspace_audit` packet with stack, commands, risks, and existing control-plane artifacts.
- Explicit constraints, available commands, approval limits, and rollback expectations.
- Complexity profile and lifecycle state from the orchestrator.
- Acceptance scenario packet when behavior changes: `.codex/artifact-templates/acceptance-scenarios.md`, ATDD, BDD, `requirement -> scenario -> check -> evidence owner`, Given, When, Then, equivalent behavior format, business rule, edge case, non-goal, explicit gap, and evidence owner.
- Business/Product methodology packet when product, MVP, user value, analytics, release measurement, or workflow promotion claims are present: `product_hypothesis_present`, `value_proposition_evidence_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, `metric_scope_classified`, `.codex/artifact-templates/product-brief.md`, `.codex/artifact-templates/value-proposition.md`, `.codex/artifact-templates/opportunity-tree.md`, `.codex/artifact-templates/experiment-plan.md`, `.codex/artifact-templates/tracking-plan.md`, and accepted gap status.
- Domain modeling input when `domain_model_when_complex_domain` applies: `.codex/artifact-templates/domain-modeling.md`, `.codex/artifact-templates/architecture-overview.md`, complex backend, workflow, enterprise, data-heavy, bounded context, ubiquitous language, invariant, accepted gap, `bounded_context_architecture_boundary_trace`, `context-to-boundary traceability`, `ubiquitous_language_traceability`, term-to-requirement, requirement or source, API/event/contract, UI label, code module or owner, domain expert review, and `missing domain model for complex domain`.
- UI architecture input when `fsd_structure` applies: `.codex/artifact-templates/component-card.md`, Feature-Sliced Design, layer, slice, segment, public API, import rule, `not applicable` reason, accepted gap, backend, native, simple CRUD, simple MVP, and `missing fsd structure boundary`.

## Process

1. Validate that requirements are staged and the lifecycle state is `requirements_ready`.
2. Route back to `requirements-author` if acceptance criteria, constraints, or open questions are incomplete.
3. For behavior changes, stop before implementation unless `.codex/artifact-templates/acceptance-scenarios.md` or an explicit gap maps ATDD or BDD scenarios through `requirement -> scenario -> check -> evidence owner`.
4. Accept Given, When, Then or an equivalent behavior format when it names business rule, edge case, non-goal, and evidence owner.
5. For product, MVP, value, analytics, release measurement, or workflow promotion claims, stop before build unless `product_hypothesis_present`, `value_proposition_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, and `metric_scope_classified` are present, explicitly not applicable, or accepted as gaps with owner and residual risk.
6. For analytics, telemetry, usage data, or dashboard claims, require `analytics_tracking_plan_present` and `.codex/artifact-templates/tracking-plan.md` or an accepted gap before returning `plan_ready`.
7. For discovery or product feedback loops, require `qualitative_feedback_loop_present`; for release or success claims, require `release_measurement_evidence_present`.
8. Apply `domain_model_when_complex_domain` only when the slice is complex backend, workflow, enterprise, data-heavy, multi-service, or multi-context.
9. When `domain_model_when_complex_domain` applies, require `.codex/artifact-templates/domain-modeling.md` or an accepted gap with bounded context, ubiquitous language, and invariant status before returning `plan_ready`.
10. When a domain model is required, enforce `bounded_context_architecture_boundary_trace`: every bounded context maps to architecture boundary in `.codex/artifact-templates/architecture-overview.md`, or an accepted gap names the reason and evidence owner.
11. If a bounded context has no architecture boundary mapping, stop before build with `missing bounded context architecture boundary trace`.
12. When a domain model is required, enforce `ubiquitous_language_traceability`: every ubiquitous language term maps through term-to-requirement evidence, a requirement or source, and at least one API/event/contract, UI label, code module or owner.
13. If a ubiquitous language term is untraceable, require an accepted gap names the reason and evidence owner plus domain expert review; otherwise stop before build with `missing ubiquitous language traceability`.
14. Do not force DDD for simple CRUD or simple MVP work; record `not_applicable` or accepted gap instead of adding ceremony.
15. If the workspace audit reports `missing domain model for complex domain`, stop before build and route to domain model planning or return a plan repair packet.
16. Apply `fsd_structure` only for web UI/component architecture when the workspace audit detects Feature-Sliced Design directories or the owner explicitly chooses that boundary.
17. When `fsd_structure` applies, require `.codex/artifact-templates/component-card.md` or an accepted gap with layer, slice, segment, public API, and import rule before returning `plan_ready`.
18. If `fsd_structure` applies but layer, slice, segment, public API, or import rule is missing, stop before build with `missing fsd structure boundary`.
19. Do not force FSD for backend, native, simple CRUD, or simple MVP work; record `not applicable` or accepted gap instead of adding UI architecture ceremony.
20. For every relevant methodology/tooling gate, fill conditional readiness gates with `readiness_statuses`: `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`.
21. Detection alone can only support `present_unverified`; return `plan_ready` only when applicable gates have required evidence, owner, applicability reason, and residual risk, or an explicit accepted gap.
22. Decompose work into focused slices with clear acceptance criteria and verification per slice.
23. For each slice, name the architecture boundary, test-first or eval-first path, documentation impact, acceptance scenarios, Business/Product methodology gates, domain model applicability, context-to-boundary traceability, ubiquitous language traceability, FSD applicability, and post-release measurement note.
24. Run the no-placeholder planning gate before returning `plan_ready`.
25. For every non-trivial slice, fill the `plan_quality_check` fields from `.codex/artifact-templates/plan-quality-check.md`: exact files, owned files, forbidden files, exact commands, expected outputs, rollback, evidence owner, and placeholder scan.
26. Treat vague validation, repeated-by-reference steps, command steps without expected outputs, undefined file names, and hidden "fill later" work as blocking gaps.
27. Use `mechanical_change` only for small docs, formatting, or config edits whose reduced plan still names exact files, exact commands or explicit no-command gap, rollback, evidence owner, and the mechanical_change reason.
28. If the no-placeholder gate fails, stop before build and return a plan repair packet instead of `plan_ready`.
29. Identify dependencies, file or subsystem ownership, rollback notes, risks, and command evidence needed.
30. Keep commands as proposed `commands_to_run` unless already run in the current session.
31. Route to `agent-team-designer` if ownership overlaps, parallel work is needed, or handoff risk is high.
32. Return `plan_ready` only when slices, verification gates, rollback notes, documentation impact, risks, conditional readiness gates, and `plan_quality_check` are staged.

## Outputs

Return an implementation plan packet:

```yaml
implementation_plan_packet:
  slices: []
  architecture_boundaries: []
  test_first_paths: []
  documentation_impacts: []
  fsd_structure_gate:
    signal: "fsd_structure"
    applicability: "required | not applicable | accepted gap"
    artifact: ".codex/artifact-templates/component-card.md"
    methodology: "Feature-Sliced Design"
    layer: ""
    slice: ""
    segment: ""
    public_api: ""
    import_rule: ""
    accepted_gap: ""
    not_applicable_reason: ""
  domain_model_gate:
    gate: "domain_model_when_complex_domain"
    applicability: "required | not_applicable | accepted gap"
    artifact: ".codex/artifact-templates/domain-modeling.md"
    bounded_context: ""
    architecture_boundary: ""
    context_to_boundary_traceability: "bounded_context_architecture_boundary_trace"
    boundary_mapping_artifact: ".codex/artifact-templates/architecture-overview.md"
    ubiquitous_language: ""
    ubiquitous_language_traceability: "ubiquitous_language_traceability"
    term_to_requirement: ""
    requirement_or_source: ""
    api_event_contract: ""
    ui_label: ""
    code_module_or_owner: ""
    domain_expert_review: ""
    invariant: ""
    accepted_gap: ""
    not_applicable_reason: ""
  acceptance_scenarios:
    artifact: ".codex/artifact-templates/acceptance-scenarios.md"
    traceability: "requirement -> scenario -> check -> evidence owner"
    format: "Given/When/Then | equivalent behavior format | explicit gap"
    business_rule: ""
    edge_case: ""
    non_goal: ""
    evidence_owner: ""
  business_product_gate:
    gates:
      - "product_hypothesis_present"
      - "value_proposition_evidence_present"
      - "analytics_tracking_plan_present"
      - "qualitative_feedback_loop_present"
      - "release_measurement_evidence_present"
      - "decision_horizon_present"
      - "outcome_metric_level_separated"
      - "metric_scope_classified"
    artifacts:
      - ".codex/artifact-templates/product-brief.md"
      - ".codex/artifact-templates/value-proposition.md"
      - ".codex/artifact-templates/opportunity-tree.md"
      - ".codex/artifact-templates/experiment-plan.md"
      - ".codex/artifact-templates/tracking-plan.md"
    status: "not_applicable | applicable_missing | present_unverified | present_verified | explicit_gap_accepted"
    residual_risk: ""
  conditional_readiness_gates:
    readiness_statuses:
      - "not_applicable"
      - "applicable_missing"
      - "present_unverified"
      - "present_verified"
      - "proposal_staged"
      - "explicit_gap_accepted"
      - "approval_required"
    gates:
      - gate: ""
        applies_when: ""
        applicability_reason: ""
        required_evidence: []
        status: ""
        owner: ""
        accepted_gap: ""
        residual_risk: ""
  plan_quality_check:
    status: "pending | passed | blocked | mechanical_change"
    exact_files: []
    owned_files: []
    forbidden_files: []
    exact_commands: []
    expected_outputs: []
    rollback: []
    evidence_owner: ""
    placeholder_scan: ""
    mechanical_change_reason: ""
    blocking_gaps: []
  dependencies: []
  commands_to_run: []
  verification_gates: []
  rollback_notes: []
  risks: []
  assumptions: []
  files_proposed:
    - "PLAN.md"
    - "TEST.md"
  next_lifecycle_state: "plan_ready"
```

## Conditional Readiness Gates

Use conditional readiness gates before returning `plan_ready`. `readiness_statuses` are `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`. Detection alone can only produce `present_unverified`; `present_verified` requires current command evidence, owner evidence, or verified artifact evidence. Use `applicable_missing` for applicable gates without evidence, `not_applicable` only with an applicability reason, and `explicit_gap_accepted` only with owner, reason, residual risk, and follow-up condition.

## Docs Tooling Selector

Use `docs_tooling_selector` with `docs-tooling-decision.md` to close `docs_as_code_impact` without forcing a docs portal. Record `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, or `approval_required`; selected tools, rejected tools, evidence owner, maintenance owner, no forced install, no CI activation without approval, hosted docs approval, DB introspection approval, docs-light, and internal-only reasons.

## Standards Trigger Policy

Use `standards_trigger_policy` before `plan_ready` when the slice touches architecture, API, release, ownership, or CI governance. Require ADR trigger policy for architecture boundary, API contract, storage, auth/security, irreversible migration, or automation activation. Route architecture docs through C4 and arc42 only as far as the project needs. Treat OpenAPI source of truth as the HTTP contract and Swagger UI as optional tooling; treat AsyncAPI as the event contract path. For release-bound public changes, require SemVer impact and Keep a Changelog categories. For ownership or CI governance, stage `governance-proposal.md` with CODEOWNERS status, GitHub Actions workflow names, commands, permissions, triggers, owners, least privilege, `proposal_staged`, `approval_required`, no external activation without approval, and no forced external activation.

## Requirements Domain Methodology

Before `plan_ready`, require the applicable Requirements & Domain artifacts: `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, and `domain-review-record.md`. Block implementation when `requirements_traceability_present`, `requirement_quality_present`, `constraints_traceability_present`, `declarative_acceptance_scenarios_present`, `business_rules_present`, `domain_expert_review_present`, `requirement_change_impact_review_present`, `accepted_gap_recorded`, or `requirements_evidence_before_implementation` is applicable but missing. Use bounded contexts for ownership split only when domain complexity applies; do not force DDD on simple CRUD or simple MVP.

## Solution Architecture Methodology

Use Solution Architecture routing when a slice touches architecture boundary, public contract, data ownership, trust boundary, runtime topology, observability, rollback, or parallel agent ownership. Track `solution_architecture_scope_present`, `architecture_boundary_per_slice`, `boundary_responsibility_owner_present`, `adr_for_architecture_decision`, `diagram_render_check_present`, `runtime_deployment_topology_present`, `observability_architecture_present`, `migration_rollback_path_present`, and `architecture_fitness_function_present`.

Stage or request `.codex/artifact-templates/architecture-overview.md`, `.codex/artifact-templates/adr.md`, `.codex/artifact-templates/architecture-review-record.md`, `.codex/artifact-templates/architecture-fitness-functions.md`, `.codex/artifact-templates/trust-boundary-map.md`, and `.codex/artifact-templates/architecture-docs-tooling-decision.md` when the corresponding gate applies. C4/arc42 only when applicable; architecture-as-code is conditional; Well-Architected review is conditional. Use `not_applicable` or `explicit_gap_accepted` with owner, reason, residual risk and follow-up condition rather than forcing diagrams, cloud review or docs tooling.

## Quality Testing & Evals Methodology

Use `quality_testing_evals` when quality, test, eval, runtime, manual QA, visual/a11y, CI, flaky, coverage, test data privacy, bugfix, regression, release, readiness, or completion evidence applies. Stage or request `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md` when the corresponding gate applies.

Track `quality_strategy_present`, `risk_based_scope_present`, `test_first_or_gap_present`, `acceptance_traceability_present`, `contract_check_present`, `runtime_evidence_present`, `manual_qa_evidence_present`, `visual_a11y_evidence_present`, `eval_spec_present`, `eval_rerun_evidence_present`, `current_evidence_before_completion`, `ci_quality_gate_present`, `flaky_test_policy_present`, `coverage_policy_present`, `test_data_privacy_present`, `bug_reproduction_evidence_present`, and `regression_impact_present`. Coverage is a signal, not proof. Do not force TDD, do not force E2E, do not force coverage, and do not force AI evals when not applicable; use `not_applicable`, `present_unverified`, `explicit_gap_accepted`, or `approval_required` with owner, reason, residual risk and follow-up condition.

## Track 9 Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

## Track 9 Frontend Methodology

When frontend work applies, route it through `frontend` methodology before UI completion claims.

Required artifacts: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, and `frontend-performance-budget.md`.

Required gates: `frontend_user_flow_acceptance_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_api_contract_alignment_present`, `frontend_runtime_console_evidence_present`, and `frontend_interaction_test_evidence_present`.

Keep Storybook and Feature-Sliced Design conditional. Storybook is documentation and verification surface, not proof by itself. Feature-Sliced Design applies only when UI scale or coupling justifies layer, slice, segment, public API, and import rule review.

Public UI defaults to WCAG 2.2 AA unless owner records an accepted exception. UI completion requires browser/runtime evidence, console status, Playwright trace or explicit accepted gap. Keep screenshots, stories, mocks, and fixtures synthetic and privacy-safe: no secrets, credentials, production payloads, or private customer data.

Status remains `present_unverified` until current evidence exists. Use `approval_required` before external visual services, hosted browser services, production-data screenshots, or publication.

## Track 9 Backend Methodology

When backend work applies, route it through `backend` methodology before backend completion or readiness claims.

Required artifacts: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, and `backend-operational-runbook.md`.

Required gates: `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_dependency_failure_matrix_present`, `backend_observability_contract_present`, `backend_slo_or_gap_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_strategy_present`, `backend_config_secrets_boundary_present`, `backend_security_reviewed`, and `backend_rollback_plan_present`.

Keep microservices conditional. Modular monolith remains the default until independent deploy/scale/team/ownership evidence justifies a service split. Backend readiness requires runtime/failure/observability/security/rollback evidence or `explicit_gap_accepted`; use `approval_required` before production data, external writes, secrets, deploy actions or irreversible side effects.

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.

## Track 9 API & Integrations Methodology

Use `api-integrations` when OpenAPI, AsyncAPI, GraphQL, gRPC/protobuf, JSON Schema, Pact, webhook/event, generated SDK, external provider, auth/scope/token, rate-limit, sensitive field or external write signals appear. Record all signals as `present_unverified`; Swagger UI is not source of truth and rendered docs alone do not prove a contract.

Required artifacts: `api-inventory.md`, `api-contract-review.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, and `external-integration-approval.md`.

Required gates: `api_contract_source_present`, `api_consumer_map_present`, `api_breaking_change_reviewed`, `api_security_reviewed`, `api_error_contract_present`, `api_contract_test_matrix_present`, `event_delivery_contract_present`, `generated_client_manifest_present`, and `external_write_approval_present`.

Contract drift blocks completion claims. External writes are approval_required. Use `explicit_gap_accepted` only with owner, reason, review date, downstream risk and follow-up. No universal GraphQL/gRPC/event default; style/tool choices remain project-specific.

## Verification

Check that each slice maps to acceptance criteria, each gate names evidence required, rollback notes exist for risky changes, conditional readiness gates record status, owner, applicability reason, and residual risk, `plan_quality_check` has no-placeholder coverage, and every proposed artifact remains staged. For behavior changes, verify acceptance scenarios or explicit gap before implementation; the scenario chain must be `requirement -> scenario -> check -> evidence owner`, with ATDD/BDD or equivalent behavior format fields and evidence owner named. For complex backend, workflow, enterprise, data-heavy, multi-service, or multi-context work, verify `domain_model_when_complex_domain`: `.codex/artifact-templates/domain-modeling.md` or accepted gap, bounded context, ubiquitous language, invariant, and evidence owner. Also verify `bounded_context_architecture_boundary_trace`: every bounded context maps to architecture boundary in `.codex/artifact-templates/architecture-overview.md` or records an accepted gap. Verify `ubiquitous_language_traceability`: every ubiquitous language term maps through term-to-requirement evidence to a requirement or source and at least one API/event/contract, UI label, code module or owner, or an accepted gap with domain expert review. For web UI/component work where `fsd_structure` applies, verify `.codex/artifact-templates/component-card.md` names Feature-Sliced Design layer, slice, segment, public API, and import rule; for backend, native, simple CRUD, or simple MVP work, verify `not applicable` or accepted gap instead of forcing FSD. Do not claim without evidence.

## Failure Modes

- If requirements are missing, stop and route to `requirements-author`.
- If acceptance criteria cannot be mapped to slices, return open planning questions.
- If behavior changes lack `.codex/artifact-templates/acceptance-scenarios.md`, Given/When/Then or equivalent behavior format, business rule, edge case, non-goal, explicit gap, check, or evidence owner, stop before build and route to `requirements-author`.
- If `domain_model_when_complex_domain` applies and bounded context, ubiquitous language, invariant, domain-modeling artifact, or accepted gap is missing, stop before build with `missing domain model for complex domain`.
- If `bounded_context_architecture_boundary_trace` applies and every bounded context maps to architecture boundary cannot be shown in `.codex/artifact-templates/architecture-overview.md` or accepted gap, stop before build with `missing bounded context architecture boundary trace`.
- If `ubiquitous_language_traceability` applies and every ubiquitous language term cannot be traced to requirement or source plus API/event/contract, UI label, code module or owner, or accepted gap with domain expert review, stop before build with `missing ubiquitous language traceability`.
- If the work is simple CRUD or simple MVP, do not force DDD; mark the gate `not_applicable` with a reason.
- If `fsd_structure` applies and layer, slice, segment, public API, import rule, `.codex/artifact-templates/component-card.md`, or accepted gap is missing, stop before build with `missing fsd structure boundary`.
- If the work is backend, native, simple CRUD, or simple MVP, do not force FSD; mark the gate `not applicable` with a reason.
- If exact files, owned files, forbidden files, exact commands, expected outputs, rollback, evidence owner, or placeholder scan are missing for non-trivial work, stop before build and return plan repair.
- If the plan contains vague validation, repeated-by-reference steps, or commands without expected outputs, keep `next_lifecycle_state` out of `plan_ready`.
- If file ownership overlaps, route to `agent-team-designer` before implementation.
- If available commands are unknown, list discovery needed and keep verification proposed.
- If approval is needed, stop before writes or external actions.

## Final Response Contract

Return status, lifecycle state, `implementation_plan_packet`, `plan_quality_check`, files proposed, commands proposed or run, verification evidence, unsupported claims, approval requirements, risks, and the next recommended skill.
