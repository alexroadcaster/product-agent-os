import {test} from 'node:test';
import assert from 'node:assert/strict';
import {m2Fixture} from './m2-fixture.mts';
import {createTeamService} from '../../apps/local-service/src/team/service.mts';
import {createAppAgentGateway} from '../../apps/local-service/src/runtime/app-agent-gateway.mts';
const from='1970-01-01T00:00:00.000Z',to='2100-01-01T00:00:00.000Z';

test('interrupted observation remains unknown after gateway recovery instead of inventing elapsed time',async t=>{
 const f=await m2Fixture(t);let now=1000;
 await f.store.write({projectId:'p',actorId:'fixture',idempotencyKey:'session',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 const gateway=createAppAgentGateway({store:f.store,profileId:'partial-metrics',actorId:'fixture',now:()=>now});
 await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'worker',generation:'g'});
 const binding=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'discussion'});
 await gateway.runtime.dispatch('send',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,clientMessageId:'partial',input:'Synthetic'});
 await gateway.agent('claim',{workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken});
 now=9000;await gateway.close();
 const metrics=await createTeamService(f.store).metrics('p',from,to);
 assert.equal(metrics.runs.length,1);assert.equal(metrics.totals.durationSeconds,null);assert.equal(metrics.totals.confirmedMilliseconds,0);assert.equal(metrics.runs[0].duration.unresolvedIntervals,1);assert.equal(metrics.runs[0].status,'recovery_required');
 assert.deepEqual((await createTeamService(f.store).metrics('p',from,to)).totals,metrics.totals);
});

test('discussion run duration is measured from server lifecycle receipts without requiring a task',async t=>{
 const f=await m2Fixture(t);let now=1000;
 await f.store.write({projectId:'p',actorId:'fixture',idempotencyKey:'session',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 const gateway=createAppAgentGateway({store:f.store,profileId:'discussion-metrics',actorId:'fixture',now:()=>now});f.beforeClose(()=>gateway.close());
 await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'worker',generation:'g'}),auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};
 const binding=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'discussion'});
 const run=await gateway.runtime.dispatch('send',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,clientMessageId:'discussion',input:'Synthetic discussion'});
 await gateway.agent('claim',auth);now=3000;await gateway.agent('report',{...auth,runId:run.id,seq:1,idempotencyKey:'done',status:'completed',text:'Done'});
 const metrics=await createTeamService(f.store).metrics('p',from,to);assert.equal(metrics.totals.durationSeconds,2);assert.equal(metrics.runs[0].taskId,null);assert.equal(metrics.runs[0].duration.complete,true);
});

test('observed run metrics exclude approval wait, deduplicate retries and expose only scoped numeric evidence',async t=>{
 const f=await m2Fixture(t),team=createTeamService(f.store);let now=1000;
 const proposal={kind:'agent',action:'create',name:'Fixture agent',description:'Telemetry fixture',content:'model="fixture-model"\nmodel_reasoning_effort="medium"',dependencies:[],reason:'Synthetic fixture'};
 const preview=await team.preview('p',{proposal,expectedRevision:0});
 const asset=await team.apply('p','fixture',{...preview,expectedRevision:0,epoch:1,idempotencyKey:'agent'});
 const task=await f.ready('Measured task',{agentAssignments:[asset.assetId]});
 await f.store.write({projectId:'p',actorId:'fixture',idempotencyKey:'session',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 const gateway=createAppAgentGateway({store:f.store,profileId:'telemetry-fixture',actorId:'fixture-bridge',now:()=>now,executorFactory:async binding=>({metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:binding.workspaceRoot,mode:binding.mode},execute:async()=>({exitCode:0,stdout:'private-output-canary',stderr:''}),interrupt:async()=>{},close:async()=>{}}) as any});
 f.beforeClose(()=>gateway.close());await gateway.connection.connect({});
 const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'worker',generation:'generation'}),auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};
 const binding=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 const run=await gateway.runtime.dispatch('send',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,clientMessageId:'run',input:'private-input-canary',taskId:task.id});
 await gateway.agent('claim',auth);await gateway.agent('claim',auth);
 assert.equal((await team.metrics('p',from,to)).agents[0].durationSeconds,null);
 now=2000;const command={...auth,runId:run.id,operationId:'one-command',argv:['synthetic-command','private-argv-canary']};await gateway.agent('command',command);await gateway.agent('command',command);
 now=3000;await gateway.runtime.dispatch('approve',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,runId:run.id,requestId:'one-command',generation:'generation',decision:'accept'});
 const deadline=Date.now()+3000;while((await gateway.agent('operation',{...auth,runId:run.id,operationId:'one-command'})).state!=='completed'){if(Date.now()>deadline)assert.fail('fixture command did not settle');await new Promise(r=>setTimeout(r,5));}
 now=6000;const report={...auth,runId:run.id,seq:1,idempotencyKey:'finished',status:'completed',text:'private-final-canary'};await gateway.agent('report',report);
 now=9000;await gateway.agent('report',report);
 const metrics=await team.metrics('p',from,to);
 assert.equal(metrics.agents[0].durationSeconds,4);
 assert.equal(metrics.denominator,1);assert.equal(metrics.totals.mediatedCommands.requested,1);assert.equal(metrics.totals.mediatedCommands.completed,1);
 assert.equal(metrics.totals.tokenCount,null);assert.equal(metrics.totals.cost,null);assert.equal(metrics.totals.hostToolCalls,null);
 assert.equal(metrics.runs[0].duration.confirmedMilliseconds,4000);assert.equal(metrics.runs[0].duration.complete,true);
 assert.ok(!JSON.stringify(metrics).includes('private-'));
 assert.equal((await createTeamService(f.store).metrics('p',from,to)).agents[0].durationSeconds,4);
 assert.equal((await (team.metrics as any)('p',from,to,{taskId:'another-task'})).runs.length,0);
 assert.equal((await (team.metrics as any)('p',from,to,{sessionId:'another-session'})).runs.length,0);
 assert.equal((await (team.metrics as any)('p',from,to,{agentId:asset.assetId})).totals.durationSeconds,4);
 await assert.rejects((team.metrics as any)('p',from,to,{agentId:123}),{code:'METRICS_SCOPE_INVALID'});
});
