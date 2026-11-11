import assert from 'node:assert/strict';
import {test,type TestContext} from 'node:test';
import {mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createRuntimeCoordinator,type RuntimeRun} from '../../apps/local-service/src/runtime/codex/coordinator.ts';
import {fixtureTask,runtimeTaskId} from './runtime-adapter-time.fixture.mts';

async function fixture(t:TestContext,mode:'execution'|'discussion'='discussion') {
 const root=await mkdtemp(join(tmpdir(),'paos-race-'));t.after(()=>rm(root,{recursive:true,force:true}));
 let authorize=async()=>true;let append=async()=>{};let transition=async(_run:RuntimeRun)=>{};let interruptRpc=async()=>({});let beforeThread=async()=>{};let readThread=async()=>({});let listener:(event:any)=>void=()=>{};let closed:()=>void=()=>{};
 const calls:string[]=[];const responses:unknown[]=[];const saved:RuntimeRun[]=[];
 const coordinator=createRuntimeCoordinator({isEnabled:()=>true,authorizeDispatch:()=>authorize(),
  persistence:{findRun:async()=>null,saveBinding:async()=>{},appendIntent:async(run)=>{await append();saved.push({...run});},updateRun:async(run)=>{await transition(run);saved.push({...run});},saveVisibleMessage:async()=>{}},
  rpc:{generation:'g',notify(){},snapshot:()=>({generation:'g',status:'open',pending:0,stderrBytes:0}),close:async()=>{},
   subscribe(next){listener=next;return()=>{};},onClosed(next){closed=()=>next('runtime_eof');return()=>{};},respond(_id,result){responses.push(result);},respondError(){},
   async request(method,params:any){calls.push(method);if(method==='turn/interrupt')return interruptRpc();if(method==='thread/read')return readThread();if(method==='thread/start'){await beforeThread();return {thread:{id:'thread'},cwd:params.cwd,runtimeWorkspaceRoots:[params.cwd],activePermissionProfile:{id:params.permissions},approvalPolicy:params.approvalPolicy,sandbox:{type:params.permissions==='paos_execution'?'workspaceWrite':'readOnly',networkAccess:false,writableRoots:[],excludeSlashTmp:true,excludeTmpdirEnvVar:true}};}
    if(method==='turn/start')return {turn:{id:'turn',status:'inProgress'}};return {};}}});
 const input={projectId:'p',sessionId:'s',accountId:'a',workspaceRoot:root,profileId:'profile',mode};
 const binding=await coordinator.openBinding(input);
 const send=()=>coordinator.send({bindingId:binding.id,clientMessageId:'message',input:'synthetic',...(mode==='execution'?{taskId:runtimeTaskId,scopeDigest:'scope',targetRevision:1,taskContext:{...fixtureTask(),taskId:runtimeTaskId,revision:1,files:[]}}:{})});
 return {coordinator,binding,input,calls,responses,saved,send,event:(value:any)=>listener(value),eof:()=>closed(),setAuthorize:(next:()=>Promise<boolean>)=>{authorize=next;},setAppend:(next:()=>Promise<void>)=>{append=next;},setThreadStart:(next:()=>Promise<void>)=>{beforeThread=next;},setThreadRead:(next:()=>Promise<any>)=>{readThread=next;},setInterrupt:(next:()=>Promise<any>)=>{interruptRpc=next;},setTransition:(next:(run:RuntimeRun)=>Promise<void>)=>{transition=next;}};
}

test('a rejected Stop response cannot turn an already completed run back into recovery',async(t)=>{
 const f=await fixture(t);const run=await f.send();const gate=Promise.withResolvers<any>();const entered=Promise.withResolvers<void>();
 f.setInterrupt(()=>{entered.resolve();return gate.promise;});const interrupting=f.coordinator.interrupt({bindingId:f.binding.id,runId:run.id});await entered.promise;
 f.event({method:'turn/completed',params:{threadId:'thread',turn:{id:'turn',status:'completed'}}});await f.coordinator.flush();gate.reject(new Error('late RPC error'));
 assert.equal((await interrupting).state,'completed');assert.equal(f.saved.at(-1)?.state,'completed');
});

test('Stop delayed in persistence cannot send an interrupt after shutdown wins',async(t)=>{
 const f=await fixture(t);const run=await f.send();const gate=Promise.withResolvers<void>();const entered=Promise.withResolvers<void>();
 f.setTransition(async(state)=>{if(state.state==='interrupt_requested'){entered.resolve();await gate.promise;}});
 const interrupting=f.coordinator.interrupt({bindingId:f.binding.id,runId:run.id});await entered.promise;const stopping=f.coordinator.prepareShutdown();gate.resolve();
 assert.equal((await interrupting).state,'recovery_required');await stopping;assert.equal(f.calls.includes('turn/interrupt'),false);
});

