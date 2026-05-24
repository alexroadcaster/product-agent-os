---
name: pr-release-operator
description: Use when verified Product-Agent OS work needs a staged PR packet, release packet, rollback note, or approval note.
---

# PR Release Operator

## Trigger

Use this skill when Product-Agent OS work is review-ready and needs a PR packet, release packet, rollout note, rollback note, or explicit approval note.

## Boundaries

This is a Track 2 skill. Produce a staged `pr_release_packet` only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not publish externally, push branches, open pull requests, edit files, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim release readiness, command success, test coverage, runtime behavior, external publication, or rollback safety without evidence from the current run.
Ask for approval before any write, external publishing action, expanded scope, dependency installation, or operation outside the allowed workspace.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- `requirements_packet` with goal, scope, acceptance criteria, and constraints.
- `implementation_plan_packet` with slices, files proposed, rollback notes, and risks.
- `risk_review_packet` with verdict, findings, missing tests, approval risks, and residual risks.
- Commands run, observed results, verification evidence, unsupported claims, and test gaps.
- User impact, rollback notes, release notes, approvals needed, and residual risks.

## Process

1. Validate that risk review verdict is `ready` and lifecycle state is `review_ready`.
2. Summarize what changed and why, grounded in requirements and implementation plan packets.
3. Include verification commands with observed results, artifacts inspected, and remaining gaps.
4. Document user impact, operational impact, rollout considerations, rollback steps, and residual risks.
5. List approval requirements, external publishing constraints, and actions that remain outside the staged packet.
6. Prepare staged PR or release text without publishing externally.
7. Keep proposed `RUNLOG.md` updates staged; do not write the file directly.
8. Return `release_ready` only when summary, checks, impact, rollback, residual risks, and approval requirements are explicit.

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
  files_proposed:
    - "RUNLOG.md"
  next_lifecycle_state: "release_ready"
```

## Verification

Check that release text is backed by current evidence, commands include observed results, rollback is actionable, residual risks and approvals are explicit, and every proposed artifact remains staged. Do not claim without evidence.

## Failure Modes

- If risk review is missing, stop and route to `risk-reviewer`.
- If verdict is not `ready`, stop and return the blocking findings or requested changes.
- If command evidence is missing, record unsupported claims and request verification.
- If rollback or user impact is unknown, return open release questions.
- If approval is needed, stop before publishing, external actions, or writes.

## Final Response Contract

Return status, lifecycle state, `pr_release_packet`, files proposed, verification evidence, unsupported claims, approval requirements, residual risks, and the next recommended skill.
