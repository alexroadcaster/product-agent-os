import {test} from 'node:test';
import assert from 'node:assert/strict';
import {join} from 'node:path';
import {m2Fixture} from './m2-fixture.mts';
import {fixtureFetch,revision} from './remote-skill-fixture.mts';
import {createLocalApplication} from '../../apps/local-service/src/http/application.mts';

test('paired capability APIs keep external discovery opt-in and preserve immutable source proof',async t=>{
 const f=await m2Fixture(t),remote=fixtureFetch(true),origin='http://127.0.0.1:49837',app=await createLocalApplication({store:f.store,origin,instanceId:'g05-api',profileDirectory:join(f.root,'profile'),externalSkillFetch:remote.fetcher});f.beforeClose(()=>app.close());
 const paired=await app.handleRequest(new Request(origin+'/bootstrap/exchange',{method:'POST',headers:{host:'127.0.0.1:49837',origin,'content-type':'application/json'},body:JSON.stringify({code:app.issuePairingCode()})}));
 const cookie=paired.headers.get('set-cookie')!.split(';')[0],csrf=(await paired.json() as any).csrfToken;
 async function request(path:string,input?:unknown,auth=true){const response=await app.handleRequest(new Request(origin+'/api/v1/projects/p'+path,{method:input===undefined?'GET':'POST',headers:{host:'127.0.0.1:49837',origin,...(auth?{cookie,'x-paos-csrf':csrf}:{}),'content-type':'application/json'},...(input===undefined?{}:{body:JSON.stringify(input)})}));return {status:response.status,body:await response.json() as any};}
 assert.equal((await request('/team/skills/discovery')).status,200);assert.equal(remote.calls.length,0);
 assert.equal((await request('/team/skills/discovery?external=1',undefined,false)).status,401);assert.equal(remote.calls.length,0);
 const found=await request('/team/skills/discovery?external=1&q=verification');assert.equal(found.status,200);
 const candidateId=found.body.remote.candidates[0].id,preview=await request('/team/skills/remote-preview',{candidateId,revision});assert.equal(preview.status,200);
 assert.equal((await request('/team/skills/remote-preview',{candidateId,revision,url:'https://untrusted.invalid'})).status,400);
 const input={...preview.body,expectedRevision:0,epoch:1,idempotencyKey:'external-copy'};
 const changed=structuredClone(input);changed.proposal.content+='\nTampered';assert.equal((await request('/team/proposals/apply',changed)).status,409);
 const applied=await request('/team/proposals/apply',input);assert.equal(applied.status,200,JSON.stringify(applied.body));
 const profile=await request('/team/assets/'+applied.body.assetId);assert.equal(profile.body.source.revision,revision);assert.equal(profile.body.loadedVersion,null);assert.equal(profile.body.executionEvidence.observed,null);
 assert.equal((await request('/team/metrics?from=invalid&to=invalid')).status,400);
 const metrics=await request('/team/metrics?from=1970-01-01T00:00:00Z&to=2100-01-01T00:00:00Z&taskId=another');assert.equal(metrics.status,200);assert.deepEqual(metrics.body.runs,[]);assert.equal(metrics.body.totals.tokenCount,null);
 const history=await request('/sessions/catalog');assert.equal(history.body.source.hostHistory,'not_connected');assert.equal(history.body.source.loadedProfiles,'unavailable');
 assert.ok(remote.calls.every(url=>!url.includes('verification')));
});
