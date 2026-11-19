export type FileSnapshot={path:string;kind:'missing'|'present'|'excluded';sha256?:string;fileRevision?:string;content?:string};
export type FileChange={kind:'actual';path:string;operation:'add'|'modify'|'delete';diff:string;beforeSha256?:string;afterSha256?:string};
import {createHash} from 'node:crypto';
import {inventoryForProject,type SourceProject} from '../code-index/sources.mts';
import {normaliseRelativePath} from '../project-inventory/service.mts';
import {EXECUTION_FILE_LIMITS,type ExecutionFileProject,type ExecutionFileRequest,type ExecutionFileOperation,type FilePreflight,type FilePreflightItem} from '../../../../packages/contracts/runtime/file-preflight.ts';
const fail=(code:string):never=>{throw Object.assign(new Error('The saved task file is unavailable.'),{code});};
const digest=(value:unknown)=>createHash('sha256').update(JSON.stringify(value)).digest('hex');
const scrub=(value:string)=>value.replace(/sk-[A-Za-z0-9_-]+/g,'[REDACTED]').replace(/^(\s*(?:OPENAI_API_KEY|ANTHROPIC_API_KEY|AWS_SECRET_ACCESS_KEY|PRIVATE_KEY|ACCESS_TOKEN|REFRESH_TOKEN|PASSWORD|CLIENT_SECRET|_AUTHTOKEN)\s*[:=]).+$/gim,'$1 [REDACTED]')
 .replace(/("(?:access_token|refresh_token|password|client_secret|_authToken)"\s*:\s*)"(?:[^"\\]|\\.)*"/gi,'$1"[REDACTED]"');
function sourceProject(project:ExecutionFileProject):SourceProject{return 'canonicalRoot' in project?{id:project.id??'task-files',canonicalRoot:project.canonicalRoot,rootIdentity:project.rootIdentity,inventoryPolicy:project.inventoryPolicy}:{id:project.projectId??'task-files',canonicalRoot:project.workspaceRoot,rootIdentity:project.directoryIdentity,inventoryPolicy:project.inventoryPolicy};}
type Expanded={item:FilePreflightItem;revision?:string|null;fileRevision?:string|null};
const operations=new Set<ExecutionFileOperation>(['read','create','modify','delete','rename','create_or_modify_after_discovery','create_or_modify']);
function expand(files:readonly ExecutionFileRequest[],validateOperations:boolean):Expanded[]{
 if(!Array.isArray(files)||files.length>1000)fail('task_file_budget_exceeded');const rows:Expanded[]=[],seen=new Map<string,FilePreflightItem>();
 for(const request of files){
  const requested=request?.plannedOperation??'read',operation=operations.has(requested)?requested:'read';
  const append=(value:unknown,role:FilePreflightItem['role'],pins:boolean)=>{
   let path=typeof value==='string'?value.slice(0,2048):'<invalid>',invalid=false;try{path=normaliseRelativePath(value as string);}catch{invalid=true;}
   const item:FilePreflightItem={path,operation,role,state:invalid?'invalid':'not_checked',allowed:false,...(invalid?{reason:'path_invalid'}:{})};
   if(validateOperations&&!operations.has(requested)){item.state='invalid';item.reason='operation_invalid';}
   if(pins&&[request?.revision,request?.fileRevision].some(pin=>pin!=null&&(typeof pin!=='string'||!/^[a-f0-9]{64}$/.test(pin)))){item.state='invalid';item.reason='revision_invalid';}
   const key=process.platform==='win32'?path.toLowerCase():path,previous=seen.get(key);if(previous){previous.state='invalid';previous.reason='path_duplicate';item.state='invalid';item.reason='path_duplicate';}else seen.set(key,item);
   rows.push({item,...(pins?{revision:request?.revision,fileRevision:request?.fileRevision}:{})});
  };
  if(operation==='rename'){append(request?.previousRelativePath,'rename_source',true);append(request?.relativePath,'rename_destination',false);}
  else append(request?.relativePath,'target',true);
 }return rows;
}
type Observation={snapshot:FileSnapshot;byteSize?:number;reason?:string;fileRevision?:string;redacted?:boolean};
/** One checked inspector owns both admission metadata and private before/after
 * observations. Capture deliberately does not validate planned operations. */
