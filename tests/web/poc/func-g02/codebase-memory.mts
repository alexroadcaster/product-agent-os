import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
import {readFile,writeFile,mkdir,readdir} from 'node:fs/promises';
import {resolve,join,dirname,relative} from 'node:path';
import {pathToFileURL} from 'node:url';

const hash=(value:string|Uint8Array)=>createHash('sha256').update(value).digest('hex');
export function isolatedEnvironment(home:string,allowedRoot:string){
 return {SystemRoot:process.env.SystemRoot!,SystemDrive:process.env.SystemDrive??'C:',PATH:join(process.env.SystemRoot!,'System32'),
  USERPROFILE:home,HOME:home,APPDATA:join(home,'appdata'),LOCALAPPDATA:join(home,'local'),XDG_CONFIG_HOME:join(home,'config'),
  TEMP:join(home,'temp'),TMP:join(home,'temp'),CBM_CACHE_DIR:join(home,'cache'),CBM_RUNTIME_DIR:join(home,'runtime'),
  CBM_ALLOWED_ROOT:allowedRoot,CBM_WORKERS:'1',CBM_LOG_LEVEL:'warn',CBM_DIAGNOSTICS:'false'};
}
export async function runCommand(binary:string,args:string[],cwd:string,env:Record<string,string>,timeoutMs:number){
 const began=performance.now();let stdout='',stderr='',timedOut=false;
 return await new Promise<any>(resolveResult=>{
  const child=spawn(binary,args,{cwd,env,windowsHide:true,stdio:['ignore','pipe','pipe']});
  const timer=setTimeout(()=>{timedOut=true;child.kill();},timeoutMs);
  child.stdout.on('data',chunk=>{stdout+=chunk;if(stdout.length>1048576)child.kill();});
  child.stderr.on('data',chunk=>{stderr+=chunk;if(stderr.length>1048576)child.kill();});
  child.on('error',error=>{clearTimeout(timer);resolveResult({args,exitCode:null,error:String(error),stdout,stderr,timedOut,elapsedMs:performance.now()-began});});
  child.on('close',(code,signal)=>{clearTimeout(timer);resolveResult({args,exitCode:code,signal,stdout,stderr,timedOut,elapsedMs:performance.now()-began,pid:child.pid});});
 });
}
export async function manifest(directory:string):Promise<Record<string,string>>{
 const result:Record<string,string>={};
 async function walk(path:string){for(const entry of await readdir(path,{withFileTypes:true})){const target=join(path,entry.name);if(entry.isDirectory())await walk(target);else if(entry.isFile())result[relative(directory,target).replaceAll('\\','/')]=hash(await readFile(target));}}
 await walk(directory);return result;
}
export function classifyAdmission(result:{exitCode:number|null;error?:string;stderr:string}){
 if(result.error||result.exitCode===null)return 'executor_or_spawn_failure';
 if(result.exitCode!==0&&result.stderr.includes('could not load saved runtime settings'))return 'runtime_settings_admission_rejected';
 return result.exitCode===0?'admitted':'other_engine_error';
}
async function admissionProbe(){
 const root=resolve('.tmp/func-g02/f31'),fixture=join(root,'fixture'),project=join(fixture,'project-a'),home=join(root,'native-created-home');
 const binary=resolve('.tmp/func-g02/tools/codebase-binary/codebase-memory-mcp.exe');
 // This variant lets the verified tool create the cache itself; no inherited cache/database can explain the failure.
 const command=await runCommand(binary,['cli','--quiet','index_repository','--repo-path',project,'--format','json'],project,isolatedEnvironment(home,fixture),30000);
 const record={variant:'native_creates_fresh_cache',classification:classifyAdmission(command),command,cacheFiles:await manifest(join(home,'cache')).catch(()=>({})),runtimeFiles:await manifest(join(home,'runtime')).catch(()=>({})),finishedAt:new Date().toISOString()};
 await writeFile(join(root,'admission-rejection.json'),JSON.stringify(record,null,2)+'\n');console.log(JSON.stringify(record));
}
async function probe(){
 if(process.argv[2]!=='--native-poc')throw Error('EXPLICIT_NATIVE_POC_REQUIRED');
 const root=resolve('.tmp/func-g02/f31'),fixture=join(root,'fixture'),original=join(root,'original'),home=join(root,'home'),project=join(fixture,'project-a');
 const binary=resolve('.tmp/func-g02/tools/codebase-binary/codebase-memory-mcp.exe');
 const protocol=JSON.parse(await readFile('tests/fixtures/func_g02/protocol.json','utf8')),corpus=JSON.parse(await readFile(protocol.corpus,'utf8'));
 for(const directory of [project,original,home,...Object.values(isolatedEnvironment(home,fixture)).filter(v=>v.startsWith(home))])await mkdir(directory,{recursive:true});
 for(const [path,content] of Object.entries({...corpus.files,...corpus.excludedFiles}) as [string,string][]){const destination=join(original,path);await mkdir(dirname(destination),{recursive:true});await writeFile(destination,content);}
 for(const [path,content] of Object.entries(corpus.files) as [string,string][]){const destination=join(project,path);await mkdir(dirname(destination),{recursive:true});await writeFile(destination,content);}
 const before=await manifest(original),projection=await manifest(project),env=isolatedEnvironment(home,fixture);
 const commands=[];for(const args of [['--version'],['cli','--help'],['cli','index_repository','--help'],['cli','--quiet','list_projects','--format','json']])commands.push(await runCommand(binary,args,project,env,protocol.budgets.smallIndexTimeoutMs));
 const report={schemaVersion:'paos_cbm_poc_v1',taskId:'PAOS-FUNC-31',version:'0.12.1',commit:'a7158ac2f48ca646b4527341b76f930f2aeff87e',binarySha256:hash(await readFile(binary)),protocolSha256:hash(await readFile('tests/fixtures/func_g02/protocol.json')),corpusSha256:hash(await readFile(protocol.corpus)),startedScope:'isolated_cli_preflight',networkDuringMeasurement:false,providerCalls:false,realCredentials:false,globalConfigurationChanged:false,commands,sourcePreserved:JSON.stringify(before)===JSON.stringify(await manifest(original)),projectionPreserved:JSON.stringify(projection)===JSON.stringify(await manifest(project)),runtimePaths:{home,cache:env.CBM_CACHE_DIR,runtime:env.CBM_RUNTIME_DIR,allowedRoot:fixture},finishedAt:new Date().toISOString()};
 await writeFile(join(root,'preflight.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({report:join(root,'preflight.json'),commands:commands.map(r=>({args:r.args,exitCode:r.exitCode,error:r.error,stdout:r.stdout.slice(0,200),stderr:r.stderr.slice(0,700),elapsedMs:r.elapsedMs})),sourcePreserved:report.sourcePreserved}));
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){if(process.argv[2]==='--admission-probe')await admissionProbe();else await probe();}
