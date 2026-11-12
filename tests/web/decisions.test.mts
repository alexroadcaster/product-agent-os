import {test} from 'node:test';
import assert from 'node:assert/strict';
import {join} from 'node:path';
import {m2Fixture} from './m2-fixture.mts';
import {createLocalApplication} from '../../apps/local-service/src/http/application.mts';

test('paired Decisions view is distinct from private runtime entities and starts no work',async t=>{
 const f=await m2Fixture(t),origin='http://127.0.0.1:43201';let calls=0;
 const app=await createLocalApplication({store:f.store,origin,instanceId:'decisions-fixture',profileDirectory:join(f.root,'profile'),runtime:{snapshot:async()=>({}),dispatch:async()=>{calls++;throw Error('No work');}}});
 const paired=await app.handleRequest(new Request(origin+'/api/v1/bootstrap/exchange',{method:'POST',headers:{origin,host:'127.0.0.1:43201','content-type':'application/json'},body:JSON.stringify({code:app.issuePairingCode()})}));const cookie=paired.headers.get('set-cookie')!.split(';')[0];
 const response=await app.handleRequest(new Request(origin+'/api/v1/projects/p/decisions',{headers:{origin,host:'127.0.0.1:43201',cookie}}));assert.equal(response.status,200,JSON.stringify(await response.clone().json()));assert.deepEqual((await response.json()).items,[]);assert.equal(calls,0);
});

test('decision HTTP contract preserves CSRF/private entity boundaries and exact response replay',async t=>{
 const f=await m2Fixture(t),origin='http://127.0.0.1:43202',host='127.0.0.1:43202',app=await createLocalApplication({store:f.store,origin,instanceId:'decisions-http',profileDirectory:join(f.root,'profile')});
 const pair=await app.handleRequest(new Request(origin+'/api/v1/bootstrap/exchange',{method:'POST',headers:{origin,host,'content-type':'application/json'},body:JSON.stringify({code:app.issuePairingCode()})}));const cookie=pair.headers.get('set-cookie')!.split(';')[0],csrf=(await pair.json()).csrfToken;
 async function api(path:string,input?:any,token=csrf){const r=await app.handleRequest(new Request(origin+'/api/v1'+path,{method:input?'POST':'GET',headers:{origin,host,cookie,'content-type':'application/json','x-paos-csrf':token},...input?{body:JSON.stringify(input)}:{}}));return {status:r.status,body:await r.json()};}
 const input={kind:'product',title:'Decision HTTP',body:'Owner choice',proposedDiff:'- old\n+ new',expiresInSeconds:60,expectedAuthorityEpoch:1,idempotencyKey:'create'};
 assert.notEqual((await api('/projects/p/decisions',input,'invalid')).status,200);const created=await api('/projects/p/decisions',input);assert.equal(created.status,200);const d=created.body;assert.equal(d.diff.status,'proposed');
 assert.equal((await api('/projects/p/entities/'+d.id)).body.error.code,'PRIVATE_RUNTIME_STATE');assert.equal((await api('/projects/p/decisions',{...input,kind:'runtime_permission',idempotencyKey:'forged'})).body.error.code,'DECISION_KIND_FORBIDDEN');
 const response={expectedRevision:d.revision,expectedAuthorityEpoch:1,idempotencyKey:'respond',response:'accept'};const answered=await api('/projects/p/decisions/'+d.id+'/respond',response);assert.equal(answered.status,200);assert.deepEqual((await api('/projects/p/decisions/'+d.id+'/respond',response)).body,answered.body);
 assert.equal((await api('/projects/p/decisions/'+d.id)).body.history.length,2);assert.equal((await api('/projects/p/decisions?kind=product&state=resolved')).body.total,1);
});
