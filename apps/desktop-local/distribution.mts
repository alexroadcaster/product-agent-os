import {createHash,randomUUID} from 'node:crypto';
import {lstat,readdir,readFile,mkdir,copyFile,rename,rm,rmdir,open,realpath} from 'node:fs/promises';
import {join,resolve,dirname,relative,isAbsolute,parse,sep} from 'node:path';
import {platform,arch,release} from 'node:os';
import {pathToFileURL} from 'node:url';
import {DatabaseSync} from 'node:sqlite';
type Entry={path:string;bytes:number;sha256:string};
type Manifest={schemaVersion:'paos_local_distribution_v1';version:string;releaseId:string;files:Entry[];runtimeDependencies:{name:string;version:string;license:string}[];adapterRevision:string;node:{version:string;sha256:string};sqliteVersion:string;platform:string;arch:string;windowsRelease:string};
type Target={installDirectory:string;releaseId:string;profileDirectory:string};
type Selection={schemaVersion:1;current:Target;previous:Target|null;digest:string};
const dependencyTrees=['rolldown','@rolldown/binding-win32-x64-msvc','@rolldown/pluginutils','@oxc-project/types'].map(n=>'apps/web/node_modules/'+n);
const trees=['apps/launcher','apps/local-service/src','packages/contracts','apps/web/dist','apps/desktop-local',...dependencyTrees];
const singles=['package.json','apps/local-service/package.json','apps/web/package.json','apps/web/package-lock.json','apps/web/src/design/preferences.ts'];
const required=['apps/launcher/main.mts','apps/launcher/native-window.ps1','apps/local-service/src/main.mts','apps/local-service/src/storage/sqlite-worker.mts','apps/local-service/src/storage/restore-worker.mts','apps/local-service/src/import-export/source-freeze.ps1','packages/contracts/runtime/qualified-manifest.json','apps/web/dist/index.html','apps/web/package-lock.json','apps/web/src/design/preferences.ts','apps/desktop-local/main.mts'];
const sha=(bytes:Uint8Array|string)=>createHash('sha256').update(bytes).digest('hex');
const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
const id=(v:unknown):v is string=>typeof v==='string'&&/^[0-9a-f]{64}$/.test(v);
function privateState(name:string){const dependency=dependencyTrees.find(p=>name.startsWith(p+'/'));if(name.endsWith('.node')&&!name.startsWith('apps/web/node_modules/@rolldown/binding-win32-x64-msvc/'))return true;return /(^|\/)(?:node_modules|\.git|\.codex|\.local|__pycache__|\.env(?:\.[^/]*)?|auth\.json|credentials\.json|runtime-selection\.json|profile[-.]identity\.json|desktop-restore\.json)(?:\/|$)|\.(?:sqlite(?:-(?:wal|shm))?|db|pem|key|exe|dll|pyc)$/i.test(dependency?name.slice(dependency.length+1):name);}
const allowed=(name:string)=>singles.includes(name)||trees.some(t=>name.startsWith(t+'/'));
const child=(parent:string,path:string)=>{const r=relative(parent,path);return r===''||r!=='..'&&!r.startsWith('..'+sep)&&!isAbsolute(r);};

