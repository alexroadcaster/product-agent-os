import assert from 'node:assert/strict';
import {test,type TestContext} from 'node:test';
import {mkdtemp,rm,writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {randomUUID} from 'node:crypto';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {createAppAgentGateway} from '../../apps/local-service/src/runtime/app-agent-gateway.mts';
import {fixtureTask,runtimeTaskId} from './runtime-adapter-time.fixture.mts';

async function setup(t:TestContext,extra:Record<string,any>={}){
 const root=await mkdtemp(join(tmpdir(),'paos-app-agent-'));const pin=await bindProject('p',root);
 const store=await openLocalStore({databasePath:join(root,'state.sqlite')});
 t.after(async()=>{await store.close();await rm(root,{recursive:true,force:true});});
 await store.registerProject({id:'p',keyPrefix:'TEST',canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'sql'});
 await store.write({projectId:'p',actorId:'user',idempotencyKey:'session',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 let time=1000;const gateway=createAppAgentGateway({store,profileId:'profile_fixture',actorId:'app-bridge',now:()=>time,...extra});
 await gateway.connection.connect({});
 const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'worker',generation:'generation'});
 const binding=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'discussion'});
 const auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};
 const input={projectId:'p',sessionId:'s',bindingId:binding.bindingId,clientMessageId:randomUUID(),input:'Explain only this synthetic request.'};
 return {root,store,gateway,worker,auth,input,advance:(milliseconds:number)=>{time+=milliseconds;}};
}

test('actual App pull lease claims a durable job once and reports a final visible answer idempotently',async(t)=>{
 const f=await setup(t);const run=await f.gateway.runtime.dispatch('send',f.input);
 const scope={projectId:'p',sessionId:'s'};
 assert.equal(run.state,'queued');assert.equal((await f.gateway.runtime.snapshot(scope)).state,'queued');
 const {job}=await f.gateway.agent('claim',f.auth);assert.equal(job.runId,run.id);assert.equal(job.input,f.input.input);
 assert.equal((await f.gateway.agent('claim',f.auth)).job.runId,run.id);
 const report={...f.auth,runId:run.id,seq:1,idempotencyKey:'final',status:'completed',text:'Synthetic App agent result.'};
 await f.gateway.agent('progress',{...f.auth,runId:run.id,seq:1,phase:'final_answer',text:'Synthetic App agent'});
 const receipt=await f.gateway.agent('report',report);assert.deepEqual(await f.gateway.agent('report',report),receipt);
 const state=await f.gateway.runtime.snapshot(scope);assert.equal(state.state,'completed');assert.equal(state.runId,undefined);assert.equal(state.canSend,true);
 assert.equal(state.capabilities.nativeSandbox,false);assert.equal(state.capabilities.actualAppServer,false);
 assert.equal('leaseToken' in state,false);assert.equal('leaseToken' in receipt,false);
 const finalMessage=(await f.store.list('p',{kind:'message',parentId:'s'})).find(row=>row.data.role==='assistant');
 assert.equal(finalMessage?.data.sourceItemId,state.visibleDrafts[0].sourceItemId);
 assert.equal((await f.gateway.runtime.dispatch('send',f.input)).id,run.id);
 assert.deepEqual((await f.store.list('p',{kind:'message',parentId:'s',order:'newest'})).map(row=>row.body).sort(),[f.input.input,report.text].sort());
});

function brokerFactory(execute:(input:any)=>Promise<any>,interrupt:()=>Promise<void>=async()=>{}){return async(binding:any)=>({metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:binding.workspaceRoot,mode:binding.mode,threadId:'fixture-thread',generation:'broker-gen'},execute,interrupt,close:async()=>{}});}

test('App approval expiry during awaited boundary checks never commits or dispatches a grant',async t=>{
 let executed=0;const f=await setup(t,{executorFactory:brokerFactory(async()=>{executed++;return {exitCode:0,stdout:'',stderr:''};})});
 await f.store.write({projectId:'p',actorId:'user',idempotencyKey:'expiry-task',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:runtimeTaskId,kind:'task',data:fixtureTask()}}]});
 const b=await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'}),run=await f.gateway.runtime.dispatch('send',{...f.input,bindingId:b.bindingId,taskId:runtimeTaskId});await f.gateway.agent('claim',f.auth);await f.gateway.agent('command',{...f.auth,runId:run.id,operationId:'expiry',argv:['synthetic']});
 const all=f.store.projectEntities;let crossed=false;f.store.projectEntities=async project=>{const rows=await all(project);if(!crossed){crossed=true;f.advance(300000);}return rows;};
 try{await assert.rejects(()=>f.gateway.runtime.dispatch('approve',{projectId:'p',sessionId:'s',bindingId:b.bindingId,runId:run.id,requestId:'expiry',generation:'generation',decision:'accept'}),{code:'approval_stale'});assert.equal(crossed,true);assert.equal(executed,0);}finally{f.store.projectEntities=all;await f.gateway.close();}
});

