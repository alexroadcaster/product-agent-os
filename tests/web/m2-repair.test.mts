import assert from 'node:assert/strict';
import { test } from 'node:test';
import { randomUUID } from 'node:crypto';
import { createAppAgentGateway } from '../../apps/local-service/src/runtime/app-agent-gateway.mts';
import { m2Fixture } from './m2-fixture.mts';
import { applyUserCommand,recordManualCheck,acceptTask } from '../../apps/local-service/src/tasks/user-commands.mts';
import { createLocalApplication } from '../../apps/local-service/src/http/application.mts';
import { taskManagerSnapshot,uploadTaskAttachment,downloadTaskAttachment } from '../../apps/local-service/src/task-manager/service.mts';
import { join } from 'node:path';
import { readdir,mkdir } from 'node:fs/promises';
import { startLocalService } from '../../apps/local-service/src/main.mts';
import { openLocalStore,restoreLocalBackup } from '../../apps/local-service/src/storage/local-store.mts';
import { DatabaseSync } from 'node:sqlite';
import { newTask } from '../../apps/web/src/api/task.ts';
import { createDomainTools } from '../../apps/local-service/src/commands/domain-tools.mts';

function legacyTaskProjection(task:Record<string,unknown>){
  const shape=newTask(String(task.projectId),String(task.title),'',[],String(task.id)).data!;
  return {...Object.fromEntries(Object.keys(shape).map(key=>[key,task[key]])),schemaVersion:'m1_task_profile_v1',type:'Task'};
}
async function pairedRepairApplication(f:Awaited<ReturnType<typeof m2Fixture>>){
  const origin='http://127.0.0.1:49829',app=await createLocalApplication({store:f.store,origin,instanceId:'m2-repair',profileDirectory:join(f.root,'repair-profile')});
  let cookie='',csrf='';
  const request=async(path:string,input?:unknown)=>{const response=await app.handleRequest(new Request(`${origin}/api/v1${path}`,{method:input===undefined?'GET':'POST',
    headers:{host:'127.0.0.1:49829',origin,cookie,'x-paos-csrf':csrf,'content-type':'application/json'},...(input===undefined?{}:{body:JSON.stringify(input)})}));
    return {status:response.status,body:await response.json() as any};};
  const response=await app.handleRequest(new Request(`${origin}/bootstrap/exchange`,{method:'POST',headers:{host:'127.0.0.1:49829',origin,'content-type':'application/json'},body:JSON.stringify({code:app.issuePairingCode()})}));
  cookie=response.headers.get('set-cookie')!.split(';')[0];csrf=(await response.json() as any).csrfToken;return request;
}

test('authenticated generic commands cannot downgrade an existing M2 profile or lose its fields',async t=>{
  const f=await m2Fixture(t),task=await f.create('M2 Bug',{type:'bug',components:['DB'],acceptanceCriteria:['Preserve M2']}),request=await pairedRepairApplication(f);
  const before=(await f.store.get('p',task.id))!,events=await f.store.audit('p');
  const response=await request('/projects/p/commands',{expectedAuthorityEpoch:1,idempotencyKey:'downgrade-http',changes:[{expectedRevision:before.revision,entity:{id:task.id,kind:'task',data:{...legacyTaskProjection(before.data),status:'cancelled'}}}]});
  assert.equal(response.status,409);assert.equal(response.body.error.code,'PROFILE_DOWNGRADE_FORBIDDEN');
  assert.deepEqual(await f.store.get('p',task.id),before);assert.deepEqual(await f.store.audit('p'),events);assert.equal(await f.store.receipt('p','downgrade-http'),null);
});

test('the atomic writer rejects M2-to-M1 downgrade before legacy dispatch without revisions or events',async t=>{
  const f=await m2Fixture(t),task=await f.create('M2 Bug',{type:'bug',components:['DB']}),before=(await f.store.get('p',task.id))!,events=await f.store.audit('p');
  for(const schemaVersion of ['m1_task_profile_v1','unrecognized_profile_v1']){
    const idempotencyKey=`downgrade-store-${schemaVersion}`;
    await assert.rejects(()=>f.store.write({projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey,changes:[{expectedRevision:before.revision,
      entity:{id:task.id,kind:'task',data:{...legacyTaskProjection(before.data),schemaVersion,status:'in_progress'}}}]}),{code:'PROFILE_DOWNGRADE_FORBIDDEN'});
    assert.deepEqual(await f.store.get('p',task.id),before);assert.deepEqual(await f.store.audit('p'),events);assert.equal(await f.store.receipt('p',idempotencyKey),null);
  }
});

