import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {createHash} from 'node:crypto';
import {mkdtemp,mkdir,readFile,writeFile,stat,realpath,rm} from 'node:fs/promises';
import {join,resolve,win32,basename} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createInterface} from 'node:readline/promises';
import {runNativeLauncher,nativeWindow,readLoopbackHealth} from '../../../apps/launcher/main.mts';

export type ProcessObservation=Readonly<{pid:number;parentPid:number;path:string}>;
const normalized=(path:string)=>win32.normalize(path).toLowerCase();
const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
export function desktopExecutableName(path:string):string {
 if(!/^[a-z]:\\Program Files\\WindowsApps\\OpenAI\.Codex_[A-Za-z0-9._-]+\\app\\(?:ChatGPT|Codex)\.exe$/i.test(win32.normalize(path)))fail('DESKTOP_EXECUTABLE_REQUIRED');
 return win32.basename(path);
}
/** A missing ancestor is uncertainty, never permission to proceed. Explorer is the external desktop anchor. */
export function assertExternalParent(rows:readonly ProcessObservation[],pid:number,desktopExe:string,systemRoot:string):void {
 const seen=new Set<number>();
 for(let depth=0;depth<64;depth++) {
  const row=rows.find(row=>row.pid===pid);
  if(!row||!row.path||seen.has(pid))fail('ANCESTRY_UNVERIFIED');
  if(normalized(row.path)===normalized(desktopExe))fail('APP_ANCESTOR');
  if(normalized(row.path)===normalized(win32.join(systemRoot,'explorer.exe')))return;
  seen.add(pid);if(row.parentPid===0)return;pid=row.parentPid;
 }
 fail('ANCESTRY_UNVERIFIED');
}

/** Sampled absence is not continuous OS tracing. A gap invalidates this qualification attempt permanently. */
export class AbsenceMonitor {
 private start:number|null=null;private last:number|null=null;private samples=0;private invalid=false;
 private desktopExe:string;private maxGapMs:number;
 constructor(desktopExe:string,maxGapMs=10_000){this.desktopExe=desktopExe;this.maxGapMs=maxGapMs;}
 observe(rows:readonly ProcessObservation[],at:number) {
  if(this.invalid)fail('ABSENCE_INVALIDATED');
  if(!Array.isArray(rows)||!rows.length||rows.some(row=>!row||!Number.isInteger(row.pid)||row.pid<=0||!Number.isInteger(row.parentPid)||row.parentPid<0||typeof row.path!=='string'||!win32.isAbsolute(row.path))){this.invalid=true;fail('INVENTORY_INVALID');}
  if(!Number.isFinite(at)||(this.last!==null&&(at<this.last||at-this.last>this.maxGapMs))) {this.invalid=true;fail('OBSERVATION_GAP');}
  if(rows.some(row=>normalized(row.path)===normalized(this.desktopExe))){this.invalid=true;fail('APP_RUNNING');}
  this.start??=at;this.last=at;this.samples++;
 }
 invalidate(){this.invalid=true;}
 receipt(){return {coverage:'sampled_process_inventory',valid:!this.invalid&&this.samples>=2,from:this.start,to:this.last,samples:this.samples,maxGapMs:this.maxGapMs};}
}

