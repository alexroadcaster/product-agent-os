import { realpath, stat } from 'node:fs/promises';
import { isAbsolute } from 'node:path';
import {inventoryForProject,type SourceProject} from '../code-index/sources.mts';
import type {InventoryPolicy} from '../../../../packages/contracts/project-inventory.ts';
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
export async function readProjectSource(binding: ProjectBinding, sourceId: string, policy?:InventoryPolicy) {
  const relativePath = Object.entries(controlPlaneFiles).find(([id, file]) => id === sourceId || file === sourceId)?.[1];
  const fail = (code:string):never => {throw Object.assign(new Error('The requested source is unavailable.'),{code});};
  if(!relativePath)return fail('SOURCE_NOT_FOUND');
  const project:SourceProject={id:binding.projectId,canonicalRoot:binding.workspaceRoot,rootIdentity:binding.directoryIdentity,inventoryPolicy:policy};
  try{
    const file=await inventoryForProject(project).read(project,{path:relativePath,redactSensitive:true});
    return {relativePath,content:file.text,sha256:file.hash,coverage:'complete' as const,redacted:file.redacted===true};
  }catch(error){
    const code=(error as {code?:string}).code;
    if(code==='PROJECT_ROOT_UNAVAILABLE')throw error;
    return fail(code==='INVENTORY_FILE_TOO_LARGE'?'SOURCE_TOO_LARGE':code==='INVENTORY_ENCODING_UNSUPPORTED'?'SOURCE_ENCODING_INVALID':code==='INVENTORY_SOURCE_DRIFT'||code==='INVENTORY_REVISION_STALE'?'SOURCE_CHANGED':'SOURCE_UNAVAILABLE');
  }
}

/** Fixed control-plane sources are a projection of the same policy/identity boundary as Files. */
async function inspectControlPlaneFile(project:SourceProject,id:ProjectSourceId,relativePath:string):Promise<ProjectSourceCoverage>{
  const source={id,relativePath};
  try{
    const entry=await inventoryForProject(project).inspect(project,relativePath);
    if(entry.kind==='link')return {...source,status:'excluded',reason:'linked_file'};
    if(entry.kind!=='file')return {...source,status:'excluded',reason:'unsupported_file'};
    if(!entry.access.readable)return {...source,status:'excluded',reason:'policy_excluded',policyReason:entry.access.reason};
    return {...source,status:'available'};
  }catch(error){
    const code=(error as NodeJS.ErrnoException).code;
    if(code==='PROJECT_ROOT_UNAVAILABLE'||code==='INVENTORY_SOURCE_DRIFT')throw error;
    return {...source,status:'unavailable',reason:code==='ENOENT'?'missing':'unreadable'};
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
  policy?:InventoryPolicy,
): Promise<ProjectSources> {
  if (binding.projectId !== requestedProjectId) {
    throw bindingError('PROJECT_NOT_FOUND');
  }
  await assertCurrentBinding(binding);
  const entries = Object.entries(controlPlaneFiles) as [keyof typeof controlPlaneFiles, string][];
  const sources = await Promise.all([
    ...entries.map(([id, file]) => inspectControlPlaneFile({id:binding.projectId,canonicalRoot:binding.workspaceRoot,rootIdentity:binding.directoryIdentity,inventoryPolicy:policy}, id, file)),
    inspectRuntimeHistory(binding.workspaceRoot, listThreads),
  ]);
  await assertCurrentBinding(binding);
  return { projectId: binding.projectId, sources };
}
