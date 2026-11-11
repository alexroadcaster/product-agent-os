import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtemp,mkdir,writeFile,readFile,readdir,rm,symlink,link} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {inspectAppHostEndpoint,classifyAppHostConnectFailure} from '../../apps/local-service/src/runtime/app-host-endpoint.mts';

test('absent documented parent is diagnosed without creating it or disclosing paths',async(t)=>{
 const home=await mkdtemp(join(tmpdir(),'paos-endpoint-'));t.after(()=>rm(home,{recursive:true,force:true}));
 await writeFile(join(home,'auth.json'),'synthetic-do-not-read');
 const result=await inspectAppHostEndpoint({codexHome:home});
 assert.deepEqual(result,{status:'unavailable',reason:'app_host_endpoint_missing',transport:'websocket_over_stdio_proxy'});
 assert.deepEqual(await readdir(home),['auth.json']);
 assert.equal(await readFile(join(home,'auth.json'),'utf8'),'synthetic-do-not-read');
 assert.equal(JSON.stringify(result).includes(home),false);
 assert.equal(classifyAppHostConnectFailure(10050,result),'app_host_endpoint_missing');
 assert.equal(classifyAppHostConnectFailure('WSAENETDOWN',result),'app_host_connect_failed');
});

test('missing endpoint differs from existing unverified endpoint and never establishes App connectivity',async(t)=>{
 const home=await mkdtemp(join(tmpdir(),'paos-endpoint-'));t.after(()=>rm(home,{recursive:true,force:true}));
 const parent=join(home,'app-server-control');await mkdir(parent);
 assert.equal((await inspectAppHostEndpoint({codexHome:home})).reason,'app_host_endpoint_missing');
 await writeFile(join(parent,'app-server-control.sock'),'synthetic-metadata-only');
 const result=await inspectAppHostEndpoint({codexHome:home});
 assert.deepEqual(result,{status:'unverified',reason:'app_host_endpoint_unverified',transport:'websocket_over_stdio_proxy'});
 assert.equal(classifyAppHostConnectFailure(10050,result),'app_host_connect_failed');
 assert.equal(classifyAppHostConnectFailure(10061,result),'app_host_connect_failed');
});

test('invalid parent or endpoint directory is rejected rather than called missing',async(t)=>{
 const home=await mkdtemp(join(tmpdir(),'paos-endpoint-'));t.after(()=>rm(home,{recursive:true,force:true}));
 const parent=join(home,'app-server-control');await writeFile(parent,'synthetic');
 assert.equal((await inspectAppHostEndpoint({codexHome:home})).reason,'app_host_endpoint_invalid');
 await rm(parent);await mkdir(join(parent,'app-server-control.sock'),{recursive:true});
 assert.equal((await inspectAppHostEndpoint({codexHome:home})).reason,'app_host_endpoint_invalid');
 assert.equal((await inspectAppHostEndpoint({codexHome:'relative-home'})).reason,'app_host_endpoint_invalid');
});

test('linked home, parent and endpoint cannot redirect inspection into another profile',async(t)=>{
 const root=await mkdtemp(join(tmpdir(),'paos-endpoint-links-'));t.after(()=>rm(root,{recursive:true,force:true}));
 const home=join(root,'home'),foreign=join(root,'foreign');await mkdir(home);await mkdir(foreign);
 const alias=join(root,'alias');await symlink(home,alias,process.platform==='win32'?'junction':'dir');
 assert.equal((await inspectAppHostEndpoint({codexHome:alias})).reason,'app_host_endpoint_invalid');
 const parent=join(home,'app-server-control');await symlink(foreign,parent,process.platform==='win32'?'junction':'dir');
 assert.equal((await inspectAppHostEndpoint({codexHome:home})).reason,'app_host_endpoint_invalid');
 await rm(parent);await mkdir(parent);
 await symlink(foreign,join(parent,'app-server-control.sock'),process.platform==='win32'?'junction':'dir');
 assert.equal((await inspectAppHostEndpoint({codexHome:home})).reason,'app_host_endpoint_invalid');
 assert.deepEqual(await readdir(foreign),[]);
});

test('hardlinked endpoint is rejected without reading or altering its target',async(t)=>{
 const home=await mkdtemp(join(tmpdir(),'paos-endpoint-hardlink-'));t.after(()=>rm(home,{recursive:true,force:true}));
 const parent=join(home,'app-server-control');await mkdir(parent);
 const target=join(home,'synthetic.txt');await writeFile(target,'unchanged');await link(target,join(parent,'app-server-control.sock'));
 assert.equal((await inspectAppHostEndpoint({codexHome:home})).reason,'app_host_endpoint_invalid');
 assert.equal(await readFile(target,'utf8'),'unchanged');
});
