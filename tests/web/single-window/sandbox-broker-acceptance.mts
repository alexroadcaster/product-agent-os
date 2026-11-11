import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {mkdir,mkdtemp,readFile,readdir,rm,writeFile,access} from 'node:fs/promises';
import {arch,platform,release} from 'node:os';
import {isAbsolute,join,resolve,sep} from 'node:path';
import {createSandboxBroker,sandboxBrokerConfiguration,type SandboxBroker} from '../../../apps/local-service/src/runtime/sandbox-broker.mts';
import {adapterRevision,inspectConfiguredRuntime,inspectRuntimeTuple,type RuntimeManifest} from '../../../packages/contracts/runtime/manifest.mts';

const args=process.argv.slice(2),binary=args[args.indexOf('--binary')+1];
if(!args.includes('--run-once')||!args.includes('--binary')||!binary||!isAbsolute(binary))throw new Error('Explicit --run-once --binary ABSOLUTE_PATH required.');
const candidate=args.includes('--candidate-inspection'),scratch=resolve('.tmp/paos-m1/astra-transport');await mkdir(scratch,{recursive:true});
const manifest:RuntimeManifest=JSON.parse(await readFile('packages/contracts/runtime/qualified-manifest.json','utf8'));
const sha=(bytes:Uint8Array)=>createHash('sha256').update(bytes).digest('hex');
const fingerprint={version:manifest.codex.version,sha256:sha(await readFile(binary))};
const currentRevision=await adapterRevision();
const reasons=inspectRuntimeTuple(manifest,{platform:platform(),arch:arch(),windowsRelease:release(),node:{version:process.version,sha256:sha(await readFile(process.execPath))},sqliteVersion:process.versions.sqlite!,adapterRevision:currentRevision,packageLockSha256:sha(await readFile('apps/web/package-lock.json')),codexSha256:fingerprint.sha256});
assert.equal(manifest.codex.version,'0.167.0');assert.deepEqual(reasons.filter(reason=>candidate&&reason==='adapter_mismatch'?false:true),[]);
const root=await mkdtemp(join(scratch,'broker-acceptance-'));assert.ok(root.startsWith(scratch+sep));
const evidence:Record<string,unknown>={claim:candidate?'candidate_native_command_broker':'qualified_native_command_broker',candidateInspection:candidate,binarySha256:fingerprint.sha256,adapterRevision:currentRevision,manifestAdapterRevision:manifest.adapterRevision,providerRequests:0,modelTurns:0,credentialOperations:0,cases:[]};
let broker:SandboxBroker|undefined;
const exists=async(path:string)=>{try{await access(path);return true;}catch{return false;}};
try {
 const workspace=join(root,'workspace'),profile=join(root,'profile'),outside=join(root,'outside.txt');await mkdir(workspace);await mkdir(profile);await writeFile(outside,'canary');
 await writeFile(join(profile,'runtime-selection.json'),JSON.stringify({binaryPath:binary}));
 const deps=candidate?{inspect:async()=>({qualified:true,reasons:[],fingerprint,expected:manifest.codex,binaryPath:binary})}:undefined;
 const script=`const fs=require('node:fs');const paths=process.argv.slice(1);const out={};for(let i=0;i<paths.length;i++){try{fs.writeFileSync(paths[i],'written');out[['inside','outside','temp'][i]]='written';}catch(e){out[['inside','outside','temp'][i]]=e.code;}}console.log(JSON.stringify(out));`;
 for(const mode of ['discussion','planning','execution'] as const) {
  broker=await createSandboxBroker({binaryPath:binary,profileDirectory:profile,workspaceRoot:workspace,mode},deps);
  const homes=(await readdir(profile)).filter(name=>name.startsWith('sandbox-broker-'));assert.equal(homes.length,1);const home=join(profile,homes[0]);
  const inside=join(workspace,'inside.txt'),temp=join(home,'temp','temp.txt');await writeFile(inside,'canary');await writeFile(temp,'canary');
  const reply=await broker.execute({operationId:`writes-${mode}`,argv:[process.execPath,'-e',script,inside,outside,temp],timeoutMs:10000});
  if(reply.exitCode!==0)evidence.syntheticCommandFailure={mode,exitCode:reply.exitCode,stdout:reply.stdout.replaceAll(root,'<synthetic-root>'),stderr:reply.stderr.replaceAll(root,'<synthetic-root>')};
  assert.equal(reply.exitCode,0);const writes=JSON.parse(reply.stdout);assert.equal(writes.inside,mode==='execution'?'written':'EPERM');
  assert.ok(['EACCES','EPERM'].includes(writes.outside));assert.ok(['EACCES','EPERM'].includes(writes.temp));
  assert.equal(await readFile(outside,'utf8'),'canary');assert.equal(await readFile(temp,'utf8'),'canary');assert.equal(await readFile(inside,'utf8'),mode==='execution'?'written':'canary');
  const row:Record<string,unknown>={mode,writeResults:writes,exitCode:reply.exitCode,nativeSandbox:broker.metadata.nativeSandbox,scope:broker.metadata.scope};
  const configBytes=await readFile(join(home,'config.toml'));row.configuration={beforeSha256:sha(Buffer.from(sandboxBrokerConfiguration)),afterSha256:sha(configBytes),beforeTrustTables:0,afterTrustTables:(configBytes.toString('utf8').match(/^\[projects\./gm)??[]).length};
  if(mode==='execution') {
   const marker=join(workspace,'running.txt');const pending=broker.execute({operationId:'interrupt-long',argv:[process.execPath,'-e',`require('node:fs').writeFileSync(process.argv[1],'running');setInterval(()=>{},1000)`,marker],timeoutMs:30000});
   for(let n=0;n<100&&!await exists(marker);n++)await new Promise(resolve=>setTimeout(resolve,50));assert.equal(await exists(marker),true);
   const start=Date.now();await broker.interrupt('interrupt-long');const stopped=await pending;row.stopElapsedMs=Date.now()-start;row.stopExitCode=stopped.exitCode;assert.ok(Date.now()-start<5000);assert.notEqual(stopped.exitCode,0);
  }
  row.authFileCreated=await exists(join(home,'auth.json'));assert.equal(row.authFileCreated,false);
  await broker.close();broker=undefined;row.homeCleaned=!await exists(home);assert.equal(row.homeCleaned,true);(evidence.cases as unknown[]).push(row);
 }
 evidence.status='passed';
} catch(error) {
 evidence.status='failed';evidence.errorCode=(error as {code?:string}).code??(error as Error).name;evidence.errorMessage=(error as Error).message.replaceAll(root,'<synthetic-root>');process.exitCode=1;
} finally {
 try{await broker?.close();}catch{evidence.closeFailure=true;process.exitCode=1;}
 if(!evidence.closeFailure){await rm(root,{recursive:true,force:true});evidence.fixtureCleaned=true;}
 const file=join(scratch,`sandbox-broker-${candidate?'candidate':'default'}-${Date.now()}.json`);await writeFile(file,JSON.stringify(evidence,null,2));console.log(JSON.stringify(evidence,null,2));
}
