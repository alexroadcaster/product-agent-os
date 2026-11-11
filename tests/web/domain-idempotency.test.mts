import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createDomainTools } from '../../apps/local-service/src/commands/domain-tools.mts';
import type { LocalStore } from '../../apps/local-service/src/storage/local-store.mts';
import { fixtureTask, runtimeTaskId } from './runtime-adapter-time.fixture.mts';

test('agent tool retries compare canonical arguments while rejecting a changed payload', async () => {
  let receipt: unknown;
  let operation: unknown;
  let writes = 0;
  const store = {
    project: async () => ({ id: 'p', authorityEpoch: 1 }),
    receipt: async () => receipt,
    get: async () => operation,
    write: async (command: { changes: { entity: unknown }[] }) => {
      writes++;
      operation = command.changes.at(-1)!.entity;
      return receipt = { commandId: 'synthetic-receipt' };
    },
  } as unknown as LocalStore;
  const tools = createDomainTools({ store });
  const binding = { id: 'b', projectId: 'p', sessionId: 's', generation: 'g', threadId: 'thread', mode: 'planning', profileId: 'fixture' } as const;
  const run = { id: 'r', bindingId: 'b', projectId: 'p', generation: 'g', threadId: 'thread', state: 'running' } as const;
  const request = { tool: 'task_propose', requestId: 1, binding, run } as unknown as Parameters<typeof tools.dispatch>[0];
  const first = await tools.dispatch({ ...request, arguments: { title: 'Fixture', summary: 'Same' } });
  assert.deepEqual(await tools.dispatch({ ...request, arguments: { summary: 'Same', title: 'Fixture' } }), first);
  assert.equal(writes, 1);
  await assert.rejects(tools.dispatch({ ...request, arguments: { title: 'Changed', summary: 'Same' } }), { code: 'IDEMPOTENCY_CONFLICT' });
});

test('agent patches cannot erase system review guards', async () => {
  const target = { id: runtimeTaskId, kind: 'task', revision: 1,
    data: { ...fixtureTask(), status: 'in_progress', risks: ['recovery_review', 'acceptance_unverified'] } };
  const store = { project: async () => ({ id: 'p', authorityEpoch: 1 }), receipt: async () => undefined,
    get: async () => target, write: async () => ({ commandId: 'should-not-commit' }) } as unknown as LocalStore;
  const tools = createDomainTools({ store });
  const request = { tool: 'task_patch', requestId: 1,
    binding: { id: 'b', projectId: 'p', sessionId: 's', generation: 'g', threadId: 'thread', mode: 'execution', profileId: 'fixture' },
    run: { id: 'r', bindingId: 'b', projectId: 'p', generation: 'g', threadId: 'thread', state: 'running', taskId: runtimeTaskId, scopeDigest: 'pinned' },
    arguments: { taskId: runtimeTaskId, expectedRevision: 1, patch: { risks: [] } },
  } as unknown as Parameters<typeof tools.dispatch>[0];
  await assert.rejects(tools.dispatch(request), { code: 'SYSTEM_REVIEW_REQUIRED' });
});
