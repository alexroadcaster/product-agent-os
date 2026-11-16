import {test} from 'node:test';
import assert from 'node:assert/strict';
import {m2Fixture} from './m2-fixture.mts';
import {createTeamService} from '../../apps/local-service/src/team/service.mts';
import {createAppAgentGateway} from '../../apps/local-service/src/runtime/app-agent-gateway.mts';
import {createSessionHistory} from '../../apps/local-service/src/sessions/service.mts';

test('configured profile changes do not rewrite pinned model or imply loaded attestation',async t=>{
 const f=await m2Fixture(t),team=createTeamService(f.store);
 const proposal={kind:'agent',action:'create',name:'Evidence agent',description:'Synthetic',content:'model="fixture-a"\nmodel_reasoning_effort="medium"',dependencies:[],reason:'Synthetic'};
 const plan=await team.preview('p',{proposal,expectedRevision:0}),asset=await team.apply('p','fixture',{...plan,epoch:1,expectedRevision:0,idempotencyKey:'agent'});
 const task=await f.ready('Pinned task',{agentAssignments:[asset.assetId]});
 await f.store.write({projectId:'p',actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'session',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 const gateway=createAppAgentGateway({store:f.store,profileId:'host-evidence',actorId:'fixture',now:()=>1000,executorFactory:async binding=>({metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:binding.workspaceRoot,mode:binding.mode},execute:async()=>({exitCode:0,stdout:'',stderr:''}),interrupt:async()=>{},close:async()=>{}}) as any});f.beforeClose(()=>gateway.close());await gateway.connection.connect({});
 await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'fixture-worker',generation:'g'});
 const binding=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 await gateway.runtime.dispatch('send',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,clientMessageId:'run',input:'Synthetic',taskId:task.id});
 const before=await team.profile('p',asset.assetId),update=await team.preview('p',{proposal:{...proposal,assetId:asset.assetId,action:'update',content:'model="fixture-b"\nmodel_reasoning_effort="high"'},expectedRevision:before.revision});
 await team.apply('p','fixture',{...update,epoch:1,expectedRevision:before.revision,idempotencyKey:'update'});
 const current:any=await team.profile('p',asset.assetId);
 assert.equal(current.executionEvidence.configured.model,'fixture-b');assert.equal(current.executionEvidence.configured.effort,'high');
 assert.equal(current.executionEvidence.pinned[0].requestedModel,'fixture-a');assert.equal(current.executionEvidence.pinned[0].requestedEffort,'medium');
 assert.equal(current.executionEvidence.observed,null);assert.equal(current.loadedVersion,null);assert.equal(current.executionEvidence.reason,'selected_route_has_no_loaded_profile_attestation');
});

test('history capability is scoped to the selected local profile and foreign cursors fail closed',async t=>{
 const a=await m2Fixture(t),b=await m2Fixture(t);
 for(const [f,prefix] of [[a,'first'],[b,'second']] as const)for(let i=0;i<2;i++)await f.store.write({projectId:'p',actorId:'fixture',idempotencyKey:prefix+i,expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:prefix+i,kind:'session',title:prefix}}]});
 const ah=createSessionHistory(a.store),bh=createSessionHistory(b.store),page:any=await ah.catalog('p',new URLSearchParams({limit:'1'}));
 assert.equal(page.source.schemaVersion,'paos_history_capability_v1');assert.equal(page.source.projectId,'p');assert.equal(page.source.generation,page.snapshot.generation);
 assert.equal(page.source.localHistory,'available');assert.equal(page.source.hostHistory,'not_connected');assert.equal(page.source.loadedProfiles,'unavailable');
 await assert.rejects(bh.catalog('p',new URLSearchParams({limit:'1',cursor:page.nextCursor})),{code:'CURSOR_STALE'});
 const other=await bh.catalog('p',new URLSearchParams());assert.ok(other.items.every(i=>i.title==='second'));assert.notEqual(other.snapshot.generation,page.snapshot.generation);
});
