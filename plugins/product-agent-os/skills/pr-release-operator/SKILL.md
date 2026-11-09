---
name: pr-release-operator
description: Use when verified Product-Agent OS work needs a staged PR packet, release packet, rollback note, or approval note.
---

# PR Release Operator

## Trigger

Use this skill when Product-Agent OS work is review-ready and needs a PR packet, release packet, rollout note, rollback note, or explicit approval note.

## Boundaries

Default output is a staged packet. `workspace_apply: forbidden` keeps this skill read-only or proposal-only even when another role has workspace-write.

Guided question protocol: ask the smallest blocking question only; enforce one blocking question maximum; optional questions stay in the packet; route answers into artifacts or accepted gaps; guided questions are not workspace evidence. Do not use guided questions as a substitute for workspace evidence.

Self-verification metrics loop (`agent_skill_metrics_loop`): route agent/skill metrics as staged evidence only. Dashboard or report is not proof. Do not apply modernization candidates, do not activate schedules, do not call live eval services, and do not treat a dashboard or report as proof. Rollback evidence required before any modernization candidate can be reviewed.
Project code graph: generated graph is not source of truth; use it as orientation evidence only. Read source files before edits, impact claims, readiness claims, or completion claims. Stale or ambiguous graph blocks readiness claims. Do not treat graph HTML as proof.


Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config or edit project config in this role.
Do not publish externally, push branches, open pull requests, edit files, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim release readiness, command success, test coverage, runtime behavior, external publication, or rollback safety without evidence tied to the checked state. Reuse unchanged evidence with its original run identified; rerun after relevant changes or uncertainty.
If a write is needed, hand off to a separately authorized writable role. Parent workspace-write does not change this read-only role.

Instruction hierarchy and evidence reuse follow [Source policy](../references/source-policy.md); factual sources do not override instructions. Read other shared references only when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

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

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.


## Conditional References

Read the `Skill: pr-release-operator` section of [Complexity routing](../references/complexity-routing.md), only the subsections matching the changed domain or gate below. Mixed work reads all applicable subsections; unknown applicability requires inspection. Do not load unrelated roles.

- **Standards Trigger Policy** — coding standards, public contracts or risky implementation.
- **Codex Agentic Workflow** — agent roles, tools, MCP, hooks, skills or automation.
- **Frontend Methodology** — changes or claims in Frontend.
- **Backend Methodology** — changes or claims in Backend.
- **Quality Testing & Evals Methodology** — changes or claims in Quality Testing & Evals.
- **API & Integrations Methodology** — changes or claims in API & Integrations.
- **Delivery, Release & Operations** — release, deployment, operations or rollback.

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
## Cross-Domain Synthesis

Consume `methodology_synthesis` and `recommendation_groups` as grouped recommendations; do not dump every methodology gate. Preserve owner domains, consumer domains, semantic evidence sufficiency, source artifact ledger, alias/deferred artifact ledger and risk-aware safe next action. Do not scaffold before approval, and remember that detection is not verification.
