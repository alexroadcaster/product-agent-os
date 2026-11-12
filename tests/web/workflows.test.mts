import test from 'node:test';
import assert from 'node:assert/strict';
import {m2Fixture} from './m2-fixture.mts';
import {taskManagerSnapshot} from '../../apps/local-service/src/task-manager/service.mts';
import {defaultRegistry,workflowDigest} from '../../apps/local-service/src/workflows/registry.mts';
import type {WorkflowDefinition} from '../../packages/contracts/workflows/workflow.ts';
import {createRuntimeStoragePorts,taskScopeDigest} from '../../apps/local-service/src/runtime/storage-ports.mts';
import type {RuntimeRun} from '../../apps/local-service/src/runtime/codex/coordinator.ts';
import {randomUUID} from 'node:crypto';
import {validateWorkflow} from '../../apps/local-service/src/workflows/registry.mts';
import {recordManualCheck,acceptTask} from '../../apps/local-service/src/tasks/user-commands.mts';
import {createDomainTools} from '../../apps/local-service/src/commands/domain-tools.mts';
import {mkdir} from 'node:fs/promises';
import {join} from 'node:path';
import {DatabaseSync} from 'node:sqlite';
import {openLocalStore,restoreLocalBackup} from '../../apps/local-service/src/storage/local-store.mts';
import {MIGRATION_CHECKSUM,M2_MIGRATION_CHECKSUM,M2B_MIGRATION_CHECKSUM} from '../../apps/local-service/src/storage/migrations/schema.mts';

test('workflow draft is persisted without changing tasks',async t=>{
 const f=await m2Fixture(t),task=await f.create();
 await f.command({action:'workflow-save-draft',workflowId:'manual',expectedRevision:0,definition:{name:'Manual',states:[{id:'queue',name:'Queue',category:'backlog',initial:true},{id:'closed',name:'Closed',category:'done'}],transitions:[{id:'finish',name:'Finish',from:'queue',to:'closed',actors:['user'],requiredFields:[],guards:['criteria','dependencies','children','blocker']}],recipes:[]}});
 assert.equal((await f.store.get('p',task.id))!.revision,1);
 assert.equal((await f.store.get('p','m2-workflows'))!.data.category,'workflow_registry');
});
test('migration reopening a prerequisite marks completed dependents outside its cohort without changing Done',async t=>{
 const f=await m2Fixture(t);await outOfBoard(f);await saveDraft(f,'custom');await publish(f,'custom');let s=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-assign',expectedRevision:s.settingsRevisions.workflows,defaultWorkflowId:'custom'});
 const prerequisite=await f.create('Prerequisite',{acceptanceCriteria:['Verified']});s=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-assign',expectedRevision:s.settingsRevisions.workflows,defaultWorkflowId:'default'});const dependent=await f.create('Completed dependent',{acceptanceCriteria:['Verified']});
 s=await taskManagerSnapshot(f.store,'p');await f.command({action:'link',expectedRevision:s.settingsRevisions.links,link:{sourceId:prerequisite.id,targetId:dependent.id,relation:'blocks',reason:'Required'}});
 const evidence=[{criterion:'Verified',outcome:'passed',evidence:'Observed fixture'}];await f.command({action:'transition',taskId:prerequisite.id,expectedRevision:prerequisite.revision,status:'custom_done',manual:true,reason:'Verified',evidence});await f.command({action:'transition',taskId:dependent.id,expectedRevision:dependent.revision,status:'done',manual:true,reason:'Verified',evidence});
 const before=(await f.store.get('p',dependent.id))!;await saveDraft(f,'custom');await publish(f,'custom');s=await taskManagerSnapshot(f.store,'p');const args={workflowId:'custom',fromVersion:1,toVersion:2,statusMapping:{custom_done:'custom_backlog'},expectedRevision:s.settingsRevisions.workflows};const preview=await f.command({action:'workflow-migration-preview',...args}) as any;assert.equal(preview.tasks.length,1);
 await f.command({action:'workflow-migrate',...args,previewDigest:preview.previewDigest,reason:'Reopen migrated prerequisite'});const after=(await f.store.get('p',dependent.id))!;assert.equal(after.status,'done');assert.equal(after.data.resolution,before.data.resolution);assert.deepEqual(after.data.criteriaEvidence,before.data.criteriaEvidence);assert.ok((after.data.risks as string[]).includes('dependency_review'));
});

