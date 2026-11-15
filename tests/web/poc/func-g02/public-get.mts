import {mkdir,writeFile} from 'node:fs/promises';
import {resolve,relative,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';

const repositories=['DeusData/codebase-memory-mcp','k1LoW/tbls','sverweij/dependency-cruiser'];
const allowedHost=new Set(['api.github.com','github.com','raw.githubusercontent.com','release-assets.githubusercontent.com','objects.githubusercontent.com']);
/** Public, unauthenticated GET only. No installer, credential lookup, execution or arbitrary destination is supported. */
export async function publicGet(address:string,destination:string){
 const first=new URL(address),target=resolve(destination),root=resolve('.tmp/func-g02');
 if(first.protocol!=='https:'||first.username||first.password||!['github.com','api.github.com','raw.githubusercontent.com'].includes(first.hostname)||!repositories.some(repo=>first.pathname.toLowerCase().includes(repo.toLowerCase())))throw Error('PUBLIC_RESEARCH_URL_REQUIRED');
 const rel=relative(root,target);if(!rel||rel.startsWith('..')||resolve(root,rel)!==target)throw Error('POC_DESTINATION_REQUIRED');
 let current=first;let response:Response|undefined;
 for(let redirects=0;redirects<=4;redirects++){
  if(current.protocol!=='https:'||current.username||current.password||!allowedHost.has(current.hostname))throw Error('REDIRECT_NOT_ALLOWED');
  response=await fetch(current,{method:'GET',redirect:'manual',headers:{'User-Agent':'PAOS-isolated-public-PoC','Accept':'application/octet-stream, application/json, text/plain'},signal:AbortSignal.timeout(120000)});
  if([301,302,303,307,308].includes(response.status)){const next=response.headers.get('location');await response.body?.cancel();if(!next)throw Error('REDIRECT_INVALID');current=new URL(next,current);continue;}
  break;
 }
 if(!response?.ok)throw Error('PUBLIC_GET_'+response?.status);
 const maxBytes=150*1024*1024;if(Number(response.headers.get('content-length')??0)>maxBytes)throw Error('ARTIFACT_TOO_LARGE');
 const chunks:Uint8Array[]=[];let bytes=0;
 for await(const chunk of response.body!){bytes+=chunk.byteLength;if(bytes>maxBytes)throw Error('ARTIFACT_TOO_LARGE');chunks.push(chunk);}
 const body=Buffer.concat(chunks);await mkdir(dirname(target),{recursive:true});await writeFile(target,body,{flag:'wx'});
 const receipt={url:first.href,finalHost:current.hostname,bytes,sha256:createHash('sha256').update(body).digest('hex'),retrievedAt:new Date().toISOString()};
 await writeFile(target+'.receipt.json',JSON.stringify(receipt,null,2)+'\n',{flag:'wx'});return receipt;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){if(process.argv.length!==4)throw Error('URL_AND_DESTINATION_REQUIRED');console.log(JSON.stringify(await publicGet(process.argv[2],process.argv[3])));}
