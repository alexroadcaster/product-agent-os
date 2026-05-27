---
name: pr-release-operator
description: Use when verified Product-Agent OS work needs a staged PR packet, release packet, rollback note, or approval note.
---

# PR Release Operator

## Trigger

Use this skill when Product-Agent OS work is review-ready and needs a PR packet, release packet, rollout note, rollback note, or explicit approval note.

## Boundaries

This is a Track 2 skill. Produce a staged `pr_release_packet` only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not publish externally, push branches, open pull requests, edit files, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim release readiness, command success, test coverage, runtime behavior, external publication, or rollback safety without evidence from the current run.
Ask for approval before any write, external publishing action, expanded scope, dependency installation, or operation outside the allowed workspace.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- `requirements_packet` with goal, scope, acceptance criteria, and constraints.
- `implementation_plan_packet` with slices, files proposed, rollback notes, and risks.
- `risk_review_packet` with verdict, findings, missing tests, approval risks, and residual risks.
- Commands run, observed results, verification evidence, unsupported claims, and test gaps.
- User impact, rollback notes, release notes, approvals needed, and residual risks.
- Release packaging input when applicable: `release-readiness.md`, release scope, package metadata, version, SemVer impact, changelog, build evidence, test evidence, docs evidence, security notes, license notes, artifacts, package registry, publish approval, tag boundary, rollback, owner review, and residual risk.
- Metric hardening input when product behavior changes: `metric-spec.md`, `metric_hardening_when_product_behavior_changes`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence.

## Process

1. Validate that risk review verdict is `ready` and lifecycle state is `review_ready`.
2. Summarize what changed and why, grounded in requirements and implementation plan packets.
3. Include verification commands with observed results, artifacts inspected, and remaining gaps.
4. Document user impact, operational impact, rollout considerations, rollback steps, and residual risks.
5. List approval requirements, external publishing constraints, and actions that remain outside the staged packet.
6. For release packaging, verify that `release-readiness.md` or an explicit gap covers release scope, package metadata, version, SemVer impact, changelog, build evidence, test evidence, docs evidence, security notes, license notes, artifacts, package registry, owner review, publish approval, tag boundary, rollback, and residual risk.
7. For product behavior changes, verify `metric_hardening_when_product_behavior_changes` before release text: require `metric-spec.md`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence. Do not claim success from a proxy metric without counter-metric, guardrail, qualitative review, and post-release review evidence.
8. Prepare staged PR or release text without publishing externally.
9. Keep proposed `RUNLOG.md` updates staged; do not write the file directly.
10. Return `release_ready` only when summary, checks, impact, rollback, residual risks, metric evidence, and approval requirements are explicit.

## Outputs

Return a PR and release packet:

```yaml
pr_release_packet:
  summary: []
  checks_run: []
  user_impact: []
  rollback: []
  residual_risks: []
  approval_required: []
  staged_pr_text: ""
  staged_release_text: ""
  release_readiness:
    release_scope: ""
    package_metadata: ""
    version: ""
    semver: ""
    changelog: ""
    publish_approval: ""
    package_registry: ""
    rollback: ""
    residual_risk: ""
  metric_hardening:
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
  files_proposed:
    - "RUNLOG.md"
  next_lifecycle_state: "release_ready"
```

## Standards Trigger Policy

Use `standards_trigger_policy` in the staged release packet when architecture, API, release, ownership, or CI governance changed. Verify ADR trigger policy, C4, arc42, OpenAPI source of truth, Swagger UI as optional tooling, AsyncAPI, SemVer impact, and Keep a Changelog before release text. When CODEOWNERS status or GitHub Actions are affected, reference `governance-proposal.md`, least privilege, workflow names, commands, permissions, triggers, owners, `proposal_staged`, `approval_required`, no external activation without approval, and no forced external activation.

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

## Quality Testing & Evals Methodology

