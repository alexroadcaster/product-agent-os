---
name: requirements-author
description: Use when a workspace audit and project goal exist but requirements, non-goals, constraints, users, and acceptance criteria are not yet staged.
---

# Requirements Author

## Trigger

Use this skill when a workspace audit and project goal exist but requirements, non-goals, constraints, users, and acceptance criteria are not yet staged.

## Boundaries

This is a Track 2 skill. Produce a staged requirements packet only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not write `REQUIREMENTS.md` directly, edit code, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim requirements readiness, stakeholder agreement, source support, or verification results without evidence from the current run.
Ask for approval before any write, external action, expanded scope, or irreversible product decision.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- `workspace_audit` packet with observed files, commands, constraints, and risks.
- User goal, target users, product context, and explicit constraints.
- Source notes with trust level, verification status, and unsupported claims.
- Complexity profile and lifecycle state from the orchestrator.
- Behavior change input for `.codex/artifact-templates/acceptance-scenarios.md`: ATDD, BDD, `requirement -> scenario -> check -> evidence owner`, Given, When, Then, equivalent behavior format, business rule, edge case, non-goal, explicit gap, and evidence owner.
- Business/Product methodology input when product, MVP, user value, analytics, release measurement, or workflow promotion claims are present: `product_hypothesis_present`, `value_proposition_evidence_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, `metric_scope_classified`, `.codex/artifact-templates/product-brief.md`, `.codex/artifact-templates/value-proposition.md`, `.codex/artifact-templates/opportunity-tree.md`, `.codex/artifact-templates/experiment-plan.md`, and `.codex/artifact-templates/tracking-plan.md`.
- Metric hardening input for `.codex/artifact-templates/metric-spec.md` when product behavior changes: `metric_hardening_when_product_behavior_changes`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence.

## Process

1. Check lifecycle state and confirm the project is ready for requirements work.
2. If `workspace_audit` is missing or stale, route back to `workspace-discovery-auditor`.
3. Separate supported facts, assumptions, open questions, and product decisions that need user input.
4. Convert the user goal into clear in-scope outcomes, non-goals, constraints, target users, and acceptance criteria.
5. For product, MVP, value, analytics, release measurement, or workflow promotion claims, stage the Business/Product methodology gates: `product_hypothesis_present`, `value_proposition_evidence_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, and `metric_scope_classified`.
6. Add a product hypothesis, target segment, value proposition evidence, opportunity-not-solution framing, decision horizon, metric scope, success metric, guardrail metrics, privacy/data constraints, analytics tracking plan, qualitative feedback loop, and post-release measurement plan when product behavior changes.
7. For product behavior changes, stage metric hardening in `.codex/artifact-templates/metric-spec.md`: `metric_hardening_when_product_behavior_changes`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence. Do not claim success from a proxy metric without counter-metric, guardrail, qualitative review, and post-release review evidence.
8. Use `.codex/artifact-templates/tracking-plan.md` when product analytics, event instrumentation, usage data, dashboards, or telemetry claims are in scope; record event taxonomy, owner, validation evidence, and privacy classification.
9. For behavior changes, stage acceptance scenarios or an explicit gap before implementation; do not treat a plain checklist as ATDD coverage.
10. Map each scenario through `requirement -> scenario -> check -> evidence owner`.
11. Use Given, When, Then or an equivalent behavior format to capture the business rule, edge case, non-goal, explicit gap, and evidence owner without forcing BDD when another clear scenario format fits better.
12. Name source-of-truth documentation artifacts that must move with the feature, such as architecture docs, API contracts, UI component docs, database docs, user-facing docs, or release notes.
13. Keep acceptance criteria observable and testable, with evidence notes for each source-backed claim.
14. Propose `REQUIREMENTS.md`, `.codex/artifact-templates/acceptance-scenarios.md`, `.codex/artifact-templates/metric-spec.md`, and applicable Business/Product artifacts as staged content only when behavior changes.
15. Return `requirements_ready` only when required fields are present and unsupported decisions are marked.

