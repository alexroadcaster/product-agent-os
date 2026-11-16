import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createArtifactCatalog} from '../../apps/local-service/src/artifacts/service.mts';
import {m2Fixture} from './m2-fixture.mts';
import {mkdir,writeFile,readFile,rename,open,link,symlink,unlink,access,utimes} from 'node:fs/promises';
import {join,dirname,basename,resolve} from 'node:path';
import {tmpdir} from 'node:os';
import {spawn} from 'node:child_process';
import {setTimeout as delay} from 'node:timers/promises';
import {createHash,randomUUID} from 'node:crypto';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {newM2Task} from '../../packages/contracts/issues/task-profile.ts';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {inventoryScopeFingerprint} from '../../apps/local-service/src/project-inventory/scope.mts';
const hash=(bytes:Buffer)=>createHash('sha256').update(bytes).digest('hex');
test('same-byte external metadata change before native acquisition invalidates the preview revision',async t=>{
 let path='';const bytes=Buffer.from('# Before\n');const f=await workspaceProposal(t,'docs/revision.md',bytes,'# After\n',{beforeAcquire:async()=>{await utimes(path,new Date(10000000),new Date(10000000));}});path=f.path;
 const preview=await f.catalog.applyPreview('p',{proposalId:f.row.id,proposalRevision:f.row.revision});
 await assert.rejects(f.catalog.apply('p','local-user',{proposalId:f.row.id,proposalRevision:f.row.revision,previewDigest:preview.previewDigest,epoch:1,idempotencyKey:'metadata-race'}),{code:'DOCUMENT_SOURCE_CONFLICT'});
 assert.deepEqual(await readFile(f.path),bytes);
});
async function workspaceProposal(t:any,path='PLAN.md',bytes=Buffer.from('# Before\n'),after='# After\n',options={}){
 const f=await m2Fixture(t);await mkdir(join(f.root,path,'..'),{recursive:true});await writeFile(join(f.root,path),bytes);
 const catalog=createArtifactCatalog(f.store,undefined,options),page=await catalog.catalog('p',new URLSearchParams({kind:'documents'})),item=page.items.find(row=>row.source.path===path)!;assert.ok(item);
 const plan=await catalog.preview('p',{documentId:item.id,sourceVersion:item.source.version,body:after});
 const saved=await catalog.saveProposal('p','local-user',{...plan,body:after,epoch:1,idempotencyKey:'proposal'}),row=(await f.store.get('p',saved.id))!;
 return {...f,catalog,row,path:join(f.root,path),bytes};
}

test('SQL document apply is preview bound, idempotent and distinct from owner acceptance',async t=>{
 const f=await m2Fixture(t),catalog=createArtifactCatalog(f.store);
 await f.store.write({projectId:'p',actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'document',changes:[{expectedRevision:0,entity:{id:'doc',kind:'document',title:'Document',body:'# Before\n'}}]});
 const staged=await catalog.preview('p',{documentId:'doc',sourceVersion:'entity:1',body:'# After\n'});
 const saved=await catalog.saveProposal('p','local-user',{...staged,body:staged.after,epoch:1,idempotencyKey:'proposal'});
 const proposal=(await f.store.get('p',saved.id))!;
 const preview=await (catalog as any).applyPreview('p',{proposalId:saved.id,proposalRevision:proposal.revision});
 const input={proposalId:saved.id,proposalRevision:proposal.revision,previewDigest:preview.previewDigest,epoch:1,idempotencyKey:'apply'};
 const result=await (catalog as any).apply('p','local-user',input);
 assert.equal(result.state,'applied');assert.equal(result.accepted,false);
 assert.equal((await f.store.get('p','doc'))!.body,'# After\n');
 assert.deepEqual(await (catalog as any).apply('p','local-user',input),result);
 const read=await catalog.read('p',saved.id);assert.equal(read.proposal!.state,'applied');assert.equal(read.proposal!.applied,true);
});

