import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp, mkdir, writeFile, readFile, rm, rename, link, symlink} from 'node:fs/promises';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {createProjectInventory, normaliseRelativePath} from '../../apps/local-service/src/project-inventory/service.mts';

async function fixture(t:any){const root=await mkdtemp(join(tmpdir(),'paos-inventory-'));t.after(()=>rm(root,{recursive:true,force:true}));const binding=await bindProject('p',root);return {root,project:{id:'p',canonicalRoot:binding.workspaceRoot,rootIdentity:binding.directoryIdentity}};}

test('directory metadata includes unsupported files and empty folders without indexing or reading their bytes', async t => {
  const root = await mkdtemp(join(tmpdir(),'paos-inventory-'));
  t.after(()=>rm(root,{recursive:true,force:true}));
  await mkdir(join(root,'empty')); await writeFile(join(root,'unknown.xyz'),Buffer.from([0,255,1]));
  const binding=await bindProject('p',root),project={id:'p',canonicalRoot:binding.workspaceRoot,rootIdentity:binding.directoryIdentity};
  const result=await createProjectInventory().listDirectory(project);
  assert.deepEqual(result.entries.map(x=>x.relativePath),['empty','unknown.xyz']);
  assert.equal(result.counts.discovered,2);assert.equal(result.counts.unsupported,1);
  assert.equal(result.counts.readable,null);assert.equal(result.counts.indexed,null);
});

test('gitignore uses nested precedence, negation and excluded parent semantics while keeping metadata visible',async t=>{
 const {root,project}=await fixture(t);await mkdir(join(root,'nested'));await mkdir(join(root,'blocked'));
 await writeFile(join(root,'.gitignore'),'*.log\n!keep.log\nblocked/\n!blocked/child.ts\n');
 await writeFile(join(root,'nested','.gitignore'),'!inside.log\n');
 for(const name of ['omit.log','keep.log','nested/inside.log','nested/omit.log','blocked/child.ts'])await writeFile(join(root,name),'ordinary text');
 const api=createProjectInventory(),snapshot=await api.snapshot(project),byPath=new Map(snapshot.entries.map(e=>[e.relativePath,e]));
 assert.equal(byPath.get('omit.log')!.access.reason,'gitignore');assert.equal(byPath.get('keep.log')!.access.readable,true);
 assert.equal(byPath.get('nested/inside.log')!.access.readable,true);assert.equal(byPath.get('nested/omit.log')!.access.reason,'gitignore');
 assert.equal(byPath.has('blocked/child.ts'),false);assert.ok(snapshot.reasons.includes('excluded_subtree:gitignore'));
 await assert.rejects(api.read(project,{path:'blocked/child.ts'}),{code:'INVENTORY_SOURCE_FORBIDDEN'});
});

test('gitignore wildcard rules include dotfiles and distinguish anchored, escaped and globstar patterns',async t=>{
 const {root,project}=await fixture(t);await mkdir(join(root,'nested'));await mkdir(join(root,'cache'));
 await writeFile(join(root,'.gitignore'),'*.tmp\n/root.txt\n\\#literal\n\\!literal\n**/cache/*.js\n');
 for(const name of ['.hidden.tmp','root.txt','nested/root.txt','#literal','!literal','cache/a.js','cache/a.ts'])await writeFile(join(root,name),'text');
 const api=createProjectInventory(),snap=await api.snapshot(project),paths=new Map(snap.entries.map(e=>[e.relativePath,e]));
 for(const path of ['.hidden.tmp','root.txt','#literal','!literal','cache/a.js'])assert.equal(paths.get(path)!.access.reason,'gitignore',path);
 assert.equal(paths.get('nested/root.txt')!.access.readable,true);assert.equal(paths.get('cache/a.ts')!.access.indexable,true);
});

test('project excludes outrank includes and includes never override sensitive or database content denial',async t=>{
 const {root,project}=await fixture(t);await writeFile(join(root,'.gitignore'),'*.ts\n');
 for(const name of ['allowed.ts','denied.ts','.env','.npmrc','auth.json','private.key','schema.db'])await writeFile(join(root,name),'ordinary fixture');
 const api=createProjectInventory({policy:{include:['*'],exclude:['denied.ts']}}),rows=(await api.listDirectory(project)).entries;
 assert.equal(rows.find(e=>e.name==='allowed.ts')!.access.indexable,true);assert.equal(rows.find(e=>e.name==='denied.ts')!.access.reason,'project_exclude');
 for(const path of ['.env','.npmrc','auth.json','private.key','schema.db']){assert.equal(rows.find(e=>e.name===path)!.access.readable,false);await assert.rejects(api.read(project,{path}),{code:'INVENTORY_SOURCE_FORBIDDEN'});}
});

