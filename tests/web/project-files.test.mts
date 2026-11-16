import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdir,writeFile,readFile,unlink,link,symlink,rename,mkdtemp,rm} from 'node:fs/promises';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {createHash} from 'node:crypto';
import {m2Fixture} from './m2-fixture.mts';
import {createProjectFiles} from '../../apps/local-service/src/project-files/service.mts';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';

test('registered project exposes a lazy directory before any graph or scan is ready',async t=>{
 const f=await m2Fixture(t);await mkdir(join(f.root,'empty'));await mkdir(join(f.root,'nested'));await writeFile(join(f.root,'nested','source.xyz'),'unknown source');
 const files=createProjectFiles(f.store),root=await files.list('p',new URLSearchParams());
 assert.ok(root.entries.some(e=>e.relativePath==='empty'));
 const nested=await files.list('p',new URLSearchParams({path:'nested'}));assert.deepEqual(nested.entries.map(e=>e.relativePath),['nested/source.xyz']);
});

test('safe text reads carry a raw SHA task reference separately from inventory revision and never evaluate HTML',async t=>{
 const f=await m2Fixture(t),body='<script>globalThis.syntheticFileExecuted=true</script>\r\nтекст';await writeFile(join(f.root,'source.html'),body);
 const files=createProjectFiles(f.store),page=await files.list('p',new URLSearchParams()),entry=page.entries.find(e=>e.name==='source.html')!,result=await files.read('p',{path:'source.html',revision:entry.revision,line:2});
 assert.equal(result.state,'available');if(result.state!=='available')return;
 const expected=createHash('sha256').update(body).digest('hex');assert.equal(result.content,body);assert.equal(result.hash,expected);assert.equal(result.reference.revision,expected);assert.equal(result.reference.revisionKind,'sha256');assert.equal(result.reference.fileRevision,entry.revision);assert.equal(result.reference.rootIdentity,page.rootIdentity);assert.equal(result.reference.policyVersion,page.policyVersion);assert.equal(result.reference.line,2);assert.equal((globalThis as any).syntheticFileExecuted,undefined);assert.equal(await readFile(join(f.root,'source.html'),'utf8'),body);
});

test('stale, missing, binary, oversized, encoding and policy failures are explicit without hiding the tree',async t=>{
 const f=await m2Fixture(t);await writeFile(join(f.root,'stale.txt'),'first');await writeFile(join(f.root,'missing.txt'),'present');await writeFile(join(f.root,'binary.bin'),Buffer.from([1,0,2]));await writeFile(join(f.root,'encoding.txt'),Buffer.from([255]));await writeFile(join(f.root,'large.txt'),'x'.repeat(512*1024+1));await writeFile(join(f.root,'.env'),'API_KEY=synthetic');
 const files=createProjectFiles(f.store),page=await files.list('p',new URLSearchParams()),stale=page.entries.find(e=>e.name==='stale.txt')!,missing=page.entries.find(e=>e.name==='missing.txt')!;
 await writeFile(join(f.root,'stale.txt'),'second');await unlink(join(f.root,'missing.txt'));
 for(const [path,state,revision] of [['stale.txt','stale',stale.revision],['missing.txt','unavailable',missing.revision],['binary.bin','binary'],['encoding.txt','unsupported'],['large.txt','too_large'],['.env','forbidden']]){const result=await files.read('p',{path,revision});assert.equal(result.state,state,path);assert.equal(result.content,null);}
 assert.ok((await files.list('p',new URLSearchParams())).entries.some(e=>e.name==='binary.bin'));
 await f.store.writeProjectState('p','project_inventory_policy_v1',0,{schemaVersion:'paos_inventory_policy_v1',policy:{exclude:['stale.txt']}});
 assert.equal((await files.read('p',{path:'stale.txt'})).state,'forbidden');
});

test('Files display redacts regular documents but denies complete and truncated private keys',async t=>{
 const f=await m2Fixture(t);await writeFile(join(f.root,'report.md'),'token = synthetic_private_value\n# report');await writeFile(join(f.root,'key.md'),'-----BEGIN PRIVATE KEY-----\ntruncated fixture');
 const files=createProjectFiles(f.store),display=await files.read('p',{path:'report.md'});assert.equal(display.state,'available');if(display.state==='available'){assert.equal(display.content,'token = [redacted]\n# report');assert.equal(display.redacted,true);assert.ok(!JSON.stringify(display).includes('synthetic_private_value'));}
 const key=await files.read('p',{path:'key.md'});assert.equal(key.state,'forbidden');assert.equal(key.content,null);
});

