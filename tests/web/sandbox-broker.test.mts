import assert from 'node:assert/strict';
import {test,type TestContext} from 'node:test';
import {mkdtemp,mkdir,rm,readFile,appendFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createSandboxBroker,type SandboxBrokerOptions,type SandboxBrokerSpawnPlan} from '../../apps/local-service/src/runtime/sandbox-broker.mts';
import type {RuntimeRpc,RpcMessage} from '../../apps/local-service/src/runtime/codex/stdio-rpc.ts';

async function fixture(t:TestContext,overrides:Record<string,unknown>={}) {
 const root=await mkdtemp(join(tmpdir(),'paos-broker-'));t.after(()=>rm(root,{recursive:true,force:true}));
 const profileDirectory=join(root,'profile'),workspaceRoot=join(root,'workspace');await mkdir(profileDirectory);await mkdir(workspaceRoot);
 const options:SandboxBrokerOptions={binaryPath:process.execPath,profileDirectory,workspaceRoot,mode:'execution'};
 const calls:{method:string;params:any}[]=[];let closed=false;let plan:SandboxBrokerSpawnPlan|undefined;let release:((value:RpcMessage)=>void)|undefined;
 const inspect=async()=>({qualified:true,reasons:[],binaryPath:options.binaryPath,fingerprint:{version:'0.167.0',sha256:'a'.repeat(64)},expected:{version:'0.167.0',sha256:'a'.repeat(64)}});
 const spawnRpc=async(input:SandboxBrokerSpawnPlan):Promise<RuntimeRpc>=>{
  plan=input;const home=input.env.CODEX_HOME;
  return {generation:'synthetic-generation',notify(){},respond(){},respondError(){},subscribe(){return()=>{};},onClosed(){return()=>{};},snapshot(){return {generation:'synthetic-generation',status:closed?'closed':'open',pending:0,stderrBytes:0};},close:async()=>{closed=true;},
   async request(method,params:any){
    calls.push({method,params});
    if(method==='initialize')return {codexHome:home};
    if(method==='config/read')return {config:{model_provider:'paos_offline_broker',model:'paos-offline-no-inference',cli_auth_credentials_store:'ephemeral',forced_login_method:'api',approval_policy:'never',default_permissions:'paos_readonly',check_for_update_on_startup:false,project_root_markers:[],web_search:'disabled',mcp_servers:{},windows:{sandbox:'mxc'},features:{apps:false,plugins:false,computer_use:false},analytics:{enabled:false},shell_environment_policy:{inherit:'none'},model_providers:{paos_offline_broker:{base_url:'http://127.0.0.1:1/v1',requires_openai_auth:false}},permissions:{paos_readonly:{extends:':read-only',network:{enabled:false}},paos_execution:{extends:':read-only',filesystem:{':workspace_roots':{'.':'write'}},network:{enabled:false}}}},layers:[{name:{type:'user',file:join(home,'config.toml')}},...(overrides.projectLayer?[{name:{type:'project'}}]:[])]};
    if(method==='windowsSandbox/readiness')return {status:overrides.readiness??'ready'};
    if(method==='configRequirements/read')return {requirements:null};
    if(method==='permissionProfile/list')return {data:[{id:'paos_readonly',allowed:true},{id:'paos_execution',allowed:true}],nextCursor:null};
    if(method==='thread/start'){
     if(overrides.nativeTrust)await appendFile(join(home,'config.toml'),`\n[projects.'${workspaceRoot}']\ntrust_level = "trusted"\n`);
     return {thread:{id:'synthetic-thread'},cwd:workspaceRoot,runtimeWorkspaceRoots:[workspaceRoot],approvalPolicy:'never',modelProvider:'paos_offline_broker',activePermissionProfile:{id:params.permissions},sandbox:params.permissions==='paos_execution'?{type:'workspaceWrite',networkAccess:false,writableRoots:[],excludeSlashTmp:true,excludeTmpdirEnvVar:true}:{type:'readOnly',networkAccess:false},...overrides.thread};
    }
    if(method==='command/exec') {if(overrides.rejectCommand)throw new Error('synthetic unknown outcome');if(overrides.hold)return new Promise(resolve=>{release=resolve;});return {exitCode:0,stdout:overrides.largeOutput?'x'.repeat(16385):'synthetic',stderr:''};}
    if(method==='command/exec/terminate'){release?.({exitCode:1,stdout:'stopped',stderr:''});return {};}
    throw new Error('Unexpected method '+method);
   }};
 };
 return {options,calls,inspect,spawnRpc,get closed(){return closed;},get plan(){return plan;}};
}

test('unqualified runtime fails before any child launch',async(t)=>{
 const f=await fixture(t);await assert.rejects(createSandboxBroker(f.options,{inspect:async()=>({qualified:false,reasons:['mismatch'],fingerprint:null,expected:null}),spawnRpc:f.spawnRpc}),{code:'BROKER_RUNTIME_UNQUALIFIED'});assert.equal(f.plan,undefined);
});
test('broker profile cannot be inside the bound workspace in any mode',async(t)=>{
 const f=await fixture(t);
 for(const mode of ['discussion','planning','execution'] as const){
  await assert.rejects(createSandboxBroker({...f.options,mode,profileDirectory:f.options.workspaceRoot},f),{code:'BROKER_PROFILE_IN_WORKSPACE'});
  await assert.rejects(createSandboxBroker({...f.options,mode,profileDirectory:join(f.options.workspaceRoot,'nested-profile')},f),{code:'BROKER_PROFILE_IN_WORKSPACE'});
 }
 assert.equal(f.plan,undefined);
});