/** Only PID, parent PID, and executable path leave CIM. No command line, window title, or chat is read. */
async function inventory(desktopExe:string):Promise<ProcessObservation[]> {
 const systemRoot=process.env.SystemRoot;if(!systemRoot)fail('WINDOWS_REQUIRED');
 const selectedName=desktopExecutableName(desktopExe);
 const script="$ErrorActionPreference='Stop'; if ($env:PAOS_DESKTOP_EXE_NAME -notin @('ChatGPT.exe','Codex.exe')) { throw 'Invalid selection' }; $rows=@(Get-CimInstance Win32_Process | ForEach-Object { if ($_.Name -ieq $env:PAOS_DESKTOP_EXE_NAME -and -not $_.ExecutablePath) { throw 'Unobservable desktop process' }; if ($_.ExecutablePath) { @{pid=[int]$_.ProcessId;parentPid=[int]$_.ParentProcessId;path=[string]$_.ExecutablePath} } }); ConvertTo-Json -Compress -InputObject $rows";
 const {stdout}=await promisify(execFile)(join(systemRoot,'System32','WindowsPowerShell','v1.0','powershell.exe'),
  ['-NoLogo','-NoProfile','-NonInteractive','-EncodedCommand',Buffer.from(script,'utf16le').toString('base64')],
  {windowsHide:true,timeout:8000,maxBuffer:2*1024*1024,env:{SystemRoot:systemRoot,PAOS_DESKTOP_EXE_NAME:selectedName}});
 const rows:unknown=JSON.parse(stdout.replace(/^\uFEFF/,''));
 if(!Array.isArray(rows)||!rows.length||rows.length>10000||rows.some(row=>!row||!Number.isInteger(row.pid)||row.pid<=0||!Number.isInteger(row.parentPid)||row.parentPid<0||typeof row.path!=='string'||!win32.isAbsolute(row.path)))fail('INVENTORY_INVALID');
 return rows as ProcessObservation[];
}
const pause=(ms:number)=>new Promise<void>(accept=>setTimeout(accept,ms));
async function exists(path:string){try{await stat(path);return true;}catch(error){if((error as NodeJS.ErrnoException).code==='ENOENT')return false;throw error;}}

