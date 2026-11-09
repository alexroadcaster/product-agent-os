# Product-Agent OS Complexity Routing

Use this reference when adapting lifecycle depth to the project profile.

Profiles:

- `guided-small`: keep packets concise; propose minimal control-plane files; avoid custom agent generation.
- `standard-product`: require requirements, implementation plan, tests, release notes, and runlog evidence.
- `production-team`: require ownership boundaries, handoff fields, reviewer gates, and write-scope separation.
- `ai-product`: require prompt/context policy, deterministic checks, subjective eval criteria, and source fidelity.
- `enterprise-governed`: require approval gates, forbidden paths, audit evidence, and stricter source policy.
- `autonomous-maintenance`: require manual stability evidence before an automation candidate.

Rules:

- Complexity changes depth and risk gates. It does not change lifecycle order.
- Use the smallest profile that covers project risk, team size, external impact, and verification needs.
- Escalate depth when work touches production, external systems, sensitive data, security, billing, or irreversible operations.
- Downgrade depth only when scope, risk, and verification evidence support a lighter Product-Agent OS route.


## Conditional skill details

Read only the named skill and applicable domain subsection below. These sections
retain existing gates and grant no authority. Mixed work reads every affected
domain; unknown applicability requires inspection before a readiness claim.
Do not preload this catalog.

## Skill: agent-team-designer

### Requirements Domain Methodology

Use Requirements & Domain evidence to assign ownership. `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, and `domain-review-record.md` identify owners, bounded contexts, business rules, domain expert review, accepted gaps, and handoff boundaries. Treat `requirements_traceability_present`, `requirement_quality_present`, `constraints_traceability_present`, `declarative_acceptance_scenarios_present`, `business_rules_present`, `domain_expert_review_present`, `requirement_change_impact_review_present`, `accepted_gap_recorded`, and `requirements_evidence_before_implementation` as ownership inputs before splitting work.

### Solution Architecture Methodology

Use Solution Architecture routing when a slice touches architecture boundary, public contract, data ownership, trust boundary, runtime topology, observability, rollback, or parallel agent ownership. Track `solution_architecture_scope_present`, `architecture_boundary_per_slice`, `boundary_responsibility_owner_present`, `adr_for_architecture_decision`, `diagram_render_check_present`, `runtime_deployment_topology_present`, `observability_architecture_present`, `migration_rollback_path_present`, and `architecture_fitness_function_present`.

Stage or request `.codex/artifact-templates/architecture-overview.md`, `.codex/artifact-templates/adr.md`, `.codex/artifact-templates/architecture-review-record.md`, `.codex/artifact-templates/architecture-fitness-functions.md`, `.codex/artifact-templates/trust-boundary-map.md`, and `.codex/artifact-templates/architecture-docs-tooling-decision.md` when the corresponding gate applies. C4/arc42 only when applicable; architecture-as-code is conditional; Well-Architected review is conditional. Use `not_applicable` or `explicit_gap_accepted` with owner, reason, residual risk and follow-up condition rather than forcing diagrams, cloud review or docs tooling.

### Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.


## Skill: automation-promoter

### Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

### Delivery, Release & Operations

Use `delivery_release_operations` for planning-first delivery classification when release, deploy, publish, package, version, changelog, artifact, rollout, rollback, CI/CD governance, operations, incident, post-release, DORA, GitOps, feature flag, deployment, or automation promotion signals appear.

Track `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, and `automation_manual_stability_present`. Stage or request `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `ci-cd-workflow-inventory.md`, `operations-runbook.md`, `incident-record.md`, `post-release-review.md`, and `automation-candidate.md` when applicable.

Require release scope, version impact, current evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary, and automation candidate-only behavior. For automation promotion, require manual success evidence, stable inputs/outputs, owner, deterministic command evidence, owner approval, accepted residual risks, approval requirements, value evidence, rollback/disable path, candidate-only automation, and keep active schedules remain out of scope.

Do not publish, tag, deploy, upload artifacts, mutate package registries, create releases, or activate automation without explicit approval and rollback/recovery evidence.


## Skill: docs-maintainer

### Solution Architecture Methodology

Use Solution Architecture routing when a slice touches architecture boundary, public contract, data ownership, trust boundary, runtime topology, observability, rollback, or parallel agent ownership. Track `solution_architecture_scope_present`, `architecture_boundary_per_slice`, `boundary_responsibility_owner_present`, `adr_for_architecture_decision`, `diagram_render_check_present`, `runtime_deployment_topology_present`, `observability_architecture_present`, `migration_rollback_path_present`, and `architecture_fitness_function_present`.

Stage or request `.codex/artifact-templates/architecture-overview.md`, `.codex/artifact-templates/adr.md`, `.codex/artifact-templates/architecture-review-record.md`, `.codex/artifact-templates/architecture-fitness-functions.md`, `.codex/artifact-templates/trust-boundary-map.md`, and `.codex/artifact-templates/architecture-docs-tooling-decision.md` when the corresponding gate applies. C4/arc42 only when applicable; architecture-as-code is conditional; Well-Architected review is conditional. Use `not_applicable` or `explicit_gap_accepted` with owner, reason, residual risk and follow-up condition rather than forcing diagrams, cloud review or docs tooling.

### Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

### LLM / AI / RAG Methodology

Maintain `llm_ai_rag` docs when AI behavior, prompt/model changes, structured outputs, AI tools, MCP/function calling, RAG retrieval, grounding, datasets, agent traces, safety, latency or cost are documented.

Docs must preserve AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, prompt/context inventory, dataset governance, safety evidence, cost evidence, approval boundary, accepted gaps and unsupported claims. Keep `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, and `ai-cost-latency-budget.md` aligned when applicable.

Do not force one eval runner, do not force multi-agent architecture, and do not run live model calls from docs maintenance. Use `approval_required` before live model/API calls, external writes, risky tools, data exposure or irreversible side effects.

### Frontend Methodology

When frontend work applies, route it through `frontend` methodology before UI completion claims.

Required artifacts: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, and `frontend-performance-budget.md`.

Required gates: `frontend_user_flow_acceptance_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_api_contract_alignment_present`, `frontend_runtime_console_evidence_present`, and `frontend_interaction_test_evidence_present`.

Keep Storybook and Feature-Sliced Design conditional. Storybook is documentation and verification surface, not proof by itself. Feature-Sliced Design applies only when UI scale or coupling justifies layer, slice, segment, public API, and import rule review.

Public UI defaults to WCAG 2.2 AA unless owner records an accepted exception. UI completion requires browser/runtime evidence, console status, Playwright trace or explicit accepted gap. Keep screenshots, stories, mocks, and fixtures synthetic and privacy-safe: no secrets, credentials, production payloads, or private customer data.

Status remains `present_unverified` until current evidence exists. Use `approval_required` before external visual services, hosted browser services, production-data screenshots, or publication.

### Backend Methodology

When backend work applies, route it through `backend` methodology before backend completion or readiness claims.

Required artifacts: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, and `backend-operational-runbook.md`.

Required gates: `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_dependency_failure_matrix_present`, `backend_observability_contract_present`, `backend_slo_or_gap_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_strategy_present`, `backend_config_secrets_boundary_present`, `backend_security_reviewed`, and `backend_rollback_plan_present`.

Keep microservices conditional. Modular monolith remains the default until independent deploy/scale/team/ownership evidence justifies a service split. Backend readiness requires runtime/failure/observability/security/rollback evidence or `explicit_gap_accepted`; use `approval_required` before production data, external writes, secrets, deploy actions or irreversible side effects.

### Quality Testing & Evals Methodology

Use `quality_testing_evals` when quality, test, eval, runtime, manual QA, visual/a11y, CI, flaky, coverage, test data privacy, bugfix, regression, release, readiness, or completion evidence applies. Stage or request `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md` when the corresponding gate applies.

Track `quality_strategy_present`, `risk_based_scope_present`, `test_first_or_gap_present`, `acceptance_traceability_present`, `contract_check_present`, `runtime_evidence_present`, `manual_qa_evidence_present`, `visual_a11y_evidence_present`, `eval_spec_present`, `eval_rerun_evidence_present`, `current_evidence_before_completion`, `ci_quality_gate_present`, `flaky_test_policy_present`, `coverage_policy_present`, `test_data_privacy_present`, `bug_reproduction_evidence_present`, and `regression_impact_present`. Coverage is a signal, not proof. Do not force TDD, do not force E2E, do not force coverage, and do not force AI evals when not applicable; use `not_applicable`, `present_unverified`, `explicit_gap_accepted`, or `approval_required` with owner, reason, residual risk and follow-up condition.

### API & Integrations Methodology

