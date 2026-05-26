---
name: project-lifecycle-orchestrator
description: Route Product-Agent OS lifecycle work to the next staged skill from current state, blockers, complexity, and evidence.
---

# Project Lifecycle Orchestrator

## Trigger

Use this skill when a Product-Agent OS project needs lifecycle routing, state recovery, next-role selection, blocker triage, or maintenance routing.

## Boundaries

This is a Track 2 skill. Produce a staged lifecycle route packet only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim readiness, passing checks, or lifecycle advancement without evidence from the current run.
Ask for approval before external writes, permission changes, deployment, billing, auth, database, production operations, or any action outside the current write scope.

Read shared references when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

## Inputs

- User goal, workspace path, and requested lifecycle action.
- Existing `AGENTS.md`, control-plane files, `.codex/` inventory, and previous packets when available.
- Discovery output from `workspace-discovery-auditor` or `plugins/product-agent-os/scripts/detect_project.py` when available.
- `usage_mode`, `bug_reproduction_signals`, `api_migration_signals`, `ai_eval_signals`, `native_mobile_signals`, `desktop_local_signals`, `data_migration_signals`, `database_data_signals`, `security_sensitive_signals`, `ci_stabilization_signals`, `release_packaging_signals`, methodology gaps, and behavioral eval cases when discovery provides them.
- Current commands run, verification evidence, unsupported claims, risks, approval constraints, and complexity profile.
- Scenario handoff packets from bug rescue, greenfield idea, complex acceleration, or other scenario workflows when available.
- First-run `first_response_contract` when the plugin is started in an empty workspace, failed verification workspace, existing control-plane workspace, or complex system workspace.

## Process

1. Identify the current lifecycle state from available packets, files, and evidence.
2. Check lifecycle order and stop if a required gate would be skipped.
3. Detect blocking missing inputs and ask only questions required for routing.
4. Check whether product metrics, architecture boundary, test/eval route, documentation impact, and measurement evidence are missing for the current state.
5. Apply `usage_mode` overlay before the default route map.
6. Select exactly one next skill from the route map.
7. Apply complexity depth from `guided-small`, `standard-product`, `production-team`, `ai-product`, `enterprise-governed`, or `autonomous-maintenance` without changing lifecycle order.
8. Require a scenario handoff before role transition when a scenario workflow has produced or stopped work. The handoff includes sources/context used, assumptions, files touched, files proposed, verification evidence, open risks, recommended next role, and stop reason.
9. For first-run use, stage `.codex/workflows/first-run-intake.md` as a proposed file and return a compact first response contract: mode, confidence, next smallest action, minimum artifacts, evidence gaps, and approval boundary.
10. Normalize conditional readiness gates before lifecycle advancement. Use `readiness_statuses`: `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`.
11. Detection alone can only support `present_unverified`; route back to the owning skill when a required gate is `applicable_missing`, lacks owner/applicability reason/residual risk, or needs `approval_required`.
12. Return a staged `lifecycle_route` packet with proposed files, approval needs, blockers, scenario handoff status, conditional readiness gates, and stop reason.

First-run route overlay:

- Empty workspace: use `greenfield_idea`, ask at most one blocking question only when direction is unclear, propose the next smallest action, and stop at the `greenfield idea brief` until approval. Do not scaffold before product direction, minimum artifacts, evidence gaps, and approval boundary are explicit.
- Failed verification: use `bug_rescue`, list candidate failing evidence and missing current reproduction evidence, propose the next reproduction step, and stop at diagnosis when reproduction is missing. Do not fix, do not rewrite broadly, and do not claim a fix without reproduction evidence or owner-confirmed failure evidence.
- Existing control-plane: use `maintenance`, preserve existing control-plane files, list missing control-plane files, and propose exactly one next action. Do not regenerate, overwrite, or ignore existing `AGENTS.md`, `.codex/config.toml`, hooks, workflows, or automation candidates without approval.
- Complex system: use `complex_system_acceleration`, route to integration catalog, ownership split, and release gates before parallel work. Do not parallelize until owned files, forbidden files, external systems, release gates, and overlapping files are explicit.

