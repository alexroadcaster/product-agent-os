---
name: agent-team-designer
description: Use when an implementation plan exists and agent roles, file ownership, handoffs, reasoning guidance, and stop conditions are needed.
---

# Agent Team Designer

## Trigger

Use this skill when an implementation plan exists and the project needs agent roles, file ownership, handoff packets, reasoning/model guidance, and stop conditions.

## Boundaries

This is a Track 2 skill. Produce a staged team design packet only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not create `.codex/agents/*.toml`, write `AGENTS.md` or `RUNLOG.md` directly, edit code, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim team readiness, ownership safety, verification completion, or model suitability without evidence from the current run.
Ask for approval before any write, external action, expanded scope, permission change, or irreversible team/runtime decision.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- `implementation_plan_packet` with slices, dependencies, verification gates, rollback notes, and risks.
- `workspace_audit` packet with project structure, existing Codex assets, and constraints.
- Complexity profile, team constraints, approval limits, and available verification gates.
- Known file or subsystem ownership requirements from the user or project docs.

## Process

1. Validate that an implementation plan exists and the lifecycle state is `plan_ready`.
2. Route back to `implementation-planner` if slices, gates, or ownership signals are incomplete.
3. Choose only needed roles around ownership: Product Manager, Architect, Builder, Tester, Reviewer, Docs Maintainer, and Release Operator.
4. Assign disjoint file or subsystem ownership for each role and mark unresolved overlaps.
5. Define handoff packet fields: sources/context used, assumptions, files proposed, verification evidence, open risks, stop reason, and recommended next role.
6. Define model/reasoning policy with escalation and downgrade rules tied to risk, ambiguity, cost, and latency.
7. Define stop conditions for missing evidence, overlapping ownership, approvals, secrets exposure, or failed verification gates.
8. Return `team_ready` only when ownership, handoffs, model guidance, escalation rules, and stop conditions are staged.

## Outputs

Return an agent team design packet:

```yaml
agent_team_design_packet:
  roles: []
  ownership_map: []
  handoff_packets: []
  model_reasoning_policy: []
  escalation_rules: []
  stop_conditions: []
  unresolved_overlaps: []
  files_proposed:
    - "AGENTS.md"
    - "RUNLOG.md"
  next_lifecycle_state: "team_ready"
```

## Verification

Check that each role has a concrete ownership boundary, no planned agents share write scope without a handoff rule, every handoff includes verification evidence fields, and every proposed artifact remains staged. Do not claim without evidence.

## Failure Modes

- If no implementation plan exists, stop and route to `implementation-planner`.
- If ownership cannot be separated, route back to planning with overlap details.
- If required verification gates are absent, stop and request planning updates.
- If model or reasoning guidance would override project rules, keep it as a proposal and flag the conflict.
- If approval is needed, stop before writes or external actions.

## Final Response Contract

Return status, lifecycle state, `agent_team_design_packet`, files proposed, ownership overlaps, verification evidence, unsupported claims, approval requirements, risks, and the next recommended skill.