test('trusted channel redactor combines with lease redaction before durable broker output, progress and file diffs',async(t)=>{
 const capability='c'.repeat(64);let root='',lease='';
 const f=await setup(t,{redact:(value:string)=>value.replaceAll(capability,'[REDACTED]'),executorFactory:brokerFactory(async()=>{
  await writeFile(join(root,'note.txt'),`after ${capability} ${lease}`);return {exitCode:0,stdout:`output ${capability} ${lease}`,stderr:`diagnostic ${capability}`};
 })});root=f.root;lease=f.worker.leaseToken;await writeFile(join(root,'note.txt'),`before ${capability} ${lease}`);
 await f.store.write({projectId:'p',actorId:'user',idempotencyKey:'redaction-task',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:runtimeTaskId,kind:'task',data:{...fixtureTask(),files:[{relativePath:'note.txt',plannedOperation:'modify',actualOperation:null}]}}}]});
 const binding=await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 const run=await f.gateway.runtime.dispatch('send',{...f.input,bindingId:binding.bindingId,taskId:runtimeTaskId});await f.gateway.agent('claim',f.auth);
 await f.gateway.agent('progress',{...f.auth,runId:run.id,seq:1,phase:'commentary',text:`progress ${capability} ${lease}`});
 await f.gateway.agent('command',{...f.auth,runId:run.id,operationId:'safe',argv:['synthetic','update']});
 await f.gateway.runtime.dispatch('approve',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,runId:run.id,requestId:'safe',generation:'generation',decision:'accept'});
 let state:any;for(let i=0;i<100;i++){state=await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'});if(state.checks.length)break;await new Promise(resolve=>setTimeout(resolve,5));}
 assert.equal(state.fileChanges.length,1);assert.match(state.fileChanges[0].diff,/\[REDACTED\]/);
 for(const secret of [capability,lease])assert.equal(JSON.stringify(state).includes(secret),false);
 await assert.rejects(f.gateway.agent('command',{...f.auth,runId:run.id,operationId:'secret-argument',argv:['echo',capability]}),{code:'app_agent_credential_rejected'});
 await f.gateway.agent('report',{...f.auth,runId:run.id,seq:1,idempotencyKey:'secret-safe-report',status:'completed',text:`final ${capability} ${lease}`});
 const persisted=[await f.store.get('p',run.id),...await f.store.list('p',{kind:'message'})];
 for(const secret of [capability,lease]){assert.equal(JSON.stringify(state).includes(secret),false);assert.equal(JSON.stringify(persisted).includes(secret),false);}
 await f.gateway.close();
});