async function observe(project:SourceProject,path:string,remaining:number,redact:(text:string)=>string):Promise<Observation>{
 const inventory=inventoryForProject(project),excluded=(reason:string,byteSize?:number):Observation=>({snapshot:{path,kind:'excluded'},byteSize,reason});let byteSize:number|undefined;
 try{
  const access=await inventory.access(project,path);if(!access.allowed)return excluded(access.reason??'policy_excluded');
  if(!access.exists)return {snapshot:{path,kind:'missing'},byteSize:0,fileRevision:access.revision};
  const metadata=await inventory.inspect(project,path);byteSize=metadata.byteSize;
  if(metadata.kind!=='file'||!metadata.access.readable)return excluded(metadata.access.reason??'not_regular_file',byteSize);
  if(byteSize>EXECUTION_FILE_LIMITS.fileBytes)return excluded('file_byte_limit',byteSize);
  if(byteSize>remaining)return excluded('total_byte_limit',byteSize);
  const file=await inventory.read(project,{path,revision:metadata.revision,maxBytes:EXECUTION_FILE_LIMITS.fileBytes,redactSensitive:true});
  const display=file.redacted?file.text.replaceAll('[redacted]','[REDACTED]'):file.text;
  return {snapshot:{path,kind:'present',sha256:file.hash,fileRevision:file.fileRevision,content:redact(scrub(display))},byteSize:file.byteSize,fileRevision:file.fileRevision,redacted:file.redacted};
 }catch(error){const code=String((error as {code?:string}).code??'source_unavailable');if(code==='PROJECT_ROOT_UNAVAILABLE')fail('project_root_changed');if(code==='ENOENT')return {snapshot:{path,kind:'missing'},byteSize:0};
  const reasons:Record<string,string>={INVENTORY_LINKED_SOURCE:'linked_source',INVENTORY_FILE_TOO_LARGE:'file_byte_limit',INVENTORY_BINARY_FILE:'binary_file',INVENTORY_ENCODING_UNSUPPORTED:'encoding_unsupported',INVENTORY_SENSITIVE_CONTENT:'sensitive_content',INVENTORY_SOURCE_DRIFT:'revision_changed',INVENTORY_POLICY_DRIFT:'policy_changed',INVENTORY_REVISION_STALE:'revision_changed',INVENTORY_SOURCE_FORBIDDEN:'policy_excluded',EACCES:'unreadable',EPERM:'unreadable'};
  return excluded(reasons[code]??'source_unavailable',byteSize);
 }
}
/** Read only selected task files. New post-command targets are observations,
 * not invalid create operations; their policy/root/budget checks still apply. */
export async function captureTaskFiles(binding:ExecutionFileProject,files:readonly ExecutionFileRequest[],redact:(text:string)=>string=value=>value):Promise<FileSnapshot[]>{
 const selected=expand(files,false);if(files.length>EXECUTION_FILE_LIMITS.files||selected.length>EXECUTION_FILE_LIMITS.files)fail('task_file_budget_exceeded');if(selected.some(row=>row.item.state==='invalid'))fail('task_file_path_invalid');
 const project=sourceProject(binding),inventory=inventoryForProject(project);try{await inventory.assertProject(project);}catch{fail('project_root_changed');}
 const rows:FileSnapshot[]=[];let total=0;for(const {item} of selected){const observed=await observe(project,item.path,EXECUTION_FILE_LIMITS.totalBytes-total,redact);rows.push(observed.snapshot);if(observed.snapshot.kind==='present')total+=observed.byteSize??0;}
 try{await inventory.assertProject(project);}catch{fail('project_root_changed');}return rows;
}

/** Metadata-only execution admission; no source bytes or diffs enter this report.
 * Root endpoint owns task revision/CAS, and dispatch must re-run this inspector. */