type Fixture=Awaited<ReturnType<typeof m2Fixture>>;
const customDefinition=():WorkflowDefinition=>{
 const d=structuredClone(defaultRegistry().workflows[0].versions[0].definition);d.name='Custom delivery';
 d.states=d.states.map(s=>({...s,id:`custom_${s.id}`}));d.transitions=d.transitions.map(tr=>({...tr,from:`custom_${tr.from}`,to:`custom_${tr.to}`}));return d;
};
async function saveDraft(f:Fixture,id:string,definition=customDefinition()){
 const snapshot=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-save-draft',workflowId:id,definition,expectedRevision:snapshot.settingsRevisions.workflows});
}
async function publish(f:Fixture,id:string){
 const snapshot=await taskManagerSnapshot(f.store,'p');
 const preview=await f.command({action:'workflow-publish-preview',workflowId:id,expectedRevision:snapshot.settingsRevisions.workflows}) as any;
 await f.command({action:'workflow-publish',workflowId:id,expectedRevision:snapshot.settingsRevisions.workflows,previewDigest:preview.previewDigest});return preview;
}
async function outOfBoard(f:Fixture){const s=await taskManagerSnapshot(f.store,'p');await f.command({action:'board',expectedRevision:s.settingsRevisions.board,board:{...s.board,outOfBoard:true}});}
async function customReady(f:Fixture,title='Prepared'){
 const row=await f.create(title,{summary:'Scope',technicalValue:'Technical value',productValue:'Product value',files:[{relativePath:'fixture.txt',plannedOperation:'create',actualOperation:null}],acceptanceCriteria:['Observed fixture'],estimateSeconds:60,risks:['none']});
 await f.command({action:'transition',taskId:row.id,expectedRevision:row.revision,status:'custom_ready',reason:'Prepared'});return (await f.store.get('p',row.id))!;
}

test('publish custom workflow, assignment precedence and immutable pins survive rollback/archive',async t=>{
 const f=await m2Fixture(t);await outOfBoard(f);const legacy=await f.create();
 await saveDraft(f,'custom');const preview=await publish(f,'custom');assert.equal(preview.missingStates.length,8);
 assert.deepEqual((await f.store.get('p',legacy.id))!.data.workflow,{id:'default',version:1});
 let s=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-assign',expectedRevision:s.settingsRevisions.workflows,typeMapping:{bug:'custom'}});
 const bug=await f.create('Bug',{type:'bug'});assert.equal(bug.status,'custom_backlog');assert.deepEqual(bug.data.workflow,{id:'custom',version:1});
 const raw={...bug.data,id:randomUUID(),key:'',title:'Explicit default'};await f.command({action:'save',task:raw,workflowId:'default',expectedRevision:0});assert.equal((await f.store.get('p',String(raw.id)))!.status,'backlog');
 await assert.rejects(f.command({action:'save',task:{...bug.data,workflow:{id:'default',version:1}},expectedRevision:bug.revision}),{code:'WORKFLOW_MIGRATION_REQUIRED'});
 await saveDraft(f,'custom',{...customDefinition(),name:'Version two'});await publish(f,'custom');
 assert.deepEqual((await f.store.get('p',bug.id))!.data.workflow,{id:'custom',version:1});
 s=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-rollback',workflowId:'custom',version:1,expectedRevision:s.settingsRevisions.workflows});
 assert.equal((await taskManagerSnapshot(f.store,'p')).workflows.workflows.find(w=>w.id==='custom')!.versions.length,2);
 s=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-assign',expectedRevision:s.settingsRevisions.workflows,typeMapping:{}});
 s=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-archive',workflowId:'custom',expectedRevision:s.settingsRevisions.workflows});
 await assert.rejects(f.command({action:'save',task:{...bug.data,id:randomUUID(),key:''},workflowId:'custom',expectedRevision:0}),{code:'WORKFLOW_ASSIGNMENT_INVALID'});
 assert.deepEqual((await f.store.get('p',bug.id))!.data.workflow,{id:'custom',version:1});
});