Use `api-integrations` when OpenAPI, AsyncAPI, GraphQL, gRPC/protobuf, JSON Schema, Pact, webhook/event, generated SDK, external provider, auth/scope/token, rate-limit, sensitive field or external write signals appear. Record all signals as `present_unverified`; Swagger UI is not source of truth and rendered docs alone do not prove a contract.

Required artifacts: `api-inventory.md`, `api-contract-review.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, and `external-integration-approval.md`.

Required gates: `api_contract_source_present`, `api_consumer_map_present`, `api_breaking_change_reviewed`, `api_security_reviewed`, `api_error_contract_present`, `api_contract_test_matrix_present`, `event_delivery_contract_present`, `generated_client_manifest_present`, and `external_write_approval_present`.

Contract drift blocks completion claims. External writes are approval_required. Use `explicit_gap_accepted` only with owner, reason, review date, downstream risk and follow-up. No universal GraphQL/gRPC/event default; style/tool choices remain project-specific.

### Security, Privacy & Compliance Methodology

Use `security_privacy_compliance` when authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data, policy changes, regulated, contractual or compliance overlays appear. Record `security_sensitive_classification_present` and all detected signals as `present_unverified` until owner-reviewed evidence exists.

Stage or request `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md`, and `approval-record.md` when applicable.

Compliance output is methodology planning evidence, not legal advice. Record Codex Security scan status as not requested, requested/run, or blocked; never imply a scan ran. Docs-only security article and keyword-only mentions stay `not_applicable` unless code, data, CI, dependency, policy, external write or owner compliance claim changes apply. Use `approval_required` before payment/billing, production data, secret rotation, policy changes, external security-system mutation, external writes or publish actions. Use `explicit_gap_accepted` only with owner, reason, residual risk, review date and follow-up.


## Skill: implementation-planner

### Conditional Readiness Gates

Use conditional readiness gates before returning `plan_ready`. `readiness_statuses` are `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`. Detection alone can only produce `present_unverified`; `present_verified` requires current command evidence, owner evidence, or verified artifact evidence. Use `applicable_missing` for applicable gates without evidence, `not_applicable` only with an applicability reason, and `explicit_gap_accepted` only with owner, reason, residual risk, and follow-up condition.

### Docs Tooling Selector

Use `docs_tooling_selector` with `docs-tooling-decision.md` to close `docs_as_code_impact` without forcing a docs portal. Record `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, or `approval_required`; selected tools, rejected tools, evidence owner, maintenance owner, no forced install, no CI activation without approval, hosted docs approval, DB introspection approval, docs-light, and internal-only reasons.

### Standards Trigger Policy

Use `standards_trigger_policy` before `plan_ready` when the slice touches architecture, API, release, ownership, or CI governance. Require ADR trigger policy for architecture boundary, API contract, storage, auth/security, irreversible migration, or automation activation. Route architecture docs through C4 and arc42 only as far as the project needs. Treat OpenAPI source of truth as the HTTP contract and Swagger UI as optional tooling; treat AsyncAPI as the event contract path. For release-bound public changes, require SemVer impact and Keep a Changelog categories. For ownership or CI governance, stage `governance-proposal.md` with CODEOWNERS status, GitHub Actions workflow names, commands, permissions, triggers, owners, least privilege, `proposal_staged`, `approval_required`, no external activation without approval, and no forced external activation.

### Requirements Domain Methodology

Before `plan_ready`, require the applicable Requirements & Domain artifacts: `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, and `domain-review-record.md`. Block implementation when `requirements_traceability_present`, `requirement_quality_present`, `constraints_traceability_present`, `declarative_acceptance_scenarios_present`, `business_rules_present`, `domain_expert_review_present`, `requirement_change_impact_review_present`, `accepted_gap_recorded`, or `requirements_evidence_before_implementation` is applicable but missing. Use bounded contexts for ownership split only when domain complexity applies; do not force DDD on simple CRUD or simple MVP.

### Solution Architecture Methodology

Use Solution Architecture routing when a slice touches architecture boundary, public contract, data ownership, trust boundary, runtime topology, observability, rollback, or parallel agent ownership. Track `solution_architecture_scope_present`, `architecture_boundary_per_slice`, `boundary_responsibility_owner_present`, `adr_for_architecture_decision`, `diagram_render_check_present`, `runtime_deployment_topology_present`, `observability_architecture_present`, `migration_rollback_path_present`, and `architecture_fitness_function_present`.

Stage or request `.codex/artifact-templates/architecture-overview.md`, `.codex/artifact-templates/adr.md`, `.codex/artifact-templates/architecture-review-record.md`, `.codex/artifact-templates/architecture-fitness-functions.md`, `.codex/artifact-templates/trust-boundary-map.md`, and `.codex/artifact-templates/architecture-docs-tooling-decision.md` when the corresponding gate applies. C4/arc42 only when applicable; architecture-as-code is conditional; Well-Architected review is conditional. Use `not_applicable` or `explicit_gap_accepted` with owner, reason, residual risk and follow-up condition rather than forcing diagrams, cloud review or docs tooling.

### Quality Testing & Evals Methodology

Use `quality_testing_evals` when quality, test, eval, runtime, manual QA, visual/a11y, CI, flaky, coverage, test data privacy, bugfix, regression, release, readiness, or completion evidence applies. Stage or request `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md` when the corresponding gate applies.

Track `quality_strategy_present`, `risk_based_scope_present`, `test_first_or_gap_present`, `acceptance_traceability_present`, `contract_check_present`, `runtime_evidence_present`, `manual_qa_evidence_present`, `visual_a11y_evidence_present`, `eval_spec_present`, `eval_rerun_evidence_present`, `current_evidence_before_completion`, `ci_quality_gate_present`, `flaky_test_policy_present`, `coverage_policy_present`, `test_data_privacy_present`, `bug_reproduction_evidence_present`, and `regression_impact_present`. Coverage is a signal, not proof. Do not force TDD, do not force E2E, do not force coverage, and do not force AI evals when not applicable; use `not_applicable`, `present_unverified`, `explicit_gap_accepted`, or `approval_required` with owner, reason, residual risk and follow-up condition.

### Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

### LLM / AI / RAG Methodology

Use `llm_ai_rag` before `plan_ready` when prompts, model selection, structured outputs, AI tools, MCP/function calling, RAG retrieval, grounding, eval datasets, agent traces, safety, latency or cost change behavior.

Plan slices must name AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, prompt/context inventory, dataset governance, safety evidence, cost evidence, approval boundary, accepted gaps and exact verification commands or explicit command gaps. Stage or request `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, and `ai-cost-latency-budget.md` when applicable.

Do not force one eval runner, do not force multi-agent architecture, and do not run live model calls from the plan. Use `approval_required` before live model/API calls, external writes, risky tools, data exposure or irreversible side effects.

### Frontend Methodology

When frontend work applies, route it through `frontend` methodology before UI completion claims.

Required artifacts: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, and `frontend-performance-budget.md`.

Required gates: `frontend_user_flow_acceptance_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_api_contract_alignment_present`, `frontend_runtime_console_evidence_present`, and `frontend_interaction_test_evidence_present`.

Keep Storybook and Feature-Sliced Design conditional. Storybook is documentation and verification surface, not proof by itself. Feature-Sliced Design applies only when UI scale or coupling justifies layer, slice, segment, public API, and import rule review.

Public UI defaults to WCAG 2.2 AA unless owner records an accepted exception. UI completion requires browser/runtime evidence, console status, Playwright trace or explicit accepted gap. Keep screenshots, stories, mocks, and fixtures synthetic and privacy-safe: no secrets, credentials, production payloads, or private customer data.

Status remains `present_unverified` until current evidence exists. Use `approval_required` before external visual services, hosted browser services, production-data screenshots, or publication.

### Backend Methodology

When backend work applies, route it through `backend` methodology before backend completion or readiness claims.

Required artifacts: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, and `backend-operational-runbook.md`.

Required gates: `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_dependency_failure_matrix_present`, `backend_observability_contract_present`, `backend_slo_or_gap_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_strategy_present`, `backend_config_secrets_boundary_present`, `backend_security_reviewed`, and `backend_rollback_plan_present`.

Keep microservices conditional. Modular monolith remains the default until independent deploy/scale/team/ownership evidence justifies a service split. Backend readiness requires runtime/failure/observability/security/rollback evidence or `explicit_gap_accepted`; use `approval_required` before production data, external writes, secrets, deploy actions or irreversible side effects.

### API & Integrations Methodology

Use `api-integrations` when OpenAPI, AsyncAPI, GraphQL, gRPC/protobuf, JSON Schema, Pact, webhook/event, generated SDK, external provider, auth/scope/token, rate-limit, sensitive field or external write signals appear. Record all signals as `present_unverified`; Swagger UI is not source of truth and rendered docs alone do not prove a contract.

