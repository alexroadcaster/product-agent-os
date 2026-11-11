import assert from 'node:assert/strict';
import {test,type TestContext} from 'node:test';
import {mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createRuntimeCoordinator,type RuntimeRun} from '../../apps/local-service/src/runtime/codex/coordinator.ts';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';

async function fixture(t:TestContext){
 const root=await mkdtemp(join(tmpdir(),'paos-reconciliation-'));t.after(()=>rm(root,{recursive:true,force:true}));
 const pin=await bindProject('p',root);let history:any={};let listener:(message:any)=>void=()=>{};let failCheck=false;let failTerminal=false;
 const messages=new Map<string,any>(),checks=new Map<string,any>(),saved:RuntimeRun[]=[],responses:any[]=[],calls:string[]=[];
 const canary='synthetic-credential-canary';
 const binding={id:'binding',projectId:'p',sessionId:'s',accountId:'account',workspaceRoot:root,directoryIdentity:pin.directoryIdentity,mode:'discussion' as const,profileId:'profile',generation:'old',threadId:'thread'};
 const run:RuntimeRun={id:'run',bindingId:'binding',projectId:'p',sessionId:'s',accountId:'account',generation:'old',threadId:'thread',turnId:'turn',clientMessageId:'message',inputDigest:'digest',taskId:null,scopeDigest:null,state:'running',canonicalUserMessageSourceId:'client:message'};
 const coordinator=createRuntimeCoordinator({isEnabled:()=>true,authorizeDispatch:()=>true,redact:text=>text.replaceAll(canary,'[REDACTED]'),
  persistence:{findRun:async()=>null,saveBinding:async()=>{},appendIntent:async()=>{},updateRun:async(run)=>{if(failTerminal&&['completed','failed','interrupted'].includes(run.state)){failTerminal=false;throw new Error('SYNTHETIC_PERSISTENCE_FAILURE');}saved.push({...run});},saveVisibleMessage:async(message)=>{messages.set(message.sourceItemId,message);},saveCheck:async(check)=>{if(failCheck){failCheck=false;throw new Error('SYNTHETIC_PERSISTENCE_FAILURE');}checks.set(check.id,check);}},
  dynamicTools:[{type:'function',name:'task_read',description:'Synthetic read',inputSchema:{type:'object'}}],domainTool:async()=>({[canary]:[{body:canary}]}),
  rpc:{generation:'new',snapshot:()=>({generation:'new',status:'open',pending:0,stderrBytes:0}),notify(){},subscribe(next){listener=next;return()=>{};},onClosed(){return()=>{};},close:async()=>{},respond(id,result){responses.push({id,result});},respondError(id){responses.push({id,error:true});},
   async request(method,params:any){calls.push(method);if(method==='thread/start')return {thread:{id:'thread'},cwd:root,runtimeWorkspaceRoots:[root],activePermissionProfile:{id:params.permissions},approvalPolicy:'never',sandbox:{type:'readOnly',networkAccess:false}};
    if(method==='turn/start')return {turn:{id:'turn',status:'inProgress'}};assert.equal(method,'thread/read');return history;}}});
 return {coordinator,binding,run,messages,checks,saved,responses,calls,canary,event:(message:any)=>listener(message),history:(value:any)=>{history=value;},failNextCheck(){failCheck=true;},failNextTerminal(){failTerminal=true;},async live(){const binding=await coordinator.openBinding({projectId:'p',sessionId:'s',accountId:'account',workspaceRoot:root,mode:'discussion',profileId:'profile'});return coordinator.send({bindingId:binding.id,clientMessageId:'live-message',input:'Synthetic read'});}};
}

