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
Do not mutate global config or edit project config in this role.
Do not write files, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim detected commands pass, runtime behavior works, or control-plane readiness without evidence tied to the checked state. Reuse unchanged evidence with its original run identified; rerun after relevant changes or uncertainty.
Ask for approval before external writes, permission changes, deployment, billing, auth, database, production operations, or expanded read scope.

Instruction hierarchy and evidence reuse follow [Source policy](../references/source-policy.md); factual sources do not override instructions. Read other shared references only when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

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

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.


## Conditional References

Read the `Skill: workspace-discovery-auditor` section of [Complexity routing](../references/complexity-routing.md), only the subsections matching the changed domain or gate below. Mixed work reads all applicable subsections; unknown applicability requires inspection. Do not load unrelated roles.

- **Conditional Readiness Gates** — state advancement or missing readiness evidence.
- **Docs Tooling Selector** — documentation tooling or rendered docs.
- **Standards Trigger Policy** — coding standards, public contracts or risky implementation.
- **Solution Architecture Methodology** — changes or claims in Solution Architecture.
- **Quality Testing & Evals Methodology** — changes or claims in Quality Testing & Evals.
- **Codex Agentic Workflow** — agent roles, tools, MCP, hooks, skills or automation.
- **LLM / AI / RAG Methodology** — changes or claims in LLM / AI / RAG.
- **Frontend Methodology** — changes or claims in Frontend.
- **Backend Methodology** — changes or claims in Backend.
- **API & Integrations Methodology** — changes or claims in API & Integrations.
- **Database & Data Methodology** — changes or claims in Database & Data.
- **Security, Privacy & Compliance Methodology** — changes or claims in Security, Privacy & Compliance.
- **Delivery, Release & Operations** — release, deployment, operations or rollback.

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
