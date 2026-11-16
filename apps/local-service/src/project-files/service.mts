import type {LocalStore} from '../storage/local-store.mts';
import {inventoryForProject} from '../code-index/sources.mts';
import {normaliseRelativePath} from '../project-inventory/service.mts';
import {assertCurrentSourceProject} from '../project-inventory/scope.mts';
import type {ProjectFilesPage,ProjectFileRead,ProjectFileReference} from '../../../../packages/contracts/project-files.ts';
import type {InventoryEntry} from '../../../../packages/contracts/project-inventory.ts';

const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
/** The registry, not a browser-supplied root or policy, owns filesystem authority. */
export function createProjectFiles(store:LocalStore){
 async function project(id:string){const value=await store.project(id);if(!value)fail('PROJECT_NOT_FOUND');return value!;}
 async function stillCurrent(before:Awaited<ReturnType<typeof project>>){const current=await project(before.id);if(current.rootIdentity!==before.rootIdentity||current.canonicalRoot!==before.canonicalRoot)fail('PROJECT_ROOT_UNAVAILABLE');if(inventoryForProject(current).policyVersion!==inventoryForProject(before).policyVersion)fail('INVENTORY_POLICY_DRIFT');await inventoryForProject(current).assertProject(current);await assertCurrentSourceProject(store,before);}
 return {
  async list(projectId:string,params:URLSearchParams):Promise<ProjectFilesPage>{
   if([...params.keys()].some(key=>!['path','cursor','limit','filter','query'].includes(key))||[...new Set(params.keys())].some(key=>params.getAll(key).length!==1))fail('PROJECT_FILES_QUERY_INVALID');
   const limit=params.get('limit');if(limit!==null&&!/^\d+$/.test(limit))fail('PROJECT_FILES_QUERY_INVALID');
   const p=await project(projectId),page=await inventoryForProject(p).listDirectory(p,{path:params.get('path')??'',...(params.has('cursor')?{cursor:params.get('cursor')!}:{}),...(limit===null?{}:{limit:Number(limit)}),filter:(params.get('filter')??'all') as 'all'|'control_plane',query:params.get('query')??''});await stillCurrent(p);return page;
  },
  async read(projectId:string,input:{path:string;revision?:string;line?:number}):Promise<ProjectFileRead>{
   const path=normaliseRelativePath(input.path),line=input.line??1;
   if(input.revision!==undefined&&(typeof input.revision!=='string'||!/^[a-f0-9]{64}$/.test(input.revision))||!Number.isSafeInteger(line)||line<1||line>1000000)fail('PROJECT_FILES_QUERY_INVALID');
   const p=await project(projectId),inventory=inventoryForProject(p);await inventory.assertProject(p);
   let entry:InventoryEntry|undefined;
   const base=()=>({schemaVersion:'paos_project_file_v1' as const,projectId,rootIdentity:p.rootIdentity,policyVersion:inventory.policyVersion,relativePath:path,observedAt:new Date().toISOString(),line,...(entry?{entry,fileRevision:entry.revision}:{}),...(input.revision?{expectedRevision:input.revision}:{})});
   try{
    entry=await inventory.inspect(p,path);
    if(entry.kind!=='file')return {...base(),state:entry.kind==='directory'?'unsupported':'forbidden',content:null,reason:entry.access.reason??'unsupported_file'};
    if(!entry.access.readable)return {...base(),state:'forbidden',content:null,reason:entry.access.reason??'policy_excluded'};
    if(input.revision&&input.revision!==entry.revision)return {...base(),state:'stale',content:null,reason:'INVENTORY_REVISION_STALE'};
    // Display-only redaction never grants indexing or execution permission.
    const file=await inventory.read(p,{path,revision:input.revision??entry.revision,redactSensitive:true});
    await stillCurrent(p);const reference:ProjectFileReference={relativePath:path,revision:file.hash,revisionKind:'sha256',fileRevision:file.fileRevision,rootIdentity:p.rootIdentity,policyVersion:file.policyVersion,line};
    return {...base(),state:'available',content:file.text,hash:file.hash,redacted:file.redacted,fileRevision:file.fileRevision,reference};
   }catch(error){
    const code=String((error as {code?:string}).code??'FILE_UNAVAILABLE');
    if(['PROJECT_ROOT_UNAVAILABLE','INVENTORY_PATH_FORBIDDEN','INVENTORY_CANCELLED','INVENTORY_TIMEOUT'].includes(code))throw error;
    const state:Exclude<ProjectFileRead['state'],'available'>=['INVENTORY_REVISION_STALE','INVENTORY_SOURCE_DRIFT','INVENTORY_POLICY_DRIFT'].includes(code)?'stale':code==='INVENTORY_BINARY_FILE'?'binary':code==='INVENTORY_ENCODING_UNSUPPORTED'?'unsupported':code==='INVENTORY_FILE_TOO_LARGE'?'too_large':['INVENTORY_SOURCE_FORBIDDEN','INVENTORY_LINKED_SOURCE','INVENTORY_SENSITIVE_CONTENT'].includes(code)?'forbidden':'unavailable';
    return {...base(),state,content:null,reason:code};
   }
  },
 };
}
