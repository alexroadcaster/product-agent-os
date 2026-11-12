import { parentPort, workerData } from 'node:worker_threads';
import { createHash, randomUUID } from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';
import { unlinkSync,realpathSync,lstatSync } from 'node:fs';
import { resolve,join,dirname } from 'node:path';
import { migrate,ensureM2Schema,databaseCompatibility } from './migrations/schema.mts';
import { decodeTaskProfile as decodeM1TaskProfile, validateIssueGraph, validateReady, transitionAllowed, canonicalIssueLinks, type M2TaskProfile, type TaskProfile, type IssueLink } from '../../../../packages/contracts/issues/task-profile.ts';
import { createSnapshot, writeBlob, readManagedBlob,blobDirectory } from './snapshot.mts';
import { RANKED_SEARCH_SQL } from './search-queries.mts';
import type { EntityKind, Project, PromoteLegacy, StoreWrite, StoredEntity } from '../../../../packages/contracts/storage/local-store.ts';

function fail(code: string, message = code): never { throw Object.assign(new Error(message), { code }); }
function text(value: unknown): asserts value is string {
  if (typeof value !== 'string' || !value.trim() || value.length > 8192) fail('INVALID_ARGUMENT');
}
function hash(input: unknown) {
  function ordered(value: any): any {
    if (Array.isArray(value)) return value.map(ordered);
    if (value && typeof value === 'object') return Object.fromEntries(Object.keys(value).sort().map(key => [key, ordered(value[key])]));
    return value;
  }
  return createHash('sha256').update(JSON.stringify(ordered(input))).digest('hex');
}
function page(limit = 50, offset = 0) {
  if (!Number.isSafeInteger(limit) || limit < 1 || limit > 100 || !Number.isSafeInteger(offset) || offset < 0) fail('INVALID_PAGINATION');
  return { limit, offset };
}