test('inspect, directory and read use the same project/path/policy revision with Unicode and inert HTML',async t=>{
 const {root,project}=await fixture(t);await mkdir(join(root,'данные'));await writeFile(join(root,'данные','имя с пробелом.html'),'<script>never execute()</script>\r\nтекст');
 const api=createProjectInventory(),page=await api.listDirectory(project,{path:'данные'}),entry=await api.inspect(project,'данные/имя с пробелом.html');
 assert.equal(entry.revision,page.entries[0].revision);const read=await api.read(project,{path:'данные\\имя с пробелом.html',revision:entry.revision});
 assert.equal(read.fileRevision,entry.revision);assert.equal(read.text,'<script>never execute()</script>\r\nтекст');assert.equal(read.policyVersion,page.policyVersion);
 assert.equal(JSON.stringify(page).includes(root),false);assert.equal(normaliseRelativePath('a\\b.ts'),'a/b.ts');
});

test('file, ignore and configured-policy changes invalidate prior source pins without reading every source',async t=>{
 const {root,project}=await fixture(t);await writeFile(join(root,'file.ts'),'let ordinary=1;');await writeFile(join(root,'.gitignore'),'# first\n');
 const api=createProjectInventory(),first=await api.inspect(project,'file.ts'),oldSnapshot=await api.snapshot(project);
 await writeFile(join(root,'file.ts'),'let ordinary=2;');await assert.rejects(api.read(project,{path:'file.ts',revision:first.revision}),{code:'INVENTORY_REVISION_STALE'});
 const second=await api.inspect(project,'file.ts');await writeFile(join(root,'.gitignore'),'# second\n');await assert.rejects(api.read(project,{path:'file.ts',revision:second.revision}),{code:'INVENTORY_REVISION_STALE'});
 const newSnapshot=await api.snapshot(project);assert.notEqual(newSnapshot.revision,oldSnapshot.revision);assert.equal(newSnapshot.policyVersion,oldSnapshot.policyVersion);assert.notEqual(newSnapshot.ignoreRevision,oldSnapshot.ignoreRevision);
 const third=await api.inspect(project,'file.ts'),different=createProjectInventory({policy:{version:'other'}});await assert.rejects(different.read(project,{path:'file.ts',revision:third.revision}),{code:'INVENTORY_REVISION_STALE'});
});

test('binary, encoding, oversize and recognized credential content failures keep ordinary metadata and reads available',async t=>{
 const {root,project}=await fixture(t);await writeFile(join(root,'normal.txt'),'safe text');await writeFile(join(root,'binary.txt'),Buffer.from([65,0,66]));await writeFile(join(root,'encoding.txt'),Buffer.from([255]));await writeFile(join(root,'large.txt'),'x'.repeat(512*1024+1));await writeFile(join(root,'credential.txt'),'api_key = synthetic_canary_value');
 const api=createProjectInventory(),snapshot=await api.snapshot(project);assert.equal(snapshot.entries.length,5);assert.equal((await api.read(project,{path:'normal.txt'})).text,'safe text');
 for(const [path,code] of [['binary.txt','INVENTORY_BINARY_FILE'],['encoding.txt','INVENTORY_ENCODING_UNSUPPORTED'],['large.txt','INVENTORY_FILE_TOO_LARGE'],['credential.txt','INVENTORY_SENSITIVE_CONTENT']])await assert.rejects(api.read(project,{path}),{code});
 assert.equal((await api.listDirectory(project)).entries.length,5);
});

test('directory cursors bind project, policy, revision, filters and pagination without accepting tampering',async t=>{
 const {root,project}=await fixture(t);for(const name of ['AGENTS.md','a.txt','b.txt'])await writeFile(join(root,name),'text');const api=createProjectInventory(),one=await api.listDirectory(project,{limit:1});assert.ok(one.nextCursor);
 const two=await api.listDirectory(project,{limit:1,cursor:one.nextCursor!});assert.notEqual(two.entries[0].relativePath,one.entries[0].relativePath);assert.equal(two.searchScope,'directory');
 await assert.rejects(api.listDirectory({...project,id:'other'},{limit:1,cursor:one.nextCursor!}),{code:'INVENTORY_CURSOR_STALE'});
 await assert.rejects(api.listDirectory(project,{limit:1,cursor:one.nextCursor!+'x'}),{code:'INVENTORY_CURSOR_INVALID'});
 await assert.rejects(api.listDirectory(project,{limit:2,cursor:one.nextCursor!}),{code:'INVENTORY_CURSOR_STALE'});
 await writeFile(join(root,'c.txt'),'text');await assert.rejects(api.listDirectory(project,{limit:1,cursor:one.nextCursor!}),{code:'INVENTORY_CURSOR_STALE'});
 assert.deepEqual((await api.listDirectory(project,{filter:'control_plane'})).entries.map(e=>e.name),['AGENTS.md']);assert.equal((await api.listDirectory(project,{query:'b.txt'})).total,1);
});

