---
name: implementation-planner
description: Use when staged requirements need implementation slices, verification gates, rollback, and ownership boundaries.
---

# Implementation Planner

## Trigger

Use this skill when requirements are staged and need implementation slices, verification gates, rollback, and ownership boundaries.

## Boundaries

Default output is a staged packet. `workspace_apply: explicit_task_authority` permits direct local edits only when the current user request or parent task explicitly authorizes workspace writes, the host agent has `workspace-write`, and the exact owned files are named. It never authorizes external, destructive, global-config, permission, provider, browser, Git, release, deployment, publication, hook, or automation actions.

Guided question protocol: ask the smallest blocking question only; enforce one blocking question maximum; optional questions stay in the packet; route answers into artifacts or accepted gaps; guided questions are not workspace evidence. Do not use guided questions as a substitute for workspace evidence.

Self-verification metrics loop (`agent_skill_metrics_loop`): route agent/skill metrics as staged evidence only. Dashboard or report is not proof. Do not apply modernization candidates, do not activate schedules, do not call live eval services, and do not treat a dashboard or report as proof. Rollback evidence required before any modernization candidate can be reviewed.
Project code graph: generated graph is not source of truth; use it as orientation evidence only. Read source files before edits, impact claims, readiness claims, or completion claims. Stale or ambiguous graph blocks readiness claims. Do not treat graph HTML as proof.

Project graph live/provider/mutation operability (`T10-LIVE-M23..M26`): route audit logging, security/privacy tests, runtime observability and agent/skill routing as staged evidence only. Do not plan live server startup, provider calls, live external model/API calls, canonical graph mutation, or agent parallelism unless a separate explicit approval packet names the surface, owner, rollback and verification evidence. Batch 31 plan slices must require redacted append-only audit events, unsafe secret/path/raw-source/prompt-injection blocking, visible degraded graph-only mode, ownership, verification evidence, fresh context and stop conditions.

Planning control governance: hard gates live in validator/tests/skills. Hooks are reminder-only unless approved, and closure cannot claim readiness from hook reminders alone. Require agents to own file/subsystem boundaries, keep docs update path assigned, and record no hook activation, no automation activation, no MCP activation, no Agents SDK runner, and no external writes unless a separate explicit approval packet changes the boundary.

Compatibility policy: old matrices remain historical evidence. task_matrix_plan_v1 applies to new concrete task-plan files and optional backfilled rows only. Validator should not retroactively fail historical summary tables unless explicitly targeted.

