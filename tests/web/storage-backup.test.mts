import assert from 'node:assert/strict';
import { mkdtemp, readFile, readdir, rm, unlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve, sep } from 'node:path';
import { test } from 'node:test';
import { DatabaseSync } from 'node:sqlite';
import { openLocalStore, pruneManagedBackups, restoreLocalBackup } from '../../apps/local-service/src/storage/local-store.mts';
import { createSnapshot } from '../../apps/local-service/src/storage/snapshot.mts';

test('restoring an immutable snapshot preserves messages/settings/blobs and invalidates approvals, dispatch and cursors', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'paos-backup-test-'));
  t.after(async () => { assert.ok(resolve(root).startsWith(resolve(tmpdir()) + sep)); await rm(root, { recursive: true, force: true }); });
  const databasePath = join(root, 'paos.sqlite');
  const store = await openLocalStore({ databasePath });
  try {
    await store.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: 'synthetic', authorityMode: 'sql' });
    const blob = await store.putBlob('p1', Buffer.from('immutable synthetic blob'));
    const base = { projectId: 'p1', actorId: 'u', expectedAuthorityEpoch: 1 };
    await store.write({ ...base, idempotencyKey: 'initial', changes: [
      { expectedRevision: 0, entity: { id: 'session', kind: 'session', title: 'History' } },
      { expectedRevision: 0, entity: { id: 'message', kind: 'message', parentId: 'session', body: 'видимое сообщение', coverage: 'partial', blobIds: [blob.id] } },
      { expectedRevision: 0, entity: { id: 'settings', kind: 'settings', data: { locale: 'ru', theme: 'dark' } } },
      { expectedRevision: 0, entity: { id: 'approval', kind: 'approval', status: 'pending' } },
      { expectedRevision: 0, entity: { id: 'run', kind: 'run', status: 'running' } },
    ], outbox: [{ kind: 'dispatch', payload: { runId: 'run' } }] });
    const before = await store.events('p1');
    const backup = await store.backup(root);
    const snapshotBytes = await readFile(join(backup.directory, 'database.sqlite'));
    await store.write({ ...base, idempotencyKey: 'later', changes: [{ expectedRevision: 1,
      entity: { id: 'settings', kind: 'settings', data: { locale: 'en', theme: 'light' } } }] });
    const restoredPath = join(root, 'restored.sqlite');
    await restoreLocalBackup(backup.directory, restoredPath);
    const restored = await openLocalStore({ databasePath: restoredPath });
    try {
      assert.equal((await restored.get('p1', 'message'))?.body, 'видимое сообщение');
      assert.equal((await restored.get('p1', 'message'))?.coverage, 'partial');
      assert.deepEqual((await restored.get('p1', 'settings'))?.data, { locale: 'ru', theme: 'dark' });
      assert.equal((await restored.get('p1', 'approval'))?.status, 'stale');
      assert.equal((await restored.get('p1', 'run'))?.status, 'recovery_required');
      assert.equal((await restored.outbox('p1'))[0]?.state, 'recovery_required');
      assert.equal((await restored.search('p1', { query: 'сообщение' })).coverage, 'partial');
      await assert.rejects(restored.events('p1', { generation: before.generation }), { code: 'CURSOR_STALE' });
      assert.deepEqual(await readFile(join(`${restoredPath}.blobs`, blob.id)), Buffer.from('immutable synthetic blob'));
    } finally { await restored.close(); }
    assert.deepEqual(await readFile(join(backup.directory, 'database.sqlite')), snapshotBytes);
    assert.equal((await store.get('p1', 'settings'))?.data.locale, 'en');
    await assert.rejects(restoreLocalBackup(backup.directory, databasePath), { code: 'RESTORE_DESTINATION_EXISTS' });

    await writeFile(join(backup.directory, 'blobs', blob.id), 'corrupt');
    await assert.rejects(restoreLocalBackup(backup.directory, join(root, 'bad.sqlite')), { code: 'BLOB_HASH_MISMATCH' });
    await unlink(join(backup.directory, 'blobs', blob.id));
    await assert.rejects(restoreLocalBackup(backup.directory, join(root, 'missing.sqlite')), { code: 'BLOB_MISSING' });
  } finally { await store.close(); }
});

