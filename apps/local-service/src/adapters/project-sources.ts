import { lstat, open, realpath, stat } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { isAbsolute, join } from 'node:path';
import type {
  ListRuntimeThreads, ProjectBinding, ProjectSourceCoverage, ProjectSourceId, ProjectSources,
} from '../../../../packages/contracts/project.ts';

const controlPlaneFiles = {
  instructions: 'AGENTS.md',
  requirements: 'REQUIREMENTS.md',
  plan: 'PLAN.md',
  test: 'TEST.md',
  evals: 'EVALS.md',
  runlog: 'RUNLOG.md',
} as const satisfies Partial<Record<ProjectSourceId, string>>;

function bindingError(code: 'PROJECT_NOT_FOUND' | 'PROJECT_ROOT_UNAVAILABLE'): Error {
  const message = code === 'PROJECT_NOT_FOUND'
    ? 'The requested project is unavailable.'
    : 'The registered project directory is unavailable or changed.';
  return Object.assign(new Error(message), { code });
}

async function directoryIdentity(root: string): Promise<string> {
  const info = await stat(root, { bigint: true });
  if (!info.isDirectory() || info.ino === 0n) {
    throw bindingError('PROJECT_ROOT_UNAVAILABLE');
  }
  return `${info.dev}:${info.ino}`;
}

function isLocalAbsolutePath(path: string): boolean {
  return process.platform === 'win32' ? /^[a-z]:[\\/]/i.test(path) : isAbsolute(path);
}

/** Register a directory selected by the local service, independently of the client project ID lookup. */
export async function bindProject(projectId: string, workspaceRoot: string): Promise<ProjectBinding> {
  if (!projectId.trim() || !isLocalAbsolutePath(workspaceRoot)) {
    throw bindingError('PROJECT_ROOT_UNAVAILABLE');
  }
  try {
    const canonicalRoot = await realpath(workspaceRoot);
    if (!isLocalAbsolutePath(canonicalRoot)) {
      throw bindingError('PROJECT_ROOT_UNAVAILABLE');
    }
    return { projectId, workspaceRoot: canonicalRoot, directoryIdentity: await directoryIdentity(canonicalRoot) };
  } catch {
    throw bindingError('PROJECT_ROOT_UNAVAILABLE');
  }
}

async function assertCurrentBinding(binding: ProjectBinding): Promise<void> {
  const current = await bindProject(binding.projectId, binding.workspaceRoot);
  if (current.workspaceRoot !== binding.workspaceRoot || current.directoryIdentity !== binding.directoryIdentity) {
    throw bindingError('PROJECT_ROOT_UNAVAILABLE');
  }
}

/** Read fixed source names through a checked handle. The digest identifies raw bytes; display text may be redacted. */
export async function readProjectSource(binding: ProjectBinding, sourceId: string) {
  const relativePath = Object.entries(controlPlaneFiles).find(([id, file]) => id === sourceId || file === sourceId)?.[1];
  const fail = (code: string): never => { throw Object.assign(new Error('The requested source is unavailable.'), { code }); };
  if (!relativePath) return fail('SOURCE_NOT_FOUND');
  await assertCurrentBinding(binding);
  const path = join(binding.workspaceRoot, relativePath);
  const before = await lstat(path, { bigint: true }).catch(() => fail('SOURCE_UNAVAILABLE'));
  if (!before.isFile() || before.isSymbolicLink() || before.nlink !== 1n) fail('SOURCE_UNAVAILABLE');
  const limit = 1024 * 1024;
  if (before.size > BigInt(limit)) fail('SOURCE_TOO_LARGE');
  const handle = await open(path, 'r').catch(() => fail('SOURCE_UNAVAILABLE'));
  try {
    const opened = await handle.stat({ bigint: true });
    if (opened.dev !== before.dev || opened.ino !== before.ino || opened.nlink !== 1n) fail('SOURCE_UNAVAILABLE');
    const bytes = Buffer.alloc(limit + 1);
    let count = 0;
    while (count < bytes.length) {
      const result = await handle.read(bytes, count, bytes.length - count, count);
      if (!result.bytesRead) break;
      count += result.bytesRead;
    }
    const after = await handle.stat({ bigint: true });
    const current = await lstat(path, { bigint: true });
    await assertCurrentBinding(binding);
    if (count > limit) fail('SOURCE_TOO_LARGE');
    if (after.dev !== opened.dev || after.ino !== opened.ino || after.size !== BigInt(count)
      || after.mtimeNs !== before.mtimeNs || after.ctimeNs !== before.ctimeNs || after.nlink !== 1n
      || current.isSymbolicLink() || current.ino !== opened.ino || current.dev !== opened.dev || current.nlink !== 1n
      || current.size !== after.size || current.mtimeNs !== after.mtimeNs || current.ctimeNs !== after.ctimeNs) fail('SOURCE_CHANGED');
    const text = (() => {
      try { return new TextDecoder('utf-8', { fatal: true }).decode(bytes.subarray(0, count)); }
      catch { return fail('SOURCE_ENCODING_INVALID'); }
    })();
    const content = text.replace(/sk-[A-Za-z0-9_-]+/g, '[REDACTED]')
      .replace(/^(\s*(?:OPENAI_API_KEY|ANTHROPIC_API_KEY|AWS_SECRET_ACCESS_KEY|PRIVATE_KEY|ACCESS_TOKEN)\s*[:=]).+$/gim, '$1 [REDACTED]');
    return { relativePath, content, sha256: createHash('sha256').update(bytes.subarray(0, count)).digest('hex'),
      coverage: 'complete' as const, redacted: content !== text };
  } finally { await handle.close(); }
}

