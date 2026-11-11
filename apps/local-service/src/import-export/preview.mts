import { createHash } from 'node:crypto';
import { decodeM1TaskProfile } from '../tasks/task-profile.ts';
import { M1_TASK_STATUSES, type M1TaskProfile, type M1TaskStatus } from '../../../../packages/contracts/tasks/m1-task-profile.ts';

export type ImportSourceInput = { role: 'records' | 'projection'; sourceName: string; sourceRelativePath?: string; content: string };
export type ImportSourcePin = { role: 'records' | 'projection'; sourceName: string; sourceRelativePath: string;
  sourceDigest: string; byteSize: number; sourceSnapshot: string };
type Options = { projectId: string; sourceName: string; content: string } | { projectId: string; sources: readonly ImportSourceInput[] };
function previewBundle(projectId: string, sources: readonly ImportSourceInput[]): ImportPreview {
  const invalid = () => Object.assign(new Error('Invalid import bundle'), { code: 'IMPORT_BUNDLE_INVALID' });
  if (!Array.isArray(sources) || sources.length !== 2) throw invalid();
  const pins: ImportSourcePin[] = sources.map(source => {
    if (!source || !['records', 'projection'].includes(source.role) || typeof source.sourceName !== 'string'
      || !source.sourceName.trim() || typeof source.content !== 'string' || Buffer.byteLength(source.content) > 1024 * 1024) throw invalid();
    const path = source.sourceRelativePath ?? source.sourceName;
    if (typeof path !== 'string' || !path || path.split(/[\\/]/).some(part => !part || part === '.' || part === '..'
      || /[\u0000-\u001f:<>"|?*]/.test(part) || /[. ]$/.test(part)
      || /^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)/i.test(part))) throw invalid();
    if (source.role === 'records' ? !/\.json$/i.test(source.sourceName) : !/\.md$/i.test(source.sourceName)) throw invalid();
    return { role: source.role, sourceName: source.sourceName, sourceRelativePath: path.replaceAll('\\', '/'),
      sourceDigest: sha256(source.content), byteSize: Buffer.byteLength(source.content), sourceSnapshot: source.content };
  });
  if (new Set(pins.map(pin => pin.role)).size !== 2 || new Set(pins.map(pin => pin.sourceRelativePath.toLowerCase())).size !== 2) throw invalid();
  pins.sort((a, b) => a.sourceRelativePath.toLowerCase() < b.sourceRelativePath.toLowerCase() ? -1 : 1);
  const records = pins.find(pin => pin.role === 'records')!;
  const projection = pins.find(pin => pin.role === 'projection')!;
  const primary = previewTaskImport({ projectId, sourceName: records.sourceName, content: records.sourceSnapshot });
  const secondary = previewTaskImport({ projectId, sourceName: projection.sourceName, content: projection.sourceSnapshot });
  if (primary.mode !== 'legacy_import' || secondary.mode !== 'legacy_import') throw invalid();
  const sourceSnapshot = JSON.stringify(pins.map(pin => ({ role: pin.role, sourceName: pin.sourceName,
    sourceRelativePath: pin.sourceRelativePath, content: pin.sourceSnapshot })));
  const sourceDigest = sha256(JSON.stringify(pins.map(({ sourceSnapshot: _content, ...pin }) => pin)));
  const result: ImportPreview = { ...primary, sourceDigest, sourceSnapshot, sources: pins,
    blocked: [...primary.blocked.map(item => ({ ...item, sourceId: `${records.sourceName}:${item.sourceId}` })),
      ...secondary.blocked.map(item => ({ ...item, sourceId: `${projection.sourceName}:${item.sourceId}` }))] };
  const fields: Record<string, keyof M1TaskProfile> = { title: 'title', short_description: 'summary', technical_value: 'technicalValue',
    product_value: 'productValue', agents: 'agentAssignments', project_artifacts: 'artifactReferences', acceptance_criteria: 'acceptanceCriteria',
    estimated_duration_hms: 'estimateSeconds', risks: 'risks', status: 'status', priority: 'priority', start_date: 'startDate', due_date: 'dueDate' };
  const cards = new Map(markdownCards(projection.sourceSnapshot).map(card => [text(card.id), card]));
  const primaryByKey = new Map(primary.items.map(item => [item.task.key, item]));
  const primaryKeys = new Map(primary.items.map(item => [item.task.id, item.task.key]));
  const secondaryKeys = new Map(secondary.items.map(item => [item.task.id, item.task.key]));
  const conflicts = new Set<string>();
  for (const item of secondary.items) {
    const authoritative = primaryByKey.get(item.task.key);
    if (!authoritative) {
      result.blocked.push({ sourceId: item.sourceId, reasons: ['projection_record_missing'] });
      continue;
    }
    const present = cards.get(item.sourceId)!;
    const reasons: string[] = [];
    for (const field of Object.keys(present)) {
      let expected: unknown;
      let observed: unknown;
      if (fields[field]) { expected = authoritative.task[fields[field]]; observed = item.task[fields[field]]; }
      else if (field === 'affected_files') {
        expected = authoritative.task.files.map(file => file.relativePath).sort();
        observed = item.task.files.map(file => file.relativePath).sort();
      } else if (field === 'depends_on') {
        expected = authoritative.task.links.filter(link => link.relation === 'blocked_by').map(link => primaryKeys.get(link.taskId)).sort();
        observed = item.task.links.filter(link => link.relation === 'blocked_by').map(link => secondaryKeys.get(link.taskId)).sort();
      } else if (['actual_started_at', 'actual_ended_at', 'actual_duration_hms', 'actual_duration_seconds'].includes(field)) {
        const key = field === 'actual_started_at' ? 'startedAt' : field === 'actual_ended_at' ? 'endedAt' : 'durationSeconds';
        expected = authoritative.task.actual[key]; observed = item.task.actual[key];
      } else continue;
      if (JSON.stringify(expected) !== JSON.stringify(observed)) reasons.push(`projection_conflict:${field}`);
    }
    if (reasons.length) { conflicts.add(item.task.key); result.blocked.push({ sourceId: item.sourceId, reasons }); }
  }
  result.items = primary.items.filter(item => !conflicts.has(item.task.key));
  return result;
}
export type ImportPreview = {
  parserVersion: 'm1_import_v1'; sourceDigest: string; sourceSnapshot: string; sourceName: string;
  mode: 'legacy_import' | 'normalized_proposal';
  sources?: ImportSourcePin[];
  proposal?: { baseAuthorityEpoch: number; baseStreamGeneration: string; baseThroughSeq: number;
    baseRevisions: Record<string, number>; requiresCurrentSnapshot: true };
  items: { sourceId: string; task: M1TaskProfile }[];
  blocked: { sourceId: string; reasons: string[] }[];
};

