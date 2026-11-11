import { createHash, randomUUID } from 'node:crypto';
import { spawn } from 'node:child_process';
import { mkdir, mkdtemp, readFile, rm, stat, writeFile } from 'node:fs/promises';
import { cpus, release, totalmem } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { performance } from 'node:perf_hooks';
import { fileURLToPath } from 'node:url';
import { Worker } from 'node:worker_threads';
import { openLocalStore } from '../../../apps/local-service/src/storage/local-store.mts';
import { MIGRATION_CHECKSUM, SCHEMA_VERSION } from '../../../apps/local-service/src/storage/migrations/schema.mts';
import type { EntityInput } from '../../../packages/contracts/storage/local-store.ts';
import type { M1TaskProfile } from '../../../packages/contracts/tasks/m1-task-profile.ts';

const requested = { tasks: 10000, messages: 100000, documents: 1000, approximateTextMiB: 200 };
const executionLimitMs = 180000;
const maximumTextBytes = 512 * 1024 * 1024;
const repository = fileURLToPath(new URL('../../../', import.meta.url));
const fixtureBase = join(repository, '.tmp', 'paos-m1');
const resultPath = join(fixtureBase, 'workload-result.json');

function percentile(values: number[], quantile: number) {
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.max(0, Math.ceil(sorted.length * quantile) - 1)];
}
function syntheticText(bytes: number, label: string) {
  const prefix = `${label} fixtureproject проект `;
  const remaining = bytes - Buffer.byteLength(prefix);
  const words = ' sample corpus content';
  return prefix + words.repeat(Math.ceil(remaining / words.length)).slice(0, remaining);
}
function syntheticTask(projectId: string, number: number): M1TaskProfile {
  return { schemaVersion: 'm1_task_profile_v1', type: 'Task', id: randomUUID(), projectId, key: `LOAD-${number}`,
    legacyAlias: null, title: `Synthetic task ${number} fixtureproject`, summary: `searchable tasknumber${number}`,
    technicalValue: '', productValue: '', files: [], agentAssignments: [], artifactReferences: [], acceptanceCriteria: [],
    estimateSeconds: null, actual: { startedAt: null, endedAt: null, durationSeconds: null }, risks: [], status: 'backlog',
    creator: { kind: 'user', actorId: 'synthetic-user' }, priority: null, startDate: null, dueDate: null,
    links: [], sessionIds: [], provenance: null };
}
async function databaseCounts(databasePath: string): Promise<Record<string, unknown>> {
  const worker = new Worker(`
    const { parentPort, workerData } = require('node:worker_threads');
    const { DatabaseSync } = require('node:sqlite');
    const db = new DatabaseSync(workerData, { readOnly: true });
    const counts = db.prepare('SELECT kind,count(*) AS count FROM entities WHERE deleted=0 GROUP BY kind').all();
    const indexed = db.prepare('SELECT count(*) AS count FROM indexed_documents').get().count;
    const foreignKeyFailures = db.prepare('PRAGMA foreign_key_check').all().length;
    db.close();
    parentPort.postMessage({ counts: Object.fromEntries(counts.map(row=>[row.kind,row.count])), indexed, foreignKeyFailures });
  `, { eval: true, workerData: databasePath });
  try {
    return await new Promise((accept, reject) => { worker.once('message', accept); worker.once('error', reject); });
  } finally { await worker.terminate(); }
}

