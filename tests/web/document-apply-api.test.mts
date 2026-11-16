import {test} from 'node:test';
import assert from 'node:assert/strict';
import {join} from 'node:path';
import {m2Fixture} from './m2-fixture.mts';
import {createLocalApplication} from '../../apps/local-service/src/http/application.mts';

test('paired document API applies a staged proposal, preserves conflicts and supports explicit rollback without acceptance',async t=>{
 const f=await m2Fixture(t),origin='http://127.0.0.1:49836',app=await createLocalApplication({store:f.store,origin,instanceId:'document-apply-api',profileDirectory:join(f.root,'profile')});f.beforeClose(()=>app.close());
 const paired=await app.handleRequest(new Request(origin+'/bootstrap/exchange',{method:'POST',headers:{host:'127.0.0.1:49836',origin,'content-type':'application/json'},body:JSON.stringify({code:app.issuePairingCode()})}));
 const cookie=paired.headers.get('set-cookie')!.split(';')[0],csrf=(await paired.json() as any).csrfToken;
 async function request(path:string,input?:unknown,withCsrf=true){const r=await app.handleRequest(new Request(origin+'/api/v1/projects/p'+path,{method:input===undefined?'GET':'POST',headers:{host:'127.0.0.1:49836',origin,cookie,...(withCsrf?{'x-paos-csrf':csrf}:{}),'content-type':'application/json'},...(input===undefined?{}:{body:JSON.stringify(input)})}));return {status:r.status,body:await r.json() as any};}
 await f.store.write({projectId:'p',actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'document',changes:[{expectedRevision:0,entity:{id:'doc',kind:'document',title:'Fixture document',body:'# Before\n'}}]});
 const staged=await request('/artifacts/proposals/preview',{documentId:'doc',sourceVersion:'entity:1',body:'# After\n'});assert.equal(staged.status,200);
 const saved=await request('/artifacts/proposals',{...staged.body,body:'# After\n',epoch:1,idempotencyKey:'stage'});assert.equal(saved.status,200);
 const proposal=await request('/artifacts/'+saved.body.id),revision=Number(proposal.body.item.source.version.slice(7));
 const preview=await request('/artifacts/proposals/apply-preview',{proposalId:saved.body.id,proposalRevision:revision});
 assert.equal(preview.status,200,JSON.stringify(preview.body));
 assert.equal((await request('/artifacts/proposals/apply-preview',{proposalId:saved.body.id,proposalRevision:revision},false)).status,403);
 const input={proposalId:saved.body.id,proposalRevision:revision,previewDigest:preview.body.previewDigest,epoch:1,idempotencyKey:'apply'};
 assert.equal((await request('/artifacts/proposals/apply',{...input,path:'../wrong.md'})).status,400);
 const applied=await request('/artifacts/proposals/apply',input);assert.equal(applied.status,200);assert.equal(applied.body.state,'applied');assert.equal(applied.body.accepted,false);assert.deepEqual(await request('/artifacts/proposals/apply',input),applied);
 assert.equal((await request('/artifacts/doc')).body.body,'# After\n');
 const current=await request('/artifacts/'+saved.body.id),r=Number(current.body.item.source.version.slice(7));
 const rollback=await request('/artifacts/proposals/rollback-preview',{proposalId:saved.body.id,proposalRevision:r});assert.equal(rollback.status,200);
 await f.store.write({projectId:'p',actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'external-edit',changes:[{expectedRevision:2,entity:{id:'doc',kind:'document',title:'Fixture document',body:'# External\n'}}]});
 const rollbackInput={proposalId:saved.body.id,proposalRevision:r,previewDigest:rollback.body.previewDigest,epoch:1,idempotencyKey:'rollback'};
 assert.equal((await request('/artifacts/proposals/rollback',rollbackInput)).status,409);assert.equal((await request('/artifacts/doc')).body.body,'# External\n');
 const fresh=await request('/artifacts/proposals/rollback-preview',{proposalId:saved.body.id,proposalRevision:r});assert.equal(fresh.body.before,'# External\n');
 const restored=await request('/artifacts/proposals/rollback',{...rollbackInput,previewDigest:fresh.body.previewDigest,idempotencyKey:'rollback-reviewed'});assert.equal(restored.body.state,'rolled_back');assert.equal((await request('/artifacts/doc')).body.body,'# Before\n');
 assert.ok(!JSON.stringify([preview.body,applied.body,restored.body,(await request('/artifacts')).body]).includes('beforeBase64'));
});
