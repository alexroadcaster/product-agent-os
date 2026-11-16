import {lstat, realpath, open, opendir} from 'node:fs/promises';
import {constants,type BigIntStats} from 'node:fs';
import {resolve, relative, join, parse, sep, isAbsolute, extname} from 'node:path';
import {createHash, createHmac, randomBytes, timingSafeEqual} from 'node:crypto';
import {safePersistedText} from '../redaction/persisted.mts';
import type {InventoryProject, InventoryPolicy, InventoryLimits, InventoryEntry, InventoryCounts, InventoryMeta, InventorySnapshot, InventoryDirectory, InventoryRead, InventoryAccess} from '../../../../packages/contracts/project-inventory.ts';
export type {InventoryProject} from '../../../../packages/contracts/project-inventory.ts';

const digest=(value:unknown)=>createHash('sha256').update(typeof value==='string'||Buffer.isBuffer(value)?value:JSON.stringify(value)).digest('hex');
const compare=(value:string)=>process.platform==='win32'?value.toLowerCase():value;
const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
const codeExtensions=new Set(['.ts','.mts','.cts','.tsx','.js','.mjs','.cjs','.jsx','.py','.go','.rs','.java','.cs','.c','.cpp','.h','.rb','.vue','.svelte']);
const hardPart=/^\.(?:git|aws|ssh|azure|gnupg|npmrc|pypirc|netrc)$|^_netrc$|^auth\.json$|^\.(?:credentials)(?:\.|$)|^\.env(?:\.|$)|^(?:credentials|secrets?)(?:\.|$)|\.(?:pem|key|p12|pfx)$/i;
const heavyPart=/^(?:node_modules|vendor|dist|build|site|coverage|\.venv.*|\.tmp|\.docs-tools|\.codex-tmp|backups|profile)$/i;
const controlPlane=new Set(['AGENTS.md','REQUIREMENTS.md','PLAN.md','TEST.md','EVALS.md','RUNLOG.md'].map(compare));
const defaults:InventoryLimits={pageSize:100,directoryEntries:2000,entries:10000,files:1000,depth:32,milliseconds:30000,fileBytes:512*1024,responseBytes:1024*1024};

/** References may use Windows separators; absolute, ADS and traversal syntax never becomes relative authority. */
export function normaliseRelativePath(value:string,allowEmpty=false):string{
 if(typeof value!=='string'||value.length>2048||/[\x00-\x1f:]/.test(value)||/^[\\/]/.test(value))fail('INVENTORY_PATH_FORBIDDEN');
 const path=value.replaceAll('\\','/');
 if(!path&&allowEmpty)return '';
 if(!path||path.split('/').some(p=>!p||p==='.'||p==='..'))fail('INVENTORY_PATH_FORBIDDEN');
 if(process.platform==='win32'&&path.split('/').some(p=>/[. ]$/.test(p)||/^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)/i.test(p)))fail('INVENTORY_PATH_FORBIDDEN');
 return path;
}

export function classifyInventoryPath(path:string,kind:InventoryEntry['kind']='file'):InventoryAccess{
 const parts=normaliseRelativePath(path).split('/');
 if(parts.some(p=>hardPart.test(p)))return {readable:false,indexable:false,reason:'sensitive_path'};
 if(kind==='link')return {readable:false,indexable:false,reason:'linked_source'};
 if(parts.some(p=>heavyPart.test(p)))return {readable:false,indexable:false,reason:'generated_or_vendor'};
 if(kind!=='file')return {readable:false,indexable:false,reason:kind==='directory'?'directory':'unsupported_file'};
 if(/\.(?:sqlite|db)(?:$|-)/i.test(path))return {readable:false,indexable:false,reason:'database_content'};
 const indexable=codeExtensions.has(extname(path).toLowerCase());
 return {readable:true,indexable,...(!indexable?{reason:'unsupported_language'}:{})};
}

type Rule={base:string;pattern:string;negated:boolean;directory:boolean;anchored:boolean};
type Context={rules:Rule[];rulesLoaded:Set<string>;policyParts:string[];policyErrors:Set<string>;ignorePins:Map<string,string|null>;reasons:Set<string>;started:number;signal?:AbortSignal};
type DirPin={path:string;dev:bigint;ino:bigint};

