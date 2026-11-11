import type { LocalStore } from '../storage/local-store.mts';
import { createConnectionBroker, type CredentialStore } from '../connections/broker.ts';
import { createRuntimeCoordinator, type RuntimeBinding } from './codex/coordinator.ts';
import type { RuntimeRpc } from './codex/stdio-rpc.ts';
import { createRuntimeStoragePorts,taskScopeDigest } from './storage-ports.mts';
import {decodeM1TaskProfile} from '../tasks/task-profile.ts';
import { bindProject } from '../adapters/project-sources.ts';
import type {SavedTaskContext} from './m1-recipe.mts';

export class LiveGatewayError extends Error {
  readonly code: string;
  constructor(code: string) { super('The runtime gateway is unavailable.'); this.code=code; }
}

/** HTTP receives opaque IDs only. The trusted local store supplies root/account scope before any RPC. */
export function createLiveGateway(options: Readonly<{
  store: LocalStore; profileId: string; actorId: string;
  rpcFactory: () => Promise<RuntimeRpc>;
  isEnabled?: () => boolean; providerAuthority?: () => boolean;
  credentialStore?: CredentialStore;
  onEvent?: (event: Record<string,unknown>)=>void;
  redact?: (text:string)=>string;
  domainTool?: Parameters<typeof createRuntimeCoordinator>[0]['domainTool'];
  dynamicTools?: Parameters<typeof createRuntimeCoordinator>[0]['dynamicTools'];
}>) {
  let rpc: RuntimeRpc|undefined;
  let coordinator: ReturnType<typeof createRuntimeCoordinator>|undefined;
  let connecting=false;
  let connectionWork:Promise<unknown>|undefined;
  let retirement:Promise<void>|undefined;
  let dead=false;let closing=false;
  const bindings=new Map<string,RuntimeBinding>();
  const sendPins=new Map<string,{taskId:string;scopeDigest?:string;targetRevision?:number;taskContext:SavedTaskContext}>();
  const persistence=createRuntimeStoragePorts(options.store,{actorId:options.actorId});
  const broker=createConnectionBroker({profileId:options.profileId,store:options.credentialStore,
    request: async (method,params)=>{if(!rpc)throw new LiveGatewayError('runtime_disconnected');return rpc.request(method,params);}});
  const admitted=()=>options.isEnabled?.()===true && options.providerAuthority?.()===true;
  const publicRun=(run:Record<string,unknown>)=>{const {accountId,inputDigest,scopeDigest,targetRevision,...visible}=run;return visible;};
  const connectionStatus=()=>({...broker.snapshot(),verified:broker.snapshot().state==='connected',
    verificationScope:'local_login' as const,providerAuthority:options.providerAuthority?.()===true});
  function available(){if(closing)throw new LiveGatewayError('runtime_stopping');}
  /** Retire a generation completely before replacing it; late callbacks cannot revoke the successor's account. */
  function retire():Promise<void> {
    retirement??=(async()=>{
    if(coordinator)await coordinator.prepareShutdown();
    if(rpc)await rpc.close();
    if(coordinator){await coordinator.flush();coordinator.detach();}
    rpc=undefined;coordinator=undefined;dead=false;bindings.clear();sendPins.clear();
    })().finally(()=>{retirement=undefined;});return retirement;
  }
  function requiredText(input:Record<string,unknown>,key:string):string {
    if(typeof input[key]!=='string'||!(input[key] as string).trim())throw new LiveGatewayError('input_invalid');
    return input[key] as string;
  }
  async function scope(input:Record<string,unknown>) {
    const projectId=requiredText(input,'projectId'); const sessionId=requiredText(input,'sessionId');
    const project=await options.store.project(projectId); const session=await options.store.get(projectId,sessionId);
    if(!project||!session||session.kind!=='session'||session.deleted)throw new LiveGatewayError('scope_not_found');
    return {project,sessionId};
  }
  async function binding(input:Record<string,unknown>) {
    const current=await scope(input);const bindingId=requiredText(input,'bindingId'); const found=bindings.get(bindingId);
    if(!found||found.projectId!==current.project.id||found.sessionId!==current.sessionId)throw new LiveGatewayError('binding_scope_mismatch');
    return found;
  }
  const runtime={
    async snapshot(input:Record<string,unknown>) {
      const current=await scope(input);
      const found=[...bindings.values()].reverse().find((entry)=>entry.projectId===current.project.id&&entry.sessionId===current.sessionId);
      const state=found&&coordinator?coordinator.snapshot(found.id):null;
      const authorized=admitted()&&broker.authorize(broker.accountScopeId()??'');
      const busy=state?.hasActiveRun===true;
      return {canSend:authorized&&!!found&&!busy&&!state?.suspended&&found.generation===rpc?.generation,
        reason:!options.isEnabled?.()?'runtime_unverified':!options.providerAuthority?.()?'provider_authority_required':!authorized?'connection_unavailable':!found?'binding_required':state?.suspended?'runtime_stopping':busy?'runtime_busy':found.generation!==rpc?.generation?'binding_stale':null,
        state:state?.run?.state??broker.snapshot().state,bindingId:found?.id,runId:state?.run?.id,
        generation:state?.generation,mode:found?.mode,pendingApprovals:state?.approvals.filter((entry)=>entry.state==='pending'||entry.state==='response_sent')??[],modelAccess:'unverified',
        visibleDrafts:state?.visibleDrafts??[],fileChanges:state?.fileChanges??[],profile:state?.profile??null,checks:state?.checks??[],
        questions:state?.questions??{status:'unsupported',reason:'request_user_input_unsupported'},
        streaming:state?.streaming??{policy:'final_answer_only',phaseStatus:'not_observed'}};
    },
    async dispatch(action:string,input:Record<string,unknown>) {
      if(!admitted()||!coordinator)throw new LiveGatewayError('runtime_unverified');
      if(action==='bindings') {
        const selected=coordinator;
        const {project,sessionId}=await scope(input); const accountId=broker.accountScopeId();
        if(!accountId||!broker.authorize(accountId))throw new LiveGatewayError('connection_unavailable');
        const actualRoot=await bindProject(project.id,project.canonicalRoot);
        if(actualRoot.directoryIdentity!==project.rootIdentity)throw new LiveGatewayError('project_root_changed');
        const mode=requiredText(input,'mode');
        if(!['discussion','planning','execution'].includes(mode))throw new LiveGatewayError('mode_invalid');
        const created=await selected.openBinding({projectId:project.id,sessionId,accountId,workspaceRoot:project.canonicalRoot,
          profileId:options.profileId,mode:mode as RuntimeBinding['mode']});
        if(created.directoryIdentity!==project.rootIdentity)throw new LiveGatewayError('project_root_changed');
        available();
        if(selected!==coordinator||created.generation!==rpc?.generation||!broker.authorize(accountId))throw new LiveGatewayError('binding_stale');
        if(selected.snapshot(created.id).hasActiveRun)throw new LiveGatewayError('runtime_busy');
        bindings.delete(created.id);bindings.set(created.id,created);
        return {bindingId:created.id,projectId:created.projectId,sessionId:created.sessionId,mode:created.mode,generation:created.generation};
      }
      const found=await binding(input);
      if(action==='send') {
        let pinned: {taskId?:string;scopeDigest?:string;targetRevision?:number;taskContext?:SavedTaskContext}={};
        if(found.mode==='execution') {
          const taskId=requiredText(input,'taskId');const task=await options.store.get(found.projectId,taskId);
          if(!task||task.deleted||task.kind!=='task')throw new LiveGatewayError('task_scope_unavailable');
          const profile=decodeM1TaskProfile(task.data);
          const previous=await persistence.findRun(found.id,requiredText(input,'clientMessageId'));
          if(!previous&&(profile.status!=='ready'||profile.risks.includes('recovery_review')))throw new LiveGatewayError('task_scope_review_required');
          if(!profile.acceptanceCriteria.length||!profile.acceptanceCriteria.every((criterion)=>criterion.trim()))throw new LiveGatewayError('saved_criteria_required');
          const pinKey=`${found.id}:${requiredText(input,'clientMessageId')}`;const cached=sendPins.get(pinKey);
          pinned=cached?.taskId===taskId?cached:{taskId,scopeDigest:previous?.taskId===taskId?previous.scopeDigest??undefined:taskScopeDigest(task),
            targetRevision:previous?.taskId===taskId?previous.targetRevision:task.revision,
            taskContext:{taskId,key:profile.key,title:profile.title,revision:previous?.taskId===taskId?previous.targetRevision??task.revision:task.revision,
              files:profile.files.map((file)=>({relativePath:file.relativePath,previousRelativePath:file.previousRelativePath,plannedOperation:file.plannedOperation})),
              acceptanceCriteria:[...profile.acceptanceCriteria],risks:[...profile.risks]}};
          sendPins.set(pinKey,pinned as {taskId:string;scopeDigest?:string;targetRevision?:number;taskContext:SavedTaskContext});
        }
        return publicRun(await coordinator.send({bindingId:found.id,clientMessageId:requiredText(input,'clientMessageId'),input:requiredText(input,'input'),...pinned}));
      }
      if(action==='interrupt')return publicRun(await coordinator.interrupt({bindingId:found.id,runId:requiredText(input,'runId')}));
      if(action==='reconcile'){const result=await coordinator.reconcile({bindingId:found.id,accountId:broker.accountScopeId()??''});return result?publicRun(result):null;}
      if(action==='approve') {
        if(typeof input.requestId!=='string'&&typeof input.requestId!=='number')throw new LiveGatewayError('approval_invalid');
        if(!['accept','decline','cancel'].includes(String(input.decision)))throw new LiveGatewayError('approval_invalid');
        return coordinator.answerApproval({bindingId:found.id,runId:requiredText(input,'runId'),generation:requiredText(input,'generation'),
          requestId:input.requestId,decision:input.decision as 'accept'|'decline'|'cancel'});
      }
      throw new LiveGatewayError('action_invalid');
    },
  };
  const connection={status:connectionStatus,
    async connect(input:Record<string,unknown>) {
      available();
      if(!admitted())throw new LiveGatewayError('runtime_unverified');
      if(connecting||(rpc&&!dead))throw new LiveGatewayError('connection_busy');
      connecting=true;
      const work=(async()=>{try {
        if(dead)await retire();available();
        rpc=await options.rpcFactory();
        available();const selected=rpc;
        await rpc.request('initialize',{clientInfo:{name:'product-agent-os',version:'m1'},capabilities:{experimentalApi:true}});rpc.notify('initialized');
        available();rpc.onClosed(()=>{if(rpc===selected){dead=true;broker.runtimeClosed();}});
        await broker.connect({connectionId:requiredText(input,'connectionId'),apiKey:typeof input.apiKey==='string'?input.apiKey:undefined,remember:input.remember===true});
        available();
        coordinator=createRuntimeCoordinator({rpc,persistence,isEnabled:admitted,authorizeDispatch:(binding)=>broker.authorize(binding.accountId),
          onEvent:(event)=>options.onEvent?.(event.kind==='run'?{...event,run:publicRun(event.run as Record<string,unknown>)}:event),
          createStreamRedactor:()=>broker.createStreamRedactor(),
          redact:(text)=>broker.redact(options.redact?.(text)??text),domainTool:options.domainTool,dynamicTools:options.dynamicTools});
        for(const project of await options.store.projects())for(const recovered of await persistence.recoverable(project.id)) {
          // M1 has one global run. Multiple unresolved durable runs require explicit repair.
          await coordinator.restoreRecovery({...recovered,accountId:broker.accountScopeId()??''});bindings.set(recovered.binding.id,recovered.binding);
        }
        return connectionStatus();
      } catch(error) {broker.runtimeClosed();dead=true;await retire();throw error;}})();
      connectionWork=work;
      try{return await work;}finally {connecting=false;if(connectionWork===work)connectionWork=undefined;}
    },
    async disconnect() {
      available();
      if(connecting)throw new LiveGatewayError('connection_busy');
      connecting=true;
      const work=(async()=>{
        if(coordinator)await coordinator.prepareShutdown();
        try {await broker.disconnect();}finally {await retire();}
        return connectionStatus();
      })();
      connectionWork=work;try{return await work;}finally{connecting=false;if(connectionWork===work)connectionWork=undefined;}
    },
  };
  return {runtime,connection,async close(){closing=true;if(connectionWork)await Promise.allSettled([connectionWork]);await retire();broker.runtimeClosed();}};
}