export async function preflightTaskFiles(binding:ExecutionFileProject,files:readonly ExecutionFileRequest[]):Promise<FilePreflight>{
 const project=sourceProject(binding),inventory=inventoryForProject(project),selected=expand(files,true),items=selected.map(row=>row.item),globalReasons:string[]=[];let total=0;
 if(files.length>EXECUTION_FILE_LIMITS.files||items.length>EXECUTION_FILE_LIMITS.files){globalReasons.push('file_count_limit');for(const item of items)if(item.state!=='invalid')item.reason='file_count_limit';}
 else{
  try{await inventory.assertProject(project);}catch{globalReasons.push('project_root_changed');}
  if(!globalReasons.length)for(const row of selected){const item=row.item;if(item.state==='invalid')continue;
   let observed:Observation;try{observed=await observe(project,item.path,EXECUTION_FILE_LIMITS.totalBytes-total,value=>value);}catch{item.state='excluded';item.reason='project_root_changed';globalReasons.push('project_root_changed');continue;}total+=observed.byteSize??0;item.byteSize=observed.byteSize;item.fileRevision=observed.fileRevision;
   if(observed.snapshot.kind==='excluded'){item.state=['revision_changed','policy_changed'].includes(observed.reason??'')?'stale':'excluded';item.reason=observed.reason;continue;}
   item.state=observed.snapshot.kind;item.sha256=observed.snapshot.sha256;item.redacted=observed.redacted;
   if(row.revision&&row.revision!==observed.snapshot.sha256||row.fileRevision&&row.fileRevision!==observed.fileRevision){item.state='stale';item.reason='source_revision_stale';continue;}
   const missing=observed.snapshot.kind==='missing',destination=item.role==='rename_destination'||item.operation==='create',allowsEither=item.operation==='create_or_modify'||item.operation==='create_or_modify_after_discovery';
   if(destination&&!missing){item.state='conflict';item.reason='destination_exists';continue;}
   if(!destination&&!allowsEither&&missing){item.reason=item.role==='rename_source'?'rename_source_missing':'source_missing';continue;}
   item.allowed=true;
  }
  try{await inventory.assertProject(project);}catch{globalReasons.push('project_root_changed');for(const item of items){item.allowed=false;item.reason='project_root_changed';}}
 }
 const reasons=[...new Set([...globalReasons,...items.filter(item=>!item.allowed).map(item=>item.reason??'not_checked')])].sort(),counts={requested:files.length,paths:items.length,present:items.filter(item=>item.state==='present').length,missing:items.filter(item=>item.state==='missing').length,excluded:items.filter(item=>['excluded','invalid','not_checked','conflict','stale'].includes(item.state)).length,totalBytes:total,bytesComplete:items.every(item=>item.state==='missing'||item.byteSize!==undefined)};
 const inventoryRevision=digest([project.rootIdentity,inventory.policyVersion,items.map(item=>[item.path,item.fileRevision??null,item.sha256??null,item.state])]),allowed=!reasons.length&&items.every(item=>item.allowed),publicItems=items.slice(0,64),stable={allowed,rootIdentity:project.rootIdentity,policyVersion:inventory.policyVersion,inventoryRevision,limits:EXECUTION_FILE_LIMITS,counts,items:publicItems,reasons};
 return {schemaVersion:'paos_file_preflight_v1',...stable,observedAt:new Date().toISOString(),digest:digest(stable),...(items.length>64?{truncated:true}:{})};
}
/** The compact diff is an observed before/after view, not an agent assertion or a complete Git patch. */
export function compareTaskFiles(before:readonly FileSnapshot[],after:readonly FileSnapshot[]):FileChange[]{
 const changes:FileChange[]=[];
 for(const old of before){const next=after.find(file=>file.path===old.path);if(!next||old.kind==='excluded'||next.kind==='excluded'||old.sha256===next.sha256)continue;
  const operation=old.kind==='missing'?'add':next.kind==='missing'?'delete':'modify';
  const lines=[`--- ${old.path}`,`+++ ${next.path}`,...(old.content??'').split('\n').map(line=>'-'+line),...(next.content??'').split('\n').map(line=>'+'+line)];
  const raw=lines.join('\n'),diff=raw.length>8192?raw.slice(0,8192)+'\n[diff truncated]':raw;
  changes.push({kind:'actual',path:old.path,operation,diff,beforeSha256:old.sha256,afterSha256:next.sha256});
 }
 return changes;
}
