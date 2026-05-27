---
name: risk-reviewer
description: Use when a Product-Agent OS plan, diff, implementation slice, or quality gate needs risk review before readiness or release.
---

# Risk Reviewer

## Trigger

Use this skill when a Product-Agent OS diff, implementation slice, plan, or quality gate needs review before release readiness or handoff.

## Boundaries

This is a Track 2 skill. Produce a staged `risk_review_packet` only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not edit files, apply fixes, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
For PR review, do not perform external writes, PR creation, push, publish actions, deployment, release tagging, or package publishing without explicit approval.
Do not claim readiness, security, test coverage, command success, runtime behavior, or risk closure without evidence from the current run.
Ask for approval before any write, external action, expanded scope, dependency installation, or operation outside the allowed workspace.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- Diff summary, proposed changes, implementation slice summary, or quality gate packet.
- Generalized two-stage review input when applicable: `review-slice.md`, `RUNLOG.md`, risk triggers, changed files, acceptance criteria, source constraints, public contract, migration, security-sensitive, data migration, release packaging, parallel work, missing evidence, and residual risk.
- PR review input when applicable: diff source, changed files map, base branch or comparison point, changed files, and reviewer questions already known.
- Security-sensitive input when applicable: `security-risk-review.md`, threat surface, authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, audit logging, tests, rollback, owner review, approval, and residual risk.
- CI stabilization input when applicable: `ci-stabilization-report.md`, failing job, command, logs, environment, deterministic/flaky classification, failure evidence, isolation plan, local reproduction, rerun evidence, remote CI, GitHub Actions, approval, and residual risk.
- Release packaging input when applicable: `release-readiness.md`, release scope, package metadata, version, SemVer impact, changelog, build evidence, test evidence, docs evidence, security notes, license notes, artifacts, package registry, publish approval, tag boundary, rollback, owner review, and residual risk.
- Metric hardening input when product behavior changes: `metric-spec.md`, `metric_hardening_when_product_behavior_changes`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence.
- Business/Product methodology input when product, MVP, user value, analytics, release measurement, or workflow promotion claims are present: `product_hypothesis_present`, `value_proposition_evidence_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, `metric_scope_classified`, `.codex/artifact-templates/tracking-plan.md`, accepted gap, owner, residual risk, and evidence status.
- `requirements_packet` with scope, acceptance criteria, constraints, and source requirements.
- `implementation_plan_packet` with slices, rollback notes, ownership, and verification gates.
- Commands run, observed results, verification evidence, unsupported claims, and known test gaps.
- Known risks, approvals, data constraints, migration concerns, source constraints, and external-system boundaries.

## Process

1. Validate that enough context exists to review behavior against requirements and the lifecycle state is `build_active` or `quality_gate`.
2. Lead with findings by severity: blocker, high, medium, low, or note.
3. Identify whether generalized two-stage review is required. It is required for PR review, public contract changes, migration, security-sensitive work, data migration, release packaging, parallel work, external-system changes, or any slice with missing evidence.
4. For required two-stage review, run `stage 1: spec compliance` before `stage 2: quality/risk`; do not collapse the stages, do not accept generic review only, and do not run quality/risk before spec compliance.
5. Stage 1 checks changed or proposed behavior against acceptance criteria, source constraints, public contract, compatibility, owner decisions, scope, ownership, rollback, and approval boundaries.
6. Stage 2 checks implementation quality, tests, evidence strength, regressions, security, privacy, docs, release impact, runtime risk, maintainability, and unsupported claims.
7. For PR review, require a changed files map and use the same two-stage review: spec compliance verdict first, then quality/risk verdict.
8. Map review impact across behavior impact, API impact, database impact, UI impact, security impact, docs impact, and release impact.
9. For security-sensitive review, require `security-risk-review.md` or an explicit gap and check threat surface, authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, audit logging, tests, rollback, owner review, approval, and residual risk before readiness.
10. For CI stabilization review, require `ci-stabilization-report.md` or an explicit gap and check failing job, command, logs, environment, deterministic/flaky classification, failure evidence, isolation plan, local reproduction, rerun evidence, remote CI, GitHub Actions, approval, and residual risk before readiness.
11. For release packaging review, require `release-readiness.md` or an explicit gap and check release scope, package metadata, version, SemVer impact, changelog, build evidence, test evidence, docs evidence, security notes, license notes, artifacts, package registry, publish approval, tag boundary, rollback, owner review, and residual risk before readiness.
12. For product behavior changes, review `metric_hardening_when_product_behavior_changes` before readiness: require `metric-spec.md`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence. Do not claim success from a proxy metric without counter-metric, guardrail, qualitative review, and post-release review evidence.
13. For Business/Product methodology, block readiness when `product_hypothesis_present`, `value_proposition_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, or `metric_scope_classified` are missing for product behavior changes without accepted gap evidence.
14. For analytics, telemetry, usage data, or dashboard claims, review `analytics_tracking_plan_present` and `.codex/artifact-templates/tracking-plan.md`; require event taxonomy, property definitions, validation evidence, owner, and privacy classification before readiness.
15. For product discovery and release claims, require `qualitative_feedback_loop_present` and `release_measurement_evidence_present` or explicit accepted gaps before readiness.
16. Review conditional readiness gates. Required `readiness_statuses` are `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`.
17. Treat detection alone as `present_unverified`; block readiness when an applicable gate lacks required evidence, owner, applicability reason, or residual risk.
18. Check architecture boundary drift, missing test-first or eval-first evidence, documentation source-of-truth gaps, and unmeasured product hypotheses.
19. Check missing tests, weak evidence, unverifiable claims, stale source assumptions, missing checks, and commands listed without observed results.
20. Check approval, sandbox, security, secrets, data handling, migration, dependency, destructive-command, external writes, PR creation, publish actions, release packaging, package registry, tagging, remote CI, GitHub Actions, and external-system risks.
21. Assign verdict `blocked`, `changes_requested`, or `ready` based on evidence and remaining risk.
22. Block a ready verdict with missing evidence. If either stage is missing or blocked, keep the overall verdict out of `ready`.
23. Keep summary secondary to findings and do not rewrite artifacts directly.
24. Return `review_ready` only when the verdict is `ready`; otherwise return the lifecycle state that needs follow-up.

