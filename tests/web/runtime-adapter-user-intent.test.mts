import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {createRuntimeStoragePorts,taskScopeDigest} from '../../apps/local-service/src/runtime/storage-ports.mts';
import {fixtureTask,runtimeTaskId} from './runtime-adapter-time.fixture.mts';

test('canonical user text commits with intent and remains exactly once after crash/reopen/retry',async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-user-intent-'));let store=await openLocalStore({databasePath:join(root,'state.sqlite')});
 t.after(async()=>{await store.close();await rm(root,{recursive:true,force:true});});
 await store.registerProject({id:'p',keyPrefix:'TEST',canonicalRoot:root,rootIdentity:'fixture',authorityMode:'sql'});
 await store.write({projectId:'p',actorId:'u',expectedAuthorityEpoch:1,idempotencyKey:'seed',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}},{expectedRevision:0,entity:{id:runtimeTaskId,kind:'task',data:fixtureTask()}}]});
 let ports=createRuntimeStoragePorts(store,{actorId:'runtime'});const task=(await store.get('p',runtimeTaskId))!;
 const run={id:'r',bindingId:'b',projectId:'p',sessionId:'s',accountId:'private',generation:'g',threadId:'thread',turnId:null,clientMessageId:'m',inputDigest:'input-digest',taskId:runtimeTaskId,scopeDigest:taskScopeDigest(task),targetRevision:task.revision,state:'dispatching' as const};
 const text='Original user instruction [redacted]';
 const message={projectId:'p',sessionId:'s',bindingId:'b',runId:'r',sourceItemId:'client:m',revision:createHash('sha256').update(text).digest('hex'),role:'user' as const,text};
 await ports.appendIntent(run,message);
 const first=(await store.list('p',{kind:'message'}));assert.equal(first.length,1);assert.equal(first[0].body,text);
 const event=(await store.events('p')).items.find((event)=>(event.payload as any).revisions.some((revision:any)=>revision.id==='r'))!;
 assert.ok((event.payload as any).revisions.some((revision:any)=>revision.id===first[0].id));
 await store.close();store=await openLocalStore({databasePath:join(root,'state.sqlite')});ports=createRuntimeStoragePorts(store,{actorId:'runtime'});
 await ports.appendIntent(run,message);
 assert.equal((await store.list('p',{kind:'message'})).length,1);
 assert.equal((await store.get('p','r'))!.status,'dispatching');
 const second={...run,id:'invalid',clientMessageId:'invalid',taskId:null,scopeDigest:null,targetRevision:undefined};
 await assert.rejects(ports.appendIntent(second,{...message,runId:'invalid',sessionId:'foreign',sourceItemId:'client:invalid'}));
 assert.equal(await store.get('p','invalid'),null);
});

test('EOF before provider user item preserves redacted original and ignores later wrapped provider echo',async(t)=>{
 const {createRuntimeCoordinator}=await import('../../apps/local-service/src/runtime/codex/coordinator.ts');
 const {bindProject}=await import('../../apps/local-service/src/adapters/project-sources.ts');
 const root=await mkdtemp(join(tmpdir(),'paos-user-eof-'));let store=await openLocalStore({databasePath:join(root,'state.sqlite')});
 t.after(async()=>{await store.close();await rm(root,{recursive:true,force:true});});
 const pin=await bindProject('p',root);await store.registerProject({id:'p',keyPrefix:'TEST',canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'sql'});
 let listener:(message:any)=>void=()=>{};let sends=0;
 const coordinator=createRuntimeCoordinator({isEnabled:()=>true,authorizeDispatch:()=>true,redact:(text)=>text.replaceAll('synthetic-secret','[redacted]'),
  persistence:createRuntimeStoragePorts(store,{actorId:'runtime'}),
  rpc:{generation:'g',subscribe(next){listener=next;return()=>{};},onClosed(){return()=>{};},respond(){},respondError(){},notify(){},close:async()=>{},
   snapshot(){return {generation:'g',status:'open',pending:0,stderrBytes:0};},
   async request(method,params:any){
    if(method==='thread/start')return {thread:{id:'thread'},cwd:params.cwd,runtimeWorkspaceRoots:[params.cwd],activePermissionProfile:{id:params.permissions},approvalPolicy:'never',sandbox:{type:'readOnly',networkAccess:false}};
    if(method==='turn/start') {sends++;const messages=await store.list('p',{kind:'message'});assert.equal(messages.length,1);assert.equal(messages[0].body,'Original [redacted]');throw new Error('synthetic EOF');}
    return {};
   }},
 });
 const binding=await coordinator.openBinding({projectId:'p',sessionId:'s',accountId:'a',workspaceRoot:pin.workspaceRoot,mode:'discussion',profileId:'fixture'});
 const input={bindingId:binding.id,clientMessageId:'m',input:'Original synthetic-secret'};
 const run=await coordinator.send(input);assert.equal(run.state,'recovery_required');
 assert.equal((await coordinator.send(input)).id,run.id);assert.equal(sends,1);
 listener({method:'item/completed',params:{threadId:'thread',turnId:'provider-turn',item:{type:'userMessage',id:'provider-echo',content:[{type:'inputText',text:'PAOS_TASK_CONTEXT_JSON wrapped provider echo'}]}}});
 await coordinator.flush();assert.equal((await store.list('p',{kind:'message'})).length,1);
 await store.close();store=await openLocalStore({databasePath:join(root,'state.sqlite')});
 const rows=await store.list('p',{kind:'message'});assert.equal(rows.length,1);assert.equal(rows[0].body,'Original [redacted]');
 assert.equal(JSON.stringify(rows).includes('synthetic-secret'),false);assert.equal(JSON.stringify(rows).includes('wrapped provider echo'),false);
});