test('native document apply preserves exact BOM bytes, survives catalog restart and rolls back only the previewed version',async t=>{
 const bytes=Buffer.concat([Buffer.from([239,187,191]),Buffer.from('# Before\n')]),f=await workspaceProposal(t,'docs/plan.md',bytes);
 const restarted=createArtifactCatalog(f.store),preview=await restarted.applyPreview('p',{proposalId:f.row.id,proposalRevision:f.row.revision});
 const after=Buffer.concat([Buffer.from([239,187,191]),Buffer.from('# After\n')]);assert.equal(preview.beforeHash,hash(bytes));assert.equal(preview.afterHash,hash(after));
 const input={proposalId:f.row.id,proposalRevision:f.row.revision,previewDigest:preview.previewDigest,epoch:1,idempotencyKey:'native-apply'};
 const result=await restarted.apply('p','local-user',input);assert.equal(result.state,'applied');assert.equal(result.afterHash,preview.afterHash);assert.deepEqual(await readFile(f.path),after);
 assert.deepEqual(await createArtifactCatalog(f.store).apply('p','local-user',input),result);
 const current=(await f.store.get('p',f.row.id))!,rollback=await restarted.rollbackPreview('p',{proposalId:f.row.id,proposalRevision:current.revision});
 const rolled=await restarted.rollback('p','local-user',{proposalId:f.row.id,proposalRevision:current.revision,previewDigest:rollback.previewDigest,epoch:1,idempotencyKey:'native-rollback'});
 assert.equal(rolled.state,'rolled_back');assert.deepEqual(await readFile(f.path),bytes);assert.equal((await restarted.read('p',f.row.id)).proposal!.applied,false);
});

test('native prepared write fences saved policy and generic proposal edits while exclusive handles protect the exact target',async t=>{
 let f:Awaited<ReturnType<typeof workspaceProposal>>;
 f=await workspaceProposal(t,'docs/plan.md',Buffer.from('# Before\n'),'# After\n',{afterPrepare:async()=>{
  await assert.rejects(f.store.writeProjectState('p','project_inventory_policy_v1',0,{schemaVersion:'paos_inventory_policy_v1',policy:{exclude:['docs/**']}}),{code:'DOCUMENT_WRITE_RECONCILIATION_REQUIRED'});
  await assert.rejects(writeFile(f.path,'External edit'));
  await assert.rejects(rename(f.path,f.path+'.moved'));
  await assert.rejects(rename(join(f.root,'docs'),join(f.root,'docs-moved')));
  await assert.rejects(f.store.write({projectId:'p',actorId:'browser',expectedAuthorityEpoch:1,idempotencyKey:'forged',changes:[{expectedRevision:2,entity:{id:f.row.id,kind:'document',body:'Forged',data:{category:'document_proposal'}}}]}),{code:'DOCUMENT_PROPOSAL_WRITE_AUTHORITY_REQUIRED'});
 }});
 const preview=await f.catalog.applyPreview('p',{proposalId:f.row.id,proposalRevision:f.row.revision});const result=await f.catalog.apply('p','local-user',{proposalId:f.row.id,proposalRevision:f.row.revision,previewDigest:preview.previewDigest,epoch:1,idempotencyKey:'apply-fenced'});
 assert.equal(result.state,'applied');assert.equal(await readFile(f.path,'utf8'),'# After\n');
 await f.store.writeProjectState('p','project_inventory_policy_v1',0,{schemaVersion:'paos_inventory_policy_v1',policy:{}});
 assert.ok(!(await f.store.projectEntities('p')).some(row=>JSON.stringify(row).includes('beforeBase64')));
});

