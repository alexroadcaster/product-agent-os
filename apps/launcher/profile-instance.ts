import { randomUUID } from 'node:crypto';
import { lstat, mkdir, open, realpath, rename, rmdir, unlink } from 'node:fs/promises';
import type { BigIntStats } from 'node:fs';
import { isAbsolute, join } from 'node:path';
import type { StopOutcome } from '../local-service/src/supervisor/lifecycle.ts';
import { InstanceClaimError, type LauncherPorts, type RuntimeStatus, type ServiceHealth } from './launcher.ts';

const LOCK_NAME = 'service-instance';
const RECORD_NAME = 'endpoint.json';
const PENDING_NAME = 'endpoint.next';
const MAX_RECORD_BYTES = 256;

type Descriptor = Readonly<{ instanceId: string; port: number }>;
type StartedService = Readonly<{ status: 'started'; port: number; quit: () => Promise<StopOutcome> }>;
type InstanceHost = Readonly<{
  // Return not_started only when there is positive evidence no owned service is running.
  startService: (input: Readonly<{ instanceId: string; runtime: RuntimeStatus }>, signal: AbortSignal) =>
    Promise<StartedService | Readonly<{ status: 'not_started' }>>;
  readHealth: (endpoint: Descriptor, signal: AbortSignal) => Promise<ServiceHealth>;
}>;

function errorCode(error: unknown): string | undefined {
  return (error as NodeJS.ErrnoException | null)?.code;
}

function sameIdentity(first: BigIntStats, current: BigIntStats): boolean {
  return first.ino !== 0n && first.ino === current.ino && first.dev === current.dev;
}

function validPort(port: unknown): port is number {
  return typeof port === 'number' && Number.isInteger(port) && port > 0 && port <= 65535;
}

function localAbsolutePath(path: string): boolean {
  return process.platform === 'win32' ? /^[a-z]:[\\/]/i.test(path) : isAbsolute(path);
}

async function directoryIdentity(path: string): Promise<BigIntStats> {
  const info = await lstat(path, { bigint: true });
  if (!info.isDirectory() || info.isSymbolicLink() || info.ino === 0n) {
    throw new InstanceClaimError('invalid_instance_record');
  }
  return info;
}

async function assertOwnership(path: string, identity: BigIntStats): Promise<void> {
  if (!sameIdentity(identity, await directoryIdentity(path))) {
    throw new InstanceClaimError('invalid_instance_record');
  }
}

/** Read a complete, bounded endpoint record without interpreting a partial or linked file. */
async function readPublishedEndpoint(lock: string): Promise<Descriptor> {
  try {
    const identity = await directoryIdentity(lock);
    const record = join(lock, RECORD_NAME);
    const entry = await lstat(record, { bigint: true });
    if (!entry.isFile() || entry.nlink !== 1n || entry.size > BigInt(MAX_RECORD_BYTES)) {
      throw new InstanceClaimError('invalid_instance_record');
    }
    const file = await open(record, 'r');
    let decoded: Partial<Descriptor> | null;
    try {
      const info = await file.stat({ bigint: true });
      if (!sameIdentity(entry, info) || info.size !== entry.size) {
        throw new InstanceClaimError('invalid_instance_record');
      }
      const buffer = Buffer.alloc(MAX_RECORD_BYTES + 1);
      const { bytesRead } = await file.read(buffer, 0, buffer.length, 0);
      if (BigInt(bytesRead) !== info.size) throw new InstanceClaimError('invalid_instance_record');
      decoded = JSON.parse(buffer.toString('utf8', 0, bytesRead));
    } finally {
      await file.close();
    }
    await assertOwnership(lock, identity);
    if (typeof decoded?.instanceId !== 'string' || !/^[\da-f]{8}(?:-[\da-f]{4}){3}-[\da-f]{12}$/i.test(decoded.instanceId)
      || !validPort(decoded.port)) {
      throw new InstanceClaimError('invalid_instance_record');
    }
    return { instanceId: decoded.instanceId, port: decoded.port };
  } catch (error) {
    if (error instanceof InstanceClaimError) throw error;
    throw new InstanceClaimError(errorCode(error) === 'ENOENT' ? 'startup_unresolved' : 'invalid_instance_record');
  }
}

/** Atomic rename publishes the endpoint only after a complete record has been written and synced. */
async function publishEndpoint(lock: string, identity: BigIntStats, endpoint: Descriptor): Promise<void> {
  await assertOwnership(lock, identity);
  const pending = join(lock, PENDING_NAME);
  const file = await open(pending, 'wx', 0o600);
  try {
    await file.writeFile(JSON.stringify(endpoint), 'utf8');
    await file.sync();
  } finally {
    await file.close();
  }
  await assertOwnership(lock, identity);
  await rename(pending, join(lock, RECORD_NAME));
}

