---
name: workspace-discovery-auditor
description: Perform a read-only Product-Agent OS workspace audit and return a staged discovery packet for lifecycle planning.
---

# Workspace Discovery Auditor

## Trigger

Use this skill when a workspace is uninitialized, when project state is uncertain, or when a Product-Agent OS lifecycle run needs a read-only audit before requirements or planning.

## Boundaries

Default output is a staged packet. `workspace_apply: forbidden` keeps this skill read-only or proposal-only even when another role has workspace-write.

Guided question protocol: ask the smallest blocking question only; enforce one blocking question maximum; optional questions stay in the packet; route answers into artifacts or accepted gaps; guided questions are not workspace evidence. Do not use guided questions as a substitute for workspace evidence.

Self-verification metrics loop (`agent_skill_metrics_loop`): route agent/skill metrics as staged evidence only. Dashboard or report is not proof. Do not apply modernization candidates, do not activate schedules, do not call live eval services, and do not treat a dashboard or report as proof. Rollback evidence required before any modernization candidate can be reviewed.
Project code graph: generated graph is not source of truth; use it as orientation evidence only. Read source files before edits, impact claims, readiness claims, or completion claims. Stale or ambiguous graph blocks readiness claims. Do not treat graph HTML as proof.


Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not write files, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim detected commands pass, runtime behavior works, or control-plane readiness without evidence from the current run.
Ask for approval before external writes, permission changes, deployment, billing, auth, database, production operations, or expanded read scope.

Read shared references when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

## Provenance and explicit compliance routing

For an explicit instruction/tool-use compliance audit or Product-Agent OS auto-engagement failure, inspect skill source, installed cache and current-session exposure separately before generic bug rescue. Read the selected canonical SKILL.md; record its normalized digest and selected source path. Installed files do not prove exposure, selection or invocation. Never mix source and cache copies of a same-named skill within a run. Missing implicit invocation is expected while allow_implicit_invocation is false; preserve explicit-only policy unless the owner separately chooses a narrow implicit class.

Use the read-only build_skill_provenance result from product_agent_os.validators as local inventory evidence. Its selected path is caller-declared, not proof of host loading. Unknown or mismatched provenance remains a gap. OpenAI behavior claims need current official sources; route recommendations confer no write, cache, provider or publication authority. Self-learning requests produce candidate-only handoffs to learning-loop-maintainer. Fresh-session exposure and invocation require separate host receipts.

## Inputs

- Workspace path and allowed read scope.
- User goal, constraints, target runtime, and known project archetype when available.
- Existing `AGENTS.md`, README, package manifests, build files, tests, docs, `.codex/`, CI files, candidate failing logs, `RUNLOG.md`, Feature-Sliced Design or `fsd_structure` clues, legacy or undocumented repository signals, API contract migration signals, AI eval regression signals, native/mobile platform signals, desktop/local-first runtime signals, data migration signals, `database_data_signals`, security-sensitive signals, CI stabilization signals, release packaging signals, and prior lifecycle packets.
- Preferred discovery helper: `plugins/product-agent-os/scripts/detect_project.py`.

## Process