test('external edits and existing readers reject without changing bytes; protected instruction files cannot be applied',async t=>{
 const f=await workspaceProposal(t),preview=await f.catalog.applyPreview('p',{proposalId:f.row.id,proposalRevision:f.row.revision});
 await writeFile(f.path,'# Owner edit\n');await assert.rejects(f.catalog.apply('p','local-user',{proposalId:f.row.id,proposalRevision:f.row.revision,previewDigest:preview.previewDigest,epoch:1,idempotencyKey:'stale'}),{code:'DOCUMENT_SOURCE_CONFLICT'});assert.equal(await readFile(f.path,'utf8'),'# Owner edit\n');
 const busy=await workspaceProposal(t,'docs/busy.txt'),busyPlan=await busy.catalog.applyPreview('p',{proposalId:busy.row.id,proposalRevision:busy.row.revision}),reader=await open(busy.path,'r');
 try{await assert.rejects(busy.catalog.apply('p','local-user',{proposalId:busy.row.id,proposalRevision:busy.row.revision,previewDigest:busyPlan.previewDigest,epoch:1,idempotencyKey:'busy'}),{code:'DOCUMENT_NATIVE_BUSY_OR_DENIED'});}finally{await reader.close();}
 assert.deepEqual(await readFile(busy.path),busy.bytes);
 const protectedFile=await workspaceProposal(t,'AGENTS.md');await assert.rejects(protectedFile.catalog.applyPreview('p',{proposalId:protectedFile.row.id,proposalRevision:protectedFile.row.revision}),{code:'DOCUMENT_WRITE_FORBIDDEN'});
});

test('public proposal exposes the current uncertain rollback operation for explicit recovery',async t=>{
 let failRollback=false;const f=await workspaceProposal(t,'docs/rollback.md',Buffer.from('# Before\n'),'# After\n',{afterPrepare:async()=>{if(failRollback)throw Error('synthetic rollback interruption');}});
 const preview=await f.catalog.applyPreview('p',{proposalId:f.row.id,proposalRevision:f.row.revision});
 const applied=await f.catalog.apply('p','fixture',{proposalId:f.row.id,proposalRevision:f.row.revision,previewDigest:preview.previewDigest,epoch:1,idempotencyKey:'apply-before-rollback'});
 const row=(await f.store.get('p',f.row.id))!,rollback=await f.catalog.rollbackPreview('p',{proposalId:row.id,proposalRevision:row.revision});failRollback=true;
 const interrupted=await f.catalog.rollback('p','fixture',{proposalId:row.id,proposalRevision:row.revision,previewDigest:rollback.previewDigest,epoch:1,idempotencyKey:'rollback-interrupted'});assert.equal(interrupted.state,'recovery_required');
 const document=await createArtifactCatalog(f.store).read('p',row.id),operation=(document.proposal as any).operation;
 assert.equal(operation?.operationId,interrupted.operationId);assert.notEqual(operation.operationId,applied.operationId);assert.equal(operation.action,'rollback');
 const recovered=await createArtifactCatalog(f.store).recover('p','fixture',{proposalId:row.id,operationId:operation.operationId,epoch:1});assert.equal(recovered.state,'not_applied');
 assert.equal((await createArtifactCatalog(f.store).read('p',row.id)).proposal!.state,'applied');assert.equal(await readFile(f.path,'utf8'),'# After\n');
});

test('an uncertain apply never replays after recovery and a later successful retry',async t=>{
 let failOnce=true;const f=await workspaceProposal(t,'PLAN.md',Buffer.from('# Before\n'),'# After\n',{afterPrepare:async()=>{if(failOnce){failOnce=false;throw Error('synthetic failure after durable prepare');}}});
 const preview=await f.catalog.applyPreview('p',{proposalId:f.row.id,proposalRevision:f.row.revision}),firstInput={proposalId:f.row.id,proposalRevision:f.row.revision,previewDigest:preview.previewDigest,epoch:1,idempotencyKey:'first-uncertain'};
 const first=await f.catalog.apply('p','local-user',firstInput);assert.equal(first.state,'recovery_required');assert.deepEqual(await readFile(f.path),f.bytes);
 const recovered=await createArtifactCatalog(f.store).recover('p','local-user',{proposalId:f.row.id,operationId:first.operationId,epoch:1});assert.equal(recovered.state,'not_applied');
 const row=(await f.store.get('p',f.row.id))!,again=await f.catalog.applyPreview('p',{proposalId:row.id,proposalRevision:row.revision});
 assert.equal((await f.catalog.apply('p','local-user',{proposalId:row.id,proposalRevision:row.revision,previewDigest:again.previewDigest,epoch:1,idempotencyKey:'second-explicit'})).state,'applied');
 assert.deepEqual(await f.catalog.apply('p','local-user',firstInput),first);
});

