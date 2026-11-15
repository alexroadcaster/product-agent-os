# Миграции и совместимость

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: backend/storage owner; область: local SQLite Product-Agent OS, ревизия `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765` (DG03). Обновлять при изменении схемы, контрактов хранения или связанных тестов. Источники: [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts), [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); проверки: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts). Ссылки на тесты не означают их новый запуск; runtime конкретного профиля и пользовательские БД в DG03 не исследовались.

## Версии и fences

| Версия | Добавление и проверка | Результат |
| --- | --- | --- |
| 1 | Базовый DDL; SHA-256 исходной строки schema = `MIGRATION_CHECKSUM` | `paos-m1-v1` |
| 2 | Лениво, в бизнес-транзакции: `task_manager_capabilities` и `task_profile=m2_task_profile_v1`; `M2_MIGRATION_CHECKSUM` | `paos-m2-v1` |
| 3 | Лениво, в той же транзакции: `workflow_registry=m2b_workflow_registry_v1`; `M2B_MIGRATION_CHECKSUM` | `paos-m2b-v1` |

`schema_migrations` хранит version, checksum, applied_at и app_compatibility. `databaseCompatibility` допускает ровно последовательности 1, 1–2, 1–3 с известными checksum и нужными маркерами. Неизвестная/изменённая миграция, отсутствующий marker или посторонняя непустая БД без истории отклоняются `SCHEMA_INCOMPATIBLE`. Первичное создание и вставка stream/index generation в `store_meta` выполняются в `BEGIN IMMEDIATE`; ошибка откатывается.

`ensureM2Schema`/`ensureM2BSchema` выполняются внутри бизнес-транзакции: отклонённая первая команда не оставляет fence новой версии. Исправление исходного SQL без стратегии совместимости меняет checksum; не редактировать исторический DDL как обычный migration patch. Это описание source, не инструкция запускать миграцию на пользовательском профиле.

Проверки: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [domain migration tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/domain-migration.test.mts), [snapshot validation](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/snapshot.mts). Датированные результаты и новые проверки должны сохранять provenance.