1. Keep the audit read-only.
2. Prefer `plugins/product-agent-os/scripts/detect_project.py` for stack and control-plane discovery when it is available.
3. Inventory project type, languages, frameworks, tests, build commands, documentation, existing Codex assets, and control-plane files.
4. Identify existing methodology signals: product metrics, architecture docs, ADR, API contracts, UI component docs, `fsd_structure` Feature-Sliced Design directories, database docs, evals, CI, and CODEOWNERS.
5. Identify `usage_mode`, `bug_reproduction_signals`, `legacy_onboarding_signals`, `api_migration_signals`, `ai_eval_signals`, `native_mobile_signals`, `desktop_local_signals`, `data_migration_signals`, `database_data_signals`, `security_sensitive_signals`, `ci_stabilization_signals`, and `release_packaging_signals` from the workspace and user intent.
6. For `fsd_structure`, record app, pages, widgets, features, entities, and shared layer directory evidence only as architecture clues. Do not claim architecture compliance from directory names alone.
7. For first-run intake, fill `first_response_contract` with mode, confidence, next smallest action, minimum artifacts, evidence gaps, and approval boundary. Classify empty workspace, failed verification, existing control-plane, and complex system starts without writing files.
8. For legacy onboarding, record entry points, run commands, docs debt, and architecture clues as `present_unverified` until command evidence or owner evidence confirms them. Do not claim runtime behavior, command success, or docs truth from inspection.
9. For API migration, record contract sources, consumers, generated clients, compatibility, deprecation, and release clues as `present_unverified` until contract checks, generated client checks, owner evidence, or consumer review confirms them. Do not claim compatibility from inspection.
10. For AI eval regression, record baseline, dataset, prompt/context, retrieval metrics, judge rubric, threshold, latency, cost, grounding, and failure examples as `present_unverified` until eval rerun evidence confirms them. Do not claim quality from inspection.
11. For native/mobile work, record platform assumptions, iOS/Android files, permissions, offline state, simulator/emulator clues, build command clues, logs, and screenshots as `present_unverified` until platform build/run evidence confirms them. Do not claim runtime behavior from inspection.
12. For desktop/local-first work, record desktop platform assumptions, filesystem permissions, local data, local DB, background jobs, indexing, privacy, build command clues, app logs, screenshots, and recovery path as `present_unverified` until desktop build/run evidence confirms them. Do not claim desktop runtime behavior from inspection.
13. For data migration and Database & Data work, record schema, backfill, PII, sensitive fields, retention, rollback, validation, dry run, backup, database dictionary, `database_data_signals`, `migration_tools`, `destructive_change_sources`, `production_access_sources`, `pipeline_sources`, `rag_ingestion_sources`, data contract, constraints/indexes, lineage, query performance and database dictionary clues as `present_unverified` until migration dry run, validation evidence, rollback evidence, backup/restore evidence, query-plan evidence, lineage evidence, data-quality evidence or owner review confirms them. Use `approval_required` before DB introspection, production access, production data access, migration execution, destructive migration, backup restore or retention mutation. Do not claim migration safety or database safety from inspection.
14. For security-sensitive work, record authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, audit logging, tests, rollback, owner review, and approval clues as `present_unverified` until security tests, owner review, approval evidence, rollback evidence, or abuse-control evidence confirms them. Do not claim security safety from inspection.
15. For CI stabilization work, record workflow, failure log, failing job, command, environment, test result, flaky history, local reproduction, rerun, and approval clues as `present_unverified` until local reproduction, deterministic/flaky classification, rerun evidence, and owner approval confirm them. Do not claim CI health from inspection.
16. For release packaging work, record package metadata, version, SemVer clues, changelog, build evidence, test evidence, docs evidence, security notes, license notes, artifacts, rollback, owner review, and publish approval as `present_unverified` until current release evidence and owner approval confirm readiness. Do not claim release readiness from inspection.
17. Build `conditional_readiness_gates` for applicable methodology/tooling gates. Use `readiness_statuses`: `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`.
18. Treat detection alone as `present_unverified`; never infer `present_verified` without required evidence, owner, applicability reason, and residual risk.
19. Treat candidate failing logs as possible evidence, not verified truth; rerun required before fix claims or lifecycle advancement.
20. Identify missing control-plane artifacts for the next lifecycle state.
21. Infer complexity profile with confidence and source notes.
22. Return a staged `workspace_audit` packet and route back to `project-lifecycle-orchestrator`.

## Outputs

Return a workspace audit packet:

