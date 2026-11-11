import assert from 'node:assert/strict';
import {test} from 'node:test';
import {Readable} from 'node:stream';
import {toFetchRequest} from '../../apps/local-service/src/main.mts';

test('HTTP native adapter rejects foreign Host and oversized bodies before application dispatch',async()=>{
 const request=(host:string,body:string)=>Object.assign(Readable.from([Buffer.from(body)]),{method:'POST',url:'/api/v1/fixture',headers:{host,'content-type':'application/json'},rawHeaders:['Host',host]});
 await assert.rejects(toFetchRequest(request('attacker.example','{}') as any,'http://127.0.0.1:41001'),{code:'HOST_REJECTED'});
 await assert.rejects(toFetchRequest(request('127.0.0.1:41001','x'.repeat(1024*1024+1)) as any,'http://127.0.0.1:41001'),{code:'REQUEST_TOO_LARGE'});
 const accepted=await toFetchRequest(request('127.0.0.1:41001','{}') as any,'http://127.0.0.1:41001');
 assert.equal(accepted.url,'http://127.0.0.1:41001/api/v1/fixture');assert.equal(await accepted.text(),'{}');
});

test('service awaits asynchronous application init before ready and closes injected resources on Quit',async()=>{
 const {startLocalService}=await import('../../apps/local-service/src/main.mts');
 const calls:string[]=[];let finishInit:()=>void=()=>{};let initialized=false;
 const init=new Promise<void>((resolve)=>finishInit=resolve);
 const server={requestTimeout:0,headersTimeout:0,keepAliveTimeout:0,maxHeadersCount:0,
  once(){return this;},off(){return this;},listen(_port:number,host:string,callback:()=>void){assert.equal(host,'127.0.0.1');calls.push('listen-fixture');callback();return this;},
  address(){return {address:'127.0.0.1',family:'IPv4',port:41001};},close(callback?:()=>void){calls.push('server-close');callback?.();return this;}};
 const starting=startLocalService({profileDirectory:process.cwd(),instanceId:'synthetic-instance'},{
  prepareProfile:async()=>{},openStore:async()=>({close:async()=>{calls.push('store-close');}} as any),
  createHttpServer:((_handler:unknown)=>server) as any,
  createApplication:async(options:any)=>{
   assert.equal(options.runtimeCapable(),false);await init;initialized=true;
   return {async handleRequest(){return new Response('{}');},issuePairingCode(){assert.equal(initialized,true);calls.push('pairing');return 'synthetic-code';},revokeSessions(){calls.push('revoke');}} as any;
  },
 });
 await new Promise<void>((resolve)=>setImmediate(resolve));assert.equal(calls.includes('pairing'),false);
 finishInit();const service=await starting;assert.equal(service.pairingCode,'synthetic-code');
 await service.quit();
 assert.deepEqual(calls,['listen-fixture','pairing','revoke','server-close','store-close']);
});

test('native HTTP body exception is limited to exact POST import preview at three MiB',async()=>{
 const request=(path:string,method='POST',size=2*1024*1024)=>Object.assign(Readable.from([Buffer.alloc(size,65)]),{method,url:path,headers:{host:'127.0.0.1:41001'},rawHeaders:['Host','127.0.0.1:41001']});
 const origin='http://127.0.0.1:41001';
 assert.equal((await (await toFetchRequest(request('/api/v1/projects/p/imports/preview') as any,origin)).arrayBuffer()).byteLength,2*1024*1024);
 await assert.rejects(toFetchRequest(request('/api/v1/projects/p/imports/preview','PUT') as any,origin),{code:'REQUEST_TOO_LARGE'});
 await assert.rejects(toFetchRequest(request('/api/v1/projects/p/imports/preview/extra') as any,origin),{code:'REQUEST_TOO_LARGE'});
 await assert.rejects(toFetchRequest(request('/api/v1/projects/p/imports/preview','POST',3*1024*1024+1) as any,origin),{code:'REQUEST_TOO_LARGE'});
});

test('native fetch Request preserves the host cancellation signal for bounded rebuild work',async()=>{
 const incoming=Object.assign(Readable.from([]),{method:'GET',url:'/api/v1/fixture',headers:{host:'127.0.0.1:41001'},rawHeaders:['Host','127.0.0.1:41001']});
 const controller=new AbortController();
 const request=await toFetchRequest(incoming as any,'http://127.0.0.1:41001',controller.signal);
 controller.abort();
 assert.equal(request.signal.aborted,true);
});
