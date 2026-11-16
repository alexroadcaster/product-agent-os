import test from 'node:test';import assert from 'node:assert/strict';import {randomUUID} from 'node:crypto';
import {g03Fixture} from './project-g03-fixture.mts';import {newM2Task} from '../../packages/contracts/issues/task-profile.ts';
import {taskFilePreflight} from '../../apps/local-service/src/runtime/task-file-preflight.mts';
test('policy revoked during inspection invalidates the preflight instead of authorizing old policy',async t=>{
 const f=await g03Fixture(t),task={...newM2Task('p',randomUUID(),'Policy race','local-user'),files:[{relativePath:'main.ts',plannedOperation:'modify',actualOperation:null}]};
 await f.store.write({projectId:'p',actorId:'fixture',idempotencyKey:randomUUID(),expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:task.id,kind:'task',data:task}}]});
 const get=f.store.get;let crossed=false;f.store.get=async(projectId,id)=>{const row=await get(projectId,id);if(!crossed&&id===task.id){crossed=true;await f.store.writeProjectState('p','project_inventory_policy_v1',0,{schemaVersion:'paos_inventory_policy_v1',policy:{exclude:['main.ts']}});}return row;};
 try{await assert.rejects(taskFilePreflight(f.store,'p',task.id,1),{code:'FILE_PREFLIGHT_STALE'});assert.equal(crossed,true);}finally{f.store.get=get;}
});
test('execution preflight resolves only saved task scope and reports blocked limits without dispatch',async t=>{
 let dispatches=0;const f=await g03Fixture(t,{runtime:{snapshot:async()=>({}),dispatch:async()=>{dispatches++;return {};}}});
 const task={...newM2Task('p',randomUUID(),'Preflight scope','local-user'),files:Array.from({length:33},(_,i)=>({relativePath:`new-${i}.txt`,plannedOperation:'create',actualOperation:null}))};
 const saved=await f.request('/projects/p/task-manager/commands',{action:'save',task,expectedRevision:0,expectedAuthorityEpoch:1,idempotencyKey:randomUUID()});assert.equal(saved.status,200);
 const result=await f.request('/projects/p/runtime/file-preflight',{taskId:task.id,expectedRevision:1});assert.equal(result.status,200);const report=await result.json();assert.equal(report.allowed,false);assert.equal(report.limits.files,32);assert.ok(report.reasons.includes('file_count_limit'));assert.equal(report.taskRevision,1);assert.equal(dispatches,0);assert.ok(!JSON.stringify(report).includes('content'));
 assert.equal((await f.request('/projects/p/runtime/file-preflight',{taskId:task.id,expectedRevision:0})).status,409);
 assert.equal((await f.request('/projects/p/runtime/file-preflight',{taskId:task.id,expectedRevision:1,files:[]})).status,400);
 assert.equal((await f.request('/projects/p/runtime/file-preflight',{taskId:'other',expectedRevision:1})).status,404);
 assert.equal((await f.store.list('p',{kind:'run'})).length,0);
});