const sha256 = (text: string) => createHash('sha256').update(text, 'utf8').digest('hex');
const aliases: Record<string, M1TaskStatus> = { planned: 'backlog', implemented: 'awaiting_acceptance', blocked: 'backlog', not_started: 'backlog' };
const knownFields = new Set(['id', 'group_id', 'title', 'status', 'short_description', 'technical_value', 'product_value',
  'affected_files', 'agents', 'project_artifacts', 'acceptance_criteria', 'estimated_duration_hms', 'estimate_status',
  'actual_started_at', 'actual_ended_at', 'actual_duration_seconds', 'actual_duration_hms', 'risks', 'depends_on',
  'execution_order', 'delivery_stage', 'priority', 'start_date', 'due_date', 'parentId', 'children', 'components', 'versions', 'attachments']);

function record(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Expected a task object');
  return value as Record<string, unknown>;
}

function text(value: unknown, fallback = ''): string {
  if (value === undefined || value === null) return fallback;
  if (typeof value !== 'string') throw new Error('Expected text');
  return value;
}

function strings(value: unknown): string[] {
  if (value === undefined || value === null || value === '') return [];
  if (typeof value === 'string') return [value];
  if (!Array.isArray(value) || value.some((item) => typeof item !== 'string')) throw new Error('Expected a text array');
  return value as string[];
}

