import type {LocalStore} from '../storage/local-store.mts';
import type {AssetProposal,AssetProfile,TeamRegistry,AssetPin} from '../../../../packages/contracts/team/assets.ts';
import {teamId,teamFail,previewAsset,validateProposal} from './contract.mts';
import {sourceCatalog,sourceAsset,projectAssetRoots,type AssetRoot} from './sources.mts';
import {safeVisibleValue} from '../redaction/persisted.mts';
import {workflowCategory} from '../../../../packages/contracts/workflows/helpers.ts';
import {taskManagerSnapshot} from '../task-manager/service.mts';
import {bindProject} from '../adapters/project-sources.ts';
export function createTeamService(store:LocalStore,configuredRoots:AssetRoot[]=[]){
 async function roots(projectId:string){const p=await store.project(projectId);if(!p)teamFail('PROJECT_NOT_FOUND');const binding=await bindProject(projectId,p.canonicalRoot);if(binding.directoryIdentity!==p.rootIdentity)teamFail('PROJECT_ROOT_UNAVAILABLE');return [...projectAssetRoots(binding.workspaceRoot),...configuredRoots];}
 async function registry(projectId:string):Promise<TeamRegistry>{return (await store.get(projectId,teamId))?.data as unknown as TeamRegistry??{category:'team_registry',assets:[]};}
 async function runs(projectId:string){return (await store.projectEntities(projectId)).filter(r=>r.kind==='run').map(r=>({entity:r,run:(r.data.appAgentRun??r.data.runtimeRun) as any}));}
 async function preview(projectId:string,input:any){const reg=await registry(projectId),active=(await runs(projectId)).filter(({entity})=>!['completed','failed','interrupted'].includes(entity.status)).map(({entity,run})=>({id:entity.id,assetIds:(run?.assetPins??run?.taskContext?.assetPins??[]).map((p:any)=>p.assetId)}));
  const available=(await catalog(projectId)).assets;const p=previewAsset(reg,input.proposal,input.expectedRevision,active,available);
  for(const dep of p.proposal.dependencies)if(!available.some(a=>a.id===dep&&!a.archived&&!a.deleted))teamFail('ASSET_DEPENDENCY_UNAVAILABLE');return p;
 }
 async function catalog(projectId:string){const sources=await sourceCatalog(await roots(projectId)),managed=(await registry(projectId)).assets;return {...sources,assets:[...sources.assets,...safeVisibleValue(managed)].map(({content,resources,versions,...metadata})=>({...metadata,versionHash:versions.at(-1)?.hash??metadata.source?.hash??null}))};}
 async function profile(projectId:string,id:string){const managed=(await registry(projectId)).assets.find(a=>a.id===id);if(managed){const observedPins=(await runs(projectId)).flatMap(({entity,run})=>(run?.assetPins??run?.taskContext?.assetPins??[]).filter((p:any)=>p.assetId===id).map((p:any)=>({version:p.version,hash:p.hash,runId:entity.id,sessionId:run.sessionId,status:entity.status})));return {...safeVisibleValue(managed),observedPins};}
  if(!id.startsWith('source:'))teamFail('TEAM_ASSET_NOT_FOUND');const sourceRoots=await roots(projectId);const root=sourceRoots.find(r=>id.startsWith(`source:${r.id}:`));if(!root)teamFail('TEAM_ASSET_NOT_FOUND');return sourceAsset(root,id.slice(`source:${root.id}:`.length));
 }
 async function pins(projectId:string,ids:readonly string[]):Promise<AssetPin[]>{const result:AssetPin[]=[];const visited=new Set<string>(),visiting=new Set<string>();
  async function visit(id:string){if(visiting.has(id))teamFail('ASSET_DEPENDENCY_CYCLE');if(visited.has(id))return;visiting.add(id);let a=await profile(projectId,id);if(a.deleted||a.archived)teamFail('ASSET_ASSIGNMENT_UNAVAILABLE');
   if(a.management==='source_read_only'){const root=(await roots(projectId)).find(r=>r.id===a.source?.rootId);if(!root)teamFail('ASSET_SOURCE_ROOT_INVALID');a=await sourceAsset(root,a.source!.relativePath,true);}
   const resources=[];for(const r of a.resources)resources.push(r.base64!==undefined?r:{...r,base64:Buffer.from(await store.readBlob(projectId,r.blobId!)).toString('base64')});
   result.push({assetId:a.id,kind:a.kind,version:a.effectiveVersion,hash:a.versions.at(-1)?.hash??a.source!.hash,content:a.content,source:a.source,resources,requestedModel:/^model\s*=\s*["']([^"']+)["']/m.exec(a.content)?.[1]??null,requestedEffort:/^model_reasoning_effort\s*=\s*["']([^"']+)["']/m.exec(a.content)?.[1]??null,observedModel:null,observedEffort:null});
   for(const dep of a.dependencies)await visit(dep);visiting.delete(id);visited.add(id);
  }for(const id of ids)await visit(id);if(Buffer.byteLength(JSON.stringify(result))>8*1024*1024)teamFail('ASSET_PIN_LIMIT');return result;
 }
 async function assignmentPins(projectId:string,ids:readonly string[]){const available=(await catalog(projectId)).assets;const known=ids.filter(id=>available.some(a=>a.id===id));if(known.filter(id=>available.find(a=>a.id===id)?.kind==='agent').length>1)teamFail('AGENT_SELECTION_REQUIRED');return pins(projectId,known);}
 return {catalog,profile,preview,pins,assignmentPins,
  async apply(projectId:string,actorId:string,input:any){
   if(typeof input.idempotencyKey!=='string'||!input.idempotencyKey||!Number.isSafeInteger(input.epoch))teamFail('TEAM_APPLY_INPUT_INVALID');
   if(await store.receipt(projectId,input.idempotencyKey))return store.teamApply({projectId,actorId,epoch:input.epoch,idempotencyKey:input.idempotencyKey,expectedRevision:input.expectedRevision,previewDigest:input.previewDigest,proposal:validateProposal(input.proposal)});
   const p=await preview(projectId,input);if(p.previewDigest!==input.previewDigest)teamFail('TEAM_PREVIEW_STALE');const uploaded:string[]=[];
   try{const resources=[];for(const r of p.proposal.resources??[]){if(r.base64!==undefined){const blob=await store.putBlob(projectId,Buffer.from(r.base64,'base64'));uploaded.push(blob.id);resources.push({path:r.path,hash:r.hash,byteSize:r.byteSize,blobId:blob.id});}else resources.push(r);}
    return await store.teamApply({projectId,actorId,epoch:input.epoch,idempotencyKey:input.idempotencyKey,expectedRevision:input.expectedRevision,previewDigest:input.previewDigest,proposal:{...p.proposal,resources}});
   }catch(error){for(const id of uploaded)await store.discardUnreferencedBlob(projectId,id);throw error;}
  },
  async discovery(projectId:string,q:string){const result=await catalog(projectId);return {candidates:result.assets.filter(a=>a.kind==='skill'&&`${a.name} ${a.description}`.toLowerCase().includes(q.toLowerCase())),scopes:result.scopes,coverage:result.coverage,remote:{availability:'unavailable',reason:'remote_discovery_adapter_not_configured'}};},
  async sourcePreview(projectId:string,input:any){const root=(await roots(projectId)).find(r=>r.id===input.sourceRootId&&r.kind==='skill');if(!root)teamFail('ASSET_SOURCE_ROOT_INVALID');const candidate=await sourceAsset(root,input.relativePath,true);
   const proposal:AssetProposal={kind:'skill',action:'create',name:candidate.name,description:candidate.description,content:candidate.content,dependencies:[],resources:candidate.resources,source:candidate.source,reason:'Create project-owned source copy'};
   return {candidate,...await preview(projectId,{proposal,expectedRevision:0})};},
  async copyPreview(projectId:string,id:string){const original=await profile(projectId,id);let candidate=original;
   if(original.management==='source_read_only'){const root=(await roots(projectId)).find(r=>r.id===original.source?.rootId);if(!root)teamFail('ASSET_SOURCE_ROOT_INVALID');candidate=await sourceAsset(root,original.source!.relativePath,true);}
   const proposal:AssetProposal={kind:candidate.kind,action:'create',name:`${candidate.name} copy`,description:candidate.description,content:candidate.content,dependencies:candidate.dependencies,resources:candidate.resources,source:candidate.management==='source_read_only'?candidate.source:{rootId:teamId,relativePath:candidate.id,hash:candidate.versions.at(-1)!.hash,origin:'managed_copy',license:candidate.source?.license??null},reason:'Create project-owned copy'};
   return {candidate,...await preview(projectId,{proposal,expectedRevision:0})};},
  async resource(projectId:string,id:string,path:string,version?:number){const a=await profile(projectId,id);const resources=version?a.versions.find(v=>v.version===version)?.resources:a.resources;const r=resources?.find(r=>r.path===path);if(!r?.blobId)teamFail('ASSET_RESOURCE_UNAVAILABLE');return {resource:r,bytes:await store.readBlob(projectId,r.blobId)};},
  async exportAsset(projectId:string,id:string){const a=await profile(projectId,id);if(a.management!=='paos_managed')teamFail('SOURCE_READONLY');const resources=[];for(const r of a.resources)resources.push({...r,base64:Buffer.from(await store.readBlob(projectId,r.blobId!)).toString('base64')});return {format:'paos_managed_asset_staging_v1',activation:'manual_native_staging_required',asset:{...a,resources}};},
  async validateWorkflowReferences(projectId:string,definition:any){const available=(await catalog(projectId)).assets;for(const recipe of definition.recipes??[])for(const step of recipe.steps??[])for(const id of step.skills??[]){const a=available.find(a=>a.id===id&&!a.archived&&!a.deleted&&a.kind==='skill');if(!a)teamFail('WORKFLOW_SKILL_REFERENCE_INVALID');const pin=step.skillVersions?.[id];if(pin){const profile=await this.profile(projectId,id);if(!(profile.management==='paos_managed'?profile.versions.some(v=>String(v.version)===pin.replace(/^v/,'')):pin===profile.source?.hash))teamFail('WORKFLOW_SKILL_VERSION_INVALID');}}},
  async metrics(projectId:string,from:string,to:string){if(!/^\d{4}-\d{2}-\d{2}T/.test(from)||!Number.isFinite(Date.parse(from))||!Number.isFinite(Date.parse(to))||Date.parse(from)>=Date.parse(to))teamFail('METRICS_PERIOD_INVALID');const records=await runs(projectId),snapshot=await taskManagerSnapshot(store,projectId),groups=new Map<string,any>();let denominator=0;
   for(const {entity,run}of records){const timeline=Array.isArray(entity.data.timeline)?entity.data.timeline as any[]:[];const started=timeline.filter(e=>e.kind==='interval_started').map(e=>e.atMs);const at=typeof run?.observedStartedAt==='string'?Date.parse(run.observedStartedAt):started.length?Math.min(...started):null;if(at===null||at<Date.parse(from)||at>=Date.parse(to))continue;denominator++;
    const ids=(run?.assetPins??run?.taskContext?.assetPins??[]).filter((p:any)=>p.kind==='agent').map((p:any)=>p.assetId);for(const id of new Set<string>(ids)){let g=groups.get(id);if(!g){g={agentId:id,startedRuns:0,outcomes:{completed:0,failed:0,cancelled:0,needsDecision:0,acceptedTasks:0},durationSeconds:null,tokenCount:null,cost:null,taskIds:[],runIds:[],sessionIds:[]};groups.set(id,g);}g.startedRuns++;g.runIds.push(entity.id);const taskId=run.taskContext?.taskId??run.taskId;if(taskId&&!g.taskIds.includes(taskId))g.taskIds.push(taskId);if(run.sessionId&&!g.sessionIds.includes(run.sessionId))g.sessionIds.push(run.sessionId);if(entity.status==='completed')g.outcomes.completed++;else if(entity.status==='failed')g.outcomes.failed++;else if(entity.status==='interrupted')g.outcomes.cancelled++;else if(entity.status==='awaiting_approval')g.outcomes.needsDecision++;
     const task=snapshot.tasks.find(t=>t.id===taskId);if(task&&workflowCategory(snapshot.workflows,task.data as any)==='done')g.outcomes.acceptedTasks=new Set(g.taskIds.filter((tid:string)=>{const t=snapshot.tasks.find(t=>t.id===tid);return t&&workflowCategory(snapshot.workflows,t.data as any)==='done';})).size;
    }
   }return {period:{from,to},denominator:records.length?denominator:null,source:'local_observed_run_start_events',coverage:{status:'partial',reasons:['host_history_not_exposed','duration_token_cost_telemetry_unavailable']},agents:[...groups.values()]};
  }
 };
}
export type TeamService=ReturnType<typeof createTeamService>;
