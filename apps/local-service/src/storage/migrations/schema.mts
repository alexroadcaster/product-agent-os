import { createHash } from 'node:crypto';
import type { DatabaseSync } from 'node:sqlite';

const schema = `
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
`;

export const SCHEMA_VERSION = 1;
export const MIGRATION_CHECKSUM = createHash('sha256').update(schema).digest('hex');

/** Migration checksums are immutable. A drifted or newer database is never opened for writing. */
export function migrate(db: DatabaseSync, generation: string) {
  db.exec('BEGIN IMMEDIATE');
  try {
    db.exec(`CREATE TABLE IF NOT EXISTS schema_migrations (
      version INTEGER PRIMARY KEY, checksum TEXT NOT NULL, applied_at TEXT NOT NULL, app_compatibility TEXT NOT NULL
    ) STRICT`);
    const migrations = db.prepare('SELECT version,checksum FROM schema_migrations ORDER BY version').all();
    if (migrations.length === 0) {
      if (db.prepare("SELECT 1 FROM sqlite_schema WHERE name NOT LIKE 'sqlite_%' AND name<>'schema_migrations' LIMIT 1").get()) {
        throw Object.assign(new Error('Database does not belong to this application'), { code: 'SCHEMA_INCOMPATIBLE' });
      }
      db.exec(schema);
      db.prepare('INSERT INTO schema_migrations VALUES (?,?,?,?)').run(SCHEMA_VERSION, MIGRATION_CHECKSUM, new Date().toISOString(), 'paos-m1-v1');
      db.prepare('INSERT INTO store_meta VALUES (?,?)').run('stream_generation', generation);
      db.prepare('INSERT INTO store_meta VALUES (?,?)').run('index_generation', '1');
    } else if (migrations.length !== 1 || migrations[0]?.version !== SCHEMA_VERSION || migrations[0]?.checksum !== MIGRATION_CHECKSUM) {
      throw Object.assign(new Error('Unsupported or modified database migration'), { code: 'SCHEMA_INCOMPATIBLE' });
    }
    db.exec('COMMIT');
  } catch (error) {
    db.exec('ROLLBACK');
    throw error;
  }
}
