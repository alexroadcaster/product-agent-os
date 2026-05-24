# Контроль агентов и сессий

Source status: `official + experiment`  
Источники: [Agents SDK sessions](https://openai.github.io/openai-agents-js/guides/sessions/), [OpenAI Agents SDK Python](https://github.com/openai/openai-agents-python), [Codex memories](https://developers.openai.com/codex/memories), [Codex subagents](https://developers.openai.com/codex/subagents).

## Задача session control

Session control нужен, чтобы агент не превращал накопленный диалог в непроверяемую память. Сессия должна сохранять полезную continuity, но не подменять retrieved context, source registry или project rules.

## Session boundary

Каждая сессия должна иметь:

```yaml
session_id: ""
goal: ""
allowed_sources: []
memory_policy: "none | session_only | project_memory"
tool_policy: ""
handoff_policy: ""
freshness_required: true
exit_criteria: []
```

Если goal изменился, лучше создать новую сессию или явно сбросить context.

## Manager pattern как default

Для уменьшения hallucinations используйте Manager pattern:

- Manager держит source policy и final answer.
- Specialist agents выполняют bounded subtasks.
- Verifier agent проверяет claims.
- Только Manager публикует итог пользователю.

Handoff pattern оставляйте для случаев, когда следующий агент должен вести самостоятельный long-running interaction.

## Handoff contract

Минимальный handoff payload:

```yaml
goal: ""
constraints: []
allowed_sources: []
context_summary: ""
verified_claims: []
unsupported_claims: []
open_questions: []
tools_used: []
risks: []
next_agent_task: ""
```

Запрещено передавать handoff без `constraints` и `allowed_sources`: это основной путь к context drift.

## Session hygiene

Правила:

- Перед важным factual answer обновляйте retrieved context.
- После длинной сессии делайте summary с decisions, sources, unresolved questions.
- Не сохраняйте raw chain of thought, secrets и временные догадки.
- Не используйте session memory как citation source.
- При смене topic очищайте irrelevant context.

## Guardrails для сессий

| Guardrail | Trigger | Action |
| --- | --- | --- |
| Missing source | Claim без citation | Отправить в verifier или запросить retrieval |
| Context drift | Ответ опирается на старую assumption | Repack context |
| Tool overreach | Agent просит broad permissions | Запросить granular approval |
| Handoff loss | Payload без constraints | Reject handoff |
| Session bloat | Слишком много нерелевантной history | Summarize and reset |

## Tracing questions

Для каждого agent run фиксируйте:

- Какие sources видел агент?
- Какие tools реально вызваны?
- Какие assumptions выбраны?
- Какие claims проверены?
- Где возник fallback/refusal?
- Какой eval доказывает качество?

