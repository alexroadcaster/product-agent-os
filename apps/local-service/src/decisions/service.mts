import {createHash,randomUUID} from 'node:crypto';
import type {LocalStore,StoredEntity,StoreWrite} from '../storage/local-store.mts';
import {recipeScopeHash} from '../execution-recipes/contract.mts';
import {safeVisibleValue,safePersistedText} from '../redaction/persisted.mts';
import {autonomyService} from '../autonomy-policy/service.mts';
import type {DecisionView,DecisionKind,DecisionResponse,DecisionsPage} from '../../../../packages/contracts/decisions/decision.ts';
type Runtime={snapshot(input:Record<string,unknown>):Promise<unknown>;dispatch(action:string,input:Record<string,unknown>):Promise<unknown>};
type RequestIdentity={route:string;bindingId:string;runId:string;generation:string;requestId:string|number};
type Decision=Omit<DecisionView,'revision'|'actions'|'runtime'> & {category:'paos_decision';authorityEpoch:number;rootIdentity:string;scopeHash:string|null;request:RequestIdentity|null;runtimeState:string|null;runtimeReceipt?:Record<string,unknown>};
const hash=(v:unknown)=>createHash('sha256').update(JSON.stringify(v)).digest('hex');
const fail=(code:string):never=>{throw Object.assign(new Error('Decision is unavailable'),{code});};
function fields(v:Record<string,any>,keys:string[]){if(!v||typeof v!=='object'||Array.isArray(v)||Object.keys(v).some(k=>!keys.includes(k)))fail('DECISION_INPUT_INVALID');}
function text(v:unknown,max=8000){if(typeof v!=='string'||!v.trim()||v.length>max||v.includes('\0'))fail('DECISION_INPUT_INVALID');return safePersistedText((v as string).trim());}
export const runtimeDecisionId=(projectId:string,sessionId:string,request:RequestIdentity)=>'decision-'+hash([projectId,sessionId,request.route,request.bindingId,request.runId,request.generation,typeof request.requestId,request.requestId]);