test('generic and atomic M2 deadline changes require a reason while ordinary title edits remain valid',async t=>{
  const f=await m2Fixture(t),task=await f.create('Task'),request=await pairedRepairApplication(f),before=(await f.store.get('p',task.id))!,events=await f.store.audit('p');
  const change={expectedRevision:before.revision,entity:{id:task.id,kind:'task' as const,data:{...before.data,dueDate:'2026-11-30'}}};
  const response=await request('/projects/p/commands',{expectedAuthorityEpoch:1,idempotencyKey:'deadline-http',changes:[change]});
  assert.equal(response.status,409);assert.equal(response.body.error.code,'DUE_DATE_REASON_REQUIRED');
  await assert.rejects(()=>f.store.write({projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:'deadline-store',changes:[change]}),{code:'DUE_DATE_REASON_REQUIRED'});
  assert.deepEqual(await f.store.get('p',task.id),before);assert.deepEqual(await f.store.audit('p'),events);
  assert.equal((await request('/projects/p/commands',{expectedAuthorityEpoch:1,idempotencyKey:'title-http',changes:[{expectedRevision:before.revision,entity:{id:task.id,kind:'task',data:{...before.data,title:'Valid title'}}}]})).status,200);
  const current=(await f.store.get('p',task.id))!;
  await f.command({action:'save',expectedRevision:current.revision,task:{...current.data,dueDate:'2026-11-30'},reason:'Owner moves the deadline'});
  assert.equal((await f.store.get('p',task.id))!.data.dueDate,'2026-11-30');
});

test('version descriptions are bounded text and survive a later archive update that omits them',async t=>{
  const f=await m2Fixture(t),request=await pairedRepairApplication(f);
  const base={action:'version',expectedAuthorityEpoch:1,expectedRevision:0,item:{id:'v1',name:'1.0',status:'unreleased'}};
  const invalid=await request('/projects/p/task-manager/commands',{...base,idempotencyKey:'description-invalid',item:{...base.item,description:{unexpected:'object'}}});
  assert.equal(invalid.status,400);assert.equal(invalid.body.error.code,'INVALID_VERSION_DESCRIPTION');
  const oversized=await request('/projects/p/task-manager/commands',{...base,idempotencyKey:'description-long',item:{...base.item,description:'x'.repeat(20001)}});assert.equal(oversized.status,400);
  const description='Local release planning notes';
  assert.equal((await request('/projects/p/task-manager/commands',{...base,idempotencyKey:'description-save',item:{...base.item,description}})).status,200);
  assert.equal((await request('/projects/p/task-manager/commands',{...base,idempotencyKey:'description-archive',expectedRevision:1,item:{...base.item,status:'archived'}})).status,200);
  const snapshot=await request('/projects/p/task-manager');assert.equal(snapshot.body.versions[0].description,description);assert.equal(snapshot.body.versions[0].status,'archived');
});

test('an actual soft WIP override is explicit in the durable receipt and public audit',async t=>{
  const f=await m2Fixture(t),a=await f.ready('A'),b=await f.ready('B'),snapshot=await taskManagerSnapshot(f.store,'p');
  await f.command({action:'board',expectedRevision:0,board:{...snapshot.board,columns:snapshot.board.columns.map(c=>c.id==='in_progress'?{...c,wipLimit:1,wipMode:'soft'}:c)}});
  const request=await pairedRepairApplication(f),base={action:'transition',expectedAuthorityEpoch:1,status:'in_progress'};
  const first=await request('/projects/p/task-manager/commands',{...base,idempotencyKey:'soft-first',taskId:a.id,expectedRevision:a.revision,reason:'First task',softWipOverride:true});assert.equal(first.status,200);
  const firstId=first.body.revisions.find((r:any)=>r.id.startsWith('m2-operation-')).id;
  assert.equal((await request(`/projects/p/entities/${firstId}`)).body.data.wipOverride,undefined);
  const rejected=await request('/projects/p/task-manager/commands',{...base,idempotencyKey:'soft-denied',taskId:b.id,expectedRevision:b.revision,reason:'No override'});assert.equal(rejected.body.error.code,'SOFT_WIP_CONFIRMATION_REQUIRED');
  const reason='Owner approves exceeding the soft limit';
  const accepted=await request('/projects/p/task-manager/commands',{...base,idempotencyKey:'soft-override',taskId:b.id,expectedRevision:b.revision,reason,softWipOverride:true});assert.equal(accepted.status,200);
  const id=accepted.body.revisions.find((r:any)=>r.id.startsWith('m2-operation-')).id,expected={override:true,columnId:'in_progress',limit:1,count:1,actorId:'local-user',reason};
  assert.deepEqual((await request(`/projects/p/entities/${id}`)).body.data.wipOverride,expected);
  const history=await request('/projects/p/history'),event=history.body.items.find((event:any)=>event.seq===accepted.body.seq);
  assert.deepEqual(event.payload.managerChanges.find((entry:any)=>entry.id===id).current.wipOverride,expected);
});

