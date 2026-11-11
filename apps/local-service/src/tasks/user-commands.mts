import { createHash } from 'node:crypto';
import type { LocalStore } from '../storage/local-store.mts';
import type { EntityInput, StoreWrite } from '../../../../packages/contracts/storage/local-store.ts';
import { decodeM1TaskProfile } from './task-profile.ts';

function fail(code: string): never { throw Object.assign(new Error(code), { code }); }
const userKinds = new Set(['task', 'session', 'comment', 'draft']);
const reservedComments = new Set(['manual_check', 'owner_acceptance']);

async function assertNoUnresolvedRun(store: LocalStore, projectId: string) {
  for (let offset = 0; ; offset += 100) {
    const runs = await store.list(projectId, { kind: 'run', offset, limit: 100 });
    if (runs.some((run) => !['completed', 'failed', 'interrupted'].includes(run.status))) fail('ACTIVE_RUN_RECONCILIATION_REQUIRED');
    if (runs.length < 100) break;
  }
}

/** The authenticated transport owns actor/project. Runtime evidence and run state have separate writers. */
export async function applyUserCommand(store: LocalStore, command: StoreWrite) {
  if (!Array.isArray(command.changes) || command.changes.length > 100) fail('INVALID_COMMAND');
  const committed = await store.receipt(command.projectId, command.idempotencyKey);
  const changes = [];
  for (const change of command.changes) {
    const input = change.entity;
    if (!userKinds.has(input.kind) || /^(runtime-|operation-|check-|accept-)/.test(input.id)) fail('USER_WRITE_FORBIDDEN');
    const existing = await store.get(command.projectId, input.id);
    if (existing && existing.kind !== input.kind) fail('ENTITY_KIND_CONFLICT');
    if (input.kind === 'comment' && (reservedComments.has(String(input.data?.category))
      || reservedComments.has(String(existing?.data.category)))) fail('USER_WRITE_FORBIDDEN');
    let entity: EntityInput = input;
    if (input.kind === 'task') {
      const raw = input.data as Record<string, unknown>;
      const project = await store.project(command.projectId);
      if (!project) fail('PROJECT_NOT_FOUND');
      // A deleted imported task still replays against the original creator and request hash.
      const creator = existing?.data.creator ?? (committed && change.expectedRevision > 0 ? raw?.creator : { kind: 'user', actorId: command.actorId });
      const allocating = raw?.key === '' && change.expectedRevision === 0;
      const task = decodeM1TaskProfile({ ...raw, creator, key: allocating ? `${project.keyPrefix}-1` : raw?.key });
      if (task.projectId !== command.projectId || task.id !== input.id) fail('TASK_SCOPE_CONFLICT');
      if (!committed && task.status === 'done' && existing?.status !== 'done') fail('OWNER_ACCEPTANCE_REQUIRED');
      entity = { ...input, data: allocating ? { ...task, key: '' } : task };
    }
    changes.push({ ...change, entity });
  }
  const requireIdle = changes.some((change) => ['task', 'session'].includes(change.entity.kind)
    && (change.expectedRevision > 0 || change.delete === true));
  return store.write({ ...command, changes, outbox: [], ...(requireIdle ? { requireIdle: true as const } : {}) });
}

type CheckInput = { projectId: string; taskId: string; actorId: string; expectedRevision: number;
  expectedAuthorityEpoch: number; idempotencyKey: string; outcome: 'passed' | 'failed'; note: string };

const requestDigest = (input: object) => createHash('sha256').update(JSON.stringify(Object.entries(input).sort(([a], [b]) => a.localeCompare(b)))).digest('hex');

/** A manual check records the user's observation independently of task status and owner acceptance. */
export async function recordManualCheck(store: LocalStore, input: CheckInput) {
  if (!['passed', 'failed'].includes(input.outcome) || typeof input.note !== 'string') fail('INVALID_CHECK');
  const checkId = `check-${input.idempotencyKey}`;
  const requestHash = requestDigest(input);
  const previous = await store.receipt(input.projectId, input.idempotencyKey);
  if (previous) {
    if ((await store.get(input.projectId, checkId))?.data.requestHash !== requestHash) fail('IDEMPOTENCY_CONFLICT');
    return { checkId, receipt: previous };
  }
  const task = await store.get(input.projectId, input.taskId);
  if (!task || task.kind !== 'task' || task.revision !== input.expectedRevision) fail('REVISION_CONFLICT');
  const receipt = await store.write({ projectId: input.projectId, actorId: input.actorId,
    expectedAuthorityEpoch: input.expectedAuthorityEpoch, idempotencyKey: input.idempotencyKey,
    changes: [{ expectedRevision: 0, entity: { id: checkId, kind: 'comment', parentId: task.id,
      title: 'Manual check', body: input.note, data: { category: 'manual_check', outcome: input.outcome, taskRevision: task.revision, requestHash } } }] });
  return { checkId, receipt };
}

/** Acceptance consumes a check tied to the exact task revision in the same project. */
export async function acceptTask(store: LocalStore, input: Omit<CheckInput, 'outcome'> & { checkId: string; accepted: boolean }) {
  const acceptanceId = `accept-${input.idempotencyKey}`;
  const requestHash = requestDigest(input);
  const previous = await store.receipt(input.projectId, input.idempotencyKey);
  if (previous) {
    if ((await store.get(input.projectId, acceptanceId))?.data.requestHash !== requestHash) fail('IDEMPOTENCY_CONFLICT');
    return previous;
  }
  await assertNoUnresolvedRun(store, input.projectId);
  const task = await store.get(input.projectId, input.taskId);
  const check = await store.get(input.projectId, input.checkId);
  if (!task || task.kind !== 'task' || task.revision !== input.expectedRevision) fail('REVISION_CONFLICT');
  if (typeof input.accepted !== 'boolean' || typeof input.note !== 'string') fail('INVALID_ACCEPTANCE');
  if (input.accepted && (task.status !== 'awaiting_acceptance' || check?.parentId !== task.id
    || check.kind !== 'comment' || check.data.category !== 'manual_check' || check.data.outcome !== 'passed'
    || check.data.taskRevision !== task.revision)) fail('CHECK_REQUIRED');
  if (input.accepted && (!Array.isArray(task.data.acceptanceCriteria) || task.data.acceptanceCriteria.length === 0)) fail('CRITERIA_REQUIRED');
  if (input.accepted && Array.isArray(task.data.risks) && task.data.risks.includes('recovery_review')) fail('RECOVERY_REVIEW_REQUIRED');
  const risks = Array.isArray(task.data.risks) && input.accepted
    ? task.data.risks.filter((risk) => risk !== 'acceptance_unverified') : task.data.risks;
  const profile = decodeM1TaskProfile({ ...task.data, risks, status: input.accepted ? 'done' : 'review' });
  return store.write({ projectId: input.projectId, actorId: input.actorId, expectedAuthorityEpoch: input.expectedAuthorityEpoch,
    idempotencyKey: input.idempotencyKey, requireIdle: true, changes: [
      { expectedRevision: task.revision, entity: { id: task.id, kind: 'task', data: profile } },
      { expectedRevision: 0, entity: { id: acceptanceId, kind: 'comment', parentId: task.id, title: 'Owner acceptance',
        body: input.note, data: { category: 'owner_acceptance', accepted: input.accepted, checkId: input.checkId, requestHash } } },
    ] });
}