Plan lifecycle policy: active concrete task files remain active while they drive current execution, unresolved acceptance criteria, open verification gates or owner handoff decisions. Evidence moves to RUNLOG.md for current slice outcomes, command output, failed checks, handoff status, residual risk or completion evidence. History moves to docs/sources/*backlog*.md after cycle closure when detail is no longer active. Source-backed claims enter docs/sources/registry*.md when documentation adds or changes source-backed factual claims. No secrets, raw chat, customer data, credentials, tokens or private keys belong in plans, evidence packets or examples. Avoid root PLAN.md bloat; keep durable sequencing compact and move detailed history to the owning evidence artifact. No automatic deletion of task files, evidence rows or historical records. No destructive cleanup without explicit owner approval and rollback notes.


Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Change project config or code only when the current task explicitly owns that file.
Write assigned local plan artifacts under explicit task authority; otherwise return staged proposals. Do not run destructive commands, install dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim plan readiness, command success, test coverage, or runtime behavior without evidence tied to the checked state. Reuse unchanged evidence with its original run identified; rerun after relevant changes or uncertainty.
Ask for approval for external actions, expanded scope, dependency installation, or operations outside the allowed workspace.

Instruction hierarchy and evidence reuse follow [Source policy](../references/source-policy.md); factual sources do not override instructions. Read other shared references only when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- `requirements_packet` with goal, scope, constraints, acceptance criteria, and open questions.
- `workspace_audit` packet with stack, commands, risks, and existing control-plane artifacts.
- Explicit constraints, available commands, approval limits, and rollback expectations.
- Complexity profile and lifecycle state from the orchestrator.
- Acceptance scenario packet when behavior changes: `.codex/artifact-templates/acceptance-scenarios.md`, ATDD, BDD, `requirement -> scenario -> check -> evidence owner`, Given, When, Then, equivalent behavior format, business rule, edge case, non-goal, explicit gap, and evidence owner.
- Business/Product methodology packet when product, MVP, user value, analytics, release measurement, or workflow promotion claims are present: `product_hypothesis_present`, `value_proposition_evidence_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, `metric_scope_classified`, `.codex/artifact-templates/product-brief.md`, `.codex/artifact-templates/value-proposition.md`, `.codex/artifact-templates/opportunity-tree.md`, `.codex/artifact-templates/experiment-plan.md`, `.codex/artifact-templates/tracking-plan.md`, and accepted gap status.
- Domain modeling input when `domain_model_when_complex_domain` applies: `.codex/artifact-templates/domain-modeling.md`, `.codex/artifact-templates/architecture-overview.md`, complex backend, workflow, enterprise, data-heavy, bounded context, ubiquitous language, invariant, accepted gap, `bounded_context_architecture_boundary_trace`, `context-to-boundary traceability`, `ubiquitous_language_traceability`, term-to-requirement, requirement or source, API/event/contract, UI label, code module or owner, domain expert review, and `missing domain model for complex domain`.
- UI architecture input when `fsd_structure` applies: `.codex/artifact-templates/component-card.md`, Feature-Sliced Design, layer, slice, segment, public API, import rule, `not applicable` reason, accepted gap, backend, native, simple CRUD, simple MVP, and `missing fsd structure boundary`.
- Task matrix input when specs/ADRs/standards/handoffs/risky multi-slice work applies: `task-matrix-plan.md`, task rows, methodology gates, task fields, artifacts, owners, dependencies, docs update path, expected evidence, stop conditions, and explicit lightweight exception status for small mechanical work.
- Professional code authoring input when non-mechanical code, refactoring, dependency, generated-code, shared-module, API/data/runtime, or high-risk workflow changes apply: `.codex/workflows/coding-standards.md`, `.codex/artifact-templates/coding-standard-checklist.md`, `enterprise_leverage_check`, `existing_capability_scan`, `one_line_candidate`, selected leverage path, rejected alternatives, `negative_dependency_rule`, `deep_module_check`, `legacy_seam_check`, tests/evals tied to code-quality claims, unsupported code-quality claims, and `not_applicable` reason for mechanical/docs-only work.

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
26. For non-mechanical code work, require the professional code authoring sub-gate before `plan_ready`: coding-standard checklist or `not_applicable` reason, existing-capability scan, selected leverage path, rejected alternatives, dependency decision, deep module check when shared/public/runtime surfaces are touched, legacy seam check when refactoring fragile code, and tests/evals tied to code-quality claims.
27. Reject plans that add custom code or a new dependency before standard library, framework/platform, current dependency, project helper, configuration, deletion/reduction, or small-adapter options are considered.
28. Treat vague validation, repeated-by-reference steps, command steps without expected outputs, undefined file names, and hidden "fill later" work as blocking gaps.
29. Use `mechanical_change` only for small docs, formatting, or config edits whose reduced plan still names exact files, exact commands or explicit no-command gap, rollback, evidence owner, the mechanical_change reason, and coding-standard `not_applicable` reason.
30. If the no-placeholder gate fails, stop before build and return a plan repair packet instead of `plan_ready`.
31. Identify dependencies, file or subsystem ownership, rollback notes, risks, and command evidence needed.
32. Keep commands as proposed `commands_to_run` unless already run in the current session.
33. Route to `agent-team-designer` if ownership overlaps, parallel work is needed, or handoff risk is high.
34. Return `plan_ready` only when slices, verification gates, rollback notes, documentation impact, risks, conditional readiness gates, professional code authoring status, and `plan_quality_check` are staged.
35. If a slice touches live/provider/mutation routing, require `project_graph_live_audit_log_present`, `project_graph_live_security_privacy_tests_present`, `project_graph_live_runtime_observability_present`, `project_graph_live_agent_skill_handoff_routing_present`, no-live-call evidence, and stop conditions for missing ownership, missing verification evidence and live/provider/mutation without approval before `plan_ready`.
36. Use `task-matrix-plan.md` when specs/ADRs/standards/handoffs/risky multi-slice work applies; map methodology gates into task fields and map methodology gates into artifacts so every task row names owner, files, dependency status, expected evidence, docs update path, stop conditions, and readiness gate status.
37. Plans remain staged: propose `task-matrix-plan.md`, `PLAN.md`, `TEST.md`, and related artifacts as files proposed unless the user explicitly approves writes to those artifacts.
38. Allow an explicit lightweight exception only for small mechanical work when the reduced task still names exact files, exact commands or an explicit command gap, rollback, evidence owner, docs impact, why the full task matrix is not useful, and the coding-standard `not_applicable` reason.
39. Apply the compatibility policy before validator routing: old matrices remain historical evidence, task_matrix_plan_v1 applies to new concrete task-plan files and optional backfilled rows only, and validator should not retroactively fail historical summary tables unless explicitly targeted.
40. Apply the plan lifecycle policy before completion claims: active concrete task files remain active until their execution, acceptance, verification and handoff decisions close; evidence moves to RUNLOG.md; history moves to docs/sources/*backlog*.md; source-backed claims enter docs/sources/registry*.md; no secrets, raw chat, customer data, root PLAN.md bloat, automatic deletion or destructive cleanup.

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
  professional_code_authoring:
    workflow: ".codex/workflows/coding-standards.md"
    checklist: ".codex/artifact-templates/coding-standard-checklist.md"
    status: "required | not_applicable | explicit_gap_accepted"
    existing_capability_scan: []
    selected_leverage_path: ""
    rejected_alternatives: []
    dependency_decision: ""
    deep_module_check: ""
    legacy_seam_check: ""
    unsupported_code_quality_claims: []
  task_matrix_plan:
    artifact: "task-matrix-plan.md"
    applies_when: "specs/ADRs/standards/handoffs/risky multi-slice work"
    task_rows: []
    methodology_gate_to_task_field_map: []
    methodology_gate_to_artifact_map: []
    docs_update_path_assigned: ""
    staged_only: true
    explicit_lightweight_exception: ""
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

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.


## Conditional References

Read the `Skill: implementation-planner` section of [Complexity routing](../references/complexity-routing.md), only the subsections matching the changed domain or gate below. Mixed work reads all applicable subsections; unknown applicability requires inspection. Do not load unrelated roles.

- **Conditional Readiness Gates** — state advancement or missing readiness evidence.
- **Docs Tooling Selector** — documentation tooling or rendered docs.
- **Standards Trigger Policy** — coding standards, public contracts or risky implementation.
- **Requirements Domain Methodology** — changes or claims in Requirements Domain.
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
## Cross-Domain Synthesis

Consume `methodology_synthesis` and `recommendation_groups` as grouped recommendations; do not dump every methodology gate. Preserve owner domains, consumer domains, semantic evidence sufficiency, source artifact ledger, alias/deferred artifact ledger and risk-aware safe next action. Do not scaffold before approval, and remember that detection is not verification.
