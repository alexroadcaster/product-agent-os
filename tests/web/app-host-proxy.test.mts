import assert from 'node:assert/strict';
import {test} from 'node:test';
import {createProxyWebSocket,websocketAccept,MAX_PROXY_BYTES} from '../../apps/local-service/src/runtime/proxy-websocket.mts';
import {createReadOnlyProbeSession,parseProbeArguments,probeAppHost} from './single-window/app-host-proxy-probe.mts';
const key='c3ludGhldGljLXByb2JlIQ==';
function handshake(accept=websocketAccept(key)){return Buffer.from(`HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: ${accept}\r\n\r\n`);}
function frame(text:string,opcode=1,fin=true){const data=Buffer.from(text);assert.ok(data.length<126);return Buffer.concat([Buffer.from([(fin?128:0)|opcode,data.length]),data]);}
function setup(){const writes:Buffer[]=[],messages:unknown[]=[];let ready=0,closed=0;const ws=createProxyWebSocket({key,write:b=>writes.push(b),ready:()=>ready++,message:v=>messages.push(v),closed:()=>closed++});return {ws,writes,messages,get ready(){return ready;},get closed(){return closed;}};}
test('proxy rejects an invalid WebSocket accept instead of treating proxy as JSONL',()=>{const s=setup();s.ws.start();assert.match(s.writes[0].toString(),/GET \/ HTTP\/1.1/);assert.throws(()=>s.ws.feed(handshake('wrong')),{message:'PROXY_HANDSHAKE_INVALID'});});
test('split upgrade and fragmented UTF-8 JSON survive ping; client messages and pong are masked',()=>{
 const s=setup();s.ws.start();const head=handshake();s.ws.feed(head.subarray(0,11));assert.equal(s.ready,0);s.ws.feed(head.subarray(11));assert.equal(s.ready,1);
 s.ws.feed(frame('{"text":',1,false));s.ws.feed(frame('ping',9));s.ws.feed(frame('"тест"}',0));assert.deepEqual(s.messages,[{text:'тест'}]);assert.equal(s.writes.at(-1)![0],138);assert.ok(s.writes.at(-1)![1]&128);
 s.ws.send({id:1});const b=s.writes.at(-1)!;assert.equal(b[0],129);assert.ok(b[1]&128);const data=b.subarray(6).map((v,i)=>v^b[2+i%4]);assert.deepEqual(JSON.parse(data.toString()),{id:1});
});
test('coalesced handshake and frames emit each JSON response',()=>{const s=setup();s.ws.start();s.ws.feed(Buffer.concat([handshake(),frame('{"id":1}'),frame('{"id":2}') ]));assert.deepEqual(s.messages,[{id:1},{id:2}]);});
test('16-bit and 64-bit lengths support partial header/payload and binary JSON',()=>{for(const length of [130,70000]){const s=setup();s.ws.start();s.ws.feed(handshake());const data=Buffer.from(JSON.stringify({text:'x'.repeat(length)})),header=Buffer.alloc(length<65536?4:10);header[0]=130;header[1]=length<65536?126:127;if(length<65536)header.writeUInt16BE(data.length,2);else header.writeBigUInt64BE(BigInt(data.length),2);s.ws.feed(header.subarray(0,3));s.ws.feed(Buffer.concat([header.subarray(3),data.subarray(0,5)]));assert.equal(s.messages.length,0);s.ws.feed(data.subarray(5));assert.deepEqual(s.messages,[{text:'x'.repeat(length)}]);s.ws.send({text:'x'.repeat(length)});assert.equal(s.writes.at(-1)![1],length<65536?254:255);}});
test('empty fragments cannot grow metadata without a bound',()=>{const s=setup();s.ws.start();s.ws.feed(handshake());s.ws.feed(frame('',1,false));for(let i=1;i<1024;i++)s.ws.feed(frame('',0,false));assert.throws(()=>s.ws.feed(frame('',0,false)),{message:'PROXY_LIMIT'});});
for(const [name,bytes,code] of [
 ['masked server',Buffer.from([129,128]),'PROXY_FRAME_INVALID'],['RSV',Buffer.from([193,0]),'PROXY_FRAME_INVALID'],
 ['unexpected continuation',frame('{}',0),'PROXY_FRAME_INVALID'],['fragmented ping',frame('',9,false),'PROXY_FRAME_INVALID'],
 ['nonminimal length',Buffer.from([129,126,0,1]),'PROXY_FRAME_INVALID'],['invalid JSON',frame('no'),'PROXY_JSON_INVALID'],
 ['invalid UTF-8',Buffer.from([129,1,255]),'PROXY_UTF8_INVALID'],['invalid close',frame('x',8),'PROXY_CLOSE_INVALID'],
 ['reserved close code',Buffer.from([136,2,3,237]),'PROXY_CLOSE_INVALID'],['oversize control',Buffer.from([137,126]),'PROXY_FRAME_INVALID'],
 ] as const)test(`rejects ${name}`,()=>{const s=setup();s.ws.start();s.ws.feed(handshake());assert.throws(()=>s.ws.feed(bytes),{message:code});});
