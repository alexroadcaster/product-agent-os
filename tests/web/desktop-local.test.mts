import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtemp,mkdir,readFile,writeFile,rm,cp,readdir,symlink} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {DatabaseSync} from 'node:sqlite';
import {packDistribution,verifyDistribution,installDistribution,selectInstallation,readSelection,backupProfile,restoreProfile,startSelection} from '../../apps/desktop-local/distribution.mts';
import {desktopCommand} from '../../apps/desktop-local/main.mts';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {createProfileInstanceClaimer} from '../../apps/launcher/profile-instance.ts';
const source=fileURLToPath(new URL('../../',import.meta.url));
const hash=(b:Uint8Array)=>createHash('sha256').update(b).digest('hex');
async function fixture(t:any){const root=await mkdtemp(join(tmpdir(),'paos-desktop-'));t.after(async()=>{assert.equal(dirname(root),resolve(tmpdir()));await rm(root,{recursive:true,force:true});});return root;}

test('profile maintenance shares the actual launcher reservation and never removes a foreign owner',async t=>{
 const root=await fixture(t),profile=join(root,'profile');await mkdir(profile);const maintenance=(await import('../../apps/desktop-local/distribution.mts') as any).withProfileMaintenance;assert.equal(typeof maintenance,'function');let starts=0;
 const claim=createProfileInstanceClaimer(profile,{async startService(){starts++;return {status:'not_started'};},async readHealth(){throw Error('not reached');}});
 await maintenance([profile],async()=>{await assert.rejects(claim(new AbortController().signal),(e:any)=>e.reason==='startup_unresolved');await assert.rejects(maintenance([profile],async()=>{}),{code:'PROFILE_RUNNING_OR_UNRESOLVED'});assert.ok((await readdir(profile)).includes('service-instance'));});
 assert.equal(starts,0);const owner=await claim(new AbortController().signal);assert.equal(owner.kind,'owner');if(owner.kind==='owner')await owner.release(new AbortController().signal);
});

test('local distribution is content-addressed and preserves complete runtime import/assets closure without private state',async t=>{
 const root=await fixture(t),a=await packDistribution(source,join(root,'a')),b=await packDistribution(source,join(root,'b'));
 assert.equal(a.schemaVersion,'paos_local_distribution_v1');assert.match(a.releaseId,/^[a-f0-9]{64}$/);assert.equal(a.releaseId,b.releaseId);
 assert.equal((await verifyDistribution(join(root,'a'),a.releaseId)).releaseId,a.releaseId);
 const paths=a.files.map((f:any)=>f.path);for(const name of ['apps/launcher/native-window.ps1','apps/local-service/src/storage/sqlite-worker.mts','apps/local-service/src/storage/restore-worker.mts','apps/local-service/src/import-export/source-freeze.ps1','apps/web/dist/index.html','apps/web/package-lock.json','packages/contracts/runtime/qualified-manifest.json','apps/desktop-local/main.mts'])assert.ok(paths.includes(name),name);
 assert.ok(!paths.some((p:string)=>/(?:\.codex|runtime-selection|state\.sqlite|auth\.json|\.exe)/i.test(p)));
 // Windows holds loaded .node DLLs until process exit, so the probe owns a separate process.
 const probe="const {createRequire}=await import('node:module');const {pathToFileURL}=await import('node:url');const require=createRequire(process.argv[1]);const path=require.resolve('rolldown/utils');const parser=await import(pathToFileURL(path).href);if(parser.parseSync('sample.ts','export const count:number=3',{lang:'ts',astType:'ts'}).errors.length)process.exitCode=1;console.log(path);";
 const parsed=await promisify(execFile)(process.execPath,['--input-type=module','-e',probe,join(root,'a/apps/web/package.json')],{timeout:10000,windowsHide:true});assert.ok(parsed.stdout.trim().startsWith(join(root,'a')));
 const {adapterRevision}=await import(pathToFileURL(join(root,'a/packages/contracts/runtime/manifest.mts')).href);assert.equal(await adapterRevision(),JSON.parse(await readFile(join(source,'packages/contracts/runtime/qualified-manifest.json'),'utf8')).adapterRevision);
});

test('tamper, unknown payload and missing files reject before installation; existing destinations remain untouched',async t=>{
 const root=await fixture(t),dir=join(root,'package'),m=await packDistribution(source,dir),dest=join(root,'existing');await mkdir(dest);await writeFile(join(dest,'user.txt'),'preserve');
 await assert.rejects(installDistribution(dir,dest,m.releaseId),{code:'DESTINATION_EXISTS'});assert.equal(await readFile(join(dest,'user.txt'),'utf8'),'preserve');
 await writeFile(join(dir,'apps/web/dist/index.html'),'tampered');await assert.rejects(installDistribution(dir,join(root,'bad'),m.releaseId),{code:'PACKAGE_INTEGRITY'});await assert.rejects(readFile(join(root,'bad/distribution.json')));
 const other=join(root,'other');await packDistribution(source,other);await writeFile(join(other,'credentials.json'),'not a real credential');await assert.rejects(verifyDistribution(other,m.releaseId),{code:'PACKAGE_INVENTORY'});
 await assert.rejects(verifyDistribution(other,'0'.repeat(64)),{code:'PACKAGE_ID_MISMATCH'});
});