## Outputs

Return a risk review packet:

```yaml
risk_review_packet:
  review_type: "standard | generalized_two_stage"
  risk_triggers: []
  stage_order:
    - "stage 1: spec compliance"
    - "stage 2: quality/risk"
  findings: []
  changed_files: []
  spec_compliance_verdict: "blocked | changes_requested | ready"
  quality_risk_verdict: "blocked | changes_requested | ready"
  behavior_impact: ""
  api_impact: ""
  database_impact: ""
  ui_impact: ""
  security_impact: ""
  docs_impact: ""
  release_impact: ""
  missing_tests: []
  missing_checks: []
  reviewer_questions: []
  approval_risks: []
  external_write_risks: []
  pr_creation_risks: []
  publish_action_risks: []
  source_risks: []
  security_risks: []
  security_sensitive_review:
    threat_surface: ""
    authn: ""
    authz: ""
    payment: ""
    secrets: ""
    pii: ""
    approval: ""
    rollback: ""
  ci_stabilization_review:
    failing_job: ""
    command: ""
    logs: ""
    environment: ""
    classification: "deterministic | flaky | unknown"
    local_reproduction: ""
    rerun_evidence: ""
    remote_ci: ""
    approval: ""
    residual_risk: ""
  release_packaging_review:
    release_scope: ""
    package_metadata: ""
    version: ""
    semver: ""
    changelog: ""
    publish_approval: ""
    package_registry: ""
    rollback: ""
    residual_risk: ""
  metric_hardening_review:
    artifact: "metric-spec.md"
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
  business_product_review:
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
    accepted_gaps: []
    blockers: []
  conditional_readiness_review:
    readiness_statuses: "not_applicable | applicable_missing | present_unverified | present_verified | proposal_staged | explicit_gap_accepted | approval_required"
    gates_reviewed: []
    detection_alone_claims: []
    applicable_missing: []
    not_applicable_without_reason: []
    explicit_gap_accepted_without_owner_or_residual_risk: []
    approval_required: []
  architecture_risks: []
  documentation_gaps: []
  measurement_gaps: []
  unsupported_claims: []
  verdict: "blocked | changes_requested | ready"
  next_action: ""
  next_lifecycle_state: "review_ready"
```

## Conditional Readiness Gates

Review conditional readiness gates before readiness or release. `readiness_statuses` are `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`. Detection alone can only justify `present_unverified`; `present_verified` needs current command evidence, owner evidence, or verified artifact evidence. Flag `applicable_missing` gates as blockers when they are required for the requested lifecycle state. Reject `not_applicable` without an applicability reason and `explicit_gap_accepted` without owner, residual risk, and follow-up condition.

## Docs Tooling Selector

