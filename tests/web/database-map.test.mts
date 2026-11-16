import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createDatabaseMap} from '../../apps/local-service/src/database-map/service.mts';
import {m2Fixture} from './m2-fixture.mts';

test('unselected database map exposes candidates as metadata without opening a database',async t=>{
 const f=await m2Fixture(t),store={project:(id:string)=>f.store.project(id),readProjectState:async()=>null,writeProjectState:async()=>{throw Error('unexpected_write');}},map=createDatabaseMap({store,profileDatabasePath:f.root+'/state.sqlite'}),status=await map.status('p');
 assert.equal(status?.state,'unselected');assert.equal(status?.source,null);assert.equal(status?.snapshotRevision,null);
 assert.ok(!status?.candidates.some(c=>c.relativePath==='state.sqlite'));
});

import {mkdir,writeFile,rename} from 'node:fs/promises';
import {join} from 'node:path';
import {acquireDatabaseLease} from '../../apps/local-service/src/database-map/lease.mts';
test('native database lease blocks target writes and root/parent/source replacement until release',async t=>{
 const f=await m2Fixture(t);await mkdir(join(f.root,'db'));const path=join(f.root,'db','sample.db');await writeFile(path,'synthetic');
 const lease=await acquireDatabaseLease({root:f.root,path,powershellExecutable:process.env.PAOS_TEST_PWSH});
 try{assert.equal(lease.pins.length,3);await assert.rejects(writeFile(path,'changed'));await assert.rejects(rename(path,path+'.old'));await assert.rejects(rename(join(f.root,'db'),join(f.root,'db-old')));await assert.rejects(rename(f.root,f.root+'-old'));}
 finally{await lease.release();}
 await writeFile(path,'released');
});

import {DatabaseSync} from 'node:sqlite';
import {extractDatabaseMetadata} from '../../apps/local-service/src/database-map/extractor.mts';
import {DATABASE_MAP_LIMITS} from '../../apps/local-service/src/database-map/service.mts';
test('fixed SQLite metadata retains effective nullability, generated columns, composite FK order and index direction without rows/defaults/DDL',async t=>{
 const f=await m2Fixture(t),path=join(f.root,'schema.db'),db=new DatabaseSync(path);
 db.exec("CREATE TABLE parent(a INTEGER,b TEXT,PRIMARY KEY(a,b)) WITHOUT ROWID; CREATE TABLE child(id INTEGER PRIMARY KEY,a INTEGER,b TEXT,secret TEXT DEFAULT 'synthetic-do-not-export',calc TEXT GENERATED ALWAYS AS (b||'x') STORED,FOREIGN KEY(a,b) REFERENCES parent(a,b)); CREATE INDEX reverse_child ON child(b DESC,a); CREATE TABLE nullable_desc(id INTEGER PRIMARY KEY DESC); CREATE VIEW selected_view AS SELECT secret FROM child; INSERT INTO child(id,secret) VALUES(1,'synthetic-row-canary');");db.close();
 const result=extractDatabaseMetadata(path,DATABASE_MAP_LIMITS),child=result.tables.find(x=>x.name==='child')!;
 assert.equal(child.columns[0].nullable,false);assert.equal(child.columns[0].rowidAlias,true);assert.equal(child.columns.find(x=>x.name==='calc')!.generated,true);
 assert.deepEqual(child.foreignKeys.map(x=>[x.sequence,x.from,x.to]),[[0,'a','a'],[1,'b','b']]);assert.equal(child.indexes[0].columns[0].descending,true);assert.equal(child.indexes[0].columns.at(-1)!.rowid,true);
 assert.equal(result.tables.find(x=>x.name==='nullable_desc')!.columns[0].nullable,true);assert.equal(result.tables.find(x=>x.name==='parent')!.columns[0].nullable,false);
 assert.deepEqual(result.tables.find(x=>x.name==='selected_view')!.reasons,['VIEW_NOT_EXPANDED']);assert.ok(!JSON.stringify(result).includes('synthetic-do-not-export'));assert.ok(!JSON.stringify(result).includes('synthetic-row-canary'));
});

