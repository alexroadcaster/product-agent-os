import {spawn} from 'node:child_process';
import {join,relative,resolve,isAbsolute,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {tmpdir} from 'node:os';
import {lstat,mkdtemp,rm} from 'node:fs/promises';
const fail=(code:string)=>Object.assign(new Error(code),{code});
export type DatabaseLease={pins:Array<{path:string;volume:string;fileId:string}>;release():Promise<void>;lost:Promise<void>};
/** SHARE_READ-only handles deny writers and replacement of root-to-file paths.
 * Child EOF and the parent's 15s deadline release only owned handles. */
export async function acquireDatabaseLease(input:{root:string;path:string;milliseconds?:number;signal?:AbortSignal;powershellExecutable?:string}):Promise<DatabaseLease>{
 if(process.platform!=='win32')throw fail('DATABASE_LEASE_UNAVAILABLE');
 const root=resolve(input.root),path=resolve(input.path),delta=relative(root,path);
 if(!delta||delta==='..'||delta.startsWith('..\\')||isAbsolute(delta)||input.signal?.aborted)throw fail('DATABASE_LEASE_SCOPE_INVALID');
 const paths=[root];let cursor=root;for(const part of delta.split(/[\\/]/)){cursor=join(cursor,part);paths.push(cursor);}
 const before=await Promise.all(paths.map(p=>lstat(p,{bigint:true})));
 if(before.some(p=>p.isSymbolicLink())||!before.at(-1)!.isFile()||before.at(-1)!.nlink!==1n)throw fail('DATABASE_LEASE_SCOPE_INVALID');
 const executable=input.powershellExecutable??join(process.env.SystemRoot??'C:\\Windows','System32','WindowsPowerShell','v1.0','powershell.exe');
 const home=await mkdtemp(join(tmpdir(),'paos-db-lease-'));
 const child=spawn(executable,['-NoLogo','-NoProfile','-NonInteractive','-File',fileURLToPath(new URL('./lease.ps1',import.meta.url))],{windowsHide:true,shell:false,cwd:home,env:{SystemRoot:process.env.SystemRoot,WINDIR:process.env.WINDIR,PATH:dirname(executable),HOME:home,USERPROFILE:home,TEMP:home,TMP:home},stdio:['pipe','pipe','pipe']});
 let closed=false,releasing=false,output='',errors=0;let lostResolve!:()=>void;const lost=new Promise<void>(r=>{lostResolve=r;});
 const ended=new Promise<void>(r=>{child.once('close',()=>{closed=true;lostResolve();r();});child.once('error',()=>{lostResolve();r();});});
 const timeout=setTimeout(()=>{child.kill();},Math.min(input.milliseconds??15000,15000));
 const abort=()=>{child.kill();};input.signal?.addEventListener('abort',abort,{once:true});
 const release=async()=>{if(releasing){await ended;return;}releasing=true;clearTimeout(timeout);input.signal?.removeEventListener('abort',abort);child.stdin.end('\n');const force=setTimeout(()=>child.kill(),1000);await ended;clearTimeout(force);await rm(home,{recursive:true,force:true});};
 child.stdin.on('error',()=>{});child.stderr.on('data',chunk=>{errors+=chunk.length;if(errors>8192)child.kill();});
 try{
  const message=await new Promise<any>((accept,reject)=>{child.once('error',()=>reject(fail('DATABASE_LEASE_UNAVAILABLE')));child.once('close',()=>reject(fail('DATABASE_LEASE_DENIED')));child.stdout.on('data',chunk=>{output+=chunk.toString();if(output.length>32768){child.kill();reject(fail('DATABASE_LEASE_OUTPUT_LIMIT'));return;}if(output.includes('\n'))try{accept(JSON.parse(output.slice(0,output.indexOf('\n'))));}catch{reject(fail('DATABASE_LEASE_OUTPUT_INVALID'));}});child.stdin.write(JSON.stringify({paths})+'\n');});
  if(message.error||!Array.isArray(message.pins)||message.pins.length!==paths.length||closed||input.signal?.aborted)throw fail('DATABASE_LEASE_DENIED');
  for(let i=0;i<paths.length;i++){const actual=String(message.pins[i].path).replace(/^\\\\\?\\/,'');const after=await lstat(paths[i],{bigint:true});if(actual.toLowerCase()!==paths[i].toLowerCase()||String(after.dev)!==message.pins[i].volume||String(after.ino)!==message.pins[i].fileId||after.dev!==before[i].dev||after.ino!==before[i].ino||after.isSymbolicLink()||i===paths.length-1&&message.pins[i].links!=='1')throw fail('DATABASE_LEASE_SOURCE_DRIFT');}
  return {pins:message.pins,release,lost};
 }catch(error){await release();throw error;}
}
