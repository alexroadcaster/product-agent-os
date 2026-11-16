# Snapshot, backup и восстановление

Source status: repository_source / static_contract_review; 15.11.2026.; FUNC-G06_22_current_native_synthetic_verified, 16.11.2026.

Владелец: backend/storage owner; область: local SQLite Product-Agent OS, ревизия `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765` (DG03). Обновлять при изменении схемы, контрактов хранения или связанных тестов. Источники: [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts), [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); проверки: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts). Ссылки на тесты не означают их новый запуск; runtime конкретного профиля и пользовательские БД в DG03 не исследовались.

## Состав и создание

[snapshot.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/snapshot.mts) выполняет `VACUUM INTO` в новом private каталоге через сериализованный Worker; операция включает committed WAL pages. Затем snapshot открывается read-only, проверяются compatibility, `integrity_check` и `foreign_key_check`. В backup попадают доступные по связям с неудалёнными entities blobs: каждый сверяется по ID, размеру и SHA-256. Manifest содержит version/checksum/appCompatibility, hash БД и самого manifest, blob receipts, дату и ID. Исключены `credentials`, `repository_files`, `runtime_threads`, `runtime_auth_store`: backup не полный архив проекта и авторизации.

Результат также возвращает `rotationCandidates` среди проверенных managed backups после первых пяти; наличие кандидата не удаляет файл. `pruneManagedBackups` — отдельный вызов с проверкой immediate parent, списка допустимых и отсутствия `pinned`. Это описание границы, не разрешение на удаление.

## Restore

Отдельный [restore worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/restore-worker.mts) проверяет manifest и compatibility/checksum, hash базы, целостность/FK и полное соответствие blob coverage/размера/hash; source не должен быть symlink. Копирование создаёт только новый абсолютный не-UNC путь (`COPYFILE_EXCL`): `RESTORE_DESTINATION_EXISTS` не перезаписывает профиль. После копирования новая stream generation делает прежние cursors stale; неудалённые approvals становятся `stale`, незавершённые runs и pending outbox — `recovery_required`. Повторная integrity/FK проверка завершает путь; ошибка очищает только созданный destination. Возобновление внешнего эффекта автоматически не доказывается.

## Отказы и tests

`INVALID_MANIFEST`, `MANIFEST_HASH_MISMATCH`, `DATABASE_HASH_MISMATCH`, `BLOB_MISSING`, `BLOB_HASH_MISMATCH`, `BLOB_COVERAGE_MISMATCH`, `SCHEMA_INCOMPATIBLE`, `INTEGRITY_FAILED`, `FOREIGN_KEY_FAILED` и существующий destination блокируют соответствующий restore. [Backup/restore tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts) и [contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts) — маршруты проверки на synthetic данных; фактические user databases в этой задаче не открывались.

## FUNC-G06 / F22 — текущая квалификация

Проверены source drift/unknown writer freeze/CAS, interrupted pre-promotion retry без duplicate tasks, committed-receipt replay, corrupt/missing blob, независимый FK check при self-consistent hashes, new-profile restore и stale approvals/pending outbox/cursors. Source authority/profile/sourcebytes сохраняются. Evidence: .tmp/func-g06/f22-focused.log, 11/11,0fail/skip. Interrupted-import case вводит отказ в trusted pre-promotion store port; это не claim об OS-process crash. FK corruption вводится только в disposable backup copy; hashes пересчитываются как независимый negative oracle. Новые профили не наследуют runtime credentials; pending effects требуют explicit recovery. [Group decisions](../planning/functional-remediation-2026-11-15.md#func-g06-results).

### SQLite WAL bookkeeping — FUNC-G06

Read-only WAL connection может создавать вспомогательные WAL/SHM в writable каталоге. Qualification сохраняет hash каждого исходного файла, включая существовавшие sidecars; отдельно фиксируются только новые empty state.sqlite-wal и наблюдаемый32KiB regular single-link state.sqlite-shm fixture. Другие добавления, удаления или hash changes запрещены. Эти файлы автоматически не удаляются. [SQLite WAL](https://sqlite.org/wal.html#read_only_databases).
