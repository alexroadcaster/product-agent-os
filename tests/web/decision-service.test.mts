import {test} from 'node:test';
import assert from 'node:assert/strict';
import {randomUUID} from 'node:crypto';
import {m2Fixture} from './m2-fixture.mts';
import {fixture,step} from './recipe-fixture.mts';
import {createDecisions,runtimeDecisionId} from '../../apps/local-service/src/decisions/service.mts';

const local={kind:'product',title:'Review synthetic proposal',body:'Choose whether to accept the proposal',expiresInSeconds:60,expectedAuthorityEpoch:1,idempotencyKey:'create'};
const answer=(view:any,key='answer',response='accept')=>({expectedRevision:view.revision,expectedAuthorityEpoch:1,idempotencyKey:key,response,reason:'Reviewed evidence'});
async function fake(t:Parameters<typeof m2Fixture>[0]){
 const f=await m2Fixture(t);await f.store.write({projectId:'p',actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'s',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 let clock=1000,calls=0,pending=true;const request={bindingId:'b',runId:'r',generation:'g',requestId:'op',kind:'command',state:'pending',reviewable:true,source:'native_runtime',expiresAt:61000,details:{command:'synthetic check'}};
 let send=async()=>{calls++;pending=false;return {state:'response_sent'};};const runtime={snapshot:async()=>({bindingId:'b',runId:'r',generation:'g',state:'awaiting_approval',pendingApprovals:pending?[request]:[]}),dispatch:async()=>send()};
 const service=createDecisions({store:f.store,runtime,route:()=> 'local_api_byok',now:()=>clock});const observed=await service.observe('p','s',await runtime.snapshot());const id=observed.pendingApprovals[0].decisionId;
 return {...f,id,runtime,service,request,get calls(){return calls;},advance:(ms:number)=>clock+=ms,setSend:(fn:()=>Promise<any>)=>{send=fn;},restart:()=>createDecisions({store:f.store,runtime,route:()=> 'local_api_byok',now:()=>clock})};
}

test('local product/clarification responses retain scope/diff/evidence and never dispatch runtime work',async t=>{
 const f=await m2Fixture(t),task=await f.ready();let calls=0;const service=createDecisions({store:f.store,runtime:{snapshot:async()=>({}),dispatch:async()=>{calls++;throw Error('no runtime');}}});
 const d=await service.create('p','owner',{...local,taskId:task.id,proposedDiff:'- old\n+ proposed',evidenceIds:[task.id]});assert.equal(d.diff.status,'proposed');assert.equal(d.scope.files[0].path,'fixture.txt');assert.equal(d.evidence.items[0].id,task.id);
 const input=answer(d),r=await service.respond('p',d.id,'owner',input);assert.equal(r.decision.state,'resolved');assert.deepEqual(await service.respond('p',d.id,'owner',input),r);assert.equal(calls,0);
 await assert.rejects(()=>service.respond('p',d.id,'owner',{...input,response:'return'}),{code:'IDEMPOTENCY_CONFLICT'});
 const q=await service.create('p','owner',{...local,kind:'clarification',idempotencyKey:'question'});const response=await service.respond('p',q.id,'owner',{...answer(q,'reply','answer'),answer:'Use the synthetic scope'});assert.equal(response.decision.answer,'Use the synthetic scope');assert.equal(calls,0);
});

test('expiry is durable; exact committed replay after expiry returns the original result without a new effect',async t=>{
 const f=await fake(t),d=await f.service.get('p',f.id),input=answer(d);const result=await f.service.respond('p',f.id,'owner',input);assert.equal(result.decision.delivery,'response_sent');f.advance(60000);
 assert.deepEqual(await f.service.respond('p',f.id,'owner',input),result);assert.equal(f.calls,1);
 const localDecision=await f.service.create('p','owner',{...local,idempotencyKey:'expiring-local'});f.advance(60000);await assert.rejects(()=>f.service.respond('p',localDecision.id,'owner',answer(localDecision,'expired')),{code:'DECISION_EXPIRED'});assert.equal((await f.service.get('p',localDecision.id)).state,'expired');
});

test('S09 and S22 share the same request identity and concurrent responses dispatch only once',async t=>{
 const f=await fake(t),d=await f.service.get('p',f.id),input=answer(d);const [first,second]=await Promise.all([f.service.respond('p',d.id,'owner',input),f.service.inline({projectId:'p',sessionId:'s',bindingId:'b',runId:'r',generation:'g',requestId:'op',decision:'accept'},'owner')]);assert.equal(f.calls,1);assert.equal(first.decision.id,d.id);assert.equal(second.state,'response_sent');
 await assert.rejects(()=>f.service.inline({projectId:'p',sessionId:'s',bindingId:'b',runId:'r',generation:'g',requestId:'op',decision:'decline'},'owner'));
 const restarted=f.restart();assert.equal((await restarted.get('p',d.id)).state,'resolved');assert.equal((await restarted.get('p',d.id)).history.some(h=>h.event==='response_recorded'),true);
});

test('a persisted response intent is never re-dispatched after an unknown result or restart',async t=>{
 const f=await fake(t);let sends=0;f.setSend(async()=>{sends++;throw Object.assign(new Error('Lost native acknowledgement'),{code:'approval_outcome_unknown'});});const d=await f.service.get('p',f.id),input=answer(d);
 await assert.rejects(()=>f.service.respond('p',d.id,'owner',input),{code:'approval_outcome_unknown'});const restarted=f.restart(),result=await restarted.respond('p',d.id,'owner',input);assert.equal(result.decision.state,'outcome_unknown');assert.deepEqual(result.decision.actions,[]);assert.equal(sends,1);
 await assert.rejects(()=>restarted.respond('p',d.id,'owner',answer(result.decision,'different-key')));assert.equal(sends,1);
});

test('storage failure before the durable response intent prevents any runtime effect',async t=>{
 const f=await fake(t),d=await f.service.get('p',f.id),write=f.store.write;f.store.write=async input=>{if(input.idempotencyKey.startsWith('decision-intent:'))throw Object.assign(new Error('Fixture storage failure'),{code:'STORAGE_FAILED'});return write(input);};
 await assert.rejects(()=>f.service.respond('p',d.id,'owner',answer(d)),{code:'STORAGE_FAILED'});f.store.write=write;assert.equal(f.calls,0);assert.equal((await f.service.get('p',d.id)).state,'pending');
});

test('runtime identities distinguish request type, generation, project, run and binding',()=>{
 const r={route:'codex_app_agent',bindingId:'b',runId:'r',generation:'g',requestId:1};const ids=[runtimeDecisionId('p','s',r),runtimeDecisionId('p','s',{...r,requestId:'1'}),runtimeDecisionId('p','s',{...r,generation:'g2'}),runtimeDecisionId('p2','s',r),runtimeDecisionId('p','s',{...r,runId:'r2'}),runtimeDecisionId('p','s',{...r,bindingId:'b2'})];assert.equal(new Set(ids).size,ids.length);
});

test('task scope/revision, authority and fabricated runtime permission fail closed',async t=>{
 const f=await m2Fixture(t),task=await f.ready(),service=createDecisions({store:f.store});const d=await service.create('p','owner',{...local,taskId:task.id});
 await assert.rejects(()=>service.respond('p',d.id,'owner',{...answer(d),expectedRevision:0}),{code:'REVISION_CONFLICT'});await assert.rejects(()=>service.respond('p',d.id,'owner',{...answer(d),expectedAuthorityEpoch:0}),{code:'AUTHORITY_EPOCH_CONFLICT'});
 await assert.rejects(()=>service.create('p','owner',{...local,kind:'runtime_permission',idempotencyKey:'forged'}),{code:'DECISION_KIND_FORBIDDEN'});
 await f.command({action:'save',task:{...task.data,title:'Changed semantic scope'},expectedRevision:task.revision});await assert.rejects(()=>service.respond('p',d.id,'owner',answer(d)),{code:'DECISION_SCOPE_CHANGED'});
});

test('durable App operations supply retained history and observed evidence after a terminal run',async t=>{
 const f=await fixture(t,[step('one')],2,{allowedActions:['execution','command'],maxCommandsPerRun:1});await f.start();await f.service.tick();const job=(await f.gateway.agent('claim',f.auth)).job;
 await f.gateway.agent('command',{...f.auth,runId:job.runId,operationId:'check',argv:['echo','synthetic']});const service=createDecisions({store:f.store,runtime:f.gateway.runtime,route:()=> 'codex_app_agent'});const before=await service.list('p');assert.equal(before.items.length,1);const d=before.items[0];assert.equal(d.diff.status,'unavailable');assert.equal(d.scope.files[0].path,'fixture.txt');
 await service.respond('p',d.id,'owner',answer(d));for(let i=0;i<100;i++){if((await f.gateway.agent('operation',{...f.auth,runId:job.runId,operationId:'check'})).state==='completed')break;await new Promise(r=>setTimeout(r,2));}
 await f.gateway.agent('report',{...f.auth,runId:job.runId,seq:1,idempotencyKey:'terminal',status:'completed',text:'Observed synthetic check'});const final=(await service.list('p')).items[0];assert.equal(final.state,'resolved');assert.equal(final.runtime!.operationState,'completed');assert.equal(final.evidence.items[0].status,'completed');assert.equal(JSON.stringify(final).includes('Pinned fixture role'),false);assert.equal(JSON.stringify(final).includes(f.auth.leaseToken),false);
});

test('transactional decision fence rejects task drift occurring after service validation',async t=>{
 const f=await m2Fixture(t),task=await f.ready(),service=createDecisions({store:f.store}),d=await service.create('p','owner',{...local,taskId:task.id});const write=f.store.write;let changed=false;
 f.store.write=async input=>{if(input.decisionCommand&&!changed){changed=true;await f.command({action:'save',task:{...task.data,title:'Concurrent semantic change'},expectedRevision:task.revision});}return write(input);};
 try{await assert.rejects(()=>service.respond('p',d.id,'owner',answer(d)),{code:'DECISION_SCOPE_CHANGED'});assert.equal(changed,true);}finally{f.store.write=write;}assert.equal((await service.get('p',d.id)).state,'pending');
});

test('expiry while waiting to enter SQLite is rejected at commit without a local acceptance record',async t=>{
 const f=await m2Fixture(t),service=createDecisions({store:f.store}),d=await service.create('p','owner',local);const row=(await f.store.get('p',d.id))!;const deadline=Date.now()+1000;
 await f.store.write({projectId:'p',actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'fixture-short-deadline',changes:[{expectedRevision:row.revision,entity:{id:row.id,kind:'settings',status:'pending',data:{...row.data,expiresAt:deadline}}}]});const current=await service.get('p',d.id),write=f.store.write;let crossed=false;
 f.store.write=async input=>{if(input.decisionCommand){crossed=true;await new Promise(r=>setTimeout(r,Math.max(0,deadline-Date.now()+5)));}return write(input);};try{await assert.rejects(()=>service.respond('p',d.id,'owner',answer(current)),{code:'DECISION_EXPIRED'});assert.equal(crossed,true);}finally{f.store.write=write;}
 assert.equal((await service.get('p',d.id)).state,'expired');
});

test('an observed missing or old-generation native request becomes stale before TTL without inferring a response',async t=>{
 const f=await fake(t),before=await f.service.get('p',f.id);assert.equal(before.state,'pending');await f.service.observe('p','s',{bindingId:'b',runId:'r',generation:'g2',state:'recovery_required',pendingApprovals:[]});
 const after=await f.service.get('p',f.id);assert.equal(after.state,'stale');assert.deepEqual(after.actions,[]);assert.equal(after.response,null);assert.equal(f.calls,0);
});

test('file permission diff is a runtime proposal and not fabricated observed execution evidence',async t=>{
 const f=await fake(t);const result=await f.service.observe('p','s',{bindingId:'b',runId:'r',generation:'g',state:'awaiting_approval',pendingApprovals:[{...f.request,requestId:'file',kind:'file',details:{changes:[{kind:'proposed',path:'fixture.txt',diff:'- old\n+ proposed'}]}}]});
 const d=await f.service.get('p',result.pendingApprovals[0].decisionId);assert.equal(d.diff.status,'proposed');assert.match(d.diff.text,/fixture.txt/);assert.equal(d.evidence.coverage,'unavailable');
});
