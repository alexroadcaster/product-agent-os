---
name: implementation-planner
description: Use when staged requirements need implementation slices, verification gates, rollback, and ownership boundaries.
---

# Implementation Planner

## Trigger

Use this skill when requirements are staged and need implementation slices, verification gates, rollback, and ownership boundaries.

## Boundaries

This is a Track 2 skill. Produce a staged implementation plan packet only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not write `PLAN.md` or `TEST.md` directly, edit code, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim plan readiness, command success, test coverage, or runtime behavior without evidence from the current run.
Ask for approval before any write, external action, expanded scope, dependency installation, or operation outside the allowed workspace.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- `requirements_packet` with goal, scope, constraints, acceptance criteria, and open questions.
- `workspace_audit` packet with stack, commands, risks, and existing control-plane artifacts.
- Explicit constraints, available commands, approval limits, and rollback expectations.
- Complexity profile and lifecycle state from the orchestrator.

## Process

1. Validate that requirements are staged and the lifecycle state is `requirements_ready`.
2. Route back to `requirements-author` if acceptance criteria, constraints, or open questions are incomplete.
3. Decompose work into focused slices with clear acceptance criteria and verification per slice.
4. Identify dependencies, file or subsystem ownership, rollback notes, risks, and command evidence needed.
5. Keep commands as proposed `commands_to_run` unless already run in the current session.
6. Route to `agent-team-designer` if ownership overlaps, parallel work is needed, or handoff risk is high.
7. Return `plan_ready` only when slices, verification gates, rollback notes, and risks are staged.

## Outputs

Return an implementation plan packet:

```yaml
implementation_plan_packet:
  slices: []
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

## Verification

Check that each slice maps to acceptance criteria, each gate names evidence required, rollback notes exist for risky changes, and every proposed artifact remains staged. Do not claim without evidence.

## Failure Modes

- If requirements are missing, stop and route to `requirements-author`.
- If acceptance criteria cannot be mapped to slices, return open planning questions.
- If file ownership overlaps, route to `agent-team-designer` before implementation.
- If available commands are unknown, list discovery needed and keep verification proposed.
- If approval is needed, stop before writes or external actions.

## Final Response Contract

Return status, lifecycle state, `implementation_plan_packet`, files proposed, commands proposed or run, verification evidence, unsupported claims, approval requirements, risks, and the next recommended skill.
