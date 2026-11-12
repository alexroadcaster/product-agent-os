import {test} from 'node:test';
import assert from 'node:assert/strict';
import {randomUUID} from 'node:crypto';
import {writeFile,link,mkdir} from 'node:fs/promises';
import {join,parse} from 'node:path';
import {fixture,step} from './recipe-fixture.mts';
import {createScheduler} from '../../apps/local-service/src/scheduler/service.mts';
import {createTeamService} from '../../apps/local-service/src/team/service.mts';
import {verifyQueueOwnership,workspaceOverlap} from '../../apps/local-service/src/scheduler/ownership.mts';
import {taskManagerSnapshot} from '../../apps/local-service/src/task-manager/service.mts';

async function queued(t:Parameters<typeof fixture>[0]){
 const f=await fixture(t,[step('work')],10,{}, {successTarget:'review'}),second=await f.ready('Second'),prerequisite=await f.ready('Prerequisite');
 const before=await f.autonomy.snapshot('p'),policy={...before.policy!,allowedTaskIds:[f.task.id,second.id,prerequisite.id]};
 const preview=await f.autonomy.preview('p',policy,before.revision);await f.autonomy.command('p','local-user','save',{policy,previewDigest:preview.previewDigest,expectedRevision:before.revision,expectedAuthorityEpoch:1,idempotencyKey:'queue-policy'});await f.autonomy.command('p','local-user','resume',{expectedRevision:before.revision+1,expectedAuthorityEpoch:1,idempotencyKey:'queue-policy-resume'});
 let queue=createScheduler({store:f.store,recipes:f.service,automatic:false});await queue.initialized();f.beforeClose(()=>queue.close());
 const intent=(task=f.task)=>({...f.input,taskId:task.id,expectedTaskRevision:task.revision});
 async function enqueue(task=f.task,key=randomUUID()){const input=intent(task),preview=await queue.preview('p',input),request={...input,previewDigest:preview.previewDigest,expectedRevision:preview.queueRevision,expectedAuthorityEpoch:1,idempotencyKey:key};return {result:await queue.enqueue('p',request) as {entryId:string},request};}
 const act=async(action:string,extra={})=>queue.command('p',action,{expectedRevision:(await queue.snapshot('p')).revision,expectedAuthorityEpoch:1,idempotencyKey:randomUUID(),...extra});
 const finish=async()=>{await f.service.tick();let job;try{job=await f.report();}catch(error){throw new Error(JSON.stringify((await f.service.list('p')).items.map(e=>({state:e.state,reason:e.reason,attempts:e.attempts}))),{cause:error});}await f.service.tick();await f.service.tick();await queue.tick();return job;};
 return {...f,second,prerequisite,intent,enqueue,act,finish,get queue(){return queue;},async restart(){await queue.close();await f.restart();queue=createScheduler({store:f.store,recipes:f.service,automatic:false});await queue.initialized();}};
}

test('queue freezes assignment, admits one shared-workspace writer and automatically advances successor',async t=>{
 const f=await queued(t),a=await f.enqueue(),b=await f.enqueue(f.second);assert.deepEqual(await f.queue.enqueue('p',a.request),a.result);
 const initial=await f.queue.snapshot('p');assert.equal(initial.items.length,2);assert.equal((await f.autonomy.snapshot('p')).usedRuns,0);assert.equal(JSON.stringify(initial).includes('Pinned fixture role'),false);
 const binding=await f.gateway.runtime.snapshot({projectId:'p',sessionId:'s'});
 await assert.rejects(()=>f.gateway.runtime.dispatch('send',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,taskId:f.second.id,clientMessageId:'bypass',input:'Bypass queue'}),{code:'QUEUE_TASK_RESERVED'});
 await assert.rejects(async()=>f.service.start('p','local-user',{...f.input,previewDigest:(await f.service.preview('p',f.input)).previewDigest,expectedAuthorityEpoch:1,idempotencyKey:'direct'}),{code:'QUEUE_TASK_RESERVED'});
 const team=createTeamService(f.store),assetId=f.input.roleBindings.builder,proposal={kind:'agent',action:'update',assetId,name:'Builder',description:'Changed',content:'New role instructions',dependencies:[],reason:'Updated after enqueue'};
 const preview=await team.preview('p',{proposal,expectedRevision:1});await team.apply('p','local-user',{proposal,expectedRevision:1,previewDigest:preview.previewDigest,epoch:1,idempotencyKey:'new-role'});
 await f.queue.tick();let snapshot=await f.queue.snapshot('p');assert.equal(snapshot.items.find(e=>e.id===a.result.entryId)!.state,'running');assert.ok(snapshot.items.find(e=>e.id===b.result.entryId)!.waitReasons.includes('WORKSPACE_OWNERSHIP_BUSY'));
 const first=await f.finish();assert.equal(first.assetPins[0].content,'Pinned fixture role');assert.equal(first.assetPins[0].version,1);
 snapshot=await f.queue.snapshot('p');assert.equal(snapshot.items.find(e=>e.id===a.result.entryId)!.state,'completed');assert.equal(snapshot.items.find(e=>e.id===b.result.entryId)!.state,'running');
 await f.finish();assert.equal((await f.autonomy.snapshot('p')).usedRuns,2);assert.equal((await f.store.list('p',{kind:'run'})).length,2);assert.equal((await f.queue.snapshot('p')).items.every(e=>e.state==='completed'),true);
});

