import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {createLiveGateway} from '../../apps/local-service/src/runtime/live-gateway.mts';
import {createRuntimeStoragePorts} from '../../apps/local-service/src/runtime/storage-ports.mts';
import {fixtureTask,runtimeTaskId} from './runtime-adapter-time.fixture.mts';

test('EOF reconnect retires the old generation, restores recovery and ignores its late close callback',async(t)=>{
 const {bindProject}=await import('../../apps/local-service/src/adapters/project-sources.ts');
 const root=await mkdtemp(join(tmpdir(),'paos-eof-reconnect-'));const pin=await bindProject('p',root);
 const store=await openLocalStore({databasePath:join(root,'state.sqlite')});let gateway:ReturnType<typeof createLiveGateway>;
 t.after(async()=>{await gateway?.close();await store.close();await rm(root,{recursive:true,force:true});});
 await store.registerProject({id:'p',keyPrefix:'TEST',canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'sql'});
 await store.write({projectId:'p',actorId:'u',idempotencyKey:'seed',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 const closes:Array<()=>void>=[];let generations=0;let stops=0;let sends=0;const recovered=Promise.withResolvers<void>();
 gateway=createLiveGateway({store,profileId:'fixture',actorId:'runtime',isEnabled:()=>true,providerAuthority:()=>true,
  onEvent(event){if(event.kind==='run'&&(event.run as any).state==='recovery_required')recovered.resolve();},
  rpcFactory:async()=>{const generation=`g${++generations}`;return {generation,notify(){},subscribe(){return()=>{};},onClosed(next){closes.push(()=>next('runtime_eof'));return()=>{};},respond(){},respondError(){},close:async()=>{stops++;},
   async request(method,params:any){if(method==='account/login/start')return {type:'apiKey'};if(method==='account/read')return {account:{type:'apiKey'}};
    if(method==='thread/start')return {thread:{id:'thread'},cwd:params.cwd,runtimeWorkspaceRoots:[params.cwd],activePermissionProfile:{id:params.permissions},approvalPolicy:'never',sandbox:{type:'readOnly',networkAccess:false}};
    if(method==='turn/start'){sends++;return {turn:{id:'turn',status:'inProgress'}};}return {};}};}});
 await gateway.connection.connect({connectionId:'same',apiKey:'synthetic'});
 const binding:any=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'discussion'});
 const run:any=await gateway.runtime.dispatch('send',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,clientMessageId:'m',input:'synthetic'});
 for(const close of [...closes])close();await recovered.promise;
 await gateway.connection.connect({connectionId:'same',apiKey:'synthetic'});
 const snapshot=await gateway.runtime.snapshot({projectId:'p',sessionId:'s'});
 assert.equal(snapshot.runId,run.id);assert.equal(snapshot.state,'recovery_required');assert.equal(snapshot.canSend,false);
 assert.equal(sends,1);assert.equal(generations,2);assert.equal(stops,1);
 closes[0]();assert.equal(gateway.connection.status().verified,true);
});

test('gateway shutdown waits for pending connection creation and closes it before initialization',async()=>{
 const gate=Promise.withResolvers<any>();let closed=false;const calls:string[]=[];
 const gateway=createLiveGateway({store:{projects:async()=>[]} as any,profileId:'fixture',actorId:'runtime',isEnabled:()=>true,providerAuthority:()=>true,rpcFactory:()=>gate.promise});
 const connecting=gateway.connection.connect({connectionId:'c',apiKey:'synthetic'});const observed=assert.rejects(connecting,{code:'runtime_stopping'});
 let finished=false;const stopping=gateway.close().then(()=>{finished=true;});await Promise.resolve();const finishedEarly=finished;
 gate.resolve({generation:'g',notify(){},onClosed(){return()=>{};},subscribe(){return()=>{};},respond(){},respondError(){},
  request:async(method:string)=>{calls.push(method);return method==='account/login/start'?{type:'apiKey'}:method==='account/read'?{account:{type:'apiKey'}}:{};},close:async()=>{closed=true;}});
 await observed;await stopping;assert.equal(finishedEarly,false);assert.equal(closed,true);assert.deepEqual(calls,[]);
});

