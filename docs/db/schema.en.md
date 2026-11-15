# Complete PAOS SQLite schema

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: backend/storage owner; scope: Product-Agent OS local SQLite, revision `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765` (DG03). Update when the schema, storage contracts or related tests change. Sources: [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts), [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); checks: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts). Test references do not assert a new run; DG03 did not inspect a user database or a particular profile runtime.

The SQL in [schema.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts) is authoritative. All 16 source declarations follow: 15 ordinary tables (13 base tables, `schema_migrations`, conditional `task_manager_capabilities`) and virtual `search_fts`. Version 1 creates 14 ordinary tables and FTS; lazy v2 adds capabilities. FTS5 may create SQLite shadow tables, not separate domain entities.

## Exact DDL: types, PK, FK, indexes and constraints

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
  version INTEGER PRIMARY KEY, checksum TEXT NOT NULL, applied_at TEXT NOT NULL, app_compatibility TEXT NOT NULL
) STRICT;

CREATE TABLE store_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL) STRICT;
CREATE TABLE projects (
  id TEXT PRIMARY KEY, key_prefix TEXT NOT NULL UNIQUE, display_name TEXT NOT NULL, canonical_root TEXT NOT NULL UNIQUE,
  root_identity TEXT NOT NULL UNIQUE, authority_mode TEXT NOT NULL CHECK(authority_mode IN ('legacy_files','sql')),
  authority_epoch INTEGER NOT NULL CHECK(authority_epoch > 0), next_task_number INTEGER NOT NULL DEFAULT 1 CHECK(next_task_number>0)
) STRICT;
CREATE TABLE entities (
  project_id TEXT NOT NULL REFERENCES projects(id), id TEXT NOT NULL,
  kind TEXT NOT NULL CHECK(kind IN ('task','session','message','draft','comment','settings','document','run','approval','evidence')),
  parent_id TEXT, title TEXT NOT NULL, body TEXT NOT NULL, status TEXT NOT NULL,
  public_key TEXT, coverage TEXT NOT NULL CHECK(coverage IN ('complete','partial','unavailable')),
  data TEXT NOT NULL CHECK(json_valid(data)), revision INTEGER NOT NULL CHECK(revision > 0),
  deleted INTEGER NOT NULL CHECK(deleted IN (0,1)), updated_at TEXT NOT NULL,
  PRIMARY KEY(project_id,id), UNIQUE(project_id,public_key),
  FOREIGN KEY(project_id,parent_id) REFERENCES entities(project_id,id)
) STRICT;
CREATE INDEX entities_scope ON entities(project_id,kind,deleted,id);
CREATE INDEX entities_parent ON entities(project_id,parent_id,deleted,id);
CREATE TABLE blobs (
  project_id TEXT NOT NULL REFERENCES projects(id), id TEXT NOT NULL, sha256 TEXT NOT NULL, byte_size INTEGER NOT NULL CHECK(byte_size>=0),
  PRIMARY KEY(project_id,id), UNIQUE(id)
) STRICT;
CREATE TABLE entity_blobs (
  project_id TEXT NOT NULL, entity_id TEXT NOT NULL, blob_id TEXT NOT NULL,
  PRIMARY KEY(project_id,entity_id,blob_id),
  FOREIGN KEY(project_id,entity_id) REFERENCES entities(project_id,id),
  FOREIGN KEY(project_id,blob_id) REFERENCES blobs(project_id,id)
) STRICT;
CREATE TABLE task_links (
  project_id TEXT NOT NULL, owner_id TEXT NOT NULL, source_id TEXT NOT NULL, target_id TEXT NOT NULL,
  relation TEXT NOT NULL CHECK(relation IN ('blocks','related')), PRIMARY KEY(project_id,owner_id,source_id,target_id,relation),
  CHECK(source_id <> target_id),
  FOREIGN KEY(project_id,owner_id) REFERENCES entities(project_id,id),
  FOREIGN KEY(project_id,source_id) REFERENCES entities(project_id,id),
  FOREIGN KEY(project_id,target_id) REFERENCES entities(project_id,id)
) STRICT;
CREATE TABLE task_sessions (
  project_id TEXT NOT NULL, task_id TEXT NOT NULL, session_id TEXT NOT NULL,
  PRIMARY KEY(project_id,task_id,session_id),
  FOREIGN KEY(project_id,task_id) REFERENCES entities(project_id,id),
  FOREIGN KEY(project_id,session_id) REFERENCES entities(project_id,id)
) STRICT;
CREATE TABLE commands (
  project_id TEXT NOT NULL REFERENCES projects(id), command_id TEXT NOT NULL UNIQUE,
  idempotency_key TEXT NOT NULL, payload_hash TEXT NOT NULL, receipt TEXT NOT NULL CHECK(json_valid(receipt)),
  PRIMARY KEY(project_id,idempotency_key)
) STRICT;
CREATE TABLE events (
  project_id TEXT NOT NULL REFERENCES projects(id), seq INTEGER NOT NULL, event_id TEXT NOT NULL UNIQUE,
  command_id TEXT NOT NULL REFERENCES commands(command_id) DEFERRABLE INITIALLY DEFERRED,
  actor_id TEXT NOT NULL, occurred_at TEXT NOT NULL, payload TEXT NOT NULL CHECK(json_valid(payload)),
  PRIMARY KEY(project_id,seq)
) STRICT;
CREATE TABLE outbox (
  id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id),
  command_id TEXT NOT NULL REFERENCES commands(command_id) DEFERRABLE INITIALLY DEFERRED,
  kind TEXT NOT NULL, payload TEXT NOT NULL CHECK(json_valid(payload)),
  state TEXT NOT NULL CHECK(state IN ('pending','acknowledged','recovery_required'))
) STRICT;
CREATE TABLE import_mappings (
  project_id TEXT NOT NULL, source_id TEXT NOT NULL, task_id TEXT NOT NULL, source_digest TEXT NOT NULL,
  PRIMARY KEY(project_id,source_id), UNIQUE(project_id,task_id),
  FOREIGN KEY(project_id,task_id) REFERENCES entities(project_id,id)
) STRICT;
CREATE TABLE indexed_documents (
  rowid INTEGER PRIMARY KEY, project_id TEXT NOT NULL, entity_id TEXT NOT NULL, revision INTEGER NOT NULL,
  generation INTEGER NOT NULL, UNIQUE(project_id,entity_id),
  FOREIGN KEY(project_id,entity_id) REFERENCES entities(project_id,id)
) STRICT;
CREATE VIRTUAL TABLE search_fts USING fts5(title, body, tokenize='unicode61', prefix='2 3');
CREATE TABLE index_jobs (
  project_id TEXT NOT NULL, entity_id TEXT NOT NULL, revision INTEGER NOT NULL,
  PRIMARY KEY(project_id,entity_id), FOREIGN KEY(project_id,entity_id) REFERENCES entities(project_id,id)
) STRICT;

