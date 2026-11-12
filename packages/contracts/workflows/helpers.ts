import type {WorkflowCategory,WorkflowRegistry,WorkflowSnapshot} from './workflow.ts';
function fail(code:string):never{throw Object.assign(new Error(code),{code});}
export function workflowSnapshot(registry:WorkflowRegistry,ref:{id:string;version:number}):WorkflowSnapshot{
 const version=registry.workflows.find(w=>w.id===ref.id)?.versions.find(v=>v.version===ref.version);if(!version)fail('WORKFLOW_VERSION_NOT_FOUND');return structuredClone({ref,definition:version.definition,definitionHash:version.definitionHash});
}
export function workflowCategory(registry:WorkflowRegistry,task:{schemaVersion?:unknown;status:unknown;workflow?:{id:string;version:number}}):WorkflowCategory{
 if(task.schemaVersion!=='m2_task_profile_v1')return task.status as WorkflowCategory;
 const state=workflowSnapshot(registry,task.workflow!).definition.states.find(s=>s.id===task.status);if(!state)fail('WORKFLOW_STATE_NOT_FOUND');return state.category;
}
/** Runtime/owner actions require one unambiguous state, never the first matching label. */
export function categoryState(registry:WorkflowRegistry,task:{schemaVersion?:unknown;workflow?:{id:string;version:number}},category:WorkflowCategory):string{
 if(task.schemaVersion!=='m2_task_profile_v1')return category;const matches=workflowSnapshot(registry,task.workflow!).definition.states.filter(s=>s.category===category);if(matches.length!==1)fail('WORKFLOW_STATE_AMBIGUOUS');return matches[0].id;
}
export function requiredBoardStates(registry:WorkflowRegistry,tasks:{schemaVersion?:unknown;workflow?:{id:string;version:number}}[]):string[]{
 const refs=registry.workflows.filter(w=>!w.archived&&w.activeVersion!==null).map(w=>({id:w.id,version:w.activeVersion!}));
 for(const task of tasks)if(task.schemaVersion==='m2_task_profile_v1')refs.push(task.workflow!);
 return [...new Set(refs.flatMap(ref=>workflowSnapshot(registry,ref).definition.states.map(s=>s.id)))];
}