test('EOF during disconnect cannot start a replacement until the connection action finishes',async()=>{
 let generations=0;const callbacks:Array<()=>void>=[];const logout=Promise.withResolvers<void>();const entered=Promise.withResolvers<void>();
 const gateway=createLiveGateway({store:{projects:async()=>[]} as any,profileId:'fixture',actorId:'runtime',isEnabled:()=>true,providerAuthority:()=>true,
  rpcFactory:async()=>({generation:`g${++generations}`,notify(){},subscribe(){return()=>{};},onClosed(next){callbacks.push(()=>next('runtime_eof'));return()=>{};},respond(){},respondError(){},close:async()=>{},
   async request(method){if(method==='account/login/start')return {type:'apiKey'};if(method==='account/read')return {account:{type:'apiKey'}};if(method==='account/logout'){entered.resolve();await logout.promise;}return {};}})});
 await gateway.connection.connect({connectionId:'c',apiKey:'synthetic'});const disconnecting=gateway.connection.disconnect();await entered.promise;
 for(const callback of callbacks)callback();
 try{await assert.rejects(()=>gateway.connection.connect({connectionId:'c',apiKey:'synthetic'}),{code:'connection_busy'});}finally{logout.resolve();await disconnecting;await gateway.close();}
 assert.equal(generations,1);
});

