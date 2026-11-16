import {spawn} from 'node:child_process';
import {join,relative,resolve,isAbsolute,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {tmpdir} from 'node:os';
import {lstat,mkdtemp,rm} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const fail=(code:string)=>Object.assign(new Error(code),{code});
/** One fixed child owns the exclusive existing-target handle through snapshot and commit.
 * Raw recovery bytes remain on its private pipe; callers never log or return frames. */
export async function openDocumentHandle(input:{root:string;path:string;expectedHash:string}):Promise<{before:Buffer;processId:number;temporaryDirectory:string;directoryIdentity:string;commit(after:Buffer,expectedHash:string):Promise<void>;close():Promise<void>}>{
 if(process.platform!=='win32')throw fail('DOCUMENT_NATIVE_UNAVAILABLE');
 const root=resolve(input.root),path=resolve(root,input.path),delta=relative(root,path);
 if(!delta||delta==='..'||delta.startsWith('..\\')||isAbsolute(delta)||delta.split(/[\\/]/).length>33)throw fail('DOCUMENT_WRITE_FORBIDDEN');
 const paths=[root];let cursor=root;for(const part of delta.split(/[\\/]/)){cursor=join(cursor,part);paths.push(cursor);}
 const stats=await Promise.all(paths.map(p=>lstat(p,{bigint:true})));
 if(stats.some(p=>p.isSymbolicLink())||!stats.at(-1)!.isFile()||stats.at(-1)!.nlink!==1n||stats.at(-1)!.size>524288n)throw fail('DOCUMENT_WRITE_FORBIDDEN');
 const executable=join(process.env.SystemRoot??'C:\\Windows','System32','WindowsPowerShell','v1.0','powershell.exe'),home=await mkdtemp(join(tmpdir(),'paos-document-write-'));
 const homeInfo=await lstat(home,{bigint:true}),directoryIdentity=`${homeInfo.dev}:${homeInfo.ino}`;
 const child=spawn(executable,['-NoLogo','-NoProfile','-NonInteractive','-File',fileURLToPath(new URL('./write.ps1',import.meta.url))],{windowsHide:true,shell:false,cwd:home,env:{SystemRoot:process.env.SystemRoot,WINDIR:process.env.WINDIR,PATH:dirname(executable),HOME:home,USERPROFILE:home,TEMP:home,TMP:home},stdio:['pipe','pipe','pipe']});
 let ended=false,closing:Promise<void>|undefined,buffer='',total=0,errors=0;const lines:any[]=[],waiting:Array<{resolve:(v:any)=>void;reject:(e:Error)=>void}>=[];
 const closed=new Promise<void>(done=>{child.once('close',()=>{ended=true;for(const p of waiting.splice(0))p.reject(fail('DOCUMENT_NATIVE_CLOSED'));done();});child.once('error',()=>{ended=true;for(const p of waiting.splice(0))p.reject(fail('DOCUMENT_NATIVE_UNAVAILABLE'));done();});});
 const timer=setTimeout(()=>child.kill(),15000);
 child.stdin.on('error',()=>{});child.stderr.on('data',chunk=>{errors+=chunk.length;if(errors>8192)child.kill();});
 child.stdout.on('data',chunk=>{total+=chunk.length;if(total>2*1024*1024){child.kill();return;}buffer+=chunk.toString('utf8');for(;;){const at=buffer.indexOf('\n');if(at<0)break;const line=buffer.slice(0,at).trim();buffer=buffer.slice(at+1);if(!line)continue;try{const value=JSON.parse(line),pending=waiting.shift();if(pending)pending.resolve(value);else lines.push(value);}catch{child.kill();}}});
 const read=()=>lines.length?Promise.resolve(lines.shift()):ended?Promise.reject(fail('DOCUMENT_NATIVE_CLOSED')):new Promise<any>((resolve,reject)=>waiting.push({resolve,reject}));
 const close=()=>closing??=(async()=>{clearTimeout(timer);child.stdin.end('\n');const force=setTimeout(()=>child.kill(),1000);await closed;clearTimeout(force);await rm(home,{recursive:true,force:true});})();
 try{
  child.stdin.write(JSON.stringify({paths,parentPid:process.pid,expectedHash:input.expectedHash})+'\n');const ready=await read();
  if(ready.error||!Array.isArray(ready.pins)||ready.pins.length!==paths.length||typeof ready.beforeBase64!=='string')throw fail('DOCUMENT_NATIVE_BUSY_OR_DENIED');
  for(let i=0;i<paths.length;i++){const pin=ready.pins[i],actual=String(pin.path).replace(/^\\\\\?\\/,'');if(actual.toLowerCase()!==paths[i].toLowerCase()||String(stats[i].dev)!==pin.volume||String(stats[i].ino)!==pin.fileId||i===paths.length-1&&(pin.links!=='1'||BigInt(pin.size)!==stats[i].size||(BigInt(pin.writeTicks)-116444736000000000n)*100n!==stats[i].mtimeNs))throw fail('DOCUMENT_SOURCE_CONFLICT');}
  const before=Buffer.from(ready.beforeBase64,'base64');if(before.length>512*1024||createHash('sha256').update(before).digest('hex')!==input.expectedHash)throw fail('DOCUMENT_SOURCE_CONFLICT');
  let committed=false;
  return {before,processId:child.pid!,temporaryDirectory:home,directoryIdentity,close,async commit(after,expectedHash){if(committed||ended||after.length>512*1024)throw fail('DOCUMENT_NATIVE_COMMIT_INVALID');committed=true;const afterHash=createHash('sha256').update(after).digest('hex');child.stdin.write(JSON.stringify({action:'commit',expectedHash,afterHash,afterBase64:after.toString('base64')})+'\n');const result=await read();if(result.error||result.afterHash!==afterHash||result.beforeHash!==expectedHash)throw fail('DOCUMENT_NATIVE_OUTCOME_UNCERTAIN');}};
 }catch(error){await close();throw error;}
}
