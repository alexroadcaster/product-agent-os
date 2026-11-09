---
name: requirements-author
description: Use when a workspace audit and project goal exist but requirements, non-goals, constraints, users, and acceptance criteria are not yet staged.
---

# Requirements Author

## Trigger

Use this skill when a workspace audit and project goal exist but requirements, non-goals, constraints, users, and acceptance criteria are not yet staged.

## Boundaries

Default output is a staged packet. `workspace_apply: explicit_task_authority` permits direct local edits only when the current user request or parent task explicitly authorizes workspace writes, the host agent has `workspace-write`, and the exact owned files are named. It never authorizes external, destructive, global-config, permission, provider, browser, Git, release, deployment, publication, hook, or automation actions.

Guided question protocol: ask the smallest blocking question only; enforce one blocking question maximum; optional questions stay in the packet; route answers into artifacts or accepted gaps; guided questions are not workspace evidence. Do not use guided questions as a substitute for workspace evidence.

Self-verification metrics loop (`agent_skill_metrics_loop`): route agent/skill metrics as staged evidence only. Dashboard or report is not proof. Do not apply modernization candidates, do not activate schedules, do not call live eval services, and do not treat a dashboard or report as proof. Rollback evidence required before any modernization candidate can be reviewed.
Project code graph: generated graph is not source of truth; use it as orientation evidence only. Read source files before edits, impact claims, readiness claims, or completion claims. Stale or ambiguous graph blocks readiness claims. Do not treat graph HTML as proof.


Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Change project config or code only when the current task explicitly owns that file.
Write assigned local requirements artifacts under explicit task authority; otherwise return staged proposals. Do not run destructive commands, install dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim requirements readiness, stakeholder agreement, source support, or verification results without evidence tied to the checked state. Reuse unchanged evidence with its original run identified; rerun after relevant changes or uncertainty.
Ask for approval for external actions, expanded scope, or irreversible product decisions.

Instruction hierarchy and evidence reuse follow [Source policy](../references/source-policy.md); factual sources do not override instructions. Read other shared references only when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

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

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.


## Conditional References

Read the `Skill: requirements-author` section of [Complexity routing](../references/complexity-routing.md), only the subsections matching the changed domain or gate below. Mixed work reads all applicable subsections; unknown applicability requires inspection. Do not load unrelated roles.

- **Requirements Domain Methodology** — changes or claims in Requirements Domain.
- **Solution Architecture Methodology** — changes or claims in Solution Architecture.
- **Quality Testing & Evals Methodology** — changes or claims in Quality Testing & Evals.
- **Codex Agentic Workflow** — agent roles, tools, MCP, hooks, skills or automation.
- **LLM / AI / RAG Methodology** — changes or claims in LLM / AI / RAG.
- **Frontend Methodology** — changes or claims in Frontend.
- **Backend Methodology** — changes or claims in Backend.
- **Security, Privacy & Compliance Methodology** — changes or claims in Security, Privacy & Compliance.
- **Delivery, Release & Operations** — release, deployment, operations or rollback.

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
## Cross-Domain Synthesis

Consume `methodology_synthesis` and `recommendation_groups` as grouped recommendations; do not dump every methodology gate. Preserve owner domains, consumer domains, semantic evidence sufficiency, source artifact ledger, alias/deferred artifact ledger and risk-aware safe next action. Do not scaffold before approval, and remember that detection is not verification.
