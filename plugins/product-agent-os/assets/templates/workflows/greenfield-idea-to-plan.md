# Greenfield Idea To Plan

Project: {project_name}
Profile: {profile_name}

## Inputs

- Problem:
- Users:
- Constraints:
- Options:
- Non-goals:
- Existing notes:
- Approval boundary:

## Process

1. Capture the problem and users before choosing technology.
2. List options, tradeoffs and rejected directions.
3. Select one direction or ask at most one blocking question when the direction is unclear.
4. Define non-goals so the first slice stays small.
5. Define the first vertical slice with behavior, data, UI/API/docs impact and runtime boundary.
6. Draft acceptance scenarios and metrics before any scaffold.
7. Record the docs/tooling decision input: docs portal needed, API contract needed, database docs needed, or not applicable.
8. Ask for explicit approval before scaffold, package installation, external service setup, hook activation, CI, hosted docs or workspace writes.

## Outputs

- Greenfield idea brief:
- Selected direction:
- First vertical slice:
- Acceptance scenarios:
- Metrics:
- Docs/tooling decision:
- Approval boundary:
- Next smallest artifact:

## Scenario Handoff

Keep the handoff concise enough for the next role to act without reading raw conversation history.

- Sources/context used:
- Assumptions:
- Files touched:
- Files proposed:
- Verification evidence:
- Open risks:
- Recommended next role:
- Stop reason:

## Lightweight Mode

Use lightweight mode when the idea is small, personal, throwaway, or the user explicitly asks to stay fast.

- Keep one problem statement.
- Keep one user or actor.
- Keep one selected direction.
- Keep one first vertical slice.
- Keep one acceptance scenario.
- Keep one metric or success signal.
- Keep the approval boundary explicit.

## Verification

- The workflow names problem, users, options, selected direction and non-goals.
- The workflow names first vertical slice, acceptance scenarios, metrics and docs/tooling decision.
- The first response proposes the next smallest artifact instead of dumping every methodology gate.
- Safety phrase: do not scaffold before selected direction, first vertical slice and approval boundary are explicit.

## Stop Conditions

- The problem, user, or selected direction is too unclear to define a first slice.
- Approval for scaffold or workspace writes is missing.
- The requested scaffold needs external accounts, production systems, secrets, billing, hosted docs, CI or package publication.
- The user asks to skip all requirements and approval gates.
