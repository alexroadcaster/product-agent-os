import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {join} from 'node:path';
import {randomUUID} from 'node:crypto';
import {m2Fixture} from './m2-fixture.mts';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {taskManagerCommand,taskManagerSnapshot} from '../../apps/local-service/src/task-manager/service.mts';
import {defaultRegistry} from '../../apps/local-service/src/workflows/registry.mts';
import {createTeamService} from '../../apps/local-service/src/team/service.mts';
import {createAppAgentGateway} from '../../apps/local-service/src/runtime/app-agent-gateway.mts';
import {createRecipeService} from '../../apps/local-service/src/execution-recipes/service.mts';
import {createScheduler} from '../../apps/local-service/src/scheduler/service.mts';
import {autonomyService} from '../../apps/local-service/src/autonomy-policy/service.mts';
import {defaultAutonomyPolicy} from '../../packages/contracts/autonomy/policy.ts';
import {newM2Task} from '../../packages/contracts/issues/task-profile.ts';
test('five queued workspaces reserve four slots and the fifth advances after a terminal execution',async t=>{
 const f=await m2Fixture(t),gateway=createAppAgentGateway({store:f.store,profileId:'queue-capacity',actorId:'app',executorFactory:async b=>({metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:b.workspaceRoot,mode:b.mode},execute:async()=>({exitCode:0,stdout:'',stderr:''}),interrupt:async()=>{},close:async()=>{}}) as any});
 await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'w',generation:'g'}),auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};
 const inputs=[];for(let i=0;i<5;i++){const projectId='q'+i,root=join(f.root,projectId);await mkdir(root);const bound=await bindProject(projectId,root);await f.store.registerProject({id:projectId,keyPrefix:'QAA'+String.fromCharCode(65+i),canonicalRoot:bound.workspaceRoot,rootIdentity:bound.directoryIdentity,authorityMode:'sql'});
  const command=(input:any)=>taskManagerCommand(f.store,projectId,'local-user',{expectedAuthorityEpoch:1,idempotencyKey:randomUUID(),...input});const definition=structuredClone(defaultRegistry().workflows[0].versions[0].definition);definition.recipes=[{id:'recipe',name:'One step',steps:[{id:'work',role:'builder',profileVersion:'1',skills:[],skillVersions:{},inputArtifacts:[],outputArtifacts:[],checks:[],ownership:['fixture.txt'],timeoutSeconds:60,retryBudget:0,iterationBudget:1}]}];definition.transitions.find(t=>t.id==='ready-in_progress')!.recipeId='recipe';
  await command({action:'workflow-save-draft',workflowId:'recipes',definition,expectedRevision:0});let snapshot=await taskManagerSnapshot(f.store,projectId);const preview=await command({action:'workflow-publish-preview',workflowId:'recipes',expectedRevision:snapshot.settingsRevisions.workflows}) as any;await command({action:'workflow-publish',workflowId:'recipes',expectedRevision:snapshot.settingsRevisions.workflows,previewDigest:preview.previewDigest});snapshot=await taskManagerSnapshot(f.store,projectId);await command({action:'workflow-assign',defaultWorkflowId:'recipes',expectedRevision:snapshot.settingsRevisions.workflows});
  const taskId=randomUUID(),sessionId='session',task={...newM2Task(projectId,taskId,'Independent task','local-user'),summary:'Bounded fixture',technicalValue:'Ownership',productValue:'Parallel workspaces',files:[{relativePath:'fixture.txt',plannedOperation:'create' as const,actualOperation:null}],acceptanceCriteria:['Observed'],estimateSeconds:30,risks:['none']};await command({action:'save',task,expectedRevision:0});await command({action:'transition',taskId,status:'ready',expectedRevision:1,reason:'Prepared'});
  const team=createTeamService(f.store),proposal={kind:'agent',action:'create',name:'Builder',description:'Fixture',content:'Bounded role',dependencies:[],reason:'Fixture'},p=await team.preview(projectId,{proposal,expectedRevision:0}),asset=await team.apply(projectId,'local-user',{proposal,expectedRevision:0,previewDigest:p.previewDigest,epoch:1,idempotencyKey:'asset'});
  await f.store.write({projectId,actorId:'test',expectedAuthorityEpoch:1,idempotencyKey:'session',changes:[{expectedRevision:0,entity:{id:sessionId,kind:'session'}}]});await gateway.runtime.dispatch('bindings',{projectId,sessionId,mode:'execution'});
  const autonomy=autonomyService(f.store),policy={...defaultAutonomyPolicy(),allowedTaskIds:[taskId],maxRuns:4},policyPreview=await autonomy.preview(projectId,policy,0);await autonomy.command(projectId,'local-user','save',{policy,previewDigest:policyPreview.previewDigest,expectedRevision:0,expectedAuthorityEpoch:1,idempotencyKey:'policy'});await autonomy.command(projectId,'local-user','resume',{expectedRevision:1,expectedAuthorityEpoch:1,idempotencyKey:'resume'});
  inputs.push({projectId,input:{taskId,transitionId:'ready-in_progress',mode:'recipe',sessionId,roleBindings:{builder:asset.assetId},expectedTaskRevision:2,reason:'Bounded queue'}});
 }
 const recipes=createRecipeService({store:f.store,port:gateway.recipeRuntime,automatic:false}),scheduler=createScheduler({store:f.store,recipes,automatic:false});f.beforeClose(async()=>{await scheduler.close();await recipes.close();await gateway.close();});await scheduler.initialized();
 for(const {projectId,input} of inputs){const p=await scheduler.preview(projectId,input);await scheduler.enqueue(projectId,{...input,previewDigest:p.previewDigest,expectedRevision:p.queueRevision,expectedAuthorityEpoch:1,idempotencyKey:'enqueue'});}
 await scheduler.tick();let states=await Promise.all(inputs.map(({projectId})=>scheduler.snapshot(projectId)));assert.equal(states.filter(s=>s.items[0].state==='running').length,4);assert.ok(states[4].items[0].waitReasons.includes('WORKSPACE_CAPACITY_EXHAUSTED'));
 await recipes.tick();const claimed=await gateway.agent('claim',auth);await gateway.agent('report',{...auth,runId:claimed.job.runId,seq:1,idempotencyKey:'done',status:'completed',text:'Observed step'});await recipes.tick();await recipes.tick();await scheduler.tick();await recipes.tick();states=await Promise.all(inputs.map(({projectId})=>scheduler.snapshot(projectId)));assert.equal(states[4].items[0].state,'running');assert.equal(states[4].items[0].executionState,'running');assert.equal((await f.store.list('q4',{kind:'run'})).length,1);
});