Usage mode overlay:

| usage_mode | Route behavior |
| --- | --- |
| `bug_rescue` | Stage `.codex/workflows/bug-rescue.md` and `.codex/artifact-templates/bug-rescue-report.md` as proposed files. If `bug_reproduction_signals.present` is false, stop with `missing reproduction evidence` and route to diagnosis only. If evidence is present, keep the next skill evidence-first: `workspace-discovery-auditor` for unclear state, `implementation-planner` for a bounded fix plan, or `risk-reviewer` for failed repeated fixes. |
| `greenfield_idea` | Stage `.codex/workflows/greenfield-idea-to-plan.md` and `.codex/artifact-templates/greenfield-idea-brief.md` as proposed files. Ask at most one blocking question, then propose the next smallest artifact. Do not scaffold until selected direction, first vertical slice and approval boundary are explicit. Use lightweight mode for tiny ideas instead of dumping every methodology gate. |
| `complex_system_acceleration` | Stage `.codex/workflows/complex-system-acceleration.md` and `.codex/artifact-templates/integration-catalog.md` as proposed files. Route ownership-first: integration catalog, ownership split, release gates, then fresh-context task packets before parallel work. Do not parallelize when ownership boundaries, external systems, migrations, release gates, or overlapping files are unclear. |
| `pr_review` | Stage `.codex/workflows/pr-review-readiness.md` and `.codex/artifact-templates/pr-risk-review.md` as proposed files. Require a changed files map, diff source, missing checks, and two-stage review with spec compliance verdict before quality/risk verdict. Route to `risk-reviewer` in read-only review mode. Do not create a PR, do not push, do not publish, and do not perform external writes without explicit approval. |
| `legacy_onboarding` | Stage `.codex/workflows/legacy-onboarding.md` and `.codex/artifact-templates/onboarding-map.md` as proposed files. Route to read-only orientation before any cleanup: source map, entry points, run commands, docs debt, verification status, and `present_unverified` notes. Propose the first safe documentation slice without refactor. Do not refactor, rename, move files, or rewrite stale docs as truth before orientation evidence exists. |
| `api_migration` | Stage `.codex/workflows/api-migration.md` and `.codex/artifact-templates/migration-plan.md` as proposed files. Route to migration planning before implementation or release. Require OpenAPI, AsyncAPI, consumers, generated clients, backwards compatibility, deprecation, examples, rollout, release impact, owner review, contract check evidence, and approval. Do not implement, do not release, and do not update generated clients until the migration plan and owner review exist. |
| `ai_eval_regression` | Stage `.codex/workflows/ai-eval-regression.md` and `.codex/artifact-templates/ai-eval-spec.md` as proposed files. Route to eval planning before model, prompt/context, retrieval, dataset, judge, or threshold changes. Require baseline, dataset, no-secrets policy, rubric, threshold, rerun command, prompt/context inventory, retrieval metrics, judge policy, latency, cost, grounding, failure examples, residual risk, and one-factor-at-a-time change log. Do not change model, prompt, retrieval, dataset, rubric, or threshold, and do not claim quality without current eval evidence. |
| `native_mobile_feature` | Stage `.codex/workflows/native-mobile-feature.md` as a proposed file. Route to platform runtime planning before implementation or quality claims. Require platform assumptions, iOS scope, Android scope, permissions, offline state, simulator, emulator, device, logs, screenshots, build command, runtime evidence, manual device gap, approval boundary, and residual risk. Do not claim runtime behavior, do not change permissions, signing, entitlements, store metadata, or device enrollment without explicit approval. |
| `desktop_local_first` | Stage `.codex/workflows/desktop-local-first.md` as a proposed file. Route to local runtime planning before implementation or quality claims. Require desktop platform assumptions, target OS scope, filesystem permissions, local data, local DB, indexing, background jobs, privacy, app logs, runtime log check, build command, recovery path, rollback, runtime evidence, manual OS gap, approval boundary, and residual risk. Do not claim desktop runtime behavior, do not change filesystem access, local data retention, local DB migration, background autostart, telemetry, privacy-impacting storage, packaging, signing, notarization, or distribution metadata without explicit approval. |
| `data_migration` | Stage `.codex/workflows/data-migration.md`, `.codex/artifact-templates/migration-plan.md`, `.codex/artifact-templates/database-inventory.md`, `.codex/artifact-templates/database-dictionary.md`, `.codex/artifact-templates/database-migration-plan.md`, `.codex/artifact-templates/database-data-contract.md`, `.codex/artifact-templates/database-backup-restore-evidence.md`, and `.codex/artifact-templates/database-production-access-approval.md` as proposed files. Route to Database & Data methodology (`database_data`) before implementation, production DB access, or readiness claims. Require `database_migration_plan_present`, `database_backup_restore_evidence_present`, `database_constraints_integrity_review_present`, `database_production_access_approval_present`, schema change, backfill, data quality, constraints, indexes, PII, sensitive fields, retention, rollback, validation, dry run, backup, database dictionary, owner review, production DB boundary, approval boundary, and residual risk. No universal database tooling default; Liquibase, Flyway, Alembic, Prisma, Rails/Django, dbt, Great Expectations, OpenLineage, DBML, dbdocs, SchemaSpy, and schema-diff tooling are conditional. Do not access production data, do not access production DB, do not run migration, do not run destructive migration, and do not claim data safety without dry run, validation, rollback, backup, and owner review evidence. |
| `security_sensitive_change` | Stage `.codex/workflows/security-sensitive-change.md` and `.codex/artifact-templates/security-risk-review.md` as proposed files. Route to security risk review before implementation, release, production policy changes, or readiness claims. Require threat surface, authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, audit logging, tests, rollback, owner review, approval boundary, and residual risk. Do not change auth, permissions, billing, payment, secrets handling, PII handling, sensitive data access, abuse controls, rate limit behavior, or audit logging without explicit approval. Do not process payments without explicit approval. Treat Codex Security as optional and use it only when explicitly requested; do not imply a Codex Security scan ran from this workflow alone. |
| `ci_stabilization` | Stage `.codex/workflows/ci-stabilization.md` and `.codex/artifact-templates/ci-stabilization-report.md` as proposed files. Route to CI stabilization planning before implementation, remote CI mutation, release, or CI health claims. Require failing job, command, logs, environment, deterministic/flaky classification, failure evidence, isolation plan, local reproduction, rerun evidence, remote CI and GitHub Actions boundary, approval boundary, and residual risk. Do not change CI settings, secrets, branch protections, GitHub Actions permissions, hosted runner config, schedules, concurrency, cache keys, or workflow activation without explicit approval. Do not rerun remote CI without approval when it writes status, consumes hosted resources, or needs connector access. |
| `release_packaging` | Stage `.codex/workflows/release-packaging.md` and `.codex/artifact-templates/release-readiness.md` as proposed files. Route to release readiness planning before publishing, tagging, creating releases, uploading artifacts, mutating package registry settings, opening pull requests, pushing branches, marketplace submission, store submission, or readiness claims. Require release scope, package metadata, version, SemVer impact, changelog, build evidence, test evidence, docs evidence, security notes, license notes, artifacts, package registry, owner review, publish approval, tag boundary, rollback, and residual risk. Do not publish, do not tag, do not create release, do not upload artifacts, and do not mutate package registry settings without explicit approval. |