test('custom transitions enforce Ready, completion evidence, blockers, due reason and user actor',async t=>{
 const f=await m2Fixture(t);await outOfBoard(f);await saveDraft(f,'custom');await publish(f,'custom');
 let s=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-assign',expectedRevision:s.settingsRevisions.workflows,defaultWorkflowId:'custom'});
 const task=await f.create();const transition=(status:string,extra={})=>f.command({action:'transition',taskId:task.id,expectedRevision:task.revision,status,reason:'Reviewed',...extra});
 await assert.rejects(transition('custom_ready'),{code:'READY_FIELDS_REQUIRED'});
 await assert.rejects(transition('custom_done',{manual:true}),{code:'CRITERIA_EVIDENCE_REQUIRED'});
 await assert.rejects(f.store.write({projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:randomUUID(),changes:[{expectedRevision:task.revision,entity:{id:task.id,kind:'task',data:{...task.data,dueDate:'2027-01-01'}}}]}),{code:'DUE_DATE_REASON_REQUIRED'});
 const prepared=await customReady(f);
 await f.command({action:'transition',taskId:prepared.id,expectedRevision:prepared.revision,status:'custom_done',reason:'Passed',manual:true,evidence:[{criterion:'Observed fixture',outcome:'passed',evidence:'Fixture result'}]});
 assert.equal((await f.store.get('p',prepared.id))!.status,'custom_done');
});

test('migration preview rejects stale task revisions and phantom inserts atomically',async t=>{
 const f=await m2Fixture(t);await outOfBoard(f);const task=await f.create();await saveDraft(f,'default',customDefinition());await publish(f,'default');
 const mapping=Object.fromEntries(defaultRegistry().workflows[0].versions[0].definition.states.map(s=>[s.id,`custom_${s.id}`]));
 let snapshot=await taskManagerSnapshot(f.store,'p');const input={workflowId:'default',fromVersion:1,toVersion:2,statusMapping:mapping,expectedRevision:snapshot.settingsRevisions.workflows};
 const preview=await f.command({action:'workflow-migration-preview',...input}) as any;assert.equal(preview.affectedCount,1);
 await f.command({action:'save',expectedRevision:task.revision,task:{...task.data,title:'Changed'}});
 await assert.rejects(f.command({action:'workflow-migrate',...input,previewDigest:preview.previewDigest,reason:'Approved migration'}),{code:'PREVIEW_REQUIRED'});
 const fresh=await f.command({action:'workflow-migration-preview',...input}) as any;
 // Insert a v1 task under a temporary rollback, then restore v2. Both registry revisions invalidate the preview.
 await f.command({action:'workflow-rollback',workflowId:'default',version:1,expectedRevision:input.expectedRevision});await f.create('Phantom');snapshot=await taskManagerSnapshot(f.store,'p');
 await assert.rejects(f.command({action:'workflow-migrate',...input,expectedRevision:snapshot.settingsRevisions.workflows,previewDigest:fresh.previewDigest,reason:'Approved migration'}),{code:'PREVIEW_REQUIRED'});
 const finalInput={...input,expectedRevision:snapshot.settingsRevisions.workflows};const final=await f.command({action:'workflow-migration-preview',...finalInput}) as any;
 await f.command({action:'workflow-migrate',...finalInput,previewDigest:final.previewDigest,reason:'Approved migration'});
 const changed=await f.store.get('p',task.id);assert.equal(changed!.status,'custom_backlog');assert.deepEqual(changed!.data.workflow,{id:'default',version:2});
});

