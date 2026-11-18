import type {ManagerSnapshot} from '../../../../../packages/contracts/issues/manager.ts';
import type {StoredEntity} from '../../api/client.ts';
import {semanticStatus,isBlocked} from '../tasks/read.ts';
/** Progress is Done / non-cancelled task objects, including parents; it is not effort completion. */
export function summarizeTasks(snapshot:ManagerSnapshot<StoredEntity>){
 const counts:Record<string,number>=Object.create(null);for(const task of snapshot.tasks){const state=semanticStatus(task,snapshot.workflows)||'unknown';counts[state]=(counts[state]??0)+1;}
 const total=snapshot.tasks.length,done=counts.done??0,cancelled=counts.cancelled??0,remaining=total-done-cancelled;
 return {total,done,cancelled,remaining,progress:total-cancelled?done/(total-cancelled):null,counts,blocked:snapshot.tasks.filter(t=>isBlocked(t,snapshot.tasks,snapshot.links,snapshot.workflows)).length};
}
export type TaskSummary=ReturnType<typeof summarizeTasks>;
export function aggregateSnapshots(rows:{summary?:TaskSummary;error?:string}[],expected=rows.length){
 const available=rows.flatMap(r=>r.summary?[r.summary]:[]),total=available.reduce((n,r)=>n+r.total,0),done=available.reduce((n,r)=>n+r.done,0),cancelled=available.reduce((n,r)=>n+r.cancelled,0);
 return {loaded:available.length,expected,partial:available.length<expected,total,done,cancelled,remaining:total-done-cancelled,progress:total-cancelled?done/(total-cancelled):null};
}

/** Recent means updatedAt descending; unknown dates follow known dates, with stable ID ordering for ties. */
export function recentTasks(tasks:readonly StoredEntity[]){
 const time=(task:StoredEntity)=>{const value=Date.parse(task.updatedAt??'');return Number.isFinite(value)?value:Number.NEGATIVE_INFINITY;};
 return [...tasks].sort((a,b)=>{const left=time(a),right=time(b);return left!==right?(left>right?-1:1):a.id<b.id?-1:a.id>b.id?1:0;}).slice(0,3);
}