test('M2 App execution dispatches once without treating its own queued run as foreign activity',async t=>{
  const f=await m2Fixture(t),task=await f.ready();
  await f.store.write({projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:'session',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
  const gateway=createAppAgentGateway({store:f.store,profileId:'fixture',actorId:'codex-app-agent',executorFactory:async binding=>({
    metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:binding.workspaceRoot,mode:binding.mode,threadId:'fixture',generation:'broker'},
    execute:async()=>({exitCode:0,stdout:'fixture',stderr:''}),interrupt:async()=>{},close:async()=>{},
  }) as any});f.beforeClose(()=>gateway.close());
  await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'fixture-worker',generation:'fixture-generation'});
  const binding=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
  const input={projectId:'p',sessionId:'s',bindingId:binding.bindingId,clientMessageId:randomUUID(),input:'Synthetic execution',taskId:task.id};
  const run=await gateway.runtime.dispatch('send',input);assert.equal(run.state,'queued');
  assert.equal((await gateway.runtime.dispatch('send',input)).id,run.id);
  const saved=(await f.store.get('p',task.id))!;assert.equal(saved.status,'in_progress');assert.equal(saved.data.schemaVersion,'m2_task_profile_v1');
  const auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};await gateway.agent('claim',auth);
  await gateway.agent('report',{...auth,runId:run.id,seq:1,idempotencyKey:'done',status:'completed',text:'Synthetic observed result'});
  assert.equal((await f.store.get('p',task.id))!.status,'in_progress');
  const epic=await f.ready('Epic',{type:'epic'});
  await assert.rejects(()=>gateway.runtime.dispatch('send',{...input,clientMessageId:'epic',taskId:epic.id}),{code:'runtime_epic_not_executable'});
});

test('new pending dependency fences both a new command proposal and acceptance of an older proposal',async t=>{
  const f=await m2Fixture(t),task=await f.ready();let executed=0;
  await f.store.write({projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:'session',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
  const gateway=createAppAgentGateway({store:f.store,profileId:'fixture',actorId:'codex-app-agent',executorFactory:async binding=>({
    metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:binding.workspaceRoot,mode:binding.mode,threadId:'fixture',generation:'broker'},
    execute:async()=>{executed++;return {exitCode:0,stdout:'fixture',stderr:''};},interrupt:async()=>{},close:async()=>{},
  }) as any});f.beforeClose(()=>gateway.close());
  await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'fixture-worker',generation:'fixture-generation'});
  const binding=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'}),scope={projectId:'p',sessionId:'s',bindingId:binding.bindingId};
  const run=await gateway.runtime.dispatch('send',{...scope,clientMessageId:'run',input:'Synthetic',taskId:task.id});
  const auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};await gateway.agent('claim',auth);
  await gateway.agent('command',{...auth,runId:run.id,operationId:'before',argv:['synthetic']});
  const blocker=await f.create('Blocker');await f.command({action:'link',expectedRevision:0,link:{sourceId:blocker.id,targetId:task.id,relation:'blocks',reason:'new prerequisite'}});
  await assert.rejects(()=>gateway.agent('command',{...auth,runId:run.id,operationId:'after',argv:['synthetic']}),{code:'PENDING_LINK_RECONCILIATION_REQUIRED'});
  await assert.rejects(()=>gateway.runtime.dispatch('approve',{...scope,runId:run.id,requestId:'before',generation:worker.generation,decision:'accept'}),{code:'PENDING_LINK_RECONCILIATION_REQUIRED'});
  assert.equal(executed,0);
  await gateway.runtime.dispatch('interrupt',{...scope,runId:run.id});
  await gateway.agent('report',{...auth,runId:run.id,seq:1,idempotencyKey:'stopped',status:'interrupted'});
});

test('raced upload removes only its unreferenced managed blob after revision rejection',async t=>{
  const f=await m2Fixture(t),task=await f.create(),write=f.store.write;let injected=false;
  f.store.write=async command=>{
    if(!injected&&command.changes.some(c=>(c.entity.data as any)?.category==='managed_attachment')){
      injected=true;await write({projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:'raced-task-edit',changes:[{expectedRevision:task.revision,entity:{id:task.id,kind:'task',data:{...task.data,title:'Concurrent title'}}}]});
    }
    return write(command);
  };
  await assert.rejects(()=>uploadTaskAttachment(f.store,'p',task.id,'local-user',{filename:'fixture.txt',mediaType:'text/plain',base64:Buffer.from('fixture').toString('base64'),
    expectedRevision:task.revision,expectedAuthorityEpoch:1,idempotencyKey:'raced-upload'}),{code:'REVISION_CONFLICT'});
  f.store.write=write;assert.deepEqual(await readdir(join(f.root,'state.sqlite.blobs')),[]);
});