test('oversize headers, buffer, frame and fragmented message are bounded',()=>{
 const a=setup();a.ws.start();assert.throws(()=>a.ws.feed(Buffer.alloc(16385,65)),{message:'PROXY_HANDSHAKE_LIMIT'});
 const b=setup();b.ws.start();assert.throws(()=>b.ws.feed(Buffer.alloc(MAX_PROXY_BYTES+1)),{message:'PROXY_LIMIT'});
 const c=setup();c.ws.start();c.ws.feed(handshake());const header=Buffer.alloc(10);header[0]=129;header[1]=127;header.writeBigUInt64BE(BigInt(MAX_PROXY_BYTES+1),2);assert.throws(()=>c.ws.feed(header),{message:'PROXY_LIMIT'});
 const d=setup();d.ws.start();d.ws.feed(handshake());const part=Buffer.alloc(600004);part[0]=1;part[1]=127;part.writeBigUInt64BE(599994n,2);d.ws.feed(part);part[0]=128;assert.throws(()=>d.ws.feed(part),{message:'PROXY_LIMIT'});
});
test('EOF never becomes success, proper close is acknowledged and terminates',()=>{
 const a=setup();a.ws.start();assert.throws(()=>a.ws.end(),{message:'PROXY_EOF'});
 const b=setup();b.ws.start();b.ws.feed(handshake());b.ws.feed(frame('',8));assert.equal(b.closed,1);assert.equal(b.writes.at(-1)![0],136);assert.doesNotThrow(()=>b.ws.end());assert.throws(()=>b.ws.send({}),{message:'PROXY_NOT_READY'});
 const c=setup();c.ws.start();c.ws.feed(handshake());c.ws.feed(frame('{',1,false));assert.throws(()=>c.ws.end(),{message:'PROXY_EOF'});
});
test('rejects unrequested extensions and duplicate accept',()=>{for(const extra of ['Sec-WebSocket-Extensions: permessage-deflate','Sec-WebSocket-Accept: duplicate']){const s=setup();s.ws.start();assert.throws(()=>s.ws.feed(Buffer.from(handshake().toString().replace('\r\n\r\n',`\r\n${extra}\r\n\r\n`))),{message:'PROXY_HANDSHAKE_INVALID'});}});
test('probe permits only initialize and loaded list, reducing identities to boolean/count',()=>{
 const sent:any[]=[],receipts:any[]=[];const id='00000000-0000-0000-0000-000000000001';const p=createReadOnlyProbeSession(v=>sent.push(v),v=>receipts.push(v),id);p.ready();p.message({id:1,result:{userAgent:'codex/0.167.0 synthetic'}});p.message({id:2,result:{data:[id]}});
 assert.deepEqual(sent.map(v=>v.method),['initialize','initialized','thread/loaded/list']);assert.deepEqual(receipts,[{loadedThreadCount:1,expectedThreadLoaded:true,serverVersion:'0.167.0'}]);assert.ok(!JSON.stringify(receipts).includes(id));assert.throws(()=>p.message({id:3,result:{}}),{message:'PROXY_RPC_INVALID'});
});
test('probe rejects malformed or partial loaded list and unexpected server request without replying',()=>{for(const response of [{id:2,result:{data:['not-a-thread']}},{id:2,result:{data:[],nextCursor:'remaining-page'}},{id:19,method:'item/tool/call',params:{}}]){const sent:any[]=[];const p=createReadOnlyProbeSession(v=>sent.push(v),()=>assert.fail('unexpected receipt'));p.ready();p.message({id:1,result:{}});assert.throws(()=>p.message(response),{message:'PROXY_RPC_INVALID'});assert.equal(sent.length,3);}});
test('CLI has explicit read-only opt-in and rejects duplicate or unknown arguments',()=>{assert.throws(()=>parseProbeArguments(['--binary','x']));assert.throws(()=>parseProbeArguments(['--read-only-proxy','--binary','x','--binary','y']));assert.throws(()=>parseProbeArguments(['--read-only-proxy','--binary','x','--resume','yes']));assert.deepEqual(parseProbeArguments(['--read-only-proxy','--binary','x']),{binary:'x',socket:undefined,expectedThread:undefined});});
test('missing executable returns a redacted failure and confirmed proxy exit',async()=>{const receipt=await probeAppHost({binary:process.platform==='win32'?'C:/paos-synthetic-missing/never.exe':'/paos-synthetic-missing/never',timeoutMs:1000});assert.equal(receipt.status,'transport_unavailable');assert.equal(receipt.errorCategory,'PROXY_START_FAILED');assert.equal(receipt.proxyExitConfirmed,true);assert.ok(!JSON.stringify(receipt).includes('never'));});
