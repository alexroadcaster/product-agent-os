# Контроль агентов и сессий

Source status: `official + experiment`  
Источники: [Agents SDK sessions](https://openai.github.io/openai-agents-js/guides/sessions/), [OpenAI Agents SDK Python](https://github.com/openai/openai-agents-python), [Codex memories](https://developers.openai.com/codex/memories), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

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

При уточнении goal сохраните релевантный контекст и ограничения; для несовместимой новой цели явно определите границу сессии. См. steering и compaction ниже.

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
| Session bloat | Слишком много нерелевантной history | Summarize or compact; reset only with an explicit boundary |

## Tracing questions

Для каждого agent run фиксируйте:

- Какие sources видел агент?
- Какие tools реально вызваны?
- Какие assumptions выбраны?
- Какие claims проверены?
- Где возник fallback/refusal?
- Какой eval доказывает качество?

## Async tools и steering

Проверено 2026-11-03: [Async tool calling](https://developers.openai.com/api/docs/guides/async-tool-calling), [Steering](https://developers.openai.com/api/docs/guides/steering). Это описанные API-возможности, а не новая активация Product-Agent OS.

`async: true` поддерживаемого function/custom tool позволяет модели продолжать независимую работу, пока приложение исполняет tool. OpenAI не берет исполнение этого tool на себя. Возвращайте output с исходным `call_id`; async не является Background mode и не применяется автоматически к hosted tools или Programmatic Tool Calling.

| Состояние | Обязанность приложения / проектируемый контракт |
| --- | --- |
| Pending | Сохранить call_id, owner, deadline, разрешенные side effects; не объявлять зависимый результат готовым |
| Completed | Сопоставить output с вызовом и применить результат один раз |
| Failed / timeout | Вернуть явный failure, определить retry по idempotency и бюджету |
| Duplicate / late | Проверить идентичность, актуальность задачи и факт предыдущего применения; не повторять side effect |

Для mid-turn steering Responses WebSocket использует `response.steer`. Подтверждение очереди означает accepted, но не applied. Следите за продолжением response и причиной `steered`; не считайте обновление обработанным до соответствующего evidence. Steering не отменяет завершенные действия или уже запущенные tools. Перед следующим side effect приложение сверяет обновленный scope и pending calls. Финал возможен, когда обязательные зависимости завершены либо их отсутствие явно отражено в результате.

## Reasoning updates и compaction

Источники: [Reasoning](https://developers.openai.com/api/docs/guides/reasoning), [Compaction](https://developers.openai.com/api/docs/guides/compaction). В поддерживаемом standard single-agent GPT-6 Responses conversation `configuration_update` может менять effort между ответами, сохраняя request-level `reasoning.effort` и исходный prefix. Изменение действует до следующего update; response-level effort может отражать исходную настройку, а не applied update.

| Механизм | Совместимость / действие |
| --- | --- |
| `configuration_update` | Поддерживаемый single-agent режим; не считать общим для всех runtimes |
| Automatic compaction/truncation | Не сочетать с configuration updates |
| Standalone `/responses/compact` | Отклоняет history с configuration updates |
| Explicit `compaction_trigger` | После compaction заново добавить update перед следующим user message, восстановив все измененные settings |
| Server-side compaction | `context_management` и `compact_threshold`; opaque encrypted item, не обычный summary |

Уточнение задачи не требует автоматического reset. Сохраняйте цель, ограничения, решения и незавершенные calls; новую сессию выбирайте при необходимости независимого scope или свежей загрузки settings. Compaction, ручной summary и межсессионная memory имеют разные контракты. Для manual history сохраняйте возвращенные state items и требуемые поля; не запрашивайте private chain-of-thought.
