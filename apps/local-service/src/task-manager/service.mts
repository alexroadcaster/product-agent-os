import { createHash, randomUUID } from 'node:crypto';
import { readFile, realpath, lstat, open } from 'node:fs/promises';
import { resolve, relative } from 'node:path';
import type { LocalStore } from '../storage/local-store.mts';
import type { StoreWrite, StoredEntity, EntityInput } from '../../../../packages/contracts/storage/local-store.ts';
import { DEFAULT_COMPONENTS, STATUS_COLUMNS, decodeTaskProfile, newM2Task, upgradeM1Task, canonicalIssueLinks, issueFail as fail,
  isCalendarDate, ISSUE_TYPES,type M2TaskProfile, type IssueLink, type BlockedRun } from '../../../../packages/contracts/issues/task-profile.ts';

import type { CatalogItem,VersionItem,Board } from '../../../../packages/contracts/issues/manager.ts';
import {defaultRegistry,validateRegistry,workflowSnapshot,workflowCategory,requiredBoardStates} from '../workflows/registry.mts';
import {workflowCommand} from '../workflows/commands.mts';
export type {CatalogItem,VersionItem,Board} from '../../../../packages/contracts/issues/manager.ts';
const defaultBoard:Board={columns:STATUS_COLUMNS.map(c=>({id:c.id,statuses:[...c.statuses]})),outOfBoard:false,
  attachmentFileBytes:50*1024*1024,attachmentTaskBytes:500*1024*1024,timezone:'Europe/Moscow'};
const defaults=()=>DEFAULT_COMPONENTS.map(name=>({id:name,name,status:'active' as const}));
const digest=(v:unknown)=>createHash('sha256').update(JSON.stringify(v)).digest('hex');
const nonempty=(v:unknown):v is string=>typeof v==='string'&&v.trim().length>0;
const integer=(v:unknown):v is number=>Number.isSafeInteger(v)&&Number(v)>=0;
async function all(store:LocalStore,projectId:string,kind?:StoredEntity['kind']){
  const items:StoredEntity[]=[];for(let offset=0;;offset+=100){const page=await store.list(projectId,{kind,offset,limit:100});items.push(...page);if(page.length<100)return items;if(items.length>=100000)fail('SNAPSHOT_TOO_LARGE');}
}
export function pinBlockingRun(rows:readonly StoredEntity[],targetId:string):BlockedRun|undefined{
  const matches=rows.filter(r=>r.kind==='run'&&!['completed','failed','interrupted'].includes(r.status)
    &&((r.data.runtimeRun as any)?.taskId===targetId||(r.data.appAgentRun as any)?.taskContext?.taskId===targetId));
  if(matches.length>1)fail('ACTIVE_RUN_RECONCILIATION_REQUIRED');
  const active=matches[0];if(!active)return undefined;
  const run=(active.data.runtimeRun??active.data.appAgentRun) as any;
  if(!nonempty(run.bindingId)||!nonempty(run.sessionId))fail('ACTIVE_RUN_SCOPE_UNAVAILABLE');
  return {runId:active.id,bindingId:run.bindingId,sessionId:run.sessionId,generation:run.generation??null,kind:active.data.appAgentRun?'app':'runtime'};
}
export async function taskManagerSnapshot(store:LocalStore,projectId:string){
  const rows=await store.projectEntities(projectId);const setting=(name:string)=>rows.find(e=>e.id===`m2-${name}`&&e.kind==='settings');
  const board=(setting('board')?.data.value??defaultBoard) as Board;
  return {tasks:rows.filter(e=>e.kind==='task'),components:(setting('components')?.data.items??defaults()) as CatalogItem[],
    versions:(setting('versions')?.data.items??[]) as VersionItem[],workflows:validateRegistry(setting('workflows')?.data??defaultRegistry()),board,links:canonicalIssueLinks(rows.filter(e=>e.kind==='task').map(e=>decodeTaskProfile(e.data)),(setting('links')?.data.items??[]) as IssueLink[]),
    comments:rows.filter(e=>e.kind==='comment'),attachments:rows.filter(e=>e.kind==='document'&&e.data.category==='managed_attachment'),
    settingsRevisions:Object.fromEntries(['components','versions','board','links','workflows'].map(n=>[n,setting(n)?.revision??0])),
    quota:{fileBytes:board.attachmentFileBytes,taskBytes:board.attachmentTaskBytes},coverage:'complete' as const};
}
function safeName(name:unknown){
  if(!nonempty(name)||name.length>240||/[\\/:<>"|?*\x00-\x1f]/.test(name)||/[. ]$/.test(name)||name==='.'||name==='..'
    ||/^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)/i.test(name))fail('INVALID_ATTACHMENT_NAME');return name;
}
function validateMedia(name:string,type:unknown,bytes:Uint8Array){
  if(!nonempty(type)||!/^[\w.+-]+\/[\w.+-]+$/.test(type))fail('INVALID_MEDIA_TYPE');
  const ext=name.toLowerCase().split('.').at(-1),head=Buffer.from(bytes.slice(0,16));
  const matches:Record<string,[string,boolean]>={png:['image/png',head.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10]))],
    jpg:['image/jpeg',head[0]===255&&head[1]===216&&head[2]===255],jpeg:['image/jpeg',head[0]===255&&head[1]===216&&head[2]===255],
    pdf:['application/pdf',head.subarray(0,5).toString()==='%PDF-'],gif:['image/gif',/^GIF8[79]a/.test(head.toString())]};
  if(ext&&matches[ext]&&(matches[ext][0]!==type||!matches[ext][1]))fail('MIME_CONTENT_MISMATCH');
  if(type.startsWith('image/')&&!['png','jpg','jpeg','gif','svg'].includes(ext??''))fail('MIME_CONTENT_MISMATCH');
  if(type==='application/pdf'&&ext!=='pdf')fail('MIME_CONTENT_MISMATCH');
  if(type.startsWith('text/')&&Buffer.from(bytes).includes(0))fail('MIME_CONTENT_MISMATCH');
}

