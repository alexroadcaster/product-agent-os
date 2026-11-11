import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtemp, mkdir, readFile, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {startLocalService} from '../../apps/local-service/src/main.mts';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';

for(const route of ['codex_app_agent','local_api_byok'] as const)test(`production route guard refreshes foreign unresolved runs created after startup (${route})`,async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-app-foreign-'));let store:Awaited<ReturnType<typeof openLocalStore>>;let connection:any,apiConnects=0;
 const apiGateway={connection:{status:()=>({route:'local_api_byok',verified:false}),connect:async()=>{apiConnects++;return {verified:true};},disconnect:async()=>({verified:false})},runtime:{snapshot:async()=>({}),dispatch:async()=>({})},close:async()=>{}};
 const service=await startLocalService({profileDirectory:join(root,'profile'),instanceId:'route-guard'},{
  openStore:async(options)=>{store=await openLocalStore(options);return store;},createGateway:(()=>apiGateway) as any,
  createApplication:async(options)=>{connection=options.connection;return {issuePairingCode:()=>'',revokeSessions(){},handleRequest:async()=>new Response('{}')} as any;}});
 t.after(async()=>{await service.quit();await rm(root,{recursive:true,force:true});});
 await connection.connect({route:'codex_app_agent'});await connection.disconnect();
 for(const id of ['a','b']){const directory=join(root,id);await mkdir(directory);const pin=await bindProject(id,directory);await store!.registerProject({id,keyPrefix:id==='a'?'AAAA':'BBBB',canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'sql'});}
 const foreign=route==='codex_app_agent'?{runtimeRun:{state:'recovery_required'}}:{appAgentRun:{state:'recovery_required'}};
 await store!.write({projectId:'b',actorId:'fixture',idempotencyKey:'late-foreign',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'foreign',kind:'run',status:'recovery_required',data:foreign}}]});
 await assert.rejects(connection.connect({route,...(route==='local_api_byok'?{connectionId:'fixture',apiKey:'synthetic'}:{})}),{code:'FOREIGN_RUNTIME_RECOVERY_REQUIRED'});
 assert.equal(apiConnects,0);
});

test('production service selects App agents without opening API auth and persists the scoped result',async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-app-service-'));const target=join(root,'workspace');await mkdir(target);
 const service=await startLocalService({profileDirectory:join(root,'profile'),instanceId:'app-agent-test'},{sandboxBrokerFactory:false});
 t.after(async()=>{await service.quit();await rm(root,{recursive:true,force:true});});
 const origin=`http://127.0.0.1:${service.port}`;
 const paired=await fetch(`${origin}/bootstrap/exchange`,{method:'POST',headers:{origin,'content-type':'application/json'},body:JSON.stringify({code:service.pairingCode})});
 assert.equal(paired.status,200);const cookie=paired.headers.get('set-cookie')!.split(';')[0];const {csrfToken}=await paired.json() as any;
 async function api(path:string,input?:unknown){const response=await fetch(`${origin}/api/v1${path}`,{method:input===undefined?'GET':'POST',headers:{origin,cookie,'content-type':'application/json','x-paos-csrf':csrfToken},body:input===undefined?undefined:JSON.stringify(input)});return {status:response.status,body:await response.json() as any};}
 const connected=await api('/connection',{route:'codex_app_agent',connectionId:'codex-app'});
 assert.equal(connected.status,200,JSON.stringify(connected.body));assert.equal(connected.body.route,'codex_app_agent');assert.equal(connected.body.verified,false);
 assert.equal(connected.body.hostTransport.transport,'websocket_over_stdio_proxy');
 assert.notEqual(connected.body.hostTransport.status,'ready');
 assert.equal(JSON.stringify(connected.body.hostTransport).includes('codexHome'),false);
 const descriptor=JSON.parse(await readFile((service as any).appAgentDescriptorPath,'utf8'));
 async function agent(action:string,input:unknown){const response=await fetch(`${origin}/agent/v1/${action}`,{method:'POST',headers:{origin,'content-type':'application/json',authorization:`Bearer ${descriptor.capabilityToken}`},body:JSON.stringify(input)});assert.equal(response.status,200);return response.json() as Promise<any>;}
 const lease=await agent('attach',{hostIdentity:'codex_app',workerId:'fixture-worker',generation:'fixture-generation'});
 assert.equal((await api('/connection')).body.verified,true);
 assert.equal(JSON.stringify((await api('/connection')).body).includes(lease.leaseToken),false);
 const project=(await api('/projects',{name:'Synthetic App relay',workspaceRoot:target,keyPrefix:'APPA'})).body;
 const sessionId='app-session';await api(`/projects/${project.id}/commands`,{idempotencyKey:'session-seed',expectedAuthorityEpoch:project.authorityEpoch,changes:[{expectedRevision:0,entity:{id:sessionId,kind:'session',title:'Synthetic App agent'}}]});
 const scope={projectId:project.id,sessionId};
 const binding=(await api('/runtime/bindings',{...scope,mode:'discussion'})).body;
 const send={...scope,bindingId:binding.bindingId,clientMessageId:'unique-message',input:'Return the synthetic value forty-two.'};
 const sent=await api('/runtime/send',send);assert.equal(sent.status,200,JSON.stringify(sent.body));
 const duplicate=await api('/runtime/send',send);assert.equal(duplicate.body.id,sent.body.id);
 const auth={workerId:lease.workerId,generation:lease.generation,leaseToken:lease.leaseToken};
 const claimed=await agent('claim',auth);assert.equal(claimed.job.runId,sent.body.id);
 await agent('report',{...auth,runId:claimed.job.runId,seq:1,idempotencyKey:'synthetic-result',status:'completed',text:'Synthetic value: forty-two.'});
 const messages=(await api(`/projects/${project.id}/entities?kind=message&parentId=${sessionId}`)).body.items;
 assert.equal(messages.some((row:any)=>row.body==='Synthetic value: forty-two.'),true);
 const state=(await api(`/runtime/state?${new URLSearchParams(scope)}`)).body;
 assert.equal(state.state,'completed');assert.equal(state.capabilities.nativeSandbox,false);
 const execution=await api('/runtime/bindings',{...scope,mode:'execution'});assert.notEqual(execution.status,200);
 const invalid=await fetch(`${origin}/agent/v1/claim`,{method:'POST',headers:{origin,'content-type':'application/json'},body:'{}'});assert.equal(invalid.status,401);
 assert.equal((await api('/connection',{route:'local_api_byok',connectionId:'other',apiKey:'synthetic'})).status>=400,true);
});