test('published custom runtime stays pinned while v2 publishes; active migration waits for terminal receipt',async t=>{
 const f=await m2Fixture(t);await outOfBoard(f);await saveDraft(f,'custom');await publish(f,'custom');let s=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-assign',expectedRevision:s.settingsRevisions.workflows,defaultWorkflowId:'custom'});
 const task=await customReady(f,'Runtime task');const ports=createRuntimeStoragePorts(f.store,{actorId:'local-user'});
 await ports.saveBinding({id:'binding',projectId:'p',sessionId:'session',accountId:'synthetic',workspaceRoot:f.root,directoryIdentity:'fixture',mode:'execution',profileId:'fixture',generation:'generation',threadId:'thread'});
 const run:RuntimeRun={id:'run',bindingId:'binding',projectId:'p',sessionId:'session',accountId:'synthetic',generation:'generation',threadId:'thread',turnId:null,clientMessageId:'message',inputDigest:'input',taskId:task.id,scopeDigest:taskScopeDigest(task),targetRevision:task.revision,state:'dispatching'};
 await ports.appendIntent(run);let stored=await f.store.get('p','run');const pin=(stored!.data.runtimeRun as RuntimeRun).workflowSnapshot;assert.equal(pin!.ref.version,1);assert.equal((await f.store.get('p',task.id))!.status,'custom_in_progress');
 await assert.rejects(f.store.write({projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:randomUUID(),changes:[{expectedRevision:stored!.revision,entity:{id:'run',kind:'run',status:stored!.status,data:{...stored!.data,runtimeRun:{...(stored!.data.runtimeRun as RuntimeRun),workflowSnapshot:undefined}}}}]}),{code:'RUNTIME_WORKFLOW_PIN_IMMUTABLE'});
 await saveDraft(f,'custom',{...customDefinition(),name:'Version two'});await publish(f,'custom');assert.deepEqual((await f.store.get('p','run'))!.data.runtimeRun,stored!.data.runtimeRun);
 s=await taskManagerSnapshot(f.store,'p');const input={workflowId:'custom',fromVersion:1,toVersion:2,statusMapping:Object.fromEntries(customDefinition().states.map(s=>[s.id,s.id])),expectedRevision:s.settingsRevisions.workflows};const preview=await f.command({action:'workflow-migration-preview',...input}) as any;
 await assert.rejects(f.command({action:'workflow-migrate',...input,previewDigest:preview.previewDigest,reason:'Migrate'}),{code:'ACTIVE_RUN_RECONCILIATION_REQUIRED'});
 await ports.updateRun({...run,state:'interrupted'});stored=await f.store.get('p','run');assert.deepEqual((stored!.data.runtimeRun as RuntimeRun).workflowSnapshot,pin);
 const fresh=await f.command({action:'workflow-migration-preview',...input}) as any;await f.command({action:'workflow-migrate',...input,previewDigest:fresh.previewDigest,reason:'Migrate after Stop receipt'});
 assert.deepEqual((await f.store.get('p',task.id))!.data.workflow,{id:'custom',version:2});
});

test('direct store cannot rewrite immutable workflow history',async t=>{
 const f=await m2Fixture(t),registry=defaultRegistry();registry.workflows[0].versions[0].definition.name='Rewritten';
 await assert.rejects(f.store.write({projectId:'p',actorId:'local-user',idempotencyKey:randomUUID(),expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:'m2-workflows',kind:'settings',data:registry}}]}),{code:'INVALID_WORKFLOW_VERSION'});
});

test('invalid graphs, terminal actor/guard bypasses and unbounded recipes fail validation',()=>{
 const cases:[(d:WorkflowDefinition)=>void,string][]=[
  [d=>d.states[1].initial=true,'INVALID_WORKFLOW_STATES'],
  [d=>d.transitions=d.transitions.filter(t=>t.from!==d.states[0].id),'WORKFLOW_STATE_UNREACHABLE'],
  [d=>d.transitions.find(t=>t.to==='custom_done')!.guards=[],'TERMINAL_GUARDS_REQUIRED'],
  [d=>d.transitions.find(t=>t.to==='custom_done')!.actors=['agent'],'TERMINAL_GUARDS_REQUIRED'],
  [d=>d.transitions[0].guards=['disable_approvals'],'INVALID_WORKFLOW_TRANSITIONS'],
  [d=>d.transitions[0].recipeId='unknown','WORKFLOW_RECIPE_NOT_FOUND'],
  [d=>d.transitions.push({...d.transitions[0],id:'duplicate'}),'WORKFLOW_TRANSITION_AMBIGUOUS'],
 ];for(const [mutate,code] of cases){const d=customDefinition();mutate(d);assert.throws(()=>validateWorkflow(d),{code});}
 const recipe={id:'recipe',name:'Proposal',steps:[{id:'build',role:'builder',skills:[],profileVersion:'v1',skillVersions:{},inputArtifacts:[],outputArtifacts:[],checks:[],ownership:['src'],timeoutSeconds:30,retryBudget:1,iterationBudget:2,next:['build']}]};
 const valid={...customDefinition(),recipes:[recipe]};assert.equal(validateWorkflow(valid).recipes.length,1);
 recipe.steps[0].timeoutSeconds=Infinity;assert.throws(()=>validateWorkflow(valid),{code:'INVALID_WORKFLOW_RECIPE'});
});

