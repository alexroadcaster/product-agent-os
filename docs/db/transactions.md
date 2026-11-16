# Транзакции, authority и idempotency

Source status: repository_source / static_contract_review; 15.11.2026.; FUNC-G04: locally_verified_with_measured_limits, 16.11.2026.

Владелец: backend/storage owner; область: local SQLite Product-Agent OS, ревизия `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765` (DG03). Обновлять при изменении схемы, контрактов хранения или связанных тестов. Источники: [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts), [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); проверки: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts). Ссылки на тесты не означают их новый запуск; runtime конкретного профиля и пользовательские БД в DG03 не исследовались.

## Worker и очередь

[local-store.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/local-store.mts) открывает dedicated Worker для `DatabaseSync`, принимает только абсолютный не-UNC путь и ограничивает ожидающие запросы числом 100 (`STORAGE_BUSY`). Worker обрабатывает входящие сообщения последовательно. Он включает foreign keys, требует WAL (`WAL_UNAVAILABLE`), задаёт `synchronous=FULL` и `busy_timeout=5000`. Ошибка или остановка worker отклоняет ожидающие вызовы; этот контракт не доказывает безопасную работу нескольких независимых процессов.

## Команда → commit → receipt

[write](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts) проверяет project/actor/idempotency key, число изменений, outbox и размер command, затем выполняет `BEGIN IMMEDIATE`. Для существующей пары `(project_id,idempotency_key)` совпадающий hash возвращает сохранённый receipt; другой hash даёт `IDEMPOTENCY_CONFLICT`. Для новой команды проверяются project, `expectedAuthorityEpoch`, revisions и предметные guards. Изменения entities/связей, запись `commands`, event и outbox выполняются внутри одной транзакции; ошибка откатывает её. Отложенные FK на command разрешают проверку на commit. Receipt подтверждает запись, но не внешнее исполнение outbox.

`legacy_files` блокирует обычную запись task до promotion. Promotion проверяет `writerInventoryVerified`, `restoreRehearsalVerified`, текущую authority, mapping/source digests и другие условия worker; успешный переход увеличивает epoch. Сохранение исходных файлов и проверка внешних писателей зависят от конкретного import workflow и evidence, а не одного SQL-флага. Состояния outbox: `pending`, `acknowledged`, `recovery_required`; ack меняет только pending.

## Сбои и проверка

Разные payload под одним ключом, stale revision/epoch и нарушенные связи отклоняются; повтор с тем же содержимым возвращает receipt. [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [import preview](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/import-preview.test.mts) и [local-store contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts) описывают проверяемые сценарии. Их наличие не гарантирует exactly-once выполнения внешней side effect.

## FUNC-G03 — read snapshots и profile CAS

Новые SQL migrations не добавлены и прежние checksums не изменены. Durable scan и inventory policy используют versioned JSON в profile-owned `store_meta`, expectedVersion CAS и собственные namespaces. Durable registration receipt связывает request digest и project ID в той же registration transaction; повтор после restart не создаёт второй проект.

`projectSnapshot` читает rows и freshness stamp одной read transaction. `runtimeFileScope` так же читает registry/policy и saved task после file I/O: изменившиеся root/policy/task revision запрещают старый preflight. Общий `inventoryScopeFingerprint` проверяется перед source plaintext, cached preview и graph publication; native command повторяет registry fence после dependency/autonomy waits. Изменение policy после уже начавшейся команды не означает отмену совершённого side effect. Regressions policy-race воспроизведены RED и подтверждены GREEN; полный Web594/594,0skip.

## FUNC-G04 — profile CAS и read models

Новые profile-owned namespaces не являются миграцией target DB: project_database_schema_v1 ограничен2MiB (registration/status + два metadata snapshots), project_code_database_v1 —1MiB (source-backed static links/pins). Прежние project_scan_v1 (1MiB) и project_inventory_policy_v1 (32KiB) сохраняют caps. Каждый write проверяет expectedVersion и увеличивает monotonic version; исходные SQL migrations/checksums не менялись. Перед поздним schema/status/diff response повторно проверяются source/version/snapshot identities.

projectEntities/projectSnapshot выбирают consumer kinds до неизменного100k rows/64MiB safety budget; Task Manager дополнительно включает только managed attachments и сохраняет atomic freshness stamp с rows. History SQL TEMP snapshots замораживают membership/values/ordinal, сохраняют старые cursor values после edit/archive и отдают только bounded page. TEMP payload230MiB/mainfile256MiB,100 snapshots/15min expiry/LRU и page100/1MiB ограничивают работу; transient journal/sort disk и native RSS этим не сертифицированы. Cold generation latency остаётся измеренным F20 ограничением.
