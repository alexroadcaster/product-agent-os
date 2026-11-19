import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,rm,readFile,rename} from 'node:fs/promises';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {createProjectScans,type ScanAnalyzerContext} from '../../apps/local-service/src/project-scans/service.mts';
import type {ProjectScanView} from '../../packages/contracts/project-scan.ts';

async function fixture(t:any){
 const root=await mkdtemp(join(tmpdir(),'paos-scans-')),workspace=join(root,'workspace');await mkdir(workspace);await writeFile(join(workspace,'main.ts'),'export const ordinary=1;');
 const binding=await bindProject('p',workspace),store=await openLocalStore({databasePath:join(root,'state.sqlite')});
 await store.registerProject({id:'p',keyPrefix:'PAOS',canonicalRoot:binding.workspaceRoot,rootIdentity:binding.directoryIdentity,authorityMode:'sql'});
 const services:ReturnType<typeof createProjectScans>[]=[];t.after(async()=>{for(const service of services)await service.close();await store.close();await rm(root,{recursive:true,force:true});});
 return {root,workspace,store,service:(analyzers?:any,limits?:any)=>{const service=createProjectScans({store,analyzers,limits});services.push(service);return service;}};
}
const deferred=()=>{let resolve!:(value:any)=>void;const promise=new Promise<any>(r=>resolve=r);return {promise,resolve};};
async function until(service:ReturnType<typeof createProjectScans>,predicate:(value:any)=>boolean){const deadline=Date.now()+5000;while(Date.now()<deadline){const value=await service.status('p');if(predicate(value))return value;await new Promise(resolve=>setTimeout(resolve,5));}assert.fail('bounded scan condition not observed');}
test('scan start persists queued identity without waiting for a deferred analyzer',async t=>{
 const f=await fixture(t),pending=deferred(),service=f.service({code:async()=>pending.promise});await service.initialized();
 const started=await service.start('p',{requestId:'first'});assert.equal(started.latest!.state,'queued');assert.ok(started.latest!.scanId);pending.resolve({state:'completed'});
});

test('stages preserve partial results and unsupported capabilities without changing target files',async t=>{
 const f=await fixture(t),source=await readFile(join(f.workspace,'main.ts'),'utf8');
 const service=f.service({documents:async()=>({state:'completed',counts:{sources:1}}),code:async()=>{throw Object.assign(Error('fixture'),{code:'PARSER_UNAVAILABLE'});}});
 await service.start('p');const result=await until(service,v=>v.latest.state==='partial');
 assert.equal(result.latest.stages.find((s:any)=>s.kind==='documents').state,'completed');assert.equal(result.latest.stages.find((s:any)=>s.kind==='code').state,'failed');assert.equal(result.latest.stages.find((s:any)=>s.kind==='analysis').state,'unavailable');
 assert.equal(result.capabilities.schema,false);assert.equal(result.capabilities.code_database,false);assert.equal(result.lastSuccessful.scanId,result.latest.scanId);assert.equal(await readFile(join(f.workspace,'main.ts'),'utf8'),source);
});

test('cancelled analyzer cannot publish late completion or replace the last successful revision',async t=>{
 const f=await fixture(t),pending=deferred();let defer=false,context:any;
 const service=f.service({documents:async()=>({state:'completed'}),code:async(c:any)=>{context=c;if(defer){await c.onProgress(0,1);return pending.promise;}return {state:'completed'};},analysis:async()=>({state:'completed'})});
 await service.start('p',{requestId:'complete'});const good=await until(service,v=>v.latest.state==='completed');defer=true;
 const started=await service.start('p',{requestId:'cancel'});await until(service,v=>v.latest.stage==='code'&&v.latest.stages.find((s:any)=>s.kind==='code').progress?.total===1);
 const cancelled=await service.cancel('p',started.latest!.scanId);assert.equal(cancelled.latest!.state,'cancelled');assert.equal(context.canPublish(),false);await assert.rejects(context.publicationGuard());
 pending.resolve({state:'completed',data:{late:true}});const after=await service.status('p');assert.equal(after.latest!.state,'cancelled');assert.equal(after.lastSuccessful!.scanId,good.latest.scanId);
});