test('failed new execution binding persistence closes only its newly created broker',async(t)=>{
 const closes=new Map<string,number>();const factory=brokerFactory(async()=>({exitCode:0,stdout:'',stderr:''}));
 const f=await setup(t,{executorFactory:async(binding:any)=>({...await factory(binding),close:async()=>{closes.set(binding.id,(closes.get(binding.id)??0)+1);}})});
 const valid=await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 await f.store.write({projectId:'p',actorId:'user',idempotencyKey:'second-session',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'s2',kind:'session'}}]});
 const original=f.store.write;let rejectedId='';
 f.store.write=async(command)=>{const binding=command.changes.find(change=>change.entity.kind==='settings')?.entity.data?.appAgentBinding as any;
  if(binding?.sessionId==='s2'){rejectedId=binding.id;throw Object.assign(new Error('Synthetic persistence rejection'),{code:'fixture_write_rejected'});}return original(command);};
 await assert.rejects(f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s2',mode:'execution'}),{code:'fixture_write_rejected'});f.store.write=original;
 assert.ok(rejectedId);assert.equal(closes.get(rejectedId),1);assert.equal(closes.get(valid.bindingId)??0,0);
 assert.equal((await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'})).bindingId,valid.bindingId);
 await f.gateway.close();assert.equal(closes.get(rejectedId),1);assert.equal(closes.get(valid.bindingId),1);
});

test('observed task file operations are projected atomically with the command receipt without automatic Done',async(t)=>{
 let root='';const f=await setup(t,{executorFactory:brokerFactory(async()=>{await writeFile(join(root,'added.txt'),'new');await writeFile(join(root,'changed.txt'),'after');await rm(join(root,'removed.txt'));return {exitCode:0,stdout:'done',stderr:''};})});root=f.root;
 await writeFile(join(root,'changed.txt'),'before');await writeFile(join(root,'removed.txt'),'before');
 const files=['added.txt','changed.txt','removed.txt'].map(relativePath=>({relativePath,plannedOperation:null,actualOperation:null}));
 await f.store.write({projectId:'p',actorId:'user',idempotencyKey:'file-task',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:runtimeTaskId,kind:'task',data:{...fixtureTask(),files}}}]});
 const binding=await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 const run=await f.gateway.runtime.dispatch('send',{...f.input,bindingId:binding.bindingId,taskId:runtimeTaskId});await f.gateway.agent('claim',f.auth);
 const writes:any[]=[];const write=f.store.write;f.store.write=async(command)=>{writes.push(command);return write(command);};
 await f.gateway.agent('command',{...f.auth,runId:run.id,operationId:'files',argv:['synthetic','update-files']});
 await f.gateway.runtime.dispatch('approve',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,runId:run.id,requestId:'files',generation:'generation',decision:'accept'});
 for(let i=0;i<100;i++){if((await f.gateway.agent('operation',{...f.auth,runId:run.id,operationId:'files'})).state==='completed')break;await new Promise(resolve=>setTimeout(resolve,5));}
 const task=(await f.store.get('p',runtimeTaskId))!;assert.deepEqual((task.data.files as any[]).map(file=>file.actualOperation),['create','modify','delete']);assert.equal(task.data.status,'in_progress');
 assert.ok(writes.some(command=>command.changes.some((change:any)=>change.entity.id===run.id&&change.entity.data.appAgentRun.operations?.some((op:any)=>op.operationId==='files'&&op.state==='completed'))
  &&command.changes.some((change:any)=>change.entity.id===runtimeTaskId&&change.entity.data.files.every((file:any)=>file.actualOperation!==null))));f.store.write=write;
 await f.gateway.close();
});

test('App execution uses the shared time journal and excludes approval waiting from actual duration',async(t)=>{
 const f=await setup(t,{executorFactory:brokerFactory(async()=>({exitCode:0,stdout:'ok',stderr:''}))});
 await f.store.write({projectId:'p',actorId:'user',idempotencyKey:'time-task',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:runtimeTaskId,kind:'task',data:fixtureTask()}}]});
 const binding=await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 const run=await f.gateway.runtime.dispatch('send',{...f.input,bindingId:binding.bindingId,taskId:runtimeTaskId});await f.gateway.agent('claim',f.auth);
 f.advance(2000);await f.gateway.agent('command',{...f.auth,runId:run.id,operationId:'time',argv:['synthetic']});
 f.advance(10000);await f.gateway.runtime.dispatch('approve',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,runId:run.id,requestId:'time',generation:'generation',decision:'accept'});
 for(let i=0;i<100;i++){if((await f.gateway.agent('operation',{...f.auth,runId:run.id,operationId:'time'})).state==='completed')break;await new Promise(resolve=>setTimeout(resolve,5));}
 f.advance(3000);await f.gateway.agent('report',{...f.auth,runId:run.id,seq:1,idempotencyKey:'timed',status:'completed',text:'Ready for review'});
 const task=(await f.store.get('p',runtimeTaskId))!;assert.deepEqual(task.data.actual,{startedAt:new Date(1000).toISOString(),endedAt:new Date(16000).toISOString(),durationSeconds:5});assert.equal(task.data.status,'in_progress');
 const timeline=(await f.store.get('p',run.id))!.data.timeline as any[];assert.deepEqual(timeline.map(event=>event.kind),['interval_started','interval_stopped','interval_started','interval_stopped']);assert.equal(timeline[1].reason,'pause');assert.equal(timeline[3].reason,'finished');
 await f.gateway.close();
});