import {open,symlink,link} from 'node:fs/promises';
import {runSchemaExtractor} from '../../apps/local-service/src/database-map/runner.mts';
test('native lease rejects an existing writer, hardlink and reparse parent, and abort releases owned handles',async t=>{
 const f=await m2Fixture(t),path=join(f.root,'lease.db');await writeFile(path,'synthetic');
 const writer=await open(path,'r+');try{await assert.rejects(acquireDatabaseLease({root:f.root,path,powershellExecutable:process.env.PAOS_TEST_PWSH}),{code:'DATABASE_LEASE_DENIED'});}finally{await writer.close();}
 await link(path,path+'.hard');await assert.rejects(acquireDatabaseLease({root:f.root,path,powershellExecutable:process.env.PAOS_TEST_PWSH}),{code:'DATABASE_LEASE_SCOPE_INVALID'});
 await mkdir(join(f.root,'actual'));await writeFile(join(f.root,'actual','nested.db'),'synthetic');await symlink(join(f.root,'actual'),join(f.root,'junction'),'junction');
 await assert.rejects(acquireDatabaseLease({root:f.root,path:join(f.root,'junction','nested.db'),powershellExecutable:process.env.PAOS_TEST_PWSH}),{code:'DATABASE_LEASE_SCOPE_INVALID'});
 const controller=new AbortController(),lease=await acquireDatabaseLease({root:f.root,path:join(f.root,'actual','nested.db'),signal:controller.signal,powershellExecutable:process.env.PAOS_TEST_PWSH});controller.abort();await lease.lost;await lease.release();await writeFile(join(f.root,'actual','nested.db'),'released');
});
test('owned SQLite child is cancelled/deadline-bounded before file lease release',async t=>{
 const f=await m2Fixture(t),path=join(f.root,'schema.db'),db=new DatabaseSync(path);db.exec('CREATE TABLE sample(id INTEGER PRIMARY KEY)');db.close();
 let lease=await acquireDatabaseLease({root:f.root,path,powershellExecutable:process.env.PAOS_TEST_PWSH});try{const result=await runSchemaExtractor(path,DATABASE_MAP_LIMITS,lease);assert.equal(result.tables[0].name,'sample');}finally{await lease.release();}
 lease=await acquireDatabaseLease({root:f.root,path,powershellExecutable:process.env.PAOS_TEST_PWSH});try{await assert.rejects(runSchemaExtractor(path,{...DATABASE_MAP_LIMITS,milliseconds:1},lease),{code:'DATABASE_SCHEMA_TIMEOUT'});}finally{await lease.release();}
 await writeFile(path,'released');
});

