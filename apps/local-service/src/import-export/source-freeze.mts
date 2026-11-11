import { spawn, type ChildProcessWithoutNullStreams } from 'node:child_process';
import { win32, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { performance } from 'node:perf_hooks';

export type SourceFreezeInput = Readonly<{ workspaceRoot: string; sourceRelativePath: string }>;
export type FrozenSource = Readonly<{ sha256: string; byteSize: number; signal: AbortSignal; assertHeld(): void }>;
export type SourceFreezeLease = Readonly<{
  sha256: string; byteSize: number; closed: Promise<{ code: number | null }>;
  release(): Promise<void>; terminate(): Promise<void>;
}>;
export type SourceFreezeBridge = (input: { workspaceRoot: string; sourcePath: string }, signal: AbortSignal) => Promise<SourceFreezeLease>;
type Launch = (executable: string, arguments_: string[], options: Parameters<typeof spawn>[2]) => ChildProcessWithoutNullStreams;

function failure(code: string) { return Object.assign(new Error(code), { code }); }
function validate(input: SourceFreezeInput) {
  if (!input || typeof input.workspaceRoot !== 'string' || !/^[a-z]:[\\/]/i.test(input.workspaceRoot)
    || /[\u0000-\u001f]/.test(input.workspaceRoot) || typeof input.sourceRelativePath !== 'string'
    || !input.sourceRelativePath || input.sourceRelativePath.length > 4096) throw failure('SOURCE_PATH_INVALID');
  const parts = input.sourceRelativePath.split(/[\\/]/);
  if (parts.some(part => !part || part === '.' || part === '..' || /[\u0000-\u001f:<>"|?*]/.test(part) || /[. ]$/.test(part)
    || /^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)/i.test(part))) throw failure('SOURCE_PATH_INVALID');
  const workspaceRoot = win32.resolve(input.workspaceRoot);
  const sourcePath = win32.resolve(workspaceRoot, ...parts);
  if (!sourcePath.toLowerCase().startsWith(workspaceRoot.replace(/\\$/, '').toLowerCase() + '\\')) throw failure('SOURCE_PATH_INVALID');
  return { workspaceRoot, sourcePath };
}
function validObservation(value: unknown): value is { sha256: string; byteSize: number } {
  const source = value as { sha256?: unknown; byteSize?: unknown };
  return Boolean(source && typeof source === 'object' && Object.keys(source).length === 2
    && typeof source.sha256 === 'string' && /^[0-9a-f]{64}$/.test(source.sha256)
    && Number.isSafeInteger(source.byteSize) && (source.byteSize as number) >= 0 && (source.byteSize as number) <= 1024 * 1024);
}

/** Lazy Windows helper. Only canonical paths enter stdin; stdout contains no source text. */
export function nativeSourceFreezeBridge(input: Parameters<SourceFreezeBridge>[0], signal: AbortSignal,
  dependencies: { launch?: Launch } = {}): ReturnType<SourceFreezeBridge> {
  if ((!dependencies.launch && process.platform !== 'win32') || !process.env.SystemRoot) return Promise.reject(failure('SOURCE_FREEZE_UNAVAILABLE'));
  if (signal.aborted) return Promise.reject(signal.reason);
  const executable = join(process.env.SystemRoot, 'System32', 'WindowsPowerShell', 'v1.0', 'powershell.exe');
  const script = fileURLToPath(new URL('./source-freeze.ps1', import.meta.url));
  return new Promise((accept, reject) => {
    const child = (dependencies.launch ?? spawn)(executable, ['-NoLogo', '-NoProfile', '-NonInteractive', '-File', script], {
      windowsHide: true, shell: false, stdio: ['pipe', 'pipe', 'ignore'],
      env: { SystemRoot: process.env.SystemRoot, TEMP: process.env.TEMP, TMP: process.env.TMP },
    }) as ChildProcessWithoutNullStreams;
    let ready = false;
    let startupFailure: Error | undefined;
    let output = '';
    let resolveClosed!: (value: { code: number | null }) => void;
    const closed = new Promise<{ code: number | null }>(resolve => { resolveClosed = resolve; });
    const stop = (error: Error) => { startupFailure = error; child.stdin.destroy(); child.kill(); closed.then(() => reject(error)); };
    const abort = () => stop(signal.reason ?? failure('SOURCE_FREEZE_LOST'));
    signal.addEventListener('abort', abort, { once: true });
    child.once('close', code => {
      signal.removeEventListener('abort', abort);
      resolveClosed({ code });
      if (!ready) reject(startupFailure ?? failure('SOURCE_FREEZE_UNAVAILABLE'));
    });
    child.once('error', () => stop(failure('SOURCE_FREEZE_UNAVAILABLE')));
    child.stdin.on('error', () => stop(failure('SOURCE_FREEZE_LOST')));
    child.stdout.setEncoding('utf8');
    child.stdout.on('data', (chunk: string) => {
      output += chunk;
      if (Buffer.byteLength(output) > 1024 || (ready && output.trim())) {
        stop(failure('SOURCE_FREEZE_PROTOCOL_INVALID')); return;
      }
      if (ready || !output.includes('\n')) return;
      try {
        const value = JSON.parse(output.trim());
        if (!validObservation(value)) throw failure('SOURCE_FREEZE_PROTOCOL_INVALID');
        ready = true; output = '';
        accept({ ...value, closed,
          async release() {
            child.stdin.end('release\n');
            if ((await closed).code !== 0) throw failure('SOURCE_FREEZE_RELEASE_FAILED');
          },
          async terminate() { child.stdin.destroy(); child.kill(); await closed; },
        });
      } catch { stop(failure('SOURCE_FREEZE_PROTOCOL_INVALID')); }
    });
    child.stdin.write(JSON.stringify(input) + '\n');
  });
}

/** A cooperative callback must assertHeld immediately before its irreversible commit. */
export async function withFrozenSource<T>(input: SourceFreezeInput, operation: (source: FrozenSource) => Promise<T>,
  options: { bridge?: SourceFreezeBridge; timeoutMs?: number } = {}): Promise<T> {
  const normalized = validate(input);
  const timeoutMs = options.timeoutMs ?? 30000;
  if (!Number.isInteger(timeoutMs) || timeoutMs < 1 || timeoutMs > 30000) throw failure('SOURCE_FREEZE_TIMEOUT_INVALID');
  const controller = new AbortController();
  const deadline = performance.now() + timeoutMs;
  const timeout = setTimeout(() => controller.abort(failure('SOURCE_FREEZE_TIMEOUT')), timeoutMs);
  let lease: SourceFreezeLease | undefined;
  let held = false;
  let releasing = false;
  let released = false;
  let releaseAttempted = false;
  const interrupted = new Promise<never>((_, reject) => controller.signal.addEventListener('abort', () => reject(controller.signal.reason), { once: true }));
  // The abort promise may reject while startup is still waiting for the bridge.
  interrupted.catch(() => {});
  async function cleanup(action: () => Promise<void>) {
    let timer: ReturnType<typeof setTimeout>;
    try { await Promise.race([action(), new Promise<never>((_, reject) => { timer = setTimeout(() => reject(failure('SOURCE_FREEZE_CLEANUP_FAILED')), 2000); })]); }
    finally { clearTimeout(timer!); }
  }
  try {
    lease = await (options.bridge ?? nativeSourceFreezeBridge)(normalized, controller.signal);
    if (!validObservation({ sha256: lease.sha256, byteSize: lease.byteSize })) throw failure('SOURCE_FREEZE_PROTOCOL_INVALID');
    held = true;
    lease.closed.then(() => { held = false; if (!releasing) controller.abort(failure('SOURCE_FREEZE_LOST')); }, () => controller.abort(failure('SOURCE_FREEZE_LOST')));
    const assertHeld = () => {
      if (performance.now() >= deadline && !controller.signal.aborted) controller.abort(failure('SOURCE_FREEZE_TIMEOUT'));
      if (controller.signal.aborted) throw controller.signal.reason;
      if (!held) throw failure('SOURCE_FREEZE_LOST');
    };
    assertHeld();
    const result = await Promise.race([operation({ sha256: lease.sha256, byteSize: lease.byteSize, signal: controller.signal, assertHeld }), interrupted]);
    assertHeld();
    releasing = true;
    releaseAttempted = true;
    await cleanup(() => lease!.release());
    released = true;
    return result;
  } finally {
    held = false; releasing = true; clearTimeout(timeout);
    if (lease && !released) {
      if (releaseAttempted) await cleanup(() => lease!.terminate());
      else {
        try { await cleanup(() => lease!.release()); }
        catch { await cleanup(() => lease!.terminate()); }
      }
    }
  }
}
