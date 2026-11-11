import {open,lstat,unlink} from 'node:fs/promises';
import {isAbsolute,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash,randomUUID} from 'node:crypto';
import {validatedAgentOrigin,type AppAgentAction,type AppAgentDescriptor} from './app-agent-channel.mts';
const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
const identifier=(value:string)=>/^[A-Za-z0-9_-]{1,100}$/.test(value);
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
export async function callAppAgent(options:Readonly<{descriptorPath:string;workerId:string;action:AppAgentAction;input?:Record<string,unknown>}>,dependencies:Readonly<{fetch?:typeof fetch}>={}) {
 if(!identifier(options.workerId)||!['attach','heartbeat','claim','report'].includes(options.action))fail('AGENT_INPUT_INVALID');
 const text=await readPrivate(options.descriptorPath);const descriptor=JSON.parse(text) as AppAgentDescriptor;
 if(descriptor.schemaVersion!=='paos_app_agent_channel_v1'||!/^[A-Za-z0-9-]{1,80}$/.test(descriptor.instanceId)||!/^[a-f0-9]{64}$/.test(descriptor.capabilityToken))fail('AGENT_DESCRIPTOR_INVALID');
 validatedAgentOrigin(descriptor.origin);const request=dependencies.fetch??fetch;
 const health=await request(descriptor.origin+'/health',{redirect:'error',signal:AbortSignal.timeout(5000)});
 if(!health.ok)fail('AGENT_HEALTH_UNAVAILABLE');const observed=await health.json();if(observed.instanceId!==descriptor.instanceId||observed.alive!==true)fail('AGENT_INSTANCE_MISMATCH');
 const statePath=options.descriptorPath+`.worker-${options.workerId}.json`;
 const descriptorDigest=createHash('sha256').update(text).digest('hex');
 let state:Record<string,unknown>;let stateFile:Awaited<ReturnType<typeof open>>|undefined;let identity:Awaited<ReturnType<typeof lstat>>|undefined;
 try {
  if(options.action==='attach'){
   stateFile=await open(statePath,'wx',0o600);identity=await stateFile.stat();
   state={schemaVersion:'paos_app_agent_worker_v1',instanceId:descriptor.instanceId,descriptorDigest,workerId:options.workerId,generation:randomUUID()};
  }else{
   state=JSON.parse(await readPrivate(statePath));
   if(state.schemaVersion!=='paos_app_agent_worker_v1'||state.instanceId!==descriptor.instanceId||state.descriptorDigest!==descriptorDigest||state.workerId!==options.workerId||typeof state.generation!=='string'||typeof state.leaseToken!=='string'||!state.leaseToken)fail('AGENT_WORKER_STATE_INVALID');
  }
  const payload=options.action==='attach'?{hostIdentity:'codex_app',workerId:options.workerId,generation:state.generation}:{...options.input,workerId:options.workerId,generation:state.generation,leaseToken:state.leaseToken};
  const body=JSON.stringify(payload);if(Buffer.byteLength(body)>65536)fail('AGENT_BODY_TOO_LARGE');
  const response=await request(descriptor.origin+'/agent/v1/'+options.action,{method:'POST',redirect:'error',signal:AbortSignal.timeout(10000),headers:{origin:descriptor.origin,authorization:'Bearer '+descriptor.capabilityToken,'content-type':'application/json'},body});
  if(!response.ok)fail('AGENT_OPERATION_REJECTED');const result=await response.json();
  if(options.action==='attach'){
   if(result.workerId!==options.workerId||result.generation!==state.generation||typeof result.leaseToken!=='string'||!result.leaseToken||!Number.isFinite(result.expiresAt))fail('AGENT_LEASE_INVALID');
   await stateFile!.writeFile(JSON.stringify({...state,leaseToken:result.leaseToken,expiresAt:result.expiresAt}));await stateFile!.sync();
   return publicResult(result,[descriptor.capabilityToken,result.leaseToken]);
  }
  return publicResult(result,[descriptor.capabilityToken,String(state.leaseToken??'')]);
 }catch(error){if(stateFile&&identity){try{const current=await lstat(statePath);if(current.ino===identity.ino&&current.dev===identity.dev&&current.nlink===1)await unlink(statePath);}catch{}}
  throw error;
 }finally{await stateFile?.close();}
}

async function main(args:string[]){
 if(args.length!==6&&args.length!==8)fail('AGENT_CLI_USAGE');const values=Object.fromEntries(Array.from({length:args.length/2},(_,index)=>args.slice(index*2,index*2+2)));
 if(!values['--descriptor']||!values['--worker']||!values['--action']||Object.keys(values).some(key=>!['--descriptor','--worker','--action','--input'].includes(key)))fail('AGENT_CLI_USAGE');
 const input=values['--input']?JSON.parse(await readPrivate(values['--input'])):undefined;if(input&&(!input||typeof input!=='object'||Array.isArray(input)))fail('AGENT_INPUT_INVALID');
 const result=await callAppAgent({descriptorPath:values['--descriptor'],workerId:values['--worker'],action:values['--action'] as AppAgentAction,input});console.log(JSON.stringify(result));
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))main(process.argv.slice(2)).catch(()=>{console.error('AGENT_CLIENT_OPERATION_FAILED');process.exitCode=1;});
