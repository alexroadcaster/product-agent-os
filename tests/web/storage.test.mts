import assert from 'node:assert/strict';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve, sep } from 'node:path';
import { test } from 'node:test';
import { DatabaseSync } from 'node:sqlite';
import { once } from 'node:events';
import { Worker } from 'node:worker_threads';
import { RANKED_SEARCH_SQL } from '../../apps/local-service/src/storage/search-queries.mts';
import { openLocalStore } from '../../apps/local-service/src/storage/local-store.mts';
import type { M1TaskProfile } from '../../packages/contracts/tasks/m1-task-profile.ts';

function task(id = '11111111-1111-4111-8111-111111111111'): M1TaskProfile {
  return { schemaVersion: 'm1_task_profile_v1', type: 'Task', id, projectId: 'p1', key: 'TEST-1', legacyAlias: null,
    title: 'Задача storage', summary: 'search hello', technicalValue: '', productValue: '', files: [], agentAssignments: [],
    artifactReferences: [], acceptanceCriteria: [], estimateSeconds: null,
    actual: { startedAt: null, endedAt: null, durationSeconds: null }, risks: [], status: 'backlog',
    creator: { kind: 'user', actorId: 'user-1' }, priority: null, startDate: null, dueDate: null,
    links: [], sessionIds: [], provenance: null };
}

async function fixture(t: { after: (fn: () => Promise<void>) => void }) {
  const root = await mkdtemp(join(tmpdir(), 'paos-storage-'));
  t.after(async () => {
    assert.ok(resolve(root).startsWith(resolve(tmpdir()) + sep));
    await rm(root, { recursive: true, force: true });
  });
  return { root, databasePath: join(root, 'paos.sqlite') };
}

test('a real SQLite Worker persists a scoped entity, audit and idempotent outbox across reopen', async (t) => {
  const { root, databasePath } = await fixture(t);
  let store = await openLocalStore({ databasePath });
  try {
    const project = await store.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: 'synthetic:1', authorityMode: 'sql' });
    assert.equal(project.authorityEpoch, 1);
    const command = { projectId: 'p1', actorId: 'user-1', idempotencyKey: 'write-1', expectedAuthorityEpoch: 1,
      changes: [{ expectedRevision: 0, entity: { id: 'session-1', kind: 'session' as const, title: 'Сессия hello', body: 'durable' } }],
      outbox: [{ kind: 'index', payload: { entityId: 'session-1' } }] };
    const receipt = await store.write(command);
    assert.deepEqual(await store.receipt('p1', 'write-1'), receipt);
    assert.equal(await store.receipt('p2', 'write-1'), null);
    assert.deepEqual(await store.write(command), receipt);
    await assert.rejects(store.write({ ...command, actorId: 'other' }), { code: 'IDEMPOTENCY_CONFLICT' });
    await store.close();
    store = await openLocalStore({ databasePath });
    assert.equal((await store.projects())[0]?.displayName, 'TEST');
    assert.equal((await store.get('p1', 'session-1')).revision, 1);
    assert.equal(await store.get('p2', 'session-1'), null);
    const replay = await store.events('p1', {});
    assert.equal(replay.items.length, 1);
    assert.equal(replay.items[0].actorId, 'user-1');
    assert.equal((await store.outbox('p1')).length, 1);
  } finally { await store.close(); }
});

test('legacy authority, cross-project parents and failed multi-entity writes leave no partial audit or outbox', async (t) => {
  const { root, databasePath } = await fixture(t);
  const store = await openLocalStore({ databasePath });
  try {
    await store.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: 'synthetic:1', authorityMode: 'legacy_files' });
    await store.registerProject({ id: 'p2', keyPrefix: 'OTHR', canonicalRoot: join(root, 'other'), rootIdentity: 'synthetic:2', authorityMode: 'sql' });
    const base = { projectId: 'p1', actorId: 'user', idempotencyKey: 'blocked', expectedAuthorityEpoch: 1 };
    await assert.rejects(store.write({ ...base, changes: [{ expectedRevision: 0, entity: { id: task().id, kind: 'task', data: task() } }] }), { code: 'LEGACY_AUTHORITY' });
    await store.write({ ...base, idempotencyKey: 'session', changes: [{ expectedRevision: 0, entity: { id: 'session', kind: 'session' } }] });
    await assert.rejects(store.write({ ...base, projectId: 'p2', changes: [
      { expectedRevision: 0, entity: { id: 'first', kind: 'session' } },
      { expectedRevision: 0, entity: { id: 'message', kind: 'message', parentId: 'session' } },
    ], outbox: [{ kind: 'dispatch', payload: {} }] }), { code: 'PARENT_SCOPE_CONFLICT' });
    assert.deepEqual(await store.list('p2'), []);
    assert.deepEqual((await store.events('p2')).items, []);
    assert.deepEqual(await store.outbox('p2'), []);
  } finally { await store.close(); }
});