Route map:

| Lifecycle state | Recommended skill |
| --- | --- |
| `uninitialized` | `workspace-discovery-auditor` |
| `infrastructure_planned` | `requirements-author` |
| `requirements_ready` | `implementation-planner` |
| `plan_ready` | `agent-team-designer` |
| `team_ready` | `test-eval-designer` |
| `build_active` | `risk-reviewer` |
| `quality_gate` | `risk-reviewer` |
| `review_ready` | `pr-release-operator` |
| `release_ready` | `learning-loop-maintainer` |
| `learning_ready` | `automation-promoter` |
| `maintenance` | `project-lifecycle-orchestrator` |

## Outputs

Return a lifecycle route packet:

```yaml
lifecycle_route:
  current_state: ""
  next_state: ""
  recommended_skill: ""
  complexity_profile: ""
  usage_mode: ""
  bug_reproduction_signals: {}
  native_mobile_signals: {}
  desktop_local_signals: {}
  data_migration_signals: {}
  database_data_signals: {}
  security_sensitive_signals: {}
  ci_stabilization_signals: {}
  release_packaging_signals: {}
  blockers: []
  methodology_gaps: []
  conditional_readiness_gates:
    readiness_statuses: "not_applicable | applicable_missing | present_unverified | present_verified | proposal_staged | explicit_gap_accepted | approval_required"
    applicable_missing: []
    present_unverified: []
    present_verified: []
    not_applicable: []
    explicit_gap_accepted: []
    approval_required: []
    owner: ""
    applicability_reason: ""
    residual_risk: ""
  questions: []
  proposed_files: []
  approval_required: []
  scenario_handoff:
    sources_context_used: []
    assumptions: []
    files_touched: []
    files_proposed: []
    verification_evidence: []
    open_risks: []
    recommended_next_role: ""
    stop_reason: ""
  stop_reason: ""
```