let db: DatabaseSync;
function project(projectId: string): Project | null {
  const row = db.prepare('SELECT * FROM projects WHERE id=?').get(projectId);
  return row ? { id: row.id as string, keyPrefix: row.key_prefix as string, canonicalRoot: row.canonical_root as string,
    displayName: row.display_name as string, rootIdentity: row.root_identity as string,
    authorityMode: row.authority_mode as Project['authorityMode'], authorityEpoch: row.authority_epoch as number } : null;
}
function entity(row: Record<string, any>): StoredEntity {
  return { projectId: row.project_id, id: row.id, kind: row.kind, parentId: row.parent_id, title: row.title, body: row.body,
    status: row.status, publicKey: row.public_key, coverage: row.coverage, data: JSON.parse(row.data), revision: row.revision,
    deleted: Boolean(row.deleted), updatedAt: row.updated_at,
    blobIds: db.prepare('SELECT blob_id FROM entity_blobs WHERE project_id=? AND entity_id=? ORDER BY blob_id').all(row.project_id, row.id).map(blob => blob.blob_id as string) };
}
function get(projectId: string, id: string) {
  const row = db.prepare('SELECT * FROM entities WHERE project_id=? AND id=? AND deleted=0').get(projectId, id);
  return row ? entity(row) : null;
}
function transaction<T>(operation: () => T): T {
  db.exec('BEGIN IMMEDIATE');
  try { const value = operation(); db.exec('COMMIT'); return value; }
  catch (error) { db.exec('ROLLBACK'); throw error; }
}
function assertIdle(projectId: string, code = 'ACTIVE_RUN_RECONCILIATION_REQUIRED') {
  if (db.prepare(`SELECT 1 FROM entities WHERE project_id=? AND deleted=0 AND
    ((kind='run' AND status NOT IN ('completed','failed','interrupted')) OR
    (kind='approval' AND status NOT IN ('stale','denied','resolved','expired'))) LIMIT 1`).get(projectId)) fail(code);
}
const searchableKinds = ['task', 'session', 'message', 'comment', 'document'];
const requiredParentKinds: Partial<Record<EntityKind, EntityKind>> = { message: 'session', draft: 'session', comment: 'task' };
type SearchCounts = { eligible: number; indexed: number; incomplete: number };
const searchIndexFormat = 'project-path-token-v2';
function saveSearchCounts(projectId: string, counts: SearchCounts) {
  db.prepare('INSERT INTO store_meta VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value')
    .run(`search_counts:${projectId}`, JSON.stringify(counts));
}
function readSearchCounts(projectId: string): SearchCounts {
  const row = db.prepare('SELECT value FROM store_meta WHERE key=?').get(`search_counts:${projectId}`);
  return row ? JSON.parse(row.value as string) : { eligible: 0, indexed: 0, incomplete: 0 };
}
/** Older v1 profiles initialize this rebuildable ledger once, under the writer transaction. */
function initializeSearchCounts(projectId: string) {
  if (db.prepare('SELECT 1 FROM store_meta WHERE key=?').get(`search_counts:${projectId}`)) return;
  const source = db.prepare(`SELECT
    COALESCE(SUM(CASE WHEN deleted=0 AND kind IN ('task','session','message','comment','document') THEN 1 ELSE 0 END),0) AS eligible,
    COALESCE(SUM(CASE WHEN deleted=0 AND coverage<>'complete' THEN 1 ELSE 0 END),0) AS incomplete
    FROM entities WHERE project_id=?`).get(projectId)!;
  const indexed = db.prepare('SELECT count(*) AS count FROM indexed_documents WHERE project_id=?').get(projectId)!.count as number;
  saveSearchCounts(projectId, { eligible: source.eligible as number, indexed, incomplete: source.incomplete as number });
  if (indexed === 0) db.prepare('INSERT OR IGNORE INTO store_meta VALUES (?,?)').run(`search_format:${projectId}`, searchIndexFormat);
}
function scopeToken(projectId: string) { return `paosscope${createHash('sha256').update(projectId).digest('hex')}`; }
function pathToken(path: string) { return `paospath${createHash('sha256').update(path).digest('hex')}`; }
function hasCurrentSearchFormat(projectId: string) {
  return db.prepare('SELECT value FROM store_meta WHERE key=?').get(`search_format:${projectId}`)?.value === searchIndexFormat;
}
function indexEntity(projectId: string, id: string) {
  let countDelta = 0;
  const previous = db.prepare('SELECT rowid FROM indexed_documents WHERE project_id=? AND entity_id=?').get(projectId, id);
  if (previous) {
    db.prepare('DELETE FROM search_fts WHERE rowid=?').run(previous.rowid);
    db.prepare('DELETE FROM indexed_documents WHERE rowid=?').run(previous.rowid);
    countDelta--;
  }
  const current = get(projectId, id);
  if (!current || !searchableKinds.includes(current.kind) || Buffer.byteLength(current.title + current.body) > 1024 * 1024) return countDelta;
  const generation = Number(db.prepare("SELECT value FROM store_meta WHERE key=?").get(`index_generation:${projectId}`)?.value ?? 1);
  const row = db.prepare('INSERT INTO indexed_documents(project_id,entity_id,revision,generation) VALUES (?,?,?,?)')
    .run(projectId, id, current.revision, generation);
  const path = current.kind === 'document' && typeof current.data.relativePath === 'string' ? pathToken(current.data.relativePath) : '';
  db.prepare('INSERT INTO search_fts(rowid,title,body) VALUES (?,?,?)')
    .run(row.lastInsertRowid, `${scopeToken(projectId)} ${path} ${current.title}`, current.body);
  return countDelta + 1;
}
function search(params: { projectId: string; query: string; limit?: number; offset?: number }) {
  text(params.query);
  const { limit, offset } = page(params.limit, params.offset);
  const generation = Number(db.prepare("SELECT value FROM store_meta WHERE key=?").get(`index_generation:${params.projectId}`)?.value ?? 1);
  const counts = readSearchCounts(params.projectId);
  const available = db.prepare("SELECT 1 FROM sqlite_schema WHERE type='table' AND name='search_fts'").get();
  const pendingIndex = db.prepare('SELECT 1 FROM index_jobs WHERE project_id=? LIMIT 1').get(params.projectId);
  const currentFormat = hasCurrentSearchFormat(params.projectId);
  const coverage = counts.indexed === counts.eligible && !counts.incomplete && available && !pendingIndex && currentFormat ? 'complete' : 'partial';
  // Separate indexed key probes avoid an OR expression forcing every entity's JSON to be read.
  const exact = db.prepare('SELECT * FROM entities WHERE project_id=? AND id=? AND deleted=0').get(params.projectId, params.query)
    ?? db.prepare('SELECT * FROM entities WHERE project_id=? AND public_key=? AND deleted=0').get(params.projectId, params.query);
  if (exact) return { items: offset === 0 ? [entity(exact)] : [], coverage, generation };
  const paths = available && currentFormat
    ? db.prepare(`SELECT e.* FROM search_fts f JOIN indexed_documents d ON d.rowid=f.rowid
        JOIN entities e ON e.project_id=d.project_id AND e.id=d.entity_id WHERE search_fts MATCH ? AND e.project_id=?
        AND e.kind='document' AND e.deleted=0 AND e.revision=d.revision AND json_extract(e.data,'$.relativePath')=?
        ORDER BY e.id LIMIT ? OFFSET ?`).all(`"${scopeToken(params.projectId)}" AND "${pathToken(params.query)}"`, params.projectId, params.query, limit, offset)
    : db.prepare("SELECT * FROM entities WHERE project_id=? AND kind='document' AND deleted=0 AND json_extract(data,'$.relativePath')=? ORDER BY id LIMIT ? OFFSET ?")
      .all(params.projectId, params.query, limit, offset);
  if (paths.length) return { items: paths.map(entity), coverage, generation };
  if (!available) return { items: [], coverage: 'partial', generation };
  const tokens = params.query.match(/[\p{L}\p{N}_]+/gu) ?? [];
  if (tokens.length === 0) return { items: [], coverage, generation };
  const terms = tokens.map(token => `"${token}"`).join(' AND ');
  const query = currentFormat ? `"${scopeToken(params.projectId)}" AND (${terms})` : terms;
  return { items: db.prepare(RANKED_SEARCH_SQL).all(query, params.projectId, limit, offset).map(entity), coverage, generation };
}
/** History keeps changed task fields only. Oversized values are explicitly unavailable, never a hidden full-state copy. */
function redactHistoryText(value:string):string {
  return value.replace(/-----BEGIN [^-]*PRIVATE KEY-----[\s\S]*?-----END [^-]*PRIVATE KEY-----/g,'[redacted]')
    .replace(/\bsk-[A-Za-z0-9_-]{12,}/g,'[redacted]').replace(/\bBearer\s+[A-Za-z0-9._~+\/-]{12,}/gi,'Bearer [redacted]')
    .replace(/\b((?:password|passwd|api[_-]?key|access[_-]?token|secret|token)\s*[:=]\s*)(?:"[^"]*"|'[^']*'|[^\s,;]+)/gi,'$1[redacted]');
}
function historyValue(value:unknown):{value:unknown;redacted:boolean;partial:boolean} {
  let redacted=false;
  const encoded=JSON.stringify(value??null,(key,item)=>{
    if(/(?:password|secret|api[_-]?key|access[_-]?token|private[_-]?key)/i.test(key)){redacted=true;return '[redacted]';}
    if(typeof item!=='string')return item;
    const clean=redactHistoryText(item);
    if(clean!==item)redacted=true;return clean;
  });
  if(Buffer.byteLength(encoded)>4096)return {value:{unavailable:'value_exceeds_history_budget',redactedByteSize:Buffer.byteLength(encoded),sha256:hash(encoded)},redacted,partial:true};
  return {value:JSON.parse(encoded),redacted,partial:false};
}
/** Legacy immutable records remain untouched; public replay/audit never reveals prior/deleted comment bodies. */
function publicAuditPayload(raw:string):unknown {
  const payload=JSON.parse(raw);
  if(Array.isArray(payload.commentChanges))payload.commentChanges=payload.commentChanges.map((change:any)=>{
    const clean={...change,contentExcluded:true};for(const side of ['previous','current'])if(clean[side]&&typeof clean[side]==='object'){
      const {body:omitted,title:omittedTitle,...metadata}=clean[side];clean[side]=metadata;
    }return clean;
  });
  return JSON.parse(JSON.stringify(payload,(_key,item)=>typeof item==='string'?redactHistoryText(item):item));
}
function write(command: StoreWrite, promotion?: PromoteLegacy) {
  text(command.projectId); text(command.actorId); text(command.idempotencyKey);
  if (!Array.isArray(command.changes) || command.changes.length === 0 || command.changes.length > (promotion ? 10000 : 100)) fail('INVALID_COMMAND');
  if (command.outbox && (!Array.isArray(command.outbox) || command.outbox.length > 100)) fail('INVALID_COMMAND');
  if (Buffer.byteLength(JSON.stringify(command)) > 16 * 1024 * 1024) fail('COMMAND_TOO_LARGE');
  const payloadHash = hash(promotion ?? command);
  const result = transaction(() => {
    const previous = db.prepare('SELECT payload_hash,receipt FROM commands WHERE project_id=? AND idempotency_key=?')
      .get(command.projectId, command.idempotencyKey);
    if (previous) {
      if (previous.payload_hash !== payloadHash) fail('IDEMPOTENCY_CONFLICT');
      return JSON.parse(previous.receipt as string);
    }
    const scope = project(command.projectId);
    if (!scope) fail('PROJECT_NOT_FOUND');
    if (scope.authorityEpoch !== command.expectedAuthorityEpoch) fail('AUTHORITY_CONFLICT');
    // Check the pre-command state: the same atomic dispatch may insert its own run before its task row.
    if(command.taskManagerRun){
      const pin=command.taskManagerRun,row=get(scope.id,pin.id),run=(row?.data.runtimeRun??row?.data.appAgentRun) as any;
      const taskId=run?.taskId??run?.taskContext?.taskId;
      if(!row||row.kind!=='run'||!run||!['running','dispatching','awaiting_approval'].includes(row.status)||run.bindingId!==pin.bindingId
        ||run.generation!==pin.generation||taskId!==pin.taskId||!command.actorId.startsWith('agent:')
        ||!command.actorId.endsWith(`:${pin.id}`)||command.changes.some(c=>c.entity.kind==='task'&&(c.entity.id!==pin.taskId||['done','cancelled'].includes(String(c.entity.data?.status)))))fail('TOOL_SCOPE_INVALID');
    }
    if (command.requireIdle || (command.taskManagerAction&&!command.taskManagerRun)) assertIdle(scope.id);
    if(command.changes.some(c=>c.entity.data?.schemaVersion==='m2_task_profile_v1'||c.entity.id.startsWith('m2-')
      ||['m2_comment','managed_attachment'].includes(String((c.entity.data as any)?.category))))ensureM2Schema(db);
    if (promotion) {
      if(promotion.cutoverBackupId!==undefined&&(typeof promotion.cutoverBackupId!=='string'||!/^[A-Za-z0-9][A-Za-z0-9_-]{0,199}$/.test(promotion.cutoverBackupId)))fail('BACKUP_INVALID');
      if (!promotion.writerInventoryVerified || !promotion.restoreRehearsalVerified) fail('CUTOVER_GATE_FAILED');
      if (!/^[0-9a-f]{64}$/.test(promotion.sourceDigest) || promotion.sourceDigest !== promotion.verifiedSourceDigest) fail('SOURCE_DRIFT');
      if (scope.authorityMode !== 'legacy_files') fail('AUTHORITY_CONFLICT');
      assertIdle(scope.id, 'ACTIVE_RUNTIME');
      if (promotion.sourceBindings !== undefined) {
        const bindings = promotion.sourceBindings;
        const fields = new Set(['role', 'sourceName', 'sourceRelativePath', 'sourceDigest', 'byteSize']);
        if (!Array.isArray(bindings) || bindings.length < 1 || bindings.length > 2) fail('SOURCE_BINDINGS_INVALID');
        const paths = new Set<string>();
        for (const binding of bindings) {
          if (!binding || Object.keys(binding).some(key => !fields.has(key)) || !['records', 'projection'].includes(binding.role)
            || typeof binding.sourceName !== 'string' || !binding.sourceName.trim() || binding.sourceName.length > 4096
            || typeof binding.sourceRelativePath !== 'string' || !binding.sourceRelativePath || binding.sourceRelativePath.length > 4096
            || binding.sourceRelativePath.split(/[\\/]/).some((part: string) => !part || part === '.' || part === '..'
              || /[\u0000-\u001f:<>"|?*]/.test(part) || /[. ]$/.test(part)
              || /^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)/i.test(part))
            || !/^[a-f0-9]{64}$/.test(binding.sourceDigest) || !Number.isSafeInteger(binding.byteSize)
            || binding.byteSize < 0 || binding.byteSize > 1024 * 1024) fail('SOURCE_BINDINGS_INVALID');
          const path = binding.sourceRelativePath.replaceAll('\\', '/').toLowerCase();
          if (paths.has(path)) fail('SOURCE_BINDINGS_INVALID');
          paths.add(path);
        }
        if (!bindings.some(binding => binding.role === 'records') || (bindings.length === 2 && new Set(bindings.map(binding => binding.role)).size !== 2)) fail('SOURCE_BINDINGS_INVALID');
      }
      db.prepare("UPDATE projects SET authority_mode='sql',authority_epoch=authority_epoch+1 WHERE id=?").run(scope.id);
    }
    const revisions = [];
    const commentChanges = [];
    const taskChanges:Array<Record<string,unknown>>=[];let historyBytes=0;
    const issueGuardIds=new Set<string>();
    const managerChanges:Array<Record<string,unknown>>=[];
    // Only the atomic count below may assert an actual override; supplied receipt metadata is not evidence.
    for(const change of command.changes){const data=change.entity.data as Record<string,unknown>|undefined;if(data?.category==='m2_command_receipt')delete data.wipOverride;}
    const now = new Date().toISOString();
    const seen = new Set<string>();
    const searchCounts = readSearchCounts(scope.id);
    for (const change of command.changes) {
      let input = change.entity;
      text(input.id);
      if (seen.has(input.id)) fail('DUPLICATE_ENTITY');
      seen.add(input.id);
      const old = db.prepare('SELECT revision,kind,public_key,title,body,status,data,coverage,deleted FROM entities WHERE project_id=? AND id=?').get(scope.id, input.id);
      // Profile selection is itself an invariant: choosing the legacy decoder cannot remove M2 guards or fields.
      if(input.kind==='task'&&old?.kind==='task'&&JSON.parse(old.data as string).schemaVersion==='m2_task_profile_v1'
        &&input.data?.schemaVersion!=='m2_task_profile_v1')fail('PROFILE_DOWNGRADE_FORBIDDEN');
      if (input.kind === 'task' && scope.authorityMode !== 'sql' && !promotion) fail('LEGACY_AUTHORITY');
      if (input.kind === 'task') {
        let data = input.data;
        if (data?.key === '' && change.expectedRevision === 0) {
          const number = db.prepare('SELECT next_task_number FROM projects WHERE id=?').get(scope.id)!.next_task_number;
          data = { ...data, key: `${scope.keyPrefix}-${number}` };
        }
        const task = decodeM1TaskProfile(data);
        if (task.id !== input.id || task.projectId !== scope.id) fail('TASK_SCOPE_CONFLICT');
        if (!task.key.startsWith(`${scope.keyPrefix}-`)) fail('TASK_KEY_CONFLICT');
        const number = Number(task.key.split('-')[1]);
        if (!Number.isSafeInteger(number) || number >= Number.MAX_SAFE_INTEGER) fail('TASK_KEY_OUT_OF_RANGE');
        db.prepare('UPDATE projects SET next_task_number=MAX(next_task_number,?) WHERE id=?').run(number + 1, scope.id);
        input = { ...input, ...(task.schemaVersion === 'm2_task_profile_v1' ? {parentId: task.parentId} : {}), title: task.title, body: [task.summary, task.technicalValue, task.productValue, ...task.acceptanceCriteria].join('\n'), status: task.status, publicKey: task.key, data: task };
      }
      if (Buffer.byteLength(input.body ?? '') > 1024 * 1024 && input.kind !== 'document') fail('CONTENT_TOO_LARGE');
      if (!Number.isSafeInteger(change.expectedRevision) || change.expectedRevision < 0
        || (old?.revision ?? 0) !== change.expectedRevision) fail('REVISION_CONFLICT');
      if (old && old.kind !== input.kind) fail('ENTITY_KIND_CONFLICT');
      if (old && input.kind === 'task' && old.public_key !== input.publicKey) fail('TASK_KEY_IMMUTABLE');
      if(input.kind==='task'&&(!old||old.status!==input.status))issueGuardIds.add(input.id);
      if(input.kind==='task'&&!promotion&&db.prepare('SELECT 1 FROM schema_migrations WHERE version=2').get()){
        const profile=input.data as TaskProfile,prior=old?JSON.parse(old.data as string) as TaskProfile:null;
        for(const ref of profile.links.filter(link=>link.relation!=='related'&&!prior?.links.some(old=>JSON.stringify(old)===JSON.stringify(link)))){
          const targetId=ref.relation==='blocked_by'?profile.id:ref.taskId;
          if(db.prepare(`SELECT 1 FROM entities WHERE project_id=? AND kind='run' AND deleted=0 AND status NOT IN ('completed','failed','interrupted')
            AND (json_extract(data,'$.runtimeRun.taskId')=? OR json_extract(data,'$.appAgentRun.taskContext.taskId')=?) LIMIT 1`).get(scope.id,targetId,targetId))fail('ACTIVE_RUN_RECONCILIATION_REQUIRED');
        }
      }
      if (input.parentId && !get(scope.id, input.parentId)) fail('PARENT_SCOPE_CONFLICT');
      if (input.parentId === input.id || (input.parentId && (['session','settings','document'].includes(input.kind)
        || (input.kind === 'task' && input.data?.schemaVersion !== 'm2_task_profile_v1')))) fail('PARENT_KIND_CONFLICT');
      if (input.kind === 'task' && input.data?.schemaVersion === 'm2_task_profile_v1') {
        const task = input.data as M2TaskProfile;
        const before = old ? JSON.parse(old.data as string) as TaskProfile : null;
        if(!before||before.status!==task.status)issueGuardIds.add(task.id);
        if(task.parentId&&(!before||(before as M2TaskProfile).parentId!==task.parentId))issueGuardIds.add(task.parentId);
        if (before && JSON.stringify(before.creator)!==JSON.stringify(task.creator)) fail('CREATOR_IMMUTABLE');
        if (before?.schemaVersion==='m2_task_profile_v1' && (before.createdAt!==task.createdAt || before.initiatedBy!==task.initiatedBy)) fail('CREATOR_IMMUTABLE');
        if(before?.schemaVersion==='m2_task_profile_v1'){
          const old=before as M2TaskProfile;
          if(old.dueDate!==task.dueDate&&!command.taskManagerReason?.trim()&&!command.taskManagerReviewReason?.trim())fail('DUE_DATE_REASON_REQUIRED');
          if(old.status==='done'&&task.status==='done'&&['summary','technicalValue','productValue','files','artifactReferences','acceptanceCriteria','criteriaEvidence','scopeExclusions','parentId','type','artifacts','fileContexts','estimateSeconds','blocker']
            .some(field=>JSON.stringify((old as any)[field])!==JSON.stringify((task as any)[field])))fail('REOPEN_REQUIRED');
          if(old.status===task.status&&old.resolution!==task.resolution&&!command.taskManagerAction)fail('TRANSITION_REQUIRED');
          if(old.status===task.status&&['dependency_review','scope_review','recovery_review','acceptance_unverified'].some(flag=>old.risks.includes(flag)&&!task.risks.includes(flag))){
            if(!command.taskManagerReviewReason?.trim()||command.actorId.startsWith('agent:'))fail('SYSTEM_REVIEW_REQUIRED');
            issueGuardIds.add(task.id);
          }
        }
        if(task.hotfixReason!==((before as M2TaskProfile|null)?.hotfixReason??null)&&command.taskManagerAction!=='transition')fail('HOTFIX_APPROVAL_REQUIRED');
        if (!before && (task.status!=='backlog' || task.resolution!==null)) fail('INITIAL_STATUS_REQUIRED');
        if (before && before.status!==task.status) {
          if (!command.taskManagerAction || !transitionAllowed(before.status,task.status,command.taskManagerAction==='complete')) fail('TRANSITION_REQUIRED');
          if (['done','cancelled'].includes(task.status) && !command.taskManagerReason?.trim()) fail('REASON_REQUIRED');
          if (task.status==='done' && (!task.acceptanceCriteria.length || task.acceptanceCriteria.some(c=>!task.criteriaEvidence.some(e=>e.criterion===c&&e.outcome==='passed'&&e.evidence.trim())))) fail('CRITERIA_EVIDENCE_REQUIRED');
          if(task.blocker&&['in_progress','done'].includes(task.status))fail('BLOCKER_RESOLUTION_REQUIRED');
        }
        if(before?.schemaVersion==='m2_task_profile_v1'&&task.blocker&&JSON.stringify(before.blocker)!==JSON.stringify(task.blocker))assertIdle(scope.id);
        if ((task.status==='ready' || task.status==='in_progress')&&!(before?.schemaVersion==='m1_task_profile_v1'&&before.status===task.status&&task.risks.includes('recovery_review'))) validateReady(task);
        const board=get(scope.id,'m2-board')?.data.value as any;
        if(['ready','in_progress'].includes(task.status)&&(board?.releaseRequiredTypes?.includes(task.type)||board?.releaseRequiredComponents?.some((id:string)=>task.components.includes(id)))
          &&!task.fixVersions.length&&!task.hotfixReason&&!command.taskManagerHotfixReason)fail('TARGET_RELEASE_REQUIRED');
        if(before&&before.status!==task.status){
          const column=board?.columns?.find((c:any)=>c.statuses.includes(task.status));
          if(column?.wipLimit!==undefined&&!column.statuses.includes(before.status)){
            const count=db.prepare("SELECT status FROM entities WHERE project_id=? AND kind='task' AND deleted=0 AND id<>?").all(scope.id,task.id).filter(r=>column.statuses.includes(r.status)).length;
            if(count>=column.wipLimit&&column.wipMode==='hard')fail('HARD_WIP_LIMIT');
            if(count>=column.wipLimit&&column.wipMode==='soft'){
              const receipt=command.changes.find(c=>{const data=c.entity.data as Record<string,unknown>|undefined;return data?.category==='m2_command_receipt'&&data.action==='transition'&&data.taskId===task.id;})?.entity.data as Record<string,unknown>|undefined;
              if(receipt?.softWipOverrideRequested!==true)fail('SOFT_WIP_CONFIRMATION_REQUIRED');
              if(!command.taskManagerReason?.trim())fail('REASON_REQUIRED');
              receipt.wipOverride={override:true,columnId:column.id,limit:column.wipLimit,count,actorId:command.actorId,reason:command.taskManagerReason};
            }
          }
        }
        if ((task.status==='done' && task.resolution!=='completed') || (task.status==='cancelled' && !['cancelled','duplicate','wont_do'].includes(task.resolution??''))
          || (!['done','cancelled'].includes(task.status)&&task.resolution!==null)) fail('RESOLUTION_REQUIRED');
      }
      const expectedParent = requiredParentKinds[input.kind];
      if (expectedParent && (!input.parentId || get(scope.id, input.parentId)?.kind !== expectedParent)) fail('PARENT_KIND_CONFLICT');
      if (change.delete && db.prepare('SELECT 1 FROM entities WHERE project_id=? AND parent_id=? AND deleted=0').get(scope.id, input.id)) fail('ENTITY_HAS_CHILDREN');
      const revision = change.expectedRevision + 1;
      db.prepare(`INSERT INTO entities (project_id,id,kind,parent_id,title,body,status,public_key,coverage,data,revision,deleted,updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(project_id,id) DO UPDATE SET
        parent_id=excluded.parent_id,title=excluded.title,body=excluded.body,status=excluded.status,public_key=excluded.public_key,
        coverage=excluded.coverage,data=excluded.data,revision=excluded.revision,deleted=excluded.deleted,updated_at=excluded.updated_at`)
        .run(scope.id, input.id, input.kind, input.parentId ?? null, input.title ?? '', input.body ?? '', input.status ?? '',
          input.publicKey ?? null, input.coverage ?? 'complete', JSON.stringify(input.data ?? {}), revision, change.delete ? 1 : 0, now);
      revisions.push({ id: input.id, revision });
      if(input.kind==='task') {
        const previous=old?JSON.parse(old.data as string) as Record<string,unknown>:{};
        const current=input.data as Record<string,unknown>;
        const fields=[];
        for(const field of Object.keys(current))if(JSON.stringify(previous[field])!==JSON.stringify(current[field])) {
          const before=historyValue(previous[field]),after=historyValue(current[field]);
          fields.push({field,previous:before.value,current:after.value,redacted:before.redacted||after.redacted,coverage:before.partial||after.partial?'partial':'complete'});
        }
        if(Boolean(old?.deleted)!==Boolean(change.delete))fields.push({field:'deleted',previous:Boolean(old?.deleted),current:Boolean(change.delete),redacted:false,coverage:'complete'});
        const acceptance=command.changes.find(item=>item.entity.kind==='comment'&&item.entity.parentId===input.id&&(item.entity.data as Record<string,unknown>|undefined)?.category==='owner_acceptance');
        const reason=acceptance?.entity.body?historyValue(acceptance.entity.body).value:null;
        const entry={id:input.id,previousRevision:old?.revision??null,currentRevision:revision,operation:change.delete?'delete':old?'update':'create',
          source:promotion?'import_promotion':'transactional_command',reason,fields,coverage:fields.some(field=>field.coverage==='partial')?'partial':'complete'};
        const bytes=Buffer.byteLength(JSON.stringify(entry));
        if(historyBytes+bytes<=256*1024){taskChanges.push(entry);historyBytes+=bytes;}
        else taskChanges.push({...entry,fields:[],coverage:'partial',omittedFields:fields.length});
      }
      if (old && !old.deleted) {
        if (searchableKinds.includes(old.kind as string)) searchCounts.eligible--;
        if (old.coverage !== 'complete') searchCounts.incomplete--;
      }
      if (!change.delete) {
        if (searchableKinds.includes(input.kind)) searchCounts.eligible++;
        if ((input.coverage ?? 'complete') !== 'complete') searchCounts.incomplete++;
      }
      if (input.kind === 'comment') commentChanges.push({ id: input.id,parentId:input.parentId??null,contentExcluded:true,category:(input.data as Record<string,unknown>|undefined)?.category??null,
        previous: old ? { revision: old.revision } : null,
        current: { revision, deleted: Boolean(change.delete) } });
      const metadata=input.data as Record<string,unknown>|undefined;
      if((input.kind==='settings'&&input.id.startsWith('m2-'))||metadata?.category==='managed_attachment'||metadata?.category==='m2_command_receipt'){
        const before=historyValue(old?JSON.parse(old.data as string):null),after=historyValue(input.data);
        managerChanges.push({id:input.id,kind:input.kind,taskId:metadata?.taskId??null,previous:before.value,current:after.value,redacted:before.redacted||after.redacted,revision});
      }
      db.prepare('DELETE FROM entity_blobs WHERE project_id=? AND entity_id=?').run(scope.id, input.id);
      for (const blobId of input.blobIds ?? []) {
        if (!db.prepare('SELECT 1 FROM blobs WHERE project_id=? AND id=?').get(scope.id, blobId)) fail('BLOB_SCOPE_CONFLICT');
        db.prepare('INSERT INTO entity_blobs VALUES (?,?,?)').run(scope.id, input.id, blobId);
      }
      db.prepare('INSERT INTO index_jobs VALUES (?,?,?) ON CONFLICT(project_id,entity_id) DO UPDATE SET revision=excluded.revision')
        .run(scope.id, input.id, revision);
    }
    if (command.changes.some(c=>c.entity.kind==='task' || c.entity.id==='m2-links')
      &&db.prepare("SELECT 1 FROM schema_migrations WHERE version=2").get()) {
      const tasks=db.prepare("SELECT data FROM entities WHERE project_id=? AND kind='task' AND deleted=0").all(scope.id).map(row=>decodeM1TaskProfile(JSON.parse(row.data as string)));
      const links=canonicalIssueLinks(tasks,(get(scope.id,'m2-links')?.data.items??[]) as IssueLink[]);
      const components=(get(scope.id,'m2-components')?.data.items??['BackEnd','FrontEnd','DB','RAG','LLM','Design','Marketing','Integrations','DevOps','QA','Analytic'].map(id=>({id}))) as {id:string}[];
      const versions=(get(scope.id,'m2-versions')?.data.items??[]) as {id:string}[];
      for(const task of tasks){if(task.schemaVersion!=='m2_task_profile_v1')continue;
        if(task.components.some(id=>!components.some(c=>c.id===id)))fail('COMPONENT_NOT_FOUND');
        if([...task.affectsVersions,...task.fixVersions].some(id=>!versions.some(c=>c.id===id)))fail('VERSION_NOT_FOUND');
      }
      validateIssueGraph(tasks,links,issueGuardIds);
      for(const task of tasks)if(task.schemaVersion==='m2_task_profile_v1'&&issueGuardIds.has(task.id)&&task.resolution==='duplicate'
        &&!links.some(link=>link.sourceId===task.id&&link.relation==='duplicates'))fail('CANONICAL_DUPLICATE_REQUIRED');
    }
    if(command.changes.some(c=>(c.entity.data as Record<string,unknown>|undefined)?.category==='managed_attachment')){
      const board=get(scope.id,'m2-board')?.data.value as any;
      const attachments=db.prepare("SELECT data FROM entities WHERE project_id=? AND kind='document' AND deleted=0 AND json_extract(data,'$.category')='managed_attachment'").all(scope.id).map(row=>JSON.parse(row.data as string));
      const totals=new Map<string,number>();
      for(const attachment of attachments){if(attachment.status==='deleted')continue;
        if(!get(scope.id,attachment.taskId)||attachment.byteSize>(board?.attachmentFileBytes??50*1024*1024))fail('FILE_QUOTA_EXCEEDED');
        totals.set(attachment.taskId,(totals.get(attachment.taskId)??0)+attachment.byteSize);
      }
      if([...totals.values()].some(n=>n>(board?.attachmentTaskBytes??500*1024*1024)))fail('TASK_QUOTA_EXCEEDED');
    }
    saveSearchCounts(scope.id, searchCounts);
    for (const change of command.changes) {
      if (change.entity.kind !== 'task') continue;
      const task = decodeM1TaskProfile(get(scope.id, change.entity.id)?.data ?? change.entity.data);
      db.prepare('DELETE FROM task_links WHERE project_id=? AND owner_id=?').run(scope.id, task.id);
      db.prepare('DELETE FROM task_sessions WHERE project_id=? AND task_id=?').run(scope.id, task.id);
      if (change.delete) continue;
      for (const link of task.links) {
        if (get(scope.id, link.taskId)?.kind !== 'task') fail('TASK_LINK_CONFLICT');
        let source = task.id;
        let target = link.taskId;
        if (link.relation === 'blocked_by' || (link.relation === 'related' && source > target)) [source, target] = [target, source];
        db.prepare('INSERT OR IGNORE INTO task_links VALUES (?,?,?,?,?)').run(scope.id, task.id, source, target, link.relation === 'related' ? 'related' : 'blocks');
        if (link.relation !== 'related' && db.prepare(`WITH RECURSIVE reachable(id) AS (
          SELECT target_id FROM task_links WHERE project_id=? AND source_id=? AND relation='blocks'
          UNION SELECT l.target_id FROM task_links l JOIN reachable r ON l.source_id=r.id WHERE l.project_id=? AND l.relation='blocks'
        ) SELECT 1 FROM reachable WHERE id=?`).get(scope.id, target, scope.id, source)) fail('TASK_LINK_CYCLE');
      }
      for (const sessionId of task.sessionIds) {
        if (get(scope.id, sessionId)?.kind !== 'session') fail('TASK_SESSION_CONFLICT');
        db.prepare('INSERT INTO task_sessions VALUES (?,?,?)').run(scope.id, task.id, sessionId);
      }
      if (promotion) {
        db.prepare('INSERT INTO import_mappings VALUES (?,?,?,?)').run(scope.id, task.provenance?.sourceId ?? task.legacyAlias ?? task.id, task.id, promotion.sourceDigest);
      }
    }
    const commandId = randomUUID();
    if (promotion?.sourceBindings) {
      const id = 'runtime-import-sources';
      const data = { schemaVersion: 1, category: 'import_source_bindings', authorityEpoch: scope.authorityEpoch + 1,
        sourceDigest: promotion.sourceDigest, bindings: promotion.sourceBindings.map(binding => ({ ...binding,
          sourceRelativePath: binding.sourceRelativePath.replaceAll('\\', '/') })) };
      db.prepare(`INSERT INTO entities(project_id,id,kind,parent_id,title,body,status,public_key,coverage,data,revision,deleted,updated_at)
        VALUES (?,?,'settings',NULL,'Imported sources','','bound',NULL,'complete',?,1,0,?)`).run(scope.id, id, JSON.stringify(data), now);
      revisions.push({ id, revision: 1 });
    }
    const seq = (db.prepare('SELECT COALESCE(MAX(seq),0) AS seq FROM events WHERE project_id=?').get(scope.id)!.seq as number) + 1;
    const receipt = { commandId, projectId: scope.id, seq, revisions,...(promotion?.cutoverBackupId?{cutoverBackupId:promotion.cutoverBackupId}:{}) };
    db.prepare('INSERT INTO commands VALUES (?,?,?,?,?)').run(scope.id, commandId, command.idempotencyKey, payloadHash, JSON.stringify(receipt));
    const payload = JSON.stringify({ schemaVersion: 1,commandId, revisions, commentChanges,taskChanges,...(managerChanges.length?{managerChanges}:{}) });
    if (Buffer.byteLength(payload) > 16 * 1024 * 1024) fail('AUDIT_TOO_LARGE');
    db.prepare('INSERT INTO events VALUES (?,?,?,?,?,?,?)').run(scope.id, seq, randomUUID(), commandId, command.actorId, now, payload);
    for (const job of command.outbox ?? []) {
      text(job.kind);
      db.prepare('INSERT INTO outbox VALUES (?,?,?,?,?,?)').run(randomUUID(), scope.id, commandId, job.kind, JSON.stringify(job.payload), 'pending');
    }
    return receipt;
  });
  // Business state is committed before touching a rebuildable derived index.
  // A failed refresh leaves durable jobs and partial coverage for an explicit rebuild/retry.
  try {
    transaction(() => {
      const counts = readSearchCounts(command.projectId);
      for (const job of db.prepare('SELECT * FROM index_jobs WHERE project_id=?').all(command.projectId)) {
        const current = db.prepare('SELECT revision FROM entities WHERE project_id=? AND id=?').get(command.projectId, job.entity_id);
        if (current?.revision === job.revision) counts.indexed += indexEntity(command.projectId, job.entity_id as string);
        db.prepare('DELETE FROM index_jobs WHERE project_id=? AND entity_id=? AND revision=?').run(command.projectId, job.entity_id, job.revision);
      }
      saveSearchCounts(command.projectId, counts);
    });
  } catch {}
  return result;
}

function dispatch(method: string, params: any, requestId: number): unknown {
  switch (method) {
    case 'registerProject': {
      for (const value of [params.id, params.canonicalRoot, params.rootIdentity]) text(value);
      if (!/^[A-Z]{4}$/.test(params.keyPrefix) || !['legacy_files', 'sql'].includes(params.authorityMode)) fail('INVALID_PROJECT');
      const canonicalRoot = process.platform === 'win32' ? params.canonicalRoot.toLowerCase() : params.canonicalRoot;
      const previous = project(params.id);
      if (previous) {
        if (previous.canonicalRoot !== canonicalRoot || previous.rootIdentity !== params.rootIdentity || previous.keyPrefix !== params.keyPrefix) fail('PROJECT_IDENTITY_CONFLICT');
        return previous;
      }
      if (db.prepare('SELECT 1 FROM projects WHERE canonical_root=? OR root_identity=? OR key_prefix=?').get(canonicalRoot, params.rootIdentity, params.keyPrefix)) fail('PROJECT_IDENTITY_CONFLICT');
      db.prepare('INSERT INTO projects(id,key_prefix,display_name,canonical_root,root_identity,authority_mode,authority_epoch) VALUES (?,?,?,?,?,?,1)')
        .run(params.id, params.keyPrefix, params.displayName ?? params.keyPrefix, canonicalRoot, params.rootIdentity, params.authorityMode);
      transaction(() => initializeSearchCounts(params.id));
      return project(params.id);
    }
    case 'projects': return db.prepare('SELECT id FROM projects ORDER BY id').all().map(row => project(row.id as string));
    case 'project': return project(params.projectId);
    case 'compatibility': return databaseCompatibility(db);
    case 'projectEntities': {
      const rows=db.prepare('SELECT * FROM entities WHERE project_id=? AND deleted=0 ORDER BY id LIMIT 100001').all(params.projectId);
      if(rows.length>100000||rows.reduce((n,r)=>n+Buffer.byteLength(r.data as string)+Buffer.byteLength(r.body as string),0)>64*1024*1024)fail('SNAPSHOT_TOO_LARGE');
      return rows.map(entity);
    }
    case 'exportTasks': {
      db.exec('BEGIN');
      try {
        const scope = project(params.projectId);
        if (!scope) fail('PROJECT_NOT_FOUND');
        if (scope.authorityMode !== 'sql') fail('LEGACY_AUTHORITY');
        const rows = db.prepare("SELECT data FROM entities WHERE project_id=? AND kind='task' AND deleted=0 ORDER BY id LIMIT 10001").all(scope.id);
        if (rows.length > 10000 || rows.reduce((bytes, row) => bytes + Buffer.byteLength(row.data as string), 0) > 16 * 1024 * 1024) fail('EXPORT_SNAPSHOT_REQUIRED');
        const tasks = rows.map(row => decodeM1TaskProfile(JSON.parse(row.data as string)));
        const generation = db.prepare("SELECT value FROM store_meta WHERE key='stream_generation'").get()!.value;
        const throughSeq = db.prepare('SELECT COALESCE(MAX(seq),0) AS seq FROM events WHERE project_id=?').get(scope.id)!.seq;
        db.exec('COMMIT');
        return { project: scope, tasks, generation, throughSeq };
      } catch (error) { db.exec('ROLLBACK'); throw error; }
    }
    case 'putBlob': {
      if (!project(params.projectId)) fail('PROJECT_NOT_FOUND');
      return writeBlob(workerData.databasePath, params.projectId, params.bytes).then(blob => {
        db.prepare('INSERT INTO blobs VALUES (?,?,?,?)').run(blob.projectId, blob.id, blob.sha256, blob.byteSize);
        return blob;
      });
    }
    case 'readBlob': {
      const row=db.prepare('SELECT * FROM blobs WHERE project_id=? AND id=?').get(params.projectId,params.id);
      if(!row)fail('BLOB_NOT_FOUND');
      return readManagedBlob(workerData.databasePath,{id:row.id as string,projectId:row.project_id as string,sha256:row.sha256 as string,byteSize:row.byte_size as number});
    }
    case 'discardUnreferencedBlob': return transaction(()=>{
      if(typeof params.id!=='string'||!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(params.id))fail('INVALID_BLOB');
      const row=db.prepare('SELECT 1 FROM blobs WHERE project_id=? AND id=?').get(params.projectId,params.id);
      if(!row)return {discarded:false,reason:'not_found'};
      if(db.prepare('SELECT 1 FROM entity_blobs WHERE project_id=? AND blob_id=? LIMIT 1').get(params.projectId,params.id))return {discarded:false,reason:'referenced'};
      const intended=resolve(blobDirectory(workerData.databasePath)),directory=realpathSync(intended);
      const normalize=(v:string)=>process.platform==='win32'?v.toLowerCase():v;
      if(normalize(directory)!==normalize(intended))fail('BLOB_PATH_CONFLICT');
      const target=resolve(join(directory,params.id));if(dirname(target)!==directory)fail('BLOB_PATH_CONFLICT');
      try{const info=lstatSync(target);if(!info.isFile()||info.isSymbolicLink())fail('BLOB_PATH_CONFLICT');unlinkSync(target);}
      catch(error){if((error as any).code!=='ENOENT')throw error;}
      db.prepare('DELETE FROM blobs WHERE project_id=? AND id=?').run(params.projectId,params.id);return {discarded:true};
    });
    case 'backup': return createSnapshot(db, workerData.databasePath, params.outputRoot);
    case 'write': return write(params);
    case 'receipt': {
      const row = db.prepare('SELECT receipt FROM commands WHERE project_id=? AND idempotency_key=?').get(params.projectId, params.idempotencyKey);
      return row ? JSON.parse(row.receipt as string) : null;
    }
    case 'search': return search(params);
    case 'rebuildSearch': return transaction(() => {
      db.exec("CREATE VIRTUAL TABLE IF NOT EXISTS search_fts USING fts5(title,body,tokenize='unicode61',prefix='2 3')");
      const key = `index_generation:${params.projectId}`;
      db.prepare("INSERT INTO store_meta VALUES (?,'2') ON CONFLICT(key) DO UPDATE SET value=CAST(CAST(value AS INTEGER)+1 AS TEXT)").run(key);
      const ids = db.prepare('SELECT id FROM entities WHERE project_id=?').all(params.projectId);
      const counts = readSearchCounts(params.projectId);
      for (const [index, row] of ids.entries()) {
        if (Atomics.load(new Int32Array(params.cancelBuffer), 0) !== 0) fail('INDEX_REBUILD_CANCELLED');
        counts.indexed += indexEntity(params.projectId, row.id as string);
        if ((index + 1) % 100 === 0 || index + 1 === ids.length) parentPort!.postMessage({ id: requestId, progress: { completed: index + 1, total: ids.length } });
      }
      if (Atomics.load(new Int32Array(params.cancelBuffer), 0) !== 0) fail('INDEX_REBUILD_CANCELLED');
      db.prepare('DELETE FROM index_jobs WHERE project_id=?').run(params.projectId);
      saveSearchCounts(params.projectId, counts);
      db.prepare('INSERT INTO store_meta VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value').run(`search_format:${params.projectId}`, searchIndexFormat);
    });
    case 'promoteLegacy': return write({ projectId: params.projectId, actorId: params.actorId, idempotencyKey: params.idempotencyKey,
      expectedAuthorityEpoch: params.expectedAuthorityEpoch,
      changes: params.items.map((task: any) => ({ expectedRevision: 0, entity: { id: task.id, kind: 'task', data: task } })),
    }, params);
    case 'get': return get(params.projectId, params.id);
    case 'list': {
      const { limit, offset } = page(params.limit, params.offset);
      if (params.order !== undefined) {
        if (params.order !== 'newest' || params.kind !== 'message' || typeof params.parentId !== 'string') fail('INVALID_PAGINATION');
        // Row ordinals are local to this DB generation. New messages must remain visible after a large history.
        return db.prepare(`SELECT rowid AS journal_order,* FROM entities NOT INDEXED WHERE project_id=? AND kind='message'
          AND deleted=0 AND parent_id=? ORDER BY rowid DESC LIMIT ? OFFSET ?`)
          .all(params.projectId, params.parentId, limit, offset).map(row => ({ ...entity(row), journalOrder: row.journal_order as number }));
      }
      return db.prepare(`SELECT * FROM entities WHERE project_id=? AND deleted=0
        AND (? IS NULL OR kind=?) AND (? IS NULL OR parent_id=?) ORDER BY id LIMIT ? OFFSET ?`)
        .all(params.projectId, params.kind ?? null, params.kind ?? null, params.parentId ?? null, params.parentId ?? null, limit, offset).map(entity);
    }
    case 'events':
    case 'audit': {
      const generation = db.prepare("SELECT value FROM store_meta WHERE key='stream_generation'").get()!.value;
      if (params.generation !== undefined && params.generation !== generation) fail('CURSOR_STALE');
      const { limit } = page(params.limit);
      if (!Number.isSafeInteger(params.after ?? 0) || (params.after ?? 0) < 0) fail('INVALID_CURSOR');
      const cutoff = method === 'events' ? new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString() : '';
      if (method === 'events' && (params.after ?? 0) > 0) {
        const cursor = db.prepare('SELECT occurred_at FROM events WHERE project_id=? AND seq=?').get(params.projectId, params.after);
        if (!cursor || (cursor.occurred_at as string) < cutoff) fail('CURSOR_STALE', 'Replay cursor expired or unknown; load a new project snapshot');
      }
      const rows = db.prepare('SELECT * FROM events WHERE project_id=? AND seq>? AND occurred_at>=? ORDER BY seq LIMIT ?')
        .all(params.projectId, params.after ?? 0, cutoff, limit + 1);
      const items = [];
      let bytes = 0;
      const byteLimit = method === 'audit' ? 16 * 1024 * 1024 : 1024 * 1024;
      for (const row of rows.slice(0, limit)) {
        const item = { seq: row.seq, eventId: row.event_id, actorId: row.actor_id, occurredAt: row.occurred_at, payload: publicAuditPayload(row.payload as string) };
        const size = Buffer.byteLength(JSON.stringify(item));
        if (bytes + size > byteLimit) {
          if (!items.length) fail('EVENT_SNAPSHOT_REQUIRED', 'Event exceeds the replay budget; load a project snapshot');
          break;
        }
        bytes += size;
        items.push(item);
      }
      return { generation, items, hasMore: rows.length > items.length };
    }
    case 'outbox': return db.prepare('SELECT * FROM outbox WHERE project_id=? ORDER BY id').all(params.projectId)
      .map(row => ({ id: row.id, kind: row.kind, payload: JSON.parse(row.payload as string), state: row.state }));
    case 'acknowledgeOutbox': db.prepare("UPDATE outbox SET state='acknowledged' WHERE project_id=? AND id=? AND state='pending'").run(params.projectId, params.id); return;
    case 'close': db.close(); return;
    default: fail('UNKNOWN_STORAGE_METHOD');
  }
}

try {
  db = new DatabaseSync(workerData.databasePath, { enableForeignKeyConstraints: true, timeout: 5000 });
  migrate(db, randomUUID());
  if (db.prepare('PRAGMA journal_mode=WAL').get()?.journal_mode !== 'wal') fail('WAL_UNAVAILABLE');
  db.exec('PRAGMA synchronous=FULL; PRAGMA busy_timeout=5000');
  transaction(() => {
    for (const row of db.prepare('SELECT id FROM projects').all()) initializeSearchCounts(row.id as string);
  });
  parentPort!.postMessage({ id: 0 });
  let queue = Promise.resolve();
  parentPort!.on('message', ({ id, method, params }) => {
    queue = queue.then(async () => {
      try { parentPort!.postMessage({ id, value: await dispatch(method, params, id) }); }
      catch (error) {
        const failure = error as Error & { code?: string;cyclePath?:string[] };
        parentPort!.postMessage({ id, error: { message: failure.message, code: failure.code ?? 'STORAGE_FAILURE',
          ...(Array.isArray(failure.cyclePath)?{cyclePath:failure.cyclePath.slice(0,100),cyclePathTruncated:failure.cyclePath.length>100}:{}) } });
      }
    });
  });
} catch (error) {
  try { db!?.close(); } catch {}
  const failure = error as Error & { code?: string };
  parentPort!.postMessage({ id: 0, error: { message: failure.message, code: failure.code ?? 'STORAGE_FAILURE' } });
}
