import {spawn} from 'node:child_process';
import {mkdir,lstat,readFile,writeFile,realpath} from 'node:fs/promises';
import {join,isAbsolute,resolve,win32} from 'node:path';
import {inspectConfiguredRuntime} from '../../../../packages/contracts/runtime/manifest.mts';
import {createStdioRpc,type RuntimeRpc} from './codex/stdio-rpc.ts';

const blocked=(code:string)=>Object.assign(new Error('The qualified native runtime is unavailable.'),{code});
const object=(value:unknown)=>value!==null&&typeof value==='object'&&!Array.isArray(value)?value as Record<string,unknown>:{};
const pathIdentity=(value:string)=>process.platform==='win32'?resolve(value).replaceAll('/','\\').toLowerCase():resolve(value);
// Config semantics: https://learn.chatgpt.com/docs/config-file/config-reference
// Native named-profile baseline: .tmp/paos-m1/windows-boundary.py (qualification evidence, not a runtime fallback).
export const nativeProfileConfiguration=`model_provider = "openai"
cli_auth_credentials_store = "ephemeral"
forced_login_method = "api"
default_permissions = "paos_readonly"
approval_policy = "never"
check_for_update_on_startup = false
project_root_markers = []
web_search = "disabled"
mcp_servers = {}
[analytics]
enabled = false
[features]
apps = false
plugins = false
computer_use = false
[computer_use]
default_app_access = "deny"
[shell_environment_policy]
inherit = "none"
[windows]
sandbox = "mxc"
[permissions.paos_readonly]
extends = ":read-only"
[permissions.paos_readonly.network]
enabled = false
[permissions.paos_execution]
extends = ":read-only"
[permissions.paos_execution.filesystem.":workspace_roots"]
"." = "write"
[permissions.paos_execution.network]
enabled = false
`;

type SpawnPlan=Readonly<{binaryPath:string;args:readonly string[];cwd:string;env:Record<string,string|undefined>}>;
type NativeRpcDependencies=Readonly<{
 inspect?:typeof inspectConfiguredRuntime;
 prepareHome?:(profile:string)=>Promise<string>;
 spawnRpc?:(plan:SpawnPlan)=>Promise<RuntimeRpc>;
}>;
async function prepareHome(profile:string) {
 const home=join(profile,'codex-runtime');await mkdir(home,{recursive:true,mode:0o700});
 if((await lstat(home)).isSymbolicLink()||pathIdentity(await realpath(home))!==pathIdentity(home))throw blocked('RUNTIME_HOME_INVALID');
 // MXC requires SystemRoot and LOCALAPPDATA. Keep every per-user/temp location inside the isolated profile.
 // https://learn.microsoft.com/en-us/windows/apps/develop/mxc/quickstart
 for(const directory of [join(home,'user'),join(home,'user','AppData'),join(home,'user','AppData','Roaming'),join(home,'user','AppData','Local'),join(home,'temp')]) {
  try {await mkdir(directory,{mode:0o700});}catch(error){if((error as {code?:string}).code!=='EEXIST')throw error;}
  const info=await lstat(directory);
  if(!info.isDirectory()||info.isSymbolicLink()||pathIdentity(await realpath(directory))!==pathIdentity(directory))throw blocked('RUNTIME_HOME_INVALID');
 }
 for(const name of ['auth.json','.credentials.json']) {
  try {await lstat(join(home,name));throw blocked('INHERITED_AUTH_FORBIDDEN');}
  catch(error){if((error as {code?:string}).code!=='ENOENT')throw error;}
 }
 const config=join(home,'config.toml');
 try {
  const stat=await lstat(config);
  if(!stat.isFile()||stat.isSymbolicLink()||stat.nlink!==1||await readFile(config,'utf8')!==nativeProfileConfiguration)throw blocked('RUNTIME_CONFIG_DRIFT');
 } catch(error) {
  if((error as {code?:string}).code!=='ENOENT')throw error;
  await writeFile(config,nativeProfileConfiguration,{flag:'wx',mode:0o600});
 }
 return home;
}

