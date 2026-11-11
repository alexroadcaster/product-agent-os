import assert from 'node:assert/strict';
import { test } from 'node:test';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createRuntimeCoordinator } from '../../apps/local-service/src/runtime/codex/coordinator.ts';
const context=(taskId:string)=>({targetRevision:1,taskContext:{taskId,key:'TEST-1',title:'Synthetic task',revision:1,files:[],acceptanceCriteria:['Synthetic criterion'],risks:[]}});

test('persists one dispatch intent and deduplicates repeated user sends without accepting a task', async (t) => {
  const workspaceRoot = await mkdtemp(join(tmpdir(), 'paos-coordinator-'));
  t.after(() => rm(workspaceRoot, { recursive: true, force: true }));
  let dispatches = 0;
  const writes: unknown[] = [];
  const coordinator = createRuntimeCoordinator({
    isEnabled: () => true, authorizeDispatch: () => true,
    rpc: { generation: 'fixture-generation', subscribe() { return () => {}; }, onClosed() { return () => {}; },
      async request(method, params) {
        if (method === 'thread/start') return {
          thread: { id: 'thread-fixture' }, cwd: params.cwd, runtimeWorkspaceRoots: [params.cwd],
          activePermissionProfile: { id: params.permissions }, approvalPolicy: 'on-request',
          sandbox: { type: 'workspaceWrite', networkAccess: false, writableRoots: [], excludeSlashTmp: true, excludeTmpdirEnvVar: true },
        };
        if (method === 'turn/start') { dispatches += 1; return { turn: { id: 'turn-fixture', status: 'inProgress' } }; }
        return {};
      },
      respond() {}, respondError() {},
    },
    persistence: {
      async findRun() { return null; }, async saveBinding(binding) { writes.push({ binding }); },
      async appendIntent(run) { writes.push({ intent: run }); }, async updateRun(run) { writes.push({ run }); },
      async saveVisibleMessage() {},
    },
  });
  const binding = await coordinator.openBinding({ projectId: 'project-fixture', sessionId: 'session-fixture',
    accountId: 'account-fixture', workspaceRoot, mode: 'execution', profileId: 'profile-fixture' });
  const request = { bindingId: binding.id, clientMessageId: 'message-fixture', input: 'Synthetic request',
    taskId: 'task-fixture', scopeDigest: 'scope-fixture',...context('task-fixture') };
  const [first, duplicate] = await Promise.all([coordinator.send(request), coordinator.send(request)]);
  assert.equal(dispatches, 1);
  assert.equal(first.id, duplicate.id);
  assert.equal(first.state, 'running');
  await assert.rejects(coordinator.send({...request,taskContext:{...request.taskContext,acceptanceCriteria:['Changed saved scope']}}),{code:'message_conflict'});
  assert.equal(writes.filter((entry) => Object.hasOwn(entry as object, 'intent')).length, 1);
  assert.equal(Object.hasOwn(first, 'taskAccepted'), false);
});