test('separate Workers serialize competing revisions without losing committed state', async (t) => {
  const { root, databasePath } = await fixture(t);
  const first = await openLocalStore({ databasePath });
  const second = await openLocalStore({ databasePath });
  try {
    await first.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: 'synthetic:1', authorityMode: 'sql' });
    const base = { projectId: 'p1', actorId: 'user', expectedAuthorityEpoch: 1 };
    await first.write({ ...base, idempotencyKey: 'create', changes: [{ expectedRevision: 0, entity: { id: 's', kind: 'session' } }] });
    const writes = [first, second].map((store, index) => store.write({ ...base, idempotencyKey: `edit-${index}`,
      changes: [{ expectedRevision: 1, entity: { id: 's', kind: 'session', title: `winner-${index}` } }] }));
    const results = await Promise.allSettled(writes);
    assert.equal(results.filter(result => result.status === 'fulfilled').length, 1);
    assert.equal(results.find(result => result.status === 'rejected')?.reason.code, 'REVISION_CONFLICT');
    assert.equal((await first.get('p1', 's'))?.revision, 2);
    assert.equal((await second.events('p1')).items.length, 2);
  } finally { await first.close(); await second.close(); }
});

test('promotion validates drift and writer gates, then atomically imports tasks and advances the epoch', async (t) => {
  const { root, databasePath } = await fixture(t);
  const store = await openLocalStore({ databasePath });
  try {
    await store.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: 'synthetic:1', authorityMode: 'legacy_files' });
    const command = { projectId: 'p1', actorId: 'user', idempotencyKey: 'promote', expectedAuthorityEpoch: 1,
      sourceDigest: 'a'.repeat(64), verifiedSourceDigest: 'a'.repeat(64), writerInventoryVerified: true,
      restoreRehearsalVerified: true, items: [task()] };
    await assert.rejects(store.promoteLegacy({ ...command, writerInventoryVerified: false }), { code: 'CUTOVER_GATE_FAILED' });
    await assert.rejects(store.promoteLegacy({ ...command, verifiedSourceDigest: 'b'.repeat(64) }), { code: 'SOURCE_DRIFT' });
    assert.equal((await store.project('p1'))?.authorityMode, 'legacy_files');
    assert.deepEqual(await store.list('p1'), []);
    const receipt = await store.promoteLegacy(command);
    assert.deepEqual(await store.promoteLegacy(command), receipt);
    assert.equal((await store.project('p1'))?.authorityEpoch, 2);
    assert.equal((await store.project('p1'))?.authorityMode, 'sql');
    assert.deepEqual((await store.get('p1', task().id))?.data, task());
    await assert.rejects(store.write({ projectId: 'p1', actorId: 'user', idempotencyKey: 'stale', expectedAuthorityEpoch: 1,
      changes: [{ expectedRevision: 1, entity: { id: task().id, kind: 'task', data: task() } }] }), { code: 'AUTHORITY_CONFLICT' });
    const delta = await store.write({ projectId: 'p1', actorId: 'user', idempotencyKey: 'after-cutover', expectedAuthorityEpoch: 2,
      changes: [{ expectedRevision: 1, entity: { id: task().id, kind: 'task', data: { ...task(), summary: 'post-cutover change' } } }] });
    const exported = await store.exportTasks('p1');
    assert.equal(exported.tasks[0]?.summary, 'post-cutover change');
    assert.equal(exported.throughSeq, delta.seq);
    assert.equal(exported.project.authorityEpoch, 2);
  } finally { await store.close(); }
});

