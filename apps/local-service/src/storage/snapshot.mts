import { createHash, randomUUID } from 'node:crypto';
import { constants } from 'node:fs';
import { copyFile, lstat, mkdir, mkdtemp, open, readFile, readdir, rm } from 'node:fs/promises';
import { dirname, isAbsolute, join, resolve } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { MIGRATION_CHECKSUM, M2_MIGRATION_CHECKSUM,M2B_MIGRATION_CHECKSUM,databaseCompatibility } from './migrations/schema.mts';
import type { BackupManifest, BlobReceipt } from '../../../../packages/contracts/storage/local-store.ts';

function fail(code: string): never { throw Object.assign(new Error(code), { code }); }
function digest(bytes: Uint8Array | string) { return createHash('sha256').update(bytes).digest('hex'); }
function manifestDigest(manifest: Omit<BackupManifest, 'manifestSha256'> | BackupManifest) {
  const { manifestSha256: _ignored, ...body } = manifest as BackupManifest;
  return digest(JSON.stringify(body));
}
async function durableFile(path: string, bytes: Uint8Array | string) {
  const file = await open(path, 'wx');
  try { await file.writeFile(bytes); await file.sync(); } finally { await file.close(); }
}
async function readManifest(directory: string): Promise<BackupManifest> {
  const path = join(directory, 'manifest.json');
  const info = await lstat(path);
  if (!info.isFile() || info.isSymbolicLink() || info.size > 16 * 1024 * 1024) fail('INVALID_MANIFEST');
  try { return JSON.parse(await readFile(path, 'utf8')); }
  catch { fail('INVALID_MANIFEST'); }
}
async function managedBackups(outputRoot: string) {
  const managed: { directory: string; createdAt: string }[] = [];
  for (const entry of await readdir(outputRoot, { withFileTypes: true })) {
    if (!entry.isDirectory() || entry.isSymbolicLink() || !entry.name.startsWith('paos-backup-')) continue;
    const directory = join(outputRoot, entry.name);
    try {
      const manifest = await readManifest(directory);
      if (!validManifestCompatibility(manifest) || manifest.manifestSha256 !== manifestDigest(manifest)) continue;
      try { await lstat(join(directory, 'pinned')); continue; } catch {}
      managed.push({ directory, createdAt: manifest.createdAt });
    } catch {}
  }
  return managed.sort((a, b) => b.createdAt.localeCompare(a.createdAt) || b.directory.localeCompare(a.directory));
}