```yaml
workspace_audit:
  status: "ready_for_plan | blocked | needs_user_input"
  detected_stack: []
  existing_control_plane: []
  missing_control_plane: []
  existing_codex_assets: []
  methodology_signals:
    architecture_docs: false
    adr: false
    openapi: false
    asyncapi: false
    storybook: false
    fsd_structure: false
    database_docs: false
    docs_portal: false
    codeowners: false
    ci: false
    evals: false
    metrics: false
  methodology_gaps: []
  conditional_readiness_gates:
    - gate: ""
      applies_when: ""
      applicability_reason: ""
      status: "not_applicable | applicable_missing | present_unverified | present_verified | proposal_staged | explicit_gap_accepted | approval_required"
      required_evidence: []
      owner: ""
      accepted_gap: ""
      residual_risk: ""
  usage_mode:
    primary: ""
    secondary: []
    confidence: ""
    reasons: []
    fallback: ""
    first_response_contract: []
    minimum_artifacts: []
    behavioral_eval_cases: []
  bug_reproduction_signals:
    present: false
    evidence_files: []
    verification_status: "not_found | possible_evidence"
    note: ""
  legacy_onboarding_signals:
    entry_points_status: "applicable_missing | present_unverified"
    run_commands_status: "applicable_missing | present_unverified"
    documentation_status: "applicable_missing | present_unverified"
    architecture_status: "applicable_missing | present_unverified"
    note: ""
  api_migration_signals:
    contract_sources_status: "applicable_missing | present_unverified"
    consumer_impact_status: "applicable_missing | present_unverified"
    generated_clients_status: "applicable_missing | present_unverified"
    deprecation_status: "applicable_missing | present_unverified"
    release_impact_status: "applicable_missing | present_unverified"
    verification_status: "applicable_missing | present_unverified"
    note: ""
  ai_eval_signals:
    baseline_status: "applicable_missing | present_unverified"
    dataset_status: "applicable_missing | present_unverified"
    prompt_context_status: "applicable_missing | present_unverified"
    retrieval_status: "applicable_missing | present_unverified"
    judge_rubric_status: "applicable_missing | present_unverified"
    threshold_status: "applicable_missing | present_unverified"
    latency_cost_status: "applicable_missing | present_unverified"
    failure_examples_status: "applicable_missing | present_unverified"
    verification_status: "applicable_missing | present_unverified"
    note: ""
  native_mobile_signals:
    platform_status: "applicable_missing | present_unverified"
    permission_status: "applicable_missing | present_unverified"
    offline_status: "applicable_missing | present_unverified"
    simulator_emulator_status: "applicable_missing | present_unverified"
    build_command_status: "applicable_missing | present_unverified"
    logs_status: "applicable_missing | present_unverified"
    screenshot_status: "applicable_missing | present_unverified"
    verification_status: "applicable_missing | present_unverified"
    note: ""
  desktop_local_signals:
    platform_status: "applicable_missing | present_unverified"
    filesystem_status: "applicable_missing | present_unverified"
    local_data_status: "applicable_missing | present_unverified"
    background_job_status: "applicable_missing | present_unverified"
    privacy_status: "applicable_missing | present_unverified"
    build_command_status: "applicable_missing | present_unverified"
    runtime_log_status: "applicable_missing | present_unverified"
    screenshot_status: "applicable_missing | present_unverified"
    recovery_status: "applicable_missing | present_unverified"
    verification_status: "applicable_missing | present_unverified"
    note: ""
  data_migration_signals:
    schema_status: "applicable_missing | present_unverified"
    backfill_status: "applicable_missing | present_unverified"
    sensitive_data_status: "applicable_missing | present_unverified"
    retention_status: "applicable_missing | present_unverified"
    rollback_status: "applicable_missing | present_unverified"
    validation_status: "applicable_missing | present_unverified"
    dry_run_status: "applicable_missing | present_unverified"
    database_dictionary_status: "applicable_missing | present_unverified"
    verification_status: "applicable_missing | present_unverified"
    note: ""
  database_data_signals:
    migration_tools: "applicable_missing | present_unverified"
    destructive_change_sources: "applicable_missing | present_unverified"
    production_access_sources: "applicable_missing | present_unverified"
    pipeline_sources: "applicable_missing | present_unverified"
    rag_ingestion_sources: "applicable_missing | present_unverified"
    verification_status: "applicable_missing | present_unverified"
    note: "do not claim database safety from detection"
  security_sensitive_signals:
    authn_status: "applicable_missing | present_unverified"
    authz_status: "applicable_missing | present_unverified"
    permission_status: "applicable_missing | present_unverified"
    payment_status: "applicable_missing | present_unverified"
    secret_status: "applicable_missing | present_unverified"
    sensitive_data_status: "applicable_missing | present_unverified"
    abuse_control_status: "applicable_missing | present_unverified"
    audit_logging_status: "applicable_missing | present_unverified"
    test_status: "applicable_missing | present_unverified"
    rollback_status: "applicable_missing | present_unverified"
    approval_status: "applicable_missing | present_unverified"
    verification_status: "applicable_missing | present_unverified"
    note: ""
  ci_stabilization_signals:
    workflow_status: "applicable_missing | present_unverified"
    failure_log_status: "applicable_missing | present_unverified"
    job_status: "applicable_missing | present_unverified"
    command_status: "applicable_missing | present_unverified"
    environment_status: "applicable_missing | present_unverified"
    test_result_status: "applicable_missing | present_unverified"
    flaky_status: "applicable_missing | present_unverified"
    local_reproduction_status: "applicable_missing | present_unverified"
    rerun_status: "applicable_missing | present_unverified"
    approval_status: "applicable_missing | present_unverified"
    verification_status: "applicable_missing | present_unverified"
    note: ""
  release_packaging_signals:
    package_metadata_status: "applicable_missing | present_unverified"
    version_status: "applicable_missing | present_unverified"
    changelog_status: "applicable_missing | present_unverified"
    build_status: "applicable_missing | present_unverified"
    test_status: "applicable_missing | present_unverified"
    docs_status: "applicable_missing | present_unverified"
    security_status: "applicable_missing | present_unverified"
    license_status: "applicable_missing | present_unverified"
    artifact_status: "applicable_missing | present_unverified"
    rollback_status: "applicable_missing | present_unverified"
    approval_status: "applicable_missing | present_unverified"
    verification_status: "applicable_missing | present_unverified"
    note: ""
  risks: []
  complexity_profile:
    name: ""
    confidence: ""
  next_action: ""
```

