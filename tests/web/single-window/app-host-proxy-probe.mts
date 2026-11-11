import {spawn} from 'node:child_process';
import {isAbsolute,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createProxyWebSocket} from '../../../apps/local-service/src/runtime/proxy-websocket.mts';
type Receipt={transport:'official_app_server_proxy';status:string;providerRequests:0;authReads:0;threadContentReads:0;loadedThreadCount:number|null;expectedThreadLoaded:boolean|null;serverVersion:string|null;proxyExitConfirmed:boolean;errorCategory?:string};
const uuid=/^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i;
/** Exactly two read-only requests. Presence on a server is evidence, never a cryptographic Desktop identity claim. */
export function createReadOnlyProbeSession(send:(value:unknown)=>void,done:(value:{loadedThreadCount:number;expectedThreadLoaded:boolean|null;serverVersion:string|null})=>void,expectedThread?:string){
 let stage=0,version:string|null=null;
 const fail=():never=>{throw new Error('PROXY_RPC_INVALID');};
 return {ready(){if(stage!==0)fail();stage=1;send({id:1,method:'initialize',params:{clientInfo:{name:'paos-readonly-qualification',version:'m1'},capabilities:{experimentalApi:true}}});},
  message(value:unknown){
   if(!value||typeof value!=='object'||Array.isArray(value))fail();const row=value as Record<string,any>;
   if(!Object.hasOwn(row,'id')){if(typeof row.method!=='string')fail();return;}
   if(row.method||row.error||!row.result||typeof row.result!=='object'||Array.isArray(row.result))fail();
   if(stage===1&&row.id===1){const observed=row.result.userAgent??row.result.version;version=typeof observed==='string'?observed.match(/\b\d{1,5}\.\d{1,5}\.\d{1,5}\b/)?.[0]??null:null;stage=2;
    send({method:'initialized',params:{}});send({id:2,method:'thread/loaded/list',params:{}});return;}
   if(stage===2&&row.id===2){const ids=row.result.data;if(!Array.isArray(ids)||ids.length>10000||ids.some(id=>typeof id!=='string'||!uuid.test(id))||new Set(ids).size!==ids.length||row.result.nextCursor!=null)fail();stage=3;done({loadedThreadCount:ids.length,expectedThreadLoaded:expectedThread?ids.includes(expectedThread):null,serverVersion:version});return;}
   fail();
  }};
}
export async function probeAppHost(options:{binary:string;socket?:string;expectedThread?:string;timeoutMs?:number}):Promise<Receipt>{
 if(!isAbsolute(options.binary)||options.socket!==undefined&&!isAbsolute(options.socket)||options.expectedThread!==undefined&&!uuid.test(options.expectedThread))throw new Error('PROXY_ARGUMENT_INVALID');
 const timeoutMs=options.timeoutMs??5000;if(!Number.isInteger(timeoutMs)||timeoutMs<100||timeoutMs>30000)throw new Error('PROXY_ARGUMENT_INVALID');
 const receipt:Receipt={transport:'official_app_server_proxy',status:'pending',providerRequests:0,authReads:0,threadContentReads:0,loadedThreadCount:null,expectedThreadLoaded:null,serverVersion:null,proxyExitConfirmed:false};
 return new Promise(resolveResult=>{
  const child=spawn(options.binary,['app-server','proxy',...(options.socket?['--sock',options.socket]:[])],{shell:false,windowsHide:true,stdio:['pipe','pipe','pipe']});
  let finished=false,resolved=false,stderrTail='',stderrCategory:string|undefined;let killTimer:ReturnType<typeof setTimeout>|undefined,exitTimer:ReturnType<typeof setTimeout>|undefined;
  function resolveOnce(){if(resolved)return;resolved=true;clearTimeout(deadline);clearTimeout(killTimer);clearTimeout(exitTimer);resolveResult(receipt);}
  function finish(status:string,errorCategory?:string){if(finished)return;finished=true;receipt.status=status;if(errorCategory)receipt.errorCategory=errorCategory;clearTimeout(deadline);
   try{ws.close();}catch{}child.stdin.end();killTimer=setTimeout(()=>{child.kill();exitTimer=setTimeout(()=>{receipt.status='proxy_stop_unconfirmed';resolveOnce();},1000);},500);
  }
  const protocol=createReadOnlyProbeSession(v=>ws.send(v),observed=>{Object.assign(receipt,observed);finish('qualified_readonly_transport');},options.expectedThread);
  const ws=createProxyWebSocket({write:bytes=>{child.stdin.write(bytes);},ready:protocol.ready,message:protocol.message,closed:()=>finish('transport_closed')});
  const deadline=setTimeout(()=>finish('bounded_timeout'),timeoutMs);
  child.stdout.on('data',(bytes:Buffer)=>{if(finished)return;try{ws.feed(bytes);}catch(error){finish('protocol_rejected',error instanceof Error&&/^PROXY_[A-Z_]+$/.test(error.message)?error.message:'PROXY_PROTOCOL_ERROR');}});
  child.stderr.on('data',(bytes:Buffer)=>{stderrTail=(stderrTail+bytes.toString('utf8')).slice(-256);if(stderrTail.includes('10050'))stderrCategory='WSA_10050';else if(stderrTail.includes('10061')&&!stderrCategory)stderrCategory='WSA_10061';});
  child.stdin.on('error',()=>finish('transport_unavailable',stderrCategory??'PROXY_WRITE_FAILED'));
  child.on('error',()=>finish('transport_unavailable','PROXY_START_FAILED'));
  child.on('close',()=>{receipt.proxyExitConfirmed=true;if(!finished){finished=true;receipt.status='transport_unavailable';receipt.errorCategory=stderrCategory??'PROXY_EOF';}resolveOnce();});
  try{ws.start();}catch{finish('transport_unavailable','PROXY_WRITE_FAILED');}
 });
}
export function parseProbeArguments(args:string[]){
 if(args[0]!=='--read-only-proxy'||args.length%2!==1)throw new Error('PROXY_CLI_USAGE');const pairs=new Map<string,string>();
 for(let i=1;i<args.length;i+=2){if(!['--binary','--socket','--expected-thread'].includes(args[i])||pairs.has(args[i])||!args[i+1])throw new Error('PROXY_CLI_USAGE');pairs.set(args[i],args[i+1]);}
 const binary=pairs.get('--binary');if(!binary)throw new Error('PROXY_CLI_USAGE');return {binary,socket:pairs.get('--socket'),expectedThread:pairs.get('--expected-thread')};
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 Promise.resolve().then(()=>probeAppHost(parseProbeArguments(process.argv.slice(2)))).then(receipt=>{console.log(JSON.stringify(receipt));process.exitCode=receipt.status==='qualified_readonly_transport'&&receipt.proxyExitConfirmed?0:1;}).catch(()=>{console.error('PROXY_PROBE_FAILED');process.exitCode=1;});
}
