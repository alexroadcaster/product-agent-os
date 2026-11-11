import {createHash,randomBytes,randomUUID,timingSafeEqual} from 'node:crypto';
import type {LocalStore,StoredEntity} from '../storage/local-store.mts';
import {bindProject} from '../adapters/project-sources.ts';

type Input=Record<string,unknown>;
type State='queued'|'running'|'cancel_requested'|'recovery_required'|'completed'|'failed'|'interrupted';
type Binding={id:string;projectId:string;sessionId:string;mode:'discussion'|'planning';workspaceRoot:string;rootIdentity:string};
type Job={id:string;bindingId:string;projectId:string;sessionId:string;mode:Binding['mode'];clientMessageId:string;input:string;inputDigest:string;
 state:State;seq:number;workerId?:string;generation?:string;lastReport?:{key:string;hash:string;receipt:Input}};
type Worker={workerId:string;generation:string;leaseToken:string;expiresAt:number};
const route='codex_app_agent';
const terminal=new Set<State>(['completed','failed','interrupted']);
const capabilities=Object.freeze({nativeSandbox:false,actualAppServer:false,cooperativeCancel:true,execution:false,streaming:false,permissions:false,hostIdentity:'attested_not_cryptographic'});
const hash=(value:string)=>createHash('sha256').update(value).digest('hex');
function fail(code:string):never{throw Object.assign(new Error('The App agent operation is unavailable.'),{code});}
function input(value:unknown,keys:string[]):Input {
 if(!value||typeof value!=='object'||Array.isArray(value))fail('app_agent_input_invalid');
 const row=value as Input;if(Object.keys(row).some(key=>!keys.includes(key)))fail('app_agent_input_invalid');return row;
}
function text(row:Input,key:string,max=200):string {const value=row[key];if(typeof value!=='string'||!value.trim()||Buffer.byteLength(value)>max||/[\0]/.test(value))fail('app_agent_input_invalid');return value;}
/** App-hosted pull channel. Host identity is attested by the trusted caller, not proven by this protocol.
 * Public browser calls never receive worker capabilities. No App Server/sandbox/auth cache is used.
 * One owner service serializes operations; profile instance reservation remains the cross-process boundary. */