/** Reject linked ancestors, UNC/device paths and unsupported node_modules TypeScript layout. */
async function checkedPath(input:string,exists=false,dependencyFile=false){
 if(typeof input!=='string'||!isAbsolute(input)||input.includes('\0')||!dependencyFile&&input.split(/[\\/]/).some(p=>p.toLowerCase()==='node_modules')||process.platform==='win32'&&(!/^[a-z]:[\\/]/i.test(input)||/[<>:"|?*]/.test(input.slice(3))))fail('PATH_INVALID');
 const path=resolve(input);let cursor=parse(path).root;for(const part of relative(cursor,path).split(sep).filter(Boolean)){cursor=join(cursor,part);try{if((await lstat(cursor)).isSymbolicLink())fail('LINKED_PATH');}catch(e){if((e as NodeJS.ErrnoException).code!=='ENOENT')throw e;}}
 if(exists)await lstat(path);return path;
}
async function fresh(path:string){await checkedPath(path);try{await lstat(path);fail('DESTINATION_EXISTS');}catch(e){if((e as NodeJS.ErrnoException).code!=='ENOENT')throw e;}}
async function walk(root:string):Promise<string[]>{const result:string[]=[];async function visit(dir:string){for(const item of await readdir(dir,{withFileTypes:true})){const p=join(dir,item.name),s=await lstat(p);if(s.isSymbolicLink()||s.isFile()&&s.nlink!==1)fail('LINKED_PATH');if(s.isDirectory())await visit(p);else if(s.isFile())result.push(relative(root,p).replaceAll('\\','/'));else fail('PACKAGE_INVENTORY');}}await visit(root);return result.sort();}
async function boundedJson(path:string,dependencyFile=false){await checkedPath(path,true,dependencyFile);const s=await lstat(path);if(!s.isFile()||s.nlink!==1||s.size>2*1024*1024)fail('METADATA_INVALID');try{const value=JSON.parse(await readFile(path,'utf8'));if(!value||typeof value!=='object'||Array.isArray(value))fail('METADATA_INVALID');return value;}catch{fail('METADATA_INVALID');}}
async function durable(path:string,value:unknown){const f=await open(path,'wx',0o600);try{await f.writeFile(JSON.stringify(value,null,2)+'\n');await f.sync();}finally{await f.close();}}
function manifestId(m:Manifest){const {releaseId:_ignored,...body}=m;return sha(JSON.stringify(body));}
async function stopped(profile:string){await checkedPath(profile);try{await lstat(join(profile,'service-instance'));fail('PROFILE_RUNNING_OR_UNRESOLVED');}catch(e){if((e as NodeJS.ErrnoException).code!=='ENOENT')throw e;}}
/** Share the launcher's atomic reservation, including direct launches and other selection directories. */
export async function withProfileMaintenance<T>(profiles:string[],operation:()=>Promise<T>){
 const paths=new Map<string,string>();for(const p of profiles){const path=await realpath(await checkedPath(p,true));paths.set(process.platform==='win32'?path.toLowerCase():path,path);}const owned:{path:string;ino:bigint;dev:bigint}[]=[];
 try{for(const profile of [...paths.values()].sort()){const path=join(profile,'service-instance');try{await mkdir(path,{mode:0o700});}catch(e){if((e as NodeJS.ErrnoException).code==='EEXIST')fail('PROFILE_RUNNING_OR_UNRESOLVED');throw e;}const identity=await lstat(path,{bigint:true});owned.push({path,ino:identity.ino,dev:identity.dev});}return await operation();}
 finally{for(const item of owned.reverse()){await checkedPath(item.path,true);const current=await lstat(item.path,{bigint:true});if(current.ino!==item.ino||current.dev!==item.dev||current.isSymbolicLink())fail('MAINTENANCE_OWNERSHIP_CHANGED');await rmdir(item.path);}}
}
async function copyInventory(source:string,destination:string,files:Entry[]){for(const f of files){const dest=join(destination,f.path);await mkdir(dirname(dest),{recursive:true});await copyFile(join(source,f.path),dest);}}

/** Preserve source structure and every byte participating in adapter qualification. */
export async function packDistribution(sourceInput:string,outputInput:string):Promise<Manifest>{
 const source=await checkedPath(sourceInput,true),output=await checkedPath(outputInput);await fresh(output);if(trees.some(t=>child(join(source,t),output)))fail('PATH_OVERLAP');
 const paths=[...singles];for(const tree of trees){await checkedPath(join(source,tree),true,dependencyTrees.includes(tree));for(const f of await walk(join(source,tree)))paths.push(tree+'/'+f);}
 const files:Entry[]=[];for(const path of paths.sort()){if(privateState(path))fail('PACKAGE_PRIVATE_STATE');await checkedPath(join(source,path),true,dependencyTrees.some(p=>path.startsWith(p+'/')));const s=await lstat(join(source,path));if(!s.isFile()||s.nlink!==1||s.size>64*1024*1024)fail('PACKAGE_INVENTORY');const b=await readFile(join(source,path));files.push({path,bytes:b.length,sha256:sha(b)});}
 const pin=await boundedJson(join(source,'packages/contracts/runtime/qualified-manifest.json'));const {adapterRevision}=await import(pathToFileURL(join(source,'packages/contracts/runtime/manifest.mts')).href);if(await adapterRevision(source)!==pin.adapterRevision)fail('ADAPTER_NOT_QUALIFIED');
 const lock=await boundedJson(join(source,'apps/web/package-lock.json')),runtimeDependencies=[];
 for(const tree of dependencyTrees){const name=tree.slice('apps/web/node_modules/'.length),metadata=await boundedJson(join(source,tree,'package.json'),true);if(metadata.name!==name||metadata.version!==lock.packages?.['node_modules/'+name]?.version)fail('DEPENDENCY_LOCK_MISMATCH');runtimeDependencies.push({name,version:String(metadata.version),license:String(metadata.license??'unknown')});}
 const body={schemaVersion:'paos_local_distribution_v1' as const,version:'0.1.0',files,runtimeDependencies,adapterRevision:pin.adapterRevision,node:pin.node,sqliteVersion:pin.sqliteVersion,platform:pin.platform,arch:pin.arch,windowsRelease:pin.windowsRelease};const manifest={...body,releaseId:sha(JSON.stringify(body))};
 await mkdir(output);try{await copyInventory(source,output,files);await durable(join(output,'distribution.json'),manifest);await verifyDistribution(output,manifest.releaseId);return manifest;}catch(e){await rm(output,{recursive:true,force:true});throw e;}
}

/** Expected digest must be reviewed separately; self-hashes do not establish publisher identity. */
export async function verifyDistribution(input:string,expectedId:string):Promise<Manifest>{
 if(!id(expectedId))fail('PACKAGE_ID_MISMATCH');const root=await checkedPath(input,true),m=await boundedJson(join(root,'distribution.json')) as Manifest;
 if(m.schemaVersion!=='paos_local_distribution_v1'||!Array.isArray(m.files)||m.files.length>2000||m.files.length<required.length||!Array.isArray(m.runtimeDependencies)||m.runtimeDependencies.length!==4||!id(m.adapterRevision)||!m.node||!id(m.node.sha256)||typeof m.node.version!=='string')fail('PACKAGE_INVENTORY');
 if(m.releaseId!==expectedId||manifestId(m)!==expectedId)fail('PACKAGE_ID_MISMATCH');const names=new Set<string>();let total=0;
 for(const f of m.files){if(!f||typeof f.path!=='string'||! /^[A-Za-z0-9_./@-]+$/.test(f.path)||f.path.split('/').some(p=>p===''||p==='.'||p==='..')||!allowed(f.path)||privateState(f.path)||names.has(f.path.toLowerCase())||!id(f.sha256)||!Number.isSafeInteger(f.bytes)||f.bytes<0||f.bytes>64*1024*1024)fail('PACKAGE_INVENTORY');names.add(f.path.toLowerCase());total+=f.bytes;}
 if(total>128*1024*1024||required.some(p=>!names.has(p)))fail('PACKAGE_INVENTORY');const actual=await walk(root);if(actual.length!==m.files.length+1||actual.some(p=>p!=='distribution.json'&&!names.has(p.toLowerCase())))fail('PACKAGE_INVENTORY');
 for(const f of m.files){const p=join(root,f.path);await checkedPath(p,true,dependencyTrees.some(t=>f.path.startsWith(t+'/')));const b=await readFile(p);if(b.length!==f.bytes||sha(b)!==f.sha256)fail('PACKAGE_INTEGRITY');}return m;
}

/** Install creates only a new local directory: no registry/PATH changes or overwrite. */
export async function installDistribution(packageInput:string,destinationInput:string,expectedId:string){
 const destination=await checkedPath(destinationInput);await fresh(destination);const source=await checkedPath(packageInput,true);if(child(source,destination)||child(destination,source))fail('PATH_OVERLAP');const m=await verifyDistribution(source,expectedId);await mkdir(destination);
 try{await copyInventory(source,destination,m.files);await copyFile(join(source,'distribution.json'),join(destination,'distribution.json'));await verifyDistribution(destination,expectedId);return {installDirectory:destination,releaseId:expectedId,systemInstalled:false};}catch(e){await rm(destination,{recursive:true,force:true});throw e;}
}
async function locked<T>(stateInput:string,action:(state:string)=>Promise<T>){const state=await checkedPath(stateInput);await mkdir(state,{recursive:true});let lock;try{lock=await open(join(state,'operation.lock'),'wx',0o600);}catch(e){if((e as NodeJS.ErrnoException).code==='EEXIST')fail('SELECTION_BUSY');throw e;}try{return await action(state);}finally{await lock.close();await rm(join(state,'operation.lock'));}}
export async function readSelection(stateInput:string):Promise<Selection|null>{
 const state=await checkedPath(stateInput);try{await lstat(join(state,'selection.json'));}catch(e){if((e as NodeJS.ErrnoException).code==='ENOENT')return null;throw e;}
 const value=await boundedJson(join(state,'selection.json')) as Selection;const {digest,...body}=value;if(value.schemaVersion!==1||!value.current||!id(value.current.releaseId)||!id(digest)||sha(JSON.stringify(body))!==digest)fail('SELECTION_INVALID');return value;
}

/** Upgrade/rollback select an explicitly restored copy; they never downgrade a live DB in place. */
export async function selectInstallation(stateInput:string,installInput:string,releaseId:string,profileInput:string,expectedCurrentDigest:string|null){
 const statePath=await checkedPath(stateInput),installPath=await checkedPath(installInput),profilePath=await checkedPath(profileInput);
 if(child(installPath,profilePath)||child(profilePath,installPath)||child(installPath,statePath)||child(profilePath,statePath)||child(statePath,profilePath)||child(statePath,installPath))fail('PATH_OVERLAP');
 return locked(stateInput,async state=>{const previous=await readSelection(state);if((previous?.digest??null)!==expectedCurrentDigest)fail('SELECTION_CONFLICT');if(previous)await stopped(previous.current.profileDirectory);
  const install=await checkedPath(installInput,true);await verifyDistribution(install,releaseId);const profile=await checkedPath(profileInput,true);await stopped(profile);
  if(child(install,profile)||child(profile,install)||child(install,state)||child(profile,state)||child(state,profile)||child(state,install))fail('PATH_OVERLAP');
  return withProfileMaintenance(previous?[previous.current.profileDirectory,profile]:[profile],async()=>{
  if(previous){if(await realpath(profile)===await realpath(previous.current.profileDirectory))fail('RESTORED_PROFILE_REQUIRED');let r;try{r=await boundedJson(join(profile,'desktop-restore.json'));}catch{fail('RESTORED_PROFILE_REQUIRED');}if(r.releaseId!==releaseId||r.databaseSha256!==sha(await readFile(join(profile,'state.sqlite'))))fail('RESTORED_PROFILE_REQUIRED');}
  const body={schemaVersion:1 as const,current:{installDirectory:install,releaseId,profileDirectory:profile},previous:previous?.current??null},next={...body,digest:sha(JSON.stringify(body))};const temp=join(state,'selection-'+randomUUID()+'.next');await durable(temp,next);try{await rename(temp,join(state,'selection.json'));}finally{await rm(temp,{force:true});}return next;});
 });
}

/** Read-only SQLite snapshot excludes workspace, identity, credentials and runtime auth. */
export async function backupProfile(install:string,releaseId:string,profileInput:string,outputInput:string){
 await verifyDistribution(install,releaseId);const profile=await checkedPath(profileInput,true),output=await checkedPath(outputInput,true);if(child(resolve(install),profile)||child(profile,resolve(install))||child(resolve(install),output)||child(profile,output))fail('PATH_OVERLAP');await stopped(profile);const dbPath=await checkedPath(join(profile,'state.sqlite'),true);const blobs=join(profile,'state.sqlite.blobs');try{await checkedPath(blobs,true);await walk(blobs);}catch(e){if((e as NodeJS.ErrnoException).code!=='ENOENT')throw e;}
 return withProfileMaintenance([profile],async()=>{const {createSnapshot}=await import(pathToFileURL(join(install,'apps/local-service/src/storage/snapshot.mts')).href);using db=new DatabaseSync(dbPath,{readOnly:true});const result=await createSnapshot(db,dbPath,output);return {...result,sourceReleaseId:releaseId,credentialsIncluded:false};});
}

/** Restore validates existing snapshot format into a new profile; identity is recreated on first start. */
export async function restoreProfile(install:string,releaseId:string,backupInput:string,profileInput:string){
 await verifyDistribution(install,releaseId);const backup=await checkedPath(backupInput,true),profile=await checkedPath(profileInput);await fresh(profile);await walk(backup);if(child(backup,profile)||child(profile,backup)||child(resolve(install),profile)||child(profile,resolve(install)))fail('PATH_OVERLAP');const {restoreLocalBackup}=await import(pathToFileURL(join(install,'apps/local-service/src/storage/local-store.mts')).href);await mkdir(profile);
 try{return await withProfileMaintenance([profile],async()=>{const restored=await restoreLocalBackup(backup,join(profile,'state.sqlite'));
  // Only this private bookkeeping scope follows the profile directory; real workspace bindings never move.
  {using db=new DatabaseSync(join(profile,'state.sqlite'));const row=db.prepare("SELECT * FROM projects WHERE id='_paos_profile'").get();if(row){const normalize=(p:string)=>process.platform==='win32'?p.toLowerCase():p;
   if(row.key_prefix!=='PREF'||row.authority_mode!=='sql'||typeof row.root_identity!=='string'||!row.root_identity.startsWith('profile:')||normalize(row.root_identity.slice(8))!==row.canonical_root)fail('RESTORE_PROFILE_METADATA_INVALID');
   const canonical=await realpath(profile);db.exec('BEGIN IMMEDIATE');try{db.prepare("UPDATE projects SET canonical_root=?,root_identity=?,authority_epoch=authority_epoch+1 WHERE id='_paos_profile'").run(normalize(canonical),'profile:'+canonical);db.exec('COMMIT');}catch(error){db.exec('ROLLBACK');throw error;}
  }}
  const receipt={schemaVersion:1,releaseId,backupId:restored.backupId,databaseSha256:sha(await readFile(join(profile,'state.sqlite'))),credentialsIncluded:false,requiresRestart:true,activeProfileChanged:false};await durable(join(profile,'desktop-restore.json'),receipt);return receipt;});}catch(e){
  // A concurrent launcher or a completed partial restore may own data now; remove only an empty new directory.
  try{await rmdir(profile);}catch{}throw e;
 }
}

/** Hold the selection lock for the owned launcher lifetime, fencing concurrent switches. */
export async function startSelection(stateInput:string,showWindow?:Parameters<typeof import('../launcher/main.mts').runNativeLauncher>[0]['showWindow']){
 return locked(stateInput,async state=>{const selection=await readSelection(state);if(!selection)return fail('SELECTION_REQUIRED');const target=selection.current,m=await verifyDistribution(target.installDirectory,target.releaseId);
  if(process.version!==m.node.version||sha(await readFile(process.execPath))!==m.node.sha256||process.versions.sqlite!==m.sqliteVersion||platform()!==m.platform||arch()!==m.arch||release()!==m.windowsRelease)fail('HOST_PREREQUISITE_MISMATCH');
  const {runNativeLauncher}=await import(pathToFileURL(join(target.installDirectory,'apps/launcher/main.mts')).href);return runNativeLauncher({profileDirectory:target.profileDirectory,...(showWindow?{showWindow}:{})});
 });
}