## Conditional Readiness Gates

Use conditional readiness gates to separate applicability from evidence. `readiness_statuses` are `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`. Detection alone can only produce `present_unverified`; `present_verified` requires current command evidence, owner evidence, or verified artifact evidence. Use `applicable_missing` when the gate applies but evidence is missing, `not_applicable` only with an applicability reason, and `explicit_gap_accepted` only with owner, reason, residual risk, and follow-up condition.

## Docs Tooling Selector

Use `docs_tooling_selector` with `docs-tooling-decision.md` to close `docs_as_code_impact` without forcing a docs portal. Record `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, or `approval_required`; selected tools, rejected tools, evidence owner, maintenance owner, no forced install, no CI activation without approval, hosted docs approval, DB introspection approval, docs-light, and internal-only reasons.

## Standards Trigger Policy

Use `standards_trigger_policy` during discovery to record whether repository context raises ADR trigger policy, C4, arc42, OpenAPI source of truth, Swagger UI, AsyncAPI, SemVer impact, Keep a Changelog, CODEOWNERS status, GitHub Actions, or least privilege concerns. Report `governance-proposal.md` as the staged artifact for CODEOWNERS status and GitHub Actions governance. Use `proposal_staged` for draft governance text, `approval_required` for external activation or settings changes, and `not_applicable` with reason for small slices. Record no external activation without approval and no forced external activation.

## Solution Architecture Methodology

Use Solution Architecture routing when a slice touches architecture boundary, public contract, data ownership, trust boundary, runtime topology, observability, rollback, or parallel agent ownership. Track `solution_architecture_scope_present`, `architecture_boundary_per_slice`, `boundary_responsibility_owner_present`, `adr_for_architecture_decision`, `diagram_render_check_present`, `runtime_deployment_topology_present`, `observability_architecture_present`, `migration_rollback_path_present`, and `architecture_fitness_function_present`.

Stage or request `.codex/artifact-templates/architecture-overview.md`, `.codex/artifact-templates/adr.md`, `.codex/artifact-templates/architecture-review-record.md`, `.codex/artifact-templates/architecture-fitness-functions.md`, `.codex/artifact-templates/trust-boundary-map.md`, and `.codex/artifact-templates/architecture-docs-tooling-decision.md` when the corresponding gate applies. C4/arc42 only when applicable; architecture-as-code is conditional; Well-Architected review is conditional. Use `not_applicable` or `explicit_gap_accepted` with owner, reason, residual risk and follow-up condition rather than forcing diagrams, cloud review or docs tooling.

## Quality Testing & Evals Methodology

Use `quality_testing_evals` when quality, test, eval, runtime, manual QA, visual/a11y, CI, flaky, coverage, test data privacy, bugfix, regression, release, readiness, or completion evidence applies. Stage or request `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md` when the corresponding gate applies.

Track `quality_strategy_present`, `risk_based_scope_present`, `test_first_or_gap_present`, `acceptance_traceability_present`, `contract_check_present`, `runtime_evidence_present`, `manual_qa_evidence_present`, `visual_a11y_evidence_present`, `eval_spec_present`, `eval_rerun_evidence_present`, `current_evidence_before_completion`, `ci_quality_gate_present`, `flaky_test_policy_present`, `coverage_policy_present`, `test_data_privacy_present`, `bug_reproduction_evidence_present`, and `regression_impact_present`. Coverage is a signal, not proof. Do not force TDD, do not force E2E, do not force coverage, and do not force AI evals when not applicable; use `not_applicable`, `present_unverified`, `explicit_gap_accepted`, or `approval_required` with owner, reason, residual risk and follow-up condition.

## Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

## LLM / AI / RAG Methodology

Use `llm_ai_rag` when prompts, model selection, structured outputs, AI tools, MCP/function calling, RAG retrieval, grounding, eval datasets, agent traces, safety, latency or cost signals appear. Record `llm_ai_rag_signals` as `present_unverified` until current eval evidence or owner-reviewed artifact evidence exists.

Require AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, prompt/context inventory, dataset governance, safety evidence and cost evidence when AI behavior changes. Stage or request `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, and `ai-cost-latency-budget.md` when the corresponding gate applies.