test('lease loss marks an open App task interval crashed and leaves actual duration unknown',async(t)=>{
 const f=await setup(t,{executorFactory:brokerFactory(async()=>({exitCode:0,stdout:'',stderr:''}))});
 await f.store.write({projectId:'p',actorId:'user',idempotencyKey:'crash-task',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:runtimeTaskId,kind:'task',data:fixtureTask()}}]});
 const binding=await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 const run=await f.gateway.runtime.dispatch('send',{...f.input,bindingId:binding.bindingId,taskId:runtimeTaskId});await f.gateway.agent('claim',f.auth);f.advance(30001);
 assert.equal((await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).state,'recovery_required');
 const timeline=(await f.store.get('p',run.id))!.data.timeline as any[];assert.deepEqual(timeline.map(event=>event.kind),['interval_started','interval_crashed']);
 const actual=(await f.store.get('p',runtimeTaskId))!.data.actual as any;assert.equal(actual.durationSeconds,null);assert.equal(actual.endedAt,null);assert.equal(actual.startedAt,new Date(1000).toISOString());await f.gateway.close();
});
test('App command approval decline is durable and does not execute; accept dispatches exactly once',async(t)=>{
 let calls=0;const f=await setup(t,{executorFactory:brokerFactory(async()=>{calls++;return {exitCode:0,stdout:'checked',stderr:''};})});
 const run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);
 const command={...f.auth,runId:run.id,operationId:'read-1',argv:['tool','read']};
 const proposed=await f.gateway.agent('command',command);assert.equal(proposed.state,'awaiting_approval');assert.equal(calls,0);
 const approval={projectId:'p',sessionId:'s',bindingId:f.input.bindingId,runId:run.id,requestId:'read-1',generation:'generation',decision:'decline'};
 assert.equal((await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).pendingApprovals[0].source,'paos_domain');
 await f.gateway.runtime.dispatch('approve',approval);assert.equal((await f.gateway.agent('operation',{...f.auth,runId:run.id,operationId:'read-1'})).state,'declined');assert.equal(calls,0);
 await f.gateway.agent('command',{...command,operationId:'read-2'});await f.gateway.runtime.dispatch('approve',{...approval,requestId:'read-2',decision:'accept'});
 await f.gateway.runtime.dispatch('approve',{...approval,requestId:'read-2',decision:'accept'});
 for(let i=0;i<20;i++){const state=await f.gateway.agent('operation',{...f.auth,runId:run.id,operationId:'read-2'});if(state.state==='completed')break;await new Promise(resolve=>setImmediate(resolve));}
 assert.equal(calls,1);assert.equal((await f.gateway.agent('command',{...command,operationId:'read-2'})).stdout,'checked');
});
test('Stop and heartbeat remain responsive during command; interrupted report waits for settled process',async(t)=>{
 let finish!:(result:any)=>void,started!:(value?:unknown)=>void;const start=new Promise(resolve=>{started=resolve;});let stops=0;
 const f=await setup(t,{executorFactory:brokerFactory(async()=>{started();return new Promise(resolve=>{finish=resolve;});},async()=>{stops++;})});
 const run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);
 await f.gateway.agent('command',{...f.auth,runId:run.id,operationId:'slow',argv:['tool','wait']});
 await f.gateway.runtime.dispatch('approve',{projectId:'p',sessionId:'s',bindingId:f.input.bindingId,runId:run.id,requestId:'slow',generation:'generation',decision:'accept'});await start;
 assert.equal((await f.gateway.agent('heartbeat',f.auth)).job.runId,run.id);
 await f.gateway.runtime.dispatch('interrupt',{projectId:'p',sessionId:'s',bindingId:f.input.bindingId,runId:run.id});assert.equal(stops,1);
 const report={...f.auth,runId:run.id,seq:1,idempotencyKey:'stopped',status:'interrupted'};
 await assert.rejects(f.gateway.agent('report',report),{code:'app_agent_operation_pending'});finish({exitCode:130,stdout:'',stderr:'stopped'});
 for(let i=0;i<20;i++){if((await f.gateway.agent('operation',{...f.auth,runId:run.id,operationId:'slow'})).state==='completed')break;await new Promise(resolve=>setImmediate(resolve));}
 assert.equal((await f.gateway.agent('report',report)).state,'interrupted');
});
test('Execution pins saved criteria/files/revision and links task atomically without automatic Done',async(t)=>{
 const f=await setup(t,{executorFactory:brokerFactory(async()=>({exitCode:0,stdout:'ok',stderr:''}))});
 await f.store.write({projectId:'p',actorId:'user',idempotencyKey:'task',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:runtimeTaskId,kind:'task',data:fixtureTask()}}]});
 const before=(await f.store.get('p',runtimeTaskId))!;
 const binding=await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 await assert.rejects(f.gateway.runtime.dispatch('send',{...f.input,bindingId:binding.bindingId}),{code:'app_agent_input_invalid'});
 const sent={...f.input,bindingId:binding.bindingId,taskId:runtimeTaskId};const run=await f.gateway.runtime.dispatch('send',sent);const {job}=await f.gateway.agent('claim',f.auth);
 assert.equal(job.taskContext.revision,before.revision);assert.deepEqual(job.taskContext.acceptanceCriteria,before.data.acceptanceCriteria);assert.deepEqual(job.taskContext.files,before.data.files);
 assert.equal((await f.store.get('p',runtimeTaskId))!.data.status,'in_progress');assert.deepEqual((await f.store.get('p',runtimeTaskId))!.data.sessionIds,['s']);
 assert.equal((await f.gateway.runtime.dispatch('send',sent)).id,run.id);
 await f.gateway.agent('report',{...f.auth,runId:run.id,seq:1,idempotencyKey:'done',status:'completed',text:'Ready for review'});assert.equal((await f.store.get('p',runtimeTaskId))!.data.status,'in_progress');
});
test('unknown command outcome is durable recovery and restart never replays or accepts stale approval',async(t)=>{
 let calls=0;const factory=brokerFactory(async()=>{calls++;throw new Error('private failure');});const f=await setup(t,{executorFactory:factory});
 const run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);
 await f.gateway.agent('command',{...f.auth,runId:run.id,operationId:'lost',argv:['tool','unknown']});const approval={projectId:'p',sessionId:'s',bindingId:f.input.bindingId,runId:run.id,requestId:'lost',generation:'generation',decision:'accept'};
 await f.gateway.runtime.dispatch('approve',approval);for(let i=0;i<20;i++){if((await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).state==='recovery_required')break;await new Promise(resolve=>setImmediate(resolve));}
 await f.gateway.close();const next=createAppAgentGateway({store:f.store,profileId:'profile_fixture',actorId:'restart',executorFactory:factory});await next.connection.connect({});
 const attached=await next.agent('attach',{hostIdentity:'codex_app',workerId:'foreign',generation:'foreign'});
 await assert.rejects(next.runtime.dispatch('approve',approval),{code:'approval_stale'});
 await assert.rejects(next.agent('reconcile',{workerId:attached.workerId,generation:attached.generation,leaseToken:attached.leaseToken,runId:run.id}),{code:'app_agent_generation_mismatch'});
 assert.equal((await next.runtime.snapshot({projectId:'p',sessionId:'s'})).state,'recovery_required');assert.equal(calls,1);await next.close();
});

