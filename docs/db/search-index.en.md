# Search and index

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: backend/storage owner; scope: Product-Agent OS local SQLite, revision `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765` (DG03). Update when the schema, storage contracts or related tests change. Sources: [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts), [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); checks: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts). Test references do not assert a new run; DG03 did not inspect a user database or a particular profile runtime.

## Indexing

`search_fts` is FTS5 with `title`, `body`, `unicode61`, prefix `2 3`. The [Worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts) maintains `indexed_documents` with project/entity/revision/generation and a rowid corresponding to the FTS rowid. This relationship is implemented by queries, not an FK. Only eligible kinds are indexed; text over 1 MiB is excluded. Scope and path tokens use SHA-256 for project separation and exact paths; this is not database encryption.

## Reads and coverage

The worker checks exact entity ID/public key first, then exact relative document path, then FTS: [RANKED_SEARCH_SQL](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/search-queries.mts) joins FTS to a live entity of the matching revision and project; values are bound parameters. The result includes `coverage` and generation. `complete` requires equal eligible/indexed counts, no incomplete or pending jobs, FTS availability and current format; otherwise it is `partial`. A partial result does not establish absence.

The index is derived from business state: the worker commits the business transaction first, then processes durable `index_jobs` in a separate transaction. A failed refresh does not roll back an accepted receipt; the job and partial coverage remain for rebuild/retry. Therefore a receipt does not prove index freshness.

## Rebuild and limits

`rebuildSearch` is transactional: it increments generation, reindexes entities, reports progress and deletes jobs after completion. Abort through the shared buffer yields `INDEX_REBUILD_CANCELLED` and rollback. Index restore/change does not imply semantic search or production RAG: this is local SQLite FTS, and target-project graph and PoCs F30–F34 belong to the [functional plan](../planning/functional-remediation-2026-11-15.md).

Checks: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [UI stream/search tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/ui-stream-search.test.mts); [result contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts). See [backup/restore](backup-restore.md) for generation and stale cursors with a different purpose: stream generation must not be confused with index generation.
