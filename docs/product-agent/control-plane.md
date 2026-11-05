# Control-plane files

Source status: `official + experiment`  
Источники: [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [AGENTS.md docs](https://developers.openai.com/codex/guides/agents-md), [AGENTS.md open format](https://agents.md/), [Iterate на difficult problems](https://developers.openai.com/codex/use-cases/iterate-on-difficult-problems).

## Почему нужны control-plane files

Длинная сессия не должна быть единственным местом, где живут требования и решения. Control-plane files делают работу resumable, reviewable и пригодной для skills/automations.

## Набор файлов

| Файл | Назначение | Обновляется |
| --- | --- | --- |
| `AGENTS.md` | Постоянные правила проекта | Когда правило должно жить между задачами |
| `REQUIREMENTS.md` | Scope, users, acceptance criteria | Перед планированием |
| `PLAN.md` | Decomposition, ownership, sequence | До implementation |
| `TEST.md` | Deterministic checks, manual QA, visual QA | До review |
| `EVALS.md` | LLM-as-judge, score thresholds, artifacts | Для subjective/long-horizon задач |
| `RUNLOG.md` | Iterations, scores, decisions, текущий best | Во время длинного цикла |

## Что идет в AGENTS.md

Подходит:

- setup commands;
- build/test/lint commands;
- code style;
- security constraints;
- architecture map;
- PR/release rules;
- rules который every agent запуск должен know.

Не подходит:

- редкие длинные справочники;
- transient task details;
- raw logs;
- secrets;
- policy, которая должна жить в sandbox/approval config.

## Nested AGENTS.md

Для monorepo используйте root `AGENTS.md` для общих правил и nested files для отдельных packages или services. Ближайшие инструкции должны уточнять, а не дублировать root policy.

## Применимость и загрузка

Для небольшой задачи переиспользуйте existing artifacts. `AGENTS.md` загружается по [discovery rules](https://learn.chatgpt.com/docs/agent-configuration/agents-md); остальные файлы читаются по task/reference, а не автоматически. Проверка свежей сессии нужна для claim о loading, не для каждой текстовой правки.
