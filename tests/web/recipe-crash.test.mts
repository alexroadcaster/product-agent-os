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

test('real fixture process crash preserves a terminal checkpoint and resumes only its successor in a new host',async t=>{
 const scratch=await mkdtemp(join(tmpdir(),'paos-crash-'));let store:any,gateway:any,service:any;
 const child=fork(new URL('./recipe-crash.fixture.mts',import.meta.url),[],{execArgv:[],silent:true,env:{SystemRoot:process.env.SystemRoot,TEMP:scratch,TMP:scratch}});
 let stderr='';child.stderr!.on('data',value=>{stderr+=value;});const deadline=setTimeout(()=>child.kill(),15000);deadline.unref();
 t.after(async()=>{clearTimeout(deadline);if(child.exitCode===null&&child.signalCode===null){const exit=once(child,'exit');child.kill();await exit;}await service?.close();await gateway?.close();await store?.close();await rm(scratch,{recursive:true,force:true});});
 const [message]=await Promise.race([once(child,'message'),once(child,'exit').then(()=>{throw Error('Fixture exited before durable checkpoint: '+stderr);})]);
 const {root,executionId,firstRunId}=message as any;assert.equal(resolve(root).startsWith(resolve(scratch)+ (process.platform==='win32'?'\\':'/')),true);
 const exit=once(child,'exit');assert.equal(child.kill('SIGKILL'),true);await exit;clearTimeout(deadline);
 store=await openLocalStore({databasePath:join(root,'state.sqlite')});
 gateway=createAppAgentGateway({store,profileId:'recipe-test',actorId:'app',executorFactory:async(b:any)=>({metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:b.workspaceRoot,mode:b.mode},execute:async()=>({exitCode:0,stdout:'',stderr:''}),interrupt:async()=>{},close:async()=>{}}) as any});
 await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'new-host',generation:'new-generation'}),auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};
 service=createRecipeService({store,port:gateway.recipeRuntime,automatic:false});const checkpoint=await service.get('p',executionId);
 assert.equal(checkpoint.state,'recovery_required');assert.equal(checkpoint.recovery!.checkpoint,'terminal_result');assert.equal(checkpoint.attempts[0].runId,firstRunId);assert.equal((await store.list('p',{kind:'run'})).length,1);
 await service.command('p',executionId,'resume',{expectedRevision:checkpoint.revision,expectedAuthorityEpoch:1,idempotencyKey:'new-host-resume',reason:'Reviewed persisted terminal checkpoint after process crash'});
 await service.tick();await service.tick();const claim=await gateway.agent('claim',auth);assert.ok(claim.job,JSON.stringify(await service.get('p',executionId)));assert.notEqual(claim.job.runId,firstRunId);assert.equal(JSON.parse(claim.job.input).step.id,'two');
 await gateway.agent('report',{...auth,runId:claim.job.runId,seq:1,idempotencyKey:'new-host-result',status:'completed',text:'Observed successor complete'});await service.tick();await service.tick();assert.equal((await service.get('p',executionId)).state,'completed');assert.equal((await store.list('p',{kind:'run'})).length,2);
});