const writers=new WeakMap<LocalStore,Map<string,Promise<unknown>>>();
async function serialize<T>(store:LocalStore,projectId:string,operation:()=>Promise<T>):Promise<T>{
  let queue=writers.get(store);if(!queue){queue=new Map();writers.set(store,queue);}
  const previous=queue.get(projectId)??Promise.resolve(),next=previous.catch(()=>{}).then(operation);queue.set(projectId,next);
  try{return await next;}finally{if(queue.get(projectId)===next)queue.delete(projectId);}
}
/** All browser M2 mutations use this single authenticated command boundary. */
export type WorkflowCommandOptions={validateWorkflowReferences?:(definition:import('../../../../packages/contracts/workflows/workflow.ts').WorkflowDefinition)=>Promise<void>;recipeExecution?:StoreWrite['recipeExecution'];additionalChanges?:StoreWrite['changes']};
export function taskManagerCommand(store:LocalStore,projectId:string,actorId:string,input:Record<string,any>,options:WorkflowCommandOptions={}){
  return serialize(store,projectId,()=>applyTaskManagerCommand(store,projectId,actorId,input,options));
}
async function applyTaskManagerCommand(store:LocalStore,projectId:string,actorId:string,input:Record<string,any>,options:WorkflowCommandOptions){
  if(!nonempty(input.idempotencyKey)||!integer(input.expectedAuthorityEpoch)||!nonempty(input.action))fail('INVALID_COMMAND');
  const project=await store.project(projectId);if(!project)fail('PROJECT_NOT_FOUND');
  if(project.authorityEpoch!==input.expectedAuthorityEpoch)fail('AUTHORITY_CONFLICT');
  // A persisted operation digest makes retry independent of subsequent task/catalog revisions.
  const operationId=`m2-operation-${createHash('sha256').update(input.idempotencyKey).digest('hex')}`;
  const inputHash=digest(input),previous=await store.receipt(projectId,input.idempotencyKey);
  if(previous){const operation=await store.get(projectId,operationId);if(operation?.data.inputHash!==inputHash)fail('IDEMPOTENCY_CONFLICT');return {...previous,...(operation.data.linkId?{linkId:operation.data.linkId}:{})};}
  const snapshot=await taskManagerSnapshot(store,projectId);
  const command:StoreWrite={projectId,actorId,idempotencyKey:input.idempotencyKey,expectedAuthorityEpoch:input.expectedAuthorityEpoch,changes:[]};
  const changes:Array<StoreWrite['changes'][number]>=[];
  let transition:StoreWrite['taskManagerAction'];
  let createdLinkId:string|undefined;
  let workflowMetadata:Partial<StoreWrite>={};
  const target=()=>{const t=snapshot.tasks.find(t=>t.id===input.taskId);if(!t)fail('TASK_NOT_FOUND');if(t.revision!==input.expectedRevision)fail('REVISION_CONFLICT');return t;};
  const setting=(name:string,data:Record<string,unknown>)=>{
    if(snapshot.settingsRevisions[name]!==input.expectedRevision)fail('REVISION_CONFLICT');
    changes.push({expectedRevision:input.expectedRevision,entity:{id:`m2-${name}`,kind:'settings',data}});
  };
  if(input.action.startsWith('workflow-')){
    if(['workflow-validate','workflow-publish-preview','workflow-publish'].includes(input.action)){
      const definition=input.action==='workflow-validate'&&input.definition?input.definition:snapshot.workflows.workflows.find(w=>w.id===input.workflowId)?.draft;
      if(definition?.recipes?.some((recipe:any)=>recipe.steps?.some((step:any)=>step.skills?.length))){
        if(!options.validateWorkflowReferences)fail('WORKFLOW_SKILL_CATALOG_UNAVAILABLE');
        await options.validateWorkflowReferences(definition);
      }
    }
    const result=workflowCommand(snapshot,input);if(result.preview!==undefined)return result.preview;
    changes.push(...result.changes);workflowMetadata=result.metadata??{};
  }else if(input.action==='save'||input.action==='upgrade'){
    let raw=input.task as Record<string,any>;if(!raw||raw.projectId!==projectId)fail('TASK_SCOPE_CONFLICT');
    const old=snapshot.tasks.find(t=>t.id===raw.id);
    if(old&&old.data.schemaVersion!=='m2_task_profile_v1'&&input.action!=='upgrade')fail('PROFILE_UPGRADE_REQUIRED');
    if(!integer(input.expectedRevision)||(old?.revision??0)!==input.expectedRevision)fail('REVISION_CONFLICT');
    if(input.action==='upgrade'){
      if(!old)fail('TASK_NOT_FOUND');const current=decodeTaskProfile(old.data);raw=current.schemaVersion==='m2_task_profile_v1'?current:upgradeM1Task(current);
    }
    const creator=old?.data.creator??{kind:'user',actorId};
    raw={...raw,hotfixReason:old?.data.hotfixReason??null,actual:old?.data.actual??{startedAt:null,endedAt:null,durationSeconds:null}};
    if(!old){
      const workflowId=input.workflowId??snapshot.workflows.typeMapping[raw.type]??snapshot.workflows.defaultWorkflowId;
      const selected=snapshot.workflows.workflows.find(w=>w.id===workflowId&&!w.archived&&w.activeVersion!==null);if(!selected)fail('WORKFLOW_ASSIGNMENT_INVALID');
      const workflow={id:selected.id,version:selected.activeVersion!};const initial=workflowSnapshot(snapshot.workflows,workflow).definition.states.find(s=>s.initial)!;
      raw={...raw,workflow,status:initial.id,createdAt:new Date().toISOString(),timezone:snapshot.board.timezone??'Europe/Moscow',initiatedBy:null};
    }
    const task=decodeTaskProfile({...raw,creator,key:raw.key===''?`${project.keyPrefix}-1`:raw.key});
    if(task.schemaVersion!=='m2_task_profile_v1')fail('M2_PROFILE_REQUIRED');
    if(old&&task.status!==old.status)fail('TRANSITION_REQUIRED');
    if(JSON.stringify(task.links)!==JSON.stringify(old?.data.links??[]))fail('ISSUE_LINK_COMMAND_REQUIRED');
    if(old&&old.data.dueDate!==task.dueDate&&!nonempty(input.reason))fail('DUE_DATE_REASON_REQUIRED');
    const structural=old&&old.data.schemaVersion==='m2_task_profile_v1'&&(old.data.type!==task.type||old.data.parentId!==task.parentId);
    const previewDigest=digest({...task,key:raw.key});
    if(input.preview===true)return {preview:true,task,changes:structural?['type','parentId']:[],expectedRevision:input.expectedRevision,previewDigest};
    if(structural&&input.previewDigest!==previewDigest)fail('PREVIEW_REQUIRED');
    for(const id of task.components)if(!snapshot.components.some(c=>c.id===id))fail('COMPONENT_NOT_FOUND');
    for(const id of [...task.affectsVersions,...task.fixVersions])if(!snapshot.versions.some(c=>c.id===id))fail('VERSION_NOT_FOUND');
    changes.push({expectedRevision:input.expectedRevision,entity:{id:task.id,kind:'task',data:{...task,key:raw.key===''?'':task.key}}});
  }else if(input.action==='transition'){
    const old=target();const decoded=decodeTaskProfile(old.data);if(decoded.schemaVersion!=='m2_task_profile_v1')fail('M2_PROFILE_REQUIRED');
    if(!nonempty(input.reason))fail('REASON_REQUIRED');
    transition=input.manual===true?'complete':'transition';
    const status=input.status as M2TaskProfile['status'];
    const category=workflowCategory(snapshot.workflows,{...decoded,status}),oldCategory=workflowCategory(snapshot.workflows,decoded);
    if(category==='ready'&&(snapshot.board.releaseRequiredTypes?.includes(decoded.type)||snapshot.board.releaseRequiredComponents?.some(c=>decoded.components.includes(c)))
      &&!decoded.fixVersions.length&&!input.hotfixReason&&!decoded.hotfixReason)fail('TARGET_RELEASE_REQUIRED');
    const column=snapshot.board.columns.find(c=>c.statuses.includes(status));
    if(column?.wipLimit!==undefined&&!column.statuses.includes(decoded.status)&&snapshot.tasks.filter(t=>column.statuses.includes(t.status)).length>=column.wipLimit){
      if(column.wipMode==='hard')fail('HARD_WIP_LIMIT');if(!input.softWipOverride)fail('SOFT_WIP_CONFIRMATION_REQUIRED');
    }
    const now=new Date().toISOString();
    const task={...decoded,status,resolution:category==='done'?'completed':category==='cancelled'?(input.resolution??'cancelled'):null,
      hotfixReason:input.hotfixReason??decoded.hotfixReason,
      criteriaEvidence:input.evidence??decoded.criteriaEvidence,
      actual:category==='in_progress'?{...decoded.actual,startedAt:decoded.actual.startedAt??now,endedAt:null}
        :['done','cancelled'].includes(category)?{...decoded.actual,endedAt:now}
        :['done','cancelled'].includes(oldCategory)?{...decoded.actual,endedAt:null}:decoded.actual};
    changes.push({expectedRevision:old.revision,entity:{id:old.id,kind:'task',data:task}});
    // Reopening a prerequisite preserves completed history and marks downstream review explicitly.
    if(['done','cancelled'].includes(oldCategory)&&!['done','cancelled'].includes(category)){
      for(const link of snapshot.links.filter(l=>l.relation==='blocks'&&l.sourceId===old.id)){
        const dependent=snapshot.tasks.find(t=>t.id===link.targetId);if(dependent?.data.schemaVersion==='m2_task_profile_v1'&&workflowCategory(snapshot.workflows,decodeTaskProfile(dependent.data))==='done')changes.push({expectedRevision:dependent.revision,
          entity:{id:dependent.id,kind:'task',data:{...dependent.data,risks:[...new Set([...(dependent.data.risks as string[]),'dependency_review'])]}}});
      }
      const parent=snapshot.tasks.find(t=>t.id===decoded.parentId);if(parent?.data.schemaVersion==='m2_task_profile_v1'&&workflowCategory(snapshot.workflows,decodeTaskProfile(parent.data))==='done')changes.push({expectedRevision:parent.revision,
        entity:{id:parent.id,kind:'task',data:{...parent.data,risks:[...new Set([...(parent.data.risks as string[]),'scope_review'])]}}});
    }
  }else if(input.action==='component'||input.action==='version'){
    const name=input.action==='component'?'components':'versions';const item=input.item;
    if(!item||!nonempty(item.id)||!nonempty(item.name)||item.name.length>200)fail('INVALID_CATALOG_ITEM');
    const allowed=input.action==='component'?['active','archived']:['unreleased','released','archived'];if(!allowed.includes(item.status))fail('INVALID_CATALOG_ITEM');
    if(input.action==='version'&&item.description!==undefined&&(typeof item.description!=='string'||item.description.length>20000))fail('INVALID_VERSION_DESCRIPTION');
    if(input.action==='version'&&(['startDate','releaseDate'].some(k=>item[k]!==undefined&&item[k]!==null&&!isCalendarDate(item[k]))
      ||item.startDate&&item.releaseDate&&item.startDate>item.releaseDate))fail('INVALID_VERSION_DATES');
    const list=[...snapshot[name]];const index=list.findIndex(v=>v.id===item.id);if(index>=0)list[index]={...list[index],...item};else list.push(item);
    setting(name,{items:list});
  }else if(input.action==='board'){
    const board=input.board as Board;if(!board||!Array.isArray(board.columns)||!board.columns.length)fail('INVALID_BOARD');
    if(typeof board.outOfBoard!=='boolean'||new Set(board.columns.map(c=>c.id)).size!==board.columns.length)fail('INVALID_BOARD_MAPPING');
    if(board.timezone!==undefined){try{if(!nonempty(board.timezone))fail('INVALID_TIMEZONE');new Intl.DateTimeFormat('en',{timeZone:board.timezone}).format();}catch{fail('INVALID_TIMEZONE');}}
    if(board.releaseRequiredTypes!==undefined&&(!Array.isArray(board.releaseRequiredTypes)||board.releaseRequiredTypes.some(t=>!ISSUE_TYPES.includes(t as any))))fail('INVALID_RELEASE_POLICY');
    if(board.releaseRequiredComponents!==undefined&&(!Array.isArray(board.releaseRequiredComponents)||board.releaseRequiredComponents.some(id=>!snapshot.components.some(c=>c.id===id))))fail('INVALID_RELEASE_POLICY');
    const statuses=board.columns.flatMap(c=>c.statuses);const known=requiredBoardStates(snapshot.workflows,snapshot.tasks.map(t=>t.data));
    if(new Set(statuses).size!==statuses.length||statuses.some(s=>!known.includes(s as any))||(!board.outOfBoard&&known.some(s=>!statuses.includes(s))))fail('INVALID_BOARD_MAPPING');
    if(board.columns.some(c=>!nonempty(c.id)||!Array.isArray(c.statuses)||(c.wipLimit!==undefined&&(!integer(c.wipLimit)||!['soft','hard'].includes(c.wipMode??'')))))fail('INVALID_WIP');
    if(!integer(board.attachmentFileBytes)||board.attachmentFileBytes<1||board.attachmentFileBytes>50*1024*1024||!integer(board.attachmentTaskBytes)||board.attachmentTaskBytes<board.attachmentFileBytes)fail('INVALID_QUOTA');
    setting('board',{value:board});
  }else if(input.action==='link'||input.action==='unlink'||input.action==='activate-link'){
    const links=[...snapshot.links];
    if(input.action==='activate-link'){
      const link=links.find(l=>l.id===input.linkId);if(!link||link.state!=='pending')fail('LINK_NOT_FOUND');
      const runs=await all(store,projectId,'run');if(runs.some(r=>!['completed','failed','interrupted'].includes(r.status)))fail('ACTIVE_RUN_RECONCILIATION_REQUIRED');
      link.state='active';
    }else if(input.action==='unlink'){
      if(!nonempty(input.reason))fail('REASON_REQUIRED');const index=links.findIndex(l=>l.id===input.linkId);if(index<0)fail('LINK_NOT_FOUND');
      const removed=links[index];links.splice(index,1);
      for(const task of snapshot.tasks){const profile=decodeTaskProfile(task.data);
        const retained=profile.links.filter(ref=>{let sourceId=task.id,targetId=ref.taskId;if(ref.relation==='blocked_by')[sourceId,targetId]=[targetId,sourceId];
          return !((ref.relation==='related'?removed.relation==='relates_to'&&[sourceId,targetId].sort().join(':')===[removed.sourceId,removed.targetId].sort().join(':')
            :removed.relation==='blocks'&&sourceId===removed.sourceId&&targetId===removed.targetId));});
        if(retained.length!==profile.links.length)changes.push({expectedRevision:task.revision,entity:{id:task.id,kind:'task',data:{...profile,links:retained}}});
      }
    }else{
      const l=input.link;if(!l||!nonempty(l.reason))fail('INVALID_ISSUE_LINK');
      let targetId=l.targetId;
      if(l.relation==='duplicates'){
        const visited=new Set<string>([l.sourceId]);while(true){if(visited.has(targetId))fail('DUPLICATE_CYCLE');visited.add(targetId);const next=links.find(e=>e.relation==='duplicates'&&e.sourceId===targetId);if(!next)break;targetId=next.targetId;}
        for(const edge of links)if(edge.relation==='duplicates'&&edge.targetId===l.sourceId)edge.targetId=targetId;
      }
      const runs=l.relation==='blocks'?await all(store,projectId,'run'):[];
      const blockedRun=pinBlockingRun(runs,targetId);
      createdLinkId=randomUUID();
      links.push({id:createdLinkId,sourceId:l.sourceId,targetId,relation:l.relation,reason:l.reason,actorId,createdAt:new Date().toISOString(),source:'user',state:blockedRun?'pending':'active',
        ...(blockedRun?{blockedRun,requiredAction:'stop_and_reconcile_then_activate' as const}:{}),...(l.waiver?{waiver:l.waiver}:{})});
    }
    setting('links',{items:links});
  }else if(input.action==='comment'){
    const task=snapshot.tasks.find(t=>t.id===input.taskId);if(!task)fail('TASK_NOT_FOUND');
    const id=input.id??randomUUID(),old=await store.get(projectId,id);
    if(old&&(old.kind!=='comment'||old.parentId!==task.id||old.data.category!=='m2_comment'))fail('COMMENT_SCOPE_CONFLICT');
    if(old&&old.data.actorId!==actorId)fail('COMMENT_AUTHOR_REQUIRED');
    if(!integer(input.expectedRevision)||(old?.revision??0)!==input.expectedRevision)fail('REVISION_CONFLICT');
    if(!input.delete&&!nonempty(input.body))fail('COMMENT_BODY_REQUIRED');
    if(input.replyTo&&!snapshot.comments.some(c=>c.id===input.replyTo&&c.parentId===task.id))fail('COMMENT_REPLY_SCOPE');
    if(input.attachmentIds&&(!Array.isArray(input.attachmentIds)||input.attachmentIds.some((id:string)=>!snapshot.attachments.some(a=>a.id===id&&a.data.taskId===task.id&&a.data.status!=='deleted'))))fail('ATTACHMENT_SCOPE_CONFLICT');
    changes.push({expectedRevision:input.expectedRevision,entity:{id,kind:'comment',parentId:task.id,body:input.delete?'':input.body,
      data:{category:'m2_comment',actorId,createdAt:old?.data.createdAt??new Date().toISOString(),edited:!!old,deleted:!!input.delete,
        replyTo:input.replyTo??old?.data.replyTo??null,attachmentIds:input.attachmentIds??[],mentions:input.mentions??[],runId:null,sessionId:null}}});
  }else if(input.action==='attachment-delete'){
    const attachment=await store.get(projectId,input.attachmentId);if(!attachment||attachment.data.taskId!==input.taskId||attachment.data.category!=='managed_attachment')fail('ATTACHMENT_NOT_FOUND');
    if(!nonempty(input.reason))fail('REASON_REQUIRED');
    const references=snapshot.comments.filter(c=>(c.data.attachmentIds as string[]|undefined)?.includes(attachment.id));
    if(references.length&&!input.referencesAcknowledged)fail('ATTACHMENT_REFERENCES_CONFIRMATION_REQUIRED');
    changes.push({expectedRevision:input.expectedRevision,entity:{...attachment,blobIds:[],data:{...attachment.data,status:'deleted',deletedBy:actorId,reason:input.reason}}});
  }else fail('UNSUPPORTED_TASK_MANAGER_ACTION');
  changes.push({expectedRevision:0,entity:{id:operationId,kind:'evidence',data:{category:'m2_command_receipt',inputHash,action:input.action,taskId:input.taskId??input.task?.id??null,
    sourceId:input.link?.sourceId??null,targetId:input.link?.targetId??null,linkId:createdLinkId??null,reason:input.reason??input.link?.reason??null,
    ...(input.action==='transition'?{softWipOverrideRequested:input.softWipOverride===true}:{})}}});
  const editsExistingTask=changes.some(change=>change.entity.kind==='task'&&change.expectedRevision>0);
  changes.push(...(options.additionalChanges??[]));
  const receipt=await store.write({...command,...workflowMetadata,changes,...(input.action==='activate-link'||editsExistingTask?{requireIdle:true as const}:{}),...(transition?{taskManagerAction:transition,taskManagerReason:input.reason,
    ...(input.hotfixReason?{taskManagerHotfixReason:String(input.hotfixReason)}:{}),requireIdle:true as const}:{}),
    ...(['save','upgrade'].includes(input.action)&&nonempty(input.reason)?{taskManagerReviewReason:input.reason}:{}),...(options.recipeExecution?{recipeExecution:options.recipeExecution}:{})});
  return {...receipt,...(createdLinkId?{linkId:createdLinkId}:{})};
}

