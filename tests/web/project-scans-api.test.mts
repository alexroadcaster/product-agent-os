import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import {join} from 'node:path';
import {g03Fixture,until} from './project-g03-fixture.mts';

test('Add returns a registered project and Files before a deferred scan finishes; cancellation rejects late publication',async t=>{
 let release!:()=>void;const deferred=new Promise<void>(resolve=>release=resolve);
 const f=await g03Fixture(t,{scanAnalyzers:{documents:async()=>{await deferred;return {state:'completed'};}}} as any);
 const workspace=join(f.root,'added');await mkdir(workspace);await writeFile(join(workspace,'new.ts'),'export const retained=1;');
 try{
  const response=await f.request('/projects',{name:'Added',workspaceRoot:workspace,requestId:'async-add',scan:true});assert.equal(response.status,201);const project=await response.json();
  assert.equal(project.scan.schemaVersion,'paos_project_scan_view_v1');assert.equal(project.scan.latest.state,'queued');
  assert.equal((await f.request('/projects/'+project.id+'/files')).status,200);
  const running=await until(async()=>await(await f.request('/projects/'+project.id+'/scans')).json(),view=>view.latest?.stages.some((stage:any)=>stage.kind==='documents'&&stage.state==='running'));
  assert.equal((await f.request('/projects/p/scans/'+running.latest.scanId+'/cancel',{})).status,404);
  const cancelled=await f.request('/projects/'+project.id+'/scans/'+running.latest.scanId+'/cancel',{});assert.equal(cancelled.status,200);assert.equal((await cancelled.json()).latest.state,'cancelled');
  release();await until(async()=>await(await f.request('/projects/'+project.id+'/scans')).json(),view=>view.latest?.state==='cancelled');
  assert.equal((await(await f.request('/projects/'+project.id+'/graph/status')).json()).state,'unavailable');
  assert.equal(await readFile(join(workspace,'new.ts'),'utf8'),'export const retained=1;');
 }finally{release();}
});

test('durable Add replay after restart returns one project and rejects a changed envelope',async t=>{
 const f=await g03Fixture(t),workspace=join(f.root,'registered');await mkdir(workspace);
 const input={name:'Durable',workspaceRoot:workspace,requestId:'durable-add',scan:false};
 const first=await f.request('/projects',input);assert.equal(first.status,201);const id=(await first.json()).id;
 await f.restart();const replay=await f.request('/projects',input);assert.equal(replay.status,201);assert.equal((await replay.json()).id,id);
 assert.equal((await f.request('/projects',{...input,name:'Changed'})).status,409);
 const items=(await(await f.request('/projects')).json()).items;assert.equal(items.filter((project:any)=>project.id===id).length,1);
});

test('the default scan executes guarded inventory/documents/code stages and persists restart status',async t=>{
 const f=await g03Fixture(t),started=await f.request('/projects/p/scans',{requestId:'real-scan'});assert.equal(started.status,202);
 const view=await until(async()=>await(await f.request('/projects/p/scans')).json(),value=>['completed','partial','failed'].includes(value.latest?.state));
 assert.equal(view.latest.stages.find((stage:any)=>stage.kind==='code').state,'completed');
 const analysis=view.latest.stages.find((stage:any)=>stage.kind==='analysis');assert.equal(analysis.state,'partial');assert.equal(analysis.data.analysis.availability,'available');assert.equal(analysis.data.analysis.runtime.coreModule,'product_agent_os.discovery.analyze_workspace');
 assert.equal((await(await f.request('/projects/p/graph/status')).json()).revision,view.latest.stages.find((stage:any)=>stage.kind==='code').data.revision);
 await f.restart();assert.equal((await(await f.request('/projects/p/scans')).json()).latest.scanId,view.latest.scanId);
 assert.equal((await f.request('/projects/p/scans',{requestId:'other'},{'x-paos-csrf':''})).status,403);
});