test('directory paging/search/filter and registry scoping reject malformed or cross-project requests',async t=>{
 const f=await m2Fixture(t);for(const name of ['AGENTS.md','a.txt','b.txt'])await writeFile(join(f.root,name),'text');const files=createProjectFiles(f.store),first=await files.list('p',new URLSearchParams({limit:'1'}));assert.ok(first.nextCursor);
 const next=await files.list('p',new URLSearchParams({limit:'1',cursor:first.nextCursor!}));assert.notEqual(next.entries[0].relativePath,first.entries[0].relativePath);
 assert.deepEqual((await files.list('p',new URLSearchParams({filter:'control_plane'}))).entries.map(e=>e.name),['AGENTS.md']);assert.equal((await files.list('p',new URLSearchParams({query:'b.txt'}))).total,1);
 for(const input of [{limit:'-1'},{limit:'201'},{workspaceRoot:'C:/outside'},{filter:'unknown'}])await assert.rejects(files.list('p',new URLSearchParams(input)));
 await assert.rejects(files.list('p',new URLSearchParams('path=a&path=b')),{code:'PROJECT_FILES_QUERY_INVALID'});await assert.rejects(files.read('p',{path:'../outside'}),{code:'INVENTORY_PATH_FORBIDDEN'});await assert.rejects(files.read('p',{path:'https://example.com/private'}),{code:'INVENTORY_PATH_FORBIDDEN'});await assert.rejects(files.read('p',{path:'a.txt',line:0}),{code:'PROJECT_FILES_QUERY_INVALID'});await assert.rejects(files.list('unknown',new URLSearchParams()),{code:'PROJECT_NOT_FOUND'});
 const other=await mkdtemp(join(tmpdir(),'paos-files-other-'));t.after(()=>rm(other,{recursive:true,force:true}));await writeFile(join(other,'a.txt'),'other project');const binding=await bindProject('q',other);await f.store.registerProject({id:'q',keyPrefix:'OTHR',canonicalRoot:binding.workspaceRoot,rootIdentity:binding.directoryIdentity,authorityMode:'sql'});
 await assert.rejects(files.list('q',new URLSearchParams({limit:'1',cursor:first.nextCursor!})),{code:'INVENTORY_CURSOR_STALE'});const read=await files.read('q',{path:'a.txt'});assert.equal(read.projectId,'q');assert.equal(read.content,'other project');
});

test('linked entries and replaced roots never open outside content through Files',async t=>{
 const f=await m2Fixture(t),other=await mkdtemp(join(tmpdir(),'paos-files-boundary-'));t.after(()=>rm(other,{recursive:true,force:true}));await writeFile(join(other,'foreign.txt'),'foreign source');await link(join(other,'foreign.txt'),join(f.root,'linked.txt'));await symlink(other,join(f.root,'junction'),'junction');
 const files=createProjectFiles(f.store);assert.equal((await files.read('p',{path:'linked.txt'})).state,'forbidden');assert.equal((await files.read('p',{path:'junction/foreign.txt'})).state,'forbidden');await assert.rejects(files.list('p',new URLSearchParams({path:'junction'})),{code:'INVENTORY_LINKED_SOURCE'});
 const root=join(f.root,'registered');await mkdir(root);const binding=await bindProject('r',root);await f.store.registerProject({id:'r',keyPrefix:'ROOT',canonicalRoot:binding.workspaceRoot,rootIdentity:binding.directoryIdentity,authorityMode:'sql'});await rename(root,join(f.root,'old-registered'));await mkdir(root);await writeFile(join(root,'foreign.txt'),'replacement');await assert.rejects(files.read('r',{path:'foreign.txt'}),{code:'PROJECT_ROOT_UNAVAILABLE'});
});

test('a policy revocation while a read is in flight cannot publish previously eligible contents',async t=>{
 const f=await m2Fixture(t);await writeFile(join(f.root,'revoked.txt'),'must not be published after revocation');const files=createProjectFiles(f.store),pending=files.read('p',{path:'revoked.txt'});
 await f.store.writeProjectState('p','project_inventory_policy_v1',0,{schemaVersion:'paos_inventory_policy_v1',policy:{exclude:['revoked.txt']}});
 const result=await pending;assert.ok(['stale','forbidden'].includes(result.state));assert.equal(result.content,null);
});