test('a delayed mode binding cannot publish after a run starts on the prior binding',async(t)=>{
 const f=await fixture(t);const gate=Promise.withResolvers<void>();const entered=Promise.withResolvers<void>();
 f.setThreadStart(()=>{entered.resolve();return gate.promise;});const opening=f.coordinator.openBinding({...f.input,mode:'planning'});
 const observed=assert.rejects(opening,{code:'runtime_busy'});await entered.promise;const run=await f.send();gate.resolve();await observed;
 assert.equal(f.coordinator.snapshot(f.binding.id).run?.id,run.id);
});

test('shutdown drains a started reconciliation before persisting recovery or closing storage',async(t)=>{
 const f=await fixture(t);await f.send();const gate=Promise.withResolvers<any>();const entered=Promise.withResolvers<void>();
 f.setThreadRead(()=>{entered.resolve();return gate.promise;});const reconciling=f.coordinator.reconcile({bindingId:f.binding.id,accountId:'a'});await entered.promise;
 let stopped=false;const stopping=f.coordinator.prepareShutdown().then(()=>{stopped=true;});await Promise.resolve();await Promise.resolve();const stoppedEarly=stopped;
 gate.resolve({thread:{id:'thread',turns:[{id:'turn',status:'completed'}]}});await reconciling;await stopping;
 assert.equal(stoppedEarly,false);assert.equal(f.saved.at(-1)?.state,'completed');
 await assert.rejects(()=>f.coordinator.reconcile({bindingId:f.binding.id,accountId:'a'}),{code:'runtime_stopping'});
});

test('shutdown fences delayed authorization and waits for the pending public send',async(t)=>{
 const f=await fixture(t);const gate=Promise.withResolvers<boolean>();const entered=Promise.withResolvers<void>();
 f.setAuthorize(()=>{entered.resolve();return gate.promise;});
 const sending=f.send();const observed=assert.rejects(sending,{code:'runtime_stopping'});await entered.promise;
 let finished=false;const stopping=f.coordinator.prepareShutdown().then(()=>{finished=true;});await Promise.resolve();
 const finishedBeforeRelease=finished;gate.resolve(true);await observed;await stopping;
 assert.equal(finishedBeforeRelease,false);assert.equal(f.calls.includes('turn/start'),false);assert.equal(f.saved.length,0);
});

test('shutdown after intent starts preserves recovery and never dispatches turn/start',async(t)=>{
 const f=await fixture(t);const gate=Promise.withResolvers<void>();const entered=Promise.withResolvers<void>();
 f.setAppend(()=>{entered.resolve();return gate.promise;});const sending=f.send();await entered.promise;
 const stopping=f.coordinator.prepareShutdown();gate.resolve();const run=await sending;await stopping;
 assert.equal(f.calls.includes('turn/start'),false);assert.equal(run.state,'recovery_required');assert.equal(f.saved.at(-1)?.state,'recovery_required');
});

test('active run prevents opening a different mode and keeps its controls addressable',async(t)=>{
 const f=await fixture(t);const run=await f.send();
 await assert.rejects(()=>f.coordinator.openBinding({...f.input,mode:'planning'}),{code:'runtime_busy'});
 assert.equal(f.coordinator.snapshot(f.binding.id).run?.id,run.id);assert.equal(f.calls.filter(method=>method==='thread/start').length,1);
});

for(const transition of ['resolved','terminal','eof','shutdown'] as const)test(`approval cannot be accepted after ${transition} wins delayed authorization`,async(t)=>{
 const f=await fixture(t,'execution');const run=await f.send();
 f.event({id:7,method:'item/commandExecution/requestApproval',params:{threadId:'thread',turnId:'turn',itemId:'command',command:'synthetic',cwd:f.binding.workspaceRoot}});await f.coordinator.flush();
 const gate=Promise.withResolvers<boolean>();const entered=Promise.withResolvers<void>();f.setAuthorize(()=>{entered.resolve();return gate.promise;});
 const answering=f.coordinator.answerApproval({bindingId:f.binding.id,runId:run.id,generation:'g',requestId:7,decision:'accept'});
 const observed=assert.rejects(answering);await entered.promise;
 let stopping:Promise<void>|undefined;
 if(transition==='resolved')f.event({method:'serverRequest/resolved',params:{threadId:'thread',requestId:7}});
 if(transition==='terminal')f.event({method:'turn/completed',params:{threadId:'thread',turn:{id:'turn',status:'completed'}}});
 if(transition==='eof')f.eof();if(transition==='shutdown')stopping=f.coordinator.prepareShutdown();
 await f.coordinator.flush();gate.resolve(true);await observed;if(stopping)await stopping;
 assert.equal(f.responses.some((value:any)=>value.decision==='accept'),false);
});
