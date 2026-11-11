import { Worker } from 'node:worker_threads';
import { isAbsolute } from 'node:path';
import type { BackupManifest, BlobReceipt, ListOptions, Project, PromoteLegacy, StoredEntity, StoreEventPage, StoreReceipt, StoreWrite } from '../../../../packages/contracts/storage/local-store.ts';
import type { M1TaskProfile } from '../../../../packages/contracts/tasks/m1-task-profile.ts';
export { pruneManagedBackups } from './snapshot.mts';

export type { Project, StoredEntity, StoreWrite } from '../../../../packages/contracts/storage/local-store.ts';

/** Dedicated DatabaseSync Worker. At most 100 requests may wait for its single writer. */
export async function openLocalStore(options: { databasePath: string }) {
  if (!isAbsolute(options.databasePath) || options.databasePath.startsWith('\\\\')) {
    throw Object.assign(new Error('An absolute local database path is required'), { code: 'INVALID_DATABASE_PATH' });
  }
  const worker = new Worker(new URL('./sqlite-worker.mts', import.meta.url), { workerData: options });
  let nextId = 1;
  let closed = false;
  let closing: Promise<void> | null = null;
  const pending = new Map<number, { resolve: (value: any) => void; reject: (error: Error) => void;
    onProgress?: (progress: { completed: number; total: number }) => void }>();
  function rejectAll(error: Error) {
    closed = true;
    for (const request of pending.values()) request.reject(error);
    pending.clear();
  }
  worker.on('message', ({ id, value, error, progress }) => {
    const request = pending.get(id);
    if (progress) { try { request?.onProgress?.(progress); } catch {} return; }
    pending.delete(id);
    if (error) request?.reject(Object.assign(new Error(error.message), { code: error.code }));
    else request?.resolve(value);
  });
  worker.on('error', rejectAll);
  worker.on('exit', () => rejectAll(Object.assign(new Error('Storage Worker closed'), { code: 'STORAGE_CLOSED' })));
  const ready = new Promise<void>((resolve, reject) => pending.set(0, { resolve, reject }));
  async function call<T>(method: string, params: unknown, onProgress?: (progress: { completed: number; total: number }) => void): Promise<T> {
    if (closed || closing) throw Object.assign(new Error('Storage is closed'), { code: 'STORAGE_CLOSED' });
    if (pending.size >= 100) throw Object.assign(new Error('Storage write queue is full'), { code: 'STORAGE_BUSY' });
    const id = nextId++;
    return new Promise<T>((resolve, reject) => {
      pending.set(id, { resolve, reject, onProgress });
      try { worker.postMessage({ id, method, params }); }
      catch (error) { pending.delete(id); reject(error as Error); }
    });
  }
  try { await ready; } catch (error) { await worker.terminate(); throw error; }
  return {
    registerProject: (project: Omit<Project, 'authorityEpoch'>) => call<Project>('registerProject', project),
    projects: () => call<Project[]>('projects', {}),
    project: (projectId: string) => call<Project | null>('project', { projectId }),
    exportTasks: (projectId: string) => call<{ project: Project; tasks: M1TaskProfile[]; generation: string; throughSeq: number }>('exportTasks', { projectId }),
    write: (command: StoreWrite) => call<StoreReceipt>('write', command),
    receipt: (projectId: string, idempotencyKey: string) => call<StoreReceipt | null>('receipt', { projectId, idempotencyKey }),
    get: (projectId: string, id: string) => call<StoredEntity | null>('get', { projectId, id }),
    list: (projectId: string, options: ListOptions = {}) => call<StoredEntity[]>('list', { projectId, ...options }),
    events: (projectId: string, options: { after?: number; generation?: string; limit?: number } = {}) => call<StoreEventPage>('events', { projectId, ...options }),
    audit: (projectId: string, options: { after?: number; limit?: number } = {}) => call<StoreEventPage>('audit', { projectId, ...options }),
    outbox: (projectId: string) => call<{ id: string; kind: string; payload: unknown; state: string }[]>('outbox', { projectId }),
    acknowledgeOutbox: (projectId: string, id: string) => call<void>('acknowledgeOutbox', { projectId, id }),
    search: (projectId: string, options: { query: string; limit?: number; offset?: number }) => call<{
      items: StoredEntity[]; coverage: 'complete' | 'partial'; generation: number;
    }>('search', { projectId, ...options }),
    async rebuildSearch(projectId: string, options: { signal?: AbortSignal; onProgress?: (progress: { completed: number; total: number }) => void } = {}) {
      if (options.signal?.aborted) throw Object.assign(new Error('Index rebuild cancelled'), { code: 'INDEX_REBUILD_CANCELLED' });
      const cancelBuffer = new SharedArrayBuffer(4);
      const cancel = () => Atomics.store(new Int32Array(cancelBuffer), 0, 1);
      options.signal?.addEventListener('abort', cancel, { once: true });
      try { await call<void>('rebuildSearch', { projectId, cancelBuffer }, options.onProgress); }
      finally { options.signal?.removeEventListener('abort', cancel); }
    },
    putBlob: (projectId: string, bytes: Uint8Array) => call<BlobReceipt>('putBlob', { projectId, bytes }),
    backup: (outputRoot: string) => call<{ directory: string; manifest: BackupManifest; rotationCandidates: string[] }>('backup', { outputRoot }),
    promoteLegacy: (command: PromoteLegacy) => call<StoreReceipt>('promoteLegacy', command),
    close(): Promise<void> {
      if (closing) return closing;
      if (closed) return Promise.resolve();
      closing = call<void>('close', {}).finally(async () => { closed = true; await worker.terminate(); });
      return closing;
    },
  };
}

export type LocalStore = Awaited<ReturnType<typeof openLocalStore>>;

/** Snapshot validation and restore use their own Worker, including read-only SQLite checks. */
export async function restoreLocalBackup(directory: string, newDatabasePath: string): Promise<{
  databasePath: string; backupId: string; generationChanged: boolean;
}> {
  const worker = new Worker(new URL('./restore-worker.mts', import.meta.url), { workerData: { directory, newDatabasePath } });
  try {
    return await new Promise((resolve, reject) => {
      worker.once('message', ({ value, error }) => {
        if (error) reject(Object.assign(new Error(error.message), { code: error.code }));
        else resolve(value);
      });
      worker.once('error', reject);
      worker.once('exit', code => { if (code !== 0) reject(Object.assign(new Error('Restore Worker exited'), { code: 'STORAGE_CLOSED' })); });
    });
  } finally { await worker.terminate(); }
}
