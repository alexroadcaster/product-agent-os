# PAOS SQLite: relationships and authority

Source status: repository_source / static_architecture_map; 2026-11-15.

Owner: backend/storage; scope/version: DG03 v1. Update with [schema.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), constraints or migrations; related [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts) and [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts) are not a new run. The diagram describes the PAOS source contract, not a real user database or the F33 target.

## Declared FKs

Lines below represent only declared foreign keys. Composite FKs include `project_id`; separate owner/source/target and task/session roles are shown separately. Zero or many relationships do not guarantee a business scenario and depend on guards. Tables without FKs appear separately; all columns, CHECK, UNIQUE and indexes are in the [exact DDL](../db/schema.md).

```mermaid
erDiagram
  PROJECTS ||--o{ ENTITIES : owns
  PROJECTS ||--o{ BLOBS : owns
  PROJECTS ||--o{ COMMANDS : owns
  PROJECTS ||--o{ EVENTS : owns
  PROJECTS ||--o{ OUTBOX : owns
  ENTITIES o|--o{ ENTITIES : parent
  ENTITIES ||--o{ ENTITY_BLOBS : entity
  BLOBS ||--o{ ENTITY_BLOBS : blob
  ENTITIES ||--o{ TASK_LINKS : owner
  ENTITIES ||--o{ TASK_LINKS : source
  ENTITIES ||--o{ TASK_LINKS : target
  ENTITIES ||--o{ TASK_SESSIONS : task
  ENTITIES ||--o{ TASK_SESSIONS : session
  COMMANDS ||--o{ EVENTS : command
  COMMANDS ||--o{ OUTBOX : command
  ENTITIES ||--o| IMPORT_MAPPINGS : task
  ENTITIES ||--o| INDEXED_DOCUMENTS : indexed
  ENTITIES ||--o| INDEX_JOBS : queued
  PROJECTS {
    text id PK
    text authority_mode
    integer authority_epoch
  }
  ENTITIES {
    text project_id PK, FK
    text id PK
    text parent_id FK
    text kind
    text data
    integer revision
  }
  BLOBS {
    text project_id PK, FK
    text id PK
    text sha256
  }
  COMMANDS {
    text project_id PK, FK
    text idempotency_key PK
    text command_id UK
    text receipt
  }
  EVENTS {
    text project_id PK, FK
    integer seq PK
    text command_id FK
    text payload
  }
  OUTBOX {
    text id PK
    text project_id FK
    text command_id FK
    text payload
  }
  INDEXED_DOCUMENTS {
    integer rowid PK
    text project_id FK
    text entity_id FK
  }
  SEARCH_FTS {
    text title
    text body
  }
  STORE_META {
    text key PK
    text value
  }
  SCHEMA_MIGRATIONS {
    integer version PK
    text checksum
  }
  TASK_MANAGER_CAPABILITIES {
    text key PK
    text value
  }
```

## Logical relationships without a SQL FK

`SEARCH_FTS.rowid` corresponds to `INDEXED_DOCUMENTS.rowid` in worker queries, but no SQL FK is declared. `STORE_META`, `SCHEMA_MIGRATIONS` and conditional `TASK_MANAGER_CAPABILITIES` are local system tables without a project FK. Do not infer semantic retrieval or an external DB map from FTS.

## Usage and common failures

Start with the [authority model](../db/index.md), then [transactions](../db/transactions.md), [migrations](../db/migrations.md) and [restore](../db/backup-restore.md). Common errors: treating all relationships as SQL FKs, confusing stream and index generations, or treating planned PostgreSQL/M5 or target DB F33 as current PAOS storage.
