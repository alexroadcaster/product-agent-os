import {fixture} from './recipe-fixture.mts';
// Parent owns this isolated process and its root. No cleanup runs before the deliberate crash.
const f=await fixture({after(){}} as any),{execution}=await f.start();await f.service.tick();const job=await f.report();
process.send?.({root:f.root,executionId:execution.id,firstRunId:job.runId});
setInterval(()=>{},1000);
