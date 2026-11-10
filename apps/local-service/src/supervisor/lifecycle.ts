import { withinDeadline } from './deadline.ts';

type DrainOutcome = 'acknowledged' | 'unknown';
export type StopOutcome = Readonly<
  | { status: 'stopped' | 'stopped_recovery_required' }
  | { status: 'stop_blocked'; phase: 'record_recovery' | 'stop_children' }
>;
type QuitAction = 'stop' | 'keep_running' | 'cancel';
type QuitOutcome = StopOutcome | Readonly<{ status: 'kept_running' | 'cancelled' }>;

export type SupervisorPorts = Readonly<{
  // Close dispatch first. Acknowledged means active runs acknowledged interruption and known outcomes are durable.
  interruptAndDrain: (signal: AbortSignal) => Promise<DrainOutcome>;
  // Acknowledgement means the recovery receipt is durable. A retry must preserve one receipt per stop.
  recordRecovery: (signal: AbortSignal) => Promise<void>;
  // Completion means all owned children exited. Retrying a partially completed shutdown is safe.
  stopChildren: (signal: AbortSignal) => Promise<void>;
}>;

/** Coordinate a user-issued Quit while preserving uncertain outcomes before child shutdown. */
export function createServiceSupervisor(ports: SupervisorPorts, timeout = 10_000) {
  let drain: DrainOutcome | undefined;
  let recoveryRecorded = false;
  let pending: Promise<StopOutcome> | undefined;
  let last: StopOutcome | undefined;

  // A retry continues at the failed step. It never dispatches a second interrupt for the same Quit.
  async function stop(): Promise<StopOutcome> {
    if (drain === undefined) {
      try {
        const observed = await withinDeadline(timeout, (signal) => ports.interruptAndDrain(signal));
        drain = observed === 'acknowledged' ? observed : 'unknown';
      } catch {
        drain = 'unknown';
      }
    }
    if (drain === 'unknown' && !recoveryRecorded) {
      try {
        await withinDeadline(timeout, (signal) => ports.recordRecovery(signal));
        recoveryRecorded = true;
      } catch {
        return { status: 'stop_blocked', phase: 'record_recovery' };
      }
    }
    try {
      await withinDeadline(timeout, (signal) => ports.stopChildren(signal));
    } catch {
      return { status: 'stop_blocked', phase: 'stop_children' };
    }
    return { status: drain === 'unknown' ? 'stopped_recovery_required' : 'stopped' };
  }

  /** Keep-running and cancel are valid decisions only until the service starts draining. */
  function quit(): Promise<StopOutcome>;
  function quit(action: QuitAction): Promise<QuitOutcome>;
  function quit(action: QuitAction = 'stop'): Promise<QuitOutcome> {
    if (pending) return pending;
    if (last && (last.status !== 'stop_blocked' || action !== 'stop')) return Promise.resolve(last);
    if (action !== 'stop') return Promise.resolve({ status: action === 'keep_running' ? 'kept_running' : 'cancelled' });

    pending = stop().then((outcome) => {
      last = outcome;
      pending = undefined;
      return outcome;
    });
    return pending;
  }

  return { quit };
}
