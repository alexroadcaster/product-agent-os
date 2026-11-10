import {
  M1_ACTUAL_FILE_OPERATIONS, M1_PLANNED_FILE_OPERATIONS, M1_TASK_PRIORITIES, M1_TASK_PROFILE, M1_TASK_RELATIONS,
  M1_TASK_SOURCE_SCHEMAS, M1_TASK_STATUSES, type M1TaskProfile,
} from '../../../../packages/contracts/tasks/m1-task-profile.ts';

const fields = [
  'schemaVersion', 'type', 'id', 'projectId', 'key', 'legacyAlias', 'title', 'summary', 'technicalValue', 'productValue',
  'files', 'agentAssignments', 'artifactReferences', 'acceptanceCriteria', 'estimateSeconds', 'actual', 'risks',
  'status', 'creator', 'priority', 'startDate', 'dueDate', 'links', 'sessionIds', 'provenance',
] as const satisfies readonly (keyof M1TaskProfile)[];
const emptyFutureFields = new Set(['parentId', 'children', 'components', 'versions', 'affectsVersions', 'fixVersions', 'attachments']);
const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const date = /^\d{4}-\d{2}-\d{2}$/;
const timestamp = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?Z$/;

function invalid(path: string, reason: string): never {
  throw Object.assign(new Error(`${path}: ${reason}`), { code: 'INVALID_M1_TASK_PROFILE', path });
}

/** Reject extension data before constructing the profile, so unsupported fields cannot vanish in export. */
function record(input: unknown, allowed: readonly string[], path: string, permitEmptyFutureFields = false): Record<string, unknown> {
  if (typeof input !== 'object' || input === null || Array.isArray(input)
    || (Object.getPrototypeOf(input) !== Object.prototype && Object.getPrototypeOf(input) !== null)) {
    invalid(path, 'expected an object');
  }
  const object = input as Record<string, unknown>;
  for (const key of Object.keys(object)) {
    if (allowed.includes(key)) continue;
    const value = object[key];
    if (permitEmptyFutureFields && emptyFutureFields.has(key)
      && (value === null || (Array.isArray(value) && value.length === 0))) continue;
    invalid(`${path}.${key}`, 'unsupported field');
  }
  return object;
}

function text(value: unknown, path: string, allowEmpty = false): string {
  if (typeof value !== 'string' || (!allowEmpty && !value.trim())) invalid(path, 'expected text');
  return value;
}

function match(value: unknown, pattern: RegExp, path: string): string {
  if (typeof value !== 'string' || !pattern.test(value)) invalid(path, 'invalid format');
  return value;
}

function choice<T extends string>(value: unknown, values: readonly T[], path: string): T {
  if (typeof value !== 'string' || !(values as readonly string[]).includes(value)) invalid(path, 'unsupported value');
  return value as T;
}

function nullable<T>(value: unknown, parse: (value: unknown) => T): T | null {
  return value === null ? null : parse(value);
}

function seconds(value: unknown, path: string): number {
  if (typeof value !== 'number' || !Number.isSafeInteger(value) || value < 0) invalid(path, 'expected whole nonnegative seconds');
  return value;
}

function dateValue(value: unknown, pattern: RegExp, path: string): string {
  const input = match(value, pattern, path);
  // Date validates the calendar in milliseconds. Keep the original higher-precision value for exchange.
  const expected = input.length === 10 ? `${input}T00:00:00.000Z` : `${timestampOrderKey(input).slice(0, 23)}Z`;
  const milliseconds = Date.parse(expected);
  if (!Number.isFinite(milliseconds) || new Date(milliseconds).toISOString() !== expected) invalid(path, 'invalid UTC date');
  return input;
}

function timestampOrderKey(input: string): string {
  const fraction = input.endsWith('Z') && input[19] === '.' ? input.slice(20, -1) : '';
  return `${input.slice(0, 19)}.${fraction.padEnd(9, '0')}`;
}

