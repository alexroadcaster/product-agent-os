import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtemp,mkdir,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {createAppAgentGateway} from '../../apps/local-service/src/runtime/app-agent-gateway.mts';
import {fixtureTask,runtimeTaskId} from './runtime-adapter-time.fixture.mts';

test('independent workspace commands overlap while nested roots and cross-scope controls remain fenced',async t=>{
 const root=await mkdtemp(join(tmpdir(),'paos-parallel-'));
 const store=await openLocalStore({databasePath:join(root,'state.sqlite')});
 let release!:()=>void;const barrier=new Promise<void>(resolve=>{release=resolve;});const entered:string[]=[];
 const gateway=createAppAgentGateway({store,profileId:'parallel',actorId:'fixture',executorFactory:async binding=>({metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:binding.workspaceRoot,mode:binding.mode,threadId:'fixture',generation:'fixture'},execute:async()=>{entered.push(binding.projectId);await barrier;return {exitCode:0,stdout:'ok',stderr:''};},interrupt:async()=>{release();},close:async()=>{release();}})});
 t.after(async()=>{release();await gateway.close();await store.close();await rm(root,{recursive:true,force:true});});
 await gateway.connection.connect({});const lease=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'worker',generation:'generation'});
 const auth={workerId:lease.workerId,generation:lease.generation,leaseToken:lease.leaseToken};const scopes:Record<string,any>={};
 for(const [id,path] of [['a','a'],['b','b'],['nested','a/nested']]){
  await mkdir(join(root,path),{recursive:true});const pin=await bindProject(id,join(root,path));
  await store.registerProject({id,keyPrefix:({a:'AAAA',b:'BBBB',nested:'CCCC'} as any)[id],canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'sql'});
  await store.write({projectId:id,actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'setup',changes:[{expectedRevision:0,entity:{id:'session',kind:'session'}},{expectedRevision:0,entity:{id:runtimeTaskId,kind:'task',data:{...fixtureTask(id),key:({a:'AAAA-1',b:'BBBB-1',nested:'CCCC-1'} as any)[id]}}}]});
  const binding=await gateway.runtime.dispatch('bindings',{projectId:id,sessionId:'session',mode:'execution'});scopes[id]={projectId:id,sessionId:'session',bindingId:binding.bindingId};
 }
 const a=await gateway.runtime.dispatch('send',{...scopes.a,taskId:runtimeTaskId,clientMessageId:'a',input:'Synthetic A'});
 const b=await gateway.runtime.dispatch('send',{...scopes.b,taskId:runtimeTaskId,clientMessageId:'b',input:'Synthetic B'});
 assert.equal((await gateway.agent('claim',auth)).job.runId,a.id);assert.equal((await gateway.agent('claim',auth)).job.runId,b.id);
 assert.equal((await gateway.agent('claim',{...auth,runId:a.id})).job.runId,a.id);
 assert.deepEqual((await gateway.agent('heartbeat',auth)).jobs.map((job:any)=>job.runId).sort(),[a.id,b.id].sort());
 assert.equal((await gateway.recipeRuntime.prepareBinding('a','session')).bindingId,scopes.a.bindingId);
 await assert.rejects(gateway.runtime.dispatch('send',{...scopes.nested,taskId:runtimeTaskId,clientMessageId:'nested',input:'Synthetic nested'}),{code:'runtime_busy'});
 await assert.rejects(gateway.runtime.dispatch('interrupt',{...scopes.a,runId:b.id}),{code:'run_not_interruptible'});
 for(const [id,run] of [['a',a],['b',b]] as const){await gateway.agent('command',{...auth,runId:run.id,operationId:'operation',argv:['synthetic']});await gateway.runtime.dispatch('approve',{...scopes[id],runId:run.id,requestId:'operation',generation:'generation',decision:'accept'});}
 for(let n=0;n<100&&entered.length<2;n++)await new Promise(resolve=>setTimeout(resolve,5));
 assert.deepEqual(entered.sort(),['a','b']);release();
 for(const run of [a,b]){for(let n=0;n<100;n++){if((await gateway.agent('operation',{...auth,runId:run.id,operationId:'operation'})).state==='completed')break;await new Promise(resolve=>setTimeout(resolve,5));}await gateway.agent('report',{...auth,runId:run.id,seq:1,idempotencyKey:'done',status:'completed',text:'Synthetic done'});}
 assert.equal((await gateway.runtime.snapshot({projectId:'a',sessionId:'session'})).canSend,true);
});

test('workspace capacity and lease expiry cover every owner, and restart never reclaims unresolved work',async t=>{
 const root=await mkdtemp(join(tmpdir(),'paos-parallel-recovery-'));const store=await openLocalStore({databasePath:join(root,'state.sqlite')});let now=1000;
 let gateway=createAppAgentGateway({store,profileId:'parallel',actorId:'fixture',now:()=>now});
 t.after(async()=>{await gateway.close();await store.close();await rm(root,{recursive:true,force:true});});
 await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'worker',generation:'generation'});
 const auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken},scopes:any[]=[];
 for(let n=0;n<5;n++){
  const id=`project-${n}`;await mkdir(join(root,id));const pin=await bindProject(id,join(root,id));
  await store.registerProject({id,keyPrefix:['AAAA','BBBB','CCCC','DDDD','EEEE'][n],canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'sql'});
  await store.write({projectId:id,actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'setup',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
  const binding=await gateway.runtime.dispatch('bindings',{projectId:id,sessionId:'s',mode:'discussion'});scopes.push({projectId:id,sessionId:'s',bindingId:binding.bindingId});
 }
 const runs:any[]=[];for(const scope of scopes.slice(0,4))runs.push(await gateway.runtime.dispatch('send',{...scope,clientMessageId:'send',input:'Synthetic'}));
 await assert.rejects(gateway.runtime.dispatch('send',{...scopes[4],clientMessageId:'send',input:'Synthetic'}),{code:'runtime_busy'});
 for(const run of runs)assert.equal((await gateway.agent('claim',{...auth,runId:run.id})).job.runId,run.id);
 now+=30001;
 for(const scope of scopes.slice(0,4))assert.equal((await gateway.runtime.snapshot({projectId:scope.projectId,sessionId:'s'})).state,'recovery_required');
 await gateway.close();gateway=createAppAgentGateway({store,profileId:'parallel',actorId:'fixture',now:()=>now});
 await gateway.connection.connect({});const next=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'worker',generation:'generation'});
 assert.equal((await gateway.agent('claim',{workerId:next.workerId,generation:next.generation,leaseToken:next.leaseToken})).job,null);
 for(const scope of scopes.slice(0,4))assert.equal((await gateway.runtime.snapshot({projectId:scope.projectId,sessionId:'s'})).state,'recovery_required');
});



