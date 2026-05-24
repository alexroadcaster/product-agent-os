# Playbook: Context7 deep research

Source status: `official + experiment`
Источники: [Context7 results for OpenAI docs](../sources/context7-research.md), [Source registry](../sources/registry.md).

## Цель

Использовать Context7 как быстрый retrieval layer для расширения базы знаний, но сохранять official-source discipline.

## Процедура

1. Сформулировать research question как список capabilities, а не как общий запрос.
2. Resolve library ID для каждой библиотеки.
3. Query docs не более чем по трем самым важным направлениям за один проход.
4. Разделить результаты на:
   - official facts;
   - examples/recipes;
   - architecture implications;
   - claims that need direct source verification.
5. Добавить или обновить source cards.
6. Внести изменения в docs.
7. Запустить проверки.

## Хороший запрос

```text
Extract authoritative design details for the OpenAI Agents SDK:
Agent, Runner, tools, handoffs, guardrails, sessions, tracing,
context, multi-agent orchestration, and recommended architecture patterns.
Focus on concepts useful for documenting multi-agent systems with memory.
```

## Плохой запрос

```text
Tell me everything about agents.
```

Он слишком широкий: результат будет трудно проверить и перенести в source registry.

## Output contract

```yaml
context7_libraries:
  - library_id: ""
    source_reputation: "High | Medium | Low"
findings:
  - claim: ""
    source_url: ""
    target_doc: ""
    action: "add | update | reject | verify_directly"
risks:
  - ""
verification:
  - "python tools/check_docs.py"
  - "python -m mkdocs build --strict"
```

