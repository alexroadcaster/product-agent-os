import assert from 'node:assert/strict';
import { test } from 'node:test';
import { previewTaskImport } from '../../apps/local-service/src/import-export/preview.mts';

const source = { schema_version: 'paos_web_task_groups_v1', tasks: [
  { id: 'PAOS-1', title: 'Сохранить данные', status: 'implemented', short_description: 'Fixture',
    technical_value: 'Integrity', product_value: 'History', affected_files: [], agents: ['builder'],
    project_artifacts: [], acceptance_criteria: ['Round trip'], estimated_duration_hms: '01:30:00',
    actual_started_at: null, actual_ended_at: null, actual_duration_seconds: null, risks: '', depends_on: [] },
] };

test('previews stable project IDs and explicit status mapping without granting task acceptance', () => {
  const options = { projectId: 'synthetic-project', sourceName: 'fixture.json', content: JSON.stringify(source) };
  const first = previewTaskImport(options);
  const next = previewTaskImport(options);
  assert.equal(first.items.length, 1);
  assert.equal(first.items[0].task.id, next.items[0].task.id);
  assert.equal(first.items[0].task.status, 'awaiting_acceptance');
  assert.equal(first.items[0].task.provenance?.sourceStatus, 'implemented');
  assert.equal(first.items[0].task.actual.durationSeconds, null);
  assert.equal(first.items[0].task.estimateSeconds, 5400);
  assert.equal(first.items[0].task.provenance?.sourceDigest, first.sourceDigest);
  assert.notEqual(previewTaskImport({ ...options, projectId: 'other-project' }).items[0].task.id, first.items[0].task.id);
});

test('blocks unsupported data and unresolved dependencies while retaining the original snapshot', () => {
  const content = JSON.stringify({ ...source, tasks: [{ ...source.tasks[0], attachments: [{ name: 'fixture' }] }] });
  const result = previewTaskImport({ projectId: 'p', sourceName: 'fixture.json', content });
  assert.equal(result.items.length, 0);
  assert.ok(result.blocked[0].reasons.includes('unsupported:attachments'));
  assert.equal(result.sourceSnapshot, content);
  const dangling = JSON.stringify({ ...source, tasks: [{ ...source.tasks[0], depends_on: ['MISSING'] }] });
  assert.ok(previewTaskImport({ projectId: 'p', sourceName: 'fixture.json', content: dangling }).blocked[0].reasons
    .includes('unresolved_dependency:MISSING'));
});

test('parses detailed Markdown cards without taking Completion Report status as the source status', () => {
  const content = ['# Fixture', '### Task `PAOS-1`', '', '- Task: Проверка', '- Status: planned',
    '- Schema version: task_matrix_plan_v1', '- Short description: Example', '- Depends on: none',
    '- Estimated execution time: 01:00:00 (предварительно)', '', '#### Completion Report', '- Status: done'].join('\n');
  const result = previewTaskImport({ projectId: 'p', sourceName: 'fixture.md', content });
  assert.equal(result.items.length, 1);
  assert.equal(result.items[0].task.status, 'backlog');
  assert.equal(result.items[0].task.provenance?.sourceStatus, 'planned');
});

test('canonical planned Markdown keeps structured Scope and treats only the known Affected files boilerplate as metadata', () => {
  const content = ['### Task `PAOS-1`', '- Task: Fixture', '- Status: planned', '- Schema version: task_matrix_plan_v1',
    '- Scope: src/task.ts', '- Actual time: not_started; start/end/duration = null.',
    '- Affected files: proposed paths above; actual create/modify/delete receipts only after execution.'].join('\n');
  const preview = previewTaskImport({ projectId: 'p', sourceName: 'plan.md', content });
  assert.equal(preview.items.length, 1);
  assert.equal(preview.items[0].task.files[0].relativePath, 'src/task.ts');
  assert.equal(preview.items[0].task.actual.durationSeconds, null);
  const actual = previewTaskImport({ projectId: 'p', sourceName: 'plan.md', content: content.replace(
    'proposed paths above; actual create/modify/delete receipts only after execution.', 'src/actual-change.ts') });
  assert.equal(actual.items.length, 0);
  assert.ok(actual.blocked[0].reasons.includes('unsupported:markdown:Affected files'));
});

