import { parentPort, workerData } from 'node:worker_threads';
import { createHash, randomUUID } from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';
import { unlinkSync,realpathSync,lstatSync } from 'node:fs';
import { resolve,join,dirname } from 'node:path';
import { migrate,ensureM2Schema,ensureM2BSchema,databaseCompatibility } from './migrations/schema.mts';
import { decodeTaskProfile as decodeM1TaskProfile, validateIssueGraph, validateReady, canonicalIssueLinks, type M2TaskProfile, type TaskProfile, type IssueLink } from '../../../../packages/contracts/issues/task-profile.ts';
import {workflowWriteContext,validateWorkflowTask,validateWorkflowBoard} from '../workflows/guards.mts';
import {ownsTask,recipeScopeHash,recipeHash,type Execution} from '../execution-recipes/contract.mts';
import {validateSchedulerWrite,type WorkspaceLock} from '../scheduler/storage-guards.mts';
import {workflowCategory} from '../workflows/registry.mts';
import { createSnapshot, writeBlob, readManagedBlob,blobDirectory } from './snapshot.mts';
import { RANKED_SEARCH_SQL } from './search-queries.mts';
import {historySnapshotPage,artifactSummaryRows,artifactDocumentRow} from './history-snapshots.mts';
import {safePersistedText,safeVisibleValue,safeRuntimeData,isHiddenMessage} from '../redaction/persisted.mts';
import {teamId,previewAsset,applyAsset} from '../team/contract.mts';
import type {TeamRegistry} from '../../../../packages/contracts/team/assets.ts';
import {sourceCatalog,sourceAsset,projectAssetRoots,type AssetRoot} from '../team/sources.mts';
import type { EntityKind, Project, PromoteLegacy, StoreWrite, StoredEntity } from '../../../../packages/contracts/storage/local-store.ts';
import {inventoryScopeFingerprint} from '../project-inventory/scope.mts';
import type {DocumentApplyJournal,DocumentApplyRecord} from '../../../../packages/contracts/artifacts/document-apply.ts';

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
  const policyRow=row?db.prepare('SELECT value FROM store_meta WHERE key=?').get(`project_inventory_policy_v1:${projectId}`):null;
  let inventoryPolicy:Project['inventoryPolicy'];
  if(policyRow){try{const saved=JSON.parse(String(policyRow.value));if(!Number.isSafeInteger(saved.version)||!saved.value||saved.value.schemaVersion!=='paos_inventory_policy_v1')fail('PROJECT_POLICY_UNAVAILABLE');inventoryPolicy=saved.value.policy;}catch{fail('PROJECT_POLICY_UNAVAILABLE');}}
  return row ? { id: row.id as string, keyPrefix: row.key_prefix as string, canonicalRoot: row.canonical_root as string,
    displayName: row.display_name as string, rootIdentity: row.root_identity as string,
    authorityMode: row.authority_mode as Project['authorityMode'], authorityEpoch: row.authority_epoch as number,...(inventoryPolicy?{inventoryPolicy}:{}) } : null;
}
function entity(row: Record<string, any>): StoredEntity {
  if(row.kind==='message'&&isHiddenMessage(JSON.parse(row.data)))row={...row,title:'',body:'',coverage:'unavailable',data:JSON.stringify({visibility:'hidden',unavailable:'hidden_content_excluded'})};
  return { projectId: row.project_id, id: row.id, kind: row.kind, parentId: row.parent_id, title: ['session','message'].includes(row.kind)?safePersistedText(row.title):row.title, body: ['session','message'].includes(row.kind)?safePersistedText(row.body):row.body,
    status: row.status, publicKey: row.public_key, coverage: row.coverage, data: row.kind==='run'?safeRuntimeData(JSON.parse(row.data)):['message','session'].includes(row.kind)?safeVisibleValue(JSON.parse(row.data)):JSON.parse(row.data), revision: row.revision,
    deleted: Boolean(row.deleted), updatedAt: row.updated_at,
    blobIds: db.prepare('SELECT blob_id FROM entity_blobs WHERE project_id=? AND entity_id=? ORDER BY blob_id').all(row.project_id, row.id).map(blob => blob.blob_id as string) };
}
function get(projectId: string, id: string) {
  const row = db.prepare('SELECT * FROM entities WHERE project_id=? AND id=? AND deleted=0').get(projectId, id);
  return row ? entity(row) : null;
}
function projectFreshness(projectId:string){
  const scope=project(projectId);if(!scope)fail('PROJECT_NOT_FOUND');
  const version=(namespace:string)=>{const row=db.prepare('SELECT value FROM store_meta WHERE key=?').get(`${namespace}:${projectId}`);if(!row)return 0;let saved:any;try{saved=JSON.parse(String(row.value));}catch{fail('PROJECT_STATE_UNAVAILABLE');}if(!Number.isSafeInteger(saved.version)||saved.version<1)fail('PROJECT_STATE_UNAVAILABLE');return saved.version as number;};
  return {schemaVersion:'paos_project_freshness_v1' as const,projectId,generation:String(db.prepare("SELECT value FROM store_meta WHERE key='stream_generation'").get()!.value),throughSeq:Number(db.prepare('SELECT COALESCE(MAX(seq),0) AS seq FROM events WHERE project_id=?').get(projectId)!.seq),scanVersion:version('project_scan_v1'),policyVersion:version('project_inventory_policy_v1'),rootIdentity:scope!.rootIdentity};
}
function projectRows(projectId:string,options:{kinds?:string[];includeManagedAttachments?:true}={}){
  const kinds=options.kinds;
  if(kinds!==undefined&&(!Array.isArray(kinds)||!kinds.length||kinds.length>10||kinds.some(k=>!['task','session','message','draft','comment','settings','document','run','approval','evidence'].includes(k)))||options.includeManagedAttachments!==undefined&&options.includeManagedAttachments!==true)fail('INVALID_QUERY');
  const filter=kinds?` AND (kind IN (${kinds.map(()=>'?').join(',')})${options.includeManagedAttachments?" OR (kind='document' AND json_extract(data,'$.category')='managed_attachment')":''})`:'';
  // Select the consumer's kinds before applying the unchanged safety budget.
  const rows=db.prepare('SELECT * FROM entities WHERE project_id=? AND deleted=0'+filter+' ORDER BY id LIMIT 100001').all(projectId,...(kinds??[]));
  if(rows.length>100000||rows.reduce((n,r)=>n+Buffer.byteLength(r.data as string)+Buffer.byteLength(r.body as string),0)>64*1024*1024)fail('SNAPSHOT_TOO_LARGE');
  return rows.map(entity);
}
function transaction<T>(operation: () => T): T {
  db.exec('BEGIN IMMEDIATE');
  try { const value = operation(); db.exec('COMMIT'); return value; }
  catch (error) { db.exec('ROLLBACK'); throw error; }
}
function documentJournal(projectId:string):DocumentApplyJournal {
  const row=db.prepare('SELECT value FROM store_meta WHERE key=?').get(`document_apply_journal_v1:${projectId}`);
  if(!row)return {version:0,records:[]};
  try{const value=JSON.parse(String(row.value));if(!Number.isSafeInteger(value.version)||!Array.isArray(value.records)||value.records.length>4)fail('DOCUMENT_JOURNAL_UNAVAILABLE');return value;}catch{fail('DOCUMENT_JOURNAL_UNAVAILABLE');}
}
function assertDocumentIdle(projectId:string){if(documentJournal(projectId).records.some(record=>record.source.origin==='workspace_file'&&['prepared','recovery_required'].includes(record.state)))fail('DOCUMENT_WRITE_RECONCILIATION_REQUIRED');}
function saveDocumentJournal(scope:Project,input:{expectedJournalVersion:number;records:DocumentApplyRecord[];scopeFingerprint:string;generation:string}){
  if(input.scopeFingerprint!==inventoryScopeFingerprint(scope)||input.generation!==String(db.prepare("SELECT value FROM store_meta WHERE key='stream_generation'").get()!.value))fail('DOCUMENT_SCOPE_STALE');
  const old=documentJournal(scope.id);if(old.version!==input.expectedJournalVersion)fail('DOCUMENT_JOURNAL_CONFLICT');
  if(!Array.isArray(input.records)||input.records.length>4)fail('DOCUMENT_JOURNAL_LIMIT');
  const ids=new Set<string>();
  for(const record of input.records){
    if(!record||typeof record.operationId!=='string'||ids.has(record.operationId)||!['prepared','applied','not_applied','recovery_required','rolled_back'].includes(record.state)||!['local_store','workspace_file'].includes(record.source?.origin))fail('DOCUMENT_JOURNAL_INVALID');ids.add(record.operationId);
    if(Buffer.byteLength(JSON.stringify(record))>2*1024*1024)fail('DOCUMENT_JOURNAL_LIMIT');
    for(const side of ['before','after'] as const){const bytes=Buffer.from(record[side+'Base64' as 'beforeBase64'|'afterBase64'],'base64');if(bytes.length>512*1024||createHash('sha256').update(bytes).digest('hex')!==record[side+'Hash' as 'beforeHash'|'afterHash'])fail('DOCUMENT_JOURNAL_INVALID');}
    const previous=old.records.find(r=>r.operationId===record.operationId);if(!previous&&(record.authorityEpoch!==scope.authorityEpoch||record.scopeFingerprint!==input.scopeFingerprint||record.generation!==input.generation))fail('DOCUMENT_JOURNAL_INVALID');if(previous){const immutable=(r:DocumentApplyRecord)=>{const {state,result,...rest}=r;return rest;};if(hash(immutable(previous))!==hash(immutable(record)))fail('DOCUMENT_JOURNAL_CONFLICT');}
  }
  for(const record of old.records)if(['prepared','recovery_required'].includes(record.state)&&!ids.has(record.operationId))fail('DOCUMENT_WRITE_RECONCILIATION_REQUIRED');
  if(input.records.filter(record=>record.source.origin==='workspace_file'&&['prepared','recovery_required'].includes(record.state)).length>1)fail('DOCUMENT_WRITE_BUSY');
  const value={version:old.version+1,records:input.records},encoded=JSON.stringify(value);if(Buffer.byteLength(encoded)>8*1024*1024)fail('DOCUMENT_JOURNAL_LIMIT');
  db.prepare('INSERT INTO store_meta VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value').run(`document_apply_journal_v1:${scope.id}`,encoded);
}
function assertIdle(projectId: string, code = 'ACTIVE_RUN_RECONCILIATION_REQUIRED',ignoreDocumentFence=false) {
  if(!ignoreDocumentFence)assertDocumentIdle(projectId);
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
  return { items: db.prepare(RANKED_SEARCH_SQL).all(query, params.projectId, limit, offset).map(entity).filter(item=>!isHiddenMessage(item)&&tokens.every(token=>(item.title+' '+item.body).toLocaleLowerCase().includes(token.toLocaleLowerCase()))), coverage, generation };
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
  return safeVisibleValue(payload);
}
function write(command: StoreWrite, promotion?: PromoteLegacy,teamOperation?:any,trustedSourceAssets:any[]=[],documentOperation?:{trusted:true;journal?:{expectedJournalVersion:number;records:DocumentApplyRecord[];scopeFingerprint:string;generation:string};outcome?:NonNullable<import('../../../../packages/contracts/storage/local-store.ts').StoreReceipt['documentApply']>}) {
  text(command.projectId); text(command.actorId); text(command.idempotencyKey);
  if (!Array.isArray(command.changes) || command.changes.length === 0 || command.changes.length > (promotion ? 10000 : 100)) fail('INVALID_COMMAND');
  if (command.outbox && (!Array.isArray(command.outbox) || command.outbox.length > 100)) fail('INVALID_COMMAND');
  if (Buffer.byteLength(JSON.stringify(command)) > 16 * 1024 * 1024) fail('COMMAND_TOO_LARGE');
  const payloadHash = hash(teamOperation?{projectId:command.projectId,actorId:command.actorId,epoch:command.expectedAuthorityEpoch,idempotencyKey:command.idempotencyKey,expectedRevision:teamOperation.expectedRevision,previewDigest:teamOperation.previewDigest,proposal:{...teamOperation.proposal,resources:(teamOperation.proposal.resources??[]).map(({path,hash,byteSize}:any)=>({path,hash,byteSize}))}}:promotion ?? command);
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
    for(const change of command.changes){const previous=get(scope.id,change.entity.id);if((previous?.data.category==='document_proposal'||(change.entity.data as any)?.category==='document_proposal')&&!documentOperation?.trusted)fail('DOCUMENT_PROPOSAL_WRITE_AUTHORITY_REQUIRED');}
    if(promotion)assertDocumentIdle(scope.id);
    if(documentOperation?.journal){if(command.requireIdle)assertIdle(scope.id);saveDocumentJournal(scope,documentOperation.journal);}
    if(command.agentTaskCreation){const pin=command.agentTaskCreation,job=get(scope.id,pin.runId)?.data.appAgentRun as any;
      const bugs=command.changes.filter(c=>c.entity.kind==='task'),bug=bugs[0]?.entity.data as M2TaskProfile|undefined;
      if(!job||job.mode!=='execution'||job.state!=='running'||job.workerId!==pin.workerId||job.generation!==pin.generation||job.taskCreationInitiator!==pin.initiatedBy||job.autonomy||!pin.actorId.startsWith('agent:')||(pin.validationTime??Date.now())>=pin.leaseExpiresAt)fail('AGENT_CREATION_FORBIDDEN');
      if(bugs.length!==1||bugs[0].expectedRevision!==0||bug?.type!=='bug'||bug.creator?.kind!=='agent'||bug.creator.actorId!==pin.actorId||bug.initiatedBy!==pin.initiatedBy)fail('AGENT_CREATION_FORBIDDEN');
      if(Number(db.prepare("SELECT COUNT(*) AS n FROM entities WHERE project_id=? AND kind='task' AND json_extract(data,'$.creator.actorId')=?").get(scope.id,pin.actorId)!.n)>=32)fail('AGENT_CREATION_LIMIT');
    }
    if(command.decisionCommand){const pin=command.decisionCommand,row=get(scope.id,pin.id),d=row?.data;
      if(!row||row.kind!=='settings'||d?.category!=='paos_decision'||row.revision!==pin.revision||d.state!=='pending')fail('DECISION_STALE');
      if(d.authorityEpoch!==scope.authorityEpoch||d.rootIdentity!==scope.rootIdentity||pin.rootIdentity!==scope.rootIdentity||d.taskId!==pin.taskId||d.scopeHash!==pin.scopeHash||d.expiresAt!==pin.expiresAt)fail('DECISION_SCOPE_CHANGED');
      if(!Number.isFinite(pin.expiresAt)||(pin.validationTime??Date.now())>=pin.expiresAt)fail('DECISION_EXPIRED');
      if(pin.taskId){const task=get(scope.id,pin.taskId);if(!task||task.kind!=='task'||task.deleted||recipeScopeHash(task.data)!==pin.scopeHash)fail('DECISION_SCOPE_CHANGED');}
    }
    if(teamOperation){
      try{const root=realpathSync(scope.canonicalRoot),identity=lstatSync(root,{bigint:true});if(!identity.isDirectory()||`${identity.dev}:${identity.ino}`!==scope.rootIdentity)fail('PROJECT_ROOT_UNAVAILABLE');}catch{fail('PROJECT_ROOT_UNAVAILABLE');}
      ensureM2BSchema(db);
      const old=get(scope.id,teamId),registry=(old?.data??{category:'team_registry',assets:[]}) as TeamRegistry;
      const runs=db.prepare("SELECT * FROM entities WHERE project_id=? AND kind='run' AND deleted=0 AND status NOT IN ('completed','failed','interrupted')").all(scope.id).map(row=>{const data=JSON.parse(row.data as string);const run=data.appAgentRun??data.runtimeRun;return {id:String(row.id),assetIds:(run?.assetPins??run?.taskContext?.assetPins??[]).map((p:any)=>p.assetId)};});
      const preview=previewAsset(registry,teamOperation.proposal,teamOperation.expectedRevision,runs,[...registry.assets,...teamOperation.sourceAssets??[]]);
      if(preview.previewDigest!==teamOperation.previewDigest)fail('TEAM_PREVIEW_STALE');
      for(const r of preview.proposal.resources??[]){if(r.base64!==undefined)fail('ASSET_RESOURCE_NOT_MANAGED');const blob=db.prepare('SELECT * FROM blobs WHERE project_id=? AND id=?').get(scope.id,r.blobId??'');if(!blob||blob.sha256!==r.hash||blob.byte_size!==r.byteSize)fail('ASSET_RESOURCE_INVALID');}
      const applied=applyAsset(registry,{...preview,proposal:{...preview.proposal,...(preview.proposal.action==='create'?{assetId:`managed-${hash([scope.id,command.idempotencyKey]).slice(0,32)}`}:{})}},command.actorId);
      const blobIds=[...new Set(applied.registry.assets.flatMap(a=>a.versions.flatMap(v=>v.resources.flatMap(r=>r.blobId?[r.blobId]:[]))))];
      command={...command,changes:[{expectedRevision:old?.revision??0,entity:{id:teamId,kind:'settings',data:applied.registry as any,blobIds}}]};
    }
    // Recipe ownership fences only its Task; the global runtime idle gate stays unchanged.
    const settingsRows=db.prepare("SELECT * FROM entities WHERE project_id=? AND kind='settings' AND deleted=0").all(scope.id).map(row=>entity(row));
    const recipeRows=settingsRows.filter(row=>row.data.category==='recipe_execution');
    const workspaceLocks=db.prepare(`SELECT e.id,e.kind,p.canonical_root,json_extract(e.data,'$.appAgentRun.recipeExecution') AS owner_execution
      FROM entities e JOIN projects p ON p.id=e.project_id WHERE e.deleted=0 AND
      ((e.kind='run' AND e.status NOT IN ('completed','failed','interrupted')) OR
       (e.kind='settings' AND json_extract(e.data,'$.category')='recipe_execution' AND json_extract(e.data,'$.state') NOT IN ('completed','failed','cancelled','needs_user_decision','transition_blocked')))`)
      .all() as WorkspaceLock[];
    const recipePin=command.recipeExecution,recipeRow=recipePin?recipeRows.find(row=>row.id===recipePin.id):undefined;
    if(recipePin&&(recipeRow?.revision??0)!==recipePin.revision)fail('RECIPE_REVISION_CONFLICT');
    for(const change of command.changes){
      const previous=get(scope.id,change.entity.id),proposed=change.entity.data as any;
      if(previous?.data.category==='recipe_execution'||proposed?.category==='recipe_execution'){
        if(!recipePin||recipePin.id!==change.entity.id||change.delete||change.entity.kind!=='settings')fail('RECIPE_WRITE_AUTHORITY_REQUIRED');
        const before=previous?.data as unknown as Execution|undefined,after=proposed as Execution;
        if(before&&['id','projectId','taskId','sessionId','bindingId','queueEntryId','scopeHash','taskContext','workflowSnapshot','transition','recipe','pins','inputArtifacts','budgetId','policyHash','startDigest'].some(k=>recipeHash((before as any)[k])!==recipeHash((after as any)[k])))fail('RECIPE_PIN_IMMUTABLE');
        if(!before){const task=get(scope.id,after.taskId),policy=get(scope.id,'autonomy-policy');if(!task||recipeScopeHash(task.data)!==after.scopeHash||recipeRows.some(r=>ownsTask(r.data as unknown as Execution)&&r.data.taskId===after.taskId))fail('RECIPE_TASK_OWNED');
          if(!policy||policy.revision!==after.policyRevision||policy.data.budgetId!==after.budgetId||policy.data.paused||recipeHash(policy.data.policy)!==after.policyHash)fail('RECIPE_PREVIEW_STALE');
        }
      }
      if(change.entity.kind==='task'){
        const owner=recipeRows.find(r=>ownsTask(r.data as unknown as Execution)&&r.data.taskId===change.entity.id);
        if(owner&&recipePin?.id!==owner.id)fail('RECIPE_TASK_OWNED');
        if(owner&&recipeScopeHash(proposed)!==(owner.data as unknown as Execution).scopeHash)fail('RECIPE_TASK_SCOPE_CHANGED');
      }
      if(change.entity.kind==='run'&&!previous){const job=proposed?.appAgentRun??proposed?.runtimeRun,taskId=job?.taskContext?.taskId??job?.taskId,owner=recipeRows.find(r=>ownsTask(r.data as unknown as Execution)&&r.data.taskId===taskId);
        if(owner&&recipePin?.id!==owner.id)fail('RECIPE_TASK_OWNED');
        if(job?.recipeExecution){const execution=owner?.data as unknown as Execution,attempt=execution?.attempts.at(-1);if(!execution||execution.state!=='running'||job.recipeExecution!==execution.id||attempt?.state!=='planned'||attempt.clientMessageId!==job.clientMessageId||job.bindingId!==execution.bindingId||recipeHash(job.assetPins)!==recipeHash(execution.pins[attempt.stepId])||job.autonomy?.budgetId!==execution.budgetId)fail('RECIPE_ADMISSION_INVALID');}
      }
    }
    // Check the pre-command state: the same atomic dispatch may insert its own run before its task row.
    if(command.taskManagerRun){
      const pin=command.taskManagerRun,row=get(scope.id,pin.id),run=(row?.data.runtimeRun??row?.data.appAgentRun) as any;
      const taskId=run?.taskId??run?.taskContext?.taskId;
      if(!row||row.kind!=='run'||!run||!['running','dispatching','awaiting_approval'].includes(row.status)||run.bindingId!==pin.bindingId
        ||run.generation!==pin.generation||taskId!==pin.taskId||!command.actorId.startsWith('agent:')
        ||!command.actorId.endsWith(`:${pin.id}`)||command.changes.some(c=>c.entity.kind==='task'&&(c.entity.id!==pin.taskId||['done','cancelled'].includes(String(c.entity.data?.status)))))fail('TOOL_SCOPE_INVALID');
    }
    if (command.requireIdle || (command.taskManagerAction&&!command.taskManagerRun)) assertIdle(scope.id,'ACTIVE_RUN_RECONCILIATION_REQUIRED',Boolean(documentOperation?.journal));
    validateSchedulerWrite(command,settingsRows,id=>get(scope.id,id),scope.canonicalRoot,workspaceLocks);
    const workflowRows=db.prepare("SELECT * FROM entities WHERE project_id=? AND deleted=0 AND kind IN ('task','settings','run')").all(scope.id).map(row=>entity(row));
    const workflowContext=workflowWriteContext(command,workflowRows);
    if(command.workflowPublish){const available=[...((get(scope.id,teamId)?.data as unknown as TeamRegistry)?.assets??[]),...trustedSourceAssets];
      const published=workflowContext.registry.workflows.find(w=>w.id===command.workflowPublish!.workflowId)?.versions.at(-1);
      for(const recipe of published?.definition.recipes??[])for(const step of recipe.steps)for(const id of step.skills){const a=available.find(a=>a.id===id&&a.kind==='skill'&&!a.archived&&!a.deleted);if(!a)fail('WORKFLOW_SKILL_REFERENCE_INVALID');const version=step.skillVersions[id];if(version&&!(a.management==='paos_managed'?a.versions.some((v:{version:number})=>String(v.version)===version.replace(/^v/,'')):version===a.source?.hash))fail('WORKFLOW_SKILL_VERSION_INVALID');}
    }
    const migrationCohort=new Set(command.workflowMigration?.tasks.map(t=>t.id)??[]);
    if(command.workflowMigration){
      const rows=workflowRows.filter(r=>r.kind==='task'),profiles=rows.map(r=>decodeM1TaskProfile(r.data)),links=canonicalIssueLinks(profiles,(workflowRows.find(r=>r.id==='m2-links')?.data.items??[]) as IssueLink[]);
      const flags=new Map<string,Set<string>>();const mark=(id:string,flag:string)=>{const row=rows.find(r=>r.id===id);if(!row||row.data.schemaVersion!=='m2_task_profile_v1'||workflowCategory(workflowContext.registry,row.data as any)!=='done')return;const set=flags.get(id)??new Set<string>();set.add(flag);flags.set(id,set);};
      for(const change of command.changes.filter(c=>migrationCohort.has(c.entity.id))){const before=rows.find(r=>r.id===change.entity.id);if(!before)continue;const oldCategory=workflowCategory(workflowContext.registry,before.data as any),next=workflowCategory(workflowContext.registry,change.entity.data as any);if(['done','cancelled'].includes(oldCategory)&&!['done','cancelled'].includes(next)){
        for(const link of links.filter(l=>l.relation==='blocks'&&l.sourceId===before.id))mark(link.targetId,'dependency_review');const parent=(before.data as any).parentId;if(parent)mark(parent,'scope_review');
      }}
      const changes=[...command.changes];for(const [id,set]of flags){const index=changes.findIndex(c=>c.entity.id===id),old=rows.find(r=>r.id===id)!;const base=index>=0?changes[index]:{expectedRevision:old.revision,entity:{id,kind:'task' as const,data:old.data}};const revised={...base,entity:{...base.entity,data:{...base.entity.data,risks:[...new Set([...(base.entity.data as any).risks,...set])]}}};if(index>=0)changes[index]=revised;else changes.push(revised);}
      if(changes.length>100)fail('WORKFLOW_MIGRATION_TOO_LARGE');command={...command,changes};
    }
    if(command.changes.some(c=>c.entity.data?.schemaVersion==='m2_task_profile_v1'||c.entity.id.startsWith('m2-')
      ||['m2_comment','managed_attachment'].includes(String((c.entity.data as any)?.category))))ensureM2Schema(db);
    if(command.changes.some(c=>c.entity.id==='m2-workflows'))ensureM2BSchema(db);
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
    const workflowGuards=new Map<string,ReadonlySet<string>>();
    const managerChanges:Array<Record<string,unknown>>=[];
    // Only the atomic count below may assert an actual override; supplied receipt metadata is not evidence.
    for(const change of command.changes){const data=change.entity.data as Record<string,unknown>|undefined;if(data?.category==='m2_command_receipt')delete data.wipOverride;}
    const now = new Date().toISOString();
    const seen = new Set<string>();
    const searchCounts = readSearchCounts(scope.id);
    for (const change of command.changes) {
      let input = change.entity;
      if(['message','session'].includes(input.kind)){
        if(input.kind==='message'&&isHiddenMessage(input))fail('HIDDEN_MESSAGE_FORBIDDEN');
        const title=safePersistedText(input.title??''),body=safePersistedText(input.body??''),data=safeVisibleValue(input.data??{});
        const changed=title!==(input.title??'')||body!==(input.body??'')||JSON.stringify(data)!==JSON.stringify(input.data??{});
        input={...input,title,body,data};
        if(changed)input={...input,data:{...input.data,redacted:true}};
      }else if(input.kind==='run')input={...input,data:safeRuntimeData(input.data??{})};
      text(input.id);
      if (seen.has(input.id)) fail('DUPLICATE_ENTITY');
      seen.add(input.id);
      const old = db.prepare('SELECT revision,kind,public_key,title,body,status,data,coverage,deleted FROM entities WHERE project_id=? AND id=?').get(scope.id, input.id);
      if(!teamOperation&&(input.id.startsWith('m2b-team-')||String((input.data as any)?.category).startsWith('team_')||old&&String(JSON.parse(old.data as string).category).startsWith('team_')))fail('TEAM_MANAGED_WRITE_FORBIDDEN');
      if(input.kind==='run'){
        const nextRun=(input.data as any)?.appAgentRun??(input.data as any)?.runtimeRun,oldData=old?JSON.parse(old.data as string):null,oldRun=oldData?.appAgentRun??oldData?.runtimeRun;
        if(oldRun?.assetPins&&JSON.stringify(oldRun.assetPins)!==JSON.stringify(nextRun?.assetPins))fail('ASSET_RUN_PIN_IMMUTABLE');
        // A recipe continuation already proved byte equality to its immutable durable pins above.
        if(!oldRun){const registry=get(scope.id,teamId)?.data as unknown as TeamRegistry|undefined;for(const pin of nextRun?.assetPins??[]){if(!pin.assetId?.startsWith('managed-'))continue;const asset=registry?.assets.find(a=>a.id===pin.assetId),version=asset?.versions.find(v=>v.version===pin.version);if(!asset||asset.archived||asset.deleted||!version||!nextRun.recipeExecution&&version.version!==asset.effectiveVersion||version.hash!==pin.hash||version.content!==pin.content||JSON.stringify(version.resources)!==JSON.stringify((pin.resources??[]).map(({base64,...metadata}:any)=>metadata)))fail('ASSET_RUN_PIN_INVALID');}}
      }
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
        const taskCommand=command.workflowMigration&&!migrationCohort.has(task.id)?{...command,workflowMigration:undefined}:command;
        const {category,prior,migrating,guards}=validateWorkflowTask(taskCommand,task,before,workflowContext.registry);
        if(guards.length)workflowGuards.set(task.id,new Set(guards));
        if(migrating)issueGuardIds.add(task.id);
        if(!before||before.status!==task.status)issueGuardIds.add(task.id);
        if(task.parentId&&(!before||(before as M2TaskProfile).parentId!==task.parentId))issueGuardIds.add(task.parentId);
        if (before && JSON.stringify(before.creator)!==JSON.stringify(task.creator)) fail('CREATOR_IMMUTABLE');
        if (before?.schemaVersion==='m2_task_profile_v1' && (before.createdAt!==task.createdAt || before.initiatedBy!==task.initiatedBy)) fail('CREATOR_IMMUTABLE');
        if(before?.schemaVersion==='m2_task_profile_v1'){
          const old=before as M2TaskProfile;
          if(old.dueDate!==task.dueDate&&!command.taskManagerReason?.trim()&&!command.taskManagerReviewReason?.trim())fail('DUE_DATE_REASON_REQUIRED');
          if(prior==='done'&&category==='done'&&['summary','technicalValue','productValue','files','artifactReferences','acceptanceCriteria','criteriaEvidence','scopeExclusions','parentId','type','artifacts','fileContexts','estimateSeconds','blocker']
            .some(field=>JSON.stringify((old as any)[field])!==JSON.stringify((task as any)[field])))fail('REOPEN_REQUIRED');
          if(old.status===task.status&&old.resolution!==task.resolution&&!command.taskManagerAction)fail('TRANSITION_REQUIRED');
          if(old.status===task.status&&['dependency_review','scope_review','recovery_review','acceptance_unverified'].some(flag=>old.risks.includes(flag)&&!task.risks.includes(flag))){
            if(!command.taskManagerReviewReason?.trim()||command.actorId.startsWith('agent:'))fail('SYSTEM_REVIEW_REQUIRED');
            issueGuardIds.add(task.id);
          }
        }
        if(task.hotfixReason!==((before as M2TaskProfile|null)?.hotfixReason??null)&&command.taskManagerAction!=='transition')fail('HOTFIX_APPROVAL_REQUIRED');
        if (!before && (category!=='backlog' || task.resolution!==null)) fail('INITIAL_STATUS_REQUIRED');
        if (before && before.status!==task.status) {
          if (!command.taskManagerAction&&!migrating) fail('TRANSITION_REQUIRED');
        }
        if(before?.schemaVersion==='m2_task_profile_v1'&&task.blocker&&JSON.stringify(before.blocker)!==JSON.stringify(task.blocker))assertIdle(scope.id);
        if ((category==='ready' || category==='in_progress')&&!(before?.schemaVersion==='m1_task_profile_v1'&&before.status===task.status&&task.risks.includes('recovery_review'))) validateReady(task);
        const board=get(scope.id,'m2-board')?.data.value as any;
        if(['ready','in_progress'].includes(category)&&(board?.releaseRequiredTypes?.includes(task.type)||board?.releaseRequiredComponents?.some((id:string)=>task.components.includes(id)))
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
        if ((category==='done' && task.resolution!=='completed') || (category==='cancelled' && !['cancelled','duplicate','wont_do'].includes(task.resolution??''))
          || (!['done','cancelled'].includes(category)&&task.resolution!==null)) fail('RESOLUTION_REQUIRED');
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
      const semanticTasks=tasks.map(task=>task.schemaVersion==='m2_task_profile_v1'?{...task,status:workflowCategory(workflowContext.registry,task)}:task);
      validateWorkflowBoard(workflowContext.registry,tasks,get(scope.id,'m2-board')?.data.value);
      validateIssueGraph(semanticTasks,links,issueGuardIds,workflowGuards);
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
    const receipt = { commandId, projectId: scope.id, seq, revisions,...(promotion?.cutoverBackupId?{cutoverBackupId:promotion.cutoverBackupId}:{}),...(documentOperation?.outcome?{documentApply:documentOperation.outcome}:{}) };
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
    case 'teamApply': return (async()=>{
      const command={projectId:params.projectId,actorId:params.actorId,idempotencyKey:params.idempotencyKey,expectedAuthorityEpoch:params.epoch,changes:[{expectedRevision:0,entity:{id:teamId,kind:'settings' as const,data:{request:params}}}]};
      const result=(receipt:any)=>({assetId:params.proposal.action==='create'?`managed-${hash([params.projectId,params.idempotencyKey]).slice(0,32)}`:params.proposal.assetId,version:params.expectedRevision+1,receipt});
      if(db.prepare('SELECT 1 FROM commands WHERE project_id=? AND idempotency_key=?').get(params.projectId,params.idempotencyKey))return result(write(command,undefined,params));
      const scope=project(params.projectId);if(!scope)fail('PROJECT_NOT_FOUND');
      const sourceRoots=[...projectAssetRoots(scope.canonicalRoot),...workerData.assetRoots??[]] as AssetRoot[];
      const sourceAssets=(await sourceCatalog(sourceRoots)).assets;
      if(params.proposal.source&&params.proposal.action==='create'){const source=params.proposal.source;
       if(source.rootId===teamId){const original=(get(params.projectId,teamId)?.data as unknown as TeamRegistry)?.assets.find(a=>a.id===source.relativePath);if(!original||original.versions.at(-1)?.hash!==source.hash)fail('ASSET_SOURCE_DRIFT');}
       else if(source.rootId==='openai-plugins-superpowers'){
        // Only TeamService supplies this port field after its cached immutable-source check; HTTP payloads never forward it.
        const proof=params.remoteSourceProof,revision='d420d13051bffe4543ed39e30fa46b87148e47dd',resources=params.proposal.resources??[];
        const digest=(value:string)=>createHash('sha256').update(value).digest('hex');
        const bundle=digest(JSON.stringify([revision,digest(params.proposal.content),resources.map((r:any)=>[r.path,r.hash]).sort(([a]:any,[b]:any)=>a.localeCompare(b))]));
        if(!proof||proof.revision!==revision||proof.sourceHash!==source.hash||source.revision!==revision||source.hash!==bundle||source.origin!=='github_public_readonly'||source.license!=='MIT'||!/^plugins\/superpowers\/skills\/[A-Za-z0-9_-]{1,128}$/.test(source.relativePath)||!resources.some((r:any)=>r.path==='LICENSE.source.txt'&&r.hash===source.licenseHash))fail('REMOTE_SOURCE_DRIFT');
       }
       else{const root=sourceRoots.find(r=>r.id===source.rootId);if(!root)fail('ASSET_SOURCE_ROOT_INVALID');const actual=await sourceAsset(root,source.relativePath,true);if(JSON.stringify(actual.source)!==JSON.stringify(source)||JSON.stringify(actual.resources.map(({path,hash,byteSize})=>({path,hash,byteSize})))!==JSON.stringify((params.proposal.resources??[]).map(({path,hash,byteSize}:any)=>({path,hash,byteSize}))))fail('ASSET_SOURCE_DRIFT');}}
      for(const r of params.proposal.resources??[]){const blob=db.prepare('SELECT * FROM blobs WHERE project_id=? AND id=?').get(params.projectId,r.blobId??'');if(!blob)fail('ASSET_RESOURCE_INVALID');const bytes=await readManagedBlob(workerData.databasePath,{id:String(blob.id),projectId:params.projectId,sha256:String(blob.sha256),byteSize:Number(blob.byte_size)});if(params.proposal.source?.rootId==='openai-plugins-superpowers'&&(r.hash!==String(blob.sha256)||r.byteSize!==Number(blob.byte_size)))fail('REMOTE_SOURCE_DRIFT');if(safePersistedText(Buffer.from(bytes).toString('utf8'))!==Buffer.from(bytes).toString('utf8'))fail('SENSITIVE_ASSET_CONTENT');}
      return result(write(command,undefined,{...params,sourceAssets}));
    })();
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
    case 'registerSelectedProject': return transaction(()=>{
      const selected=params.project;
      for(const value of [selected.id,selected.canonicalRoot,selected.rootIdentity,selected.displayName])text(value);
      if(!/^[A-Z]{4}$/.test(selected.keyPrefix)||!['legacy_files','sql'].includes(selected.authorityMode)||!/^[-a-f0-9]{64}$/.test(params.requestDigest)
        ||params.requestId!==undefined&&(typeof params.requestId!=='string'||!/^[-A-Za-z0-9_]{1,100}$/.test(params.requestId)))fail('INVALID_PROJECT');
      const root=process.platform==='win32'?selected.canonicalRoot.toLowerCase():selected.canonicalRoot;
      const receiptKey=params.requestId?`project_registration_v1:${params.requestId}`:null;
      if(receiptKey){const receipt=db.prepare('SELECT value FROM store_meta WHERE key=?').get(receiptKey);if(receipt){let previous:any;try{previous=JSON.parse(String(receipt.value));}catch{fail('PROJECT_REGISTRATION_UNAVAILABLE');}if(previous.digest!==params.requestDigest)fail('REQUEST_CONFLICT');const saved=project(previous.projectId);if(!saved||saved.rootIdentity!==selected.rootIdentity||saved.canonicalRoot!==root)fail('PROJECT_IDENTITY_CONFLICT');return saved;}}
      const old=db.prepare('SELECT id FROM projects WHERE canonical_root=? OR root_identity=?').get(root,selected.rootIdentity);
      let saved:Project|null;
      if(old){saved=project(String(old.id));if(!saved||saved.canonicalRoot!==root||saved.rootIdentity!==selected.rootIdentity||saved.displayName!==selected.displayName||saved.authorityMode!==selected.authorityMode||params.keyPrefixExplicit&&saved.keyPrefix!==selected.keyPrefix)fail('PROJECT_IDENTITY_CONFLICT');}
      else{
        if(db.prepare('SELECT 1 FROM projects WHERE id=? OR key_prefix=?').get(selected.id,selected.keyPrefix))fail('PROJECT_IDENTITY_CONFLICT');
        db.prepare('INSERT INTO projects(id,key_prefix,display_name,canonical_root,root_identity,authority_mode,authority_epoch) VALUES (?,?,?,?,?,?,1)').run(selected.id,selected.keyPrefix,selected.displayName,root,selected.rootIdentity,selected.authorityMode);
        initializeSearchCounts(selected.id);saved=project(selected.id);
      }
      // Bounded durable Add receipts survive service restart without task/search entities.
      if(receiptKey){const oldest=db.prepare("SELECT key FROM store_meta WHERE key LIKE 'project_registration_v1:%' ORDER BY rowid").all();if(oldest.length>=1024)db.prepare('DELETE FROM store_meta WHERE key=?').run(oldest[0].key);db.prepare('INSERT INTO store_meta VALUES (?,?)').run(receiptKey,JSON.stringify({schemaVersion:'paos_project_registration_v1',digest:params.requestDigest,projectId:saved!.id}));}
      return saved;
    });
    case 'projects': return db.prepare('SELECT id FROM projects ORDER BY id').all().map(row => project(row.id as string));
    case 'documentJournal': {if(!project(params.projectId))fail('PROJECT_NOT_FOUND');return documentJournal(params.projectId);}
    case 'stageDocumentProposal': {
      if(!params.command?.changes?.every((change:any)=>change.expectedRevision===0&&change.entity.kind==='document'&&change.entity.data?.category==='document_proposal'))fail('DOCUMENT_PROPOSAL_INVALID');
      return write(params.command,undefined,undefined,[],{trusted:true});
    }
    case 'documentWrite': return write(params.command,undefined,undefined,[],{trusted:true,journal:params,outcome:params.outcome});
    case 'readProjectState': {
      if(!project(params.projectId))fail('PROJECT_NOT_FOUND');
      if(!['project_scan_v1','project_inventory_policy_v1','project_database_schema_v1','project_code_database_v1'].includes(params.namespace))fail('PROJECT_STATE_INVALID');
      const row=db.prepare('SELECT value FROM store_meta WHERE key=?').get(`${params.namespace}:${params.projectId}`);
      if(!row)return null;
      let saved:any;try{saved=JSON.parse(String(row.value));}catch{fail('PROJECT_STATE_UNAVAILABLE');}
      if(!Number.isSafeInteger(saved.version)||saved.version<1||!saved.value||typeof saved.value!=='object'||Array.isArray(saved.value))fail('PROJECT_STATE_UNAVAILABLE');
      return saved;
    }
    case 'writeProjectState': return transaction(()=>{
      if(!project(params.projectId))fail('PROJECT_NOT_FOUND');
      if(!['project_scan_v1','project_inventory_policy_v1','project_database_schema_v1','project_code_database_v1'].includes(params.namespace)||!Number.isSafeInteger(params.expectedVersion)||params.expectedVersion<0||!params.value||typeof params.value!=='object'||Array.isArray(params.value))fail('PROJECT_STATE_INVALID');
      if(params.namespace==='project_inventory_policy_v1'){
        assertDocumentIdle(params.projectId);
        const policy=params.value.policy;
        if(params.value.schemaVersion!=='paos_inventory_policy_v1'||!policy||typeof policy!=='object'||Array.isArray(policy)
          ||Object.keys(policy).some(key=>!['version','include','exclude','respectGitignore'].includes(key))
          ||policy.version!==undefined&&(typeof policy.version!=='string'||policy.version.length>64)
          ||policy.respectGitignore!==undefined&&typeof policy.respectGitignore!=='boolean'
          ||[policy.include,policy.exclude].some(patterns=>patterns!==undefined&&(!Array.isArray(patterns)||patterns.length>200||patterns.some((pattern:unknown)=>typeof pattern!=='string'||pattern.length>1024||/[\\\x00-\x1f:]/.test(pattern)||pattern.includes('..')||pattern.startsWith('/')))))fail('PROJECT_STATE_INVALID');
      }
      const key=`${params.namespace}:${params.projectId}`,old=db.prepare('SELECT value FROM store_meta WHERE key=?').get(key);
      let version=0;if(old){try{version=JSON.parse(String(old.value)).version;}catch{fail('PROJECT_STATE_UNAVAILABLE');}}
      if(version!==params.expectedVersion)fail('PROJECT_STATE_CONFLICT');
      const saved={version:version+1,value:params.value},encoded=JSON.stringify(saved);
      if(Buffer.byteLength(encoded)>(params.namespace==='project_database_schema_v1'?2*1024*1024:['project_scan_v1','project_code_database_v1'].includes(params.namespace)?1024*1024:32768))fail('PROJECT_STATE_LIMIT');
      db.prepare('INSERT INTO store_meta VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value').run(key,encoded);
      return saved;
    });
    case 'project': return project(params.projectId);
    case 'compatibility': return databaseCompatibility(db);
    case 'historyRows': {
      const rows=db.prepare("SELECT rowid AS journal_order,* FROM entities WHERE project_id=? AND deleted=0 AND kind IN ('session','message','task','run') ORDER BY rowid LIMIT 100001").all(params.projectId);
      if(rows.length>100000||rows.reduce((n,r)=>n+Buffer.byteLength(r.data as string)+Buffer.byteLength(r.body as string),0)>64*1024*1024)fail('HISTORY_TOO_LARGE');
      return rows.map(row=>({...entity(row),journalOrder:row.journal_order}));
    }
    case 'historySnapshotPage': return historySnapshotPage(db,entity,params);
    case 'artifactSummaryRows': return artifactSummaryRows(db,entity,params.projectId,params);
    case 'artifactDocumentRow': return artifactDocumentRow(db,entity,params.projectId,params.id);
    case 'projectEntities': {
      return projectRows(params.projectId,params);
    }
    case 'projectFreshness': return projectFreshness(params.projectId);
    case 'runtimeFileScope': {
      db.exec('BEGIN');
      try{const scope={project:project(params.projectId),task:get(params.projectId,params.taskId)};db.exec('COMMIT');return scope;}
      catch(error){db.exec('ROLLBACK');throw error;}
    }
    case 'projectSnapshot': {
      db.exec('BEGIN');
      try{const freshness=projectFreshness(params.projectId),entities=projectRows(params.projectId,params);db.exec('COMMIT');return {entities,freshness};}
      catch(error){db.exec('ROLLBACK');throw error;}
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
    case 'write': {
      if(!params.workflowPublish)return write(params);
      return (async()=>{const scope=project(params.projectId);if(!scope)fail('PROJECT_NOT_FOUND');const roots=[...projectAssetRoots(scope.canonicalRoot),...workerData.assetRoots??[]] as AssetRoot[];return write(params,undefined,undefined,(await sourceCatalog(roots)).assets);})();
    }
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