function relativePath(value: unknown, path: string): string {
  const input = text(value, path);
  if (/[\u0000-\u001f:<>"|?*]/.test(input)
    || input.split(/[\\/]/).some((part) => !part || part === '.' || part === '..' || /[. ]$/.test(part))) {
    invalid(path, 'expected a contained relative path');
  }
  return input;
}

function array<T>(value: unknown, path: string, parse: (item: unknown, path: string) => T): T[] {
  if (!Array.isArray(value)) invalid(path, 'expected an array');
  return Array.from(value, (item, index) => parse(item, `${path}[${index}]`));
}

/** This decoder validates a normalized task; source reconciliation and graph checks run before cutover. */
export function decodeM1TaskProfile(input: unknown): M1TaskProfile {
  const task = record(input, fields, 'task', true);
  const id = match(task.id, uuid, 'task.id');
  const projectId = text(task.projectId, 'task.projectId');
  const actual = record(task.actual, ['startedAt', 'endedAt', 'durationSeconds'], 'task.actual');
  const startedAt = nullable(actual.startedAt, (value) => dateValue(value, timestamp, 'task.actual.startedAt'));
  const endedAt = nullable(actual.endedAt, (value) => dateValue(value, timestamp, 'task.actual.endedAt'));
  if (startedAt !== null && endedAt !== null && timestampOrderKey(endedAt) < timestampOrderKey(startedAt)) {
    invalid('task.actual.endedAt', 'before start');
  }
  const startDate = nullable(task.startDate, (value) => dateValue(value, date, 'task.startDate'));
  const dueDate = nullable(task.dueDate, (value) => dateValue(value, date, 'task.dueDate'));
  if (startDate !== null && dueDate !== null && dueDate < startDate) invalid('task.dueDate', 'before start date');
  const creator = record(task.creator, ['kind', 'actorId'], 'task.creator');
  const creatorKind = choice(creator.kind, ['user', 'imported_unknown'], 'task.creator.kind');
  if (creatorKind === 'imported_unknown' && creator.actorId !== null) invalid('task.creator.actorId', 'unknown imported creator has no login identity');
  const seenLinks = new Set<string>();

  return {
    schemaVersion: choice(task.schemaVersion, [M1_TASK_PROFILE], 'task.schemaVersion'),
    type: choice(task.type, ['Task'], 'task.type'),
    id,
    projectId,
    key: match(task.key, /^[A-Z]{4}-[1-9]\d*$/, 'task.key'),
    legacyAlias: nullable(task.legacyAlias, (value) => text(value, 'task.legacyAlias')),
    title: text(task.title, 'task.title'),
    summary: text(task.summary, 'task.summary', true),
    technicalValue: text(task.technicalValue, 'task.technicalValue', true),
    productValue: text(task.productValue, 'task.productValue', true),
    files: array(task.files, 'task.files', (item, path) => {
      const file = record(item, ['relativePath', 'previousRelativePath', 'plannedOperation', 'actualOperation'], path);
      const plannedOperation = nullable(file.plannedOperation, (value) => choice(value, M1_PLANNED_FILE_OPERATIONS, `${path}.plannedOperation`));
      const actualOperation = nullable(file.actualOperation, (value) => choice(value, M1_ACTUAL_FILE_OPERATIONS, `${path}.actualOperation`));
      const target = relativePath(file.relativePath, `${path}.relativePath`);
      if (plannedOperation !== 'rename' && actualOperation !== 'rename') {
        if (Object.hasOwn(file, 'previousRelativePath')) invalid(`${path}.previousRelativePath`, 'requires rename');
        return { relativePath: target, plannedOperation, actualOperation };
      }
      const previousRelativePath = relativePath(file.previousRelativePath, `${path}.previousRelativePath`);
      if (previousRelativePath === target) invalid(`${path}.previousRelativePath`, 'matches destination');
      return { relativePath: target, previousRelativePath, plannedOperation, actualOperation };
    }),
    agentAssignments: array(task.agentAssignments, 'task.agentAssignments', text),
    artifactReferences: array(task.artifactReferences, 'task.artifactReferences', text),
    acceptanceCriteria: array(task.acceptanceCriteria, 'task.acceptanceCriteria', text),
    estimateSeconds: nullable(task.estimateSeconds, (value) => seconds(value, 'task.estimateSeconds')),
    actual: { startedAt, endedAt, durationSeconds: nullable(actual.durationSeconds, (value) => seconds(value, 'task.actual.durationSeconds')) },
    risks: array(task.risks, 'task.risks', text),
    status: choice(task.status, M1_TASK_STATUSES, 'task.status'),
    creator: creatorKind === 'user'
      ? { kind: 'user', actorId: text(creator.actorId, 'task.creator.actorId') }
      : { kind: 'imported_unknown', actorId: null },
    priority: nullable(task.priority, (value) => choice(value, M1_TASK_PRIORITIES, 'task.priority')),
    startDate,
    dueDate,
    links: array(task.links, 'task.links', (item, path) => {
      const link = record(item, ['relation', 'taskId', 'projectId'], path);
      const relation = choice(link.relation, M1_TASK_RELATIONS, `${path}.relation`);
      const taskId = match(link.taskId, uuid, `${path}.taskId`);
      if (taskId === id) invalid(`${path}.taskId`, 'cannot link task to itself');
      if (link.projectId !== projectId) invalid(`${path}.projectId`, 'cross-project link');
      const linkKey = `${relation === 'related' ? 'related' : 'blocking'}:${taskId}`;
      if (seenLinks.has(linkKey)) invalid(`${path}.taskId`, 'duplicate or conflicting link');
      seenLinks.add(linkKey);
      return { relation, taskId, projectId };
    }),
    sessionIds: array(task.sessionIds, 'task.sessionIds', text),
    provenance: nullable(task.provenance, (input) => {
      const path = 'task.provenance';
      const source = record(input, ['sourceSchema', 'adapterVersion', 'sourceId', 'sourceGroup', 'sourceStatus',
        'sourceDigest', 'sourceDocument', 'mappingReceipt'], path);
      return {
        sourceSchema: choice(source.sourceSchema, M1_TASK_SOURCE_SCHEMAS, `${path}.sourceSchema`),
        adapterVersion: text(source.adapterVersion, `${path}.adapterVersion`),
        sourceId: text(source.sourceId, `${path}.sourceId`),
        sourceGroup: nullable(source.sourceGroup, (value) => text(value, `${path}.sourceGroup`)),
        sourceStatus: text(source.sourceStatus, `${path}.sourceStatus`),
        sourceDigest: match(source.sourceDigest, /^[0-9a-f]{64}$/, `${path}.sourceDigest`),
        sourceDocument: relativePath(source.sourceDocument, `${path}.sourceDocument`),
        mappingReceipt: text(source.mappingReceipt, `${path}.mappingReceipt`),
      };
    }),
  };
}

export function encodeM1TaskProfile(task: M1TaskProfile): string {
  return JSON.stringify(decodeM1TaskProfile(task));
}