test('blocks both legacy aliases when their canonical task keys collide', () => {
  const content = JSON.stringify({ ...source, tasks: [{ ...source.tasks[0], id: 'PAOS-1' }, { ...source.tasks[0], id: 'PAOS-0001' }] });
  const preview = previewTaskImport({ projectId: 'p', sourceName: 'fixture.json', content });
  assert.equal(preview.items.length, 0);
  assert.equal(preview.blocked.length, 2);
  assert.ok(preview.blocked.every(item => item.reasons.includes('duplicate_canonical_key:PAOS-1')));
});

test('rejects string dependencies before graph validation can miss their cycle', () => {
  const content = JSON.stringify({ ...source, tasks: [
    { ...source.tasks[0], id: 'PAOS-1', depends_on: 'PAOS-2' },
    { ...source.tasks[0], id: 'PAOS-2', depends_on: 'PAOS-1' },
  ] });
  const preview = previewTaskImport({ projectId: 'p', sourceName: 'fixture.json', content });
  assert.equal(preview.items.length, 0);
  assert.equal(preview.blocked.length, 2);
  assert.ok(preview.blocked.every(item => item.reasons.includes('invalid_dependencies')));
});

test('a two-source bundle deduplicates matching Markdown projection by canonical key and blocks conflicting values', () => {
  const records = { ...source, tasks: [{ ...source.tasks[0], id: 'PAOS-0001', title: 'Same title', status: 'planned' }] };
  const md = ['### Task `PAOS-1`', '- Schema version: task_matrix_plan_v1', '- Task: Same title', '- Status: planned'].join('\n');
  const sources = [
    { role: 'records' as const, sourceName: 'tasks.json', sourceRelativePath: 'data/tasks.json', content: JSON.stringify(records) },
    { role: 'projection' as const, sourceName: 'plan.md', sourceRelativePath: 'docs/plan.md', content: md },
  ];
  const preview = previewTaskImport({ projectId: 'p', sources });
  assert.equal(preview.items.length, 1);
  assert.equal(preview.blocked.length, 0);
  assert.equal(preview.items[0].task.legacyAlias, 'PAOS-0001');
  assert.equal(preview.sources?.length, 2);
  const conflict = previewTaskImport({ projectId: 'p', sources: [sources[0], { ...sources[1], content: md.replace('Same title', 'Conflicting title') }] });
  assert.equal(conflict.items.length, 0);
  assert.ok(conflict.blocked.some(item => item.reasons.includes('projection_conflict:title')));
  assert.equal(previewTaskImport({ projectId: 'p', sources: [...sources].reverse() }).sourceDigest, preview.sourceDigest);
  for (const invalid of [sources.slice(0, 1), [sources[0], { ...sources[1], role: 'records' as const }],
    [sources[0], { ...sources[1], sourceRelativePath: 'DATA\\TASKS.JSON' }],
    [sources[0], { ...sources[1], sourceRelativePath: '../plan.md' }],
    [sources[0], { ...sources[1], content: 'x'.repeat(1024 * 1024 + 1) }]]) {
    assert.throws(() => previewTaskImport({ projectId: 'p', sources: invalid }), { code: 'IMPORT_BUNDLE_INVALID' });
  }
});

