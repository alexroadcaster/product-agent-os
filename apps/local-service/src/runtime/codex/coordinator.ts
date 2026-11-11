import { createHash, randomUUID } from 'node:crypto';
import { bindProject } from '../../adapters/project-sources.ts';
import { mapRuntimeEvent, mapTurnAccepted } from '../../../../../packages/contracts/runtime/events.ts';
import type { RpcMessage, RuntimeRpc } from './stdio-rpc.ts';
import type {MessageStreamRedactor} from '../message-stream.mts';
import {m1Recipe,quotedTaskInput,type RecipeMetadata,type SavedTaskContext} from '../m1-recipe.mts';
import {isAbsolute,relative,resolve} from 'node:path';

export type RuntimeMode = 'discussion' | 'planning' | 'execution';
export type RunState = 'dispatching' | 'running' | 'awaiting_approval' | 'interrupt_requested'
  | 'completed' | 'failed' | 'interrupted' | 'recovery_required';
export type RuntimeBinding = Readonly<{
  id: string; projectId: string; sessionId: string; accountId: string; workspaceRoot: string;
  directoryIdentity: string; mode: RuntimeMode; profileId: string; generation: string; threadId: string;
  recipe?:RecipeMetadata;
}>;
export type RuntimeRun = {
  id: string; bindingId: string; projectId: string; sessionId: string; accountId: string;
  generation: string; threadId: string; turnId: string | null; clientMessageId: string; inputDigest: string;
  taskId: string | null; scopeDigest: string | null; state: RunState;
  targetRevision?: number;
  canonicalUserMessageSourceId?:string;
};
export type VisibleMessage = Readonly<{
  projectId: string; sessionId: string; bindingId: string; runId: string; sourceItemId: string;
  revision: string; role: 'user' | 'assistant'; text: string;
}>;
export type RuntimeCheck=Readonly<{id:string;projectId:string;bindingId:string;sessionId:string;runId:string;taskId:string|null;itemId:string;itemType:string;
 status:string;outcome?:string;coverage:'runtime_reported';reason?:string}>;
export type RuntimePersistence = Readonly<{
  findRun: (bindingId: string, clientMessageId: string) => Promise<RuntimeRun | null>;
  saveBinding: (binding: RuntimeBinding) => Promise<void>;
  appendIntent: (run: RuntimeRun,visibleUserMessage?:VisibleMessage) => Promise<void>;
  updateRun: (run: RuntimeRun) => Promise<void>;
  saveVisibleMessage: (message: VisibleMessage) => Promise<void>;
  saveCheck?:(check:RuntimeCheck)=>Promise<void>;
  loadChecks?:(projectId:string,bindingId:string)=>Promise<RuntimeCheck[]>;
}>;
type BindingInput = Omit<RuntimeBinding, 'id' | 'directoryIdentity' | 'generation' | 'threadId'|'recipe'>;
type SendInput = Readonly<{ bindingId: string; clientMessageId: string; input: string; taskId?: string; scopeDigest?: string;targetRevision?:number;taskContext?:SavedTaskContext }>;
export type VisibleDraft={runId:string;sourceItemId:string;role:'assistant';phase:'final_answer';text:string;revision:number;status:'streaming'|'completed'|'interrupted'|'recovery_required'};
export type VisibleFileChange={kind:'actual'|'proposed'|'external';path:string;previousPath?:string;diff?:string;operation?:string;coverage:'partial'|'unavailable';reason:string};
type Approval = { requestId: string | number; runId: string; bindingId: string; generation: string;
  itemId: string; expiresAt: number; kind: 'command' | 'file'; state: 'pending' | 'response_sent' | 'answered_or_cleared';
  reviewable: boolean; details: Readonly<{command?:string;reason?:string;changes?:unknown}>;
  decision?: 'accept' | 'decline' | 'cancel' };
type CoordinatorOptions = Readonly<{
  rpc: RuntimeRpc; persistence: RuntimePersistence;
  isEnabled?: () => boolean; authorizeDispatch?: (binding: RuntimeBinding) => boolean | Promise<boolean>;
  onEvent?: (event: RpcMessage) => void;
  redact?: (text: string) => string;
  createStreamRedactor?:()=>MessageStreamRedactor;
  now?: () => number;
  approvalTtlMs?: number;
  dynamicTools?: readonly Readonly<{type:'function';name:string;description:string;inputSchema:unknown}>[];
  domainTool?: (request: Readonly<{ tool: string; arguments: unknown; binding: RuntimeBinding; run: RuntimeRun; requestId: string | number }>) => Promise<unknown>;
}>;

