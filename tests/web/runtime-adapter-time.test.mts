import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtemp,rm} from 'node:fs/promises';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {createRuntimeStoragePorts,taskScopeDigest} from '../../apps/local-service/src/runtime/storage-ports.mts';
const taskId='11111111-1111-4111-8111-111111111111';

function fullJournal(open:boolean) {
 const events:any[]=[];
 const add=(kind:string,intervalId:string,extra={})=>events.push({projectId:'p',taskId,eventId:`event-${events.length+1}`,seq:events.length+1,intervalId,runId:'r',actorId:'runtime',source:'runtime_observation',atMs:events.length+1,kind,...extra});
 add('interval_started','crash');add('interval_crashed','crash');add('interval_reconciled','crash',{confirmedEndedAtMs:2});
 for(let i=0;i<4998;i++){add('interval_started',`closed-${i}`);add('interval_stopped',`closed-${i}`,{reason:'finished'});}
 if(open)add('interval_started','active');return events;
}
function journalStore(open:boolean) {
 const run:any={id:'r',bindingId:'b',projectId:'p',sessionId:'s',accountId:'private',generation:'g',threadId:'thread',turnId:'turn',clientMessageId:'m',inputDigest:'digest',taskId,scopeDigest:'scope',state:'running'};
 const rows=new Map<string,any>([[taskId,{id:taskId,kind:'task',revision:1,data:fixtureTask()}],['s',{id:'s',kind:'session',revision:1}],['r',{id:'r',kind:'run',revision:1,status:'running',data:{runtimeRun:run,timeline:fullJournal(open)}}]]);
 let writes=0;const store:any={project:async()=>({authorityEpoch:1}),get:async(_p:string,id:string)=>rows.get(id)??null,list:async(_p:string,filter:any)=>[...rows.values()].filter(row=>row.kind===filter.kind),
  write:async(command:any)=>{writes++;for(const change of command.changes)rows.set(change.entity.id,{...change.entity,revision:change.expectedRevision+1});}};
 return {run,rows,ports:createRuntimeStoragePorts(store,{actorId:'runtime',now:()=>20000}),writes:()=>writes};
}

test('full time journal still permits interrupt metadata and terminal or crash closure',async()=>{
 for(const state of ['completed','interrupted','recovery_required'] as const) {
  const f=journalStore(true);assert.equal(f.rows.get('r').data.timeline.length,10000);
  await f.ports.updateRun({...f.run,state:'interrupt_requested'});
  await f.ports.updateRun({...f.run,state});
  assert.equal(f.rows.get('r').status,state);assert.equal(f.rows.get('r').data.timeline.length,10001);
  await f.ports.updateRun({...f.run,state});assert.equal(f.rows.get('r').data.timeline.length,10001);
 }
});

test('new work reserves both time start and terminal slots before accepting an intent',async()=>{
 const f=journalStore(false);const task=f.rows.get(taskId);
 await assert.rejects(()=>f.ports.appendIntent({...f.run,id:'new',state:'dispatching',targetRevision:task.revision,scopeDigest:taskScopeDigest(task)}),{code:'runtime_time_limit'});
 assert.equal(f.writes(),0);assert.equal(f.rows.has('new'),false);
});

test('runtime intent pins saved task atomically and confirmed timing excludes approval wait and crash guesses',async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-runtime-time-'));const store=await openLocalStore({databasePath:join(root,'state.sqlite')});
 t.after(async()=>{await store.close();await rm(root,{recursive:true,force:true});});
 await store.registerProject({id:'p',keyPrefix:'TEST',canonicalRoot:root,rootIdentity:'fixture',authorityMode:'sql'});
 const imported={...fixtureTask(),actual:{startedAt:'2026-01-01T00:00:00Z',endedAt:'2026-01-01T00:00:42Z',durationSeconds:42}};
 await store.write({projectId:'p',actorId:'u',idempotencyKey:'seed',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:taskId,kind:'task',data:imported}},{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 let now=1000;const ports=createRuntimeStoragePorts(store,{actorId:'runtime',now:()=>now});const task=(await store.get('p',taskId))!;
 const run={id:'run',bindingId:'b',projectId:'p',sessionId:'s',accountId:'private',generation:'g',threadId:'thread',turnId:null,clientMessageId:'m',inputDigest:'digest',taskId,scopeDigest:taskScopeDigest(task),targetRevision:task.revision,state:'dispatching' as const};
 await ports.appendIntent(run);
 assert.deepEqual((await store.get('p',taskId))!.data.sessionIds,['s']);
 assert.equal(((await store.get('p',taskId))!.data.actual as any).durationSeconds,42);
 assert.equal((await store.get('p',taskId))!.status,'in_progress');
 const secondId='22222222-2222-4222-8222-222222222222';
 await store.write({projectId:'p',actorId:'u',idempotencyKey:'other-task',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:secondId,kind:'task',data:{...fixtureTask(),id:secondId,key:'TEST-2'}}}]});
 const second=(await store.get('p',secondId))!;
 await assert.rejects(ports.appendIntent({...run,id:'other-task-run',taskId:secondId,clientMessageId:'other-task',targetRevision:second.revision,scopeDigest:taskScopeDigest(second)}),{code:'ACTIVE_RUN_RECONCILIATION_REQUIRED'});
 assert.equal(await store.get('p','other-task-run'),null);
 await assert.rejects(ports.appendIntent({...run,id:'competing',clientMessageId:'other'}));
 assert.equal(await store.get('p','competing'),null);
 await ports.updateRun({...run,turnId:'turn',state:'running'});now=5000;
 await ports.updateRun({...run,turnId:'turn',state:'awaiting_approval'});
 assert.equal(((await store.get('p',taskId))!.data.actual as any).durationSeconds,4);
 now=9000;await ports.updateRun({...run,turnId:'turn',state:'running'});now=12000;
 await ports.updateRun({...run,turnId:'turn',state:'completed'});
 assert.equal(((await store.get('p',taskId))!.data.actual as any).durationSeconds,7);
 const before=(await store.get('p','run'))!;await ports.updateRun({...run,turnId:'turn',state:'completed'});
 assert.equal((await store.get('p','run'))!.revision,before.revision);
 const completed=(await store.get('p',taskId))!;
 await store.write({projectId:'p',actorId:'u',idempotencyKey:'reviewed-retry',requireIdle:true,expectedAuthorityEpoch:1,changes:[{expectedRevision:completed.revision,entity:{id:taskId,kind:'task',data:{...completed.data,status:'ready'}}}]});
 const current=(await store.get('p',taskId))!;const retry={...run,id:'retry',clientMessageId:'retry',targetRevision:current.revision,scopeDigest:taskScopeDigest(current)};
 now=13000;await ports.appendIntent(retry);await ports.updateRun({...retry,turnId:'turn2',state:'running'});now=17000;
 await ports.updateRun({...retry,turnId:'turn2',state:'recovery_required'});now=21000;
 await ports.updateRun({...retry,turnId:'turn2',state:'interrupted'});
 assert.equal(((await store.get('p',taskId))!.data.actual as any).durationSeconds,null);
 const timeline=(await store.get('p','retry'))!.data.timeline as any[];
 assert.equal(timeline.filter((event)=>event.kind==='interval_crashed').length,1);
 assert.equal(timeline.some((event)=>event.kind==='interval_stopped'),false);
});
import {fixtureTask} from './runtime-adapter-time.fixture.mts';
