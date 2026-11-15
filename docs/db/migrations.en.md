# Migrations and compatibility

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: backend/storage owner; scope: Product-Agent OS local SQLite, revision `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765` (DG03). Update when the schema, storage contracts or related tests change. Sources: [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts), [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); checks: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts). Test references do not assert a new run; DG03 did not inspect a user database or a particular profile runtime.

## Versions and fences

| Version | Addition and validation | Result |
| --- | --- | --- |
| 1 | Base DDL; SHA-256 of source schema string = `MIGRATION_CHECKSUM` | `paos-m1-v1` |
| 2 | Lazy, in the business transaction: `task_manager_capabilities` and `task_profile=m2_task_profile_v1`; `M2_MIGRATION_CHECKSUM` | `paos-m2-v1` |
| 3 | Lazy, in the same transaction: `workflow_registry=m2b_workflow_registry_v1`; `M2B_MIGRATION_CHECKSUM` | `paos-m2b-v1` |

`schema_migrations` stores version, checksum, applied_at and app_compatibility. `databaseCompatibility` allows exactly the sequences 1, 1–2, or 1–3 with known checksums and required markers. An unknown/modified migration, missing marker or foreign non-empty database without history is rejected as `SCHEMA_INCOMPATIBLE`. Initial creation and stream/index generation entries in `store_meta` occur in `BEGIN IMMEDIATE`; failure rolls back.

`ensureM2Schema`/`ensureM2BSchema` run inside the business transaction: a rejected first command cannot leave a newer format fence. Editing original SQL without a compatibility strategy changes its checksum; do not treat historical DDL as an ordinary migration patch. This source description is not an instruction to migrate a user profile.

Checks: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [domain migration tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/domain-migration.test.mts), [snapshot validation](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/snapshot.mts). Dated evidence and new checks retain provenance.
