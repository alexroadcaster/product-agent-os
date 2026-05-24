---
name: automation-promoter
description: Use when a repeated Product-Agent OS workflow has manual stability evidence and needs candidate-only automation readiness analysis.
---

# Automation Promoter

## Trigger

Use this skill when a recurring or repeated Product-Agent OS workflow may be promoted from manual process to automation candidate.

## Boundaries

This is a Track 2 skill. Produce a staged `automation_candidate` packet only. Readiness is `candidate_only`.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, schedules, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not modify external systems, perform external writes, install dependencies, use network access, write user-level memory, run destructive commands, or create runtime jobs.
Do not claim automation readiness, manual stability, verification coverage, rollback safety, owner acceptance, or lifecycle advancement without evidence from the current run.
Ask for approval before any write, external action, schedule proposal beyond the staged packet, permission change, or operation outside the allowed scope.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- Manual stability evidence from repeated successful manual runs.
- Workflow purpose, trigger or cadence, owner, expected inputs, and expected outputs.
- Verification method, known failure modes, rollback or disable path, and recovery notes.
- Write policy preference: `read_only`, `draft_only`, or `approved_write`.
- Approval requirements, scope boundaries, source status, and unsupported claims.

## Process

1. Confirm manual stability evidence exists and identifies repeated successful manual execution.
2. Identify required inputs and stable outputs with enough detail to detect drift.
3. Define write policy as exactly one of `read_only`, `draft_only`, or `approved_write`.
4. Name verification checks, failure modes, owner, trigger or cadence, and rollback_or_disable path.
5. Mark approval requirements for any future write, schedule, external action, or privileged operation.
6. Return `candidate_only` readiness without activating, scheduling, connecting, or executing anything.
7. Block promotion when manual stability evidence, owner, stable inputs, stable outputs, verification, or rollback_or_disable is missing.
8. Return next lifecycle state `maintenance` only when candidate readiness and blockers are explicit.

## Outputs

Return an automation candidate packet:

```yaml
automation_candidate:
  name: ""
  purpose: ""
  trigger_or_cadence: ""
  required_inputs: []
  stable_outputs: []
  write_policy: "read_only | draft_only | approved_write"
  verification: []
  failure_modes: []
  owner: ""
  rollback_or_disable: ""
  approval_required: []
  readiness: "candidate_only"
  next_lifecycle_state: "maintenance"
```

## Verification

Check that manual stability evidence is present, owner is named, required inputs and stable outputs are explicit, write policy is one allowed value, rollback_or_disable is actionable, approval requirements are listed, and readiness remains `candidate_only`. Do not claim without evidence.

## Failure Modes

- If manual stability evidence is missing, stop and return readiness `candidate_only` with blockers.
- If owner is missing, stop and request owner assignment.
- If stable inputs or stable outputs are missing, stop and request a clearer workflow contract.
- If verification or failure modes are missing, stop and request evidence from manual runs.
- If rollback_or_disable is missing, stop and request an operational disable path.
- If approval is needed, stop before writes, schedules, external actions, or runtime execution.

## Final Response Contract

Return status, lifecycle state, `automation_candidate`, readiness, blockers, evidence used, unsupported claims, approval requirements, residual risks, and the next recommended skill.
