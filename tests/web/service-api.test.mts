import assert from 'node:assert/strict';
import { createHash, randomUUID } from 'node:crypto';
import { mkdtemp, mkdir, rm, writeFile, link, readdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { openLocalStore } from '../../apps/local-service/src/storage/local-store.mts';
import { createLocalApplication } from '../../apps/local-service/src/http/application.mts';

const origin = 'http://127.0.0.1:43127';
async function fixture(t: { after(fn: () => Promise<void>): void }) {
  const root = await mkdtemp(join(tmpdir(), 'paos-http-'));
  const workspace = join(root, 'project');
  await mkdir(workspace);
  const store = await openLocalStore({ databasePath: join(root, 'state.sqlite') });
  t.after(async () => { await store.close(); await rm(root, { recursive: true, force: true }); });
  const app = await createLocalApplication({ store, origin, instanceId: 'fixture', profileDirectory: root });
  let cookie = '', csrf = '';
  async function request(path: string, payload?: unknown, method = payload === undefined ? 'GET' : 'POST') {
    return app.handleRequest(new Request(`${origin}/api/v1${path}`, { method,
      headers: { host: '127.0.0.1:43127', origin, cookie, 'x-paos-csrf': csrf, 'content-type': 'application/json' },
      ...(payload === undefined ? {} : { body: JSON.stringify(payload) }) }));
  }
  const paired = await request('/bootstrap/exchange', { code: app.issuePairingCode() });
  cookie = paired.headers.get('set-cookie')!.split(';')[0];
  csrf = (await paired.json()).csrfToken;
  const created = await request('/projects', { name: 'Fixture', workspaceRoot: workspace, keyPrefix: 'PAOS' });
  assert.equal(created.status, 201, JSON.stringify(await created.clone().json()));
  const project = await created.json();
  return { root, store, app, request, project };
}

function task(projectId: string) {
  return { schemaVersion: 'm1_task_profile_v1', type: 'Task', id: randomUUID(), projectId, key: 'PAOS-1', legacyAlias: null,
    title: 'Fixture task', summary: '', technicalValue: '', productValue: '', files: [], agentAssignments: [],
    artifactReferences: [], acceptanceCriteria: ['Verified by owner'], estimateSeconds: null,
    actual: { startedAt: null, endedAt: null, durationSeconds: null }, risks: [], status: 'awaiting_acceptance',
    creator: { kind: 'user', actorId: 'forged-client-actor' }, priority: null, startDate: null, dueDate: null,
    links: [], sessionIds: [], provenance: null };
}

test('uses the real Worker for paired CRUD, durable preferences, search and project-scoped cursors', async (t) => {
  const { request, project, store } = await fixture(t);
  const value = task(project.id);
  const command = { expectedAuthorityEpoch: project.authorityEpoch, idempotencyKey: 'create-task',
    changes: [{ expectedRevision: 0, entity: { id: value.id, kind: 'task', data: value } }] };
  assert.equal((await request(`/projects/${project.id}/commands`, command)).status, 200);
  const saved = await store.get(project.id, value.id);
  assert.deepEqual(saved!.data.creator, { kind: 'user', actorId: 'local-user' });
  const found = await (await request(`/projects/${project.id}/search?q=Fixture`)).json();
  assert.equal(found.items[0].id, value.id);
  await request('/preferences', { locale: 'en', theme: 'dark' }, 'PUT');
  assert.deepEqual(await (await request('/preferences')).json(), { locale: 'en', theme: 'dark' });
  const events = await (await request(`/projects/${project.id}/events`)).json();
  assert.ok(events.nextCursor);
  const empty = await (await request(`/projects/${project.id}/events?cursor=${events.nextCursor}`)).json();
  assert.equal(empty.nextCursor, events.nextCursor);
  assert.equal((await request(`/projects/${project.id}/events?cursor=${events.nextCursor}x`)).status, 400);
  const connection = await (await request('/connection')).json();
  assert.equal(connection.verified, false);
  assert.equal((await request('/runtime/send', { input: 'not dispatched' })).status, 409);
});

test('keeps check and owner acceptance separate and retries a committed acceptance without duplicate work', async (t) => {
  const { request, project, store } = await fixture(t);
  const value = task(project.id);
  const base = `/projects/${project.id}`;
  await request(`${base}/commands`, { expectedAuthorityEpoch: project.authorityEpoch, idempotencyKey: 'create-task',
    changes: [{ expectedRevision: 0, entity: { id: value.id, kind: 'task', data: value } }] });
  const current = await store.get(project.id, value.id);
  const epoch = (await store.project(project.id))!.authorityEpoch;
  const forged = await request(`${base}/commands`, { expectedAuthorityEpoch: epoch, idempotencyKey: 'forged-done',
    changes: [{ expectedRevision: current!.revision, entity: { id: value.id, kind: 'task', data: { ...value, status: 'done' } } }] });
  assert.equal(forged.status, 409);
  const check = await request(`${base}/tasks/${value.id}/check`, { expectedRevision: current!.revision,
    expectedAuthorityEpoch: epoch, idempotencyKey: 'check-task', outcome: 'passed', note: 'Manual fixture observation' });
  const { checkId } = await check.json();
  assert.equal((await store.get(project.id, value.id))!.status, 'awaiting_acceptance');
  const input = { expectedRevision: current!.revision, expectedAuthorityEpoch: epoch, idempotencyKey: 'accept-task',
    checkId, accepted: true, note: 'Owner accepts fixture' };
  const accepted = await request(`${base}/tasks/${value.id}/accept`, input);
  assert.equal(accepted.status, 200, JSON.stringify(await accepted.clone().json()));
  const repeated = await request(`${base}/tasks/${value.id}/accept`, input);
  assert.equal(repeated.status, 200);
  assert.deepEqual(await repeated.json(), await accepted.json());
  assert.equal((await store.get(project.id, value.id))!.status, 'done');
});

test('reserves check history for dedicated endpoints and blocks acceptance during an unresolved run', async (t) => {
  const { request, project, store } = await fixture(t);
  const value = task(project.id);
  const base = `/projects/${project.id}`;
  await request(`${base}/commands`, { expectedAuthorityEpoch: project.authorityEpoch, idempotencyKey: 'create-task',
    changes: [{ expectedRevision: 0, entity: { id: value.id, kind: 'task', data: value } }] });
  const forged = await request(`${base}/commands`, { expectedAuthorityEpoch: project.authorityEpoch, idempotencyKey: 'fake-check',
    changes: [{ expectedRevision: 0, entity: { id: 'fake-check', kind: 'comment', parentId: value.id,
      data: { category: 'manual_check', outcome: 'passed', taskRevision: 1 } } }] });
  assert.equal(forged.status, 409);
  const check = await (await request(`${base}/tasks/${value.id}/check`, { expectedAuthorityEpoch: project.authorityEpoch,
    expectedRevision: 1, idempotencyKey: 'legitimate-check', outcome: 'passed', note: 'Fixture' })).json();
  await store.write({ projectId: project.id, actorId: 'runtime', idempotencyKey: 'running', expectedAuthorityEpoch: project.authorityEpoch,
    changes: [{ expectedRevision: 0, entity: { id: 'session', kind: 'session' } },
      { expectedRevision: 0, entity: { id: 'run', kind: 'run', parentId: 'session', status: 'recovery_required', data: { taskId: value.id } } }] });
  const accepted = await request(`${base}/tasks/${value.id}/accept`, { expectedAuthorityEpoch: project.authorityEpoch,
    expectedRevision: 1, idempotencyKey: 'unsafe-accept', accepted: true, checkId: check.checkId, note: 'Fixture' });
  assert.equal(accepted.status, 409);
  const privateWrite = await request(`${base}/commands`, { expectedAuthorityEpoch: project.authorityEpoch,
    idempotencyKey: 'private-binding', changes: [{ expectedRevision: 0, entity: { id: 'runtime-binding-fixture',
      kind: 'settings', data: { runtimeBinding: { accountId: 'private-fixture' } } } }] });
  assert.equal(privateWrite.status, 409);
  await store.write({ projectId: project.id, actorId: 'runtime', idempotencyKey: 'private-fixture',
    expectedAuthorityEpoch: project.authorityEpoch, changes: [{ expectedRevision: 0, entity: {
      id: 'runtime-binding-fixture', kind: 'settings', data: { runtimeBinding: { accountId: 'private-fixture' } } } }] });
  const search = await (await request(`${base}/search?q=runtime-binding-fixture`)).json();
  assert.deepEqual(search.items, []);
});

test('a committed edit of a done task retries after reopening without reapplying or bypassing payload conflict checks', async (t) => {
  const { request, project, store } = await fixture(t);
  const value = task(project.id);
  await store.write({ projectId: project.id, actorId: 'local-user', idempotencyKey: 'seed-done', expectedAuthorityEpoch: project.authorityEpoch,
    changes: [{ expectedRevision: 0, entity: { id: value.id, kind: 'task', data: { ...value, status: 'done', creator: { kind: 'user', actorId: 'local-user' } } } }] });
  const base = `/projects/${project.id}/commands`;
  const edit = { expectedAuthorityEpoch: project.authorityEpoch, idempotencyKey: 'edit-done', changes: [
    { expectedRevision: 1, entity: { id: value.id, kind: 'task', data: { ...value, status: 'done', title: 'Edited while done' } } },
  ] };
  const committed = await request(base, edit);
  assert.equal(committed.status, 200);
  const reopened = await request(base, { expectedAuthorityEpoch: project.authorityEpoch, idempotencyKey: 'reopen', changes: [
    { expectedRevision: 2, entity: { id: value.id, kind: 'task', data: { ...value, status: 'ready', title: 'Edited while done' } } },
  ] });
  assert.equal(reopened.status, 200);
  const retry = await request(base, edit);
  assert.equal(retry.status, 200);
  assert.deepEqual(await retry.json(), await committed.json());
  assert.equal((await store.get(project.id, value.id))?.status, 'ready');
  assert.equal((await store.get(project.id, value.id))?.revision, 3);
  const conflict = await request(base, { ...edit, changes: [{ ...edit.changes[0], entity: { ...edit.changes[0].entity,
    data: { ...edit.changes[0].entity.data, title: 'Different request' } } }] });
  assert.equal(conflict.status, 409);
  assert.equal((await conflict.json()).error.code, 'IDEMPOTENCY_CONFLICT');
});

test('reads only fixed bound UTF-8 sources with a raw hash and redacted display, and rebuilds scoped search', async (t) => {
  const { request, project, root } = await fixture(t);
  await writeFile(join(root, 'project', 'REQUIREMENTS.md'), '# Synthetic source\nAPI example sk-SYNTHETIC_ONLY_DO_NOT_USE\n');
  const source = await request(`/projects/${project.id}/sources/requirements`);
  assert.equal(source.status, 200);
  const detail = await source.json();
  assert.match(detail.sha256, /^[a-f0-9]{64}$/);
  assert.equal(detail.sha256, createHash('sha256').update('# Synthetic source\nAPI example sk-SYNTHETIC_ONLY_DO_NOT_USE\n').digest('hex'));
  assert.equal(detail.relativePath, 'REQUIREMENTS.md');
  assert.equal(detail.redacted, true);
  assert.ok(!detail.content.includes('sk-SYNTHETIC'));
  assert.equal((await request(`/projects/${project.id}/sources/.env`)).status, 404);
  await link(join(root, 'project', 'REQUIREMENTS.md'), join(root, 'project', 'AGENTS.md'));
  assert.equal((await request(`/projects/${project.id}/sources/instructions`)).status, 409);
  await writeFile(join(root, 'project', 'TEST.md'), Buffer.from([0xff, 0xfe, 0x80]));
  assert.equal((await (await request(`/projects/${project.id}/sources/test`)).json()).error.code, 'SOURCE_ENCODING_INVALID');
  await writeFile(join(root, 'project', 'TEST.md'), 'x'.repeat(1024 * 1024 + 1));
  assert.equal((await (await request(`/projects/${project.id}/sources/test`)).json()).error.code, 'SOURCE_TOO_LARGE');
  const rebuilt = await request(`/projects/${project.id}/search/rebuild`, {});
  assert.equal(rebuilt.status, 200);
  assert.equal((await rebuilt.json()).status, 'rebuilt');
});

test('user backup actions retain the five newest managed snapshots', async (t) => {
  const { request, project, root } = await fixture(t);
  let last: { rotationCandidateIds: string[]; retention: string } | undefined;
  for (let count = 0; count < 6; count++) {
    const result = await request(`/projects/${project.id}/backups`, {});
    assert.equal(result.status, 200);
    last = await result.json();
  }
  assert.equal(last!.retention, 'pending');
  assert.equal(last!.rotationCandidateIds.length, 1);
  assert.equal((await readdir(join(root, 'backups'))).filter((name) => name.startsWith('paos-backup-')).length, 6);
  const applied = await request(`/projects/${project.id}/backups/rotation`, { candidateIds: last!.rotationCandidateIds });
  assert.equal(applied.status, 200);
  assert.deepEqual((await applied.json()).rotatedBackupIds, last!.rotationCandidateIds);
  assert.equal((await readdir(join(root, 'backups'))).filter((name) => name.startsWith('paos-backup-')).length, 5);
});
