import assert from 'node:assert/strict';
import {test} from 'node:test';
import {join} from 'node:path';
import {m2Fixture} from './m2-fixture.mts';
import {createLocalApplication} from '../../apps/local-service/src/http/application.mts';

test('Manual preview and transition work without policy, worker or any agent dispatch',async t=>{
 const f=await m2Fixture(t),task=await f.ready(),origin='http://127.0.0.1:43201';let calls=0;
 const app=await createLocalApplication({store:f.store,origin,instanceId:'recipe-fixture',profileDirectory:join(f.root,'profile'),runtime:{snapshot:async()=>({}),dispatch:async()=>{calls++;throw Error('must not dispatch');}}});
 let cookie='',csrf='';const request=(path:string,input:unknown)=>app.handleRequest(new Request(origin+'/api/v1'+path,{method:'POST',headers:{origin,host:'127.0.0.1:43201',cookie,'x-paos-csrf':csrf,'content-type':'application/json'},body:JSON.stringify(input)}));
 const paired=await request('/bootstrap/exchange',{code:app.issuePairingCode()});cookie=paired.headers.get('set-cookie')!.split(';')[0];csrf=(await paired.json()).csrfToken;
 const input={taskId:task.id,transitionId:'ready-in_progress',mode:'manual',expectedTaskRevision:task.revision,reason:'Manual work'};
 const preview=await request('/projects/p/execution-recipes/preview',input);assert.equal(preview.status,200,JSON.stringify(await preview.clone().json()));
 const value=await preview.json();assert.equal(value.mode,'manual');assert.equal(value.agentRuns,0);
 const started=await request('/projects/p/execution-recipes/start',{...input,previewDigest:value.previewDigest,expectedAuthorityEpoch:1,idempotencyKey:'manual'});
 assert.equal(started.status,200);assert.equal((await f.store.get('p',task.id))!.status,'in_progress');assert.equal(calls,0);assert.equal((await f.store.list('p',{kind:'run'})).length,0);
});