/** Version 8 UUIDs remain stable for re-import into the same project. */
function taskId(projectId: string, sourceId: string): string {
  const hex = sha256(`${projectId}\0${sourceId}`).slice(0, 32).split('');
  hex[12] = '8';
  hex[16] = ((parseInt(hex[16], 16) & 3) | 8).toString(16);
  const id = hex.join('');
  return `${id.slice(0, 8)}-${id.slice(8, 12)}-${id.slice(12, 16)}-${id.slice(16, 20)}-${id.slice(20)}`;
}

function canonicalKey(sourceId: string): string {
  const match = /^([A-Z]{4})-0*([1-9]\d*)$/.exec(sourceId);
  if (!match || !Number.isSafeInteger(Number(match[2]))) throw new Error('Unsupported task key');
  return `${match[1]}-${match[2]}`;
}

function seconds(value: unknown): number | null {
  if (value == null || value === '') return null;
  const match = /^(\d+):([0-5]\d):([0-5]\d)/.exec(text(value));
  if (!match) throw new Error('Unsupported estimate');
  const result = Number(match[1]) * 3600 + Number(match[2]) * 60 + Number(match[3]);
  if (!Number.isSafeInteger(result)) throw new Error('Estimate overflow');
  return result;
}

function utc(value: unknown): string | null {
  if (value == null || value === '') return null;
  const input = text(value);
  const match = /^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$/.exec(input);
  if (!match || !Number.isFinite(Date.parse(input))) throw new Error('Unsupported source timestamp');
  return new Date(Date.parse(`${match[1]}${match[3]}`)).toISOString().slice(0, 19) + (match[2] ?? '') + 'Z';
}

function markdownCards(content: string): Record<string, unknown>[] {
  const fields: Record<string, string> = { Task: 'title', Status: 'status', 'Short description': 'short_description',
    'Technical value': 'technical_value', 'Product value': 'product_value', 'Acceptance criteria': 'acceptance_criteria',
    'Estimated execution time': 'estimated_duration_hms', Risks: 'risks', 'Risks / approval gates': 'risks',
    'Actual duration': 'actual_duration_hms', 'Actual started at': 'actual_started_at', 'Actual ended at': 'actual_ended_at',
    Priority: 'priority', 'Start date': 'start_date', 'Due date': 'due_date', Attachments: 'attachments', Parent: 'parentId', Children: 'children' };
  const metadata = new Set(['Delivery stage', 'Execution order', 'Schema version', 'Timezone', 'Plan trigger', 'Validator target',
    'Date and time of task implementation', 'Blocks', 'Source', 'Non-goals', 'Expected result', 'Verification gates',
    'Complexity', 'Skills', 'Output artifacts', 'Next step']);
  return content.split(/^### Task `([^`]+)`\s*$/m).slice(1).reduce<Record<string, unknown>[]>((cards, part, index, parts) => {
    if (index % 2 !== 0) return cards;
    const block = parts[index + 1].split(/^#### Completion Report/m)[0];
    if (!/^- Schema version: task_matrix_plan_v1\s*$/m.test(block)) throw new Error('Unsupported Markdown task schema');
    const card: Record<string, unknown> = { id: part };
    for (const line of block.split('\n')) {
      const match = /^- ([^:]+):\s*(.*)$/.exec(line);
      if (!match) continue;
      const [_, label, value] = match;
      if (fields[label]) card[fields[label]] = value;
      else if (label === 'Depends on') card.depends_on = /^(none|—|нет|not_applicable)$/i.test(value) ? [] : value.split(/,\s*/);
      else if (label === 'Agents') card.agents = value.split(/,\s*/);
      else if (label === 'Project artifacts') card.project_artifacts = value.split(/;\s*/);
      else if (label === 'Scope') {
        card.affected_files = value.split(/;\s*/).map((path) => ({ path, planned_operation: 'create_or_modify_after_discovery', actual_operation: null }));
      } else if (label === 'Actual time' && /^(not_started|unknown|pending)(?:[; .]|$)/i.test(value)) {
        card.actual_duration_seconds = null;
      } else if (label === 'Affected files' && /^proposed paths above(?:; actual create\/modify\/delete receipts only after execution)?\.?$/i.test(value)) {
        // This canonical note adds no operations beyond the structured Scope field.
      } else if (!metadata.has(label) && value && !/^(pending|not_applicable)$/i.test(value)) card[`markdown:${label}`] = value;
    }
    cards.push(card);
    return cards;
  }, []);
}

