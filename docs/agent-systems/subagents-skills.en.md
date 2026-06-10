# Subagents, skills and AGENTS.md

Source status: `official + experiment`

Subagents handle bounded work with fresh context. Skills encode repeated methods. `AGENTS.md` stores durable project rules. Product-Agent OS keeps these separate so agents do not use memory or generated views as source truth.

## Completion-skeptic Promotion Path

`completion-skeptic` follows the normal repeatable-method chain: manual -> playbook -> skill -> plugin -> automation candidate. Owner review, rollback notes, failure log, eval cases and candidate-only status are required before promotion. A generated handoff or dashboard is not enough.

For documentation and scorecards, owner review is the explicit approval checkpoint.

Automation blockers remain explicit: no active hook, schedule, MCP server, Agents SDK runner, provider call or external write is created until manual evidence, scorecard review and a separate approval packet exist.

## Inputs

- Current user request, project rules, source files and ownership map.
- Candidate skill trigger, inputs, outputs, verification and failure modes.

## Outputs

- Handoff packet for subagents or a skill candidate for a repeated method.
- Durable rule updates only when evidence proves they should persist.

## Verification

Each worker should return sources used, assumptions, files touched, verification evidence, open risks and recommended next role.

## Risks

- Subagents without fresh context can miss project constraints.
- A skill with broad scope can over-trigger and perform unrelated work.