Use `docs_tooling_selector` with `docs-tooling-decision.md` to close `docs_as_code_impact` without forcing a docs portal. Record `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, or `approval_required`; selected tools, rejected tools, evidence owner, maintenance owner, no forced install, no CI activation without approval, hosted docs approval, DB introspection approval, docs-light, and internal-only reasons.

## Standards Trigger Policy

Review `standards_trigger_policy` before readiness when architecture, API, release, ownership, or CI governance changes are present. Check ADR trigger policy for architecture boundary, API contract, storage, auth/security, irreversible migration, or automation activation. Check C4 and arc42 coverage for architecture goals, constraints, quality attributes, and risks. Check OpenAPI source of truth and Swagger UI separation for HTTP APIs, AsyncAPI coverage for event contracts, SemVer impact and Keep a Changelog categories for release-bound public changes, and `governance-proposal.md` for CODEOWNERS status or GitHub Actions. For GitHub Actions, require least privilege, workflow names, commands, permissions, triggers, owners, `proposal_staged` or `approval_required`, no external activation without approval, and no forced external activation.

## Requirements Domain Methodology

Review Requirements & Domain evidence before readiness: `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, and `domain-review-record.md`. Block readiness when `requirements_traceability_present`, `requirement_quality_present`, `constraints_traceability_present`, `declarative_acceptance_scenarios_present`, `business_rules_present`, `domain_expert_review_present`, `requirement_change_impact_review_present`, `accepted_gap_recorded`, or `requirements_evidence_before_implementation` is applicable but missing. Review domain claims, unsupported claims, business rules, accepted gaps and change impact before approving implementation, PR or release readiness.

## Solution Architecture Methodology

Use Solution Architecture routing when a slice touches architecture boundary, public contract, data ownership, trust boundary, runtime topology, observability, rollback, or parallel agent ownership. Track `solution_architecture_scope_present`, `architecture_boundary_per_slice`, `boundary_responsibility_owner_present`, `adr_for_architecture_decision`, `diagram_render_check_present`, `runtime_deployment_topology_present`, `observability_architecture_present`, `migration_rollback_path_present`, and `architecture_fitness_function_present`.

Stage or request `.codex/artifact-templates/architecture-overview.md`, `.codex/artifact-templates/adr.md`, `.codex/artifact-templates/architecture-review-record.md`, `.codex/artifact-templates/architecture-fitness-functions.md`, `.codex/artifact-templates/trust-boundary-map.md`, and `.codex/artifact-templates/architecture-docs-tooling-decision.md` when the corresponding gate applies. C4/arc42 only when applicable; architecture-as-code is conditional; Well-Architected review is conditional. Use `not_applicable` or `explicit_gap_accepted` with owner, reason, residual risk and follow-up condition rather than forcing diagrams, cloud review or docs tooling.

## Track 9 Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

## Track 9 LLM / AI / RAG Methodology

Review `llm_ai_rag` before readiness when AI behavior, prompt/model changes, structured outputs, AI tools, MCP/function calling, RAG retrieval, grounding, datasets, agent traces, safety, latency or cost are in scope.

Block readiness without AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, prompt/context inventory, dataset governance, retrieval metrics, grounding, failed cases, safety evidence, cost evidence, approval boundary and accepted gaps. Review `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, and `ai-cost-latency-budget.md` when applicable.

Do not force one eval runner, do not force multi-agent architecture, and do not run live model calls during review. Use `approval_required` before live model/API calls, external writes, risky tools, data exposure or irreversible side effects.

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

## Quality Testing & Evals Methodology

Use `quality_testing_evals` when quality, test, eval, runtime, manual QA, visual/a11y, CI, flaky, coverage, test data privacy, bugfix, regression, release, readiness, or completion evidence applies. Stage or request `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md` when the corresponding gate applies.

Track `quality_strategy_present`, `risk_based_scope_present`, `test_first_or_gap_present`, `acceptance_traceability_present`, `contract_check_present`, `runtime_evidence_present`, `manual_qa_evidence_present`, `visual_a11y_evidence_present`, `eval_spec_present`, `eval_rerun_evidence_present`, `current_evidence_before_completion`, `ci_quality_gate_present`, `flaky_test_policy_present`, `coverage_policy_present`, `test_data_privacy_present`, `bug_reproduction_evidence_present`, and `regression_impact_present`. Coverage is a signal, not proof. Do not force TDD, do not force E2E, do not force coverage, and do not force AI evals when not applicable; use `not_applicable`, `present_unverified`, `explicit_gap_accepted`, or `approval_required` with owner, reason, residual risk and follow-up condition.

## Track 9 API & Integrations Methodology

Use `api-integrations` when OpenAPI, AsyncAPI, GraphQL, gRPC/protobuf, JSON Schema, Pact, webhook/event, generated SDK, external provider, auth/scope/token, rate-limit, sensitive field or external write signals appear. Record all signals as `present_unverified`; Swagger UI is not source of truth and rendered docs alone do not prove a contract.

Required artifacts: `api-inventory.md`, `api-contract-review.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, and `external-integration-approval.md`.