## Conditional Readiness Gates

Use conditional readiness gates as lifecycle blockers, not decorative labels. `readiness_statuses` are `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`. Detection alone can only produce `present_unverified`; `present_verified` requires current evidence. A gate can be `not_applicable` only with an applicability reason, and `explicit_gap_accepted` only with owner, residual risk, and follow-up condition.

## Track 9 Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

## Track 9 Database & Data Methodology

Use `database_data` when schema, migration, backfill, persistent data model, production data, PII, retention, deletion, backup/restore, data quality, data contract, lineage, RAG ingestion, runtime pipeline, query performance, index, constraint or transaction boundary signals appear.

Required artifacts: `database-inventory.md`, `database-dictionary.md`, `database-migration-plan.md`, `database-expand-contract-record.md`, `database-backfill-runbook.md`, `database-rollback-feasibility.md`, `database-backup-restore-evidence.md`, `database-data-classification-matrix.md`, `database-data-quality-checks.md`, `database-data-contract.md`, `database-lineage-map.md`, `database-query-performance-review.md`, `database-retention-deletion-policy.md`, `database-synthetic-fixtures-policy.md`, and `database-production-access-approval.md`.

Required gates: `database_inventory_present`, `database_dictionary_present`, `database_schema_source_present`, `database_migration_plan_present`, `database_expand_contract_reviewed`, `database_transaction_boundary_present`, `database_rollback_feasibility_present`, `database_backup_restore_evidence_present`, `database_data_classification_present`, `database_data_quality_contract_present`, `database_data_contract_present`, `database_lineage_present`, `database_performance_review_present`, `database_retention_deletion_policy_present`, `database_synthetic_fixture_policy_present`, `database_production_access_approval_present`, `database_constraints_integrity_review_present`, and `database_unsupported_claims_rejected`.

Use `database_data_signals` with `migration_tools`, `destructive_change_sources`, `production_access_sources`, `pipeline_sources`, and `rag_ingestion_sources` as `present_unverified` until owner-reviewed evidence exists. Production access is `approval_required`. Do not access production data, do not run migration, and do not run destructive migration without explicit approval.

## Track 9 LLM / AI / RAG Methodology

Use `llm_ai_rag` when prompts, model selection, structured outputs, AI tools, MCP/function calling, RAG retrieval, grounding, eval datasets, agent traces, safety, latency or cost signals appear. Route to requirements, planning, test/eval or review before AI behavior changes and quality claims.

