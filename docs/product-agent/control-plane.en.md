# Control-plane files

Source status: `official + experiment`  
Sources: [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [AGENTS.md docs](https://developers.openai.com/codex/guides/agents-md), [AGENTS.md open format](https://agents.md/), [Iterate on difficult problems](https://developers.openai.com/codex/use-cases/iterate-on-difficult-problems).

## Why control-plane files are needed

A long session should not be the only place where requirements and decisions live. Control-plane files make work resumable, reviewable and suitable for skills or automations.

## File set

| File | Purpose | Updated when |
| --- | --- | --- |
| `AGENTS.md` | Durable project rules | A rule must live across work items |
| `REQUIREMENTS.md` | Scope, users, acceptance criteria | Before planning |
| `PLAN.md` | Decomposition, ownership, sequence | Before implementation |
| `TEST.md` | Deterministic checks, manual QA, visual QA | Before review |
| `EVALS.md` | LLM-as-judge, score thresholds, artifacts | For subjective or long-horizon work |
| `RUNLOG.md` | Iterations, scores, decisions, current best | During a long cycle |

## What goes into AGENTS.md

Appropriate content:

- setup commands;
- build/test/lint commands;
- code style;
- security constraints;
- architecture map;
- PR/release rules;
- rules that every agent run must know.

Not appropriate:

- rare long reference material;
- transient work details;
- raw logs;
- secrets;
- policy that belongs in sandbox/approval config.

## Nested AGENTS.md

For a monorepo, use the root `AGENTS.md` for shared rules and nested files for individual packages or services. The nearest instructions should clarify the root policy, not duplicate it.

## Inputs

- Project rules, requirements, plan, tests, evals and run history.
- Current owner decisions, approvals and accepted gaps.

## Outputs

- Durable files that keep the work resumable, reviewable and evidence-backed.
- Clear separation between project rules, transient run history and verification records.

## Verification

Check that control-plane files match the current slice before claiming readiness or closure.

## Risks

- Storing transient logs or secrets in durable files can leak private data.
- Letting memory replace checked-in rules can make future runs inconsistent.
