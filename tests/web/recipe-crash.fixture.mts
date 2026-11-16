import {fixture} from './recipe-fixture.mts';
// Parent owns this isolated process and its root. No cleanup runs before the deliberate crash.
const phase=process.argv[2]??'terminal';
if(!['before-dispatch','after-dispatch','terminal'].includes(phase))throw Error('INVALID_CRASH_PHASE');
const f=await fixture({after(){}} as any),{execution}=await f.start();
let firstRunId:string|undefined;
if(phase!=='before-dispatch'){
 await f.service.tick();
 if(phase==='terminal')firstRunId=(await f.report()).runId;
 else {const claim=await f.gateway.agent('claim',f.auth);if(!claim.job)throw Error('FIXTURE_DISPATCH_MISSING');firstRunId=claim.job.runId;}
}
// IPC is emitted only after the selected public lifecycle boundary has persisted.
process.send?.({root:f.root,executionId:execution.id,firstRunId,phase});
setInterval(()=>{},1000);
