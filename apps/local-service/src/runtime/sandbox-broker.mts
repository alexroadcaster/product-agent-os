import {spawn} from 'node:child_process';
import {createHash,randomUUID} from 'node:crypto';
import {lstat,mkdir,mkdtemp,readFile,realpath,rm,writeFile} from 'node:fs/promises';
import {isAbsolute,join,relative,resolve,win32} from 'node:path';
import {createStdioRpc,type RuntimeRpc} from './codex/stdio-rpc.ts';
import {inspectConfiguredRuntime} from '../../../../packages/contracts/runtime/manifest.mts';
import {nativeProfileConfiguration} from './native-rpc.mts';

export type SandboxBrokerOptions=Readonly<{binaryPath:string;profileDirectory:string;workspaceRoot:string;mode:'discussion'|'planning'|'execution'}>;
export type SandboxBroker=Readonly<{
 metadata:Readonly<{nativeSandbox:true;scope:'paos_mediated_commands';workspaceRoot:string;mode:SandboxBrokerOptions['mode'];threadId:string;generation:string}>;
 execute:(options:Readonly<{operationId:string;argv:readonly string[];timeoutMs?:number}>)=>Promise<{exitCode:number;stdout:string;stderr:string}>;
 interrupt:(operationId:string)=>Promise<void>;
 close:()=>Promise<void>;
}>;
export type SandboxBrokerSpawnPlan=Readonly<{binaryPath:string;args:readonly string[];cwd:string;env:Record<string,string>}>;
export type SandboxBrokerDependencies=Readonly<{inspect?:typeof inspectConfiguredRuntime;spawnRpc?:(plan:SandboxBrokerSpawnPlan)=>Promise<RuntimeRpc>}>;
const fail=(code:string)=>Object.assign(new Error('The local sandbox broker is unavailable.'),{code});
const object=(value:unknown):Record<string,unknown>=>value!==null&&typeof value==='object'&&!Array.isArray(value)?value as Record<string,unknown>:{};
const identity=(path:string)=>process.platform==='win32'?resolve(path).toLowerCase():resolve(path);
const offlineProvider='paos_offline_broker';
/** The broker never issues a model request. A non-authenticated loopback provider also fails closed if a future caller errs. */
export const sandboxBrokerConfiguration=nativeProfileConfiguration.replace('model_provider = "openai"',`model_provider = "${offlineProvider}"\nmodel = "paos-offline-no-inference"\nchatgpt_base_url = "http://127.0.0.1:1/"\nopenai_base_url = "http://127.0.0.1:1/v1"`)+`
[model_providers.${offlineProvider}]
name = "PAOS Offline Command Broker"
base_url = "http://127.0.0.1:1/v1"
wire_api = "responses"
requires_openai_auth = false
`;
async function directory(path:string) {
 const info=await lstat(path);
 if(!info.isDirectory()||info.isSymbolicLink()||identity(await realpath(path))!==identity(path))throw fail('BROKER_PATH_INVALID');
 return info;
}
/** One immutable workspace/mode binding. command/exec is standalone, so threadId records policy qualification, not command membership.
 * Protocol: pinned Codex 0.167.0 CommandExecParams/CommandExecTerminateParams. All worker fields except argv/id/timeout are broker-owned.
 */
