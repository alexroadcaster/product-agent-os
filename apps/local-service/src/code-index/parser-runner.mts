import {spawn} from 'node:child_process';
import {mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {dirname,join,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const failure=(code:string)=>Object.assign(Error(code),{code});
/** A native parser fatal error must not terminate the local HTTP/storage host.
 * Only a trusted checked-in script runs; target source is stdin data, never code. */
export async function runGraphParser(input:unknown,options:{signal?:AbortSignal;milliseconds?:number;onChildStarted?:(pid:number)=>void}={}){
 const milliseconds=options.milliseconds??10000;if(!Number.isSafeInteger(milliseconds)||milliseconds<1||milliseconds>10000)throw failure('GRAPH_BUILD_LIMIT');
 if(options.signal?.aborted)throw failure('GRAPH_BUILD_CANCELLED');const encoded=JSON.stringify({...input as object,watchdogMilliseconds:milliseconds+1000});if(Buffer.byteLength(encoded)>20*1024*1024)throw failure('GRAPH_BUILD_LIMIT');
 const scratch=resolve(tmpdir()),home=await mkdtemp(join(scratch,'paos-graph-parser-'));let child:ReturnType<typeof spawn>|undefined,ended=false,reason:string|undefined,timer:ReturnType<typeof setTimeout>|undefined;
 const stop=(code:string)=>{reason??=code;if(!ended)child?.kill('SIGKILL');},abort=()=>stop('GRAPH_BUILD_CANCELLED');
 try{child=spawn(process.execPath,['--max-old-space-size=128',fileURLToPath(new URL('./parser-worker.mts',import.meta.url))],{cwd:home,windowsHide:true,shell:false,env:{SystemRoot:process.env.SystemRoot,WINDIR:process.env.WINDIR,PATH:dirname(process.execPath),HOME:home,USERPROFILE:home,TEMP:home,TMP:home},stdio:['pipe','pipe','pipe']});
  let bytes=0,stderr=0;const chunks:Buffer[]=[];child.stdin!.on('error',()=>{});child.stdout!.on('data',(chunk:Buffer)=>{bytes+=chunk.length;if(bytes>16*1024*1024)stop('GRAPH_BUILD_LIMIT');else chunks.push(chunk);});child.stderr!.on('data',(chunk:Buffer)=>{stderr+=chunk.length;if(stderr>8192)stop('GRAPH_PARSER_UNAVAILABLE');});
  const closed=new Promise<number|null>((accept,reject)=>{child!.once('error',()=>reject(failure('GRAPH_PARSER_UNAVAILABLE')));child!.once('close',code=>{ended=true;accept(code);});});
  timer=setTimeout(()=>stop('GRAPH_BUILD_LIMIT'),milliseconds);options.signal?.addEventListener('abort',abort,{once:true});if(options.signal?.aborted)abort();child.stdin!.end(encoded);if(child.pid)options.onChildStarted?.(child.pid);
  const exit=await closed;if(reason)throw failure(reason);if(exit!==0)throw failure('GRAPH_PARSER_UNAVAILABLE');let result:any;try{result=JSON.parse(Buffer.concat(chunks).toString('utf8'));}catch{throw failure('GRAPH_PARSER_UNAVAILABLE');}if(result.error)throw failure(result.error);if(!Array.isArray(result.results)||result.results.length>1000)throw failure('GRAPH_BUILD_LIMIT');return result;
 }finally{clearTimeout(timer);options.signal?.removeEventListener('abort',abort);if(child&&!ended){child.kill('SIGKILL');await new Promise<void>(done=>child!.once('close',()=>done()));}if(dirname(home)!==scratch)throw failure('GRAPH_PARSER_UNAVAILABLE');await rm(home,{recursive:true,force:true});}
}
