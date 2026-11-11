import assert from 'node:assert/strict';
import {test} from 'node:test';
import {fileURLToPath} from 'node:url';
import {fork} from 'node:child_process';
import {startIpcService} from '../../apps/launcher/main.mts';

test('native launcher host awaits ready and stopped plus clean exit, with synthetic IPC only',async(t)=>{
 const child=fork(fileURLToPath(new URL('./launcher-native.fixture.mts',import.meta.url)),[],{execArgv:[],env:{SystemRoot:process.env.SystemRoot},silent:true});
 t.after(()=>{if(child.exitCode===null&&child.signalCode===null)child.kill();});
 const controller=new AbortController();
 const service=await startIpcService({child,instanceId:'fixture-instance',build:'paos-m1-0.1.0',onPairingCode(code){assert.equal(code,'synthetic-pairing');}},controller.signal);
 assert.equal(service.status,'started');
 if(service.status==='started') {
  assert.equal(service.port,41231);
  assert.deepEqual(await service.quit(),{status:'stopped'});
  assert.equal(child.exitCode,0);
 }
});

test('native entrypoint joins launcher ownership to synthetic IPC and never writes the pairing code',async(t)=>{
 const {mkdtemp,readFile,rm,stat}=await import('node:fs/promises');const {tmpdir}=await import('node:os');const {join}=await import('node:path');
 const {runNativeLauncher}=await import('../../apps/launcher/main.mts');
 const profile=await mkdtemp(join(tmpdir(),'paos-native-launcher-'));
 t.after(()=>rm(profile,{recursive:true,force:true}));
 let windows=0;
 const result=await runNativeLauncher({profileDirectory:profile,
  serviceModule:fileURLToPath(new URL('./launcher-native.fixture.mts',import.meta.url)),
  async readHealth(endpoint){return {...endpoint,build:'paos-m1-0.1.0',alive:true,sourceReaderReady:true,runtimeCapable:false};},
  async showWindow(input){windows++;assert.equal(input.pairingCode,'synthetic-pairing');assert.equal(input.owner,true);
   const record=await readFile(join(profile,'service-instance','endpoint.json'),'utf8');
   assert.equal(record.includes('synthetic-pairing'),false);assert.match(input.origin,/^http:\/\/127\.0\.0\.1:/);return 'quit';},
 });
 assert.equal(result.status,'opened');assert.equal(windows,1);
 if(result.status==='opened')assert.equal(result.runtime,'runtime_qualification_required');
 await assert.rejects(stat(join(profile,'service-instance')),{code:'ENOENT'});
});

test('clean child exit without a stopped acknowledgement keeps shutdown unresolved',async(t)=>{
 const child=fork(fileURLToPath(new URL('./launcher-native.fixture.mts',import.meta.url)),['no-ack'],{execArgv:[],env:{SystemRoot:process.env.SystemRoot},silent:true});
 t.after(()=>{if(child.exitCode===null&&child.signalCode===null)child.kill();});
 const service=await startIpcService({child,instanceId:'fixture-instance',build:'paos-m1-0.1.0',onPairingCode(){}},new AbortController().signal);
 assert.equal(service.status,'started');if(service.status!=='started')return;
 assert.deepEqual(await service.quit(),{status:'stop_blocked',phase:'stop_children'});
});

test('dismissed native controls retain IPC ownership and a later quit request releases the reservation',{timeout:5000},async(t)=>{
 const {mkdtemp,rm,stat}=await import('node:fs/promises');const {tmpdir}=await import('node:os');const {join}=await import('node:path');
 const {runNativeLauncher}=await import('../../apps/launcher/main.mts');const profile=await mkdtemp(join(tmpdir(),'paos-keep-running-'));
 t.after(()=>rm(profile,{recursive:true,force:true}));
 const result=await runNativeLauncher({profileDirectory:profile,serviceModule:fileURLToPath(new URL('./launcher-keep-running.fixture.mts',import.meta.url)),
  async readHealth(endpoint){return {...endpoint,build:'paos-m1-0.1.0',alive:true,sourceReaderReady:true,runtimeCapable:false};},
  async showWindow(){return 'closed';},
 });
 assert.equal(result.status,'opened');await stat(join(profile,'service-instance'));
 const deadline=Date.now()+1500;let released=false;
 while(Date.now()<deadline) {
  try{await stat(join(profile,'service-instance'));}catch(error){if((error as any).code==='ENOENT'){released=true;break;}throw error;}
  await new Promise((resolve)=>setTimeout(resolve,10));
 }
 assert.equal(released,true);
});
