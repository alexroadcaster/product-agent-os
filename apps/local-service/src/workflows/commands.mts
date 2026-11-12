import type {StoredEntity,StoreWrite} from '../../../../packages/contracts/storage/local-store.ts';
import {workflowDigest,validateWorkflow,validateRegistry,workflowSnapshot,requiredBoardStates,type WorkflowRegistry} from './registry.mts';
function fail(code:string):never{throw Object.assign(new Error(code),{code});}
type Snapshot={tasks:StoredEntity[];board:{columns:{statuses:string[]}[];outOfBoard:boolean};workflows:WorkflowRegistry;settingsRevisions:Record<string,number>};
export function publishPreview(snapshot:Snapshot,workflowId:string){
 const workflow=snapshot.workflows.workflows.find(w=>w.id===workflowId);if(!workflow||workflow.archived||!workflow.draft)fail('WORKFLOW_DRAFT_NOT_FOUND');
 const definition=validateWorkflow(workflow.draft),version=Math.max(0,...workflow.versions.map(v=>v.version))+1;
 const proposed=structuredClone(snapshot.workflows);const next=proposed.workflows.find(w=>w.id===workflowId)!;next.activeVersion=version;next.versions.push({version,definition,definitionHash:workflowDigest(definition),publishedAt:null});
 const missingStates=requiredBoardStates(proposed,snapshot.tasks.map(t=>t.data)).filter(id=>!snapshot.board.columns.some(c=>c.statuses.includes(id)));
 const affectedTasks=snapshot.tasks.filter(t=>(t.data.workflow as any)?.id===workflowId).map(t=>({id:t.id,revision:t.revision,workflow:t.data.workflow}));
 const preview={workflowId,version,definitionHash:workflowDigest(definition),registryRevision:snapshot.settingsRevisions.workflows,boardRevision:snapshot.settingsRevisions.board,missingStates,affectedTasks,existingTasksUnchanged:true,recipesExecutable:false};
 return {...preview,previewDigest:workflowDigest(preview)};
}
export function migrationPreview(snapshot:Snapshot,input:Record<string,any>){
 if(!Number.isSafeInteger(input.fromVersion)||!Number.isSafeInteger(input.toVersion)||input.fromVersion<1||input.toVersion<1||!input.statusMapping||typeof input.statusMapping!=='object'||Array.isArray(input.statusMapping))fail('INVALID_WORKFLOW_MIGRATION');
 const old=workflowSnapshot(snapshot.workflows,{id:input.workflowId,version:input.fromVersion}),next=workflowSnapshot(snapshot.workflows,{id:input.workflowId,version:input.toVersion});
 const workflow=snapshot.workflows.workflows.find(w=>w.id===input.workflowId)!;if(workflow.archived)fail('WORKFLOW_ARCHIVED');
 if(Object.entries(input.statusMapping).some(([a,b])=>!old.definition.states.some(s=>s.id===a)||!next.definition.states.some(s=>s.id===b)))fail('INVALID_STATUS_MAPPING');
 const tasks=snapshot.tasks.filter(t=>{const ref=t.data.workflow as any;return t.data.schemaVersion==='m2_task_profile_v1'&&ref?.id===input.workflowId&&ref.version===input.fromVersion;}).sort((a,b)=>a.id.localeCompare(b.id));
 if(tasks.length>90)fail('WORKFLOW_MIGRATION_TOO_LARGE');
 const mappings=tasks.map(t=>{const target=input.statusMapping[t.status];if(!next.definition.states.some(s=>s.id===target))fail('STATUS_MAPPING_REQUIRED');return {id:t.id,revision:t.revision,oldStatus:t.status,newStatus:target};});
 const preview={workflowId:input.workflowId,fromVersion:input.fromVersion,toVersion:input.toVersion,statusMapping:input.statusMapping,registryRevision:snapshot.settingsRevisions.workflows,boardRevision:snapshot.settingsRevisions.board,tasks:mappings,
  oldStates:old.definition.states,newStates:next.definition.states,oldTransitions:old.definition.transitions,newTransitions:next.definition.transitions,board:snapshot.board,requiredFields:next.definition.transitions.map(t=>({transitionId:t.id,requiredFields:t.requiredFields})),affectedCount:tasks.length};
 return {...preview,previewDigest:workflowDigest(preview)};
}
export function workflowCommand(snapshot:Snapshot,input:Record<string,any>):{preview?:Record<string,any>;changes:StoreWrite['changes'];metadata?:Partial<StoreWrite>}{
 const registry=structuredClone(snapshot.workflows),workflow=registry.workflows.find(w=>w.id===input.workflowId),action=input.action;
 if(input.expectedRevision!==snapshot.settingsRevisions.workflows)fail('REVISION_CONFLICT');
 if(action==='workflow-validate'){validateWorkflow(input.definition??workflow?.draft);return {changes:[],preview:{valid:true,recipesExecutable:false}};}
 if(action==='workflow-publish-preview')return {changes:[],preview:publishPreview(snapshot,input.workflowId)};
 if(action==='workflow-migration-preview')return {changes:[],preview:migrationPreview(snapshot,input)};
 let metadata:Partial<StoreWrite>|undefined;
 if(action==='workflow-save-draft'){
  const definition=validateWorkflow(input.definition);if(workflow){if(workflow.archived)fail('WORKFLOW_ARCHIVED');workflow.draft=definition;}else registry.workflows.push({id:input.workflowId,archived:false,activeVersion:null,draft:definition,versions:[]});
 }else if(action==='workflow-publish'){
  const preview=publishPreview(snapshot,input.workflowId);if(preview.previewDigest!==input.previewDigest)fail('PREVIEW_REQUIRED');if(preview.missingStates.length&&!snapshot.board.outOfBoard)fail('WORKFLOW_BOARD_MAPPING_REQUIRED');
  workflow!.versions.push({version:preview.version,definition:workflow!.draft!,definitionHash:preview.definitionHash,publishedAt:new Date().toISOString()});workflow!.activeVersion=preview.version;workflow!.draft=null;
  metadata={workflowPublish:{previewDigest:input.previewDigest,workflowId:input.workflowId,registryRevision:preview.registryRevision,boardRevision:preview.boardRevision}};
 }else if(action==='workflow-assign'){
  if(input.defaultWorkflowId!==undefined)registry.defaultWorkflowId=input.defaultWorkflowId;
  if(input.typeMapping!==undefined)registry.typeMapping=input.typeMapping;
 }else if(action==='workflow-archive'){
  if(!workflow)fail('WORKFLOW_NOT_FOUND');workflow.archived=true;
 }else if(action==='workflow-rollback'){
  if(!workflow||workflow.archived)fail('WORKFLOW_NOT_FOUND');if(!workflow.versions.some(v=>v.version===input.version))fail('WORKFLOW_VERSION_NOT_FOUND');workflow.activeVersion=input.version;
 }else if(action==='workflow-migrate'){
  const preview=migrationPreview(snapshot,input);if(preview.previewDigest!==input.previewDigest)fail('PREVIEW_REQUIRED');if(typeof input.reason!=='string'||!input.reason.trim())fail('REASON_REQUIRED');
  const changes=preview.tasks.map(pin=>{const row=snapshot.tasks.find(t=>t.id===pin.id)!;const state=workflowSnapshot(registry,{id:input.workflowId,version:input.toVersion}).definition.states.find(s=>s.id===pin.newStatus)!;const terminal=['done','cancelled'].includes(state.category);return {expectedRevision:pin.revision,entity:{id:pin.id,kind:'task' as const,data:{...row.data,status:pin.newStatus,workflow:{id:input.workflowId,version:input.toVersion},resolution:state.category==='done'?'completed':state.category==='cancelled'?'cancelled':null,actual:{...(row.data.actual as object),endedAt:terminal?(row.data.actual as any).endedAt??new Date().toISOString():null}}}};});
  return {changes,metadata:{requireIdle:true,taskManagerReason:input.reason,workflowMigration:{previewDigest:input.previewDigest,workflowId:input.workflowId,fromVersion:input.fromVersion,toVersion:input.toVersion,statusMapping:input.statusMapping,registryRevision:preview.registryRevision,boardRevision:preview.boardRevision,tasks:preview.tasks.map(t=>({id:t.id,revision:t.revision}))}}};
 }else fail('UNSUPPORTED_WORKFLOW_ACTION');
 validateRegistry(registry);
 const missing=requiredBoardStates(registry,snapshot.tasks.map(t=>t.data)).filter(s=>!snapshot.board.columns.some(c=>c.statuses.includes(s)));
 if(missing.length&&!snapshot.board.outOfBoard)fail('WORKFLOW_BOARD_MAPPING_REQUIRED');
 return {changes:[{expectedRevision:input.expectedRevision,entity:{id:'m2-workflows',kind:'settings',data:registry}}],metadata};
}