test('limits return explicit partial metadata and cancelled snapshots never publish success',async t=>{
 const {root,project}=await fixture(t);for(const name of ['a.txt','b.txt','c.txt'])await writeFile(join(root,name),'text');
 const limited=await createProjectInventory({limits:{directoryEntries:2}}).listDirectory(project);assert.equal(limited.entries.length,2);assert.equal(limited.coverage,'partial');assert.ok(limited.reasons.includes('directory_entry_limit'));
 const snapshot=await createProjectInventory({limits:{files:1}}).snapshot(project);assert.equal(snapshot.entries.length,1);assert.equal(snapshot.coverage,'partial');
 await assert.rejects(createProjectInventory().snapshot(project,{signal:AbortSignal.abort()}),{code:'INVENTORY_CANCELLED'});
});

test('path/root identity denial and linked files cannot widen reading or listing authority',async t=>{
 const {root,project}=await fixture(t),outside=await mkdtemp(join(tmpdir(),'paos-inventory-outside-'));t.after(()=>rm(outside,{recursive:true,force:true}));await writeFile(join(outside,'foreign.txt'),'foreign contents');
 const api=createProjectInventory();for(const path of ['../foreign.txt','/foreign.txt','C:\\foreign.txt','a/../b','a//b','a:stream'])await assert.rejects(api.read(project,{path}),{code:'INVENTORY_PATH_FORBIDDEN'});
 await link(join(outside,'foreign.txt'),join(root,'linked.txt'));await symlink(outside,join(root,'junction'),'junction');
 const page=await api.listDirectory(project);for(const name of ['linked.txt','junction'])assert.equal(page.entries.find(e=>e.name===name)!.access.reason,'linked_source');
 await assert.rejects(api.read(project,{path:'linked.txt'}),{code:'INVENTORY_LINKED_SOURCE'});await assert.rejects(api.read(project,{path:'junction/foreign.txt'}),{code:'INVENTORY_LINKED_SOURCE'});
 await assert.rejects(api.listDirectory(project,{path:'junction'}),{code:'INVENTORY_LINKED_SOURCE'});
 const old=root+'-old';await rename(root,old);t.after(()=>rm(old,{recursive:true,force:true}));await mkdir(root);await assert.rejects(api.snapshot(project),{code:'PROJECT_ROOT_UNAVAILABLE'});
});

test('invalid policy is rejected and unsupported ignore syntax denies content only inside its scope',async t=>{
 const {root,project}=await fixture(t);await mkdir(join(root,'nested'));await writeFile(join(root,'normal.ts'),'let ordinary=1;');await writeFile(join(root,'nested','.gitignore'),'[[:digit:]]\n');await writeFile(join(root,'nested','inside.ts'),'let ordinary=2;');
 for(const policy of [{include:'*'},{respectGitignore:'yes'},{arbitrary:true},{exclude:['../private']}])assert.throws(()=>createProjectInventory({policy:policy as any}),{code:'INVENTORY_POLICY_INVALID'});
 const api=createProjectInventory(),snap=await api.snapshot(project);assert.equal(snap.coverage,'partial');assert.ok(snap.reasons.includes('gitignore_pattern_unsupported'));assert.equal((await api.read(project,{path:'normal.ts'})).text,'let ordinary=1;');
 await assert.rejects(api.read(project,{path:'nested/inside.ts'}),{code:'INVENTORY_SOURCE_FORBIDDEN'});
});

test('metadata, content reads and policy interpretation leave original source/config bytes unchanged',async t=>{
 const {root,project}=await fixture(t);const source='export const ordinary=1;\n',ignore='*.log\n';await writeFile(join(root,'source.ts'),source);await writeFile(join(root,'.gitignore'),ignore);
 const api=createProjectInventory();await api.snapshot(project);const entry=await api.inspect(project,'source.ts');await api.read(project,{path:'source.ts',revision:entry.revision});
 assert.equal(await readFile(join(root,'source.ts'),'utf8'),source);assert.equal(await readFile(join(root,'.gitignore'),'utf8'),ignore);
});

