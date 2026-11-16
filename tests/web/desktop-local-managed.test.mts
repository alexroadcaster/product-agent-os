import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,readFile,writeFile,rm,readdir} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {packDistribution,readSelection,managedDelivery} from '../../apps/desktop-local/distribution.mts';
import {desktopCommand} from '../../apps/desktop-local/main.mts';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {createProfileInstanceClaimer} from '../../apps/launcher/profile-instance.ts';
const source=fileURLToPath(new URL('../../',import.meta.url));
const hash=(bytes:Buffer)=>createHash('sha256').update(bytes).digest('hex');
async function fixture(t:any){const root=await mkdtemp(join(tmpdir(),'paos-managed-'));t.after(async()=>{assert.equal(dirname(root),resolve(tmpdir()));await rm(root,{recursive:true,force:true});});return root;}

test('managed CLI sets up, updates and explicitly rolls back into new profiles without changing old data',async t=>{
 const root=await fixture(t),a=join(root,'package-a'),am=await packDistribution(source,a),home=join(root,'Пилот home');
 const first:any=await desktopCommand(['setup','--home',home,'--package',a,'--expected-id',am.releaseId,'--expected-selection','none']);
 assert.equal(first.selection.current.releaseId,am.releaseId);assert.equal(first.channel,'private_local_pilot');assert.equal(first.signed,false);
 assert.ok(first.selection.current.installDirectory.startsWith(join(home,'versions')));assert.ok(first.selection.current.profileDirectory.startsWith(join(home,'profiles')));
 const oldProfile=first.selection.current.profileDirectory,store=await openLocalStore({databasePath:join(oldProfile,'state.sqlite')});let blob:any;
 try{await store.registerProject({id:'p',keyPrefix:'TEST',canonicalRoot:root,rootIdentity:'synthetic',authorityMode:'sql'});blob=await store.putBlob('p',Buffer.from('Retained managed attachment'));await store.write({projectId:'p',actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'seed',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}},{expectedRevision:0,entity:{id:'m',kind:'message',parentId:'s',body:'Retained managed message',blobIds:[blob.id]}},{expectedRevision:0,entity:{id:'approval',kind:'approval',status:'pending'}},{expectedRevision:0,entity:{id:'run',kind:'run',status:'running'}}],outbox:[{kind:'dispatch',payload:{runId:'run'}}]});}finally{await store.close();}
 const before=hash(await readFile(join(oldProfile,'state.sqlite')));await writeFile(join(a,'apps/web/dist/index.html'),(await readFile(join(a,'apps/web/dist/index.html'),'utf8'))+'\n<!-- managed release B -->');const b=join(root,'package-b'),bm=await packDistribution(a,b);
 const updated:any=await desktopCommand(['update','--home',home,'--package',b,'--expected-id',bm.releaseId,'--expected-selection',first.selection.digest]);
 assert.notEqual(updated.selection.current.profileDirectory,oldProfile);assert.equal(hash(await readFile(join(oldProfile,'state.sqlite'))),before);assert.equal(updated.selection.previous.releaseId,am.releaseId);
 const restored=await openLocalStore({databasePath:join(updated.selection.current.profileDirectory,'state.sqlite')});try{assert.equal((await restored.get('p','m'))!.body,'Retained managed message');assert.equal((await restored.get('p','approval'))!.status,'stale');assert.equal((await restored.get('p','run'))!.status,'recovery_required');assert.equal((await restored.outbox('p'))[0].state,'recovery_required');assert.equal(Buffer.from(await restored.readBlob('p',blob.id)).toString(),'Retained managed attachment');}finally{await restored.close();}
 const secondBefore=hash(await readFile(join(updated.selection.current.profileDirectory,'state.sqlite')));
 const rolled:any=await desktopCommand(['rollback','--home',home,'--expected-id',am.releaseId,'--expected-selection',updated.selection.digest,'--backup',updated.backupDirectory]);
 assert.equal(rolled.selection.current.releaseId,am.releaseId);assert.notEqual(rolled.selection.current.profileDirectory,oldProfile);assert.notEqual(rolled.selection.current.profileDirectory,updated.selection.current.profileDirectory);assert.equal(hash(await readFile(join(oldProfile,'state.sqlite'))),before);assert.equal(hash(await readFile(join(updated.selection.current.profileDirectory,'state.sqlite'))),secondBefore);
 await assert.rejects(desktopCommand(['update','--home',home,'--package',b,'--expected-id',bm.releaseId,'--expected-selection',first.selection.digest]),{code:'SELECTION_CONFLICT'});
 const status:any=await desktopCommand(['managed-status','--home',home]);assert.equal(status.selection.digest,rolled.selection.digest);assert.equal(status.operation.state,'completed');assert.equal((await readdir(join(home,'profiles'))).length,3);
});