Required artifacts: `api-inventory.md`, `api-contract-review.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, and `external-integration-approval.md`.

Required gates: `api_contract_source_present`, `api_consumer_map_present`, `api_breaking_change_reviewed`, `api_security_reviewed`, `api_error_contract_present`, `api_contract_test_matrix_present`, `event_delivery_contract_present`, `generated_client_manifest_present`, and `external_write_approval_present`.

Contract drift blocks completion claims. External writes are approval_required. Use `explicit_gap_accepted` only with owner, reason, review date, downstream risk and follow-up. No universal GraphQL/gRPC/event default; style/tool choices remain project-specific.

### Database & Data Methodology

When database work applies, route it through `database_data` before implementation, migration execution, production data access or readiness claims. Stage or require `database-inventory.md`, `database-dictionary.md`, `database-migration-plan.md`, `database-data-contract.md`, `database-backup-restore-evidence.md`, and `database-production-access-approval.md`.

Required gates include `database_migration_plan_present`, `database_backup_restore_evidence_present`, `database_constraints_integrity_review_present`, and `database_production_access_approval_present`. Use `database_data_signals` as `present_unverified`; schema-only artifact is not safety proof. Production access is `approval_required`. No universal database tooling default; schema-diff tooling deferred needs owner/reason. Do not access production data, do not run migration, and do not run destructive migration without explicit approval.

### Security, Privacy & Compliance Methodology

Use `security_privacy_compliance` when authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data, policy changes, regulated, contractual or compliance overlays appear. Record `security_sensitive_classification_present` and all detected signals as `present_unverified` until owner-reviewed evidence exists.

Stage or request `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md`, and `approval-record.md` when applicable.

Compliance output is methodology planning evidence, not legal advice. Record Codex Security scan status as not requested, requested/run, or blocked; never imply a scan ran. Docs-only security article and keyword-only mentions stay `not_applicable` unless code, data, CI, dependency, policy, external write or owner compliance claim changes apply. Use `approval_required` before payment/billing, production data, secret rotation, policy changes, external security-system mutation, external writes or publish actions. Use `explicit_gap_accepted` only with owner, reason, residual risk, review date and follow-up.

### Delivery, Release & Operations

Use `delivery_release_operations` for planning-first delivery classification when release, deploy, publish, package, version, changelog, artifact, rollout, rollback, CI/CD governance, operations, incident, post-release, DORA, GitOps, feature flag, deployment, or automation promotion signals appear.

Track `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, and `automation_manual_stability_present`. Stage or request `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `ci-cd-workflow-inventory.md`, `operations-runbook.md`, `incident-record.md`, `post-release-review.md`, and `automation-candidate.md` when applicable.

Require release scope, version impact, current evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary, and automation candidate-only behavior. For automation promotion, require manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence, rollback/disable path, candidate-only automation, and keep active schedules remain out of scope.

Do not publish, tag, deploy, upload artifacts, mutate package registries, create releases, or activate automation without explicit approval and rollback/recovery evidence.


## Skill: learning-loop-maintainer

### Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

### LLM / AI / RAG Methodology

Capture `llm_ai_rag` lessons when AI behavior, prompt/model changes, structured outputs, AI tools, MCP/function calling, RAG retrieval, grounding, datasets, agent traces, safety, latency or cost shaped the run outcome.

Record whether AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, prompt/context inventory, dataset governance, safety evidence, cost evidence, approval boundary and accepted gaps were satisfied, missing or disproved. Preserve references to `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, and `ai-cost-latency-budget.md` without copying raw private prompts, traces or data.

Do not force one eval runner, do not force multi-agent architecture, and do not run live model calls during learning capture. Use `approval_required` before live model/API calls, external writes, risky tools, data exposure or irreversible side effects.

### Security, Privacy & Compliance Methodology

Use `security_privacy_compliance` when authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data, policy changes, regulated, contractual or compliance overlays appear. Record `security_sensitive_classification_present` and all detected signals as `present_unverified` until owner-reviewed evidence exists.

Stage or request `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md`, and `approval-record.md` when applicable.

Compliance output is methodology planning evidence, not legal advice. Record Codex Security scan status as not requested, requested/run, or blocked; never imply a scan ran. Docs-only security article and keyword-only mentions stay `not_applicable` unless code, data, CI, dependency, policy, external write or owner compliance claim changes apply. Use `approval_required` before payment/billing, production data, secret rotation, policy changes, external security-system mutation, external writes or publish actions. Use `explicit_gap_accepted` only with owner, reason, residual risk, review date and follow-up.

### Delivery, Release & Operations

Use `delivery_release_operations` for planning-first delivery classification when release, deploy, publish, package, version, changelog, artifact, rollout, rollback, CI/CD governance, operations, incident, post-release, DORA, GitOps, feature flag, deployment, or automation promotion signals appear.

Track `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, and `automation_manual_stability_present`. Stage or request `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `ci-cd-workflow-inventory.md`, `operations-runbook.md`, `incident-record.md`, `post-release-review.md`, and `automation-candidate.md` when applicable.

Require release scope, version impact, current evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary, and automation candidate-only behavior. For automation promotion, require manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence, rollback/disable path, candidate-only automation, and keep active schedules remain out of scope.

Do not publish, tag, deploy, upload artifacts, mutate package registries, create releases, or activate automation without explicit approval and rollback/recovery evidence.


## Skill: pr-release-operator

### Standards Trigger Policy

Use `standards_trigger_policy` in the staged release packet when architecture, API, release, ownership, or CI governance changed. Verify ADR trigger policy, C4, arc42, OpenAPI source of truth, Swagger UI as optional tooling, AsyncAPI, SemVer impact, and Keep a Changelog before release text. When CODEOWNERS status or GitHub Actions are affected, reference `governance-proposal.md`, least privilege, workflow names, commands, permissions, triggers, owners, `proposal_staged`, `approval_required`, no external activation without approval, and no forced external activation.

### Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

### Frontend Methodology

When frontend work applies, route it through `frontend` methodology before UI completion claims.

Required artifacts: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, and `frontend-performance-budget.md`.

Required gates: `frontend_user_flow_acceptance_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_api_contract_alignment_present`, `frontend_runtime_console_evidence_present`, and `frontend_interaction_test_evidence_present`.

Keep Storybook and Feature-Sliced Design conditional. Storybook is documentation and verification surface, not proof by itself. Feature-Sliced Design applies only when UI scale or coupling justifies layer, slice, segment, public API, and import rule review.

Public UI defaults to WCAG 2.2 AA unless owner records an accepted exception. UI completion requires browser/runtime evidence, console status, Playwright trace or explicit accepted gap. Keep screenshots, stories, mocks, and fixtures synthetic and privacy-safe: no secrets, credentials, production payloads, or private customer data.

Status remains `present_unverified` until current evidence exists. Use `approval_required` before external visual services, hosted browser services, production-data screenshots, or publication.

### Backend Methodology

When backend work applies, route it through `backend` methodology before backend completion or readiness claims.

Required artifacts: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, and `backend-operational-runbook.md`.

Required gates: `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_dependency_failure_matrix_present`, `backend_observability_contract_present`, `backend_slo_or_gap_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_strategy_present`, `backend_config_secrets_boundary_present`, `backend_security_reviewed`, and `backend_rollback_plan_present`.

Keep microservices conditional. Modular monolith remains the default until independent deploy/scale/team/ownership evidence justifies a service split. Backend readiness requires runtime/failure/observability/security/rollback evidence or `explicit_gap_accepted`; use `approval_required` before production data, external writes, secrets, deploy actions or irreversible side effects.

### Quality Testing & Evals Methodology

Use `quality_testing_evals` when quality, test, eval, runtime, manual QA, visual/a11y, CI, flaky, coverage, test data privacy, bugfix, regression, release, readiness, or completion evidence applies. Stage or request `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md` when the corresponding gate applies.

Track `quality_strategy_present`, `risk_based_scope_present`, `test_first_or_gap_present`, `acceptance_traceability_present`, `contract_check_present`, `runtime_evidence_present`, `manual_qa_evidence_present`, `visual_a11y_evidence_present`, `eval_spec_present`, `eval_rerun_evidence_present`, `current_evidence_before_completion`, `ci_quality_gate_present`, `flaky_test_policy_present`, `coverage_policy_present`, `test_data_privacy_present`, `bug_reproduction_evidence_present`, and `regression_impact_present`. Coverage is a signal, not proof. Do not force TDD, do not force E2E, do not force coverage, and do not force AI evals when not applicable; use `not_applicable`, `present_unverified`, `explicit_gap_accepted`, or `approval_required` with owner, reason, residual risk and follow-up condition.