## Outputs

Return a requirements packet:

```yaml
requirements_packet:
  goal: ""
  product_hypothesis: ""
  success_metrics: []
  metric_spec:
    artifact: ".codex/artifact-templates/metric-spec.md"
    gate: "metric_hardening_when_product_behavior_changes"
    north_star_or_primary_value_metric: ""
    input_metric: ""
    counter_metric: ""
    proxy_metric_risk: ""
    guardrail: ""
    qualitative_review: ""
    privacy_classification: ""
    retention_period: ""
    data_minimization: ""
    owner_signoff: ""
    post_release_review_evidence: ""
  business_product:
    gates:
      - "product_hypothesis_present"
      - "value_proposition_evidence_present"
      - "analytics_tracking_plan_present"
      - "qualitative_feedback_loop_present"
      - "release_measurement_evidence_present"
      - "decision_horizon_present"
      - "outcome_metric_level_separated"
      - "metric_scope_classified"
    decision_horizon: "discovery | MVP | beta | production | scale"
    tracking_plan_artifact: ".codex/artifact-templates/tracking-plan.md"
  users: []
  in_scope: []
  non_goals: []
  constraints: []
  acceptance_criteria: []
  acceptance_scenarios:
    artifact: ".codex/artifact-templates/acceptance-scenarios.md"
    method: "ATDD | BDD | equivalent behavior format | explicit gap"
    traceability: "requirement -> scenario -> check -> evidence owner"
    scenarios:
      - business_rule: ""
        given: ""
        when: ""
        then: ""
        edge_case: ""
        non_goal: ""
        evidence_owner: ""
  source_of_truth_artifacts: []
  open_questions: []
  assumptions: []
  source_notes: []
  files_proposed:
    - "REQUIREMENTS.md"
    - ".codex/artifact-templates/acceptance-scenarios.md"
    - ".codex/artifact-templates/metric-spec.md"
    - ".codex/artifact-templates/product-brief.md"
    - ".codex/artifact-templates/value-proposition.md"
    - ".codex/artifact-templates/opportunity-tree.md"
    - ".codex/artifact-templates/experiment-plan.md"
    - ".codex/artifact-templates/tracking-plan.md"
  next_lifecycle_state: "requirements_ready"
```

## Requirements Domain Methodology

