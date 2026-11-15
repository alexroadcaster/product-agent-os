# SQLite Product-Agent OS

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: backend/storage owner; область: local SQLite Product-Agent OS, ревизия `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765` (DG03). Обновлять при изменении схемы, контрактов хранения или связанных тестов. Источники: [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts), [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); проверки: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts). Ссылки на тесты не означают их новый запуск; runtime конкретного профиля и пользовательские БД в DG03 не исследовались.

Локальное хранилище принадлежит профилю PAOS, а не подключённому проекту. [Schema](schema.md) содержит полный SQL; [ERD](erd.md) ведёт к редактируемой схеме. [Миграции](migrations.md), [транзакции](transactions.md), [backup/restore](backup-restore.md), [поиск](search-index.md) описывают соседние контракты.

## Authority и границы

`projects.authority_mode` различает `legacy_files` и `sql`; `authority_epoch` защищает команды от устаревшей authority. Исходники и документация остаются файлами. SQL владеет допустимыми operational entities после проверенного cutover, а не всем workspace; до cutover task нельзя незаметно записать в SQL как primary source. См. [решение W03](../architecture/decisions/adr-w03-storage-authority.md) и [транзакции](transactions.md).

[F33/F34](../planning/functional-remediation-2026-11-15.md) предусматривают отдельную карту target DB и связи кода с таблицами; текущая PAOS SQLite не предоставляет их. Team PostgreSQL/pgvector M5 остаётся planned. Эта схема описывает source ревизии, а не чужую БД или production readiness.