test('request replay and concurrent equivalent starts do not duplicate a scan; restart requires retry',async t=>{
 const f=await fixture(t),pending=deferred();let calls=0;
 const first=f.service({code:async(c:any)=>{calls++;await c.onProgress(0,1);return pending.promise;}});await first.initialized();
 const starts=await Promise.all(['a','a','b','c'].map(requestId=>first.start('p',{requestId})));assert.equal(new Set(starts.map(v=>v.latest!.scanId)).size,1);
 await until(first,v=>v.latest.stages.find((s:any)=>s.kind==='code').progress?.total===1);assert.equal(calls,1);
 const restarted=f.service({code:async()=>({state:'completed'})});await restarted.initialized();assert.equal((await restarted.status('p')).latest!.state,'interrupted');
 const replay=await restarted.start('p',{requestId:'a'});assert.equal(replay.replayedScanId,starts[0].latest!.scanId);assert.equal(replay.latest!.state,'interrupted');
 const retry=await restarted.retry('p',starts[0].latest!.scanId);assert.notEqual(retry.latest!.scanId,starts[0].latest!.scanId);pending.resolve({state:'completed'});
 await until(restarted,v=>v.latest.state==='partial');assert.equal(calls,1);
});

test('a foreign project cannot cancel a known scan ID',async t=>{
 const f=await fixture(t),other=join(f.root,'other');await mkdir(other);const binding=await bindProject('q',other);await f.store.registerProject({id:'q',keyPrefix:'OTHR',canonicalRoot:binding.workspaceRoot,rootIdentity:binding.directoryIdentity,authorityMode:'sql'});
 const pending=deferred();let context:any;const service=f.service({code:async(c:any)=>{context=c;await c.onProgress(0,1);return pending.promise;}});const start=await service.start('p');await until(service,v=>v.latest.stages.find((s:any)=>s.kind==='code').progress?.total===1);
 await assert.rejects(service.cancel('q',start.latest!.scanId),{code:'PROJECT_SCAN_NOT_FOUND'});assert.equal(context.canPublish(),true);pending.resolve({state:'completed'});
});

test('source or root drift rejects late stages without claiming successful publication',async t=>{
 const f=await fixture(t),pending=deferred();
 const service=f.service({
  code:async({onProgress}:ScanAnalyzerContext)=>{
   await onProgress(0,1);
   return pending.promise;
  },
 });
 await service.start('p');
 // The scan records the code stage before its inventory check admits the analyzer.
 await until(service,(view:ProjectScanView)=>view.latest?.stages.find(stage=>stage.kind==='code')?.progress?.total===1);

 await writeFile(join(f.workspace,'main.ts'),'export const changed=2;');
 pending.resolve({state:'completed',counts:{files:1}});
 const {latest,lastSuccessful}=await until(service,(view:ProjectScanView)=>view.latest?.state==='interrupted');
 assert.ok(latest);
 assert.ok(latest.reasons.includes('PROJECT_SCAN_SOURCE_STALE'),JSON.stringify(latest.reasons));
 const codeStage=latest.stages.find(stage=>stage.kind==='code');
 assert.equal(codeStage?.state,'cancelled');
 assert.equal(codeStage?.counts,undefined);
 assert.equal(lastSuccessful,null);

 await rename(f.workspace,join(f.root,'old'));
 await mkdir(f.workspace);
 await assert.rejects(service.start('p'),{code:'PROJECT_ROOT_UNAVAILABLE'});
});

test('timeout is explicit and an unknown persisted schema does not prevent service initialization',async t=>{
 const f=await fixture(t),pending=deferred(),service=f.service({code:async()=>pending.promise},{stageMilliseconds:30});await service.start('p');const timed=await until(service,v=>['failed','cancelled'].includes(v.latest.state));assert.ok(timed.latest.reasons.includes('PROJECT_SCAN_TIMEOUT'));assert.equal(timed.latest.state,'failed');pending.resolve({state:'completed'});await service.close();
 const saved=await f.store.readProjectState('p','project_scan_v1');await f.store.writeProjectState('p','project_scan_v1',saved!.version,{schemaVersion:'future_unknown'});
 const unknown=f.service();await unknown.initialized();await assert.rejects(unknown.status('p'),{code:'PROJECT_SCAN_STATE_UNAVAILABLE'});
});

