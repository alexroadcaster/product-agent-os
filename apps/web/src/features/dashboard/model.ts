import type {ManagerSnapshot} from '../../../../../packages/contracts/issues/manager.ts';
import type {StoredEntity} from '../../api/client.ts';
import {semanticStatus,isBlocked} from '../tasks/model.ts';
/** Progress is Done / non-cancelled task objects, including parents; it is not effort completion. */
export function summarizeTasks(snapshot:ManagerSnapshot<StoredEntity>){
 const counts:Record<string,number>=Object.create(null);for(const task of snapshot.tasks){const state=semanticStatus(task,snapshot.workflows)||'unknown';counts[state]=(counts[state]??0)+1;}
 const total=snapshot.tasks.length,done=counts.done??0,cancelled=counts.cancelled??0,remaining=total-done-cancelled;
 return {total,done,cancelled,remaining,progress:total-cancelled?done/(total-cancelled):null,counts,blocked:snapshot.tasks.filter(t=>isBlocked(t,snapshot.tasks,snapshot.links,snapshot.workflows)).length};
}
export type TaskSummary=ReturnType<typeof summarizeTasks>;
export function aggregateSnapshots(rows:{summary?:TaskSummary;error?:string}[]){
 const available=rows.flatMap(r=>r.summary?[r.summary]:[]),total=available.reduce((n,r)=>n+r.total,0),done=available.reduce((n,r)=>n+r.done,0),cancelled=available.reduce((n,r)=>n+r.cancelled,0);
 return {loaded:available.length,expected:rows.length,partial:available.length<rows.length,total,done,cancelled,remaining:total-done-cancelled,progress:total-cancelled?done/(total-cancelled):null};
}

/** Declared open task assignments, not observed CPU utilization or proof of a running agent. */
export function assignedWork(snapshot:ManagerSnapshot<StoredEntity>):Record<string,string[]> {
 const result=new Map<string,string[]>();
 for(const task of snapshot.tasks){if(['done','cancelled'].includes(semanticStatus(task,snapshot.workflows)))continue;
  const declared=Array.isArray(task.data?.agentAssignments)?task.data.agentAssignments.filter((a):a is string=>typeof a==='string'&&Boolean(a)):[];
  const active=Array.isArray(task.data?.assignments)?task.data.assignments.filter(a=>a&&typeof a==='object'&&!a.endedAt&&typeof a.agentId==='string').map(a=>a.agentId as string):[];
  for(const id of new Set([...declared,...active])){const ids=result.get(id)??[];ids.push(task.id);result.set(id,ids);}
 }
 return Object.fromEntries(result);
}
