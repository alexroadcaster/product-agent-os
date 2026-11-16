import test from 'node:test';
import assert from 'node:assert/strict';
import {randomUUID} from 'node:crypto';
import {g03Fixture} from './project-g03-fixture.mts';
import {newM2Task} from '../../packages/contracts/issues/task-profile.ts';

test('snapshot freshness is captured with rows and an independent write invalidates the old snapshot',async t=>{
 const f=await g03Fixture(t);
 const before=await(await f.request('/projects/p/task-manager')).json();
 const stamp=await f.request('/projects/p/freshness');assert.equal(stamp.status,200);
 const current=await stamp.json();assert.equal(current.schemaVersion,'paos_project_freshness_v1');assert.deepEqual(before.freshness,current);
 const task=newM2Task('p',randomUUID(),'External channel','local-user');
 assert.equal((await f.request('/projects/p/task-manager/commands',{action:'save',task,expectedRevision:0,expectedAuthorityEpoch:1,idempotencyKey:randomUUID()})).status,200);
 const after=await(await f.request('/projects/p/freshness')).json();assert.ok(after.throughSeq>current.throughSeq);assert.equal(after.projectId,'p');assert.equal(after.generation,current.generation);
 const snapshot=await(await f.request('/projects/p/task-manager')).json();assert.deepEqual(snapshot.freshness,after);assert.ok(snapshot.tasks.some((row:any)=>row.id===task.id));
 await f.restart();assert.deepEqual(await(await f.request('/projects/p/freshness')).json(),after);
});
test('scan and policy changes invalidate independently without filesystem scans and remain project scoped',async t=>{
 const f=await g03Fixture(t),before=await(await f.request('/projects/p/freshness')).json();
 assert.equal((await f.request('/projects/p/files/policy',{expectedVersion:0,policy:{exclude:['main.ts']}})).status,200);
 const policy=await(await f.request('/projects/p/freshness')).json();assert.notEqual(policy.policyVersion,before.policyVersion);assert.equal(policy.throughSeq,before.throughSeq);
 const scan=await f.request('/projects/p/scans',{requestId:'freshness-'+randomUUID()});assert.equal(scan.status,202);
 const scanned=await(await f.request('/projects/p/freshness')).json();assert.ok(scanned.scanVersion>before.scanVersion);
 assert.equal((await f.request('/projects/unknown/freshness')).status,404);
 const anonymous=await f.app.handleRequest(new Request('http://127.0.0.1:43210/api/v1/projects/p/freshness',{headers:{host:'127.0.0.1:43210'}}));assert.equal(anonymous.status,401);
});
