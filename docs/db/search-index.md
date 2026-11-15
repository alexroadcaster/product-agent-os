# Поиск и индекс

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: backend/storage owner; область: local SQLite Product-Agent OS, ревизия `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765` (DG03). Обновлять при изменении схемы, контрактов хранения или связанных тестов. Источники: [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts), [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); проверки: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts). Ссылки на тесты не означают их новый запуск; runtime конкретного профиля и пользовательские БД в DG03 не исследовались.

## Индексация

`search_fts` — FTS5 с `title`, `body`, `unicode61`, prefix `2 3`. [Worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts) поддерживает `indexed_documents` с project/entity/revision/generation и rowid, соответствующим FTS rowid. Это соответствие реализовано запросами, а не FK. Записи только допустимых видов; текст свыше 1 MiB не индексируется. Scope token и path token вычисляются через SHA-256 для разделения проектов и точного пути; это не механизм шифрования базы.

## Чтение и покрытие

Сначала проверяются точный entity ID/public key, затем точный относительный путь документа, затем FTS: [RANKED_SEARCH_SQL](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/search-queries.mts) связывает FTS с живой entity соответствующей revision и проектом; значения bind-параметризованы. Итог включает `coverage` и generation. `complete` требует совпадения eligible/indexed counts, отсутствия incomplete, pending jobs, наличия FTS и текущего формата; иначе `partial`. Выдача с partial не доказывает отсутствие результатов.

Индекс — производный от бизнес-состояния: worker сначала фиксирует бизнес-транзакцию, затем в отдельной транзакции обрабатывает durable `index_jobs`. Ошибка refresh не откатывает уже принятый receipt; job и partial coverage остаются для rebuild/retry. Поэтому receipt не доказывает обновление индекса.

## Rebuild и ограничения

`rebuildSearch` выполняется транзакционно: увеличивает generation, переиндексирует entities, сообщает progress и удаляет jobs после завершения. Abort через shared buffer приводит к `INDEX_REBUILD_CANCELLED` и rollback. Восстановление/изменение индекса не означает семантический поиск или production RAG: это локальный SQLite FTS, а граф целевого проекта и PoC F30–F34 принадлежат [функциональному плану](../planning/functional-remediation-2026-11-15.md).

Проверки: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [UI stream/search tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/ui-stream-search.test.mts); [контракт результатов](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts). См. [backup/restore](backup-restore.md) для generation и stale cursors другого назначения: stream generation не следует смешивать с index generation.