When Requirements & Domain applies, stage or reference `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, and `domain-review-record.md`. Require `requirements_traceability_present`, `requirement_quality_present`, `constraints_traceability_present`, `declarative_acceptance_scenarios_present`, `business_rules_present`, `domain_expert_review_present`, `requirement_change_impact_review_present`, `accepted_gap_recorded`, and `requirements_evidence_before_implementation` before calling the requirements packet ready. Accepted gaps need owner, reason, scope, review date, downstream risk, and follow-up condition.

## Solution Architecture Methodology

Use Solution Architecture routing when a slice touches architecture boundary, public contract, data ownership, trust boundary, runtime topology, observability, rollback, or parallel agent ownership. Track `solution_architecture_scope_present`, `architecture_boundary_per_slice`, `boundary_responsibility_owner_present`, `adr_for_architecture_decision`, `diagram_render_check_present`, `runtime_deployment_topology_present`, `observability_architecture_present`, `migration_rollback_path_present`, and `architecture_fitness_function_present`.

Stage or request `.codex/artifact-templates/architecture-overview.md`, `.codex/artifact-templates/adr.md`, `.codex/artifact-templates/architecture-review-record.md`, `.codex/artifact-templates/architecture-fitness-functions.md`, `.codex/artifact-templates/trust-boundary-map.md`, and `.codex/artifact-templates/architecture-docs-tooling-decision.md` when the corresponding gate applies. C4/arc42 only when applicable; architecture-as-code is conditional; Well-Architected review is conditional. Use `not_applicable` or `explicit_gap_accepted` with owner, reason, residual risk and follow-up condition rather than forcing diagrams, cloud review or docs tooling.

## Quality Testing & Evals Methodology

Use `quality_testing_evals` when quality, test, eval, runtime, manual QA, visual/a11y, CI, flaky, coverage, test data privacy, bugfix, regression, release, readiness, or completion evidence applies. Stage or request `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md` when the corresponding gate applies.

Track `quality_strategy_present`, `risk_based_scope_present`, `test_first_or_gap_present`, `acceptance_traceability_present`, `contract_check_present`, `runtime_evidence_present`, `manual_qa_evidence_present`, `visual_a11y_evidence_present`, `eval_spec_present`, `eval_rerun_evidence_present`, `current_evidence_before_completion`, `ci_quality_gate_present`, `flaky_test_policy_present`, `coverage_policy_present`, `test_data_privacy_present`, `bug_reproduction_evidence_present`, and `regression_impact_present`. Coverage is a signal, not proof. Do not force TDD, do not force E2E, do not force coverage, and do not force AI evals when not applicable; use `not_applicable`, `present_unverified`, `explicit_gap_accepted`, or `approval_required` with owner, reason, residual risk and follow-up condition.

## Track 9 Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

## Track 9 LLM / AI / RAG Methodology

Use `llm_ai_rag` requirements when prompts, model selection, structured outputs, AI tools, MCP/function calling, RAG retrieval, grounding, eval datasets, agent traces, safety, latency or cost affect user-visible behavior.

Requirements must capture AI behavior promise, baseline eval need, eval rerun evidence, app-backed eval path, prompt/context inventory, dataset governance, safety evidence, cost evidence, approval boundary and accepted gaps. Stage or request `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, and `ai-cost-latency-budget.md` when applicable.

Do not force one eval runner, do not force multi-agent architecture, and do not run live model calls while authoring requirements. Use `approval_required` before live model/API calls, external writes, risky tools, data exposure or irreversible side effects.

## Track 9 Frontend Methodology

When frontend work applies, route it through `frontend` methodology before UI completion claims.

Required artifacts: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, and `frontend-performance-budget.md`.

Required gates: `frontend_user_flow_acceptance_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_api_contract_alignment_present`, `frontend_runtime_console_evidence_present`, and `frontend_interaction_test_evidence_present`.

Keep Storybook and Feature-Sliced Design conditional. Storybook is documentation and verification surface, not proof by itself. Feature-Sliced Design applies only when UI scale or coupling justifies layer, slice, segment, public API, and import rule review.

Public UI defaults to WCAG 2.2 AA unless owner records an accepted exception. UI completion requires browser/runtime evidence, console status, Playwright trace or explicit accepted gap. Keep screenshots, stories, mocks, and fixtures synthetic and privacy-safe: no secrets, credentials, production payloads, or private customer data.

Status remains `present_unverified` until current evidence exists. Use `approval_required` before external visual services, hosted browser services, production-data screenshots, or publication.

## Track 9 Backend Methodology

When backend work applies, route it through `backend` methodology before backend completion or readiness claims.

Backend requirements intake must capture service/user behavior, non-goals, runtime constraints, affected backend unit, dependencies, data stores, operational assumptions and explicit gaps before implementation planning.

Required artifacts: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, and `backend-operational-runbook.md`.

Required gates: `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_dependency_failure_matrix_present`, `backend_observability_contract_present`, `backend_slo_or_gap_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_strategy_present`, `backend_config_secrets_boundary_present`, `backend_security_reviewed`, and `backend_rollback_plan_present`.

Keep microservices conditional. Modular monolith remains the default until independent deploy/scale/team/ownership evidence justifies a service split. Backend readiness requires runtime/failure/observability/security/rollback evidence or `explicit_gap_accepted`; use `approval_required` before production data, external writes, secrets, deploy actions or irreversible side effects.

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.

