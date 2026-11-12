import {test} from 'node:test';
import assert from 'node:assert/strict';
import {join} from 'node:path';
import {m2Fixture} from './m2-fixture.mts';
import {createLocalApplication} from '../../apps/local-service/src/http/application.mts';
import {mkdir,writeFile,readFile,symlink,link,unlink} from 'node:fs/promises';
import {createAppAgentGateway} from '../../apps/local-service/src/runtime/app-agent-gateway.mts';
import {createTeamService} from '../../apps/local-service/src/team/service.mts';
async function paired(f:Awaited<ReturnType<typeof m2Fixture>>,runtime?:any){
 const origin='http://127.0.0.1:49831',app=await createLocalApplication({store:f.store,origin,instanceId:'sessions-team',profileDirectory:join(f.root,'profile'),runtime});
 const response=await app.handleRequest(new Request(origin+'/bootstrap/exchange',{method:'POST',headers:{host:'127.0.0.1:49831',origin,'content-type':'application/json'},body:JSON.stringify({code:app.issuePairingCode()})}));
 const cookie=response.headers.get('set-cookie')!.split(';')[0],csrf=(await response.json() as any).csrfToken;
 return async(path:string,input?:unknown)=>{const response=await app.handleRequest(new Request(origin+'/api/v1/projects/p'+path,{method:input===undefined?'GET':'POST',headers:{host:'127.0.0.1:49831',origin,cookie,'x-paos-csrf':csrf,'content-type':'application/json'},...(input===undefined?{}:{body:JSON.stringify(input)})}));return {status:response.status,body:await response.json() as any};};
}
test('session catalog snapshot survives insertion and transcript anchors reach full history',async t=>{
 const f=await m2Fixture(t),request=await paired(f);
 for(let i=0;i<3;i++)await f.store.write({projectId:'p',actorId:'test',expectedAuthorityEpoch:1,idempotencyKey:`s${i}`,changes:[{expectedRevision:0,entity:{id:`s${i}`,kind:'session',title:`Session ${i}`}}]});
 const first=await request('/sessions/catalog?limit=2');assert.equal(first.status,200);assert.equal(first.body.items.length,2);
 await f.store.write({projectId:'p',actorId:'test',expectedAuthorityEpoch:1,idempotencyKey:'new',changes:[{expectedRevision:0,entity:{id:'new',kind:'session'}}]});
 const last=await request('/sessions/catalog?limit=2&cursor='+encodeURIComponent(first.body.nextCursor));assert.equal(last.status,200);
 assert.equal(new Set([...first.body.items,...last.body.items].map(x=>x.id)).size,3);assert.equal(last.body.snapshot.total,3);
 for(let i=0;i<120;i++)await f.store.write({projectId:'p',actorId:'test',expectedAuthorityEpoch:1,idempotencyKey:`m${i}`,changes:[{expectedRevision:0,entity:{id:`m${i}`,kind:'message',parentId:'s0',body:`Message ${i}`,data:{role:'user'}}}]});
 const anchor=await request('/sessions/s0/transcript?anchor=m110&limit=10');assert.equal(anchor.status,200);assert.equal(anchor.body.anchorFound,true);assert.ok(anchor.body.items.some(x=>x.id==='m110'));
});
test('skill import keeps binary resources and origin, rejects sensitive files and restores original bytes',async t=>{
 const f=await m2Fixture(t),request=await paired(f),folder=join(f.root,'.agents','skills','review');await mkdir(folder,{recursive:true});const content='---\nname: Review\ndescription: Review source\nlicense: MIT\n---\nUse references/data.bin';await writeFile(join(folder,'SKILL.md'),content);const original=Buffer.from([0,1,2,3,255]);await writeFile(join(folder,'data.bin'),original);
 const preview=await request('/team/skills/source-preview',{sourceRootId:'project-skills-agents',relativePath:'review'});assert.equal(preview.status,200);assert.equal(preview.body.candidate.source.license,'MIT');assert.equal(preview.body.proposal.resources.length,1);
 const input={...preview.body,expectedRevision:0,epoch:1,idempotencyKey:'copy-skill'};const applied=await request('/team/proposals/apply',input);assert.equal(applied.status,200,JSON.stringify(applied.body));assert.deepEqual(await request('/team/proposals/apply',input),applied);
 assert.equal(await readFile(join(folder,'SKILL.md'),'utf8'),content);assert.deepEqual(await readFile(join(folder,'data.bin')),original);
 const profile=(await request('/team/assets/'+applied.body.assetId)).body;const service=createTeamService(f.store);assert.deepEqual(Buffer.from((await service.resource('p',profile.id,'data.bin')).bytes),original);
 const changed={assetId:profile.id,kind:'skill',action:'update',name:profile.name,description:profile.description,content:profile.content+'\nUpdated',dependencies:[],resources:[],reason:'Edit copy'};
 let plan=(await request('/team/proposals/preview',{proposal:changed,expectedRevision:1})).body;assert.equal((await request('/team/proposals/apply',{...plan,expectedRevision:1,epoch:1,idempotencyKey:'edit-skill'})).status,200);
 plan=(await request('/team/proposals/preview',{proposal:{...changed,action:'restore',restoreVersion:1},expectedRevision:2})).body;assert.equal((await request('/team/proposals/apply',{...plan,expectedRevision:2,epoch:1,idempotencyKey:'restore-skill'})).status,200);assert.deepEqual(Buffer.from((await service.resource('p',profile.id,'data.bin')).bytes),original);
 await writeFile(join(folder,'.env'),'api_key=neverPersistSyntheticCredential');const bad=await request('/team/skills/source-preview',{sourceRootId:'project-skills-agents',relativePath:'review'});assert.equal(bad.status,400);assert.equal(bad.body.error.code,'SENSITIVE_ASSET_RESOURCE');
 const escape=await request('/team/skills/source-preview',{sourceRootId:'project-skills-agents',relativePath:'../../outside'});assert.equal(escape.status,400);
});
test('App planning generation is correlated, redacted and read-only until explicit proposal apply',async t=>{
 const f=await m2Fixture(t);await f.store.write({projectId:'p',actorId:'test',expectedAuthorityEpoch:1,idempotencyKey:'session',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 const gateway=createAppAgentGateway({store:f.store,profileId:'team-test',actorId:'app'});f.beforeClose(()=>gateway.close());await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'worker',generation:'g'});const auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};const binding=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'planning'}),request=await paired(f,gateway.runtime);
 const start=await request('/team/generation',{sessionId:'s',bindingId:binding.bindingId,description:'Create reviewer. api_key=notForModelSyntheticCanary'});assert.equal(start.status,200);const claim=await gateway.agent('claim',auth);assert.equal(claim.job.purpose,'team_proposal');assert.equal(JSON.stringify(claim).includes('notForModelSyntheticCanary'),false);assert.equal(JSON.stringify(await f.store.get('p',start.body.runId)).includes('notForModelSyntheticCanary'),false);
 const proposal={kind:'agent',action:'create',name:'Generated reviewer',description:'Review source',content:'Read source and report findings.',dependencies:[],reason:'Project need'};
 await gateway.agent('report',{...auth,runId:start.body.runId,seq:1,idempotencyKey:'proposal-final',status:'completed',text:JSON.stringify(proposal)});
 const result=await request('/team/generation/'+start.body.id);assert.equal(result.body.proposal.name,proposal.name);assert.equal((await request('/team/catalog')).body.assets.filter(a=>a.management==='paos_managed').length,0);
 const metrics=await request('/team/metrics?from=1970-01-01T00:00:00.000Z&to=2100-01-01T00:00:00.000Z');assert.equal(metrics.body.denominator,1);
 assert.equal((await request('/team/proposals/apply',{...result.body.preview,expectedRevision:0,epoch:1,idempotencyKey:'accept-generation'})).status,200);
 assert.equal(JSON.stringify(await f.store.events('p')).includes('notForModelSyntheticCanary'),false);
});
test('message secrets are removed before persistence and indexing',async t=>{
 const f=await m2Fixture(t);await f.store.write({projectId:'p',actorId:'test',expectedAuthorityEpoch:1,idempotencyKey:'secret',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}},{expectedRevision:0,entity:{id:'m',kind:'message',parentId:'s',body:'api_key=syntheticCredentialCanaryXYZ',data:{role:'user'}}}]});
 assert.equal(JSON.stringify(await f.store.get('p','m')).includes('syntheticCredentialCanaryXYZ'),false);
 assert.equal((await f.store.search('p',{query:'syntheticCredentialCanaryXYZ'})).items.length,0);
});
test('managed team proposals have preview CAS, immutable history and raw-write protection',async t=>{
 const f=await m2Fixture(t),request=await paired(f),proposal={kind:'agent',action:'create',name:'Reviewer',description:'Review',content:'Inspect source carefully',dependencies:[],reason:'Project team'};
 const preview=await request('/team/proposals/preview',{proposal,expectedRevision:0});assert.equal(preview.status,200);
 const apply=await request('/team/proposals/apply',{...preview.body,expectedRevision:0,epoch:1,idempotencyKey:'agent-create'});assert.equal(apply.status,200);
 const profile=await request('/team/assets/'+apply.body.assetId);assert.equal(profile.body.content,proposal.content);assert.equal(profile.body.effectiveVersion,1);assert.equal(profile.body.loadedVersion,null);
 const before=await f.store.get('p','m2b-team-assets');assert.ok(before);
 await assert.rejects(()=>f.store.write({projectId:'p',actorId:'local-user',expectedAuthorityEpoch:1,idempotencyKey:'forged',changes:[{expectedRevision:before!.revision,entity:{id:before!.id,kind:'session',data:{}}}]}),{code:'TEAM_MANAGED_WRITE_FORBIDDEN'});
 const updated={...proposal,assetId:apply.body.assetId,action:'update',content:'Updated instructions'};
 const next=await request('/team/proposals/preview',{proposal:updated,expectedRevision:1});assert.equal(next.status,200);
 const changed=await request('/team/proposals/apply',{...next.body,expectedRevision:1,epoch:1,idempotencyKey:'agent-update'});assert.equal(changed.status,200);
 const stale=await request('/team/proposals/apply',{...next.body,expectedRevision:1,epoch:1,idempotencyKey:'stale-update'});assert.equal(stale.status,409);
 const history=await request('/team/assets/'+apply.body.assetId+'/history');assert.equal(history.body.versions.length,2);assert.equal(history.body.versions[0].content,proposal.content);
});
test('managed execution pins stay immutable across profile updates and queued runs do not inflate starts',async t=>{
 const f=await m2Fixture(t),team=createTeamService(f.store),proposal={kind:'agent',action:'create',name:'Builder',description:'Build',content:'Original instructions',dependencies:[],reason:'Team'};
 const preview=await team.preview('p',{proposal,expectedRevision:0}),created=await team.apply('p','local-user',{...preview,expectedRevision:0,epoch:1,idempotencyKey:'builder'});
 const task=await f.ready('Execute',{agentAssignments:[created.assetId]});await f.store.write({projectId:'p',actorId:'test',expectedAuthorityEpoch:1,idempotencyKey:'session',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 const gateway=createAppAgentGateway({store:f.store,profileId:'pins',actorId:'app',executorFactory:async binding=>({metadata:{nativeSandbox:true,scope:'paos_mediated_commands',workspaceRoot:binding.workspaceRoot,mode:binding.mode},execute:async()=>({exitCode:0,stdout:'',stderr:''}),interrupt:async()=>{},close:async()=>{}}) as any});f.beforeClose(()=>gateway.close());await gateway.connection.connect({});const worker=await gateway.agent('attach',{hostIdentity:'codex_app',workerId:'w',generation:'g'}),auth={workerId:worker.workerId,generation:worker.generation,leaseToken:worker.leaseToken};const binding=await gateway.runtime.dispatch('bindings',{projectId:'p',sessionId:'s',mode:'execution'});
 const run=await gateway.runtime.dispatch('send',{projectId:'p',sessionId:'s',bindingId:binding.bindingId,clientMessageId:'run',input:'Execute bounded fixture',taskId:task.id});
 const before=await team.metrics('p','1970-01-01T00:00:00.000Z','2100-01-01T00:00:00.000Z');assert.equal(before.denominator,0);
 const claimed=await gateway.agent('claim',auth);assert.equal(claimed.job.assetPins[0].version,1);assert.equal(claimed.job.assetPins[0].content,'Original instructions');assert.equal(claimed.job.assetPins[0].observedModel,null);
 const updated=await team.preview('p',{proposal:{...proposal,action:'update',assetId:created.assetId,content:'New instructions'},expectedRevision:1});assert.deepEqual(updated.dependencyImpact.activeRunIds,[run.id]);await team.apply('p','local-user',{...updated,expectedRevision:1,epoch:1,idempotencyKey:'builder-v2'});
 assert.equal((await gateway.agent('claim',auth)).job.assetPins[0].content,'Original instructions');const profile=await team.profile('p',created.assetId);assert.equal(profile.effectiveVersion,2);assert.equal(profile.observedPins![0].version,1);
 const metrics=await team.metrics('p','1970-01-01T00:00:00.000Z','2100-01-01T00:00:00.000Z');assert.equal(metrics.denominator,1);assert.equal(metrics.agents[0].startedRuns,1);assert.equal(metrics.agents[0].durationSeconds,null);
 await assert.rejects(()=>team.preview('p',{proposal:{...proposal,action:'delete',assetId:created.assetId},expectedRevision:2}),{code:'ASSET_DEPENDENCY_CONFLICT'});
 await gateway.agent('report',{...auth,runId:run.id,seq:1,idempotencyKey:'done',status:'completed',text:'Observed fixture result'});
});
test('semantic hidden messages are rejected and project search never leaks another project',async t=>{
 const f=await m2Fixture(t),request=await paired(f);await f.store.write({projectId:'p',actorId:'test',expectedAuthorityEpoch:1,idempotencyKey:'session',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}}]});
 await assert.rejects(()=>f.store.write({projectId:'p',actorId:'test',expectedAuthorityEpoch:1,idempotencyKey:'hidden',changes:[{expectedRevision:0,entity:{id:'hidden',kind:'message',parentId:'s',body:'Never exposed hidden fixture',data:{role:'reasoning'}}}]}),{code:'HIDDEN_MESSAGE_FORBIDDEN'});
 await f.store.registerProject({id:'q',keyPrefix:'QQQQ',canonicalRoot:f.root+'-other',rootIdentity:'other',authorityMode:'sql'});await f.store.write({projectId:'q',actorId:'test',expectedAuthorityEpoch:1,idempotencyKey:'other',changes:[{expectedRevision:0,entity:{id:'other-session',kind:'session'}},{expectedRevision:0,entity:{id:'other-message',kind:'message',parentId:'other-session',body:'CrossProjectCanary'}}]});
 const result=await request('/sessions/search?q=CrossProjectCanary');assert.equal(result.status,200);assert.equal(result.body.items.length,0);assert.equal((await f.store.search('p',{query:'CrossProjectCanary'})).items.length,0);
});
test('source preview rejects hardlinks, directory escapes and credential content before managed persistence',async t=>{
 const f=await m2Fixture(t),request=await paired(f),folder=join(f.root,'.agents','skills','unsafe');await mkdir(folder,{recursive:true});await writeFile(join(folder,'SKILL.md'),'---\nname: Unsafe\ndescription: Test\n---\nTest');await writeFile(join(f.root,'outside.txt'),'Outside fixture');
 try{await link(join(f.root,'outside.txt'),join(folder,'hardlink.txt'));}catch(error){if((error as any).code==='EPERM'){t.skip('Native hardlink fixture denied; requires native qualification');return;}throw error;}
 let response=await request('/team/skills/source-preview',{sourceRootId:'project-skills-agents',relativePath:'unsafe'});assert.equal(response.body.error.code,'LINKED_ASSET_SOURCE');await unlink(join(folder,'hardlink.txt'));
 await writeFile(join(folder,'credentials.json'),'The path itself is sensitive');response=await request('/team/skills/source-preview',{sourceRootId:'project-skills-agents',relativePath:'unsafe'});assert.equal(response.body.error.code,'SENSITIVE_ASSET_RESOURCE');await unlink(join(folder,'credentials.json'));
 await writeFile(join(folder,'safe-name.json'),'{"api_key":"SyntheticResourceCredentialCanary"}');response=await request('/team/skills/source-preview',{sourceRootId:'project-skills-agents',relativePath:'unsafe'});assert.equal(response.body.error.code,'SENSITIVE_ASSET_CONTENT');await unlink(join(folder,'safe-name.json'));
 await mkdir(join(f.root,'outside'));try{await symlink(join(f.root,'outside'),join(folder,'escape'),'junction');}catch(error){if((error as any).code==='EPERM'){t.skip('Native junction fixture denied; requires native qualification');return;}throw error;}
 response=await request('/team/skills/source-preview',{sourceRootId:'project-skills-agents',relativePath:'unsafe'});assert.equal(response.body.error.code,'LINKED_ASSET_SOURCE');assert.equal(await f.store.get('p','m2b-team-assets'),null);
});