test('native launcher child uses the fresh user-space home and only the explicit environment whitelist',async t=>{
 const root=await fixture(t),profile=join(root,'profile'),fresh=join(root,'fresh-home');await mkdir(profile);await mkdir(fresh);
 const names=['USERPROFILE','HOME','APPDATA','LOCALAPPDATA','TEMP','TMP','CODEX_HOME','PAOS_UNAPPROVED_CANARY','NODE_OPTIONS'] as const,previous=new Map(names.map(name=>[name,process.env[name]]));
 const values={USERPROFILE:fresh,HOME:fresh,APPDATA:join(fresh,'Roaming'),LOCALAPPDATA:join(fresh,'Local'),TEMP:join(fresh,'Temp'),TMP:join(fresh,'Temp'),CODEX_HOME:join(fresh,'.codex'),PAOS_UNAPPROVED_CANARY:'synthetic-only',NODE_OPTIONS:'--not-an-approved-node-option'};for(const [name,value]of Object.entries(values))process.env[name]=value;
 const probe=join(root,'env-probe.mjs');await writeFile(probe,`import {writeFile} from 'node:fs/promises';import {homedir} from 'node:os';import {join,dirname} from 'node:path';const profile=process.env.PAOS_PROFILE_DIR,expected=join(dirname(profile),'fresh-home');await writeFile(join(profile,'environment-proof.json'),JSON.stringify({homeMatchesFixture:homedir()===expected,home:process.env.HOME,userprofile:process.env.USERPROFILE,codeHome:process.env.CODEX_HOME,unapproved:process.env.PAOS_UNAPPROVED_CANARY!==undefined,nodeOptions:process.env.NODE_OPTIONS!==undefined}));process.on('message',m=>{if(m.type==='quit'){process.send({type:'stopped'},()=>process.exit(0));}});process.send({type:'ready',instanceId:process.env.PAOS_INSTANCE_ID,build:'paos-m1-0.1.0',port:41232,pairingCode:'synthetic-env-pairing'});`);
 try{const {runNativeLauncher}=await import('../../apps/launcher/main.mts');const result=await runNativeLauncher({profileDirectory:profile,serviceModule:probe,inspectRuntime:async()=>({status:'unverified'}),readHealth:async endpoint=>({...endpoint,build:'paos-m1-0.1.0',alive:true,sourceReaderReady:true,runtimeCapable:false,browserLaunchVersion:1}),showWindow:async()=>{const proof=JSON.parse(await readFile(join(profile,'environment-proof.json'),'utf8'));assert.equal(proof.homeMatchesFixture,true);assert.equal(proof.home,fresh);assert.equal(proof.userprofile,fresh);assert.equal(proof.codeHome,values.CODEX_HOME);assert.equal(proof.unapproved,false);assert.equal(proof.nodeOptions,false);return 'quit';}});assert.equal(result.status,'opened');}
 finally{for(const [name,value]of previous)if(value===undefined)delete process.env[name];else process.env[name]=value;}
});

