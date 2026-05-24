# Playbook: multi-agent research loop

Source status: `official + experiment`  
Источники: [Codex subagents](https://developers.openai.com/codex/concepts/subagents), [Codex workflows](https://developers.openai.com/codex/workflows), [Agent Skills](https://developers.openai.com/codex/skills).

## Цель

Создать управляемый research loop для обновления базы знаний: поиск источников, отделение официальных фактов от community signals, проверка claims и выпуск документационного изменения.

## Когда использовать

- Появился новый Codex changelog entry.
- Нужно добавить раздел по новой возможности.
- Есть community trick, который может быть полезен, но требует проверки.

## Single-agent режим

```text
Исследуй тему "{topic}" для базы знаний Codex.

Сделай:
1. Найди официальные источники OpenAI.
2. Составь source cards.
3. Отдели community claims от official claims.
4. Предложи изменения в docs.
5. Укажи verification commands.
Не смешивай неподтвержденные tricks с официальными инструкциями.
```

## Parallel режим

Используйте только когда явно хотите subagents:

```text
Use parallel subagents for this research task.

Agent 1: official Codex docs.
Agent 2: Agents SDK docs for memory/orchestration.
Agent 3: community insight backlog.

Each agent returns verified claims, uncertain claims, and source cards.
Wait for all agents. Then synthesize one update plan and do not include raw logs.
```

## Acceptance criteria

- Новые official claims имеют source cards.
- Community claims лежат только в `docs/insights/`.
- Каждый proposed edit имеет verification status.
- MkDocs build проходит.

## Context7 enrichment

Когда тема связана с OpenAI SDK, Responses API, Codex или Agents SDK, добавьте отдельный проход по [Context7 deep research](context7-deep-research.md). Его цель - найти SDK-level details: primitives, method contracts, tool types, structured output examples и observability patterns. После retrieval все равно обновляйте source registry, а не вставляйте неподписанные claims напрямую.
