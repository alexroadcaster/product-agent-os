import test from 'node:test';
import assert from 'node:assert/strict';
import {m2Fixture} from './m2-fixture.mts';
import {createLocalApplication} from '../../apps/local-service/src/http/application.mts';
import {join} from 'node:path';
test('team run navigation exposes a scoped safe summary without lease, prompt or pin instructions',async t=>{
 const f=await m2Fixture(t);await f.store.write({projectId:'p',actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'run',changes:[{expectedRevision:0,entity:{id:'run1',kind:'run',status:'completed',data:{appAgentRun:{id:'run1',projectId:'p',sessionId:'s1',mode:'planning',state:'completed',input:'private synthetic prompt',leaseToken:'privateSyntheticLease',assetPins:[{assetId:'agent1',kind:'agent',version:2,hash:'a'.repeat(64),content:'private instructions'}]}}}}]});
 const origin='http://127.0.0.1:49831',app=await createLocalApplication({store:f.store,origin,instanceId:'safe-run',profileDirectory:join(f.root,'profile')});
 const paired=await app.handleRequest(new Request(origin+'/bootstrap/exchange',{method:'POST',headers:{host:'127.0.0.1:49831',origin,'content-type':'application/json'},body:JSON.stringify({code:app.issuePairingCode()})}));const cookie=paired.headers.get('set-cookie')!.split(';')[0];
 const get=(id:string)=>app.handleRequest(new Request(origin+'/api/v1/projects/p/team/runs/'+id,{headers:{host:'127.0.0.1:49831',cookie}}));
 const response=await get('run1');assert.equal(response.status,200);const body=await response.json() as any;assert.equal(body.id,'run1');assert.equal(body.sessionId,'s1');assert.equal(body.assetPins[0].version,2);assert.equal(body.workflow,null);assert.equal(JSON.stringify(body).includes('private'),false);assert.equal((await get('other-project-run')).status,404);
});


test('ordinary messages without optional title do not claim sensitive text was redacted',async t=>{const f=await m2Fixture(t);await f.store.write({projectId:'p',actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'normal-message',changes:[{expectedRevision:0,entity:{id:'session1',kind:'session'}},{expectedRevision:0,entity:{id:'normal',kind:'message',parentId:'session1',body:'Ordinary synthetic message',data:{role:'user'}}}]});assert.notEqual((await f.store.get('p','normal'))!.data.redacted,true);});
