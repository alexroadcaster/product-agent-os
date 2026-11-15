# ERD and data relationships

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: backend/storage owner; scope: Product-Agent OS local SQLite, revision `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765` (DG03). Update when the schema, storage contracts or related tests change. Sources: [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts), [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); checks: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts). Test references do not assert a new run; DG03 did not inspect a user database or a particular profile runtime.

The single editable Mermaid ERD is in the [diagram atlas](../diagrams/paos-sqlite-erd.md). It shows actual declared FKs with roles and separately explains the logical FTS rowid join without an FK. Full SQL with columns, types, PK/FK, indexes and CHECK is in [schema](schema.md).

Cardinalities reflect only nullable/unique schema constraints; business guards and actual data existence must be checked separately. This ERD does not establish an external F33 target DB, migration readiness, graph-to-table links or PostgreSQL M5.
