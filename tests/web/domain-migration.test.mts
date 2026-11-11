import assert from 'node:assert/strict';
import { mkdtemp, mkdir, rm, readFile, unlink, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { openLocalStore } from '../../apps/local-service/src/storage/local-store.mts';
import { previewTaskImport } from '../../apps/local-service/src/import-export/preview.mts';
import { createMigrationManager } from '../../apps/local-service/src/import-export/migration.mts';
import { createDomainTools } from '../../apps/local-service/src/commands/domain-tools.mts';
import { bindProject } from '../../apps/local-service/src/adapters/project-sources.ts';

const content = JSON.stringify({ schema_version: 'paos_web_task_groups_v1', tasks: [
  { id: 'PAOS-0001', title: 'Fixture', status: 'planned', depends_on: [] },
] });
async function fixture(t: { after(fn: () => Promise<void>): void }, legacy = false) {
  const root = await mkdtemp(join(tmpdir(), 'paos-domain-'));
  const store = await openLocalStore({ databasePath: join(root, 'state.sqlite') });
  t.after(async () => { await store.close(); await rm(root, { recursive: true, force: true }); });
  await mkdir(join(root, 'project'));
  const binding = await bindProject('p', join(root, 'project'));
  await writeFile(join(root, 'project', 'fixture.json'), content);
  await store.registerProject({ id: 'p', keyPrefix: 'PAOS', canonicalRoot: binding.workspaceRoot, rootIdentity: binding.directoryIdentity,
    authorityMode: legacy ? 'legacy_files' : 'sql' });
  const preview = previewTaskImport({ projectId: 'p', sourceName: 'fixture.json', content });
  const project = (await store.project('p'))!;
  return { root, store, preview, epoch: project.authorityEpoch };
}

test('cutover rejects source drift and unmanaged writers, then rehearses restore before atomic promotion', async (t) => {
  const { store, root, preview, epoch } = await fixture(t, true);
  await store.write({ projectId: 'p', actorId: 'user', expectedAuthorityEpoch: epoch, idempotencyKey: 'stage', changes: [
    { expectedRevision: 0, entity: { id: 'stage', kind: 'document', data: { ...preview, category: 'import_staging' } } },
  ] });
  let complete = false;
  const manager = createMigrationManager({ store, profileDirectory: root,
    freeze: async (input, callback) => {
      const bytes = await readFile(join(input.workspaceRoot, input.sourceRelativePath));
      return callback({ sha256: createHash('sha256').update(bytes).digest('hex'), byteSize: bytes.length,
        signal: new AbortController().signal, assertHeld() {} });
    }, inventory: async () => ({ complete,
    entries: [{ id: 'fixture-writer', role: 'writer', route: 'domain_adapter', verified: true, sourceDigest: 'a'.repeat(64) }] }) });
  const input = { projectId: 'p', stageId: 'stage', actorId: 'user', currentSource: content,
    sourceDigest: preview.sourceDigest, expectedAuthorityEpoch: epoch, idempotencyKey: 'cutover' };
  await assert.rejects(manager.cutover({ ...input, currentSource: content + ' ' }), { code: 'SOURCE_DRIFT' });
  await assert.rejects(manager.cutover(input), { code: 'WRITER_INVENTORY_INCOMPLETE' });
  assert.equal((await store.project('p'))!.authorityMode, 'legacy_files');
  complete = true;
  const result = await manager.cutover(input);
  assert.equal(result.mappingCount, 1);
  assert.equal((await store.project('p'))!.authorityMode, 'sql');
  assert.equal((await store.project('p'))!.authorityEpoch, epoch + 1);
  const exported = await manager.reverseTransfer('p');
  assert.equal(exported.tasks.length, 1);
  assert.equal(exported.operation, 'staged_reverse_transfer');
  const exportedContent = JSON.stringify(exported);
  const proposal = previewTaskImport({ projectId: 'p', sourceName: 'own-export.json', content: exportedContent });
  assert.equal(proposal.mode, 'normalized_proposal');
  assert.equal(proposal.proposal?.baseAuthorityEpoch, epoch + 1);
  assert.equal(proposal.proposal?.baseRevisions[exported.tasks[0].id], 1);
  assert.equal(proposal.proposal?.baseThroughSeq, exported.throughSeq);
  assert.deepEqual(proposal.items[0]?.task, exported.tasks[0]);
  await store.write({ projectId: 'p', actorId: 'user', expectedAuthorityEpoch: epoch + 1, idempotencyKey: 'stage-export', changes: [
    { expectedRevision: 0, entity: { id: 'stage-export', kind: 'document', data: { ...proposal, category: 'import_staging' } } },
  ] });
  await assert.rejects(manager.cutover({ ...input, stageId: 'stage-export', currentSource: exportedContent,
    sourceDigest: proposal.sourceDigest, expectedAuthorityEpoch: epoch + 1, idempotencyKey: 'no-auto-reimport' }), { code: 'IMPORT_PROPOSAL_ONLY' });
});

test('domain commands use trusted scope, preserve proposals and never grant Done', async (t) => {
  const { store, root, preview, epoch } = await fixture(t);
  const task = preview.items[0].task;
  await store.write({ projectId: 'p', actorId: 'user', expectedAuthorityEpoch: epoch, idempotencyKey: 'seed', changes: [
    { expectedRevision: 0, entity: { id: task.id, kind: 'task', data: task } },
    { expectedRevision: 0, entity: { id: 'session', kind: 'session' } },
  ] });
  const domain = createDomainTools({ store });
  const binding = { id: 'binding', projectId: 'p', sessionId: 'session', accountId: 'fixture-account', workspaceRoot: root,
    directoryIdentity: 'fixture-root', mode: 'execution' as const, profileId: 'fixture', generation: 'generation', threadId: 'thread' };
  const run = { id: 'run', bindingId: binding.id, projectId: 'p', sessionId: 'session', accountId: binding.accountId,
    generation: binding.generation, threadId: binding.threadId, turnId: 'turn', clientMessageId: 'message', inputDigest: 'digest',
    taskId: task.id, scopeDigest: 'pinned-scope', state: 'running' as const };
  const base = { binding, run, requestId: 1 };
  await assert.rejects(domain.dispatch({ ...base, tool: 'task_patch', arguments: { taskId: task.id, expectedRevision: 1, patch: { status: 'done' } } }),
    { code: 'TOOL_PATCH_FORBIDDEN' });
  await assert.rejects(domain.dispatch({ ...base, tool: 'task_read', arguments: { taskId: task.id, projectId: 'other' } }), { code: 'TOOL_ARGUMENTS_INVALID' });
  const patch = { ...base, tool: 'task_patch', arguments: { taskId: task.id, expectedRevision: 1, patch: { status: 'review' } } };
  const receipt = await domain.dispatch(patch);
  assert.deepEqual(await domain.dispatch(patch), receipt);
  const proposal = await domain.dispatch({ ...base, requestId: 2, binding: { ...binding, mode: 'planning' }, tool: 'task_propose', arguments: { title: 'Draft only' } });
  assert.ok(proposal);
  assert.equal((await store.list('p', { kind: 'task' })).length, 1);
  assert.equal((await store.list('p', { kind: 'draft' }))[0].data.category, 'task_proposal');
});

test('export metadata refuses a concurrent task revision instead of returning an inconsistent base', async (t) => {
  const { store, root, preview, epoch } = await fixture(t);
  const task = preview.items[0].task;
  await store.write({ projectId: 'p', actorId: 'user', expectedAuthorityEpoch: epoch, idempotencyKey: 'seed', changes: [
    { expectedRevision: 0, entity: { id: task.id, kind: 'task', data: task } },
  ] });
  let edit = true;
  const proxy = { ...store, async list(...arguments_: Parameters<typeof store.list>) {
    if (edit) {
      edit = false;
      await store.write({ projectId: 'p', actorId: 'user', expectedAuthorityEpoch: epoch, idempotencyKey: 'concurrent', changes: [
        { expectedRevision: 1, entity: { id: task.id, kind: 'task', data: { ...task, title: 'After concurrent edit' } } },
      ] });
    }
    return store.list(...arguments_);
  } };
  const manager = createMigrationManager({ store: proxy, profileDirectory: root, inventory: async () => ({ complete: false, entries: [] }) });
  await assert.rejects(manager.reverseTransfer('p'), { code: 'EXPORT_CONFLICT' });
  const consistent = await manager.reverseTransfer('p');
  assert.equal(consistent.tasks[0].title, 'After concurrent edit');
  assert.equal(consistent.baseRevisions[task.id], 2);
});

test('bundle cutover holds both source pins and reports later source changes without changing SQL authority', async (t) => {
  const { store, root, epoch } = await fixture(t, true);
  const md = ['### Task `PAOS-1`', '- Schema version: task_matrix_plan_v1', '- Task: Fixture', '- Status: planned'].join('\n');
  await writeFile(join(root, 'project', 'plan.md'), md);
  const sources = [
    { role: 'records' as const, sourceName: 'fixture.json', sourceRelativePath: 'fixture.json', content },
    { role: 'projection' as const, sourceName: 'plan.md', sourceRelativePath: 'plan.md', content: md },
  ];
  const preview = previewTaskImport({ projectId: 'p', sources });
  await store.write({ projectId: 'p', actorId: 'user', expectedAuthorityEpoch: epoch, idempotencyKey: 'bundle-stage', changes: [
    { expectedRevision: 0, entity: { id: 'bundle-stage', kind: 'document', data: { ...preview, category: 'import_staging' } } },
  ] });
  const held = new Set<string>();
  const acquisition: string[] = [];
  const proxy = { ...store, async promoteLegacy(command: Parameters<typeof store.promoteLegacy>[0]) {
    if (!await store.receipt('p', command.idempotencyKey)) assert.equal(held.size, 2);
    return store.promoteLegacy(command);
  } };
  const manager = createMigrationManager({ store: proxy, profileDirectory: root, inventory: async () => ({ complete: true,
    entries: [{ id: 'fixture-writer', role: 'writer', route: 'domain_adapter', verified: true, sourceDigest: 'a'.repeat(64) }] }),
    freeze: async (input, callback) => {
      const bytes = await readFile(join(input.workspaceRoot, input.sourceRelativePath));
      acquisition.push(input.sourceRelativePath); held.add(input.sourceRelativePath);
      try { return await callback({ sha256: createHash('sha256').update(bytes).digest('hex'), byteSize: bytes.length,
        signal: new AbortController().signal, assertHeld() { assert.ok(held.has(input.sourceRelativePath)); } }); }
      finally { held.delete(input.sourceRelativePath); }
    } });
  const command = { projectId: 'p', stageId: 'bundle-stage', actorId: 'user', sourceDigest: preview.sourceDigest,
    expectedAuthorityEpoch: epoch, idempotencyKey: 'bundle-cutover' };
  await assert.rejects(manager.cutover({ ...command, currentSources: [sources[0], { ...sources[1], content: md + ' ' }] }), { code: 'SOURCE_DRIFT' });
  assert.deepEqual(acquisition, []);
  const receipt = (await manager.cutover(command)).receipt;
  assert.deepEqual(acquisition, ['fixture.json', 'plan.md']);
  assert.equal(held.size, 0);
  const before = await store.events('p');
  const unchanged = await manager.sourceStatus('p');
  assert.ok(unchanged.items.every(item => item.status === 'unchanged'));
  await writeFile(join(root, 'project', 'plan.md'), md + '\nchanged externally');
  const changed = await manager.sourceStatus('p');
  assert.equal(changed.items.find(item => item.sourceName === 'plan.md')?.status, 'changed');
  assert.equal(JSON.stringify(changed).includes('sourceSnapshot'), false);
  const freezesBeforeRetry = acquisition.length;
  assert.deepEqual((await manager.cutover(command)).receipt, receipt);
  assert.equal(acquisition.length, freezesBeforeRetry);
  await unlink(join(root, 'project', 'fixture.json'));
  assert.ok((await manager.sourceStatus('p')).items.some(item => item.status === 'unavailable'));
  assert.equal((await store.project('p'))?.authorityMode, 'sql');
  assert.deepEqual((await store.events('p')).items, before.items);
});