test('terminal document journals retain their historical epoch after legacy cutover',async t=>{
 const f=await m2Fixture(t),root=join(f.root,'legacy');await mkdir(root);const pin=await bindProject('q',root);
 await f.store.registerProject({id:'q',keyPrefix:'DOCS',canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'legacy_files'});
 const catalog=createArtifactCatalog(f.store);
 async function apply(id:string,epoch:number){await f.store.write({projectId:'q',actorId:'fixture',expectedAuthorityEpoch:epoch,idempotencyKey:'create-'+id,changes:[{expectedRevision:0,entity:{id,kind:'document',body:'# Before\n'}}]});const plan=await catalog.preview('q',{documentId:id,sourceVersion:'entity:1',body:'# After\n'}),saved=await catalog.saveProposal('q','local-user',{...plan,body:plan.after,epoch,idempotencyKey:'proposal-'+id}),row=(await f.store.get('q',saved.id))!,preview=await catalog.applyPreview('q',{proposalId:row.id,proposalRevision:row.revision});return catalog.apply('q','local-user',{proposalId:row.id,proposalRevision:row.revision,previewDigest:preview.previewDigest,epoch,idempotencyKey:'apply-'+id});}
 const first=await apply('old-epoch',1);
 await f.store.promoteLegacy({projectId:'q',actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'cutover',sourceDigest:'a'.repeat(64),verifiedSourceDigest:'a'.repeat(64),writerInventoryVerified:true,restoreRehearsalVerified:true,items:[newM2Task('q',randomUUID(),'Imported','fixture')]});
 assert.equal((await f.store.project('q'))!.authorityEpoch,2);assert.equal((await apply('new-epoch',2)).state,'applied');
 const journal=await f.store.documentJournal('q');assert.equal(journal.records.find(r=>r.operationId===first.operationId)!.authorityEpoch,1);
});

test('canonical instruction files are excluded even when readable as plain documents',async t=>{
 for(const path of ['CLAUDE.md','GEMINI.md','.github/copilot-instructions.md','docs/security.instructions.md']){const f=await workspaceProposal(t,path);await assert.rejects(f.catalog.applyPreview('p',{proposalId:f.row.id,proposalRevision:f.row.revision}),{code:'DOCUMENT_WRITE_FORBIDDEN'});assert.deepEqual(await readFile(f.path),f.bytes);}
});