test('same worker fresh lease can explicitly cancel a restarted never-dispatched approval without executing it',async(t)=>{
 let calls=0;const factory=brokerFactory(async()=>{calls++;return {exitCode:0,stdout:'',stderr:''};});const f=await setup(t,{executorFactory:factory});
 await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'planning'});
 await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'discussion'});
 await f.store.write({projectId:'p',actorId:'user',idempotencyKey:'other-session',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'other',kind:'session'}}]});
 const run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);
 await f.gateway.agent('command',{...f.auth,runId:run.id,operationId:'never-dispatched',argv:['synthetic']});await f.gateway.close();
 // Storage enumeration is not a selection journal: put the active binding first, deterministically.
 const list=f.store.list;f.store.list=async(projectId,options)=>{const rows=await list(projectId,options);return options?.kind==='settings'?rows.sort((a,b)=>Number(b.id===`app-binding-${f.input.bindingId}`)-Number(a.id===`app-binding-${f.input.bindingId}`)):rows;};
 const next=createAppAgentGateway({store:f.store,profileId:'profile_fixture',actorId:'restart',executorFactory:factory});await next.connection.connect({});
 const recovered=await next.runtime.snapshot({projectId:'p',sessionId:'s'});
 assert.equal(recovered.state,'recovery_required');assert.equal(recovered.bindingId,f.input.bindingId);assert.equal(recovered.mode,'discussion');assert.equal(recovered.runId,run.id);
 assert.deepEqual(recovered.pendingApprovals,[]);assert.equal(recovered.recovery?.canCancelUndispatched,false);
 const other=await next.runtime.snapshot({projectId:'p',sessionId:'other'});assert.equal(other.bindingId,undefined);assert.equal(other.runId,undefined);assert.equal(other.recovery,null);
 const current=await next.agent('attach',{hostIdentity:'codex_app',workerId:'worker',generation:'generation'});assert.notEqual(current.leaseToken,f.auth.leaseToken);
 assert.equal((await next.runtime.snapshot({projectId:'p',sessionId:'s'})).recovery?.canCancelUndispatched,true);
 const reconcile={projectId:'p',sessionId:'s',bindingId:f.input.bindingId,runId:run.id};
 assert.equal((await next.runtime.dispatch('reconcile',reconcile)).state,'recovery_required');
 const resolved=await next.runtime.dispatch('reconcile',{...reconcile,resolution:'cancel_undispatched'});assert.equal(resolved.state,'interrupted');assert.equal(resolved.reason,'dispatch_not_observed');
 assert.equal(calls,0);assert.equal((await next.runtime.snapshot({projectId:'p',sessionId:'s'})).canSend,true);
 const saved=(await f.store.get('p',run.id))!.data.appAgentRun as any;assert.equal(saved.operations[0].state,'cancelled');assert.equal(saved.recoveryResolution.reason,'dispatch_not_observed');
 await assert.rejects(next.runtime.dispatch('approve',{...reconcile,requestId:'never-dispatched',generation:'generation',decision:'accept'}),{code:'approval_stale'});
 await assert.rejects(next.agent('heartbeat',f.auth),{code:'app_agent_lease_invalid'});
 assert.equal((await next.runtime.dispatch('send',{...f.input,clientMessageId:'after-recovery'})).state,'queued');await next.close();
});

