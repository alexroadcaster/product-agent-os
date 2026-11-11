import { createHash } from 'node:crypto';
import type { LocalStore } from '../storage/local-store.mts';
import type { EntityInput } from '../../../../packages/contracts/storage/local-store.ts';
import type { RuntimeBinding, RuntimePersistence, RuntimeRun, VisibleMessage,RuntimeCheck } from './codex/coordinator.ts';
import type { StoredEntity } from '../../../../packages/contracts/storage/local-store.ts';
import type {TaskTimeEvent} from '../../../../packages/contracts/time/task-time.ts';
import {projectTaskTime} from '../events/task-time.ts';
import {decodeM1TaskProfile} from '../tasks/task-profile.ts';

const hash = (text: string) => createHash('sha256').update(text).digest('hex');
export const taskScopeDigest=(task:StoredEntity)=>hash(JSON.stringify({projectId:task.projectId,id:task.id,revision:task.revision,data:task.data}));
/** Private binding/run metadata contains no input text or credentials. Visible messages use the session parent. */
export function createRuntimeStoragePorts(store: LocalStore, options: Readonly<{actorId: string;now?:()=>number}>) {
  async function write(projectId: string, entity: EntityInput) {
    const project = await store.project(projectId);
    if (!project) throw Object.assign(new Error('Runtime project is unavailable.'), {code:'runtime_project_missing'});
    const previous = await store.get(projectId,entity.id);
    if (previous && previous.kind !== entity.kind) throw Object.assign(new Error('Runtime entity conflicts.'),{code:'runtime_entity_conflict'});
    if (previous && JSON.stringify(previous.data)===JSON.stringify(entity.data??{}) && previous.body===(entity.body??'') && previous.status===(entity.status??'')) return;
    const revision = previous?.revision??0;
    await store.write({projectId,actorId:options.actorId,expectedAuthorityEpoch:project.authorityEpoch,
      idempotencyKey:`runtime:${entity.id}:${revision}:${hash(JSON.stringify(entity))}`,
      changes:[{expectedRevision:revision,entity}]});
  }
  async function listAll(projectId: string, kind: 'run'|'settings'|'evidence') {
    const rows = [];
    for(let offset=0;offset<100_000;offset+=100) {
      const page=await store.list(projectId,{kind,limit:100,offset}); rows.push(...page);
      if(page.length<100) return rows;
    }
    throw Object.assign(new Error('Runtime history requires narrowing.'),{code:'runtime_history_limit'});
  }
  const bindings = new Map<string,string>();
  function messageEntity(message:VisibleMessage):EntityInput {
    return {id:`runtime-message-${hash(`${message.bindingId}:${message.sourceItemId}`)}`,kind:'message',parentId:message.sessionId,
      body:message.text,status:'committed',data:{...message,text:undefined}};
  }
  async function writeRun(run:RuntimeRun,append:boolean,visibleUserMessage?:VisibleMessage) {
    const project=await store.project(run.projectId);const previous=await store.get(run.projectId,run.id);
    if(!project)throw Object.assign(new Error('Runtime project is unavailable.'),{code:'runtime_project_missing'});
    if(visibleUserMessage&&(visibleUserMessage.projectId!==run.projectId||visibleUserMessage.sessionId!==run.sessionId||visibleUserMessage.bindingId!==run.bindingId
      ||visibleUserMessage.runId!==run.id||visibleUserMessage.role!=='user'||visibleUserMessage.sourceItemId!==`client:${run.clientMessageId}`
      ||visibleUserMessage.revision!==hash(visibleUserMessage.text)||Buffer.byteLength(visibleUserMessage.text)>1024*1024))throw Object.assign(new Error('Canonical user message is invalid.'),{code:'runtime_user_message_invalid'});
    if(append&&previous) {
      const old=previous.data.runtimeRun as RuntimeRun;
      if(old.bindingId!==run.bindingId||old.clientMessageId!==run.clientMessageId||old.inputDigest!==run.inputDigest)throw Object.assign(new Error('Intent conflicts.'),{code:'runtime_intent_conflict'});
      return;
    }
    const sourceId=visibleUserMessage?.sourceItemId??(previous?.data.runtimeRun as RuntimeRun|undefined)?.canonicalUserMessageSourceId;
    if(sourceId)run={...run,canonicalUserMessageSourceId:sourceId};
    const messageChanges=visibleUserMessage?[{expectedRevision:0,entity:messageEntity(visibleUserMessage)}]:[];
    if(!run.taskId) {
      if(!append){await write(run.projectId,{id:run.id,kind:'run',status:run.state,data:{runtimeRun:run}});return;}
      await store.write({projectId:run.projectId,actorId:options.actorId,expectedAuthorityEpoch:project.authorityEpoch,
        idempotencyKey:`runtime-intent:${run.id}:${hash(JSON.stringify({run,visibleUserMessage}))}`,requireIdle:true,
        changes:[{expectedRevision:0,entity:{id:run.id,kind:'run',status:run.state,data:{runtimeRun:run}}},...messageChanges]});return;
    }
    const task=await store.get(run.projectId,run.taskId);const session=await store.get(run.projectId,run.sessionId);
    if(!task||task.kind!=='task'||!session||session.kind!=='session')throw Object.assign(new Error('Task/session is unavailable.'),{code:'runtime_target_missing'});
    const profile=decodeM1TaskProfile(task.data);
    if(append&&(profile.status!=='ready'||profile.risks.includes('recovery_review')||!profile.acceptanceCriteria.length))throw Object.assign(new Error('Task requires review.'),{code:'runtime_target_review_required'});
    if(append&&(task.revision!==run.targetRevision||taskScopeDigest(task)!==run.scopeDigest))throw Object.assign(new Error('Saved task changed.'),{code:'runtime_target_changed'});
    if(!append&&!previous)throw Object.assign(new Error('Intent is missing.'),{code:'runtime_intent_missing'});
    const oldTimeline=Array.isArray(previous?.data.timeline)?previous.data.timeline as TaskTimeEvent[]:[];
    const timeline=[...oldTimeline];
    const all=(await listAll(run.projectId,'run')).filter((row)=>(row.data.runtimeRun as RuntimeRun|undefined)?.taskId===run.taskId)
      .flatMap((row)=>Array.isArray(row.data.timeline)?row.data.timeline as TaskTimeEvent[]:[]);
    if(all.length>=10_000)throw Object.assign(new Error('Time journal is full.'),{code:'runtime_time_limit'});
    const lastStart=timeline.toReversed().find((event)=>event.kind==='interval_started');
    const open=lastStart&&!timeline.some((event)=>event.intervalId===lastStart.intervalId&&event.kind!=='interval_started');
    const now=(options.now??Date.now)();let kind:'interval_started'|'interval_stopped'|'interval_crashed'|undefined;
    if(!append&&run.state==='running'&&!open&&(previous!.data.runtimeRun as RuntimeRun).state!=='recovery_required')kind='interval_started';
    else if(open&&run.state==='recovery_required')kind='interval_crashed';
    else if(open&&['awaiting_approval','completed','failed','interrupted'].includes(run.state))kind='interval_stopped';
    if(kind) {
      const seq=Math.max(0,...all.map((event)=>event.seq))+1;
      const base={projectId:run.projectId,taskId:run.taskId,eventId:`${run.id}:time:${seq}`,seq,
        intervalId:kind==='interval_started'?`${run.id}:interval:${seq}`:lastStart!.intervalId,
        runId:run.id,actorId:options.actorId,source:'runtime_observation',atMs:now};
      timeline.push(kind==='interval_stopped'?{...base,kind,reason:run.state==='awaiting_approval'?'pause':'finished'}:{...base,kind});
    }
    const combined=[...all.filter((event)=>event.runId!==run.id),...timeline];
    const projection=projectTaskTime({projectId:run.projectId,taskId:run.taskId},combined);
    let actual=profile.actual;
    if(combined.length) {
      const start=Math.min(...combined.filter((event)=>event.kind==='interval_started').map((event)=>event.atMs));
      const end=Math.max(...combined.filter((event)=>event.kind==='interval_stopped').map((event)=>event.atMs));
      actual={startedAt:new Date(start).toISOString(),endedAt:projection.actualDurationMs===null?null:new Date(end).toISOString(),
        durationSeconds:projection.actualDurationMs===null?null:Math.floor(projection.actualDurationMs/1000)};
    }
    const data={runtimeRun:run,timeline};
    if(previous&&JSON.stringify(previous.data)===JSON.stringify(data))return;
    await store.write({projectId:run.projectId,actorId:options.actorId,expectedAuthorityEpoch:project.authorityEpoch,
      idempotencyKey:`runtime-transition:${run.id}:${previous?.revision??0}:${hash(JSON.stringify(data))}`,
      ...(append?{requireIdle:true as const}:{}),changes:[
        {expectedRevision:task.revision,entity:{id:task.id,kind:'task',data:{...profile,status:append?'in_progress':profile.status,actual,sessionIds:[...new Set([...profile.sessionIds,run.sessionId])]}}},
        {expectedRevision:previous?.revision??0,entity:{id:run.id,kind:'run',status:run.state,data}},
        ...messageChanges,
      ]});
  }
  let pendingWrites=Promise.resolve();
  function saveRun(run:RuntimeRun,append:boolean,visibleUserMessage?:VisibleMessage) {
    const pending=pendingWrites.then(()=>writeRun(run,append,visibleUserMessage));pendingWrites=pending.catch(()=>{});return pending;
  }
  const ports: RuntimePersistence = {
    async saveBinding(binding) {
      const session = await store.get(binding.projectId,binding.sessionId);
      if(!session) await write(binding.projectId,{id:binding.sessionId,kind:'session',title:'Runtime session',data:{}});
      else if(session.kind!=='session') throw Object.assign(new Error('Runtime session conflicts.'),{code:'runtime_session_conflict'});
      await write(binding.projectId,{id:`runtime-binding-${binding.id}`,kind:'settings',data:{runtimeBinding:binding}});
      bindings.set(binding.id,binding.projectId);
    },
    async findRun(bindingId,clientMessageId) {
      const projectId=bindings.get(bindingId);
      if(!projectId) return null;
      const row=(await listAll(projectId,'run')).find((row)=>row.data.runtimeRun
        && (row.data.runtimeRun as RuntimeRun).bindingId===bindingId && (row.data.runtimeRun as RuntimeRun).clientMessageId===clientMessageId);
      return row?structuredClone(row.data.runtimeRun as RuntimeRun):null;
    },
    async appendIntent(run,visibleUserMessage) { await saveRun(run,true,visibleUserMessage); },
    async updateRun(run) { await saveRun(run,false); },
    async saveVisibleMessage(message: VisibleMessage) {
      await write(message.projectId,messageEntity(message));
    },
    async saveCheck(check:RuntimeCheck) {
      await write(check.projectId,{id:`runtime-check-${check.id}`,kind:'evidence',parentId:check.taskId,
        status:check.status,coverage:'partial',data:{category:'runtime_item_outcome',observed:true,receipt:check}});
    },
    async loadChecks(projectId,bindingId) {
      return (await listAll(projectId,'evidence')).filter((row)=>row.data.category==='runtime_item_outcome'
        &&(row.data.receipt as RuntimeCheck|undefined)?.bindingId===bindingId).slice(-64).map((row)=>row.data.receipt as RuntimeCheck);
    },
  };
  return {...ports,
    async recoverable(projectId: string) {
      const bindingRows=await listAll(projectId,'settings');
      const runRows=await listAll(projectId,'run');
      const results:Array<{binding:RuntimeBinding;run:RuntimeRun}>=[];
      for(const row of runRows) {
        const run=row.data.runtimeRun as RuntimeRun|undefined;
        if(!run||['completed','failed','interrupted'].includes(run.state)) continue;
        const binding=bindingRows.map((row)=>row.data.runtimeBinding as RuntimeBinding|undefined).find((binding)=>binding?.id===run.bindingId);
        if(!binding) throw Object.assign(new Error('Runtime binding is missing.'),{code:'runtime_recovery_incomplete'});
        bindings.set(binding.id,projectId); results.push({binding:structuredClone(binding),run:structuredClone(run)});
      }
      return results;
    },
  };
}