test('managed backup rotation requires preview candidates and preserves five recent snapshots, pinned backups and user exports', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'paos-backup-retention-'));
  t.after(async () => { assert.ok(resolve(root).startsWith(resolve(tmpdir()) + sep)); await rm(root, { recursive: true, force: true }); });
  const store = await openLocalStore({ databasePath: join(root, 'paos.sqlite') });
  try {
    await writeFile(join(root, 'user-export.txt'), 'keep');
    const pinned = await store.backup(root);
    await writeFile(join(pinned.directory, 'pinned'), 'pinned by owner');
    let latest = pinned;
    for (let index = 0; index < 6; index++) latest = await store.backup(root);
    assert.equal(latest.rotationCandidates.length, 1);
    await assert.rejects(pruneManagedBackups(root, [latest.directory]), { code: 'INVALID_BACKUP_PRUNE' });
    await pruneManagedBackups(root, latest.rotationCandidates);
    assert.equal((await readdir(root)).filter(name => name.startsWith('paos-backup-')).length, 6);
    assert.equal(await readFile(join(root, 'user-export.txt'), 'utf8'), 'keep');
    assert.ok(await readFile(join(pinned.directory, 'manifest.json')));
  } finally { await store.close(); }
});

test('newest message pages use journal insertion order and preserve relative chronology through restore', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'paos-message-order-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const store = await openLocalStore({ databasePath: join(root, 'state.sqlite') });
  try {
    await store.registerProject({ id: 'p', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: 'synthetic', authorityMode: 'sql' });
    await store.write({ projectId: 'p', actorId: 'u', idempotencyKey: 'journal', expectedAuthorityEpoch: 1, changes: [
      { expectedRevision: 0, entity: { id: 's', kind: 'session' } },
      ...Array.from({ length: 60 }, (_, index) => ({ expectedRevision: 0, entity: { id: `m-${String(100 - index)}`,
        kind: 'message' as const, parentId: 's', body: `message ${index}` } })),
    ] });
    const recent = await store.list('p', { kind: 'message', parentId: 's', order: 'newest', limit: 50 });
    assert.equal(recent[0].body, 'message 59');
    assert.equal(recent.at(-1)!.body, 'message 10');
    assert.ok(recent[0].journalOrder! > recent.at(-1)!.journalOrder!);
    const older = await store.list('p', { kind: 'message', parentId: 's', order: 'newest', offset: 50, limit: 50 });
    assert.equal(older.length, 10);
    assert.equal(older.at(-1)!.body, 'message 0');
    const backup = await store.backup(root);
    await restoreLocalBackup(backup.directory, join(root, 'restored.sqlite'));
    const restored = await openLocalStore({ databasePath: join(root, 'restored.sqlite') });
    try {
      assert.deepEqual((await restored.list('p', { kind: 'message', parentId: 's', order: 'newest', limit: 100 })).map(row => row.body),
        Array.from({ length: 60 }, (_, index) => `message ${59 - index}`));
    } finally { await restored.close(); }
  } finally { await store.close(); }
});

test('a simulated disk-full snapshot write removes its incomplete directory and preserves the live database', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'paos-backup-full-'));
  t.after(async () => { assert.ok(resolve(root).startsWith(resolve(tmpdir()) + sep)); await rm(root, { recursive: true, force: true }); });
  const databasePath = join(root, 'paos.sqlite');
  const store = await openLocalStore({ databasePath });
  try {
    await store.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: '1', authorityMode: 'sql' });
    await store.write({ projectId: 'p1', actorId: 'u', expectedAuthorityEpoch: 1, idempotencyKey: 'session', changes: [
      { expectedRevision: 0, entity: { id: 'session', kind: 'session', title: 'Preserved after disk full' } },
    ] });
    using source = new DatabaseSync(databasePath);
    await assert.rejects(createSnapshot(source, databasePath, root, { writeFile: async () => {
      throw Object.assign(new Error('Synthetic disk full'), { code: 'ENOSPC' });
    } }), { code: 'ENOSPC' });
    assert.deepEqual((await readdir(root)).filter(name => name.startsWith('paos-backup-')), []);
    assert.equal((await store.get('p1', 'session'))?.title, 'Preserved after disk full');
    assert.equal((await store.events('p1')).items.length, 1);
  } finally { await store.close(); }
});
