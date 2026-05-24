# Playbook: build full feature with agents

Source status: `official + experiment`  
Источники: [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/), [Codex workflows](https://developers.openai.com/codex/workflows), [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/).

## Цель

Провести feature от идеи до PR с управляемыми агентными ролями и проверками.

## Procedure

1. Создать `REQUIREMENTS.md`.
2. Попросить Codex подготовить `PLAN.md`, не меняя код.
3. Разделить work по ownership: backend, frontend, tests, docs, release.
4. Запустить builder tasks в отдельных worktrees или с непересекающимися write scopes.
5. Запустить test/review agents.
6. Запустить evals или visual/manual QA.
7. Подготовить PR body и release notes.
8. Перенести повторяемый метод в skill или `AGENTS.md`.

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