test('promotion pins bounded source bindings in its transaction and rejects aliased paths without importing', async (t) => {
  const { root, databasePath } = await fixture(t);
  const store = await openLocalStore({ databasePath });
  try {
    await store.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: '1', authorityMode: 'legacy_files' });
    const binding = { role: 'records' as const, sourceName: 'tasks.json', sourceRelativePath: 'data/tasks.json', sourceDigest: 'a'.repeat(64), byteSize: 100 };
    const command = { projectId: 'p1', actorId: 'u', expectedAuthorityEpoch: 1, idempotencyKey: 'bound-cutover', sourceDigest: 'a'.repeat(64),
      verifiedSourceDigest: 'a'.repeat(64), writerInventoryVerified: true, restoreRehearsalVerified: true, items: [task()], sourceBindings: [binding] };
    await assert.rejects(store.promoteLegacy({ ...command, sourceBindings: [binding, { ...binding, sourceRelativePath: 'DATA\\TASKS.JSON' }] }), { code: 'SOURCE_BINDINGS_INVALID' });
    assert.equal((await store.project('p1'))?.authorityMode, 'legacy_files');
    assert.deepEqual(await store.list('p1'), []);
    const receipt = await store.promoteLegacy(command);
    const stored = await store.get('p1', 'runtime-import-sources');
    assert.equal(stored?.kind, 'settings');
    assert.deepEqual(stored?.data.bindings, [binding]);
    assert.equal(stored?.data.authorityEpoch, 2);
    assert.ok(receipt.revisions.some(revision => revision.id === 'runtime-import-sources'));
  } finally { await store.close(); }
});

test('RU/EN FTS search and exact lookup are project-scoped, paginated and remove deleted or stale text', async (t) => {
  const { root, databasePath } = await fixture(t);
  const store = await openLocalStore({ databasePath });
  try {
    await store.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: '1', authorityMode: 'sql' });
    await store.registerProject({ id: 'p2', keyPrefix: 'OTHR', canonicalRoot: join(root, 'other'), rootIdentity: '2', authorityMode: 'sql' });
    const put = (projectId: string, id: string, body: string, revision = 0, deleted = false) => store.write({ projectId, actorId: 'u',
      idempotencyKey: `${id}-${revision}`, expectedAuthorityEpoch: 1,
      changes: [{ expectedRevision: revision, delete: deleted, entity: { id, kind: 'document', body, data: { relativePath: `docs/${id}.md` } } }] });
    await put('p1', 'a', 'проект searchable old');
    await put('p1', 'b', 'проект searchable');
    await put('p2', 'secret', 'проект searchable');
    const first = (await store.search('p1', { query: 'проект', limit: 1 })).items;
    const second = (await store.search('p1', { query: 'проект', limit: 1, offset: 1 })).items;
    assert.deepEqual([...first, ...second].map(item => item.id).sort(), ['a', 'b']);
    assert.equal((await store.search('p1', { query: 'docs/a.md' })).items[0]?.id, 'a');
    await put('p1', 'a', 'new body', 1);
    assert.equal((await store.search('p1', { query: 'old' })).items.length, 0);
    await put('p1', 'b', '', 1, true);
    const progress: { completed: number; total: number }[] = [];
    await store.rebuildSearch('p1', { onProgress: value => progress.push(value) });
    assert.equal(progress.at(-1)?.completed, 2);
    const cancelled = new AbortController();
    cancelled.abort();
    await assert.rejects(store.rebuildSearch('p1', { signal: cancelled.signal }), { code: 'INDEX_REBUILD_CANCELLED' });
    const result = await store.search('p1', { query: 'searchable' });
    assert.equal(result.items.length, 0);
    assert.equal(result.coverage, 'complete');
    await assert.rejects(store.search('p1', { query: 'x', limit: 101 }), { code: 'INVALID_PAGINATION' });
    await put('p1', 'large', 'x'.repeat(1024 * 1024 + 1));
    assert.equal((await store.search('p1', { query: 'x' })).coverage, 'partial');
  } finally { await store.close(); }
});

