import assert from 'node:assert/strict';
import { test } from 'node:test';
import { decodeM1TaskProfile, encodeM1TaskProfile } from '../../apps/local-service/src/tasks/task-profile.ts';

const sample = {
  schemaVersion: 'm1_task_profile_v1',
  type: 'Task',
  id: '579d7a1c-7070-4efe-b30c-2a9819c37123',
  projectId: 'fixture-project',
  key: 'PAOS-42',
  legacyAlias: 'PAOS-0042',
  title: 'Проверить обмен',
  summary: 'Профиль M1',
  technicalValue: 'Проверяемый перенос',
  productValue: 'Устойчивые ссылки на задачу',
  files: [{ relativePath: 'src/fixture.ts', plannedOperation: 'modify', actualOperation: null }],
  agentAssignments: ['builder', 'tester'],
  artifactReferences: ['evidence/fixture.md'],
  acceptanceCriteria: ['Исходный статус сохранён'],
  estimateSeconds: 3600,
  actual: { startedAt: '2026-11-10T19:30:00Z', endedAt: null, durationSeconds: null },
  risks: ['Неизвестный исход исполнения'],
  status: 'ready',
  creator: { kind: 'imported_unknown', actorId: null },
  priority: 'high',
  startDate: '2026-11-10',
  dueDate: '2026-11-12',
  links: [{ relation: 'blocks', taskId: 'a945a41b-b87f-4ab3-9ef7-068662b98489', projectId: 'fixture-project' }],
  sessionIds: ['fixture-session'],
  provenance: {
    sourceSchema: 'paos_web_task_groups_v1', adapterVersion: '1', sourceId: 'PAOS-0042', sourceGroup: 'G11',
    sourceStatus: 'in_progress', sourceDigest: 'a'.repeat(64), sourceDocument: 'research/fixture.json', mappingReceipt: 'fixture-receipt',
  },
};

test('round-trips the M1 card with stable identity, separate source status and unknown actual time', () => {
  const task = decodeM1TaskProfile(sample);
  assert.deepEqual(JSON.parse(encodeM1TaskProfile(task)), sample);
  assert.deepEqual(decodeM1TaskProfile(JSON.parse(encodeM1TaskProfile(task))), task);
});

test('preserves supported timestamps and fields when future-stage placeholders are empty', () => {
  const actual = { startedAt: '2026-11-10T19:30:00.123456Z', endedAt: '2026-11-10T19:31:00.987654Z', durationSeconds: 60 };
  const task = decodeM1TaskProfile({ ...sample, actual, parentId: null, children: [], attachments: [] });
  assert.deepEqual(JSON.parse(encodeM1TaskProfile(task)), { ...sample, actual });
});

test('rejects unsupported significant fields and invalid task relations before export', () => {
  const otherTask = sample.links[0];
  const invalidCases = [
    [{ ...sample, type: 'Epic' }, 'task.type'],
    [{ ...sample, status: 'planned' }, 'task.status'],
    [{ ...sample, parentId: 'parent' }, 'task.parentId'],
    [{ ...sample, attachments: [{ id: 'fixture-blob' }] }, 'task.attachments'],
    [{ ...sample, links: [{ ...otherTask, relation: 'duplicates' }] }, 'task.links[0].relation'],
    [{ ...sample, links: [{ ...otherTask, projectId: 'other-project' }] }, 'task.links[0].projectId'],
    [{ ...sample, links: [{ ...otherTask, taskId: sample.id }] }, 'task.links[0].taskId'],
    [{ ...sample, links: [otherTask, otherTask] }, 'task.links[1].taskId'],
    [{ ...sample, links: [otherTask, { ...otherTask, relation: 'blocked_by' }] }, 'task.links[1].taskId'],
  ] as const;

  for (const [input, path] of invalidCases) {
    assert.throws(() => decodeM1TaskProfile(input), { code: 'INVALID_M1_TASK_PROFILE', path });
  }
});