Do not force one eval runner, do not force multi-agent architecture, and do not run live model calls, vector DB calls, live API calls, external tools or eval jobs during discovery. Use `approval_required` before live model/API calls, external writes, risky tools, data exposure or irreversible side effects.

## Frontend Methodology

When frontend work applies, route it through `frontend` methodology before UI completion claims.

Required artifacts: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, and `frontend-performance-budget.md`.

Required gates: `frontend_user_flow_acceptance_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_api_contract_alignment_present`, `frontend_runtime_console_evidence_present`, and `frontend_interaction_test_evidence_present`.

Keep Storybook and Feature-Sliced Design conditional. Storybook is documentation and verification surface, not proof by itself. Feature-Sliced Design applies only when UI scale or coupling justifies layer, slice, segment, public API, and import rule review.

Public UI defaults to WCAG 2.2 AA unless owner records an accepted exception. UI completion requires browser/runtime evidence, console status, Playwright trace or explicit accepted gap. Keep screenshots, stories, mocks, and fixtures synthetic and privacy-safe: no secrets, credentials, production payloads, or private customer data.

Status remains `present_unverified` until current evidence exists. Use `approval_required` before external visual services, hosted browser services, production-data screenshots, or publication.

## Backend Methodology

When backend work applies, route it through `backend` methodology before backend completion or readiness claims.

Required artifacts: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, and `backend-operational-runbook.md`.

Required gates: `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_dependency_failure_matrix_present`, `backend_observability_contract_present`, `backend_slo_or_gap_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_strategy_present`, `backend_config_secrets_boundary_present`, `backend_security_reviewed`, and `backend_rollback_plan_present`.

Keep microservices conditional. Modular monolith remains the default until independent deploy/scale/team/ownership evidence justifies a service split. Backend readiness requires runtime/failure/observability/security/rollback evidence or `explicit_gap_accepted`; use `approval_required` before production data, external writes, secrets, deploy actions or irreversible side effects.

