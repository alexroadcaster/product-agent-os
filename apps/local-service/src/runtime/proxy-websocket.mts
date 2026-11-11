import {createHash,randomBytes} from 'node:crypto';
export const MAX_PROXY_BYTES=1024*1024;
export function websocketAccept(key:string){return createHash('sha1').update(key+'258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest('base64');}
export function createProxyWebSocket(options:{write:(bytes:Buffer)=>void;ready:()=>void;message:(value:unknown)=>void;closed:()=>void;key?:string}) {
 const key=options.key??randomBytes(16).toString('base64');
 let buffer:Buffer=Buffer.alloc(0),upgraded=false,started=false,dead=false,fragmentOpcode=0,fragmentBytes=0;let fragments:Buffer[]=[];
 function fail(code:string):never{dead=true;buffer=Buffer.alloc(0);fragments=[];throw new Error(code);}
 function utf8(data:Buffer){try{return new TextDecoder('utf-8',{fatal:true}).decode(data);}catch{return fail('PROXY_UTF8_INVALID');}}
 function writeFrame(opcode:number,data:Buffer){
  if(data.length>MAX_PROXY_BYTES)fail('PROXY_LIMIT');const mask=randomBytes(4);let header:Buffer;
  if(data.length<126)header=Buffer.from([128|opcode,128|data.length]);
  else if(data.length<=65535){header=Buffer.alloc(4);header[0]=128|opcode;header[1]=254;header.writeUInt16BE(data.length,2);}
  else{header=Buffer.alloc(10);header[0]=128|opcode;header[1]=255;header.writeBigUInt64BE(BigInt(data.length),2);}
  const encoded=Buffer.alloc(data.length);for(let i=0;i<data.length;i++)encoded[i]=data[i]^mask[i%4];options.write(Buffer.concat([header,mask,encoded]));
 }
 function decode(data:Buffer){let value:unknown;try{value=JSON.parse(utf8(data));}catch(error){if(dead)throw error;return fail('PROXY_JSON_INVALID');}options.message(value);}
 function feed(bytes:Buffer){
  if(dead)fail('PROXY_CLOSED');if(!started)fail('PROXY_NOT_STARTED');
  if(buffer.length+bytes.length>MAX_PROXY_BYTES)fail('PROXY_LIMIT');buffer=Buffer.concat([buffer,bytes]);
  if(!upgraded){
   const end=buffer.indexOf('\r\n\r\n');if(end<0){if(buffer.length>16384)fail('PROXY_HANDSHAKE_LIMIT');return;}
   if(end>16384)fail('PROXY_HANDSHAKE_LIMIT');const lines=buffer.subarray(0,end).toString('ascii').split('\r\n');
   if(!/^HTTP\/1\.1 101(?: |$)/.test(lines.shift()??''))fail('PROXY_HANDSHAKE_INVALID');const headers=new Map<string,string>();
   for(const line of lines){const colon=line.indexOf(':');if(colon<=0||!/^[!#$%&'*+.^_`|~0-9A-Za-z-]+$/.test(line.slice(0,colon)))fail('PROXY_HANDSHAKE_INVALID');const name=line.slice(0,colon).toLowerCase(),value=line.slice(colon+1).trim();if(headers.has(name))fail('PROXY_HANDSHAKE_INVALID');headers.set(name,value);}
   if(headers.get('upgrade')?.toLowerCase()!=='websocket'||!headers.get('connection')?.toLowerCase().split(',').map(v=>v.trim()).includes('upgrade')||headers.get('sec-websocket-accept')!==websocketAccept(key)||headers.has('sec-websocket-extensions')||headers.has('sec-websocket-protocol'))fail('PROXY_HANDSHAKE_INVALID');
   buffer=buffer.subarray(end+4);upgraded=true;options.ready();
  }
  while(!dead&&buffer.length>=2){
   const first=buffer[0],second=buffer[1],fin=!!(first&128),opcode=first&15,control=opcode>=8;let length=second&127,offset=2;
   if(first&112||second&128||![0,1,2,8,9,10].includes(opcode)||control&&(!fin||length>125))fail('PROXY_FRAME_INVALID');
   if(length===126){if(buffer.length<4)return;length=buffer.readUInt16BE(2);offset=4;if(length<126)fail('PROXY_FRAME_INVALID');}
   else if(length===127){if(buffer.length<10)return;const wide=buffer.readBigUInt64BE(2);if(wide>BigInt(MAX_PROXY_BYTES))fail('PROXY_LIMIT');length=Number(wide);offset=10;if(length<65536)fail('PROXY_FRAME_INVALID');}
   if(length+offset>MAX_PROXY_BYTES)fail('PROXY_LIMIT');if(buffer.length<offset+length)return;
   const payload=Buffer.from(buffer.subarray(offset,offset+length));buffer=buffer.subarray(offset+length);
   if(control){
    if(opcode===9)writeFrame(10,payload);
    if(opcode===8){if(length===1)fail('PROXY_CLOSE_INVALID');if(length>=2){const code=payload.readUInt16BE();if(code<1000||code>=5000||[1004,1005,1006,1015].includes(code)||(code>=1016&&code<3000))fail('PROXY_CLOSE_INVALID');utf8(payload.subarray(2));}writeFrame(8,payload);dead=true;options.closed();}
    continue;
   }
   if(opcode===0){if(!fragmentOpcode)fail('PROXY_FRAME_INVALID');}
   else if(fragmentOpcode)fail('PROXY_FRAME_INVALID');else if(!fin)fragmentOpcode=opcode;
   if(fragmentOpcode){fragmentBytes+=payload.length;if(fragmentBytes>MAX_PROXY_BYTES||fragments.length>=1024)fail('PROXY_LIMIT');fragments.push(payload);if(fin){const joined=Buffer.concat(fragments);fragments=[];fragmentBytes=0;fragmentOpcode=0;decode(joined);}}
   else decode(payload);
  }
 }
 // Narrow uncompressed WebSocket transport. This module never connects, authenticates or starts a Codex turn.
 return {start(){if(started||dead)fail('PROXY_STATE_INVALID');started=true;options.write(Buffer.from(`GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: ${key}\r\nSec-WebSocket-Version: 13\r\n\r\n`));},feed,
  send(value:unknown){if(!upgraded||dead)fail('PROXY_NOT_READY');writeFrame(1,Buffer.from(JSON.stringify(value)));},
  end(){if(!dead)fail('PROXY_EOF');},close(){if(!dead&&upgraded)writeFrame(8,Buffer.from([3,232]));dead=true;buffer=Buffer.alloc(0);fragments=[];}};
}
