import {test} from 'node:test';
import assert from 'node:assert/strict';
import {randomUUID,createHash} from 'node:crypto';
import {mkdir,writeFile,unlink} from 'node:fs/promises';
import {join} from 'node:path';
import {m2Fixture} from './m2-fixture.mts';
import {createTeamService} from '../../apps/local-service/src/team/service.mts';
import {resolveRecipePins} from '../../apps/local-service/src/execution-recipes/pins.mts';
import type {WorkflowRecipe} from '../../packages/contracts/workflows/workflow.ts';
const step=(extra:Partial<WorkflowRecipe['steps'][number]>={}):WorkflowRecipe['steps'][number]=>({id:'build',role:'builder',profileVersion:'1',skills:[],skillVersions:{},inputArtifacts:[],outputArtifacts:[],checks:[],ownership:[],timeoutSeconds:60,retryBudget:0,iterationBudget:1,...extra});
async function asset(team:ReturnType<typeof createTeamService>,changes:Record<string,unknown>={},revision=0){const proposal={kind:'agent',action:'create',name:'Builder',description:'Build fixture',content:'Original instructions',dependencies:[],reason:'Fixture',...changes};const preview=await team.preview('p',{proposal,expectedRevision:revision});return team.apply('p','local-user',{...preview,expectedRevision:revision,epoch:1,idempotencyKey:randomUUID()});}
test('recipe exact managed pin preserves historical content and frozen result after newer update',async t=>{
 const f=await m2Fixture(t),team=createTeamService(f.store),a=await asset(team);
 await asset(team,{action:'update',assetId:a.assetId,content:'New instructions'},1);
 const result=await resolveRecipePins(f.store,'p',[step({profileVersion:'v1'})],{builder:a.assetId});
 assert.equal(result.build[0].content,'Original instructions');assert.equal(result.build[0].version,1);assert.equal(result.build[0].observedModel,null);
 assert.ok(Object.isFrozen(result));assert.ok(Object.isFrozen(result.build));assert.ok(Object.isFrozen(result.build[0]));
});
test('recipe bindings and exact versions fail closed',async t=>{
 const f=await m2Fixture(t),team=createTeamService(f.store),a=await asset(team);
 await assert.rejects(()=>resolveRecipePins(f.store,'p',[step()],{}),{code:'RECIPE_ROLE_BINDING_REQUIRED'});
 await assert.rejects(()=>resolveRecipePins(f.store,'p',[step()],{builder:[a.assetId,a.assetId]} as any),{code:'RECIPE_ROLE_BINDING_REQUIRED'});
 await assert.rejects(()=>resolveRecipePins(f.store,'p',[step()],{builder:'missing'}));
 await assert.rejects(()=>resolveRecipePins(f.store,'p',[step({profileVersion:'99'})],{builder:a.assetId}),{code:'RECIPE_ASSET_VERSION_UNAVAILABLE'});
 await assert.rejects(()=>resolveRecipePins(f.store,'p',[step(),step({id:'other',profileVersion:'2'})],{builder:a.assetId}),{code:'RECIPE_ASSET_VERSION_CONFLICT'});
});
test('source hash pins preserve full skill ID and binary resources, reject content drift',async t=>{
 const f=await m2Fixture(t),team=createTeamService(f.store),a=await asset(team),folder=join(f.root,'.agents','skills','review');await mkdir(folder,{recursive:true});
 const content='---\nname: Review\ndescription: Fixture review\n---\nReview fixture';await writeFile(join(folder,'SKILL.md'),content);await writeFile(join(folder,'data.bin'),Buffer.from([0,1,255]));
 const id='source:project-skills-agents:review',hash=createHash('sha256').update(content).digest('hex'),s=step({skills:[id],skillVersions:{[id]:hash}});
 const result=await resolveRecipePins(f.store,'p',[s],{builder:a.assetId});const pin=result.build.find(p=>p.assetId===id)!;
 assert.deepEqual(Buffer.from(pin.resources![0].base64!,'base64'),Buffer.from([0,1,255]));assert.equal(pin.hash,hash);
 await writeFile(join(folder,'SKILL.md'),content+'\nChanged');await assert.rejects(()=>resolveRecipePins(f.store,'p',[s],{builder:a.assetId}),{code:'RECIPE_ASSET_VERSION_UNAVAILABLE'});
});
test('historical dependency closure detects cycles and missing dependencies',async t=>{
 const f=await m2Fixture(t),team=createTeamService(f.store),a=await asset(team),b=await asset(team,{kind:'skill',name:'Dependency',dependencies:[a.assetId]});
 await asset(team,{kind:'skill',action:'update',assetId:b.assetId,dependencies:[]},1);
 await asset(team,{action:'update',assetId:a.assetId,dependencies:[b.assetId]},1);
 await assert.rejects(()=>resolveRecipePins(f.store,'p',[step({profileVersion:'2',skills:[b.assetId],skillVersions:{[b.assetId]:'1'}})],{builder:a.assetId}),{code:'ASSET_DEPENDENCY_CYCLE'});
 // A historical dependency can become unavailable after its owner archives it.
 const c=await asset(team,{name:'Independent'});await asset(team,{action:'archive',assetId:c.assetId},1);
 await assert.rejects(()=>resolveRecipePins(f.store,'p',[step()],{builder:c.assetId}),{code:'ASSET_ASSIGNMENT_UNAVAILABLE'});
});
test('managed historical skill pins materialize blob resources and retain dependency closure',async t=>{
 const f=await m2Fixture(t),team=createTeamService(f.store),raw=Buffer.from([4,0,255]),resource={path:'data.bin',hash:createHash('sha256').update(raw).digest('hex'),byteSize:raw.length,base64:raw.toString('base64')};
 const skill=await asset(team,{kind:'skill',resources:[resource]}),a=await asset(team,{dependencies:[skill.assetId]});
 await asset(team,{kind:'skill',action:'update',assetId:skill.assetId,content:'Updated skill',resources:[]},1);
 const pins=(await resolveRecipePins(f.store,'p',[step({skills:[skill.assetId],skillVersions:{[skill.assetId]:'v1'}})],{builder:a.assetId})).build;
 assert.equal(pins.length,2);assert.deepEqual(Buffer.from(pins[1].resources![0].base64!,'base64'),raw);assert.equal(pins[1].version,1);
 const current=(await resolveRecipePins(f.store,'p',[step()],{builder:a.assetId})).build;
 assert.equal(current[1].version,2);assert.equal(current[1].content,'Updated skill');
});
test('unavailable dependency never disappears from a resolved recipe',async t=>{
 const f=await m2Fixture(t),team=createTeamService(f.store),folder=join(f.root,'.agents','skills','dependency');await mkdir(folder,{recursive:true});
 await writeFile(join(folder,'SKILL.md'),'---\nname: Dependency\ndescription: Fixture\n---\nFixture');
 const a=await asset(team,{dependencies:['source:project-skills-agents:dependency']});await unlink(join(folder,'SKILL.md'));
 await assert.rejects(()=>resolveRecipePins(f.store,'p',[step()],{builder:a.assetId}));
});
