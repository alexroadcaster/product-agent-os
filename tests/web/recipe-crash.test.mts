import {test} from 'node:test';
import assert from 'node:assert/strict';
import {fork} from 'node:child_process';
import {once} from 'node:events';
import {mkdtemp,rm} from 'node:fs/promises';
import {join,resolve} from 'node:path';
import {tmpdir} from 'node:os';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {createAppAgentGateway} from '../../apps/local-service/src/runtime/app-agent-gateway.mts';
import {createRecipeService} from '../../apps/local-service/src/execution-recipes/service.mts';

for(const phase of ['before-dispatch','after-dispatch'] as const)test(`real fixture process crash ${phase} preserves the admission boundary without replay`,async t=>{
 const scratch=await mkdtemp(join(tmpdir(),'paos-crash-'));let store:any,gateway:any,service:any;
 const child=fork(new URL('./recipe-crash.fixture.mts',import.meta.url),[phase],{execArgv:[],silent:true,env:{SystemRoot:process.env.SystemRoot,TEMP:scratch,TMP:scratch}});
 let stderr='';child.stderr!.on('data',value=>{stderr+=value;});const deadline=setTimeout(()=>child.kill(),15000);deadline.unref();
 t.after(async()=>{clearTimeout(deadline);if(child.exitCode===null&&child.signalCode===null){const close=once(child,'close');child.kill('SIGKILL');await close;}await service?.close();await gateway?.close();await store?.close();const target=resolve(scratch);assert.equal(target.startsWith(resolve(tmpdir())+(process.platform==='win32'?'\\':'/')),true);await rm(target,{recursive:true,force:true});});
 const [message]=await Promise.race([once(child,'message'),once(child,'exit').then(()=>{throw Error('Fixture exited before selected durable boundary: '+stderr);})]);
 const {root,executionId,firstRunId,phase:observedPhase}=message as any;assert.equal(observedPhase,phase);assert.equal(resolve(root).startsWith(resolve(scratch)+(process.platform==='win32'?'\\':'/')),true);
 const close=once(child,'close');assert.equal(child.kill('SIGKILL'),true);await close;clearTimeout(deadline);
 store=await openLocalStore({databasePath:join(root,'state.sqlite')});
 gateway=createAppAgentGateway({store,profileId:'recipe-test',actorId:'app',executorFactory:async(b:any)=>({metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:b.workspaceRoot,mode:b.mode},execute:async()=>({exitCode:0,stdout:'',stderr:''}),interrupt:async()=>{},close:async()=>{}}) as any});
 await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'new-host',generation:'new-generation'}),auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};
 service=createRecipeService({store,port:gateway.recipeRuntime,automatic:false});let checkpoint=await service.get('p',executionId);
 assert.equal(checkpoint.state,'recovery_required');assert.equal((await gateway.agent('claim',auth)).job,null);
 const command=(action:string,key=action)=>service.command('p',executionId,action,{expectedRevision:checkpoint.revision,expectedAuthorityEpoch:1,idempotencyKey:key,reason:'Reviewed process-crash checkpoint'});
 if(phase==='before-dispatch'){
  assert.equal(checkpoint.recovery.checkpoint,'not_dispatched');assert.equal(checkpoint.recovery.canResume,true);assert.equal(checkpoint.attempts.length,0);assert.equal((await store.list('p',{kind:'run'})).length,0);
  await command('resume');await service.tick();const claim=await gateway.agent('claim',auth);assert.ok(claim.job);assert.equal(JSON.parse(claim.job.input).step.id,'one');
  const runId=claim.job.runId;await service.tick();await service.tick();assert.equal((await store.list('p',{kind:'run'})).length,1);assert.equal((await service.get('p',executionId)).attempts[0].runId,runId);
 }else{
  assert.equal(checkpoint.recovery.checkpoint,'unresolved');assert.equal(checkpoint.recovery.canResume,false);assert.equal(checkpoint.recovery.canCancel,false);assert.equal(checkpoint.attempts[0].runId,firstRunId);
  assert.equal((await store.get('p',firstRunId)).status,'recovery_required');
  await assert.rejects(command('resume'),{code:'RECIPE_RECOVERY_REQUIRED'});await assert.rejects(command('reconcile'),{code:'RECIPE_RECOVERY_UNRESOLVED'});
  await command('cancel');await service.tick();checkpoint=await service.get('p',executionId);assert.equal(checkpoint.state,'cancel_requested');assert.equal(checkpoint.recovery.canCancel,false);
  await service.tick();assert.equal((await service.get('p',executionId)).state,'cancel_requested');assert.equal((await gateway.agent('claim',auth)).job,null);
  const runs=await store.list('p',{kind:'run'});assert.equal(runs.length,1);assert.equal(runs[0].id,firstRunId);
 }
});