test('actual process death after durable prepare reopens as unresolved without replay and releases owned native helper',async t=>{
 const f=await workspaceProposal(t);await f.store.close();
 const storeModule=new URL('../../apps/local-service/src/storage/local-store.mts',import.meta.url).href,catalogModule=new URL('../../apps/local-service/src/artifacts/service.mts',import.meta.url).href;
 const code=`const {openLocalStore}=await import(${JSON.stringify(storeModule)});const {createArtifactCatalog}=await import(${JSON.stringify(catalogModule)});const [databasePath,proposalId,revision]=process.argv.slice(2);const store=await openLocalStore({databasePath});const catalog=createArtifactCatalog(store,undefined,{afterPrepare:async owner=>{console.log(JSON.stringify({phase:'prepared',...owner}));await new Promise(()=>{});}});const preview=await catalog.applyPreview('p',{proposalId,proposalRevision:Number(revision)});await catalog.apply('p','local-user',{proposalId,proposalRevision:Number(revision),previewDigest:preview.previewDigest,epoch:1,idempotencyKey:'crashed-apply'});`;
 const script=join(f.root,'crash-fixture.mjs');await writeFile(script,code);
 const child=spawn(process.execPath,[script,join(f.root,'state.sqlite'),f.row.id,String(f.row.revision)],{stdio:['ignore','pipe','pipe'],windowsHide:true,env:{SystemRoot:process.env.SystemRoot,WINDIR:process.env.WINDIR,TEMP:tmpdir(),TMP:tmpdir()}});
 let owner:{processId:number;temporaryDirectory:string}|undefined,stderr='';child.stderr.on('data',chunk=>{if(stderr.length<8192)stderr+=chunk.toString();});
 const closed=new Promise<void>(done=>child.once('close',()=>done()));
 try{
  owner=await new Promise<any>((accept,reject)=>{let buffer='';const timer=setTimeout(()=>reject(Error('prepared signal timeout: '+stderr)),12000);child.once('error',reject);child.once('close',()=>{clearTimeout(timer);reject(Error('fixture process exited: '+stderr));});child.stdout.on('data',chunk=>{buffer+=chunk.toString();if(buffer.length>8192){clearTimeout(timer);reject(Error('fixture signal limit'));return;}const at=buffer.indexOf('\n');if(at>=0){clearTimeout(timer);try{const value=JSON.parse(buffer.slice(0,at));assert.equal(value.phase,'prepared');accept(value);}catch(error){reject(error);}}});});
  assert.ok(Number.isSafeInteger(owner!.processId)&&owner!.processId>0);assert.equal(dirname(resolve(owner!.temporaryDirectory)),resolve(tmpdir()));assert.ok(basename(owner!.temporaryDirectory).startsWith('paos-document-write-'));
  child.kill('SIGKILL');await closed;
  const deadline=Date.now()+4000;let alive=true;
  while(Date.now()<deadline){try{process.kill(owner!.processId,0);}catch{alive=false;break;}await delay(25);}
  assert.equal(alive,false,'only the owned native helper must exit after its parent');
  const reopened=await openLocalStore({databasePath:join(f.root,'state.sqlite')});f.beforeClose(()=>reopened.close());
  const journal=await reopened.documentJournal('p'),record=journal.records.find(r=>r.proposalId===f.row.id)!;assert.equal(record.state,'prepared');
  const catalog=createArtifactCatalog(reopened);assert.equal((await catalog.read('p',f.row.id)).proposal!.state,'prepared');await delay(30);assert.deepEqual(await readFile(f.path),f.bytes);
  const result=await catalog.recover('p','local-user',{proposalId:f.row.id,operationId:record.operationId,epoch:1});assert.equal(result.state,'not_applied');assert.equal(result.reason,'DOCUMENT_EXPLICIT_RETRY_REQUIRED');assert.deepEqual(await readFile(f.path),f.bytes);await assert.rejects(access(owner!.temporaryDirectory),{code:'ENOENT'});
 }finally{if(child.exitCode===null)child.kill('SIGKILL');await closed;}
});

test('hardlinks, reparse parents and an existing writer never redirect native document writes',async t=>{
 const hard=await workspaceProposal(t),alias=join(hard.root,'alias.txt');await link(hard.path,alias);
 await assert.rejects(hard.catalog.applyPreview('p',{proposalId:hard.row.id,proposalRevision:hard.row.revision}),(e:any)=>/LINKED_SOURCE|SOURCE_FORBIDDEN/.test(e.code));assert.deepEqual(await readFile(hard.path),hard.bytes);await unlink(alias);
 const reparse=await workspaceProposal(t,'docs/plan.md');await rename(join(reparse.root,'docs'),join(reparse.root,'actual'));await symlink(join(reparse.root,'actual'),join(reparse.root,'docs'),'junction');
 await assert.rejects(reparse.catalog.applyPreview('p',{proposalId:reparse.row.id,proposalRevision:reparse.row.revision}),(e:any)=>/LINKED_SOURCE|SOURCE_FORBIDDEN/.test(e.code));assert.deepEqual(await readFile(join(reparse.root,'actual','plan.md')),reparse.bytes);
 const busy=await workspaceProposal(t),preview=await busy.catalog.applyPreview('p',{proposalId:busy.row.id,proposalRevision:busy.row.revision}),writer=await open(busy.path,'r+');
 try{await assert.rejects(busy.catalog.apply('p','local-user',{proposalId:busy.row.id,proposalRevision:busy.row.revision,previewDigest:preview.previewDigest,epoch:1,idempotencyKey:'busy-writer'}),{code:'DOCUMENT_NATIVE_BUSY_OR_DENIED'});}finally{await writer.close();}assert.deepEqual(await readFile(busy.path),busy.bytes);
});