test('linked parents and node_modules destinations cannot redirect package writes',async t=>{
 const root=await fixture(t),outside=join(root,'outside'),link=join(root,'link');await mkdir(outside);await symlink(outside,link,process.platform==='win32'?'junction':'dir');
 await assert.rejects(packDistribution(source,join(link,'package')),{code:'LINKED_PATH'});assert.deepEqual(await readdir(outside),[]);
 await assert.rejects(packDistribution(source,join(root,'node_modules/package')),{code:'PATH_INVALID'});
});

test('CLI rejects unknown and duplicate flags; an incompatible host cannot start or discover credentials',async t=>{
 await assert.rejects(desktopCommand(['install','--unknown','x']),/ARGUMENTS_INVALID/);await assert.rejects(desktopCommand(['status','--state','x','--state','y']),/ARGUMENTS_INVALID/);
 const root=await fixture(t),copy=join(root,'source'),m=await packDistribution(source,copy),pinPath=join(copy,'packages/contracts/runtime/qualified-manifest.json'),pin=JSON.parse(await readFile(pinPath,'utf8'));pin.node.version='v0.0.0';await writeFile(pinPath,JSON.stringify(pin));const bad=await packDistribution(copy,join(root,'incompatible')),profile=join(root,'profile');await mkdir(profile);const state=join(root,'selection');await selectInstallation(state,join(root,'incompatible'),bad.releaseId,profile,null);await assert.rejects(startSelection(state),{code:'HOST_PREREQUISITE_MISMATCH'});assert.deepEqual(await readdir(profile),[]);assert.equal((await readSelection(state))?.current.releaseId,bad.releaseId);assert.notEqual(bad.releaseId,m.releaseId);
});

test('offline backup restores into a new profile, preserves original and fences approval/outbox/cursors',async t=>{
 const root=await fixture(t),dir=join(root,'package'),m=await packDistribution(source,dir),profile=join(root,'profile');await mkdir(profile);
 const store=await openLocalStore({databasePath:join(profile,'state.sqlite')});let blob:any;
 try{await store.registerProject({id:'p',keyPrefix:'PKGT',canonicalRoot:root,rootIdentity:'fixture',authorityMode:'sql'});blob=await store.putBlob('p',Buffer.from('package pilot attachment'));
 await store.write({projectId:'p',actorId:'u',expectedAuthorityEpoch:1,idempotencyKey:'seed',changes:[{expectedRevision:0,entity:{id:'s',kind:'session'}},{expectedRevision:0,entity:{id:'m',kind:'message',parentId:'s',body:'Сохранённый текст',blobIds:[blob.id]}},{expectedRevision:0,entity:{id:'a',kind:'approval',status:'pending'}},{expectedRevision:0,entity:{id:'r',kind:'run',status:'running'}}],outbox:[{kind:'dispatch',payload:{runId:'r'}}]});}finally{await store.close();}
 const before=hash(await readFile(join(profile,'state.sqlite'))),backups=join(root,'backups');await mkdir(backups);const backup=await backupProfile(dir,m.releaseId,profile,backups),newProfile=join(root,'restored');await restoreProfile(dir,m.releaseId,backup.directory,newProfile);
 assert.equal(hash(await readFile(join(profile,'state.sqlite'))),before);assert.deepEqual((await readdir(newProfile)).sort(),['desktop-restore.json','state.sqlite','state.sqlite.blobs']);
 const restored=await openLocalStore({databasePath:join(newProfile,'state.sqlite')});assert.equal((await restored.get('p','m'))?.body,'Сохранённый текст');assert.equal((await restored.get('p','a'))?.status,'stale');assert.equal((await restored.get('p','r'))?.status,'recovery_required');assert.equal((await restored.outbox('p'))[0].state,'recovery_required');assert.equal((await readFile(join(newProfile,'state.sqlite.blobs',blob.id))).toString(),'package pilot attachment');await restored.close();
 await assert.rejects(restoreProfile(dir,m.releaseId,backup.directory,newProfile),{code:'DESTINATION_EXISTS'});await writeFile(join(backup.directory,'blobs',blob.id),'corrupt');await assert.rejects(restoreProfile(dir,m.releaseId,backup.directory,join(root,'rejected')),{code:'BLOB_HASH_MISMATCH'});assert.equal(hash(await readFile(join(profile,'state.sqlite'))),before);
});

