export type TaskTimeScope = Readonly<{ projectId: string; taskId: string }>;

type TaskTimeEventBase = TaskTimeScope & Readonly<{
  eventId: string;
  seq: number;
  intervalId: string;
  runId: string;
  actorId: string;
  source: string;
  /** UTC epoch milliseconds, measured by the authoritative event source. */
  atMs: number;
}>;

export type TaskTimeEvent = TaskTimeEventBase & (
  | { readonly kind: 'interval_started' }
  | { readonly kind: 'interval_stopped'; readonly reason: 'pause' | 'retry' | 'finished' }
  | { readonly kind: 'interval_crashed' }
  | { readonly kind: 'interval_reconciled'; readonly confirmedEndedAtMs: number }
);

export type TaskTimeProjection = Readonly<{
  actualDurationMs: number | null;
  confirmedElapsedMs: number;
  confirmedAgentEffortMs: number;
  openIntervalCount: number;
  unresolvedIntervalCount: number;
}>;