/** The caller displays rotationCandidates before explicitly applying this bounded managed-only removal. */
export async function pruneManagedBackups(outputRoot: string, candidates: readonly string[]) {
  if (!isAbsolute(outputRoot) || outputRoot.startsWith('\\\\') || !Array.isArray(candidates)) fail('INVALID_BACKUP_PRUNE');
  const eligible = new Set((await managedBackups(outputRoot)).slice(5).map(item => resolve(item.directory)));
  for (const candidate of candidates) {
    if (typeof candidate !== 'string' || dirname(resolve(candidate)) !== resolve(outputRoot) || !eligible.has(resolve(candidate))) fail('INVALID_BACKUP_PRUNE');
  }
  for (const candidate of candidates) {
    // Membership and the resolved immediate parent were validated for every candidate before any deletion.
    await rm(candidate, { recursive: true, force: false });
  }
}
function checkDatabase(db: DatabaseSync) {
  const compatibility=databaseCompatibility(db);
  if (db.prepare('PRAGMA integrity_check').get()?.integrity_check !== 'ok') fail('INTEGRITY_FAILED');
  if (db.prepare('PRAGMA foreign_key_check').all().length !== 0) fail('FOREIGN_KEY_FAILED');
  return compatibility;
}
function validManifestCompatibility(manifest:BackupManifest){
  return manifest.schemaVersion===1&&manifest.appCompatibility==='paos-m1-v1'&&manifest.migrationChecksum===MIGRATION_CHECKSUM
    ||manifest.schemaVersion===2&&manifest.appCompatibility==='paos-m2-v1'&&manifest.migrationChecksum===M2_MIGRATION_CHECKSUM
    ||manifest.schemaVersion===3&&manifest.appCompatibility==='paos-m2b-v1'&&manifest.migrationChecksum===M2B_MIGRATION_CHECKSUM;
}
export function blobDirectory(databasePath: string) { return `${databasePath}.blobs`; }
export async function writeBlob(databasePath: string, projectId: string, bytes: Uint8Array): Promise<BlobReceipt> {
  if (!(bytes instanceof Uint8Array) || bytes.length > 50 * 1024 * 1024) fail('INVALID_BLOB');
  const directory = blobDirectory(databasePath);
  await mkdir(directory, { recursive: true });
  const id = randomUUID();
  await durableFile(join(directory, id), bytes);
  return { id, projectId, sha256: digest(bytes), byteSize: bytes.length };
}
async function checkedBlob(directory: string, blob: BlobReceipt) {
  if (!/^[0-9a-f-]{36}$/.test(blob.id) || !/^[0-9a-f]{64}$/.test(blob.sha256) || !Number.isSafeInteger(blob.byteSize) || blob.byteSize < 0) fail('INVALID_MANIFEST');
  const path = join(directory, blob.id);
  let info;
  try { info = await lstat(path); } catch { fail('BLOB_MISSING'); }
  if (!info.isFile() || info.isSymbolicLink()) fail('BLOB_MISSING');
  const bytes = await readFile(path);
  if (bytes.length !== blob.byteSize || digest(bytes) !== blob.sha256) fail('BLOB_HASH_MISMATCH');
  return bytes;
}
export async function readManagedBlob(databasePath:string,blob:BlobReceipt){return checkedBlob(blobDirectory(databasePath),blob);}

/** The Worker serializes this operation. VACUUM INTO includes committed WAL pages. */
export async function createSnapshot(db: DatabaseSync, databasePath: string, outputRoot: string,
  options: { writeFile?: typeof durableFile } = {}) {
  if (!isAbsolute(outputRoot) || outputRoot.startsWith('\\\\')) fail('INVALID_BACKUP_ROOT');
  const directory = await mkdtemp(join(outputRoot, 'paos-backup-'));
  const persist = options.writeFile ?? durableFile;
  try {
    const path = join(directory, 'database.sqlite');
    db.prepare('VACUUM INTO ?').run(path);
    using snapshot = new DatabaseSync(path, { readOnly: true, enableForeignKeyConstraints: true });
    const compatibility=checkDatabase(snapshot);
    const blobs = snapshot.prepare(`SELECT DISTINCT b.* FROM blobs b JOIN entity_blobs l ON l.project_id=b.project_id AND l.blob_id=b.id
      JOIN entities e ON e.project_id=l.project_id AND e.id=l.entity_id WHERE e.deleted=0 ORDER BY b.id`).all()
      .map(row => ({ id: row.id as string, projectId: row.project_id as string, sha256: row.sha256 as string, byteSize: row.byte_size as number }));
    await mkdir(join(directory, 'blobs'));
    for (const blob of blobs) {
      const bytes = await checkedBlob(blobDirectory(databasePath), blob);
      await persist(join(directory, 'blobs', blob.id), bytes);
    }
    const body = { ...compatibility,
      backupId: randomUUID(), createdAt: new Date().toISOString(), databaseSha256: digest(await readFile(path)), blobs,
      exclusions: ['credentials', 'repository_files', 'runtime_threads', 'runtime_auth_store'] };
    const manifest = { ...body, manifestSha256: manifestDigest(body) };
    await persist(join(directory, 'manifest.json'), JSON.stringify(manifest, null, 2));
    const managed = await managedBackups(outputRoot);
    return { directory, manifest, rotationCandidates: managed.slice(5).map(item => item.directory) };
  } catch (error) {
    // Only this just-created, private backup directory is removed on failure.
    if (dirname(resolve(directory)) !== resolve(outputRoot)) fail('BACKUP_PATH_CONFLICT');
    await rm(directory, { recursive: true, force: true });
    throw error;
  }
}