test('upload lost ACK cannot remove a referenced blob and original intent remains replayable',async t=>{
  const f=await m2Fixture(t),task=await f.create(),write=f.store.write;let lost=false;
  f.store.write=async command=>{const receipt=await write(command);if(!lost&&command.changes.some(c=>(c.entity.data as any)?.category==='managed_attachment')){lost=true;throw Object.assign(new Error('Synthetic lost ACK'),{code:'FIXTURE_LOST_ACK'});}return receipt;};
  const input={filename:'fixture.txt',mediaType:'text/plain',base64:Buffer.from('committed bytes').toString('base64'),expectedRevision:task.revision,expectedAuthorityEpoch:1,idempotencyKey:'lost-ack'};
  await assert.rejects(()=>uploadTaskAttachment(f.store,'p',task.id,'local-user',input),{code:'FIXTURE_LOST_ACK'});f.store.write=write;
  const receipt=await uploadTaskAttachment(f.store,'p',task.id,'local-user',input);assert.ok(receipt.commandId);
  const attachments=(await taskManagerSnapshot(f.store,'p')).attachments;assert.equal(attachments.length,1);assert.equal(await (await downloadTaskAttachment(f.store,'p',task.id,attachments[0].id)).text(),'committed bytes');
  assert.equal((await readdir(join(f.root,'state.sqlite.blobs'))).length,1);
});

test('actual HTTP upload accepts a bounded file above 1MiB while an ordinary route retains its smaller cap',async t=>{
  const f=await m2Fixture(t),task=await f.create();
  const service=await startLocalService({profileDirectory:join(f.root,'profile'),instanceId:'m2-large-upload'},{openStore:async()=>f.store,sandboxBrokerFactory:false});f.beforeClose(()=>service.quit());
  const origin=`http://127.0.0.1:${service.port}`;
  const paired=await fetch(`${origin}/bootstrap/exchange`,{method:'POST',headers:{origin,'content-type':'application/json'},body:JSON.stringify({code:service.pairingCode})});
  const cookie=paired.headers.get('set-cookie')!.split(';')[0],csrf=(await paired.json() as any).csrfToken;
  const headers={origin,cookie,'content-type':'application/json','x-paos-csrf':csrf},content='Synthetic text fixture\n'.repeat(60000);
  const response=await fetch(`${origin}/api/v1/projects/p/tasks/${task.id}/attachments`,{method:'POST',headers,
    body:JSON.stringify({filename:'large.txt',mediaType:'text/plain',base64:Buffer.from(content).toString('base64'),expectedRevision:task.revision,expectedAuthorityEpoch:1,idempotencyKey:'large-upload'})});
  assert.equal(response.status,200,await response.text());
  const metadata=(await taskManagerSnapshot(f.store,'p')).attachments[0];assert.ok(Number(metadata.data.byteSize)>1024*1024);
  const download=await fetch(`${origin}/api/v1/projects/p/tasks/${task.id}/attachments/${metadata.id}`,{headers});assert.equal(await download.text(),content);
  const oversized=await fetch(`${origin}/api/v1/projects`,{method:'POST',headers,body:JSON.stringify({data:content})});assert.equal(oversized.status,413);
});

