import type {StoreWrite,StoredEntity} from '../../../../packages/contracts/storage/local-store.ts';
import {defaultRegistry,validateRegistry,workflowCategory,workflowSnapshot,requiredBoardStates,type WorkflowRegistry} from './registry.mts';
import {transitionAllowed,validateReady} from '../../../../packages/contracts/issues/task-profile.ts';
import {publishPreview,migrationPreview} from './commands.mts';
function fail(code:string):never{throw Object.assign(new Error(code),{code});}
export function registryFromRows(rows:readonly StoredEntity[]):WorkflowRegistry{return validateRegistry(rows.find(r=>r.id==='m2-workflows')?.data??defaultRegistry());}
export function workflowWriteContext(command:StoreWrite,rows:StoredEntity[]){
 const registry=registryFromRows(rows),registryRow=rows.find(r=>r.id==='m2-workflows'),boardRow=rows.find(r=>r.id==='m2-board');
 const tasks=rows.filter(r=>r.kind==='task');const board=(boardRow?.data.value??{columns:defaultRegistry().workflows[0].versions[0].definition.states.map(s=>({statuses:[s.id]})),outOfBoard:false}) as any;
 const snapshot={tasks,board,workflows:registry,settingsRevisions:{workflows:registryRow?.revision??0,board:boardRow?.revision??0}};
 const change=command.changes.find(c=>c.entity.id==='m2-workflows');
 let proposed=registry;
 if(change){
  if(change.delete||change.entity.kind!=='settings')fail('WORKFLOW_HISTORY_IMMUTABLE');
  proposed=validateRegistry(change.entity.data);
  for(const old of registry.workflows){const next=proposed.workflows.find(w=>w.id===old.id);if(!next||old.archived&&!next.archived||old.versions.some((v,i)=>JSON.stringify(v)!==JSON.stringify(next.versions[i])))fail('WORKFLOW_HISTORY_IMMUTABLE');}
  const added=proposed.workflows.flatMap(w=>w.versions.filter(v=>!registry.workflows.find(old=>old.id===w.id)?.versions.some(old=>old.version===v.version)));
  if(added.length){const pin=command.workflowPublish;if(!pin||added.length!==1)fail('WORKFLOW_PUBLISH_PREVIEW_REQUIRED');const preview=publishPreview(snapshot,pin.workflowId);const expected=registry.workflows.find(w=>w.id===pin.workflowId)!;
   if(command.changes.some(c=>c.entity.kind==='task'||c.entity.kind==='run'))fail('WORKFLOW_PUBLISH_SCOPE_CONFLICT');
   if(pin.registryRevision!==snapshot.settingsRevisions.workflows||pin.boardRevision!==snapshot.settingsRevisions.board||pin.previewDigest!==preview.previewDigest||added[0].version!==preview.version||added[0].definitionHash!==preview.definitionHash||JSON.stringify(added[0].definition)!==JSON.stringify(expected.draft))fail('WORKFLOW_PUBLISH_PREVIEW_REQUIRED');
  }
 }
 if(command.workflowMigration){const pin=command.workflowMigration,preview=migrationPreview(snapshot,pin);
  if(pin.previewDigest!==preview.previewDigest||pin.registryRevision!==snapshot.settingsRevisions.workflows||pin.boardRevision!==snapshot.settingsRevisions.board||JSON.stringify(pin.tasks)!==JSON.stringify(preview.tasks.map(t=>({id:t.id,revision:t.revision}))))fail('WORKFLOW_MIGRATION_STALE');
  const changes=command.changes.filter(c=>c.entity.kind==='task');if(changes.some(c=>c.delete)||changes.length!==preview.tasks.length||preview.tasks.some(t=>!changes.some(c=>c.entity.id===t.id&&c.expectedRevision===t.revision&&c.entity.data?.status===t.newStatus&&((c.entity.data as any)?.workflow)?.id===pin.workflowId&&((c.entity.data as any)?.workflow)?.version===pin.toVersion)))fail('WORKFLOW_MIGRATION_SCOPE_CONFLICT');
  if(!command.requireIdle||!command.taskManagerReason?.trim()||command.actorId.startsWith('agent:'))fail('WORKFLOW_MIGRATION_AUTHORITY_REQUIRED');
 }
 const proposedBoard=(command.changes.find(c=>c.entity.id==='m2-board')?.entity.data as Record<string,unknown>|undefined)?.value??board;
 const proposedTasks=tasks.filter(t=>!command.changes.some(c=>c.entity.kind==='task'&&c.entity.id===t.id)).map(t=>t.data);
 for(const c of command.changes)if(c.entity.kind==='task'&&!c.delete)proposedTasks.push(c.entity.data as Record<string,unknown>);
 // Board coverage includes every active version and every historical pin still in use.
 if(change||command.changes.some(c=>c.entity.id==='m2-board'))validateWorkflowBoard(proposed,proposedTasks,proposedBoard);
 for(const c of command.changes){if(c.entity.kind!=='run')continue;const old=rows.find(r=>r.id===c.entity.id);const before=(old?.data.runtimeRun??old?.data.appAgentRun) as any;const after=((c.entity.data as any)?.runtimeRun??(c.entity.data as any)?.appAgentRun) as any;
  if(before?.workflowSnapshot&&JSON.stringify(before.workflowSnapshot)!==JSON.stringify(after?.workflowSnapshot))fail('RUNTIME_WORKFLOW_PIN_IMMUTABLE');
  if(after?.workflowSnapshot){const ref=after.workflowSnapshot.ref,snapshot=workflowSnapshot(proposed,ref);if(after.workflowSnapshot.definitionHash!==snapshot.definitionHash||JSON.stringify(after.workflowSnapshot.definition)!==JSON.stringify(snapshot.definition)||JSON.stringify(after.workflowSnapshot.executionRecipe)!==JSON.stringify({id:'paos_m1_execution',version:'m1_fixed_v1'}))fail('RUNTIME_WORKFLOW_PIN_INVALID');const task=tasks.find(t=>t.id===(after.taskId??after.taskContext?.taskId));if(!before&&(!task||JSON.stringify(task.data.workflow)!==JSON.stringify(ref)))fail('RUNTIME_WORKFLOW_PIN_INVALID');}
 }
 return {registry:proposed,board};
}
export function validateWorkflowTask(command:StoreWrite,task:any,before:any,registry:WorkflowRegistry){
 if(before?.schemaVersion==='m2_task_profile_v1'&&JSON.stringify(before.workflow)!==JSON.stringify(task.workflow)&&!command.workflowMigration)fail('WORKFLOW_MIGRATION_REQUIRED');
 const definition=workflowSnapshot(registry,task.workflow).definition,category=workflowCategory(registry,task),prior=before?workflowCategory(registry,before):null;
 const migrating=!!command.workflowMigration;
 let guards:string[]=[];
 if(!before){const workflow=registry.workflows.find(w=>w.id===task.workflow.id);if(!workflow||workflow.archived||workflow.activeVersion!==task.workflow.version)fail('WORKFLOW_ASSIGNMENT_INVALID');if(task.status!==definition.states.find(s=>s.initial)!.id)fail('INITIAL_STATUS_REQUIRED');}
 if(before&&before.status!==task.status&&!migrating){const actor=command.actorId.startsWith('agent:')?'agent':'user';const transitions=definition.transitions.filter(t=>t.from===before.status&&t.to===task.status&&t.actors.includes(actor));if(!transitions.length)fail('TRANSITION_REQUIRED');if(transitions.length>1)fail('WORKFLOW_TRANSITION_AMBIGUOUS');
  if(task.workflow.id==='default'&&task.workflow.version===1&&!transitionAllowed(prior!,category,command.taskManagerAction==='complete'))fail('TRANSITION_REQUIRED');
  const transition=transitions[0];guards=transition.guards;if(transition.requiresDecision&&(!command.taskManagerReason?.trim()||actor==='agent'))fail('WORKFLOW_DECISION_REQUIRED');
  for(const field of transition.requiredFields){const v=task[field];if(v===null||v===undefined||typeof v==='string'&&!v.trim()||Array.isArray(v)&&!v.length)fail('WORKFLOW_REQUIRED_FIELDS');}
 }
 // Same-state migrations can change semantic category, so terminal and blocker gates use categories too.
 if(guards.includes('ready'))validateReady(task);
 if(migrating||!before||before.status!==task.status){if((category==='done'||guards.includes('criteria'))&&(!task.acceptanceCriteria.length||task.acceptanceCriteria.some((c:string)=>!task.criteriaEvidence.some((e:any)=>e.criterion===c&&e.outcome==='passed'&&e.evidence.trim()))))fail('CRITERIA_EVIDENCE_REQUIRED');if(task.blocker&&(['in_progress','done'].includes(category)||guards.includes('blocker')))fail('BLOCKER_RESOLUTION_REQUIRED');if(['done','cancelled'].includes(category)&&before&&!command.taskManagerReason?.trim())fail('REASON_REQUIRED');}
 return {category,prior,migrating,guards};
}
export function validateWorkflowBoard(registry:WorkflowRegistry,tasks:any[],board:any){if(!board)return;const required=requiredBoardStates(registry,tasks),statuses=board.columns?.flatMap((c:any)=>c.statuses);if(!Array.isArray(statuses)||new Set(statuses).size!==statuses.length||(!board.outOfBoard&&required.some(s=>!statuses.includes(s))))fail('WORKFLOW_BOARD_MAPPING_REQUIRED');}
