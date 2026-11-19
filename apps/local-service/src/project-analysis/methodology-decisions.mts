import {createHash} from 'node:crypto';
import type {MethodologyDecisionCommand,MethodologyDecisionEntry,MethodologyDecisionView} from '../../../../packages/contracts/methodology-workspace.ts';
import type {LocalStore,StoredEntity} from '../storage/local-store.mts';
import {inventoryScopeFingerprint} from '../project-inventory/scope.mts';
import {safePersistedText} from '../redaction/persisted.mts';
import {currentMethodologyScope,methodologyCriteria} from './methodology-evidence.mts';

const schema='paos_methodology_decision_record_v1';
const historyLimit=64;
const hash=(data:unknown)=>createHash('sha256').update(JSON.stringify(data)).digest('hex');
const decisionId=(projectId:string,taskId:string)=>'methodology-decision-'+hash([projectId,taskId]);
const dispositions=['use_recommendation','review_required','accepted_gap'];
type Entry=MethodologyDecisionEntry & {requestId:string;requestDigest:string};
type Decision={schemaVersion:typeof schema;category:'methodology_decision';taskId:string;history:Entry[]};
function fail(code:string):never { throw Object.assign(new Error(code),{code}); }

function readRow(row:StoredEntity|null,taskId:string):Decision|null {
  if(!row)return null;
  const data=row.data as Partial<Decision>;
  if(row.kind!=='settings'||data.category!=='methodology_decision'||data.schemaVersion!==schema||data.taskId!==taskId
    ||!Array.isArray(data.history)||data.history.length<1||data.history.length>historyLimit)return null;
  const valid=data.history.every(entry=>entry&&typeof entry.reason==='string'&&typeof entry.actorId==='string'
    &&typeof entry.observedAt==='string'&&typeof entry.scopeDigest==='string'&&typeof entry.requestId==='string'
    &&typeof entry.requestDigest==='string'&&Number.isSafeInteger(entry.taskRevision)&&dispositions.includes(entry.disposition)
    &&(entry.criterionId===null||typeof entry.criterionId==='string'));
  return valid?data as Decision:null;
}

function decodeInput(raw:Record<string,unknown>):MethodologyDecisionCommand {
  const {expectedRevision,taskRevision,scopeDigest,idempotencyKey,disposition,criterionId,reason}=raw;
  if(Object.keys(raw).some(key=>!['expectedRevision','taskRevision','scopeDigest','idempotencyKey','disposition','criterionId','reason'].includes(key))
    ||typeof expectedRevision!=='number'||!Number.isSafeInteger(expectedRevision)||expectedRevision<0
    ||typeof taskRevision!=='number'||!Number.isSafeInteger(taskRevision)||taskRevision<1
    ||typeof scopeDigest!=='string'||!(/^[a-f0-9]{64}$/.test(scopeDigest))
    ||typeof idempotencyKey!=='string'||!(/^[a-zA-Z0-9_-]{1,128}$/.test(idempotencyKey))
    ||typeof disposition!=='string'||!dispositions.includes(disposition)
    ||(disposition==='accepted_gap'?typeof criterionId!=='string'||!/^AC-[1-9][0-9]{0,2}$/.test(criterionId):criterionId!==null)
    ||typeof reason!=='string'||!reason.trim()||reason.length>800||/[\u0000-\u001f]/.test(reason)||safePersistedText(reason)!==reason)
    fail('METHODOLOGY_DECISION_INVALID');
  return {expectedRevision,taskRevision,scopeDigest,idempotencyKey,disposition,criterionId,reason:reason.trim()} as MethodologyDecisionCommand;
}

export function createMethodologyDecisions(store:LocalStore) {
  async function observed(projectId:string,taskId:string){
    const id=decisionId(projectId,taskId);
    const [scope,row,freshness]=await Promise.all([
      currentMethodologyScope(store,projectId,taskId),store.get(projectId,id),store.projectFreshness(projectId),
    ]);
    const decision=readRow(row,taskId),inventoryScope=inventoryScopeFingerprint(scope.project);
    const scopeDigest=hash([projectId,taskId,scope.task.revision,scope.taskSpecRevision,scope.sourceRevision,
      scope.project.authorityEpoch,inventoryScope,freshness.generation]);
    const latest=decision?.history.at(-1);
    const status=!row?'unknown':!decision?'unsupported':latest?.scopeDigest===scopeDigest?'current':'stale';
    const history=decision?.history.map(({requestId,requestDigest,...entry})=>entry)??[];
    const view:MethodologyDecisionView={schemaVersion:schema,taskId,taskRevision:scope.task.revision,
      scopeDigest,revision:row?.revision??0,status,history};
    return {id,scope,freshness,inventoryScope,decision,view};
  }
  return {
    get:async(projectId:string,taskId:string)=>(await observed(projectId,taskId)).view,
    async save(projectId:string,taskId:string,actorId:string,raw:Record<string,unknown>){
      const input=decodeInput(raw);
      const state=await observed(projectId,taskId),{view,scope}=state;
      if(view.status==='unsupported')fail('METHODOLOGY_DECISION_UNSUPPORTED');
      const requestId=hash([actorId,input.idempotencyKey]);
      const requestDigest=hash(input),prior=state.decision?.history.find(entry=>entry.requestId===requestId);
      if(prior){if(prior.requestDigest!==requestDigest)fail('IDEMPOTENCY_CONFLICT');return view;}
      if(input.expectedRevision!==view.revision||input.taskRevision!==view.taskRevision||input.scopeDigest!==view.scopeDigest)
        fail('METHODOLOGY_DECISION_STALE');
      if(input.criterionId&&Number(input.criterionId.slice(3))>methodologyCriteria(scope.task).length)
        fail('METHODOLOGY_DECISION_INVALID');
      const history=state.decision?.history??[];
      if(history.length>=historyLimit)fail('METHODOLOGY_DECISION_HISTORY_LIMIT');
      const entry:Entry={taskRevision:input.taskRevision,scopeDigest:input.scopeDigest,disposition:input.disposition,
        criterionId:input.criterionId,reason:input.reason,actorId,observedAt:new Date().toISOString(),requestId,requestDigest};
      await store.write({projectId,actorId,expectedAuthorityEpoch:scope.project.authorityEpoch,
        idempotencyKey:`methodology:${state.id}:${requestId}`,
        methodologyDecisionScope:{taskId,taskRevision:input.taskRevision,generation:state.freshness.generation,inventoryScope:state.inventoryScope},
        changes:[{expectedRevision:view.revision,entity:{id:state.id,kind:'settings',data:{
          category:'methodology_decision',schemaVersion:schema,taskId,history:[...history,entry],
        }}}]});
      return (await observed(projectId,taskId)).view;
    },
  };
}