test('pending blocking link stops only its pinned original run and a replay cannot stop its successor',async t=>{
  const f=await m2Fixture(t),task=await f.ready(),blocker=await f.create('Blocker');
  await f.store.write({projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:'session',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
  const gateway=createAppAgentGateway({store:f.store,profileId:'fixture',actorId:'codex-app-agent',executorFactory:async binding=>({
    metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:binding.workspaceRoot,mode:binding.mode,threadId:'fixture',generation:'broker'},
    execute:async()=>({exitCode:0,stdout:'fixture',stderr:''}),interrupt:async()=>{},close:async()=>{},
  }) as any});f.beforeClose(()=>gateway.close());
  await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'fixture-worker',generation:'fixture-generation'});
  const binding=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'}),scope={projectId:'p',sessionId:'s',bindingId:binding.bindingId};
  const run=await gateway.runtime.dispatch('send',{...scope,clientMessageId:'one',input:'Synthetic',taskId:task.id});
  const auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};await gateway.agent('claim',auth);
  const origin='http://127.0.0.1:49827',app=await createLocalApplication({store:f.store,origin,instanceId:'m2-stop',profileDirectory:join(f.root,'profile'),runtime:gateway.runtime});
  let cookie='',csrf='';
  const request=async(path:string,input?:unknown)=>{const response=await app.handleRequest(new Request(`${origin}/api/v1${path}`,{method:input===undefined?'GET':'POST',
    headers:{host:'127.0.0.1:49827',origin,cookie,'x-paos-csrf':csrf,'content-type':'application/json'},...(input===undefined?{}:{body:JSON.stringify(input)})}));
    return {status:response.status,body:await response.json() as any,headers:response.headers};};
  const paired=await request('/bootstrap/exchange',{code:app.issuePairingCode()});cookie=paired.headers.get('set-cookie')!.split(';')[0];csrf=paired.body.csrfToken;
  const command={action:'link',idempotencyKey:'first-link',expectedAuthorityEpoch:1,expectedRevision:0,link:{sourceId:blocker.id,targetId:task.id,relation:'blocks',reason:'new prerequisite'}};
  const linked=await request('/projects/p/task-manager/commands',command);assert.equal(linked.status,200,JSON.stringify(linked.body));assert.equal(linked.body.pendingStop.stopRequested,true);assert.equal(linked.body.pendingStop.terminalReceipt,false);
  assert.equal((await gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).state,'cancel_requested');
  const link=(await taskManagerSnapshot(f.store,'p')).links[0];assert.equal(link.blockedRun!.runId,run.id);
  await assert.rejects(()=>f.command({action:'activate-link',expectedRevision:1,linkId:link.id}),{code:'ACTIVE_RUN_RECONCILIATION_REQUIRED'});
  await gateway.agent('report',{...auth,runId:run.id,seq:1,idempotencyKey:'stop-ack',status:'interrupted'});
  const current=(await f.store.get('p',task.id))!;
  await assert.rejects(()=>f.command({action:'transition',taskId:task.id,expectedRevision:current.revision,status:'done',manual:true,reason:'premature',evidence:[{criterion:'Observed fixture',evidence:'manual',outcome:'passed'}]}),{code:'PENDING_LINK_RECONCILIATION_REQUIRED'});
  const stop=await request(`/projects/p/task-manager/links/${link.id}/stop`,{});assert.equal(stop.body.terminalReceipt,true);assert.equal(stop.body.stopRequested,false);
  await f.command({action:'unlink',linkId:link.id,expectedRevision:1,reason:'remove prerequisite'});
  await f.command({action:'transition',taskId:task.id,expectedRevision:current.revision,status:'done',manual:true,reason:'manual',evidence:[{criterion:'Observed fixture',evidence:'manual',outcome:'passed'}]});
  await f.command({action:'transition',taskId:task.id,expectedRevision:current.revision+1,status:'ready',reason:'reopen'});
  const next=await gateway.runtime.dispatch('send',{...scope,clientMessageId:'two',input:'Synthetic successor',taskId:task.id});
  await f.command({action:'link',idempotencyKey:'second-link',expectedRevision:2,link:{sourceId:blocker.id,targetId:task.id,relation:'blocks',reason:'new prerequisite'}});
  const replay=await request('/projects/p/task-manager/commands',command);assert.equal(replay.status,200);assert.equal(replay.body.linkId,link.id);
  const nextState=await gateway.runtime.snapshot({projectId:'p',sessionId:'s'});assert.equal(nextState.runId,next.id);assert.equal(nextState.state,'queued');
  assert.equal((await request(`/projects/p/task-manager/links/${link.id}/stop`,{})).status,404);
});

test('generic user commands cannot bypass structural preview and dedicated save fences an active writer',async t=>{
  const f=await m2Fixture(t),task=await f.create();
  await assert.rejects(()=>applyUserCommand(f.store,{projectId:'p',actorId:'local-user',idempotencyKey:'raw-type',expectedAuthorityEpoch:1,
    changes:[{expectedRevision:task.revision,entity:{id:task.id,kind:'task',data:{...task.data,type:'bug'}}}]}),{code:'PREVIEW_REQUIRED'});
  await f.store.write({projectId:'p',actorId:'runtime',expectedAuthorityEpoch:1,idempotencyKey:'run',changes:[{expectedRevision:0,entity:{id:'run',kind:'run',status:'running',data:{}}}]});
  await assert.rejects(()=>f.command({action:'save',expectedRevision:task.revision,task:{...task.data,title:'Unsafe active edit'}}),{code:'ACTIVE_RUN_RECONCILIATION_REQUIRED'});
});

test('Done task cannot replace its accepted scope or hide server review flags without Reopen',async t=>{
  const f=await m2Fixture(t),task=await f.ready();
  await f.command({action:'transition',taskId:task.id,expectedRevision:task.revision,status:'done',manual:true,reason:'observed',evidence:[{criterion:'Observed fixture',evidence:'manual proof',outcome:'passed'}]});
  const done=(await f.store.get('p',task.id))!;
  await assert.rejects(()=>f.command({action:'save',expectedRevision:done.revision,task:{...done.data,acceptanceCriteria:['New unmet criterion']}}),{code:'REOPEN_REQUIRED'});
  await assert.rejects(()=>f.command({action:'save',expectedRevision:done.revision,task:{...done.data,criteriaEvidence:[]}}),{code:'REOPEN_REQUIRED'});
});

test('catalog dates and board timezone/mappings reject malformed values before persistence',async t=>{
  const f=await m2Fixture(t),board=(await taskManagerSnapshot(f.store,'p')).board;
  await assert.rejects(()=>f.command({action:'version',expectedRevision:0,item:{id:'bad',name:'Bad date',status:'unreleased',releaseDate:'2026-02-30'}}),{code:'INVALID_VERSION_DATES'});
  await assert.rejects(()=>f.command({action:'board',expectedRevision:0,board:{...board,timezone:'Not/A_Timezone'}}),{code:'INVALID_TIMEZONE'});
  await assert.rejects(()=>f.command({action:'board',expectedRevision:0,board:{...board,columns:board.columns.map((c,i)=>i===1?{...c,id:board.columns[0].id}:c)}}),{code:'INVALID_BOARD_MAPPING'});
  assert.equal((await taskManagerSnapshot(f.store,'p')).settingsRevisions.board,0);
});