test('reused mode selection survives restart independently of settings enumeration with no active run',async(t)=>{
 const factory=brokerFactory(async()=>({exitCode:0,stdout:'',stderr:''}));const f=await setup(t,{executorFactory:factory});
 await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'planning'});
 await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'discussion'});
 assert.equal((await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).bindingId,f.input.bindingId);await f.gateway.close();
 const list=f.store.list;f.store.list=async(projectId,options)=>{const rows=await list(projectId,options);return options?.kind==='settings'?rows.sort((a,b)=>Number(b.id===`app-binding-${f.input.bindingId}`)-Number(a.id===`app-binding-${f.input.bindingId}`)):rows;};
 const next=createAppAgentGateway({store:f.store,profileId:'profile_fixture',actorId:'restart',executorFactory:factory});await next.connection.connect({});
 const state=await next.runtime.snapshot({projectId:'p',sessionId:'s'});assert.equal(state.bindingId,f.input.bindingId);assert.equal(state.mode,'discussion');assert.equal(state.runId,undefined);assert.equal(state.recovery,null);
 await next.close();
});

test('an unknown native outcome cannot use cancel-undispatched even with the same worker on a fresh lease',async(t)=>{
 const factory=brokerFactory(async()=>{throw new Error('unknown native outcome');});const f=await setup(t,{executorFactory:factory});
 const run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);await f.gateway.agent('command',{...f.auth,runId:run.id,operationId:'unknown',argv:['synthetic']});
 await f.gateway.runtime.dispatch('approve',{projectId:'p',sessionId:'s',bindingId:f.input.bindingId,runId:run.id,requestId:'unknown',generation:'generation',decision:'accept'});
 for(let i=0;i<100;i++){if((await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).state==='recovery_required')break;await new Promise(resolve=>setTimeout(resolve,5));}await f.gateway.close();
 const next=createAppAgentGateway({store:f.store,profileId:'profile_fixture',actorId:'restart',executorFactory:factory});await next.connection.connect({});await next.agent('attach',{hostIdentity:'codex_app',workerId:'worker',generation:'generation'});
 assert.equal((await next.runtime.snapshot({projectId:'p',sessionId:'s'})).recovery?.canCancelUndispatched,false);
 await assert.rejects(next.runtime.dispatch('reconcile',{projectId:'p',sessionId:'s',bindingId:f.input.bindingId,runId:run.id,resolution:'cancel_undispatched'}),{code:'app_agent_recovery_unresolved'});
 assert.equal((await next.runtime.snapshot({projectId:'p',sessionId:'s'})).state,'recovery_required');await next.close();
});
test('known terminal report is recoverable only by same worker generation on fresh lease',async(t)=>{
 const f=await setup(t);const run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);const receipt=await f.gateway.agent('report',{...f.auth,runId:run.id,seq:1,idempotencyKey:'final',status:'completed',text:'Saved'});
 await f.gateway.connection.disconnect();await f.gateway.connection.connect({});const worker=await f.gateway.agent('attach',{hostIdentity:'codex_app',workerId:'worker',generation:'generation'});
 assert.deepEqual(await f.gateway.agent('reconcile',{workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken,runId:run.id}),receipt);
});
test('approval expires, credential command is rejected, visible progress is bounded and no command runs',async(t)=>{
 let calls=0;const f=await setup(t,{executorFactory:brokerFactory(async()=>{calls++;return {exitCode:0,stdout:'',stderr:''};})});const run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);
 const base={...f.auth,runId:run.id,operationId:'cmd'};await assert.rejects(f.gateway.agent('command',{...base,argv:['tool',f.worker.leaseToken]}),{code:'app_agent_credential_rejected'});
 await assert.rejects(f.gateway.agent('command',{...base,argv:['tool','--api-key','synthetic']}),{code:'app_agent_credential_rejected'});
 await f.gateway.agent('progress',{...f.auth,runId:run.id,seq:1,phase:'commentary',text:'Checking fixture'});assert.equal((await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).visibleDrafts[0].text,'Checking fixture');
 await f.gateway.agent('command',{...base,argv:['tool','read']});await assert.rejects(f.gateway.agent('report',{...f.auth,runId:run.id,seq:1,idempotencyKey:'early',status:'completed',text:'too early'}),{code:'app_agent_operation_pending'});
 for(let i=0;i<11;i++){f.advance(29000);await f.gateway.agent('heartbeat',f.auth);}
 await assert.rejects(f.gateway.runtime.dispatch('approve',{projectId:'p',sessionId:'s',bindingId:f.input.bindingId,runId:run.id,requestId:'cmd',generation:'generation',decision:'accept'}),{code:'approval_conflict'});assert.equal(calls,0);
 assert.equal((await f.gateway.agent('operation',{...f.auth,runId:run.id,operationId:'cmd'})).state,'declined');
});
test('normal discussion does not launch native broker; command parameter conflict never redispatches',async(t)=>{
 let factories=0;const factory=brokerFactory(async()=>({exitCode:0,stdout:'',stderr:''}));const f=await setup(t,{executorFactory:async(binding:any)=>{factories++;return factory(binding);}});
 assert.equal(factories,0);const run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);assert.equal(factories,0);
 const command={...f.auth,runId:run.id,operationId:'once',argv:['tool','read']};await f.gateway.agent('command',command);assert.equal(factories,0);
 await assert.rejects(f.gateway.agent('command',{...command,argv:['tool','write']}),{code:'app_agent_operation_conflict'});
 await f.gateway.runtime.dispatch('interrupt',{projectId:'p',sessionId:'s',bindingId:f.input.bindingId,runId:run.id});assert.equal(factories,0);
 await f.gateway.agent('report',{...f.auth,runId:run.id,seq:1,idempotencyKey:'cancelled',status:'interrupted'});
});
test('broker operation IDs are run scoped even when worker reuses a command label',async(t)=>{
 const ids:string[]=[];const f=await setup(t,{executorFactory:brokerFactory(async(input)=>{ids.push(input.operationId);return {exitCode:0,stdout:'ok',stderr:''};})});
 for(let attempt=0;attempt<2;attempt++){
  const run=await f.gateway.runtime.dispatch('send',{...f.input,clientMessageId:`repeat-${attempt}`});await f.gateway.agent('claim',f.auth);
  await f.gateway.agent('command',{...f.auth,runId:run.id,operationId:'same-label',argv:['tool','read']});
  await f.gateway.runtime.dispatch('approve',{projectId:'p',sessionId:'s',bindingId:f.input.bindingId,runId:run.id,requestId:'same-label',generation:'generation',decision:'accept'});
  for(let i=0;i<20;i++){if((await f.gateway.agent('operation',{...f.auth,runId:run.id,operationId:'same-label'})).state==='completed')break;await new Promise(resolve=>setImmediate(resolve));}
  await f.gateway.agent('report',{...f.auth,runId:run.id,seq:1,idempotencyKey:`result-${attempt}`,status:'completed',text:'ok'});
 }
 assert.equal(ids.length,2);assert.notEqual(ids[0],ids[1]);
});