test('recipe skill references remain draft metadata and validation fails closed without a trusted resolver',async t=>{
 const f=await m2Fixture(t),definition=customDefinition();definition.recipes=[{id:'recipe',name:'Proposal',steps:[{id:'build',role:'builder',skills:['missing-skill'],profileVersion:'v1',skillVersions:{'missing-skill':'v1'},inputArtifacts:[],outputArtifacts:[],checks:[],ownership:['src'],timeoutSeconds:30,retryBudget:0,iterationBudget:1}]}];
 await saveDraft(f,'custom',definition);const snapshot=await taskManagerSnapshot(f.store,'p');
 await assert.rejects(f.command({action:'workflow-validate',workflowId:'custom',expectedRevision:snapshot.settingsRevisions.workflows}),{code:'WORKFLOW_SKILL_CATALOG_UNAVAILABLE'});
 await assert.rejects(f.command({action:'workflow-publish-preview',workflowId:'custom',expectedRevision:snapshot.settingsRevisions.workflows}),{code:'WORKFLOW_SKILL_CATALOG_UNAVAILABLE'});
 assert.equal((await taskManagerSnapshot(f.store,'p')).workflows.workflows.find(w=>w.id==='custom')!.versions.length,0);
});

test('publish preview binds board revision and direct writer cannot append or rehash published versions',async t=>{
 const f=await m2Fixture(t);await saveDraft(f,'custom');let s=await taskManagerSnapshot(f.store,'p');const preview=await f.command({action:'workflow-publish-preview',workflowId:'custom',expectedRevision:s.settingsRevisions.workflows}) as any;
 await assert.rejects(f.command({action:'workflow-publish',workflowId:'custom',expectedRevision:s.settingsRevisions.workflows,previewDigest:preview.previewDigest}),{code:'WORKFLOW_BOARD_MAPPING_REQUIRED'});
 await outOfBoard(f);await assert.rejects(f.command({action:'workflow-publish',workflowId:'custom',expectedRevision:s.settingsRevisions.workflows,previewDigest:preview.previewDigest}),{code:'PREVIEW_REQUIRED'});
 await publish(f,'custom');s=await taskManagerSnapshot(f.store,'p');const modified=structuredClone(s.workflows);const definition=modified.workflows[0].versions[0].definition;definition.name='Rehash rewrite';modified.workflows[0].versions[0].definitionHash=workflowDigest(definition);
 const write=(data:any)=>f.store.write({projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:randomUUID(),changes:[{expectedRevision:s.settingsRevisions.workflows,entity:{id:'m2-workflows',kind:'settings',data}}]});
 await assert.rejects(write(modified),{code:'WORKFLOW_HISTORY_IMMUTABLE'});
 const append=structuredClone(s.workflows);append.workflows[0].versions.push({...append.workflows[0].versions[0],version:2,publishedAt:new Date().toISOString()});await assert.rejects(write(append),{code:'WORKFLOW_PUBLISH_PREVIEW_REQUIRED'});
});

test('migration into Done cannot bypass criteria evidence',async t=>{
 const f=await m2Fixture(t);const parent=await f.create('Parent',{type:'epic',acceptanceCriteria:['Verified']});await f.create('Child',{parentId:parent.id});
 const d=structuredClone(defaultRegistry().workflows[0].versions[0].definition);d.states=d.states.map(s=>s.id==='backlog'?{...s,id:'queue'}:s);d.transitions=d.transitions.map(tr=>({...tr,from:tr.from==='backlog'?'queue':tr.from,to:tr.to==='backlog'?'queue':tr.to}));
 await outOfBoard(f);await saveDraft(f,'default',d);await publish(f,'default');const s=await taskManagerSnapshot(f.store,'p');const args={workflowId:'default',fromVersion:1,toVersion:2,statusMapping:{backlog:'done'},expectedRevision:s.settingsRevisions.workflows};const preview=await f.command({action:'workflow-migration-preview',...args}) as any;
 await assert.rejects(f.command({action:'workflow-migrate',...args,previewDigest:preview.previewDigest,reason:'Attempt'}),{code:'CRITERIA_EVIDENCE_REQUIRED'});
 assert.equal((await f.store.get('p',parent.id))!.status,'backlog');
});