test('lazy M2 migration stamps truthful archive compatibility while v1 archives still restore',async t=>{
  const f=await m2Fixture(t);await mkdir(join(f.root,'backups'));
  const legacy=await f.store.backup(join(f.root,'backups'));assert.equal(legacy.manifest.schemaVersion,1);assert.equal(legacy.manifest.appCompatibility,'paos-m1-v1');
  await assert.rejects(()=>f.create('Invalid subtask',{type:'sub_task',parentId:randomUUID()}),{code:'PARENT_SCOPE_CONFLICT'});
  assert.equal((await f.store.backup(join(f.root,'backups'))).manifest.schemaVersion,1);
  await f.create();const m2=await f.store.backup(join(f.root,'backups'));
  assert.equal(m2.manifest.schemaVersion,2);assert.equal(m2.manifest.appCompatibility,'paos-m2-v1');assert.notEqual(m2.manifest.migrationChecksum,legacy.manifest.migrationChecksum);
  using snapshot=new DatabaseSync(join(m2.directory,'database.sqlite'),{readOnly:true});
  const chain=snapshot.prepare('SELECT version,checksum FROM schema_migrations ORDER BY version').all();assert.deepEqual(chain.map(row=>row.version),[1,2]);assert.equal(chain[0].checksum,legacy.manifest.migrationChecksum);
  await restoreLocalBackup(legacy.directory,join(f.root,'legacy-restored.sqlite'));
  const restored=await openLocalStore({databasePath:join(f.root,'legacy-restored.sqlite')});try{assert.equal((await restored.projectEntities('p')).length,0);}finally{await restored.close();}
});

test('affects/fix references survive archive and manual Done never publishes the target release',async t=>{
  const f=await m2Fixture(t);
  await f.command({action:'version',expectedRevision:0,item:{id:'v12',name:'1.2',status:'released'}});
  await f.command({action:'version',expectedRevision:1,item:{id:'v13',name:'1.3',status:'unreleased'}});
  const task=await f.create('Bug',{type:'bug',affectsVersions:['v12'],fixVersions:['v13'],acceptanceCriteria:['Fixed']});
  await f.command({action:'version',expectedRevision:2,item:{id:'v12',name:'1.2',status:'archived'}});
  await f.command({action:'transition',taskId:task.id,expectedRevision:1,status:'done',manual:true,reason:'manually checked',evidence:[{criterion:'Fixed',evidence:'observed fix',outcome:'passed'}]});
  const snapshot=await taskManagerSnapshot(f.store,'p'),saved=snapshot.tasks.find(t=>t.id===task.id)!;
  assert.deepEqual(saved.data.affectsVersions,['v12']);assert.deepEqual(saved.data.fixVersions,['v13']);assert.equal(snapshot.versions.find(v=>v.id==='v13')!.status,'unreleased');
});

test('explicit M1 upgrade preserves unknown provenance and legacy links can be removed persistently',async t=>{
  const f=await m2Fixture(t),a=newTask('p','Legacy blocker','',[],randomUUID()),b=newTask('p','Legacy target','',[],randomUUID());
  a.data!.key='PAOS-10';b.data!.key='PAOS-11';a.data!.creator={kind:'imported_unknown',actorId:null};
  b.data!.creator={kind:'imported_unknown',actorId:null};b.data!.links=[{relation:'blocked_by',taskId:a.id,projectId:'p'}];
  await f.store.write({projectId:'p',actorId:'import',expectedAuthorityEpoch:1,idempotencyKey:'legacy',changes:[{expectedRevision:0,entity:a as any},{expectedRevision:0,entity:b as any}]});
  await f.command({action:'upgrade',task:{id:b.id,projectId:'p'},expectedRevision:1});
  const upgraded=(await f.store.get('p',b.id))!;assert.equal(upgraded.data.createdAt,null);assert.deepEqual(upgraded.data.creator,{kind:'imported_unknown',actorId:null});assert.equal(upgraded.publicKey,'PAOS-11');
  const snapshot=await taskManagerSnapshot(f.store,'p');assert.equal(snapshot.links.length,1);assert.equal(snapshot.links[0].sourceId,a.id);assert.equal(snapshot.links[0].targetId,b.id);
  await f.command({action:'unlink',linkId:snapshot.links[0].id,expectedRevision:0,reason:'Remove old prerequisite'});
  assert.deepEqual((await taskManagerSnapshot(f.store,'p')).links,[]);assert.deepEqual((await f.store.get('p',b.id))!.data.links,[]);
});