type ManagerRuntime={snapshot(input:Record<string,unknown>):Promise<unknown>;dispatch(action:string,input:Record<string,unknown>):Promise<unknown>};
/** A pending link pins its original writer. A retry can never discover and interrupt a newer task run. */
export async function requestPendingLinkStop(store:LocalStore,runtime:ManagerRuntime|undefined,projectId:string,linkId:string){
  const link=(await taskManagerSnapshot(store,projectId)).links.find(l=>l.id===linkId);
  if(!link||link.state!=='pending'||!link.blockedRun)fail('PENDING_LINK_NOT_FOUND');
  const pin=link.blockedRun,row=await store.get(projectId,pin.runId),run=(row?.data.runtimeRun??row?.data.appAgentRun) as any;
  if(!row||row.kind!=='run'||!run||run.bindingId!==pin.bindingId||run.sessionId!==pin.sessionId||run.projectId!==projectId
    ||(run.taskId??run.taskContext?.taskId)!==link.targetId)fail('PENDING_RUN_SCOPE_CONFLICT');
  if(['completed','failed','interrupted'].includes(row.status))return {linkId,state:'pending',stopRequested:false,terminalReceipt:true,runId:pin.runId,activationRequired:true};
  if(!runtime)fail('RUNTIME_UNAVAILABLE');
  const state=await runtime.snapshot({projectId,sessionId:pin.sessionId}) as Record<string,any>;
  if(state.runId!==pin.runId||state.bindingId!==pin.bindingId||state.state==='recovery_required'
    ||(pin.generation!==null&&state.generation!==pin.generation)
    ||(pin.generation===null&&run.state!=='queued'))fail('PENDING_RUN_STALE');
  await runtime.dispatch('interrupt',{projectId,sessionId:pin.sessionId,bindingId:pin.bindingId,runId:pin.runId,...(state.generation?{generation:state.generation}:{})});
  const saved=await store.get(projectId,pin.runId);
  return {linkId,state:'pending',stopRequested:true,terminalReceipt:!!saved&&['completed','failed','interrupted'].includes(saved.status),runId:pin.runId,activationRequired:true};
}

