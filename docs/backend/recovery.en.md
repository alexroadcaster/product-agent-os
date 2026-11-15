# Backend: stop and recovery

Source status: repository_source / static_source_review; 2026-11-15.

Owner: backend/runtime and storage; scope/version: DG03, `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Update when cancellation, checkpoints, ownership, backup/restore or shutdown contracts change.

## Cancellation is not a confirmed outcome

[execution-recipes/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/execution-recipes/service.mts) records `cancel_requested` and requests interrupt when a child is active. An interrupt error does not establish that the child stopped. If admission was planned but neither a child nor rejected admission is confirmed, state becomes `recovery_required` / `UNCONFIRMED_ADMISSION_NO_REPLAY`. A step timeout pauses execution and requests interrupt; the child outcome is checked separately. See also the [lifecycle](lifecycle.md).

[recipe-checkpoint.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/recovery/recipe-checkpoint.mts) checks run ID, binding, client message and child run state. Lease timeout or a Stop request is insufficient: unsettled operations including `dispatching`, `recovery_required` and `awaiting_approval` leave the checkpoint unresolved. `canResume` is allowed for specified states and confirmed checkpoints; `canCancel` is unavailable for an unresolved checkpoint. These fields assess persisted state, not guarantee an external operation.

## Restart and queue

On initialization [execution-recipes/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/execution-recipes/service.mts) moves unfinished task-owning executions to `recovery_required` with `SERVICE_RESTART_NO_REPLAY`. [scheduler/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts) rechecks running/recovery entries: a terminal persisted recipe is projected to an outcome, otherwise recovery_required remains. There is no automatic replay after uncertain dispatch. Preview and admission recheck task revision/scope, authority epoch, policy, dependencies and workspace ownership. User decisions and reconciliation must use the current revision; stale state must not be presented as success.

## Storage and failure

A storage Worker error/exit rejects waiting calls; the service may return `STORAGE_CLOSED` or `STORAGE_BUSY`. For an unknown request outcome, first inspect the receipt and current entity/revision. A unique key protects an identical storage-command retry but does not establish the outcome of provider-side work. Backup/restore use a separate Worker and validation route: [backup/restore](../db/backup-restore.md). This documentation does not inspect or restore a user database.

## Checks and limits

[recipe-recovery.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/recipe-recovery.test.mts), [runtime-adapter-shutdown.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-adapter-shutdown.test.mts), [scheduler-runtime.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/scheduler-runtime.test.mts) and [runtime-sqlite.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-sqlite.test.mts) cover related restart, queue-boundary and recovery scenarios. They are verification routes, not proof of a new live runtime run, actual child termination, provider access or human acceptance. Use TEST and the task owner for applicable commands and historical evidence.
