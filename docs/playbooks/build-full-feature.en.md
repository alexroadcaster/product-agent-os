# Playbook: build full feature with agents

Source status: `official + experiment`  
Sources: [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/), [Codex workflows](https://developers.openai.com/codex/workflows), [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/).

## Goal

Take a feature from idea to PR with managed agent roles and verification.

## Procedure

1. Clarify requirements and reuse `REQUIREMENTS.md` when it already exists.
2. Ask Codex to prepare `PLAN.md` without changing code.
3. Split work by ownership: backend, frontend, tests, docs, release.
4. Execute focused slices with one agent; delegate independent work only when useful and authorized. Create worktrees only when needed and permitted.
5. Perform testing/review; use a separate agent when risk or independence requirements justify it.
6. Run evals or visual/manual QA.
7. Prepare the PR body and release notes.
8. Move the repeatable method into a skill or `AGENTS.md`.

## Prompt

```text
Build this feature as a product-agent workflow.

Read:
- AGENTS.md
- REQUIREMENTS.md

Before changing files:
- reuse or update the existing plan; create PLAN.md for material multi-step work;
- name ownership boundaries;
- identify required tests and evals;
- list risks and rollback.

During implementation:
- make one focused slice at a time;
- run verification after each meaningful slice;
- update RUNLOG.md.

Final output:
- changed files;
- commands run;
- test/eval result;
- PR summary;
- release notes draft;
- lessons for AGENTS.md or skills.
```

## Acceptance criteria

- Requirements, plan, tests and run log are explicit.
- No agent edits outside its ownership without approval.
- PR summary includes verification evidence.
- Reusable lessons are captured.

## Ordinary change

For a small fix use scope → change → affected checks → result/limits. The full feature workflow above is not a quota for documents or agents. Git/PR/release actions need applicable authority. [Lifecycle routing](../product-agent/lifecycle.md).