export function uploadTaskAttachment(store:LocalStore,projectId:string,taskId:string,actorId:string,input:Record<string,any>){
  return serialize(store,projectId,()=>applyUploadTaskAttachment(store,projectId,taskId,actorId,input));
}
async function applyUploadTaskAttachment(store:LocalStore,projectId:string,taskId:string,actorId:string,input:Record<string,any>){
  if(!nonempty(input.idempotencyKey)||!integer(input.expectedAuthorityEpoch))fail('INVALID_UPLOAD');
  const operationId=`m2-upload-${digest(input.idempotencyKey)}`,inputHash=digest({...input,taskId});
  const previous=await store.receipt(projectId,input.idempotencyKey);
  if(previous){if((await store.get(projectId,operationId))?.data.inputHash!==inputHash)fail('IDEMPOTENCY_CONFLICT');return previous;}
  const task=await store.get(projectId,taskId);if(!task||task.kind!=='task')fail('TASK_NOT_FOUND');
  if(task.revision!==input.expectedRevision)fail('REVISION_CONFLICT');
  const snapshot=await taskManagerSnapshot(store,projectId),filename=safeName(input.filename);
  if(typeof input.base64!=='string'||!/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(input.base64))fail('INVALID_UPLOAD');
  const bytes=Buffer.from(input.base64,'base64');if(bytes.length>snapshot.quota.fileBytes)fail('FILE_QUOTA_EXCEEDED');
  const used=snapshot.attachments.filter(a=>a.data.taskId===taskId&&a.data.status!=='deleted').reduce((n,a)=>n+Number(a.data.byteSize),0);
  if(used+bytes.length>snapshot.quota.taskBytes)fail('TASK_QUOTA_EXCEEDED');validateMedia(filename,input.mediaType,bytes);
  const blob=await store.putBlob(projectId,bytes),id=randomUUID();
  try{
  const project=await store.project(projectId);if(!project||project.authorityEpoch!==input.expectedAuthorityEpoch)fail('AUTHORITY_CONFLICT');
  return await store.write({projectId,actorId,idempotencyKey:input.idempotencyKey,expectedAuthorityEpoch:input.expectedAuthorityEpoch,
    changes:[{expectedRevision:task.revision,entity:{...task}},
      {expectedRevision:0,entity:{id:operationId,kind:'evidence',data:{category:'m2_upload_receipt',inputHash}}},
      {expectedRevision:0,entity:{id,kind:'document',title:filename,blobIds:[blob.id],data:{category:'managed_attachment',taskId,filename,
      mediaType:input.mediaType,byteSize:blob.byteSize,sha256:blob.sha256,storageReference:blob.id,actorId,createdAt:new Date().toISOString(),status:'available'}}}]});
  }catch(error){
    // A lost ACK may follow a committed link; the Worker checks references before discarding only this new UUID.
    await store.discardUnreferencedBlob(projectId,blob.id);
    throw error;
  }
}