/** One lower boundary owns listing, policy and checked reads; no adapter imports create a dependency cycle. */
export function createProjectInventory(options:{policy?:InventoryPolicy;limits?:Partial<InventoryLimits>}={}){
 const plain=(value:unknown)=>Boolean(value)&&typeof value==='object'&&!Array.isArray(value)&&Object.getPrototypeOf(value)===Object.prototype;
 if(options.policy!==undefined&&(!plain(options.policy)||Object.keys(options.policy).some(k=>!['version','include','exclude','respectGitignore'].includes(k))||options.policy.respectGitignore!==undefined&&typeof options.policy.respectGitignore!=='boolean'||options.policy.version!==undefined&&(typeof options.policy.version!=='string'||options.policy.version.length>100)||options.policy.include!==undefined&&!Array.isArray(options.policy.include)||options.policy.exclude!==undefined&&!Array.isArray(options.policy.exclude)))fail('INVENTORY_POLICY_INVALID');
 if(options.limits!==undefined&&(!plain(options.limits)||Object.keys(options.limits).some(k=>!(k in defaults))))fail('INVENTORY_LIMIT_INVALID');
 const policy={respectGitignore:true,...options.policy,include:[...(options.policy?.include??[])],exclude:[...(options.policy?.exclude??[])]};
 if(policy.include.length>200||policy.exclude.length>200||[...policy.include,...policy.exclude].some(p=>typeof p!=='string'||p.length>1024||p.includes('..')||p.includes('\\')||p.startsWith('/')))fail('INVENTORY_POLICY_INVALID');
 const limits={...defaults,...options.limits};for(const [key,value] of Object.entries(limits))if(!Number.isSafeInteger(value)||value<1||value>defaults[key as keyof InventoryLimits])fail('INVENTORY_LIMIT_INVALID');
 if(limits.responseBytes<8192)fail('INVENTORY_LIMIT_INVALID');
 const baseVersion='inventory-v1:'+digest(policy).slice(0,24),secret=randomBytes(32);
 const context=(signal?:AbortSignal):Context=>({rules:[],rulesLoaded:new Set(),policyParts:[baseVersion],policyErrors:new Set(),ignorePins:new Map(),reasons:new Set(),started:Date.now(),signal});
 function budget(ctx:Context){if(ctx.signal?.aborted)fail('INVENTORY_CANCELLED');if(Date.now()-ctx.started>limits.milliseconds)fail('INVENTORY_TIMEOUT');}
 async function assertProject(project:InventoryProject){
  if(!project.id||!isAbsolute(project.canonicalRoot)||project.canonicalRoot.startsWith('\\\\'))fail('PROJECT_ROOT_UNAVAILABLE');
  try{
   const absolute=resolve(project.canonicalRoot),root=parse(absolute).root;let cursor=root;
   for(const part of absolute.slice(root.length).split(sep).filter(Boolean)){cursor=join(cursor,part);if((await lstat(cursor)).isSymbolicLink())fail('INVENTORY_LINKED_SOURCE');}
   const info=await lstat(absolute,{bigint:true}),canonical=await realpath(absolute);
   if(!info.isDirectory()||info.ino===0n||`${info.dev}:${info.ino}`!==project.rootIdentity||compare(canonical)!==compare(absolute))fail('PROJECT_ROOT_UNAVAILABLE');
  }catch(error){if((error as any)?.code==='INVENTORY_LINKED_SOURCE')throw error;fail('PROJECT_ROOT_UNAVAILABLE');}
 }
 async function checked(project:InventoryProject,path:string){
  await assertProject(project);const pins:DirPin[]=[];let target=project.canonicalRoot;
  for(const part of path.split('/').filter(Boolean)){target=join(target,part);const info=await lstat(target,{bigint:true});if(info.isSymbolicLink())fail('INVENTORY_LINKED_SOURCE');if(info.isDirectory())pins.push({path:target,dev:info.dev,ino:info.ino});}
  const canonical=await realpath(target),inside=relative(project.canonicalRoot,canonical);
  if(inside==='..'||inside.startsWith('..'+sep)||isAbsolute(inside)||compare(resolve(project.canonicalRoot,inside))!==compare(canonical)||compare(canonical)!==compare(resolve(project.canonicalRoot,path)))fail('INVENTORY_PATH_FORBIDDEN');
  return {target,pins};
 }
 async function recheck(project:InventoryProject,pins:DirPin[]){await assertProject(project);for(const pin of pins){const now=await lstat(pin.path,{bigint:true});if(now.isSymbolicLink()||!now.isDirectory()||now.dev!==pin.dev||now.ino!==pin.ino)fail('INVENTORY_SOURCE_DRIFT');}}
 const statRevision=(project:InventoryProject,path:string,info:any)=>digest([project.rootIdentity,compare(path),String(info.dev),String(info.ino),String(info.size),String(info.mtimeNs),String(info.ctimeNs),String(info.nlink)]);
 const scopedPolicy=(path:string,ctx:Context)=>ctx.policyParts.filter(part=>part===baseVersion||part.startsWith('.gitignore:')||compare(path).startsWith(compare(part.slice(0,part.indexOf('/.gitignore:'))+'/'))).map(compare).sort();
 const fileRevision=(project:InventoryProject,path:string,info:any,ctx:Context)=>digest([statRevision(project,path,info),baseVersion,scopedPolicy(path,ctx)]);
 async function raw(project:InventoryProject,path:string,maxBytes:number,redactSensitive=false){
  const {target,pins}=await checked(project,path),before=await lstat(target,{bigint:true});
  if(!before.isFile()||before.nlink!==1n)fail('INVENTORY_LINKED_SOURCE');if(before.size>BigInt(maxBytes))fail('INVENTORY_FILE_TOO_LARGE');
  const handle=await open(target,constants.O_RDONLY|(constants.O_NOFOLLOW??0));
  try{
   const opened=await handle.stat({bigint:true});if(opened.dev!==before.dev||opened.ino!==before.ino||opened.nlink!==1n)fail('INVENTORY_SOURCE_DRIFT');
   const bytes=Buffer.alloc(maxBytes+1);let count=0;while(count<bytes.length){const result=await handle.read(bytes,count,bytes.length-count,count);if(!result.bytesRead)break;count+=result.bytesRead;}
   const after=await handle.stat({bigint:true}),current=await lstat(target,{bigint:true});await recheck(project,pins);
   if(count>maxBytes||after.size!==BigInt(count)||current.isSymbolicLink()||current.nlink!==1n||after.dev!==current.dev||after.ino!==current.ino||before.mtimeNs!==after.mtimeNs||before.ctimeNs!==after.ctimeNs||current.mtimeNs!==after.mtimeNs||current.ctimeNs!==after.ctimeNs||current.size!==after.size)fail('INVENTORY_SOURCE_DRIFT');
   const value=bytes.subarray(0,count);let text:string;try{text=new TextDecoder('utf-8',{fatal:true}).decode(value);}catch{fail('INVENTORY_ENCODING_UNSUPPORTED');}
   if(text!.includes('\0'))fail('INVENTORY_BINARY_FILE');
   // A truncated key must not bypass a redactor that recognizes complete blocks.
   if(/-----BEGIN [^-]*PRIVATE KEY-----/.test(text!))fail('INVENTORY_SENSITIVE_CONTENT');
   const safe=safePersistedText(text!),redacted=safe!==text!;
   if(redacted&&!redactSensitive)fail('INVENTORY_SENSITIVE_CONTENT');
   return {text:redacted?safe:text!,redacted,hash:digest(value),byteSize:count,modifiedAt:new Date(Number(after.mtimeNs/1000000n)).toISOString(),statRevision:statRevision(project,path,after)};
  }finally{await handle.close();}
 }
 /** gitignore wildcard grammar: unlike path.matchesGlob, '*' includes dotfiles;
  * globstar spans directories only in documented whole-component positions.
  * Position sets avoid regex backtracking on user-authored wildcard chains. */
 function glob(path:string,pattern:string){
  const segments=compare(path).split('/'),patterns=compare(pattern).split('/');
  function segment(value:string,rule:string){let positions=new Set([0]);
   for(let i=0;i<rule.length;i++){const c=rule[i];if(c==='*'){if(!positions.size)return false;const from=Math.min(...positions);positions=new Set(Array.from({length:value.length-from+1},(_v,j)=>from+j));continue;}
    let accepts:(value:string)=>boolean;
    if(c==='?')accepts=()=>true;
    else if(c==='\\'){if(i+1===rule.length)return false;const literal=rule[++i];accepts=value=>value===literal;}
    else if(c==='['&&rule.indexOf(']',i+1)>=0){const end=rule.indexOf(']',i+1);let body=rule.slice(i+1,end);if(body.startsWith('!'))body='^'+body.slice(1);else if(body.startsWith('^'))body='\\'+body;let match:RegExp;try{match=new RegExp('^['+body+']$');}catch{return false;}accepts=value=>match.test(value);i=end;}
    else accepts=value=>value===c;
    const next=new Set<number>();for(const at of positions)if(at<value.length&&accepts(value[at]))next.add(at+1);positions=next;
   }return positions.has(value.length);
  }
  let positions=new Set([0]);for(const rule of patterns){const next=new Set<number>();if(rule==='**'){if(!positions.size)return false;const from=Math.min(...positions);for(let i=from;i<=segments.length;i++)next.add(i);}else for(const at of positions)if(at<segments.length&&segment(segments[at],rule))next.add(at+1);positions=next;}return positions.has(segments.length);
 }
 function parseRules(text:string,base:string,ctx:Context){
  const lines=text.split(/\r?\n/);if(lines.length+ctx.rules.length>4096){ctx.reasons.add('gitignore_rule_limit');ctx.policyErrors.add(base);return;}
  for(let line of lines){while(line.endsWith(' ')&&!line.endsWith('\\ '))line=line.slice(0,-1);if(!line||line.startsWith('#'))continue;
   const negated=line.startsWith('!');if(negated)line=line.slice(1);
   // POSIX named classes are deliberately unsupported; partial policy denies
   // content rather than silently assigning different matching semantics.
   if(line.includes('[[:')||line.endsWith('\\')){ctx.reasons.add('gitignore_pattern_unsupported');ctx.policyErrors.add(base);continue;}
   const directory=line.endsWith('/');if(directory)line=line.slice(0,-1);const anchored=line.startsWith('/')||line.includes('/');if(line.startsWith('/'))line=line.slice(1);
   if(line)ctx.rules.push({base,pattern:line,negated,directory,anchored});
  }
 }
 async function rulesFor(project:InventoryProject,path:string,ctx:Context){
  if(!policy.respectGitignore)return;const dirs=[''];let at='';for(const part of path.split('/').filter(Boolean)){at=at?at+'/'+part:part;dirs.push(at);}
  for(const dir of dirs){if(ctx.rulesLoaded.has(dir))continue;ctx.rulesLoaded.add(dir);budget(ctx);if(dir&&(dir.split('/').some(p=>hardPart.test(p)||heavyPart.test(p))||ignored(dir,true,ctx)))continue;const name=dir?dir+'/.gitignore':'.gitignore';
   try{const data=await raw(project,name,Math.min(limits.fileBytes,64*1024));ctx.ignorePins.set(name,data.statRevision);ctx.policyParts.push(name+':'+data.hash);parseRules(data.text,dir,ctx);}catch(error){if((error as any).code==='ENOENT')ctx.ignorePins.set(name,null);else{if(['PROJECT_ROOT_UNAVAILABLE','INVENTORY_SOURCE_DRIFT'].includes((error as any).code))throw error;ctx.reasons.add('gitignore_unavailable');ctx.policyErrors.add(dir);}}
  }
 }
 function ignored(path:string,isDirectory:boolean,ctx:Context){
  const parts=path.split('/');for(let end=1;end<=parts.length;end++){const prefix=parts.slice(0,end).join('/'),directory=end<parts.length||isDirectory;let excluded=false;
   for(const rule of ctx.rules){if(rule.base&&!compare(prefix).startsWith(compare(rule.base+'/')))continue;const rel=rule.base?prefix.slice(rule.base.length+1):prefix;if(rule.directory&&!directory)continue;
    if(rule.anchored?glob(rel,rule.pattern):glob(rel.split('/').at(-1)!,rule.pattern))excluded=!rule.negated;
   }if(excluded)return true;
  }return false;
 }
 function access(path:string,kind:InventoryEntry['kind'],ctx:Context,databaseSchema=false):InventoryAccess{
  const base=classifyInventoryPath(path,kind);
  if(base.reason==='sensitive_path'||base.reason==='linked_source'||base.reason==='database_content'&&!databaseSchema||kind==='other')return base;
  if(policy.exclude.some(pattern=>glob(path,pattern)||path.split('/').some((_p,i)=>glob(path.split('/').slice(0,i+1).join('/'),pattern))))return {readable:false,indexable:false,reason:'project_exclude'};
  const included=policy.include.some(pattern=>glob(path,pattern)||kind==='directory'&&compare(pattern).startsWith(compare(path+'/')));
  if(!included&&(base.reason==='generated_or_vendor'||ignored(path,kind==='directory',ctx)))return {readable:false,indexable:false,reason:base.reason==='generated_or_vendor'?'generated_or_vendor':'gitignore'};
  if([...ctx.policyErrors].some(base=>!base||compare(path).startsWith(compare(base+'/'))))return {readable:false,indexable:false,reason:'policy_incomplete'};
  if(kind==='directory')return {readable:false,indexable:false,reason:'directory'};
  const indexable=codeExtensions.has(extname(path).toLowerCase());return {readable:true,indexable,...(!indexable?{reason:'unsupported_language'}:{})};
 }
 async function policyCurrent(project:InventoryProject,ctx:Context){
  for(const [path,pin] of ctx.ignorePins){budget(ctx);let current:string|null=null;try{const {target}=await checked(project,path),info=await lstat(target,{bigint:true});if(!info.isFile()||info.nlink!==1n)fail('INVENTORY_POLICY_DRIFT');current=statRevision(project,path,info);}catch(error){if((error as any).code!=='ENOENT')throw error;}if(current!==pin)fail('INVENTORY_POLICY_DRIFT');}
 }
 async function inspectEntry(project:InventoryProject,path:string,ctx:Context){
  const parent=path.split('/').slice(0,-1).join('/');await rulesFor(project,parent,ctx);const {target,pins}=await checked(project,parent),info=await lstat(join(target,path.split('/').at(-1)!),{bigint:true}),kind:InventoryEntry['kind']=info.isSymbolicLink()||info.isFile()&&info.nlink!==1n?'link':info.isDirectory()?'directory':info.isFile()?'file':'other';
  await recheck(project,pins);return {relativePath:path,name:path.split('/').at(-1)!,kind,byteSize:Number(info.size),modifiedAt:new Date(Number(info.mtimeNs/1000000n)).toISOString(),revision:fileRevision(project,path,info,ctx),access:access(path,kind,ctx)} satisfies InventoryEntry;
 }
 /** Revalidate observed metadata without reading source bytes. An unstable
  * manifest is rejected instead of being published as one reliable revision. */
 async function entriesCurrent(project:InventoryProject,entries:InventoryEntry[],ctx:Context){
  await assertProject(project);
  for(const entry of entries){budget(ctx);try{const info=await lstat(join(project.canonicalRoot,...entry.relativePath.split('/')),{bigint:true});if(fileRevision(project,entry.relativePath,info,ctx)!==entry.revision)fail('INVENTORY_SOURCE_DRIFT');}catch{fail('INVENTORY_SOURCE_DRIFT');}}
  for(const entry of entries.filter(e=>e.kind==='directory')){const info=await lstat(join(project.canonicalRoot,...entry.relativePath.split('/')),{bigint:true});if(info.isSymbolicLink()||fileRevision(project,entry.relativePath,info,ctx)!==entry.revision)fail('INVENTORY_SOURCE_DRIFT');}
  await assertProject(project);await policyCurrent(project,ctx);
 }
 async function branch(project:InventoryProject,path:string,ctx:Context){
  budget(ctx);const {target,pins}=await checked(project,path);if(!(await lstat(target)).isDirectory())fail('INVENTORY_NOT_DIRECTORY');await rulesFor(project,path,ctx);
  if(path){const state=access(path,'directory',ctx);if(state.reason!=='directory'){ctx.reasons.add('excluded_subtree:'+state.reason);return [];}}
  const entries:InventoryEntry[]=[];const dir=await opendir(target,{bufferSize:32});let seen=0;
  for await(const item of dir){budget(ctx);if(seen++>=limits.directoryEntries){ctx.reasons.add('directory_entry_limit');break;}const relativePath=path?path+'/'+item.name:item.name;
   try{const info=await lstat(join(target,item.name),{bigint:true}),kind:InventoryEntry['kind']=info.isSymbolicLink()||info.isFile()&&info.nlink!==1n?'link':info.isDirectory()?'directory':info.isFile()?'file':'other';entries.push({relativePath,name:item.name,kind,byteSize:Number(info.size),modifiedAt:new Date(Number(info.mtimeNs/1000000n)).toISOString(),revision:fileRevision(project,relativePath,info,ctx),access:access(relativePath,kind,ctx)});}catch(error){if(['INVENTORY_SOURCE_DRIFT','PROJECT_ROOT_UNAVAILABLE'].includes((error as any).code))throw error;ctx.reasons.add('entry_unavailable');}
  }
  await recheck(project,pins);entries.sort((a,b)=>compare(a.relativePath)<compare(b.relativePath)?-1:compare(a.relativePath)>compare(b.relativePath)?1:0);return entries;
 }
 const counts=(entries:InventoryEntry[],ctx:Context):InventoryCounts=>({discovered:entries.length,files:entries.filter(e=>e.kind==='file').length,directories:entries.filter(e=>e.kind==='directory').length,readEligible:entries.filter(e=>e.access.readable).length,indexEligible:entries.filter(e=>e.access.indexable).length,readable:null,indexed:null,unsupported:entries.filter(e=>e.kind==='file'&&e.access.reason==='unsupported_language').length,excluded:entries.filter(e=>!e.access.readable&&e.access.reason!=='directory').length,error:[...ctx.reasons].filter(r=>r.includes('unavailable')).length});
 function meta(project:InventoryProject,ctx:Context,entries:InventoryEntry[]):InventoryMeta{return {schemaVersion:'paos_project_inventory_v1',projectId:project.id,rootIdentity:project.rootIdentity,policyVersion:baseVersion,ignoreRevision:digest([...ctx.policyParts].sort()),revision:digest([project.rootIdentity,baseVersion,[...ctx.policyParts].sort(),entries]),observedAt:new Date().toISOString(),coverage:ctx.reasons.size?'partial':'complete',reasons:[...ctx.reasons].sort()};}
 function bound(entries:InventoryEntry[],ctx:Context){let bytes=0;const out:InventoryEntry[]=[];for(const entry of entries){bytes+=Buffer.byteLength(JSON.stringify(entry));if(bytes>limits.responseBytes-4096){ctx.reasons.add('response_byte_limit');break;}out.push(entry);}return out;}
 return {
  assertProject,
  /** Purpose-specific admission reads only the 100-byte SQLite header. It does
   * not grant generic text reads, index permission or authority to execute SQL.
   * The caller must hold a native lease before opening SQLite by path. */
  async admitDatabaseSource(project:InventoryProject,input:{path:string;revision?:string;maxBytes?:number}){
   const path=normaliseRelativePath(input.path),ctx=context(),maxBytes=input.maxBytes??128*1024*1024;
   if(!Number.isSafeInteger(maxBytes)||maxBytes<100||maxBytes>128*1024*1024)fail('INVENTORY_LIMIT_INVALID');
   if(input.revision!==undefined&&!/^[a-f0-9]{64}$/.test(input.revision))fail('INVENTORY_REVISION_STALE');
   if(/-(wal|shm|journal)$/i.test(path))fail('INVENTORY_DATABASE_SIDECAR');
   await assertProject(project);await rulesFor(project,path.split('/').slice(0,-1).join('/'),ctx);
   const {target,pins}=await checked(project,path),before=await lstat(target,{bigint:true});
   const kind:InventoryEntry['kind']=before.isSymbolicLink()||before.isFile()&&before.nlink!==1n?'link':before.isFile()?'file':before.isDirectory()?'directory':'other';
   if(kind!=='file'||!access(path,kind,ctx,true).readable)fail('INVENTORY_SOURCE_FORBIDDEN');
   if(before.size>BigInt(maxBytes))fail('INVENTORY_FILE_TOO_LARGE');
   const revision=fileRevision(project,path,before,ctx);if(input.revision&&input.revision!==revision)fail('INVENTORY_REVISION_STALE');
   const sidecars=async()=>{for(const suffix of ['-wal','-shm','-journal'])try{await lstat(target+suffix);fail('INVENTORY_DATABASE_SIDECAR');}catch(error){if((error as any).code!=='ENOENT')throw error;}};
   await sidecars();const handle=await open(target,constants.O_RDONLY|(constants.O_NOFOLLOW??0));
   try{
    const opened=await handle.stat({bigint:true});if(opened.dev!==before.dev||opened.ino!==before.ino||opened.nlink!==1n)fail('INVENTORY_SOURCE_DRIFT');
    const bytes=Buffer.alloc(100);let count=0;while(count<100){const read=await handle.read(bytes,count,100-count,count);if(!read.bytesRead)break;count+=read.bytesRead;}
    if(count!==100||!bytes.subarray(0,16).equals(Buffer.from('SQLite format 3\0')))fail('INVENTORY_DATABASE_FORMAT_UNSUPPORTED');
    if(bytes[18]!==1||bytes[19]!==1)fail('INVENTORY_DATABASE_WAL_UNSUPPORTED');
    const after=await handle.stat({bigint:true}),now=await lstat(target,{bigint:true});await recheck(project,pins);await policyCurrent(project,ctx);await sidecars();
    if(now.isSymbolicLink()||now.nlink!==1n||fileRevision(project,path,after,ctx)!==revision||fileRevision(project,path,now,ctx)!==revision)fail('INVENTORY_SOURCE_DRIFT');
    return {relativePath:path,fileRevision:revision,policyVersion:baseVersion,byteSize:Number(after.size),rootIdentity:project.rootIdentity};
   }finally{await handle.close();}
  },
  policyVersion:baseVersion,
  limits:{...limits},
  /** Classify a virtual create target using only existing ancestor metadata and
   * ignore data. Missing ancestors are neither opened nor created. */
  async access(project:InventoryProject,input:string){
   const path=normaliseRelativePath(input),ctx=context(),parts=path.split('/');await assertProject(project);
   let parent='',missingParent:string|undefined;
   for(const part of parts.slice(0,-1)){
    const candidate=parent?parent+'/'+part:part;try{const {target}=await checked(project,candidate);if(!(await lstat(target)).isDirectory())fail('INVENTORY_NOT_DIRECTORY');parent=candidate;}catch(error){if((error as any).code!=='ENOENT')throw error;missingParent=candidate;break;}
   }
   const {pins}=await checked(project,parent);await rulesFor(project,parent,ctx);
   let info:BigIntStats|undefined;try{info=await lstat(join(project.canonicalRoot,...parts),{bigint:true});}catch(error){if((error as any).code!=='ENOENT')throw error;}
   const kind:InventoryEntry['kind']=!info?'file':info.isSymbolicLink()||info.isFile()&&info.nlink!==1n?'link':info.isDirectory()?'directory':info.isFile()?'file':'other';
   const result=access(path,kind,ctx),revision=digest([project.rootIdentity,compare(path),baseVersion,scopedPolicy(path,ctx),info?statRevision(project,path,info):'missing']);
   await recheck(project,pins);await policyCurrent(project,ctx);
   if(missingParent){try{await lstat(join(project.canonicalRoot,...missingParent.split('/')));fail('INVENTORY_SOURCE_DRIFT');}catch(error){if((error as any).code!=='ENOENT')throw error;}}
   let after:BigIntStats|undefined;try{after=await lstat(join(project.canonicalRoot,...parts),{bigint:true});}catch(error){if((error as any).code!=='ENOENT')throw error;}
   if(Boolean(after)!==Boolean(info)||info&&after&&statRevision(project,path,info)!==statRevision(project,path,after))fail('INVENTORY_SOURCE_DRIFT');
   await recheck(project,pins);return {allowed:result.readable,reason:result.reason,policyVersion:baseVersion,revision,exists:Boolean(info)};
  },
  async inspect(project:InventoryProject,path:string):Promise<InventoryEntry>{const relativePath=normaliseRelativePath(path),ctx=context();await assertProject(project);const entry=await inspectEntry(project,relativePath,ctx);await policyCurrent(project,ctx);return entry;},
  async listDirectory(project:InventoryProject,input:{path?:string;cursor?:string;limit?:number;filter?:'all'|'control_plane';query?:string}={}):Promise<InventoryDirectory>{
   const path=normaliseRelativePath(input.path??'',true),limit=input.limit??limits.pageSize;if(!Number.isSafeInteger(limit)||limit<1||limit>Math.min(200,limits.pageSize*2))fail('INVENTORY_QUERY_INVALID');if((input.query?.length??0)>256||input.filter&&!['all','control_plane'].includes(input.filter))fail('INVENTORY_QUERY_INVALID');
   const ctx=context(),all=await branch(project,path,ctx),base=meta(project,ctx,all),query=compare(input.query??''),selected=all.filter(e=>(!query||compare(e.relativePath).includes(query))&&(input.filter!=='control_plane'||controlPlane.has(compare(e.relativePath)))),binding=digest([project.id,project.rootIdentity,path,base.policyVersion,base.revision,limit,input.filter??'all',query]);let offset=0;
   if(input.cursor){try{if(input.cursor.length>2048)fail('INVENTORY_CURSOR_INVALID');const [payload,signature,extra]=input.cursor.split('.'),expected=createHmac('sha256',secret).update(payload).digest('base64url');if(extra||signature?.length!==expected.length||!timingSafeEqual(Buffer.from(signature),Buffer.from(expected)))fail('INVENTORY_CURSOR_INVALID');const cursor=JSON.parse(Buffer.from(payload,'base64url').toString());if(cursor.binding!==binding)fail('INVENTORY_CURSOR_STALE');if(!Number.isSafeInteger(cursor.offset)||cursor.offset<0||cursor.offset>selected.length)fail('INVENTORY_CURSOR_INVALID');offset=cursor.offset;}catch(error){if((error as any).code==='INVENTORY_CURSOR_STALE')throw error;fail('INVENTORY_CURSOR_INVALID');}}
   const entries=bound(selected.slice(offset,offset+limit),ctx);let nextCursor:string|null=null;if(entries.length&&offset+entries.length<selected.length){const payload=Buffer.from(JSON.stringify({binding,offset:offset+entries.length})).toString('base64url');nextCursor=payload+'.'+createHmac('sha256',secret).update(payload).digest('base64url');}await entriesCurrent(project,all,ctx);
   return {...base,coverage:ctx.reasons.size?'partial':'complete',reasons:[...ctx.reasons].sort(),entries,counts:counts(all,ctx),path,searchScope:'directory',nextCursor,total:selected.length,limit};
  },
  async snapshot(project:InventoryProject,input:{signal?:AbortSignal}={}):Promise<InventorySnapshot>{
   const ctx=context(input.signal),entries:InventoryEntry[]=[];let files=0;
   async function walk(path:string,depth:number):Promise<void>{budget(ctx);if(depth>limits.depth){ctx.reasons.add('depth_limit');return;}let items:InventoryEntry[];try{items=await branch(project,path,ctx);}catch(error){if(['PROJECT_ROOT_UNAVAILABLE','INVENTORY_SOURCE_DRIFT','INVENTORY_LINKED_SOURCE','INVENTORY_CANCELLED','INVENTORY_TIMEOUT'].includes((error as any).code))throw error;ctx.reasons.add('directory_unavailable');return;}
    for(const entry of items){budget(ctx);if(entries.length>=limits.entries||files>=limits.files){ctx.reasons.add('inventory_entry_limit');return;}entries.push(entry);if(entry.kind==='file')files++;if(entry.kind==='directory'){if(entry.access.reason==='directory')await walk(entry.relativePath,depth+1);else ctx.reasons.add('excluded_subtree:'+entry.access.reason);}}
   }
   await walk('',0);await entriesCurrent(project,entries,ctx);const result=bound(entries,ctx);return {...meta(project,ctx,entries),entries:result,counts:counts(entries,ctx)};
  },
  async read(project:InventoryProject,input:{path:string;revision?:string;maxBytes?:number;redactSensitive?:boolean}):Promise<InventoryRead>{
   const path=normaliseRelativePath(input.path),ctx=context();await assertProject(project);const {target}=await checked(project,path);await rulesFor(project,path.split('/').slice(0,-1).join('/'),ctx);const state=access(path,'file',ctx);if(!state.readable)fail('INVENTORY_SOURCE_FORBIDDEN');const info=await lstat(target,{bigint:true});
   if(input.revision&&input.revision!==fileRevision(project,path,info,ctx))fail('INVENTORY_REVISION_STALE');const maxBytes=input.maxBytes??limits.fileBytes;if(!Number.isSafeInteger(maxBytes)||maxBytes<1||maxBytes>limits.fileBytes||input.redactSensitive!==undefined&&typeof input.redactSensitive!=='boolean')fail('INVENTORY_LIMIT_INVALID');const {statRevision:stat,...result}=await raw(project,path,maxBytes,input.redactSensitive),revision=digest([stat,baseVersion,scopedPolicy(path,ctx)]);
   if(input.revision&&input.revision!==revision)fail('INVENTORY_REVISION_STALE');await policyCurrent(project,ctx);return {...meta(project,ctx,[]),revision,relativePath:path,...result,fileRevision:revision};
  },
 };
}
