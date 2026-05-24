# Evals и observability

Source status: `official + experiment`
Источники: [OpenAI Agents SDK Python](https://github.com/openai/openai-agents-python), [Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses), [Codex workflows](https://developers.openai.com/codex/workflows).

## Зачем это в базе Codex

Продвинутый Codex workflow должен проверяться не только тестами проекта. Для агентных систем нужны отдельные quality gates:

- source fidelity;
- task completion;
- tool correctness;
- safety policy adherence;
- handoff completeness;
- regression stability.

## Guardrails

Guardrails в Agents SDK используются для проверки inputs и outputs. В документационном проекте guardrail можно описывать как проверяемое правило:

| Guardrail | Проверка |
| --- | --- |
| Official-source fidelity | Каждый factual claim имеет official source или статус `community/experiment` |
| No secret retention | Docs, insights и memory не содержат secrets |
| Handoff completeness | Handoff payload содержит goal, constraints, sources, claims, risks |
| Tool boundary | Tool call не выходит за sandbox/approval policy |
| Structured output | Agent возвращает JSON/YAML по контракту, если это требуется |

## Tracing

Tracing нужен для debugging и monitoring агентных приложений: какие agents вызывались, какие tools использовались, где была задержка, где возник failure.

Для Codex-документации tracing-эквивалентом является evidence trail:

```yaml
task: "Update memory docs"
sources:
  - "https://developers.openai.com/codex/memories"
  - "https://openai.github.io/openai-agents-js/guides/sessions/"
decisions:
  - "AGENTS.md is mandatory policy; memories are recall layer."
checks:
  - "python tools/check_docs.py"
  - "python -m mkdocs build --strict"
result: "accepted | needs_review | rejected"
```

## Evals для базы знаний

Минимальный eval suite:

| Eval | Prompt | Pass condition |
| --- | --- | --- |
| Source audit | "Проверь раздел на claims без источников" | Нет unsupported official claims |
| Navigation | "Найди путь от Codex App к multi-agent playbook" | Путь проходит через overview -> surfaces -> agent systems -> playbook |
| Insight separation | "Найди community tricks в core docs" | Community claims есть только с явным статусом |
| Handoff quality | "Оцени handoff contract" | Есть goal, constraints, sources, claims, risks |
| Build health | `python tools/check_docs.py` + MkDocs build | Оба проходят |

## Long-horizon improvement loop

Для сложных product tasks используйте цикл:

1. Run baseline eval.
2. Identify one bottleneck.
3. Make one focused change.
4. Re-run deterministic checks and LLM-as-judge.
5. Inspect artifact directly when output is visual or subjective.
6. Log score and decision in `RUNLOG.md`.
7. Continue until explicit thresholds are met.

Не меняйте несколько независимых вещей за одну итерацию: иначе нельзя понять, что улучшило score.

## LLM-as-judge + deterministic checks

| Слой | Что доказывает | Что не доказывает |
| --- | --- | --- |
| Deterministic checks | Code compiles, links exist, schema passes | UX quality, usefulness, semantic correctness |
| LLM-as-judge | Rubric-based quality, clarity, relevance | Security correctness by itself |
| Artifact inspection | Real generated output matches intent | No hidden regression elsewhere |
| Human review | Product fit and risk judgment | Repeatability without evals |

## Failure taxonomy

| Failure | Симптом | Исправление |
| --- | --- | --- |
| Source drift | Официальная страница изменилась, docs устарели | Обновить source card и affected sections |
| Context rot | Agent использует старые assumptions | Переоткрыть sources и сократить memory reliance |
| Handoff loss | Worker теряет constraints | Ввести structured handoff schema |
| Tool overreach | Agent просит слишком широкие permissions | Ужесточить approval policy |
| Eval blind spot | Build проходит, но качество слабое | Добавить scenario eval |