async function main(args:string[]) {
 if(process.platform!=='win32'||args.length!==2||args[0]!=='--desktop-exe'||!win32.isAbsolute(args[1])||args[1].startsWith('\\\\'))fail('USAGE_STANDALONE_DESKTOP_EXE');
 const desktopExe=await realpath(args[1]);desktopExecutableName(desktopExe);if(!(await stat(desktopExe)).isFile())fail('DESKTOP_EXECUTABLE_REQUIRED');
 assertExternalParent(await inventory(desktopExe),process.pid,desktopExe,process.env.SystemRoot!);
 const scratch=fileURLToPath(new URL('../../../.tmp/paos-m1/',import.meta.url));await mkdir(scratch,{recursive:true});
 const fixture=await mkdtemp(join(scratch,'standalone-'));const profile=join(fixture,'profile');const workspace=join(fixture,'workspace');
 await mkdir(profile);await mkdir(workspace);
 const receiptPath=join(scratch,`${basename(fixture)}-result.json`);
 const receipt:Record<string,unknown>={status:'needs_user_acceptance',syntheticOnly:true,providerUsed:false,keysUsed:false,vaultUsed:false,
  appClosedByRunner:false,forcedTermination:false,startedAt:new Date().toISOString(),desktopExe,fixture,
  actualSignals:{},ownerAttestations:null,limits:['Absence is sampled, not continuous tracing.','Native dialog return does not prove browser interactions.','No provider/runtime turn acceptance.']};
 const signals=receipt.actualSignals as Record<string,unknown>;
 const sourceHashes:Record<string,string>={};
 receipt.sourceHashes=sourceHashes;
 let monitor:AbsenceMonitor|undefined;let sampling:Promise<void>|undefined;let stopSampling=false;let observationError:string|undefined;
 const abort=new AbortController();let deadline:ReturnType<typeof setTimeout>|undefined;
 const lock=join(profile,'service-instance');
 try {
  for(const relative of ['tests/web/single-window/standalone-acceptance.mts','apps/launcher/main.mts','apps/launcher/launcher.ts','apps/launcher/profile-instance.ts','apps/launcher/native-window.ps1','apps/local-service/src/main.mts','apps/web/dist/index.html']) {
   sourceHashes[relative]=createHash('sha256').update(await readFile(fileURLToPath(new URL('../../../'+relative,import.meta.url)))).digest('hex');
  }
  console.log('Ready. Save other work and quit Codex App normally. Waiting up to 5 minutes; no process will be closed by this runner.');
  const waitUntil=Date.now()+300_000;
  while(true){const rows=await inventory(desktopExe);if(!rows.some(row=>normalized(row.path)===normalized(desktopExe)))break;if(Date.now()>waitUntil)fail('APP_NOT_CLOSED');await pause(1000);}
  monitor=new AbsenceMonitor(desktopExe);monitor.observe(await inventory(desktopExe),Date.now());
  deadline=setTimeout(()=>abort.abort(),600_000);
  sampling=(async()=>{while(!stopSampling){await pause(1000);if(stopSampling)break;try{monitor!.observe(await inventory(desktopExe),Date.now());}catch(error){monitor!.invalidate();observationError=(error as {code?:string}).code??'INVENTORY_UNAVAILABLE';abort.abort();break;}}})();
  console.log('App absence observed. Use native dialogs: open PAOS, pair manually, register ONLY the printed synthetic workspace, inspect offline Send. A second native dialog checks reuse. Close the tab/keep running, then browser Quit; or native Quit. Do not connect an account.');
  console.log(`Synthetic workspace: ${workspace}`);
  let second:Promise<Awaited<ReturnType<typeof runNativeLauncher>>>|undefined;
  const result=await runNativeLauncher({profileDirectory:profile,
   async readHealth(endpoint,signal){const health=await readLoopbackHealth(endpoint,signal);signals.health={...health};return health;},
   async showWindow(input,signal){
    if(!input.owner)fail('OWNER_EXPECTED');
    signals.nativeOwnerDialogInvoked=true;
    second=runNativeLauncher({profileDirectory:profile,async showWindow(reused,reuseSignal){
     if(reused.owner||reused.origin!==input.origin)fail('REUSE_MISMATCH');signals.nativeReuseDialogInvoked=true;
     await nativeWindow(reused,AbortSignal.any([abort.signal,...(reuseSignal?[reuseSignal]:[])]));return 'closed';
    }});
    second.catch(()=>abort.abort());
    const action=await nativeWindow(input,AbortSignal.any([abort.signal,...(signal?[signal]:[])]));
    signals.nativeOwnerDialogResult=action;
    if(action==='closed')while(await exists(lock)){if(abort.signal.aborted)return 'quit';await pause(250);}
    return abort.signal.aborted?'quit':action;
   }});
  signals.ownerLauncher=result;
  if(second){const reused=await second;signals.secondLauncher=reused;if(reused.status!=='opened'||reused.instance!=='existing')fail('REUSE_NOT_OBSERVED');}
  if(result.status!=='opened'||result.instance!=='started')fail('OWNER_NOT_STARTED');
  for(let count=0;count<80&&await exists(lock);count++)await pause(250);
  signals.reservationReleased=!await exists(lock);
  if(!signals.reservationReleased)fail('SHUTDOWN_UNCONFIRMED');
  signals.shutdownAcknowledgement='owner_reservation_released_after_service_stop';
  monitor.observe(await inventory(desktopExe),Date.now());
  if(observationError)fail(observationError);if(abort.signal.aborted)fail('JOURNEY_DEADLINE');
  // These answers remain owner statements, separate from process/health evidence.
  const terminal=createInterface({input:process.stdin,output:process.stdout});
  try {
   const answer=await terminal.question('After actual browser use, type ACCEPT only if pairing/project/session/offline Send, second-instance reuse and Quit behaved correctly. Otherwise type REJECT: ',{signal:AbortSignal.timeout(120_000)});
   receipt.ownerAttestations={scope:'manual_native_browser_launcher_journey',accepted:answer==='ACCEPT',recordedAt:new Date().toISOString()};
  } finally {terminal.close();}
  // Deliberately never label this full M1/SW-AC-01 provider acceptance.
  receipt.status='needs_user_acceptance';
 } catch(error){receipt.status='failed';receipt.errorCode=(error as {code?:string}).code??'STANDALONE_CHECK_FAILED';process.exitCode=1;}
 finally {
  if(deadline)clearTimeout(deadline);stopSampling=true;await sampling;receipt.appAbsence=monitor?.receipt()??null;
  if(observationError||monitor&&!monitor.receipt().valid){receipt.status='failed';receipt.errorCode=observationError??'ABSENCE_UNVERIFIED';process.exitCode=1;}
  const reserved=await exists(lock);signals.reservationRemaining=reserved;
  if(!reserved&&resolve(fixture,'..')===resolve(scratch)){await rm(fixture,{recursive:true,force:true});receipt.fixtureCleaned=true;}else receipt.fixtureCleaned=false;
  receipt.finishedAt=new Date().toISOString();await writeFile(receiptPath,JSON.stringify(receipt,null,2));console.log(`Receipt: ${receiptPath}`);
 }
}

if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
 main(process.argv.slice(2)).catch(error=>{console.error((error as {code?:string}).code??'STANDALONE_SETUP_FAILED');process.exitCode=1;});
}