async function runFixture(root: string) {
  const started = performance.now();
  const databasePath = join(root, 'fixture.sqlite');
  const inserted = { tasks: 0, messages: 0, documents: 0 };
  let sourceTextBytes = 0;
  const notify = (value: Record<string, unknown>) => process.send?.({ inserted: { ...inserted }, sourceTextBytes, elapsedMs: performance.now() - started, ...value });
  const firstOpen = performance.now();
  let store = await openLocalStore({ databasePath });
  const emptyStoreOpenMs = performance.now() - firstOpen;
  try {
    const projectId = 'synthetic-workload-project';
    await store.registerProject({ id: projectId, keyPrefix: 'LOAD', canonicalRoot: root, rootIdentity: 'synthetic-workload-root', authorityMode: 'sql' });
    let sequence = 0;
    async function put(entities: EntityInput[]) {
      if (performance.now() - started > executionLimitMs - 1000) throw Object.assign(new Error('Workload deadline'), { code: 'WORKLOAD_TIMEOUT' });
      for (const entity of entities) sourceTextBytes += Buffer.byteLength((entity.title ?? '') + (entity.body ?? ''));
      if (sourceTextBytes > maximumTextBytes) throw Object.assign(new Error('Synthetic source text cap'), { code: 'WORKLOAD_DATA_CAP' });
      await store.write({ projectId, actorId: 'synthetic-user', idempotencyKey: `workload-${sequence++}`,
        expectedAuthorityEpoch: 1, changes: entities.map(entity => ({ expectedRevision: 0, entity })) });
    }
    notify({ phase: 'tasks' });
    for (let start = 0; start < requested.tasks; start += 100) {
      const entities = Array.from({ length: 100 }, (_, offset) => {
        const task = syntheticTask(projectId, start + offset + 1);
        return { id: task.id, kind: 'task' as const, data: task };
      });
      await put(entities);
      inserted.tasks += entities.length;
      if (inserted.tasks % 1000 === 0) notify({ phase: 'tasks' });
    }
    await put([{ id: 'synthetic-session', kind: 'session', title: 'Synthetic visible-message history' }]);
    notify({ phase: 'messages' });
    for (let start = 0; start < requested.messages; start += 100) {
      const entities = Array.from({ length: 100 }, (_, offset) => {
        const number = start + offset;
        return { id: `message-${String(number).padStart(6, '0')}`, kind: 'message' as const, parentId: 'synthetic-session',
          body: syntheticText(1024, `Visible synthetic message messagenumber${number}`), coverage: 'complete' as const,
          data: { schemaVersion: 1, visibility: 'visible', sourceItemId: `synthetic-item-${number}`, sourceRevision: 1 } };
      });
      await put(entities);
      inserted.messages += entities.length;
      if (inserted.messages % 10000 === 0) notify({ phase: 'messages' });
    }
    notify({ phase: 'documents' });
    for (let start = 0; start < requested.documents; start += 100) {
      const entities = Array.from({ length: 100 }, (_, offset) => {
        const number = start + offset;
        return { id: `document-${String(number).padStart(4, '0')}`, kind: 'document' as const,
          title: `Synthetic document ${number}`, body: syntheticText(107315, `Synthetic document documentnumber${number}`),
          coverage: 'complete' as const, data: { schemaVersion: 1, relativePath: `docs/synthetic-${number}.md` } };
      });
      await put(entities);
      inserted.documents += entities.length;
      notify({ phase: 'documents' });
    }
    await store.close();
    const reopenStart = performance.now();
    store = await openLocalStore({ databasePath });
    const freshWorkerOpenExistingDatabaseMs = performance.now() - reopenStart;
    notify({ phase: 'measurements' });
    const searchMs: number[] = [];
    const smallCommandAckMs: number[] = [];
    const warmTaskListMs: number[] = [];
    const queryCases = ['fixtureproject', 'проект', 'tasknumber9999', 'messagenumber90000', 'documentnumber900', 'LOAD-9999', 'docs/synthetic-900.md', 'no-synthetic-match'];
    let coverage = 'complete';
    for (let sample = 0; sample < 40; sample++) {
      const before = performance.now();
      const result = await store.search(projectId, { query: queryCases[sample % queryCases.length]!, limit: 50 });
      searchMs.push(performance.now() - before);
      if (result.coverage !== 'complete') coverage = result.coverage;
      const listStart = performance.now();
      const page = await store.list(projectId, { kind: 'task', limit: 50, offset: sample * 50 });
      warmTaskListMs.push(performance.now() - listStart);
      if (page.length !== 50) throw Object.assign(new Error('Task page count mismatch'), { code: 'WORKLOAD_COUNT_MISMATCH' });
      const ackStart = performance.now();
      await store.write({ projectId, actorId: 'synthetic-user', expectedAuthorityEpoch: 1, idempotencyKey: `measured-small-command-${sample}`,
        changes: [{ expectedRevision: sample, entity: { id: 'measured-settings', kind: 'settings', data: { schemaVersion: 1, locale: sample % 2 ? 'ru' : 'en' } } }] });
      smallCommandAckMs.push(performance.now() - ackStart);
    }
    const verification = await databaseCounts(databasePath);
    const counts = verification.counts as Record<string, number>;
    const countsMatch = counts.task === requested.tasks && counts.message === requested.messages && counts.document === requested.documents;
    const metrics = {
      emptyStoreOpenMs, freshWorkerOpenExistingDatabaseMs, osCacheFlushed: false,
      indexedSearch: { samples: searchMs.length, p95Ms: percentile(searchMs, 0.95), maxMs: Math.max(...searchMs), queries: queryCases },
      smallCommandAck: { samples: smallCommandAckMs.length, p95Ms: percentile(smallCommandAckMs, 0.95), maxMs: Math.max(...smallCommandAckMs) },
      warmTaskPage50: { samples: warmTaskListMs.length, p95Ms: percentile(warmTaskListMs, 0.95), maxMs: Math.max(...warmTaskListMs) },
    };
    const targets = { indexedSearchP95Ms: 500, smallCommandAckP95Ms: 500, warmProjectViewMs: 1000 };
    notify({ phase: 'completed', status: countsMatch && coverage === 'complete' ? 'completed_offline' : 'partially_verified',
      verification, coverage, metrics, targets,
      targetObservations: { indexedSearchPassed: metrics.indexedSearch.p95Ms! <= 500,
        smallCommandAckPassed: metrics.smallCommandAck.p95Ms! <= 500,
        warmTaskPagePassed: metrics.warmTaskPage50.p95Ms! <= 1000,
        fullColdLaunchMeasured: false, eventToVisibleMeasured: false } });
  } catch (error) {
    notify({ phase: 'stopped', status: 'partially_verified', errorCode: (error as { code?: string }).code ?? 'WORKLOAD_FAILED' });
    process.exitCode = 1;
  } finally {
    await store.close();
    notify({ databaseBytesAfterClose: (await stat(databasePath)).size });
  }
}