Required gates: `api_contract_source_present`, `api_consumer_map_present`, `api_breaking_change_reviewed`, `api_security_reviewed`, `api_error_contract_present`, `api_contract_test_matrix_present`, `event_delivery_contract_present`, `generated_client_manifest_present`, and `external_write_approval_present`.

Contract drift blocks completion claims. External writes are approval_required. Use `explicit_gap_accepted` only with owner, reason, review date, downstream risk and follow-up. No universal GraphQL/gRPC/event default; style/tool choices remain project-specific.

## Track 9 Database & Data Methodology

Review `database_data` before readiness when schema, migration, backfill, persistent data model, production data, PII, retention, deletion, backup/restore, data quality, data contract, lineage, RAG ingestion, runtime pipeline, query performance, index, constraint or transaction boundary changes are present.

Block readiness when `database_migration_plan_present`, `database_backup_restore_evidence_present`, `database_constraints_integrity_review_present`, or `database_production_access_approval_present` is applicable but missing. Production access is `approval_required`; schema-only artifact is not safety proof; runtime pipeline and RAG ingestion signals are `present_unverified`; no universal database tooling default; schema-diff tooling deferred needs owner/reason. Do not access production data or run destructive migration without explicit approval.

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

Check that every finding has severity, evidence, affected scope, and required action. Check that missing tests and approval risks are explicit, source constraints are respected, and `review_ready` appears only with a `ready` verdict. Do not claim without evidence.
For generalized two-stage review, check that `stage 1: spec compliance` appears before `stage 2: quality/risk`, both `spec compliance verdict` and `quality/risk verdict` are explicit, acceptance criteria and source constraints are checked before public contract, migration, security-sensitive, data migration, release packaging, or parallel work quality review, and `RUNLOG.md` records missing evidence. Do not collapse the review into generic review only. Do not allow quality/risk before spec compliance. Do not allow a ready verdict with missing evidence.
For PR review, check that changed files, spec compliance verdict, quality/risk verdict, impact map, missing checks, reviewer questions, external writes, PR creation, publish actions, and release impact are explicit.
For release packaging, check that `release-readiness.md`, SemVer impact, changelog, package registry, publish approval, tag boundary, rollback, and residual risk are explicit before readiness.
For metric hardening, check that `metric_hardening_when_product_behavior_changes` has `metric-spec.md`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence before readiness. Do not claim success from a proxy metric without counter-metric, guardrail, qualitative review, and post-release review evidence.
For Business/Product methodology, check that `product_hypothesis_present`, `value_proposition_evidence_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, and `metric_scope_classified` are present, explicitly not applicable, or accepted gaps with owner and residual risk. Check `.codex/artifact-templates/tracking-plan.md` when analytics, telemetry, usage data, or dashboard claims exist.
For conditional readiness gates, check that every applicable gate names status, required evidence, owner, applicability reason, and residual risk before readiness.

## Failure Modes

- If no diff, slice, or plan summary exists, stop and request the missing review input.
- If PR review lacks a changed files map or diff source, stop and request review input instead of guessing impact.
- If risky work lacks a generalized two-stage review, return `blocked` and request `review-slice.md` or equivalent review input.
- If the review uses generic review only, skips source constraints, or runs quality/risk before spec compliance, return `blocked`.
- If either stage has missing evidence, do not return a ready verdict with missing evidence.
- If requirements are absent, stop and route to `requirements-author`.
- If verification evidence is absent, return `changes_requested` or `blocked` with missing evidence.
- If product behavior changes lack metric hardening, return `blocked` with the missing metric-spec, counter-metric, qualitative review, privacy classification, retention period, data minimization, owner signoff, or post-release review evidence.
- If product behavior changes lack Business/Product methodology evidence, return `blocked` with missing `product_hypothesis_present`, `value_proposition_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, `metric_scope_classified`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, or `.codex/artifact-templates/tracking-plan.md`.
- If secrets, approval gaps, migration risk, or external-system risk is unresolved, return `blocked`.
- If source claims lack authoritative support, record source risks and request verification.

## Final Response Contract

Return status, lifecycle state, `risk_review_packet`, findings by severity, missing tests, approval requirements, verification evidence, unsupported claims, verdict, risks, and the next recommended skill.
