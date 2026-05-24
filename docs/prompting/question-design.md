# Проектирование вопросов к GPT-моделям

Source status: `official + experiment`  
Источники: [Prompting](https://developers.openai.com/api/docs/guides/prompting), [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), [OpenAI Cookbook](https://github.com/openai/openai-cookbook).

## Формула хорошего вопроса

Плохой вопрос:

```text
Расскажи про agents.
```

Хороший вопрос:

```text
Goal: Спроектировать multi-agent research workflow для обновления документации Codex.
Audience: Advanced agent builder.
Context: Используй только перечисленные источники и текущую структуру docs.
Constraints: Не смешивай official и community claims.
Output: Верни architecture, roles, handoff contract, evals, risks.
Uncertainty: Если источника не хватает, пометь claim как needs_source.
Verification: Укажи, какие docs/checks нужно обновить.
```

## Prompt packet

Используйте этот пакет как default:

```text
# Role
You are ...

# Goal
...

# Context
<source id="S1">
...
</source>

# Constraints
- ...

# Unknowns and assumptions
- Ask a clarifying question if ...
- Otherwise assume ...

# Tools
- Use ... only when ...

# Output format
...

# Verification
...
```

## Правила конкретности

| Вместо | Пишите |
| --- | --- |
| "Сделай лучше" | "Сократи до 800 слов, сохрани citations, добавь failure modes" |
| "Проанализируй" | "Найди contradictions, unsupported claims, missing tests" |
| "Объясни подробно" | "Дай mental model, workflow, examples, pitfalls" |
| "Не галлюцинируй" | "Если claim не подтвержден context, пометь `needs_source`" |
| "Ответь JSON" | "Верни JSON по схеме, при нехватке данных используй empty array и `missing_context`" |

## Когда задавать уточняющий вопрос

Модель должна уточнять, если:

- задача имеет несколько несовместимых трактовок;
- отсутствует критичный input;
- действие может быть опасным или дорогим;
- результат зависит от свежих фактов, а tools недоступны;
- user intent важнее repo facts.

Если ambiguity не блокирует работу, лучше явно выбрать assumption:

```text
Assumption: Под "agents" я понимаю OpenAI Agents SDK, а не general AI agents.
```

## Few-shot examples

Few-shot нужен, когда важно не только "что", но и "как выглядит хороший ответ". Держите примеры короткими:

```yaml
examples:
  - input: "Проверь claim: Codex сам запускает subagents."
    output:
      status: "rejected"
      reason: "Official docs require explicit user request for subagents."
      source: "https://developers.openai.com/codex/subagents"
  - input: "Проверь claim: Structured Outputs решают все hallucinations."
    output:
      status: "qualified"
      reason: "They constrain shape, but factual mistakes remain possible."
      source: "https://developers.openai.com/api/docs/guides/structured-outputs"
```

## Checklist перед отправкой

- Есть конкретный outcome?
- Есть список допустимых источников?
- Есть запрет на неподтвержденные факты?
- Есть формат вывода?
- Есть правило для uncertainty?
- Есть критерий проверки?

