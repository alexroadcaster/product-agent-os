# Product lifecycle

Source status: `official + experiment`  
Источники: [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/), [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Iterate on difficult problems](https://developers.openai.com/codex/use-cases/iterate-on-difficult-problems), [Codex workflows](https://developers.openai.com/codex/workflows).

## End-to-end loop

| Stage | Agent work | Artifact | Gate |
| --- | --- | --- | --- |
| Idea | Clarify user value, hypothesis, metric and constraints | `REQUIREMENTS.md` | Scope and success metric are explicit |
| Spec | Turn idea into behavior and acceptance criteria | `REQUIREMENTS.md` | User intent and source-of-truth docs are locked |
| Plan | Decompose work, architecture boundary and ownership | `PLAN.md` | Tasks are independent enough |
| Build | Implement one focused slice at a time | Diff | Test-first or eval-first path exists |
| Eval | Score deterministic, subjective and AI quality | `TEST.md`, `EVALS.md`, reports | Threshold met or gap accepted |
| Review | Find bugs, security risks, test gaps | Review findings | No unresolved blocker |
| PR | Prepare branch, PR body, docs impact and release notes | PR / changelog | Verification evidence included |
| Learn | Capture reusable method | `AGENTS.md`, skill, insight | Next run improves |

## Ask Mode before Code Mode

OpenAI's Codex guidance recommends starting large changes with a plan before implementation. In this project, that means:

```text
First produce PLAN.md from REQUIREMENTS.md.
Do not edit product code until the plan names:
- files or subsystems;
- acceptance criteria;
- verification commands;
- risks and rollback;
- what is out of scope.
```

## Work granularity

Good Codex tasks are scoped enough that a human could complete them in a focused block. If a task spans product, design, backend, frontend, tests, docs and release at once, split it into lifecycle stages and use control-plane files as the handoff.

## Learning loop

Every finished product-agent workflow should answer:

- Which instructions should move into `AGENTS.md`?
- Which repeated steps deserve a skill?
- Which check should become an automation?
- Which failure needs an eval?
- Which source or architecture decision should be documented?
- Which metric or user feedback should drive the next product iteration?
