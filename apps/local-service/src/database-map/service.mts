import {resolve} from 'node:path';
import {lstat} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {inventoryScopeFingerprint} from '../project-inventory/scope.mts';
import {normaliseRelativePath} from '../project-inventory/service.mts';
import {acquireDatabaseLease} from './lease.mts';
import {runSchemaExtractor} from './runner.mts';
import {databaseMermaid,databaseEntityId} from './mermaid.mts';
import type {ScanAnalyzerContext} from '../project-scans/service.mts';
import {inventoryForProject,type SourceProject} from '../code-index/sources.mts';
import type {DatabaseMapLimits,DatabaseMapStatus,DatabaseMapSource,DatabaseSchemaSnapshot,DatabaseMapPage,DatabaseSchemaChanges} from '../../../../packages/contracts/database-map.ts';
export type DatabaseMapStore={project(id:string):Promise<SourceProject|null>;readProjectState(id:string,namespace:'project_database_schema_v1'):Promise<{version:number;value:unknown}|null>;writeProjectState(id:string,namespace:'project_database_schema_v1',expectedVersion:number,value:unknown):Promise<{version:number;value:unknown}>};
export const DATABASE_MAP_LIMITS:DatabaseMapLimits=Object.freeze({fileBytes:128*1024*1024,tables:200,columns:4096,foreignKeys:1024,indexParts:4096,milliseconds:5000,outputBytes:512*1024,leaseMilliseconds:15000});
const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
type RecordState={schemaVersion:'paos_database_schema_record_v1';source:DatabaseMapSource|null;state:DatabaseMapStatus['state'];reasons:string[];snapshots:DatabaseSchemaSnapshot[]};
const empty=():RecordState=>({schemaVersion:'paos_database_schema_record_v1',source:null,state:'unselected',reasons:[],snapshots:[]});
/** Only profile metadata is durable. This service never accepts SQL or connection credentials. */
export function createDatabaseMap(options:{store:DatabaseMapStore;profileDatabasePath?:string;limits?:Partial<DatabaseMapLimits>;powershellExecutable?:string}){
 const {store}=options,limits={...DATABASE_MAP_LIMITS,...options.limits};
 for(const [key,value] of Object.entries(limits))if(!(key in DATABASE_MAP_LIMITS)||!Number.isSafeInteger(value)||value<1||value>DATABASE_MAP_LIMITS[key as keyof DatabaseMapLimits])fail('DATABASE_MAP_LIMIT_INVALID');
 async function project(id:string){const p=await store.project(id);if(!p)fail('PROJECT_NOT_FOUND');return p!;}
 async function saved(id:string){const row=await store.readProjectState(id,'project_database_schema_v1');if(!row)return {version:0,value:empty()};const v=row.value as RecordState;if(!v||v.schemaVersion!=='paos_database_schema_record_v1'||!['unselected','selected','ready','partial','stale','unavailable'].includes(v.state)||!Array.isArray(v.reasons)||v.reasons.some(r=>typeof r!=='string')||!Array.isArray(v.snapshots)||v.snapshots.length>2||v.snapshots.some(s=>s.schemaVersion!=='paos_database_schema_v1'||s.projectId!==id||!Array.isArray(s.tables)||s.tables.length>limits.tables||!Array.isArray(s.reasons)||s.tables.some(t=>!Array.isArray(t.columns)||!Array.isArray(t.foreignKeys)||!Array.isArray(t.indexes)))||v.source!==null&&(!v.source||typeof v.source.relativePath!=='string'||typeof v.source.scopeFingerprint!=='string'||typeof v.source.fileRevision!=='string'))fail('DATABASE_MAP_STATE_UNAVAILABLE');return {version:row.version,value:v};}
 async function profileFile(path:string){if(!options.profileDatabasePath)return false;const a=resolve(path),b=resolve(options.profileDatabasePath);if((process.platform==='win32'?a.toLowerCase():a)===(process.platform==='win32'?b.toLowerCase():b))return true;try{const [x,y]=await Promise.all([lstat(a,{bigint:true}),lstat(b,{bigint:true})]);return x.dev===y.dev&&x.ino===y.ino;}catch{return false;}}

 let active=false;
 const hash=(v:unknown)=>createHash('sha256').update(JSON.stringify(v)).digest('hex');
 async function current(p:SourceProject){const now=await project(p.id);if(inventoryScopeFingerprint(now)!==inventoryScopeFingerprint(p))fail('PROJECT_SCOPE_STALE');await inventoryForProject(now).assertProject(now);}
 async function admit(p:SourceProject,path:string,revision?:string){
  if(await profileFile(resolve(p.canonicalRoot,path)))fail('DATABASE_PROFILE_SOURCE_FORBIDDEN');
  // Dedicated capability permits only offline SQLite metadata admission; generic
  // source reads retain database_content denial. Native lease precedes SQLite.
  return inventoryForProject(p).admitDatabaseSource(p,{path,revision,maxBytes:limits.fileBytes});
 }
 async function state(id:string){const p=await project(id),row=await saved(id);let state=row.value.state,reasons=[...row.value.reasons];
  if(row.value.source)try{if(row.value.source.scopeFingerprint!==inventoryScopeFingerprint(p))fail('DATABASE_SOURCE_SCOPE_STALE');await admit(p,row.value.source.relativePath,row.value.source.fileRevision);await current(p);}catch(error){state='stale';reasons=[String((error as any).code??'DATABASE_SOURCE_UNAVAILABLE')];}
  return {p,row,state,reasons};
 }
 async function finalRead(result:Awaited<ReturnType<typeof state>>){await current(result.p);const latest=await saved(result.p.id);if(latest.version!==result.row.version||hash(latest.value.source)!==hash(result.row.value.source)||hash(latest.value.snapshots.map(s=>s.revision))!==hash(result.row.value.snapshots.map(s=>s.revision)))fail('DATABASE_SOURCE_SELECTION_STALE');}
 async function status(id:string):Promise<DatabaseMapStatus>{
  const observedState=await state(id),{p,row,state:observed,reasons}=observedState,inventory=await inventoryForProject(p).snapshot(p),candidates=[] as DatabaseMapStatus['candidates'];
  for(const e of inventory.entries)if(e.kind==='file'&&/\.(db|sqlite|sqlite3)$/i.test(e.relativePath)&&!await profileFile(resolve(p.canonicalRoot,e.relativePath)))candidates.push({relativePath:e.relativePath,fileRevision:e.revision,...(e.access.reason?{reason:e.access.reason}:{})});
  await finalRead(observedState);return {schemaVersion:'paos_database_map_v1',projectId:id,version:row.version,state:process.platform!=='win32'&&row.value.source?'unavailable':observed,source:row.value.source,snapshotRevision:row.value.snapshots.at(-1)?.revision??null,reasons:[...reasons,...(process.platform!=='win32'?['DATABASE_LEASE_UNAVAILABLE']:[])],candidates,candidateCoverage:inventory.coverage,limits};
 }
 async function selectSource(id:string,input:{relativePath:string;expectedFileRevision:string;expectedVersion:number}|{clear:true;expectedVersion:number}){
  if(!input||typeof input!=='object'||Array.isArray(input)||!Number.isSafeInteger(input.expectedVersion)||input.expectedVersion<0)fail('DATABASE_MAP_INPUT_INVALID');
  const p=await project(id),row=await saved(id);if(row.version!==input.expectedVersion)fail('PROJECT_STATE_CONFLICT');
  if('clear' in input){if(input.clear!==true||Object.keys(input).some(k=>!['clear','expectedVersion'].includes(k)))fail('DATABASE_MAP_INPUT_INVALID');await current(p);await store.writeProjectState(id,'project_database_schema_v1',row.version,empty());return status(id);}
  if(Object.keys(input).some(k=>!['relativePath','expectedFileRevision','expectedVersion'].includes(k))||typeof input.expectedFileRevision!=='string'||!/^[a-f0-9]{64}$/.test(input.expectedFileRevision))fail('DATABASE_MAP_INPUT_INVALID');
  const relativePath=normaliseRelativePath(input.relativePath),entry=await admit(p,relativePath,input.expectedFileRevision);await current(p);
  const source:DatabaseMapSource={relativePath,fileRevision:entry.fileRevision,rootIdentity:p.rootIdentity,policyVersion:entry.policyVersion,scopeFingerprint:inventoryScopeFingerprint(p)};
  const keep=row.value.source?.relativePath===relativePath&&row.value.source?.scopeFingerprint===source.scopeFingerprint;
  await store.writeProjectState(id,'project_database_schema_v1',row.version,{schemaVersion:'paos_database_schema_record_v1',source,state:'selected',reasons:[],snapshots:keep?row.value.snapshots:[]} satisfies RecordState);return status(id);
 }
 async function analyzer(context:ScanAnalyzerContext){
  const {project:p,signal}=context,row=await saved(p.id),source=row.value.source;
  if(!source)return {state:'unavailable' as const,reasons:['DATABASE_SOURCE_NOT_SELECTED']};
  if(active)return {state:'unavailable' as const,reasons:['DATABASE_SCHEMA_BUSY']};active=true;
  const guard=async()=>{if(signal.aborted||!context.canPublish())fail('DATABASE_SCHEMA_CANCELLED');await current(p);const now=await saved(p.id);if(now.version!==row.version||hash(now.value.source)!==hash(source))fail('DATABASE_SOURCE_SELECTION_STALE');if(source.scopeFingerprint!==inventoryScopeFingerprint(p))fail('DATABASE_SOURCE_SCOPE_STALE');await admit(p,source.relativePath,source.fileRevision);await context.publicationGuard();if(signal.aborted||!context.canPublish())fail('DATABASE_SCHEMA_CANCELLED');if((await saved(p.id)).version!==row.version)fail('DATABASE_SOURCE_SELECTION_STALE');};
  let lease:Awaited<ReturnType<typeof acquireDatabaseLease>>|undefined;
  try{
   await guard();const path=resolve(p.canonicalRoot,source.relativePath);
   lease=await acquireDatabaseLease({root:p.canonicalRoot,path,milliseconds:limits.leaseMilliseconds,signal,powershellExecutable:options.powershellExecutable});
   // Recheck Node stat, root and policy after native readiness before opening SQLite.
   await guard();let leaseLost=false;void lease.lost.then(()=>{leaseLost=true;});
   const extracted=await runSchemaExtractor(path,limits,lease,signal);if(leaseLost)fail('DATABASE_LEASE_LOST');await guard();
   const snapshot:DatabaseSchemaSnapshot={schemaVersion:'paos_database_schema_v1',projectId:p.id,rootIdentity:p.rootIdentity,policyVersion:source.policyVersion,inventoryRevision:context.inventory.revision,fileRevision:source.fileRevision,relativePath:source.relativePath,revision:hash([source,extracted.revision]),observedAt:new Date().toISOString(),coverage:extracted.reasons.length?'partial':'complete',reasons:extracted.reasons,tables:extracted.tables,normalizationVersion:'sqlite_metadata_v2_effective_nullable',adapterVersion:'offline_sqlite_lease_v1'};
   if(Buffer.byteLength(JSON.stringify(snapshot))>limits.outputBytes)fail('DATABASE_SCHEMA_OUTPUT_LIMIT');
   const snapshots=[...row.value.snapshots.filter(s=>s.revision!==snapshot.revision),snapshot].slice(-2);
   await guard();if(leaseLost||!context.canPublish()||signal.aborted)fail('DATABASE_SCHEMA_CANCELLED');await store.writeProjectState(p.id,'project_database_schema_v1',row.version,{...row.value,state:snapshot.coverage==='complete'?'ready':'partial',reasons:snapshot.reasons,snapshots});
   return {state:snapshot.coverage==='complete'?'completed' as const:'partial' as const,reasons:snapshot.reasons,counts:{tables:snapshot.tables.length,columns:snapshot.tables.reduce((n,t)=>n+t.columns.length,0)},data:{snapshotRevision:snapshot.revision,rootIdentity:snapshot.rootIdentity,policyVersion:snapshot.policyVersion,inventoryRevision:snapshot.inventoryRevision,...(extracted.metrics?{metrics:extracted.metrics}:{})}};
  }catch(error){
   const code=String((error as any).code??'DATABASE_SCHEMA_UNAVAILABLE');
   if(signal.aborted||!context.canPublish()||/CANCELLED|SELECTION_STALE|PROJECT_SCOPE_STALE/.test(code))throw error;
   try{await current(p);const now=await saved(p.id);if(now.version===row.version)await store.writeProjectState(p.id,'project_database_schema_v1',row.version,{...row.value,state:/STALE|DRIFT|FORBIDDEN/.test(code)?'stale':'unavailable',reasons:[code]});}catch{}
   return {state:'unavailable' as const,reasons:[code]};
  }finally{try{await lease?.release();}finally{active=false;}}
 }
 async function snapshot(id:string,query:URLSearchParams=new URLSearchParams()):Promise<DatabaseMapPage>{
  if([...query.keys()].some(k=>!['revision','query','table','limit','cursor'].includes(k))||[...new Set(query.keys())].some(k=>query.getAll(k).length!==1))fail('DATABASE_MAP_QUERY_INVALID');
  const result=await state(id),value=result.row.value.snapshots.at(-1);if(!value)fail('DATABASE_SCHEMA_NOT_OBSERVED');if(!result.row.value.source||result.row.value.source.scopeFingerprint!==inventoryScopeFingerprint(result.p)||value!.rootIdentity!==result.p.rootIdentity||value!.policyVersion!==inventoryForProject(result.p).policyVersion||value!.relativePath!==result.row.value.source.relativePath)fail('DATABASE_SOURCE_SCOPE_STALE');
  const stale=result.state==='stale'||value!.fileRevision!==result.row.value.source!.fileRevision;
  const revision=query.get('revision');if(revision&&revision!==value!.revision)fail('DATABASE_SCHEMA_REVISION_STALE');
  const search=query.get('query')??'',table=query.get('table'),limit=Number(query.get('limit')??50);if(search.length>256||!Number.isSafeInteger(limit)||limit<1||limit>200)fail('DATABASE_MAP_QUERY_INVALID');
  const binding=hash([id,value!.revision,search,table,limit]);let offset=0;if(query.has('cursor'))try{const cursor=JSON.parse(Buffer.from(query.get('cursor')!,'base64url').toString());if(cursor.binding!==binding||!Number.isSafeInteger(cursor.offset)||cursor.offset<0)fail('DATABASE_MAP_CURSOR_STALE');offset=cursor.offset;}catch{fail('DATABASE_MAP_CURSOR_STALE');}
  const selected=value!.tables.filter(t=>(!table||t.name===table)&&(!search||t.name.toLowerCase().includes(search.toLowerCase())||t.columns.some(c=>c.name.toLowerCase().includes(search.toLowerCase())))),tables=selected.slice(offset,offset+limit),{tables:ignored,...meta}=value!;
  const output={state:stale?'stale' as const:'current' as const,reasons:stale?[...new Set([...result.reasons,'DATABASE_SCHEMA_SOURCE_STALE'])]:value!.reasons,snapshot:meta,tables,total:selected.length,nextCursor:offset+limit<selected.length?Buffer.from(JSON.stringify({binding,offset:offset+limit})).toString('base64url'):null,mermaid:databaseMermaid(tables),diagramEntities:tables.map(t=>({id:databaseEntityId(t.name),name:t.name}))};if(Buffer.byteLength(JSON.stringify(output))>limits.outputBytes)fail('DATABASE_SCHEMA_OUTPUT_LIMIT');await finalRead(result);return output;
 }
 async function changes(id:string):Promise<DatabaseSchemaChanges>{
  const result=await state(id),[before,after]=result.row.value.snapshots.slice(-2),blank={beforeRevision:before?.revision??null,afterRevision:after?.revision??before?.revision??null,added:[] as string[],removed:[] as string[],changed:[] as string[]};
  await finalRead(result);
  if(!before||!after)return {state:'unavailable',reason:'DATABASE_SCHEMA_BASELINE_NOT_OBSERVED',...blank,beforeRevision:null};
  const compatible=before.projectId===after.projectId&&before.projectId===id&&before.rootIdentity===after.rootIdentity&&after.rootIdentity===result.p.rootIdentity&&before.policyVersion===after.policyVersion&&after.policyVersion===inventoryForProject(result.p).policyVersion&&before.relativePath===after.relativePath&&after.relativePath===result.row.value.source?.relativePath&&before.normalizationVersion===after.normalizationVersion&&before.adapterVersion===after.adapterVersion&&result.row.value.source?.scopeFingerprint===inventoryScopeFingerprint(result.p);
  if(!compatible)return {state:'incompatible',reason:'DATABASE_SCHEMA_REBASELINE_REQUIRED',...blank};
  const a=new Map(before.tables.map(t=>[t.name,t])),b=new Map(after.tables.map(t=>[t.name,t]));
  return {state:result.state==='stale'||after.fileRevision!==result.row.value.source?.fileRevision?'stale':'available',beforeRevision:before.revision,afterRevision:after.revision,added:[...b.keys()].filter(k=>!a.has(k)),removed:[...a.keys()].filter(k=>!b.has(k)),changed:[...b.keys()].filter(k=>a.has(k)&&hash(a.get(k))!==hash(b.get(k)))};
 }
 return {status,selectSource,analyzer,snapshot,changes};
}
