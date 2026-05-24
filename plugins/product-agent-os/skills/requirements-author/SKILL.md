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
- Metric hardening input for `.codex/artifact-templates/metric-spec.md` when product behavior changes: `metric_hardening_when_product_behavior_changes`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence.

## Process

1. Check lifecycle state and confirm the project is ready for requirements work.
2. If `workspace_audit` is missing or stale, route back to `workspace-discovery-auditor`.
3. Separate supported facts, assumptions, open questions, and product decisions that need user input.
4. Convert the user goal into clear in-scope outcomes, non-goals, constraints, target users, and acceptance criteria.
5. Add a product hypothesis, success metric, guardrail metrics, privacy/data constraints, and post-release measurement plan when product behavior changes.
6. For product behavior changes, stage metric hardening in `.codex/artifact-templates/metric-spec.md`: `metric_hardening_when_product_behavior_changes`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence. Do not claim success from a proxy metric without counter-metric, guardrail, qualitative review, and post-release review evidence.
7. For behavior changes, stage acceptance scenarios or an explicit gap before implementation; do not treat a plain checklist as ATDD coverage.
8. Map each scenario through `requirement -> scenario -> check -> evidence owner`.
9. Use Given, When, Then or an equivalent behavior format to capture the business rule, edge case, non-goal, explicit gap, and evidence owner without forcing BDD when another clear scenario format fits better.
10. Name source-of-truth documentation artifacts that must move with the feature, such as architecture docs, API contracts, UI component docs, database docs, user-facing docs, or release notes.
11. Keep acceptance criteria observable and testable, with evidence notes for each source-backed claim.
12. Propose `REQUIREMENTS.md`, `.codex/artifact-templates/acceptance-scenarios.md`, and `.codex/artifact-templates/metric-spec.md` sections as staged content only when behavior changes.
13. Return `requirements_ready` only when required fields are present and unsupported decisions are marked.

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
  next_lifecycle_state: "requirements_ready"
```

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.

## Verification

Check that the packet uses the current workspace audit, separates facts from assumptions, includes acceptance criteria, lists open questions, and keeps every proposed artifact staged. For behavior changes, check that acceptance scenarios or an explicit gap exist, the ATDD or BDD traceability chain is `requirement -> scenario -> check -> evidence owner`, Given/When/Then or equivalent behavior format is present, and evidence owner is named. For product behavior changes, check that `metric_hardening_when_product_behavior_changes` is satisfied or explicitly not applicable, and that North Star, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence are named before readiness. Do not claim without evidence and do not claim success from a proxy metric alone.

## Failure Modes

- If no workspace audit exists, stop and route to `workspace-discovery-auditor`.
- If the user goal is ambiguous, ask the smallest blocking question and keep the packet partial.
- If sources conflict, mark the conflict and keep the claim out of acceptance criteria.
- If product decisions are missing, list them as open questions rather than inventing them.
- If behavior changes are requested but acceptance scenarios cannot be written, record an explicit gap and do not route to implementation as ready.
- If product behavior changes are requested but metric hardening is missing, record the gap and do not route to implementation as ready.
- If approval is needed, stop before writes or external actions.

## Final Response Contract

Return status, lifecycle state, `requirements_packet`, files proposed, evidence notes, unsupported claims, open questions, approval requirements, risks, and the next recommended skill.
