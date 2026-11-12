import {test} from 'node:test';
import assert from 'node:assert/strict';
import {randomUUID} from 'node:crypto';
import {writeFile} from 'node:fs/promises';
import {join} from 'node:path';
import {m2Fixture} from './m2-fixture.mts';
import {defaultRegistry} from '../../apps/local-service/src/workflows/registry.mts';
import {taskManagerSnapshot} from '../../apps/local-service/src/task-manager/service.mts';
import {createTeamService} from '../../apps/local-service/src/team/service.mts';
import {createAppAgentGateway} from '../../apps/local-service/src/runtime/app-agent-gateway.mts';
import {createRecipeService} from '../../apps/local-service/src/execution-recipes/service.mts';
import {autonomyService} from '../../apps/local-service/src/autonomy-policy/service.mts';
import {defaultAutonomyPolicy} from '../../packages/contracts/autonomy/policy.ts';
import {qualifyGraph} from '../../apps/local-service/src/execution-recipes/contract.mts';
import type {WorkflowRecipe} from '../../packages/contracts/workflows/workflow.ts';
const step=(id:string,extra:Partial<WorkflowRecipe['steps'][number]>={}):WorkflowRecipe['steps'][number]=>({id,role:'builder',profileVersion:'1',skills:[],skillVersions:{},inputArtifacts:[],outputArtifacts:[],checks:[],ownership:[],timeoutSeconds:60,retryBudget:0,iterationBudget:1,...extra});
async function fixture(t:Parameters<typeof m2Fixture>[0],steps=[step('one'),step('two')],maxRuns=20,extraPolicy:Record<string,any>={},targets:Record<string,string>={}){
 const f=await m2Fixture(t),definition=structuredClone(defaultRegistry().workflows[0].versions[0].definition);definition.name='Recipe fixture';definition.recipes=[{id:'recipe',name:'Recipe',steps}];definition.transitions.find(tr=>tr.id==='ready-in_progress')!.recipeId='recipe';Object.assign(definition.transitions.find(tr=>tr.id==='ready-in_progress')!,targets);
 await f.command({action:'workflow-save-draft',workflowId:'recipes',definition,expectedRevision:0});let snap=await taskManagerSnapshot(f.store,'p');const p=await f.command({action:'workflow-publish-preview',workflowId:'recipes',expectedRevision:snap.settingsRevisions.workflows}) as any;
 await f.command({action:'workflow-publish',workflowId:'recipes',expectedRevision:snap.settingsRevisions.workflows,previewDigest:p.previewDigest});snap=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-assign',defaultWorkflowId:'recipes',expectedRevision:snap.settingsRevisions.workflows});
 const task=await f.ready(),team=createTeamService(f.store),preview=await team.preview('p',{proposal:{kind:'agent',action:'create',name:'Builder',description:'Fixture',content:'Pinned fixture role',dependencies:[],reason:'Fixture'},expectedRevision:0});const a=await team.apply('p','local-user',{...preview,expectedRevision:0,epoch:1,idempotencyKey:'role'});
 await f.store.write({projectId:'p',actorId:'test',expectedAuthorityEpoch:1,idempotencyKey:'session',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 const gateway=createAppAgentGateway({store:f.store,profileId:'recipe-test',actorId:'app',executorFactory:async b=>({metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:b.workspaceRoot,mode:b.mode},execute:async()=>({exitCode:0,stdout:'',stderr:''}),interrupt:async()=>{},close:async()=>{}}) as any});
 await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'w',generation:'g'}),auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 const autonomy=autonomyService(f.store),policy={...defaultAutonomyPolicy(),allowedTaskIds:[task.id],maxRuns,...extraPolicy};const policyPreview=await autonomy.preview('p',policy,0);await autonomy.command('p','local-user','save',{expectedRevision:0,expectedAuthorityEpoch:1,idempotencyKey:'policy',policy,previewDigest:policyPreview.previewDigest});await autonomy.command('p','local-user','resume',{expectedRevision:1,expectedAuthorityEpoch:1,idempotencyKey:'resume'});
 let service=createRecipeService({store:f.store,port:gateway.recipeRuntime,automatic:false});f.beforeClose(async()=>{await service.close();await gateway.close();});
 const input={taskId:task.id,transitionId:'ready-in_progress',mode:'recipe',sessionId:'s',roleBindings:{builder:a.assetId},expectedTaskRevision:task.revision,reason:'Fixture recipe'};
 const start=async()=>{const preview=await service.preview('p',input);const request={...input,previewDigest:preview.previewDigest,expectedAuthorityEpoch:1,idempotencyKey:'start'};return {execution:await service.start('p','local-user',request),request};};
 const report=async(status='completed')=>{const claim=await gateway.agent('claim',auth);assert.ok(claim.job);await gateway.agent('report',{...auth,runId:claim.job.runId,seq:1,idempotencyKey:randomUUID(),status,text:'Fixture outcome'});return claim.job;};
 return {...f,task,gateway,auth,autonomy,input,start,report,get service(){return service;},async restart(){await service.close();service=createRecipeService({store:f.store,port:gateway.recipeRuntime,automatic:false});await service.list('p');}};
}
test('recipe sequential attempts keep exact task/pins and start/report replay cannot create runs',async t=>{
 const f=await fixture(t),{execution,request}=await f.start();assert.equal(execution.state,'running');assert.deepEqual(await f.service.start('p','local-user',request),execution);
 await f.service.tick();const first=await f.report();assert.equal(first.assetPins[0].content,'Pinned fixture role');assert.equal(first.workflowSnapshot.executionRecipe.id,'recipe');
 await f.service.tick();await f.service.tick();const second=await f.report();assert.notEqual(first.runId,second.runId);assert.equal(second.taskContext.taskId,f.task.id);
 await f.service.tick();await f.service.tick();assert.equal((await f.service.get('p',execution.id!)).state,'completed');assert.equal((await f.store.get('p',f.task.id))!.status,'in_progress');assert.equal((await f.autonomy.snapshot('p')).usedRuns,2);
});
test('recipe owns task between child runs and rejects public continuation authority',async t=>{
 const f=await fixture(t),{execution}=await f.start();const task=(await f.store.get('p',f.task.id))!;
 await assert.rejects(()=>f.command({action:'transition',taskId:task.id,status:'review',expectedRevision:task.revision,reason:'Interleave'}),{code:'RECIPE_TASK_OWNED'});
 const binding=await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'});
 await assert.rejects(()=>f.gateway.runtime.dispatch('send',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,taskId:task.id,clientMessageId:'external',input:'Continue',recipeExecution:execution.id}),{code:'app_agent_input_invalid'});
 await f.service.command('p',execution.id!,'cancel',{expectedRevision:1,expectedAuthorityEpoch:1,idempotencyKey:'cancel'});await f.service.tick();assert.equal((await f.service.get('p',execution.id!)).state,'cancelled');
});
test('bounded retry uses policy budget and restart cannot replay an attempt',async t=>{
 const f=await fixture(t,[step('one',{retryBudget:1})],2),{execution}=await f.start();await f.service.tick();await f.report('failed');await f.service.tick();await f.service.tick();assert.equal((await f.autonomy.snapshot('p')).usedRuns,2);
 await f.restart();assert.equal((await f.service.get('p',execution.id!)).state,'recovery_required');await f.service.tick();assert.equal((await f.store.list('p',{kind:'run'})).length,2);
});
test('finite self-loop terminates at iteration budget and nested unordered writers are rejected',async t=>{
 const f=await fixture(t,[step('one',{next:['one'],iterationBudget:2})]),{execution}=await f.start();for(let i=0;i<2;i++){await f.service.tick();await f.report();await f.service.tick();}await f.service.tick();assert.equal((await f.service.get('p',execution.id!)).state,'completed');
 assert.throws(()=>qualifyGraph({id:'x',name:'x',steps:[step('root',{next:['a','b']}),step('a',{next:['deep']}),step('b',{next:[],ownership:['SRC']}),step('deep',{next:[],ownership:['src/file.ts']})]}),{code:'WORKFLOW_WRITER_OVERLAP'});
});
test('deep reconvergence waits for every forward parent and executes join once',async t=>{
 const f=await fixture(t,[step('root',{next:['left','right']}),step('left',{next:['end']}),step('right',{next:['deep']}),step('deep',{next:['end']}),step('end',{next:[]})]),{execution}=await f.start(),order=[];
 for(let i=0;i<5;i++){await f.service.tick();const job=await f.report();order.push(JSON.parse(job.input).step.id);await f.service.tick();}
 await f.service.tick();assert.deepEqual(order,['root','left','right','deep','end']);assert.equal((await f.service.get('p',execution.id!)).state,'completed');
 assert.throws(()=>qualifyGraph({id:'x',name:'x',steps:[step('root',{next:['a','b']}),step('a',{next:['end']}),step('b',{next:['end']}),step('end',{join:['a'],next:[]})]}),{code:'RECIPE_JOIN_INCOMPLETE'});
 for(const path of ['src.','src /file','src\u0001'])assert.throws(()=>qualifyGraph({id:'x',name:'x',steps:[step('one',{ownership:[path]})]}),{code:'RECIPE_PATH_INVALID'});
});
test('policy budget exhaustion never dispatches another child or grants a fresh budget',async t=>{
 const f=await fixture(t,[step('one'),step('two')],1),{execution}=await f.start();await f.service.tick();await f.report();await f.service.tick();await f.service.tick();
 const view=await f.service.get('p',execution.id!);assert.equal(view.state,'recovery_required');assert.equal(view.reason,'AUTONOMY_BUDGET_EXHAUSTED');assert.equal((await f.store.list('p',{kind:'run'})).length,1);
 const resolved=await f.service.command('p',execution.id!,'reconcile',{expectedRevision:view.revision,expectedAuthorityEpoch:1,idempotencyKey:'rejected-admission-resolution'});
 assert.equal(resolved.state,'cancelled');assert.equal((await f.store.list('p',{kind:'run'})).length,1);
 const task=(await f.store.get('p',f.task.id))!;await f.command({action:'transition',taskId:task.id,status:'review',expectedRevision:task.revision,reason:'Rejected admission reconciled'});
});
test('pause fences mediated commands before Stop ACK and no interrupted work is replayed',async t=>{
 const f=await fixture(t,[step('one')],2,{allowedActions:['execution','command'],maxCommandsPerRun:2}),{execution}=await f.start();await f.service.tick();const claim=await f.gateway.agent('claim',f.auth),view=await f.service.get('p',execution.id!);
 await f.service.command('p',execution.id!,'pause',{expectedRevision:view.revision,expectedAuthorityEpoch:1,idempotencyKey:'pause'});
 await assert.rejects(()=>f.gateway.agent('command',{...f.auth,runId:claim.job.runId,operationId:'afterpause',argv:['echo','fixture']}));
 await f.gateway.agent('report',{...f.auth,runId:claim.job.runId,seq:1,idempotencyKey:'stop',status:'interrupted',text:'Stopped'});await f.service.tick();assert.equal((await f.store.list('p',{kind:'run'})).length,1);
 const paused=await f.service.get('p',execution.id!);await assert.rejects(()=>f.service.command('p',execution.id!,'resume',{expectedRevision:paused.revision,expectedAuthorityEpoch:1,idempotencyKey:'resume'}),{code:'RECIPE_RECOVERY_REQUIRED'});
});
test('declared check requires observed successful command and terminal target requires owner decision',async t=>{
 const f=await fixture(t,[step('one',{checks:['echo fixture']})]),{execution}=await f.start();await f.service.tick();await f.report();await f.service.tick();assert.equal((await f.service.get('p',execution.id!)).state,'failed');
 const g=await fixture(t,[step('one')],2,{}, {successTarget:'done'}),started=await g.start();await g.service.tick();await g.report();await g.service.tick();await g.service.tick();assert.equal((await g.service.get('p',started.execution.id!)).state,'needs_user_decision');assert.equal((await g.store.get('p',g.task.id))!.status,'in_progress');
});
test('initial artifact hashes bind preview/start and dispatch, public DTO omits private pin bytes',async t=>{
 const f=await fixture(t,[step('one',{inputArtifacts:['input.txt']})]);await writeFile(join(f.root,'input.txt'),'Original');const preview=await f.service.preview('p',f.input);await writeFile(join(f.root,'input.txt'),'Changed');
 await assert.rejects(()=>f.service.start('p','local-user',{...f.input,previewDigest:preview.previewDigest,expectedAuthorityEpoch:1,idempotencyKey:'stale'}),{code:'RECIPE_PREVIEW_STALE'});
 const {execution}=await f.start();await writeFile(join(f.root,'input.txt'),'Changed again');await f.service.tick();const view=await f.service.get('p',execution.id!);assert.equal(view.reason,'RECIPE_ARTIFACT_DRIFT');assert.equal((await f.store.list('p',{kind:'run'})).length,0);assert.equal(JSON.stringify(view).includes('Pinned fixture role'),false);assert.ok(view.steps[0].pins[0].hash);
});
test('observed successful check and real output advance to permitted success target',async t=>{
 const f=await fixture(t,[step('one',{checks:['["echo","fixture"]'],outputArtifacts:['result.txt']})],2,{allowedActions:['execution','command'],maxCommandsPerRun:2},{successTarget:'review'}),{execution}=await f.start();await f.service.tick();const claim=await f.gateway.agent('claim',f.auth),job=claim.job;
 await f.gateway.agent('command',{...f.auth,runId:job.runId,operationId:'check',argv:['echo','fixture']});await f.gateway.runtime.dispatch('approve',{projectId:'p',sessionId:'s',bindingId:job.bindingId,runId:job.runId,generation:'g',requestId:'check',decision:'accept'});
 for(let i=0;i<100;i++){const operation=await f.gateway.agent('operation',{...f.auth,runId:job.runId,operationId:'check'});if(operation.state==='completed')break;await new Promise(r=>setTimeout(r,2));}
 await writeFile(join(f.root,'result.txt'),'Observed fixture output');await f.gateway.agent('report',{...f.auth,runId:job.runId,seq:1,idempotencyKey:'success',status:'completed',text:'Done step'});await f.service.tick();await f.service.tick();const result=await f.service.get('p',execution.id!);assert.equal(result.state,'completed');assert.equal(result.attempts[0].artifacts![0].path,'result.txt');assert.equal((await f.store.get('p',f.task.id))!.status,'review');
});
test('missing output is failed evidence; multi-node bounded cycle does not replay beyond budget',async t=>{
 const f=await fixture(t,[step('one',{outputArtifacts:['absent.txt']})]),{execution}=await f.start();await f.service.tick();await f.report();await f.service.tick();assert.equal((await f.service.get('p',execution.id!)).state,'failed');
 const g=await fixture(t,[step('one',{next:['two'],iterationBudget:2}),step('two',{next:['one'],iterationBudget:2})]),started=await g.start();const order=[];
 for(let i=0;i<4;i++){await g.service.tick();order.push(JSON.parse((await g.report()).input).step.id);await g.service.tick();}await g.service.tick();assert.deepEqual(order,['one','two','one','two']);assert.equal((await g.service.get('p',started.execution.id!)).state,'completed');
});

