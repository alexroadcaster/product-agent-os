import type {LocalStore} from '../storage/local-store.mts';
import {defaultRegistry,validateRegistry,workflowSnapshot,workflowCategory,categoryState} from './registry.mts';
export async function runtimeWorkflow(store:LocalStore,projectId:string,task:any){
 const registry=task.schemaVersion==='m2_task_profile_v1'?validateRegistry((await store.get(projectId,'m2-workflows'))?.data??defaultRegistry()):defaultRegistry();
 const snapshot=task.schemaVersion==='m2_task_profile_v1'?{...workflowSnapshot(registry,task.workflow),executionRecipe:{id:'paos_m1_execution',version:'m1_fixed_v1'}}:undefined;
 return {registry,snapshot,category:workflowCategory(registry,task),executionState:()=>categoryState(registry,task,'in_progress')};
}
