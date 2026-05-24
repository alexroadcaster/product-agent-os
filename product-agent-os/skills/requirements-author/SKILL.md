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

## Process

1. Check lifecycle state and confirm the project is ready for requirements work.
2. If `workspace_audit` is missing or stale, route back to `workspace-discovery-auditor`.
3. Separate supported facts, assumptions, open questions, and product decisions that need user input.
4. Convert the user goal into clear in-scope outcomes, non-goals, constraints, target users, and acceptance criteria.
5. Keep acceptance criteria observable and testable, with evidence notes for each source-backed claim.
6. Propose `REQUIREMENTS.md` sections as staged content only.
7. Return `requirements_ready` only when required fields are present and unsupported decisions are marked.

## Outputs

Return a requirements packet:

```yaml
requirements_packet:
  goal: ""
  users: []
  in_scope: []
  non_goals: []
  constraints: []
  acceptance_criteria: []
  open_questions: []
  assumptions: []
  source_notes: []
  files_proposed:
    - "REQUIREMENTS.md"
  next_lifecycle_state: "requirements_ready"
```

## Verification

Check that the packet uses the current workspace audit, separates facts from assumptions, includes acceptance criteria, lists open questions, and keeps every proposed artifact staged. Do not claim without evidence.

## Failure Modes

- If no workspace audit exists, stop and route to `workspace-discovery-auditor`.
- If the user goal is ambiguous, ask the smallest blocking question and keep the packet partial.
- If sources conflict, mark the conflict and keep the claim out of acceptance criteria.
- If product decisions are missing, list them as open questions rather than inventing them.
- If approval is needed, stop before writes or external actions.

## Final Response Contract

Return status, lifecycle state, `requirements_packet`, files proposed, evidence notes, unsupported claims, open questions, approval requirements, risks, and the next recommended skill.
