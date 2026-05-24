---
name: risk-reviewer
description: Use when a Product-Agent OS plan, diff, implementation slice, or quality gate needs risk review before readiness or release.
---

# Risk Reviewer

## Trigger

Use this skill when a Product-Agent OS diff, implementation slice, plan, or quality gate needs review before release readiness or handoff.

## Boundaries

This is a Track 2 skill. Produce a staged `risk_review_packet` only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not edit files, apply fixes, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim readiness, security, test coverage, command success, runtime behavior, or risk closure without evidence from the current run.
Ask for approval before any write, external action, expanded scope, dependency installation, or operation outside the allowed workspace.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- Diff summary, proposed changes, implementation slice summary, or quality gate packet.
- `requirements_packet` with scope, acceptance criteria, constraints, and source requirements.
- `implementation_plan_packet` with slices, rollback notes, ownership, and verification gates.
- Commands run, observed results, verification evidence, unsupported claims, and known test gaps.
- Known risks, approvals, data constraints, migration concerns, source constraints, and external-system boundaries.

## Process

1. Validate that enough context exists to review behavior against requirements and the lifecycle state is `build_active` or `quality_gate`.
2. Lead with findings by severity: blocker, high, medium, low, or note.
3. Check changed or proposed behavior against acceptance criteria, constraints, ownership, and rollback expectations.
4. Check missing tests, weak evidence, unverifiable claims, stale source assumptions, and commands listed without observed results.
5. Check approval, sandbox, security, secrets, data handling, migration, dependency, destructive-command, and external-system risks.
6. Assign verdict `blocked`, `changes_requested`, or `ready` based on evidence and remaining risk.
7. Keep summary secondary to findings and do not rewrite artifacts directly.
8. Return `review_ready` only when the verdict is `ready`; otherwise return the lifecycle state that needs follow-up.

## Outputs

Return a risk review packet:

```yaml
risk_review_packet:
  findings: []
  missing_tests: []
  approval_risks: []
  source_risks: []
  security_risks: []
  unsupported_claims: []
  verdict: "blocked | changes_requested | ready"
  next_action: ""
  next_lifecycle_state: "review_ready"
```

## Verification

Check that every finding has severity, evidence, affected scope, and required action. Check that missing tests and approval risks are explicit, source constraints are respected, and `review_ready` appears only with a `ready` verdict. Do not claim without evidence.

## Failure Modes

- If no diff, slice, or plan summary exists, stop and request the missing review input.
- If requirements are absent, stop and route to `requirements-author`.
- If verification evidence is absent, return `changes_requested` or `blocked` with missing evidence.
- If secrets, approval gaps, migration risk, or external-system risk is unresolved, return `blocked`.
- If source claims lack authoritative support, record source risks and request verification.

## Final Response Contract

Return status, lifecycle state, `risk_review_packet`, findings by severity, missing tests, approval requirements, verification evidence, unsupported claims, verdict, risks, and the next recommended skill.