test('normalized SQL export edits stay proposals with stable identity and reject significant extensions', () => {
  const task = previewTaskImport({ projectId: 'p', sourceName: 'fixture.json', content: JSON.stringify(source) }).items[0].task;
  const exported = { schema_version: 'm1_task_profile_v1', projectId: 'p', authorityEpoch: 2, streamGeneration: 'generation-1',
    throughSeq: 10, baseRevisions: { [task.id]: 4 }, tasks: [{ ...task, title: 'Proposed edit' }], authority: 'sql', operation: 'staged_reverse_transfer' };
  const preview = previewTaskImport({ projectId: 'p', sourceName: 'export.json', content: JSON.stringify(exported) });
  assert.equal(preview.mode, 'normalized_proposal');
  assert.equal(preview.items[0].task.id, task.id);
  assert.equal(preview.items[0].task.key, task.key);
  assert.equal(preview.items[0].task.title, 'Proposed edit');
  assert.deepEqual(preview.proposal, { baseAuthorityEpoch: 2, baseStreamGeneration: 'generation-1', baseThroughSeq: 10,
    baseRevisions: { [task.id]: 4 }, requiresCurrentSnapshot: true });
  const unsupported = previewTaskImport({ projectId: 'p', sourceName: 'export.json', content: JSON.stringify({ ...exported,
    tasks: [{ ...task, attachments: [{ source: 'must be preserved' }] }] }) });
  assert.equal(unsupported.items.length, 0);
  assert.equal(unsupported.blocked.length, 1);
  assert.throws(() => previewTaskImport({ projectId: 'other', sourceName: 'export.json', content: JSON.stringify(exported) }), { code: 'IMPORT_SCOPE_CONFLICT' });
  const other = previewTaskImport({ projectId: 'p', sourceName: 'fixture.json', content: JSON.stringify({ ...source,
    tasks: [{ ...source.tasks[0], id: 'PAOS-2' }] }) }).items[0].task;
  const cyclic = previewTaskImport({ projectId: 'p', sourceName: 'export.json', content: JSON.stringify({ ...exported,
    baseRevisions: { [task.id]: 1, [other.id]: 1 }, tasks: [
      { ...task, links: [{ relation: 'blocks', projectId: 'p', taskId: other.id }] },
      { ...other, links: [{ relation: 'blocks', projectId: 'p', taskId: task.id }] },
    ] }) });
  assert.equal(cyclic.items.length, 0);
  assert.ok(cyclic.blocked.every(item => item.reasons.includes('dependency_cycle')));
});

test('imports active and closed statuses with the required review guards and preserves non-null source duration', () => {
  const preview = (status: string) => previewTaskImport({ projectId: 'p', sourceName: 'fixture.json',
    content: JSON.stringify({ ...source, tasks: [{ ...source.tasks[0], status, actual_duration_hms: '00:42:00' }] }) });
  const active = preview('in_progress').items[0].task;
  assert.equal(active.status, 'ready');
  assert.ok(active.risks.includes('recovery_review'));
  const closed = preview('done').items[0].task;
  assert.equal(closed.status, 'awaiting_acceptance');
  assert.ok(closed.risks.includes('acceptance_unverified'));
  assert.equal(closed.actual.durationSeconds, 2520);
});

test('rejects unknown Markdown values and dependency cycles without losing the source snapshot', () => {
  const content = ['### Task `PAOS-1`', '- Task: Fixture', '- Status: planned', '- Schema version: task_matrix_plan_v1',
    '- Attachments: important.bin', '- Project artifacts: important-plan.md', '- Actual duration: 00:42:00'].join('\n');
  const md = previewTaskImport({ projectId: 'p', sourceName: 'fixture.md', content });
  assert.equal(md.items.length, 0);
  assert.ok(md.blocked[0].reasons.includes('unsupported:attachments'));
  const cyclic = previewTaskImport({ projectId: 'p', sourceName: 'fixture.json', content: JSON.stringify({ ...source,
    tasks: [{ ...source.tasks[0], id: 'PAOS-1', depends_on: ['PAOS-2'] }, { ...source.tasks[0], id: 'PAOS-2', depends_on: ['PAOS-1'] }] }) });
  assert.ok(cyclic.blocked.length > 0);
});
