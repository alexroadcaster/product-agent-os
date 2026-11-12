import { decodeM1TaskProfile } from '../../../apps/local-service/src/tasks/task-profile.ts';
import type { M1TaskProfile, M1TaskStatus } from '../tasks/m1-task-profile.ts';

export const ISSUE_TYPES = ['epic','task','bug','user_story','sub_task'] as const;
export const DEFAULT_COMPONENTS = ['BackEnd','FrontEnd','DB','RAG','LLM','Design','Marketing','Integrations','DevOps','QA','Analytic'];
export const STATUS_COLUMNS = [
  {id:'backlog',statuses:['backlog']},{id:'ready',statuses:['ready']},{id:'in_progress',statuses:['in_progress']},
  {id:'review',statuses:['review']},{id:'verification',statuses:['verification']},{id:'awaiting_acceptance',statuses:['awaiting_acceptance']},
  {id:'closed',statuses:['done','cancelled']},
] as const;
export type IssueType = typeof ISSUE_TYPES[number];
export type BlockedRun={runId:string;bindingId:string;sessionId:string;generation:string|null;kind:'app'|'runtime'};
export type IssueLink = {id:string;sourceId:string;targetId:string;relation:'blocks'|'relates_to'|'duplicates'|'clones';actorId:string;createdAt:string|null;reason:string;source:string;waiver?:string;state?:'pending'|'active';
  blockedRun?:BlockedRun;requiredAction?:'stop_and_reconcile_then_activate'};
export type M2TaskProfile = Omit<M1TaskProfile,'schemaVersion'|'type'|'creator'> & {
  schemaVersion:'m2_task_profile_v1'; type:IssueType; parentId:string|null;
  creator:{kind:'user'|'agent'|'system'|'imported_unknown';actorId:string|null;displayName?:string};
  initiatedBy:string|null;createdAt:string|null;timezone:string;components:string[];affectsVersions:string[];fixVersions:string[];
  rank:number;resolution:null|'completed'|'cancelled'|'duplicate'|'wont_do';
  blocker:null|{reason:string;owner:string;since:string};
  criteriaEvidence:{criterion:string;evidence:string;outcome:'passed'|'failed'}[];
  assignments:{agentId:string;profileVersion:string|null;runId:string|null;sessionId:string|null;startedAt:string|null;endedAt:string|null}[];
  artifacts:{type:string;reference:string;revision:string|null;provenance:string;availability:'available'|'unverified'|'unavailable'|'stale'}[];
  fileContexts:{relativePath:string;revision:string|null;context:string}[];
  scopeExclusions:{taskId:string;reason:string}[];workflow:{id:string;version:number};
  hotfixReason:string|null;
};
export type TaskProfile = M1TaskProfile | M2TaskProfile;
export function issueFail(code:string):never { throw Object.assign(new Error(code),{code}); }
const text = (v:unknown):v is string => typeof v==='string'&&v.trim().length>0;
export function isCalendarDate(value:unknown):value is string {
  return typeof value==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(value)&&Number.isFinite(Date.parse(`${value}T00:00:00.000Z`))
    &&new Date(`${value}T00:00:00.000Z`).toISOString()===`${value}T00:00:00.000Z`;
}
export function isUtcTimestamp(value:unknown):value is string {
  if(typeof value!=='string'||!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?Z$/.test(value))return false;
  const normalized=`${value.slice(0,19)}.${(value[19]==='.'?value.slice(20,-1):'').padEnd(3,'0').slice(0,3)}Z`;
  return Number.isFinite(Date.parse(normalized))&&new Date(normalized).toISOString()===normalized;
}
function safeRelativePath(value:unknown){
  return text(value)&&!/[\x00-\x1f:<>"|?*]/.test(value)&&!value.split(/[\\/]/).some(part=>!part||part==='.'||part==='..'||/[. ]$/.test(part)
    ||/^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)/i.test(part));
}
function strings(v:unknown):v is string[] {return Array.isArray(v)&&v.every(text)&&new Set(v).size===v.length;}
const extensionFields=['parentId','initiatedBy','createdAt','timezone','components','affectsVersions','fixVersions','rank','resolution','blocker',
  'criteriaEvidence','assignments','artifacts','fileContexts','scopeExclusions','workflow','hotfixReason'];

