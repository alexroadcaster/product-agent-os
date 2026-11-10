import type { TaskTimeEvent, TaskTimeProjection, TaskTimeScope } from '../../../../packages/contracts/time/task-time.ts';

type Interval = { actorId: string; runId: string; startMs: number; endMs: number | null; crashObservedAtMs: number | null };
type ConfirmedInterval = Readonly<{ startMs: number; endMs: number }>;

function invalid(reason: string): never {
  throw Object.assign(new Error(reason), { code: 'INVALID_TASK_TIME_JOURNAL' });
}

function nonempty(value: unknown): value is string {
  return typeof value === 'string' && Boolean(value.trim());
}

function validate(scope: TaskTimeScope, event: TaskTimeEvent): void {
  if (event.projectId !== scope.projectId || event.taskId !== scope.taskId) invalid('event is outside task scope');
  if (![event.eventId, event.intervalId, event.runId, event.actorId, event.source].every(nonempty)
    || !Number.isSafeInteger(event.seq) || event.seq < 1 || !Number.isSafeInteger(event.atMs) || event.atMs < 0) {
    invalid('event identity, sequence or timestamp is invalid');
  }
  if (event.kind === 'interval_stopped' && !['pause', 'retry', 'finished'].includes(event.reason)) invalid('unsupported stop reason');
  if (event.kind === 'interval_reconciled' && (!Number.isSafeInteger(event.confirmedEndedAtMs)
    || event.confirmedEndedAtMs < 0 || event.confirmedEndedAtMs > event.atMs)) invalid('confirmed end is outside the observed range');
}

/** Collapse overlapping confirmed work before computing the task or actor time. */
function unionLength(intervals: readonly ConfirmedInterval[]): number {
  let sum = 0;
  let end = 0;
  for (const item of intervals.toSorted((left, right) => left.startMs - right.startMs)) {
    sum += Math.max(0, item.endMs - Math.max(end, item.startMs));
    end = Math.max(end, item.endMs);
  }
  return sum;
}

/** Replay scoped journal receipts in order. Journal persistence and dispatch are separate consumers. */
export function projectTaskTime(scope: TaskTimeScope, events: readonly TaskTimeEvent[]): TaskTimeProjection {
  if (!nonempty(scope.projectId) || !nonempty(scope.taskId)) invalid('task scope is required');
  const seenEvents = new Map<string, string>();
  const sequences = new Map<number, string>();
  const intervals = new Map<string, Interval>();
  const activeAgents = new Set<string>();
  for (const event of events.toSorted((left, right) => left.seq - right.seq)) {
    validate(scope, event);
    const sequenceOwner = sequences.get(event.seq);
    if (sequenceOwner !== undefined && sequenceOwner !== event.eventId) invalid('sequence is reused by another event');
    sequences.set(event.seq, event.eventId);

    // A re-delivery may carry another journal sequence while retaining the same source event ID.
    const detail = event.kind === 'interval_stopped' ? event.reason
      : event.kind === 'interval_reconciled' ? event.confirmedEndedAtMs : null;
    const fingerprint = JSON.stringify([event.intervalId, event.runId, event.actorId, event.source, event.kind, event.atMs, detail]);
    const previous = seenEvents.get(event.eventId);
    if (previous !== undefined) {
      if (previous !== fingerprint) invalid('event ID is reused with a different payload');
      continue;
    }
    seenEvents.set(event.eventId, fingerprint);

    const interval = intervals.get(event.intervalId);
    const agentKey = JSON.stringify([event.runId, event.actorId]);
    if (event.kind === 'interval_started') {
      if (interval || activeAgents.has(agentKey)) invalid('agent already has an active interval or reused its ID');
      intervals.set(event.intervalId, {
        actorId: event.actorId, runId: event.runId, startMs: event.atMs, endMs: null, crashObservedAtMs: null,
      });
      activeAgents.add(agentKey);
      continue;
    }
    if (!interval || interval.endMs !== null || event.atMs < interval.startMs
      || interval.actorId !== event.actorId || interval.runId !== event.runId) {
      invalid('event does not match an open or unresolved interval');
    }
    if (event.kind === 'interval_reconciled') {
      if (interval.crashObservedAtMs === null || event.atMs < interval.crashObservedAtMs || event.confirmedEndedAtMs < interval.startMs) {
        invalid('reconciliation does not confirm the end of an unresolved interval');
      }
      // A retry may already be active for this actor. Resolving the old interval must not close it.
      interval.endMs = event.confirmedEndedAtMs;
      continue;
    }
    if (interval.crashObservedAtMs !== null) invalid('unresolved interval requires reconciliation');
    switch (event.kind) {
      case 'interval_crashed':
        interval.crashObservedAtMs = event.atMs;
        break;
      case 'interval_stopped':
        interval.endMs = event.atMs;
        break;
      default:
        invalid('unsupported interval event');
    }
    activeAgents.delete(agentKey);
  }

  const confirmed: ConfirmedInterval[] = [];
  const perAgent = new Map<string, ConfirmedInterval[]>();
  let unresolvedIntervalCount = 0;
  for (const interval of intervals.values()) {
    if (interval.endMs === null) {
      if (interval.crashObservedAtMs !== null) unresolvedIntervalCount++;
      continue;
    }
    const item = { startMs: interval.startMs, endMs: interval.endMs };
    confirmed.push(item);
    const effort = perAgent.get(interval.actorId) ?? [];
    effort.push(item);
    perAgent.set(interval.actorId, effort);
  }
  const confirmedElapsedMs = unionLength(confirmed);
  const confirmedAgentEffortMs = [...perAgent.values()].reduce((total, work) => total + unionLength(work), 0);
  if (!Number.isSafeInteger(confirmedAgentEffortMs)) invalid('confirmed agent effort exceeds safe range');
  return {
    actualDurationMs: confirmed.length > 0 && activeAgents.size === 0 && unresolvedIntervalCount === 0 ? confirmedElapsedMs : null,
    confirmedElapsedMs,
    confirmedAgentEffortMs,
    openIntervalCount: activeAgents.size,
    unresolvedIntervalCount,
  };
}
