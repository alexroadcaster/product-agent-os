# Playbook: grounded answering

Source status: `official + experiment`  
Источники: [Prompting](https://developers.openai.com/api/docs/guides/prompting), [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [Model optimization](https://developers.openai.com/api/docs/guides/model-optimization), [OpenAI Cookbook](https://github.com/openai/openai-cookbook).

## Цель

Дать ответ GPT-моделью с минимальным риском hallucinations: retrieve, constrain, answer, cite, verify, escalate uncertainty.

## Procedure

1. Определите тип вопроса: factual, design, coding, current data, opinion.
2. Соберите context из разрешенных источников.
3. Упакуйте context с source IDs.
4. Сформулируйте prompt contract.
5. Потребуйте citations или structured output.
6. Пропустите ответ через verifier.
7. Если context недостаточен, верните missing context вместо догадки.

## Prompt

```text
# Role
You are a grounded answer generator.

# Goal
Answer the user question using only the provided sources.

# Context
<source id="S1" type="official" url="...">
...
</source>

# Rules
- Every factual claim must cite a source ID.
- If a claim is not supported, put it in unsupported_claims.
- If sources conflict, describe the conflict.
- If context is insufficient, do not guess.

# Output
Return:
- answer
- citations
- assumptions
- unsupported_claims
- missing_context
- confidence: high | medium | low
```

## Verifier prompt

```text
Check the answer against the provided sources.

For each factual claim:
- supported
- unsupported
- contradicted
- needs_fresh_check

Return verdict: pass | fail | needs_more_context.
```

## Acceptance criteria

- Нет factual claims без citation.
- Нет invented source IDs.
- Missing context явно назван.
- Если confidence ниже high, ответ объясняет почему.
- Для текущих фактов выполнена fresh verification или указана невозможность проверки.