test('versioned optional schema stage executes only when an explicit adapter is supplied',async t=>{
 const f=await fixture(t);let called=false;const service=f.service({schema:async(c:any)=>{await c.publicationGuard();called=true;return {state:'completed',counts:{tables:2}};}});
 await service.start('p');const result=await until(service,v=>v.latest.state==='partial');
 assert.equal(result.capabilities.schema,true);assert.equal(result.capabilities.code_database,false);assert.equal(called,true);assert.equal(result.latest.stages.find((s:any)=>s.kind==='schema')?.counts.tables,2);
});

test('policy drift interrupts an admitted analyzer and result budgets preserve other stages',async t=>{
 const f=await fixture(t),pending=deferred();let context:any;const service=f.service({code:async(c:any)=>{context=c;await c.onProgress(0,1);return pending.promise;}});
 await service.start('p');await until(service,v=>v.latest.stages.find((s:any)=>s.kind==='code').progress?.total===1);
 await f.store.writeProjectState('p','project_inventory_policy_v1',0,{schemaVersion:'paos_inventory_policy_v1',policy:{exclude:['main.ts']}});await assert.rejects(context.publicationGuard(),{code:'PROJECT_SCAN_SCOPE_STALE'});pending.resolve({state:'completed'});await until(service,v=>v.latest.state==='interrupted');
 const limited=f.service({documents:async()=>({state:'completed',data:{large:'x'.repeat(1024)}}),code:async()=>({state:'completed'})},{resultBytes:256});await limited.start('p');const result=await until(limited,v=>v.latest.state==='partial');
 assert.equal(result.latest.stages.find((s:any)=>s.kind==='documents').state,'failed');assert.ok(result.latest.reasons.includes('PROJECT_SCAN_RESULT_LIMIT'));assert.equal(result.latest.stages.find((s:any)=>s.kind==='code').state,'completed');
});

test('a stale expected revision and external CAS supersession cannot publish a success',async t=>{
 const f=await fixture(t),service=f.service();await service.start('p',{revision:'0'.repeat(64)});const stale=await until(service,v=>v.latest.state==='interrupted');assert.equal(stale.lastSuccessful,null);
 const pending=deferred();let context:any;const active=f.service({code:async(c:any)=>{context=c;await c.onProgress(0,1);return pending.promise;}});await active.start('p');await until(active,v=>v.latest.stages.find((s:any)=>s.kind==='code').progress?.total===1);
 const saved=await f.store.readProjectState('p','project_scan_v1'),value=structuredClone(saved!.value) as any;value.latest.state='cancelled';value.latest.reasons=['OTHER_OWNER_CANCELLED'];await f.store.writeProjectState('p','project_scan_v1',saved!.version,value);
 await assert.rejects(context.publicationGuard(),{code:'PROJECT_SCAN_SUPERSEDED'});pending.resolve({state:'completed'});assert.equal((await active.status('p')).latest!.state,'cancelled');
});

test('malformed start input is rejected before durable scan state changes',async t=>{
 const f=await fixture(t),service=f.service();await service.initialized();
 await assert.rejects(service.start('p',{requestId:42} as any),{code:'PROJECT_SCAN_INPUT_INVALID'});await assert.rejects(service.start('p',{extra:true} as any),{code:'PROJECT_SCAN_INPUT_INVALID'});assert.equal((await service.status('p')).latest,null);
});

test('a malformed current-version record cannot masquerade as a completed scan',async t=>{
 const f=await fixture(t);await f.store.writeProjectState('p','project_scan_v1',0,{schemaVersion:'paos_project_scan_record_v1',latest:{schemaVersion:'paos_project_scan_v1',state:'completed'},lastSuccessful:null,requests:[]});
 const service=f.service();await service.initialized();await assert.rejects(service.status('p'),{code:'PROJECT_SCAN_STATE_UNAVAILABLE'});
});