test('BOM preservation obeys the exact 512KiB boundary before preview and native commit',async t=>{
 const before=Buffer.concat([Buffer.from([239,187,191]),Buffer.from('# Before\n')]),f=await workspaceProposal(t,'PLAN.md',before,'x'.repeat(512*1024-3));
 const preview=await f.catalog.applyPreview('p',{proposalId:f.row.id,proposalRevision:f.row.revision});assert.equal(preview.afterHash,hash(Buffer.concat([Buffer.from([239,187,191]),Buffer.from('x'.repeat(512*1024-3))])));
 const result=await f.catalog.apply('p','local-user',{proposalId:f.row.id,proposalRevision:f.row.revision,previewDigest:preview.previewDigest,epoch:1,idempotencyKey:'exact-limit'});assert.equal(result.state,'applied');assert.equal((await readFile(f.path)).length,512*1024);
 const over=await workspaceProposal(t,'PLAN.md',before,'x'.repeat(512*1024));await assert.rejects(over.catalog.applyPreview('p',{proposalId:over.row.id,proposalRevision:over.row.revision}),{code:'DOCUMENT_TOO_LARGE'});assert.deepEqual(await readFile(over.path),before);
});

test('terminal journal retention is bounded while old immutable apply receipts survive eviction and oversized journals reject',async t=>{
 const f=await m2Fixture(t),catalog=createArtifactCatalog(f.store);let first:any,firstInput:any;
 for(let i=0;i<5;i++){const id='doc-'+i;await f.store.write({projectId:'p',actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:id,changes:[{expectedRevision:0,entity:{id,kind:'document',body:'# Before\n'}}]});const plan=await catalog.preview('p',{documentId:id,sourceVersion:'entity:1',body:'# After\n'}),saved=await catalog.saveProposal('p','local-user',{...plan,body:plan.after,epoch:1,idempotencyKey:'stage-'+i}),row=(await f.store.get('p',saved.id))!,preview=await catalog.applyPreview('p',{proposalId:row.id,proposalRevision:row.revision}),input={proposalId:row.id,proposalRevision:row.revision,previewDigest:preview.previewDigest,epoch:1,idempotencyKey:'apply-'+i},result=await catalog.apply('p','local-user',input);if(i===0){first=result;firstInput=input;}}
 const journal=await f.store.documentJournal('p');assert.equal(journal.records.length,4);assert.ok(!journal.records.some(r=>r.operationId===first.operationId));assert.deepEqual(await catalog.apply('p','local-user',firstInput),first);
 const p=(await f.store.project('p'))!,row=(await f.store.get('p',journal.records[0].proposalId))!,scopeFingerprint=inventoryScopeFingerprint(p),generation=(await f.store.projectFreshness('p')).generation;
 const input={command:{projectId:'p',actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'oversized-journal',changes:[{expectedRevision:row.revision,entity:{id:row.id,kind:'document' as const,body:row.body,data:row.data}}]},expectedJournalVersion:journal.version,records:[{...journal.records[0],padding:'x'.repeat(2*1024*1024)}],scopeFingerprint,generation};
 await assert.rejects(f.store.documentWrite(input as any),{code:'DOCUMENT_JOURNAL_LIMIT'});assert.deepEqual(await f.store.documentJournal('p'),journal);
 await assert.rejects(f.store.documentWrite({...input,command:{...input.command,idempotencyKey:'count-journal'},records:[...journal.records,journal.records[0]]} as any),{code:'DOCUMENT_JOURNAL_LIMIT'});assert.deepEqual(await f.store.documentJournal('p'),journal);
});