test('canonical M2 blockers also fence a legacy M1 start and owner acceptance without forcing an upgrade',async t=>{
  const f=await m2Fixture(t),a=await f.create('M2 prerequisite',{acceptanceCriteria:['A verified']}),b=newTask('p','Legacy target','', ['M1 verified'],randomUUID());b.data!.key='PAOS-100';
  await f.store.write({projectId:'p',actorId:'import',expectedAuthorityEpoch:1,idempotencyKey:'legacy-target',changes:[{expectedRevision:0,entity:b as any}]});
  await f.command({action:'link',expectedRevision:0,link:{sourceId:a.id,targetId:b.id,relation:'blocks',reason:'M2 dependency'}});
  await assert.rejects(()=>applyUserCommand(f.store,{projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:'legacy-start',changes:[{expectedRevision:1,entity:{id:b.id,kind:'task',data:{...b.data,status:'in_progress'}}}]}),{code:'DEPENDENCY_BLOCKED'});
  await applyUserCommand(f.store,{projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:'legacy-check-state',changes:[{expectedRevision:1,entity:{id:b.id,kind:'task',data:{...b.data,status:'awaiting_acceptance'}}}]});
  const common={projectId:'p',taskId:b.id,actorId:'local-user',expectedAuthorityEpoch:1,expectedRevision:2,note:'Manual observation'};
  const check=await recordManualCheck(f.store,{...common,idempotencyKey:'legacy-check',outcome:'passed'});
  await assert.rejects(()=>acceptTask(f.store,{...common,idempotencyKey:'legacy-accept',checkId:check.checkId,accepted:true}),{code:'DEPENDENCY_BLOCKED'});
  await f.command({action:'transition',taskId:a.id,expectedRevision:1,status:'done',manual:true,reason:'A verified',evidence:[{criterion:'A verified',evidence:'observed',outcome:'passed'}]});
  await acceptTask(f.store,{...common,idempotencyKey:'legacy-accept',checkId:check.checkId,accepted:true});
  assert.equal((await f.store.get('p',b.id))!.status,'done');assert.equal((await f.store.get('p',b.id))!.data.schemaVersion,'m1_task_profile_v1');
});

test('a mixed legacy agent link is canonical and pins the active M1 writer as pending',async t=>{
  const f=await m2Fixture(t),a=await f.create('M2 prerequisite'),b=newTask('p','M1 execution','', ['M1 criterion'],randomUUID());b.data!.key='PAOS-100';b.data!.status='in_progress';
  await f.store.write({projectId:'p',actorId:'import',expectedAuthorityEpoch:1,idempotencyKey:'legacy-running',changes:[{expectedRevision:0,entity:b as any}]});
  await f.store.write({projectId:'p',actorId:'runtime',expectedAuthorityEpoch:1,idempotencyKey:'legacy-run',changes:[{expectedRevision:0,entity:{id:'legacy-run',kind:'run',status:'running',data:{runtimeRun:{id:'legacy-run',projectId:'p',taskId:b.id,bindingId:'binding',sessionId:'session',generation:'generation'}}}}]});
  const bypass=newTask('p','Legacy edge bypass','',[],randomUUID());bypass.data!.links=[{relation:'blocks',taskId:b.id,projectId:'p'}];
  await assert.rejects(()=>applyUserCommand(f.store,{projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:'raw-legacy-edge',changes:[{expectedRevision:0,entity:bypass as any}]}),{code:'ACTIVE_RUN_RECONCILIATION_REQUIRED'});
  const requested:Array<{projectId:string;linkId:string}>=[],tools=createDomainTools({store:f.store,onPendingLink:async input=>{requested.push(input);}});
  const request={tool:'task_link',requestId:'mixed',binding:{id:'binding',projectId:'p',sessionId:'session',profileId:'builder',threadId:'thread',generation:'generation',mode:'execution'},
    run:{id:'legacy-run',projectId:'p',bindingId:'binding',threadId:'thread',generation:'generation',state:'running',taskId:b.id,scopeDigest:'scope'},
    arguments:{taskId:b.id,toTaskId:a.id,expectedRevision:1,relation:'blocked_by'}} as any;
  await tools.dispatch(request);const link=(await taskManagerSnapshot(f.store,'p')).links[0];assert.equal(link.state,'pending');assert.equal(link.blockedRun?.runId,'legacy-run');assert.equal(requested[0].linkId,link.id);
  assert.deepEqual((await f.store.get('p',b.id))!.data.links,[]);
  const read=await tools.dispatch({...request,tool:'task_read',requestId:'read',arguments:{taskId:b.id}}) as any;assert.equal(read.issueLinks[0].id,link.id);
});

