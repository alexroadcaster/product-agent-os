import {test} from 'node:test';
import assert from 'node:assert/strict';
import {join} from 'node:path';
import {m2Fixture} from './m2-fixture.mts';
import {createLocalApplication} from '../../apps/local-service/src/http/application.mts';

test('paired queue view is available without a worker or configured policy and starts no runs',async t=>{
 const f=await m2Fixture(t),origin='http://127.0.0.1:43201';let calls=0;
 const app=await createLocalApplication({store:f.store,origin,instanceId:'queue-fixture',profileDirectory:join(f.root,'profile'),runtime:{snapshot:async()=>({}),dispatch:async()=>{calls++;throw Error('must not dispatch');}}});
 const paired=await app.handleRequest(new Request(origin+'/api/v1/bootstrap/exchange',{method:'POST',headers:{origin,host:'127.0.0.1:43201','content-type':'application/json'},body:JSON.stringify({code:app.issuePairingCode()})}));
 const cookie=paired.headers.get('set-cookie')!.split(';')[0];
 const response=await app.handleRequest(new Request(origin+'/api/v1/projects/p/scheduler',{headers:{origin,host:'127.0.0.1:43201',cookie}}));
 assert.equal(response.status,200,JSON.stringify(await response.clone().json()));const value=await response.json();assert.deepEqual(value.items,[]);assert.equal(value.capabilities.maxWritersPerWorkspace,1);assert.equal(calls,0);
});
