# Prompt & Context Engineering

Source status: `official + experiment`  
Источники: [Prompting](https://developers.openai.com/api/docs/guides/prompting), [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), [Model optimization](https://developers.openai.com/api/docs/guides/model-optimization), [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [OpenAI Cookbook](https://github.com/openai/openai-cookbook).

## Разделение понятий

Prompt engineering отвечает за инструкции: что модель должна сделать, в каком стиле, с какими ограничениями и каким форматом результата.

Context engineering отвечает за рабочую память конкретного вызова: какие факты, документы, цитаты, history, tool outputs и session state модель видит перед ответом.

Для уменьшения hallucinations важнее не "идеальная фраза", а полный контроль контура:

```mermaid
flowchart LR
    Q["Question"] --> P["Prompt contract"]
    C["Retrieved context"] --> P
    M["Memory / session"] --> P
    P --> R["Model response"]
    R --> V["Verifier / guardrail"]
    V -->|Pass| O["Final answer"]
    V -->|Fail| E["Clarify / retrieve more / refuse"]
```

## Prompt как контракт

Хороший prompt должен явно отвечать на восемь вопросов:

| Вопрос | Поле prompt contract |
| --- | --- |
| Кто отвечает? | `Role` |
| Что считается успехом? | `Goal` |
| На чем можно основываться? | `Context` |
| Что запрещено? | `Constraints` |
| Что делать с неизвестным? | `Uncertainty policy` |
| Какие tools можно использовать? | `Tools` |
| Как вернуть результат? | `Output format` |
| Как проверить ответ? | `Verification` |

## Instruction hierarchy

Для API и агентных систем полезно разделять уровни:

- System/developer instructions: стабильная политика, tone, safety, tool rules.
- User task: конкретная задача, данные, цель.
- Retrieved context: факты, документы, outputs tools.
- Examples: компактные few-shot примеры нужного результата.
- Output schema: машинно-проверяемый контракт.

Не кладите transient task details в постоянный system prompt. Не кладите долгосрочную policy в user message, если она должна соблюдаться всегда.

## Оптимизационный цикл

OpenAI model optimization guidance описывает цикл: eval baseline, prompt/context, реалистичные test inputs, измерение, корректировка, повтор. Для этой базы знаний это означает:

1. Сначала определить eval: "ответ должен цитировать source IDs", "не должен выдумывать источник", "должен спросить уточнение при нехватке данных".
2. Затем писать prompt.
3. Проверять на наборах вопросов, похожих на реальные.
4. Версионировать prompt и фиксировать изменения.

## Anti-hallucination baseline

Минимальный baseline для factual tasks:

```text
Answer only from the provided context.
If the context is insufficient, say what is missing.
Do not invent facts, citations, file paths, versions, prices, dates, or line numbers.
Separate verified facts from assumptions.
Return citations for every factual claim when sources are provided.
```

