import {createHash} from 'node:crypto';
import type {AssetProposal} from '../../../../packages/contracts/team/assets.ts';
import type {RemoteSkillCandidate,RemoteSkillSearch} from '../../../../packages/contracts/team/discovery.ts';
import {metadata} from './sources.mts';
import {safePersistedText} from '../redaction/persisted.mts';

export const externalSkillSourceId='openai-plugins-superpowers';
export const externalSkillRevision='d420d13051bffe4543ed39e30fa46b87148e47dd';
const endpoint='https://api.github.com/repos/openai/plugins/',prefix='plugins/superpowers/',maxBody=2*1024*1024;
const sha=(bytes:Buffer|string)=>createHash('sha256').update(bytes).digest('hex'),git=(bytes:Buffer)=>createHash('sha1').update(`blob ${bytes.length}\0`).update(bytes).digest('hex');
const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
const validSha=(value:unknown):value is string=>typeof value==='string'&&/^[a-f0-9]{40}$/.test(value);
type Entry={path:string;type:string;mode:string;sha:string;size?:number};
type Index={entries:Entry[];license:Buffer;licenseSha:string;fetchedAt:string};
/** Anonymous fixed-source reads only. Private search text is filtered locally; remote files remain untrusted data. */
export function createExternalSkillSource(fetcher:typeof fetch=fetch){
 let cached:Index|undefined,expires=0,loading:Promise<Index>|undefined;
 const previews=new Map<string,{proposal:AssetProposal;expires:number}>();
 async function json(path:string,deadline:number):Promise<any>{
  const remaining=deadline-Date.now();if(remaining<=0)fail('REMOTE_SOURCE_TIMEOUT');
  const response=await fetcher(endpoint+path,{method:'GET',credentials:'omit',redirect:'error',headers:{accept:'application/vnd.github+json','x-github-api-version':'2022-11-28'},signal:AbortSignal.timeout(Math.min(5000,remaining))});
  if(!response.ok){await response.body?.cancel();fail(response.status===403||response.status===429?'REMOTE_SOURCE_RATE_LIMITED':'REMOTE_SOURCE_UNAVAILABLE');}
  if(Number(response.headers.get('content-length'))>maxBody){await response.body?.cancel();fail('REMOTE_SOURCE_RESPONSE_LIMIT');}
  if(!response.body)fail('REMOTE_SOURCE_RESPONSE_INVALID');const reader=response.body!.getReader(),chunks:Uint8Array[]=[];let size=0;
  try{for(;;){const part=await reader.read();if(part.done)break;size+=part.value.length;if(size>maxBody){await reader.cancel();fail('REMOTE_SOURCE_RESPONSE_LIMIT');}chunks.push(part.value);}return JSON.parse(Buffer.concat(chunks).toString('utf8'));}finally{reader.releaseLock();}
 }
 async function tree(hash:string,deadline:number,recursive=false):Promise<Entry[]>{
  if(!validSha(hash))fail('REMOTE_TREE_INVALID');const value=await json('git/trees/'+hash+(recursive?'?recursive=1':''),deadline);
  if(value.sha!==hash||value.truncated!==false||!Array.isArray(value.tree)||value.tree.length>1000)fail('REMOTE_TREE_INCOMPLETE');
  const paths=new Set<string>();for(const entry of value.tree){if(typeof entry.path!=='string'||entry.path.length>1024||entry.path.includes('\\')||entry.path.includes(':')||entry.path.split('/').some((p:string)=>!p||p==='.'||p==='..')||!validSha(entry.sha)||paths.has(entry.path.toLowerCase()))fail('REMOTE_TREE_INVALID');paths.add(entry.path.toLowerCase());}
  return value.tree;
 }
 function select(entries:Entry[],path:string,type:'tree'|'blob'){const entry=entries.find(e=>e.path===path);if(!entry||entry.type!==type||entry.mode!==(type==='tree'?'040000':'100644'))fail('REMOTE_SOURCE_UNSUPPORTED_ENTRY');return entry!;}
 async function blob(entry:Entry,deadline:number,max=512*1024){
  if(entry.type!=='blob'||entry.mode!=='100644'||!Number.isSafeInteger(entry.size)||entry.size!<0||entry.size!>max)fail('REMOTE_RESOURCE_UNSUPPORTED');
  const value=await json('git/blobs/'+entry.sha,deadline);if(value.sha!==entry.sha||value.encoding!=='base64'||typeof value.content!=='string')fail('REMOTE_BLOB_INVALID');const encoded=value.content.replace(/\r?\n/g,''),bytes=Buffer.from(encoded,'base64');
  if(bytes.length>max||bytes.length!==entry.size||value.size!==bytes.length||bytes.toString('base64')!==encoded||git(bytes)!==entry.sha)fail('REMOTE_SOURCE_DRIFT');return bytes;
 }
 async function load():Promise<Index>{
  if(cached&&expires>Date.now())return cached;if(loading)return loading;
  loading=(async()=>{const deadline=Date.now()+10000,commit=await json('git/commits/'+externalSkillRevision,deadline);if(commit.sha!==externalSkillRevision||!validSha(commit.tree?.sha))fail('REMOTE_REVISION_INVALID');
   const root=await tree(commit.tree.sha,deadline),plugins=await tree(select(root,'plugins','tree').sha,deadline),entries=await tree(select(plugins,'superpowers','tree').sha,deadline,true);
   const [manifestBytes,license]=await Promise.all([blob(select(entries,'.codex-plugin/plugin.json','blob'),deadline),blob(select(entries,'LICENSE','blob'),deadline)]),manifest=JSON.parse(manifestBytes.toString('utf8')),text=license.toString('utf8');
   if(manifest.name!=='superpowers'||manifest.skills!=='./skills/'||manifest.license!=='MIT'||!text.includes('MIT License')||!text.includes('Permission is hereby granted')||!text.includes('THE SOFTWARE IS PROVIDED'))fail('REMOTE_LICENSE_UNVERIFIED');
   cached={entries,license,licenseSha:sha(license),fetchedAt:new Date().toISOString()};expires=Date.now()+15*60000;return cached;
  })();try{return await loading;}finally{loading=undefined;}
 }
 function candidates(index:Index){return index.entries.filter(e=>/^skills\/[A-Za-z0-9_-]{1,128}\/SKILL\.md$/.test(e.path)).map(entry=>{
  const name=entry.path.split('/')[1],folder='skills/'+name+'/',files=index.entries.filter(e=>e.path.startsWith(folder)&&e.type!=='tree');
  const supported=entry.mode==='100644'&&files.length<=33&&files.every(e=>e.mode==='100644'&&e.type==='blob'&&(/\.(?:md|txt)$/i.test(e.path)||e.path.endsWith('/agents/openai.yaml')));
  return {id:'remote:superpowers:'+name,name,path:prefix+'skills/'+name,origin:'https://github.com/openai/plugins',revision:externalSkillRevision,license:'MIT',licenseVerified:true,importable:supported,...(!supported?{reason:'REMOTE_RESOURCE_UNSUPPORTED'}:{})} satisfies RemoteSkillCandidate;
 });}
 async function search(query:string):Promise<RemoteSkillSearch>{
  if(typeof query!=='string'||query.length>200)fail('REMOTE_QUERY_INVALID');const source={id:externalSkillSourceId,repository:'openai/plugins',revision:externalSkillRevision,package:'superpowers',license:'MIT',fetchedAt:null as string|null};
  try{const index=await load();return {availability:'available',source:{...source,fetchedAt:index.fetchedAt},candidates:candidates(index).filter(c=>c.name.toLowerCase().includes(query.toLowerCase())),querySentToRemote:false};}catch(error){return {availability:'unavailable',reason:String((error as any).code??'REMOTE_SOURCE_UNAVAILABLE'),source,candidates:[],querySentToRemote:false};}
 }
 async function preview(input:{candidateId:string;revision:string}):Promise<AssetProposal>{
  if(!input||Object.keys(input).some(k=>!['candidateId','revision'].includes(k))||typeof input.candidateId!=='string'||input.candidateId.length>200||typeof input.revision!=='string')fail('REMOTE_PREVIEW_INPUT_INVALID');
  if(input.revision!==externalSkillRevision)fail('REMOTE_REVISION_STALE');const index=await load(),candidate=candidates(index).find(c=>c.id===input.candidateId);if(!candidate?.importable)fail('REMOTE_RESOURCE_UNSUPPORTED');
  const folder='skills/'+candidate!.name+'/',files=index.entries.filter(e=>e.path.startsWith(folder)&&e.type!=='tree');if(files.length>33)fail('REMOTE_RESOURCE_LIMIT');const deadline=Date.now()+10000,loaded=new Map<string,Buffer>();let at=0,total=0;
  await Promise.all(Array.from({length:Math.min(4,files.length)},async()=>{while(at<files.length){const entry=files[at++],bytes=await blob(entry,deadline,entry.path===folder+'SKILL.md'?256*1024:512*1024);total+=bytes.length;if(total>1024*1024)fail('REMOTE_RESOURCE_LIMIT');const path=entry.path.slice(folder.length);if(/(?:^|\/)LICENSE(?:\.|$)/i.test(path)||path==='LICENSE.source.txt')fail('REMOTE_NESTED_LICENSE_UNSUPPORTED');let text:string;try{text=new TextDecoder('utf-8',{fatal:true}).decode(bytes);}catch{fail('REMOTE_RESOURCE_UNSUPPORTED');}if(safePersistedText(text!)!==text!)fail('SENSITIVE_ASSET_CONTENT');loaded.set(path,bytes);}}));
  const content=loaded.get('SKILL.md')!.toString('utf8'),meta=metadata(content,'skill');if(meta.unsupported)fail('SKILL_METADATA_UNSUPPORTED');
  for(const match of content.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){let path=match[1].split('#')[0];if(!path||/^https?:\/\//.test(path))continue;try{path=decodeURIComponent(path).replace(/^\.\//,'');}catch{fail('REMOTE_DEPENDENCY_UNAVAILABLE');}if(path.split('/').some(p=>!p||p==='.'||p==='..')||!loaded.has(path))fail('REMOTE_DEPENDENCY_UNAVAILABLE');}
  loaded.delete('SKILL.md');loaded.set('LICENSE.source.txt',index.license);
  const resources=[...loaded].sort(([a],[b])=>a.localeCompare(b)).map(([path,bytes])=>({path,hash:sha(bytes),byteSize:bytes.length,base64:bytes.toString('base64')}));
  const bundleHash=sha(JSON.stringify([externalSkillRevision,sha(Buffer.from(content)),resources.map(r=>[r.path,r.hash])]));
  const proposal:AssetProposal={kind:'skill',action:'create',name:meta.name||candidate!.name,description:meta.description,content,dependencies:[],resources,source:{rootId:externalSkillSourceId,relativePath:candidate!.path,hash:bundleHash,origin:'github_public_readonly',license:'MIT',revision:externalSkillRevision,licenseHash:index.licenseSha},reason:'Reviewed project copy from a pinned public source; no native installation'};
  if(previews.size>=4)previews.delete(previews.keys().next().value!);previews.set(bundleHash,{proposal:structuredClone(proposal),expires:Date.now()+15*60000});return structuredClone(proposal);
 }
 function verify(proposal:AssetProposal){if(!proposal||typeof proposal!=='object')return;if(proposal.action!=='create'||proposal.source?.rootId!==externalSkillSourceId)return;const known=previews.get(proposal.source.hash);if(!known||known.expires<Date.now())fail('REMOTE_PREVIEW_EXPIRED');const canonical=(p:AssetProposal)=>JSON.stringify([p.kind,p.name,p.description,p.content,p.source,(p.resources??[]).map(r=>[r.path,r.hash,r.byteSize,r.base64]).sort(([a],[b])=>String(a).localeCompare(String(b)))]);if(canonical(proposal)!==canonical(known!.proposal))fail('REMOTE_SOURCE_DRIFT');}
 return {search,preview,verify};
}
