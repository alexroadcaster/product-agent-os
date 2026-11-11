export type FileSnapshot={path:string;kind:'missing'|'present'|'excluded';sha256?:string;content?:string};
export type FileChange={kind:'actual';path:string;operation:'add'|'modify'|'delete';diff:string;beforeSha256?:string;afterSha256?:string};
import {lstat,realpath,open} from 'node:fs/promises';
import {join,resolve,relative,isAbsolute} from 'node:path';
import {createHash} from 'node:crypto';
import {bindProject} from '../adapters/project-sources.ts';
const fail=(code:string):never=>{throw Object.assign(new Error('The saved task file is unavailable.'),{code});};
const normalize=(value:string)=>process.platform==='win32'?resolve(value).toLowerCase():resolve(value);
const scrub=(value:string)=>value.replace(/sk-[A-Za-z0-9_-]+/g,'[REDACTED]').replace(/^(\s*(?:OPENAI_API_KEY|ANTHROPIC_API_KEY|AWS_SECRET_ACCESS_KEY|PRIVATE_KEY|ACCESS_TOKEN|REFRESH_TOKEN|PASSWORD|CLIENT_SECRET|_AUTHTOKEN)\s*[:=]).+$/gim,'$1 [REDACTED]')
 .replace(/("(?:access_token|refresh_token|password|client_secret|_authToken)"\s*:\s*)"(?:[^"\\]|\\.)*"/gi,'$1"[REDACTED]"');
/** Read only pinned task files. Linked, private, binary and over-budget content never becomes a public diff. */
export async function captureTaskFiles(binding:{workspaceRoot:string;directoryIdentity:string},files:readonly{relativePath:string}[],redact:(text:string)=>string=value=>value):Promise<FileSnapshot[]>{
 if(!Array.isArray(files)||files.length>32)fail('task_file_budget_exceeded');
 const current=await bindProject('task-files',binding.workspaceRoot);if(current.directoryIdentity!==binding.directoryIdentity)fail('project_root_changed');
 const rows:FileSnapshot[]=[],seen=new Set<string>();let total=0;
 for(const file of files){
  const path=file.relativePath?.replaceAll('\\','/');
  if(typeof path!=='string'||!path||isAbsolute(path)||/[:\0]/.test(path)||path.split('/').some(part=>!part||part==='.'||part==='..')||seen.has(path))fail('task_file_path_invalid');seen.add(path);
  const excluded=()=>rows.push({path,kind:'excluded'});
  if(/(^|\/)(\.env(?:\..*)?|\.npmrc|\.pypirc|\.netrc|_netrc|auth\.json|\.credentials\.json|[^/]+\.(?:pem|key|p12|pfx))$/i.test(path)
    ||/(^|\/)(?:\.ssh|\.aws|\.azure|\.gnupg)(?:\/|$)/i.test(path)){excluded();continue;}
  const absolute=join(current.workspaceRoot,path);let unavailable=false;
  for(const part of path.split('/').slice(0,-1).map((_,i)=>path.split('/').slice(0,i+1).join('/'))){
   try{const directory=join(current.workspaceRoot,part),info=await lstat(directory);if(!info.isDirectory()||info.isSymbolicLink()||normalize(await realpath(directory))!==normalize(directory)){unavailable=true;break;}}
   catch(error){if((error as NodeJS.ErrnoException).code==='ENOENT')break;unavailable=true;break;}
  }
  if(unavailable){excluded();continue;}
  try{
   const before=await lstat(absolute,{bigint:true});
   if(!before.isFile()||before.isSymbolicLink()||before.nlink!==1n||before.size>65536n||total+Number(before.size)>524288){excluded();continue;}
   const canonical=await realpath(absolute),within=relative(current.workspaceRoot,canonical);
   if(within.startsWith('..')||isAbsolute(within)||normalize(canonical)!==normalize(absolute)){excluded();continue;}
   const handle=await open(absolute,'r');
   try{
    const opened=await handle.stat({bigint:true});if(opened.ino!==before.ino||opened.dev!==before.dev||opened.nlink!==1n){excluded();continue;}
    const bytes=Buffer.alloc(65537);let count=0;
    while(count<bytes.length){const read=await handle.read(bytes,count,bytes.length-count,count);if(!read.bytesRead)break;count+=read.bytesRead;}
    const after=await handle.stat({bigint:true}),selected=await lstat(absolute,{bigint:true});
    if(count>65536||after.size!==BigInt(count)||after.ino!==before.ino||after.dev!==before.dev||after.mtimeNs!==before.mtimeNs||after.ctimeNs!==before.ctimeNs||after.nlink!==1n||selected.isSymbolicLink()||selected.ino!==before.ino||selected.dev!==before.dev||selected.nlink!==1n){excluded();continue;}
    const root=await bindProject('task-files',binding.workspaceRoot);if(root.directoryIdentity!==binding.directoryIdentity)fail('project_root_changed');
    let content:string;try{content=new TextDecoder('utf-8',{fatal:true}).decode(bytes.subarray(0,count));if(content.includes('\0')||/-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----/.test(content)||/-----BEGIN OPENSSH PRIVATE KEY-----/.test(content))throw Error('private_or_binary');}catch{excluded();continue;}
    total+=count;rows.push({path,kind:'present',sha256:createHash('sha256').update(bytes.subarray(0,count)).digest('hex'),content:redact(scrub(content))});
   }finally{await handle.close();}
  }catch(error){if((error as NodeJS.ErrnoException).code==='ENOENT')rows.push({path,kind:'missing'});else if((error as {code?:string}).code==='project_root_changed')throw error;else excluded();}
 }
 return rows;
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
