import {constants} from 'node:fs';
import {lstat,realpath,open,readdir} from 'node:fs/promises';
import {resolve,relative,join,sep} from 'node:path';
import {createHash} from 'node:crypto';
import type {AssetProfile,AssetResource,AssetScope,AssetSource} from '../../../../packages/contracts/team/assets.ts';
import {safePersistedText} from '../redaction/persisted.mts';
import {safeAssetPath,sensitivePath,teamFail,digest} from './contract.mts';
export type AssetRoot={id:string;path:string;scope:'project'|'global'|'vendor';kind:'agent'|'skill'};
export const projectAssetRoots=(root:string):AssetRoot[]=>[{id:'project-agents',path:join(root,'.codex','agents'),scope:'project',kind:'agent'},...['.agents','.codex'].map(p=>({id:`project-skills-${p.slice(1)}`,path:join(root,p,'skills'),scope:'project' as const,kind:'skill' as const}))];
/** Reject all linked ancestors and hardlinked files. Recheck the opened handle before bytes leave the source boundary. */
async function safe(root:AssetRoot,path:string,directory=false){
 if(path&&!safeAssetPath(path))teamFail('ASSET_SOURCE_PATH_INVALID');let target=resolve(root.path);const absolute=resolve(target);const parts=absolute.split(/[\\/]/);let ancestor=parts.shift()!+(process.platform==='win32'?'\\':'/');
 for(const p of parts.filter(Boolean)){ancestor=join(ancestor,p);if((await lstat(ancestor)).isSymbolicLink())teamFail('LINKED_ASSET_SOURCE');}
 const base=await realpath(target);for(const p of path.split('/').filter(Boolean)){target=join(target,p);if((await lstat(target)).isSymbolicLink())teamFail('LINKED_ASSET_SOURCE');}
 const canonical=await realpath(target),within=relative(base,canonical);if(within==='..'||within.startsWith(`..${sep}`)||resolve(base,within)!==canonical)teamFail('ASSET_SOURCE_ESCAPE');
 const stat=await lstat(target);if(directory?!stat.isDirectory():!stat.isFile()||stat.nlink>1)teamFail('LINKED_ASSET_SOURCE');return {target,stat};
}
async function bytes(root:AssetRoot,path:string){const {target,stat}=await safe(root,path);if(stat.size>5*1024*1024)teamFail('ASSET_RESOURCE_LIMIT');const file=await open(target,constants.O_RDONLY|(constants.O_NOFOLLOW??0));try{const current=await file.stat();if(current.ino!==stat.ino||current.dev!==stat.dev||current.nlink>1||current.size!==stat.size)teamFail('ASSET_SOURCE_DRIFT');const data=await file.readFile();if(data.length!==stat.size)teamFail('ASSET_SOURCE_DRIFT');return data;}finally{await file.close();}}
/** Only the documented scalar YAML header subset is projected; unsupported structures stay explicit. */
function metadata(content:string,kind:'agent'|'skill'){
 const header=kind==='skill'?/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(content)?.[1]:content.split(/^developer_instructions\s*=/m)[0];
 const field=(name:string)=>new RegExp(`^${name}\\s*${kind==='skill'?':':'='}\\s*["']?(.*?)["']?\\s*$`,'m').exec(header??'')?.[1]??'';
 const unsupported=kind==='skill'&&(!header||/^\s+(?:-|\w)|[&*!]|:\s*[\[{>|]/m.test(header));
 return {name:field('name').slice(0,512),description:field('description').slice(0,2048),license:field('license').slice(0,512)||null,unsupported};
}
export async function sourceAsset(root:AssetRoot,path:string,copy=false,details=true):Promise<AssetProfile>{
 if(root.kind==='agent'&&!/^[\w.-]+\.toml$/.test(path))teamFail('ASSET_SOURCE_PATH_INVALID');
 if(root.kind==='skill'&&!safeAssetPath(path))teamFail('ASSET_SOURCE_PATH_INVALID');
 const contentPath=root.kind==='skill'?`${path}/SKILL.md`:path,raw=await bytes(root,contentPath),text=raw.toString('utf8');if(raw.length>256*1024)teamFail('ASSET_CONTENT_LIMIT');
 const meta=metadata(text,root.kind);if(copy&&meta.unsupported)teamFail('SKILL_METADATA_UNSUPPORTED');
 const resources:AssetResource[]=[];let total=raw.length;
 async function tree(sub:string){const {target}=await safe(root,sub,true);const entries=await readdir(target,{withFileTypes:true});entries.sort((a,b)=>a.name.localeCompare(b.name));
  for(const e of entries){const full=`${sub}/${e.name}`;if(e.isSymbolicLink())teamFail('LINKED_ASSET_SOURCE');if(e.isDirectory()){await tree(full);continue;}if(full===contentPath)continue;
   if(resources.length>=100||sensitivePath(full))teamFail(sensitivePath(full)?'SENSITIVE_ASSET_RESOURCE':'ASSET_RESOURCE_LIMIT');const data=await bytes(root,full);total+=data.length;if(total>5*1024*1024)teamFail('ASSET_RESOURCE_LIMIT');
   if(copy&&safePersistedText(data.toString('utf8'))!==data.toString('utf8'))teamFail('SENSITIVE_ASSET_CONTENT');
   resources.push({path:relative(path,full).replaceAll('\\','/'),hash:createHash('sha256').update(data).digest('hex'),byteSize:data.length,...(copy?{base64:data.toString('base64')}:{})});
  }
 }
 if(root.kind==='skill'&&(details||copy))await tree(path);
 const content=safePersistedText(text);if(copy&&content!==text)teamFail('SENSITIVE_ASSET_CONTENT');
 const source:AssetSource={rootId:root.id,relativePath:path,hash:createHash('sha256').update(raw).digest('hex'),origin:root.scope,license:meta.license};
 return {id:`source:${root.id}:${path}`,kind:root.kind,name:meta.name||path,description:safePersistedText(meta.description),scope:root.scope,source,content,resources,dependencies:[],revision:0,effectiveVersion:null,loadedVersion:null,loadedCoverage:'unavailable',archived:false,deleted:false,versions:[],redacted:content!==text,management:'source_read_only'};
}
export async function sourceCatalog(roots:AssetRoot[]){const assets:AssetProfile[]=[],scopes:AssetScope[]=[];
 for(const root of roots){let partial=false;try{const {target}=await safe(root,'',true);const names=(await readdir(target)).sort();if(names.length>128)partial=true;
  for(const name of names.slice(0,128)){if(root.kind==='agent'&&!/^[\w.-]+\.toml$/.test(name))continue;if(root.kind==='skill'&&!/^[\w.-]+$/.test(name))continue;try{assets.push({...await sourceAsset(root,name,false,false),content:''});}catch{partial=true;}}
  scopes.push({id:root.id,scope:root.scope,availability:'available',...(partial?{reason:'partial_source_inventory'}:{})});
 }catch{scopes.push({id:root.id,scope:root.scope,availability:'unavailable',reason:'source_directory_unavailable'});}}
 if(!roots.some(r=>r.scope==='global'))scopes.push({id:'global',scope:'global',availability:'unavailable',reason:'not_configured'});if(!roots.some(r=>r.scope==='vendor'))scopes.push({id:'vendor',scope:'vendor',availability:'unavailable',reason:'not_configured'});
 return {assets,scopes,coverage:scopes.some(s=>s.availability==='unavailable'||s.reason)?'partial' as const:'complete' as const};
}
