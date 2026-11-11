import {createServer,type IncomingMessage,type ServerResponse} from 'node:http';
import {Readable} from 'node:stream';
import {mkdir,readFile} from 'node:fs/promises';
import {join,isAbsolute,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {openLocalStore} from './storage/local-store.mts';
import {createLocalApplication} from './http/application.mts';
import {createLiveGateway} from './runtime/live-gateway.mts';
import {createNativeRpc} from './runtime/native-rpc.mts';
import {createAppAgentGateway} from './runtime/app-agent-gateway.mts';
import {createAppAgentChannel} from './runtime/app-agent-channel.mts';
import {createRuntimeRouteSelector} from './runtime/route-selector.ts';
import {createWindowsCredentialStore} from './connections/windows-credential-store.ts';
import {bindProfile,assertProfileIdentity,createProfileScopedStore} from './connections/profile-identity.mts';
import {createDomainTools} from './commands/domain-tools.mts';
import {inspectConfiguredRuntime} from '../../../packages/contracts/runtime/manifest.mts';
import {inspectLegacyWriterInventory} from './commands/writer-inventory.mts';

const failure=(code:string)=>Object.assign(new Error('The local request is unavailable.'),{code});
/** Bound raw bytes before constructing Request. Exact Host and origin prohibit proxy/absolute-target reinterpretation. */
export async function toFetchRequest(incoming:IncomingMessage,origin:string,signal?:AbortSignal):Promise<Request> {
 const expected=new URL(origin);
 const hosts=incoming.rawHeaders.filter((_,index)=>index%2===0&&incoming.rawHeaders[index].toLowerCase()==='host');
 if(hosts.length!==1||incoming.headers.host!==expected.host)throw failure('HOST_REJECTED');
 const target=incoming.url??'/';
 if(!target.startsWith('/')||target.startsWith('//')||target.includes('\\')||/[\r\n\0]/.test(target))throw failure('TARGET_REJECTED');
 const url=new URL(target,origin);if(url.origin!==origin)throw failure('TARGET_REJECTED');
 const method=incoming.method??'GET';
 const bodyLimit=method==='POST'&&/^\/api\/v1\/projects\/[^/]+\/imports\/preview$/.test(url.pathname)?3*1024*1024:1024*1024;
 const length=incoming.headers['content-length'];
 if(length!==undefined&&(!/^\d+$/.test(String(length))||Number(length)>bodyLimit))throw failure('REQUEST_TOO_LARGE');
 const chunks:Buffer[]=[];let bytes=0;
 for await(const chunk of incoming) {
  const data=Buffer.isBuffer(chunk)?chunk:Buffer.from(chunk);bytes+=data.length;
  if(bytes>bodyLimit)throw failure('REQUEST_TOO_LARGE');chunks.push(data);
 }
 if(['GET','HEAD'].includes(method)&&bytes)throw failure('BODY_REJECTED');
 const headers=new Headers();
 for(const [name,value] of Object.entries(incoming.headers))if(value!==undefined) {
  for(const item of Array.isArray(value)?value:[value])headers.append(name,item);
 }
 return new Request(url,{method,headers,body:bytes?Buffer.concat(chunks):undefined,signal});
}
async function respond(outgoing:ServerResponse,response:Response) {
 outgoing.statusCode=response.status;
 response.headers.forEach((value,name)=>{if(name.toLowerCase()!=='set-cookie')outgoing.setHeader(name,value);});
 const cookies=response.headers.getSetCookie();if(cookies.length)outgoing.setHeader('set-cookie',cookies);
 if(!response.body){outgoing.end();return;}
 await new Promise<void>((resolve,reject)=>{
  const body=Readable.fromWeb(response.body as any);body.on('error',reject);outgoing.on('error',reject);
  outgoing.on('finish',resolve);outgoing.on('close',()=>{body.destroy();resolve();});body.pipe(outgoing);
 });
}

/** Source-only executable wiring. Importing this module creates no database, server, GUI, or runtime child. */
export async function startLocalService(options:Readonly<{profileDirectory:string;instanceId:string}>,deps:Readonly<{
 openStore?:typeof openLocalStore;createHttpServer?:typeof createServer;createApplication?:typeof createLocalApplication;createGateway?:typeof createLiveGateway;
 prepareProfile?:(profile:string)=>Promise<void>;
}>={}) {
 if(!isAbsolute(options.profileDirectory)||options.profileDirectory.startsWith('\\\\')||!options.instanceId)throw failure('PROFILE_INVALID');
 await(deps.prepareProfile??(async(profile)=>{await mkdir(profile,{recursive:true,mode:0o700});}))(options.profileDirectory);
 const profile=await bindProfile(options.profileDirectory);const profileDirectory=profile.canonicalRoot;
 const store=await(deps.openStore??openLocalStore)({databasePath:join(profileDirectory,'state.sqlite')});
 let qualified=false;let providerAuthority=false;let stopping=false;
 try {qualified=(await inspectConfiguredRuntime(profileDirectory)).qualified;} catch {qualified=false;}
 const tools=createDomainTools({store});
 const gateway=(deps.createGateway??createLiveGateway)({store,profileId:profile.profileId,actorId:'local-runtime',
  isEnabled:()=>qualified,providerAuthority:()=>providerAuthority,credentialStore:createProfileScopedStore(profile,createWindowsCredentialStore()),
  dynamicTools:tools.specifications,domainTool:tools.dispatch,
  rpcFactory:async()=>{
   await assertProfileIdentity(profile);
   const check=await inspectConfiguredRuntime(profileDirectory);
   if(!check.qualified||!check.binaryPath)throw failure('RUNTIME_UNQUALIFIED');
   const selected=JSON.parse(await readFile(join(profileDirectory,'runtime-selection.json'),'utf8'));
   if(selected.providerAuthority!==true)throw failure('PROVIDER_AUTHORITY_REQUIRED');
   return createNativeRpc({profileDirectory,binaryPath:check.binaryPath});
  }});
 // App agents and the legacy API runtime are explicit choices; neither is a fallback for the other.
 const appGateway=createAppAgentGateway({store,profileId:profile.profileId,actorId:'codex-app-agent'});
 const selector=createRuntimeRouteSelector({app:appGateway,api:gateway,
  assertProfile:async()=>{if(stopping)throw failure('SERVICE_STOPPING');await assertProfileIdentity(profile);},
  // Recheck every project after route changes; project-local SQLite requireIdle is insufficient here.
  assertNoForeignUnresolved:async(requested)=>{
   for(const project of await store.projects())for(let offset=0;offset<100_000;offset+=100){
    const rows=await store.list(project.id,{kind:'run',limit:100,offset});
    for(const row of rows)if(!['completed','failed','interrupted'].includes(row.status)) {
     const own=requested==='codex_app_agent'?row.data.appAgentRun:row.data.runtimeRun;
     if(!own)throw failure('FOREIGN_RUNTIME_RECOVERY_REQUIRED');
    }
    if(rows.length<100)break;
    if(offset===99_900)throw failure('RUNTIME_HISTORY_LIMIT');
   }
  },
  beforeApiConnect:async()=>{
   const check=await inspectConfiguredRuntime(profileDirectory);qualified=check.qualified;
   try {providerAuthority=JSON.parse(await readFile(join(profileDirectory,'runtime-selection.json'),'utf8')).providerAuthority===true;}
   catch {providerAuthority=false;}
  }});
 const {connection,runtime}=selector;
 let agentChannel:Awaited<ReturnType<typeof createAppAgentChannel>>|undefined;
 let application:Awaited<ReturnType<typeof createLocalApplication>>|undefined;let origin='';
 const server=(deps.createHttpServer??createServer)(async(incoming,outgoing)=>{
  const controller=new AbortController();
  const aborted=()=>controller.abort();
  const disconnected=()=>{if(!outgoing.writableFinished)controller.abort();};
  incoming.once('aborted',aborted);outgoing.once('close',disconnected);
  if(incoming.aborted||outgoing.destroyed)controller.abort();
  try {
   if(stopping||!application)throw failure('SERVICE_STOPPING');
   const request=await toFetchRequest(incoming,origin,controller.signal);
   await respond(outgoing,await application.handleRequest(request));
  } catch(error) {
   if(outgoing.headersSent){outgoing.destroy();return;}
   const code=(error as {code?:string}).code;
   outgoing.statusCode=code==='REQUEST_TOO_LARGE'?413:code==='HOST_REJECTED'?403:400;
   outgoing.setHeader('content-type','application/json');outgoing.setHeader('cache-control','no-store');
   outgoing.end(JSON.stringify({error:{code:['REQUEST_TOO_LARGE','HOST_REJECTED','TARGET_REJECTED','SERVICE_STOPPING','BODY_REJECTED'].includes(code??'')?code:'INVALID_REQUEST'}}));
  } finally {incoming.off('aborted',aborted);outgoing.off('close',disconnected);}
 });
 server.requestTimeout=15_000;server.headersTimeout=10_000;server.keepAliveTimeout=2_000;server.maxHeadersCount=64;
 try {
  await new Promise<void>((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',()=>{server.off('error',reject);resolve();});});
  const address=server.address();if(!address||typeof address==='string')throw failure('LISTEN_FAILED');
  origin=`http://127.0.0.1:${address.port}`;
  agentChannel=await createAppAgentChannel({profileDirectory,instanceId:options.instanceId,origin,
   assertProfile:()=>assertProfileIdentity(profile),dispatch:(action,input)=>appGateway.agent(action,input)});
  application=await(deps.createApplication??createLocalApplication)({store,origin,instanceId:options.instanceId,profileDirectory,
   staticDirectory:fileURLToPath(new URL('../../web/dist/',import.meta.url)),connection,runtime,agentChannel,
   runtimeCapable:()=>connection.status().route==='local_api_byok'?qualified:appGateway.connection.status().verified,
   onQuit:()=>{if(!process.send||!process.connected)throw failure('OWNER_UNAVAILABLE');process.send({type:'quit_requested'},()=>{});},
   writerInventory:async(projectId)=>{const project=await store.project(projectId);if(!project)throw failure('PROJECT_NOT_FOUND');return inspectLegacyWriterInventory(project.canonicalRoot);}});
  let shutdown:Promise<void>|undefined;let serverClosing:Promise<void>|undefined;let gatewayClosed=false;let storeClosed=false;
  async function quit() {
   shutdown??=(async()=>{
    stopping=true;application!.revokeSessions();
    serverClosing??=new Promise<void>((resolve,reject)=>server.close((error)=>error?reject(error):resolve()));
    const failures:unknown[]=[];
    if(!gatewayClosed){
     try{await selector.drain();}catch(error){failures.push(error);}
     const results=await Promise.allSettled([appGateway.close(),gateway.close(),agentChannel?.close()]);
     for(const result of results)if(result.status==='rejected')failures.push(result.reason);
     gatewayClosed=true;
    }
    // Existing import/restore handlers retain their store until the HTTP server has drained.
    await serverClosing;
    if(!storeClosed){await store.close();storeClosed=true;}
    if(failures.length)throw failures[0];
   })().catch((error)=>{shutdown=undefined;throw error;});return shutdown;
  }
  return {port:address.port,instanceId:options.instanceId,build:'paos-m1-0.1.0',pairingCode:application.issuePairingCode(),
   appAgentDescriptorPath:agentChannel.descriptorPath,quit};
 } catch(error){server.close();await Promise.allSettled([appGateway.close(),gateway.close(),agentChannel?.close()]);await store.close();throw error;}
}

if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
 try {
  if(!process.send||!process.env.PAOS_PROFILE_DIR||!process.env.PAOS_INSTANCE_ID)throw failure('LAUNCHER_REQUIRED');
  const service=await startLocalService({profileDirectory:process.env.PAOS_PROFILE_DIR,instanceId:process.env.PAOS_INSTANCE_ID});
  let ending=false;
  const quit=async()=>{if(ending)return;ending=true;try{await service.quit();process.send?.({type:'stopped'},()=>process.exit(0));}catch{ending=false;process.exitCode=1;}};
  process.on('message',(message)=>{if(message&&typeof message==='object'&&(message as {type?:string}).type==='quit')void quit();});
  process.on('disconnect',()=>void quit());process.on('SIGTERM',()=>void quit());process.on('SIGINT',()=>void quit());
  process.send({type:'ready',port:service.port,instanceId:service.instanceId,build:service.build,pairingCode:service.pairingCode});
 } catch {process.exitCode=1;}
}
