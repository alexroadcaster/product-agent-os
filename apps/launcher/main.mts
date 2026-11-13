import {fork,spawn,type ChildProcess} from 'node:child_process';
import {get} from 'node:http';
import {mkdir} from 'node:fs/promises';
import {isAbsolute,join,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {launch,type RuntimeFingerprint,type LauncherPorts,type ServiceHealth,type OwnedLauncherControls} from './launcher.ts';
import {createProfileInstanceClaimer} from './profile-instance.ts';
import type {StopOutcome} from '../local-service/src/supervisor/lifecycle.ts';

// Owned requirements: research/product-agent-os-web-prd-2026-11-05.md SW-02;
// research/product-agent-os-web-architecture-2026-11-05.md runtime/lifecycle and ADR-W09;
// research/product-agent-os-web-auth-commercial-2026-11-09.md section 7 pairing bootstrap.

const BUILD='paos-m1-0.1.0';
export class NativeLauncherError extends Error {
 readonly code:string;
 constructor(code:string){super('The local launcher operation is unavailable.');this.code=code;}
}
const record=(value:unknown):Record<string,unknown>=>value!==null&&typeof value==='object'&&!Array.isArray(value)?value as Record<string,unknown>:{};

/** IPC readiness contains a short-lived pairing code; it is never published to the instance record or stdout. */
export async function startIpcService(options:Readonly<{child:ChildProcess;instanceId:string;build:string;
 onPairingCode:(code:string)=>void;onQuitRequested?:()=>void;stopTimeoutMs?:number}>,signal:AbortSignal) {
 const {child}=options;
 let ready=false;let stopped=false;let stopRequested=false;let exited=false;let exitCode:number|null=null;
 let resolveReady:(value:Record<string,unknown>|null)=>void=()=>{};let rejectReady:(error:Error)=>void=()=>{};
 let resolveExit:()=>void=()=>{};
 const exit=new Promise<void>((resolve)=>resolveExit=resolve);
 const readiness=new Promise<Record<string,unknown>|null>((resolve,reject)=>{resolveReady=resolve;rejectReady=reject;});
 const abort=()=>rejectReady(new NativeLauncherError('startup_unresolved'));
 signal.addEventListener('abort',abort,{once:true});
 child.on('message',(raw)=>{
  const message=record(raw);
  if(message.type==='quit_requested'){options.onQuitRequested?.();return;}
  if(message.type==='stopped'){if(stopRequested)stopped=true;return;}
  if(message.type!=='ready'||ready)return;
  if(message.instanceId!==options.instanceId||message.build!==options.build||typeof message.port!=='number'
   ||!Number.isInteger(message.port)||message.port<1||message.port>65535
   ||typeof message.pairingCode!=='string'||!message.pairingCode||message.pairingCode.length>256) {
   rejectReady(new NativeLauncherError('startup_unresolved'));return;
  }
  ready=true;options.onPairingCode(message.pairingCode);resolveReady(message);
 });
 child.on('error',()=>rejectReady(new NativeLauncherError('startup_unresolved')));
 child.on('exit',(code)=>{exited=true;exitCode=code;resolveExit();if(!ready)resolveReady(null);});
 if(signal.aborted)abort();
 let pendingStop:Promise<StopOutcome>|undefined;
 async function stop():Promise<StopOutcome> {
  if(exited)return stopped&&exitCode===0?{status:'stopped'}:{status:'stop_blocked',phase:'stop_children'};
  if(!child.connected)return {status:'stop_blocked',phase:'stop_children'};
  stopRequested=true;
  try {child.send({type:'quit'});}catch{return {status:'stop_blocked',phase:'stop_children'};}
  let timer:ReturnType<typeof setTimeout>|undefined;
  try {await Promise.race([exit,new Promise<void>((resolve)=>{timer=setTimeout(resolve,options.stopTimeoutMs??10_000);})]);}
  finally {if(timer)clearTimeout(timer);}
  return exited&&stopped&&exitCode===0?{status:'stopped'}:{status:'stop_blocked',phase:'stop_children'};
 }
 try {
  const message=await readiness;
  if(!message)return {status:'not_started' as const};
  return {status:'started' as const,port:message.port as number,
   quit(){pendingStop??=stop().finally(()=>pendingStop=undefined);return pendingStop;}};
 } finally {signal.removeEventListener('abort',abort);}
}

/** Fixed loopback destination, no redirects, bounded JSON; health identity is checked by launch(). */
export async function readLoopbackHealth(endpoint:Readonly<{instanceId:string;port:number}>,signal:AbortSignal):Promise<ServiceHealth> {
 if(!Number.isInteger(endpoint.port)||endpoint.port<1||endpoint.port>65535)throw new NativeLauncherError('health_invalid');
 return new Promise((resolve,reject)=>{
  const request=get({hostname:'127.0.0.1',port:endpoint.port,path:'/health',method:'GET',signal,
   headers:{Origin:`http://127.0.0.1:${endpoint.port}`}},(response)=>{
   let body='';response.setEncoding('utf8');
   response.on('data',(chunk:string)=>{body+=chunk;if(Buffer.byteLength(body)>4096)request.destroy(new NativeLauncherError('health_invalid'));});
   response.on('end',()=>{try{if(response.statusCode!==200)throw new Error();resolve(JSON.parse(body));}catch{reject(new NativeLauncherError('health_invalid'));}});
   response.on('error',()=>reject(new NativeLauncherError('health_unavailable')));
  });
  request.on('error',()=>reject(new NativeLauncherError('health_unavailable')));
 });
}

type WindowInput=Readonly<{origin:string;pairingCode?:string;owner:boolean;runtime:string;
 /** Explicit browser adapter for bounded acceptance or an owned browser profile; never inherit a user profile. */
 browserExecutable?:string;browserProfileDirectory?:string}>;
/** Browser/MessageBox side effects exist only behind the explicitly invoked launcher, never at module import. */
export async function nativeWindow(input:WindowInput,signal?:AbortSignal):Promise<'quit'|'closed'> {
 if(process.platform!=='win32'||!process.env.SystemRoot)throw new NativeLauncherError('native_ui_unavailable');
 if(!/^http:\/\/127\.0\.0\.1:[1-9][0-9]{0,4}$/.test(input.origin)||new URL(input.origin).port==='')throw new NativeLauncherError('origin_invalid');
 const executable=join(process.env.SystemRoot,'System32','WindowsPowerShell','v1.0','powershell.exe');
 return new Promise((resolve,reject)=>{
  const child=spawn(executable,['-NoLogo','-NoProfile','-NonInteractive','-STA','-File',fileURLToPath(new URL('./native-window.ps1',import.meta.url))],
   {windowsHide:true,shell:false,env:{SystemRoot:process.env.SystemRoot},stdio:['pipe','pipe','ignore']});
  let output='';child.stdout.setEncoding('utf8');
  const abort=()=>child.kill();signal?.addEventListener('abort',abort,{once:true});if(signal?.aborted)abort();
  child.stdout.on('data',(chunk:string)=>{output+=chunk;if(output.length>256){child.kill();reject(new NativeLauncherError('native_ui_failed'));}});
  child.on('error',()=>reject(new NativeLauncherError('native_ui_failed')));
  child.on('close',(code)=>{signal?.removeEventListener('abort',abort);if(signal?.aborted)resolve('closed');else if(code!==0)reject(new NativeLauncherError('native_ui_failed'));else resolve(output.trim()==='quit'?'quit':'closed');});
  child.stdin.on('error',()=>reject(new NativeLauncherError('native_ui_failed')));
   // Legacy pairing is retained in the internal IPC contract, never sent to the native browser opener.
   child.stdin.end(JSON.stringify({origin:input.origin,owner:input.owner,runtime:input.runtime,
    browserExecutable:input.browserExecutable,browserProfileDirectory:input.browserProfileDirectory}));
 });
}

/** Default entrypoint is local-only: provider authorization and native runtime qualification belong to service config. */
export async function runNativeLauncher(options:Readonly<{profileDirectory:string;
 inspectRuntime?:LauncherPorts['inspectRuntime'];expectedRuntime?:RuntimeFingerprint|null;
 serviceModule?:string;showWindow?:(input:WindowInput,signal?:AbortSignal)=>Promise<'quit'|'closed'>;
 readHealth?:typeof readLoopbackHealth}>) {
 if(!isAbsolute(options.profileDirectory)||options.profileDirectory.startsWith('\\\\'))throw new NativeLauncherError('profile_invalid');
 await mkdir(options.profileDirectory,{recursive:true,mode:0o700});
 let inspect=options.inspectRuntime;let expectedRuntime=options.expectedRuntime??null;
 if(!inspect) {
  // The shared manifest reader hashes configured binaries; it must not spawn Codex or discover inherited auth.
  try {
   const {inspectConfiguredRuntime}=await import('../../packages/contracts/runtime/manifest.mts');
   const configured=await inspectConfiguredRuntime(options.profileDirectory);
   expectedRuntime=configured.expected;
   const observed=configured.qualified?configured.fingerprint:{status:'unverified' as const};
   inspect=async()=>observed;
  } catch {inspect=async()=>({status:'unverified' as const});}
 }
 let pairingCode:string|undefined;let windowDone:Promise<void>|undefined;
 let ownerControl:OwnedLauncherControls|undefined;let pendingQuit=false;let requestedStop:Promise<void>|undefined;
 const windowAbort=new AbortController();
 async function requestOwnerQuit() {
  if(!ownerControl){pendingQuit=true;return;}
  requestedStop??=(async()=>{const outcome=await ownerControl!.quit();
   if(outcome.status==='stop_blocked')throw new NativeLauncherError('shutdown_unresolved');windowAbort.abort();
  })().finally(()=>{requestedStop=undefined;});
  return requestedStop;
 }
 const host={
  async startService(input:{instanceId:string},signal:AbortSignal) {
   const child=fork(options.serviceModule??fileURLToPath(new URL('../local-service/src/main.mts',import.meta.url)),[],{
    execArgv:[],windowsHide:true,silent:true,env:{SystemRoot:process.env.SystemRoot,
     PAOS_PROFILE_DIR:options.profileDirectory,PAOS_INSTANCE_ID:input.instanceId}});
   // Service logs are not a transport and must never expose pairing/auth material.
   child.stdout?.resume();child.stderr?.resume();
   return startIpcService({child,instanceId:input.instanceId,build:BUILD,onPairingCode(code){pairingCode=code;},
    onQuitRequested(){void requestOwnerQuit().catch(()=>process.stderr.write('PAOS launcher: shutdown_unresolved\n'));}},signal);
  },
  readHealth:options.readHealth??readLoopbackHealth,
 };
 const result=await launch({claimInstance:createProfileInstanceClaimer(options.profileDirectory,host),
  inspectRuntime:inspect,
  async openUi(origin,state,_signal,owner) {
   ownerControl=owner;if(pendingQuit){pendingQuit=false;void requestOwnerQuit().catch(()=>process.stderr.write('PAOS launcher: shutdown_unresolved\n'));}
   windowDone=(async()=>{
    try {
     const action=await(options.showWindow??nativeWindow)({origin,pairingCode,owner:!!owner,runtime:state.runtime},windowAbort.signal);
     pairingCode=undefined;
     if(owner&&action==='quit') {
      const stopped=await owner.quit();if(stopped.status==='stop_blocked')throw new NativeLauncherError('shutdown_unresolved');
     }
    } catch(error) {
     pairingCode=undefined;
     if(owner){const stopped=await owner.quit();if(stopped.status==='stop_blocked')throw new NativeLauncherError('shutdown_unresolved');}
     throw error;
    }
   })();
   // Attach a handler immediately; launch() does not wait on human interaction.
   windowDone.catch(()=>{});
  }},{serviceBuild:BUILD,runtime:expectedRuntime,browserLaunchVersion:1});
 if(result.status==='opened'&&windowDone)await windowDone;
 return result;
}

if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
 try {
  if(process.argv.length!==4||process.argv[2]!=='--profile')throw new NativeLauncherError('profile_argument_required');
  const result=await runNativeLauncher({profileDirectory:process.argv[3]});
  if(result.status!=='opened'){process.stderr.write(`PAOS launcher: ${result.status}\n`);
   if(result.status==='service_restart_required')process.stderr.write('Завершите прежний экземпляр через Выход / Quit и повторите запуск. Данные профиля сохранятся.\n');process.exitCode=1;}
 } catch(error) {process.stderr.write(`PAOS launcher: ${error instanceof NativeLauncherError?error.code:'unavailable'}\n`);process.exitCode=1;}
}
