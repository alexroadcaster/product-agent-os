# Playbook: build full feature with agents

Source status: `official + experiment`  
Источники: [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/), [Codex workflows](https://developers.openai.com/codex/workflows), [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/).

## Цель

Провести feature от идеи до PR с управляемыми агентными ролями и проверками.

## Procedure

1. Уточнить требования и переиспользовать `REQUIREMENTS.md`, если файл уже есть.
2. Попросить Codex подготовить `PLAN.md`, не меняя код.
3. Разделить work по ownership: backend, frontend, tests, docs, release.
4. Выполнять focused slices одним агентом; независимые задачи делегировать только при пользе и authority. Worktrees создавать только при необходимости и разрешении.
5. Выполнить test/review; отдельный агент нужен по риску или требованию независимости.
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

## Критерии приемки

- Requirements, plan, tests and run log are explicit.
- No agent edits outside its ownership without approval.
- PR summary includes verification evidence.
- Reusable lessons are captured.

## Обычная правка

Для небольшого исправления используйте scope → change → affected checks → result/limits. Полный feature workflow выше не является квотой на документы или агентов. Git/PR/release действия требуют применимого разрешения. [Lifecycle routing](../product-agent/lifecycle.md).
