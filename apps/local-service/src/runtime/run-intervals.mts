import type {RunIntervalReceipt} from '../../../../packages/contracts/telemetry/run-metrics.ts';
/** Non-task runs retain only bounded server lifecycle receipts. Recovery never invents a confirmed end.
 * Task runs continue to use their existing task-time journal; no duplicate journal is stored for them. */
export function appendRunInterval(receipts:readonly RunIntervalReceipt[],projectId:string,runId:string,actorId:string,previousState:string|undefined,state:string,atMs:number):RunIntervalReceipt[]{
 const events=[...receipts],last=events.toReversed().find(e=>e.kind==='interval_started');
 const open=last&&!events.some(e=>e.intervalId===last.intervalId&&e.kind!=='interval_started');
 let kind:RunIntervalReceipt['kind']|undefined;
 if(state==='running'&&!open&&previousState!=='recovery_required')kind='interval_started';
 else if(open&&state==='recovery_required')kind='interval_crashed';
 else if(open&&['awaiting_approval','completed','failed','interrupted'].includes(state))kind='interval_stopped';
 if(!kind)return events;
 if(kind==='interval_started'&&events.length>9998)throw Object.assign(new Error('Run interval journal is full'),{code:'runtime_time_limit'});
 const seq=Math.max(0,...events.map(e=>e.seq))+1;
 const base={projectId,runId,actorId,source:'paos_runtime_lifecycle_v1' as const,eventId:`${runId}:run-time:${seq}`,seq,intervalId:kind==='interval_started'?`${runId}:run-interval:${seq}`:last!.intervalId,atMs};
 events.push(kind==='interval_stopped'?{...base,kind,reason:state==='awaiting_approval'?'pause':'finished'}:{...base,kind});return events;
}
