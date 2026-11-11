import { parentPort, workerData } from 'node:worker_threads';
import { restoreLocalBackup } from './snapshot.mts';

try {
  const value = await restoreLocalBackup(workerData.directory, workerData.newDatabasePath);
  parentPort!.postMessage({ value });
} catch (error) {
  const failure = error as Error & { code?: string };
  parentPort!.postMessage({ error: { message: failure.message, code: failure.code ?? 'RESTORE_FAILED' } });
}
