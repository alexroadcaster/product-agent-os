import {isAbsolute} from 'node:path';
import {pathToFileURL} from 'node:url';

// Disposable acceptance runner: the installed production launcher owns the actual service child.
// Pairing material is IPC-only and never written to stdout, URLs or evidence files.
const [modulePath,home]=process.argv.slice(2);
if(!isAbsolute(modulePath??'')||!isAbsolute(home??'')||!process.send)throw Error('FIXTURE_IPC_ARGUMENTS_REQUIRED');
let resolveAction:((action:'quit')=>void)|undefined,timedOut=false;
const quit=()=>resolveAction?.('quit');
process.on('message',(message:any)=>{if(message?.type==='quit')quit();});
process.on('disconnect',quit);
const timer=setTimeout(()=>{timedOut=true;quit();},120000);
try{
 const {startManaged}=await import(pathToFileURL(modulePath).href);
 const result=await startManaged(home,async(input:any)=>{
  if(input.owner!==true||typeof input.pairingCode!=='string'||!/^http:\/\/127\.0\.0\.1:\d+$/.test(input.origin))throw Error('OWNED_PRODUCTION_WINDOW_REQUIRED');
  const action=new Promise<'quit'>(resolve=>{resolveAction=resolve;});
  process.send!({type:'window',origin:input.origin,pairingCode:input.pairingCode,owner:true,runtime:input.runtime});
  return action;
 });
 process.send!({type:'result',result,timedOut});
 if(timedOut||result.status!=='opened')process.exitCode=1;
}catch(error){
 process.send?.({type:'failure',code:typeof(error as any)?.code==='string'?(error as any).code:(error as Error).message});process.exitCode=1;
}finally{clearTimeout(timer);if(process.connected)process.disconnect();}
