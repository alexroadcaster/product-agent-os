import {randomUUID} from 'node:crypto';
import type {LocalStore,StoredEntity} from '../storage/local-store.mts';
import type {AssetRoot} from '../team/sources.mts';
import {taskManagerSnapshot,taskManagerCommand} from '../task-manager/service.mts';
import {workflowSnapshot} from '../workflows/registry.mts';
import {autonomyService} from '../autonomy-policy/service.mts';
import {resolveRecipePins} from './pins.mts';
import {recipeFail as fail,recipeHash as hash,recipeScopeHash,qualifyGraph,publicExecution,publicSteps,ownsTask,type Execution,type Attempt} from './contract.mts';
import {captureTaskFiles} from '../runtime/app-agent-files.mts';
import type {FrozenRecipePlan,QueueEntry,QueueRegistry} from '../scheduler/contract.mts';
import {verifyQueueOwnership,recipeClaims} from '../scheduler/ownership.mts';
export type RecipePort={initialized?():Promise<void>;prepareBinding?(projectId:string,sessionId:string):Promise<{bindingId:string}>;eligible(projectId:string,sessionId:string):Promise<{bindingId:string}>;sendAttempt(input:{projectId:string;executionId:string}):Promise<{id:string}>;inspectAttempt?(input:{projectId:string;executionId:string}):Promise<{runId?:string;admissionRejected?:boolean}>;interrupt(input:{projectId:string;sessionId:string;bindingId:string;runId:string}):Promise<unknown>};
import type {RecipePreview} from '../../../../packages/contracts/execution-recipes/recipe.ts';
export type {RecipePreview} from '../../../../packages/contracts/execution-recipes/recipe.ts';
export function createRecipeService(options:{store:LocalStore;port?:RecipePort;assetRoots?:AssetRoot[];now?:()=>number;automatic?:boolean}){
 const {store,port}=options,now=options.now??Date.now,autonomy=autonomyService(store,now);let queue:Promise<unknown>=Promise.resolve(),closed=false;
 const serial=<T,>(fn:()=>Promise<T>)=>{const work=queue.then(async()=>{if(closed)fail('RECIPE_SERVICE_CLOSED');await ready;return fn();});queue=work.catch(()=>{});return work;};
 const rows=async(projectId:string)=>(await store.projectEntities(projectId)).filter(r=>r.kind==='settings'&&r.data.category==='recipe_execution');
 const read=async(projectId:string,id:string)=>{const row=await store.get(projectId,id);if(!row||row.data.category!=='recipe_execution')fail('RECIPE_NOT_FOUND');return row!;};
 async function save(row:StoredEntity,e:Execution,key=hash(e)){
  const project=(await store.project(row.projectId))!;e.updatedAt=now();await store.write({projectId:row.projectId,actorId:'recipe-scheduler',expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:`recipe:${e.id}:${row.revision}:${key}`,recipeExecution:{id:e.id,revision:row.revision},changes:[{expectedRevision:row.revision,entity:{id:e.id,kind:'settings',data:e as any}}]});
 }
 const ready=(async()=>{await port?.initialized?.();for(const project of await store.projects())for(const row of await rows(project.id)){const e=row.data as unknown as Execution;if(ownsTask(e)&&e.state!=='recovery_required'){e.state='recovery_required';e.reason='SERVICE_RESTART_NO_REPLAY';await save(row,e);}}})();
 function fields(input:Record<string,any>,allowed:string[]){if(Object.keys(input).some(k=>!allowed.includes(k)))fail('RECIPE_INPUT_INVALID');}
 const startFields=['taskId','transitionId','mode','sessionId','roleBindings','expectedTaskRevision','reason','previewDigest','expectedAuthorityEpoch','idempotencyKey'];
 async function prepare(projectId:string,input:Record<string,any>,deferred=false){
  fields(input,startFields);if(!['manual','recipe'].includes(input.mode)||typeof input.reason!=='string'||!input.reason.trim())fail('RECIPE_INPUT_INVALID');
  const snapshot=await taskManagerSnapshot(store,projectId),task=await store.get(projectId,input.taskId);if(!task||task.kind!=='task'||task.deleted)fail('TASK_NOT_FOUND');
  if(task!.revision!==input.expectedTaskRevision)fail('REVISION_CONFLICT');const data=task!.data as any;if(data.schemaVersion!=='m2_task_profile_v1')fail('M2_PROFILE_REQUIRED');
  if((await rows(projectId)).some(r=>ownsTask(r.data as unknown as Execution)&&(r.data as any).taskId===task!.id))fail('RECIPE_TASK_OWNED');
  const workflow=workflowSnapshot(snapshot.workflows,data.workflow),transition=workflow.definition.transitions.find(t=>t.id===input.transitionId&&t.from===data.status);
  if(!transition||!transition.actors.includes('user'))fail('TRANSITION_REQUIRED');
  const base={taskId:task!.id,taskRevision:task!.revision,scopeHash:recipeScopeHash(data),workflow,transition,mode:input.mode,reason:input.reason};
  if(input.mode==='manual')return {task:task!,transition,workflow,preview:{mode:'manual',agentRuns:0,previewDigest:hash(base),transitionId:transition.id,target:transition.to},pins:{},bindingId:'',policy:null,recipe:null};
  if(!port)fail('RECIPE_RUNTIME_UNAVAILABLE');if(typeof input.sessionId!=='string'||!input.sessionId)fail('RECIPE_SESSION_REQUIRED');
  if(workflow.definition.states.find(s=>s.id===transition.to)?.category!=='in_progress')fail('RECIPE_EXECUTION_PHASE_REQUIRED');
  const recipe=workflow.definition.recipes.find(r=>r.id===transition.recipeId);if(!recipe)fail('WORKFLOW_RECIPE_NOT_FOUND');qualifyGraph(recipe!);
  if(!input.roleBindings||typeof input.roleBindings!=='object'||Array.isArray(input.roleBindings))fail('RECIPE_ROLE_BINDING_REQUIRED');
  const policy=await autonomy.snapshot(projectId);if(!policy.policy||policy.paused&&!deferred)fail('AUTONOMY_PAUSED');if(!policy.policy.allowedTaskIds.includes(task!.id))fail('AUTONOMY_TASK_FORBIDDEN');
  if(!(await autonomy.preview(projectId,policy.policy,policy.revision)).executable)fail('AUTONOMY_SCOPE_UNAVAILABLE');if(policy.usedRuns>=policy.policy.maxRuns&&!deferred)fail('AUTONOMY_BUDGET_EXHAUSTED');
  const {bindingId}=await (deferred&&port!.prepareBinding?port!.prepareBinding(projectId,input.sessionId):port!.eligible(projectId,input.sessionId)),pins=await resolveRecipePins(store,projectId,recipe!.steps,input.roleBindings,options.assetRoots);
  const produced=new Set(recipe.steps.flatMap(s=>s.outputArtifacts)),initialPaths=[...new Set([...recipe.steps[0].inputArtifacts,...recipe.steps.flatMap(s=>s.inputArtifacts).filter(path=>!produced.has(path))])];
  const inputArtifacts=await artifacts({projectId} as Execution,initialPaths);
  const previewDigest=hash({...base,sessionId:input.sessionId,bindingId,pins,inputArtifacts,policyRevision:policy.revision,budgetId:policy.budgetId,policy:policy.policy});
  return {task:task!,transition,workflow,recipe:recipe!,pins,inputArtifacts,bindingId,policy,preview:{mode:'recipe',agentRuns:recipe!.steps.length,previewDigest,transitionId:transition.id,target:transition.to,recipeId:recipe!.id,workflow:workflow.ref,steps:publicSteps(recipe,pins),policy:{budgetId:policy.budgetId,remainingRuns:policy.policy.maxRuns-policy.usedRuns,maxRunSeconds:policy.policy.maxRunSeconds,concurrency:1},maxAttempts:recipe!.steps.reduce((n,s)=>n+s.iterationBudget*(s.retryBudget+1),0),concurrency:1}};
 }
 async function artifacts(e:Execution,paths:string[]){const project=(await store.project(e.projectId))!;const captured=await captureTaskFiles({workspaceRoot:project.canonicalRoot,directoryIdentity:project.rootIdentity},paths.map(relativePath=>({relativePath})));if(captured.some(p=>p.kind!=='present'))fail('RECIPE_ARTIFACT_UNAVAILABLE');return captured.map(p=>({path:p.path,sha256:p.sha256!}));}
 async function finish(row:StoredEntity,e:Execution,outcome:'success'|'failure'){
  e.outcome=outcome;const target=outcome==='success'?e.transition.successTarget:e.transition.failureTarget;
  if(!target){e.state=outcome==='success'?'completed':'failed';await save(row,e);return;}
  const task=(await store.get(e.projectId,e.taskId))!,edge=e.workflowSnapshot.definition.transitions.find(t=>t.from===task.status&&t.to===target&&t.actors.includes('agent'));
  const category=e.workflowSnapshot.definition.states.find(s=>s.id===target)?.category;
  if(!edge||edge.requiresDecision||category==='done'||category==='cancelled'){e.state='needs_user_decision';e.reason='RECIPE_OUTCOME_DECISION_REQUIRED';await save(row,e);return;}
  e.state=outcome==='success'?'completed':'failed';e.updatedAt=now();
  try{await taskManagerCommand(store,e.projectId,`agent:recipe:${e.id}`,{action:'transition',taskId:e.taskId,status:target,expectedRevision:task.revision,expectedAuthorityEpoch:(await store.project(e.projectId))!.authorityEpoch,idempotencyKey:`recipe-outcome:${e.id}:${outcome}`,reason:'Observed recipe outcome'},
   {recipeExecution:{id:e.id,revision:row.revision},additionalChanges:[{expectedRevision:row.revision,entity:{id:e.id,kind:'settings',data:e as any}}]});}
  catch(error){e.state='transition_blocked';e.reason=(error as any).code??'RECIPE_OUTCOME_TRANSITION_FAILED';await save(row,e);}
 }
 async function advance(row:StoredEntity){
  const e=structuredClone(row.data) as unknown as Execution;if(!ownsTask(e)||e.state==='recovery_required')return;
  const current=e.attempts.at(-1),jobRow=current?.runId?await store.get(e.projectId,current.runId):null,job=jobRow?.data.appAgentRun as any;
  if(e.state==='paused'||e.state==='cancel_requested'){
   if(job&&!['completed','failed','interrupted'].includes(job.state)){try{await port?.interrupt({projectId:e.projectId,sessionId:e.sessionId,bindingId:e.bindingId,runId:job.id});}catch{}return;}
   if(current&&current.state==='planned'&&!current.admissionRejected){e.state='recovery_required';e.reason='UNCONFIRMED_ADMISSION_NO_REPLAY';await save(row,e);return;}
   if(e.state==='cancel_requested'){e.state='cancelled';await save(row,e);}return;
  }
  const policy=await autonomy.snapshot(e.projectId);if(policy.budgetId!==e.budgetId||hash(policy.policy)!==e.policyHash||policy.paused){e.state='paused';e.reason='AUTONOMY_POLICY_CHANGED_OR_PAUSED';await save(row,e);return;}
  const task=await store.get(e.projectId,e.taskId);if(!task||recipeScopeHash(task.data)!==e.scopeHash||task.status!==e.transition.to){e.state='recovery_required';e.reason='RECIPE_TASK_SCOPE_CHANGED';await save(row,e);return;}
  if(current&&['planned','dispatched'].includes(current.state)){
   if(!job){e.state='recovery_required';e.reason='UNCONFIRMED_ADMISSION_NO_REPLAY';await save(row,e);return;}
   if(job.state==='recovery_required'||job.state==='interrupted'||job.autonomyStopReason){e.state='recovery_required';e.reason=job.autonomyStopReason??'CHILD_UNRESOLVED_NO_REPLAY';await save(row,e);return;}
   if(!['completed','failed'].includes(job.state)){
    if(now()>=current.deadlineAt){e.state='paused';e.reason='RECIPE_STEP_TIMEOUT';await save(row,e);try{await port?.interrupt({projectId:e.projectId,sessionId:e.sessionId,bindingId:e.bindingId,runId:job.id});}catch{}}return;
   }
   const step=e.recipe.steps.find(s=>s.id===current.stepId)!;let success=job.state==='completed';
   if(success)try{if(!step.checks.every(check=>(job.operations??[]).some((op:any)=>op.state==='completed'&&op.exitCode===0&&(JSON.stringify(op.argv)===check||op.argv.join(' ')===check))))fail('RECIPE_CHECK_EVIDENCE_REQUIRED');current.artifacts=await artifacts(e,step.outputArtifacts);}catch(error){success=false;e.reason=(error as any).code??'RECIPE_EVIDENCE_FAILED';}
   current.state=success?'completed':'failed';
   if(!success){
    if(job.state==='failed'&&current.try<step.retryBudget){e.queue.unshift(step.id);await save(row,e);return;}
    await finish(row,e,'failure');return;
   }
   const graph=qualifyGraph(e.recipe);for(const target of graph.edges.get(step.id)!){const child=e.recipe.steps.find(s=>s.id===target)!,arrivals=e.arrivals[target]??={};arrivals[step.id]=(arrivals[step.id]??0)+1;
    const forwardParents=graph.forwardParents.get(target)!;const required=!forwardParents.includes(step.id)?[step.id]:child.join?.length?child.join:forwardParents;if(required.every(parent=>(arrivals[parent]??0)>0)){for(const parent of required)arrivals[parent]--;if((e.iterations[target]??0)<child.iterationBudget)e.queue.push(target);}
   }
   await save(row,e);return;
  }
  if(!e.queue.length){if(Object.values(e.arrivals).some(arrivals=>Object.values(arrivals).some(count=>count>0))){e.reason='RECIPE_JOIN_UNSATISFIED';await finish(row,e,'failure');}else await finish(row,e,'success');return;}
  const stepId=e.queue.shift()!,step=e.recipe.steps.find(s=>s.id===stepId)!,prior=e.attempts.at(-1),retry=prior?.stepId===stepId&&prior.state==='failed';
  const iteration=retry?prior.iteration:(e.iterations[stepId]??0)+1;if(iteration>step.iterationBudget){await save(row,e);return;}
  if(e.attempts.length>=1000){e.reason='RECIPE_ATTEMPT_LIMIT';await finish(row,e,'failure');return;}
  try{const current=await artifacts(e,step.inputArtifacts),expected=new Map([...e.inputArtifacts,...e.attempts.filter(a=>a.state==='completed').flatMap(a=>a.artifacts??[])].map(a=>[a.path,a.sha256]));if(current.some(a=>!expected.has(a.path)||expected.get(a.path)!==a.sha256))fail('RECIPE_ARTIFACT_DRIFT');await port!.eligible(e.projectId,e.sessionId);}catch(error){e.state='paused';e.reason=(error as any).code??'RECIPE_RUNTIME_UNAVAILABLE';e.queue.unshift(stepId);await save(row,e);return;}
  const attempt:Attempt={stepId,iteration,try:retry?prior.try+1:0,clientMessageId:`recipe-${hash([e.id,stepId,iteration,retry?prior.try+1:0])}`,state:'planned',startedAt:now(),deadlineAt:now()+Math.min(step.timeoutSeconds,policy.policy!.maxRunSeconds)*1000};
  e.iterations[stepId]=iteration;e.attempts.push(attempt);await save(row,e);
  // The durable planned identity is never re-dispatched after uncertain failure or restart.
  try{const run=await port!.sendAttempt({projectId:e.projectId,executionId:e.id});const saved=await read(e.projectId,e.id),next=saved.data as unknown as Execution;next.attempts.at(-1)!.runId=run.id;next.attempts.at(-1)!.state='dispatched';await save(saved,next);}
  catch(error){const saved=await read(e.projectId,e.id),next=saved.data as unknown as Execution,last=next.attempts.at(-1)!;next.state='recovery_required';next.reason=(error as any).code??'RECIPE_DISPATCH_UNCERTAIN';
   if((error as any).recipeAdmissionRejected===true)last.admissionRejected=true;
   if(typeof (error as any).recipeObservedRunId==='string'){last.runId=(error as any).recipeObservedRunId;last.state='dispatched';}
   await save(saved,next);}
 }
 async function tick(){return serial(async()=>{if(!port)return;for(const project of await store.projects())for(const row of await rows(project.id))try{await advance(row);}catch(error){
  const saved=await read(project.id,row.id),e=saved.data as unknown as Execution;if(!ownsTask(e))continue;e.state='recovery_required';e.reason=(error as any).code??'RECIPE_SCHEDULER_FAILED';await save(saved,e);const run=e.attempts.at(-1)?.runId;if(run)try{await port.interrupt({projectId:project.id,sessionId:e.sessionId,bindingId:e.bindingId,runId:run});}catch{}
 }});}
 const timer=port&&options.automatic!==false?setInterval(()=>void tick().catch(()=>{}),250):undefined;timer?.unref();
 return {
  initialized:async()=>{await ready;},
  queueAvailability:(plan:FrozenRecipePlan)=>serial(async()=>{if(!port||((await port.eligible(plan.taskContext.projectId??'',plan.sessionId)).bindingId!==plan.bindingId))fail('RECIPE_RUNTIME_UNAVAILABLE');}),
  freezeQueue:(projectId:string,input:Record<string,any>):Promise<FrozenRecipePlan>=>serial(async()=>{
   if(input.mode!=='recipe')fail('QUEUE_RECIPE_REQUIRED');const p=await prepare(projectId,input,true),project=(await store.project(projectId))!;
   const plan:FrozenRecipePlan={taskId:p.task.id,taskRevision:p.task.revision,taskContext:structuredClone(p.task.data),scopeHash:recipeScopeHash(p.task.data),workflowSnapshot:p.workflow,transition:p.transition,recipe:p.recipe!,pins:p.pins,inputArtifacts:p.inputArtifacts??[],budgetId:p.policy!.budgetId,policyHash:hash(p.policy!.policy),bindingId:p.bindingId,sessionId:input.sessionId,authorityEpoch:project.authorityEpoch,workspaceRoot:project.canonicalRoot,rootIdentity:project.rootIdentity,reason:input.reason};
   await verifyQueueOwnership(plan,recipeClaims(plan));return plan;
  }),
  // Consume only the durable scheduler record. The browser can never supply a frozen plan or skip admission guards.
  admitQueue:(projectId:string,entryId:string,entryRevision:number,queueRevision:number)=>serial(async()=>{
   const row=await store.get(projectId,entryId);if(!row||row.data.category!=='scheduler_entry')fail('QUEUE_ENTRY_NOT_FOUND');const entry=row!.data as unknown as QueueEntry,p=entry.plan;
   if(entry.executionId){const existing=await store.get(projectId,entry.executionId);if(existing?.data.appAgentRun)fail('QUEUE_EXECUTION_INVALID');if(existing)return publicExecution(existing.data as unknown as Execution,existing.revision);}
   if(row!.revision!==entryRevision||entry.state!=='queued')fail('QUEUE_REVISION_CONFLICT');
   const queueRow=await store.get(projectId,'scheduler-queue'),registry=queueRow?.data as unknown as QueueRegistry;
   if(queueRow?.revision!==queueRevision||registry.paused||!registry.order.includes(entryId))fail('QUEUE_REVISION_CONFLICT');
   const project=(await store.project(projectId))!,task=await store.get(projectId,p.taskId),policy=await autonomy.snapshot(projectId);
   if(project.authorityEpoch!==p.authorityEpoch||project.rootIdentity!==p.rootIdentity||project.canonicalRoot!==p.workspaceRoot)fail('QUEUE_AUTHORITY_CHANGED');
   if(!task||task.revision!==p.taskRevision||recipeScopeHash(task.data)!==p.scopeHash)fail('QUEUE_TASK_CHANGED');
   if(policy.budgetId!==p.budgetId||hash(policy.policy)!==p.policyHash)fail('QUEUE_POLICY_CHANGED');if(policy.paused)fail('AUTONOMY_PAUSED');if(policy.usedRuns>=policy.policy!.maxRuns)fail('AUTONOMY_BUDGET_EXHAUSTED');
   await verifyQueueOwnership(p,entry.claims);const observed=await artifacts({projectId} as Execution,p.inputArtifacts.map(a=>a.path));if(hash(observed)!==hash(p.inputArtifacts))fail('RECIPE_ARTIFACT_DRIFT');
   if(!port||((await port.eligible(projectId,p.sessionId)).bindingId!==p.bindingId))fail('RECIPE_RUNTIME_UNAVAILABLE');
   const id=`recipe-queue-${hash([projectId,entryId])}`,e:Execution={category:'recipe_execution',id,projectId,taskId:p.taskId,sessionId:p.sessionId,bindingId:p.bindingId,queueEntryId:entryId,mode:'recipe',state:'running',scopeHash:p.scopeHash,taskContext:p.taskContext,workflowSnapshot:p.workflowSnapshot,transition:p.transition,recipe:p.recipe,pins:p.pins,inputArtifacts:p.inputArtifacts,budgetId:p.budgetId,policyRevision:policy.revision,policyHash:p.policyHash,queue:[p.recipe.steps[0].id],arrivals:{},iterations:{},attempts:[],createdAt:now(),updatedAt:now(),startDigest:hash(p)};
   const next={...entry,state:'running' as const,executionId:id,updatedAt:now()};
   await taskManagerCommand(store,projectId,'local-user',{action:'transition',taskId:p.taskId,status:p.transition.to,expectedRevision:p.taskRevision,expectedAuthorityEpoch:p.authorityEpoch,idempotencyKey:`queue-admit:${entryId}`,reason:p.reason},{recipeExecution:{id,revision:0},schedulerCommand:{queueRevision,entryId,entryRevision,admit:true},additionalChanges:[{expectedRevision:0,entity:{id,kind:'settings',data:e as any}},{expectedRevision:entryRevision,entity:{id:entryId,kind:'settings',data:next as any}},{expectedRevision:queueRevision,entity:{id:'scheduler-queue',kind:'settings',data:{...registry,order:registry.order.filter(id=>id!==entryId)} as any}}]});
   return publicExecution(e,1);
  }),
  preview:(projectId:string,input:Record<string,any>):Promise<RecipePreview>=>serial(async()=>(await prepare(projectId,input)).preview as RecipePreview),
  list:(projectId:string)=>serial(async()=>({items:(await rows(projectId)).map(r=>publicExecution(r.data as unknown as Execution,r.revision))})),
  get:(projectId:string,id:string)=>serial(async()=>{const r=await read(projectId,id);return publicExecution(r.data as unknown as Execution,r.revision);}),
  start:(projectId:string,actorId:string,input:Record<string,any>)=>serial(async()=>{
   fields(input,startFields);if(typeof input.idempotencyKey!=='string'||!input.idempotencyKey||input.idempotencyKey.length>200)fail('RECIPE_INPUT_INVALID');
   const receiptId=`recipe-start-${hash(input.idempotencyKey)}`,digest=hash(input),prior=await store.get(projectId,receiptId);if(prior){if(prior.data.digest!==digest)fail('IDEMPOTENCY_CONFLICT');return prior.data.result;}
   const project=(await store.project(projectId))!;if(project.authorityEpoch!==input.expectedAuthorityEpoch)fail('AUTHORITY_EPOCH_CONFLICT');const prepared=await prepare(projectId,input);if(input.previewDigest!==prepared.preview.previewDigest)fail('RECIPE_PREVIEW_STALE');
   const id=`recipe-${randomUUID()}`,e:Execution|undefined=input.mode==='recipe'?{category:'recipe_execution',id,projectId,taskId:prepared.task.id,sessionId:input.sessionId,bindingId:prepared.bindingId,mode:'recipe',state:'running',scopeHash:recipeScopeHash(prepared.task.data),taskContext:structuredClone(prepared.task.data),workflowSnapshot:prepared.workflow,transition:prepared.transition,recipe:prepared.recipe!,pins:prepared.pins,inputArtifacts:prepared.inputArtifacts??[],budgetId:prepared.policy!.budgetId,policyRevision:prepared.policy!.revision,policyHash:hash(prepared.policy!.policy),queue:[prepared.recipe!.steps[0].id],arrivals:{},iterations:{},attempts:[],createdAt:now(),updatedAt:now(),startDigest:digest}:undefined;
   const result=e?publicExecution(e,1):{mode:'manual',agentRuns:0,taskId:prepared.task.id,target:prepared.transition.to};
   await taskManagerCommand(store,projectId,actorId,{action:'transition',taskId:prepared.task.id,status:prepared.transition.to,expectedRevision:prepared.task.revision,expectedAuthorityEpoch:input.expectedAuthorityEpoch,idempotencyKey:`recipe-start-command:${input.idempotencyKey}`,reason:input.reason},
    {recipeExecution:e?{id,revision:0}:undefined,additionalChanges:[...(e?[{expectedRevision:0,entity:{id,kind:'settings' as const,data:e as any}}]:[]),{expectedRevision:0,entity:{id:receiptId,kind:'settings',data:{category:'recipe_start_receipt',digest,result}}}]});return result;
  }),
  command:(projectId:string,id:string,action:string,input:Record<string,any>)=>serial(async()=>{
   fields(input,['expectedRevision','expectedAuthorityEpoch','idempotencyKey','reason']);if(typeof input.idempotencyKey!=='string'||!input.idempotencyKey||input.idempotencyKey.length>200)fail('RECIPE_INPUT_INVALID');
   const receiptId=`recipe-command-${hash(input.idempotencyKey)}`,digest=hash({id,action,input}),old=await store.get(projectId,receiptId);if(old){if(old.data.digest!==digest)fail('IDEMPOTENCY_CONFLICT');return old.data.result;}
   const row=await read(projectId,id),e=row.data as unknown as Execution,project=(await store.project(projectId))!;if(row.revision!==input.expectedRevision)fail('REVISION_CONFLICT');if(project.authorityEpoch!==input.expectedAuthorityEpoch)fail('AUTHORITY_EPOCH_CONFLICT');
   if(!ownsTask(e))fail('RECIPE_TERMINAL');const last=e.attempts.at(-1);let child=last?.runId?await store.get(projectId,last.runId):null;
   if(action==='pause'){if(e.state==='recovery_required')fail('RECIPE_RECOVERY_REQUIRED');e.state='paused';}
   else if(action==='cancel'){e.state='cancel_requested';}
   else if(action==='resume'){
    if(e.state!=='paused'||last&&['planned','dispatched'].includes(last.state))fail('RECIPE_RECOVERY_REQUIRED');const policy=await autonomy.snapshot(projectId);if(policy.paused||policy.budgetId!==e.budgetId||hash(policy.policy)!==e.policyHash)fail('AUTONOMY_RESERVATION_CONFLICT');
    if(recipeScopeHash((await store.get(projectId,e.taskId))!.data)!==e.scopeHash)fail('RECIPE_TASK_SCOPE_CHANGED');await port?.eligible(projectId,e.sessionId);e.state='running';
   }else if(action==='reconcile'){
    if(e.state!=='recovery_required'&&e.state!=='cancel_requested')fail('RECIPE_RECOVERY_REQUIRED');
    if(last&&!last.runId&&port?.inspectAttempt){const proof=await port.inspectAttempt({projectId,executionId:id});if(proof.runId){last.runId=proof.runId;last.state='dispatched';child=await store.get(projectId,proof.runId);}else if(proof.admissionRejected===true)last.admissionRejected=true;}
    if(last&&(!child?!(last.admissionRejected&&!last.runId):!['completed','failed','interrupted'].includes(child.status)))fail('RECIPE_RECOVERY_UNRESOLVED');e.state='cancelled';e.reason='RECONCILED_WITHOUT_REPLAY';
   }else fail('RECIPE_ACTION_INVALID');
   e.updatedAt=now();const result=publicExecution(e,row.revision+1);await store.write({projectId,actorId:'recipe-owner',expectedAuthorityEpoch:project.authorityEpoch,idempotencyKey:`recipe-command:${input.idempotencyKey}`,recipeExecution:{id,revision:row.revision},changes:[{expectedRevision:row.revision,entity:{id,kind:'settings',data:e as any}},{expectedRevision:0,entity:{id:receiptId,kind:'settings',data:{category:'recipe_command_receipt',digest,result}}}]});
   if(child&&!['completed','failed','interrupted'].includes(child.status)&&['pause','cancel'].includes(action))try{await port?.interrupt({projectId,sessionId:e.sessionId,bindingId:e.bindingId,runId:child.id});}catch{}return result;
  }),tick,
  async close(){if(timer)clearInterval(timer);await queue;await ready;closed=true;},
 };
}
