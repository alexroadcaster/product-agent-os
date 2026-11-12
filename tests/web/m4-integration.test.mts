import test from 'node:test';
import assert from 'node:assert/strict';
import {randomUUID} from 'node:crypto';
import {m2Fixture} from './m2-fixture.mts';
import {createAppAgentGateway} from '../../apps/local-service/src/runtime/app-agent-gateway.mts';
import {taskManagerSnapshot,uploadTaskAttachment,downloadTaskAttachment} from '../../apps/local-service/src/task-manager/service.mts';
import {defaultRegistry} from '../../apps/local-service/src/workflows/registry.mts';
import {createLocalApplication} from '../../apps/local-service/src/http/application.mts';
import {join} from 'node:path';

test('SC14-02: owner-authorized App Bug creation binds creator/initiator, retries once and preserves author on edit',async t=>{
 const f=await m2Fixture(t),task=await f.ready();
 await f.store.write({projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:'session',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 const gateway=createAppAgentGateway({store:f.store,profileId:'fixture',actorId:'app-runtime',executorFactory:async b=>({metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:b.workspaceRoot,mode:b.mode},close:async()=>{},interrupt:async()=>{}} as any)});f.beforeClose(()=>gateway.close());
 await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'worker',generation:'generation'}),auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};
 const binding=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 const run=await gateway.runtime.dispatch('send',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,taskId:task.id,clientMessageId:randomUUID(),input:'Create a Bug for the observed defect; no target writes.',taskCreationApproved:true,taskCreationInitiator:'local-user'});await gateway.agent('claim',auth);
 const request={...auth,runId:run.id,operationId:'observed-bug',title:'Observed Bug',summary:'Synthetic defect',acceptanceCriteria:['Regression passes']};
 const receipt=await gateway.agent('task-create',request);await new Promise(resolve=>setTimeout(resolve,10));assert.deepEqual(await gateway.agent('task-create',request),receipt);
 const bug=(await f.store.get('p',receipt.taskId))!;assert.equal(bug.data.type,'bug');assert.equal(bug.status,'backlog');assert.deepEqual(bug.data.creator,{kind:'agent',actorId:`agent:fixture:${run.id}`});assert.equal(bug.data.initiatedBy,'local-user');
 assert.equal((await f.store.list('p',{kind:'task'})).length,2);
 await assert.rejects(gateway.agent('task-create',{...request,title:'Changed request'}),{code:'IDEMPOTENCY_CONFLICT'});
 await assert.rejects(gateway.agent('task-create',{...request,operationId:'forged',creator:{kind:'user',actorId:'forged'}}),{code:'app_agent_input_invalid'});
 await gateway.agent('report',{...auth,runId:run.id,seq:1,idempotencyKey:'done',status:'completed',text:'Bug recorded; no execution.'});
 await f.command({action:'save',task:{...bug.data,title:'Owner edited title',priority:'high'},expectedRevision:bug.revision});const edited=(await f.store.get('p',bug.id))!;assert.deepEqual(edited.data.creator,bug.data.creator);assert.equal(edited.data.initiatedBy,bug.data.initiatedBy);
 const history=(await f.store.audit('p')).items;
 assert.ok(history.some((e:any)=>e.actorId==='local-user'&&e.occurredAt&&e.payload.taskChanges?.some((c:any)=>c.id===bug.id&&c.fields.some((v:any)=>v.field==='priority'&&v.previous==='medium'&&v.current==='high'))));
 assert.ok(history.some((e:any)=>e.actorId==='local-user'&&e.occurredAt&&e.payload.taskChanges?.some((c:any)=>c.id===task.id&&c.fields.some((v:any)=>v.field==='status'&&v.previous==='backlog'&&v.current==='ready'))));
 assert.equal((await f.store.list('p',{kind:'comment',parentId:bug.id}))[0].data.runId,run.id);
 await assert.rejects(gateway.agent('task-create',{...request,operationId:'after-terminal'}),{code:'app_agent_report_stale'});
 await assert.rejects(f.store.write({projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:'forge',changes:[{expectedRevision:edited.revision,entity:{id:bug.id,kind:'task',data:{...edited.data,initiatedBy:'forged'}}}]}),{code:'CREATOR_IMMUTABLE'});
 const unapprovedTask=await f.ready('Unapproved source');const unapproved=await gateway.runtime.dispatch('send',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,taskId:unapprovedTask.id,clientMessageId:randomUUID(),input:'No task creation authorization.'});await gateway.agent('claim',auth);
 await assert.rejects(gateway.agent('task-create',{...request,runId:unapproved.id}),{code:'app_agent_creation_forbidden'});
 await gateway.runtime.dispatch('interrupt',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,runId:unapproved.id});await assert.rejects(gateway.agent('task-create',{...request,runId:unapproved.id}),{code:'app_agent_report_stale'});
 await gateway.agent('report',{...auth,runId:unapproved.id,seq:1,idempotencyKey:'stop',status:'interrupted'});
 const planning=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'planning'});
 await assert.rejects(gateway.runtime.dispatch('send',{projectId:'p',sessionId:'s',bindingId:planning.bindingId,clientMessageId:randomUUID(),input:'Planning only',taskCreationApproved:true,taskCreationInitiator:'local-user'}),{code:'app_agent_creation_forbidden'});
 assert.equal((await f.store.list('p',{kind:'task'})).length,3);
});

