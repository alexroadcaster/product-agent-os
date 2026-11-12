import {randomUUID} from 'node:crypto';
import type {LocalStore,StoredEntity,StoreWrite} from '../storage/local-store.mts';
import type {createRecipeService} from '../execution-recipes/service.mts';
import {recipeHash as hash,recipeScopeHash,publicSteps,ownsTask,type Execution} from '../execution-recipes/contract.mts';
import {autonomyService} from '../autonomy-policy/service.mts';
import {taskManagerSnapshot} from '../task-manager/service.mts';
import {workflowCategory} from '../workflows/registry.mts';
import {queueRegistryId,liveQueue,type QueueEntry,type QueueRegistry,type FrozenRecipePlan} from './contract.mts';
import {recipeClaims,verifyQueueOwnership,workspaceOverlap,workspaceCount} from './ownership.mts';
import type {QueueSnapshot,QueueEntryView,QueuePreview} from '../../../../packages/contracts/scheduler/queue.ts';
const fail=(code:string):never=>{throw Object.assign(new Error('Queue operation unavailable'),{code});};
const capabilities={maxWritersPerWorkspace:1,maxConcurrentWorkspaces:4,parallelism:'disjoint_canonical_workspaces',hostToolsConstrained:false} as const;
const terminalRecipe=(state:string)=>['completed','failed','cancelled','needs_user_decision','transition_blocked'].includes(state);
/** Single profile coordinator. Pending intents are not WIP; only atomic recipe admission consumes a slot. */
export function createScheduler(options:{store:LocalStore;recipes:ReturnType<typeof createRecipeService>;automatic?:boolean;now?:()=>number}){
 const {store,recipes}=options,now=options.now??Date.now,autonomy=autonomyService(store);let closed=false,tail:Promise<unknown>=Promise.resolve();
 const serial=<T,>(fn:()=>Promise<T>)=>{const result=tail.then(async()=>{if(closed)fail('QUEUE_CLOSED');await ready;return fn();});tail=result.catch(()=>{});return result;};
 const entries=async(projectId:string)=>(await store.projectEntities(projectId)).filter(r=>r.kind==='settings'&&r.data.category==='scheduler_entry');
 const registry=async(projectId:string)=>{const row=await store.get(projectId,queueRegistryId);return {revision:row?.revision??0,value:row?.data as unknown as QueueRegistry??{category:'scheduler_queue',paused:false,order:[]}};};
 async function write(projectId:string,revision:number,value:QueueRegistry,changes:StoreWrite['changes'],key:string,entry?:StoredEntity){const p=(await store.project(projectId))!;return store.write({projectId,actorId:'queue-coordinator',expectedAuthorityEpoch:p.authorityEpoch,idempotencyKey:key,schedulerCommand:{queueRevision:revision,...(entry?{entryId:entry.id,entryRevision:entry.revision}:{})},changes:[{expectedRevision:revision,entity:{id:queueRegistryId,kind:'settings',data:value as any}},...changes]});}
 async function saveEntry(row:StoredEntity,entry:QueueEntry){const q=await registry(row.projectId);await write(row.projectId,q.revision,q.value,[{expectedRevision:row.revision,entity:{id:row.id,kind:'settings',data:{...entry,updatedAt:now()} as any}}],`queue-state:${row.id}:${row.revision}:${hash(entry)}`,row);}
 const ready=(async()=>{await recipes.initialized();for(const project of await store.projects())for(const row of await entries(project.id)){const e=row.data as unknown as QueueEntry;if(['running','recovery_required'].includes(e.state)){const execution=e.executionId?await store.get(project.id,e.executionId):null,state=(execution?.data as unknown as Execution)?.state;e.state=state&&terminalRecipe(state)?state==='failed'?'failed':state==='cancelled'?'cancelled':'completed':'recovery_required';e.reason=state&&terminalRecipe(state)?undefined:'SERVICE_RESTART_NO_REPLAY';await saveEntry(row,e);}}})();
 function fields(input:Record<string,any>,keys:string[]){if(!input||typeof input!=='object'||Array.isArray(input)||Object.keys(input).some(k=>!keys.includes(k)))fail('QUEUE_INPUT_INVALID');}
 async function locks(){const result:{root:string;executionId?:string}[]=[];for(const project of await store.projects())for(const row of await store.projectEntities(project.id)){
  if(row.kind==='settings'&&row.data.category==='recipe_execution'&&ownsTask(row.data as unknown as Execution))result.push({root:project.canonicalRoot,executionId:row.id});
  if(row.kind==='run'&&!['completed','failed','interrupted'].includes(row.status))result.push({root:project.canonicalRoot,executionId:(row.data.appAgentRun as any)?.recipeExecution});
 }return result;}
 async function reasons(projectId:string,entry:QueueEntry,q:QueueRegistry):Promise<string[]>{
  if(entry.state!=='queued')return entry.reason?[entry.reason]:entry.state==='paused'?['QUEUE_ENTRY_PAUSED']:[];
  const result:string[]=[];if(q.paused)result.push('QUEUE_PAUSED');const p=entry.plan,project=(await store.project(projectId))!,snapshot=await taskManagerSnapshot(store,projectId),task=snapshot.tasks.find(t=>t.id===p.taskId);
  if(project.authorityEpoch!==p.authorityEpoch||project.rootIdentity!==p.rootIdentity)result.push('QUEUE_AUTHORITY_CHANGED');
  if(!task||task.revision!==p.taskRevision||recipeScopeHash(task.data)!==p.scopeHash)result.push('QUEUE_TASK_CHANGED');
  if(task?.data.blocker)result.push('BLOCKER_RESOLUTION_REQUIRED');
  for(const link of snapshot.links.filter(l=>l.relation==='blocks'&&l.targetId===p.taskId)){
   if(link.state==='pending')result.push('PENDING_LINK_RECONCILIATION_REQUIRED');else if(!link.waiver){const source=snapshot.tasks.find(t=>t.id===link.sourceId);if(!source||workflowCategory(snapshot.workflows,source.data as any)!=='done')result.push('DEPENDENCY_BLOCKED');}
  }
  const column=snapshot.board.columns.find(c=>c.statuses.includes(p.transition.to));if(column?.wipLimit!==undefined&&task&&!column.statuses.includes(task.status)&&snapshot.tasks.filter(t=>column.statuses.includes(t.status)).length>=column.wipLimit)result.push(column.wipMode==='hard'?'HARD_WIP_LIMIT':'SOFT_WIP_CONFIRMATION_REQUIRED');
  const policy=await autonomy.snapshot(projectId);if(policy.budgetId!==p.budgetId||hash(policy.policy)!==p.policyHash)result.push('QUEUE_POLICY_CHANGED');else{if(policy.paused)result.push('AUTONOMY_PAUSED');if(policy.usedRuns>=policy.policy!.maxRuns)result.push('AUTONOMY_BUDGET_EXHAUSTED');}
  const activeLocks=await locks();if(activeLocks.some(lock=>lock.executionId!==entry.executionId&&workspaceOverlap(lock.root,p.workspaceRoot)))result.push('WORKSPACE_OWNERSHIP_BUSY');
  else if(workspaceCount(activeLocks.map(lock=>lock.root))>=4)result.push('WORKSPACE_CAPACITY_EXHAUSTED');
  if(!result.length)try{await verifyQueueOwnership(p,entry.claims);await recipes.queueAvailability(p);}catch(error){result.push((error as any).code??'RECIPE_RUNTIME_UNAVAILABLE');}
  return [...new Set(result)];
 }
 async function view(projectId:string,row:StoredEntity,q:QueueRegistry):Promise<QueueEntryView>{const e=row.data as unknown as QueueEntry,execution=e.executionId?await store.get(projectId,e.executionId):null;return {id:e.id,taskId:e.plan.taskId,taskKey:e.plan.taskContext.key??e.plan.taskId,taskTitle:e.plan.taskContext.title??'',revision:row.revision,state:e.state,position:q.order.includes(e.id)?q.order.indexOf(e.id)+1:null,workflow:e.plan.workflowSnapshot.ref,recipeId:e.plan.recipe.id,sessionId:e.plan.sessionId,steps:publicSteps(e.plan.recipe,e.plan.pins),claims:e.claims,ownershipScope:'entire_workspace',executionId:e.executionId,executionState:(execution?.data as unknown as Execution)?.state??null,waitReasons:await reasons(projectId,e,q),createdAt:e.createdAt,updatedAt:e.updatedAt};}
 async function snapshot(projectId:string):Promise<QueueSnapshot>{if(!await store.project(projectId))fail('PROJECT_NOT_FOUND');const q=await registry(projectId),rows=await entries(projectId);rows.sort((a,b)=>{const ai=q.value.order.indexOf(a.id),bi=q.value.order.indexOf(b.id);return ai<0&&bi<0?(b.data.createdAt as number)-(a.data.createdAt as number):ai<0?1:bi<0?-1:ai-bi;});const items=[];for(const row of rows)items.push(await view(projectId,row,q.value));return {revision:q.revision,paused:q.value.paused,order:q.value.order,items,capabilities};}
 const intentKeys=['taskId','transitionId','mode','sessionId','roleBindings','expectedTaskRevision','reason'];
 async function preview(projectId:string,input:Record<string,any>){fields(input,intentKeys);const plan=await recipes.freezeQueue(projectId,input),q=await registry(projectId),claims=recipeClaims(plan);const entry:QueueEntry={category:'scheduler_entry',id:'preview',projectId,plan,claims,state:'queued',executionId:null,createdAt:0,updatedAt:0};const policy=await autonomy.snapshot(projectId);const result:QueuePreview={mode:'recipe',previewDigest:hash({plan,queueRevision:q.revision}),queueRevision:q.revision,target:plan.transition.to,recipeId:plan.recipe.id,workflow:plan.workflowSnapshot.ref,steps:publicSteps(plan.recipe,plan.pins),maxAttempts:plan.recipe.steps.reduce((n,s)=>n+s.iterationBudget*(s.retryBudget+1),0),claims,waitReasons:await reasons(projectId,entry,q.value),policy:{remainingRuns:policy.policy!.maxRuns-policy.usedRuns,concurrency:1},ownershipScope:'entire_workspace'};return {plan,result};}
 async function checkedCommand(projectId:string,action:string,input:Record<string,any>,fn:(q:Awaited<ReturnType<typeof registry>>)=>Promise<{changes:StoreWrite['changes'];registry:QueueRegistry;result:unknown;entry?:StoredEntity}>){
  if(typeof input.idempotencyKey!=='string'||!input.idempotencyKey||input.idempotencyKey.length>200)fail('QUEUE_INPUT_INVALID');
  const receiptId=`queue-receipt-${hash(input.idempotencyKey)}`,digest=hash({action,input}),old=await store.get(projectId,receiptId);if(old){if(old.data.digest!==digest)fail('IDEMPOTENCY_CONFLICT');return old.data.result;}
  const project=(await store.project(projectId))!;if(!project||project.authorityEpoch!==input.expectedAuthorityEpoch)fail('AUTHORITY_EPOCH_CONFLICT');const q=await registry(projectId);if(q.revision!==input.expectedRevision)fail('QUEUE_REVISION_CONFLICT');
  const prepared=await fn(q);await write(projectId,q.revision,prepared.registry,[...prepared.changes,{expectedRevision:0,entity:{id:receiptId,kind:'settings',data:{category:'scheduler_receipt',digest,result:prepared.result}}}],`queue-user:${input.idempotencyKey}`,prepared.entry);return prepared.result;
 }
 const permanent=new Set(['QUEUE_TASK_CHANGED','QUEUE_AUTHORITY_CHANGED','QUEUE_POLICY_CHANGED','QUEUE_ROOT_CHANGED','QUEUE_UNSAFE_OWNERSHIP','RECIPE_ARTIFACT_DRIFT']);
 async function tick(){return serial(async()=>{
  for(const project of await store.projects()){
   for(const row of await entries(project.id)){const e=row.data as unknown as QueueEntry;if(!['running','recovery_required'].includes(e.state)||!e.executionId)continue;const execution=await recipes.get(project.id,e.executionId);const next=terminalRecipe(execution.state)?execution.state==='failed'?'failed':execution.state==='cancelled'?'cancelled':'completed':execution.state==='recovery_required'?'recovery_required':e.state;if(next!==e.state)await saveEntry(row,{...e,state:next,reason:execution.reason??undefined});}
   const q=await registry(project.id);if(q.value.paused)continue;
   for(const id of q.value.order){const row=await store.get(project.id,id);if(!row||row.data.state!=='queued')continue;const entry=row.data as unknown as QueueEntry,wait=await reasons(project.id,entry,q.value);
    if(wait.length){const reason=wait.find(r=>permanent.has(r));if(reason)await saveEntry(row,{...entry,state:'needs_review',reason});continue;}
    try{const current=await registry(project.id);await recipes.admitQueue(project.id,id,row.revision,current.revision);}catch(error){const code=(error as any).code??'QUEUE_ADMISSION_UNCONFIRMED';const latest=await store.get(project.id,id);if(latest?.revision===row.revision&&latest.data.state==='queued'&&permanent.has(code))await saveEntry(latest,{...entry,state:'needs_review',reason:code});}
   }
  }
 });}
 const timer=options.automatic!==false?setInterval(()=>void tick().catch(()=>{}),500):undefined;timer?.unref();
 return {initialized:async()=>{await ready;},snapshot:(projectId:string)=>serial(()=>snapshot(projectId)),preview:(projectId:string,input:Record<string,any>)=>serial(async()=>(await preview(projectId,input)).result),
  enqueue:(projectId:string,input:Record<string,any>)=>serial(async()=>{fields(input,[...intentKeys,'previewDigest','expectedRevision','expectedAuthorityEpoch','idempotencyKey']);return checkedCommand(projectId,'enqueue',input,async q=>{
   const intent=Object.fromEntries(intentKeys.map(k=>[k,input[k]])),prepared=await preview(projectId,intent);if(prepared.result.previewDigest!==input.previewDigest)fail('QUEUE_PREVIEW_STALE');
   const rows=await entries(projectId);if(rows.length>=200||rows.filter(r=>liveQueue(r.data as unknown as QueueEntry)).length>=32||rows.reduce((n,r)=>n+Buffer.byteLength(JSON.stringify(r.data)),0)+Buffer.byteLength(JSON.stringify(prepared.plan))>16*1024*1024)fail('QUEUE_CAPACITY_EXCEEDED');
   if(rows.some(r=>liveQueue(r.data as unknown as QueueEntry)&&(r.data as unknown as QueueEntry).plan.taskId===prepared.plan.taskId))fail('QUEUE_TASK_RESERVED');
   const id=`queue-${randomUUID()}`,entry:QueueEntry={category:'scheduler_entry',id,projectId,plan:prepared.plan,claims:prepared.result.claims,state:'queued',executionId:null,createdAt:now(),updatedAt:now()},value={...q.value,order:[...q.value.order,id]};
   return {changes:[{expectedRevision:0,entity:{id,kind:'settings',data:entry as any}}],registry:value,result:{entryId:id,revision:q.revision+1},entry:{id,revision:0} as StoredEntity};
  });}),
  command:(projectId:string,action:string,input:Record<string,any>)=>serial(async()=>{fields(input,['entryId','order','expectedRevision','expectedAuthorityEpoch','idempotencyKey']);return checkedCommand(projectId,action,input,async q=>{
   if(action==='pause'||action==='resume')return {changes:[],registry:{...q.value,paused:action==='pause'},result:{revision:q.revision+1}};
   if(action==='reorder'){if(!Array.isArray(input.order)||input.order.length!==q.value.order.length||new Set(input.order).size!==input.order.length||input.order.some((id:string)=>!q.value.order.includes(id)))fail('QUEUE_ORDER_INVALID');return {changes:[],registry:{...q.value,order:input.order},result:{revision:q.revision+1}};}
   const row=await store.get(projectId,input.entryId);if(!row||row.data.category!=='scheduler_entry')fail('QUEUE_ENTRY_NOT_FOUND');const e=row!.data as unknown as QueueEntry;
   if(action==='cancel'&&e.executionId){const execution=await recipes.get(projectId,e.executionId);await recipes.command(projectId,e.executionId,execution.state==='recovery_required'?'reconcile':'cancel',{expectedRevision:execution.revision,expectedAuthorityEpoch:input.expectedAuthorityEpoch,idempotencyKey:`queue-cancel:${input.idempotencyKey}`});return {changes:[],registry:q.value,result:{revision:q.revision+1},entry:row!};}
   if(!['queued','paused','needs_review'].includes(e.state))fail('QUEUE_ACTION_UNAVAILABLE');if(!['cancel','pause-entry','resume-entry'].includes(action))fail('QUEUE_ACTION_INVALID');if(action==='resume-entry'&&e.state==='needs_review')fail('QUEUE_REPREVIEW_REQUIRED');
   const next={...e,state:action==='cancel'?'cancelled' as const:action==='pause-entry'?'paused' as const:'queued' as const,updatedAt:now()};return {changes:[{expectedRevision:row!.revision,entity:{id:e.id,kind:'settings',data:next as any}}],registry:{...q.value,order:action==='cancel'?q.value.order.filter(id=>id!==e.id):q.value.order},result:{revision:q.revision+1},entry:row!};
  });}),tick,async close(){if(timer)clearInterval(timer);await tail;await ready;closed=true;}};
}