### API & Integrations Methodology

Use `api-integrations` when OpenAPI, AsyncAPI, GraphQL, gRPC/protobuf, JSON Schema, Pact, webhook/event, generated SDK, external provider, auth/scope/token, rate-limit, sensitive field or external write signals appear. Record all signals as `present_unverified`; Swagger UI is not source of truth and rendered docs alone do not prove a contract.

Required artifacts: `api-inventory.md`, `api-contract-review.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, and `external-integration-approval.md`.

Required gates: `api_contract_source_present`, `api_consumer_map_present`, `api_breaking_change_reviewed`, `api_security_reviewed`, `api_error_contract_present`, `api_contract_test_matrix_present`, `event_delivery_contract_present`, `generated_client_manifest_present`, and `external_write_approval_present`.

Contract drift blocks completion claims. External writes are approval_required. Use `explicit_gap_accepted` only with owner, reason, review date, downstream risk and follow-up. No universal GraphQL/gRPC/event default; style/tool choices remain project-specific.

### Delivery, Release & Operations

Use `delivery_release_operations` for planning-first delivery classification when release, deploy, publish, package, version, changelog, artifact, rollout, rollback, CI/CD governance, operations, incident, post-release, DORA, GitOps, feature flag, deployment, or automation promotion signals appear.

Track `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, and `automation_manual_stability_present`. Stage or request `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `ci-cd-workflow-inventory.md`, `operations-runbook.md`, `incident-record.md`, `post-release-review.md`, and `automation-candidate.md` when applicable.

Require release scope, version impact, current evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary, and automation candidate-only behavior. For automation promotion, require manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence, rollback/disable path, candidate-only automation, and keep active schedules remain out of scope.

Do not publish, tag, deploy, upload artifacts, mutate package registries, create releases, or activate automation without explicit approval and rollback/recovery evidence.


## Skill: project-lifecycle-orchestrator

### Conditional Readiness Gates

Use conditional readiness gates as lifecycle blockers, not decorative labels. `readiness_statuses` are `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`. Detection alone can only produce `present_unverified`; `present_verified` requires current evidence. A gate can be `not_applicable` only with an applicability reason, and `explicit_gap_accepted` only with owner, residual risk, and follow-up condition.

### Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

### Database & Data Methodology

Use `database_data` when schema, migration, backfill, persistent data model, production data, PII, retention, deletion, backup/restore, data quality, data contract, lineage, RAG ingestion, runtime pipeline, query performance, index, constraint or transaction boundary signals appear.

Required artifacts: `database-inventory.md`, `database-dictionary.md`, `database-migration-plan.md`, `database-expand-contract-record.md`, `database-backfill-runbook.md`, `database-rollback-feasibility.md`, `database-backup-restore-evidence.md`, `database-data-classification-matrix.md`, `database-data-quality-checks.md`, `database-data-contract.md`, `database-lineage-map.md`, `database-query-performance-review.md`, `database-retention-deletion-policy.md`, `database-synthetic-fixtures-policy.md`, and `database-production-access-approval.md`.

Required gates: `database_inventory_present`, `database_dictionary_present`, `database_schema_source_present`, `database_migration_plan_present`, `database_expand_contract_reviewed`, `database_transaction_boundary_present`, `database_rollback_feasibility_present`, `database_backup_restore_evidence_present`, `database_data_classification_present`, `database_data_quality_contract_present`, `database_data_contract_present`, `database_lineage_present`, `database_performance_review_present`, `database_retention_deletion_policy_present`, `database_synthetic_fixture_policy_present`, `database_production_access_approval_present`, `database_constraints_integrity_review_present`, and `database_unsupported_claims_rejected`.

Use `database_data_signals` with `migration_tools`, `destructive_change_sources`, `production_access_sources`, `pipeline_sources`, and `rag_ingestion_sources` as `present_unverified` until owner-reviewed evidence exists. Production access is `approval_required`. Do not access production data, do not run migration, and do not run destructive migration without explicit approval.

### LLM / AI / RAG Methodology

Use `llm_ai_rag` when prompts, model selection, structured outputs, AI tools, MCP/function calling, RAG retrieval, grounding, eval datasets, agent traces, safety, latency or cost signals appear. Route to requirements, planning, test/eval or review before AI behavior changes and quality claims.

Require AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, prompt/context inventory, dataset governance, safety evidence and cost evidence. Stage or request `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, and `ai-cost-latency-budget.md` when applicable.

Do not force one eval runner, do not force multi-agent architecture, and do not run live model calls during lifecycle routing. Use `approval_required` before live model/API calls, external writes, risky tools, data exposure or irreversible side effects.

### Security, Privacy & Compliance Methodology

Use `security_privacy_compliance` when authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data, policy changes, regulated, contractual or compliance overlays appear. Record `security_sensitive_classification_present` and all detected signals as `present_unverified` until owner-reviewed evidence exists.

Stage or request `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md`, and `approval-record.md` when applicable.

Compliance output is methodology planning evidence, not legal advice. Record Codex Security scan status as not requested, requested/run, or blocked; never imply a scan ran. Docs-only security article and keyword-only mentions stay `not_applicable` unless code, data, CI, dependency, policy, external write or owner compliance claim changes apply. Use `approval_required` before payment/billing, production data, secret rotation, policy changes, external security-system mutation, external writes or publish actions. Use `explicit_gap_accepted` only with owner, reason, residual risk, review date and follow-up.

### Delivery, Release & Operations

Use `delivery_release_operations` for planning-first delivery classification when release, deploy, publish, package, version, changelog, artifact, rollout, rollback, CI/CD governance, operations, incident, post-release, DORA, GitOps, feature flag, deployment, or automation promotion signals appear.

Track `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, and `automation_manual_stability_present`. Stage or request `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `ci-cd-workflow-inventory.md`, `operations-runbook.md`, `incident-record.md`, `post-release-review.md`, and `automation-candidate.md` when applicable.

Require release scope, version impact, current evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary, and automation candidate-only behavior. For automation promotion, require manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence, rollback/disable path, candidate-only automation, and keep active schedules remain out of scope.

Do not publish, tag, deploy, upload artifacts, mutate package registries, create releases, or activate automation without explicit approval and rollback/recovery evidence.


## Skill: requirements-author

### Requirements Domain Methodology

When Requirements & Domain applies, stage or reference `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, and `domain-review-record.md`. Require `requirements_traceability_present`, `requirement_quality_present`, `constraints_traceability_present`, `declarative_acceptance_scenarios_present`, `business_rules_present`, `domain_expert_review_present`, `requirement_change_impact_review_present`, `accepted_gap_recorded`, and `requirements_evidence_before_implementation` before calling the requirements packet ready. Accepted gaps need owner, reason, scope, review date, downstream risk, and follow-up condition.

### Solution Architecture Methodology

Use Solution Architecture routing when a slice touches architecture boundary, public contract, data ownership, trust boundary, runtime topology, observability, rollback, or parallel agent ownership. Track `solution_architecture_scope_present`, `architecture_boundary_per_slice`, `boundary_responsibility_owner_present`, `adr_for_architecture_decision`, `diagram_render_check_present`, `runtime_deployment_topology_present`, `observability_architecture_present`, `migration_rollback_path_present`, and `architecture_fitness_function_present`.

Stage or request `.codex/artifact-templates/architecture-overview.md`, `.codex/artifact-templates/adr.md`, `.codex/artifact-templates/architecture-review-record.md`, `.codex/artifact-templates/architecture-fitness-functions.md`, `.codex/artifact-templates/trust-boundary-map.md`, and `.codex/artifact-templates/architecture-docs-tooling-decision.md` when the corresponding gate applies. C4/arc42 only when applicable; architecture-as-code is conditional; Well-Architected review is conditional. Use `not_applicable` or `explicit_gap_accepted` with owner, reason, residual risk and follow-up condition rather than forcing diagrams, cloud review or docs tooling.

### Quality Testing & Evals Methodology

Use `quality_testing_evals` when quality, test, eval, runtime, manual QA, visual/a11y, CI, flaky, coverage, test data privacy, bugfix, regression, release, readiness, or completion evidence applies. Stage or request `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md` when the corresponding gate applies.

Track `quality_strategy_present`, `risk_based_scope_present`, `test_first_or_gap_present`, `acceptance_traceability_present`, `contract_check_present`, `runtime_evidence_present`, `manual_qa_evidence_present`, `visual_a11y_evidence_present`, `eval_spec_present`, `eval_rerun_evidence_present`, `current_evidence_before_completion`, `ci_quality_gate_present`, `flaky_test_policy_present`, `coverage_policy_present`, `test_data_privacy_present`, `bug_reproduction_evidence_present`, and `regression_impact_present`. Coverage is a signal, not proof. Do not force TDD, do not force E2E, do not force coverage, and do not force AI evals when not applicable; use `not_applicable`, `present_unverified`, `explicit_gap_accepted`, or `approval_required` with owner, reason, residual risk and follow-up condition.

### Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

### LLM / AI / RAG Methodology

Use `llm_ai_rag` requirements when prompts, model selection, structured outputs, AI tools, MCP/function calling, RAG retrieval, grounding, eval datasets, agent traces, safety, latency or cost affect user-visible behavior.

Requirements must capture AI behavior promise, baseline eval need, eval rerun evidence, app-backed eval path, prompt/context inventory, dataset governance, safety evidence, cost evidence, approval boundary and accepted gaps. Stage or request `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, and `ai-cost-latency-budget.md` when applicable.