test('concurrent task creation allocates immutable public keys inside the transaction and retries preserve them', async (t) => {
  const { root, databasePath } = await fixture(t);
  const first = await openLocalStore({ databasePath });
  const second = await openLocalStore({ databasePath });
  try {
    await first.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: '1', authorityMode: 'sql' });
    const make = (id: string) => ({ projectId: 'p1', actorId: 'u', idempotencyKey: id, expectedAuthorityEpoch: 1,
      changes: [{ expectedRevision: 0, entity: { id, kind: 'task' as const, data: { ...task(id), key: '' } } }] });
    const a = make(task().id);
    const b = make('22222222-2222-4222-8222-222222222222');
    const receipts = await Promise.all([first.write(a), second.write(b)]);
    assert.deepEqual((await first.list('p1', { kind: 'task' })).map(item => item.publicKey).sort(), ['TEST-1', 'TEST-2']);
    assert.deepEqual(await first.write(a), receipts[0]);
    const current = await first.get('p1', a.changes[0]!.entity.id);
    await assert.rejects(first.write({ ...a, idempotencyKey: 'rename-key', changes: [{ expectedRevision: 1,
      entity: { id: current!.id, kind: 'task', data: { ...current!.data, key: 'TEST-9' } } }] }), { code: 'TASK_KEY_IMMUTABLE' });
  } finally { await first.close(); await second.close(); }
});

test('a derived index failure preserves the business commit and exposes partial coverage until rebuild', async (t) => {
  const { root, databasePath } = await fixture(t);
  const store = await openLocalStore({ databasePath });
  try {
    await store.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: '1', authorityMode: 'sql' });
    {
      using fault = new DatabaseSync(databasePath);
      fault.exec('DROP TABLE search_fts');
    }
    await store.write({ projectId: 'p1', actorId: 'u', idempotencyKey: 'index-down', expectedAuthorityEpoch: 1,
      changes: [{ expectedRevision: 0, entity: { id: 'doc', kind: 'document', body: 'rebuild searchable' } }] });
    assert.equal((await store.get('p1', 'doc'))?.revision, 1);
    assert.equal((await store.search('p1', { query: 'searchable' })).coverage, 'partial');
    await store.rebuildSearch('p1');
    assert.equal((await store.search('p1', { query: 'searchable' })).items[0]?.id, 'doc');
  } finally { await store.close(); }
});

test('an interrupted native transaction rolls back and a changed migration checksum fails closed', async (t) => {
  const { root, databasePath } = await fixture(t);
  const store = await openLocalStore({ databasePath });
  await store.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: '1', authorityMode: 'sql' });
  await store.write({ projectId: 'p1', actorId: 'u', idempotencyKey: 'initial', expectedAuthorityEpoch: 1,
    changes: [{ expectedRevision: 0, entity: { id: 'session', kind: 'session', title: 'before-crash' } }] });
  await store.close();
  const crash = new Worker(`
    const { parentPort, workerData } = require('node:worker_threads');
    const { DatabaseSync } = require('node:sqlite');
    const db = new DatabaseSync(workerData);
    db.exec("BEGIN IMMEDIATE; UPDATE entities SET title='uncommitted' WHERE id='session'");
    parentPort.postMessage('transaction-open');
    parentPort.on('message', () => {});
  `, { eval: true, workerData: databasePath });
  try { await once(crash, 'message'); } finally { await crash.terminate(); }
  const reopened = await openLocalStore({ databasePath });
  try {
    assert.equal((await reopened.get('p1', 'session'))?.title, 'before-crash');
    assert.equal((await reopened.events('p1')).items.length, 1);
  } finally { await reopened.close(); }
  {
    using fault = new DatabaseSync(databasePath);
    fault.exec("UPDATE schema_migrations SET checksum='modified'");
  }
  await assert.rejects(openLocalStore({ databasePath }), { code: 'SCHEMA_INCOMPATIBLE' });
});