/** A release removes only its generation's own files. An interrupted release leaves a blocking reservation. */
async function removeReservation(lock: string, identity: BigIntStats): Promise<void> {
  await assertOwnership(lock, identity);
  for (const name of [RECORD_NAME, PENDING_NAME]) {
    try {
      await unlink(join(lock, name));
    } catch (error) {
      if (errorCode(error) !== 'ENOENT') throw error;
    }
  }
  await assertOwnership(lock, identity);
  await rmdir(lock);
}

/** Keep the on-disk reservation fenced until a definitive start failure or acknowledged service shutdown. */
function ownReservation(lock: string, identity: BigIntStats, host: InstanceHost) {
  const instanceId = randomUUID();
  let phase: 'reserved' | 'starting' | 'live' | 'stopped' | 'releasing' | 'released' = 'reserved';
  let releasing: Promise<void> | undefined;

  function release(signal: AbortSignal): Promise<void> {
    if (releasing) return releasing;
    if (phase === 'released') return Promise.resolve();
    if (phase === 'starting' || phase === 'live') throw new InstanceClaimError('startup_unresolved');
    signal.throwIfAborted();
    phase = 'releasing';
    releasing = removeReservation(lock, identity).then(() => { phase = 'released'; }).finally(() => { releasing = undefined; });
    return releasing;
  }

  /** A thrown or interrupted host start is uncertain unless the host explicitly reports no child. */
  async function start(runtime: RuntimeStatus, signal: AbortSignal) {
    signal.throwIfAborted();
    if (phase !== 'reserved') throw new InstanceClaimError('startup_unresolved');
    phase = 'starting';
    const child = await host.startService({ instanceId, runtime }, signal);
    if (child.status === 'not_started') {
      phase = 'stopped';
      if (signal.aborted) await release(new AbortController().signal);
      throw new Error('The local service did not start.');
    }
    const startedChild = child;
    phase = 'live';
    let stopping: Promise<StopOutcome> | undefined;
    let terminal: StopOutcome | undefined;

    async function stopAndRelease(): Promise<StopOutcome> {
      let stoppedOutcome = terminal;
      if (!stoppedOutcome) {
        const outcome = await startedChild.quit();
        if (outcome.status === 'stop_blocked') return outcome;
        terminal = outcome; stoppedOutcome = outcome;
        phase = 'stopped';
      }
      await release(new AbortController().signal);
      return stoppedOutcome;
    }

    function quit(): Promise<StopOutcome> {
      stopping ??= stopAndRelease().finally(() => { stopping = undefined; });
      return stopping;
    }

    const endpoint = { instanceId, port: child.port };
    try {
      signal.throwIfAborted();
      if (!validPort(endpoint.port)) throw new Error('Invalid local service port.');
      await publishEndpoint(lock, identity, endpoint);
      signal.throwIfAborted();
    } catch (error) {
      // A late or partially published child may still be alive. Only a successful Quit releases its reservation.
      await quit();
      throw error;
    }
    return { ...endpoint, health: (healthSignal: AbortSignal) => host.readHealth(endpoint, healthSignal), quit };
  }

  return { kind: 'owner' as const, start, release };
}

/** Attach per-profile election to LauncherPorts. The host creates a private profile on the local filesystem. */
export function createProfileInstanceClaimer(profileDirectory: string, host: InstanceHost): LauncherPorts['claimInstance'] {
  return async (signal) => {
    signal.throwIfAborted();
    if (!localAbsolutePath(profileDirectory)) throw new InstanceClaimError('invalid_instance_record');
    const profile = await realpath(profileDirectory);
    if (!localAbsolutePath(profile)) throw new InstanceClaimError('invalid_instance_record');
    await directoryIdentity(profile);
    const lock = join(profile, LOCK_NAME);
    try {
      await mkdir(lock, { mode: 0o700 });
    } catch (error) {
      if (errorCode(error) !== 'EEXIST') throw error;
      const endpoint = await readPublishedEndpoint(lock);
      signal.throwIfAborted();
      return { kind: 'existing', service: { ...endpoint, health: (healthSignal) => host.readHealth(endpoint, healthSignal) } };
    }
    const identity = await directoryIdentity(lock);
    const claim = ownReservation(lock, identity, host);
    if (signal.aborted) {
      await claim.release(new AbortController().signal);
      signal.throwIfAborted();
    }
    return claim;
  };
}
