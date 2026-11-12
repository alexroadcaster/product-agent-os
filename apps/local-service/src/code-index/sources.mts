import {lstat,realpath,open,readdir} from 'node:fs/promises';
import {constants} from 'node:fs';
import {resolve,relative,join,parse,sep,extname} from 'node:path';
import {createHash} from 'node:crypto';
import {bindProject} from '../adapters/project-sources.ts';
export const graphFail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
export const digest=(value:string|Buffer)=>createHash('sha256').update(value).digest('hex');
const comparable=(path:string)=>process.platform==='win32'?path.toLowerCase():path;
export type SourceProject={id:string;canonicalRoot:string;rootIdentity:string};
export const sensitiveSourcePath=(path:string)=>path.split(/[\\/]/).some(p=>/^\.(?:git|env|aws|ssh|azure)$|^(?:node_modules|vendor|dist|build|site|coverage|\.venv[^/]*|\.tmp|\.docs-tools|\.codex-tmp|backups|profile)$/i.test(p)||/^\.env(?:\.|$)|^(?:credentials|secrets?)(?:\.|$)|\.(?:pem|key|p12|pfx|sqlite|db)(?:$|-)/i.test(p));
/** Ancestors are checked as well as the final registered directory; junctions and links cannot widen authority. */
export async function assertSourceProject(project:SourceProject){
 const absolute=resolve(project.canonicalRoot),root=parse(absolute).root;let cursor=root;
 for(const part of absolute.slice(root.length).split(sep).filter(Boolean)){cursor=join(cursor,part);if((await lstat(cursor)).isSymbolicLink())graphFail('GRAPH_LINKED_SOURCE');}
 const binding=await bindProject(project.id,absolute);if(comparable(binding.workspaceRoot)!==comparable(project.canonicalRoot)||binding.directoryIdentity!==project.rootIdentity)graphFail('PROJECT_ROOT_UNAVAILABLE');
}
export async function readCheckedSource(project:SourceProject,path:string,limit=512*1024){
 if(!path||path.includes('\\')||path.split('/').some(p=>!p||p==='.'||p==='..')||sensitiveSourcePath(path))graphFail('GRAPH_SOURCE_FORBIDDEN');
 await assertSourceProject(project);let target=project.canonicalRoot;
 for(const part of path.split('/')){target=join(target,part);if((await lstat(target)).isSymbolicLink())graphFail('GRAPH_LINKED_SOURCE');}
 const canonical=await realpath(target),within=relative(project.canonicalRoot,canonical);if(within.startsWith('..')||comparable(resolve(project.canonicalRoot,within))!==comparable(canonical))graphFail('GRAPH_SOURCE_FORBIDDEN');
 const before=await lstat(target,{bigint:true});if(!before.isFile()||before.nlink!==1n)graphFail('GRAPH_LINKED_SOURCE');if(before.size>BigInt(limit))graphFail('GRAPH_SOURCE_LIMIT');
 const handle=await open(target,constants.O_RDONLY|(constants.O_NOFOLLOW??0));try{
  const opened=await handle.stat({bigint:true});if(opened.ino!==before.ino||opened.dev!==before.dev||opened.nlink!==1n)graphFail('GRAPH_SOURCE_DRIFT');
  const bytes=Buffer.alloc(limit+1);let count=0;while(count<bytes.length){const r=await handle.read(bytes,count,bytes.length-count,count);if(!r.bytesRead)break;count+=r.bytesRead;}
  const after=await handle.stat({bigint:true}),current=await lstat(target,{bigint:true});await assertSourceProject(project);
  let checked=project.canonicalRoot;for(const part of path.split('/')){checked=join(checked,part);if((await lstat(checked)).isSymbolicLink())graphFail('GRAPH_SOURCE_DRIFT');}
  if(count>limit||after.size!==BigInt(count)||after.ino!==current.ino||after.dev!==current.dev||current.isSymbolicLink()||current.nlink!==1n||after.mtimeNs!==before.mtimeNs||after.ctimeNs!==before.ctimeNs||current.mtimeNs!==after.mtimeNs||current.ctimeNs!==after.ctimeNs)graphFail('GRAPH_SOURCE_DRIFT');
  const raw=bytes.subarray(0,count);let text:string;try{text=new TextDecoder('utf-8',{fatal:true}).decode(raw);}catch{graphFail('GRAPH_SOURCE_ENCODING');}
  return {relativePath:path,text:text!,hash:digest(raw),byteSize:count,modifiedAt:new Date(Number(after.mtimeNs/1000000n)).toISOString()};
 }finally{await handle.close();}
}
/** Bounded inventory reusable by read-only document catalogs; it never parses source or follows links. */
export async function scanCheckedSources(project:SourceProject,extensions?:Set<string>){
 await assertSourceProject(project);const files:string[]=[],excluded:string[]=[];let entries=0;
 async function walk(path:string,depth:number){if(depth>32)graphFail('GRAPH_INVENTORY_LIMIT');let dir=project.canonicalRoot;for(const part of path.split('/').filter(Boolean)){dir=join(dir,part);if((await lstat(dir)).isSymbolicLink())graphFail('GRAPH_SOURCE_DRIFT');}const items=await readdir(dir,{withFileTypes:true});items.sort((a,b)=>a.name.localeCompare(b.name));
  for(const item of items){if(++entries>10000)graphFail('GRAPH_INVENTORY_LIMIT');const p=path?`${path}/${item.name}`:item.name;if(sensitiveSourcePath(p))continue;
   const info=await lstat(join(project.canonicalRoot,p));if(info.isSymbolicLink()||info.isFile()&&info.nlink!==1){excluded.push(p);continue;}
   if(info.isDirectory())await walk(p,depth+1);else if(info.isFile()&&(!extensions||extensions.has(extname(p).toLowerCase()))){files.push(p);if(files.length>1000)graphFail('GRAPH_INVENTORY_LIMIT');}
  }
 }
 await walk('',0);await assertSourceProject(project);return {files,excluded};
}