test('SC14-01/05/07 DATA: exact story hierarchy and three-node graph reject invalid writes without changing records, audit or attachment bytes',async t=>{
 const f=await m2Fixture(t),epic=await f.create('Epic',{type:'epic'}),story=await f.create('UserStory',{type:'user_story',parentId:epic.id}),sub=await f.create('Sub-Task',{type:'sub_task',parentId:story.id});
 const a=await f.ready('A'),b=await f.ready('B'),c=await f.ready('C');
 const cmdLink=async(sourceId:string,targetId:string,relation:string)=>f.command({action:'link',expectedRevision:(await taskManagerSnapshot(f.store,'p')).settingsRevisions.links,link:{sourceId,targetId,relation,reason:'Observed integration dependency'}});
 await cmdLink(a.id,b.id,'blocks');await cmdLink(b.id,c.id,'blocks');await cmdLink(a.id,c.id,'relates_to');
 const upload={filename:'proof.txt',mediaType:'text/plain',base64:Buffer.from('preserve exact managed bytes').toString('base64'),expectedRevision:sub.revision,expectedAuthorityEpoch:1,idempotencyKey:'managed-proof'};
 await uploadTaskAttachment(f.store,'p',sub.id,'local-user',upload);const attachment=(await taskManagerSnapshot(f.store,'p')).attachments[0];
 const unchanged=async(fn:()=>Promise<unknown>,code:string)=>{const rows=await f.store.projectEntities('p'),audit=await f.store.audit('p');await assert.rejects(fn,{code});assert.deepEqual(await f.store.projectEntities('p'),rows);assert.deepEqual(await f.store.audit('p'),audit);assert.equal(await(await downloadTaskAttachment(f.store,'p',sub.id,attachment.id)).text(),'preserve exact managed bytes');};
 await unchanged(()=>f.create('Invalid Task under story',{type:'task',parentId:story.id}),'INVALID_PARENT_TYPE');
 await unchanged(()=>f.command({action:'save',task:{...story.data,parentId:story.id},expectedRevision:story.revision}),'INVALID_PARENT');
 await unchanged(()=>cmdLink(c.id,a.id,'blocks'),'TASK_LINK_CYCLE');
 await unchanged(()=>cmdLink(c.id,a.id,'relates_to'),'DUPLICATE_ISSUE_LINK');
 await unchanged(()=>f.command({action:'transition',taskId:a.id,expectedRevision:a.revision,status:'verification',reason:'No direct transition'}),'TRANSITION_REQUIRED');
 await unchanged(async()=>uploadTaskAttachment(f.store,'p',sub.id,'local-user',{...upload,expectedRevision:(await f.store.get('p',sub.id))!.revision,filename:'bad.png',mediaType:'image/png',base64:Buffer.from('invalid png').toString('base64'),idempotencyKey:'bad-mime'}),'MIME_CONTENT_MISMATCH');
 await f.command({action:'transition',taskId:a.id,expectedRevision:a.revision,status:'in_progress',reason:'Informational reciprocal relation does not block source'});assert.equal((await f.store.get('p',a.id))!.status,'in_progress');
});

