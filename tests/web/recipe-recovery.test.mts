import {test} from 'node:test';
import assert from 'node:assert/strict';
import {fixture,step} from './recipe-fixture.mts';
import {createRecipeService} from '../../apps/local-service/src/execution-recipes/service.mts';
import {createScheduler} from '../../apps/local-service/src/scheduler/service.mts';
import {readFile,rename,writeFile} from 'node:fs/promises';
import {join} from 'node:path';
import {setTimeout as delay} from 'node:timers/promises';
import {recipeCheckpoint} from '../../apps/local-service/src/recovery/recipe-checkpoint.mts';

const control=async(f:Awaited<ReturnType<typeof fixture>>,id:string,action:string,key=action)=>f.service.command('p',id,action,{expectedRevision:(await f.service.get('p',id)).revision,expectedAuthorityEpoch:1,idempotencyKey:key,reason:'Reviewed checkpoint recovery'});

async function createdArtifact(t:Parameters<typeof fixture>[0]) {
 const file='proof.txt',calls:string[]=[];
 const f=await fixture(t,[step('build',{outputArtifacts:[file],ownership:[file],checks:['["create"]']}),
  step('review',{inputArtifacts:[file],checks:['["read"]']})],20,{allowedActions:['execution','command'],maxCommandsPerRun:2},{},
 {files:[{relativePath:file,plannedOperation:'create'}],execute:async(root,[action])=>{
  calls.push(action);
  if(action==='create')await writeFile(join(root,file),'fixture output',{flag:'wx'});
  else assert.equal(await readFile(join(root,file),'utf8'),'fixture output');
 }});
 const {execution}=await f.start(),id=execution.id!;
 async function propose(action:string){
  const {job}=await f.gateway.agent('claim',f.auth);
  assert.ok(job);
  const request={...f.auth,runId:job.runId,operationId:action};
  const approval={projectId:'p',sessionId:'s',bindingId:job.bindingId,runId:job.runId,
   requestId:action,generation:f.auth.generation,decision:'accept'};
  assert.equal((await f.gateway.agent('command',{...request,argv:[action]})).state,'awaiting_approval');
  return {job,request,approval};
 }
 async function complete(command:Awaited<ReturnType<typeof propose>>){
  await f.gateway.runtime.dispatch('approve',command.approval);
  for(let attempt=0;attempt<150;attempt++){
   if((await f.gateway.agent('operation',command.request)).state==='completed')break;
   await delay(10);
  }
  assert.equal((await f.gateway.agent('operation',command.request)).exitCode,0);
  await f.gateway.agent('report',{...f.auth,runId:command.job.runId,seq:1,idempotencyKey:'report',
   status:'completed',text:'Observed fixture command'});
 }
 await f.service.tick();
 const first=await propose('create');
 await complete(first);
 await f.restart();
 await control(f,id,'resume');
 return {f,id,file,calls,first,propose,complete};
}

test('resumed recipe reads an observed create output without replaying the producer',async t=>{
 const {f,id,calls,first,propose,complete}=await createdArtifact(t);
 await f.service.tick();
 await f.service.tick();
 const resumed=await f.service.get('p',id);
 assert.equal(resumed.state,'running',resumed.reason??undefined);
 assert.equal(resumed.attempts[0].runId,first.job.runId);
 const review=await propose('read');
 assert.notEqual(review.job.runId,first.job.runId);
 await complete(review);
 await f.service.tick();
 await f.service.tick();
 assert.equal((await f.service.get('p',id)).state,'completed');
 assert.deepEqual(calls,['create','read']);
});

test('resumed recipe rejects same-byte substitution after review command proposal',async t=>{
 const {f,file,calls,propose,id}=await createdArtifact(t);
 await f.service.tick();
 await f.service.tick();
 const resumed=await f.service.get('p',id);
 assert.equal(resumed.state,'running',resumed.reason??undefined);
 const review=await propose('read');
 await rename(join(f.root,file),join(f.root,'former-output.txt'));
 await writeFile(join(f.root,file),'fixture output',{flag:'wx'});
 await assert.rejects(()=>f.gateway.runtime.dispatch('approve',review.approval),{code:'RECIPE_ARTIFACT_DRIFT'});
 assert.deepEqual(calls,['create']);
});