test('legacy default account recovery is fenced before thread access and leaves durable rows unchanged',async(t)=>{
 const {createHash}=await import('node:crypto');
 const root=await mkdtemp(join(tmpdir(),'paos-legacy-profile-'));const store=await openLocalStore({databasePath:join(root,'store.sqlite')});
 let gatewayCleanup=async()=>{};t.after(async()=>{await gatewayCleanup();await store.close();await rm(root,{recursive:true,force:true});});
 await store.registerProject({id:'p',keyPrefix:'TEST',canonicalRoot:root,rootIdentity:'fixture-root',authorityMode:'sql'});
 const ports=createRuntimeStoragePorts(store,{actorId:'runtime'});
 const accountId=createHash('sha256').update(JSON.stringify(['default','same','synthetic'])).digest('hex');
 const binding={id:'b',projectId:'p',sessionId:'s',accountId,workspaceRoot:root,directoryIdentity:'fixture-root',mode:'execution' as const,profileId:'fixture',generation:'old',threadId:'thread'};
 const run={id:'r',bindingId:'b',projectId:'p',sessionId:'s',accountId,generation:'old',threadId:'thread',turnId:'turn',clientMessageId:'m',inputDigest:'digest',taskId:null,scopeDigest:null,state:'running' as const};
 await ports.saveBinding(binding);await ports.appendIntent(run);const before=await ports.recoverable('p');
 const methods:string[]=[];let closed=0;
 const gateway=createLiveGateway({store,profileId:'profile_'+'a'.repeat(64),actorId:'test',isEnabled:()=>true,providerAuthority:()=>true,
  rpcFactory:async()=>({generation:'new',notify(){},onClosed(){return()=>{};},subscribe(){return()=>{};},close:async()=>{closed++;},respond(){},respondError(){},
   async request(method){methods.push(method);if(method==='account/login/start')return {type:'apiKey'};if(method==='account/read')return {account:{type:'apiKey'}};return {};}})});
 gatewayCleanup=()=>gateway.close();
 await assert.rejects(()=>gateway.connection.connect({connectionId:'same',apiKey:'synthetic'}),{code:'account_mismatch'});
 assert.equal(methods.some(method=>/^(thread|turn)\//.test(method)),false);assert.equal(closed,1);
 assert.deepEqual(await ports.recoverable('p'),before);
});

test('gateway defaults deny process creation and fences changed project identity before thread/start',async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-gateway-'));const store=await openLocalStore({databasePath:join(root,'store.sqlite')});
 let gatewayCleanup=async()=>{};t.after(async()=>{await gatewayCleanup();await store.close();await rm(root,{recursive:true,force:true});});
 await store.registerProject({id:'p',keyPrefix:'TEST',canonicalRoot:root,rootIdentity:'different-root',authorityMode:'sql'});
 await store.write({projectId:'p',actorId:'test',idempotencyKey:'session',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 let factories=0;let threads=0;
 const rpcFactory=async()=>{factories++;return {generation:'g',notify(){},onClosed(){return()=>{};},subscribe(){return()=>{};},close:async()=>{},respond(){},respondError(){},
  async request(method:string){if(method==='initialize')return {};if(method==='account/login/start')return {type:'apiKey'};if(method==='account/read')return {account:{type:'apiKey'}};
   if(method==='thread/start'){threads++;throw new Error('unexpected');}return {};}};};
 const denied=createLiveGateway({store,profileId:'fixture',actorId:'test',rpcFactory});
 await assert.rejects(denied.connection.connect({connectionId:'c',apiKey:'synthetic'}),{code:'runtime_unverified'});assert.equal(factories,0);
 const gateway=createLiveGateway({store,profileId:'fixture',actorId:'test',rpcFactory,isEnabled:()=>true,providerAuthority:()=>true});
 gatewayCleanup=()=>gateway.close();
 await gateway.connection.connect({connectionId:'c',apiKey:'synthetic'});
 await assert.rejects(gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution',workspaceRoot:'untrusted',accountId:'untrusted'}),{code:'project_root_changed'});
 assert.equal(threads,0);
});

test('runtime storage keeps recoverable metadata and visible messages across SQLite reopen',async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-runtime-storage-'));let store=await openLocalStore({databasePath:join(root,'store.sqlite')});
 let gatewayCleanup=async()=>{};t.after(async()=>{await gatewayCleanup();await store.close();await rm(root,{recursive:true,force:true});});
 await store.registerProject({id:'p',keyPrefix:'TEST',canonicalRoot:root,rootIdentity:'fixture-root',authorityMode:'sql'});
 let ports=createRuntimeStoragePorts(store,{actorId:'runtime'});
 const binding={id:'b',projectId:'p',sessionId:'s',accountId:'c',workspaceRoot:root,directoryIdentity:'fixture-root',mode:'execution' as const,profileId:'fixture',generation:'g',threadId:'thread'};
 const run={id:'r',bindingId:'b',projectId:'p',sessionId:'s',accountId:'c',generation:'g',threadId:'thread',turnId:'turn',clientMessageId:'m',inputDigest:'digest',taskId:null,scopeDigest:null,state:'running' as const};
 await ports.saveBinding(binding);await ports.appendIntent(run);
 await ports.saveVisibleMessage({projectId:'p',sessionId:'s',bindingId:'b',runId:'r',sourceItemId:'message',revision:'rev',role:'assistant',text:'visible final'});
 await ports.saveCheck!({id:'synthetic-check',projectId:'p',bindingId:'b',sessionId:'s',runId:'r',taskId:null,itemId:'check',itemType:'commandExecution',status:'failed',outcome:'exit_1',coverage:'runtime_reported'});
 await store.close();store=await openLocalStore({databasePath:join(root,'store.sqlite')});ports=createRuntimeStoragePorts(store,{actorId:'runtime'});
 assert.deepEqual(await ports.recoverable('p'),[{binding,run}]);
 assert.equal((await ports.findRun('b','m'))?.id,'r');
 assert.equal((await store.list('p',{kind:'message'}))[0].body,'visible final');
 assert.equal((await ports.loadChecks!('p','b'))[0].status,'failed');
});

test('protected gateway scrubs synthetic credential echoes from finals and discards raw errors',{timeout:5000},async(t)=>{
 const {bindProject}=await import('../../apps/local-service/src/adapters/project-sources.ts');
 const root=await mkdtemp(join(tmpdir(),'paos-gateway-secret-'));const rootPin=await bindProject('p',root);
 const store=await openLocalStore({databasePath:join(root,'store.sqlite')});
 let gatewayCleanup=async()=>{};t.after(async()=>{await gatewayCleanup();await store.close();await rm(root,{recursive:true,force:true});});
 await store.registerProject({id:'p',keyPrefix:'TEST',canonicalRoot:rootPin.workspaceRoot,rootIdentity:rootPin.directoryIdentity,authorityMode:'sql'});
 await store.write({projectId:'p',actorId:'test',idempotencyKey:'task-seed',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:runtimeTaskId,kind:'task',data:fixtureTask()}}]});
 await store.write({projectId:'p',actorId:'test',idempotencyKey:'session',expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 const secret='synthetic-credential-canary';const output:unknown[]=[];const runtimeCalls:Array<{method:string;params:any}>=[];let listener:(message:Record<string,unknown>)=>void=()=>{};
 let dispatched=0;let committed:()=>void=()=>{};let terminal:()=>void=()=>{};
 const finalCommit=new Promise<void>((resolve)=>committed=resolve);
 const terminalCommit=new Promise<void>((resolve)=>terminal=resolve);
 const gateway=createLiveGateway({store,profileId:'fixture',actorId:'test',isEnabled:()=>true,providerAuthority:()=>true,
 onEvent(event){output.push(event);if(event.kind==='message_committed'&&(event.message as any).role==='assistant')committed();if(event.kind==='run'&&(event.run as any).state==='completed')terminal();},
 rpcFactory:async()=>({generation:'g',notify(){},onClosed(){return()=>{};},subscribe(next){listener=next;return()=>{};},close:async()=>{},respond(){},respondError(){},
 async request(method,params:any){
  if(['thread/start','turn/start'].includes(method))runtimeCalls.push({method,params});
  if(method==='initialize')return {};if(method==='account/login/start')return {type:'apiKey'};if(method==='account/read')return {account:{type:'apiKey'}};
  if(method==='thread/start')return {thread:{id:'thread'},cwd:params.cwd,runtimeWorkspaceRoots:[params.cwd],activePermissionProfile:{id:params.permissions},approvalPolicy:params.approvalPolicy,sandbox:{type:params.permissions==='paos_execution'?'workspaceWrite':'readOnly',networkAccess:false,writableRoots:[],excludeSlashTmp:true,excludeTmpdirEnvVar:true}};
  if(method==='turn/start'){if(dispatched++)throw new Error(secret);return {turn:{id:'turn',status:'inProgress'}};}return {};
 }})});
 gatewayCleanup=()=>gateway.close();
 const status=await gateway.connection.connect({connectionId:'connection',apiKey:secret});
 assert.equal(status.verified,true);assert.equal(status.modelAccess,'unverified');
 const binding:any=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 const input={projectId:'p',sessionId:'s',bindingId:binding.bindingId,clientMessageId:'m',input:'synthetic',taskId:runtimeTaskId,scopeDigest:'untrusted-browser-value'};
 const first:any=await gateway.runtime.dispatch('send',input);
 const duplicate:any=await gateway.runtime.dispatch('send',input);
 assert.equal(first.id,duplicate.id);assert.equal('scopeDigest' in first,false);
 assert.notEqual(((await store.list('p',{kind:'run'}))[0].data.runtimeRun as any).scopeDigest,'untrusted-browser-value');
 listener({id:88,method:'item/commandExecution/requestApproval',params:{threadId:'thread',turnId:'turn',itemId:'approval-check',command:'synthetic-check',cwd:rootPin.workspaceRoot}});
 let approvalState=await gateway.runtime.snapshot({projectId:'p',sessionId:'s'});
 assert.equal(approvalState.pendingApprovals[0].state,'pending');
 await gateway.runtime.dispatch('approve',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,runId:first.id,generation:'g',requestId:88,decision:'decline'});
 approvalState=await gateway.runtime.snapshot({projectId:'p',sessionId:'s'});
 assert.equal(approvalState.pendingApprovals[0]?.state,'response_sent');
 listener({method:'serverRequest/resolved',params:{threadId:'thread',requestId:88}});
 const approvalDeadline=Date.now()+1000;
 do {approvalState=await gateway.runtime.snapshot({projectId:'p',sessionId:'s'});}while(approvalState.pendingApprovals.length&&Date.now()<approvalDeadline);
 assert.equal(approvalState.pendingApprovals.length,0);
 listener({method:'item/started',params:{threadId:'thread',turnId:'turn',item:{id:'unknown-phase',type:'agentMessage',text:''}}});
 listener({method:'item/agentMessage/delta',params:{threadId:'thread',turnId:'turn',itemId:'unknown-phase',delta:secret.slice(0,10)}});
 listener({method:'item/agentMessage/delta',params:{threadId:'thread',turnId:'turn',itemId:'unknown-phase',delta:secret.slice(10)}});
 const phaseDeadline=Date.now()+1000;let unknownPhase=await gateway.runtime.snapshot({projectId:'p',sessionId:'s'});
 while(unknownPhase.streaming.phaseStatus==='not_observed'&&Date.now()<phaseDeadline)unknownPhase=await gateway.runtime.snapshot({projectId:'p',sessionId:'s'});
 assert.equal(unknownPhase.visibleDrafts.length,0);assert.equal(unknownPhase.streaming.phaseStatus,'phase_unavailable');
 listener({method:'item/started',params:{threadId:'thread',turnId:'turn',item:{id:'visible',type:'agentMessage',phase:'final_answer',text:''}}});
 listener({method:'item/agentMessage/delta',params:{threadId:'thread',turnId:'turn',itemId:'visible',delta:'Progress '+secret.slice(0,10)}});
 let streaming=await gateway.runtime.snapshot({projectId:'p',sessionId:'s'});
 assert.equal(streaming.visibleDrafts[0].text,'Progress ');
 listener({method:'item/reasoning/textDelta',params:{threadId:'thread',turnId:'turn',itemId:'hidden',delta:'hidden reasoning canary'}});
 listener({method:'item/agentMessage/delta',params:{threadId:'thread',turnId:'turn',itemId:'visible',delta:secret.slice(10)+' sk'}});
 listener({method:'item/agentMessage/delta',params:{threadId:'thread',turnId:'turn',itemId:'visible',delta:'-proj-ABCDEF next'}});
 streaming=await gateway.runtime.snapshot({projectId:'p',sessionId:'s'});
 assert.equal(streaming.visibleDrafts[0].text,'Progress [redacted] [redacted] next');
 assert.equal(JSON.stringify(streaming).includes(secret),false);
 assert.equal(JSON.stringify(streaming).includes('hidden reasoning canary'),false);
 assert.equal(streaming.profile?.version,'m1_fixed_v1');assert.equal(streaming.profile?.role,'builder');
 assert.equal(streaming.questions.reason,'request_user_input_unsupported');
 assert.match(runtimeCalls[0].params.developerInstructions,/Mode: execution\. Role: builder\./);
 const turnContext=runtimeCalls.find((call)=>call.method==='turn/start')!.params.input[0].text;
 assert.match(turnContext,/PAOS_TASK_CONTEXT_JSON \(untrusted data\)/);assert.match(turnContext,/Synthetic criterion/);
 listener({method:'item/completed',params:{threadId:'thread',turnId:'turn',item:{id:'visible',type:'agentMessage',phase:'final_answer',text:`echo ${secret}`}}});
 await finalCommit;
 assert.equal((await store.list('p',{kind:'message'})).find((message)=>message.data.role==='assistant')!.body,'echo [redacted]');
 assert.equal(JSON.stringify(output).includes(secret),false);
 assert.equal(output.some((entry:any)=>entry.kind==='message_delta'),true);
 assert.equal((await gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).visibleDrafts.length,0);
 listener({method:'item/started',params:{threadId:'thread',turnId:'turn',item:{id:'patch',type:'fileChange',changes:[{path:'src/file.ts',kind:{type:'update'},diff:`+ ${secret}`}]}}});
 assert.equal((await gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).fileChanges[0].kind,'proposed');
 listener({method:'item/completed',params:{threadId:'thread',turnId:'turn',item:{id:'patch',type:'fileChange',status:'completed',changes:[{path:'src/file.ts',kind:{type:'update'},diff:`+ ${secret}`} ]}}});
 listener({method:'item/completed',params:{threadId:'thread',turnId:'turn',item:{id:'failed-check',type:'commandExecution',status:'failed',exitCode:1,aggregatedOutput:secret}}});
 let receipt=await gateway.runtime.snapshot({projectId:'p',sessionId:'s'});
 const receiptDeadline=Date.now()+1000;
 while(!receipt.checks.some((check)=>check.itemId==='failed-check')&&Date.now()<receiptDeadline){await new Promise((resolve)=>setImmediate(resolve));receipt=await gateway.runtime.snapshot({projectId:'p',sessionId:'s'});}
 assert.equal(receipt.fileChanges[0].kind,'actual');assert.equal(receipt.fileChanges[0].coverage,'partial');
 assert.equal(receipt.fileChanges[0].diff,'+ [redacted]');assert.equal(receipt.checks.find((check)=>check.itemId==='failed-check')!.status,'failed');
 listener({method:'item/started',params:{threadId:'thread',turnId:'turn',item:{id:'external-patch',type:'fileChange',changes:[{path:'../foreign.ts',kind:{type:'update'},diff:`+ ${secret}`}]}}});
 const external=(await gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).fileChanges.find((change)=>change.kind==='external')!;
 assert.equal(external.coverage,'unavailable');assert.equal(external.diff,undefined);
 assert.equal(JSON.stringify(await store.list('p',{kind:'evidence'})).includes(secret),false);
 listener({method:'turn/completed',params:{threadId:'thread',turn:{id:'turn',status:'completed'}}});
 await terminalCommit;
 assert.equal((await gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).checks.find((check)=>check.itemId==='failed-check')!.status,'failed');
 assert.equal((await gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).canSend,true);
 await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'discussion'});
 assert.equal((await gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).mode,'discussion');
 await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 assert.equal((await gateway.runtime.snapshot({projectId:'p',sessionId:'s'})).mode,'execution');
 const reviewed=(await store.get('p',runtimeTaskId))!;
 await store.write({projectId:'p',actorId:'u',idempotencyKey:'reviewed-second-send',requireIdle:true,expectedAuthorityEpoch:1,changes:[{expectedRevision:reviewed.revision,entity:{id:runtimeTaskId,kind:'task',data:{...reviewed.data,status:'ready'}}}]});
 const result:any=await gateway.runtime.dispatch('send',{...input,clientMessageId:'second'});
 assert.equal(result.state,'recovery_required');
 assert.equal(JSON.stringify(await store.list('p',{kind:'run'})).includes(secret),false);
});