test('worker lease text is redacted before a final result becomes a public message',async(t)=>{
 const f=await setup(t);const run=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);
 await f.gateway.agent('report',{...f.auth,runId:run.id,seq:1,idempotencyKey:'redaction',status:'completed',text:`Result ${f.worker.leaseToken}`});
 const rows=await f.store.list('p',{kind:'message',parentId:'s'});
 assert.equal(JSON.stringify(rows).includes(f.worker.leaseToken),false);
 assert.equal(rows.some(row=>row.body==='Result [REDACTED]'),true);
});
test('queued Stop cannot be claimed and claimed Stop requires explicit interrupted acknowledgement',async(t)=>{
 const f=await setup(t);const queued=await f.gateway.runtime.dispatch('send',f.input);
 await f.gateway.runtime.dispatch('interrupt',{...f.input,input:undefined,clientMessageId:undefined,runId:queued.id});
 assert.equal((await f.gateway.agent('claim',f.auth)).job,null);
 const next=await f.gateway.runtime.dispatch('send',{...f.input,clientMessageId:randomUUID()});await f.gateway.agent('claim',f.auth);
 await f.gateway.runtime.dispatch('interrupt',{projectId:'p',sessionId:'s',bindingId:f.input.bindingId,runId:next.id});
 assert.equal((await f.gateway.agent('heartbeat',f.auth)).job.cancelRequested,true);
 await assert.rejects(f.gateway.agent('report',{...f.auth,runId:next.id,seq:1,idempotencyKey:'late',status:'completed',text:'late'}),{code:'app_agent_cancel_ack_required'});
 assert.equal((await f.gateway.agent('report',{...f.auth,runId:next.id,seq:1,idempotencyKey:'stop',status:'interrupted'})).state,'interrupted');
});