test('the bounded seven-day replay window retains the full audit and rejects an expired cursor', async (t) => {
  const { root, databasePath } = await fixture(t);
  const store = await openLocalStore({ databasePath });
  try {
    await store.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: '1', authorityMode: 'sql' });
    for (let revision = 0; revision < 2; revision++) {
      await store.write({ projectId: 'p1', actorId: 'u', idempotencyKey: `command-${revision}`, expectedAuthorityEpoch: 1,
        changes: [{ expectedRevision: revision, entity: { id: 'session', kind: 'session', title: `revision-${revision}` } }] });
    }
    {
      using time = new DatabaseSync(databasePath);
      time.exec("UPDATE events SET occurred_at='2000-01-01T00:00:00.000Z' WHERE seq=1");
    }
    assert.deepEqual((await store.events('p1')).items.map(item => item.seq), [2]);
    await assert.rejects(store.events('p1', { after: 1 }), { code: 'CURSOR_STALE' });
    assert.equal((await store.audit('p1')).items.length, 2);
  } finally { await store.close(); }
});

test('comment edits retain their prior body and revision in durable audit', async (t) => {
  const { root, databasePath } = await fixture(t);
  const store = await openLocalStore({ databasePath });
  try {
    await store.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: '1', authorityMode: 'sql' });
    await store.write({ projectId: 'p1', actorId: 'u', expectedAuthorityEpoch: 1, idempotencyKey: 'task',
      changes: [{ expectedRevision: 0, entity: { id: task().id, kind: 'task', data: task() } }] });
    for (let revision = 0; revision < 2; revision++) {
      await store.write({ projectId: 'p1', actorId: 'u', idempotencyKey: `comment-${revision}`, expectedAuthorityEpoch: 1,
        changes: [{ expectedRevision: revision, entity: { id: 'comment', kind: 'comment', parentId: task().id, body: `body-${revision}` } }] });
    }
    const events = await store.audit('p1');
    const payload = events.items.at(-1)?.payload as { commentChanges: { previous: { body: string; revision: number } }[] };
    assert.deepEqual(payload.commentChanges[0]?.previous, { body: 'body-0', title: '', revision: 1 });
  } finally { await store.close(); }
});

test('an idle-required command is serialized with run intents and pending approvals while a committed retry stays idempotent', async (t) => {
  const { root, databasePath } = await fixture(t);
  const first = await openLocalStore({ databasePath });
  const second = await openLocalStore({ databasePath });
  try {
    await first.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: '1', authorityMode: 'sql' });
    const base = { projectId: 'p1', actorId: 'u', expectedAuthorityEpoch: 1 };
    await first.write({ ...base, idempotencyKey: 'task', changes: [{ expectedRevision: 0,
      entity: { id: task().id, kind: 'task', data: { ...task(), status: 'awaiting_acceptance' } } }] });
    const acceptance = { ...base, idempotencyKey: 'accept-race', requireIdle: true as const, changes: [{ expectedRevision: 1,
      entity: { id: task().id, kind: 'task' as const, data: { ...task(), status: 'done' as const } } }] };
    const [run, accepted] = await Promise.allSettled([
      first.write({ ...base, idempotencyKey: 'run', changes: [{ expectedRevision: 0, entity: { id: 'run', kind: 'run', status: 'running' } }] }),
      second.write(acceptance),
    ]);
    assert.equal(run.status, 'fulfilled');
    if (accepted.status === 'fulfilled') {
      assert.ok(accepted.value.seq < (run as PromiseFulfilledResult<any>).value.seq);
      assert.deepEqual(await second.write(acceptance), accepted.value);
    } else assert.equal(accepted.reason.code, 'ACTIVE_RUN_RECONCILIATION_REQUIRED');
    await first.write({ ...base, idempotencyKey: 'run-complete', changes: [
      { expectedRevision: 1, entity: { id: 'run', kind: 'run', status: 'completed' } },
      { expectedRevision: 0, entity: { id: 'approval', kind: 'approval', status: 'pending' } },
    ] });
    await assert.rejects(second.write({ ...acceptance, idempotencyKey: 'blocked-approval', changes: [{ expectedRevision: (await second.get('p1', task().id))!.revision,
      entity: { id: task().id, kind: 'task', data: task() } }] }), { code: 'ACTIVE_RUN_RECONCILIATION_REQUIRED' });
    await first.write({ ...base, idempotencyKey: 'approval-resolved', changes: [{ expectedRevision: 1,
      entity: { id: 'approval', kind: 'approval', status: 'resolved' } }] });
    const stable = { ...acceptance, idempotencyKey: 'accepted-before-new-run', changes: [{ expectedRevision: (await first.get('p1', task().id))!.revision,
      entity: { id: task().id, kind: 'task' as const, data: { ...task(), status: 'done' as const } } }] };
    const receipt = await first.write(stable);
    await second.write({ ...base, idempotencyKey: 'new-run', changes: [{ expectedRevision: 2,
      entity: { id: 'run', kind: 'run', status: 'running' } }] });
    assert.deepEqual(await first.write(stable), receipt);
  } finally { await first.close(); await second.close(); }
});