Do not force one eval runner, do not force multi-agent architecture, and do not run live model calls while authoring requirements. Use `approval_required` before live model/API calls, external writes, risky tools, data exposure or irreversible side effects.

### Frontend Methodology

When frontend work applies, route it through `frontend` methodology before UI completion claims.

Required artifacts: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, and `frontend-performance-budget.md`.

Required gates: `frontend_user_flow_acceptance_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_api_contract_alignment_present`, `frontend_runtime_console_evidence_present`, and `frontend_interaction_test_evidence_present`.

Keep Storybook and Feature-Sliced Design conditional. Storybook is documentation and verification surface, not proof by itself. Feature-Sliced Design applies only when UI scale or coupling justifies layer, slice, segment, public API, and import rule review.

Public UI defaults to WCAG 2.2 AA unless owner records an accepted exception. UI completion requires browser/runtime evidence, console status, Playwright trace or explicit accepted gap. Keep screenshots, stories, mocks, and fixtures synthetic and privacy-safe: no secrets, credentials, production payloads, or private customer data.

Status remains `present_unverified` until current evidence exists. Use `approval_required` before external visual services, hosted browser services, production-data screenshots, or publication.

### Backend Methodology

When backend work applies, route it through `backend` methodology before backend completion or readiness claims.

Backend requirements intake must capture service/user behavior, non-goals, runtime constraints, affected backend unit, dependencies, data stores, operational assumptions and explicit gaps before implementation planning.

Required artifacts: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, and `backend-operational-runbook.md`.

Required gates: `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_dependency_failure_matrix_present`, `backend_observability_contract_present`, `backend_slo_or_gap_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_strategy_present`, `backend_config_secrets_boundary_present`, `backend_security_reviewed`, and `backend_rollback_plan_present`.

Keep microservices conditional. Modular monolith remains the default until independent deploy/scale/team/ownership evidence justifies a service split. Backend readiness requires runtime/failure/observability/security/rollback evidence or `explicit_gap_accepted`; use `approval_required` before production data, external writes, secrets, deploy actions or irreversible side effects.

### Security, Privacy & Compliance Methodology

Use `security_privacy_compliance` when authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data, policy changes, regulated, contractual or compliance overlays appear. Record `security_sensitive_classification_present` and all detected signals as `present_unverified` until owner-reviewed evidence exists.

Stage or request `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md`, and `approval-record.md` when applicable.

Compliance output is methodology planning evidence, not legal advice. Record Codex Security scan status as not requested, requested/run, or blocked; never imply a scan ran. Docs-only security article and keyword-only mentions stay `not_applicable` unless code, data, CI, dependency, policy, external write or owner compliance claim changes apply. Use `approval_required` before payment/billing, production data, secret rotation, policy changes, external security-system mutation, external writes or publish actions. Use `explicit_gap_accepted` only with owner, reason, residual risk, review date and follow-up.

### Delivery, Release & Operations

Use `delivery_release_operations` for planning-first delivery classification when release, deploy, publish, package, version, changelog, artifact, rollout, rollback, CI/CD governance, operations, incident, post-release, DORA, GitOps, feature flag, deployment, or automation promotion signals appear.

Track `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, and `automation_manual_stability_present`. Stage or request `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `ci-cd-workflow-inventory.md`, `operations-runbook.md`, `incident-record.md`, `post-release-review.md`, and `automation-candidate.md` when applicable.

Require release scope, version impact, current evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary, and automation candidate-only behavior. For automation promotion, require manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence, rollback/disable path, candidate-only automation, and keep active schedules remain out of scope.

Do not publish, tag, deploy, upload artifacts, mutate package registries, create releases, or activate automation without explicit approval and rollback/recovery evidence.


## Skill: risk-reviewer

### Conditional Readiness Gates

Review conditional readiness gates before readiness or release. `readiness_statuses` are `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`. Detection alone can only justify `present_unverified`; `present_verified` needs current command evidence, owner evidence, or verified artifact evidence. Flag `applicable_missing` gates as blockers when they are required for the requested lifecycle state. Reject `not_applicable` without an applicability reason and `explicit_gap_accepted` without owner, residual risk, and follow-up condition.

### Docs Tooling Selector

Use `docs_tooling_selector` with `docs-tooling-decision.md` to close `docs_as_code_impact` without forcing a docs portal. Record `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, or `approval_required`; selected tools, rejected tools, evidence owner, maintenance owner, no forced install, no CI activation without approval, hosted docs approval, DB introspection approval, docs-light, and internal-only reasons.

### Standards Trigger Policy

Review `standards_trigger_policy` before readiness when architecture, API, release, ownership, or CI governance changes are present. Check ADR trigger policy for architecture boundary, API contract, storage, auth/security, irreversible migration, or automation activation. Check C4 and arc42 coverage for architecture goals, constraints, quality attributes, and risks. Check OpenAPI source of truth and Swagger UI separation for HTTP APIs, AsyncAPI coverage for event contracts, SemVer impact and Keep a Changelog categories for release-bound public changes, and `governance-proposal.md` for CODEOWNERS status or GitHub Actions. For GitHub Actions, require least privilege, workflow names, commands, permissions, triggers, owners, `proposal_staged` or `approval_required`, no external activation without approval, and no forced external activation.

### Requirements Domain Methodology

Review Requirements & Domain evidence before readiness: `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, and `domain-review-record.md`. Block readiness when `requirements_traceability_present`, `requirement_quality_present`, `constraints_traceability_present`, `declarative_acceptance_scenarios_present`, `business_rules_present`, `domain_expert_review_present`, `requirement_change_impact_review_present`, `accepted_gap_recorded`, or `requirements_evidence_before_implementation` is applicable but missing. Review domain claims, unsupported claims, business rules, accepted gaps and change impact before approving implementation, PR or release readiness.

### Solution Architecture Methodology

Use Solution Architecture routing when a slice touches architecture boundary, public contract, data ownership, trust boundary, runtime topology, observability, rollback, or parallel agent ownership. Track `solution_architecture_scope_present`, `architecture_boundary_per_slice`, `boundary_responsibility_owner_present`, `adr_for_architecture_decision`, `diagram_render_check_present`, `runtime_deployment_topology_present`, `observability_architecture_present`, `migration_rollback_path_present`, and `architecture_fitness_function_present`.

Stage or request `.codex/artifact-templates/architecture-overview.md`, `.codex/artifact-templates/adr.md`, `.codex/artifact-templates/architecture-review-record.md`, `.codex/artifact-templates/architecture-fitness-functions.md`, `.codex/artifact-templates/trust-boundary-map.md`, and `.codex/artifact-templates/architecture-docs-tooling-decision.md` when the corresponding gate applies. C4/arc42 only when applicable; architecture-as-code is conditional; Well-Architected review is conditional. Use `not_applicable` or `explicit_gap_accepted` with owner, reason, residual risk and follow-up condition rather than forcing diagrams, cloud review or docs tooling.

### Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

### LLM / AI / RAG Methodology

Review `llm_ai_rag` before readiness when AI behavior, prompt/model changes, structured outputs, AI tools, MCP/function calling, RAG retrieval, grounding, datasets, agent traces, safety, latency or cost are in scope.