test('generic M2 attachment-to-session and safe comment receipts replay after later state changes',async t=>{
  const f=await m2Fixture(t),task=await f.ready();
  await f.store.write({projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:'session',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
  const attach={projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:'attach',changes:[{expectedRevision:task.revision,entity:{id:task.id,kind:'task' as const,data:{...task.data,sessionIds:['s']}}}]};
  const receipt=await applyUserCommand(f.store,attach);
  await f.command({action:'transition',taskId:task.id,expectedRevision:task.revision+1,status:'in_progress',reason:'start'});
  assert.deepEqual(await applyUserCommand(f.store,attach),receipt);assert.equal((await f.store.get('p',task.id))!.status,'in_progress');
  const comment={projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:'comment',changes:[{expectedRevision:0,entity:{id:'generic-comment',kind:'comment' as const,parentId:task.id,body:'Original',data:{category:'user_comment'}}}]};
  const commentReceipt=await applyUserCommand(f.store,comment);
  await applyUserCommand(f.store,{...comment,idempotencyKey:'comment-edit',changes:[{...comment.changes[0],expectedRevision:1,entity:{...comment.changes[0].entity,body:'Edited'}}]});
  assert.deepEqual(await applyUserCommand(f.store,comment),commentReceipt);assert.equal((await f.store.get('p','generic-comment'))!.body,'Edited');
});

test('manual terminal event preserves first start and leaves unmeasured active duration unknown on reopen',async t=>{
  const f=await m2Fixture(t),task=await f.ready();
  await f.command({action:'transition',taskId:task.id,expectedRevision:task.revision,status:'in_progress',reason:'manual start'});
  const started=(await f.store.get('p',task.id))!;
  await f.command({action:'transition',taskId:task.id,expectedRevision:started.revision,status:'done',manual:true,reason:'observed',evidence:[{criterion:'Observed fixture',evidence:'manual',outcome:'passed'}]});
  const done=(await f.store.get('p',task.id))!,actual=done.data.actual as any;
  assert.ok(actual.startedAt);assert.ok(actual.endedAt);assert.equal(actual.durationSeconds,null);
  await f.command({action:'transition',taskId:task.id,expectedRevision:done.revision,status:'ready',reason:'reopen'});
  const reopened=(await f.store.get('p',task.id))!;assert.equal((reopened.data.actual as any).startedAt,(started.data.actual as any).startedAt);assert.equal((reopened.data.actual as any).endedAt,null);assert.equal(reopened.data.resolution,null);
});

test('manual blocker cannot be bypassed by risk labels and runtime tools use canonical M2 links',async t=>{
  const f=await m2Fixture(t),blocked=await f.ready('Blocked',{blocker:{reason:'Needs owner decision',owner:'local-user',since:new Date().toISOString()},risks:['dependency_review']});
  await assert.rejects(()=>f.command({action:'transition',taskId:blocked.id,expectedRevision:blocked.revision,status:'in_progress',reason:'attempt'}),{code:'BLOCKER_RESOLUTION_REQUIRED'});
  const task=await f.ready('Runtime target'),other=await f.create('Other');
  await f.command({action:'transition',taskId:task.id,expectedRevision:task.revision,status:'in_progress',reason:'start'});
  await f.store.write({projectId:'p',actorId:'runtime',expectedAuthorityEpoch:1,idempotencyKey:'tool-run',changes:[{expectedRevision:0,entity:{id:'run',kind:'run',status:'running',data:{runtimeRun:{id:'run',projectId:'p',taskId:task.id,bindingId:'binding',sessionId:'session',generation:'generation'}}}}]});
  const tools=createDomainTools({store:f.store}),current=(await f.store.get('p',task.id))!;
  const request={binding:{id:'binding',projectId:'p',sessionId:'session',profileId:'builder',threadId:'thread',generation:'generation',mode:'execution'},
    run:{id:'run',projectId:'p',bindingId:'binding',threadId:'thread',generation:'generation',state:'running',taskId:task.id,scopeDigest:'scope'}} as any;
  const args={taskId:task.id,toTaskId:other.id,expectedRevision:current.revision,relation:'blocked_by'};
  const first=await tools.dispatch({...request,tool:'task_link',requestId:'link',arguments:args});assert.deepEqual(await tools.dispatch({...request,tool:'task_link',requestId:'link',arguments:args}),first);
  const links=(await taskManagerSnapshot(f.store,'p')).links;assert.equal(links[0].state,'pending');assert.equal(links[0].blockedRun?.runId,'run');assert.match(links[0].actorId,/^agent:/);
  const updated=(await f.store.get('p',task.id))!;
  await tools.dispatch({...request,tool:'task_patch',requestId:'review',arguments:{taskId:task.id,expectedRevision:updated.revision,patch:{status:'review'}}});
  assert.equal((await f.store.get('p',task.id))!.status,'review');
  await tools.dispatch({...request,tool:'task_comment',requestId:'comment',arguments:{taskId:task.id,body:'Synthetic agent comment'}});
  const comment=(await taskManagerSnapshot(f.store,'p')).comments.find(c=>c.body==='Synthetic agent comment')!;
  assert.equal(comment.data.actorId,'agent:builder:run');assert.equal(comment.data.runId,'run');assert.equal(comment.data.sessionId,'session');assert.ok(comment.data.createdAt);
});
