import test from 'node:test';
import assert from 'node:assert/strict';
import {open,writeFile,mkdir} from 'node:fs/promises';
import {join} from 'node:path';
import {m2Fixture} from './m2-fixture.mts';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {createCodeIndex} from '../../apps/local-service/src/code-index/service.mts';
import {taskManagerSnapshot} from '../../apps/local-service/src/task-manager/service.mts';
import {createLocalApplication} from '../../apps/local-service/src/http/application.mts';

test('graph status uses metadata only; source excerpts still verify raw bytes',async t=>{
 const f=await m2Fixture(t);await writeFile(join(f.root,'entry.ts'),'export const marker=1;');
 const index=createCodeIndex(f.store),built=await index.rebuild('p');
 const handle=await open(join(f.root,'entry.ts'),'r'),prototype=Object.getPrototypeOf(handle),original=prototype.read;await handle.close();let reads=0;
 prototype.read=async function(...args:any[]){reads++;return original.apply(this,args);};
 try{assert.equal((await index.status('p')).state,'fresh');assert.equal(reads,0,'status must not reopen every source body');
  const graph=await index.graph('p',new URLSearchParams({revision:built.revision!})),file=graph.nodes.find(n=>n.kind==='file'&&n.relativePath==='entry.ts')!;
  assert.equal((await index.source('p',new URLSearchParams({revision:built.revision!,fileId:file.id}))).content,'export const marker=1;');assert.ok(reads>0);
  await writeFile(join(f.root,'entry.ts'),'export const marker=2;');assert.equal((await index.status('p')).state,'stale');
  await assert.rejects(index.source('p',new URLSearchParams({revision:built.revision!,fileId:file.id})),{code:'GRAPH_SOURCE_STALE'});
 }finally{prototype.read=original;}
});

test('ninth project evicts and rebuilds graphs without losing file access or accepting old cursors',async t=>{
 const f=await m2Fixture(t),index=createCodeIndex(f.store);let original='';
 for(let n=0;n<9;n++){const root=join(f.root,'workspace-'+n);await mkdir(root);await writeFile(join(root,'entry.ts'),'export const a=1,b=2;');const pin=await bindProject('g'+n,root);await f.store.registerProject({id:'g'+n,keyPrefix:'AAA'+String.fromCharCode(65+n),canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'sql'});const built=await index.rebuild('g'+n);if(n===0)original=built.revision!;assert.equal(built.state,'fresh');}
 assert.equal((await index.status('g0')).state,'unavailable');
 await assert.rejects(index.graph('g0',new URLSearchParams({revision:original})),{code:'GRAPH_INDEX_UNAVAILABLE'});
 assert.equal((await index.rebuild('g0')).state,'fresh');
});

test('task and startup reads exclude unrelated large document bodies before snapshot limits',async t=>{
 const f=await m2Fixture(t),task=await f.create('Retained task');
 for(let n=0;n<18;n++)await f.store.write({projectId:'p',actorId:'synthetic-user',expectedAuthorityEpoch:1,idempotencyKey:'large-'+n,changes:[{expectedRevision:0,entity:{id:'large-'+n,kind:'document',title:'Synthetic large document',body:'x'.repeat(4*1024*1024)}}]});
 await assert.rejects(f.store.projectEntities('p'),{code:'SNAPSHOT_TOO_LARGE'});
 const snapshot=await taskManagerSnapshot(f.store,'p',{observe:true});assert.equal(snapshot.tasks.length,1);assert.equal(snapshot.tasks[0].id,task.id);assert.ok(snapshot.freshness);
 const app=await createLocalApplication({store:f.store,origin:'http://127.0.0.1:43219',instanceId:'bounded-startup',profileDirectory:join(f.root,'profile'),assetRoots:[]});await app.close();
});