test('SC14-02 HTTP: authenticated principal owns initiator; public metadata cannot impersonate an agent or inject trusted provenance',async t=>{
 const f=await m2Fixture(t),calls:any[]=[],origin='http://127.0.0.1:49829';
 const app=await createLocalApplication({store:f.store,origin,instanceId:'integration',profileDirectory:join(f.root,'http'),runtime:{snapshot:async()=>({}),dispatch:async(action,input)=>{calls.push({action,input});return {accepted:true};}}});
 const paired=await app.handleRequest(new Request(origin+'/bootstrap/exchange',{method:'POST',headers:{host:'127.0.0.1:49829',origin,'content-type':'application/json'},body:JSON.stringify({code:app.issuePairingCode()})}));const cookie=paired.headers.get('set-cookie')!.split(';')[0],csrf=(await paired.json() as any).csrfToken;
 const post=async(path:string,input:any)=>app.handleRequest(new Request(origin+'/api/v1'+path,{method:'POST',headers:{host:'127.0.0.1:49829',origin,cookie,'x-paos-csrf':csrf,'content-type':'application/json'},body:JSON.stringify(input)}));
 assert.equal((await post('/runtime/send',{taskCreationApproved:true})).status,200);assert.equal(calls[0].input.taskCreationInitiator,'local-user');
 assert.notEqual((await post('/runtime/send',{taskCreationApproved:true,taskCreationInitiator:'forged'})).status,200);assert.equal(calls.length,1);
 const task=await f.create('Public owner',{creator:{kind:'agent',actorId:'forged'},initiatedBy:'forged'});assert.deepEqual(task.data.creator,{kind:'user',actorId:'local-user'});assert.equal(task.data.initiatedBy,null);
});

test('SC14-06 DATA: missing mapping and stale workflow preview preserve task graph, history and attachment bytes atomically',async t=>{
 const f=await m2Fixture(t),task=await f.create('Pinned task'),other=await f.create('Linked context');let snap=await taskManagerSnapshot(f.store,'p');
 await f.command({action:'link',expectedRevision:snap.settingsRevisions.links,link:{sourceId:task.id,targetId:other.id,relation:'relates_to',reason:'Preserved context'}});
 await uploadTaskAttachment(f.store,'p',task.id,'local-user',{filename:'plan.txt',mediaType:'text/plain',base64:Buffer.from('original plan').toString('base64'),expectedRevision:task.revision,expectedAuthorityEpoch:1,idempotencyKey:'plan'});
 snap=await taskManagerSnapshot(f.store,'p');await f.command({action:'board',expectedRevision:snap.settingsRevisions.board,board:{...snap.board,outOfBoard:true}});
 const definition=structuredClone(defaultRegistry().workflows[0].versions[0].definition);definition.states=definition.states.map(s=>({...s,id:'v2_'+s.id}));definition.transitions=definition.transitions.map(tr=>({...tr,from:'v2_'+tr.from,to:'v2_'+tr.to}));
 snap=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-save-draft',workflowId:'default',definition,expectedRevision:snap.settingsRevisions.workflows});snap=await taskManagerSnapshot(f.store,'p');const publish=await f.command({action:'workflow-publish-preview',workflowId:'default',expectedRevision:snap.settingsRevisions.workflows}) as any;await f.command({action:'workflow-publish',workflowId:'default',expectedRevision:snap.settingsRevisions.workflows,previewDigest:publish.previewDigest});
 snap=await taskManagerSnapshot(f.store,'p');const args={workflowId:'default',fromVersion:1,toVersion:2,expectedRevision:snap.settingsRevisions.workflows};
 const before=await f.store.projectEntities('p'),audit=await f.store.audit('p');await assert.rejects(f.command({action:'workflow-migration-preview',...args,statusMapping:{}}));assert.deepEqual(await f.store.projectEntities('p'),before);assert.deepEqual(await f.store.audit('p'),audit);
 const mapping=Object.fromEntries(defaultRegistry().workflows[0].versions[0].definition.states.map(s=>[s.id,'v2_'+s.id])),preview=await f.command({action:'workflow-migration-preview',...args,statusMapping:mapping}) as any;
 const current=(await f.store.get('p',task.id))!;await f.command({action:'save',task:{...current.data,title:'Concurrent owner title'},expectedRevision:current.revision});const changed=await f.store.projectEntities('p'),history=await f.store.audit('p');
 await assert.rejects(f.command({action:'workflow-migrate',...args,statusMapping:mapping,previewDigest:preview.previewDigest,reason:'Stale preview'}),{code:'PREVIEW_REQUIRED'});assert.deepEqual(await f.store.projectEntities('p'),changed);assert.deepEqual(await f.store.audit('p'),history);
 const attachment=(await taskManagerSnapshot(f.store,'p')).attachments[0];assert.equal(await(await downloadTaskAttachment(f.store,'p',task.id,attachment.id)).text(),'original plan');
});