/** Only an explicit credential connect calls this factory. No install/setup/fallback or inherited process environment. */
export async function createNativeRpc(options:Readonly<{profileDirectory:string;binaryPath:string}>,deps:NativeRpcDependencies={}):Promise<RuntimeRpc> {
 const inspection=await(deps.inspect??inspectConfiguredRuntime)(options.profileDirectory);
 if(!inspection.qualified||inspection.binaryPath!==options.binaryPath)throw blocked('RUNTIME_UNQUALIFIED');
 if(!isAbsolute(options.profileDirectory)||!isAbsolute(options.binaryPath)||(!deps.spawnRpc&&process.platform!=='win32'))throw blocked('RUNTIME_PLATFORM_UNSUPPORTED');
 const home=await(deps.prepareHome??prepareHome)(options.profileDirectory);
 const systemRoot=process.env.SystemRoot;
 if(!systemRoot||!win32.isAbsolute(systemRoot))throw blocked('RUNTIME_SYSTEMROOT_UNAVAILABLE');
 const system32=join(systemRoot,'System32');const user=join(home,'user');
 const plan:SpawnPlan={binaryPath:options.binaryPath,args:['app-server','--listen','stdio://'],cwd:home,
  env:{SystemRoot:systemRoot,WINDIR:systemRoot,ComSpec:join(system32,'cmd.exe'),SystemDrive:win32.parse(systemRoot).root.replace(/[\\/]+$/,''),
   PATH:system32,CODEX_HOME:home,USERPROFILE:user,HOME:user,APPDATA:join(user,'AppData','Roaming'),
   LOCALAPPDATA:join(user,'AppData','Local'),TEMP:join(home,'temp'),TMP:join(home,'temp')}};
 const rpc=deps.spawnRpc?await deps.spawnRpc(plan):createStdioRpc(spawn(plan.binaryPath,[...plan.args],{
  cwd:plan.cwd,env:plan.env,windowsHide:true,shell:false,stdio:['pipe','pipe','pipe']}));
 let initialized=false;let notified=false;
 async function validateConfiguration(cwd:string) {
  const result=await rpc.request('config/read',{cwd,includeLayers:true});const config=object(result.config);
  const layers=Array.isArray(result.layers)?result.layers.map(object):[];
  const user=layers.filter((layer)=>object(layer.name).type==='user');
  if(config.cli_auth_credentials_store!=='ephemeral'||config.forced_login_method!=='api'||object(config.windows).sandbox!=='mxc'
   ||config.model_provider!=='openai'||config.web_search!=='disabled'||Object.keys(object(config.mcp_servers)).length
   ||object(config.features).apps!==false||object(config.features).plugins!==false||object(config.features).computer_use!==false
   ||layers.some((layer)=>object(layer.name).type==='project')||user.length!==1
   ||typeof object(user[0].name).file!=='string'
   ||pathIdentity(object(user[0].name).file as string)!==pathIdentity(join(home,'config.toml')))throw blocked('RUNTIME_CONFIG_DRIFT');
 }
 return {...rpc,
  notify(method){if(!notified){rpc.notify(method);notified=true;}},
  async request(method,params) {
   try {
    if(method==='initialize') {
     if(initialized)throw blocked('RUNTIME_ALREADY_INITIALIZED');
     const result=await rpc.request(method,params);
     if(typeof result.codexHome!=='string'||pathIdentity(result.codexHome)!==pathIdentity(home))throw blocked('RUNTIME_HOME_MISMATCH');
     rpc.notify('initialized');notified=true;
     await validateConfiguration(home);
     const readiness=await rpc.request('windowsSandbox/readiness',null);
     if(readiness.status!=='ready')throw blocked('RUNTIME_SANDBOX_UNAVAILABLE');
     const account=await rpc.request('account/read',{refreshToken:false});
     if(account.account!==null)throw blocked('INHERITED_AUTH_FORBIDDEN');
     initialized=true;return result;
    }
    if(!initialized)throw blocked('RUNTIME_NOT_INITIALIZED');
    if(method==='thread/start'||method==='turn/start') {
     const cwd=object(params).cwd;if(typeof cwd!=='string')throw blocked('RUNTIME_ROOT_REQUIRED');
     await validateConfiguration(cwd);
    }
    return await rpc.request(method,params);
   } catch(error) {await rpc.close();throw error;}
  }};
}