test('ranked paging uses the FTS rank plan and coverage counts remain committed metadata', async (t) => {
  const { root, databasePath } = await fixture(t);
  const store = await openLocalStore({ databasePath });
  try {
    await store.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: '1', authorityMode: 'sql' });
    await store.write({ projectId: 'p1', actorId: 'u', expectedAuthorityEpoch: 1, idempotencyKey: 'docs', changes: [
      { expectedRevision: 0, entity: { id: 'doc1', kind: 'document', body: 'searchable', data: { relativePath: 'README.md' } } },
      { expectedRevision: 0, entity: { id: 'doc2', kind: 'document', body: 'searchable', data: { relativePath: 'docs/other.md' } } },
    ] });
    using inspect = new DatabaseSync(databasePath, { readOnly: true });
    const plan = inspect.prepare(`EXPLAIN QUERY PLAN ${RANKED_SEARCH_SQL}`).all('searchable', 'p1', 50, 0);
    assert.equal(plan.some(row => String(row.detail).includes('TEMP B-TREE')), false, JSON.stringify(plan));
    assert.deepEqual(JSON.parse(inspect.prepare('SELECT value FROM store_meta WHERE key=?').get('search_counts:p1')?.value as string),
      { eligible: 2, indexed: 2, incomplete: 0 });
    assert.equal((await store.search('p1', { query: 'README.md' })).items[0]?.id, 'doc1');
    await store.write({ projectId: 'p1', actorId: 'u', expectedAuthorityEpoch: 1, idempotencyKey: 'delete', changes: [
      { expectedRevision: 1, delete: true, entity: { id: 'doc1', kind: 'document', body: '' } },
    ] });
    assert.deepEqual(JSON.parse(inspect.prepare('SELECT value FROM store_meta WHERE key=?').get('search_counts:p1')?.value as string),
      { eligible: 1, indexed: 1, incomplete: 0 });
    assert.equal((await store.search('p1', { query: 'README.md' })).items.length, 0);
  } finally { await store.close(); }
});

test('older v1 search projections remain partial until a scoped rebuild upgrades derived metadata', async (t) => {
  const { root, databasePath } = await fixture(t);
  let store = await openLocalStore({ databasePath });
  try {
    await store.registerProject({ id: 'p1', keyPrefix: 'TEST', canonicalRoot: root, rootIdentity: '1', authorityMode: 'sql' });
    await store.write({ projectId: 'p1', actorId: 'u', expectedAuthorityEpoch: 1, idempotencyKey: 'doc', changes: [
      { expectedRevision: 0, entity: { id: 'doc', kind: 'document', body: 'legacy searchable', data: { relativePath: 'README.md' } } },
    ] });
    await store.close();
    {
      using prior = new DatabaseSync(databasePath);
      prior.exec("DELETE FROM store_meta WHERE key IN ('search_counts:p1','search_format:p1'); UPDATE search_fts SET title='Old document title'");
    }
    store = await openLocalStore({ databasePath });
    const before = await store.search('p1', { query: 'searchable' });
    assert.equal(before.coverage, 'partial');
    assert.equal(before.items[0]?.id, 'doc');
    assert.equal((await store.search('p1', { query: 'README.md' })).items[0]?.id, 'doc');
    await store.rebuildSearch('p1');
    assert.equal((await store.search('p1', { query: 'searchable' })).coverage, 'complete');
    assert.equal((await store.search('p1', { query: 'README.md' })).items[0]?.id, 'doc');
  } finally { await store.close(); }
});
