# Transactions, authority and idempotency

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: backend/storage owner; scope: Product-Agent OS local SQLite, revision `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765` (DG03). Update when the schema, storage contracts or related tests change. Sources: [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts), [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); checks: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts). Test references do not assert a new run; DG03 did not inspect a user database or a particular profile runtime.

## Worker and queue

[local-store.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/local-store.mts) opens a dedicated `DatabaseSync` Worker, accepts only an absolute non-UNC path and limits outstanding requests to 100 (`STORAGE_BUSY`). The Worker processes messages serially. It enables foreign keys, requires WAL (`WAL_UNAVAILABLE`), sets `synchronous=FULL` and `busy_timeout=5000`. Worker error or exit rejects pending calls; this contract does not establish safe operation of multiple independent processes.

## Command → commit → receipt

[write](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts) validates project/actor/idempotency key, change count, outbox and command size, then runs `BEGIN IMMEDIATE`. For an existing `(project_id,idempotency_key)`, the same hash returns the saved receipt; a different hash yields `IDEMPOTENCY_CONFLICT`. A new command checks project, `expectedAuthorityEpoch`, revisions and domain guards. Entity/link changes, `commands`, event and outbox records occur inside one transaction; an error rolls it back. Deferred command FKs are checked at commit. A receipt confirms persistence, not external outbox execution.

`legacy_files` blocks ordinary task writes until promotion. Promotion checks `writerInventoryVerified`, `restoreRehearsalVerified`, current authority, mapping/source digests and other worker guards; success increments the epoch. Source-file preservation and external writer checks depend on the specific import workflow and evidence, not a single SQL flag. Outbox states are `pending`, `acknowledged`, `recovery_required`; ack changes only pending.

## Failures and verification

Different payloads under one key, stale revision/epoch and invalid relationships are rejected; an identical retry returns its receipt. [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [import preview](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/import-preview.test.mts) and the [local-store contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts) identify relevant scenarios. Their existence does not guarantee exactly-once external side effects.