export async function createSandboxBroker(options:SandboxBrokerOptions,deps:SandboxBrokerDependencies={}):Promise<SandboxBroker> {
 if(!['discussion','planning','execution'].includes(options.mode)||![options.binaryPath,options.profileDirectory,options.workspaceRoot].every(isAbsolute))throw fail('BROKER_OPTIONS_INVALID');
 if(!deps.spawnRpc&&process.platform!=='win32')throw fail('BROKER_PLATFORM_UNSUPPORTED');
 const inspected=await(deps.inspect??inspectConfiguredRuntime)(options.profileDirectory);
 if(!inspected.qualified||inspected.binaryPath!==options.binaryPath||inspected.fingerprint?.version!=='0.167.0'||inspected.expected?.version!=='0.167.0'
  ||!inspected.fingerprint?.sha256||inspected.fingerprint.sha256!==inspected.expected.sha256)throw fail('BROKER_RUNTIME_UNQUALIFIED');
 const workspaceRoot=resolve(options.workspaceRoot),profileDirectory=resolve(options.profileDirectory);
 const profileRelative=relative(workspaceRoot,profileDirectory);
 if(!isAbsolute(profileRelative)&&profileRelative!=='..'&&!profileRelative.startsWith('..'+(process.platform==='win32'?'\\':'/')))throw fail('BROKER_PROFILE_IN_WORKSPACE');
 const rootIdentity=await directory(workspaceRoot);await directory(profileDirectory);
 const systemRoot=process.env.SystemRoot;
 if(!systemRoot||!win32.isAbsolute(systemRoot))throw fail('BROKER_SYSTEMROOT_UNAVAILABLE');
 const home=await mkdtemp(join(profileDirectory,'sandbox-broker-'));const homeIdentity=await directory(home);
 const system32=join(systemRoot,'System32'),user=join(home,'user');
 // inherit=none also applies to command/exec. MXC still requires SYSTEMROOT; supply only broker-owned values.
 const commandEnvironment={SystemRoot:systemRoot,WINDIR:systemRoot,ComSpec:join(system32,'cmd.exe'),SystemDrive:win32.parse(systemRoot).root.replace(/[\\/]+$/,''),PATH:system32,
  USERPROFILE:user,HOME:user,APPDATA:join(user,'AppData','Roaming'),LOCALAPPDATA:join(user,'AppData','Local'),TEMP:join(home,'temp'),TMP:join(home,'temp')};
 const profile=options.mode==='execution'?'paos_execution':'paos_readonly';
 let pinnedConfiguration=sandboxBrokerConfiguration;
 let rpc:RuntimeRpc|undefined;let unsubscribe:()=>void=()=>{};let closed=false;let closing:Promise<void>|undefined;
 type CommandResult={exitCode:number;stdout:string;stderr:string};
 type Operation={id:string;digest:string;processId:string;started:boolean;cancelled:boolean;settled:boolean;promise:Promise<CommandResult>};
 const operations=new Map<string,Operation>();let active:Operation|undefined;
 async function cleanup() {
  const current=await directory(home);
  if(current.dev!==homeIdentity.dev||current.ino!==homeIdentity.ino)throw fail('BROKER_HOME_REPLACED');
  await rm(home,{recursive:true,force:true});
 }
 async function assertRoot() {
  const current=await directory(workspaceRoot);
  if(current.dev!==rootIdentity.dev||current.ino!==rootIdentity.ino)throw fail('BROKER_ROOT_REPLACED');
 }
 async function validateConfiguration(acceptNativeTrust=false) {
  await assertRoot();
  const configFile=join(home,'config.toml'),file=await lstat(configFile);
  if(!file.isFile()||file.isSymbolicLink()||file.nlink!==1)throw fail('BROKER_CONFIG_DRIFT');
  const bytes=await readFile(configFile,'utf8');
  if(bytes!==pinnedConfiguration) {
   // Codex 0.167.0 may append its repository trust decision on an execution thread/start.
   // Accept only this exact table in the isolated home; every effective setting and project layer is still checked below.
   if(!acceptNativeTrust||pinnedConfiguration!==sandboxBrokerConfiguration)throw fail('BROKER_CONFIG_DRIFT');
   const added=bytes.startsWith(sandboxBrokerConfiguration)?bytes.slice(sandboxBrokerConfiguration.length):'';
   const trusted=/^\n?\[projects\.'([^'\r\n]+)'\]\r?\ntrust_level = "trusted"\r?\n?$/.exec(added);
   if(!trusted||!isAbsolute(trusted[1]))throw fail('BROKER_CONFIG_DRIFT');
   const fromTrusted=relative(trusted[1],workspaceRoot);
   if(isAbsolute(fromTrusted)||fromTrusted==='..'||fromTrusted.startsWith('..'+(process.platform==='win32'?'\\':'/'))||identity(await realpath(trusted[1]))!==identity(trusted[1]))throw fail('BROKER_CONFIG_DRIFT');
  }
  const reply=await rpc!.request('config/read',{cwd:workspaceRoot,includeLayers:true});const config=object(reply.config);
  const layers=Array.isArray(reply.layers)?reply.layers.map(object):[];const user=layers.filter(row=>object(row.name).type==='user');
  const provider=object(object(config.model_providers)[offlineProvider]);const permissions=object(config.permissions);
  const readonly=object(permissions.paos_readonly),execution=object(permissions.paos_execution);
  // config/read materializes the schema's optional scan depth as null; it is not a filesystem grant.
  const executionFilesystem=Object.fromEntries(Object.entries(object(execution.filesystem)).filter(([key,value])=>!(key==='glob_scan_max_depth'&&value===null)));
  const valid={
   provider:config.model_provider===offlineProvider&&config.model==='paos-offline-no-inference'&&provider.base_url==='http://127.0.0.1:1/v1'&&provider.requires_openai_auth===false
    &&['env_key','experimental_bearer_token','auth','gateway_oauth','credential_file','aws','http_headers','env_http_headers','model_catalog_url'].every(key=>provider[key]==null),
   auth:config.cli_auth_credentials_store==='ephemeral'&&config.forced_login_method==='api',
   sandbox:object(config.windows).sandbox==='mxc'&&config.approval_policy==='never'&&config.default_permissions==='paos_readonly',
   tools:config.web_search==='disabled'&&Object.keys(object(config.mcp_servers)).length===0&&object(config.features).apps===false&&object(config.features).plugins===false&&object(config.features).computer_use===false,
   environment:object(config.analytics).enabled===false&&object(config.shell_environment_policy).inherit==='none'&&Object.keys(object(object(config.shell_environment_policy).set)).length===0&&config.check_for_update_on_startup===false,
   projectMarkers:Array.isArray(config.project_root_markers)&&config.project_root_markers.length===0,
   profileBases:readonly.extends===':read-only'&&object(readonly.network).enabled===false&&execution.extends===':read-only'&&object(execution.network).enabled===false,
   profileScope:Object.keys(permissions).sort().join(',')==='paos_execution,paos_readonly'&&Object.keys(object(readonly.filesystem)).length===0&&readonly.workspace_roots==null&&execution.workspace_roots==null,
   filesystem:JSON.stringify(executionFilesystem)===JSON.stringify({':workspace_roots':{'.':'write'}}),
   provenance:!layers.some(row=>object(row.name).type==='project')&&user.length===1&&typeof object(user[0].name).file==='string'&&identity(object(user[0].name).file as string)===identity(configFile),
  };
  const failedChecks=Object.entries(valid).filter(([,ok])=>!ok).map(([name])=>name);
  if(failedChecks.length)throw Object.assign(fail('BROKER_CONFIG_DRIFT'),{failedChecks});
  if(acceptNativeTrust)pinnedConfiguration=bytes;
 }
 async function interrupt(operationId:string) {
  const operation=operations.get(operationId);if(!operation||operation.settled)return;
  operation.cancelled=true;
  if(operation.started) {
   try {await rpc!.request('command/exec/terminate',{processId:operation.processId});}
   catch {if(!operation.settled)throw fail('BROKER_STOP_UNVERIFIED');}
  }
  await operation.promise.catch(()=>{});
 }
 function close():Promise<void> {
  if(closing)return closing;closed=true;
  closing=(async()=>{
   let stopError:unknown;
   try {if(active)await interrupt(active.id);}catch(error){stopError=error;}
   await rpc?.close();unsubscribe();await cleanup();
   if(stopError)throw stopError;
  })();return closing;
 }
 try {
  for(const path of [user,join(user,'AppData'),join(user,'AppData','Roaming'),join(user,'AppData','Local'),join(home,'temp')])await mkdir(path,{mode:0o700});
  await writeFile(join(home,'config.toml'),sandboxBrokerConfiguration,{flag:'wx',mode:0o600});
  const plan:SandboxBrokerSpawnPlan={binaryPath:options.binaryPath,args:['app-server','--listen','stdio://'],cwd:workspaceRoot,
   env:{...commandEnvironment,CODEX_HOME:home}};
  rpc=deps.spawnRpc?await deps.spawnRpc(plan):createStdioRpc(spawn(plan.binaryPath,[...plan.args],{cwd:plan.cwd,env:plan.env,windowsHide:true,shell:false,stdio:['pipe','pipe','pipe']}),{timeoutMs:35_000});
  unsubscribe=rpc.subscribe(message=>{if((typeof message.id==='string'||typeof message.id==='number')&&typeof message.method==='string')rpc!.respondError(message.id,-32601);});
  const initialized=await rpc.request('initialize',{clientInfo:{name:'paos_offline_command_broker',version:'1'},capabilities:{experimentalApi:true}});
  if(typeof initialized.codexHome!=='string'||identity(initialized.codexHome)!==identity(home))throw fail('BROKER_HOME_MISMATCH');
  rpc.notify('initialized');await validateConfiguration();await rpc.request('configRequirements/read',null);
  if((await rpc.request('windowsSandbox/readiness',null)).status!=='ready')throw fail('BROKER_SANDBOX_UNAVAILABLE');
  const profiles=await rpc.request('permissionProfile/list',{cwd:workspaceRoot});
  if(profiles.nextCursor!=null||!Array.isArray(profiles.data)||!profiles.data.some(row=>object(row).id===profile&&object(row).allowed===true))throw fail('BROKER_PROFILE_UNAVAILABLE');
  const started=await rpc.request('thread/start',{cwd:workspaceRoot,runtimeWorkspaceRoots:[workspaceRoot],ephemeral:true,permissions:profile,approvalPolicy:'never',allowProviderModelFallback:false});
  const policy=object(started.sandbox),threadId=object(started.thread).id,roots=started.runtimeWorkspaceRoots;
  if(typeof threadId!=='string'||!threadId||typeof started.cwd!=='string'||identity(started.cwd)!==identity(workspaceRoot)||!Array.isArray(roots)||roots.length!==1||typeof roots[0]!=='string'||identity(roots[0])!==identity(workspaceRoot)
   ||started.approvalPolicy!=='never'||started.modelProvider!==offlineProvider||object(started.activePermissionProfile).id!==profile||policy.networkAccess!==false
   ||(options.mode==='execution'?(policy.type!=='workspaceWrite'||!Array.isArray(policy.writableRoots)||policy.writableRoots.length!==0||policy.excludeSlashTmp!==true||policy.excludeTmpdirEnvVar!==true):policy.type!=='readOnly'))throw fail('BROKER_POLICY_MISMATCH');
  // Only this immediate native startup window may add trust metadata. All later operations require these exact bytes.
  await validateConfiguration(true);
  const metadata=Object.freeze({nativeSandbox:true as const,scope:'paos_mediated_commands' as const,workspaceRoot,mode:options.mode,threadId,generation:rpc.generation});
  return {metadata,interrupt,close,
   execute(command) {
    const timeoutMs=command.timeoutMs??30_000;
    if(typeof command.operationId!=='string'||!command.operationId||command.operationId.length>128||!Array.isArray(command.argv)||command.argv.length===0||!command.argv[0]||command.argv.some(arg=>typeof arg!=='string'||arg.includes('\0'))
     ||Buffer.byteLength(command.argv.join('\0'))>32768||!Number.isInteger(timeoutMs)||timeoutMs<1||timeoutMs>30_000)return Promise.reject(fail('BROKER_COMMAND_INVALID'));
    const argv=[...command.argv];
    const digest=createHash('sha256').update(JSON.stringify({argv,timeoutMs})).digest('hex');const previous=operations.get(command.operationId);
    if(previous)return previous.digest===digest?previous.promise:Promise.reject(fail('BROKER_OPERATION_CONFLICT'));
    if(closed)return Promise.reject(fail('BROKER_CLOSED'));if(active)return Promise.reject(fail('BROKER_BUSY'));if(operations.size>=256)return Promise.reject(fail('BROKER_OPERATION_LIMIT'));
    const operation:Operation={id:command.operationId,digest,processId:randomUUID(),started:false,cancelled:false,settled:false,promise:undefined as unknown as Promise<CommandResult>};active=operation;
    operation.promise=(async()=>{
     await validateConfiguration();if(operation.cancelled||closed)throw fail('BROKER_INTERRUPTED');operation.started=true;
     const response=await rpc!.request('command/exec',{command:argv,cwd:workspaceRoot,permissionProfile:profile,timeoutMs,outputBytesCap:16384,processId:operation.processId,env:commandEnvironment});
     if(!Number.isInteger(response.exitCode)||typeof response.stdout!=='string'||typeof response.stderr!=='string')throw fail('BROKER_OUTCOME_UNKNOWN');
     if(Buffer.byteLength(response.stdout)>16384||Buffer.byteLength(response.stderr)>16384)throw fail('BROKER_OUTPUT_LIMIT');
     return {exitCode:response.exitCode as number,stdout:response.stdout,stderr:response.stderr};
    })().finally(()=>{operation.settled=true;if(active===operation)active=undefined;});
    operations.set(command.operationId,operation);return operation.promise;
   }};
 } catch(error) {await close();throw error;}
}
