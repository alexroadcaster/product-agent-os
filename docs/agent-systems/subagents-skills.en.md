# Subagents, skills and AGENTS.md

Source status: `official + experiment`

Subagents handle bounded work with fresh context. Skills encode repeated methods. `AGENTS.md` stores durable project rules. Product-Agent OS keeps these separate so agents do not use memory or generated views as source truth.

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