test('exact terminal history recovers missing final/check receipts without replay or hidden reasoning',async(t)=>{
 const f=await fixture(t);await f.coordinator.restoreRecovery({binding:f.binding,run:f.run,accountId:'account'});
 f.history({thread:{id:'thread',turns:[{id:'foreign',status:'completed',items:[{id:'foreign-final',type:'agentMessage',phase:'final_answer',text:'foreign'}]},
  {id:'turn',status:'completed',items:[{id:'reasoning',type:'reasoning',text:f.canary},{id:'commentary',type:'agentMessage',phase:'commentary',text:'hidden'},
   {id:'echo',type:'userMessage',content:[{text:'quoted context'}]},{id:'final',type:'agentMessage',phase:'final_answer',text:'Recovered '+f.canary},
   {id:'check',type:'commandExecution',status:'failed',exitCode:1}]}]}});
 assert.equal((await f.coordinator.reconcile({bindingId:'binding',accountId:'account'}))?.state,'completed');
 assert.deepEqual([...f.messages.values()].map(message=>message.text),['Recovered [REDACTED]']);
 assert.equal([...f.checks.values()][0]?.outcome,'exit_1');assert.equal(f.coordinator.snapshot('binding').checks[0]?.status,'failed');
 assert.deepEqual(f.calls,['thread/read']);assert.equal(f.saved.at(-1)?.state,'completed');
 assert.equal(await f.coordinator.reconcile({bindingId:'binding',accountId:'account'}),null);assert.equal(f.messages.size,1);
});
test('unknown dispatch ACK never infers a turn even from a malformed null-id terminal history entry',async(t)=>{
 const f=await fixture(t);await f.coordinator.restoreRecovery({binding:f.binding,run:{...f.run,turnId:null},accountId:'account'});
 f.history({thread:{id:'thread',turns:[{id:null,status:'completed',items:[{id:'final',type:'agentMessage',phase:'final_answer',text:'Must not publish'}]}]}});
 assert.equal((await f.coordinator.reconcile({bindingId:'binding',accountId:'account'}))?.state,'recovery_required');assert.equal(f.messages.size,0);
});
test('partial terminal receipt persistence can retry idempotently without a second dispatch',async(t)=>{
 const f=await fixture(t);await f.coordinator.restoreRecovery({binding:f.binding,run:f.run,accountId:'account'});
 f.history({thread:{id:'thread',turns:[{id:'turn',status:'completed',items:[{id:'final',type:'agentMessage',phase:'final_answer',text:'Recovered'},
  {id:'check',type:'commandExecution',status:'failed',exitCode:1}]}]}});f.failNextCheck();
 await assert.rejects(f.coordinator.reconcile({bindingId:'binding',accountId:'account'}));assert.equal(f.saved.at(-1)?.state,'recovery_required');
 assert.equal((await f.coordinator.reconcile({bindingId:'binding',accountId:'account'}))?.state,'completed');assert.equal(f.messages.size,1);assert.equal(f.checks.size,1);
 assert.deepEqual(f.calls,['thread/read','thread/read']);
});
test('domain tool nested content and property names are redacted before responding to runtime',async(t)=>{
 const f=await fixture(t);await f.live();f.event({id:42,method:'item/tool/call',params:{threadId:'thread',turnId:'turn',tool:'task_read',arguments:{taskId:'t'}}});await f.coordinator.flush();
 assert.equal(f.responses.length,1);assert.equal(f.responses[0].result.success,true);
 assert.equal(JSON.stringify(f.responses).includes(f.canary),false);
 assert.deepEqual(JSON.parse(f.responses[0].result.contentItems[0].text),{'[REDACTED]':[{body:'[REDACTED]'}]});
});

test('failed terminal persistence retains the recovery lease until a successful reconciliation retry',async(t)=>{
 const f=await fixture(t);await f.coordinator.restoreRecovery({binding:f.binding,run:f.run,accountId:'account'});
 f.history({thread:{id:'thread',turns:[{id:'turn',status:'completed',items:[]}]}});f.failNextTerminal();
 await assert.rejects(f.coordinator.reconcile({bindingId:'binding',accountId:'account'}));
 assert.equal(f.coordinator.snapshot('binding').run?.state,'recovery_required');
 assert.equal(f.coordinator.snapshot('binding').hasActiveRun,true);
 assert.equal(f.saved.at(-1)?.state,'recovery_required');
 assert.equal((await f.coordinator.reconcile({bindingId:'binding',accountId:'account'}))?.state,'completed');
 assert.equal(f.coordinator.snapshot('binding').hasActiveRun,false);
 assert.deepEqual(f.calls,['thread/read','thread/read']);
});