/** A SQL export is a proposed revision of its base snapshot. It never becomes a legacy cutover. */
function normalizedProposal(projectId: string, sourceName: string, content: string, parsed: Record<string, unknown>): ImportPreview {
  const invalid = () => Object.assign(new Error('Invalid normalized export'), { code: 'IMPORT_INVALID' });
  if (parsed.projectId !== projectId) throw Object.assign(new Error('Export belongs to another project'), { code: 'IMPORT_SCOPE_CONFLICT' });
  if (parsed.authority !== 'sql' || parsed.operation !== 'staged_reverse_transfer'
    || !Number.isSafeInteger(parsed.authorityEpoch) || (parsed.authorityEpoch as number) < 1
    || !Number.isSafeInteger(parsed.throughSeq) || (parsed.throughSeq as number) < 0
    || typeof parsed.streamGeneration !== 'string' || !parsed.streamGeneration.trim()
    || !Array.isArray(parsed.tasks) || parsed.tasks.length > 10000) throw invalid();
  const revisions = record(parsed.baseRevisions);
  const baseRevisions: Record<string, number> = {};
  for (const [id, revision] of Object.entries(revisions)) {
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(id)
      || !Number.isSafeInteger(revision) || (revision as number) < 0) throw invalid();
    baseRevisions[id] = revision as number;
  }
  const result: ImportPreview = { parserVersion: 'm1_import_v1', sourceDigest: sha256(content), sourceSnapshot: content, sourceName,
    mode: 'normalized_proposal', proposal: { baseAuthorityEpoch: parsed.authorityEpoch as number,
      baseStreamGeneration: parsed.streamGeneration, baseThroughSeq: parsed.throughSeq as number,
      baseRevisions, requiresCurrentSnapshot: true }, items: [], blocked: [] };
  const allowed = new Set(['schema_version', 'projectId', 'authorityEpoch', 'streamGeneration', 'throughSeq', 'baseRevisions', 'tasks', 'authority', 'operation']);
  for (const [field, value] of Object.entries(parsed)) {
    if (!allowed.has(field) && value != null && value !== '') result.blocked.push({ sourceId: '_document', reasons: [`unsupported:${field}`] });
  }
  const tasks: M1TaskProfile[] = [];
  const ids = new Map<string, number>();
  const keys = new Map<string, number>();
  for (const [index, input] of parsed.tasks.entries()) {
    try {
      const task = decodeM1TaskProfile(input);
      if (task.projectId !== projectId || !Object.hasOwn(baseRevisions, task.id)) throw invalid();
      tasks.push(task);
      ids.set(task.id, (ids.get(task.id) ?? 0) + 1);
      keys.set(task.key, (keys.get(task.key) ?? 0) + 1);
    } catch { result.blocked.push({ sourceId: String(index), reasons: ['invalid_normalized_task'] }); }
  }
  const edges = new Map(tasks.map(task => [task.id, new Set<string>()]));
  const incoming = new Map(tasks.map(task => [task.id, 0]));
  for (const task of tasks) {
    for (const link of task.links) {
      if (link.relation === 'related' || !ids.has(link.taskId)) continue;
      const [from, to] = link.relation === 'blocked_by' ? [link.taskId, task.id] : [task.id, link.taskId];
      if (!edges.get(from)!.has(to)) { edges.get(from)!.add(to); incoming.set(to, incoming.get(to)! + 1); }
    }
  }
  const ready = [...incoming].filter(([, count]) => count === 0).map(([id]) => id);
  for (let index = 0; index < ready.length; index++) {
    for (const id of edges.get(ready[index])!) {
      incoming.set(id, incoming.get(id)! - 1);
      if (incoming.get(id) === 0) ready.push(id);
    }
  }
  for (const task of tasks) {
    const reasons: string[] = [];
    if ((ids.get(task.id) ?? 0) > 1) reasons.push('duplicate_or_missing_id');
    if ((keys.get(task.key) ?? 0) > 1) reasons.push(`duplicate_canonical_key:${task.key}`);
    if ((incoming.get(task.id) ?? 0) > 0) reasons.push('dependency_cycle');
    if (task.links.some(link => !ids.has(link.taskId))) reasons.push('unresolved_dependency');
    const sourceId = task.provenance?.sourceId ?? task.legacyAlias ?? task.key;
    if (reasons.length) result.blocked.push({ sourceId, reasons });
    else result.items.push({ sourceId, task });
  }
  return result;
}

