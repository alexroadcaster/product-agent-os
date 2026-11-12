import assert from 'node:assert/strict';
import { test } from 'node:test';
import { randomUUID } from 'node:crypto';
import { mkdtemp, rm, mkdir, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join,resolve,dirname,basename } from 'node:path';
import { openLocalStore, restoreLocalBackup } from '../../apps/local-service/src/storage/local-store.mts';
import { taskManagerCommand, taskManagerSnapshot, uploadTaskAttachment, downloadTaskAttachment, resolveTaskReference } from '../../apps/local-service/src/task-manager/service.mts';
import { newM2Task } from '../../packages/contracts/issues/task-profile.ts';

async function fixture(t:any){const root=await mkdtemp(join(tmpdir(),'paos-m2-'));const store=await openLocalStore({databasePath:join(root,'state.sqlite')});
  await store.registerProject({id:'p',keyPrefix:'PAOS',canonicalRoot:root,rootIdentity:'fixture',authorityMode:'sql'});
  t.after(async()=>{await store.close();const target=resolve(root);assert.equal(dirname(target),resolve(tmpdir()));assert.ok(basename(target).startsWith('paos-m2-'));await rm(target,{recursive:true,force:true});});
  const command=(payload:Record<string,any>)=>taskManagerCommand(store,'p','u',{expectedAuthorityEpoch:1,idempotencyKey:randomUUID(),...payload});
  const create=async(title='Task',extra={})=>{const task={...newM2Task('p',randomUUID(),title,'u'),...extra};await command({action:'save',task,expectedRevision:0});return (await store.get('p',task.id))!;};
  return {root,store,command,create};}

test('transactionally enforces hierarchy, Ready fields, manual criteria and immutable creator',async t=>{
  const {store,command,create}=await fixture(t);const epic=await create('Epic',{type:'epic',acceptanceCriteria:['Children delivered']}),child=await create('Child',{parentId:epic.id});
  await assert.rejects(()=>command({action:'transition',taskId:child.id,expectedRevision:child.revision,status:'ready',reason:'ready'}),{code:'READY_FIELDS_REQUIRED'});
  await assert.rejects(()=>command({action:'transition',taskId:epic.id,expectedRevision:epic.revision,status:'done',manual:true,reason:'complete',evidence:[{criterion:'Children delivered',outcome:'passed',evidence:'attempt'}]}),{code:'CHILDREN_INCOMPLETE'});
  const data={...child.data,summary:'scope',technicalValue:'tech',productValue:'value',files:[{relativePath:'src/a.ts',plannedOperation:'modify',actualOperation:null}],risks:['none'],estimateSeconds:60,acceptanceCriteria:['Works']};
  await command({action:'save',task:data,expectedRevision:child.revision});
  const saved=(await store.get('p',child.id))!;
  await command({action:'transition',taskId:child.id,expectedRevision:saved.revision,status:'done',manual:true,reason:'checked',evidence:[{criterion:'Works',evidence:'manual observed',outcome:'passed'}]});
  assert.equal((await store.get('p',child.id))!.status,'done');
  const completed=(await store.get('p',child.id))!;
  await assert.rejects(()=>store.write({projectId:'p',actorId:'u',idempotencyKey:randomUUID(),expectedAuthorityEpoch:1,changes:[{expectedRevision:completed.revision,entity:{id:child.id,kind:'task',data:{...completed.data,creator:{kind:'user',actorId:'forged'}}}}]}),{code:'CREATOR_IMMUTABLE'});
});

test('canonical links are inverse-visible, DAG guarded, cancellation remains blocking',async t=>{
  const {store,command,create}=await fixture(t);const a=await create('A'),b=await create('B',{acceptanceCriteria:['B verified'],risks:['dependency_review']});
  await command({action:'link',expectedRevision:0,link:{sourceId:a.id,targetId:b.id,relation:'blocks',reason:'prerequisite'}});
  await assert.rejects(()=>command({action:'link',expectedRevision:1,link:{sourceId:b.id,targetId:a.id,relation:'blocks',reason:'cycle'}}),{code:'TASK_LINK_CYCLE'});
  await command({action:'transition',taskId:a.id,expectedRevision:a.revision,status:'cancelled',reason:'not doing'});
  await assert.rejects(()=>command({action:'transition',taskId:b.id,expectedRevision:b.revision,status:'done',manual:true,reason:'attempt',evidence:[{criterion:'B verified',outcome:'passed',evidence:'observed'}]}),{code:'DEPENDENCY_BLOCKED'});
  assert.equal((await taskManagerSnapshot(store,'p')).links.length,1);
});