/** Restore never replaces an existing database. A new generation invalidates old replay cursors. */
export async function restoreLocalBackup(directory: string, newDatabasePath: string) {
  if (!isAbsolute(directory) || !isAbsolute(newDatabasePath) || newDatabasePath.startsWith('\\\\')) fail('INVALID_RESTORE_PATH');
  const manifest = await readManifest(directory);
  if (!validManifestCompatibility(manifest)) fail('SCHEMA_INCOMPATIBLE');
  if (manifest.manifestSha256 !== manifestDigest(manifest)) fail('MANIFEST_HASH_MISMATCH');
  const source = join(directory, 'database.sqlite');
  const sourceInfo = await lstat(source);
  if (!sourceInfo.isFile() || sourceInfo.isSymbolicLink()) fail('INVALID_BACKUP_DATABASE');
  if (digest(await readFile(source)) !== manifest.databaseSha256) fail('DATABASE_HASH_MISMATCH');
  using snapshot = new DatabaseSync(source, { readOnly: true, enableForeignKeyConstraints: true });
  const compatibility=checkDatabase(snapshot);
  if(compatibility.schemaVersion!==manifest.schemaVersion||compatibility.migrationChecksum!==manifest.migrationChecksum||compatibility.appCompatibility!==manifest.appCompatibility)fail('SCHEMA_INCOMPATIBLE');
  const required = snapshot.prepare(`SELECT DISTINCT b.id,b.project_id,b.sha256,b.byte_size FROM blobs b
    JOIN entity_blobs l ON l.project_id=b.project_id AND l.blob_id=b.id JOIN entities e ON e.project_id=l.project_id AND e.id=l.entity_id
    WHERE e.deleted=0 ORDER BY b.id`).all();
  if (!Array.isArray(manifest.blobs) || manifest.blobs.length !== required.length) fail('BLOB_COVERAGE_MISMATCH');
  for (const [index, row] of required.entries()) {
    const blob = manifest.blobs[index];
    if (!blob || blob.id !== row.id || blob.projectId !== row.project_id || blob.sha256 !== row.sha256 || blob.byteSize !== row.byte_size) fail('BLOB_COVERAGE_MISMATCH');
    await checkedBlob(join(directory, 'blobs'), blob);
  }
  try { await copyFile(source, newDatabasePath, constants.COPYFILE_EXCL); }
  catch (error) {
    if ((error as NodeJS.ErrnoException).code === 'EEXIST') fail('RESTORE_DESTINATION_EXISTS');
    throw error;
  }
  let createdBlobDirectory = false;
  try {
    await mkdir(blobDirectory(newDatabasePath));
    createdBlobDirectory = true;
    for (const blob of manifest.blobs) {
      await durableFile(join(blobDirectory(newDatabasePath), blob.id), await checkedBlob(join(directory, 'blobs'), blob));
    }
    using restored = new DatabaseSync(newDatabasePath, { enableForeignKeyConstraints: true });
    restored.exec('PRAGMA synchronous=FULL; BEGIN IMMEDIATE');
    try {
      restored.prepare("UPDATE store_meta SET value=? WHERE key='stream_generation'").run(randomUUID());
      restored.exec(`UPDATE entities SET status='stale',revision=revision+1 WHERE kind='approval' AND deleted=0;
        UPDATE entities SET status='recovery_required',revision=revision+1 WHERE kind='run' AND status NOT IN ('completed','failed','interrupted') AND deleted=0;
        UPDATE outbox SET state='recovery_required' WHERE state='pending';`);
      restored.exec('COMMIT');
    } catch (error) { restored.exec('ROLLBACK'); throw error; }
    checkDatabase(restored);
    return { databasePath: newDatabasePath, backupId: manifest.backupId, generationChanged: true };
  } catch (error) {
    await rm(newDatabasePath, { force: true });
    if (createdBlobDirectory && dirname(resolve(blobDirectory(newDatabasePath))) === dirname(resolve(newDatabasePath))) {
      await rm(blobDirectory(newDatabasePath), { recursive: true, force: true });
    }
    // A failed restore stays separate from every existing database/profile.
    throw error;
  }
}
