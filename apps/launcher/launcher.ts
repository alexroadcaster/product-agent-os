import { LifecycleDeadlineError, withinDeadline } from '../local-service/src/supervisor/deadline.ts';
import type { StopOutcome } from '../local-service/src/supervisor/lifecycle.ts';

export type RuntimeFingerprint = Readonly<{ version: string; sha256: string }>;
export type RuntimeInspection = RuntimeFingerprint | null | Readonly<{status:'unverified'}>;
export type RuntimeStatus = 'runtime_candidate' | 'runtime_missing' | 'runtime_incompatible'
  | 'runtime_qualification_required' | 'runtime_probe_failed';

export type ServiceHealth = Readonly<{
  instanceId: string;
  build: string;
  alive: boolean;
  sourceReaderReady: boolean;
  runtimeCapable: boolean;
}>;

type ServiceEndpoint = Readonly<{
  instanceId: string;
  port: number;
  health: (signal: AbortSignal) => Promise<ServiceHealth>;
}>;

type LocalService = ServiceEndpoint & Readonly<{
  quit: () => Promise<StopOutcome>;
}>;

type Claim = Readonly<
  | { kind: 'existing'; service: ServiceEndpoint }
  | {
    kind: 'owner';
    // An adapter must refuse release while a partial or timed-out start could have left a service alive.
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
type InstanceReason = 'startup_unresolved' | 'invalid_instance_record';

export class InstanceClaimError extends Error {
  readonly reason: InstanceReason;

  constructor(reason: InstanceReason) {
    super('The local service instance needs reconciliation.');
    this.reason = reason;
  }
}

export type LauncherPorts = Readonly<{
  inspectRuntime: (signal: AbortSignal) => Promise<RuntimeInspection>;
  // The platform adapter atomically reserves this profile through the service lifetime, including during startup.
  claimInstance: (signal: AbortSignal) => Promise<Claim>;
  // Native controls stay in the launcher host; browser state contains only the Opened receipt.
  openUi: (origin: string, state: Opened, signal: AbortSignal, owner?: OwnedLauncherControls) => Promise<void>;
}>;

export type OwnedLauncherControls = Readonly<{ quit: () => Promise<StopOutcome> }>;

/** Only an exact configured version and fingerprint can become a candidate; this does not activate a connection. */
async function inspectRuntime(
  inspect: LauncherPorts['inspectRuntime'],
  expected: RuntimeFingerprint | null,
  timeout: number,
): Promise<RuntimeStatus> {
  try {
    const installed = await withinDeadline(timeout, inspect);
    if(installed&&'status' in installed)return 'runtime_qualification_required';
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
): Promise<Opened | { status: Failure; cleanupPending?: true; instanceReason?: InstanceReason }> {
  let claim: Claim | undefined;
  let ownedService: LocalService | undefined;
  let phase: Failure = 'instance_unavailable';
  try {
    claim = await withinDeadline(timeout, (signal) => ports.claimInstance(signal));
    const runtime = await inspectRuntime((signal) => ports.inspectRuntime(signal), expected.runtime, timeout);
    phase = 'service_start_failed';
    let current: ServiceEndpoint;
    if (claim.kind === 'owner') {
      const owner = claim;
      ownedService = await withinDeadline(timeout, (signal) => owner.start(runtime, signal));
      current = ownedService;
    } else {
      current = claim.service;
    }

    phase = 'service_unhealthy';
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
    const owner = ownedService ? { quit: ownedService.quit.bind(ownedService) } : undefined;
    await withinDeadline(timeout, (signal) => ports.openUi(state.origin, state, signal, owner));
    return state;
  } catch (error) {
    if (phase === 'instance_unavailable' && error instanceof InstanceClaimError) {
      return { status: phase, instanceReason: error.reason };
    }
    if (claim?.kind === 'owner') {
      if (phase === 'service_start_failed' && error instanceof LifecycleDeadlineError) {
        return { status: phase, cleanupPending: true };
      }
      try {
        if (ownedService) {
          const current = ownedService;
          const stopped = await withinDeadline(timeout * 3, () => current.quit());
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
