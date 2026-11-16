import {test} from 'node:test';
import assert from 'node:assert/strict';
import {m2Fixture} from './m2-fixture.mts';
import {createTeamService} from '../../apps/local-service/src/team/service.mts';
import {fixtureFetch,revision} from './remote-skill-fixture.mts';
test('remote failures and unsafe Git entries preserve the local catalog without fetching executable content',async t=>{
 const f=await m2Fixture(t),fs=await import('node:fs/promises'),path=await import('node:path');await fs.mkdir(path.join(f.root,'.agents/skills/local'),{recursive:true});await fs.writeFile(path.join(f.root,'.agents/skills/local/SKILL.md'),'---\nname: Local fixture\ndescription: Available offline\n---\nLocal');
 for(const mode of ['truncated','symlink','rate-limit','blob-drift'] as const){const remote=fixtureFetch(),tree=remote.data.get('git/trees/'+'3'.repeat(40)+'?recursive=1') as any;if(mode==='truncated')tree.truncated=true;if(mode==='symlink')tree.tree.find((e:any)=>e.path.endsWith('/SKILL.md')).mode='120000';const fetcher:typeof fetch=async(url,init)=>mode==='rate-limit'?new Response('{}',{status:429}):mode==='blob-drift'&&String(url).includes('/git/blobs/')?new Response(JSON.stringify({sha:String(url).split('/').at(-1),size:1,encoding:'base64',content:'eA=='})):remote.fetcher(url,init);const team=createTeamService(f.store,[],{externalFetch:fetcher});const local=await team.discovery('p','');assert.ok(local.candidates.some(c=>c.name==='Local fixture'));assert.equal(remote.calls.length,0);const result=await team.discovery('p','',{external:true});assert.ok(result.candidates.some(c=>c.name==='Local fixture'));if(mode==='symlink'){assert.equal(result.remote.availability,'available');assert.equal(result.remote.candidates[0].importable,false);await assert.rejects(team.remotePreview('p',{candidateId:result.remote.candidates[0].id,revision}),{code:'REMOTE_RESOURCE_UNSUPPORTED'});}else assert.equal(result.remote.availability,'unavailable');}
});
test('native interface metadata is copied as opaque text without activating host agents',async t=>{
 const f=await m2Fixture(t),remote=fixtureFetch(true),team=createTeamService(f.store,[],{externalFetch:remote.fetcher} as any),found=await team.discovery('p','verification',{external:true});
 assert.equal(found.remote.candidates[0].importable,true);
 const plan=await team.remotePreview('p',{candidateId:found.remote.candidates[0].id,revision});assert.ok(plan.proposal.resources.some(r=>r.path==='agents/openai.yaml'));
 const applied=await team.apply('p','fixture',{...plan,epoch:1,expectedRevision:0,idempotencyKey:'opaque-metadata'});const profile=await team.profile('p',applied.assetId);assert.equal(profile.loadedVersion,null);
 assert.match(Buffer.from((await team.resource('p',applied.assetId,'agents/openai.yaml')).bytes).toString('utf8'),/Synthetic skill/);
});
test('explicit external discovery keeps query local and previews a licensed immutable managed copy',async t=>{
 const f=await m2Fixture(t),remote=fixtureFetch(),team=createTeamService(f.store,[],{externalFetch:remote.fetcher} as any);
 const found=await team.discovery('p','verification',{external:true});
 assert.equal(found.remote.availability,'available');assert.equal(found.remote.candidates.length,1);assert.equal(found.remote.source.revision,revision);
 const plan=await team.remotePreview('p',{candidateId:found.remote.candidates[0].id,revision});
 assert.equal(plan.proposal.resources.length,2);assert.ok(plan.proposal.resources.some(r=>r.path==='guide.md'));assert.ok(plan.proposal.resources.some(r=>r.path==='LICENSE.source.txt'));
 const applied=await team.apply('p','fixture',{...plan,expectedRevision:0,epoch:1,idempotencyKey:'remote-copy'}),asset=await team.profile('p',applied.assetId);
 assert.equal(asset.source?.origin,'github_public_readonly');assert.equal(asset.source?.license,'MIT');assert.equal(asset.loadedVersion,null);
 await team.discovery('p','private-query-canary',{external:true});assert.ok(remote.calls.every(url=>!url.includes('private-query-canary')));
 const changed=structuredClone(plan);changed.proposal.content+='tampered';await assert.rejects(team.apply('p','fixture',{...changed,expectedRevision:0,epoch:1,idempotencyKey:'tampered'}),{code:'REMOTE_SOURCE_DRIFT'});
});
