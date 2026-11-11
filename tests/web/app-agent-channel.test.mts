import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtemp,readFile,rm,writeFile,link} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createAppAgentChannel} from '../../apps/local-service/src/runtime/app-agent-channel.mts';
import {callAppAgent} from '../../apps/local-service/src/runtime/app-agent-client.mts';
test('channel requires exact capability and local origin before dispatch',async(t)=>{
 const profileDirectory=await mkdtemp(join(tmpdir(),'paos-channel-'));t.after(()=>rm(profileDirectory,{recursive:true,force:true}));let calls=0;
 const origin='http://127.0.0.1:41111';
 const channel=await createAppAgentChannel({profileDirectory,instanceId:'fixture',origin,assertProfile:async()=>{},dispatch:async()=>{calls++;return {ok:true};}});t.after(()=>channel.close());
 const descriptor=JSON.parse(await readFile(channel.descriptorPath,'utf8'));
 const request=(token:string,selectedOrigin=origin)=>new Request(origin+'/agent/v1/claim',{method:'POST',headers:{host:'127.0.0.1:41111',origin:selectedOrigin,authorization:'Bearer '+token,'content-type':'application/json'},body:'{}'});
 assert.equal((await channel.handle(request('wrong'))).status,401);assert.equal(calls,0);
 assert.equal((await channel.handle(request(descriptor.capabilityToken,'https://foreign.invalid'))).status,403);assert.equal(calls,0);
 assert.equal((await channel.handle(request(descriptor.capabilityToken))).status,200);assert.equal(calls,1);
});
test('channel capability echoed in a report is scrubbed before dispatch can persist it',async(t)=>{
 const profileDirectory=await mkdtemp(join(tmpdir(),'paos-cap-redaction-'));t.after(()=>rm(profileDirectory,{recursive:true,force:true}));
 const origin='http://127.0.0.1:41111';let observed:unknown;
 const channel=await createAppAgentChannel({profileDirectory,instanceId:'redact',origin,assertProfile:async()=>{},dispatch:async(_action,input)=>{observed=input;return {};}});t.after(()=>channel.close());
 const descriptor=JSON.parse(await readFile(channel.descriptorPath,'utf8'));
 const response=await channel.handle(new Request(origin+'/agent/v1/report',{method:'POST',headers:{host:'127.0.0.1:41111',origin,authorization:`Bearer ${descriptor.capabilityToken}`,'content-type':'application/json'},body:JSON.stringify({text:`Result ${descriptor.capabilityToken}`})}));
 assert.equal(response.status,200);assert.deepEqual(observed,{text:'Result [REDACTED]'});
});
test('profile revocation and stale health fail closed without worker dispatch or secret error text',async(t)=>{
 const profileDirectory=await mkdtemp(join(tmpdir(),'paos-channel-fences-'));t.after(()=>rm(profileDirectory,{recursive:true,force:true}));let current=true,calls=0;
 const origin='http://127.0.0.1:41111';const channel=await createAppAgentChannel({profileDirectory,instanceId:'fixture',origin,assertProfile:async()=>{if(!current)throw Object.assign(new Error('private detail'),{code:'PROFILE_ROOT_UNAVAILABLE'});},dispatch:async()=>{calls++;return {};}});
 t.after(()=>channel.close());const descriptor=JSON.parse(await readFile(channel.descriptorPath,'utf8'));current=false;
 const response=await channel.handle(new Request(origin+'/agent/v1/claim',{method:'POST',headers:{host:'127.0.0.1:41111',origin,authorization:'Bearer '+descriptor.capabilityToken,'content-type':'application/json'},body:'{}'}));
 assert.deepEqual(await response.json(),{error:{code:'PROFILE_ROOT_UNAVAILABLE'}});assert.equal(calls,0);
 const fetcher:typeof fetch=async()=>Response.json({instanceId:'foreign',alive:true});
 await assert.rejects(()=>callAppAgent({descriptorPath:channel.descriptorPath,workerId:'worker',action:'attach'},{fetch:fetcher}),{code:'AGENT_INSTANCE_MISMATCH'});
});
test('restart rotates capability, bounded parsing rejects oversize, close preserves changed descriptors',async(t)=>{
 const profileDirectory=await mkdtemp(join(tmpdir(),'paos-channel-restart-'));t.after(()=>rm(profileDirectory,{recursive:true,force:true}));let calls=0;
 const options={profileDirectory,origin:'http://127.0.0.1:41111',assertProfile:async()=>{},dispatch:async()=>{calls++;return {};}};
 const first=await createAppAgentChannel({...options,instanceId:'first'}),second=await createAppAgentChannel({...options,instanceId:'second'});t.after(()=>second.close());
 const a=JSON.parse(await readFile(first.descriptorPath,'utf8')),b=JSON.parse(await readFile(second.descriptorPath,'utf8'));assert.notEqual(a.capabilityToken,b.capabilityToken);
 const request=(token:string,body:string)=>new Request(options.origin+'/agent/v1/report',{method:'POST',headers:{host:'127.0.0.1:41111',origin:options.origin,authorization:'Bearer '+token,'content-type':'application/json'},body});
 assert.equal((await second.handle(request(a.capabilityToken,'{}'))).status,401);
 assert.equal((await second.handle(request(b.capabilityToken,' '.repeat(65537)))).status,413);assert.equal(calls,0);
 await writeFile(first.descriptorPath,'foreign');await first.close();assert.equal(await readFile(first.descriptorPath,'utf8'),'foreign');
});
test('client stores lease privately, never prints returned tokens, fences auth overrides and foreign state',async(t)=>{
 const profileDirectory=await mkdtemp(join(tmpdir(),'paos-agent-client-'));t.after(()=>rm(profileDirectory,{recursive:true,force:true}));const origin='http://127.0.0.1:41111';
 let channel:Awaited<ReturnType<typeof createAppAgentChannel>>;let claims=0;const lease='synthetic-worker-lease';
 channel=await createAppAgentChannel({profileDirectory,instanceId:'fixture',origin,assertProfile:async()=>{},dispatch:async(action,input)=>{
  if(action==='attach')return {workerId:input.workerId,generation:input.generation,leaseToken:lease,expiresAt:Date.now()+60000};
  claims++;assert.equal(input.workerId,'worker');assert.equal(input.leaseToken,lease);return {leaseToken:lease,job:{text:'synthetic'}};
 }});t.after(()=>channel.close());
 const fetcher:typeof fetch=async(input,init)=>{const request=new Request(input,init);if(new URL(request.url).pathname==='/health')return Response.json({instanceId:'fixture',alive:true});
  request.headers.set('host','127.0.0.1:41111');return channel.handle(request);};
 const options={descriptorPath:channel.descriptorPath,workerId:'worker',action:'attach' as const};
 const attached=await callAppAgent(options,{fetch:fetcher});assert.equal(JSON.stringify(attached).includes(lease),false);
 const claimed=await callAppAgent({...options,action:'claim',input:{workerId:'foreign',leaseToken:'foreign'}},{fetch:fetcher});
 assert.equal(JSON.stringify(claimed).includes(lease),false);assert.equal(claims,1);
 await assert.rejects(()=>callAppAgent(options,{fetch:fetcher}),{code:'EEXIST'});
 const hardlink=join(profileDirectory,'linked.json');await link(channel.descriptorPath,hardlink);
 await assert.rejects(()=>callAppAgent({...options,descriptorPath:hardlink},{fetch:fetcher}),{code:'AGENT_FILE_INVALID'});
});
