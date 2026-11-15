import test from 'node:test';
import assert from 'node:assert/strict';
import {createPreview} from './prototype-preview.mts';
test('preview binds loopback, serves synthetic bundle, rejects mutation and outside paths',async()=>{
 const {server,url}=await createPreview();
 try{
  assert.equal((server.address() as {address:string}).address,'127.0.0.1');
  const index=await fetch(url);assert.equal(index.status,200);assert.match(await index.text(),/FUNC-G02/);
  const data=await fetch(url+'/data.json');assert.equal((await data.json()).f31.meta.coverage.status,'unavailable');
  assert.equal((await fetch(url+'/data.json',{method:'POST'})).status,405);
  assert.equal((await fetch(url+'/%2e%2e%5cprototype-build.json')).status,404);
  assert.equal((await fetch(url+'/missing')).status,404);
 }finally{await new Promise<void>(done=>server.close(()=>done()));}
});
