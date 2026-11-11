import assert from 'node:assert/strict';
import { test } from 'node:test';
import { mapRuntimeEvent, mapTurnAccepted } from '../../packages/contracts/runtime/events.ts';

test('separates turn dispatch from running and from terminal outcomes', () => {
  const turn = { id: 'turn-1', status: 'inProgress', items: [], error: null };
  const params = { threadId: 'thread-1', turn };
  const identity = { threadId: 'thread-1', turnId: 'turn-1' };
  assert.deepEqual(mapTurnAccepted('thread-1', { turn }), { kind: 'turn_accepted', ...identity });
  assert.deepEqual(mapRuntimeEvent({ method: 'turn/started', params }), { kind: 'turn_started', ...identity });
  for (const outcome of ['completed', 'failed', 'interrupted']) {
    assert.deepEqual(mapRuntimeEvent({ method: 'turn/completed', params: { ...params, turn: { ...turn, status: outcome } } }),
      { kind: 'turn_ended', ...identity, outcome });
  }
  assert.deepEqual(mapRuntimeEvent({ method: 'turn/completed', params }), { kind: 'recovery_required' });
});

test('projects the request identity and never infers approval or execution from request resolution', () => {
  const params = { threadId: 'thread-1', turnId: 'turn-1', itemId: 'item-1', reason: 'fixture detail' };
  assert.deepEqual(mapRuntimeEvent({ method: 'item/commandExecution/requestApproval', id: 7, params }), {
    kind: 'approval_requested', approval: 'command', requestId: 7,
    threadId: 'thread-1', turnId: 'turn-1', itemId: 'item-1',
  });
  assert.deepEqual(mapRuntimeEvent({ method: 'serverRequest/resolved', params: { threadId: 'thread-1', requestId: 7 } }), {
    kind: 'request_resolved', threadId: 'thread-1', requestId: 7,
  });
  assert.deepEqual(mapRuntimeEvent({ method: 'item/permissions/requestApproval', params }), { kind: 'recovery_required' });
  assert.deepEqual(mapRuntimeEvent({ method: 'item/fileChange/requestApproval', id: '7', params }), {
    kind: 'approval_requested', approval: 'file', requestId: '7',
    threadId: 'thread-1', turnId: 'turn-1', itemId: 'item-1',
  });
});

test('keeps completed items separate from the turn and fails closed on unknown state signals', () => {
  const params = { threadId: 'thread-1', turnId: 'turn-1', item: {
    id: 'item-1', type: 'commandExecution', status: 'declined', aggregatedOutput: 'fixture output',
  } };
  assert.deepEqual(mapRuntimeEvent({ method: 'item/completed', params }), {
    kind: 'item_ended', threadId: 'thread-1', turnId: 'turn-1', itemId: 'item-1',
    itemType: 'commandExecution', itemStatus: 'declined',
  });
  assert.deepEqual(mapRuntimeEvent({ method: 'serverRequest/resolved', params: { requestId: 7 } }), { kind: 'recovery_required' });
  assert.deepEqual(mapRuntimeEvent({ method: 'future/unknown', params }), { kind: 'recovery_required' });
  assert.deepEqual(mapRuntimeEvent(null), { kind: 'recovery_required' });
});

test('requires terminal statuses valid for the item kind and nonblank correlation IDs', () => {
  const scope = { threadId: 'thread-1', turnId: 'turn-1' };
  for (const item of [{ type: 'commandExecution', status: 'interrupted' }, { type: 'mcpToolCall', status: 'declined' },
    { type: 'fileChange' }, { type: 'commandExecution', status: 'inProgress' }]) {
    assert.deepEqual(mapRuntimeEvent({ method: 'item/completed', params: { ...scope, item: { id: 'item-1', ...item } } }),
      { kind: 'recovery_required' });
  }
  assert.deepEqual(mapRuntimeEvent({ method: 'item/permissions/requestApproval', id: '',
    params: { ...scope, itemId: 'item-1' } }), { kind: 'recovery_required' });
  assert.deepEqual(mapRuntimeEvent({ method: 'serverRequest/resolved', params: { threadId: '  ', requestId: 7 } }),
    { kind: 'recovery_required' });
  assert.deepEqual(mapRuntimeEvent({ method: 'item/completed', params: { ...scope, item: { id: 'item-1', type: 'agentMessage' } } }),
    { kind: 'item_ended', ...scope, itemId: 'item-1', itemType: 'agentMessage', itemStatus: null });
});

test('distinguishes known item progress frames from unknown lifecycle signals', () => {
  const scope = { threadId: 'thread-1', turnId: 'turn-1' };
  assert.deepEqual(mapRuntimeEvent({ method: 'item/started', params: { ...scope, item: { id: 'item-1' } } }),
    { kind: 'non_lifecycle' });
  assert.deepEqual(mapRuntimeEvent({ method: 'item/agentMessage/delta', params: { ...scope, itemId: 'item-1', delta: 'fixture' } }),
    { kind: 'non_lifecycle' });
  assert.deepEqual(mapRuntimeEvent({ method: 'item/agentMessage/delta', params: scope }), { kind: 'recovery_required' });
});
