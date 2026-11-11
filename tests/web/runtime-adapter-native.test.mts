import assert from 'node:assert/strict';
import {test} from 'node:test';
import {join} from 'node:path';
import {createNativeRpc,nativeProfileConfiguration} from '../../apps/local-service/src/runtime/native-rpc.mts';

test('native RPC gate creates no process when manifest is unqualified',async()=>{
 let prepared=false;let spawned=false;
 await assert.rejects(createNativeRpc({profileDirectory:process.cwd(),binaryPath:process.execPath},{
  inspect:async()=>({qualified:false,reasons:['fixture'],fingerprint:null,expected:null}),
  prepareHome:async()=>{prepared=true;return process.cwd();},spawnRpc:async()=>{spawned=true;throw new Error();},
 }),{code:'RUNTIME_UNQUALIFIED'});
 assert.equal(prepared,false);assert.equal(spawned,false);
});

test('native RPC uses credential-free plan and refuses project config without provider dispatch',async()=>{
 const home=join(process.cwd(),'synthetic-private-runtime');let closed=false;let notifications=0;let turns=0;
 const inspect=async()=>({qualified:true,binaryPath:process.execPath,fingerprint:{version:'fixture',sha256:'fixture'},expected:{version:'fixture',sha256:'fixture'},reasons:[]});
 const rpc=await createNativeRpc({profileDirectory:process.cwd(),binaryPath:process.execPath},{inspect,prepareHome:async()=>home,
  spawnRpc:async(plan)=>{
   assert.deepEqual(plan.args,['app-server','--listen','stdio://']);assert.equal(plan.env.CODEX_HOME,home);
   assert.deepEqual(Object.keys(plan.env).sort(),['SystemRoot','WINDIR','ComSpec','SystemDrive','PATH','CODEX_HOME','USERPROFILE','HOME','APPDATA','LOCALAPPDATA','TEMP','TMP'].sort());
   for(const name of ['USERPROFILE','HOME','APPDATA','LOCALAPPDATA','TEMP','TMP'])assert.ok(plan.env[name]!.startsWith(home+'\\'));
   assert.equal(plan.env.HOME,plan.env.USERPROFILE);assert.equal(plan.env.TEMP,plan.env.TMP);
   assert.equal(plan.env.PATH,join(process.env.SystemRoot!,'System32'));
   assert.equal(plan.env.ComSpec,join(process.env.SystemRoot!,'System32','cmd.exe'));
   assert.equal(plan.env.WINDIR,process.env.SystemRoot);
   assert.equal('OPENAI_API_KEY' in plan.env,false);assert.equal('CODEX_API_KEY' in plan.env,false);
   assert.match(nativeProfileConfiguration,/cli_auth_credentials_store = "ephemeral"/);assert.match(nativeProfileConfiguration,/sandbox = "mxc"/);
   return {generation:'fixture',notify(){notifications++;},close:async()=>{closed=true;},snapshot(){return {generation:'fixture',status:'open',pending:0,stderrBytes:0};},subscribe(){return()=>{};},onClosed(){return()=>{};},respond(){},respondError(){},
    async request(method,params:any){
     if(method==='initialize')return {codexHome:home};
     if(method==='windowsSandbox/readiness')return {status:'ready'};
     if(method==='account/read')return {account:null};
     if(method==='config/read')return {config:{cli_auth_credentials_store:'ephemeral',forced_login_method:'api',windows:{sandbox:'mxc'},model_provider:'openai',web_search:'disabled',mcp_servers:{},features:{apps:false,plugins:false,computer_use:false}},
      layers:[{name:{type:'user',file:join(home,'config.toml')}},...(params.cwd!==home?[{name:{type:'project'}}]:[])]};
     if(method==='turn/start')turns++;return {};
    }};
  }});
 await rpc.request('initialize',{});rpc.notify('initialized');assert.equal(notifications,1);
 await assert.rejects(rpc.request('turn/start',{cwd:process.cwd()}),{code:'RUNTIME_CONFIG_DRIFT'});
 assert.equal(closed,true);assert.equal(turns,0);
});

test('native profile preparation creates private user/AppData/temp directories without launching a process',async(t)=>{
 const {mkdtemp,rm,lstat}=await import('node:fs/promises');const {tmpdir}=await import('node:os');const {resolve,sep}=await import('node:path');
 const profile=await mkdtemp(join(tmpdir(),'paos-native-env-'));
 t.after(async()=>{assert.ok(resolve(profile).startsWith(resolve(tmpdir())+sep));await rm(profile,{recursive:true,force:true});});
 let plans=0;
 await createNativeRpc({profileDirectory:profile,binaryPath:process.execPath},{
  inspect:async()=>({qualified:true,binaryPath:process.execPath,fingerprint:{version:'fixture',sha256:'fixture'},expected:{version:'fixture',sha256:'fixture'},reasons:[]}),
  spawnRpc:async(plan)=>{
   plans++;const home=join(profile,'codex-runtime');assert.equal(plan.env.CODEX_HOME,home);
   for(const name of ['USERPROFILE','HOME','APPDATA','LOCALAPPDATA','TEMP','TMP']) {
    const path=plan.env[name]!;assert.ok(path.startsWith(home+sep));const info=await lstat(path);assert.equal(info.isDirectory(),true);assert.equal(info.isSymbolicLink(),false);
   }
   return {generation:'fixture',request:async()=>({}),notify(){},respond(){},respondError(){},subscribe(){return()=>{};},onClosed(){return()=>{};},close:async()=>{},snapshot(){return {generation:'fixture',status:'open',pending:0,stderrBytes:0};}};
  },
 });
 assert.equal(plans,1);
});
