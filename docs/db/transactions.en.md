# Transactions, authority and idempotency

Source status: repository_source / static_contract_review; 2026-11-15.; FUNC-G04: locally_verified_with_measured_limits, 16.11.2026.

Owner: backend/storage owner; scope: Product-Agent OS local SQLite, revision `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765` (DG03). Update when the schema, storage contracts or related tests change. Sources: [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts), [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); checks: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts). Test references do not assert a new run; DG03 did not inspect a user database or a particular profile runtime.

## Worker and queue

[local-store.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/local-store.mts) opens a dedicated `DatabaseSync` Worker, accepts only an absolute non-UNC path and limits outstanding requests to 100 (`STORAGE_BUSY`). The Worker processes messages serially. It enables foreign keys, requires WAL (`WAL_UNAVAILABLE`), sets `synchronous=FULL` and `busy_timeout=5000`. Worker error or exit rejects pending calls; this contract does not establish safe operation of multiple independent processes.

## Command → commit → receipt

[write](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts) validates project/actor/idempotency key, change count, outbox and command size, then runs `BEGIN IMMEDIATE`. For an existing `(project_id,idempotency_key)`, the same hash returns the saved receipt; a different hash yields `IDEMPOTENCY_CONFLICT`. A new command checks project, `expectedAuthorityEpoch`, revisions and domain guards. Entity/link changes, `commands`, event and outbox records occur inside one transaction; an error rolls it back. Deferred command FKs are checked at commit. A receipt confirms persistence, not external outbox execution.

`legacy_files` blocks ordinary task writes until promotion. Promotion checks `writerInventoryVerified`, `restoreRehearsalVerified`, current authority, mapping/source digests and other worker guards; success increments the epoch. Source-file preservation and external writer checks depend on the specific import workflow and evidence, not a single SQL flag. Outbox states are `pending`, `acknowledged`, `recovery_required`; ack changes only pending.

## Failures and verification

Different payloads under one key, stale revision/epoch and invalid relationships are rejected; an identical retry returns its receipt. [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [import preview](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/import-preview.test.mts) and the [local-store contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts) identify relevant scenarios. Their existence does not guarantee exactly-once external side effects.

## FUNC-G03 — read snapshots and profile CAS

No SQL migration was added and previous checksums remain unchanged. Durable scans and inventory policy use versioned JSON in profile-owned `store_meta`, expectedVersion CAS and dedicated namespaces. The durable registration receipt binds request digest and project ID in the registration transaction; replay after restart does not create another project.

`projectSnapshot` reads rows and freshness stamp in one read transaction. `runtimeFileScope` likewise reads registry/policy and the saved task after file I/O, rejecting old preflight after root/policy/task changes. Shared `inventoryScopeFingerprint` guards plaintext, cached previews and graph publication; native commands repeat the registry fence after dependency/autonomy waits. Policy changes after a command has begun do not undo its effects. Policy-race regressions have observed RED/GREEN evidence; full Web594/594,0skip.

## FUNC-G04 — profile CAS and read models

New profile-owned namespaces are not target DB migrations: project_database_schema_v1 is capped at2MiB (registration/status and two metadata snapshots); project_code_database_v1 at1MiB (source-backed static links/pins). Existing project_scan_v1 (1MiB) and project_inventory_policy_v1 (32KiB) retain their caps. Writes check expectedVersion and increment monotonic versions; original SQL migrations/checksums are unchanged. Late schema/status/diff replies recheck source/version/snapshot identities.

projectEntities/projectSnapshot select consumer kinds before the unchanged100k rows/64MiB safety budget. Task Manager additionally selects managed attachments and retains an atomic freshness stamp with its rows. History TEMP SQL snapshots freeze membership/values/ordinal, preserve old cursor values after edit/archive, and return only bounded pages. Payload230MiB/mainfile256MiB,100 snapshots/15-minute expiry/LRU and100 items/1MiB pages bound work; transient journal/sort disk and native RSS are not certified by these caps. Cold generation latency remains a measured F20 limit.
