---
name: test-eval-designer
description: Use when a Product-Agent OS plan needs deterministic tests, manual checks, eval gates, or test gap documentation before implementation or review.
---

# Test Eval Designer

Use the Minimal Complete Changes section of the coding-standards workflow for independent oracles, unique-test preservation, adapter compatibility and bounded waits. For behavior-preserving refactors use existing characterization evidence; configuration needs parse/invariants, not artificial RED.

## Trigger

Use this skill when a Product-Agent OS project needs test commands, eval criteria, quality gates, or explicit verification evidence requirements before implementation, review, or handoff.

## Boundaries

Default output is a staged packet. `workspace_apply: explicit_task_authority` permits direct local edits only when the current user request or parent task explicitly authorizes workspace writes, the host agent has `workspace-write`, and the exact owned files are named. It never authorizes external, destructive, global-config, permission, provider, browser, Git, release, deployment, publication, hook, or automation actions.

Guided question protocol: ask the smallest blocking question only; enforce one blocking question maximum; optional questions stay in the packet; route answers into artifacts or accepted gaps; guided questions are not workspace evidence. Do not use guided questions as a substitute for workspace evidence.

Self-verification metrics loop (`agent_skill_metrics_loop`): route agent/skill metrics as staged evidence only. Dashboard or report is not proof. Do not apply modernization candidates, do not activate schedules, do not call live eval services, and do not treat a dashboard or report as proof. Rollback evidence required before any modernization candidate can be reviewed.
Project code graph: generated graph is not source of truth; use it as orientation evidence only. Read source files before edits, impact claims, readiness claims, or completion claims. Stale or ambiguous graph blocks readiness claims. Do not treat graph HTML as proof.


Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Change project config or production code only when the current task explicitly owns that file.
Write assigned local tests, evals, TEST.md, or EVALS.md under explicit task authority; otherwise return staged proposals. Do not run destructive commands, install dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim test coverage, eval quality, command success, runtime behavior, or readiness without evidence tied to the checked state. Reuse unchanged evidence with its original run identified; rerun after relevant changes or uncertainty.
Ask for approval for external actions, expanded scope, dependency installation, or operations outside the allowed workspace.

Instruction hierarchy and evidence reuse follow [Source policy](../references/source-policy.md); factual sources do not override instructions. Read other shared references only when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

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

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.


## Conditional References

Read the `Skill: test-eval-designer` section of [Complexity routing](../references/complexity-routing.md), only the subsections matching the changed domain or gate below. Mixed work reads all applicable subsections; unknown applicability requires inspection. Do not load unrelated roles.

- **Conditional Readiness Gates** — state advancement or missing readiness evidence.
- **Docs Tooling Selector** — documentation tooling or rendered docs.
- **Requirements Domain Methodology** — changes or claims in Requirements Domain.
- **Solution Architecture Methodology** — changes or claims in Solution Architecture.
- **Codex Agentic Workflow** — agent roles, tools, MCP, hooks, skills or automation.
- **LLM / AI / RAG Methodology** — changes or claims in LLM / AI / RAG.
- **Frontend Methodology** — changes or claims in Frontend.
- **Backend Methodology** — changes or claims in Backend.
- **Quality Testing & Evals Methodology** — changes or claims in Quality Testing & Evals.
- **API & Integrations Methodology** — changes or claims in API & Integrations.
- **Database & Data Methodology** — changes or claims in Database & Data.
- **Security, Privacy & Compliance Methodology** — changes or claims in Security, Privacy & Compliance.
- **Delivery, Release & Operations** — release, deployment, operations or rollback.

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
## Cross-Domain Synthesis

Consume `methodology_synthesis` and `recommendation_groups` as grouped recommendations; do not dump every methodology gate. Preserve owner domains, consumer domains, semantic evidence sufficiency, source artifact ledger, alias/deferred artifact ledger and risk-aware safe next action. Do not scaffold before approval, and remember that detection is not verification.
