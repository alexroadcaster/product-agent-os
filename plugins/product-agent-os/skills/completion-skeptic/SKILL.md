---
name: completion-skeptic
description: Use after an apparent completion claim or before final handoff to re-check claims, evidence, gaps, approvals, and missing details.
---

# Completion Skeptic

## Trigger

Use this skill when the user asks to check again, when a final response would say done/ready/verified/implemented/complete, or when a Product-Agent OS route includes `completion_skeptic_recommendation`.

## Boundaries

Produce a `doubt_verification_packet` and handoff mapping only. `workspace_apply: forbidden` preserves read-only assurance; fixes belong to a separately authorized writable role.

Guided question protocol: ask the smallest blocking question only; enforce one blocking question maximum; optional questions stay in the packet; route answers into artifacts or accepted gaps; guided questions are not workspace evidence. Do not use guided questions as a substitute for workspace evidence.

Self-verification metrics loop (`agent_skill_metrics_loop`): route agent/skill metrics as staged evidence only. Dashboard or report is not proof. Do not apply modernization candidates, do not activate schedules, do not call live eval services, and do not treat a dashboard or report as proof. Rollback evidence required before any modernization candidate can be reviewed.
Project code graph: generated graph is not source of truth; use it as orientation evidence only. Read source files before edits, impact claims, readiness claims, or completion claims. Stale or ambiguous graph blocks readiness claims. Do not treat graph HTML as proof.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config or edit project config in this role.
Do not edit files, apply fixes, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not use network access.
Do not claim completion, readiness, security, test coverage, command success, runtime behavior, or risk closure without evidence tied to the checked state. Reuse unchanged evidence with its original run identified; rerun after relevant changes or uncertainty.
Generated dashboards are not completion proof; generated status, site, report, or graph views are orientation evidence until backed by underlying source artifacts or current command evidence.
If a write is needed, hand off to a separately authorized writable role. Parent workspace-write does not change this read-only role.

Instruction hierarchy and evidence reuse follow [Source policy](../references/source-policy.md); factual sources do not override instructions. Read other shared references only when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- Completion claim, final response draft, task row, handoff packet, runtime result, or status snapshot.
- Requirements, acceptance criteria, plan rows, source constraints, approval boundaries, and non-goals.
- Current command evidence, fixture eval, transcript eval, Codex compatibility evidence, source registry entries, owner evidence, and accepted gaps.
- Known stale evidence, unsupported claims, generated dashboard/report/site/project graph views, or missing evidence.

## Process

1. Identify the exact claims that would be presented as supported claims.
2. Build `claim_ledger`: mark each claim as supported, unsupported, contradicted, needs_fresh_check, assumption, or accepted_gap.
3. Build `requirement_ledger`: map every relevant requirement, acceptance criterion, task row, source-policy rule, and approval boundary.
4. Build `evidence_ledger`: separate proof from orientation evidence; generated dashboards are not completion proof.
5. Check evidence freshness, command results, verification tied to the checked state, source-backed docs, owner approvals, accepted gaps, and residual risks.
6. Check approval boundaries for live automation, provider/live external model/API calls, browser automation, target workspace mutation, canonical graph mutation, external writes, git stage/commit/push/PR, MCP activation, hooks, or Agents SDK runner activation.
7. Map results into handoff mapping: supported claims, unsupported claims, commands run, verification evidence, approval requirements, open risks, stop reason, and recommended next role.
8. Return verdict `pass`, `revise`, `needs_more_context`, `blocked_by_approval`, `accepted_risk`, or `blocked`.
9. If evidence is missing, stale, generated-view-only, or approval-bound, do not claim completion; return the smallest next action.

## Outputs

Return a doubt verification packet:

```yaml
doubt_verification_packet:
  schema_version: "doubt_verification_packet_v1"
  verdict: "pass | revise | needs_more_context | blocked_by_approval | accepted_risk | blocked"
  artifact_under_review:
    kind: "task_row | runtime_result | handoff_packet | docs_page | code_change | staged_artifact | not_available"
    path: ""
    label: ""
  claim_ledger: []
  requirement_ledger: []
  evidence_ledger: []
  approval_boundary:
    status: "not_required | required | approval_blocked"
    hits: []
  gap_ledger: []
  handoff:
    verified_claims: []
    unsupported_claims: []
    commands_run: []
    verification_evidence: []
    approval_requirements: []
    open_risks: []
    stop_reason: ""
    recommended_next_role: ""
  source_policy: "doubt verification packet is evidence ledger, not generated dashboard proof"
  redaction_status:
    status: "clean | redacted | blocked"
    categories: []
```

## Verification

- Validate the packet shape with `validate_doubt_verification_packet.py` when a JSON packet is produced.
- Confirm every supported claim has current evidence or an accepted gap.
- Confirm every unsupported claim remains visible in handoff mapping.
- Confirm generated dashboards are not completion proof.
- Confirm no secrets, raw private chat logs, private customer data, or local absolute paths are present.

## Failure Modes

- Completion claim from stale, missing, inspection-only, dashboard-only, report-only, site-only, or graph-only evidence.
- Supported claims without provenance.
- Accepted gaps without owner, reason, residual risk, and follow-up.
- Approval-bound action treated as completed without approval.
- Handoff mapping omits unsupported claims or open risks.

## Final Response Contract

Lead with the verdict and the missing or unsupported claims.
Name supported claims separately from unsupported claims.
List current verification evidence and accepted gaps.
State approval boundaries and residual risks.
End with the next smallest action, not a completion claim, unless the packet verdict is `pass`.
