import {randomUUID,createHash} from 'node:crypto';
import type {LocalStore} from '../storage/local-store.mts';
import {validateProposal,teamFail} from './contract.mts';
import {safePersistedText} from '../redaction/persisted.mts';
import type {TeamService} from './service.mts';
export async function startTeamGeneration(store:LocalStore,runtime:{dispatch(action:string,input:Record<string,unknown>):Promise<unknown>;snapshot(input:Record<string,unknown>):Promise<unknown>}|undefined,projectId:string,value:any){
 if(!runtime)teamFail('APP_GENERATION_UNAVAILABLE');if(typeof value.description!=='string'||!value.description.trim()||value.description.length>20000)teamFail('TEAM_GENERATION_INPUT_INVALID');
 const status=await runtime.snapshot({projectId,sessionId:value.sessionId}) as any;if(status.route!=='codex_app_agent')teamFail('APP_GENERATION_UNAVAILABLE');
 const input=safePersistedText(value.description);const result=await runtime.dispatch('team-proposal',{projectId,sessionId:value.sessionId,bindingId:value.bindingId,clientMessageId:typeof value.idempotencyKey==='string'?value.idempotencyKey:randomUUID(),input,...(value.targetAssetId?{targetAssetId:value.targetAssetId}:{})}) as any;
 const row=await store.get(projectId,result.id);if(!row?.data.appAgentRun||(row.data.appAgentRun as any).purpose!=='team_proposal')teamFail('APP_GENERATION_UNAVAILABLE');
 return {id:result.id,sessionId:result.sessionId,runId:result.id,purpose:'team_proposal',state:result.state};
}
export async function teamGenerationResult(store:LocalStore,team:TeamService,projectId:string,id:string){
 const row=await store.get(projectId,id),job=row?.data.appAgentRun as any;if(!job||job.purpose!=='team_proposal'||job.projectId!==projectId)teamFail('TEAM_GENERATION_NOT_FOUND');
 const planningRun={id,sessionId:job.sessionId,runId:id,purpose:'team_proposal'},base={state:job.state,planningRun};if(job.state!=='completed')return base;
 const message=await store.get(projectId,`app-assistant-${createHash('sha256').update(id).digest('hex')}`);if(!message||message.data.runId!==id)return {...base,validationErrors:['result_message_unavailable']};
 try{const parsed=JSON.parse(message.body);if(typeof parsed.clarification==='string')return {...base,clarification:safePersistedText(parsed.clarification)};
  const proposal=validateProposal(parsed);if(proposal.kind!=='agent'||!['create','update','archive','delete'].includes(proposal.action))teamFail('TEAM_GENERATION_RESULT_INVALID');
  const context=job.proposalContext;if(proposal.action!=='create'&&(!context?.targetAssetId||context.targetAssetId!==proposal.assetId))return {...base,clarification:'Select the exact existing agent target before generating this change.'};
  const expectedRevision=proposal.action==='create'?0:context.targetRevision;const preview=await team.preview(projectId,{proposal,expectedRevision});return {...base,proposal:preview.proposal,expectedRevision,preview};
 }catch(error){return {...base,validationErrors:[(error as any).code??'TEAM_GENERATION_JSON_INVALID']};}
}