export async function downloadTaskAttachment(store:LocalStore,projectId:string,taskId:string,id:string){
  const attachment=await store.get(projectId,id);if(!attachment||attachment.data.category!=='managed_attachment'||attachment.data.taskId!==taskId||attachment.data.status==='deleted')fail('ATTACHMENT_NOT_FOUND');
  const bytes=await store.readBlob(projectId,String(attachment.data.storageReference));
  return new Response(new Uint8Array(bytes).buffer,{headers:{'content-type':'application/octet-stream','content-disposition':`attachment; filename*=UTF-8''${encodeURIComponent(String(attachment.data.filename))}`,
    'x-content-type-options':'nosniff','cache-control':'no-store','content-security-policy':"default-src 'none'; sandbox"}});
}

/** Only task-declared paths are readable. A changed revision returns stale, never replacement content. */
export async function resolveTaskReference(store:LocalStore,projectId:string,input:Record<string,any>){
  const task=await store.get(projectId,input.taskId),project=await store.project(projectId);
  if(!task||task.kind!=='task'||!project)fail('TASK_NOT_FOUND');
  const path=input.relativePath;
  if(!nonempty(path)||path.split(/[\\/]/).some(p=>!p||p==='.'||p==='..'||/[\x00-\x1f:<>"|?*]/.test(p)||/[. ]$/.test(p)
    ||/^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)/i.test(p)))fail('REFERENCE_PATH_FORBIDDEN');
  if(/(?:^|[\\/])(?:\.env(?:\.|$)|\.git|\.aws|credentials|auth\.json|id_rsa|id_ed25519)/i.test(path)||/\.(?:pem|key|pfx|p12)$/i.test(path))fail('REFERENCE_PATH_FORBIDDEN');
  const files=(task.data.files??[]) as any[],artifacts=(task.data.artifacts??[]) as any[];
  if(!files.some(f=>f.relativePath===path||f.previousRelativePath===path)&&!artifacts.some(a=>a.reference===path))fail('REFERENCE_OUT_OF_SCOPE');
  const root=await realpath(project.canonicalRoot),candidate=resolve(root,path);
  if(relative(root,candidate).startsWith('..'))fail('REFERENCE_PATH_FORBIDDEN');
  try{
    const final=await realpath(candidate);if(relative(root,final).startsWith('..'))fail('REFERENCE_PATH_FORBIDDEN');
    const before=await lstat(candidate,{bigint:true});if(!before.isFile()||before.isSymbolicLink()||before.nlink!==1n||before.size>1048576n)return {availability:'unavailable',reason:'unsupported_source',relativePath:path};
    const file=await open(candidate,'r');try{
      const opened=await file.stat({bigint:true});if(opened.ino!==before.ino||opened.dev!==before.dev||opened.nlink!==1n)fail('REFERENCE_SOURCE_CHANGED');
      const buffer=Buffer.alloc(1048577);let size=0;
      while(size<buffer.length){const part=await file.read(buffer,size,buffer.length-size,size);if(!part.bytesRead)break;size+=part.bytesRead;}
      const after=await file.stat({bigint:true});if(size>1048576||after.mtimeNs!==before.mtimeNs||after.ctimeNs!==before.ctimeNs||after.size!==BigInt(size))fail('REFERENCE_SOURCE_CHANGED');
      if(await realpath(candidate)!==final)fail('REFERENCE_SOURCE_CHANGED');
      const bytes=buffer.subarray(0,size),revision=createHash('sha256').update(bytes).digest('hex');
      const expected=input.revision??((task.data.fileContexts??[]) as any[]).find(c=>c.relativePath===path)?.revision;
      if(!expected)return {availability:'unavailable',reason:'revision_required',relativePath:path,revision};
      if(expected!==revision)return {availability:'stale',relativePath:path,expectedRevision:expected,revision};
      const text=new TextDecoder('utf-8',{fatal:true}).decode(bytes),content=text.replace(/sk-[A-Za-z0-9_-]+/g,'[REDACTED]')
        .replace(/^(\s*(?:[A-Z_]*(?:TOKEN|PASSWORD|SECRET|API_KEY)|PRIVATE_KEY)\s*[:=]).+$/gim,'$1 [REDACTED]');
      return {availability:'available',relativePath:path,revision,content,redacted:content!==text};
    }finally{await file.close();}
  }catch(error){if((error as any).code==='REFERENCE_PATH_FORBIDDEN')throw error;return {availability:'unavailable',relativePath:path,reason:'source_unavailable'};}
}