Require AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, prompt/context inventory, dataset governance, safety evidence and cost evidence. Stage or request `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, and `ai-cost-latency-budget.md` when applicable.

Do not force one eval runner, do not force multi-agent architecture, and do not run live model calls during lifecycle routing. Use `approval_required` before live model/API calls, external writes, risky tools, data exposure or irreversible side effects.

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.

## Verification

Check that the selected route matches the route map, the state is not skipped, each readiness claim cites current evidence, conditional readiness gates have valid statuses and evidence, every proposed write remains staged, and scenario handoff fields are present before role transition.

## Failure Modes

- If lifecycle state is unknown, route to `workspace-discovery-auditor` for read-only audit.
- If evidence is missing, stop and list unsupported claims.
- If a scenario handoff is missing sources/context used, assumptions, files touched, files proposed, verification evidence, open risks, or recommended next role, stop before role transition.
- If `usage_mode` is `bug_rescue` and reproduction evidence is missing, stop at diagnosis and do not claim a fix.
- If `usage_mode` is `greenfield_idea` and scaffold approval is missing, stop at the idea brief or first-slice plan.
- If `usage_mode` is `complex_system_acceleration` and ownership overlaps, stop before parallel work and route to ownership-first planning.
- If `usage_mode` is `legacy_onboarding`, stop before refactor and require source map, run commands, docs debt, verification status, and `present_unverified` evidence gaps.
- If `usage_mode` is `api_migration` and migration plan, owner review, approval, or contract check evidence is missing, stop before implementation, generated client updates, and release.
- If `usage_mode` is `ai_eval_regression` and baseline, dataset policy, no-secrets handling, threshold, rerun command, or eval evidence is missing, stop before model, prompt/context, retrieval, judge, threshold, release, or quality claims.
- If `usage_mode` is `native_mobile_feature` and platform assumptions, permissions, offline state, build command, simulator/emulator or device evidence, logs, screenshots, manual device gap, or approval is missing, stop before permission changes, production signing, store publishing, or runtime behavior claims.
- If `usage_mode` is `desktop_local_first` and desktop platform assumptions, filesystem permissions, local data, local DB, indexing, background jobs, privacy, build command, app logs, runtime log check, recovery path, rollback, manual OS gap, or approval is missing, stop before filesystem access changes, local data deletion, packaging, signing, notarization, distribution metadata, or desktop runtime behavior claims.
- If `usage_mode` is `data_migration` and schema change, backfill, data quality, PII, sensitive fields, retention, rollback, validation, dry run, backup, database dictionary, owner review, production DB boundary, or approval is missing, stop before production data access, production DB access, migration execution, destructive cleanup, retention changes, or data safety claims.
- If `usage_mode` is `security_sensitive_change` and threat surface, authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, audit logging, tests, rollback, owner review, approval, or residual risk is missing, stop before auth changes, permission changes, payment processing, billing changes, secret handling changes, PII handling changes, sensitive-data access changes, abuse-control changes, audit-logging changes, release, or security safety claims.
- If `usage_mode` is `ci_stabilization` and failing job, command, logs, environment, deterministic/flaky classification, failure evidence, isolation plan, local reproduction, rerun evidence, remote CI boundary, GitHub Actions boundary, approval, or residual risk is missing, stop before implementation, remote CI mutation, release, CI health claims, CI settings changes, workflow permission changes, branch protection changes, hosted runner changes, or remote CI rerun.
- If `usage_mode` is `release_packaging` and release scope, package metadata, version, SemVer impact, changelog, build evidence, test evidence, docs evidence, security notes, license notes, artifacts, package registry, owner review, publish approval, tag boundary, rollback, or residual risk is missing, stop before publishing, tagging, release creation, artifact upload, package registry mutation, PR creation, branch push, marketplace submission, store submission, or release readiness claims.
- If approval is required, stop before external writes or privileged operations.
- If the request asks for Track 3 generation, return proposed files and route details only.
- If automation is requested without manual stability evidence, route to candidate-only analysis.

## Final Response Contract

Return current state, next state, recommended skill, blockers, questions, proposed files, scenario handoff status, approval requirements, unsupported claims, risks, and stop reason.