/** One local owner mediates S09/S22. Runtime still owns grants; durable intent never grants replay authority. */
export function createDecisions(options:{store:LocalStore;runtime?:Runtime;route?:()=>string;now?:()=>number;recipes?:{list(p:string):Promise<{items:any[]}>};scheduler?:{snapshot(p:string):Promise<any>}}){
 const {store,runtime}=options,now=options.now??Date.now;let tail:Promise<unknown>=Promise.resolve();
 const serial=<T,>(fn:()=>Promise<T>)=>{const p=tail.then(async()=>{await ready;return fn();});tail=p.catch(()=>{});return p;};
 const rows=async(p:string)=>(await store.projectEntities(p)).filter(r=>r.kind==='settings'&&r.data.category==='paos_decision');
 const read=async(p:string,id:string)=>{const r=await store.get(p,id);if(!r||r.kind!=='settings'||r.data.category!=='paos_decision')fail('DECISION_NOT_FOUND');return r!;};
 async function save(p:string,d:Decision,row?:StoredEntity,extra:any[]=[],key?:string,decisionCommand?:StoreWrite['decisionCommand']){
  if(row&&JSON.stringify(row.data)===JSON.stringify(d)&&!extra.length)return row;
  if(!row&&(await rows(p)).length>=5000)fail('DECISION_HISTORY_CAPACITY');
  const project=(await store.project(p))!;d.updatedAt=now();
  await store.write({projectId:p,actorId:'decision-service',expectedAuthorityEpoch:decisionCommand?d.authorityEpoch:project.authorityEpoch,idempotencyKey:key??`decision-state:${d.id}:${row?.revision??0}:${hash(d)}`,...(decisionCommand?{decisionCommand}:{}),changes:[{expectedRevision:row?.revision??0,entity:{id:d.id,kind:'settings',status:d.state,data:d as any}},...extra]});return (await store.get(p,d.id))!;
 }
 function event(d:Decision,event:string,actor:string,detail:string){if(d.history.length>=64)fail('DECISION_HISTORY_CAPACITY');d.history.push({at:now(),event,actor,detail:safePersistedText(detail).slice(0,2000)});}
 const ready=(async()=>{for(const p of await store.projects())for(const row of await rows(p.id)){const d=structuredClone(row.data) as unknown as Decision;if(d.delivery==='intent_persisted'){d.state='outcome_unknown';event(d,'restart_no_replay','service','Response intent has no confirmed receipt');await save(p.id,d,row);}}})();
 async function scope(p:string,taskId:string|null){const project=await store.project(p);if(!project)fail('PROJECT_NOT_FOUND');const task=taskId?await store.get(p,taskId):null;if(taskId&&(!task||task.kind!=='task'||task.deleted))fail('TASK_NOT_FOUND');
  return {project:project!,task,scopeHash:task?recipeScopeHash(task.data):null,scope:{taskRevision:task?.revision??null,files:((task?.data.files??[]) as any[]).slice(0,100).map(f=>({path:String(f.relativePath),operation:f.plannedOperation??null})),summary:task?String(task.title||task.data.title||task.id):'Session-local decision; no task grant',coverage:task?'saved_task_scope':'session_only'}};
 }
 function view(row:StoredEntity):DecisionView{const d=row.data as unknown as Decision;const actions=d.state==='pending'&&d.expiresAt!==null&&d.expiresAt>now()?(d.kind==='runtime_permission'?(d.reviewable?['accept','decline']:['decline']):d.kind==='product'?['accept','return']:['answer']):[];
  const {category,authorityEpoch,rootIdentity,scopeHash,request,runtimeState,runtimeReceipt,...publicData}=d;return safeVisibleValue({...publicData,revision:row.revision,actions,runtime:request?{...request,operationState:runtimeState}:null});
 }
 function review(state:any,op?:any,request?:any){const proposal=Array.isArray(request?.details?.changes)?request.details.changes:null,changes=op?.fileChanges??proposal??state.fileChanges??[],checks=op?[{id:op.operationId,kind:'command',status:op.state,summary:typeof op.exitCode==='number'?`exitCode ${op.exitCode}`:'No terminal command receipt'}]:(state.checks??[]).slice(0,64).map((c:any)=>({id:String(c.id),kind:String(c.itemType??'check'),status:String(c.status),summary:String(c.command??c.reason??'').slice(0,2000)}));
  const status=changes.length?(proposal||changes.some((c:any)=>c.kind==='proposed')?'proposed' as const:'observed' as const):'unavailable' as const;
  return safeVisibleValue({diff:{status,text:changes.slice(0,64).map((c:any)=>`${c.path}\n${c.diff??c.reason??'Diff unavailable'}`).join('\n').slice(0,64000),reason:status==='proposed'?'Runtime-reported proposal; no executed file effect inferred':changes.length?'Observed changes; coverage remains partial':'Future command diff is unavailable before execution'},evidence:{coverage:checks.length?'partial':'unavailable',items:checks}});
 }
 async function observeOne(p:string,s:string,request:any,state:any,op?:any,job?:any){
  if(typeof request.bindingId!=='string'||typeof request.runId!=='string'||typeof request.generation!=='string'||!['string','number'].includes(typeof request.requestId)||!Number.isFinite(request.expiresAt))return null;
  const identity:RequestIdentity={route:request.route??options.route?.()??state.route??'unknown',bindingId:request.bindingId,runId:request.runId,generation:request.generation,requestId:request.requestId},id=runtimeDecisionId(p,s,identity),old=await store.get(p,id);
  let d:Decision;if(old)d=structuredClone(old.data) as unknown as Decision;else{const run=await store.get(p,identity.runId),raw=(run?.data.appAgentRun??run?.data.runtimeRun) as any,taskId=raw?.taskContext?.taskId??raw?.taskId??null,c=await scope(p,taskId);
   d={category:'paos_decision',id,projectId:p,sessionId:s,taskId,kind:'runtime_permission',source:request.source??'native_runtime',title:request.kind==='file'?'Runtime file permission':'Runtime command permission',body:safePersistedText(String(request.details?.command??request.command??request.description??'Details unavailable')).slice(0,16384),state:'pending',delivery:'not_sent',response:null,answer:null,createdAt:now(),updatedAt:now(),expiresAt:request.expiresAt,reviewable:op?true:request.reviewable===true,authorityEpoch:c.project.authorityEpoch,rootIdentity:c.project.rootIdentity,scopeHash:c.scopeHash,scope:c.scope,...review(state,op,request),request:identity,runtimeState:op?.state??request.state??'pending',history:[]};event(d,'requested',d.source,'Runtime-owned request; no permission granted');
  }
  const previous=hash([d.state,d.delivery,d.response,d.runtimeState,d.diff,d.evidence]);
  if(op){d.runtimeState=op.state;Object.assign(d,review(state,op));if(['accept','decline','cancel'].includes(op.decision)){d.state='resolved';d.response=op.decision;d.delivery='acknowledged';}
   else if(op.decision==='expired'||d.expiresAt!<=now())d.state='expired';else if(['recovery_required','interrupted','completed','failed'].includes(job?.state)||op.state!=='awaiting_approval')d.state='stale';
  }else if(request.state==='response_sent'){d.state='resolved';d.delivery='response_sent';d.response=request.decision??d.response;}
  if(d.state==='pending'&&d.expiresAt!<=now())d.state='expired';
  if(old&&previous!==hash([d.state,d.delivery,d.response,d.runtimeState,d.diff,d.evidence]))event(d,'source_observed',d.source,`${d.state}; ${d.runtimeState}`);
  return view(await save(p,d,old??undefined));
 }
 async function observe(p:string,s:string,state:any){const ids=new Map<string,string>();for(const r of state.pendingApprovals??[]){const d=await observeOne(p,s,r,state);if(d)ids.set(`${typeof r.requestId}:${r.requestId}`,d.id);}
  // A successful snapshot may clear an observed request. Absence is not an accepted response or command success.
  const currentIds=new Set(ids.values());for(const row of await rows(p)){const d=structuredClone(row.data) as unknown as Decision;if(d.kind!=='runtime_permission'||d.sessionId!==s||d.state!=='pending'||!d.request||currentIds.has(d.id))continue;
   if((options.route?.()??d.request.route)!==d.request.route)continue;d.state=d.expiresAt!<=now()?'expired':'stale';event(d,'request_no_longer_pending','runtime','Current snapshot no longer offers this exact request; no response inferred');await save(p,d,row);
  }return {...state,pendingApprovals:(state.pendingApprovals??[]).map((r:any)=>({...r,decisionId:ids.get(`${typeof r.requestId}:${r.requestId}`)}))};}
 async function sync(p:string){const entities=await store.projectEntities(p);let coverage='not_available';
  // App operations are durable source truth even if no browser observed their pending interval.
  for(const row of entities.filter(r=>r.kind==='run'&&r.data.appAgentRun)){const job=row.data.appAgentRun as any;for(const op of job.operations??[])await observeOne(p,job.sessionId,{route:'codex_app_agent',source:'paos_domain',kind:'command',requestId:op.operationId,bindingId:job.bindingId,runId:job.id,generation:op.generation,expiresAt:op.expiresAt,details:{command:JSON.stringify(op.argv)}},{},op,job);}
  if(runtime){const known=await rows(p);const sessions=[...new Set([...entities.filter(r=>r.kind==='run'&&!['completed','failed','interrupted'].includes(r.status)).map(r=>(r.data.appAgentRun??r.data.runtimeRun) as any).map(r=>r?.sessionId),...known.filter(r=>r.data.kind==='runtime_permission'&&['pending','outcome_unknown'].includes(String(r.data.state))).map(r=>r.data.sessionId)].filter((s):s is string=>typeof s==='string'&&!!s))].slice(0,100);
   for(const s of sessions)try{await observe(p,s,await runtime.snapshot({projectId:p,sessionId:s}));coverage='observed_requests_and_durable_app_operations';}catch{coverage='partial_runtime_unavailable';}
   if(!sessions.length)coverage='durable_app_operations; native_requests_observed_only';
  }
  for(const row of await rows(p)){const d=structuredClone(row.data) as unknown as Decision;if(d.state==='pending'&&d.expiresAt!<=now()){d.state='expired';event(d,'expired','service','Deadline passed; no response dispatched');await save(p,d,row);}}
  return coverage;
 }
 async function list(p:string,query=new URLSearchParams()):Promise<DecisionsPage>{const coverage=await sync(p),all=await rows(p),kind=query.get('kind'),status=query.get('state'),session=query.get('sessionId');let filtered=all.filter(r=>(!kind||r.data.kind===kind)&&(!status||r.data.state===status)&&(!session||r.data.sessionId===session));filtered.sort((a,b)=>(b.data.createdAt as number)-(a.data.createdAt as number)||a.id.localeCompare(b.id));
  const offset=Number(query.get('offset')??0),limit=Number(query.get('limit')??50);if(!Number.isSafeInteger(offset)||offset<0||offset>10000||!Number.isSafeInteger(limit)||limit<1||limit>100)fail('DECISION_INPUT_INVALID');const policy=await autonomyService(store).snapshot(p),executions=(await store.projectEntities(p)).filter(r=>r.data.category==='recipe_execution'&&!['completed','failed','cancelled'].includes(String(r.data.state))).map(r=>({id:r.id,taskId:String(r.data.taskId),sessionId:String(r.data.sessionId),state:String(r.data.state),reason:typeof r.data.reason==='string'?r.data.reason:null,checkpoint:null as string|null}));
  if(options.recipes){const views=await options.recipes.list(p);for(const e of executions)e.checkpoint=views.items.find(v=>v.id===e.id)?.recovery?.checkpoint??null;}
  const runs=(await store.projectEntities(p)).filter(r=>r.kind==='run'&&!['completed','failed','interrupted'].includes(r.status)).map(r=>{const j=(r.data.appAgentRun??r.data.runtimeRun??{}) as any;return {id:r.id,sessionId:String(j.sessionId??''),taskId:j.taskContext?.taskId??j.taskId??null,state:r.status,reason:j.autonomyStopReason??null};});
  const q=options.scheduler?await options.scheduler.snapshot(p):null;const queue=q?{paused:q.paused,items:q.items.map((e:any)=>({id:e.id,taskId:e.taskId,state:e.state,waitReasons:e.waitReasons}))}:null;
  return {items:filtered.slice(offset,offset+limit).map(view),hasMore:filtered.length>offset+limit,offset,total:filtered.length,coverage:{runtime:coverage,legacyNotes:'Session product comments remain in their original history'},autonomy:{policyRevision:policy.revision,paused:policy.paused,usedRuns:policy.usedRuns,maxRuns:policy.policy?.maxRuns??null,enforcement:policy.enforcement,hostToolsConstrained:false},executions,runs,queue};
 }
 const receiptId=(key:string)=>'decision-receipt-'+hash(key);
 function commandInput(input:Record<string,any>){if(typeof input.idempotencyKey!=='string'||!input.idempotencyKey.trim()||input.idempotencyKey.length>200||/[\0\r\n]/.test(input.idempotencyKey)||safePersistedText(input.idempotencyKey)!==input.idempotencyKey)fail('DECISION_INPUT_INVALID');}
 async function respond(p:string,id:string,actor:string,input:Record<string,any>):Promise<DecisionResponse>{
  fields(input,['expectedRevision','expectedAuthorityEpoch','idempotencyKey','response','answer','reason']);commandInput(input);const key=receiptId(input.idempotencyKey),digest=hash({id,input}),receipt=await store.get(p,key);
  if(receipt){if(receipt.data.digest!==digest)fail('IDEMPOTENCY_CONFLICT');if(receipt.data.phase==='committed')return receipt.data.result as DecisionResponse;await sync(p);return {decision:view(await read(p,id))};}
  await sync(p);const row=await read(p,id),d=structuredClone(row.data) as unknown as Decision,project=(await store.project(p))!;
  if(input.expectedAuthorityEpoch!==project.authorityEpoch||d.authorityEpoch!==project.authorityEpoch)fail('AUTHORITY_EPOCH_CONFLICT');
  if(d.state==='resolved'&&d.kind==='runtime_permission'&&d.response===input.response)return {decision:view(row),runtimeReceipt:d.runtimeReceipt};
  if(d.state!=='pending'||d.expiresAt!<=now())fail(d.state==='expired'||d.expiresAt!<=now()?'DECISION_EXPIRED':'DECISION_NOT_PENDING');if(row.revision!==input.expectedRevision)fail('REVISION_CONFLICT');
  if(!view(row).actions.includes(input.response))fail('DECISION_RESPONSE_INVALID');const c=await scope(p,d.taskId);if(c.project.rootIdentity!==d.rootIdentity||c.scopeHash!==d.scopeHash)fail('DECISION_SCOPE_CHANGED');
  const answer=input.response==='answer'?text(input.answer):null;const reason=input.reason===undefined?'Explicit owner response':text(input.reason,2000);
  const fence:StoreWrite['decisionCommand']={id,revision:row.revision,taskId:d.taskId,scopeHash:d.scopeHash,rootIdentity:d.rootIdentity,expiresAt:d.expiresAt!,...(options.now?{validationTime:now()}: {})};
  if(!d.request){d.state='resolved';d.delivery='not_applicable';d.response=input.response;d.answer=answer;event(d,'owner_responded',actor,reason);const result={decision:view({...row,revision:row.revision+1,data:d as any})};await save(p,d,row,[{expectedRevision:0,entity:{id:key,kind:'settings',data:{category:'decision_receipt',digest,phase:'committed',result}}}],`decision-user:${input.idempotencyKey}`,fence);return result;}
  if(!runtime||!d.sessionId)fail('DECISION_RUNTIME_UNAVAILABLE');const state=await runtime!.snapshot({projectId:p,sessionId:d.sessionId}) as any;
  const current=(state.pendingApprovals??[]).find((r:any)=>r.bindingId===d.request!.bindingId&&r.runId===d.request!.runId&&r.generation===d.request!.generation&&typeof r.requestId===typeof d.request!.requestId&&r.requestId===d.request!.requestId&&r.state==='pending');
  if(!current||state.bindingId!==d.request.bindingId||state.runId!==d.request.runId||state.generation!==d.request.generation||(options.route?.()??d.request.route)!==d.request.route)fail('DECISION_STALE');
  if(input.response==='accept'&&current.reviewable!==true)fail('approval_details_unavailable');
  if(now()>=d.expiresAt!||now()>=current.expiresAt)fail('DECISION_EXPIRED');
  d.state='outcome_unknown';d.delivery='intent_persisted';d.response=input.response;event(d,'response_intent',actor,reason);
  let saved=await save(p,d,row,[{expectedRevision:0,entity:{id:key,kind:'settings',data:{category:'decision_receipt',digest,phase:'intent'}}}],`decision-intent:${input.idempotencyKey}`,fence);
  const {route:ignored,...identity}=d.request;let raw:any;try{raw=await runtime!.dispatch('approve',{projectId:p,sessionId:d.sessionId,...identity,decision:input.response});}
  catch(error){event(d,'response_unconfirmed','runtime',(error as any).code??'unknown');await save(p,d,saved);throw error;}
  d.state='resolved';d.delivery=raw?.state==='response_sent'?'response_sent':'acknowledged';d.runtimeReceipt=safeVisibleValue(raw??{});event(d,'response_recorded','runtime',d.delivery);
  const result:DecisionResponse={decision:view({...saved,revision:saved.revision+1,data:d as any}),runtimeReceipt:d.runtimeReceipt};const oldReceipt=(await store.get(p,key))!;
  await save(p,d,saved,[{expectedRevision:oldReceipt.revision,entity:{id:key,kind:'settings',data:{category:'decision_receipt',digest,phase:'committed',result}}}],`decision-commit:${input.idempotencyKey}`);return result;
 }
 return {
  initialized:async()=>{await ready;},list:(p:string,q?:URLSearchParams)=>serial(()=>list(p,q)),get:(p:string,id:string)=>serial(async()=>{await sync(p);return view(await read(p,id));}),
  observe:(p:string,s:string,state:unknown)=>serial(()=>observe(p,s,state)),
  respond:(p:string,id:string,actor:string,input:Record<string,any>)=>serial(()=>respond(p,id,actor,input)),
  inline:(input:Record<string,any>,actor:string)=>serial(async()=>{if(!runtime)fail('DECISION_RUNTIME_UNAVAILABLE');const p=text(input.projectId,200),s=text(input.sessionId,200);await observe(p,s,await runtime!.snapshot({projectId:p,sessionId:s}));
   const request:RequestIdentity={route:options.route?.()??'codex_app_agent',bindingId:input.bindingId,runId:input.runId,generation:input.generation,requestId:input.requestId};const id=runtimeDecisionId(p,s,request),row=await read(p,id);const result=await respond(p,id,actor,{expectedRevision:row.revision,expectedAuthorityEpoch:(await store.project(p))!.authorityEpoch,idempotencyKey:'inline:'+hash([id,input.decision]),response:input.decision});return result.runtimeReceipt??result;
  }),
  create:(p:string,actor:string,input:Record<string,any>)=>serial(async()=>{
   fields(input,['kind','title','body','taskId','sessionId','proposedDiff','evidenceIds','expiresInSeconds','expectedAuthorityEpoch','idempotencyKey']);commandInput(input);if(!['clarification','product'].includes(input.kind))fail('DECISION_KIND_FORBIDDEN');const digest=hash(input),key=receiptId(input.idempotencyKey),old=await store.get(p,key);if(old){if(old.data.digest!==digest)fail('IDEMPOTENCY_CONFLICT');return old.data.result as DecisionView;}
   if(input.taskId!==undefined&&input.taskId!==null)text(input.taskId,200);if(input.sessionId!==undefined&&input.sessionId!==null)text(input.sessionId,200);
   const c=await scope(p,input.taskId??null);if(input.expectedAuthorityEpoch!==c.project.authorityEpoch)fail('AUTHORITY_EPOCH_CONFLICT');const session=input.sessionId?await store.get(p,input.sessionId):null;if(input.sessionId&&(!session||session.kind!=='session'||session.deleted))fail('SESSION_NOT_FOUND');
   if(!Number.isSafeInteger(input.expiresInSeconds)||input.expiresInSeconds<60||input.expiresInSeconds>604800)fail('DECISION_INPUT_INVALID');const ids=input.evidenceIds??[];if(!Array.isArray(ids)||ids.length>32)fail('DECISION_INPUT_INVALID');const evidence=[];for(const id of ids){if(typeof id!=='string')fail('DECISION_INPUT_INVALID');const row=await store.get(p,id);if(!row||!['task','document','comment','evidence'].includes(row.kind)||row.deleted)fail('DECISION_EVIDENCE_UNAVAILABLE');evidence.push({id,kind:row!.kind,status:row!.status,summary:safePersistedText(row!.title).slice(0,2000)});}
   const d:Decision={category:'paos_decision',id:'decision-'+randomUUID(),projectId:p,sessionId:session?.id??null,taskId:c.task?.id??null,kind:input.kind,source:'local_owner',title:text(input.title,200),body:text(input.body),state:'pending',delivery:'not_applicable',response:null,answer:null,createdAt:now(),updatedAt:now(),expiresAt:now()+input.expiresInSeconds*1000,reviewable:true,authorityEpoch:c.project.authorityEpoch,rootIdentity:c.project.rootIdentity,scopeHash:c.scopeHash,scope:c.scope,diff:{status:input.proposedDiff?'proposed':'unavailable',text:input.proposedDiff?text(input.proposedDiff,64000):'',reason:'Owner proposal; accepting records a decision and does not apply file changes'},evidence:{coverage:evidence.length?'owner_referenced':'unavailable',items:evidence},request:null,runtimeState:null,history:[]};event(d,'created',actor,'Local decision; never a runtime permission');const result=view({revision:1,data:d} as any);await save(p,d,undefined,[{expectedRevision:0,entity:{id:key,kind:'settings',data:{category:'decision_receipt',digest,phase:'committed',result}}}],`decision-create:${input.idempotencyKey}`);return result;
  }),
 };
}
