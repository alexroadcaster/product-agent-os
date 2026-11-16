# События, replay и история

Source status: repository_source / static_contract_inventory; 15.11.2026.

Владелец: local-service/API и storage; scope/version: DG03, commit `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Обновлять при изменении событий, retention, cursor или runtime adapter. [API](index.md), [backend flow](../backend/commands-events.md).

## HTTP replay и audit

`GET /api/v1/projects/{projectId}/events?cursor=...` и `/history?cursor=...` возвращают JSON `{generation, items, hasMore, nextCursor}`. [StoreEventPage](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts) определяет item `{seq, eventId, actorId, occurredAt, payload}`. Cursor кодирует projectId/generation/seq и подписан HMAC случайным секретом экземпляра; устаревший, повреждённый или предназначенный другому project cursor должен быть обработан как отказ. Повторное создание экземпляра не гарантирует сохранение cursor.

`events` — replay с retention; `history` — отдельный immutable task audit, его сохранность не ограничивается replay retention. Это JSON polling; обработчик не объявляет `text/event-stream` или SSE endpoint. Прежние проектные документы с предложением SSE — историческая архитектура, не подтверждение такого текущего HTTP route.

Для сущностей `/entities` используются `limit` (1–100, default 50) и `offset`; `/search` использует `offset` и лимит 50. Session history использует отдельный scoped snapshot cursor со сроком 15 минут; graph cursor привязан к revision и filters; не подменяйте эти cursor друг другом. [Session history](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/sessions/service.mts), [graph service](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/code-index/service.mts).

## Runtime events и authority

[RuntimeEvent](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/runtime/events.ts) различает `turn_accepted`, `turn_started`, `turn_ended`, `approval_requested`, `request_resolved`, `item_ended`, `non_lifecycle`, `recovery_required`; полные поля и допустимые исходы определяет тип. `turn_accepted` — подтверждение dispatch, не успешное завершение turn. Runtime state возвращает snapshot; отдельный закрытый `/agent/v1` канал использует lease и capability, а не browser cookie.

Write transaction связывает изменения, receipts, events и outbox согласно [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts). Не все runtime события являются owner acceptance и не следует обещать доставку/streaming вне проверенного контракта. [Service API tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/service-api.test.mts), [runtime events test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-events.test.mts); ссылки не означают новый прогон. Примеры и результаты других запусков следует оценивать с их provenance.

## FUNC-18 — stamp вместо полного snapshot polling

Project freshness endpoint не является SSE, filesystem watcher или новым event stream. Он сравнивает generation/throughSeq с scan/policy versions; baseline приходит атомарно вместе с task-manager rows. Изменение задачи или scheduler entry через другой разрешённый канал делает прежний UI snapshot stale. Неизвестная свежесть показана отдельно от fresh; explicit refresh не перезаписывает dirty draft. Детали — [состояние frontend](../frontend/state-management.md#func-18--свежесть-снимков-и-сохранность-редактора).
