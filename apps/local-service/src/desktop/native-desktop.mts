import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {join} from 'node:path';
import {bindProject} from '../adapters/project-sources.ts';

export type FolderSelection={cancelled:true}|{cancelled:false;workspaceRoot:string};
export type DesktopActions={selectProjectDirectory(signal?:AbortSignal,initialDirectory?:string):Promise<FolderSelection>;openCodexDraft(url:string,signal?:AbortSignal):Promise<void>;close():Promise<void>};
const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};

/** Own only our short-lived native helper. No shell interpolation, clipboard or user-app termination. */
export function createNativeDesktop(options:{spawnProcess?:typeof spawn;timeoutMs?:number;closeTimeoutMs?:number}={}):DesktopActions{
 let child:ReturnType<typeof spawn>|undefined,closed=false;
 async function invoke(input:Record<string,string>,signal?:AbortSignal):Promise<any>{
  if(closed)fail('DESKTOP_CLOSED');if(child)fail('DESKTOP_BUSY');
  if(process.platform!=='win32'||!process.env.SystemRoot)fail('DESKTOP_UNAVAILABLE');
  if(signal?.aborted)fail('DESKTOP_CANCELLED');
  return new Promise((resolve,reject)=>{
   const owned=(options.spawnProcess??spawn)(join(process.env.SystemRoot!,'System32','WindowsPowerShell','v1.0','powershell.exe'),['-NoLogo','-NoProfile','-NonInteractive','-STA','-File',fileURLToPath(new URL('./native-desktop.ps1',import.meta.url))],{windowsHide:true,shell:false,env:{SystemRoot:process.env.SystemRoot},stdio:['pipe','pipe','ignore']});
   child=owned;let output='',reason:string|undefined;
   const abort=()=>{reason='DESKTOP_CANCELLED';owned.kill();};
   const timer=setTimeout(()=>{reason='DESKTOP_TIMEOUT';owned.kill();},options.timeoutMs??(input.action==='folder'?300000:15000));
   signal?.addEventListener('abort',abort,{once:true});if(signal?.aborted)abort();
   const cleanup=()=>{clearTimeout(timer);signal?.removeEventListener('abort',abort);if(child===owned)child=undefined;};
   owned.stdout.setEncoding('utf8');owned.stdout.on('data',(part:string)=>{output+=part;if(Buffer.byteLength(output)>16384){reason='DESKTOP_OUTPUT_INVALID';owned.kill();}});
   owned.on('error',()=>{cleanup();reject(Object.assign(Error('Native desktop action unavailable'),{code:'DESKTOP_UNAVAILABLE'}));});
   owned.on('close',(code)=>{cleanup();try{if(reason||code!==0)fail(reason??(input.action==='folder'?'FOLDER_PICKER_UNAVAILABLE':'CODEX_APP_OPEN_FAILED'));const value=JSON.parse(output.replace(/^\uFEFF/,''));resolve(value);}catch(error){reject(error);}});
   owned.stdin.on('error',()=>{reason='DESKTOP_UNAVAILABLE';});owned.stdin.end(JSON.stringify(input));
  });
 }
 return {
  async selectProjectDirectory(signal,initialDirectory){const initial=initialDirectory?(await bindProject('folder-initial',initialDirectory)).workspaceRoot:'';
   const result=await invoke({action:'folder',title:'Выберите папку проекта — Product-Agent OS',initialDirectory:initial},signal);
   if(result.cancelled===true)return {cancelled:true};if(result.cancelled!==false||typeof result.workspaceRoot!=='string'||result.workspaceRoot.length>4096)fail('FOLDER_SELECTION_INVALID');
   const pin=await bindProject('folder-selection',result.workspaceRoot);return {cancelled:false,workspaceRoot:pin.workspaceRoot};},
  async openCodexDraft(raw,signal){const url=new URL(raw);if(url.protocol!=='codex:'||url.hostname!=='new'||url.username||url.password||url.hash||[...url.searchParams.keys()].some(k=>!['path','prompt'].includes(k))||raw.length>24000)fail('APP_HANDOFF_INVALID');
   const result=await invoke({action:'codex',url:raw},signal);if(result.opened!==true)fail('CODEX_APP_OPEN_FAILED');},
  async close(){closed=true;const owned=child;if(owned){await new Promise<void>((resolve,reject)=>{
   const finish=()=>{clearTimeout(timer);resolve();},unresolved=()=>{owned.off('close',finish);reject(Object.assign(Error('Native helper shutdown unresolved'),{code:'DESKTOP_SHUTDOWN_UNRESOLVED'}));};
   const timer=setTimeout(unresolved,options.closeTimeoutMs??3000);owned.once('close',finish);
   if(!owned.kill()){clearTimeout(timer);unresolved();}
  });}},
 };
}