/** Inventory only fixed control-plane paths. Linked content may belong to another project. */
async function inspectControlPlaneFile(
  root: string,
  id: ProjectSourceId,
  relativePath: string,
): Promise<ProjectSourceCoverage> {
  const source = { id, relativePath };
  try {
    const info = await lstat(join(root, relativePath));
    if (info.isSymbolicLink() || (info.isFile() && info.nlink > 1)) {
      return { ...source, status: 'excluded', reason: 'linked_file' };
    }
    if (!info.isFile()) {
      return { ...source, status: 'excluded', reason: 'unsupported_file' };
    }
    return { ...source, status: 'available' };
  } catch (error) {
    const reason = (error as NodeJS.ErrnoException).code === 'ENOENT' ? 'missing' : 'unreadable';
    return { ...source, status: 'unavailable', reason };
  }
}

/** Use the native filter and independently check the canonical binding before counting any thread. */
async function inspectRuntimeHistory(root: string, listThreads?: ListRuntimeThreads): Promise<ProjectSourceCoverage> {
  const id = 'runtimeHistory';
  if (!listThreads) {
    return { id, status: 'unavailable', reason: 'runtime_not_connected' };
  }
  try {
    const limit = 50;
    const result = await listThreads({ cwd: root, sourceKinds: ['cli', 'vscode', 'appServer'], modelProviders: [], limit });
    const page = result as { data?: unknown; nextCursor?: unknown } | null;
    if (!page || !Array.isArray(page.data) || page.data.length > limit
      || (page.nextCursor != null && (typeof page.nextCursor !== 'string' || page.nextCursor.length === 0))) {
      return { id, status: 'unavailable', reason: 'runtime_history_unreadable' };
    }
    const inScope = new Set<string>();
    const excluded = new Set<string>();
    for (const value of page.data) {
      const row = value as { id?: unknown; cwd?: unknown } | null;
      if (!row || typeof row.id !== 'string' || !row.id || typeof row.cwd !== 'string') {
        return { id, status: 'unavailable', reason: 'runtime_history_unreadable' };
      }
      // Exact comparison rejects aliases and cross-project rows without opening host-supplied paths.
      (row.cwd === root ? inScope : excluded).add(row.id);
    }
    for (const foreignId of excluded) {
      inScope.delete(foreignId);
    }
    return {
      id, status: 'partial', reason: excluded.size ? 'runtime_scope_mismatch' : 'persisted_threads_only',
      visibleThreadCount: inScope.size, hasMore: Boolean(page.nextCursor),
    };
  } catch {
    return { id, status: 'unavailable', reason: 'runtime_history_unreadable' };
  }
}

/** Inventory metadata for a trusted registry binding without returning file content or absolute paths. */
export async function inspectProjectSources(
  binding: ProjectBinding,
  requestedProjectId: string,
  listThreads?: ListRuntimeThreads,
): Promise<ProjectSources> {
  if (binding.projectId !== requestedProjectId) {
    throw bindingError('PROJECT_NOT_FOUND');
  }
  await assertCurrentBinding(binding);
  const entries = Object.entries(controlPlaneFiles) as [keyof typeof controlPlaneFiles, string][];
  const sources = await Promise.all([
    ...entries.map(([id, file]) => inspectControlPlaneFile(binding.workspaceRoot, id, file)),
    inspectRuntimeHistory(binding.workspaceRoot, listThreads),
  ]);
  await assertCurrentBinding(binding);
  return { projectId: binding.projectId, sources };
}
