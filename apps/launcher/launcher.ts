import { LifecycleDeadlineError, withinDeadline } from '../local-service/src/supervisor/deadline.ts';
import type { StopOutcome } from '../local-service/src/supervisor/lifecycle.ts';

export type RuntimeFingerprint = Readonly<{ version: string; sha256: string }>;
type RuntimeStatus = 'runtime_candidate' | 'runtime_missing' | 'runtime_incompatible'
  | 'runtime_qualification_required' | 'runtime_probe_failed';

type Health = Readonly<{
  instanceId: string;
  build: string;
  alive: boolean;
  sourceReaderReady: boolean;
  runtimeCapable: boolean;
}>;

type LocalService = Readonly<{
  instanceId: string;
  port: number;
  health: (signal: AbortSignal) => Promise<Health>;
  quit: () => Promise<StopOutcome>;
}>;

type Claim = Readonly<
  | { kind: 'existing'; service: LocalService }
  | {
    kind: 'owner';
    // A rejected start has cleaned up partial effects. A timed-out start keeps the reservation until reconciled.
    start: (runtime: RuntimeStatus, signal: AbortSignal) => Promise<LocalService>;
    release: (signal: AbortSignal) => Promise<void>;
  }
>;

type Opened = Readonly<{
  status: 'opened';
  origin: string;
  instance: 'started' | 'existing';
  runtime: RuntimeStatus | 'runtime_not_ready';
  sourceReaderReady: boolean;
}>;

type Failure = 'instance_unavailable' | 'service_start_failed' | 'service_unhealthy' | 'ui_open_failed';

export type LauncherPorts = Readonly<{
  inspectRuntime: (signal: AbortSignal) => Promise<RuntimeFingerprint | null>;
  // The platform adapter atomically reserves this profile through the service lifetime, including during startup.
  claimInstance: (signal: AbortSignal) => Promise<Claim>;
  openUi: (origin: string, state: Opened, signal: AbortSignal) => Promise<void>;
}>;

/** Only an exact configured version and fingerprint can become a candidate; this does not activate a connection. */
async function inspectRuntime(
  inspect: LauncherPorts['inspectRuntime'],
  expected: RuntimeFingerprint | null,
  timeout: number,
): Promise<RuntimeStatus> {
  try {
    const installed = await withinDeadline(timeout, inspect);
    if (!installed) return 'runtime_missing';
    if (!expected) return 'runtime_qualification_required';
    if (!expected.version || installed.version !== expected.version || !/^[a-f0-9]{64}$/i.test(expected.sha256)
      || installed.sha256.toLowerCase() !== expected.sha256.toLowerCase()) {
      return 'runtime_incompatible';
    }
    return 'runtime_candidate';
  } catch {
    return 'runtime_probe_failed';
  }
}

/** Start or reuse the trusted local instance. Only a healthy service of the expected build gets a UI window. */
export async function launch(
  ports: LauncherPorts,
  expected: Readonly<{ serviceBuild: string; runtime: RuntimeFingerprint | null }>,
  timeout = 10_000,
): Promise<Opened | { status: Failure; cleanupPending?: true }> {
  let claim: Claim | undefined;
  let service: LocalService | undefined;
  let phase: Failure = 'instance_unavailable';
  try {
    claim = await withinDeadline(timeout, (signal) => ports.claimInstance(signal));
    const runtime = await inspectRuntime((signal) => ports.inspectRuntime(signal), expected.runtime, timeout);
    phase = 'service_start_failed';
    if (claim.kind === 'owner') {
      const owner = claim;
      service = await withinDeadline(timeout, (signal) => owner.start(runtime, signal));
    } else {
      service = claim.service;
    }

    phase = 'service_unhealthy';
    const current = service;
    if (!Number.isInteger(current.port) || current.port < 1 || current.port > 65535 || !current.instanceId) {
      throw new Error('Invalid local service identity.');
    }
    const health = await withinDeadline(timeout, (signal) => current.health(signal));
    if (health.instanceId !== current.instanceId || health.build !== expected.serviceBuild || health.alive !== true
      || typeof health.sourceReaderReady !== 'boolean' || typeof health.runtimeCapable !== 'boolean') {
      throw new Error('Unexpected local service health response.');
    }

    const state: Opened = {
      status: 'opened', origin: `http://127.0.0.1:${current.port}`,
      instance: claim.kind === 'owner' ? 'started' : 'existing',
      runtime: runtime === 'runtime_candidate' && !health.runtimeCapable ? 'runtime_not_ready' : runtime,
      sourceReaderReady: health.sourceReaderReady,
    };
    phase = 'ui_open_failed';
    await withinDeadline(timeout, (signal) => ports.openUi(state.origin, state, signal));
    return state;
  } catch (error) {
    if (claim?.kind === 'owner') {
      if (phase === 'service_start_failed' && error instanceof LifecycleDeadlineError) {
        return { status: phase, cleanupPending: true };
      }
      try {
        if (service) {
          const ownedService = service;
          const stopped = await withinDeadline(timeout * 3, () => ownedService.quit());
          if (stopped.status === 'stop_blocked') return { status: phase, cleanupPending: true };
        }
        const owner = claim;
        await withinDeadline(timeout, (signal) => owner.release(signal));
      } catch {
        return { status: phase, cleanupPending: true };
      }
    }
    return { status: phase };
  }
}
