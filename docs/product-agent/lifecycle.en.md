# Product lifecycle

Source status: `official + experiment`  
Sources: [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/), [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Iterate on difficult problems](https://developers.openai.com/codex/use-cases/iterate-on-difficult-problems), [Codex workflows](https://developers.openai.com/codex/workflows).

## End-to-end loop

| Stage | Agent work | Artifact | Gate |
| --- | --- | --- | --- |
| Idea | Clarify user value, hypothesis, metric and constraints | `REQUIREMENTS.md` | Scope and success metric are explicit |
| Spec | Turn the idea into behavior and acceptance criteria | `REQUIREMENTS.md` | User intent and source-of-truth docs are locked |
| Plan | Decompose work, architecture boundary and ownership | `PLAN.md` | Work items are independent enough |
| Build | Implement one focused slice at a time | Diff | Test-first or eval-first path exists |
| Eval | Score deterministic, subjective and AI quality | `TEST.md`, `EVALS.md`, reports | Threshold met or gap accepted |
| Review | Find bugs, security risks and test gaps | Review findings | No unresolved blocker |
| PR | Prepare branch, PR body, docs impact and release notes | PR / changelog | Verification evidence included |
| Learn | Capture the reusable method | `AGENTS.md`, skill, insight | Next run improves |

## Plan before implementation

OpenAI Codex guidance recommends starting large changes with a plan before implementation. In this project, that means:

```text
First produce PLAN.md from REQUIREMENTS.md.
Do not edit product code until the plan names:
- files or subsystems;
- acceptance criteria;
- verification commands;
- risks and rollback;
- what is out of scope.
```

## Start brief hook guard

For Product-Agent OS non-mechanical work, the start brief is now backed by a staged hook mechanism:

- the lifecycle contract lives in `.codex/config.toml` and `.codex/workflows/task-plan-lifecycle.md`;
- packaged hook templates live in `plugins/product-agent-os/assets/templates/hooks/`;
- the `PreToolUse` hook blocks mutating or non-read-only commands when `.codex/product-agent-os/lifecycle-state.json` has not been created after the user-visible start brief;
- the `Stop` hook reminds the agent to show a completion brief and run control-plane sync when scope, plan, tests, evals, runlog, or evidence state changed.

This is a guardrail, not proof by itself. Completion and readiness claims still require current command, runtime, or eval evidence, or an explicit accepted gap.

## Work granularity

Good Codex work is scoped enough that a human could complete it in a focused block. If one request spans product, design, backend, frontend, tests, docs and release, split it into lifecycle stages and use control-plane files as the handoff.

## Learning loop

Every finished product-agent workflow should answer:

- Which instructions should move into `AGENTS.md`?
- Which repeated steps deserve a skill?
- Which check should become an automation?
- Which failure needs an eval?
- Which source or architecture decision should be documented?
- Which metric or user feedback should drive the next product iteration?

## Inputs

- Product goal, requirements, source context and project constraints.
- Existing control-plane files and verification commands.

## Outputs

- A staged lifecycle path from idea to review, release packet and learning.
- Updated durable rules, skills or evals when the evidence justifies promotion.

## Risks

- Moving to build before plan and ownership can create broad, unverifiable changes.
- Capturing learning without source evidence can turn stale memory into policy.

## Scope size determines the route

Checked 2026-11-05: [model guidance](https://developers.openai.com/api/docs/guides/latest-model) and [eval guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices). For an ordinary fix use concise scope, the change, affected checks, results and limits. Reuse existing requirements/plan/test/runlog artifacts; do not create a new file set merely to name each phase. The full route above is for large, risky or financially material implementation and release/readiness.

Product-Agent OS uses `task_start_brief_v2` (9 fields) and Completion Ledger (13 items) for full scopes; ordinary scopes use `task_scope_note_v1` and a concise result. Legacy v1 remains for previously started sessions only. Advisory `Stop` does not validate chat. The [lifecycle hooks guide](../runtime/worktrees-hooks-rules.md) defines applicability and markers.

Single-agent is a sufficient starting point. Delegate independent work with explicit ownership, a budget and demonstrated value. PR preparation does not authorize creating branches, publishing a PR or releasing. Repeat checks after a relevant change, failure or unresolved risk, not in an unbounded general-gate loop.