async function supervise() {
  await mkdir(fixtureBase, { recursive: true });
  const root = await mkdtemp(join(fixtureBase, 'workload-'));
  const sourceDigests: Record<string, string> = {};
  for (const path of ['apps/local-service/src/storage/local-store.mts', 'apps/local-service/src/storage/sqlite-worker.mts', 'apps/local-service/src/storage/search-queries.mts', 'apps/local-service/src/storage/migrations/schema.mts', 'tests/web/single-window/workload.mts']) {
    sourceDigests[path] = createHash('sha256').update(await readFile(join(repository, path))).digest('hex');
  }
  const report: Record<string, unknown> = { schemaVersion: 1, status: 'running', requested, executionLimitMs, maximumTextBytes,
    startedAt: new Date().toISOString(), node: process.version, sqlite: process.versions.sqlite, platform: process.platform,
    arch: process.arch, windowsBuild: release(), logicalCpus: cpus().length, totalMemoryBytes: totalmem(),
    databaseSchemaVersion: SCHEMA_VERSION, migrationChecksum: MIGRATION_CHECKSUM, sourceDigests,
    evidence: 'offline synthetic SQLite Worker workload',
    excludedMeasurements: ['browser rendering', 'full launcher startup', 'provider inference', 'model quality', 'event-to-visible UI latency'] };
  const child = spawn(process.execPath, [fileURLToPath(import.meta.url), '--fixture-child', root],
    { cwd: repository, stdio: ['ignore', 'pipe', 'pipe', 'ipc'], windowsHide: true });
  let timedOut = false;
  let stderrPresent = false;
  child.stderr!.on('data', () => { stderrPresent = true; });
  child.stdout!.resume();
  child.on('message', message => {
    Object.assign(report, message);
    if ((message as { phase?: string }).phase) console.log(JSON.stringify({ phase: report.phase, inserted: report.inserted, elapsedMs: report.elapsedMs }));
  });
  const timer = setTimeout(() => { timedOut = true; child.kill(); }, executionLimitMs);
  try {
    const exitCode = await new Promise<number | null>((accept, reject) => { child.once('exit', accept); child.once('error', reject); });
    report.processExitCode = exitCode;
    report.childStderrPresent = stderrPresent;
    if (timedOut) Object.assign(report, { status: 'partially_verified', errorCode: 'WORKLOAD_TIMEOUT' });
    if (report.status === 'running') report.status = 'partially_verified';
  } finally {
    clearTimeout(timer);
    if (dirname(resolve(root)) !== resolve(fixtureBase)) throw new Error('Fixture cleanup containment failed');
    await rm(root, { recursive: true, force: true });
    report.fixtureCleaned = true;
    report.finishedAt = new Date().toISOString();
    await writeFile(resultPath, JSON.stringify(report, null, 2));
  }
  console.log(JSON.stringify({ status: report.status, verification: report.verification, metrics: report.metrics, targetObservations: report.targetObservations, fixtureCleaned: report.fixtureCleaned }));
  process.exitCode = report.status === 'completed_offline' ? 0 : 1;
}

if (process.argv[2] === '--fixture-child') await runFixture(process.argv[3]!);
else await supervise();
