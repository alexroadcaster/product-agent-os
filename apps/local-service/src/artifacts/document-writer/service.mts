import {createHash} from 'node:crypto';
import {extname,dirname,resolve,basename} from 'node:path';
import {tmpdir} from 'node:os';
import {lstat,rm} from 'node:fs/promises';
import type {LocalStore,StoredEntity} from '../../storage/local-store.mts';
import type {DocumentTargetSource,DocumentApplyRecord,DocumentApplyOutcome,DocumentApplyInput,DocumentApplyPreview} from '../../../../../packages/contracts/artifacts/document-apply.ts';
import {readCheckedSource,assertSourceProject,inventoryForProject} from '../../code-index/sources.mts';
import {inventoryScopeFingerprint,assertCurrentSourceProject} from '../../project-inventory/scope.mts';
import {safePersistedText} from '../../redaction/persisted.mts';
import {normaliseRelativePath} from '../../project-inventory/service.mts';
import {openDocumentHandle} from './native.mts';

const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
const hash=(value:Buffer|string)=>createHash('sha256').update(value).digest('hex');
const fingerprint=(value:unknown)=>hash(JSON.stringify(value));
const decode=(value:Buffer)=>new TextDecoder('utf-8',{fatal:true}).decode(value);
const limit=512*1024;
export type DocumentWriterOptions={/** Private I/O timing/fault seams; never supplied by or returned to HTTP. */ beforeAcquire?:()=>Promise<void>;afterPrepare?:(owner:{processId:number;temporaryDirectory:string;directoryIdentity:string})=>Promise<void>};
/** Exact-file preview authority. Private before/after bytes live only in the bounded journal.
 * Saved policy revocation is fenced in SQLite; external ignore files are final-checked, not atomically locked. */
