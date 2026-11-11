import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {createLiveGateway} from '../../apps/local-service/src/runtime/live-gateway.mts';
import {fixtureTask,runtimeTaskId} from './runtime-adapter-time.fixture.mts';

test('shutdown persists recovery before child close and leaves it available when persistence fails',async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-stop-receipt-'));const pin=await bindProject('p',root);
 const store=await openLocalStore({databasePath:join(root,'state.sqlite')});let gateway:ReturnType<typeof createLiveGateway>;
 t.after(async()=>{await gateway.close();await store.close();await rm(root,{recursive:true,force:true});});
 await store.registerProject({id:'p',keyPrefix:'TEST',canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'sql'});
 await store.write({projectId:'p',actorId:'u',expectedAuthorityEpoch:1,idempotencyKey:'seed',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}},{expectedRevision:0,entity:{id:runtimeTaskId,kind:'task',data:fixtureTask()}}]});
 let closed=false;gateway=createLiveGateway({store,profileId:'fixture',actorId:'runtime',isEnabled:()=>true,providerAuthority:()=>true,
 rpcFactory:async()=>({generation:'g',notify(){},subscribe(){return()=>{};},onClosed(){return()=>{};},respond(){},respondError(){},
  async close(){const rows=await store.list('p',{kind:'run'});assert.equal(rows[0].status,'recovery_required');closed=true;},
  async request(method,params:any){
   if(method==='account/login/start')return {type:'apiKey'};if(method==='account/read')return {account:{type:'apiKey'}};
   if(method==='thread/start')return {thread:{id:'thread'},cwd:params.cwd,runtimeWorkspaceRoots:[params.cwd],activePermissionProfile:{id:params.permissions},approvalPolicy:'on-request',sandbox:{type:'workspaceWrite',networkAccess:false,writableRoots:[],excludeSlashTmp:true,excludeTmpdirEnvVar:true}};
   if(method==='turn/start')return {turn:{id:'turn',status:'inProgress'}};return {};
  }})});
 await gateway.connection.connect({connectionId:'c',apiKey:'synthetic'});
 const binding:any=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 await gateway.runtime.dispatch('send',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,clientMessageId:'m',input:'synthetic',taskId:runtimeTaskId});
 let block=true;const write=store.write;store.write=async(command)=>{if(block&&command.changes.some((change)=>change.entity.kind==='run'&&change.entity.status==='recovery_required'))throw Object.assign(new Error('synthetic write failure'),{code:'FIXTURE_FAILURE'});return write(command);};
 await assert.rejects(gateway.close(),{code:'FIXTURE_FAILURE'});assert.equal(closed,false);
 assert.equal((await gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).canSend,false);
 block=false;await gateway.close();assert.equal(closed,true);
 const timeline=(await store.list('p',{kind:'run'}))[0].data.timeline as any[];
 assert.equal(timeline.filter((event)=>event.kind==='interval_crashed').length,1);
});