test('correlates approvals, retains a recovery lease on EOF, and never resends', async (t) => {
  const { fork } = await import('node:child_process');
  const { fileURLToPath } = await import('node:url');
  const { createStdioRpc } = await import('../../apps/local-service/src/runtime/codex/stdio-rpc.ts');
  const workspaceRoot = await mkdtemp(join(tmpdir(), 'paos-runtime-fixture-'));
  const child = fork(fileURLToPath(new URL('./runtime-adapter.fixture.mts', import.meta.url)), [], {
    execArgv: [], env: { SystemRoot: process.env.SystemRoot }, silent: true,
  });
  const rpc = createStdioRpc(child, {timeoutMs: 1000});
  t.after(async () => { await rpc.close(); await rm(workspaceRoot, {recursive:true,force:true}); });
  const messages: unknown[] = [];
  const coordinator = createRuntimeCoordinator({ rpc, isEnabled:()=>true, authorizeDispatch:()=>true,
    onEvent: (event) => messages.push(event),
    persistence: { async findRun(){return null;}, async saveBinding(){}, async appendIntent(){},
      async updateRun(){}, async saveVisibleMessage(message){messages.push(message);} },
  });
  const binding = await coordinator.openBinding({projectId:'p',sessionId:'s',accountId:'a',workspaceRoot,mode:'execution',profileId:'fixture'});
  const run = await coordinator.send({bindingId:binding.id,clientMessageId:'m',input:'synthetic',taskId:'t',scopeDigest:'scope',...context('t')});
  const inject = async (message: unknown) => {
    const received = new Promise<void>((resolve) => { const off=rpc.subscribe(()=>{off();resolve();}); });
    child.send({message}); await received; await coordinator.flush();
  };
  await inject({id:77,method:'item/commandExecution/requestApproval',params:{threadId:run.threadId,turnId:run.turnId,itemId:'command',cwd:binding.workspaceRoot}});
  assert.equal(coordinator.snapshot(binding.id).run?.state,'awaiting_approval');
  const approvalInput = {bindingId:binding.id,runId:run.id,generation:rpc.generation,requestId:77,decision:'decline' as const};
  await coordinator.answerApproval(approvalInput);
  await coordinator.answerApproval(approvalInput);
  await assert.rejects(coordinator.answerApproval({...approvalInput,decision:'accept'}),{code:'approval_conflict'});
  await inject({method:'serverRequest/resolved',params:{threadId:run.threadId,requestId:77}});
  assert.equal(coordinator.snapshot(binding.id).approvals[0].state,'answered_or_cleared');
  await inject({method:'item/completed',params:{threadId:run.threadId,turnId:run.turnId,item:{id:'visible',type:'agentMessage',phase:'final_answer',text:'visible final'}}});
  assert.equal(messages.some((value:any)=>value.text==='visible final'),true);
  await inject({method:'item/completed',params:{threadId:run.threadId,turnId:run.turnId,item:{id:'hidden',type:'reasoning',text:'hidden content'}}});
  assert.equal(JSON.stringify(messages).includes('hidden content'),false);
  await coordinator.interrupt({bindingId:binding.id,runId:run.id});
  assert.equal(coordinator.snapshot(binding.id).run?.state,'interrupt_requested');
  const closed = new Promise<void>((resolve)=>rpc.onClosed(()=>resolve()));
  child.send({disconnect:true}); await closed; await coordinator.flush();
  assert.equal(coordinator.snapshot(binding.id).run?.state,'recovery_required');
  await assert.rejects(coordinator.send({bindingId:binding.id,clientMessageId:'new',input:'synthetic',taskId:'t',scopeDigest:'scope'}),{code:'runtime_busy'});
});


test('restores an unresolved durable run only into explicit reconciliation, never dispatch', async (t) => {
  const workspaceRoot = await mkdtemp(join(tmpdir(),'paos-restore-'));
  t.after(()=>rm(workspaceRoot,{recursive:true,force:true}));
  const {bindProject}=await import('../../apps/local-service/src/adapters/project-sources.ts');
  const root=await bindProject('p',workspaceRoot);
  let requests=0;
  const coordinator=createRuntimeCoordinator({rpc:{generation:'new',subscribe(){return()=>{};},onClosed(){return()=>{};},
    async request(method){requests++;assert.equal(method,'thread/read');return {thread:{id:'thread',turns:[{id:'turn',status:'interrupted'}]}};},respond(){},respondError(){}},
    persistence:{async findRun(){return null;},async saveBinding(){},async appendIntent(){},async updateRun(){},async saveVisibleMessage(){}},
    isEnabled:()=>true,authorizeDispatch:()=>true});
  const binding={id:'binding',projectId:'p',sessionId:'s',accountId:'account',workspaceRoot:root.workspaceRoot,directoryIdentity:root.directoryIdentity,
    mode:'execution' as const,profileId:'profile',generation:'old',threadId:'thread'};
  const run={id:'run',bindingId:'binding',projectId:'p',sessionId:'s',accountId:'account',generation:'old',threadId:'thread',turnId:'turn',clientMessageId:'m',inputDigest:'digest',taskId:'t',scopeDigest:'scope',state:'running' as const};
  await coordinator.restoreRecovery({binding,run,accountId:'account'});
  assert.equal(requests,0);
  assert.equal(coordinator.snapshot('binding').run?.state,'recovery_required');
  await assert.rejects(coordinator.reconcile({bindingId:'binding',accountId:'different'}),{code:'account_mismatch'});
  assert.equal((await coordinator.reconcile({bindingId:'binding',accountId:'account'}))?.state,'interrupted');
  assert.equal(requests,1);
  await assert.rejects(coordinator.send({bindingId:'binding',clientMessageId:'new',input:'synthetic',taskId:'t',scopeDigest:'scope'}),{code:'binding_stale'});
});

