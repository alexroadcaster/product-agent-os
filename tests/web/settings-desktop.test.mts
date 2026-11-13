import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {createLocalApplication} from '../../apps/local-service/src/http/application.mts';
import {createNativeDesktop} from '../../apps/local-service/src/desktop/native-desktop.mts';
import {EventEmitter} from 'node:events';
import {PassThrough} from 'node:stream';

const origin='http://127.0.0.1:43128';
async function fixture(t:any,cancel=false){
 const root=await mkdtemp(join(tmpdir(),'paos-settings-')),workspace=join(root,'workspace');await mkdir(workspace);
 await writeFile(join(workspace,'main.ts'),'export const value = 3;\n');await writeFile(join(workspace,'REQUIREMENTS.md'),'# Requirements\n\nR-1: Preserve source.\n');
 const store=await openLocalStore({databasePath:join(root,'state.sqlite')});
 t.after(async()=>{await store.close();await rm(root,{recursive:true,force:true});});
 let selections=0,opened=0,connects=0;const urls:string[]=[];let connectionState:any={route:'codex_app_agent',state:'waiting_for_worker',verified:false};
 const app=await createLocalApplication({store,origin,instanceId:'settings-fixture',profileDirectory:root,
  agentChannel:{handle:async()=>new Response('{}'),descriptorPath:join(root,'app-agent-fixture.json')},
  desktop:{selectProjectDirectory:async()=>{selections++;return cancel?{cancelled:true}:{cancelled:false,workspaceRoot:workspace};},openCodexDraft:async(url:string)=>{opened++;urls.push(url);}},
  connection:{status:()=>connectionState,connect:async()=>{connects++;return connectionState={route:'codex_app_agent',state:'waiting_for_worker',verified:false};},disconnect:async()=>({verified:false})},
 } as any);
 let cookie='',csrf='';
 async function request(path:string,payload?:unknown,extra:Record<string,string>={}){return app.handleRequest(new Request(origin+'/api/v1'+path,{method:payload===undefined?'GET':'POST',headers:{host:new URL(origin).host,origin,cookie,'x-paos-csrf':csrf,'content-type':'application/json',...extra},...(payload===undefined?{}:{body:JSON.stringify(payload)})}));}
 const paired=await request('/bootstrap/exchange',{code:app.issuePairingCode()});cookie=paired.headers.get('set-cookie')!.split(';')[0];csrf=(await paired.json()).csrfToken;
 return {root,workspace,store,app,request,urls,setConnection:(value:any)=>{connectionState=value;},counts:()=>({selections,opened,connects})};
}

test('folder selection is explicit, authenticated, idempotent and does not register before Add',async t=>{
 const f=await fixture(t),id='selection-fixture';
 const response=await f.request('/desktop/project-folder',{requestId:id});assert.equal(response.status,200);
 const result=await response.json();assert.equal(result.workspaceRoot,f.workspace);assert.equal(result.cancelled,false);
 assert.equal((await f.request('/desktop/project-folder',{requestId:id})).status,200);assert.equal(f.counts().selections,1);
 assert.equal((await f.request('/projects')).status,200);assert.equal((await(await f.request('/projects')).json()).items.length,0);
 assert.equal((await f.request('/desktop/project-folder',{requestId:'other'},{'x-paos-csrf':''})).status,403);
});

test('cancel and foreign-origin desktop requests never create or inspect a project',async t=>{
 const f=await fixture(t,true);const response=await f.request('/desktop/project-folder',{requestId:'cancel'});
 assert.deepEqual(await response.json(),{cancelled:true});assert.equal((await(await f.request('/projects')).json()).items.length,0);
 assert.equal((await f.request('/desktop/project-folder',{requestId:'foreign'},{origin:'https://foreign.invalid'})).status,403);assert.equal(f.counts().selections,1);
});

test('committed registration survives scan limits and exact retry without duplicate projects',async t=>{
 const f=await fixture(t);await writeFile(join(f.workspace,'large.ts'),'a'.repeat(600000));
 const input={name:'Partial fixture',workspaceRoot:f.workspace,requestId:'scan-limit',scan:true};
 const response=await f.request('/projects',input);assert.equal(response.status,201);const project=await response.json();assert.equal(project.scan.state,'partial');assert.ok(project.scan.reason);
 assert.equal((await(await f.request('/projects',input)).json()).id,project.id);assert.equal((await(await f.request('/projects')).json()).items.length,1);
 const conflict=await f.request('/projects',{...input,name:'Changed envelope'});assert.equal(conflict.status,409);
});