test('custom terminal semantics retain children, dependency, blocker and cancellation safeguards',async t=>{
 const f=await m2Fixture(t);await outOfBoard(f);await saveDraft(f,'custom');await publish(f,'custom');let s=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-assign',expectedRevision:s.settingsRevisions.workflows,defaultWorkflowId:'custom'});
 const evidence=[{criterion:'Verified',outcome:'passed',evidence:'Observed'}],parent=await f.create('Parent',{type:'epic',acceptanceCriteria:['Verified']});await f.create('Child',{parentId:parent.id});
 await assert.rejects(f.command({action:'transition',taskId:parent.id,expectedRevision:parent.revision,status:'custom_done',manual:true,reason:'Reviewed',evidence}),{code:'CHILDREN_INCOMPLETE'});
 const blocker=await f.create('Prerequisite'),target=await f.create('Target',{acceptanceCriteria:['Verified']});s=await taskManagerSnapshot(f.store,'p');await f.command({action:'link',expectedRevision:s.settingsRevisions.links,link:{sourceId:blocker.id,targetId:target.id,relation:'blocks',reason:'Required'}});
 await assert.rejects(f.command({action:'transition',taskId:target.id,expectedRevision:target.revision,status:'custom_done',manual:true,reason:'Reviewed',evidence}),{code:'DEPENDENCY_BLOCKED'});
 const blocked=await f.create('Manual blocker',{acceptanceCriteria:['Verified'],blocker:{reason:'Await input',owner:'user',since:new Date().toISOString()}});
 await assert.rejects(f.command({action:'transition',taskId:blocked.id,expectedRevision:blocked.revision,status:'custom_done',manual:true,reason:'Reviewed',evidence}),{code:'BLOCKER_RESOLUTION_REQUIRED'});
 await assert.rejects(f.command({action:'transition',taskId:target.id,expectedRevision:target.revision,status:'custom_cancelled',reason:''}),{code:'REASON_REQUIRED'});
 await f.command({action:'transition',taskId:target.id,expectedRevision:target.revision,status:'custom_cancelled',reason:'Cancelled explicitly'});assert.equal((await f.store.get('p',target.id))!.data.resolution,'cancelled');
});

test('custom agent domain transitions and owner acceptance use semantic categories',async t=>{
 const f=await m2Fixture(t);await outOfBoard(f);await saveDraft(f,'custom');await publish(f,'custom');let s=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-assign',expectedRevision:s.settingsRevisions.workflows,defaultWorkflowId:'custom'});
 const task=await customReady(f);const ports=createRuntimeStoragePorts(f.store,{actorId:'local-user'});await ports.saveBinding({id:'binding',projectId:'p',sessionId:'session',accountId:'synthetic',workspaceRoot:f.root,directoryIdentity:'fixture',mode:'execution',profileId:'fixture',generation:'generation',threadId:'thread'});
 const run:RuntimeRun={id:'run',bindingId:'binding',projectId:'p',sessionId:'session',accountId:'synthetic',generation:'generation',threadId:'thread',turnId:null,clientMessageId:'message',inputDigest:'input',taskId:task.id,scopeDigest:taskScopeDigest(task),targetRevision:task.revision,state:'running'};await ports.appendIntent(run);
 const tools=createDomainTools({store:f.store}),binding={id:'binding',projectId:'p',sessionId:'session',accountId:'synthetic',workspaceRoot:f.root,directoryIdentity:'fixture',mode:'execution' as const,profileId:'fixture',generation:'generation',threadId:'thread'};
 let row=(await f.store.get('p',task.id))!;await assert.rejects(tools.dispatch({tool:'task_patch',arguments:{taskId:task.id,expectedRevision:row.revision,patch:{status:'custom_done'}},binding,run,requestId:1}),{code:'TOOL_PATCH_FORBIDDEN'});
 await tools.dispatch({tool:'task_patch',arguments:{taskId:task.id,expectedRevision:row.revision,patch:{status:'custom_review'}},binding,run,requestId:2});assert.equal((await f.store.get('p',task.id))!.status,'custom_review');
 await ports.updateRun({...run,state:'completed'});for(const status of ['custom_verification','custom_awaiting_acceptance']){row=(await f.store.get('p',task.id))!;await f.command({action:'transition',taskId:task.id,expectedRevision:row.revision,status,reason:'Checked'});}
 row=(await f.store.get('p',task.id))!;const check=await recordManualCheck(f.store,{projectId:'p',taskId:task.id,actorId:'local-user',expectedRevision:row.revision,expectedAuthorityEpoch:1,idempotencyKey:randomUUID(),outcome:'passed',note:'Observed fixture'});
 await acceptTask(f.store,{projectId:'p',taskId:task.id,actorId:'local-user',expectedRevision:row.revision,expectedAuthorityEpoch:1,idempotencyKey:randomUUID(),checkId:check.checkId,accepted:true,note:'Accepted fixture'});assert.equal((await f.store.get('p',task.id))!.status,'custom_done');
});

