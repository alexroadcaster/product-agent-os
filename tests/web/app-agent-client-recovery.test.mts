import assert from 'node:assert/strict';
import {test,type TestContext} from 'node:test';
import {mkdtemp,readFile,writeFile,rm,link} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {callAppAgent} from '../../apps/local-service/src/runtime/app-agent-client.mts';

async function fixture(t:TestContext){
 const root=await mkdtemp(join(tmpdir(),'paos-client-recovery-'));t.after(()=>rm(root,{recursive:true,force:true}));
 const descriptorPath=join(root,'new.json'),previousStatePath=join(root,'old.json.worker-worker.json');
 const descriptor={schemaVersion:'paos_app_agent_channel_v1',instanceId:'new-instance',origin:'http://127.0.0.1:41111',capabilityToken:'a'.repeat(64),profileId:'stable-profile'};
 const previous={schemaVersion:'paos_app_agent_worker_v1',instanceId:'old-instance',descriptorDigest:'b'.repeat(64),profileId:'stable-profile',workerId:'worker',generation:'stable-generation',leaseToken:'old-private-lease',expiresAt:1};
 await writeFile(descriptorPath,JSON.stringify(descriptor));await writeFile(previousStatePath,JSON.stringify(previous));let calls=0,posts=0;
 const fetcher:typeof fetch=async(url,init)=>{calls++;if(String(url).endsWith('/health'))return Response.json({instanceId:descriptor.instanceId,alive:true});posts++;const input=JSON.parse(String(init?.body));assert.equal(input.generation,previous.generation);assert.equal(input.workerId,'worker');
  if(String(url).endsWith('/attach'))return Response.json({workerId:'worker',generation:input.generation,leaseToken:'new-private-lease',expiresAt:10000});
  assert.ok(String(url).endsWith('/reconcile'));assert.equal(input.leaseToken,'new-private-lease');return Response.json({runId:'saved-run',state:'completed'});
 };
 return {root,descriptorPath,previousStatePath,descriptor,previous,fetcher,get calls(){return calls;},get posts(){return posts;},options:{descriptorPath,previousStatePath,workerId:'worker',action:'reattach' as const}};
}
test('explicit same-profile restart migration preserves generation, old file and terminal reconciliation',async(t)=>{
 const f=await fixture(t);const old=await readFile(f.previousStatePath,'utf8');
 const attached=await callAppAgent(f.options,{fetch:f.fetcher});assert.equal(JSON.stringify(attached).includes('private-lease'),false);
 const next=JSON.parse(await readFile(f.descriptorPath+'.worker-worker.json','utf8'));assert.equal(next.instanceId,'new-instance');assert.equal(next.profileId,'stable-profile');assert.equal(next.generation,'stable-generation');assert.equal(next.leaseToken,'new-private-lease');assert.equal(next.descriptorDigest,createHash('sha256').update(await readFile(f.descriptorPath)).digest('hex'));assert.equal(await readFile(f.previousStatePath,'utf8'),old);
 assert.deepEqual(await callAppAgent({descriptorPath:f.descriptorPath,workerId:'worker',action:'reconcile',input:{runId:'saved-run'}},{fetch:f.fetcher}),{runId:'saved-run',state:'completed'});assert.equal(f.posts,2);
});
test('foreign or legacy profile and malformed old worker state reject before any request or new state',async(t)=>{
 for(const change of [{profileId:'foreign-profile'},{profileId:undefined},{generation:''},{workerId:'other'},{descriptorDigest:'bad'},{instanceId:'../unsafe'},{expiresAt:'invalid'}]){
  const f=await fixture(t);await writeFile(f.previousStatePath,JSON.stringify({...f.previous,...change}));const before=await readFile(f.previousStatePath,'utf8');
  await assert.rejects(callAppAgent(f.options,{fetch:f.fetcher}),{code:'AGENT_WORKER_STATE_INVALID'});assert.equal(f.calls,0);assert.equal(await readFile(f.previousStatePath,'utf8'),before);
  await assert.rejects(readFile(f.descriptorPath+'.worker-worker.json'),{code:'ENOENT'});
 }
});
test('stale health prevents migration and leaves source file unchanged',async(t)=>{
 const f=await fixture(t);const before=await readFile(f.previousStatePath,'utf8');let requests=0;
 await assert.rejects(callAppAgent(f.options,{fetch:async()=>{requests++;return Response.json({instanceId:'old-instance',alive:true});}}),{code:'AGENT_INSTANCE_MISMATCH'});
 assert.equal(requests,1);assert.equal(await readFile(f.previousStatePath,'utf8'),before);await assert.rejects(readFile(f.descriptorPath+'.worker-worker.json'),{code:'ENOENT'});
});
test('previous-state is reattach only, absolute, regular and never overwrites a destination',async(t)=>{
 const f=await fixture(t);await assert.rejects(callAppAgent({...f.options,action:'attach'},{fetch:f.fetcher}),{code:'AGENT_INPUT_INVALID'});
 await assert.rejects(callAppAgent({...f.options,previousStatePath:'relative.json'},{fetch:f.fetcher}),{code:'AGENT_INPUT_INVALID'});assert.equal(f.calls,0);
 await writeFile(f.descriptorPath+'.worker-worker.json','existing-state');await assert.rejects(callAppAgent(f.options,{fetch:f.fetcher}),{code:'EEXIST'});assert.equal(f.posts,0);assert.equal(await readFile(f.descriptorPath+'.worker-worker.json','utf8'),'existing-state');
 const linked=join(f.root,'linked.json');await link(f.previousStatePath,linked);await assert.rejects(callAppAgent({...f.options,previousStatePath:linked},{fetch:f.fetcher}),{code:'AGENT_FILE_INVALID'});
});
test('rejected migrated attach removes only new empty state and preserves old recovery material',async(t)=>{
 const f=await fixture(t),before=await readFile(f.previousStatePath,'utf8');
 await assert.rejects(callAppAgent(f.options,{fetch:async(url)=>String(url).endsWith('/health')?Response.json({instanceId:f.descriptor.instanceId,alive:true}):Response.json({error:'rejected'},{status:409})}),{code:'AGENT_OPERATION_REJECTED'});
 assert.equal(await readFile(f.previousStatePath,'utf8'),before);await assert.rejects(readFile(f.descriptorPath+'.worker-worker.json'),{code:'ENOENT'});
});
test('same-instance legacy state can renew lease using CAS without profile migration',async(t)=>{
 const f=await fixture(t);delete (f.descriptor as {profileId?:string}).profileId;await writeFile(f.descriptorPath,JSON.stringify(f.descriptor));
 const statePath=f.descriptorPath+'.worker-worker.json',legacy={...f.previous,profileId:undefined,instanceId:f.descriptor.instanceId,descriptorDigest:createHash('sha256').update(await readFile(f.descriptorPath)).digest('hex')};await writeFile(statePath,JSON.stringify(legacy));
 await callAppAgent({descriptorPath:f.descriptorPath,workerId:'worker',action:'reattach'},{fetch:f.fetcher});const saved=JSON.parse(await readFile(statePath,'utf8'));assert.equal(saved.generation,'stable-generation');assert.equal(saved.leaseToken,'new-private-lease');assert.equal(saved.profileId,undefined);
});
