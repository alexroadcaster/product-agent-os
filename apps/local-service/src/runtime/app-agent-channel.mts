import {join,isAbsolute} from 'node:path';
import {open,lstat,unlink} from 'node:fs/promises';
import {randomBytes,createHash,timingSafeEqual} from 'node:crypto';
export type AppAgentAction='attach'|'heartbeat'|'claim'|'report';
export type AppAgentDescriptor=Readonly<{schemaVersion:'paos_app_agent_channel_v1';instanceId:string;origin:string;capabilityToken:string}>;
const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
export function validatedAgentOrigin(origin:string):string {
 const url=new URL(origin);
 if(url.protocol!=='http:'||url.hostname!=='127.0.0.1'||!url.port||url.origin!==origin)fail('AGENT_ORIGIN_INVALID');
 return origin;
}
function equal(first:string,second:string){return timingSafeEqual(createHash('sha256').update(first).digest(),createHash('sha256').update(second).digest());}
function response(value:unknown,status=200){return Response.json(value??null,{status,headers:{'cache-control':'no-store','x-content-type-options':'nosniff'}});}

/** A private per-instance capability channel. Browser cookies confer no authority here. */
export async function createAppAgentChannel(options:Readonly<{profileDirectory:string;instanceId:string;origin:string;assertProfile:()=>Promise<void>;dispatch:(action:AppAgentAction,input:Record<string,unknown>)=>Promise<unknown>}>) {
 validatedAgentOrigin(options.origin);
 if(!isAbsolute(options.profileDirectory)||!/^[A-Za-z0-9-]{1,80}$/.test(options.instanceId))fail('AGENT_DESCRIPTOR_INVALID');
 await options.assertProfile();
 const directory=await lstat(options.profileDirectory);if(!directory.isDirectory()||directory.isSymbolicLink())fail('AGENT_PROFILE_INVALID');
 const descriptorPath=join(options.profileDirectory,`app-agent-${options.instanceId}.json`);
 const descriptor:AppAgentDescriptor={schemaVersion:'paos_app_agent_channel_v1',instanceId:options.instanceId,origin:options.origin,capabilityToken:randomBytes(32).toString('hex')};
 const encoded=JSON.stringify(descriptor);const file=await open(descriptorPath,'wx',0o600);
 let identity;try{await file.writeFile(encoded);await file.sync();identity=await file.stat({bigint:true});}finally{await file.close();}
 let closed=false;
 return {descriptorPath,
  async handle(request:Request):Promise<Response>{
   try {
    if(closed)fail('AGENT_CHANNEL_CLOSED');
    const url=new URL(request.url);
    if(url.origin!==options.origin||request.headers.get('host')!==new URL(options.origin).host||request.headers.get('origin')!==options.origin
     ||request.headers.has('forwarded')||request.headers.has('x-forwarded-host')||request.headers.get('sec-fetch-site')==='cross-site')fail('AGENT_ORIGIN_REJECTED');
    if(request.method!=='POST')fail('AGENT_METHOD_REJECTED');
    const match=/^\/agent\/v1\/(attach|heartbeat|claim|report)$/.exec(url.pathname);
    if(!match||url.search)throw Object.assign(new Error('AGENT_ROUTE_NOT_FOUND'),{code:'AGENT_ROUTE_NOT_FOUND'});
    const bearer=request.headers.get('authorization')??'';
    if(!bearer.startsWith('Bearer ')||!equal(bearer.slice(7),descriptor.capabilityToken))fail('AGENT_CAPABILITY_REQUIRED');
    if(request.headers.get('content-type')?.split(';')[0].trim()!=='application/json')fail('AGENT_JSON_REQUIRED');
    const declared=request.headers.get('content-length');if(declared!==null&&(!/^\d+$/.test(declared)||Number(declared)>65536))fail('AGENT_BODY_TOO_LARGE');
    const reader=request.body?.getReader();const chunks:Uint8Array[]=[];let bytes=0;
    try{if(reader)while(true){const part=await reader.read();if(part.done)break;bytes+=part.value.length;if(bytes>65536){await reader.cancel();fail('AGENT_BODY_TOO_LARGE');}chunks.push(part.value);}}finally{reader?.releaseLock();}
    let input:unknown;try{input=JSON.parse(Buffer.concat(chunks).toString('utf8'));}catch{fail('AGENT_JSON_INVALID');}
    if(!input||typeof input!=='object'||Array.isArray(input))fail('AGENT_INPUT_INVALID');
    // A worker can accidentally echo its local channel capability in a final answer.
    if(match[1]==='report'&&typeof (input as Record<string,unknown>).text==='string') {
      (input as Record<string,unknown>).text=((input as Record<string,unknown>).text as string).replaceAll(descriptor.capabilityToken,'[REDACTED]');
    }
    await options.assertProfile();if(closed)fail('AGENT_CHANNEL_CLOSED');
    return response(await options.dispatch(match[1] as AppAgentAction,input as Record<string,unknown>));
   }catch(error){const candidate=(error as {code?:unknown})?.code;const code=typeof candidate==='string'&&/^[A-Za-z][A-Za-z0-9_]{0,79}$/.test(candidate)?candidate:'AGENT_OPERATION_FAILED';
    return response({error:{code}},code==='AGENT_CAPABILITY_REQUIRED'?401:/ORIGIN/.test(code)?403:/TOO_LARGE/.test(code)?413:/METHOD/.test(code)?405:/NOT_FOUND/.test(code)?404:/JSON_REQUIRED/.test(code)?415:409);}
  },
  async close(){closed=true;
   try{await options.assertProfile();const current=await lstat(descriptorPath,{bigint:true});
    if(!current.isFile()||current.isSymbolicLink()||current.nlink!==1n||current.dev!==identity.dev||current.ino!==identity.ino||current.size!==BigInt(Buffer.byteLength(encoded)))return;
    const handle=await open(descriptorPath,'r');try{const info=await handle.stat({bigint:true});if(info.dev!==identity.dev||info.ino!==identity.ino||await handle.readFile('utf8')!==encoded)return;}finally{await handle.close();}
    const final=await lstat(descriptorPath,{bigint:true});if(final.dev===identity.dev&&final.ino===identity.ino&&final.nlink===1n)await unlink(descriptorPath);
   }catch(error){if((error as NodeJS.ErrnoException).code!=='ENOENT')return;}
  }};
}