test('parser-excluded source reports partial instead of claiming a complete index',async t=>{
 const f=await fixture(t);await writeFile(join(f.workspace,'deep.ts'),'export const deep = '+ '{x:'.repeat(240)+'1'+'}'.repeat(240)+';');
 const response=await f.request('/projects',{name:'Deep fixture',workspaceRoot:f.workspace,requestId:'deep',scan:true});assert.equal(response.status,201);
 const project=await response.json(),graph=await(await f.request('/projects/'+project.id+'/graph/status')).json();
 assert.equal(graph.coverage.find((c:any)=>c.relativePath==='deep.ts').status,'excluded');assert.equal(project.scan.state,'partial');
});

test('App handoff preserves an attached worker and refuses to replace an active BYOK route',async t=>{
 const f=await fixture(t);f.setConnection({route:'codex_app_agent',state:'connected',verified:true});
 const attached=await(await f.request('/connection/app-handoff',{requestId:'attached'})).json();assert.equal(attached.opened,false);assert.equal(attached.verified,true);assert.equal(f.counts().opened,0);
 f.setConnection({route:'local_api_byok',state:'connected',verified:true});assert.equal((await f.request('/connection/app-handoff',{requestId:'active-api'})).status,409);assert.equal(f.counts().connects,0);
 f.setConnection({route:'local_api_byok',state:'disconnected',verified:false});assert.equal((await f.request('/connection/app-handoff',{requestId:'disconnected-api'})).status,200);assert.equal(f.counts().connects,1);
});

test('native shutdown is bounded and preserves unresolved ownership when kill is not acknowledged',async()=>{
 const helper:any=new EventEmitter();helper.stdout=new PassThrough();helper.stdin=new PassThrough();helper.kill=()=>false;
 const desktop=createNativeDesktop({spawnProcess:(()=>helper) as any,closeTimeoutMs:20});const result=desktop.selectProjectDirectory().catch(error=>error);
 await assert.rejects(desktop.close(),{code:'DESKTOP_SHUTDOWN_UNRESOLVED'});helper.emit('close',1);await result;
});

test('adding a project returns bounded source/code scan and exposes its ready graph',async t=>{
 const f=await fixture(t),response=await f.request('/projects',{name:'Picker fixture',workspaceRoot:f.workspace,requestId:'create-project-fixture',scan:true});
 assert.equal(response.status,201);const project=await response.json();assert.equal(project.scan.state,'ready');assert.ok(project.scan.counts.files>=1);
 assert.equal(project.scan.sources.find((s:any)=>s.id==='requirements').status,'available');
 const graph=await(await f.request('/projects/'+project.id+'/graph/status')).json();assert.equal(graph.state,'fresh');
 const repeat=await f.request('/projects',{name:'Picker fixture',workspaceRoot:f.workspace,requestId:'create-project-fixture',scan:true});
 assert.equal(repeat.status,201);assert.equal((await repeat.json()).id,project.id);
});

test('App handoff opens only a server-built draft without tokens, auto-send or fake verification',async t=>{
 const f=await fixture(t),response=await f.request('/connection/app-handoff',{requestId:'handoff-fixture'});
 assert.equal(response.status,200);const result=await response.json();assert.equal(result.opened,true);assert.equal(result.requiresSend,true);assert.equal(result.verified,false);
 assert.equal(f.urls.length,1);const url=new URL(f.urls[0]);assert.equal(url.protocol,'codex:');assert.equal(url.hostname,'new');assert.ok(url.searchParams.get('path'));
 const prompt=url.searchParams.get('prompt')!;assert.match(prompt,/heartbeat/);assert.match(prompt,/claim/);assert.match(prompt,/report/);assert.match(prompt,/app-agent-client/);
 assert.equal(url.searchParams.has('send'),false);assert.doesNotMatch(f.urls[0],/capabilityToken|leaseToken|apiKey/);
 assert.equal((await f.request('/connection/app-handoff',{requestId:'handoff-fixture'})).status,200);assert.equal(f.counts().opened,1);
 assert.equal((await f.request('/connection/app-handoff',{requestId:'other',url:'file:///untrusted'})).status,400);
});
