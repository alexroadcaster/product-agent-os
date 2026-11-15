# Snapshot, backup and restore

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: backend/storage owner; scope: Product-Agent OS local SQLite, revision `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765` (DG03). Update when the schema, storage contracts or related tests change. Sources: [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts), [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); checks: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts). Test references do not assert a new run; DG03 did not inspect a user database or a particular profile runtime.

## Contents and creation

[snapshot.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/snapshot.mts) runs `VACUUM INTO` in a new private directory through the serialized Worker; it includes committed WAL pages. The snapshot is opened read-only and checked for compatibility, `integrity_check` and `foreign_key_check`. Backup includes blobs linked to non-deleted entities; each is checked for ID, size and SHA-256. The manifest contains version/checksum/appCompatibility, database and manifest hashes, blob receipts, date and ID. `credentials`, `repository_files`, `runtime_threads`, and `runtime_auth_store` are excluded: this is not a full project and authentication archive.

The result also returns `rotationCandidates` among valid managed backups beyond the newest five; a candidate is not deleted automatically. `pruneManagedBackups` is a separate call that checks the immediate parent, eligible set and absence of `pinned`. This is a boundary description, not permission to delete.

## Restore

A separate [restore worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/restore-worker.mts) verifies manifest and compatibility/checksum, database hash, integrity/FKs and full blob coverage/size/hash; the source must not be a symlink. Copying creates only a new absolute non-UNC path (`COPYFILE_EXCL`): `RESTORE_DESTINATION_EXISTS` does not overwrite a profile. After copy, a new stream generation makes old cursors stale; non-deleted approvals become `stale`, unfinished runs and pending outbox become `recovery_required`. A final integrity/FK check completes the path; failure cleans up only the created destination. Resumption of an external effect is not thereby proven.

## Failures and tests

`INVALID_MANIFEST`, `MANIFEST_HASH_MISMATCH`, `DATABASE_HASH_MISMATCH`, `BLOB_MISSING`, `BLOB_HASH_MISMATCH`, `BLOB_COVERAGE_MISMATCH`, `SCHEMA_INCOMPATIBLE`, `INTEGRITY_FAILED`, `FOREIGN_KEY_FAILED` and an existing destination block the respective restore. [Backup/restore tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts) and the [contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts) point to synthetic checks; no user database was opened in this task.
