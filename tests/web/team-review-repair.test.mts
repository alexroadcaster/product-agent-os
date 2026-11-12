import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdir,rename} from 'node:fs/promises';
import {join,resolve,dirname} from 'node:path';
import {m2Fixture} from './m2-fixture.mts';
import {createTeamService} from '../../apps/local-service/src/team/service.mts';
import {previewAsset,applyAsset} from '../../apps/local-service/src/team/contract.mts';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {defaultRegistry} from '../../apps/local-service/src/workflows/registry.mts';
import {taskManagerSnapshot} from '../../apps/local-service/src/task-manager/service.mts';
const base={kind:'skill' as const,action:'create' as const,name:'Skill',description:'Description',content:'Instructions',dependencies:[] as string[],reason:'Review test'};
function create(registry:any,proposal:any){return applyAsset(registry,previewAsset(registry,proposal,0,[]),'test');}
test('restore validates restored deleted/archived dependencies and restored cycles, ignoring decoy input',()=>{
 for(const state of ['deleted','archived','cycle']){
  let registry:any={category:'team_registry',assets:[]};let a=create(registry,{...base,assetId:'dep'});registry=a.registry;a=create(registry,{...base,assetId:'owner',dependencies:['dep']});registry=a.registry;
  const update={...base,assetId:'owner',action:'update',dependencies:[]};registry=applyAsset(registry,previewAsset(registry,update,1,[]),'test').registry;
  if(state==='cycle')registry.assets.find((a:any)=>a.id==='dep').dependencies=['owner'];else registry.assets.find((a:any)=>a.id==='dep')[state]=true;
  assert.throws(()=>previewAsset(registry,{...update,action:'restore',restoreVersion:1},2,[]),{code:state==='cycle'?'ASSET_DEPENDENCY_CYCLE':'ASSET_DEPENDENCY_UNAVAILABLE'});
 }
});
test('atomic restore rejects dependency changes after preview even with decoy dependencies',async t=>{
 const f=await m2Fixture(t),team=createTeamService(f.store);let seq=0;
 const apply=async(proposal:any,expectedRevision:number)=>{const preview=await team.preview('p',{proposal,expectedRevision});return team.apply('p','test',{...preview,expectedRevision,epoch:1,idempotencyKey:`repair-${++seq}`});};
 for(const state of ['delete','archive','cycle']){
  const dep=await apply({...base,name:'Dep '+state},0),owner=await apply({...base,name:'Owner '+state,dependencies:[dep.assetId]},0);await apply({...base,action:'update',assetId:owner.assetId,dependencies:[]},1);
  const restore={...base,assetId:owner.assetId,action:'restore',restoreVersion:1,dependencies:[]};const valid=await team.preview('p',{proposal:restore,expectedRevision:2});
  await apply({...base,assetId:dep.assetId,action:state==='cycle'?'update':state,dependencies:state==='cycle'?[owner.assetId]:[]},1);
  const before=await f.store.get('p','m2b-team-assets'),events=await f.store.audit('p');await assert.rejects(()=>f.store.teamApply({projectId:'p',actorId:'test',epoch:1,idempotencyKey:`unsafe-restore-${state}`,proposal:restore,previewDigest:valid.previewDigest,expectedRevision:2}),{code:state==='cycle'?'ASSET_DEPENDENCY_CYCLE':'ASSET_DEPENDENCY_UNAVAILABLE'});assert.deepEqual(await f.store.get('p','m2b-team-assets'),before);assert.deepEqual(await f.store.audit('p'),events);
 }
});
test('proposal diff exposes metadata and resource changes without embedding binary bytes',()=>{
 const bytes=Buffer.from('fixture'),resource={path:'reference.txt',hash:'afake',byteSize:bytes.length,blobId:'blob'};let registry:any={category:'team_registry',assets:[]};registry=create(registry,{...base,assetId:'dep'}).registry;registry=create(registry,{...base,assetId:'owner'}).registry;
 const preview=previewAsset(registry,{...base,action:'update',assetId:'owner',name:'Renamed',description:'New description',dependencies:['dep'],resources:[resource]},1,[]);
 assert.notEqual(preview.diff.before,preview.diff.after);for(const text of ['Renamed','New description','reference.txt','afake','dep'])assert.ok(preview.diff.after.includes(text));assert.equal(preview.diff.after.includes('base64'),false);
});
test('replaced project roots deny service discovery and atomic team apply without persistence',async t=>{
 const f=await m2Fixture(t),original=join(f.root,'source-root'),moved=join(f.root,'old-source-root');await mkdir(original);const pin=await bindProject('q',original);await f.store.registerProject({id:'q',keyPrefix:'QQQQ',canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'sql'});const team=createTeamService(f.store),preview=await team.preview('q',{proposal:base,expectedRevision:0});
 assert.equal(dirname(resolve(original)),resolve(f.root));assert.equal(dirname(resolve(moved)),resolve(f.root));await rename(original,moved);await mkdir(original);
 await assert.rejects(()=>team.catalog('q'),{code:'PROJECT_ROOT_UNAVAILABLE'});await assert.rejects(()=>f.store.teamApply({projectId:'q',actorId:'test',epoch:1,idempotencyKey:'root-replaced',expectedRevision:0,...preview}),{code:'PROJECT_ROOT_UNAVAILABLE'});assert.equal(await f.store.get('q','m2b-team-assets'),null);
});
test('agent accepted task metrics use custom workflow categories from task profiles',async t=>{
 const f=await m2Fixture(t),team=createTeamService(f.store),preview=await team.preview('p',{proposal:{...base,kind:'agent'},expectedRevision:0}),agent=await team.apply('p','test',{...preview,expectedRevision:0,epoch:1,idempotencyKey:'metric-agent'});
 let snapshot=await taskManagerSnapshot(f.store,'p');await f.command({action:'board',expectedRevision:snapshot.settingsRevisions.board,board:{...snapshot.board,outOfBoard:true}});const d=structuredClone(defaultRegistry().workflows[0].versions[0].definition);d.states=d.states.map(s=>({...s,id:'metric_'+s.id}));d.transitions=d.transitions.map(s=>({...s,from:'metric_'+s.from,to:'metric_'+s.to}));snapshot=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-save-draft',workflowId:'metrics',definition:d,expectedRevision:snapshot.settingsRevisions.workflows});snapshot=await taskManagerSnapshot(f.store,'p');const published=await f.command({action:'workflow-publish-preview',workflowId:'metrics',expectedRevision:snapshot.settingsRevisions.workflows}) as any;await f.command({action:'workflow-publish',workflowId:'metrics',expectedRevision:snapshot.settingsRevisions.workflows,previewDigest:published.previewDigest});snapshot=await taskManagerSnapshot(f.store,'p');await f.command({action:'workflow-assign',defaultWorkflowId:'metrics',expectedRevision:snapshot.settingsRevisions.workflows});const task=await f.create('Accepted custom',{acceptanceCriteria:['Verified']});await f.command({action:'transition',taskId:task.id,expectedRevision:task.revision,status:'metric_done',manual:true,reason:'Verified',evidence:[{criterion:'Verified',evidence:'Observed',outcome:'passed'}]});
 await f.store.write({projectId:'p',actorId:'test',expectedAuthorityEpoch:1,idempotencyKey:'observed-run',changes:[{expectedRevision:0,entity:{id:'observed-run',kind:'run',status:'completed',data:{appAgentRun:{id:'observed-run',sessionId:'s',observedStartedAt:'2026-11-12T00:00:00.000Z',taskContext:{taskId:task.id},assetPins:await team.assignmentPins('p',[agent.assetId])}}}}]});const metrics=await team.metrics('p','2026-11-01T00:00:00.000Z','2026-12-01T00:00:00.000Z');assert.equal(metrics.agents[0].outcomes.acceptedTasks,1);
});