Block readiness without AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, prompt/context inventory, dataset governance, retrieval metrics, grounding, failed cases, safety evidence, cost evidence, approval boundary and accepted gaps. Review `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, and `ai-cost-latency-budget.md` when applicable.

Do not force one eval runner, do not force multi-agent architecture, and do not run live model calls during review. Use `approval_required` before live model/API calls, external writes, risky tools, data exposure or irreversible side effects.

### Frontend Methodology

When frontend work applies, route it through `frontend` methodology before UI completion claims.

Required artifacts: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, and `frontend-performance-budget.md`.

Required gates: `frontend_user_flow_acceptance_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_api_contract_alignment_present`, `frontend_runtime_console_evidence_present`, and `frontend_interaction_test_evidence_present`.

Keep Storybook and Feature-Sliced Design conditional. Storybook is documentation and verification surface, not proof by itself. Feature-Sliced Design applies only when UI scale or coupling justifies layer, slice, segment, public API, and import rule review.

Public UI defaults to WCAG 2.2 AA unless owner records an accepted exception. UI completion requires browser/runtime evidence, console status, Playwright trace or explicit accepted gap. Keep screenshots, stories, mocks, and fixtures synthetic and privacy-safe: no secrets, credentials, production payloads, or private customer data.

Status remains `present_unverified` until current evidence exists. Use `approval_required` before external visual services, hosted browser services, production-data screenshots, or publication.

### Backend Methodology

When backend work applies, route it through `backend` methodology before backend completion or readiness claims.

Required artifacts: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, and `backend-operational-runbook.md`.

Required gates: `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_dependency_failure_matrix_present`, `backend_observability_contract_present`, `backend_slo_or_gap_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_strategy_present`, `backend_config_secrets_boundary_present`, `backend_security_reviewed`, and `backend_rollback_plan_present`.

Keep microservices conditional. Modular monolith remains the default until independent deploy/scale/team/ownership evidence justifies a service split. Backend readiness requires runtime/failure/observability/security/rollback evidence or `explicit_gap_accepted`; use `approval_required` before production data, external writes, secrets, deploy actions or irreversible side effects.

### Quality Testing & Evals Methodology

Use `quality_testing_evals` when quality, test, eval, runtime, manual QA, visual/a11y, CI, flaky, coverage, test data privacy, bugfix, regression, release, readiness, or completion evidence applies. Stage or request `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md` when the corresponding gate applies.

Track `quality_strategy_present`, `risk_based_scope_present`, `test_first_or_gap_present`, `acceptance_traceability_present`, `contract_check_present`, `runtime_evidence_present`, `manual_qa_evidence_present`, `visual_a11y_evidence_present`, `eval_spec_present`, `eval_rerun_evidence_present`, `current_evidence_before_completion`, `ci_quality_gate_present`, `flaky_test_policy_present`, `coverage_policy_present`, `test_data_privacy_present`, `bug_reproduction_evidence_present`, and `regression_impact_present`. Coverage is a signal, not proof. Do not force TDD, do not force E2E, do not force coverage, and do not force AI evals when not applicable; use `not_applicable`, `present_unverified`, `explicit_gap_accepted`, or `approval_required` with owner, reason, residual risk and follow-up condition.

### API & Integrations Methodology

Use `api-integrations` when OpenAPI, AsyncAPI, GraphQL, gRPC/protobuf, JSON Schema, Pact, webhook/event, generated SDK, external provider, auth/scope/token, rate-limit, sensitive field or external write signals appear. Record all signals as `present_unverified`; Swagger UI is not source of truth and rendered docs alone do not prove a contract.

Required artifacts: `api-inventory.md`, `api-contract-review.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, and `external-integration-approval.md`.

Required gates: `api_contract_source_present`, `api_consumer_map_present`, `api_breaking_change_reviewed`, `api_security_reviewed`, `api_error_contract_present`, `api_contract_test_matrix_present`, `event_delivery_contract_present`, `generated_client_manifest_present`, and `external_write_approval_present`.

Contract drift blocks completion claims. External writes are approval_required. Use `explicit_gap_accepted` only with owner, reason, review date, downstream risk and follow-up. No universal GraphQL/gRPC/event default; style/tool choices remain project-specific.

### Database & Data Methodology

Review `database_data` before readiness when schema, migration, backfill, persistent data model, production data, PII, retention, deletion, backup/restore, data quality, data contract, lineage, RAG ingestion, runtime pipeline, query performance, index, constraint or transaction boundary changes are present.

Block readiness when `database_migration_plan_present`, `database_backup_restore_evidence_present`, `database_constraints_integrity_review_present`, or `database_production_access_approval_present` is applicable but missing. Production access is `approval_required`; schema-only artifact is not safety proof; runtime pipeline and RAG ingestion signals are `present_unverified`; no universal database tooling default; schema-diff tooling deferred needs owner/reason. Do not access production data or run destructive migration without explicit approval.

### Security, Privacy & Compliance Methodology

Use `security_privacy_compliance` when authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data, policy changes, regulated, contractual or compliance overlays appear. Record `security_sensitive_classification_present` and all detected signals as `present_unverified` until owner-reviewed evidence exists.

Stage or request `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md`, and `approval-record.md` when applicable.

Compliance output is methodology planning evidence, not legal advice. Record Codex Security scan status as not requested, requested/run, or blocked; never imply a scan ran. Docs-only security article and keyword-only mentions stay `not_applicable` unless code, data, CI, dependency, policy, external write or owner compliance claim changes apply. Use `approval_required` before payment/billing, production data, secret rotation, policy changes, external security-system mutation, external writes or publish actions. Use `explicit_gap_accepted` only with owner, reason, residual risk, review date and follow-up.

### Delivery, Release & Operations

Use `delivery_release_operations` for planning-first delivery classification when release, deploy, publish, package, version, changelog, artifact, rollout, rollback, CI/CD governance, operations, incident, post-release, DORA, GitOps, feature flag, deployment, or automation promotion signals appear.

Track `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, and `automation_manual_stability_present`. Stage or request `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `ci-cd-workflow-inventory.md`, `operations-runbook.md`, `incident-record.md`, `post-release-review.md`, and `automation-candidate.md` when applicable.

Require release scope, version impact, current evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary, and automation candidate-only behavior. For automation promotion, require manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence, rollback/disable path, candidate-only automation, and keep active schedules remain out of scope.

Do not publish, tag, deploy, upload artifacts, mutate package registries, create releases, or activate automation without explicit approval and rollback/recovery evidence.


## Skill: test-eval-designer

### Conditional Readiness Gates

Use conditional readiness gates to prove applicability and evidence transitions, not just artifact names. `readiness_statuses` are `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`. Detection alone can only produce `present_unverified`; tests/evals should fail if a route claims `present_verified` without command, owner, or artifact evidence. Record `not_applicable` with an applicability reason, `applicable_missing` when evidence is absent, and `explicit_gap_accepted` only with owner, residual risk, and follow-up condition.

### Docs Tooling Selector

Use `docs_tooling_selector` with `docs-tooling-decision.md` to close `docs_as_code_impact` without forcing a docs portal. Record `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, or `approval_required`; selected tools, rejected tools, evidence owner, maintenance owner, no forced install, no CI activation without approval, hosted docs approval, DB introspection approval, docs-light, and internal-only reasons.

### Requirements Domain Methodology

Map Requirements & Domain artifacts to checks and evals: `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, and `domain-review-record.md`. Test `requirements_traceability_present`, `requirement_quality_present`, `constraints_traceability_present`, `declarative_acceptance_scenarios_present`, `business_rules_present`, `domain_expert_review_present`, `requirement_change_impact_review_present`, `accepted_gap_recorded`, and `requirements_evidence_before_implementation` with deterministic checks, owner review, manual evidence, or explicit gaps. Reject scenarios with UI selectors, database internals, function names, or test harness details as business-facing acceptance evidence.

### Solution Architecture Methodology

Use Solution Architecture routing when a slice touches architecture boundary, public contract, data ownership, trust boundary, runtime topology, observability, rollback, or parallel agent ownership. Track `solution_architecture_scope_present`, `architecture_boundary_per_slice`, `boundary_responsibility_owner_present`, `adr_for_architecture_decision`, `diagram_render_check_present`, `runtime_deployment_topology_present`, `observability_architecture_present`, `migration_rollback_path_present`, and `architecture_fitness_function_present`.

Stage or request `.codex/artifact-templates/architecture-overview.md`, `.codex/artifact-templates/adr.md`, `.codex/artifact-templates/architecture-review-record.md`, `.codex/artifact-templates/architecture-fitness-functions.md`, `.codex/artifact-templates/trust-boundary-map.md`, and `.codex/artifact-templates/architecture-docs-tooling-decision.md` when the corresponding gate applies. C4/arc42 only when applicable; architecture-as-code is conditional; Well-Architected review is conditional. Use `not_applicable` or `explicit_gap_accepted` with owner, reason, residual risk and follow-up condition rather than forcing diagrams, cloud review or docs tooling.

### Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

### LLM / AI / RAG Methodology

Use `llm_ai_rag` eval routing when AI behavior, prompt/model changes, structured outputs, AI tools, MCP/function calling, RAG retrieval, grounding, datasets, agent traces, safety, latency or cost are in scope.

