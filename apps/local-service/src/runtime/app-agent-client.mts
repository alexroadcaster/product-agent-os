import {open,lstat,unlink} from 'node:fs/promises';
import {isAbsolute,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash,randomUUID} from 'node:crypto';
import {validatedAgentOrigin,type AppAgentAction,type AppAgentDescriptor} from './app-agent-channel.mts';
const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
const identifier=(value:string)=>/^[A-Za-z0-9_-]{1,100}$/.test(value);
export type AppAgentClientAction=AppAgentAction|'reattach';
function publicResult(value:unknown,secrets:readonly string[]):unknown {
 if(typeof value==='string'){let text=value;for(const secret of secrets)if(secret)text=text.replaceAll(secret,'[REDACTED]');return text;}
 if(Array.isArray(value))return value.map(item=>publicResult(item,secrets));
 if(value&&typeof value==='object')return Object.fromEntries(Object.entries(value).filter(([key])=>!['leaseToken','capabilityToken'].includes(key)).map(([key,item])=>[publicResult(key,secrets) as string,publicResult(item,secrets)]));
 return value;
}
/** Checked bounded file read; no descriptor/state symlinks, hardlinks or replacement during the read. */
async function readPrivate(path:string):Promise<string>{
 if(!isAbsolute(path))fail('AGENT_PATH_INVALID');const before=await lstat(path,{bigint:true});
 if(!before.isFile()||before.isSymbolicLink()||before.nlink!==1n||before.size>65536n)fail('AGENT_FILE_INVALID');
 const handle=await open(path,'r');try{const opened=await handle.stat({bigint:true});if(opened.ino!==before.ino||opened.dev!==before.dev||opened.size!==before.size)fail('AGENT_FILE_CHANGED');
  const bytes=Buffer.alloc(65537);let count=0;while(count<bytes.length){const read=await handle.read(bytes,count,bytes.length-count,count);if(!read.bytesRead)break;count+=read.bytesRead;}
  const after=await handle.stat({bigint:true}),current=await lstat(path,{bigint:true});
  if(count>65536||after.size!==BigInt(count)||after.ino!==before.ino||after.dev!==before.dev||after.mtimeNs!==before.mtimeNs||after.ctimeNs!==before.ctimeNs||after.nlink!==1n||current.isSymbolicLink()||current.nlink!==1n||current.ino!==after.ino||current.dev!==after.dev||current.size!==after.size||current.mtimeNs!==after.mtimeNs||current.ctimeNs!==after.ctimeNs)fail('AGENT_FILE_CHANGED');
  return new TextDecoder('utf-8',{fatal:true}).decode(bytes.subarray(0,count));
 }finally{await handle.close();}
}
/** One finite operation for an explicitly invoked Codex App worker; never auto-wakes or launches an agent. */
export async function callAppAgent(options:Readonly<{descriptorPath:string;workerId:string;action:AppAgentClientAction;input?:Record<string,unknown>;previousStatePath?:string}>,dependencies:Readonly<{fetch?:typeof fetch}>={}) {
 if(!identifier(options.workerId)||!['attach','heartbeat','claim','report','command','operation','progress','reconcile','task-create','reattach'].includes(options.action))fail('AGENT_INPUT_INVALID');
 if(options.previousStatePath!==undefined&&(options.action!=='reattach'||!isAbsolute(options.previousStatePath)))fail('AGENT_INPUT_INVALID');
 const text=await readPrivate(options.descriptorPath);const descriptor=JSON.parse(text) as AppAgentDescriptor;
 if(descriptor.schemaVersion!=='paos_app_agent_channel_v1'||!/^[A-Za-z0-9-]{1,80}$/.test(descriptor.instanceId)||!/^[a-f0-9]{64}$/.test(descriptor.capabilityToken))fail('AGENT_DESCRIPTOR_INVALID');
 if(descriptor.profileId!==undefined&&(typeof descriptor.profileId!=='string'||!identifier(descriptor.profileId)))fail('AGENT_DESCRIPTOR_INVALID');
 validatedAgentOrigin(descriptor.origin);const request=dependencies.fetch??fetch;
 const statePath=options.descriptorPath+`.worker-${options.workerId}.json`;
 const descriptorDigest=createHash('sha256').update(text).digest('hex');
 let state:Record<string,unknown>;let stateFile:Awaited<ReturnType<typeof open>>|undefined;let identity:Awaited<ReturnType<typeof lstat>>|undefined;let created=false,previousStateText='',previousLease='';
 try {
  if(options.action==='attach'){
   state={schemaVersion:'paos_app_agent_worker_v1',instanceId:descriptor.instanceId,descriptorDigest,workerId:options.workerId,generation:randomUUID(),...(descriptor.profileId?{profileId:descriptor.profileId}:{})};
  }else{
   const sourcePath=options.previousStatePath??statePath;previousStateText=await readPrivate(sourcePath);state=JSON.parse(previousStateText);
   if(!state||typeof state!=='object'||Array.isArray(state)||state.schemaVersion!=='paos_app_agent_worker_v1'||state.workerId!==options.workerId
    ||typeof state.generation!=='string'||!identifier(state.generation)||typeof state.leaseToken!=='string'||!state.leaseToken||state.leaseToken.length>8192||!Number.isFinite(state.expiresAt)
    ||typeof state.instanceId!=='string'||!/^[A-Za-z0-9-]{1,80}$/.test(state.instanceId)||typeof state.descriptorDigest!=='string'||!/^[a-f0-9]{64}$/.test(state.descriptorDigest))fail('AGENT_WORKER_STATE_INVALID');
   previousLease=state.leaseToken as string;
   const sameInstance=state.instanceId===descriptor.instanceId&&state.descriptorDigest===descriptorDigest;
   if(!sameInstance){
    if(options.action!=='reattach'||!options.previousStatePath||resolve(sourcePath)===resolve(statePath)||!descriptor.profileId||state.profileId!==descriptor.profileId)fail('AGENT_WORKER_STATE_INVALID');
    // Explicit migration trusts the stable PAOS profile, not a ChatGPT account identity. Never alter the old state.
    state={...state,instanceId:descriptor.instanceId,descriptorDigest,profileId:descriptor.profileId};
   }else if(options.previousStatePath&&resolve(sourcePath)!==resolve(statePath))fail('AGENT_WORKER_STATE_INVALID');
   if(sameInstance&&state.profileId!==undefined&&state.profileId!==descriptor.profileId)fail('AGENT_WORKER_STATE_INVALID');
  }
  const health=await request(descriptor.origin+'/health',{redirect:'error',signal:AbortSignal.timeout(5000)});
  if(!health.ok)fail('AGENT_HEALTH_UNAVAILABLE');const observed=await health.json();if(observed.instanceId!==descriptor.instanceId||observed.alive!==true)fail('AGENT_INSTANCE_MISMATCH');
  const migrating=options.previousStatePath!==undefined&&resolve(options.previousStatePath)!==resolve(statePath);
  if(options.action==='attach'||migrating){stateFile=await open(statePath,'wx',0o600);identity=await stateFile.stat();created=true;}
  const attaching=options.action==='attach'||options.action==='reattach';
  const payload=attaching?{hostIdentity:'codex_app',workerId:options.workerId,generation:state.generation}:{...options.input,workerId:options.workerId,generation:state.generation,leaseToken:state.leaseToken};
  const body=JSON.stringify(payload);if(Buffer.byteLength(body)>65536)fail('AGENT_BODY_TOO_LARGE');
  const response=await request(descriptor.origin+'/agent/v1/'+(attaching?'attach':options.action),{method:'POST',redirect:'error',signal:AbortSignal.timeout(10000),headers:{origin:descriptor.origin,authorization:'Bearer '+descriptor.capabilityToken,'content-type':'application/json'},body});
  if(!response.ok)fail('AGENT_OPERATION_REJECTED');const result=await response.json();
  if(attaching){
   if(result.workerId!==options.workerId||result.generation!==state.generation||typeof result.leaseToken!=='string'||!result.leaseToken||!Number.isFinite(result.expiresAt))fail('AGENT_LEASE_INVALID');
   if(!created){
    const before=await lstat(statePath);if(!before.isFile()||before.isSymbolicLink()||before.nlink!==1)fail('AGENT_FILE_CHANGED');
    stateFile=await open(statePath,'r+');const current=await stateFile.stat();
    if(current.ino!==before.ino||current.dev!==before.dev||current.nlink!==1||await stateFile.readFile('utf8')!==previousStateText)fail('AGENT_FILE_CHANGED');
   }
   const encoded=Buffer.from(JSON.stringify({...state,leaseToken:result.leaseToken,expiresAt:result.expiresAt}));
   await stateFile!.write(encoded,0,encoded.length,0);await stateFile!.truncate(encoded.length);await stateFile!.sync();
   return publicResult(result,[descriptor.capabilityToken,result.leaseToken,previousLease]);
  }
  return publicResult(result,[descriptor.capabilityToken,String(state.leaseToken??'')]);
 }catch(error){if(created&&stateFile&&identity){try{const current=await lstat(statePath);if(current.ino===identity.ino&&current.dev===identity.dev&&current.nlink===1)await unlink(statePath);}catch{}}
  throw error;
 }finally{await stateFile?.close();}
}

async function main(args:string[]){
 if(![6,8,10].includes(args.length))fail('AGENT_CLI_USAGE');const values=Object.fromEntries(Array.from({length:args.length/2},(_,index)=>args.slice(index*2,index*2+2)));
 if(Object.keys(values).length!==args.length/2||!values['--descriptor']||!values['--worker']||!values['--action']||Object.keys(values).some(key=>!['--descriptor','--worker','--action','--input','--previous-state'].includes(key)))fail('AGENT_CLI_USAGE');
 const input=values['--input']?JSON.parse(await readPrivate(values['--input'])):undefined;if(input&&(!input||typeof input!=='object'||Array.isArray(input)))fail('AGENT_INPUT_INVALID');
 const result=await callAppAgent({descriptorPath:values['--descriptor'],workerId:values['--worker'],action:values['--action'] as AppAgentClientAction,input,previousStatePath:values['--previous-state']});console.log(JSON.stringify(result));
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))main(process.argv.slice(2)).catch(()=>{console.error('AGENT_CLIENT_OPERATION_FAILED');process.exitCode=1;});
