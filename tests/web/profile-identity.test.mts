import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtemp,mkdir,rename,rm,symlink} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {bindProfile,assertProfileIdentity,createProfileScopedStore} from '../../apps/local-service/src/connections/profile-identity.mts';
import {createConnectionBroker,type CredentialStore} from '../../apps/local-service/src/connections/broker.ts';

test('profile namespace is stable for restart and canonical aliases, including Windows case',async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-profile-'));t.after(()=>rm(root,{recursive:true,force:true}));
 const directory=join(root,'profile');await mkdir(directory);
 const first=await bindProfile(directory);
 assert.match(first.profileId,/^profile_[a-f0-9]{64}$/);
 assert.equal((await bindProfile(directory)).profileId,first.profileId);
 const alias=join(root,'alias');await symlink(directory,alias,process.platform==='win32'?'junction':'dir');
 assert.equal((await bindProfile(alias)).profileId,first.profileId);
 if(process.platform==='win32')assert.equal((await bindProfile(directory.toUpperCase())).profileId,first.profileId);
 await assertProfileIdentity(first);
});

test('replaced or retargeted profile fails before any credential access and has a new namespace',async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-profile-replace-'));t.after(()=>rm(root,{recursive:true,force:true}));
 const directory=join(root,'profile');await mkdir(directory);const first=await bindProfile(directory);
 let calls=0;const scoped=createProfileScopedStore(first,{read:async()=>{calls++;return null;},write:async()=>{calls++;},delete:async()=>{calls++;}});
 await rename(directory,join(root,'old'));await mkdir(directory);
 assert.notEqual((await bindProfile(directory)).profileId,first.profileId);
 const target=`PAOS/${first.profileId}/same`;
 for(const action of [()=>scoped.read(target),()=>scoped.write(target,'synthetic'),()=>scoped.delete(target)]) {
  await assert.rejects(action,{code:'PROFILE_ROOT_UNAVAILABLE'});
 }
 assert.equal(calls,0);
 await assert.rejects(bindProfile(join(root,'missing')),{code:'PROFILE_ROOT_UNAVAILABLE'});
});

test('scoped store rejects foreign, legacy and malformed targets without consulting its underlying store',async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-profile-target-'));t.after(()=>rm(root,{recursive:true,force:true}));
 const identity=await bindProfile(root);let calls=0;
 const scoped=createProfileScopedStore(identity,{read:async()=>{calls++;return null;},write:async()=>{calls++;},delete:async()=>{calls++;}});
 for(const target of ['PAOS/default/same','PAOS/other/same',`PAOS/${identity.profileId}/../other`,`PAOS/${identity.profileId}/`]) {
  await assert.rejects(()=>scoped.read(target),{code:'PROFILE_TARGET_REJECTED'});
  await assert.rejects(()=>scoped.write(target,'synthetic'),{code:'PROFILE_TARGET_REJECTED'});
  await assert.rejects(()=>scoped.delete(target),{code:'PROFILE_TARGET_REJECTED'});
 }
 assert.equal(calls,0);
});

test('same connection alias cannot load or forget another profile key; restart retains its own key',async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-profile-broker-'));t.after(()=>rm(root,{recursive:true,force:true}));
 const first=join(root,'first'),second=join(root,'second');await mkdir(first);await mkdir(second);
 const values=new Map<string,string>();const targets:string[]=[];
 const store:CredentialStore={read:async(target)=>{targets.push(target);return values.get(target)??null;},write:async(target,value)=>{targets.push(target);values.set(target,value);},delete:async(target)=>{targets.push(target);values.delete(target);}};
 const request=async(method:string)=>method==='account/login/start'?{type:'apiKey'}:method==='account/read'?{account:{type:'apiKey'}}:{};
 const broker=async(path:string)=>{const identity=await bindProfile(path);return createConnectionBroker({profileId:identity.profileId,store:createProfileScopedStore(identity,store),request});};
 const a=await broker(first);await a.connect({connectionId:'same',apiKey:'synthetic-profile-key',remember:true});const scope=a.accountScopeId();
 await a.disconnect();const b=await broker(second);
 await assert.rejects(()=>b.connect({connectionId:'same'}),{code:'connection_failed'});
 await b.disconnect({forget:true});assert.equal(values.size,1);
 const restarted=await broker(first);await restarted.connect({connectionId:'same'});assert.equal(restarted.accountScopeId(),scope);
 await restarted.disconnect({forget:true});assert.equal(values.size,0);
 assert.equal(targets.some(target=>target.startsWith('PAOS/default/')),false);
});
