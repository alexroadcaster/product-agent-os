import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,dirname} from 'node:path';
import type {DatabaseMapLimits} from '../../../../packages/contracts/database-map.ts';
import type {DatabaseLease} from './lease.mts';
import type {extractDatabaseMetadata} from './extractor.mts';
const failure=(code:string)=>Object.assign(new Error(code),{code});
/** Own the native SQLite process through exit, then release the file lease.
 * The 64MiB JS heap flag does not cap SQLite's native allocations or RSS. */
export async function runSchemaExtractor(path:string,limits:DatabaseMapLimits,lease:DatabaseLease,signal?:AbortSignal):Promise<ReturnType<typeof extractDatabaseMetadata>&{metrics?:{elapsedMs:number;maxRssKiB:number}}>{
 const home=await mkdtemp(join(tmpdir(),'paos-db-extract-'));
 const child=spawn(process.execPath,['--max-old-space-size=64',fileURLToPath(new URL('./extractor.mts',import.meta.url))],{cwd:home,windowsHide:true,shell:false,env:{SystemRoot:process.env.SystemRoot,WINDIR:process.env.WINDIR,PATH:dirname(process.execPath),HOME:home,USERPROFILE:home,TEMP:home,TMP:home},stdio:['pipe','pipe','pipe']});
 let output='',stderrBytes=0,code:string|undefined,finished=false;
 const stop=(reason:string)=>{if(finished)return;code??=reason;child.kill();};
 const abort=()=>stop('DATABASE_SCHEMA_CANCELLED');signal?.addEventListener('abort',abort,{once:true});if(signal?.aborted)abort();
 const timer=setTimeout(()=>stop('DATABASE_SCHEMA_TIMEOUT'),limits.milliseconds);void lease.lost.then(()=>stop('DATABASE_LEASE_LOST'));
 child.stdin.on('error',()=>{});child.stdout.on('data',chunk=>{if(Buffer.byteLength(output)+chunk.length>limits.outputBytes){stop('DATABASE_SCHEMA_OUTPUT_LIMIT');return;}output+=chunk.toString();});child.stderr.on('data',chunk=>{stderrBytes+=chunk.length;if(stderrBytes>8192)stop('DATABASE_SCHEMA_OUTPUT_LIMIT');});
 try{
  const exit=await new Promise<number|null>((accept,reject)=>{child.once('error',()=>reject(failure('DATABASE_SCHEMA_RUNTIME_UNAVAILABLE')));child.once('close',accept);child.stdin.end(JSON.stringify({path,limits}));});
  if(code)throw failure(code);if(signal?.aborted)throw failure('DATABASE_SCHEMA_CANCELLED');let parsed:any;try{parsed=JSON.parse(output);}catch{throw failure('DATABASE_SCHEMA_OUTPUT_INVALID');}if(exit!==0||parsed.error)throw failure(parsed.error??'DATABASE_SCHEMA_UNAVAILABLE');
  if(!parsed.result||!Array.isArray(parsed.result.tables)||parsed.result.tables.length>limits.tables)throw failure('DATABASE_SCHEMA_OUTPUT_INVALID');return parsed.result;
 }finally{finished=true;clearTimeout(timer);signal?.removeEventListener('abort',abort);await rm(home,{recursive:true,force:true});}
}