test('command replay retains requested identity while remaining step timeout shrinks',async t=>{
 const f=await fixture(t,[step('one',{timeoutSeconds:5})],2,{allowedActions:['execution','command'],maxCommandsPerRun:2});await f.start();await f.service.tick();const job=(await f.gateway.agent('claim',f.auth)).job;
 const input={...f.auth,runId:job.runId,operationId:'same',argv:['echo','fixture'],timeoutMs:30000};const first=await f.gateway.agent('command',input);await new Promise(r=>setTimeout(r,25));assert.deepEqual(await f.gateway.agent('command',input),first);assert.equal((await f.autonomy.snapshot('p')).runs[0].operationIds.length,1);
});

test('lost admission acknowledgement is reconciled by observed child identity without replay',async t=>{
 const f=await fixture(t,[step('one')]);await f.service.close();const service=createRecipeService({store:f.store,automatic:false,port:{...f.gateway.recipeRuntime,sendAttempt:async input=>{await f.gateway.recipeRuntime.sendAttempt(input);throw Object.assign(new Error('Lost local acknowledgement'),{code:'FIXTURE_LOST_ACK'});}}});f.beforeClose(()=>service.close());
 const preview=await service.preview('p',f.input),execution=await service.start('p','local-user',{...f.input,previewDigest:preview.previewDigest,expectedAuthorityEpoch:1,idempotencyKey:'lost-start'});await service.tick();const row=(await f.store.list('p',{kind:'run'}))[0],job=row.data.appAgentRun as any;
 const recovered=await service.get('p',execution.id!);assert.equal(recovered.state,'recovery_required');assert.equal(recovered.attempts[0].runId,undefined);
 await assert.rejects(()=>service.command('p',execution.id!,'reconcile',{expectedRevision:recovered.revision,expectedAuthorityEpoch:1,idempotencyKey:'still-active'}),{code:'RECIPE_RECOVERY_UNRESOLVED'});
 await f.gateway.runtime.dispatch('interrupt',{projectId:'p',sessionId:'s',bindingId:job.bindingId,runId:row.id});const resolved=await service.command('p',execution.id!,'reconcile',{expectedRevision:recovered.revision,expectedAuthorityEpoch:1,idempotencyKey:'settled'});
 assert.equal(resolved.state,'cancelled');assert.equal(resolved.attempts[0].runId,row.id);assert.equal((await f.store.list('p',{kind:'run'})).length,1);
});
