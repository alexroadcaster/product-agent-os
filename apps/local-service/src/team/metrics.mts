import type {LocalStore,StoredEntity} from '../storage/local-store.mts';
import {projectTaskTime} from '../events/task-time.ts';
import type {TaskTimeEvent} from '../../../../packages/contracts/time/task-time.ts';
import type {RunMetrics,RunMetric,ObservedDuration,MediatedCommands,AgentMetric} from '../../../../packages/contracts/telemetry/run-metrics.ts';
import {taskManagerSnapshot} from '../task-manager/service.mts';
import {workflowCategory} from '../../../../packages/contracts/workflows/helpers.ts';

const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
const object=(v:unknown):Record<string,any>=>v&&typeof v==='object'&&!Array.isArray(v)?v as Record<string,any>:{};
const missingDuration=(reason:string):ObservedDuration=>({seconds:null,confirmedMilliseconds:0,complete:false,openIntervals:0,unresolvedIntervals:0,reason});
function duration(projectId:string,row:StoredEntity):ObservedDuration{
 // Adapt a run-only scope for the existing interval projector; no fictional task ID is persisted or returned.
 const events=(Array.isArray(row.data.timeline)?row.data.timeline:Array.isArray(row.data.runTimeline)?row.data.runTimeline.map((e:any)=>({...e,taskId:'@run:'+row.id})):[]) as TaskTimeEvent[];
 if(!events.length)return missingDuration('run_interval_receipts_not_observed');
 if(events.some(e=>e.runId!==row.id||e.projectId!==projectId))return missingDuration('interval_scope_mismatch');
 try{const value=projectTaskTime({projectId,taskId:events[0].taskId},events);return {seconds:value.actualDurationMs===null?null:value.actualDurationMs/1000,confirmedMilliseconds:value.confirmedElapsedMs,complete:value.actualDurationMs!==null,openIntervals:value.openIntervalCount,unresolvedIntervals:value.unresolvedIntervalCount,...(value.actualDurationMs===null?{reason:'open_or_unresolved_intervals'}:{})};}catch{return missingDuration('invalid_interval_receipts');}
}
function commands(run:Record<string,any>,observed:boolean):MediatedCommands{
 if(!observed)return {requested:null,dispatched:null,completed:null,failed:null,declined:null,uncertain:null};
 const ops=[...new Map((Array.isArray(run.operations)?run.operations:[]).filter((o:any)=>typeof o?.operationId==='string').map((o:any)=>[o.operationId,o])).values()] as any[];
 return {requested:ops.length,dispatched:ops.filter(o=>['dispatching','completed','recovery_required'].includes(o.state)).length,completed:ops.filter(o=>o.state==='completed').length,failed:ops.filter(o=>o.state==='completed'&&o.exitCode!==0).length,declined:ops.filter(o=>['declined','cancelled'].includes(o.state)).length,uncertain:ops.filter(o=>o.state==='recovery_required'||o.state==='dispatching').length};
}
function sumCommands(rows:readonly {mediatedCommands:MediatedCommands}[]):MediatedCommands{
 const result={} as MediatedCommands;for(const key of ['requested','dispatched','completed','failed','declined','uncertain'] as const)result[key]=rows.some(r=>r.mediatedCommands[key]===null)?null:rows.reduce((n,r)=>n+(r.mediatedCommands[key]??0),0);return result;
}
/** Derive numeric evidence from immutable run identities and scoped interval/operation receipts.
 * Agent rows attribute the pinned run and are not additive; no prompt, argv or output is returned or newly stored. */
