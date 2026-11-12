import {createHash} from 'node:crypto';
import type {LocalStore} from '../storage/local-store.mts';
import type {AssetProposal} from '../../../../packages/contracts/team/assets.ts';
import type {TeamService} from './service.mts';
import {validateProposal,teamFail,digest} from './contract.mts';
import {safePersistedText} from '../redaction/persisted.mts';
import {bindProject,readProjectSource} from '../adapters/project-sources.ts';
type Runtime={snapshot(input:Record<string,unknown>):Promise<unknown>;dispatch(action:string,input:Record<string,unknown>):Promise<unknown>};
type RequirementRef={id:string;revision:string;relativePath:string|null;startLine:number|null;endLine:number|null;excerpt:string};
const hash=(s:string)=>createHash('sha256').update(s).digest('hex');
function generatedSkill(value:unknown):AssetProposal {
 const proposal=validateProposal(value);if(proposal.kind!=='skill'||proposal.action!=='create'||proposal.assetId||proposal.source||(proposal.resources?.length??0)>0)teamFail('SKILL_GENERATION_RESULT_INVALID');
 const header=/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(proposal.content);
 if(!header)teamFail('SKILL_FRONTMATTER_INVALID');
 for(const field of ['name','description']){const values=header[1].split(/\r?\n/).filter(line=>line.startsWith(field+':'));if(values.length!==1||!values[0].slice(field.length+1).trim().replace(/^["']|["']$/g,'').trim()||/^[>|&*!\[{]/.test(values[0].slice(field.length+1).trim()))teamFail('SKILL_FRONTMATTER_INVALID');}
 return proposal;
}
/** Skill recommendations are planning proposals. The existing transactional team writer owns Apply and its stable retry receipt. */
export function createSkillGeneration(store:LocalStore,team:TeamService,runtime?:Runtime){
 const pendingStarts=new Map<string,Promise<any>>();
 async function requirements(projectId:string,input:any){
  if(!input||!['requirements','description'].includes(input.mode))teamFail('SKILL_GENERATION_INPUT_INVALID');
  const description=typeof input.description==='string'?safePersistedText(input.description.trim()):'';if(description.length>12000)teamFail('SKILL_GENERATION_INPUT_INVALID');
  let refs:RequirementRef[]=[];
  if(input.mode==='requirements'){
   const project=await store.project(projectId);if(!project)teamFail('PROJECT_NOT_FOUND');const binding=await bindProject(projectId,project.canonicalRoot);if(binding.directoryIdentity!==project.rootIdentity)teamFail('PROJECT_ROOT_UNAVAILABLE');
   const source=await readProjectSource(binding,'requirements');if(source.sha256!==input.expectedRevision)teamFail('REQUIREMENT_STALE');
   const lines=source.content.split(/\r?\n/),start=input.startLine??1,end=input.endLine??Math.min(lines.length,80);
   if(!Number.isSafeInteger(start)||!Number.isSafeInteger(end)||start<1||end<start||end>lines.length||end-start>=200)teamFail('REQUIREMENT_RANGE_INVALID');
   const excerpt=safePersistedText(lines.slice(start-1,end).join('\n'));if(Buffer.byteLength(excerpt)>16000)teamFail('REQUIREMENT_CONTEXT_LIMIT');if(excerpt.trim().length<16)teamFail('INSUFFICIENT_REQUIREMENTS');
   refs=[{id:`requirements:${start}-${end}`,relativePath:source.relativePath,revision:source.sha256,startLine:start,endLine:end,excerpt}];
  }else{if(description.length<8)teamFail('INSUFFICIENT_REQUIREMENTS');refs=[{id:'user-description',revision:hash(description),relativePath:null,startLine:null,endLine:null,excerpt:description}];}
  const request={mode:input.mode,description,...(input.mode==='requirements'?{expectedRevision:refs[0].revision,startLine:refs[0].startLine,endLine:refs[0].endLine}:{})};
  const generationKey=hash(JSON.stringify({projectId,request,refs}));return {generationKey,request,refs};
 }
 const applyKey=(key:string)=>'skill-generation-'+key;
 const generatedId=(projectId:string,key:string)=>`managed-${digest([projectId,applyKey(key)]).slice(0,32)}`;
 async function job(projectId:string,id:string){const row=await store.get(projectId,id),run=row?.data.appAgentRun as any;if(!run||run.projectId!==projectId||run.purpose!=='team_proposal'||run.proposalContext?.assetKind!=='skill'||!run.proposalContext.requirementContext)teamFail('SKILL_GENERATION_NOT_FOUND');return run;}
 async function result(projectId:string,id:string){
  const run=await job(projectId,id),context=run.proposalContext.requirementContext,base={id,runId:id,sessionId:run.sessionId,state:run.state,requirements:context.refs,generationKey:context.generationKey,applyKey:applyKey(context.generationKey)};
  const receipt=await store.receipt(projectId,base.applyKey);if(receipt){const asset=await team.profile(projectId,generatedId(projectId,context.generationKey));return {...base,state:'applied',assetId:asset.id,archived:asset.archived,deleted:asset.deleted};}
  try{const fresh=await requirements(projectId,context.request);if(fresh.generationKey!==context.generationKey)teamFail('REQUIREMENT_STALE');}catch(error){return {...base,state:'stale',validationErrors:[(error as any).code??'REQUIREMENT_UNAVAILABLE']};}
  if(run.state!=='completed')return base;
  const message=await store.get(projectId,'app-assistant-'+hash(id));if(!message||message.data.runId!==id)return {...base,state:'invalid',validationErrors:['RESULT_MESSAGE_UNAVAILABLE']};
  try{
   const raw=JSON.parse(message.body);if(typeof raw.clarification==='string')return {...base,state:'clarification',clarification:safePersistedText(raw.clarification)};
   if(raw.noGap===true&&typeof raw.reason==='string')return {...base,state:'covered',reason:safePersistedText(raw.reason)};
   const proposal=generatedSkill(raw);
   if(!Array.isArray(raw.requirementIds)||!raw.requirementIds.length||raw.requirementIds.some((ref:unknown)=>typeof ref!=='string'||!context.refs.some((r:RequirementRef)=>r.id===ref)))teamFail('SKILL_REQUIREMENT_REFERENCE_INVALID');
   const selected:RequirementRef[]=context.refs.filter((ref:RequirementRef)=>raw.requirementIds.includes(ref.id));
   const content=proposal.content+'\n\n## Requirement provenance\n\nGeneration request: '+context.generationKey+'\n'+selected.map(ref=>`- ${ref.id} (${ref.relativePath??'user description'}), sha256:${ref.revision}${ref.startLine?`, lines ${ref.startLine}-${ref.endLine}`:''}`).join('\n')+'\n';
   const normalized:AssetProposal={kind:'skill',action:'create',name:proposal.name,description:proposal.description,content,dependencies:proposal.dependencies,reason:proposal.reason};
   const existing=(await team.catalog(projectId)).assets.filter(a=>a.kind==='skill'&&!a.deleted&&a.name.trim().toLowerCase()===normalized.name.trim().toLowerCase());
   if(existing.length)return {...base,state:'duplicate_candidate',duplicates:existing.map(a=>({id:a.id,name:a.name,scope:a.scope})),proposal:normalized};
   const preview=await team.preview(projectId,{proposal:normalized,expectedRevision:0});return {...base,state:'completed',proposal:preview.proposal,preview,expectedRevision:0};
  }catch(error){return {...base,state:'invalid',validationErrors:[(error as any).code??'SKILL_GENERATION_JSON_INVALID']};}
 }
 return {requirements,
  async start(projectId:string,input:any){
   const context=await requirements(projectId,input),pendingKey=projectId+':'+context.generationKey;const inFlight=pendingStarts.get(pendingKey);if(inFlight)return inFlight;
   const operation=(async()=>{const rows=await store.projectEntities(projectId),prior=rows.filter(r=>r.kind==='run').map(r=>r.data.appAgentRun as any).find(r=>r?.proposalContext?.assetKind==='skill'&&r.proposalContext.requirementContext?.generationKey===context.generationKey);
   // Stable across bindings/restarts: a repeat returns the prior proposal/result instead of paying for another job.
   if(prior)return result(projectId,prior.id);
   if(!runtime)teamFail('APP_GENERATION_UNAVAILABLE');const state=await runtime.snapshot({projectId,sessionId:input.sessionId}) as any;if(state.route!=='codex_app_agent')teamFail('APP_GENERATION_UNAVAILABLE');
   const queued=await runtime.dispatch('team-proposal',{projectId,sessionId:input.sessionId,bindingId:input.bindingId,clientMessageId:'skill-'+context.generationKey,assetKind:'skill',requirementContext:context,input:'Recommend one missing project skill grounded only in the selected requirement references. Compare existing skill metadata. Return one editable SKILL.md create proposal with requirementIds, or {noGap:true,reason:string}, or {clarification:string}. Never apply or install. User request: '+context.request.description}) as any;
   return {id:queued.id,runId:queued.id,sessionId:queued.sessionId,state:queued.state,generationKey:context.generationKey,requirements:context.refs,applyKey:applyKey(context.generationKey)};})();pendingStarts.set(pendingKey,operation);try{return await operation;}finally{pendingStarts.delete(pendingKey);}
  },result,
  async apply(projectId:string,actorId:string,id:string,input:any){
   const current=await result(projectId,id);if(current.state==='applied')return team.apply(projectId,actorId,{...input,expectedRevision:0,idempotencyKey:current.applyKey});
   if(current.state!=='completed'||!('proposal' in current)||!current.proposal)teamFail(current.state==='stale'?'REQUIREMENT_STALE':'SKILL_PROPOSAL_NOT_APPLICABLE');
   generatedSkill(input.proposal);
   const reviewed=await team.preview(projectId,{proposal:input.proposal,expectedRevision:0});
   if(input.proposal.kind!=='skill'||input.proposal.action!=='create'||!input.proposal.content.includes('Generation request: '+current.generationKey))teamFail('SKILL_REQUIREMENT_REFERENCE_INVALID');
   if(reviewed.previewDigest!==input.previewDigest)teamFail('TEAM_PREVIEW_STALE');
   return team.apply(projectId,actorId,{...input,expectedRevision:0,idempotencyKey:current.applyKey});
  }
 };
}