During workspace discovery, record backend stack, backend commands, CI, APIs, DB, queues, workers, deployment manifests and security signals as `present_unverified`. Do this without executing deployments, running commands, triggering CI, touching external writes or mutating external systems. Use `approval_required` before any deploy action, external write, secret access, production data access or irreversible side effect.

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.

## API & Integrations Methodology

Use `api-integrations` when OpenAPI, AsyncAPI, GraphQL, gRPC/protobuf, JSON Schema, Pact, webhook/event, generated SDK, external provider, auth/scope/token, rate-limit, sensitive field or external write signals appear. Record all signals as `present_unverified`; Swagger UI is not source of truth and rendered docs alone do not prove a contract.

Required artifacts: `api-inventory.md`, `api-contract-review.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, and `external-integration-approval.md`.

Required gates: `api_contract_source_present`, `api_consumer_map_present`, `api_breaking_change_reviewed`, `api_security_reviewed`, `api_error_contract_present`, `api_contract_test_matrix_present`, `event_delivery_contract_present`, `generated_client_manifest_present`, and `external_write_approval_present`.

Contract drift blocks completion claims. External writes are approval_required. Use `explicit_gap_accepted` only with owner, reason, review date, downstream risk and follow-up. No universal GraphQL/gRPC/event default; style/tool choices remain project-specific.

## Database & Data Methodology

Use `database_data` when schema, migration, backfill, persistent data model, production data, PII, retention, deletion, backup/restore, data quality, data contract, lineage, RAG ingestion, runtime pipeline, query performance, index, constraint or transaction boundary signals appear. Record `database_data_signals` as `present_unverified`; schema-only artifact is not safety proof.

Required artifacts: `database-inventory.md`, `database-dictionary.md`, `database-migration-plan.md`, `database-expand-contract-record.md`, `database-backfill-runbook.md`, `database-rollback-feasibility.md`, `database-backup-restore-evidence.md`, `database-data-classification-matrix.md`, `database-data-quality-checks.md`, `database-data-contract.md`, `database-lineage-map.md`, `database-query-performance-review.md`, `database-retention-deletion-policy.md`, `database-synthetic-fixtures-policy.md`, and `database-production-access-approval.md`.

Required gates: `database_inventory_present`, `database_dictionary_present`, `database_schema_source_present`, `database_migration_plan_present`, `database_expand_contract_reviewed`, `database_transaction_boundary_present`, `database_rollback_feasibility_present`, `database_backup_restore_evidence_present`, `database_data_classification_present`, `database_data_quality_contract_present`, `database_data_contract_present`, `database_lineage_present`, `database_performance_review_present`, `database_retention_deletion_policy_present`, `database_synthetic_fixture_policy_present`, `database_production_access_approval_present`, `database_constraints_integrity_review_present`, and `database_unsupported_claims_rejected`.

Record `migration_tools`, `destructive_change_sources`, `production_access_sources`, `pipeline_sources`, and `rag_ingestion_sources` as `present_unverified`. Production access is `approval_required`. No universal database tooling default; schema-diff tooling deferred needs owner/reason. Do not access production data, do not run migration, and do not claim database safety without evidence.

## Security, Privacy & Compliance Methodology

Use `security_privacy_compliance` when authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data, policy changes, regulated, contractual or compliance overlays appear. Record `security_sensitive_classification_present` and all detected signals as `present_unverified` until owner-reviewed evidence exists.

Stage or request `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md`, and `approval-record.md` when applicable.

Compliance output is methodology planning evidence, not legal advice. Record Codex Security scan status as not requested, requested/run, or blocked; never imply a scan ran. Docs-only security article and keyword-only mentions stay `not_applicable` unless code, data, CI, dependency, policy, external write or owner compliance claim changes apply. Use `approval_required` before payment/billing, production data, secret rotation, policy changes, external security-system mutation, external writes or publish actions. Use `explicit_gap_accepted` only with owner, reason, residual risk, review date and follow-up.

## Delivery, Release & Operations

Use `delivery_release_operations` for planning-first delivery classification when release, deploy, publish, package, version, changelog, artifact, rollout, rollback, CI/CD governance, operations, incident, post-release, DORA, GitOps, feature flag, deployment, or automation promotion signals appear.

Track `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, and `automation_manual_stability_present`. Stage or request `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `ci-cd-workflow-inventory.md`, `operations-runbook.md`, `incident-record.md`, `post-release-review.md`, and `automation-candidate.md` when applicable.

Require release scope, version impact, current evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary, and automation candidate-only behavior. For automation promotion, require manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence, rollback/disable path, candidate-only automation, and keep active schedules remain out of scope.

Do not publish, tag, deploy, upload artifacts, mutate package registries, create releases, or activate automation without explicit approval and rollback/recovery evidence.

## Verification

Check that every detected stack, control-plane, `usage_mode`, `legacy_onboarding_signals`, `api_migration_signals`, `ai_eval_signals`, `native_mobile_signals`, `desktop_local_signals`, `data_migration_signals`, `database_data_signals`, `security_sensitive_signals`, `ci_stabilization_signals`, `release_packaging_signals`, or `bug_reproduction_signals` claim cites observed files, command output, or explicit user input. Candidate failing logs are possible evidence, not verified truth; rerun required before any fix claim. `fsd_structure` app, pages, widgets, features, entities, and shared clues are directory evidence only; do not claim architecture compliance without owner/source evidence. Legacy entry points, run commands, docs debt, and architecture clues stay `present_unverified` until verified. API contract sources, generated clients, consumers, compatibility, deprecation, and release clues stay `present_unverified`; do not claim compatibility without contract check evidence or owner review. AI eval baseline, dataset, judge rubric, retrieval metrics, threshold, latency, cost, grounding, and failure examples stay `present_unverified`; do not claim quality without eval rerun evidence. Native/mobile permissions, offline state, simulator/emulator clues, build commands, logs, and screenshots stay `present_unverified`; do not claim runtime behavior without platform build/run or device evidence. Desktop/local-first filesystem permissions, local DB, local data, background jobs, privacy, app logs, screenshots, and recovery path stay `present_unverified`; do not claim desktop runtime behavior without desktop build/run, app log, screenshot, local data, or owner evidence. Data migration schema, backfill, PII, retention, rollback, validation, dry run, database data contract, constraints, indexes, lineage, query performance, production access, and database dictionary clues stay `present_unverified`; do not claim migration safety or database safety without migration dry run, validation, rollback, backup/restore, lineage, query-plan, data-quality or owner evidence. Security-sensitive authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, audit logging, tests, rollback, and approval clues stay `present_unverified`; do not claim security safety without security tests, owner review, approval, rollback, and abuse-control evidence. CI stabilization workflow, failure log, failing job, command, environment, test result, flaky history, local reproduction, rerun, and approval clues stay `present_unverified`; do not claim CI health without local reproduction, deterministic/flaky classification, rerun evidence, and owner approval evidence. Release packaging package metadata, version, SemVer, changelog, build evidence, test evidence, docs evidence, security notes, license, artifacts, rollback, owner review, and publish approval clues stay `present_unverified`; do not claim release readiness without current build, test, docs, artifact, owner review, approval, and rollback evidence.

## Failure Modes

- If the workspace path is inaccessible, stop and request a valid path.
- If read scope is unclear, ask a blocking question before broader inspection.
- If `detect_project.py` is unavailable, use read-only inventory and report that fallback.
- If secrets appear in inspected files, stop and request redaction without repeating secret values.
- If the project needs writes, return proposed next files only.

## Final Response Contract

Return status, detected stack, existing and missing control-plane assets, Codex assets, risks, complexity profile, evidence notes, approval requirements, and next lifecycle action.
## Cross-Domain Synthesis

Consume `methodology_synthesis` and `recommendation_groups` as grouped recommendations; do not dump every methodology gate. Preserve owner domains, consumer domains, semantic evidence sufficiency, source artifact ledger, alias/deferred artifact ledger and risk-aware safe next action. Do not scaffold before approval, and remember that detection is not verification.