export class RuntimeCoordinatorError extends Error {
  readonly code: string;
  constructor(code: string) { super('The scoped runtime operation is unavailable.'); this.code = code; }
}
const terminal = new Set<RunState>(['completed', 'failed', 'interrupted']);
const tools = new Set(['task_read', 'task_propose', 'task_patch', 'task_comment', 'task_link', 'evidence_reference']);
const record = (value: unknown): RpcMessage => value !== null && typeof value === 'object' && !Array.isArray(value) ? value as RpcMessage : {};
const digest = (text: string): string => createHash('sha256').update(text).digest('hex');
const cloneRun = (run: RuntimeRun): RuntimeRun => ({ ...run });

/** One coordinator owns the process generation and dispatch lease. Uncertain operations require explicit reconciliation. */
export function createRuntimeCoordinator(options: CoordinatorOptions) {
  const { rpc, persistence } = options;
  const bindings = new Map<string, RuntimeBinding>();
  const sessions = new Map<string, { hash: string; promise: Promise<RuntimeBinding> }>();
  const runs = new Map<string, RuntimeRun>();
  const sends = new Map<string, { hash: string; promise: Promise<RuntimeRun> }>();
  const approvals = new Map<string, Approval>();
  const interrupted = new Map<string, Promise<RuntimeRun>>();
  const fileChanges = new Map<string,unknown>();
  const visibleChanges=new Map<string,{bindingId:string;changes:VisibleFileChange[]}>();
  const streams=new Map<string,{bindingId:string;runId:string;itemId:string;redactor:MessageStreamRedactor}>();
  const drafts=new Map<string,{bindingId:string;bytes:number;value:VisibleDraft}>();
  const phaseStates=new Map<string,'not_observed'|'phase_unavailable'|'final_answer_observed'>();
  const checks=new Map<string,RuntimeCheck>();
  let draftBytes=0;
  let active: RuntimeRun | undefined;
  let queue = Promise.resolve();
  let suspended=false;
  let disconnected=false;
  const operations=new Set<Promise<unknown>>();
  function track<T>(operation:Promise<T>):Promise<T> {
    operations.add(operation);void operation.then(()=>operations.delete(operation),()=>operations.delete(operation));return operation;
  }

  function enabled(checkConnection=true): void {
    if(suspended)throw new RuntimeCoordinatorError('runtime_stopping');
    if(checkConnection&&disconnected)throw new RuntimeCoordinatorError('runtime_disconnected');
    if (!options.isEnabled?.()) throw new RuntimeCoordinatorError('runtime_unverified');
  }
  function bindingById(id: string): RuntimeBinding {
    const binding = bindings.get(id);
    if (!binding) throw new RuntimeCoordinatorError('binding_not_found');
    return binding;
  }
  function emit(event: RpcMessage): void { options.onEvent?.(event); }
  function appendDraft(run:RuntimeRun,itemId:string,text:string) {
    if(!text)return;
    const key=`${run.id}:${itemId}`;const draft=drafts.get(key);
    if(!draft)throw new RuntimeCoordinatorError('stream_not_correlated');
    const bytes=Buffer.byteLength(text);if(draftBytes+bytes>1024*1024)throw new RuntimeCoordinatorError('visible_stream_limit');
    draftBytes+=bytes;draft.bytes+=bytes;draft.value.text+=text;draft.value.revision++;
    emit({kind:'message_delta',bindingId:run.bindingId,runId:run.id,itemId,text,revision:draft.value.revision,phase:'final_answer'});
  }
  function finishStream(run:RuntimeRun,itemId:string,status:VisibleDraft['status']) {
    const key=`${run.id}:${itemId}`;const stream=streams.get(key);
    if(stream){streams.delete(key);try{appendDraft(run,itemId,stream.redactor.finish());}catch{status='recovery_required';}}
    const draft=drafts.get(key);if(draft){draft.value.status=status;draft.value.revision++;}
  }
  function finishRunStreams(run:RuntimeRun,status:VisibleDraft['status']) {
    for(const stream of [...streams.values()])if(stream.runId===run.id)finishStream(run,stream.itemId,status);
  }
  function projectChanges(binding:RuntimeBinding,item:RpcMessage,actual:boolean) {
    if(typeof item.id!=='string'||!Array.isArray(item.changes))return;
    const key=`${binding.id}:${item.id}`;
    if(!visibleChanges.has(key)&&visibleChanges.size>=64)return;
    let bytes=0;const changes:VisibleFileChange[]=[];
    const scrub=options.redact??((text:string)=>text);
    for(const raw of item.changes.slice(0,64)) {
      const change=record(raw);const kind=record(change.kind);if(typeof change.path!=='string'||change.path.length>4096)continue;
      const previous=typeof kind.move_path==='string'?change.path:undefined;
      const destination=typeof kind.move_path==='string'?kind.move_path:change.path;
      if(destination.length>4096||!['add','delete','update'].includes(String(kind.type))||typeof change.diff!=='string')continue;
      const scoped=(path:string)=>{const rel=relative(binding.workspaceRoot,resolve(binding.workspaceRoot,path));return !rel.startsWith('..')&&!isAbsolute(rel);};
      const external=!scoped(destination)||(previous!==undefined&&!scoped(previous));
      let diff=typeof change.diff==='string'&&!external?scrub(change.diff):undefined;
      const truncated=diff!==undefined&&Buffer.byteLength(diff)>16*1024;
      if(truncated)diff=undefined;
      const projected:VisibleFileChange={kind:external?'external':actual?'actual':'proposed',path:scrub(destination),
        previousPath:previous===undefined?undefined:scrub(previous),diff,operation:kind.type==='update'&&previous?'rename':typeof kind.type==='string'?kind.type:undefined,
        coverage:external?'unavailable':'partial',reason:external?'outside_bound_workspace':truncated?'diff_exceeds_display_limit':actual?'runtime_reported_filesystem_unverified'
          :item.status==='failed'||item.status==='declined'?`runtime_reported_${item.status}_changes_unverified`:'runtime_proposal'};
      bytes+=Buffer.byteLength(JSON.stringify(projected));if(bytes>64*1024)break;changes.push(projected);
    }
    visibleChanges.set(key,{bindingId:binding.id,changes});
  }
  async function persist(run: RuntimeRun): Promise<void> {
    await persistence.updateRun(cloneRun(run));
    emit({ kind: 'run', run: cloneRun(run) });
  }
  async function recovery(run: RuntimeRun): Promise<void> {
    if (terminal.has(run.state)) return;
    finishRunStreams(run,'recovery_required');
    run.state = 'recovery_required';
    for (const approval of approvals.values()) {
      if (approval.runId === run.id) approval.state = 'answered_or_cleared';
    }
    await persist(run);
  }
  async function validateWorkspace(binding: RuntimeBinding): Promise<void> {
    const current = await bindProject(binding.projectId, binding.workspaceRoot);
    if (current.directoryIdentity !== binding.directoryIdentity || current.workspaceRoot !== binding.workspaceRoot) {
      throw new RuntimeCoordinatorError('workspace_changed');
    }
  }
  // Transport correlation precedes this serialized reducer; only final visible content reaches persistence.
  async function applyEvent(message: RpcMessage): Promise<void> {
    const run = active;
    if (!run || terminal.has(run.state)) return;
    const params = record(message.params);
    if (params.threadId !== run.threadId) return;
    if (run.generation !== rpc.generation) { await recovery(run); return; }
    const binding = bindingById(run.bindingId);
    const method = message.method;
    // These typed channels contain hidden reasoning or raw tool output, never visible assistant text.
    if(['item/reasoning/summaryTextDelta','item/reasoning/summaryPartAdded','item/reasoning/textDelta',
      'item/commandExecution/outputDelta','item/fileChange/outputDelta'].includes(String(method)))return;
    if(suspended&&message.id!==undefined) {
      if(typeof message.id==='string'||typeof message.id==='number')rpc.respondError(message.id);
      return;
    }
    if(method==='item/started'&&params.turnId===run.turnId) {
      const item=record(params.item);
      if(item.type==='agentMessage'&&typeof item.id==='string') {
        if(item.phase==='final_answer') {
          if(phaseStates.get(binding.id)!=='phase_unavailable')phaseStates.set(binding.id,'final_answer_observed');
          const key=`${run.id}:${item.id}`;
          if(options.createStreamRedactor&&!streams.has(key)&&!drafts.has(key)) {
            if(streams.size>=16||drafts.size>=16||item.id.length>256)throw new RuntimeCoordinatorError('visible_stream_limit');
            streams.set(key,{bindingId:binding.id,runId:run.id,itemId:item.id,redactor:options.createStreamRedactor()});
            drafts.set(key,{bindingId:binding.id,bytes:0,value:{runId:run.id,sourceItemId:item.id,role:'assistant',phase:'final_answer',text:'',revision:0,status:'streaming'}});
          }
        } else if(!['commentary','partial_answer'].includes(String(item.phase)))phaseStates.set(binding.id,'phase_unavailable');
      }
      if(item.type==='fileChange'&&typeof item.id==='string'&&Array.isArray(item.changes)) {
        projectChanges(binding,item,false);
        const encoded=JSON.stringify(item.changes);
        if(Buffer.byteLength(encoded)<=64*1024)fileChanges.set(item.id,JSON.parse((options.redact??((text)=>text))(encoded)));
      }
    }
    if (method === 'item/tool/call' && (typeof message.id === 'string' || typeof message.id === 'number')) {
      if (params.turnId !== run.turnId || typeof params.tool !== 'string' || !tools.has(params.tool)
        || !options.dynamicTools?.some((tool)=>tool.name===params.tool)
        || (binding.mode !== 'execution' && !['task_read', 'task_propose'].includes(params.tool)) || !options.domainTool) {
        rpc.respondError(message.id); return;
      }
      try {
        await validateWorkspace(binding);
        const result = await options.domainTool({ tool: params.tool, arguments: params.arguments, binding, run: cloneRun(run), requestId: message.id });
        rpc.respond(message.id, {contentItems:[{type:'inputText',text:JSON.stringify(result ?? null)}],success:true});
      } catch { rpc.respondError(message.id); }
      return;
    }
    if (method === 'item/tool/requestUserInput' || method === 'item/permissions/requestApproval') {
      if (typeof message.id === 'string' || typeof message.id === 'number') rpc.respondError(message.id);
      return;
    }
    // The durable original user instruction is authoritative; provider echoes may contain the quoted recipe context.
    if(method==='item/completed'&&run.canonicalUserMessageSourceId&&record(params.item).type==='userMessage')return;
    const event = mapRuntimeEvent(message);
    if (event.kind === 'recovery_required') { await recovery(run); return; }
    if (event.kind === 'turn_started') {
      if (run.turnId && run.turnId !== event.turnId) { await recovery(run); return; }
      run.turnId = event.turnId;
      if (run.state === 'dispatching') { run.state = 'running'; await persist(run); }
      return;
    }
    if ('turnId' in event && event.turnId !== run.turnId) { await recovery(run); return; }
    if (event.kind === 'approval_requested') {
      const denied = event.approval === 'permissions' || binding.mode !== 'execution'
        || params.grantRoot != null || params.additionalPermissions != null || params.networkApprovalContext != null
        || params.proposedExecpolicyAmendment != null || params.proposedNetworkPolicyAmendment != null
        || params.proposedNetworkPolicyAmendments != null || params.environmentId != null
        || (params.kind != null && params.kind !== 'command')
        || (params.cwd != null && params.cwd !== binding.workspaceRoot);
      if (denied) { rpc.respond(event.requestId, { decision: 'decline' }); return; }
      const key = `${run.generation}:${typeof event.requestId}:${event.requestId}`;
      if (approvals.has(key)) return;
      const approval: Approval = { requestId: event.requestId, runId: run.id, bindingId: binding.id, generation: run.generation,
        itemId: event.itemId, expiresAt: (options.now ?? Date.now)() + (options.approvalTtlMs ?? 300_000),
        reviewable:event.approval==='command'?typeof params.command==='string'&&params.command.length>0&&params.command.length<=16_384:fileChanges.has(event.itemId),
        details:{command:typeof params.command==='string'?(options.redact??((text)=>text))(params.command).slice(0,16_384):undefined,
          reason:typeof params.reason==='string'?(options.redact??((text)=>text))(params.reason).slice(0,4096):undefined,
          changes:fileChanges.get(event.itemId)},
        kind: event.approval as 'command' | 'file', state: 'pending' };
      approvals.set(key, approval); run.state = 'awaiting_approval';
      await persist(run); emit({ kind: 'approval', approval: { ...approval } }); return;
    }
    if (event.kind === 'request_resolved') {
      const approval = approvals.get(`${run.generation}:${typeof event.requestId}:${event.requestId}`);
      if (approval && approval.runId === run.id) {
        approval.state = 'answered_or_cleared'; emit({ kind: 'approval', approval: { ...approval } });
        if (run.state === 'awaiting_approval'&&![...approvals.values()].some((entry)=>entry.runId===run.id&&entry.state!=='answered_or_cleared')) { run.state = 'running'; await persist(run); }
      }
      return;
    }
    if(method==='item/agentMessage/delta') {
      if(params.turnId!==run.turnId){await recovery(run);return;}
      const stream=typeof params.itemId==='string'?streams.get(`${run.id}:${params.itemId}`):undefined;
      if(stream&&typeof params.delta==='string')appendDraft(run,stream.itemId,stream.redactor.push(params.delta));
    }
    if(event.kind==='item_ended'&&event.itemType==='fileChange')projectChanges(binding,record(params.item),event.itemStatus==='completed');
    if(event.kind==='item_ended'&&event.itemStatus!==null) {
      const item=record(params.item);const exit=Number.isSafeInteger(item.exitCode)?Number(item.exitCode):null;
      const check:RuntimeCheck={id:digest(`${run.id}:${event.itemType}:${event.itemId}`),projectId:run.projectId,bindingId:binding.id,sessionId:run.sessionId,
        runId:run.id,taskId:run.taskId,itemId:event.itemId,itemType:event.itemType,status:event.itemStatus,
        outcome:event.itemType==='commandExecution'&&exit!==null?`exit_${exit}`:event.itemStatus,
        coverage:'runtime_reported',reason:'runtime_item_receipt_not_manual_acceptance'};
      await persistence.saveCheck?.(check);
      checks.delete(check.id);checks.set(check.id,check);if(checks.size>64)checks.delete(checks.keys().next().value!);
      emit({kind:'check',check});
    }
    if (event.kind === 'item_ended' && ['agentMessage', 'userMessage'].includes(event.itemType)) {
      const item = record(params.item);
      if(event.itemType==='agentMessage'&&drafts.has(`${run.id}:${event.itemId}`)&&item.phase!=='final_answer'){await recovery(run);return;}
      if(event.itemType==='agentMessage')finishStream(run,event.itemId,'completed');
      if (event.itemType === 'agentMessage' && item.phase !== 'final_answer') return;
      const role = event.itemType === 'agentMessage' ? 'assistant' : 'user';
      const raw = typeof item.text === 'string' ? item.text : Array.isArray(item.content)
        ? item.content.map((part) => record(part).text).filter((part): part is string => typeof part === 'string').join('') : '';
      const text = (options.redact ?? ((value) => value))(raw);
      if (Buffer.byteLength(text) > 1024 * 1024) { await recovery(run); return; }
      const committed: VisibleMessage = { projectId: binding.projectId, sessionId: binding.sessionId, bindingId: binding.id,
        runId: run.id, sourceItemId: event.itemId, revision: digest(text), role, text };
      await persistence.saveVisibleMessage(committed);
      emit({ kind: 'message_committed', message: committed });
      const key=`${run.id}:${event.itemId}`;const draft=drafts.get(key);if(draft){draftBytes-=draft.bytes;drafts.delete(key);}
    }
    if (event.kind === 'turn_ended') {
      finishRunStreams(run,event.outcome==='completed'?'completed':'interrupted');
      run.state = event.outcome;
      fileChanges.clear();
      for (const approval of approvals.values()) if (approval.runId === run.id) approval.state = 'answered_or_cleared';
      try { await persist(run); active = undefined; }
      catch { run.state = 'recovery_required'; throw new RuntimeCoordinatorError('persistence_unavailable'); }
    }
  }
  const unsubscribe=rpc.subscribe((message) => {
    queue = queue.then(() => applyEvent(message)).catch(async () => { if (active) await recovery(active); });
  });
  const unsubscribeClosed=rpc.onClosed(() => { disconnected=true;queue = queue.then(async () => { if (active) await recovery(active); }).catch(() => {
    if (active) active.state = 'recovery_required';
  }); });

  // A mode creates a new thread; grants and policies never migrate from a previous binding.
  async function openBinding(input: BindingInput): Promise<RuntimeBinding> {
    enabled();
    if(active)throw new RuntimeCoordinatorError('runtime_busy');
    if (!['discussion', 'planning', 'execution'].includes(input.mode) || !input.accountId || !input.sessionId || !input.profileId) {
      throw new RuntimeCoordinatorError('binding_invalid');
    }
    const key = `${input.sessionId}:${input.mode}`;
    const hash = digest(JSON.stringify(input));
    const previous = sessions.get(key);
    if (previous) {
      if (previous.hash !== hash) throw new RuntimeCoordinatorError('binding_conflict');
      return previous.promise;
    }
    const promise = track((async () => {
      const workspace = await bindProject(input.projectId, input.workspaceRoot);
      enabled();if(active)throw new RuntimeCoordinatorError('runtime_busy');
      const permissions = input.mode === 'execution' ? 'paos_execution' : 'paos_readonly';
      const recipe=m1Recipe(input.mode);
      const dynamicTools=(options.dynamicTools??[]).filter((tool)=>tools.has(tool.name)
        && (input.mode==='execution'||['task_read','task_propose'].includes(tool.name)));
      const result = await rpc.request('thread/start', { cwd: workspace.workspaceRoot, runtimeWorkspaceRoots: [workspace.workspaceRoot],
        permissions, approvalPolicy: input.mode === 'execution' ? 'on-request' : 'never',
        allowProviderModelFallback: false, ephemeral: false, historyMode: 'paginated',dynamicTools,environments:[],developerInstructions:recipe.developerInstructions });
      const thread = record(result.thread); const policy = record(result.sandbox);
      if (typeof thread.id !== 'string' || result.cwd !== workspace.workspaceRoot || policy.networkAccess !== false
        || policy.type !== (input.mode === 'execution' ? 'workspaceWrite' : 'readOnly')
        || record(result.activePermissionProfile).id !== permissions
        || result.approvalPolicy !== (input.mode === 'execution' ? 'on-request' : 'never')
        || JSON.stringify(result.runtimeWorkspaceRoots) !== JSON.stringify([workspace.workspaceRoot])
        || (input.mode === 'execution' && (!Array.isArray(policy.writableRoots) || policy.writableRoots.length !== 0
          || policy.excludeSlashTmp !== true || policy.excludeTmpdirEnvVar !== true))) {
        throw new RuntimeCoordinatorError('runtime_policy_mismatch');
      }
      const binding: RuntimeBinding = { ...input, workspaceRoot: workspace.workspaceRoot,
        directoryIdentity: workspace.directoryIdentity, id: randomUUID(), generation: rpc.generation, threadId: thread.id,recipe:recipe.metadata };
      enabled();if(active)throw new RuntimeCoordinatorError('runtime_busy');
      await persistence.saveBinding(binding);enabled();if(active)throw new RuntimeCoordinatorError('runtime_busy');
      bindings.set(binding.id, binding); return binding;
    })());
    sessions.set(key, { hash, promise });
    void promise.catch(()=>{if(sessions.get(key)?.promise===promise)sessions.delete(key);});
    return promise;
  }

  // Cache the promise before another caller can dispatch the same user-message identity.
  function send(input: SendInput): Promise<RuntimeRun> {
    // Existing message receipts/recovery leases remain addressable after EOF; dispatch rechecks the transport.
    try { enabled(false); } catch (error) { return Promise.reject(error); }
    const binding = bindingById(input.bindingId);
    if (typeof input.clientMessageId !== 'string' || !input.clientMessageId || typeof input.input !== 'string'
      || !input.input.trim() || Buffer.byteLength(input.input) > 256 * 1024) {
      return Promise.reject(new RuntimeCoordinatorError('input_invalid'));
    }
    const hash = digest(JSON.stringify({ input: input.input, taskId: input.taskId, scopeDigest: input.scopeDigest,taskContext:input.taskContext }));
    const key = `${binding.id}:${input.clientMessageId}`;
    const previous = sends.get(key);
    if (previous) return previous.hash === hash ? previous.promise : Promise.reject(new RuntimeCoordinatorError('message_conflict'));
    const promise = track(dispatch(binding, input, hash));
    sends.set(key, { hash, promise }); return promise;
  }
  // Reserve synchronously; an uncertain dispatch retains this global lease until reconciliation.
  async function dispatch(binding: RuntimeBinding, input: SendInput, hash: string): Promise<RuntimeRun> {
    if (active) throw new RuntimeCoordinatorError('runtime_busy');
    if (binding.generation !== rpc.generation) throw new RuntimeCoordinatorError('binding_stale');
    if (binding.mode === 'execution' && (!input.taskId || !input.scopeDigest)) throw new RuntimeCoordinatorError('scope_required');
    if(binding.mode==='execution'&&(!input.taskContext||input.taskContext.taskId!==input.taskId||input.taskContext.revision!==input.targetRevision))throw new RuntimeCoordinatorError('task_context_required');
    const quoted=quotedTaskInput(input.taskContext,input.input,options.redact??((text)=>text));
    const run: RuntimeRun = { id: randomUUID(), bindingId: binding.id, projectId: binding.projectId, sessionId: binding.sessionId,
      accountId: binding.accountId, generation: rpc.generation, threadId: binding.threadId, turnId: null,
      clientMessageId: input.clientMessageId, inputDigest: hash, taskId: input.taskId ?? null, scopeDigest: input.scopeDigest ?? null,
      targetRevision:input.targetRevision,canonicalUserMessageSourceId:`client:${input.clientMessageId}`,state: 'dispatching' };
    const canonicalText=(options.redact??((text)=>text))(input.input);
    if(Buffer.byteLength(canonicalText)>1024*1024)throw new RuntimeCoordinatorError('visible_message_limit');
    const canonicalUserMessage:VisibleMessage={projectId:binding.projectId,sessionId:binding.sessionId,bindingId:binding.id,runId:run.id,
      sourceItemId:run.canonicalUserMessageSourceId!,revision:digest(canonicalText),role:'user',text:canonicalText};
    active = run;
    streams.clear();drafts.clear();draftBytes=0;visibleChanges.clear();phaseStates.set(binding.id,'not_observed');
    let dispatched = false;
    try {
      const old = await persistence.findRun(binding.id, input.clientMessageId);
      if (old) {
        if (old.inputDigest !== hash) throw new RuntimeCoordinatorError('message_conflict');
        runs.set(old.id, old); active = terminal.has(old.state) ? undefined : { ...old, state: 'recovery_required' };
        if (active) { runs.set(active.id, active); await persist(active); }
        return cloneRun(active ?? old);
      }
      if (!await options.authorizeDispatch?.(binding)) throw new RuntimeCoordinatorError('connection_unavailable');
      enabled();
      await validateWorkspace(binding);
      enabled();
      await persistence.appendIntent(cloneRun(run),canonicalUserMessage); runs.set(run.id, run);
      dispatched = true;
      // Shutdown/EOF can win any awaited check. A committed intent retains recovery, never a late dispatch.
      enabled();
      emit({kind:'message_committed',message:canonicalUserMessage});
      const result = await rpc.request('turn/start', { threadId: binding.threadId, input: [{ type: 'text', text: quoted }],
        cwd: binding.workspaceRoot,runtimeWorkspaceRoots:[binding.workspaceRoot],environments:[], permissions: binding.mode === 'execution' ? 'paos_execution' : 'paos_readonly',
        approvalPolicy: binding.mode === 'execution' ? 'on-request' : 'never', clientUserMessageId: input.clientMessageId });
      const accepted = mapTurnAccepted(binding.threadId, result);
      if (accepted.kind !== 'turn_accepted' || (run.turnId && run.turnId !== accepted.turnId)) {
        await recovery(run); return cloneRun(run);
      }
      run.turnId = accepted.turnId;
      if (run.state === 'dispatching') run.state = 'running';
      await persist(run); return cloneRun(run);
    } catch (error) {
      if (dispatched) { await recovery(run); return cloneRun(run); }
      if (active === run) active = undefined;
      throw error;
    }
  }

  function answerApproval(input: Readonly<{ bindingId: string; runId: string; generation: string;
    requestId: string | number; decision: 'accept' | 'decline' | 'cancel' }>) {
    return track(resolveApproval(input));
  }
  function liveApprovalRun(approval:Approval):RuntimeRun {
    enabled();const current=active;
    if(!current||current.id!==approval.runId||current.state==='recovery_required'||terminal.has(current.state)
      ||approval.state==='answered_or_cleared'||approval.generation!==rpc.generation||(options.now??Date.now)()>=approval.expiresAt)throw new RuntimeCoordinatorError('approval_stale');
    return current;
  }
  async function resolveApproval(input: Readonly<{bindingId:string;runId:string;generation:string;requestId:string|number;decision:'accept'|'decline'|'cancel'}>) {
    enabled();
    const approval = approvals.get(`${input.generation}:${typeof input.requestId}:${input.requestId}`);
    if (!approval || approval.bindingId !== input.bindingId || approval.runId !== input.runId
      || input.generation !== rpc.generation || active?.id !== input.runId || active.state === 'recovery_required') {
      throw new RuntimeCoordinatorError('approval_stale');
    }
    if (!['accept', 'decline', 'cancel'].includes(input.decision)) throw new RuntimeCoordinatorError('approval_invalid');
    if (approval.decision) {
      if (approval.decision !== input.decision) throw new RuntimeCoordinatorError('approval_conflict');
      return { ...approval };
    }
    if(input.decision==='accept'&&!approval.reviewable)throw new RuntimeCoordinatorError('approval_details_unavailable');
    if (approval.state !== 'pending' || (options.now ?? Date.now)() >= approval.expiresAt) throw new RuntimeCoordinatorError('approval_stale');
    const binding=bindingById(input.bindingId);
    if(!await options.authorizeDispatch?.(binding))throw new RuntimeCoordinatorError('connection_unavailable');
    await validateWorkspace(binding);
    // Approval resolution, TTL, EOF, or shutdown can change while authority/root checks are pending.
    const run=liveApprovalRun(approval);
    if(approval.decision) {
      if(approval.decision!==input.decision)throw new RuntimeCoordinatorError('approval_conflict');return {...approval};
    }
    approval.decision = input.decision; approval.state = 'response_sent';
    try { rpc.respond(input.requestId, { decision: input.decision }); }
    catch { if(active===run&&!terminal.has(run.state))await recovery(run);throw new RuntimeCoordinatorError('approval_outcome_unknown'); }
    emit({ kind: 'approval', approval: { ...approval } }); return { ...approval };
  }
  function interrupt(input: Readonly<{ bindingId: string; runId: string }>): Promise<RuntimeRun> {
    if(suspended)return Promise.reject(new RuntimeCoordinatorError('runtime_stopping'));
    const run = active;
    if (!run || run.id !== input.runId || run.bindingId !== input.bindingId || !run.turnId) {
      return Promise.reject(new RuntimeCoordinatorError('run_not_interruptible'));
    }
    if (interrupted.has(run.id)) return interrupted.get(run.id)!;
    const promise = track((async () => {
      run.state = 'interrupt_requested'; await persist(run);
      if(active!==run||terminal.has(run.state))return cloneRun(run);
      if(suspended||disconnected){await recovery(run);return cloneRun(run);}
      try { await rpc.request('turn/interrupt', { threadId: run.threadId, turnId: run.turnId }); }
      catch { if(active===run&&!terminal.has(run.state))await recovery(run); }
      return cloneRun(run);
    })());
    interrupted.set(run.id, promise); return promise;
  }
  function reconcile(input: Readonly<{bindingId:string;accountId:string}>):Promise<RuntimeRun|null> {
    return track(reconcileRun(input));
  }
  async function reconcileRun(input: Readonly<{ bindingId: string; accountId: string }>): Promise<RuntimeRun | null> {
    enabled();
    const binding = bindingById(input.bindingId);
    if (binding.accountId !== input.accountId) throw new RuntimeCoordinatorError('account_mismatch');
    const run = active;
    if (!run || run.bindingId !== binding.id) return null;
    await validateWorkspace(binding);
    enabled();if(active!==run)return cloneRun(run);
    const result = await rpc.request('thread/read', { threadId: run.threadId, includeTurns: true });
    if(active!==run)return cloneRun(run);
    const thread = record(result.thread);
    const turn = Array.isArray(thread.turns) ? thread.turns.map(record).find((entry) => entry.id === run.turnId) : undefined;
    if (thread.id === run.threadId && turn && ['completed', 'failed', 'interrupted'].includes(String(turn.status))) {
      run.state = turn.status as RunState; await persist(run); active = undefined;
    } else await recovery(run);
    return cloneRun(run);
  }

  /** Restoring durable state only holds the lease. It never resumes a turn or replays an input. */
  async function restoreRecovery(input: Readonly<{binding: RuntimeBinding; run: RuntimeRun; accountId: string}>) {
    if (active) throw new RuntimeCoordinatorError('runtime_busy');
    const {binding, run} = input;
    if (input.accountId !== binding.accountId || run.accountId !== binding.accountId) throw new RuntimeCoordinatorError('account_mismatch');
    if (run.bindingId !== binding.id || run.projectId !== binding.projectId || run.sessionId !== binding.sessionId
      || run.threadId !== binding.threadId || run.generation !== binding.generation || terminal.has(run.state)) {
      throw new RuntimeCoordinatorError('recovery_invalid');
    }
    await validateWorkspace(binding);
    bindings.set(binding.id, {...binding});
    for(const check of await persistence.loadChecks?.(binding.projectId,binding.id)??[])checks.set(check.id,check);
    while(checks.size>64)checks.delete(checks.keys().next().value!);
    active = {...run, state:'recovery_required'}; runs.set(run.id, active);
    await persist(active);
  }

  // Commit uncertain outcomes before the host is allowed to close the process. Failure leaves it alive for retry.
  async function prepareShutdown() {
    suspended=true;
    // Public RPC operations are separate from the incoming event reducer; both must drain before child/store close.
    await Promise.allSettled([...operations]);
    queue=queue.catch(()=>{}).then(async()=>{if(active)await recovery(active);});
    await queue;
  }
  return { openBinding, send, answerApproval, interrupt, reconcile, restoreRecovery,prepareShutdown,
    detach(){unsubscribe();unsubscribeClosed();},
    async flush() { await queue; },
    snapshot(bindingId: string) {
      const binding = bindingById(bindingId);
      const expectedRecipe=m1Recipe(binding.mode).metadata;const recipe=binding.recipe;
      const profile=recipe&&recipe.id===expectedRecipe.id&&recipe.version===expectedRecipe.version&&recipe.role===expectedRecipe.role&&recipe.assignment===expectedRecipe.assignment
        ?expectedRecipe:{id:binding.profileId,version:null,role:null,assignment:null,coverage:'unavailable' as const};
      return { bindingId, projectId: binding.projectId, sessionId: binding.sessionId, mode: binding.mode,
        hasActiveRun:!!active&&!terminal.has(active.state),
        suspended,
        visibleDrafts:[...drafts.values()].filter((draft)=>draft.bindingId===bindingId).map((draft)=>({...draft.value})),
        fileChanges:[...visibleChanges.values()].filter((item)=>item.bindingId===bindingId).flatMap((item)=>item.changes.map((change)=>({...change}))).slice(0,64),
        profile,
        checks:[...checks.values()].filter((check)=>check.bindingId===bindingId).map((check)=>({id:check.id,runId:check.runId,taskId:check.taskId,itemId:check.itemId,itemType:check.itemType,
          status:check.status,outcome:check.outcome,coverage:check.coverage,reason:check.reason})),
        questions:{status:'unsupported' as const,reason:'request_user_input_unsupported'},
        streaming:{policy:'final_answer_only' as const,phaseStatus:phaseStates.get(bindingId)??'not_observed'},
        generation: binding.generation, run: active?.bindingId === bindingId ? cloneRun(active) : null,
        approvals: [...approvals.values()].filter((approval) => approval.bindingId === bindingId).map((approval) => ({ ...approval })) };
    },
  };
}