import {inventoryForProject} from '../../apps/local-service/src/code-index/sources.mts';
async function mapFixture(t:any,limits?:Partial<typeof DATABASE_MAP_LIMITS>){
 const f=await m2Fixture(t),store=f.store;
 const map=createDatabaseMap({store,profileDatabasePath:join(f.root,'state.sqlite'),powershellExecutable:process.env.PAOS_TEST_PWSH,limits});
 const context=async()=>{const project=(await f.store.project('p'))!;return {project,inventory:await inventoryForProject(project).snapshot(project),signal:new AbortController().signal,publicationGuard:async()=>{},canPublish:()=>true,onProgress:async()=>{}};};
 return {...f,map,store,context};
}
test('late source revocation invalidates schema and diff reads before returning metadata as current',async t=>{
 for(const operation of ['snapshot','changes'] as const){
  const f=await mapFixture(t),path=join(f.root,'domain.db'),db=new DatabaseSync(path);db.exec('CREATE TABLE users(id INTEGER PRIMARY KEY)');db.close();
  const select=async()=>{const status=await f.map.status('p'),candidate=status.candidates.find(c=>c.relativePath==='domain.db')!;await f.map.selectSource('p',{relativePath:candidate.relativePath,expectedFileRevision:candidate.fileRevision,expectedVersion:status.version});await f.map.analyzer(await f.context());};
  await select();const change=new DatabaseSync(path);change.exec('CREATE TABLE added(id INTEGER)');change.close();await select();
  let projects=0;const store={...f.store,project:async(id:string)=>{const current=await f.store.project(id);if(++projects===3){const status=await f.map.status(id);await f.map.selectSource(id,{clear:true,expectedVersion:status.version});}return current;}};
  const map=createDatabaseMap({store,profileDatabasePath:join(f.root,'state.sqlite')});await assert.rejects(map[operation]('p'),{code:'DATABASE_SOURCE_SELECTION_STALE'});
 }
});
test('explicit source selection produces schema snapshots, scoped pages/Mermaid, stale state and compatible two-snapshot changes',async t=>{
 const f=await mapFixture(t),path=join(f.root,'domain.db'),db=new DatabaseSync(path);db.exec('CREATE TABLE parent(id INTEGER PRIMARY KEY); CREATE TABLE child(parent_id INTEGER REFERENCES parent, value TEXT GENERATED ALWAYS AS (parent_id||\'x\') VIRTUAL);');db.close();
 const initial=await f.map.status('p'),candidate=initial.candidates.find(c=>c.relativePath==='domain.db')!;
 const selected=await f.map.selectSource('p',{relativePath:candidate.relativePath,expectedFileRevision:candidate.fileRevision,expectedVersion:initial.version});assert.equal(selected.state,'selected');
 const report=await f.map.analyzer(await f.context());assert.equal(report.state,'completed');assert.ok(report.data?.snapshotRevision);assert.ok(Buffer.byteLength(JSON.stringify(report))<4096);
 const ready=await f.map.status('p');assert.equal(ready.state,'ready');const page=await f.map.snapshot('p',new URLSearchParams({revision:ready.snapshotRevision!,limit:'1'}));assert.equal(page.tables.length,1);assert.equal(page.total,2);assert.ok(page.nextCursor);assert.ok(page.mermaid.startsWith('erDiagram\n'));
 const second=await f.map.snapshot('p',new URLSearchParams({revision:ready.snapshotRevision!,limit:'1',cursor:page.nextCursor!}));assert.notEqual(second.tables[0].name,page.tables[0].name);
 const child=(await f.map.snapshot('p',new URLSearchParams({table:'child'}))).tables[0];assert.equal(child.foreignKeys[0].to,'id');assert.equal(child.foreignKeys[0].targetResolution,'primary_key');assert.equal((await f.map.changes('p')).state,'unavailable');
 const change=new DatabaseSync(path);change.exec('CREATE TABLE added(id TEXT)');change.close();assert.equal((await f.map.status('p')).state,'stale');assert.equal((await f.map.snapshot('p')).state,'stale');
 const latest=await f.map.status('p'),observed=latest.candidates.find(c=>c.relativePath==='domain.db')!;await f.map.selectSource('p',{relativePath:observed.relativePath,expectedFileRevision:observed.fileRevision,expectedVersion:latest.version});
 await f.map.analyzer(await f.context());const diff=await f.map.changes('p');assert.deepEqual(diff.added,['added']);assert.deepEqual(diff.removed,[]);
 const restarted=createDatabaseMap({store:f.store,profileDatabasePath:join(f.root,'state.sqlite')});assert.equal((await restarted.status('p')).state,'ready');
 await f.map.selectSource('p',{clear:true,expectedVersion:(await f.map.status('p')).version});assert.equal((await f.map.status('p')).state,'unselected');await assert.rejects(f.map.snapshot('p'),{code:'DATABASE_SCHEMA_NOT_OBSERVED'});
});
test('schema registration rejects the profile database, stale revisions and unsupported source bytes before native extraction',async t=>{
 const f=await mapFixture(t);await assert.rejects(f.map.selectSource('p',{relativePath:'state.sqlite',expectedFileRevision:'a'.repeat(64),expectedVersion:0}),{code:'DATABASE_PROFILE_SOURCE_FORBIDDEN'});
 await writeFile(join(f.root,'bad.db'),'corrupt');const candidate=(await f.map.status('p')).candidates.find(c=>c.relativePath==='bad.db')!;await assert.rejects(f.map.selectSource('p',{relativePath:'bad.db',expectedFileRevision:candidate.fileRevision,expectedVersion:0}),{code:'INVENTORY_DATABASE_FORMAT_UNSUPPORTED'});
 await assert.rejects(f.map.selectSource('p',{relativePath:'bad.db',expectedFileRevision:'b'.repeat(64),expectedVersion:0}),{code:'INVENTORY_REVISION_STALE'});
});
test('selection revoke during a scan fences publication and does not replace the cleared schema state',async t=>{
 const f=await mapFixture(t),path=join(f.root,'domain.db'),db=new DatabaseSync(path);db.exec('CREATE TABLE sample(id INTEGER)');db.close();const first=await f.map.status('p');await f.map.selectSource('p',{relativePath:'domain.db',expectedFileRevision:first.candidates.find(c=>c.relativePath==='domain.db')!.fileRevision,expectedVersion:0});
 const context=await f.context();let calls=0,release!:()=>void,started!:()=>void;const gate=new Promise<void>(r=>{release=r;}),readiness=new Promise<void>(r=>{started=r;});context.publicationGuard=async()=>{if(++calls===2){started();await gate;}};
 const pending=f.map.analyzer(context);await readiness;await f.map.selectSource('p',{clear:true,expectedVersion:(await f.map.status('p')).version});release();await assert.rejects(pending,{code:'DATABASE_SOURCE_SELECTION_STALE'});assert.equal((await f.map.status('p')).snapshotRevision,null);
});

