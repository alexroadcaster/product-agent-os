import assert from 'node:assert/strict';
import {test} from 'node:test';
import {randomUUID} from 'node:crypto';
import {m2Fixture} from './m2-fixture.mts';
import {autonomyService} from '../../apps/local-service/src/autonomy-policy/service.mts';
import {defaultAutonomyPolicy} from '../../packages/contracts/autonomy/policy.ts';
import {createAppAgentGateway} from '../../apps/local-service/src/runtime/app-agent-gateway.mts';
import {createLiveGateway} from '../../apps/local-service/src/runtime/live-gateway.mts';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {join} from 'node:path';

async function setup(t:Parameters<typeof m2Fixture>[0],patch:Record<string,any>={},execute?:()=>Promise<any>){
  const f=await m2Fixture(t);let time=1000,calls=0,stops=0;
  const task=await f.ready(),nextTask=await f.ready('Next task');
  await f.store.write({projectId:'p',actorId:'user',idempotencyKey:'session',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
  const policy=autonomyService(f.store,()=>time);
  const gateway=createAppAgentGateway({store:f.store,profileId:'fixture',actorId:'runtime',now:()=>time,executorFactory:async binding=>({
    metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:binding.workspaceRoot,mode:binding.mode,threadId:'synthetic',generation:'synthetic'},
    execute:async()=>{calls++;return execute?execute():{exitCode:0,stdout:'synthetic',stderr:''};},interrupt:async()=>{stops++;},close:async()=>{}})});
  f.beforeClose(()=>gateway.close());await gateway.connection.connect({});
  const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'fixture-worker',generation:'fixture-generation'});
  const auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};
  const binding=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
  const scope={projectId:'p',sessionId:'s',bindingId:binding.bindingId};
  const configured={...defaultAutonomyPolicy(),allowedTaskIds:[task.id,nextTask.id],allowedActions:['execution','command'],maxCommandsPerRun:2,...patch};
  const mutate=async(action:string,extra={})=>policy.command('p','local-user',action,{expectedAuthorityEpoch:1,expectedRevision:(await policy.snapshot('p')).revision,idempotencyKey:randomUUID(),...extra});
  const preview=await policy.preview('p',configured,0);await mutate('save',{policy:configured,previewDigest:preview.previewDigest});await mutate('resume');
  const input={...scope,clientMessageId:'first',taskId:task.id,input:'Synthetic bounded work',autonomy:true};
  const command=(runId:string,operationId='operation')=>gateway.agent('command',{...auth,runId,operationId,argv:['synthetic']});
  const approve=(runId:string,requestId='operation')=>gateway.runtime.dispatch('approve',{...scope,runId,requestId,generation:auth.generation,decision:'accept'});
  const report=(runId:string,status='interrupted')=>gateway.agent('report',{...auth,runId,seq:1,idempotencyKey:'end',status,text:status==='completed'?'Synthetic result':undefined});
  const settle=async(runId:string,operationId='operation')=>{for(let n=0;n<100;n++){const result=await gateway.agent('operation',{...auth,runId,operationId});if(['completed','cancelled'].includes(result.state))return result;await new Promise(r=>setTimeout(r,5));}assert.fail('operation did not settle');};
  return {...f,managerCommand:f.command,task,nextTask,policy,gateway,scope,auth,input,mutate,command,approve,report,settle,calls:()=>calls,stops:()=>stops,advance:(ms:number)=>{time+=ms;}};
}

test('opt-in run pins a durable budget; replay does not dispatch or charge twice; next run is exhausted',async t=>{
  const f=await setup(t),run=await f.gateway.runtime.dispatch('send',f.input);
  assert.equal(run.state,'queued');assert.equal((await f.policy.snapshot('p')).usedRuns,1);
  assert.equal((await f.gateway.runtime.dispatch('send',f.input)).id,run.id);assert.equal((await f.policy.snapshot('p')).usedRuns,1);
  await f.gateway.agent('claim',f.auth);await f.report(run.id,'completed');
  await assert.rejects(f.gateway.runtime.dispatch('send',{...f.input,taskId:f.nextTask.id,clientMessageId:'second'}),{code:'AUTONOMY_BUDGET_EXHAUSTED'});
});

test('pause fences worker claim and pending command approval while preserving Stop/reconcile',async t=>{
  const f=await setup(t),run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);await f.command(run.id);
  const state=await f.policy.snapshot('p');const paused=await f.policy.pause('p','local-user',{expectedRevision:state.revision,expectedAuthorityEpoch:1,idempotencyKey:'pause'},f.gateway.runtime);
  assert.equal(paused.paused,true);assert.equal(paused.interrupts[0].status,'stop_requested');assert.equal(f.calls(),0);
  await assert.rejects(f.approve(run.id));await assert.rejects(f.command(run.id,'next'));
  assert.equal((await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).state,'cancel_requested');await f.report(run.id);
  assert.equal((await f.gateway.runtime.dispatch('reconcile',f.scope)),null);
  await assert.rejects(f.mutate('resume'),{code:'AUTONOMY_BUDGET_EXHAUSTED'});assert.equal((await f.policy.snapshot('p')).usedRuns,1);
});

test('command approval stays explicit, operation replay charges once, command budget stops further execution',async t=>{
  const f=await setup(t,{maxCommandsPerRun:1}),run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);
  await f.command(run.id);assert.equal(f.calls(),0);await f.command(run.id);assert.equal((await f.policy.snapshot('p')).runs[0].operationIds.length,1);
  await f.approve(run.id);await f.settle(run.id);assert.equal(f.calls(),1);
  await assert.rejects(f.command(run.id,'second'),{code:'AUTONOMY_COMMAND_BUDGET_EXHAUSTED'});assert.equal(f.calls(),1);
});

