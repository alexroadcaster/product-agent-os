# Полная SQLite-схема PAOS

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: backend/storage owner; область: local SQLite Product-Agent OS, ревизия `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765` (DG03). Обновлять при изменении схемы, контрактов хранения или связанных тестов. Источники: [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts), [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); проверки: [storage tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage.test.mts), [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/storage-backup.test.mts). Ссылки на тесты не означают их новый запуск; runtime конкретного профиля и пользовательские БД в DG03 не исследовались.

Источник истины — SQL в [schema.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts). Ниже все 16 исходных объявлений: 15 обычных таблиц (13 базовых, `schema_migrations`, условная `task_manager_capabilities`) и виртуальная `search_fts`. Версия 1 создаёт 14 обычных и FTS; ленивый переход v2 добавляет capabilities. FTS5 может создавать служебные shadow-таблицы SQLite, не отдельные доменные сущности.

## Точный DDL: типы, PK, FK, indexes и constraints

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

`entities.data`, `commands.receipt`, `events.payload`, `outbox.payload` — TEXT с `json_valid`; JSON-формат не заменяет прикладную валидацию contract и revision. В `entities.kind` перечислены task/session/message/draft/comment/settings/document/run/approval/evidence. FK `events.command_id` и `outbox.command_id` отложены до commit; составные FK включают project ID. Логическая связь FTS rowid не является SQL FK.

Два явно объявленных индекса: `entities_scope(project_id,kind,deleted,id)` и `entities_parent(project_id,parent_id,deleted,id)`; PRIMARY KEY/UNIQUE создают дополнительные внутренние индексы SQLite. `search_fts` использует `unicode61`, prefix `2 3`; `rowid` связан с `indexed_documents` на уровне запросов без FK. [ERD](../diagrams/paos-sqlite-erd.md); [миграции и checksums](migrations.md).

## Владение JSON payload
| Колонка | Значение и владелец | Версия / контракт |
| --- | --- | --- |
| `entities.data` | Доменный payload вида entity; title/body/status — проекции для поиска и отображения | [M1 task profile](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/tasks/m1-task-profile.ts), [M2 task profile](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/issues/task-profile.ts); `schemaVersion` и domain guards проверяются worker |
| `commands.receipt` | Durable commandId/projectId/seq/revisions; необязательный cutoverBackupId | [StoreReceipt](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts); не receipt выполнения внешнего действия |
| `events.payload` | Генерируемый version 1 commandId/revisions/commentChanges/taskChanges, необязательный managerChanges | [worker insert/replay](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts); audit projection исключает содержимое комментариев и ограничивает значения |
| `outbox.payload` | Данные отложенного эффекта конкретного kind, в SQL только `json_valid` | [StoreWrite](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts) и владелец consumer; state хранится отдельно |

Payloads следуют развивающимся доменным контрактам, а не одной общей JSON-схеме для всех kinds. Неизменяемые migration checksums ограничивают физическую схему; `schemaVersion` внутри data ограничивает отдельный формат приложения. Это разные fences.