The test/eval packet must require AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, prompt/context inventory, dataset governance, retrieval metrics, grounding, failed cases, safety evidence, cost evidence, approval boundary and accepted gaps. Stage or request `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, and `ai-cost-latency-budget.md` when applicable.

Do not force one eval runner, do not force multi-agent architecture, and do not run live model calls while designing the packet. Use `approval_required` before live model/API calls, external writes, risky tools, data exposure or irreversible side effects.

### Frontend Methodology

When frontend work applies, route it through `frontend` methodology before UI completion claims.

Required artifacts: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, and `frontend-performance-budget.md`.

Required gates: `frontend_user_flow_acceptance_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_api_contract_alignment_present`, `frontend_runtime_console_evidence_present`, and `frontend_interaction_test_evidence_present`.

Keep Storybook and Feature-Sliced Design conditional. Storybook is documentation and verification surface, not proof by itself. Feature-Sliced Design applies only when UI scale or coupling justifies layer, slice, segment, public API, and import rule review.

Public UI defaults to WCAG 2.2 AA unless owner records an accepted exception. UI completion requires browser/runtime evidence, console status, Playwright trace or explicit accepted gap. Keep screenshots, stories, mocks, and fixtures synthetic and privacy-safe: no secrets, credentials, production payloads, or private customer data.

Status remains `present_unverified` until current evidence exists. Use `approval_required` before external visual services, hosted browser services, production-data screenshots, or publication.

### Backend Methodology

When backend work applies, route it through `backend` methodology before backend completion or readiness claims.

Required artifacts: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, and `backend-operational-runbook.md`.

Required gates: `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_dependency_failure_matrix_present`, `backend_observability_contract_present`, `backend_slo_or_gap_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_strategy_present`, `backend_config_secrets_boundary_present`, `backend_security_reviewed`, and `backend_rollback_plan_present`.

Keep microservices conditional. Modular monolith remains the default until independent deploy/scale/team/ownership evidence justifies a service split. Backend readiness requires runtime/failure/observability/security/rollback evidence or `explicit_gap_accepted`; use `approval_required` before production data, external writes, secrets, deploy actions or irreversible side effects.

### Quality Testing & Evals Methodology

Use `quality_testing_evals` when quality, test, eval, runtime, manual QA, visual/a11y, CI, flaky, coverage, test data privacy, bugfix, regression, release, readiness, or completion evidence applies. Stage or request `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md` when the corresponding gate applies.

Track `quality_strategy_present`, `risk_based_scope_present`, `test_first_or_gap_present`, `acceptance_traceability_present`, `contract_check_present`, `runtime_evidence_present`, `manual_qa_evidence_present`, `visual_a11y_evidence_present`, `eval_spec_present`, `eval_rerun_evidence_present`, `current_evidence_before_completion`, `ci_quality_gate_present`, `flaky_test_policy_present`, `coverage_policy_present`, `test_data_privacy_present`, `bug_reproduction_evidence_present`, and `regression_impact_present`. Coverage is a signal, not proof. Do not force TDD, do not force E2E, do not force coverage, and do not force AI evals when not applicable; use `not_applicable`, `present_unverified`, `explicit_gap_accepted`, or `approval_required` with owner, reason, residual risk and follow-up condition.

### API & Integrations Methodology

Use `api-integrations` when OpenAPI, AsyncAPI, GraphQL, gRPC/protobuf, JSON Schema, Pact, webhook/event, generated SDK, external provider, auth/scope/token, rate-limit, sensitive field or external write signals appear. Record all signals as `present_unverified`; Swagger UI is not source of truth and rendered docs alone do not prove a contract.

Required artifacts: `api-inventory.md`, `api-contract-review.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, and `external-integration-approval.md`.

Required gates: `api_contract_source_present`, `api_consumer_map_present`, `api_breaking_change_reviewed`, `api_security_reviewed`, `api_error_contract_present`, `api_contract_test_matrix_present`, `event_delivery_contract_present`, `generated_client_manifest_present`, and `external_write_approval_present`.

Contract drift blocks completion claims. External writes are approval_required. Use `explicit_gap_accepted` only with owner, reason, review date, downstream risk and follow-up. No universal GraphQL/gRPC/event default; style/tool choices remain project-specific.

### Database & Data Methodology

When `database_data` applies, tests/evals must cover database inventory, database dictionary, schema source, migration plan, data contract, constraints, indexes, foreign keys, unique, not null, transaction boundary, expand-contract, backfill, dry run, rollback feasibility, backup restore evidence, PII, retention, deletion, data quality, Great Expectations, dbt tests, lineage, OpenLineage, query performance, destructive migration, DROP/rename/truncate, and production access approval_required.

Keep runtime pipeline and RAG ingestion signals as `present_unverified` until current evidence exists. Reject schema-only artifact is not safety proof. Do not access production data, do not run migration, and do not claim database safety without evidence.

### Security, Privacy & Compliance Methodology

Use `security_privacy_compliance` when authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data, policy changes, regulated, contractual or compliance overlays appear. Record `security_sensitive_classification_present` and all detected signals as `present_unverified` until owner-reviewed evidence exists.

Stage or request `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md`, and `approval-record.md` when applicable.

Compliance output is methodology planning evidence, not legal advice. Record Codex Security scan status as not requested, requested/run, or blocked; never imply a scan ran. Docs-only security article and keyword-only mentions stay `not_applicable` unless code, data, CI, dependency, policy, external write or owner compliance claim changes apply. Use `approval_required` before payment/billing, production data, secret rotation, policy changes, external security-system mutation, external writes or publish actions. Use `explicit_gap_accepted` only with owner, reason, residual risk, review date and follow-up.

### Delivery, Release & Operations

Use `delivery_release_operations` for planning-first delivery classification when release, deploy, publish, package, version, changelog, artifact, rollout, rollback, CI/CD governance, operations, incident, post-release, DORA, GitOps, feature flag, deployment, or automation promotion signals appear.

Track `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, and `automation_manual_stability_present`. Stage or request `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `ci-cd-workflow-inventory.md`, `operations-runbook.md`, `incident-record.md`, `post-release-review.md`, and `automation-candidate.md` when applicable.

Require release scope, version impact, current evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary, and automation candidate-only behavior. For automation promotion, require manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence, rollback/disable path, candidate-only automation, and keep active schedules remain out of scope.

Do not publish, tag, deploy, upload artifacts, mutate package registries, create releases, or activate automation without explicit approval and rollback/recovery evidence.


## Skill: workspace-discovery-auditor

### Conditional Readiness Gates

Use conditional readiness gates to separate applicability from evidence. `readiness_statuses` are `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`. Detection alone can only produce `present_unverified`; `present_verified` requires current command evidence, owner evidence, or verified artifact evidence. Use `applicable_missing` when the gate applies but evidence is missing, `not_applicable` only with an applicability reason, and `explicit_gap_accepted` only with owner, reason, residual risk, and follow-up condition.

### Docs Tooling Selector