test('real fixture process crash preserves a terminal checkpoint and resumes only its successor in a new host',async t=>{
 const scratch=await mkdtemp(join(tmpdir(),'paos-crash-'));let store:any,gateway:any,service:any;
 const child=fork(new URL('./recipe-crash.fixture.mts',import.meta.url),[],{execArgv:[],silent:true,env:{SystemRoot:process.env.SystemRoot,TEMP:scratch,TMP:scratch}});
 let stderr='';child.stderr!.on('data',value=>{stderr+=value;});const deadline=setTimeout(()=>child.kill(),15000);deadline.unref();
 t.after(async()=>{clearTimeout(deadline);if(child.exitCode===null&&child.signalCode===null){const close=once(child,'close');child.kill('SIGKILL');await close;}await service?.close();await gateway?.close();await store?.close();assert.equal(resolve(scratch).startsWith(resolve(tmpdir())+(process.platform==='win32'?'\\':'/')),true);await rm(scratch,{recursive:true,force:true});});
 const [message]=await Promise.race([once(child,'message'),once(child,'exit').then(()=>{throw Error('Fixture exited before durable checkpoint: '+stderr);})]);
 const {root,executionId,firstRunId}=message as any;assert.equal(resolve(root).startsWith(resolve(scratch)+ (process.platform==='win32'?'\\':'/')),true);
 const close=once(child,'close');assert.equal(child.kill('SIGKILL'),true);await close;clearTimeout(deadline);
 store=await openLocalStore({databasePath:join(root,'state.sqlite')});
 gateway=createAppAgentGateway({store,profileId:'recipe-test',actorId:'app',executorFactory:async(b:any)=>({metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:b.workspaceRoot,mode:b.mode},execute:async()=>({exitCode:0,stdout:'',stderr:''}),interrupt:async()=>{},close:async()=>{}}) as any});
 await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'new-host',generation:'new-generation'}),auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};
 service=createRecipeService({store,port:gateway.recipeRuntime,automatic:false});const checkpoint=await service.get('p',executionId);
 assert.equal(checkpoint.state,'recovery_required');assert.equal(checkpoint.recovery!.checkpoint,'terminal_result');assert.equal(checkpoint.attempts[0].runId,firstRunId);assert.equal((await store.list('p',{kind:'run'})).length,1);
 await service.command('p',executionId,'resume',{expectedRevision:checkpoint.revision,expectedAuthorityEpoch:1,idempotencyKey:'new-host-resume',reason:'Reviewed persisted terminal checkpoint after process crash'});
 await service.tick();await service.tick();const claim=await gateway.agent('claim',auth);assert.ok(claim.job,JSON.stringify(await service.get('p',executionId)));assert.notEqual(claim.job.runId,firstRunId);assert.equal(JSON.parse(claim.job.input).step.id,'two');
 await gateway.agent('report',{...auth,runId:claim.job.runId,seq:1,idempotencyKey:'new-host-result',status:'completed',text:'Observed successor complete'});await service.tick();await service.tick();assert.equal((await service.get('p',executionId)).state,'completed');assert.equal((await store.list('p',{kind:'run'})).length,2);
});