test('dependency-blocked head is skipped, hard WIP is rechecked and only Done releases dependency',async t=>{
 const f=await queued(t);let snapshot=await taskManagerSnapshot(f.store,'p');await f.command({action:'link',expectedRevision:snapshot.settingsRevisions.links,link:{sourceId:f.prerequisite.id,targetId:f.task.id,relation:'blocks',reason:'Required prerequisite'}});
 const a=await f.enqueue(),b=await f.enqueue(f.second);await f.queue.tick();let view=await f.queue.snapshot('p');assert.ok(view.items.find(e=>e.id===a.result.entryId)!.waitReasons.includes('DEPENDENCY_BLOCKED'));assert.equal(view.items.find(e=>e.id===b.result.entryId)!.state,'running');await f.finish();
 const prerequisite=(await f.store.get('p',f.prerequisite.id))!;await f.command({action:'transition',taskId:prerequisite.id,status:'done',expectedRevision:prerequisite.revision,manual:true,evidence:[{criterion:'Observed fixture',outcome:'passed',evidence:'Observed prerequisite check'}],reason:'Verified prerequisite'});
 snapshot=await taskManagerSnapshot(f.store,'p');const board={...snapshot.board,columns:snapshot.workflows.workflows[0].versions[0].definition.states.map(s=>({id:s.id,statuses:[s.id],...(s.id==='in_progress'?{wipLimit:0,wipMode:'hard'}:{})}))};
 await f.command({action:'board',board,expectedRevision:snapshot.settingsRevisions.board});await f.queue.tick();view=await f.queue.snapshot('p');assert.ok(view.items.find(e=>e.id===a.result.entryId)!.waitReasons.includes('HARD_WIP_LIMIT'));assert.equal((await f.store.list('p',{kind:'run'})).length,1);
 snapshot=await taskManagerSnapshot(f.store,'p');await f.command({action:'board',board:{...board,columns:board.columns.map(c=>c.id==='in_progress'?{...c,wipLimit:1}:c)},expectedRevision:snapshot.settingsRevisions.board});await f.queue.tick();assert.equal((await f.queue.snapshot('p')).items.find(e=>e.id===a.result.entryId)!.state,'running');
});

test('queue controls preserve CAS/replay/order; changed task and policy never silently expand intent',async t=>{
 const f=await queued(t),a=await f.enqueue(),b=await f.enqueue(f.second);let s=await f.queue.snapshot('p');const order=[b.result.entryId,a.result.entryId];const request={order,expectedRevision:s.revision,expectedAuthorityEpoch:1,idempotencyKey:'order'};
 await f.queue.command('p','reorder',request);assert.deepEqual((await f.queue.snapshot('p')).order,order);assert.deepEqual(await f.queue.command('p','reorder',request),{revision:s.revision+1});await assert.rejects(()=>f.queue.command('p','pause',{expectedRevision:s.revision,expectedAuthorityEpoch:1,idempotencyKey:'stale'}),{code:'QUEUE_REVISION_CONFLICT'});
 await f.act('pause');await f.queue.tick();assert.equal((await f.queue.snapshot('p')).items.every(e=>e.state==='queued'),true);await f.act('resume');
 const task=(await f.store.get('p',f.second.id))!;await f.command({action:'save',task:{...task.data,title:'Changed scope'},expectedRevision:task.revision});await f.queue.tick();s=await f.queue.snapshot('p');assert.equal(s.items.find(e=>e.id===b.result.entryId)!.state,'needs_review');assert.equal(s.items.find(e=>e.id===a.result.entryId)!.state,'running');
 await f.act('cancel',{entryId:b.result.entryId});assert.equal((await f.queue.snapshot('p')).items.find(e=>e.id===b.result.entryId)!.state,'cancelled');
});

test('restart preserves pending intent and fences admitted work without replay or early cancellation release',async t=>{
 const f=await queued(t),a=await f.enqueue(),b=await f.enqueue(f.second);await f.queue.tick();await f.service.tick();const claim=await f.gateway.agent('claim',f.auth);await f.restart();let s=await f.queue.snapshot('p');assert.equal(s.items.find(e=>e.id===a.result.entryId)!.state,'recovery_required');assert.equal(s.items.find(e=>e.id===b.result.entryId)!.state,'queued');
 await f.queue.tick();assert.equal((await f.store.list('p',{kind:'run'})).length,1);await assert.rejects(()=>f.act('cancel',{entryId:a.result.entryId}),{code:'RECIPE_RECOVERY_UNRESOLVED'});
 await f.gateway.runtime.dispatch('interrupt',{projectId:'p',sessionId:'s',bindingId:claim.job.bindingId,runId:claim.job.runId});await f.gateway.agent('report',{...f.auth,runId:claim.job.runId,seq:1,idempotencyKey:'stopped',status:'interrupted'});await f.act('cancel',{entryId:a.result.entryId});await f.queue.tick();s=await f.queue.snapshot('p');assert.equal(s.items.find(e=>e.id===a.result.entryId)!.state,'cancelled');assert.equal(s.items.find(e=>e.id===b.result.entryId)!.state,'running');
});

test('physical ownership rejects hardlink aliases and canonical parent roots overlap',async t=>{
 const f=await queued(t),plan=await f.service.freezeQueue('p',f.input);await writeFile(join(f.root,'original.txt'),'fixture');await link(join(f.root,'original.txt'),join(f.root,'alias.txt'));
 await assert.rejects(()=>verifyQueueOwnership(plan,[{path:'alias.txt',mode:'write'}]),{code:'QUEUE_UNSAFE_OWNERSHIP'});assert.equal(workspaceOverlap(f.root,join(f.root,'nested')),true);assert.equal(workspaceOverlap(f.root,f.root+'-other'),false);
});
test('filesystem root overlaps descendants in both directions without touching that root',()=>{
 const root=parse(process.cwd()).root,child=join(root,'paos-synthetic-descendant');assert.equal(workspaceOverlap(root,child),true);assert.equal(workspaceOverlap(child,root),true);assert.equal(workspaceOverlap(child,child+'-other'),false);
});