test('deadline uses current server clock and requests cooperative stop without fabricating terminal success',async t=>{
  const f=await setup(t,{maxRunSeconds:1}),run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);
  f.advance(1001);const state=await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'});assert.equal(state.state,'cancel_requested');
  await assert.rejects(f.command(run.id));assert.equal(f.calls(),0);assert.equal((await f.store.get('p',run.id))!.status,'cancel_requested');
  await f.report(run.id);assert.equal((await f.store.get('p',run.id))!.status,'interrupted');
});

test('current pause before claim cancels an undispatched run and retains its reserved budget',async t=>{
  const f=await setup(t),run=await f.gateway.runtime.dispatch('send',f.input);
  await f.mutate('pause');assert.equal((await f.gateway.agent('claim',f.auth)).job,null);
  assert.equal((await f.store.get('p',run.id))!.status,'interrupted');
  const stored=await f.store.get('p','autonomy-policy');assert.equal(stored!.data.paused,true);assert.equal((stored!.data.runs as any[]).length,1);
});

test('policy task scope and failed command stop rule use saved task and observed exit status',async t=>{
  const f=await setup(t,{},async()=>({exitCode:2,stdout:'',stderr:'Synthetic failure'}));
  const other=await f.ready('Other');await assert.rejects(f.gateway.runtime.dispatch('send',{...f.input,taskId:other.id}),{code:'AUTONOMY_TASK_FORBIDDEN'});
  const run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);await f.command(run.id);await f.approve(run.id);await f.settle(run.id);
  assert.equal((await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).state,'cancel_requested');
  assert.equal((await f.policy.snapshot('p')).runs[0].stopReason,'AUTONOMY_COMMAND_FAILED');await f.report(run.id);
});

test('retrying an old Pause never interrupts a run admitted after Resume',async t=>{
  const f=await setup(t,{maxRuns:3}),first=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);
  const pauseInput={expectedRevision:(await f.policy.snapshot('p')).revision,expectedAuthorityEpoch:1,idempotencyKey:'original-pause'};
  await f.policy.pause('p','local-user',pauseInput,f.gateway.runtime);await f.report(first.id);await f.mutate('resume');
  const second=await f.gateway.runtime.dispatch('send',{...f.input,taskId:f.nextTask.id,clientMessageId:'later-run'});await f.gateway.agent('claim',f.auth);
  const replay=await f.policy.pause('p','local-user',pauseInput,f.gateway.runtime);
  assert.equal(replay.paused,false);assert.equal(replay.interrupts.length,0);
  assert.equal((await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).state,'running');
  await f.report(second.id,'completed');
});

test('real SQLite close/reopen retains pause and budget and restores an unresolved run without replay',async t=>{
  const f=await setup(t,{maxRuns:2}),run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);
  await f.mutate('pause');await f.gateway.close();await f.store.close();
  const reopened=await openLocalStore({databasePath:join(f.root,'state.sqlite')});let gateway:ReturnType<typeof createAppAgentGateway>|undefined;
  try{
    const policy=autonomyService(reopened),state=await policy.snapshot('p');assert.equal(state.paused,true);assert.equal(state.usedRuns,1);
    gateway=createAppAgentGateway({store:reopened,profileId:'fixture',actorId:'runtime'});
    await gateway.connection.connect({});const snapshot=await gateway.runtime.snapshot({projectId:'p',sessionId:'s'});
    assert.equal(snapshot.state,'recovery_required');assert.equal(snapshot.runId,run.id);assert.equal(snapshot.canSend,false);
    assert.equal((await reopened.list('p',{kind:'run'})).length,1);assert.equal(f.calls(),0);
  }finally{await gateway?.close();await reopened.close();}
});

test('two concurrent reservations cannot spend the last run budget twice',async t=>{
  const f=await setup(t),results=await Promise.allSettled(['one','two'].map(runId=>f.policy.reserve('p',{runId,bindingId:f.scope.bindingId,sessionId:'s',taskId:f.task.id})));
  assert.equal(results.filter(result=>result.status==='fulfilled').length,1);
  assert.equal((results.find(result=>result.status==='rejected') as PromiseRejectedResult).reason.code,'AUTONOMY_BUDGET_EXHAUSTED');
  assert.equal((await f.policy.snapshot('p')).usedRuns,1);
});

test('watchdog requests deadline Stop without browser polling or worker heartbeat',async t=>{
  const f=await setup(t,{maxRunSeconds:1}),run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);f.advance(1001);
  const end=Date.now()+2000;let saved;
  do{saved=await f.store.get('p',run.id);if(saved?.status==='cancel_requested')break;await new Promise(r=>setTimeout(r,30));}while(Date.now()<end);
  assert.equal(saved?.status,'cancel_requested');assert.equal((saved?.data.appAgentRun as any).autonomyStopReason,'AUTONOMY_DEADLINE_EXHAUSTED');
});

test('a command outside preauthorized actions stops its managed run at the permission boundary',async t=>{
  const f=await setup(t,{allowedActions:['execution'],maxCommandsPerRun:0}),run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);
  await assert.rejects(f.command(run.id),{code:'AUTONOMY_ACTION_FORBIDDEN'});
  assert.equal((await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).state,'cancel_requested');assert.equal(f.calls(),0);
});

test('legacy API route refuses opt-in before opening RPC and never falls back silently',async()=>{
  let processes=0;const gateway=createLiveGateway({store:{} as any,profileId:'synthetic',actorId:'test',rpcFactory:async()=>{processes++;throw Error('must not open');}});
  await assert.rejects(gateway.runtime.dispatch('send',{autonomy:true}),{code:'AUTONOMY_ROUTE_UNAVAILABLE'});
  assert.equal(processes,0);await gateway.close();
});