## Track 9 Security, Privacy & Compliance Methodology

Use `security_privacy_compliance` when authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data, policy changes, regulated, contractual or compliance overlays appear. Record `security_sensitive_classification_present` and all detected signals as `present_unverified` until owner-reviewed evidence exists.

Stage or request `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md`, and `approval-record.md` when applicable.

Compliance output is methodology planning evidence, not legal advice. Record Codex Security scan status as not requested, requested/run, or blocked; never imply a scan ran. Docs-only security article and keyword-only mentions stay `not_applicable` unless code, data, CI, dependency, policy, external write or owner compliance claim changes apply. Use `approval_required` before payment/billing, production data, secret rotation, policy changes, external security-system mutation, external writes or publish actions. Use `explicit_gap_accepted` only with owner, reason, residual risk, review date and follow-up.

## Track 9 Delivery, Release & Operations

Use `delivery_release_operations` for planning-first delivery classification when release, deploy, publish, package, version, changelog, artifact, rollout, rollback, CI/CD governance, operations, incident, post-release, DORA, GitOps, feature flag, deployment, or automation promotion signals appear.

Track `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, and `automation_manual_stability_present`. Stage or request `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `ci-cd-workflow-inventory.md`, `operations-runbook.md`, `incident-record.md`, `post-release-review.md`, and `automation-candidate.md` when applicable.

Require release scope, version impact, current evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary, and automation candidate-only behavior. For automation promotion, require manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence, rollback/disable path, candidate-only automation, and keep active schedules remain out of scope.

Do not publish, tag, deploy, upload artifacts, mutate package registries, create releases, or activate automation without explicit approval and rollback/recovery evidence.

## Verification

Check that the packet uses the current workspace audit, separates facts from assumptions, includes acceptance criteria, lists open questions, and keeps every proposed artifact staged. For behavior changes, check that acceptance scenarios or an explicit gap exist, the ATDD or BDD traceability chain is `requirement -> scenario -> check -> evidence owner`, Given/When/Then or equivalent behavior format is present, and evidence owner is named. For product behavior changes, check that `product_hypothesis_present`, `value_proposition_evidence_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, and `metric_scope_classified` are satisfied, explicitly not applicable, or accepted as gaps with owner and residual risk. Check that `.codex/artifact-templates/tracking-plan.md` exists for analytics or telemetry claims. Also check that `metric_hardening_when_product_behavior_changes` is satisfied or explicitly not applicable, and that North Star, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence are named before readiness. Do not claim without evidence and do not claim success from a proxy metric alone.

## Failure Modes

- If no workspace audit exists, stop and route to `workspace-discovery-auditor`.
- If the user goal is ambiguous, ask the smallest blocking question and keep the packet partial.
- If sources conflict, mark the conflict and keep the claim out of acceptance criteria.
- If product decisions are missing, list them as open questions rather than inventing them.
- If behavior changes are requested but acceptance scenarios cannot be written, record an explicit gap and do not route to implementation as ready.
- If Business/Product methodology gates are applicable but `product_hypothesis_present`, `value_proposition_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, or `metric_scope_classified` are missing, record the gap and do not route to implementation as ready.
- If analytics, telemetry, usage data, or dashboard claims exist but `analytics_tracking_plan_present` or `.codex/artifact-templates/tracking-plan.md` is missing, record the gap and do not route to implementation as ready.
- If product discovery requires feedback but `qualitative_feedback_loop_present` is missing, record the gap before requirements readiness.
- If release measurement is claimed but `release_measurement_evidence_present` is missing, record the gap before readiness.
- If product behavior changes are requested but metric hardening is missing, record the gap and do not route to implementation as ready.
- If approval is needed, stop before writes or external actions.

## Final Response Contract

Return status, lifecycle state, `requirements_packet`, files proposed, evidence notes, unsupported claims, open questions, approval requirements, risks, and the next recommended skill.