test('resumed recipe cannot adopt a replacement while recording the producer checkpoint',async t=>{
 const {f,id,file,calls,first}=await createdArtifact(t);
 await rename(join(f.root,file),join(f.root,'former-output.txt'));
 await writeFile(join(f.root,file),'fixture output',{flag:'wx'});
 await f.service.tick();
 await f.service.tick();
 const view=await f.service.get('p',id);
 assert.equal(view.state,'recovery_required');
 assert.equal(view.attempts[0].runId,first.job.runId);
 assert.equal(view.attempts[1].admissionRejected,true);
 assert.equal((await f.store.list('p',{kind:'run'})).length,1);
 assert.deepEqual(calls,['create']);
});

test('resumed recipe rechecks the artifact immediately before native review dispatch',async t=>{
 const {f,file,calls,propose}=await createdArtifact(t);
 await f.service.tick();
 await f.service.tick();
 const review=await propose('read');
 const original=f.store.project;
 let replaced=false;
 f.store.project=async projectId=>{
  const project=await original(projectId);
  const row=await f.store.get('p',review.job.runId);
  const operations=row?.data.appAgentRun as {operations?:{state:string}[]}|undefined;
  if(!replaced&&operations?.operations?.some(operation=>operation.state==='dispatching')){
   replaced=true;
   await rename(join(f.root,file),join(f.root,'former-output.txt'));
   await writeFile(join(f.root,file),'fixture output',{flag:'wx'});
  }
  return project;
 };
 try{
  await f.gateway.runtime.dispatch('approve',review.approval);
  for(let attempt=0;attempt<150;attempt++){
   if((await f.gateway.agent('operation',review.request)).state==='cancelled')break;
   await delay(10);
  }
  const outcome=await f.gateway.agent('operation',review.request);
  assert.equal(replaced,true);
  assert.equal(outcome.state,'cancelled');
  assert.equal(outcome.exitCode,130);
  assert.deepEqual(calls,['create']);
 }finally{f.store.project=original;}
});

test('restart after terminal child resumes the same checkpoint, receipt survives restart and next step dispatches once',async t=>{
 const f=await fixture(t),{execution}=await f.start();await f.service.tick();const first=await f.report();await f.restart();
 const view=await f.service.get('p',execution.id!);assert.equal(view.state,'recovery_required');
 const request={expectedRevision:view.revision,expectedAuthorityEpoch:1,idempotencyKey:'resume-checkpoint',reason:'Reviewed saved result'};
 const result=await f.service.command('p',execution.id!,'resume',request);assert.equal(result.state,'running');
 assert.equal(result.attempts[0].runId,first.runId);assert.equal((await f.store.list('p',{kind:'run'})).length,1);
 assert.deepEqual(await f.service.command('p',execution.id!,'resume',request),result);
 await assert.rejects(()=>f.service.command('p',execution.id!,'resume',{...request,reason:'Different decision'}),{code:'IDEMPOTENCY_CONFLICT'});
 await f.restart();assert.deepEqual(await f.service.command('p',execution.id!,'resume',request),result);
 await control(f,execution.id!,'resume','resume-after-restart');await f.service.tick();await f.service.tick();const second=await f.report();assert.notEqual(second.runId,first.runId);
 await f.service.tick();await f.service.tick();assert.equal((await f.service.get('p',execution.id!)).state,'completed');assert.equal((await f.autonomy.snapshot('p')).usedRuns,2);
});

test('restart before first dispatch and between processed steps preserves pins and queue reservation',async t=>{
 const f=await fixture(t);let queue=createScheduler({store:f.store,recipes:f.service,automatic:false});f.beforeClose(()=>queue.close());
 const preview=await queue.preview('p',f.input),entry=await queue.enqueue('p',{...f.input,previewDigest:preview.previewDigest,expectedRevision:preview.queueRevision,expectedAuthorityEpoch:1,idempotencyKey:'enqueue'}) as any;
 await queue.tick();let snapshot=await queue.snapshot('p');const id=snapshot.items.find(e=>e.id===entry.entryId)!.executionId!;
 await queue.close();await f.restart();queue=createScheduler({store:f.store,recipes:f.service,automatic:false});await queue.initialized();assert.equal((await queue.snapshot('p')).items[0].state,'recovery_required');
 const before=await f.service.get('p',id);await control(f,id,'resume');await queue.tick();assert.equal((await queue.snapshot('p')).items[0].state,'running');
 await f.service.tick();await f.report();await f.service.tick();await f.restart();await control(f,id,'resume','between-steps');await f.service.tick();await f.report();await f.service.tick();await f.service.tick();
 const after=await f.service.get('p',id);assert.equal(after.state,'completed');assert.deepEqual(after.steps,before.steps);assert.equal((await f.store.list('p',{kind:'run'})).length,2);
});