test('managed upload retry is idempotent, download safe, backup restores attachment bytes',async t=>{
  const {root,store,create,command}=await fixture(t);const task=await create();const other=await create('Other');
  await command({action:'component',expectedRevision:0,item:{id:'Custom',name:'Custom',status:'active'}});
  await command({action:'version',expectedRevision:0,item:{id:'v13',name:'1.3',status:'unreleased'}});
  await command({action:'link',expectedRevision:0,link:{sourceId:task.id,targetId:other.id,relation:'relates_to',reason:'context'}});
  await command({action:'comment',taskId:task.id,id:'comment-fixture',body:'Original private text',expectedRevision:0});
  await command({action:'comment',taskId:task.id,id:'comment-fixture',body:'Revised fixture',expectedRevision:1});
  await command({action:'comment',taskId:task.id,id:'comment-fixture',delete:true,expectedRevision:2});
  const input={filename:'note.txt',mediaType:'text/plain',base64:Buffer.from('safe fixture').toString('base64'),expectedRevision:task.revision,expectedAuthorityEpoch:1,idempotencyKey:'upload'};
  const first=await uploadTaskAttachment(store,'p',task.id,'u',input);const second=await uploadTaskAttachment(store,'p',task.id,'u',input);assert.deepEqual(first,second);
  const attachments=(await taskManagerSnapshot(store,'p')).attachments;assert.equal(attachments.length,1);
  const response=await downloadTaskAttachment(store,'p',task.id,attachments[0].id);assert.equal(await response.text(),'safe fixture');assert.match(response.headers.get('content-disposition')! ,/^attachment/);
  await mkdir(join(root,'backups'));const backup=await store.backup(join(root,'backups'));await restoreLocalBackup(backup.directory,join(root,'restored.sqlite'));
  const expected=await taskManagerSnapshot(store,'p');
  const restored=await openLocalStore({databasePath:join(root,'restored.sqlite')});try{
    assert.equal(await (await downloadTaskAttachment(restored,'p',task.id,attachments[0].id)).text(),'safe fixture');
    assert.deepEqual(await taskManagerSnapshot(restored,'p'),expected);
    assert.equal(JSON.stringify(await restored.audit('p')).includes('Original private text'),false);
    assert.equal(expected.comments.find(c=>c.id==='comment-fixture')!.body,'');
  }finally{await restored.close();}
});

test('rejects forged scope_review terminal bypass and preserves done history on prerequisite reopen',async t=>{
  const {store,create,command}=await fixture(t);const parent=await create('P',{type:'epic',acceptanceCriteria:['ok'],risks:['scope_review']});
  await create('Child',{parentId:parent.id});
  await assert.rejects(()=>command({action:'transition',taskId:parent.id,expectedRevision:1,status:'done',manual:true,reason:'bad bypass',evidence:[{criterion:'ok',evidence:'observed',outcome:'passed'}]}),{code:'CHILDREN_INCOMPLETE'});
  const a=await create('A',{acceptanceCriteria:['ok'],summary:'scope',technicalValue:'tech',productValue:'value',files:[{relativePath:'x',plannedOperation:'read',actualOperation:null}],estimateSeconds:1,risks:['none']}),b=await create('B',{acceptanceCriteria:['ok']});
  for(const task of [a,b])await command({action:'transition',taskId:task.id,expectedRevision:1,status:'done',manual:true,reason:'verified',evidence:[{criterion:'ok',evidence:'observed',outcome:'passed'}]});
  await command({action:'link',expectedRevision:0,link:{sourceId:a.id,targetId:b.id,relation:'blocks',reason:'dependency'}});
  await command({action:'transition',taskId:a.id,expectedRevision:2,status:'ready',reason:'reopen'});
  const dependent=(await store.get('p',b.id))!;assert.equal(dependent.status,'done');assert.ok((dependent.data.risks as string[]).includes('dependency_review'));
});

test('hard WIP and active writer fences apply in the transactional service',async t=>{
  const {store,create,command}=await fixture(t);const fields={summary:'scope',technicalValue:'tech',productValue:'value',files:[{relativePath:'x',plannedOperation:'read',actualOperation:null}],estimateSeconds:1,risks:['none'],acceptanceCriteria:['ok']};
  const a=await create('A',fields),b=await create('B',fields);const board=(await taskManagerSnapshot(store,'p')).board;
  await command({action:'board',expectedRevision:0,board:{...board,columns:board.columns.map(c=>c.id==='in_progress'?{...c,wipLimit:1,wipMode:'hard'}:c)}});
  for(const task of [a,b])await command({action:'transition',taskId:task.id,expectedRevision:1,status:'ready',reason:'prepared'});
  await command({action:'transition',taskId:a.id,expectedRevision:2,status:'in_progress',reason:'start'});
  await assert.rejects(()=>command({action:'transition',taskId:b.id,expectedRevision:2,status:'in_progress',reason:'start'}),{code:'HARD_WIP_LIMIT'});
  await store.write({projectId:'p',actorId:'runtime',expectedAuthorityEpoch:1,idempotencyKey:'run',changes:[{expectedRevision:0,entity:{id:'run',kind:'run',status:'running',data:{runtimeRun:{id:'run',projectId:'p',taskId:a.id,bindingId:'binding',sessionId:'session',generation:'generation'}}}}]});
  await assert.rejects(()=>command({action:'transition',taskId:a.id,expectedRevision:3,status:'cancelled',reason:'stop'}),{code:'ACTIVE_RUN_RECONCILIATION_REQUIRED'});
  await command({action:'link',expectedRevision:0,link:{sourceId:b.id,targetId:a.id,relation:'blocks',reason:'new blocker'}});
  const links=(await taskManagerSnapshot(store,'p')).links;assert.equal(links[0].state,'pending');
  await assert.rejects(()=>command({action:'activate-link',linkId:links[0].id,expectedRevision:1}),{code:'ACTIVE_RUN_RECONCILIATION_REQUIRED'});
});

test('reference resolution rejects traversal and returns stale without replacement content',async t=>{
  const {root,store,create}=await fixture(t);const task=await create('File',{files:[{relativePath:'a.txt',plannedOperation:'read',actualOperation:null}]});await writeFile(join(root,'a.txt'),'fixture');
  const stale=await resolveTaskReference(store,'p',{taskId:task.id,relativePath:'a.txt',revision:'0'.repeat(64)});assert.equal(stale.availability,'stale');assert.equal('content' in stale,false);
  await assert.rejects(()=>resolveTaskReference(store,'p',{taskId:task.id,relativePath:'../secret'}),{code:'REFERENCE_PATH_FORBIDDEN'});
});
