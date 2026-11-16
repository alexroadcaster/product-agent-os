# Backend: stop and recovery

Source status: repository_source / current_source_review; 2026-11-15.

Owner: backend/runtime and storage; scope/version: DG03, `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Update when cancellation, checkpoints, ownership, backup/restore or shutdown contracts change.

## FUNC-G03: background scans and source freshness

Current `project-scans/service.mts` persists queued/running/stage progress through profile CAS. After restart, unfinished queued/running scans become `interrupted` with `SERVICE_RESTART_NO_REPLAY`; analysis is not replayed automatically. `application.close()` closes scans before the store: owned controllers are aborted, owned live scans become `interrupted`/`SERVICE_SHUTDOWN_NO_REPLAY`, and owned work promises are awaited. This is a local read-only scan; its cancellation does not prove a provider run stopped.

Cancel checks project/scan ownership, removes queued work, fences late publication and persists cancelled. Retry creates a new attempt using `retry:{scanId}`; replaying a request does not create independent duplicates. Stage timeouts bound waiting; failures may yield partial, while inventory failure ends the scan. Scope drift, unavailable roots or changed inventory revisions interrupt publication. `lastSuccessful` retains the last finished scan (including partial), so state/coverage/reasons and provenance must still be checked.

Scan errors do not roll back durable Add. After interrupted/failed/unavailable, inspect reasons, repair the root/policy/runtime prerequisite and explicitly retry. The existing checkout Python core works on an owned projection; missing packaged core reports unavailable. Cleanup only affects the owned temporary projection/child; the target workspace is unchanged.

`freshness` reads a profile stamp, while task-manager obtains entities+stamp atomically. This is not a watcher or a guarantee that filesystem contents remain unchanged. External changes require manual refresh/read/scan; stale root/policy/file pins require a new observation/preflight. Preflight does not reserve files or replace approval: the gateway checks admission and fresh capture before broker operations. Missing/excluded/moved paths cannot grant source reads.

Source review covers current scan/analysis/storage/gateway files; parent-provided F29 API6/6, preflight API1/1, gateway policy28/28 and F18focused5/5 results cover local synthetic integration. Final browser/native verification and human acceptance remain outside this page. See [endpoints](../api/endpoints.md).

## Cancellation is not a confirmed outcome

[execution-recipes/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/execution-recipes/service.mts) records `cancel_requested` and requests interrupt when a child is active. An interrupt error does not establish that the child stopped. If admission was planned but neither a child nor rejected admission is confirmed, state becomes `recovery_required` / `UNCONFIRMED_ADMISSION_NO_REPLAY`. A step timeout pauses execution and requests interrupt; the child outcome is checked separately. See also the [lifecycle](lifecycle.md).

[recipe-checkpoint.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/recovery/recipe-checkpoint.mts) checks run ID, binding, client message and child run state. Lease timeout or a Stop request is insufficient: unsettled operations including `dispatching`, `recovery_required` and `awaiting_approval` leave the checkpoint unresolved. `canResume` is allowed for specified states and confirmed checkpoints; `canCancel` is unavailable for an unresolved checkpoint. These fields assess persisted state, not guarantee an external operation.

## Restart and queue

On initialization [execution-recipes/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/execution-recipes/service.mts) moves unfinished task-owning executions to `recovery_required` with `SERVICE_RESTART_NO_REPLAY`. [scheduler/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts) rechecks running/recovery entries: a terminal persisted recipe is projected to an outcome, otherwise recovery_required remains. There is no automatic replay after uncertain dispatch. Preview and admission recheck task revision/scope, authority epoch, policy, dependencies and workspace ownership. User decisions and reconciliation must use the current revision; stale state must not be presented as success.

## Storage and failure

A storage Worker error/exit rejects waiting calls; the service may return `STORAGE_CLOSED` or `STORAGE_BUSY`. For an unknown request outcome, first inspect the receipt and current entity/revision. A unique key protects an identical storage-command retry but does not establish the outcome of provider-side work. Backup/restore use a separate Worker and validation route: [backup/restore](../db/backup-restore.md). This documentation does not inspect or restore a user database.

## Checks and limits

[recipe-recovery.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/recipe-recovery.test.mts), [runtime-adapter-shutdown.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-adapter-shutdown.test.mts), [scheduler-runtime.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/scheduler-runtime.test.mts) and [runtime-sqlite.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-sqlite.test.mts) cover related restart, queue-boundary and recovery scenarios. They are verification routes, not proof of a new live runtime run, actual child termination, provider access or human acceptance. Use TEST and the task owner for applicable commands and historical evidence.