/** Preview preserves the original snapshot and refuses unsupported significant data before cutover. */
export function previewTaskImport(options: Options): ImportPreview {
  if ('sources' in options) return previewBundle(options.projectId, options.sources);
  const { projectId, sourceName, content } = options;
  if (!projectId?.trim() || !sourceName?.trim() || Buffer.byteLength(content, 'utf8') > 1024 * 1024) {
    throw Object.assign(new Error('Invalid import input'), { code: 'IMPORT_INVALID' });
  }
  const sourceDigest = sha256(content);
  let schema: 'paos_web_task_groups_v1' | 'task_matrix_plan_v1';
  let cards: Record<string, unknown>[];
  if (/\.json$/i.test(sourceName)) {
    const parsed = record(JSON.parse(content));
    if (parsed.schema_version === 'm1_task_profile_v1') return normalizedProposal(projectId, sourceName, content, parsed);
    if (!['paos_web_task_groups_v1', 'task_matrix_plan_v1'].includes(text(parsed.schema_version)) || !Array.isArray(parsed.tasks)) {
      throw Object.assign(new Error('Unsupported import schema'), { code: 'IMPORT_UNSUPPORTED' });
    }
    schema = parsed.schema_version as typeof schema;
    cards = parsed.tasks.map(record);
  } else if (/\.md$/i.test(sourceName)) {
    schema = 'task_matrix_plan_v1';
    cards = markdownCards(content);
  } else throw Object.assign(new Error('Only versioned Markdown and JSON imports are supported'), { code: 'IMPORT_UNSUPPORTED' });
  if (!cards.length || cards.length > 10_000) throw new Error('Invalid import task count');
  const result: ImportPreview = { parserVersion: 'm1_import_v1', sourceDigest, sourceName, sourceSnapshot: content, mode: 'legacy_import', items: [], blocked: [] };
  const ids = new Set(cards.map((card) => text(card.id)));
  const seen = new Set<string>();
  const canonicalCounts = new Map<string, number>();
  for (const card of cards) {
    try {
      const key = canonicalKey(text(card.id));
      canonicalCounts.set(key, (canonicalCounts.get(key) ?? 0) + 1);
    } catch { /* Invalid keys receive their own field diagnostic below. */ }
  }
  const byId = new Map(cards.map((card) => [text(card.id), card]));
  const remaining = new Map<string, number>();
  const dependents = new Map<string, string[]>();
  for (const [id, card] of byId) {
    const deps = Array.isArray(card.depends_on) ? card.depends_on.filter((dep): dep is string => typeof dep === 'string' && byId.has(dep)) : [];
    remaining.set(id, deps.length);
    for (const dep of deps) dependents.set(dep, [...(dependents.get(dep) ?? []), id]);
  }
  const ready = [...remaining].filter(([, count]) => count === 0).map(([id]) => id);
  for (let position = 0; position < ready.length; position++) {
    for (const id of dependents.get(ready[position]) ?? []) {
      const count = remaining.get(id)! - 1;
      remaining.set(id, count);
      if (count === 0) ready.push(id);
    }
  }
  const cyclic = new Set([...remaining].filter(([, count]) => count > 0).map(([id]) => id));
  for (const card of cards) {
    const sourceId = text(card.id);
    const reasons: string[] = [];
    if (!sourceId.trim() || seen.has(sourceId)) reasons.push('duplicate_or_missing_id');
    try {
      const key = canonicalKey(sourceId);
      if ((canonicalCounts.get(key) ?? 0) > 1) reasons.push(`duplicate_canonical_key:${key}`);
    } catch { reasons.push('invalid_task_key'); }
    if (cyclic.has(sourceId)) reasons.push('dependency_cycle');
    seen.add(sourceId);
    for (const [field, value] of Object.entries(card)) {
      const empty = value == null || value === '' || (Array.isArray(value) && value.length === 0);
      if ((!knownFields.has(field) || ['parentId', 'children', 'components', 'versions', 'attachments'].includes(field)) && !empty) {
        reasons.push(`unsupported:${field}`);
      }
    }
    let dependencies: string[] = [];
    if (card.depends_on != null && (!Array.isArray(card.depends_on) || card.depends_on.some(dep => typeof dep !== 'string'))) {
      reasons.push('invalid_dependencies');
    } else dependencies = (card.depends_on ?? []) as string[];
    for (const dep of dependencies) if (!ids.has(dep) || dep === sourceId) reasons.push(`unresolved_dependency:${dep}`);
    try {
      const sourceStatus = text(card.status);
      let status = M1_TASK_STATUSES.includes(sourceStatus as M1TaskStatus) ? sourceStatus : aliases[sourceStatus];
      const reviewFlags: string[] = [];
      if (sourceStatus === 'in_progress') { status = 'ready'; reviewFlags.push('recovery_review'); }
      if (sourceStatus === 'done' || sourceStatus === 'implemented') { status = 'awaiting_acceptance'; reviewFlags.push('acceptance_unverified'); }
      if (!status) reasons.push('unsupported_status');
      if (reasons.length) { result.blocked.push({ sourceId, reasons }); continue; }
      const files = (card.affected_files ?? []) as Record<string, unknown>[];
      if (!Array.isArray(files)) throw new Error('Unsupported files');
      const hmsDuration = seconds(card.actual_duration_hms);
      if (hmsDuration !== null && card.actual_duration_seconds != null && hmsDuration !== card.actual_duration_seconds) throw new Error('Source duration conflict');
      const task = decodeM1TaskProfile({
        schemaVersion: 'm1_task_profile_v1', type: 'Task', id: taskId(projectId, sourceId), projectId,
        key: canonicalKey(sourceId), legacyAlias: sourceId, title: text(card.title), summary: text(card.short_description),
        technicalValue: text(card.technical_value), productValue: text(card.product_value),
        files: files.map((file) => ({ relativePath: file.path, plannedOperation: file.planned_operation ?? null,
          actualOperation: file.actual_operation ?? null })),
        agentAssignments: strings(card.agents), artifactReferences: strings(card.project_artifacts),
        acceptanceCriteria: strings(card.acceptance_criteria), estimateSeconds: seconds(card.estimated_duration_hms),
        actual: { startedAt: utc(card.actual_started_at), endedAt: utc(card.actual_ended_at), durationSeconds: card.actual_duration_seconds ?? hmsDuration },
        risks: [...strings(card.risks), ...reviewFlags], status, creator: { kind: 'imported_unknown', actorId: null }, priority: card.priority ?? null,
        startDate: card.start_date ?? null, dueDate: card.due_date ?? null, sessionIds: [],
        links: dependencies.map((dep) => ({ relation: 'blocked_by', taskId: taskId(projectId, dep), projectId })),
        provenance: { sourceSchema: schema, adapterVersion: 'm1_import_v1', sourceId, sourceGroup: card.group_id ?? null,
          sourceStatus, sourceDigest, sourceDocument: sourceName, mappingReceipt: `${sourceDigest}:${sourceId}` },
      });
      result.items.push({ sourceId, task });
    } catch (error) {
      const detail = error as { code?: string; path?: string };
      result.blocked.push({ sourceId, reasons: [...reasons, detail.path ? `invalid:${detail.path}` : 'invalid_source_fields'] });
    }
  }
  return result;
}