CREATE TABLE task_manager_capabilities (key TEXT PRIMARY KEY,value TEXT NOT NULL) STRICT;
INSERT INTO task_manager_capabilities VALUES ('task_profile','m2_task_profile_v1');
```

`entities.data`, `commands.receipt`, `events.payload`, and `outbox.payload` are TEXT with `json_valid`; JSON validity does not replace application contract and revision validation. `entities.kind` enumerates task/session/message/draft/comment/settings/document/run/approval/evidence. FKs `events.command_id` and `outbox.command_id` are deferred until commit; composite FKs include project ID. The logical FTS rowid relationship is not a SQL FK.

The two explicit indexes are `entities_scope(project_id,kind,deleted,id)` and `entities_parent(project_id,parent_id,deleted,id)`; PRIMARY KEY/UNIQUE create additional internal SQLite indexes. `search_fts` uses `unicode61`, prefix `2 3`; `rowid` joins `indexed_documents` at query level without an FK. [ERD](../diagrams/paos-sqlite-erd.md); [migrations and checksums](migrations.md).

## JSON payload ownership
| Column | Meaning and owner | Version / contract |
| --- | --- | --- |
| `entities.data` | Domain payload for the entity kind; title/body/status are indexed projections | [M1 task profile](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/tasks/m1-task-profile.ts), [M2 task profile](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/issues/task-profile.ts); profile `schemaVersion` and domain guards are checked by worker |
| `commands.receipt` | Durable commandId/projectId/seq/revisions; optional cutoverBackupId | [StoreReceipt](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); not an external action receipt |
| `events.payload` | Generated version 1 commandId/revisions/commentChanges/taskChanges, optional managerChanges | [worker insert and replay](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts); audit projection redacts comment contents and bounds values |
| `outbox.payload` | Kind-specific deferred effect data, `json_valid` only at SQL layer | [StoreWrite](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts) and owning consumer; state is separately stored |

Payloads are examples of evolving domain contracts, not a promise that every kind shares one JSON schema. Immutable migration checksums fence the physical schema; `schemaVersion` inside data fences a separate application format. Do not substitute either for the other.
