import {createHash} from 'node:crypto';
import type {RecipeRecoveryDecision} from '../../../../packages/contracts/execution-recipes/recipe.ts';
import type {WorkflowRecipe,WorkflowSnapshot,WorkflowTransition} from '../../../../packages/contracts/workflows/workflow.ts';
import type {AssetPin} from '../../../../packages/contracts/team/assets.ts';
export function recipeFail(code:string):never{throw Object.assign(new Error(code),{code});}
export const recipeHash=(value:unknown)=>createHash('sha256').update(JSON.stringify(value)??'undefined').digest('hex');
/** Runtime accounting and phase changes cannot redefine the authorized task. */
export function semanticTask(data:Record<string,any>){const {status,actual,sessionIds,criteriaEvidence,resolution,updatedAt,...scope}=data;return {...scope,files:(scope.files??[]).map(({actualOperation,...file}:any)=>file)};}
export const recipeScopeHash=(data:Record<string,any>)=>recipeHash(semanticTask(data));
export type Attempt={stepId:string;iteration:number;try:number;clientMessageId:string;runId?:string;admissionRejected?:boolean;state:'planned'|'dispatched'|'completed'|'failed';startedAt:number;deadlineAt:number;artifacts?:{path:string;sha256:string}[]};
export type Execution={recoveryDecisions?:RecipeRecoveryDecision[];category:'recipe_execution';id:string;projectId:string;taskId:string;sessionId:string;bindingId:string;queueEntryId?:string;mode:'recipe';state:'running'|'paused'|'cancel_requested'|'recovery_required'|'completed'|'failed'|'cancelled'|'needs_user_decision'|'transition_blocked';scopeHash:string;taskContext:Record<string,any>;workflowSnapshot:WorkflowSnapshot;transition:WorkflowTransition;recipe:WorkflowRecipe;pins:Record<string,AssetPin[]>;inputArtifacts:{path:string;sha256:string}[];budgetId:string;policyRevision:number;policyHash:string;queue:string[];arrivals:Record<string,Record<string,number>>;iterations:Record<string,number>;attempts:Attempt[];createdAt:number;updatedAt:number;reason?:string;outcome?:'success'|'failure';startDigest:string};
export const ownsTask=(e:Execution)=>!['completed','failed','cancelled','needs_user_decision','transition_blocked'].includes(e.state);
export const publicSteps=(recipe:WorkflowRecipe,pins:Record<string,AssetPin[]>)=>recipe.steps.map(s=>({...s,pins:(pins[s.id]??[]).map(({assetId,kind,version,hash,requestedModel,requestedEffort,observedModel,observedEffort})=>({assetId,kind,version,hash,requestedModel,requestedEffort,observedModel,observedEffort}))}));
export type {RecipeExecutionView} from '../../../../packages/contracts/execution-recipes/recipe.ts';
export const publicExecution=(e:Execution,revision:number)=>({recoveryDecisions:e.recoveryDecisions??[],id:e.id,projectId:e.projectId,taskId:e.taskId,sessionId:e.sessionId,mode:e.mode,state:e.state,revision,workflow:e.workflowSnapshot.ref,recipeId:e.recipe.id,transitionId:e.transition.id,steps:publicSteps(e.recipe,e.pins),iterations:e.iterations,attempts:e.attempts,createdAt:e.createdAt,updatedAt:e.updatedAt,reason:e.reason??null,outcome:e.outcome??null});
export function pathKey(path:string){if(typeof path!=='string'||!path||path.includes('\\')||path.startsWith('/')||/[:\x00-\x1f*?]/.test(path)||path!=='.'&&path.split('/').some(p=>!p||p==='.'||p==='..'||/[. ]$/.test(p)))recipeFail('RECIPE_PATH_INVALID');return path.toLowerCase();}
/** Qualification preserves historical metadata, including bounded cyclic recipes. */
export function qualifyGraph(recipe:WorkflowRecipe){
 const steps=recipe.steps;if(!steps.length||steps.length>32)recipeFail('RECIPE_GRAPH_INVALID');const ids=new Set(steps.map(s=>s.id));if(ids.size!==steps.length)recipeFail('RECIPE_GRAPH_INVALID');
 const edges=new Map<string,string[]>(),parents=new Map<string,string[]>();for(const s of steps)parents.set(s.id,[]);
 for(const [i,s] of steps.entries()){
  if(s.iterationBudget<1||s.retryBudget<0||s.timeoutSeconds<1)recipeFail('RECIPE_GRAPH_INVALID');
  if(s.inputArtifacts.length>32||s.outputArtifacts.length>32||s.checks.length>64)recipeFail('RECIPE_ARTIFACT_LIMIT');
  for(const p of [...s.inputArtifacts,...s.outputArtifacts,...s.ownership])pathKey(p);
  edges.set(s.id,[...new Set(s.next??(steps[i+1]?[steps[i+1].id]:[]))]);
 }
 for(const s of steps)for(const p of s.join??[]){if(!ids.has(p))recipeFail('RECIPE_GRAPH_INVALID');edges.set(p,[...new Set([...edges.get(p)!,s.id])]);}
 for(const [id,targets] of edges)for(const target of targets){if(!ids.has(target))recipeFail('RECIPE_GRAPH_INVALID');parents.get(target)!.push(id);}
 const seen=new Set<string>(),active=new Set<string>(),forward=new Map<string,string[]>();
 function visit(id:string){if(seen.has(id))return;seen.add(id);active.add(id);forward.set(id,[]);for(const target of edges.get(id)!){if(active.has(target))continue;forward.get(id)!.push(target);visit(target);}active.delete(id);}
 visit(steps[0].id);if(seen.size!==steps.length)recipeFail('RECIPE_GRAPH_UNREACHABLE');
 const reaches=(from:string,to:string,visited=new Set<string>()):boolean=>{if(from===to)return true;if(visited.has(from))return false;visited.add(from);return (forward.get(from)??[]).some(n=>reaches(n,to,visited));};
 for(let a=0;a<steps.length;a++)for(let b=a+1;b<steps.length;b++)if(!reaches(steps[a].id,steps[b].id)&&!reaches(steps[b].id,steps[a].id)){
  for(const x of steps[a].ownership.map(pathKey))for(const y of steps[b].ownership.map(pathKey))if(x==='.'||y==='.'||x===y||x.startsWith(y+'/')||y.startsWith(x+'/'))recipeFail('WORKFLOW_WRITER_OVERLAP');
 }
 if(steps.reduce((sum,s)=>sum+s.iterationBudget*(s.retryBudget+1),0)>1000)recipeFail('RECIPE_ATTEMPT_LIMIT');const forwardParents=new Map<string,string[]>();for(const id of ids)forwardParents.set(id,[]);for(const [from,targets]of forward)for(const target of targets)forwardParents.get(target)!.push(from);for(const s of steps)if(s.join?.length&&forwardParents.get(s.id)!.some(parent=>!s.join!.includes(parent)))recipeFail('RECIPE_JOIN_INCOMPLETE');return {edges,parents,forwardParents};
}