test('package allowlist refuses misplaced private profile files and control state cannot be created inside an install',async t=>{
 const root=await fixture(t),dir=join(root,'package'),m=await packDistribution(source,dir);await writeFile(join(dir,'apps/desktop-local/auth.json'),'synthetic private-state marker');await assert.rejects(packDistribution(dir,join(root,'repacked')),{code:'PACKAGE_PRIVATE_STATE'});await rm(join(dir,'apps/desktop-local/auth.json'));
 const profile=join(root,'profile');await mkdir(profile);await assert.rejects(selectInstallation(join(dir,'control'),dir,m.releaseId,profile,null),{code:'PATH_OVERLAP'});assert.ok(!(await readdir(dir)).includes('control'));
});

test('selection is CAS guarded, refuses live profile and requires restored profile on switch/rollback',async t=>{
 const root=await fixture(t),dir=join(root,'package'),m=await packDistribution(source,dir),installed=join(root,'installed');await installDistribution(dir,installed,m.releaseId);const profile=join(root,'profile');await mkdir(profile);const state=join(root,'selection');
 const first=await selectInstallation(state,installed,m.releaseId,profile,null);assert.equal((await readSelection(state)).current.releaseId,m.releaseId);
 await assert.rejects(selectInstallation(state,installed,m.releaseId,profile,null),{code:'SELECTION_CONFLICT'});
 await mkdir(join(profile,'service-instance'));await assert.rejects(selectInstallation(state,installed,m.releaseId,join(root,'new'),first.digest),{code:'PROFILE_RUNNING_OR_UNRESOLVED'});await rm(join(profile,'service-instance'),{recursive:true});
 const other=join(root,'other');await mkdir(other);await assert.rejects(selectInstallation(state,installed,m.releaseId,other,first.digest),{code:'RESTORED_PROFILE_REQUIRED'});assert.equal((await readSelection(state)).digest,first.digest);
 const store=await openLocalStore({databasePath:join(profile,'state.sqlite')});await store.close();const backups=join(root,'backups');await mkdir(backups);const backup=await backupProfile(installed,m.releaseId,profile,backups),restored=join(root,'restored');await restoreProfile(installed,m.releaseId,backup.directory,restored);const selected=await selectInstallation(state,installed,m.releaseId,restored,first.digest);assert.equal(selected.previous.profileDirectory,profile);assert.equal(selected.current.profileDirectory,restored);
 const rollback=join(root,'rollback');await restoreProfile(installed,m.releaseId,backup.directory,rollback);const receipt=await selectInstallation(state,installed,m.releaseId,rollback,selected.digest);assert.equal(receipt.current.profileDirectory,rollback);assert.ok(await readFile(join(restored,'state.sqlite')));assert.ok(await readFile(join(profile,'state.sqlite')));
});

test('restored startup relocates only internal preference scope and preserves preferences and real project binding',async t=>{
 const root=await fixture(t),dir=join(root,'package'),m=await packDistribution(source,dir),profile=join(root,'profile'),restored=join(root,'restored'),backups=join(root,'backups');await mkdir(profile);await mkdir(backups);const store=await openLocalStore({databasePath:join(profile,'state.sqlite')});
 try{await store.registerProject({id:'_paos_profile',keyPrefix:'PREF',canonicalRoot:profile,rootIdentity:'profile:'+profile,authorityMode:'sql'});await store.registerProject({id:'real',keyPrefix:'REAL',canonicalRoot:root,rootIdentity:'real-fixture-root',authorityMode:'sql'});await store.write({projectId:'_paos_profile',actorId:'u',expectedAuthorityEpoch:1,idempotencyKey:'preferences',changes:[{expectedRevision:0,entity:{id:'ui-preferences',kind:'settings',data:{locale:'en',theme:'dark'}}}]});}finally{await store.close();}
 const before=hash(await readFile(join(profile,'state.sqlite'))),backup=await backupProfile(dir,m.releaseId,profile,backups);await restoreProfile(dir,m.releaseId,backup.directory,restored);using db=new DatabaseSync(join(restored,'state.sqlite'),{readOnly:true});const scope=db.prepare("SELECT * FROM projects WHERE id='_paos_profile'").get()!;assert.equal(scope.canonical_root,process.platform==='win32'?restored.toLowerCase():restored);assert.equal(scope.root_identity,'profile:'+restored);assert.equal(scope.authority_epoch,2);assert.equal(db.prepare("SELECT root_identity FROM projects WHERE id='real'").get()!.root_identity,'real-fixture-root');assert.deepEqual(JSON.parse(db.prepare("SELECT data FROM entities WHERE id='ui-preferences'").get()!.data as string),{locale:'en',theme:'dark'});assert.equal(hash(await readFile(join(profile,'state.sqlite'))),before);
});
