import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,rm,symlink,link} from 'node:fs/promises';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {captureTaskFiles,compareTaskFiles} from '../../apps/local-service/src/runtime/app-agent-files.mts';
test('actual task diff is derived from bounded canonical file observations, including add and delete',async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-file-diff-'));t.after(()=>rm(root,{recursive:true,force:true}));const binding=await bindProject('p',root);
 await writeFile(join(root,'changed.txt'),'before\n');await writeFile(join(root,'deleted.txt'),'remove\n');
 const files=['changed.txt','added.txt','deleted.txt'].map(relativePath=>({relativePath}));const before=await captureTaskFiles(binding,files);
 await writeFile(join(root,'changed.txt'),'after\n');await writeFile(join(root,'added.txt'),'new\n');await rm(join(root,'deleted.txt'));
 const changes=compareTaskFiles(before,await captureTaskFiles(binding,files));
 assert.deepEqual(changes.map(change=>[change.path,change.operation]),[['changed.txt','modify'],['added.txt','add'],['deleted.txt','delete']]);
 assert.match(changes[0].diff,/-before/);assert.match(changes[0].diff,/\+after/);assert.notEqual(changes[0].beforeSha256,changes[0].afterSha256);
});
test('file observations exclude secrets, hardlinks and linked directories and reject invalid task paths',async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-file-fence-'));t.after(()=>rm(root,{recursive:true,force:true}));const target=join(root,'target'),outside=join(root,'outside');await mkdir(target);await mkdir(outside);const binding=await bindProject('p',target);
 await writeFile(join(target,'.env'),'SECRET=value');await writeFile(join(outside,'secret.txt'),'outside');
 await symlink(outside,join(target,'alias'),process.platform==='win32'?'junction':'dir');await link(join(outside,'secret.txt'),join(target,'linked.txt'));
 const seen=await captureTaskFiles(binding,['.env','alias/secret.txt','linked.txt'].map(relativePath=>({relativePath})));
 assert.equal(seen.length,3);assert.equal(seen.every(file=>file.kind==='excluded'&&file.content===undefined),true);
 for(const relativePath of ['../outside/secret.txt','C:/private','/absolute','a/../b'])await assert.rejects(captureTaskFiles(binding,[{relativePath}]),{code:'task_file_path_invalid'});
});
test('common credential files and private-key markers never become diff content; structured secrets are redacted',async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-private-diff-'));t.after(()=>rm(root,{recursive:true,force:true}));const binding=await bindProject('p',root);
 await mkdir(join(root,'.aws'));await mkdir(join(root,'.ssh'));
 const privatePaths=['.npmrc','.pypirc','.aws/credentials','.ssh/id_rsa','notes.txt'];
 for(const path of privatePaths)await writeFile(join(root,path),path==='notes.txt'?'-----BEGIN PRIVATE KEY-----\nSYNTHETIC\n-----END PRIVATE KEY-----':'_authToken=synthetic-npm-credential');
 const observations=await captureTaskFiles(binding,privatePaths.map(relativePath=>({relativePath})));
 assert.equal(observations.length,privatePaths.length);assert.equal(observations.every(file=>file.kind==='excluded'&&!file.content),true);
 await writeFile(join(root,'safe.json'),' {"access_token":"synthetic-access-token","name":"fixture"}');
 const safe=await captureTaskFiles(binding,[{relativePath:'safe.json'}]);assert.equal(safe[0].kind,'present');assert.equal(safe[0].content?.includes('synthetic-access-token'),false);assert.match(safe[0].content!,/REDACTED/);
});