import {metadataAuthorizer} from '../../apps/local-service/src/database-map/extractor.mts';
test('installed SQLite authorizer permits metadata but denies rows, attachments, DDL and extension functions',()=>{
 const db=new DatabaseSync(':memory:');try{db.exec("CREATE TABLE private_rows(value TEXT);INSERT INTO private_rows VALUES('synthetic-row-canary')");db.setAuthorizer(metadataAuthorizer());assert.equal((db.prepare("SELECT name,type FROM sqlite_schema WHERE name='private_rows'").get() as any).name,'private_rows');
 for(const sql of ['SELECT value FROM private_rows',"ATTACH DATABASE ':memory:' AS other",'CREATE TABLE denied(id INTEGER)',"SELECT load_extension('synthetic-do-not-load')",'PRAGMA writable_schema=ON'])assert.throws(()=>db.prepare(sql).all());
 }finally{db.close();}
});
test('extractor enforces distinct table, column, foreign-key and index-part metadata budgets',async t=>{
 const f=await m2Fixture(t),path=join(f.root,'limits.db');let db=new DatabaseSync(path);db.exec(Array.from({length:201},(_,i)=>'CREATE TABLE t'+i+'(id INTEGER);').join(''));db.close();assert.throws(()=>extractDatabaseMetadata(path,DATABASE_MAP_LIMITS),{code:'DATABASE_SCHEMA_TABLE_LIMIT'});
 let budgetCase=0;for(const [sql,expected] of [
  [Array.from({length:3},(_,t)=>'CREATE TABLE columns'+t+'('+Array.from({length:1400},(_,i)=>'c'+i+' TEXT').join(',')+');').join(''),'DATABASE_SCHEMA_COLUMN_LIMIT'],
  ['CREATE TABLE parent(id INTEGER PRIMARY KEY);CREATE TABLE refs(id INTEGER,'+Array.from({length:1025},()=> 'FOREIGN KEY(id) REFERENCES parent(id)').join(',')+');','DATABASE_SCHEMA_FOREIGN_KEY_LIMIT'],
  ['CREATE TABLE indexes('+Array.from({length:1500},(_,i)=>'c'+i+' TEXT').join(',')+');'+Array.from({length:3},(_,i)=>'CREATE INDEX idx'+i+' ON indexes('+Array.from({length:1500},(_,c)=>'c'+c).join(',')+');').join(''),'DATABASE_SCHEMA_INDEX_LIMIT']
 ]){const unique=path+(++budgetCase)+'.db';db=new DatabaseSync(unique);db.exec(sql);db.close();assert.throws(()=>extractDatabaseMetadata(unique,DATABASE_MAP_LIMITS),{code:expected});}
});

