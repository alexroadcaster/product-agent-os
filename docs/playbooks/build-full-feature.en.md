# Playbook: build full feature with agents

Source status: `official + experiment`  
Sources: [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/), [Codex workflows](https://developers.openai.com/codex/workflows), [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/).

## Goal

Take a feature from idea to PR with managed agent roles and verification.

## Procedure

1. Create `REQUIREMENTS.md`.
2. Ask Codex to prepare `PLAN.md` without changing code.
3. Split work by ownership: backend, frontend, tests, docs, release.
4. Run builder tasks in separate worktrees or with non-overlapping write scopes.
5. Run test/review agents.
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
- produce PLAN.md;
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

