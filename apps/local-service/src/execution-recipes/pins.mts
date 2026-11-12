import type {LocalStore} from '../storage/local-store.mts';
import type {WorkflowRecipe} from '../../../../packages/contracts/workflows/workflow.ts';
import type {AssetPin,AssetProfile} from '../../../../packages/contracts/team/assets.ts';
import {projectAssetRoots,sourceAsset,type AssetRoot} from '../team/sources.mts';
import {createTeamService} from '../team/service.mts';
import {bindProject} from '../adapters/project-sources.ts';
import {createHash} from 'node:crypto';
import {safePersistedText} from '../redaction/persisted.mts';
function fail(code:string):never{throw Object.assign(new Error(code),{code});}
function freeze<T>(value:T):T{if(value&&typeof value==='object'){for(const child of Object.values(value))freeze(child);Object.freeze(value);}return value;}
/** Resolve once before dispatch. Explicit versions override unversioned dependency edges globally. */
export async function resolveRecipePins(store:LocalStore,projectId:string,steps:WorkflowRecipe['steps'],roleBindings:Record<string,string>,assetRoots:AssetRoot[]=[]):Promise<Record<string,AssetPin[]>> {
 if(!Array.isArray(steps)||!steps.length||steps.length>32||new Set(steps.map(s=>s.id)).size!==steps.length)fail('RECIPE_PIN_INPUT_INVALID');
 const team=createTeamService(store,assetRoots),explicit=new Map<string,string>(),kinds=new Map<string,'agent'|'skill'>();
 const normalize=(version:string)=>/^v?[1-9][0-9]*$/.test(version)?version.replace(/^v/,''):version;
 function request(id:string,version:string,kind:'agent'|'skill'){
  if(typeof id!=='string'||!id||typeof version!=='string'||!version)fail('RECIPE_PIN_INPUT_INVALID');
  const canonical=normalize(version);if(explicit.has(id)&&explicit.get(id)!==canonical)fail('RECIPE_ASSET_VERSION_CONFLICT');
  if(kinds.has(id)&&kinds.get(id)!==kind)fail('RECIPE_ASSET_KIND_INVALID');explicit.set(id,canonical);kinds.set(id,kind);
 }
 for(const step of steps){const role=Object.hasOwn(roleBindings,step.role)?roleBindings[step.role]:undefined;
  if(typeof role!=='string'||!role.trim())fail('RECIPE_ROLE_BINDING_REQUIRED');request(role,step.profileVersion,'agent');
  if(!Array.isArray(step.skills)||step.skills.length>16)fail('RECIPE_PIN_INPUT_INVALID');for(const id of step.skills)request(id,step.skillVersions?.[id],'skill');
 }
 const project=await store.project(projectId);if(!project)fail('PROJECT_NOT_FOUND');const binding=await bindProject(projectId,project.canonicalRoot);
 if(binding.directoryIdentity!==project.rootIdentity)fail('PROJECT_ROOT_UNAVAILABLE');const roots=[...projectAssetRoots(binding.workspaceRoot),...assetRoots];
 if(new Set(roots.map(r=>r.id)).size!==roots.length)fail('ASSET_SOURCE_ROOT_INVALID');
 const resolved=new Map<string,{pin:AssetPin;dependencies:string[]}>(),visiting=new Set<string>();let bytes=0;
 async function visit(id:string):Promise<void>{
  if(visiting.has(id))fail('ASSET_DEPENDENCY_CYCLE');if(resolved.has(id))return;
  if(resolved.size+visiting.size>=256)fail('ASSET_PIN_LIMIT');visiting.add(id);
  let profile:AssetProfile=await team.profile(projectId,id);if(profile.archived||profile.deleted)fail('ASSET_ASSIGNMENT_UNAVAILABLE');if(profile.redacted)fail('SENSITIVE_ASSET_CONTENT');
  if(kinds.has(id)&&profile.kind!==kinds.get(id))fail('RECIPE_ASSET_KIND_INVALID');
  const version=explicit.get(id);let content=profile.content,resources=profile.resources,dependencies=profile.dependencies,source=profile.source,pinVersion=profile.effectiveVersion,hash='';
  if(profile.management==='source_read_only'){
   const root=roots.find(r=>r.id===profile.source?.rootId);if(!root)fail('ASSET_SOURCE_ROOT_INVALID');
   profile=await sourceAsset(root,profile.source!.relativePath,true);hash=profile.source!.hash;
   if(version!==undefined&&version!==hash)fail('RECIPE_ASSET_VERSION_UNAVAILABLE');
   ({content,resources,dependencies,source}=profile);pinVersion=null;
  }else{
   const selected=profile.versions.find(v=>String(v.version)===(version??String(profile.effectiveVersion)));
   if(!selected)fail('RECIPE_ASSET_VERSION_UNAVAILABLE');({content,resources,dependencies,source,hash}=selected);pinVersion=selected.version;
  }
  if(safePersistedText(content)!==content)fail('SENSITIVE_ASSET_CONTENT');
  const copied=[];for(const resource of resources){
   if(!resource.base64&&!resource.blobId&&resource.byteSize!==0)fail('ASSET_RESOURCE_UNAVAILABLE');
   const raw=resource.base64!==undefined?Buffer.from(resource.base64,'base64'):resource.blobId?Buffer.from(await store.readBlob(projectId,resource.blobId)):Buffer.alloc(0);
   if(raw.length!==resource.byteSize||createHash('sha256').update(raw).digest('hex')!==resource.hash)fail('ASSET_RESOURCE_INVALID');
   if(safePersistedText(raw.toString('utf8'))!==raw.toString('utf8'))fail('SENSITIVE_ASSET_CONTENT');
   copied.push({...resource,base64:raw.toString('base64')});
  }
  const pin:AssetPin={assetId:id,kind:profile.kind,version:pinVersion,hash,content,source,resources:copied,
   requestedModel:/^model\s*=\s*["']([^"']+)["']/m.exec(content)?.[1]??null,requestedEffort:/^model_reasoning_effort\s*=\s*["']([^"']+)["']/m.exec(content)?.[1]??null,observedModel:null,observedEffort:null};
  bytes+=Buffer.byteLength(JSON.stringify(pin));if(bytes>8*1024*1024)fail('ASSET_PIN_LIMIT');
  for(const dependency of dependencies)await visit(dependency);resolved.set(id,{pin,dependencies:[...dependencies]});visiting.delete(id);
 }
 for(const id of explicit.keys())await visit(id);
 const result:Record<string,AssetPin[]>=Object.create(null);
 for(const step of steps){const seen=new Set<string>(),pins:AssetPin[]=[];function collect(id:string){if(seen.has(id))return;seen.add(id);const entry=resolved.get(id)!;pins.push(entry.pin);for(const dep of entry.dependencies)collect(dep);}collect(roleBindings[step.role]);for(const skill of step.skills)collect(skill);result[step.id]=pins;}
 if(Buffer.byteLength(JSON.stringify(result))>8*1024*1024)fail('ASSET_PIN_LIMIT');return freeze(result);
}
