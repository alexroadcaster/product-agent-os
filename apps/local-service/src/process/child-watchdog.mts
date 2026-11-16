import {Worker} from 'node:worker_threads';
/** Trusted owned-child watchdog. Ready is awaited before native parsing starts.
 * It probes the parent with signal0 and can terminate only its own process.
 * JS heap limits do not bound native parser/SQLite RSS. */
export async function startChildWatchdog(milliseconds:number,parentPid=process.ppid):Promise<Worker>{
 if(!Number.isSafeInteger(milliseconds)||milliseconds<1||milliseconds>60000||!Number.isSafeInteger(parentPid)||parentPid<1)throw Object.assign(Error('CHILD_WATCHDOG_INPUT_INVALID'),{code:'CHILD_WATCHDOG_INPUT_INVALID'});
 const worker=new Worker(`const {workerData,parentPort}=require('node:worker_threads');const self=process.pid;setTimeout(()=>process.kill(self,'SIGKILL'),workerData.milliseconds);setInterval(()=>{try{process.kill(workerData.parentPid,0);}catch{process.kill(self,'SIGKILL');}},50);parentPort.postMessage('ready');`,{eval:true,workerData:{parentPid,milliseconds},resourceLimits:{maxOldGenerationSizeMb:16}});
 try{await new Promise<void>((resolve,reject)=>{worker.once('message',()=>resolve());worker.once('error',reject);worker.once('exit',()=>reject(Object.assign(Error('CHILD_WATCHDOG_UNAVAILABLE'),{code:'CHILD_WATCHDOG_UNAVAILABLE'})));});return worker;}catch(error){await worker.terminate();throw error;}
}