export async function observedRunMetrics(store:LocalStore,projectId:string,from:string,to:string,scope:{taskId?:string;sessionId?:string;agentId?:string}={}):Promise<RunMetrics>{
 if(Object.keys(scope).some(k=>!['taskId','sessionId','agentId'].includes(k))||Object.values(scope).some(v=>typeof v!=='string'||v.length>200))fail('METRICS_SCOPE_INVALID');
 const date=(s:string)=>/^\d{4}-\d{2}-\d{2}T.*(?:Z|[+-]\d\d:\d\d)$/.test(s)&&Number.isFinite(Date.parse(s));
 if(!date(from)||!date(to)||Date.parse(from)>=Date.parse(to))fail('METRICS_PERIOD_INVALID');
 const [records,snapshot]=await Promise.all([store.projectEntities(projectId,{kinds:['run']}),taskManagerSnapshot(store,projectId)]);
 const runs:RunMetric[]=[];
 for(const row of records){if(row.deleted)continue;const run=object(row.data.appAgentRun??row.data.runtimeRun),timeline=(Array.isArray(row.data.timeline)?row.data.timeline:Array.isArray(row.data.runTimeline)?row.data.runTimeline:[]) as TaskTimeEvent[],starts=timeline.filter(e=>e.kind==='interval_started').map(e=>e.atMs).filter(Number.isFinite);
  const at=typeof run.observedStartedAt==='string'?Date.parse(run.observedStartedAt):starts.length?Math.min(...starts):NaN;
  if(!Number.isFinite(at)||at<Date.parse(from)||at>=Date.parse(to))continue;
  const pins=run.assetPins??object(run.taskContext).assetPins;
  const agentIds=[...new Set<string>((Array.isArray(pins)?pins:[]).filter(p=>p?.kind==='agent'&&typeof p.assetId==='string').map(p=>p.assetId))];
  if(scope.taskId&&scope.taskId!==(run.taskId??object(run.taskContext).taskId)||scope.sessionId&&scope.sessionId!==run.sessionId||scope.agentId&&!agentIds.includes(scope.agentId))continue;
  runs.push({runId:row.id,sessionId:typeof run.sessionId==='string'?run.sessionId:null,taskId:typeof (run.taskId??object(run.taskContext).taskId)==='string'?run.taskId??run.taskContext.taskId:null,agentIds,route:typeof run.route==='string'?run.route:row.data.appAgentRun?'codex_app_agent':'legacy_runtime_route_not_recorded',status:row.status,startedAt:new Date(at).toISOString(),sourceRevision:row.revision,duration:duration(projectId,row),mediatedCommands:commands(run,Boolean(row.data.appAgentRun))});
  if(runs.length>1000)fail('METRICS_PERIOD_TOO_BROAD');
 }
 runs.sort((a,b)=>b.startedAt.localeCompare(a.startedAt)||a.runId.localeCompare(b.runId));
 const taskById=new Map(snapshot.tasks.map(t=>[t.id,t])),groups=new Map<string,RunMetric[]>();for(const run of runs)for(const id of run.agentIds){const rows=groups.get(id)??[];rows.push(run);groups.set(id,rows);}
 const agents:AgentMetric[]=[...groups].map(([agentId,rows])=>{const taskIds=[...new Set(rows.flatMap(r=>r.taskId?[r.taskId]:[]))];return {agentId,startedRuns:rows.length,outcomes:{completed:rows.filter(r=>r.status==='completed').length,failed:rows.filter(r=>r.status==='failed').length,cancelled:rows.filter(r=>r.status==='interrupted').length,needsDecision:rows.filter(r=>r.status==='awaiting_approval').length,acceptedTasks:taskIds.filter(id=>{const task=taskById.get(id);return task&&workflowCategory(snapshot.workflows,task.data as any)==='done';}).length},durationSeconds:rows.every(r=>r.duration.complete)?rows.reduce((n,r)=>n+(r.duration.seconds??0),0):null,confirmedMilliseconds:rows.reduce((n,r)=>n+r.duration.confirmedMilliseconds,0),mediatedCommands:sumCommands(rows),tokenCount:null,cost:null,taskIds,runIds:rows.map(r=>r.runId),sessionIds:[...new Set(rows.flatMap(r=>r.sessionId?[r.sessionId]:[]))]};});
 const result:RunMetrics={schemaVersion:'paos_run_metrics_v1',period:{from,to},denominator:records.length?runs.length:null,source:'paos_observed_run_receipts_v1',coverage:{status:'partial',reasons:['host_history_not_connected_by_selected_route','host_token_cost_tool_attestation_unavailable','agent_attribution_uses_pins_not_loaded_attestation',...(runs.some(r=>!r.duration.complete)?['duration_has_unconfirmed_intervals']:[])]},retention:{policy:'derived_from_retained_project_runs',additionalRawLogsStored:false},totals:{durationSeconds:runs.every(r=>r.duration.complete)?runs.reduce((n,r)=>n+(r.duration.seconds??0),0):null,confirmedMilliseconds:runs.reduce((n,r)=>n+r.duration.confirmedMilliseconds,0),mediatedCommands:sumCommands(runs),tokenCount:null,cost:null,hostToolCalls:null},agents,runs};
 if(Buffer.byteLength(JSON.stringify(result))>1024*1024)fail('METRICS_PERIOD_TOO_BROAD');return result;
}