test('atomic migration detects phantom source tasks even when registry revisions have not changed',async t=>{
 const f=await m2Fixture(t);const task=await f.create();await saveDraft(f,'default',{...defaultRegistry().workflows[0].versions[0].definition,name:'Version two'});await publish(f,'default');let s=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-rollback',workflowId:'default',version:1,expectedRevision:s.settingsRevisions.workflows});s=await taskManagerSnapshot(f.store,'p');
 const mapping=Object.fromEntries(defaultRegistry().workflows[0].versions[0].definition.states.map(s=>[s.id,s.id]));const args={workflowId:'default',fromVersion:1,toVersion:2,statusMapping:mapping,expectedRevision:s.settingsRevisions.workflows};const preview=await f.command({action:'workflow-migration-preview',...args}) as any;await f.create('Phantom');
 await assert.rejects(f.store.write({projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:randomUUID(),requireIdle:true,taskManagerReason:'Approved',workflowMigration:{...args,previewDigest:preview.previewDigest,registryRevision:s.settingsRevisions.workflows,boardRevision:s.settingsRevisions.board,tasks:[{id:task.id,revision:task.revision}]},changes:[{expectedRevision:task.revision,entity:{id:task.id,kind:'task',data:{...task.data,workflow:{id:'default',version:2}}}}]}),{code:'WORKFLOW_MIGRATION_STALE'});
 assert.equal((await f.store.get('p',task.id))!.revision,task.revision);
});

test('workflow format fence is lazy, preserves old checksums and restores its registry/pins',async t=>{
 const f=await m2Fixture(t);assert.equal((await f.store.compatibility()).schemaVersion,1);await f.create();assert.equal((await f.store.compatibility()).schemaVersion,2);
 await assert.rejects(saveDraft(f,'invalid',{...customDefinition(),states:[]}),{code:'INVALID_WORKFLOW_DEFINITION'});assert.equal((await f.store.compatibility()).schemaVersion,2);
 await saveDraft(f,'custom');assert.equal((await f.store.compatibility()).schemaVersion,3);await outOfBoard(f);await publish(f,'custom');
 await mkdir(join(f.root,'backups'));const backup=await f.store.backup(join(f.root,'backups'));assert.equal(backup.manifest.schemaVersion,3);assert.equal(backup.manifest.appCompatibility,'paos-m2b-v1');assert.equal(backup.manifest.migrationChecksum,M2B_MIGRATION_CHECKSUM);
 using snapshot=new DatabaseSync(join(backup.directory,'database.sqlite'),{readOnly:true});const chain=snapshot.prepare('SELECT version,checksum FROM schema_migrations ORDER BY version').all();assert.deepEqual(chain.map(r=>r.version),[1,2,3]);assert.equal(chain[0].checksum,MIGRATION_CHECKSUM);assert.equal(chain[1].checksum,M2_MIGRATION_CHECKSUM);
 await restoreLocalBackup(backup.directory,join(f.root,'restored.sqlite'));const restored=await openLocalStore({databasePath:join(f.root,'restored.sqlite')});try{assert.equal((await restored.compatibility()).schemaVersion,3);assert.deepEqual((await taskManagerSnapshot(restored,'p')).workflows,(await taskManagerSnapshot(f.store,'p')).workflows);}finally{await restored.close();}
});