test('replacing a credential under the same alias cannot recover the previous account scope',async(t)=>{
 const {bindProject}=await import('../../apps/local-service/src/adapters/project-sources.ts');
 const {createConnectionBroker}=await import('../../apps/local-service/src/connections/broker.ts');
 const root=await mkdtemp(join(tmpdir(),'paos-account-scope-'));const pin=await bindProject('p',root);
 const store=await openLocalStore({databasePath:join(root,'store.sqlite')});
 let gatewayCleanup=async()=>{};t.after(async()=>{await gatewayCleanup();await store.close();await rm(root,{recursive:true,force:true});});
 await store.registerProject({id:'p',keyPrefix:'TEST',canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'sql'});
 const request=async(method:string)=>method==='account/login/start'?{type:'apiKey'}:method==='account/read'?{account:{type:'apiKey'}}:{};
 const previous=createConnectionBroker({profileId:'fixture',request});
 await previous.connect({connectionId:'same-alias',apiKey:'synthetic-old-credential'});
 const oldScope=previous.accountScopeId()!;
 const ports=createRuntimeStoragePorts(store,{actorId:'test'});
 const binding={id:'b',projectId:'p',sessionId:'s',accountId:oldScope,workspaceRoot:pin.workspaceRoot,directoryIdentity:pin.directoryIdentity,mode:'execution' as const,profileId:'fixture',generation:'old',threadId:'thread'};
 await ports.saveBinding(binding);
 await ports.appendIntent({id:'r',bindingId:'b',projectId:'p',sessionId:'s',accountId:oldScope,generation:'old',threadId:'thread',turnId:'turn',clientMessageId:'m',inputDigest:'input-digest',taskId:null,scopeDigest:null,state:'recovery_required'});
 let runtimeCalls=0;
 const gateway=createLiveGateway({store,profileId:'fixture',actorId:'test',isEnabled:()=>true,providerAuthority:()=>true,
 rpcFactory:async()=>({generation:'new',notify(){},onClosed(){return()=>{};},subscribe(){return()=>{};},close:async()=>{},respond(){},respondError(){},
 async request(method){if(method==='initialize')return {};if(method.startsWith('account/'))return request(method);runtimeCalls++;return {};}})});
 gatewayCleanup=()=>gateway.close();
 await assert.rejects(gateway.connection.connect({connectionId:'same-alias',apiKey:'synthetic-replacement-credential'}),{code:'account_mismatch'});
 assert.equal(runtimeCalls,0);assert.equal(gateway.connection.status().state,'disconnected');
 assert.equal(JSON.stringify(gateway.connection.status()).includes(oldScope),false);
});