import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {unlink,lstat} from 'node:fs/promises';
async function reparseProbe(path:string,target:string){return new Promise<string>((accept,reject)=>{const child=spawn(process.env.PAOS_TEST_PWSH??join(process.env.SystemRoot!,'System32','WindowsPowerShell','v1.0','powershell.exe'),['-NoLogo','-NoProfile','-NonInteractive','-File',fileURLToPath(new URL('./fixtures/database-reparse-probe.ps1',import.meta.url))],{windowsHide:true,shell:false,stdio:['pipe','pipe','pipe']});let output='',errors='';child.stdout.on('data',c=>{output+=c;});child.stderr.on('data',c=>{errors+=c;});child.once('error',reject);child.once('close',code=>code===0?accept(output.trim()):reject(Error('synthetic_reparse_probe_failed:'+errors.slice(0,200))));child.stdin.end(JSON.stringify({path,target}));});}
test('native directory lease blocks in-place reparse mutation with an independent working control',async t=>{
 const f=await m2Fixture(t),parent=join(f.root,'parent'),target=join(f.root,'target');await mkdir(parent);await mkdir(target);const path=join(parent,'source.db');await writeFile(path,'synthetic');
 const lease=await acquireDatabaseLease({root:f.root,path,powershellExecutable:process.env.PAOS_TEST_PWSH});try{assert.equal(await reparseProbe(parent,target),'OPEN_DENIED:32');assert.equal((await lstat(parent)).isSymbolicLink(),false);}finally{await lease.release();}
 await unlink(path);assert.equal(await reparseProbe(parent,target),'REPARSE_SET');assert.equal((await lstat(parent)).isSymbolicLink(),true);await unlink(parent);
});