/** Version dispatch preserves the strict M1 interchange contract; upgrading is explicit. */
export function decodeTaskProfile(value:unknown):TaskProfile {
  if (!value || typeof value!=='object' || Array.isArray(value)) issueFail('INVALID_TASK_PROFILE');
  const raw=value as Record<string,unknown>;
  if(raw.schemaVersion!=='m2_task_profile_v1')return decodeM1TaskProfile(value);
  if(!ISSUE_TYPES.includes(raw.type as IssueType))issueFail('INVALID_ISSUE_TYPE');
  const base=Object.fromEntries(Object.entries(raw).filter(([key])=>!extensionFields.includes(key)));
  const creator=raw.creator as M2TaskProfile['creator'];
  if(!creator || !['user','agent','system','imported_unknown'].includes(creator.kind)
    || (creator.kind==='imported_unknown'?creator.actorId!==null:!text(creator.actorId)))issueFail('INVALID_CREATOR');
  const legacy=decodeM1TaskProfile({...base,schemaVersion:'m1_task_profile_v1',type:'Task',
    creator:creator.kind==='user'?{kind:'user',actorId:creator.actorId}:{kind:'imported_unknown',actorId:null}});
  if(raw.parentId!==null&&(!text(raw.parentId)||raw.parentId===raw.id))issueFail('INVALID_PARENT');
  if(raw.initiatedBy!==null&&!text(raw.initiatedBy))issueFail('INVALID_INITIATOR');
  if(raw.hotfixReason!==null&&!text(raw.hotfixReason))issueFail('INVALID_HOTFIX_REASON');
  if(raw.createdAt!==null&&!isUtcTimestamp(raw.createdAt))issueFail('INVALID_CREATED_AT');
  if(!text(raw.timezone))issueFail('INVALID_TIMEZONE');
  try{new Intl.DateTimeFormat('en',{timeZone:raw.timezone as string}).format();}catch{issueFail('INVALID_TIMEZONE');}
  for(const field of ['components','affectsVersions','fixVersions'])if(!strings(raw[field]))issueFail('INVALID_ISSUE_FIELDS');
  if(!Number.isSafeInteger(raw.rank)||Number(raw.rank)<0)issueFail('INVALID_RANK');
  if(raw.resolution!==null&&!['completed','cancelled','duplicate','wont_do'].includes(String(raw.resolution)))issueFail('INVALID_RESOLUTION');
  if(!Array.isArray(raw.criteriaEvidence)||raw.criteriaEvidence.some(e=>!e||!text(e.criterion)||!text(e.evidence)||!['passed','failed'].includes(e.outcome)))issueFail('INVALID_CRITERIA_EVIDENCE');
  if(raw.blocker!==null&&(!raw.blocker||!text((raw.blocker as any).reason)||!text((raw.blocker as any).owner)||!isUtcTimestamp((raw.blocker as any).since)))issueFail('INVALID_BLOCKER');
  for(const name of ['assignments','artifacts','fileContexts','scopeExclusions'])if(!Array.isArray(raw[name]))issueFail('INVALID_ISSUE_FIELDS');
  if((raw.scopeExclusions as any[]).some(e=>!text(e.taskId)||!text(e.reason)))issueFail('INVALID_SCOPE_EXCLUSION');
  if((raw.assignments as any[]).some(e=>!text(e.agentId)||['profileVersion','runId','sessionId','startedAt','endedAt'].some(k=>e[k]!==null&&!text(e[k]))))issueFail('INVALID_ASSIGNMENT');
  if((raw.assignments as any[]).some(e=>['startedAt','endedAt'].some(k=>e[k]!==null&&!isUtcTimestamp(e[k]))
    ||(e.startedAt!==null&&e.endedAt!==null&&Date.parse(e.endedAt)<Date.parse(e.startedAt))))issueFail('INVALID_ASSIGNMENT');
  if((raw.artifacts as any[]).some(e=>!text(e.type)||!text(e.reference)||!text(e.provenance)||!['available','unverified','unavailable','stale'].includes(e.availability)
    || (/^[a-z]+:/i.test(e.reference)&&!/^https?:\/\//i.test(e.reference))))issueFail('INVALID_ARTIFACT');
  for(const artifact of raw.artifacts as any[]){
    if(/^https?:\/\//i.test(artifact.reference)){try{const url=new URL(artifact.reference);if(url.username||url.password)issueFail('INVALID_ARTIFACT');}catch{issueFail('INVALID_ARTIFACT');}}
    else if(!safeRelativePath(artifact.reference))issueFail('INVALID_ARTIFACT');
  }
  if(legacy.files.some(file=>!safeRelativePath(file.relativePath)||(file.previousRelativePath&&!safeRelativePath(file.previousRelativePath))))issueFail('INVALID_FILE_CONTEXT');
  if((raw.fileContexts as any[]).some(e=>!safeRelativePath(e.relativePath)||!text(e.context)||(e.revision!==null&&!text(e.revision))))issueFail('INVALID_FILE_CONTEXT');
  if(!(raw.workflow as any)?.id||!Number.isSafeInteger((raw.workflow as any)?.version))issueFail('INVALID_WORKFLOW');
  return {...legacy,...Object.fromEntries(extensionFields.map(k=>[k,raw[k]])),schemaVersion:'m2_task_profile_v1',type:raw.type,creator} as M2TaskProfile;
}
export function newM2Task(projectId:string,id:string,title:string,actorId:string):M2TaskProfile {
  return {schemaVersion:'m2_task_profile_v1',type:'task',id,projectId,key:'',legacyAlias:null,title,summary:'',technicalValue:'',productValue:'',
    files:[],agentAssignments:[],artifactReferences:[],acceptanceCriteria:[],estimateSeconds:null,actual:{startedAt:null,endedAt:null,durationSeconds:null},
    risks:[],status:'backlog',creator:{kind:'user',actorId},priority:'medium',startDate:null,dueDate:null,links:[],sessionIds:[],provenance:null,
    parentId:null,initiatedBy:null,createdAt:new Date().toISOString(),timezone:'Europe/Moscow',components:[],affectsVersions:[],fixVersions:[],rank:0,
    resolution:null,blocker:null,criteriaEvidence:[],assignments:[],artifacts:[],fileContexts:[],scopeExclusions:[],workflow:{id:'default',version:1},hotfixReason:null};
}
export function upgradeM1Task(task:M1TaskProfile):M2TaskProfile {
  const upgraded:M2TaskProfile={...newM2Task(task.projectId,task.id,task.title,task.creator.actorId??'unknown'),...task,schemaVersion:'m2_task_profile_v1',type:'task',createdAt:null,
    resolution:task.status==='done'?'completed':task.status==='cancelled'?'cancelled':null};
  if(['ready','in_progress'].includes(task.status)){try{validateReady(upgraded);}catch{return {...upgraded,risks:[...new Set([...upgraded.risks,'recovery_review'])]};}}
  return upgraded;
}
const nonterminal=['backlog','ready','in_progress','review','verification','awaiting_acceptance'];
export function validateReady(task:M2TaskProfile) {
  if(![task.title,task.summary,task.technicalValue,task.productValue].every(text)||!task.acceptanceCriteria.length
    ||task.estimateSeconds===null||(!task.files.length&&!task.artifacts.length&&!task.artifactReferences.length)||!task.risks.length)issueFail('READY_FIELDS_REQUIRED');
}
export function transitionAllowed(from:M1TaskStatus,to:M1TaskStatus,manual=false) {
  if(from===to)return true;
  if(manual&&to==='done'&&nonterminal.includes(from))return true;
  if(to==='cancelled'&&nonterminal.includes(from))return true;
  return ({backlog:['ready'],ready:['backlog','in_progress'],in_progress:['review'],review:['in_progress','verification'],verification:['in_progress','awaiting_acceptance'],
    awaiting_acceptance:['in_progress','done'],done:['ready'],cancelled:['backlog']} as Record<string,string[]>)[from]?.includes(to)??false;
}

/** Pure graph oracle used inside the SQLite writer transaction, after all proposed changes. */
export function validateIssueGraph(tasks:TaskProfile[],links:IssueLink[],transitionIds?:ReadonlySet<string>) {
  const byId=new Map(tasks.map(t=>[t.id,t]));
  const m2=tasks.filter((t):t is M2TaskProfile=>t.schemaVersion==='m2_task_profile_v1');
  for(const task of m2){
    const parent=task.parentId?byId.get(task.parentId):null;
    if(task.parentId&&(!parent||parent.projectId!==task.projectId))issueFail('PARENT_SCOPE_CONFLICT');
    const ptype=parent?.schemaVersion==='m2_task_profile_v1'?parent.type:parent?'task':null;
    if(task.type==='epic'&&parent||task.type==='sub_task'&&!['task','bug','user_story'].includes(ptype??'')
      ||['task','bug','user_story'].includes(task.type)&&parent&&ptype!=='epic')issueFail('INVALID_PARENT_TYPE');
    const seen=new Set([task.id]);let node=parent;
    while(node){if(seen.has(node.id))issueFail('HIERARCHY_CYCLE');seen.add(node.id);node=node.schemaVersion==='m2_task_profile_v1'&&node.parentId?byId.get(node.parentId):undefined;}
    if(task.status==='done'&&(!transitionIds||transitionIds.has(task.id))){
      for(const child of m2.filter(t=>t.parentId===task.id))if(child.status!=='done'&&!task.scopeExclusions.some(e=>e.taskId===child.id&&e.reason))issueFail('CHILDREN_INCOMPLETE');
    }
  }
  const seenEdges=new Set<string>();
  for(const link of links){
    if(!byId.has(link.sourceId)||!byId.has(link.targetId)||link.sourceId===link.targetId)issueFail('LINK_SCOPE_CONFLICT');
    if(!['blocks','relates_to','duplicates','clones'].includes(link.relation)||!text(link.reason)||!text(link.actorId))issueFail('INVALID_ISSUE_LINK');
    if(link.waiver!==undefined&&!text(link.waiver))issueFail('INVALID_DEPENDENCY_WAIVER');
    if(link.state==='pending'&&(!link.blockedRun||!text(link.blockedRun.runId)||!text(link.blockedRun.bindingId)||!text(link.blockedRun.sessionId)))issueFail('INVALID_PENDING_LINK');
    if(link.relation==='duplicates'&&links.some(other=>other.id!==link.id&&other.relation==='duplicates'&&other.sourceId===link.sourceId))issueFail('DUPLICATE_CANONICAL_CONFLICT');
    const endpoints=link.relation==='relates_to'?[link.sourceId,link.targetId].sort():[link.sourceId,link.targetId];
    const key=`${link.relation}:${endpoints.join(':')}`;if(seenEdges.has(key))issueFail('DUPLICATE_ISSUE_LINK');seenEdges.add(key);
    const source=byId.get(link.sourceId)!,target=byId.get(link.targetId)!;
    if(link.relation==='blocks'&&((source as M2TaskProfile).parentId===target.id||(target as M2TaskProfile).parentId===source.id))issueFail('PARENT_LINK_CONFLICT');
    if(['blocks','duplicates'].includes(link.relation)){
      const visit=(id:string,path:string[]):void=>{if(path.includes(id))throw Object.assign(new Error('Issue link cycle'),{code:link.relation==='blocks'?'TASK_LINK_CYCLE':'DUPLICATE_CYCLE',cyclePath:[...path.slice(path.indexOf(id)),id]});for(const e of links.filter(l=>l.relation===link.relation&&l.sourceId===id))visit(e.targetId,[...path,id]);};visit(link.sourceId,[]);
    }
    if(link.relation==='blocks'&&['in_progress','done'].includes(target.status)&&(!transitionIds||transitionIds.has(target.id))){
      if(link.state==='pending')issueFail('PENDING_LINK_RECONCILIATION_REQUIRED');
      if(!link.waiver&&source.status!=='done')issueFail('DEPENDENCY_BLOCKED');
    }
  }
}

export function rollup(tasks:TaskProfile[],id:string){
  const descendants=new Set<string>();const visit=(key:string)=>{for(const t of tasks)if(t.schemaVersion==='m2_task_profile_v1'&&t.parentId===key&&!descendants.has(t.id)){descendants.add(t.id);visit(t.id);}};visit(id);
  const values=tasks.filter(t=>descendants.has(t.id));return {children:values.length,done:values.filter(t=>t.status==='done').length,cancelled:values.filter(t=>t.status==='cancelled').length,
    estimateSeconds:values.reduce((n,t)=>n+(t.estimateSeconds??0),0),ownEstimateSeconds:tasks.find(t=>t.id===id)?.estimateSeconds??null};
}

/** Legacy task-owned edges remain visible and effective; explicit canonical records take precedence. */
export function canonicalIssueLinks(tasks:TaskProfile[],persisted:IssueLink[]):IssueLink[]{
  const byKey=new Map<string,IssueLink>();
  const key=(link:IssueLink)=>`${link.relation}:${link.relation==='relates_to'?[link.sourceId,link.targetId].sort().join(':'):[link.sourceId,link.targetId].join(':')}`;
  for(const task of tasks)for(const ref of task.links){
    let sourceId=task.id,targetId=ref.taskId;if(ref.relation==='blocked_by')[sourceId,targetId]=[targetId,sourceId];
    const relation=ref.relation==='related'?'relates_to':'blocks';if(relation==='relates_to'&&sourceId>targetId)[sourceId,targetId]=[targetId,sourceId];
    const link:IssueLink={id:`legacy:${relation}:${sourceId}:${targetId}`,sourceId,targetId,relation,actorId:'imported_unknown',createdAt:null,
      reason:'Preserved task link',source:'legacy_task_profile',state:'active'};byKey.set(key(link),link);
  }
  const persistedKeys=new Set<string>();for(const link of persisted){const k=key(link);if(persistedKeys.has(k))issueFail('DUPLICATE_ISSUE_LINK');persistedKeys.add(k);byKey.set(k,link);}return [...byKey.values()];
}
