import assert from 'node:assert/strict';
import {test} from 'node:test';
import {randomUUID} from 'node:crypto';
import {join} from 'node:path';
import {m2Fixture} from './m2-fixture.mts';
import {createLocalApplication} from '../../apps/local-service/src/http/application.mts';
import {defaultAutonomyPolicy,decodeAutonomyPolicy} from '../../packages/contracts/autonomy/policy.ts';

async function fixture(t:Parameters<typeof m2Fixture>[0]) {
  const f=await m2Fixture(t),origin='http://127.0.0.1:43127';
  const app=await createLocalApplication({store:f.store,origin,instanceId:'autonomy-fixture',profileDirectory:join(f.root,'profile')});
  let cookie='',csrf='';
  async function request(path:string,payload?:unknown){return app.handleRequest(new Request(origin+'/api/v1'+path,{
    method:payload===undefined?'GET':'POST',headers:{host:'127.0.0.1:43127',origin,cookie,'content-type':'application/json','x-paos-csrf':csrf},
    ...(payload===undefined?{}:{body:JSON.stringify(payload)})}));}
  const paired=await request('/bootstrap/exchange',{code:app.issuePairingCode()});cookie=paired.headers.get('set-cookie')!.split(';')[0];csrf=(await paired.json()).csrfToken;
  const read=async()=>{const r=await request('/projects/p/autonomy');assert.equal(r.status,200);return r.json();};
  const command=async(action:string,extra:Record<string,unknown>={})=>request('/projects/p/autonomy/'+action,{expectedRevision:(await read()).revision,expectedAuthorityEpoch:1,idempotencyKey:randomUUID(),...extra});
  return {...f,request,read,command};
}

test('policy preview exposes enforceable boundaries without changing permissions or starting work',async t=>{
  const f=await fixture(t),policy={...defaultAutonomyPolicy(),allowedTaskIds:['selected-task']};
  const r=await f.request('/projects/p/autonomy/preview',{policy,expectedRevision:0});
  assert.equal(r.status,200,JSON.stringify(await r.clone().json()));const preview=await r.json();
  assert.equal(preview.boundaries.hostPermissionsChanged,false);assert.equal(preview.boundaries.nativeApprovalRequired,true);
  assert.equal(preview.executable,true);assert.equal((await f.read()).policy,null);
  assert.equal((await f.store.list('p',{kind:'run'})).length,0);
});

test('rejects malformed/unsupported limits and reports narrow paths as unavailable',async t=>{
  const f=await fixture(t),policy=defaultAutonomyPolicy();
  for(const patch of [{maxRuns:NaN},{maxRunSeconds:0},{maxTokens:100},{concurrency:2},{allowedPaths:['../escape']},{allowedPaths:['C:/private']},{allowedActions:['deploy']}]){
    assert.throws(()=>decodeAutonomyPolicy({...policy,...patch}));
    assert.equal((await f.request('/projects/p/autonomy/preview',{policy:{...policy,...patch},expectedRevision:0})).status,400);
  }
  const narrow=await (await f.request('/projects/p/autonomy/preview',{policy:{...policy,allowedPaths:['src']},expectedRevision:0})).json();
  assert.equal(narrow.executable,false);assert.ok(narrow.reasons.includes('AUTONOMY_PATH_BOUNDARY_UNAVAILABLE'));
});

test('save requires reviewed digest, CAS and authority; pause is durably stored',async t=>{
  const f=await fixture(t),policy={...defaultAutonomyPolicy(),allowedTaskIds:['selected-task']};
  const preview=await (await f.request('/projects/p/autonomy/preview',{policy,expectedRevision:0})).json();
  assert.equal((await f.command('save',{policy,previewDigest:'forged'})).status,409);
  const saved=await f.command('save',{policy,previewDigest:preview.previewDigest});assert.equal(saved.status,200);
  assert.equal((await f.read()).paused,true);
  assert.equal((await f.command('resume')).status,200);assert.equal((await f.read()).paused,false);
  assert.equal((await f.command('pause')).status,200);assert.equal((await f.read()).paused,true);
  const stale=await f.request('/projects/p/autonomy/resume',{expectedRevision:0,expectedAuthorityEpoch:1,idempotencyKey:randomUUID()});assert.equal(stale.status,409);
  assert.equal((await f.command('resume',{expectedAuthorityEpoch:99})).status,409);
  const forged=await f.request('/projects/p/commands',{expectedAuthorityEpoch:1,idempotencyKey:randomUUID(),changes:[{expectedRevision:0,entity:{id:'autonomy-policy',kind:'settings',data:{paused:false}}}]});assert.equal(forged.status,409);
});