test('unknown and interrupted children stay fenced, cancel holds ownership until acknowledged',async t=>{
 const f=await fixture(t,[step('one')]),{execution}=await f.start();await f.service.tick();const job=(await f.gateway.agent('claim',f.auth)).job;await f.restart();
 await assert.rejects(()=>control(f,execution.id!,'resume'),{code:'RECIPE_RECOVERY_REQUIRED'});
 await assert.rejects(()=>control(f,execution.id!,'reconcile'),{code:'RECIPE_RECOVERY_UNRESOLVED'});
 await control(f,execution.id!,'cancel');await f.service.tick();assert.equal((await f.service.get('p',execution.id!)).state,'cancel_requested');
 await assert.rejects(()=>f.gateway.agent('report',{...f.auth,runId:job.runId,seq:1,idempotencyKey:'late-success',status:'completed',text:'Too late'}),{code:'app_agent_cancel_ack_required'});
 await f.gateway.agent('report',{...f.auth,runId:job.runId,seq:1,idempotencyKey:'stop-ack',status:'interrupted',text:'Stopped'});await f.service.tick();assert.equal((await f.service.get('p',execution.id!)).state,'cancelled');assert.equal((await f.store.list('p',{kind:'run'})).length,1);
});

test('lost dispatch acknowledgement can resume only after the durable child has settled',async t=>{
 const f=await fixture(t,[step('one')]);await f.service.close();const service=createRecipeService({store:f.store,automatic:false,port:{...f.gateway.recipeRuntime,sendAttempt:async input=>{await f.gateway.recipeRuntime.sendAttempt(input);await f.gateway.agent('claim',f.auth);throw Object.assign(new Error('Lost ACK'),{code:'LOST_ACK'});}}});f.beforeClose(()=>service.close());
 const p=await service.preview('p',f.input),e=await service.start('p','local-user',{...f.input,previewDigest:p.previewDigest,expectedAuthorityEpoch:1,idempotencyKey:'start-lost'});await service.tick();
 let view=await service.get('p',e.id!);await assert.rejects(()=>service.command('p',e.id!,'resume',{expectedRevision:view.revision,expectedAuthorityEpoch:1,idempotencyKey:'early',reason:'Review'}),{code:'RECIPE_RECOVERY_REQUIRED'});
 const row=(await f.store.list('p',{kind:'run'}))[0],run={runId:row.id};await f.gateway.agent('report',{...f.auth,runId:row.id,seq:1,idempotencyKey:'lost-result',status:'completed',text:'Saved result'});view=await service.get('p',e.id!);await service.command('p',e.id!,'resume',{expectedRevision:view.revision,expectedAuthorityEpoch:1,idempotencyKey:'settled',reason:'Review'});await service.tick();await service.tick();
 assert.equal((await service.get('p',e.id!)).state,'completed');assert.equal((await service.get('p',e.id!)).attempts[0].runId,run.runId);assert.equal((await f.store.list('p',{kind:'run'})).length,1);
});

test('deadline requests Stop, rejects late success and interrupted step cannot be resumed as a new attempt',async t=>{
 const f=await fixture(t,[step('one',{timeoutSeconds:1})]);await f.service.close();let clock=Date.now();const service=createRecipeService({store:f.store,port:f.gateway.recipeRuntime,automatic:false,now:()=>clock});f.beforeClose(()=>service.close());
 const p=await service.preview('p',f.input),e=await service.start('p','local-user',{...f.input,previewDigest:p.previewDigest,expectedAuthorityEpoch:1,idempotencyKey:'deadline-start'});await service.tick();const job=(await f.gateway.agent('claim',f.auth)).job;
 clock=(await service.get('p',e.id!)).attempts[0].deadlineAt;await service.tick();let view=await service.get('p',e.id!);assert.equal(view.state,'paused');assert.equal(view.reason,'RECIPE_STEP_TIMEOUT');assert.equal(view.recovery!.canResume,false);
 await assert.rejects(()=>f.gateway.agent('report',{...f.auth,runId:job.runId,seq:1,idempotencyKey:'late',status:'completed',text:'Late success'}),{code:'app_agent_cancel_ack_required'});
 await f.gateway.agent('report',{...f.auth,runId:job.runId,seq:1,idempotencyKey:'timeout-ack',status:'interrupted',text:'Stopped after deadline'});view=await service.get('p',e.id!);assert.equal(view.recovery!.checkpoint,'interrupted');assert.equal(view.recovery!.canResume,false);
 await service.command('p',e.id!,'cancel',{expectedRevision:view.revision,expectedAuthorityEpoch:1,idempotencyKey:'cancel-timeout'});await service.tick();assert.equal((await service.get('p',e.id!)).state,'cancelled');assert.equal((await f.store.list('p',{kind:'run'})).length,1);
});