import {readFile,readdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
test('200-table schema scan stays bounded and leaves the selected offline database and sidecar directory unchanged',async t=>{
 const f=await m2Fixture(t),target=join(f.root,'target');await mkdir(target);const path=join(target,'domain.db'),db=new DatabaseSync(path);db.exec(Array.from({length:200},(_,i)=>'CREATE TABLE t'+i+'(id INTEGER PRIMARY KEY,parent_id INTEGER'+(i?' REFERENCES t'+(i-1)+'(id)':'')+');').join(''));db.close();
 const pin=await bindProject('q',target);await f.store.registerProject({id:'q',keyPrefix:'DBMP',canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'sql'});
 const map=createDatabaseMap({store:f.store,profileDatabasePath:join(f.root,'state.sqlite'),powershellExecutable:process.env.PAOS_TEST_PWSH}),initial=await map.status('q');await map.selectSource('q',{relativePath:'domain.db',expectedFileRevision:initial.candidates[0].fileRevision,expectedVersion:0});
 const before=createHash('sha256').update(await readFile(path)).digest('hex'),entries=await readdir(target),project=(await f.store.project('q'))!,started=performance.now();
 const result=await map.analyzer({project,inventory:await inventoryForProject(project).snapshot(project),signal:new AbortController().signal,publicationGuard:async()=>{},canPublish:()=>true,onProgress:async()=>{}});assert.equal(result.state,'completed');const page=await map.snapshot('q',new URLSearchParams({limit:'200'}));assert.equal(page.tables.length,200);assert.equal(page.tables.reduce((n,t)=>n+t.foreignKeys.length,0),199);assert.ok(Buffer.byteLength(JSON.stringify(page))<=524288);
 assert.equal(createHash('sha256').update(await readFile(path)).digest('hex'),before);assert.deepEqual(await readdir(target),entries);t.diagnostic(JSON.stringify({workload:'sqlite200',elapsedMs:performance.now()-started,responseBytes:Buffer.byteLength(JSON.stringify(page)),nativeRssMeasured:false}));
});
test('output-limit and cancellation retain explicit outcomes and cannot publish after a policy change',async t=>{
 const f=await mapFixture(t,{outputBytes:100}),path=join(f.root,'domain.db'),db=new DatabaseSync(path);db.exec('CREATE TABLE sample(id INTEGER PRIMARY KEY,value TEXT)');db.close();let status=await f.map.status('p');await f.map.selectSource('p',{relativePath:'domain.db',expectedFileRevision:status.candidates.find(c=>c.relativePath==='domain.db')!.fileRevision,expectedVersion:0});
 const report=await f.map.analyzer(await f.context());assert.equal(report.state,'unavailable');assert.ok(report.reasons.includes('DATABASE_SCHEMA_OUTPUT_LIMIT'));assert.equal((await f.map.status('p')).snapshotRevision,null);
 const controller=new AbortController();controller.abort();await assert.rejects(f.map.analyzer({...await f.context(),signal:controller.signal}),{code:'DATABASE_SCHEMA_CANCELLED'});
 await f.store.writeProjectState('p','project_inventory_policy_v1',0,{schemaVersion:'paos_inventory_policy_v1',policy:{exclude:['domain.db']}});status=await f.map.status('p');assert.equal(status.state,'stale');
});


test('owned child watchdog kills a native-blocked main thread on deadline and after parent death',async()=>{
 const module=new URL('../../apps/local-service/src/database-map/watchdog.mts',import.meta.url).href;
 const blocked=(milliseconds:number)=>`const {startSchemaWatchdog}=await import(${JSON.stringify(module)});await startSchemaWatchdog(${milliseconds});Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0);`;
 let child=spawn(process.execPath,['--input-type=module','-e',blocked(50)],{stdio:'ignore',windowsHide:true});const began=performance.now();let forced=false;const cleanup=setTimeout(()=>{forced=true;child.kill('SIGKILL');},3000);await new Promise<void>((accept,reject)=>{child.once('error',reject);child.once('close',()=>accept());});clearTimeout(cleanup);assert.equal(forced,false);assert.ok(performance.now()-began<3000);
 const parentCode=`const {spawn}=await import('node:child_process');const child=spawn(process.execPath,['--input-type=module','-e',${JSON.stringify(blocked(5000))}],{stdio:'ignore',windowsHide:true});process.stdout.write(String(child.pid)+'\\n');setInterval(()=>{},1000);`;
 const parent=spawn(process.execPath,['--input-type=module','-e',parentCode],{stdio:['ignore','pipe','ignore'],windowsHide:true});let pid=0;
 try{pid=await new Promise<number>((accept,reject)=>{let text='';parent.stdout!.on('data',chunk=>{text+=chunk;const parsed=Number.parseInt(text,10);if(parsed)accept(parsed);});parent.once('error',reject);});await new Promise(r=>setTimeout(r,150));parent.kill();await new Promise<void>(r=>parent.once('close',()=>r()));const deadline=Date.now()+3000;let alive=true;while(Date.now()<deadline){try{process.kill(pid,0);}catch{alive=false;break;}await new Promise(r=>setTimeout(r,20));}assert.equal(alive,false,'owned blocked child must exit after parent death');}
 finally{parent.kill();if(pid)try{process.kill(pid);}catch{}}
});


import {databaseMermaid} from '../../apps/local-service/src/database-map/mermaid.mts';
test('canonical Mermaid retains readable aliases while hostile names cannot inject HTML or diagram syntax',()=>{
 const encoded=databaseMermaid([{name:'Customer Account',kind:'table',withoutRowid:false,strict:false,columns:[{name:'id',type:'INTEGER',nullable:false,notNullDeclared:false,rowidAlias:true,primaryKeyPosition:1,generated:false,hidden:0}],foreignKeys:[],indexes:[],reasons:[]},{name:'bad"<script>\n} evil[',kind:'table',withoutRowid:false,strict:false,columns:[],foreignKeys:[],indexes:[],reasons:[]}]);
 assert.ok(encoded.includes('["Customer Account"]'));assert.ok(encoded.includes('INTEGER c_6964 PK "id"'));assert.ok(!encoded.includes('<script>'));assert.ok(!encoded.includes('\n} evil['));assert.ok(encoded.includes('#34;#60;script#62;#10;#125; evil#91;'));
});
