# Backend: остановка и восстановление

Source status: repository_source / static_source_review; 15.11.2026.

Владелец: backend/runtime и storage; scope/version: DG03, `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Обновлять при изменении cancellation, checkpoints, ownership, backup/restore или shutdown contract.

## Cancellation не равна подтверждённому результату

[execution-recipes/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/execution-recipes/service.mts) сохраняет `cancel_requested` и при активном child запрашивает interrupt. Ошибка interrupt не превращается в подтверждение остановки. Если admission был запланирован, но наличие child и отказ при admission не подтверждены, состояние становится `recovery_required` / `UNCONFIRMED_ADMISSION_NO_REPLAY`. Timeout шага переводит execution в pause и запрашивает interrupt; исход child проверяется отдельно. Смотрите также [жизненный цикл](lifecycle.md).

[recipe-checkpoint.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/recovery/recipe-checkpoint.mts) сверяет run ID, binding, client message и состояние дочернего run. Наличие lease timeout или Stop недостаточно: unsettled operations, включая `dispatching`, `recovery_required` и `awaiting_approval`, оставляют checkpoint unresolved. `canResume` допускается для определённых состояний и подтверждённых checkpoint; `canCancel` не выдаётся для unresolved. Эти поля — оценка сохранённого состояния, а не гарантия внешней операции.

## Restart и очередь

При инициализации [execution-recipes/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/execution-recipes/service.mts) переводит владеющие task незавершённые executions в `recovery_required` с `SERVICE_RESTART_NO_REPLAY`. [scheduler/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts) пересматривает running/recovery entries: если persisted recipe terminal, проецирует результат, иначе сохраняет recovery_required. Автоматического replay после неопределённого dispatch нет. Preview и admission повторно проверяют task revision/scope, authority epoch, policy, dependencies и workspace ownership. Пользовательское решение и reconciliation должны использовать актуальную ревизию; stale состояние не следует объявлять успехом.

## Хранилище и отказ

Storage Worker при error/exit отклоняет ожидающие вызовы; сервис может вернуть `STORAGE_CLOSED` или `STORAGE_BUSY`. Неизвестный результат запроса требует сначала проверить receipt и актуальную entity/revision. Уникальный ключ защищает повтор идентичной storage-команды, но не позволяет предположить результат provider-side действия. Backup/restore имеют отдельный Worker и validation route: [backup/restore](../db/backup-restore.md). Проверки и восстановление конкретной пользовательской БД не выполняются этой документацией.

## Проверки и ограничения

[recipe-recovery.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/recipe-recovery.test.mts), [runtime-adapter-shutdown.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-adapter-shutdown.test.mts), [scheduler-runtime.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/scheduler-runtime.test.mts) и [runtime-sqlite.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-sqlite.test.mts) — связанные сценарии restart, ограничения очереди и recovery. Они приведены как маршруты проверки; новый прогон live runtime, фактическое завершение child, provider и human acceptance этим документом не подтверждаются. Для применимых команд и истории проверок используйте TEST и task owner.
