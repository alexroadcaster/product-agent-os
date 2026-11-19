import {createHash} from 'node:crypto';
import {recipeScopeHash} from '../execution-recipes/contract.mts';
import {assertCurrentSourceProject,inventoryScopeFingerprint} from '../project-inventory/scope.mts';
import {captureTaskFiles,type FileSnapshot} from '../runtime/app-agent-files.mts';
import type {LocalStore,Project,StoredEntity} from '../storage/local-store.mts';
import type {MethodologyEvidenceView,MethodologyTechnicalState} from '../../../../packages/contracts/methodology-workspace.ts';

export type MethodologyCheckPin = {
  criterionId:string; taskSpecRevision:string; sourceRevision:string; inputDigest:string;
  environmentRevision:string; profileId:string; authorityEpoch:number;
};
export type MethodologyCheck = MethodologyCheckPin & {observation:'pending'|'current'|'stale'};
type Receipt = {runId:string;operationId:string;route:'native_command_broker';inputDigest:string;environmentRevision:string};

const hash=(data:unknown)=>createHash('sha256').update(JSON.stringify(data)).digest('hex');
const environmentRevision=(profileId:string)=>hash(['native_command_broker',process.platform,process.arch,process.version,profileId]);
function fail(code:string):never { throw Object.assign(new Error(code),{code}); }

export function methodologySourceRevision(project:Project,files:readonly FileSnapshot[]):string|null {
  if (!files.length || files.every(file=>file.kind==='missing') || files.some(file=>file.kind==='excluded')) return null;
  return hash([inventoryScopeFingerprint(project),files.map(file=>[file.path,file.kind,file.sha256??null])]);
}

export function methodologyCriteria(task:StoredEntity):string[] {
  const criteria=task.data.acceptanceCriteria;
  if (!Array.isArray(criteria) || criteria.length>200 || criteria.some(value=>typeof value!=='string'||!value.trim()))
    fail('METHODOLOGY_CRITERIA_INVALID');
  return criteria;
}

export async function currentMethodologyScope(store:LocalStore,projectId:string,taskId:string) {
  const {project,task}=await store.runtimeFileScope(projectId,taskId);
  if (!project || !task || task.kind!=='task' || task.deleted) fail('TASK_NOT_FOUND');
  const files=Array.isArray(task.data.files)?task.data.files:[];
  const sourceRevision=methodologySourceRevision(project,await captureTaskFiles(project,files));
  await assertCurrentSourceProject(store,project,task);
  return {project,task,sourceRevision,taskSpecRevision:recipeScopeHash(task.data)};
}

export async function pinMethodologyCheck(store:LocalStore,projectId:string,taskId:string,criterionId:unknown,
  argv:readonly string[],profileId:string):Promise<MethodologyCheckPin> {
  if (typeof criterionId!=='string'||!/^AC-[1-9][0-9]{0,2}$/.test(criterionId)) fail('METHODOLOGY_CRITERION_INVALID');
  const scope=await currentMethodologyScope(store,projectId,taskId);
  if (Number(criterionId.slice(3))>methodologyCriteria(scope.task).length) fail('METHODOLOGY_CRITERION_INVALID');
  if (!scope.sourceRevision) fail('METHODOLOGY_SOURCE_UNAVAILABLE');
  const {sourceRevision,taskSpecRevision}=scope,authorityEpoch=scope.project.authorityEpoch;
  const environment=environmentRevision(profileId);
  return {criterionId,taskSpecRevision,sourceRevision,environmentRevision:environment,profileId,authorityEpoch,
    inputDigest:hash([projectId,taskId,criterionId,taskSpecRevision,sourceRevision,environment,authorityEpoch,argv])};
}

export type MethodologyObservation = {runId:string;operationId:string;decision:string|null;state:string;exitCode:number|null;criterionCheck:MethodologyCheck};

/** Read only authenticated broker results. The owner-reviewed link defines applicability, while the receipt supplies the outcome. */
export async function readMethodologyEvidence(store:LocalStore,projectId:string,taskId:string,expectedRevision?:number,
  activeProfileId?:string):Promise<MethodologyEvidenceView> {
  const scope=await currentMethodologyScope(store,projectId,taskId);
  if(expectedRevision!==undefined&&scope.task.revision!==expectedRevision)fail('METHODOLOGY_TASK_STALE');
  const {observations,dispositions}=await store.methodologyEvidenceRows(projectId,taskId);
  const outcomes=new Map<string,{technical:MethodologyTechnicalState;receipt:Receipt}>();
  for (const op of observations.slice(0,200)) {
    const pin=op.criterionCheck;
    if (!pin || outcomes.has(pin.criterionId)) continue;
    const outdated=pin.authorityEpoch!==scope.project.authorityEpoch||pin.taskSpecRevision!==scope.taskSpecRevision
      || pin.sourceRevision!==scope.sourceRevision||pin.environmentRevision!==environmentRevision(activeProfileId??pin.profileId);
    let technical:MethodologyTechnicalState='partial';
    if (outdated||pin.observation==='stale') technical='stale';
    else if (pin.observation==='current'&&op.decision==='accept'&&op.state==='completed'&&Number.isSafeInteger(op.exitCode))
      technical=op.exitCode===0?'passed':'failed';
    outcomes.set(pin.criterionId,{technical,receipt:{runId:op.runId,operationId:op.operationId,route:'native_command_broker',
      inputDigest:pin.inputDigest,environmentRevision:pin.environmentRevision}});
  }
  const human=dispositions.slice(0,100).find(row=>row.taskSpecRevision===scope.taskSpecRevision);
  const humanAcceptance=human?.accepted===true?'accepted':human?.accepted===false?'declined':'not_observed';
  const criteria=methodologyCriteria(scope.task).map((criterion,index)=>{
    const id=`AC-${index+1}`,observed=outcomes.get(id);
    return {id,criterion,owner:'task-owner',technical:observed?.technical??'missing',receipt:observed?.receipt??null,
      human:humanAcceptance==='accepted'?'accepted' as const:'not_observed' as const};
  });
  const pending=observations.find(row=>['dispatching','recovery_required'].includes(row.state));
  await assertCurrentSourceProject(store,scope.project,scope.task);
  return {schemaVersion:'paos_methodology_evidence_v1',projectId,taskId,taskRevision:scope.task.revision,
    taskSpecRevision:scope.taskSpecRevision,sourceRevision:scope.sourceRevision,criteria,humanAcceptance,
    releaseAcceptance:'not_evaluated',coverage:observations.length>200||dispositions.length>100?'bounded_history':'observed_history',
    recovery:pending?{state:pending.state==='recovery_required'?'reconcile_required':'observation_pending',
      runId:pending.runId,operationId:pending.operationId}:null};
}