test('document-only redaction preserves raw byte identity while default reads and private-key content remain denied',async t=>{
 const {root,project}=await fixture(t);const text='api_key = synthetic_fixture_credential\n# ordinary document';await writeFile(join(root,'report.md'),text);await writeFile(join(root,'private.md'),'-----BEGIN PRIVATE KEY-----\nsynthetic fixture\n-----END PRIVATE KEY-----');await writeFile(join(root,'partial.md'),'-----BEGIN PRIVATE KEY-----\ntruncated synthetic fixture');await writeFile(join(root,'.env'),'api_key = synthetic_fixture');
 const api=createProjectInventory(),entry=await api.inspect(project,'report.md');await assert.rejects(api.read(project,{path:'report.md'}),{code:'INVENTORY_SENSITIVE_CONTENT'});
 const displayed=await api.read(project,{path:'report.md',revision:entry.revision,redactSensitive:true});assert.equal(displayed.redacted,true);assert.equal(displayed.text,'api_key = [redacted]\n# ordinary document');assert.equal(displayed.byteSize,Buffer.byteLength(text));assert.equal(displayed.fileRevision,entry.revision);assert.equal(await readFile(join(root,'report.md'),'utf8'),text);
 await assert.rejects(api.read(project,{path:'private.md',redactSensitive:true}),{code:'INVENTORY_SENSITIVE_CONTENT'});await assert.rejects(api.read(project,{path:'.env',redactSensitive:true}),{code:'INVENTORY_SOURCE_FORBIDDEN'});
 await assert.rejects(api.read(project,{path:'partial.md',redactSensitive:true}),{code:'INVENTORY_SENSITIVE_CONTENT'});await assert.rejects(api.read(project,{path:'partial.md'}),{code:'INVENTORY_SENSITIVE_CONTENT'});
});

test('bounded responses disclose truncation and targeted includes expose metadata without reading vendor contents',async t=>{
 const {root,project}=await fixture(t);await mkdir(join(root,'vendor'));await writeFile(join(root,'vendor','allowed.ts'),'let ordinary=1;');await writeFile(join(root,'vendor','denied.ts'),'let ordinary=2;');
 const api=createProjectInventory({policy:{include:['vendor/allowed.ts']}}),entries=(await api.listDirectory(project,{path:'vendor'})).entries;assert.equal(entries.length,2);assert.equal(entries.find(e=>e.name==='allowed.ts')!.access.readable,true);assert.equal(entries.find(e=>e.name==='denied.ts')!.access.reason,'generated_or_vendor');
 const generated=createProjectInventory();assert.equal((await generated.listDirectory(project,{path:'vendor'})).entries.length,0);
 for(let i=0;i<30;i++)await writeFile(join(root,String(i).padStart(2,'0')+'-'+'x'.repeat(180)+'.txt'),'text');
 const page=await createProjectInventory({limits:{responseBytes:8192}}).listDirectory(project);assert.equal(page.coverage,'partial');assert.ok(page.reasons.includes('response_byte_limit'));assert.ok(Buffer.byteLength(JSON.stringify(page))<8192);assert.ok(page.nextCursor);
});

test('Windows case-insensitive pins agree and device/ADS/trailing-dot aliases are never relative file references',async t=>{
 const {root,project}=await fixture(t);await mkdir(join(root,'Nested'));await writeFile(join(root,'Nested','.gitignore'),'# scoped\n');await writeFile(join(root,'Nested','Source.ts'),'let ordinary=1;');
 const api=createProjectInventory(),entry=await api.inspect(project,'Nested/Source.ts');
 if(process.platform==='win32'){
  assert.equal((await api.inspect(project,'NESTED/SOURCE.TS')).revision,entry.revision);assert.equal((await api.read(project,{path:'nested/source.ts',revision:entry.revision})).text,'let ordinary=1;');
  for(const path of ['NUL','COM1.txt','ordinary.txt.','ordinary.txt ','source.ts:hidden'])assert.throws(()=>normaliseRelativePath(path),{code:'INVENTORY_PATH_FORBIDDEN'});
 }else assert.equal((await api.read(project,{path:'Nested/Source.ts',revision:entry.revision})).text,'let ordinary=1;');
});

test('virtual create access applies ancestor ignore/policy without opening missing files or creating directories',async t=>{
 const {root,project}=await fixture(t);await writeFile(join(root,'.gitignore'),'*.log\nignored/\n');
 const api=createProjectInventory();assert.equal((await api.access(project,'new/deep/source.ts')).allowed,true);assert.equal((await api.access(project,'new/deep/source.ts')).exists,false);
 await writeFile(join(root,'ordinary.ts'),'let ordinary=1;');assert.equal((await api.access(project,'ordinary.ts')).allowed,true);
 assert.equal((await api.access(project,'new/missing.log')).allowed,false);assert.equal((await api.access(project,'ignored/missing.ts')).allowed,false);assert.equal((await api.access(project,'new/.env')).allowed,false);
 assert.equal((await createProjectInventory({policy:{include:['new/missing.log']}}).access(project,'new/missing.log')).allowed,true);
 await assert.rejects(readFile(join(root,'new','deep','source.ts')),{code:'ENOENT'});
 await assert.rejects(readFile(join(root,'new')),{code:'ENOENT'});
});
