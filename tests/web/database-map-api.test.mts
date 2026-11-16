import test from 'node:test';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {join} from 'node:path';
import {readFile,writeFile} from 'node:fs/promises';
import {g03Fixture,until} from './project-g03-fixture.mts';
import {createAppAgentGateway} from '../../apps/local-service/src/runtime/app-agent-gateway.mts';
import {createAppAgentChannel} from '../../apps/local-service/src/runtime/app-agent-channel.mts';

test('database source registration is explicit, profile-scoped, metadata-only and schema stage is independently requested',async t=>{
 const f=await g03Fixture(t),path=join(f.workspace,'application.sqlite'),db=new DatabaseSync(path);db.exec('CREATE TABLE parent(id INTEGER PRIMARY KEY);CREATE TABLE child(a INTEGER,b TEXT,FOREIGN KEY(a) REFERENCES parent(id));INSERT INTO parent VALUES(1);INSERT INTO child VALUES(1,\'SYNTHETIC_ROW_NEVER_PUBLIC\');');db.close();
 const before=await readFile(path);
 const initial=await f.request('/projects/p/database');assert.equal(initial.status,200);const status=await initial.json();assert.equal(status.state,'unselected');assert.equal(status.snapshotRevision,null);
 const candidate=status.candidates.find((x:any)=>x.relativePath==='application.sqlite');assert.ok(candidate);
 const selected=await f.request('/projects/p/database/source',{relativePath:candidate.relativePath,expectedFileRevision:candidate.fileRevision,expectedVersion:status.version});assert.equal(selected.status,200);assert.equal((await selected.json()).state,'selected');
 assert.equal((await f.request('/projects/p/database/schema')).status,400); // Registration does not open SQLite.
 const started=await f.request('/projects/p/database/scan',{requestId:'metadata-only'});assert.equal(started.status,202);const scan=await started.json();assert.deepEqual(scan.latest.stages.map((s:any)=>s.kind),['inventory','schema']);
 const end=await until(async()=>await(await f.request('/projects/p/scans')).json(),(x:any)=>!['queued','running'].includes(x.latest.state),15000);
 const schemaStage=end.latest.stages.find((x:any)=>x.kind==='schema');assert.equal(schemaStage.state,'completed',JSON.stringify(schemaStage));
 const result=await f.request('/projects/p/database/schema');assert.equal(result.status,200);const page=await result.json();assert.equal(page.tables.length,2);assert.equal(page.state,'current');assert.ok(!JSON.stringify(page).includes('SYNTHETIC_ROW_NEVER_PUBLIC'));
 assert.deepEqual(await readFile(path),before);
 await f.restart();assert.equal((await(await f.request('/projects/p/database')).json()).snapshotRevision,page.snapshot.revision);
 assert.equal((await f.request('/projects/p/database/source',{clear:true,expectedVersion:0})).status,409);
});

test('production code-to-table API requires both current revisions and returns bounded source evidence',async t=>{
 const f=await g03Fixture(t),path=join(f.workspace,'application.sqlite'),db=new DatabaseSync(path);db.exec('CREATE TABLE users(id INTEGER PRIMARY KEY);');db.close();
 await writeFile(join(f.workspace,'query.ts'),'import {DatabaseSync} from "node:sqlite"; const db=new DatabaseSync(new URL("./application.sqlite",import.meta.url)); db.prepare("SELECT id FROM users WHERE id=1");');
 const initial=await f.request('/projects/p/code-database');assert.equal(initial.status,200);assert.equal((await initial.json()).state,'unavailable');
 const status=await(await f.request('/projects/p/database')).json(),candidate=status.candidates.find((x:any)=>x.relativePath==='application.sqlite');
 await f.request('/projects/p/database/source',{relativePath:candidate.relativePath,expectedFileRevision:candidate.fileRevision,expectedVersion:status.version});await f.request('/projects/p/database/scan',{requestId:'code-schema'});
 await until(async()=>await(await f.request('/projects/p/scans')).json(),(x:any)=>!['queued','running'].includes(x.latest?.state),15000);
 const graph=await(await f.request('/projects/p/graph/rebuild',{})).json();assert.equal(graph.state,'fresh');
 const started=await f.request('/projects/p/code-database/scan',{requestId:'links'});assert.equal(started.status,202);assert.deepEqual((await started.json()).latest.stages.map((s:any)=>s.kind),['inventory','code_database']);
 const result=await until(async()=>await(await f.request('/projects/p/scans')).json(),(x:any)=>!['queued','running'].includes(x.latest?.state),15000);assert.ok(['completed','partial'].includes(result.latest.state),JSON.stringify(result));
 const view=await(await f.request('/projects/p/code-database')).json();assert.ok(['fresh','partial'].includes(view.state));assert.equal(view.counts.confirmed,1);
 const query=new URLSearchParams({codeRevision:view.codeRevision,schemaRevision:view.schemaRevision,confidence:'confirmed'}),response=await f.request('/projects/p/code-database/links?'+query);assert.equal(response.status,200);const page=await response.json();assert.equal(page.links[0].table,'users');assert.equal(page.links[0].relativePath,'query.ts');assert.equal(page.links[0].sourcePath,'application.sqlite');assert.ok(page.contextBytes<=32768);
 assert.equal((await f.request('/projects/p/code-database/links?codeRevision=foreign&schemaRevision='+view.schemaRevision)).status,409);
 // An actual private channel and claimed synthetic worker reach the same production query owner.
 await f.store.write({projectId:'p',actorId:'synthetic-user',idempotencyKey:'query-session',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'query-session',kind:'session'}}]});
 const gateway=createAppAgentGateway({store:f.store,profileId:'synthetic',actorId:'synthetic-agent',queryProject:(id,input)=>f.app.queryCodeDatabase(id,input)});
 let channel:Awaited<ReturnType<typeof createAppAgentChannel>>|undefined;
 try{await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'synthetic-query-worker',generation:'synthetic-generation'}),binding=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'query-session',mode:'discussion'}),run=await gateway.runtime.dispatch('send',{projectId:'p',sessionId:'query-session',bindingId:binding.bindingId,clientMessageId:'synthetic-query',input:'Read the static dependency evidence.'});
  const auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};await gateway.agent('claim',auth);
  const origin='http://127.0.0.1:43210';channel=await createAppAgentChannel({profileDirectory:f.profile,instanceId:'synthetic-query',origin,assertProfile:async()=>{},dispatch:(action,input)=>gateway.agent(action,input)});const descriptor=JSON.parse(await readFile(channel.descriptorPath,'utf8'));
  const result=await channel.handle(new Request(origin+'/agent/v1/project-query',{method:'POST',headers:{host:'127.0.0.1:43210',origin,authorization:'Bearer '+descriptor.capabilityToken,'content-type':'application/json'},body:JSON.stringify({...auth,runId:run.id,kind:'links',codeRevision:view.codeRevision,schemaRevision:view.schemaRevision,confidence:'confirmed'})}));assert.equal(result.status,200);const evidence=await result.json();assert.equal(evidence.links[0].table,'users');assert.ok(Buffer.byteLength(JSON.stringify(evidence))<=32768);
 }finally{await channel?.close();await gateway.close();}
});