export function createDocumentWriter(store:LocalStore,options:DocumentWriterOptions={}){
 let queue:Promise<unknown>=Promise.resolve();
 const serial=<T,>(fn:()=>Promise<T>)=>{const result=queue.then(fn);queue=result.catch(()=>{});return result;};
 async function project(id:string){const p=await store.project(id);if(!p)fail('PROJECT_NOT_FOUND');await assertSourceProject(p!);return p!;}
 async function cleanupOwner(record:DocumentApplyRecord){
  const owner=record.nativeOwner;if(!owner)return;
  // A process crash may leave compiler scratch until the helper DLL is unloaded.
  // Explicit recovery removes only the captured dead owner's same-identity temp directory.
  try{process.kill(owner.processId,0);return;}catch(error){if((error as any).code!=='ESRCH')return;}
  const path=resolve(owner.temporaryDirectory);if(dirname(path)!==resolve(tmpdir())||!basename(path).startsWith('paos-document-write-'))return;
  try{const info=await lstat(path,{bigint:true});if(!info.isDirectory()||info.isSymbolicLink()||`${info.dev}:${info.ino}`!==owner.directoryIdentity)return;await rm(path,{recursive:true,force:true});}catch(error){if((error as any).code!=='ENOENT')throw error;}
 }
 async function proposal(projectId:string,id:unknown){if(typeof id!=='string'||id.length>200)fail('DOCUMENT_APPLY_INVALID');const row=await store.get(projectId,id as string);if(!row||row.kind!=='document'||row.data.category!=='document_proposal')fail('DOCUMENT_PROPOSAL_NOT_FOUND');return row!;}
 function eligible(path:string){normaliseRelativePath(path);if(!['.md','.txt'].includes(extname(path).toLowerCase())||path.split('/').some(part=>/^(?:AGENTS(?:\.override)?\.md|CLAUDE\.md|GEMINI\.md|copilot-instructions\.md|SKILL\.md|\.codex|\.agents|\.cursor|\.clinerules|\.windsurf|config|hooks|rules|plugins|skills)$/i.test(part)||/\.instructions\.md$/i.test(part)))fail('DOCUMENT_WRITE_FORBIDDEN');}
 function safe(bytes:Buffer){if(bytes.length>limit)fail('DOCUMENT_TOO_LARGE');let value:string;try{value=decode(bytes);}catch{fail('DOCUMENT_ENCODING_UNSUPPORTED');}if(safePersistedText(value!)!==value!)fail('DOCUMENT_SENSITIVE_CONTENT');return value!;}
 async function target(projectId:string,row:StoredEntity,action:'apply'|'rollback'){
  const p=await project(projectId),generation=(await store.projectFreshness(projectId)).generation,source=row.data.targetSource as DocumentTargetSource|undefined;
  if(!source||!['workspace_file','local_store'].includes(source.origin))fail('DOCUMENT_SOURCE_PIN_REQUIRED');
  let before:Buffer,after:Buffer,targetRow:StoredEntity|null=null;
  const journal=await store.documentJournal(projectId);
  if(action==='rollback'){
   const previous=journal.records.find(record=>record.operationId===(row.data.documentApply as DocumentApplyOutcome|undefined)?.operationId&&record.action==='apply');
   if(!previous)fail('DOCUMENT_ROLLBACK_EXPIRED');after=Buffer.from(previous!.beforeBase64,'base64');
  }else after=Buffer.from(row.body,'utf8');
  if(source!.origin==='workspace_file'){
   eligible(source!.path);if(source!.rootIdentity!==p.rootIdentity)fail('DOCUMENT_SCOPE_STALE');
   const file=await readCheckedSource(p,source!.path,limit);
   if(file.redacted||safePersistedText(file.text)!==file.text)fail('DOCUMENT_SENSITIVE_CONTENT');
   if(action==='apply'&&(file.hash!==source!.rawHash||file.fileRevision!==source!.fileRevision||file.policyVersion!==source!.policyVersion))fail('DOCUMENT_SOURCE_CONFLICT');
   // F28 strips only the UTF-8 BOM. Normalize exact preserved bytes before preview hashing or caps.
   before=Buffer.from(file.text,'utf8');const bom=file.byteSize-before.length===3;
   if(bom)before=Buffer.concat([Buffer.from([239,187,191]),before]);
   if(action==='apply'&&bom&&!after.subarray(0,3).equals(Buffer.from([239,187,191])))after=Buffer.concat([Buffer.from([239,187,191]),after]);
   safe(before);safe(after);
   const currentSource:DocumentTargetSource=action==='rollback'?{...source!,rawHash:file.hash,fileRevision:file.fileRevision,policyVersion:file.policyVersion}:source!;
   return {p,generation,source:currentSource,scope:inventoryScopeFingerprint(p),before,after,rawBeforeHash:file.hash,fileRevision:file.fileRevision,targetRow,journal};
  }
  targetRow=await store.get(projectId,source!.entityId);if(!targetRow||targetRow.kind!=='document'||targetRow.data.category==='document_proposal')fail('DOCUMENT_TARGET_UNAVAILABLE');
  if(action==='apply'&&targetRow!.revision!==source!.entityRevision)fail('DOCUMENT_SOURCE_CONFLICT');
  before=Buffer.from(targetRow!.body,'utf8');safe(before);safe(after!);
  return {p,generation,source:action==='rollback'?{...source!,entityRevision:targetRow!.revision}:source!,scope:inventoryScopeFingerprint(p),before,after:after!,rawBeforeHash:hash(before),fileRevision:null,targetRow,journal};
 }
 function receipt(row:StoredEntity,action:'apply'|'rollback',key:string,digest:string){const r=row.data[action==='apply'?'documentApplyReceipt':'documentRollbackReceipt'] as any;if(r?.key===key){if(r.digest!==digest)fail('IDEMPOTENCY_CONFLICT');return r.result as DocumentApplyOutcome;}return null;}
 function checkInput(input:any){if(!input||typeof input!=='object'||Object.keys(input).some(key=>!['proposalId','proposalRevision','previewDigest','epoch','idempotencyKey'].includes(key))||typeof input.idempotencyKey!=='string'||!input.idempotencyKey||input.idempotencyKey.length>200||!Number.isSafeInteger(input.epoch)||!Number.isSafeInteger(input.proposalRevision)||typeof input.previewDigest!=='string')fail('DOCUMENT_APPLY_INVALID');}
 async function preview(projectId:string,input:{proposalId:string;proposalRevision:number},action:'apply'|'rollback'):Promise<DocumentApplyPreview>{
  if(!input||Object.keys(input).some(key=>!['proposalId','proposalRevision'].includes(key)))fail('DOCUMENT_APPLY_INVALID');const row=await proposal(projectId,input.proposalId);
  if(row.revision!==input.proposalRevision)fail('DOCUMENT_PROPOSAL_STALE');
  const state=row.data.applyState??'staged';if(action==='apply'&&!['staged','not_applied'].includes(String(state))||action==='rollback'&&!['applied','recovery_required'].includes(String(state)))fail('DOCUMENT_APPLY_STATE_CONFLICT');
  const selected=await target(projectId,row,action);safe(selected.before);safe(selected.after);
  const previewDigest=fingerprint(['document_apply_v1',projectId,selected.generation,selected.scope,row.id,row.revision,action,selected.source,selected.fileRevision,selected.rawBeforeHash,hash(selected.after)]);
  return {proposalId:row.id,proposalRevision:row.revision,action,previewDigest,source:selected.source!,before:decode(selected.before),after:decode(selected.after),beforeHash:selected.rawBeforeHash,afterHash:hash(selected.after),executable:true,accepted:false};
 }
 function recordsWith(records:DocumentApplyRecord[],record:DocumentApplyRecord){const exists=records.some(r=>r.operationId===record.operationId);let next=records.filter(r=>r.operationId!==record.operationId);if(!exists&&next.some(r=>['prepared','recovery_required'].includes(r.state)))fail('DOCUMENT_WRITE_RECONCILIATION_REQUIRED');while(next.length>=4){const at=next.findIndex(r=>!['prepared','recovery_required'].includes(r.state));if(at<0)fail('DOCUMENT_JOURNAL_LIMIT');next.splice(at,1);}return [...next,record];}
 function change(row:StoredEntity,record:DocumentApplyRecord){const state=record.action==='rollback'&&record.state==='not_applied'?'applied':record.state;return {expectedRevision:row.revision,entity:{id:row.id,kind:'document' as const,title:row.title,body:row.body,status:state,data:{...row.data,applyState:state,documentOperation:record.result,[record.action==='apply'?'documentApply':'documentRollback']:record.result,[record.action==='apply'?'documentApplyReceipt':'documentRollbackReceipt']:{key:record.idempotencyKey,digest:record.requestDigest,result:record.result}}}};}
 async function persist(projectId:string,actorId:string,row:StoredEntity,record:DocumentApplyRecord,selected:Awaited<ReturnType<typeof target>>,additional:any[]=[],requireIdle=false,reconcile=false){const journal=await store.documentJournal(projectId);return store.documentWrite({command:{projectId,actorId,expectedAuthorityEpoch:record.authorityEpoch,idempotencyKey:reconcile?`document-reconcile:${record.operationId}:${record.state}:${row.revision}`:record.state==='prepared'?`document:${record.operationId}:prepared:${row.revision}`:`document-outcome:${record.operationId}`,changes:[change(row,record),...additional],...(requireIdle?{requireIdle:true as const}:{})},expectedJournalVersion:journal.version,records:recordsWith(journal.records,record),scopeFingerprint:selected.scope,generation:selected.generation,...(!reconcile&&record.state!=='prepared'?{outcome:{requestDigest:record.requestDigest,result:record.result}}:{})});}
 async function execute(projectId:string,actorId:string,input:DocumentApplyInput,action:'apply'|'rollback'){return serial(async()=>{
  checkInput(input);let row=await proposal(projectId,input.proposalId);const requestDigest=fingerprint([action,input.proposalId,input.proposalRevision,input.previewDigest,input.epoch]);const operationId='doc-write-'+fingerprint([projectId,action,input.idempotencyKey]),durable=await store.receipt(projectId,`document-outcome:${operationId}`);if(durable?.documentApply){if(durable.documentApply.requestDigest!==requestDigest)fail('IDEMPOTENCY_CONFLICT');return durable.documentApply.result;}const replay=receipt(row,action,input.idempotencyKey,requestDigest);if(replay)return replay;
  const plan=await preview(projectId,{proposalId:input.proposalId,proposalRevision:input.proposalRevision},action);if(plan.previewDigest!==input.previewDigest)fail('DOCUMENT_PREVIEW_STALE');const selected=await target(projectId,row,action);if(input.epoch!==selected.p.authorityEpoch)fail('AUTHORITY_CONFLICT');
  if(fingerprint(['document_apply_v1',projectId,selected.generation,selected.scope,row.id,row.revision,action,selected.source,selected.fileRevision,selected.rawBeforeHash,hash(selected.after)])!==input.previewDigest)fail('DOCUMENT_PREVIEW_STALE');
  let before=selected.before,after=selected.after,handle:Awaited<ReturnType<typeof openDocumentHandle>>|undefined;
  if(selected.source!.origin==='workspace_file'){
   await options.beforeAcquire?.();
   handle=await openDocumentHandle({root:selected.p.canonicalRoot,path:selected.source!.path,expectedHash:selected.rawBeforeHash});before=handle.before;
   try{safe(before);}catch(error){await handle.close();throw error;}
  }
  const state=handle?'prepared':action==='apply'?'applied':'rolled_back';
  const result:DocumentApplyOutcome={operationId,proposalId:row.id,action,state,beforeHash:hash(before),afterHash:hash(after),accepted:false,origin:selected.source!.origin};
  const record:DocumentApplyRecord={operationId,proposalId:row.id,proposalRevision:row.revision,action,idempotencyKey:input.idempotencyKey,requestDigest,state,source:selected.source!,scopeFingerprint:selected.scope,generation:selected.generation,authorityEpoch:input.epoch,beforeHash:result.beforeHash,afterHash:result.afterHash,beforeBase64:before.toString('base64'),afterBase64:after.toString('base64'),createdAt:new Date().toISOString(),result,...(handle?{nativeOwner:{processId:handle.processId,temporaryDirectory:handle.temporaryDirectory,directoryIdentity:handle.directoryIdentity}}:{})};
  let prepared=false;
  try{
   await assertCurrentSourceProject(store,selected.p);
   if(handle){const entry=await inventoryForProject(selected.p).inspect(selected.p,selected.source!.origin==='workspace_file'?selected.source!.path:'');if(!entry.access.readable)fail('DOCUMENT_WRITE_FORBIDDEN');if(entry.revision!==selected.fileRevision)fail('DOCUMENT_SOURCE_CONFLICT');}
   const additional=selected.targetRow?[{expectedRevision:selected.targetRow.revision,entity:{id:selected.targetRow.id,kind:'document',title:selected.targetRow.title,body:decode(after),data:selected.targetRow.data,status:selected.targetRow.status}}]:[];
   await persist(projectId,actorId,row,record,selected,additional,true);prepared=true;
   if(!handle)return result;
   await options.afterPrepare?.({processId:handle.processId,temporaryDirectory:handle.temporaryDirectory,directoryIdentity:handle.directoryIdentity});
   await assertCurrentSourceProject(store,selected.p);
   const entry=await inventoryForProject(selected.p).inspect(selected.p,selected.source!.origin==='workspace_file'?selected.source!.path:'');if(!entry.access.readable)fail('DOCUMENT_WRITE_FORBIDDEN');if(entry.revision!==selected.fileRevision)fail('DOCUMENT_SOURCE_CONFLICT');
   await handle.commit(after,record.beforeHash);await handle.close();handle=undefined;
   row=await proposal(projectId,row.id);record.state=action==='apply'?'applied':'rolled_back';record.result={...result,state:record.state};await persist(projectId,actorId,row,record,selected);return record.result;
  }catch(error){
   if(prepared){record.state='recovery_required';record.result={...result,state:'recovery_required',reason:'DOCUMENT_WRITE_OUTCOME_UNCERTAIN'};try{row=await proposal(projectId,row.id);await persist(projectId,actorId,row,record,selected);}catch{}return record.result;}
   throw error;
  }finally{await handle?.close();}
 });}
 async function recover(projectId:string,actorId:string,input:{proposalId:string;operationId:string;epoch:number}){return serial(async()=>{
  if(!input||Object.keys(input).some(key=>!['proposalId','operationId','epoch'].includes(key)))fail('DOCUMENT_APPLY_INVALID');const row=await proposal(projectId,input.proposalId),journal=await store.documentJournal(projectId),record=journal.records.find(r=>r.operationId===input.operationId&&r.proposalId===row.id);if(!record)fail('DOCUMENT_RECOVERY_UNAVAILABLE');const p=await project(projectId);if(input.epoch!==p.authorityEpoch)fail('AUTHORITY_CONFLICT');await cleanupOwner(record!);if(!['prepared','recovery_required'].includes(record!.state))return record!.result;
  const generation=(await store.projectFreshness(projectId)).generation;
  const source=record!.source;if(source.origin!=='workspace_file')return fail('DOCUMENT_RECOVERY_UNAVAILABLE');eligible(source.path);if(source.rootIdentity!==p.rootIdentity)fail('DOCUMENT_SCOPE_STALE');
  const file=await readCheckedSource(p,source.path,limit),state=file.hash===record!.afterHash?(record!.action==='apply'?'applied':'rolled_back'):file.hash===record!.beforeHash?'not_applied':'recovery_required';
  const result={...record!.result,state,reason:state==='recovery_required'?'DOCUMENT_EXTERNAL_OR_PARTIAL_CONTENT':state==='not_applied'?'DOCUMENT_EXPLICIT_RETRY_REQUIRED':undefined} as DocumentApplyOutcome;if(fingerprint(result)===fingerprint(record!.result))return result;
  const selected={p,generation,scope:inventoryScopeFingerprint(p)} as Awaited<ReturnType<typeof target>>;await persist(projectId,actorId,row,{...record!,state,result},selected,[],false,true);return result;
 });}
 return {applyPreview:(projectId:string,input:{proposalId:string;proposalRevision:number})=>preview(projectId,input,'apply'),apply:(projectId:string,actorId:string,input:DocumentApplyInput)=>execute(projectId,actorId,input,'apply'),rollbackPreview:(projectId:string,input:{proposalId:string;proposalRevision:number})=>preview(projectId,input,'rollback'),rollback:(projectId:string,actorId:string,input:DocumentApplyInput)=>execute(projectId,actorId,input,'rollback'),recover};
}
