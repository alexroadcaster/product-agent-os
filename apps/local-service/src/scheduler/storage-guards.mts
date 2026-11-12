import type {StoreWrite,StoredEntity} from '../../../../packages/contracts/storage/local-store.ts';
import {recipeHash as hash,recipeScopeHash,type Execution} from '../execution-recipes/contract.mts';
import {queueRegistryId,liveQueue,type QueueEntry,type QueueRegistry} from './contract.mts';
import {workspaceOverlap,workspaceCount} from './ownership.mts';
function fail(code:string):never{throw Object.assign(new Error('Queue transaction rejected'),{code});}
export type WorkspaceLock={id:string;canonical_root:string;kind:string;owner_execution:string|null};
/** Executed inside BEGIN IMMEDIATE: a process-local preview is never the admission authority. */
export function validateSchedulerWrite(command:StoreWrite,settings:StoredEntity[],getTask:(id:string)=>StoredEntity|null,currentRoot:string,locks:WorkspaceLock[]){
 const registry=settings.find(r=>r.id===queueRegistryId),queue=registry?.data as unknown as QueueRegistry|undefined,stamp=command.schedulerCommand;
 const entries=settings.filter(r=>r.data.category==='scheduler_entry'),selected=entries.find(r=>r.id===stamp?.entryId);
 if(stamp&&((registry?.revision??0)!==stamp.queueRevision||(stamp.entryId&&(selected?.revision??0)!==stamp.entryRevision)))fail('QUEUE_REVISION_CONFLICT');
 for(const change of command.changes){const before=settings.find(r=>r.id===change.entity.id),after=change.entity.data as any;
  if(change.entity.id===queueRegistryId||String(before?.data.category??after?.category??'').startsWith('scheduler_')){
   if(!stamp||change.entity.kind!=='settings'||change.delete)fail('QUEUE_WRITE_AUTHORITY_REQUIRED');
   if(after?.category==='scheduler_entry'){
    const e=after as QueueEntry,p=e.plan;if(stamp.entryId!==e.id)fail('QUEUE_WRITE_AUTHORITY_REQUIRED');
    if(before&&['id','projectId','plan','claims','createdAt'].some(k=>hash(before.data[k])!==hash((e as any)[k])))fail('QUEUE_PIN_IMMUTABLE');
    if(!before){const task=getTask(p.taskId);if(!task||task.revision!==p.taskRevision||recipeScopeHash(task.data)!==p.scopeHash)fail('QUEUE_TASK_CHANGED');if(entries.some(r=>liveQueue(r.data as unknown as QueueEntry)&&(r.data as unknown as QueueEntry).plan.taskId===p.taskId))fail('QUEUE_TASK_RESERVED');}
    if(stamp.admit){if(!before||before.data.state!=='queued'||queue?.paused||!queue?.order.includes(e.id))fail('QUEUE_ADMISSION_INVALID');const execution=command.changes.find(c=>c.entity.id===e.executionId)?.entity.data as unknown as Execution;
     if(!execution||execution.queueEntryId!==e.id||['taskId','taskContext','scopeHash','workflowSnapshot','transition','recipe','pins','inputArtifacts','budgetId','policyHash','bindingId','sessionId'].some(k=>hash((execution as any)[k])!==hash((p as any)[k])))fail('QUEUE_PIN_IMMUTABLE');}
   }
  }
  if(change.entity.kind==='run'||after?.category==='recipe_execution'){
   const run=after?.appAgentRun??after?.runtimeRun,execution=after?.category==='recipe_execution'?after as Execution:undefined;
   const taskId=execution?.taskId??run?.taskContext?.taskId??run?.taskId,executionId=execution?.id??run?.recipeExecution;
   const pending=entries.find(r=>liveQueue(r.data as unknown as QueueEntry)&&(r.data as unknown as QueueEntry).plan.taskId===taskId);
   if(pending){const e=pending.data as unknown as QueueEntry;if(!(stamp?.admit&&stamp.entryId===e.id)&&!(e.executionId&&e.executionId===executionId))fail('QUEUE_TASK_RESERVED');}
   // Only admission of a new execution/job acquires a root; bookkeeping for an existing job cannot steal one.
   const previous=getTask(change.entity.id);if(!previous){
    if(locks.some(lock=>lock.id!==executionId&&lock.owner_execution!==executionId&&workspaceOverlap(lock.canonical_root,currentRoot)))fail('WORKSPACE_OWNERSHIP_CONFLICT');
    const ownsExistingSlot=executionId&&locks.some(lock=>lock.id===executionId||lock.owner_execution===executionId);
    if(!ownsExistingSlot&&workspaceCount(locks.map(lock=>lock.canonical_root))>=4)fail('WORKSPACE_CAPACITY_EXHAUSTED');
   }
  }
 }
}
