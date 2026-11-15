# Backend: команды, события и outbox

Source status: repository_source / static_source_review; 15.11.2026.

Владелец: backend и storage; scope/version: DG03, `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Обновлять при изменении command, revision, event, outbox или cursor contract.

## От запроса к durable receipt

[application.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts) авторизует локальный запрос и передаёт domain service нормализованный ввод. Domain command использует [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts): `projectId`, `actorId`, `idempotencyKey`, `expectedAuthorityEpoch` и изменения с `expectedRevision`. Это форма storage contract, не универсальное тело каждого HTTP endpoint: актуальные request/response перечислены в [API](../api/endpoints.md).

[local-store.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/local-store.mts) связывает каждый RPC с ответом Worker. [sqlite-worker.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts) выполняет запись внутри `BEGIN IMMEDIATE`: проверяет повтор ключа и hash payload, project authority epoch и ревизии; затем применяет изменения и сохраняет command receipt, project sequence event и при наличии outbox jobs в одной транзакции. Исключение откатывает транзакцию. Повтор того же project/key и payload возвращает сохранённый receipt; другой payload с тем же ключом даёт `IDEMPOTENCY_CONFLICT`. Это свойство записи команды, не доказательство exactly-once выполнения произвольного внешнего действия.

## Порядок и чтение

Receipt содержит `commandId`, `projectId`, `seq` и revisions. Events доступны по project sequence; клиентский cursor также несёт generation, поэтому reset/restore и истёкшая история требуют отдельной обработки, а не слепого продолжения старого cursor. Outbox job создаётся в состоянии `pending` и может быть отмечен `acknowledged`; сам факт сохранения outbox не доказывает доставку или завершение внешней операции. Search index jobs обрабатываются после command transaction с отдельными проверками revision. См. [события API](../api/events.md) и [данные](../db/transactions.md).

## Очереди и ошибки

Worker ограничивает pending запросы числом 100 и возвращает `STORAGE_BUSY`; закрытие даёт `STORAGE_CLOSED`. Scheduler и recipe service имеют отдельные serial queues, но несвязанные запросы и runtime gateway нельзя считать одной глобальной очередью. Scheduler проверяет frozen preview, revision, authority и workspace ownership; повторный idempotency key с другим вводом конфликтует. Часть отказов — `REVISION_CONFLICT`, `AUTHORITY_CONFLICT`, `QUEUE_PREVIEW_STALE` — означает необходимость заново получить состояние, а не автоматически повторить потенциально изменяющую операцию. Конкретное HTTP mapping — [errors](../api/errors.md).

## Проверки и ограничения

Связанные тесты [runtime-sqlite.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-sqlite.test.mts), [scheduler-runtime.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/scheduler-runtime.test.mts), [runtime-events.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-events.test.mts); ссылки не означают, что они запускались в этом изменении. Внешние потребители outbox, доставка и текущие runtime результаты здесь не подтверждены.