Use `docs_tooling_selector` with `docs-tooling-decision.md` to close `docs_as_code_impact` without forcing a docs portal. Record `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, or `approval_required`; selected tools, rejected tools, evidence owner, maintenance owner, no forced install, no CI activation without approval, hosted docs approval, DB introspection approval, docs-light, and internal-only reasons.

### Standards Trigger Policy

Use `standards_trigger_policy` during discovery to record whether repository context raises ADR trigger policy, C4, arc42, OpenAPI source of truth, Swagger UI, AsyncAPI, SemVer impact, Keep a Changelog, CODEOWNERS status, GitHub Actions, or least privilege concerns. Report `governance-proposal.md` as the staged artifact for CODEOWNERS status and GitHub Actions governance. Use `proposal_staged` for draft governance text, `approval_required` for external activation or settings changes, and `not_applicable` with reason for small slices. Record no external activation without approval and no forced external activation.

### Solution Architecture Methodology

Use Solution Architecture routing when a slice touches architecture boundary, public contract, data ownership, trust boundary, runtime topology, observability, rollback, or parallel agent ownership. Track `solution_architecture_scope_present`, `architecture_boundary_per_slice`, `boundary_responsibility_owner_present`, `adr_for_architecture_decision`, `diagram_render_check_present`, `runtime_deployment_topology_present`, `observability_architecture_present`, `migration_rollback_path_present`, and `architecture_fitness_function_present`.

Stage or request `.codex/artifact-templates/architecture-overview.md`, `.codex/artifact-templates/adr.md`, `.codex/artifact-templates/architecture-review-record.md`, `.codex/artifact-templates/architecture-fitness-functions.md`, `.codex/artifact-templates/trust-boundary-map.md`, and `.codex/artifact-templates/architecture-docs-tooling-decision.md` when the corresponding gate applies. C4/arc42 only when applicable; architecture-as-code is conditional; Well-Architected review is conditional. Use `not_applicable` or `explicit_gap_accepted` with owner, reason, residual risk and follow-up condition rather than forcing diagrams, cloud review or docs tooling.

### Quality Testing & Evals Methodology

Use `quality_testing_evals` when quality, test, eval, runtime, manual QA, visual/a11y, CI, flaky, coverage, test data privacy, bugfix, regression, release, readiness, or completion evidence applies. Stage or request `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md` when the corresponding gate applies.

Track `quality_strategy_present`, `risk_based_scope_present`, `test_first_or_gap_present`, `acceptance_traceability_present`, `contract_check_present`, `runtime_evidence_present`, `manual_qa_evidence_present`, `visual_a11y_evidence_present`, `eval_spec_present`, `eval_rerun_evidence_present`, `current_evidence_before_completion`, `ci_quality_gate_present`, `flaky_test_policy_present`, `coverage_policy_present`, `test_data_privacy_present`, `bug_reproduction_evidence_present`, and `regression_impact_present`. Coverage is a signal, not proof. Do not force TDD, do not force E2E, do not force coverage, and do not force AI evals when not applicable; use `not_applicable`, `present_unverified`, `explicit_gap_accepted`, or `approval_required` with owner, reason, residual risk and follow-up condition.

### Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

### LLM / AI / RAG Methodology

Use `llm_ai_rag` when prompts, model selection, structured outputs, AI tools, MCP/function calling, RAG retrieval, grounding, eval datasets, agent traces, safety, latency or cost signals appear. Record `llm_ai_rag_signals` as `present_unverified` until current eval evidence or owner-reviewed artifact evidence exists.

Require AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, prompt/context inventory, dataset governance, safety evidence and cost evidence when AI behavior changes. Stage or request `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, and `ai-cost-latency-budget.md` when the corresponding gate applies.

Do not force one eval runner, do not force multi-agent architecture, and do not run live model calls, vector DB calls, live API calls, external tools or eval jobs during discovery. Use `approval_required` before live model/API calls, external writes, risky tools, data exposure or irreversible side effects.

### Frontend Methodology

When frontend work applies, route it through `frontend` methodology before UI completion claims.

Required artifacts: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, and `frontend-performance-budget.md`.

Required gates: `frontend_user_flow_acceptance_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_api_contract_alignment_present`, `frontend_runtime_console_evidence_present`, and `frontend_interaction_test_evidence_present`.

Keep Storybook and Feature-Sliced Design conditional. Storybook is documentation and verification surface, not proof by itself. Feature-Sliced Design applies only when UI scale or coupling justifies layer, slice, segment, public API, and import rule review.

Public UI defaults to WCAG 2.2 AA unless owner records an accepted exception. UI completion requires browser/runtime evidence, console status, Playwright trace or explicit accepted gap. Keep screenshots, stories, mocks, and fixtures synthetic and privacy-safe: no secrets, credentials, production payloads, or private customer data.

Status remains `present_unverified` until current evidence exists. Use `approval_required` before external visual services, hosted browser services, production-data screenshots, or publication.

### Backend Methodology

When backend work applies, route it through `backend` methodology before backend completion or readiness claims.

Required artifacts: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, and `backend-operational-runbook.md`.

Required gates: `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_dependency_failure_matrix_present`, `backend_observability_contract_present`, `backend_slo_or_gap_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_strategy_present`, `backend_config_secrets_boundary_present`, `backend_security_reviewed`, and `backend_rollback_plan_present`.

Keep microservices conditional. Modular monolith remains the default until independent deploy/scale/team/ownership evidence justifies a service split. Backend readiness requires runtime/failure/observability/security/rollback evidence or `explicit_gap_accepted`; use `approval_required` before production data, external writes, secrets, deploy actions or irreversible side effects.

During workspace discovery, record backend stack, backend commands, CI, APIs, DB, queues, workers, deployment manifests and security signals as `present_unverified`. Do this without executing deployments, running commands, triggering CI, touching external writes or mutating external systems. Use `approval_required` before any deploy action, external write, secret access, production data access or irreversible side effect.

### API & Integrations Methodology

Use `api-integrations` when OpenAPI, AsyncAPI, GraphQL, gRPC/protobuf, JSON Schema, Pact, webhook/event, generated SDK, external provider, auth/scope/token, rate-limit, sensitive field or external write signals appear. Record all signals as `present_unverified`; Swagger UI is not source of truth and rendered docs alone do not prove a contract.

Required artifacts: `api-inventory.md`, `api-contract-review.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, and `external-integration-approval.md`.

Required gates: `api_contract_source_present`, `api_consumer_map_present`, `api_breaking_change_reviewed`, `api_security_reviewed`, `api_error_contract_present`, `api_contract_test_matrix_present`, `event_delivery_contract_present`, `generated_client_manifest_present`, and `external_write_approval_present`.

Contract drift blocks completion claims. External writes are approval_required. Use `explicit_gap_accepted` only with owner, reason, review date, downstream risk and follow-up. No universal GraphQL/gRPC/event default; style/tool choices remain project-specific.

### Database & Data Methodology

Use `database_data` when schema, migration, backfill, persistent data model, production data, PII, retention, deletion, backup/restore, data quality, data contract, lineage, RAG ingestion, runtime pipeline, query performance, index, constraint or transaction boundary signals appear. Record `database_data_signals` as `present_unverified`; schema-only artifact is not safety proof.

Required artifacts: `database-inventory.md`, `database-dictionary.md`, `database-migration-plan.md`, `database-expand-contract-record.md`, `database-backfill-runbook.md`, `database-rollback-feasibility.md`, `database-backup-restore-evidence.md`, `database-data-classification-matrix.md`, `database-data-quality-checks.md`, `database-data-contract.md`, `database-lineage-map.md`, `database-query-performance-review.md`, `database-retention-deletion-policy.md`, `database-synthetic-fixtures-policy.md`, and `database-production-access-approval.md`.

Required gates: `database_inventory_present`, `database_dictionary_present`, `database_schema_source_present`, `database_migration_plan_present`, `database_expand_contract_reviewed`, `database_transaction_boundary_present`, `database_rollback_feasibility_present`, `database_backup_restore_evidence_present`, `database_data_classification_present`, `database_data_quality_contract_present`, `database_data_contract_present`, `database_lineage_present`, `database_performance_review_present`, `database_retention_deletion_policy_present`, `database_synthetic_fixture_policy_present`, `database_production_access_approval_present`, `database_constraints_integrity_review_present`, and `database_unsupported_claims_rejected`.

Record `migration_tools`, `destructive_change_sources`, `production_access_sources`, `pipeline_sources`, and `rag_ingestion_sources` as `present_unverified`. Production access is `approval_required`. No universal database tooling default; schema-diff tooling deferred needs owner/reason. Do not access production data, do not run migration, and do not claim database safety without evidence.

### Security, Privacy & Compliance Methodology

Use `security_privacy_compliance` when authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data, policy changes, regulated, contractual or compliance overlays appear. Record `security_sensitive_classification_present` and all detected signals as `present_unverified` until owner-reviewed evidence exists.

Stage or request `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md`, and `approval-record.md` when applicable.

Compliance output is methodology planning evidence, not legal advice. Record Codex Security scan status as not requested, requested/run, or blocked; never imply a scan ran. Docs-only security article and keyword-only mentions stay `not_applicable` unless code, data, CI, dependency, policy, external write or owner compliance claim changes apply. Use `approval_required` before payment/billing, production data, secret rotation, policy changes, external security-system mutation, external writes or publish actions. Use `explicit_gap_accepted` only with owner, reason, residual risk, review date and follow-up.

### Delivery, Release & Operations

Use `delivery_release_operations` for planning-first delivery classification when release, deploy, publish, package, version, changelog, artifact, rollout, rollback, CI/CD governance, operations, incident, post-release, DORA, GitOps, feature flag, deployment, or automation promotion signals appear.

Track `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, and `automation_manual_stability_present`. Stage or request `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `ci-cd-workflow-inventory.md`, `operations-runbook.md`, `incident-record.md`, `post-release-review.md`, and `automation-candidate.md` when applicable.

Require release scope, version impact, current evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary, and automation candidate-only behavior. For automation promotion, require manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence, rollback/disable path, candidate-only automation, and keep active schedules remain out of scope.

Do not publish, tag, deploy, upload artifacts, mutate package registries, create releases, or activate automation without explicit approval and rollback/recovery evidence.