test('managed update holds source ownership throughout transfer and distinguishes receipt loss after selection commit',async t=>{
 const root=await fixture(t),a=join(root,'a'),am=await packDistribution(source,a),home=join(root,'home');
 const first=await managedDelivery('setup',{home,packageDirectory:a,expectedId:am.releaseId,expectedSelection:null}),profile=first.selection.current.profileDirectory;
 await writeFile(join(a,'apps/web/dist/index.html'),(await readFile(join(a,'apps/web/dist/index.html'),'utf8'))+'\n<!-- reservation candidate -->');const b=join(root,'b'),bm=await packDistribution(a,b),input={home,packageDirectory:b,expectedId:bm.releaseId,expectedSelection:first.selection.digest};
 await mkdir(join(profile,'service-instance'));await assert.rejects(managedDelivery('update',input),{code:'PROFILE_RUNNING_OR_UNRESOLVED'});await rm(join(profile,'service-instance'),{recursive:true});assert.equal((await readSelection(join(home,'selection')))!.digest,first.selection.digest);
 await assert.rejects(managedDelivery('update',input,{afterSnapshot:async()=>{const claim=createProfileInstanceClaimer(profile,{startService:async()=>{throw Error('must not start');},readHealth:async()=>{throw Error('must not probe');}});await assert.rejects(claim(new AbortController().signal),(e:any)=>e.reason==='startup_unresolved');const {withProfileMaintenance}=await import('../../apps/desktop-local/distribution.mts');await assert.rejects(withProfileMaintenance([profile],async()=>{}),{code:'PROFILE_RUNNING_OR_UNRESOLVED'});throw Object.assign(Error('Synthetic interruption'),{code:'SYNTHETIC_INTERRUPTED'});}}),{code:'SYNTHETIC_INTERRUPTED'});
 assert.equal((await readSelection(join(home,'selection')))!.digest,first.selection.digest);const failed:any=await desktopCommand(['managed-status','--home',home]);assert.equal(failed.operation.state,'failed');assert.equal(failed.operation.phase,'restoring');assert.ok((await readdir(join(home,'backups'))).length>=1);
 const uncertain=await managedDelivery('update',input,{afterSelection:async()=>{throw Error('Synthetic lost final receipt');}});assert.equal(uncertain.state,'selection_committed_receipt_pending');const current:any=await desktopCommand(['managed-status','--home',home]);assert.equal(current.state,'selection_committed_receipt_pending');assert.equal(current.selection.digest,uncertain.selection.digest);assert.notEqual(current.selection.digest,first.selection.digest);await assert.rejects(managedDelivery('update',input),{code:'SELECTION_CONFLICT'});assert.equal((await readdir(join(home,'profiles'))).length,2);
});

test('managed admission rejects incompatible tuples and foreign recomputed selections before touching their profiles',async t=>{
 const root=await fixture(t),a=join(root,'a'),am=await packDistribution(source,a),home=join(root,'home');const first=await managedDelivery('setup',{home,packageDirectory:a,expectedId:am.releaseId,expectedSelection:null});
 const pinPath=join(a,'packages/contracts/runtime/qualified-manifest.json'),pin=JSON.parse(await readFile(pinPath,'utf8'));pin.node.version='v0.0.0';await writeFile(pinPath,JSON.stringify(pin));const bad=join(root,'bad'),bm=await packDistribution(a,bad);
 await assert.rejects(managedDelivery('update',{home,packageDirectory:bad,expectedId:bm.releaseId,expectedSelection:first.selection.digest}),{code:'HOST_PREREQUISITE_MISMATCH'});assert.equal((await readSelection(join(home,'selection')))!.digest,first.selection.digest);assert.ok(!(await readdir(join(home,'versions'))).includes(bm.releaseId));
 const selectionPath=join(home,'selection/selection.json'),selection=JSON.parse(await readFile(selectionPath,'utf8'));selection.current.profileDirectory=join(root,'foreign-profile');const {digest:ignored,...body}=selection;selection.digest=createHash('sha256').update(JSON.stringify(body)).digest('hex');await writeFile(selectionPath,JSON.stringify(selection));await assert.rejects(desktopCommand(['managed-status','--home',home]),{code:'MANAGED_SELECTION_OUTSIDE_HOME'});await assert.rejects(desktopCommand(['managed-start','--home',home]),{code:'MANAGED_SELECTION_OUTSIDE_HOME'});await assert.rejects(readFile(join(root,'foreign-profile/state.sqlite')),{code:'ENOENT'});
 // An unresolved home operation must fence start before even inspecting a selection; the invalid scope keeps this RED free of real-service side effects.
 await writeFile(join(home,'operation.lock'),'synthetic unresolved operation');await assert.rejects(desktopCommand(['managed-start','--home',home]),{code:'SELECTION_BUSY'});assert.equal(await readFile(join(home,'operation.lock'),'utf8'),'synthetic unresolved operation');
});