test('artifact drift and policy pause block continuation without changing checkpoint identity',async t=>{
 const f=await fixture(t,[step('one',{inputArtifacts:['input.txt']})]);await writeFile(join(f.root,'input.txt'),'original');const {execution}=await f.start();await f.restart();await writeFile(join(f.root,'input.txt'),'changed');
 await assert.rejects(()=>control(f,execution.id!,'resume'),{code:'RECIPE_ARTIFACT_DRIFT'});assert.equal((await f.store.list('p',{kind:'run'})).length,0);
 await writeFile(join(f.root,'input.txt'),'original');const policy=await f.autonomy.snapshot('p');await f.autonomy.command('p','local-user','pause',{expectedRevision:policy.revision,expectedAuthorityEpoch:1,idempotencyKey:'pause-recovery-policy'});
 await assert.rejects(()=>control(f,execution.id!,'resume','paused-policy'),{code:'AUTONOMY_RESERVATION_CONFLICT'});assert.equal((await f.service.get('p',execution.id!)).state,'recovery_required');
});

test('recovery of a failed child consumes the existing bounded retry budget instead of replaying its identity',async t=>{
 const f=await fixture(t,[step('one',{retryBudget:1})],2),{execution}=await f.start();await f.service.tick();const failed=await f.report('failed');await f.restart();await control(f,execution.id!,'resume');await f.service.tick();await f.service.tick();const retried=await f.report();
 assert.notEqual(retried.runId,failed.runId);await f.service.tick();await f.service.tick();const result=await f.service.get('p',execution.id!);assert.equal(result.state,'completed');assert.deepEqual(result.attempts.map(a=>a.try),[0,1]);assert.equal((await f.autonomy.snapshot('p')).usedRuns,2);
});

test('a terminal label cannot conceal unresolved native operations, missing history or a different execution',()=>{
 const e:any={id:'recipe',bindingId:'binding',state:'recovery_required',attempts:[{runId:'run',clientMessageId:'message',state:'dispatched'}]},job={recipeExecution:'recipe',clientMessageId:'message',bindingId:'binding',state:'completed'},child:any={id:'run',status:'completed',data:{appAgentRun:job}};
 assert.equal(recipeCheckpoint(e,child).canResume,true);assert.equal(recipeCheckpoint(e,{...child,data:{appAgentRun:{...job,operations:[{state:'recovery_required'}]}}}).canResume,false);
 assert.equal(recipeCheckpoint(e,{...child,data:{appAgentRun:{...job,recipeExecution:'other'}}}).canCancel,false);
 assert.equal(recipeCheckpoint({...e,attempts:[{...e.attempts[0],state:'completed'}]},null).canResume,false);
});

test('Cancel after a lost admission ACK targets the observed child and still waits for Stop acknowledgement',async t=>{
 const f=await fixture(t,[step('one')]);await f.service.close();let observedRun='';const service=createRecipeService({store:f.store,automatic:false,port:{...f.gateway.recipeRuntime,sendAttempt:async input=>{const run=await f.gateway.recipeRuntime.sendAttempt(input);observedRun=run.id;await f.gateway.agent('claim',f.auth);throw Object.assign(new Error('Lost ACK'),{code:'LOST_ACK'});}}});f.beforeClose(()=>service.close());
 const p=await service.preview('p',f.input),e=await service.start('p','local-user',{...f.input,previewDigest:p.previewDigest,expectedAuthorityEpoch:1,idempotencyKey:'cancel-lost-start'});await service.tick();const view=await service.get('p',e.id!);
 await service.command('p',e.id!,'cancel',{expectedRevision:view.revision,expectedAuthorityEpoch:1,idempotencyKey:'cancel-lost'});
 assert.equal((await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).state,'cancel_requested');assert.equal((await service.get('p',e.id!)).attempts[0].runId,observedRun);
 await service.tick();assert.equal((await service.get('p',e.id!)).state,'cancel_requested');await f.gateway.agent('report',{...f.auth,runId:observedRun,seq:1,idempotencyKey:'cancel-lost-ack',status:'interrupted',text:'Stopped'});await service.tick();assert.equal((await service.get('p',e.id!)).state,'cancelled');assert.equal((await f.store.list('p',{kind:'run'})).length,1);
});
