import assert from 'node:assert/strict';
import {test,type TestContext} from 'node:test';
import {mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {randomUUID} from 'node:crypto';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {createAppAgentGateway} from '../../apps/local-service/src/runtime/app-agent-gateway.mts';

async function setup(t:TestContext){
 const root=await mkdtemp(join(tmpdir(),'paos-app-agent-'));const pin=await bindProject('p',root);
 const store=await openLocalStore({databasePath:join(root,'state.sqlite')});
 t.after(async()=>{await store.close();await rm(root,{recursive:true,force:true});});
 await store.registerProject({id:'p',keyPrefix:'TEST',canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'sql'});
 await store.write({projectId:'p',actorId:'user',idempotencyKey:'session',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 let time=1000;const gateway=createAppAgentGateway({store,profileId:'profile_fixture',actorId:'app-bridge',now:()=>time});
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
 const receipt=await f.gateway.agent('report',report);assert.deepEqual(await f.gateway.agent('report',report),receipt);
 const state=await f.gateway.runtime.snapshot(scope);assert.equal(state.state,'completed');assert.equal(state.runId,undefined);assert.equal(state.canSend,true);
 assert.equal(state.capabilities.nativeSandbox,false);assert.equal(state.capabilities.actualAppServer,false);
 assert.equal('leaseToken' in state,false);assert.equal('leaseToken' in receipt,false);
 assert.equal((await f.gateway.runtime.dispatch('send',f.input)).id,run.id);
 assert.deepEqual((await f.store.list('p',{kind:'message',parentId:'s',order:'newest'})).map(row=>row.body).sort(),[f.input.input,report.text].sort());
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

test('concurrent Send admits one global job and private binding internals never reach browser responses',async(t)=>{
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
