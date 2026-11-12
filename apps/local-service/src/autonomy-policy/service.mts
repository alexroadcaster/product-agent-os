import {createHash,randomUUID} from 'node:crypto';
import type {LocalStore} from '../storage/local-store.mts';
import {decodeAutonomyPolicy,type AutonomyPolicy,type AutonomyPreview,type AutonomyReservation,type AutonomySnapshot} from '../../../../packages/contracts/autonomy/policy.ts';

const id='autonomy-policy';
type State={policy:AutonomyPolicy|null;paused:boolean;budgetId:string;runs:AutonomyReservation[]};
type Runtime={dispatch(action:string,input:Record<string,unknown>):Promise<unknown>};
function fail(code:string):never{throw Object.assign(new Error('Autonomy action unavailable'),{code});}
const hash=(v:unknown)=>createHash('sha256').update(JSON.stringify(v)).digest('hex');
const empty=():State=>({policy:null,paused:true,budgetId:'',runs:[]});
const services=new WeakMap<LocalStore,ReturnType<typeof createService>>();

/** One in-process owner per store; SQLite revisions fence stale writers and survive process restart. */
export function autonomyService(store:LocalStore,now:()=>number=Date.now){
  let service=services.get(store);if(!service){service=createService(store,now);services.set(store,service);}return service;
}
function createService(store:LocalStore,now:()=>number){
  let queue:Promise<unknown>=Promise.resolve();
  function serial<T>(fn:()=>Promise<T>):Promise<T>{const work=queue.then(fn);queue=work.catch(()=>{});return work;}
  async function read(projectId:string){
    if(!await store.project(projectId))fail('PROJECT_NOT_FOUND');
    const row=await store.get(projectId,id);
    return {revision:row?.revision??0,state:row?structuredClone(row.data) as unknown as State:empty()};
  }
  function view(revision:number,state:State):AutonomySnapshot{return {...structuredClone(state),revision,usedRuns:state.runs.length,
    enforcement:'paos_mediated_commands',hostToolsConstrained:false,perFileSandbox:false};}
  async function snapshot(projectId:string){const {revision,state}=await read(projectId);return view(revision,state);}
  async function preview(projectId:string,value:unknown,expectedRevision:unknown):Promise<AutonomyPreview>{
    const {revision}=await read(projectId);if(expectedRevision!==revision)fail('AUTONOMY_REVISION_CONFLICT');
    const policy=decodeAutonomyPolicy(value),whole=policy.allowedPaths.length===1&&policy.allowedPaths[0]==='.';
    return {policy,previewDigest:hash({projectId,revision,policy}),executable:whole&&policy.allowedTaskIds.length>0,
      reasons:[...(!whole?['AUTONOMY_PATH_BOUNDARY_UNAVAILABLE']:[]),...(!policy.allowedTaskIds.length?['AUTONOMY_TASK_SCOPE_REQUIRED']:[])],
      boundaries:{hostPermissionsChanged:false,nativeApprovalRequired:true,concurrency:1,scope:whole?'entire_workspace':'unsupported_narrow_paths',tokenCostMetering:'unavailable'}};
  }
  async function write(projectId:string,revision:number,state:State,key:string,actorId='autonomy-runtime',requireIdle=false,extra:Parameters<LocalStore['write']>[0]['changes']=[]){
    const project=await store.project(projectId);if(!project)fail('PROJECT_NOT_FOUND');
    await store.write({projectId,actorId,idempotencyKey:key,expectedAuthorityEpoch:project.authorityEpoch,...(requireIdle?{requireIdle:true as const}:{}),
      changes:[{expectedRevision:revision,entity:{id,kind:'settings',data:state as unknown as Record<string,unknown>}},...extra]});
    return view(revision+1,state);
  }
  async function command(projectId:string,actorId:string,action:string,input:Record<string,unknown>){return serial(async()=>{
    const allowed=['expectedRevision','expectedAuthorityEpoch','idempotencyKey',...(action==='save'?['policy','previewDigest']:[])];
    if(Object.keys(input).some(key=>!allowed.includes(key))||typeof input.idempotencyKey!=='string'||!input.idempotencyKey||input.idempotencyKey.length>200)fail('AUTONOMY_INPUT_INVALID');
    const key=`autonomy-user:${input.idempotencyKey}`,receiptId=`autonomy-receipt-${hash(key)}`,digest=hash({action,input});
    const receipt=await store.get(projectId,receiptId);
    if(receipt){if(receipt.data.digest!==digest)fail('AUTONOMY_IDEMPOTENCY_CONFLICT');return {...await snapshot(projectId),pauseTargets:(receipt.data.pauseTargets??[]) as string[]};}
    const {revision,state}=await read(projectId),project=(await store.project(projectId))!;
    if(input.expectedAuthorityEpoch!==project.authorityEpoch)fail('AUTHORITY_EPOCH_CONFLICT');
    if(input.expectedRevision!==revision)fail('AUTONOMY_REVISION_CONFLICT');
    if(action==='save'){
      const checked=await preview(projectId,input.policy,revision);
      if(input.previewDigest!==checked.previewDigest)fail('AUTONOMY_PREVIEW_STALE');
      state.policy=checked.policy;state.paused=true;state.budgetId=randomUUID();state.runs=[];
    }else if(action==='resume'){
      if(!state.policy)fail('AUTONOMY_POLICY_REQUIRED');
      if(!(await preview(projectId,state.policy,revision)).executable)fail('AUTONOMY_SCOPE_UNAVAILABLE');
      if(state.runs.length>=state.policy.maxRuns)fail('AUTONOMY_BUDGET_EXHAUSTED');
      state.paused=false;
    }else if(action==='pause')state.paused=true;
    else fail('AUTONOMY_ACTION_INVALID');
    const pauseTargets=action==='pause'?state.runs.map(run=>run.runId):[];
    return {...await write(projectId,revision,state,key,actorId,action!=='pause',[
      {expectedRevision:0,entity:{id:receiptId,kind:'settings',data:{digest,pauseTargets}}}]),pauseTargets};
  });}
  function reason(state:State,runId:string,action:'execution'|'command'){
    const run=state.runs.find(r=>r.runId===runId);
    if(!state.policy||!run)return 'AUTONOMY_RESERVATION_REQUIRED';
    if(state.paused)return 'AUTONOMY_PAUSED';
    if(run.stopReason)return run.stopReason;
    if(now()>=run.deadlineAt)return 'AUTONOMY_DEADLINE_EXHAUSTED';
    if(!state.policy.allowedActions.includes(action))return 'AUTONOMY_ACTION_FORBIDDEN';
    return null;
  }
  async function assertAllowed(projectId:string,runId:string,action:'execution'|'command'='execution'){
    const {state}=await read(projectId);const denied=reason(state,runId,action);if(denied)fail(denied);
    return structuredClone(state.runs.find(r=>r.runId===runId)!);
  }
  async function reserve(projectId:string,input:{runId:string;bindingId:string;sessionId:string;taskId:string}){return serial(async()=>{
    const {revision,state}=await read(projectId),old=state.runs.find(r=>r.runId===input.runId);
    if(old){if(old.bindingId!==input.bindingId||old.sessionId!==input.sessionId||old.taskId!==input.taskId)fail('AUTONOMY_RESERVATION_CONFLICT');await assertAllowed(projectId,input.runId);return {budgetId:state.budgetId};}
    if(!state.policy)fail('AUTONOMY_POLICY_REQUIRED');if(state.paused)fail('AUTONOMY_PAUSED');
    if(!state.policy.allowedTaskIds.includes(input.taskId))fail('AUTONOMY_TASK_FORBIDDEN');
    if(state.policy.allowedPaths.length!==1||state.policy.allowedPaths[0]!=='.')fail('AUTONOMY_PATH_BOUNDARY_UNAVAILABLE');
    if(state.runs.length>=state.policy.maxRuns)fail('AUTONOMY_BUDGET_EXHAUSTED');
    // Reservations count uncertain dispatches conservatively. A failed send never silently refunds or replays work.
    state.runs.push({...input,startedAt:now(),deadlineAt:now()+state.policy.maxRunSeconds*1000,operationIds:[]});
    await write(projectId,revision,state,`autonomy-reserve:${state.budgetId}:${input.runId}`,undefined,true);
    return {budgetId:state.budgetId};
  });}
  async function reserveCommand(projectId:string,runId:string,operationId:string){return serial(async()=>{
    const {revision,state}=await read(projectId),denied=reason(state,runId,'command');
    if(denied){
      if(denied==='AUTONOMY_ACTION_FORBIDDEN'){
        state.runs.find(run=>run.runId===runId)!.stopReason=denied;
        await write(projectId,revision,state,`autonomy-permission-boundary:${state.budgetId}:${runId}`);
      }
      fail(denied);
    }
    const run=state.runs.find(r=>r.runId===runId)!;
    if(run.operationIds.includes(operationId))return;
    if(run.operationIds.length>=state.policy!.maxCommandsPerRun){
      run.stopReason='AUTONOMY_COMMAND_BUDGET_EXHAUSTED';
      await write(projectId,revision,state,`autonomy-command-limit:${state.budgetId}:${runId}`);
      fail('AUTONOMY_COMMAND_BUDGET_EXHAUSTED');
    }
    run.operationIds.push(operationId);await write(projectId,revision,state,`autonomy-command:${state.budgetId}:${runId}:${operationId}`);
  });}
  async function observedFailure(projectId:string,runId:string){return serial(async()=>{
    const {revision,state}=await read(projectId),run=state.runs.find(r=>r.runId===runId);
    if(run&&state.policy?.stopOnFailedCommand&&!run.stopReason){run.stopReason='AUTONOMY_COMMAND_FAILED';await write(projectId,revision,state,`autonomy-failure:${state.budgetId}:${runId}`);}
  });}
  /** The durable fence is committed before requesting cooperative Stop. Never label request ACK as terminal proof. */
  async function pause(projectId:string,actorId:string,input:Record<string,unknown>,runtime?:Runtime){
    const result=await command(projectId,actorId,'pause',input),interrupts=[];
    // A retried old Pause may only target its original cohort, even after Resume/new admission.
    for(const reservation of result.runs.filter(run=>result.pauseTargets.includes(run.runId))){
      const row=await store.get(projectId,reservation.runId);if(!row||['completed','failed','interrupted'].includes(row.status))continue;
      try {if(!runtime)fail('RUNTIME_UNAVAILABLE');const receipt=await runtime.dispatch('interrupt',{projectId,sessionId:reservation.sessionId,bindingId:reservation.bindingId,runId:reservation.runId});
        interrupts.push({runId:reservation.runId,status:'stop_requested',receipt});}
      catch(error){interrupts.push({runId:reservation.runId,status:'reconciliation_required',reason:(error as {code?:string}).code??'RUNTIME_UNAVAILABLE'});}
    }
    return {...result,interrupts};
  }
  return {snapshot,preview,command,pause,reserve,reserveCommand,assertAllowed,observedFailure};
}
