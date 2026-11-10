import assert from 'node:assert/strict';
import { test } from 'node:test';
import { projectTaskTime } from '../../apps/local-service/src/events/task-time.ts';

const scope = { projectId: 'fixture-project', taskId: 'fixture-task' };

function event(seq: number, intervalId: string, actorId: string, runId: string, atMs: number) {
  return { ...scope, seq, eventId: `fixture-event-${seq}`, intervalId, actorId, runId, atMs, source: 'fixture-runtime' };
}

test('replays duplicate events without counting pauses or parallel agent time twice as task time', () => {
  const stop = { ...event(3, 'first', 'builder', 'run-a', 10_000), kind: 'interval_stopped', reason: 'pause' } as const;
  const events = [
    { ...event(1, 'first', 'builder', 'run-a', 0), kind: 'interval_started' },
    { ...event(2, 'parallel', 'tester', 'run-a', 3_000), kind: 'interval_started' },
    stop,
    { ...event(4, 'parallel', 'tester', 'run-a', 15_000), kind: 'interval_stopped', reason: 'finished' },
    { ...event(5, 'retry', 'builder', 'run-b', 20_000), kind: 'interval_started' },
    { ...event(6, 'retry', 'builder', 'run-b', 25_000), kind: 'interval_stopped', reason: 'finished' },
    { ...stop, seq: 7 },
  ] as const;

  assert.deepEqual(projectTaskTime(scope, events), {
    actualDurationMs: 20_000, confirmedElapsedMs: 20_000, confirmedAgentEffortMs: 27_000,
    openIntervalCount: 0, unresolvedIntervalCount: 0,
  });
});

test('keeps a crash end unknown until reconciliation and merges overlapping effort by the same agent', () => {
  const start = { ...event(1, 'interrupted', 'builder', 'run-a', 2_000), kind: 'interval_started' } as const;
  assert.deepEqual(projectTaskTime(scope, [start]), {
    actualDurationMs: null, confirmedElapsedMs: 0, confirmedAgentEffortMs: 0,
    openIntervalCount: 1, unresolvedIntervalCount: 0,
  });
  const retry = [
    start,
    { ...event(2, 'interrupted', 'builder', 'run-a', 8_000), kind: 'interval_crashed' },
    { ...event(3, 'retry', 'builder', 'run-b', 9_000), kind: 'interval_started' },
    { ...event(4, 'retry', 'builder', 'run-b', 15_000), kind: 'interval_stopped', reason: 'finished' },
  ] as const;
  assert.deepEqual(projectTaskTime(scope, retry), {
    actualDurationMs: null, confirmedElapsedMs: 6_000, confirmedAgentEffortMs: 6_000,
    openIntervalCount: 0, unresolvedIntervalCount: 1,
  });
  const reconciled = { ...event(5, 'interrupted', 'builder', 'run-a', 19_000), kind: 'interval_reconciled', confirmedEndedAtMs: 12_000 } as const;
  assert.deepEqual(projectTaskTime(scope, [reconciled, ...retry.toReversed()]), {
    actualDurationMs: 13_000, confirmedElapsedMs: 13_000, confirmedAgentEffortMs: 13_000,
    openIntervalCount: 0, unresolvedIntervalCount: 0,
  });
  assert.throws(() => projectTaskTime(scope, [...retry, { ...reconciled, confirmedEndedAtMs: 20_000 }]), {
    code: 'INVALID_TASK_TIME_JOURNAL',
  });
});

test('rejects foreign scope and conflicting reuse of an event identity', () => {
  const start = { ...event(1, 'first', 'builder', 'run-a', 0), kind: 'interval_started' } as const;
  assert.throws(() => projectTaskTime(scope, [{ ...start, projectId: 'other-project' }]), { code: 'INVALID_TASK_TIME_JOURNAL' });
  assert.throws(() => projectTaskTime(scope, [start, { ...start, seq: 2, atMs: 1 }]), { code: 'INVALID_TASK_TIME_JOURNAL' });
});