Use `quality_testing_evals` when quality, test, eval, runtime, manual QA, visual/a11y, CI, flaky, coverage, test data privacy, bugfix, regression, release, readiness, or completion evidence applies. Stage or request `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md` when the corresponding gate applies.

Track `quality_strategy_present`, `risk_based_scope_present`, `test_first_or_gap_present`, `acceptance_traceability_present`, `contract_check_present`, `runtime_evidence_present`, `manual_qa_evidence_present`, `visual_a11y_evidence_present`, `eval_spec_present`, `eval_rerun_evidence_present`, `current_evidence_before_completion`, `ci_quality_gate_present`, `flaky_test_policy_present`, `coverage_policy_present`, `test_data_privacy_present`, `bug_reproduction_evidence_present`, and `regression_impact_present`. Coverage is a signal, not proof. Do not force TDD, do not force E2E, do not force coverage, and do not force AI evals when not applicable; use `not_applicable`, `present_unverified`, `explicit_gap_accepted`, or `approval_required` with owner, reason, residual risk and follow-up condition.

## Track 9 API & Integrations Methodology

Use `api-integrations` when OpenAPI, AsyncAPI, GraphQL, gRPC/protobuf, JSON Schema, Pact, webhook/event, generated SDK, external provider, auth/scope/token, rate-limit, sensitive field or external write signals appear. Record all signals as `present_unverified`; Swagger UI is not source of truth and rendered docs alone do not prove a contract.

Required artifacts: `api-inventory.md`, `api-contract-review.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, and `external-integration-approval.md`.

Required gates: `api_contract_source_present`, `api_consumer_map_present`, `api_breaking_change_reviewed`, `api_security_reviewed`, `api_error_contract_present`, `api_contract_test_matrix_present`, `event_delivery_contract_present`, `generated_client_manifest_present`, and `external_write_approval_present`.

Contract drift blocks completion claims. External writes are approval_required. Use `explicit_gap_accepted` only with owner, reason, review date, downstream risk and follow-up. No universal GraphQL/gRPC/event default; style/tool choices remain project-specific.

## Track 9 Delivery, Release & Operations

Use `delivery_release_operations` for planning-first delivery classification when release, deploy, publish, package, version, changelog, artifact, rollout, rollback, CI/CD governance, operations, incident, post-release, DORA, GitOps, feature flag, deployment, or automation promotion signals appear.

Track `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, and `automation_manual_stability_present`. Stage or request `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `ci-cd-workflow-inventory.md`, `operations-runbook.md`, `incident-record.md`, `post-release-review.md`, and `automation-candidate.md` when applicable.

Require release scope, version impact, current evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary, and automation candidate-only behavior. For automation promotion, require manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence, rollback/disable path, candidate-only automation, and keep active schedules remain out of scope.

Do not publish, tag, deploy, upload artifacts, mutate package registries, create releases, or activate automation without explicit approval and rollback/recovery evidence.

## Verification

Check that release text is backed by current evidence, commands include observed results, rollback is actionable, residual risks and approvals are explicit, and every proposed artifact remains staged. For release packaging, check that `release-readiness.md`, SemVer impact, changelog, package registry, publish approval, tag boundary, rollback, and residual risk are explicit. Do not claim without evidence.
For product behavior changes, check that `metric_hardening_when_product_behavior_changes` has `metric-spec.md`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence before release text. Do not claim success from a proxy metric without counter-metric, guardrail, qualitative review, and post-release review evidence.

## Failure Modes

- If risk review is missing, stop and route to `risk-reviewer`.
- If verdict is not `ready`, stop and return the blocking findings or requested changes.
- If command evidence is missing, record unsupported claims and request verification.
- If product behavior changed but metric hardening evidence is missing, record unsupported claims and stop before release readiness.
- If rollback or user impact is unknown, return open release questions.
- If approval is needed, stop before publishing, external actions, or writes.

## Final Response Contract

Return status, lifecycle state, `pr_release_packet`, files proposed, verification evidence, unsupported claims, approval requirements, residual risks, and the next recommended skill.
