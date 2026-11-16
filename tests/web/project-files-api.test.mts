import {test} from 'node:test';
import assert from 'node:assert/strict';
import {writeFile,mkdir} from 'node:fs/promises';
import {join} from 'node:path';
import {g03Fixture} from './project-g03-fixture.mts';

test('authenticated Files API is available before graph and separates metadata pins from content hashes',async t=>{
 const f=await g03Fixture(t);await mkdir(join(f.workspace,'empty'));await writeFile(join(f.workspace,'unknown.bin'),Buffer.from([0,255]));
 const response=await f.request('/projects/p/files');assert.equal(response.status,200);const page=await response.json();
 assert.ok(page.entries.some((entry:any)=>entry.relativePath==='empty'));const file=page.entries.find((entry:any)=>entry.relativePath==='main.ts');assert.ok(file);
 assert.equal((await(await f.request('/projects/p/graph/status')).json()).state,'unavailable');
 const read=await f.request('/projects/p/files/read?path=main.ts&revision='+file.revision);assert.equal(read.status,200);const body=await read.json();assert.equal(body.state,'available');assert.equal(body.reference.revisionKind,'sha256');assert.notEqual(body.reference.revision,file.revision);
 await writeFile(join(f.workspace,'main.ts'),'export const changed=2;');assert.equal((await(await f.request('/projects/p/files/read?path=main.ts&revision='+file.revision)).json()).state,'stale');
 assert.equal((await f.request('/projects/p/files?path=..')).status,409);
 assert.equal((await f.request('/projects/p/files',undefined,{cookie:''})).status,401);
});

test('policy API uses profile CAS, preserves hard exclusions and invalidates old file selection',async t=>{
 const f=await g03Fixture(t);await writeFile(join(f.workspace,'.env'),'synthetic fixture');const page=await(await f.request('/projects/p/files')).json(),entry=page.entries.find((row:any)=>row.relativePath==='main.ts');
 const saved=await f.request('/projects/p/files/policy',{expectedVersion:0,policy:{include:['*'],exclude:['main.ts']}});assert.equal(saved.status,200);
 assert.equal((await f.request('/projects/p/files/policy',{expectedVersion:0,policy:{include:['*']}})).status,409);
 assert.equal((await(await f.request('/projects/p/files/read?path=main.ts&revision='+entry.revision)).json()).state,'forbidden');
 assert.equal((await(await f.request('/projects/p/files/read?path=.env')).json()).state,'forbidden');
 assert.equal((await f.request('/projects/p/files/policy',{expectedVersion:1,policy:{}},{'x-paos-csrf':''})).status,403);
 await f.restart();assert.deepEqual((await(await f.request('/projects/p/files/policy')).json()).policy.exclude,['main.ts']);
});
