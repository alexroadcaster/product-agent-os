# Product-Agent OS SQLite

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: backend/storage owner; scope: Product-Agent OS local SQLite, revision `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765` (DG03). Update when the schema, storage contracts or related tests change. Sources: [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts), [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); checks: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts). Test references do not assert a new run; DG03 did not inspect a user database or a particular profile runtime.

The local store belongs to a PAOS profile, not the attached project database. [Schema](schema.md) contains the complete SQL; [ERD](erd.md) links the editable diagram. [Migrations](migrations.md), [transactions](transactions.md), [backup/restore](backup-restore.md), and [search](search-index.md) describe related contracts.

## Authority and boundaries

`projects.authority_mode` distinguishes `legacy_files` and `sql`; `authority_epoch` protects commands from stale authority. Project source and documentation remain files. SQL owns eligible operational entities after verified cutover, not the whole workspace; before cutover a task cannot silently be written to SQL as primary source. See [decision W03](../architecture/decisions/adr-w03-storage-authority.md) and [transactions](transactions.md).

[F33/F34](../planning/functional-remediation-2026-11-15.md) specifies a separate target DB map and code-to-table links; current PAOS SQLite does not provide them. Team PostgreSQL/pgvector M5 remains planned. This schema describes the cited source revision, not an external database or production readiness.