test('native trust append is accepted only during startup and later config changes fail closed',async(t)=>{
 const f=await fixture(t,{nativeTrust:true});const broker=await createSandboxBroker(f.options,f);
 await broker.execute({operationId:'before-drift',argv:['synthetic']});
 await appendFile(join(f.plan!.env.CODEX_HOME,'config.toml'),'\n[projects.\'extra\']\ntrust_level = "trusted"\n');
 await assert.rejects(broker.execute({operationId:'after-drift',argv:['synthetic']}),{code:'BROKER_CONFIG_DRIFT'});
 assert.equal(f.calls.filter(x=>x.method==='command/exec').length,1);await broker.close();
});

test('unknown command outcome is retained without retry and argv is snapshotted before awaits',async(t)=>{
 const f=await fixture(t,{rejectCommand:true});const broker=await createSandboxBroker(f.options,f);
 const argv=['original'];const first=broker.execute({operationId:'unknown',argv});argv[0]='mutated';
 await assert.rejects(first);await assert.rejects(broker.execute({operationId:'unknown',argv:['original']}));
 const commands=f.calls.filter(x=>x.method==='command/exec');assert.equal(commands.length,1);assert.deepEqual(commands[0].params.command,['original']);await broker.close();
});
test('broker owns an offline isolated home and fixes command root, profile, output and timeout',async(t)=>{
 const f=await fixture(t);const broker=await createSandboxBroker(f.options,f);
 assert.equal(f.plan!.cwd,f.options.workspaceRoot);assert.equal(f.plan!.env.OPENAI_API_KEY,undefined);assert.equal(Object.keys(f.plan!.env).filter(k=>k.toLowerCase()==='path').length,1);
 const config=await readFile(join(f.plan!.env.CODEX_HOME,'config.toml'),'utf8');assert.match(config,/http:\/\/127\.0\.0\.1:1\/v1/);assert.match(config,/requires_openai_auth = false/);
 assert.equal(broker.metadata.scope,'paos_mediated_commands');assert.equal(broker.metadata.workspaceRoot,f.options.workspaceRoot);
 const request={operationId:'operation-1',argv:['synthetic-command','arg'],timeoutMs:1234};
 assert.deepEqual(await broker.execute(request),{exitCode:0,stdout:'synthetic',stderr:''});await broker.execute(request);
 const commands=f.calls.filter(x=>x.method==='command/exec');assert.equal(commands.length,1);
 const {CODEX_HOME,...commandEnv}=f.plan!.env;
 assert.deepEqual(commands[0].params,{command:request.argv,cwd:f.options.workspaceRoot,permissionProfile:'paos_execution',timeoutMs:1234,outputBytesCap:16384,processId:commands[0].params.processId,env:commandEnv});
 assert.equal(f.calls.some(x=>/turn\/|account\//.test(x.method)),false);
 await assert.rejects(broker.execute({...request,argv:['different']}),{code:'BROKER_OPERATION_CONFLICT'});
 await assert.rejects(broker.execute({operationId:'too-long',argv:['x'.repeat(32769)]}),{code:'BROKER_COMMAND_INVALID'});
 await assert.rejects(broker.execute({operationId:'timeout',argv:['x'],timeoutMs:30001}),{code:'BROKER_COMMAND_INVALID'});
 await broker.close();
});
test('project configuration, unavailable MXC or expanded returned roots stop the owned child',async(t)=>{
 for(const overrides of [{projectLayer:true},{readiness:'notReady'},{thread:{runtimeWorkspaceRoots:[join(tmpdir(),'foreign')]}}]){
  const f=await fixture(t,overrides);await assert.rejects(createSandboxBroker(f.options,f));assert.equal(f.closed,true);assert.equal(f.calls.some(x=>x.method==='command/exec'),false);
 }
});
test('read-only modes select the immutable readonly profile',async(t)=>{
 for(const mode of ['discussion','planning'] as const){const f=await fixture(t);const broker=await createSandboxBroker({...f.options,mode},f);await broker.execute({operationId:'read',argv:['synthetic']});assert.equal(f.calls.find(x=>x.method==='command/exec')!.params.permissionProfile,'paos_readonly');await broker.close();}
});
test('one active operation is interruptible using its native connection scoped process id',async(t)=>{
 const f=await fixture(t,{hold:true});const broker=await createSandboxBroker(f.options,f);
 const pending=broker.execute({operationId:'long-running',argv:['synthetic']});
 for(let n=0;n<30&&!f.calls.some(x=>x.method==='command/exec');n++)await new Promise(resolve=>setTimeout(resolve,5));
 await assert.rejects(broker.execute({operationId:'second',argv:['synthetic']}),{code:'BROKER_BUSY'});
 await broker.interrupt('long-running');assert.equal((await pending).stdout,'stopped');
 assert.equal(f.calls.find(x=>x.method==='command/exec/terminate')!.params.processId,f.calls.find(x=>x.method==='command/exec')!.params.processId);
 await broker.close();
});

test('oversized runtime output is rejected and never returned or blindly re-executed',async(t)=>{
 const f=await fixture(t,{largeOutput:true});const broker=await createSandboxBroker(f.options,f);
 const request={operationId:'oversized',argv:['synthetic']};
 await assert.rejects(broker.execute(request),{code:'BROKER_OUTPUT_LIMIT'});await assert.rejects(broker.execute(request),{code:'BROKER_OUTPUT_LIMIT'});
 assert.equal(f.calls.filter(x=>x.method==='command/exec').length,1);await broker.close();
});