export function createAppAgentGateway(options:{store:LocalStore;profileId:string;actorId:string;now?:()=>number}) {
 const {store}=options;const now=options.now??Date.now;const bindings=new Map<string,Binding>();
 let selected=false,closed=false,closing=false,foreignUnresolved=false,worker:Worker|undefined,active:Job|undefined;let queue=Promise.resolve();let shutdown:Promise<void>|undefined;
 const latest=new Map<string,Job>();const leaseMs=30_000;
 const leaseSecrets=new Set<string>();
 const redact=(value:string)=>{for(const secret of leaseSecrets)value=value.replaceAll(secret,'[REDACTED]');return value;};
 async function all(projectId:string,kind:'settings'|'run') {
  const rows:StoredEntity[]=[];for(let offset=0;offset<10_000;offset+=100){const page=await store.list(projectId,{kind,limit:100,offset});rows.push(...page);if(page.length<100)return rows;}
  fail('app_agent_history_limit');
 }
 async function save(job:Job,extra:Array<{expectedRevision:number;entity:any}>=[],requireIdle=false) {
  const project=await store.project(job.projectId);if(!project)fail('project_not_found');
  const previous=await store.get(job.projectId,job.id);
  const bindingRow=await store.get(job.projectId,`app-binding-${job.bindingId}`);
  if(!bindingRow||bindingRow.kind!=='settings'||bindingRow.data.profileId!==options.profileId)fail('binding_scope_mismatch');
  await store.write({projectId:job.projectId,actorId:options.actorId,expectedAuthorityEpoch:project.authorityEpoch,
   idempotencyKey:`app-agent:${job.id}:${previous?.revision??0}:${hash(JSON.stringify(job))}`,...(requireIdle?{requireIdle:true as const}:{}),
   changes:[{expectedRevision:previous?.revision??0,entity:{id:job.id,kind:'run',status:job.state,data:{appAgentRun:job}}},
    {expectedRevision:bindingRow.revision,entity:{id:bindingRow.id,kind:'settings',data:{...bindingRow.data,lastRunId:job.id}}},...extra]});
  latest.set(job.bindingId,job);
 }
 const ready=(async()=>{
  const savedLatest=new Map<string,string>();
  for(const project of await store.projects()) {
   for(const row of await all(project.id,'settings'))if(row.data.appAgentBinding&&row.data.profileId===options.profileId){const binding=row.data.appAgentBinding as Binding;bindings.set(binding.id,binding);if(typeof row.data.lastRunId==='string')savedLatest.set(binding.id,row.data.lastRunId);}
   for(const row of await all(project.id,'run')) {
    if(!row.data.appAgentRun){if(!terminal.has(row.status as State))foreignUnresolved=true;continue;}
    const job=row.data.appAgentRun as Job;if(!bindings.has(job.bindingId)){if(!terminal.has(job.state))foreignUnresolved=true;continue;}
    if(savedLatest.get(job.bindingId)===job.id||!latest.has(job.bindingId))latest.set(job.bindingId,job);if(!terminal.has(job.state)){job.state='recovery_required';await save(job);if(active)fail('app_agent_multiple_unresolved');active=job;}
   }
  }
 })();
 // Observe startup errors even when a caller only reads synchronous connection status.
 void ready.catch(()=>{});
 function serial<T>(operation:()=>Promise<T>):Promise<T>{if(closing||closed)return Promise.reject(Object.assign(new Error('The App agent operation is unavailable.'),{code:'runtime_stopping'}));const pending=queue.then(async()=>{await ready;if(closed)fail('runtime_stopping');await expire();return operation();});queue=pending.then(()=>{},()=>{});return pending;}
 async function expire(){if(worker&&worker.expiresAt<=now()){if(active&&!terminal.has(active.state)){const changed={...active,state:'recovery_required' as const};await save(changed);active=changed;}worker=undefined;}}
 function status(){const verified=selected&&!!worker&&worker.expiresAt>now();return {route,state:verified?'connected':selected?'waiting_for_worker':'disconnected',verified,
  verificationScope:'app_agent_lease',modelAccess:'unverified',actualCodex:false,hostIdentityAttested:verified,capabilities};}
 async function scoped(row:Input):Promise<{binding?:Binding;projectId:string;sessionId:string}> {
  const projectId=text(row,'projectId'),sessionId=text(row,'sessionId');const project=await store.project(projectId);const session=await store.get(projectId,sessionId);
  if(!project||!session||session.kind!=='session'||session.deleted)fail('scope_not_found');
  const pin=await bindProject(projectId,project.canonicalRoot);if(pin.directoryIdentity!==project.rootIdentity)fail('project_root_changed');
  const binding=row.bindingId===undefined?undefined:bindings.get(text(row,'bindingId'));
  if(row.bindingId!==undefined&&(!binding||binding.projectId!==projectId||binding.sessionId!==sessionId||binding.workspaceRoot!==pin.workspaceRoot||binding.rootIdentity!==pin.directoryIdentity))fail('binding_scope_mismatch');
  return {binding,projectId,sessionId};
 }
 function authenticated(row:Input):Worker {
  const workerId=text(row,'workerId'),generation=text(row,'generation'),token=text(row,'leaseToken',128);
  if(!selected||!worker||worker.workerId!==workerId||worker.generation!==generation||!/^[a-f0-9]{64}$/.test(token)||token.length!==worker.leaseToken.length
   ||!timingSafeEqual(Buffer.from(token),Buffer.from(worker.leaseToken)))fail('app_agent_lease_invalid');return worker;
 }
 function publicJob(job:Job){return {id:job.id,bindingId:job.bindingId,projectId:job.projectId,sessionId:job.sessionId,state:job.state,mode:job.mode,route};}
 function claimed(job:Job){return {runId:job.id,bindingId:job.bindingId,projectId:job.projectId,sessionId:job.sessionId,mode:job.mode,input:job.input,clientMessageId:job.clientMessageId,cancelRequested:job.state==='cancel_requested'};}
 const connection={status,
  connect: (value:unknown)=>serial(async()=>{input(value,['connectionId']);selected=true;return status();}),
  disconnect:()=>serial(async()=>{if(active){const changed={...active,state:'recovery_required' as const};await save(changed);active=changed;}worker=undefined;selected=false;return status();})};
 const runtime={
  snapshot:(value:Input)=>serial(async()=>{const row=input(value,['projectId','sessionId']);const scope=await scoped(row);
   const binding=[...bindings.values()].reverse().find(item=>item.projectId===scope.projectId&&item.sessionId===scope.sessionId);
   const running=active?.bindingId===binding?.id?active:undefined;const last=binding?latest.get(binding.id):undefined;
   return {...status(),state:running?.state??last?.state??status().state,bindingId:binding?.id,runId:running?.id,mode:binding?.mode,
    generation:worker?.generation,canSend:status().verified&&!!binding&&!active&&!foreignUnresolved,reason:!status().verified?'app_agent_not_attached':foreignUnresolved?'foreign_runtime_recovery_required':!binding?'binding_required':active?'runtime_busy':null,
    pendingApprovals:[],visibleDrafts:[],fileChanges:[],checks:[],capabilities,
    profile:binding?{id:'codex_app_agent',role:binding.mode==='discussion'?'analyst':'planner',assignment:binding.mode,version:'app_pull_v1',coverage:'attested'}:null,
    questions:{status:'unsupported',reason:'app_host_approvals_are_separate'},streaming:{policy:'final_answer_only',phaseStatus:'not_observed'}};
  }),
  dispatch:(action:string,value:Input)=>serial(async()=>{
   const row=input(value,['projectId','sessionId','bindingId','clientMessageId','input','mode','taskId','runId','generation']);const scope=await scoped(row);
   if(row.generation!==undefined)text(row,'generation');
   if(action==='bindings') {
    if(!status().verified)fail('app_agent_not_attached');if(active||foreignUnresolved)fail('runtime_busy');
    if(row.mode==='execution')fail('execution_boundary_unverified');if(row.mode!=='discussion'&&row.mode!=='planning')fail('mode_invalid');
    const existing=[...bindings.values()].find(item=>item.projectId===scope.projectId&&item.sessionId===scope.sessionId&&item.mode===row.mode);
    if(existing){bindings.delete(existing.id);bindings.set(existing.id,existing);return {bindingId:existing.id,projectId:scope.projectId,sessionId:scope.sessionId,mode:existing.mode,route};}
    const project=(await store.project(scope.projectId))!;const pin=await bindProject(project.id,project.canonicalRoot);
    if(pin.directoryIdentity!==project.rootIdentity)fail('project_root_changed');
    const binding:Binding={id:randomUUID(),projectId:scope.projectId,sessionId:scope.sessionId,mode:row.mode,workspaceRoot:pin.workspaceRoot,rootIdentity:project.rootIdentity};
    await store.write({projectId:project.id,actorId:options.actorId,expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:`app-binding:${binding.id}`,
     requireIdle:true,changes:[{expectedRevision:0,entity:{id:`app-binding-${binding.id}`,kind:'settings',data:{profileId:options.profileId,appAgentBinding:binding}}}]});bindings.set(binding.id,binding);
    return {bindingId:binding.id,projectId:binding.projectId,sessionId:binding.sessionId,mode:binding.mode,route};
   }
   const binding=scope.binding;if(!binding)fail('binding_not_found');
   if(action==='send') {
    const messageId=text(row,'clientMessageId'),body=text(row,'input',32*1024);if(row.taskId!==undefined) {
     const task=await store.get(scope.projectId,text(row,'taskId'));if(!task||task.kind!=='task'||task.deleted)fail('task_scope_mismatch');}
    const id=`app-run-${hash(`${options.profileId}:${binding.id}:${messageId}`)}`;const digest=hash(JSON.stringify({body,taskId:row.taskId??null}));
    const previous=await store.get(scope.projectId,id);if(previous){const old=previous.data.appAgentRun as Job;if(old.inputDigest!==digest)fail('message_conflict');return publicJob(old);}
    if(!status().verified)fail('app_agent_not_attached');if(active||foreignUnresolved)fail('runtime_busy');
    const job:Job={id,bindingId:binding.id,projectId:binding.projectId,sessionId:binding.sessionId,mode:binding.mode,clientMessageId:messageId,input:body,inputDigest:digest,state:'queued',seq:0};
    await save(job,[{expectedRevision:0,entity:{id:`app-user-${hash(id)}`,kind:'message',parentId:job.sessionId,body,status:'committed',data:{role:'user',runId:id,route}}}],true);active=job;return publicJob(job);
   }
   if(action==='interrupt') {
    if(!active||active.bindingId!==binding.id||active.id!==text(row,'runId'))fail('run_not_interruptible');
    if(active.state==='recovery_required')fail('run_not_interruptible');
    const changed={...active,state:active.state==='queued'?'interrupted' as const:'cancel_requested' as const};await save(changed);active=terminal.has(changed.state)?undefined:changed;return publicJob(changed);
   }
   if(action==='reconcile')return active?.bindingId===binding.id?publicJob(active):null;
   fail('action_unsupported');
  })};
 async function agent(action:string,value:Input):Promise<any>{return serial(async()=>{
  if(action==='attach') {
   const row=input(value,['hostIdentity','workerId','generation']);if(row.hostIdentity!=='codex_app')fail('app_agent_host_invalid');if(!selected)fail('app_agent_not_selected');if(worker)fail('app_agent_worker_busy');
   if(leaseSecrets.size>=64)fail('app_agent_restart_required');
   worker={workerId:text(row,'workerId'),generation:text(row,'generation'),leaseToken:randomBytes(32).toString('hex'),expiresAt:now()+leaseMs};leaseSecrets.add(worker.leaseToken);return {...worker};
  }
  const row=input(value,['workerId','generation','leaseToken',...(action==='report'?['runId','seq','idempotencyKey','status','text']:[])]);const current=authenticated(row);
  if(action==='heartbeat'){current.expiresAt=now()+leaseMs;return {expiresAt:current.expiresAt,job:active?.workerId===current.workerId&&active.generation===current.generation?{runId:active.id,cancelRequested:active.state==='cancel_requested',state:active.state}:null};}
  if(action==='claim') {
   current.expiresAt=now()+leaseMs;
   if(!active||active.state==='recovery_required')return {job:null};
   await scoped({projectId:active.projectId,sessionId:active.sessionId,bindingId:active.bindingId});
   if(active.state==='queued'){const changed={...active,state:'running' as const,workerId:current.workerId,generation:current.generation};await save(changed);active=changed;}
   if(active.workerId!==current.workerId||active.generation!==current.generation)fail('app_agent_generation_mismatch');return {job:claimed(active)};
  }
  if(action==='report') {
   const runId=text(row,'runId'),key=text(row,'idempotencyKey');let previous:StoredEntity|null=null;
   for(const project of await store.projects()){const found=await store.get(project.id,runId);if(found){if(previous)fail('app_agent_run_ambiguous');previous=found;}}
   const job=previous?.data.appAgentRun as Job|undefined;
   if(!job||job.workerId!==current.workerId||job.generation!==current.generation)fail('app_agent_generation_mismatch');
   const digest=hash(JSON.stringify({seq:row.seq,status:row.status,text:row.text??null}));
   if(job.lastReport?.key===key){if(job.lastReport.hash!==digest)fail('app_agent_report_conflict');return job.lastReport.receipt;}
   await scoped({projectId:job.projectId,sessionId:job.sessionId,bindingId:job.bindingId});
   if(!active||active.id!==runId||job.state==='recovery_required'||terminal.has(job.state))fail('app_agent_report_stale');
   if(!Number.isSafeInteger(row.seq)||row.seq!==job.seq+1)fail('app_agent_sequence_invalid');
   if(!['completed','interrupted','failed'].includes(String(row.status)))fail('app_agent_report_invalid');
   if(job.state==='cancel_requested'&&row.status!=='interrupted')fail('app_agent_cancel_ack_required');
   const body=row.text===undefined?'':redact(text(row,'text',32*1024));if(row.status==='completed'&&!body)fail('app_agent_result_required');
   const receipt={runId,seq:row.seq,state:row.status,route};const changed:Job={...job,state:row.status as State,seq:row.seq as number,lastReport:{key,hash:digest,receipt}};
   await save(changed,body?[{expectedRevision:0,entity:{id:`app-assistant-${hash(runId)}`,kind:'message',parentId:job.sessionId,body,status:'committed',data:{role:'assistant',runId,route,coverage:'agent_reported'}}}]:[]);active=undefined;return receipt;
  }
  fail('app_agent_action_unsupported');
 });}
 return {connection,runtime,agent,close(){closing=true;shutdown??=(async()=>{await queue;await ready;if(active){const changed={...active,state:'recovery_required' as const};await save(changed);active=changed;}selected=false;worker=undefined;closed=true;})().catch(error=>{shutdown=undefined;throw error;});return shutdown;}};
}