test('expired or restarted agent leases preserve recovery and never silently requeue jobs',async(t)=>{
 const f=await setup(t);const sent=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);f.advance(30_001);
 assert.equal((await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).state,'recovery_required');
 await assert.rejects(f.gateway.agent('heartbeat',f.auth),{code:'app_agent_lease_invalid'});
 const second=createAppAgentGateway({store:f.store,profileId:'profile_fixture',actorId:'restart'});await second.connection.connect({});
 const attached=await second.agent('attach',{hostIdentity:'codex_app',workerId:'new',generation:'new'});
 assert.equal((await second.agent('claim',{workerId:attached.workerId,generation:attached.generation,leaseToken:attached.leaseToken})).job,null);
 assert.equal((await second.runtime.snapshot({projectId:'p',sessionId:'s'})).runId,sent.id);
 assert.equal((await second.runtime.dispatch('send',f.input)).id,sent.id);
});

test('worker reports fence generation, exact payload, sequence and fields; browser cannot request execution or API auth',async(t)=>{
 const f=await setup(t);
 await assert.rejects(f.gateway.connection.connect({apiKey:'synthetic'}),{code:'app_agent_input_invalid'});
 await assert.rejects(f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'}),{code:'execution_boundary_unverified'});
 const sent=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);
 const report={...f.auth,runId:sent.id,seq:1,idempotencyKey:'report',status:'completed',text:'Safe visible answer'};
 await assert.rejects(f.gateway.agent('report',{...report,hiddenReasoning:'not accepted'}),{code:'app_agent_input_invalid'});
 await assert.rejects(f.gateway.agent('report',{...report,seq:2}),{code:'app_agent_sequence_invalid'});
 await assert.rejects(f.gateway.agent('report',{...report,generation:'foreign'}),{code:'app_agent_lease_invalid'});
 await assert.rejects(f.gateway.agent('report',{...report,leaseToken:'é'.repeat(64)}),{code:'app_agent_lease_invalid'});
 await f.gateway.agent('report',report);
 await assert.rejects(f.gateway.agent('report',{...report,text:'changed'}),{code:'app_agent_report_conflict'});
});

test('concurrent Send admits one job per workspace and private binding internals never reach browser responses',async(t)=>{
 const f=await setup(t);const attempts=await Promise.allSettled([f.gateway.runtime.dispatch('send',f.input),f.gateway.runtime.dispatch('send',{...f.input,clientMessageId:'other'})]);
 assert.equal(attempts.filter(result=>result.status==='fulfilled').length,1);
 const run=(attempts.find(result=>result.status==='fulfilled') as PromiseFulfilledResult<any>).value;
 await f.gateway.runtime.dispatch('interrupt',{projectId:'p',sessionId:'s',bindingId:f.input.bindingId,runId:run.id});
 const binding=await f.gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'discussion',bindingId:f.input.bindingId});
 assert.equal(JSON.stringify(binding).includes(f.root),false);assert.equal('binding' in binding,false);
});

test('an unresolved native route job fences the switched route; close rejects new operations',async(t)=>{
 const f=await setup(t);
 await f.store.write({projectId:'p',actorId:'native',idempotencyKey:'native-unresolved',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'native-run',kind:'run',status:'running',data:{runtimeRun:{id:'native-run'}}}}]});
 const restarted=createAppAgentGateway({store:f.store,profileId:'profile_fixture',actorId:'new-route'});
 await restarted.connection.connect({});await restarted.agent('attach',{hostIdentity:'codex_app',workerId:'new-worker',generation:'new-gen'});
 const state=await restarted.runtime.snapshot({projectId:'p',sessionId:'s'});assert.equal(state.canSend,false);assert.equal(state.reason,'foreign_runtime_recovery_required');
 await assert.rejects(restarted.runtime.dispatch('send',{...f.input,clientMessageId:'new'}),{code:'runtime_busy'});
 const closing=restarted.close();await assert.rejects(restarted.connection.connect({}),{code:'runtime_stopping'});await closing;
});

test('result budget and foreign session fences are enforced before atomic visible result persistence',async(t)=>{
 const f=await setup(t);const sent=await f.gateway.runtime.dispatch('send',f.input);await f.gateway.agent('claim',f.auth);
 const report={...f.auth,runId:sent.id,seq:1,idempotencyKey:'final',status:'completed',text:'x'.repeat(32*1024+1)};
 await assert.rejects(f.gateway.agent('report',report),{code:'app_agent_input_invalid'});
 assert.equal((await f.store.list('p',{kind:'message'})).length,1);
 await assert.rejects(f.gateway.runtime.dispatch('send',{...f.input,sessionId:'foreign'}),{code:'scope_not_found'});
 assert.equal((await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).state,'running');
});
