import { createHash } from 'node:crypto';
import type { LocalStore } from '../storage/local-store.mts';
import { decodeTaskProfile as decodeM1TaskProfile } from '../../../../packages/contracts/issues/task-profile.ts';
import type { RuntimeBinding, RuntimeRun } from '../runtime/codex/coordinator.ts';
import { taskManagerSnapshot,pinBlockingRun } from '../task-manager/service.mts';
import {runtimeWorkflow} from '../workflows/runtime.mts';

type ToolRequest = { tool: string; arguments: unknown; binding: RuntimeBinding; run: RuntimeRun; requestId: string | number };
const schemas = {
  task_read: { taskId: { type: 'string' } },
  task_propose: { title: { type: 'string' }, summary: { type: 'string' }, acceptanceCriteria: { type: 'array', items: { type: 'string' } } },
  task_patch: { taskId: { type: 'string' }, expectedRevision: { type: 'integer', minimum: 1 }, patch: { type: 'object' } },
  task_comment: { taskId: { type: 'string' }, body: { type: 'string' } },
  task_link: { taskId: { type: 'string' }, toTaskId: { type: 'string' }, expectedRevision: { type: 'integer', minimum: 1 }, relation: { enum: ['related', 'blocks', 'blocked_by'] } },
  evidence_reference: { taskId: { type: 'string' }, evidenceId: { type: 'string' } },
} as const;
const required = { task_read: ['taskId'], task_propose: ['title'], task_patch: ['taskId', 'expectedRevision', 'patch'],
  task_comment: ['taskId', 'body'], task_link: ['taskId', 'toTaskId', 'expectedRevision', 'relation'], evidence_reference: ['taskId', 'evidenceId'] };
export const domainToolSpecifications = Object.entries(schemas).map(([name, properties]) => ({ type: 'function' as const,
  name, description: `Project-scoped ${name} through the Product-Agent OS domain service.`,
  inputSchema: { type: 'object', properties, required: required[name as keyof typeof required], additionalProperties: false } }));
function fail(code: string): never { throw Object.assign(new Error(code), { code }); }
function canonicalJson(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  if (value && typeof value === 'object') return `{${Object.entries(value).sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0)
    .map(([key, item]) => `${JSON.stringify(key)}:${canonicalJson(item)}`).join(',')}}`;
  return JSON.stringify(value) ?? 'null';
}

/** Runtime supplies scope and actor. Model arguments can never change project, mode, target or authority. */
export function createDomainTools({ store,onPendingLink }: { store: LocalStore;onPendingLink?:(input:{projectId:string;linkId:string})=>Promise<unknown> }) {
  return { specifications: domainToolSpecifications, async dispatch(request: ToolRequest) {
    if (!Object.hasOwn(schemas, request.tool)) fail('TOOL_UNSUPPORTED');
    if (!request.arguments || typeof request.arguments !== 'object' || Array.isArray(request.arguments)
      || Buffer.byteLength(JSON.stringify(request.arguments)) > 64 * 1024) fail('TOOL_ARGUMENTS_INVALID');
    const args = request.arguments as Record<string, unknown>;
    const schema = schemas[request.tool as keyof typeof schemas];
    if (Object.keys(args).some((key) => !Object.hasOwn(schema, key))) fail('TOOL_ARGUMENTS_INVALID');
    const { binding, run } = request;
    if (binding.id !== run.bindingId || binding.projectId !== run.projectId || binding.generation !== run.generation
      || binding.threadId !== run.threadId || !['running', 'dispatching', 'awaiting_approval'].includes(run.state)) fail('TOOL_SCOPE_INVALID');
    const project = await store.project(binding.projectId);
    if (!project) fail('PROJECT_NOT_FOUND');
    const actorId = `agent:${binding.profileId}:${run.id}`;
    const identity = `${typeof request.requestId}:${request.requestId}`;
    const idempotencyKey = `tool:${binding.generation}:${run.id}:${identity}`;
    const entityId = createHash('sha256').update(idempotencyKey).digest('hex');
    const operationId = `operation-${entityId}`;
    const inputHash = createHash('sha256').update(canonicalJson({ tool: request.tool, arguments: args })).digest('hex');
    const previous = await store.receipt(project.id, idempotencyKey);
    if (previous) {
      const operation = await store.get(project.id, operationId);
      if (operation?.data.inputHash !== inputHash) fail('IDEMPOTENCY_CONFLICT');
      if(typeof operation.data.linkId==='string'&&onPendingLink){try{await onPendingLink({projectId:project.id,linkId:operation.data.linkId});}catch{/* The canonical edge remains visibly pending; retry never targets a successor run. */}}
      return previous;
    }
    const commit = (changes: Parameters<LocalStore['write']>[0]['changes'],m2Transition=false,linkId?:string) => store.write({ projectId: project.id, actorId,
      ...(m2Transition?{taskManagerAction:'transition' as const,taskManagerReason:'Bound agent transition',taskManagerRun:{id:run.id,bindingId:binding.id,generation:binding.generation,taskId:run.taskId!}}:{}),
      idempotencyKey, expectedAuthorityEpoch: project.authorityEpoch, changes: [...changes,
        { expectedRevision: 0, entity: { id: operationId, kind: 'evidence', coverage: 'partial',
          data: { category: 'domain_command_receipt', observed: false, inputHash, runId: run.id,...(linkId?{linkId}:{}) } } }] });
    if (request.tool === 'task_propose') {
      if (typeof args.title !== 'string' || !args.title.trim() || (args.summary !== undefined && typeof args.summary !== 'string')
        || (args.acceptanceCriteria !== undefined && (!Array.isArray(args.acceptanceCriteria)
          || args.acceptanceCriteria.some((value) => typeof value !== 'string')))) fail('TOOL_ARGUMENTS_INVALID');
      return commit([{ expectedRevision: 0, entity: { id: `proposal-${entityId}`, kind: 'draft', parentId: binding.sessionId,
          title: args.title, body: typeof args.summary === 'string' ? args.summary : '',
          data: { category: 'task_proposal', fields: args, source: 'agent_assertion', runId: run.id } } }]);
    }
    if (typeof args.taskId !== 'string') fail('TOOL_ARGUMENTS_INVALID');
    const target = await store.get(project.id, args.taskId);
    if (!target || target.kind !== 'task') fail('TASK_NOT_FOUND');
    if (request.tool === 'task_read') return target.data.schemaVersion==='m2_task_profile_v1'||(typeof store.compatibility==='function'&&(await store.compatibility()).schemaVersion===2)
      ?{...target,issueLinks:(await taskManagerSnapshot(store,project.id)).links.filter(l=>l.sourceId===target.id||l.targetId===target.id)}:target;
    if (binding.mode !== 'execution' || run.taskId !== target.id || !run.scopeDigest) fail('TOOL_WRITE_FORBIDDEN');
    if (request.tool === 'task_comment') {
      if (typeof args.body !== 'string' || !args.body.trim()) fail('TOOL_ARGUMENTS_INVALID');
      return commit([{ expectedRevision: 0, entity: { id: `comment-${entityId}`, kind: 'comment', parentId: target.id,
          body: args.body, data: { category: target.data.schemaVersion==='m2_task_profile_v1'?'m2_agent_comment':'agent_comment', source: 'agent_assertion', runId: run.id,
            ...(target.data.schemaVersion==='m2_task_profile_v1'?{actorId,createdAt:new Date().toISOString(),sessionId:binding.sessionId}:{}) } } }]);
    }
    if (request.tool === 'evidence_reference') {
      if (typeof args.evidenceId !== 'string') fail('TOOL_ARGUMENTS_INVALID');
      const evidence = await store.get(project.id, args.evidenceId);
      if (!evidence || evidence.kind !== 'evidence' || evidence.data.observed !== true || evidence.parentId !== target.id) fail('EVIDENCE_UNVERIFIED');
      return { evidenceId: evidence.id, coverage: evidence.coverage, source: 'observed_receipt' };
    }
    if (!Number.isSafeInteger(args.expectedRevision) || args.expectedRevision !== target.revision) fail('REVISION_CONFLICT');
    let changed: Record<string, unknown>;
    if (request.tool === 'task_patch') {
      if (!args.patch || typeof args.patch !== 'object' || Array.isArray(args.patch)) fail('TOOL_ARGUMENTS_INVALID');
      changed = args.patch as Record<string, unknown>;
      const workflow=await runtimeWorkflow(store,project.id,{...target.data,...changed});
      if (Object.keys(changed).some((key) => !['status', 'risks'].includes(key))
        || (changed.status !== undefined && !['in_progress', 'review', 'verification', 'awaiting_acceptance'].includes(workflow.category))) fail('TOOL_PATCH_FORBIDDEN');
      // Imported-state review is an owner decision. A model may add risks but cannot clear these guards.
      if (changed.risks !== undefined && ['recovery_review', 'acceptance_unverified'].some((flag) =>
        Array.isArray(target.data.risks) && target.data.risks.includes(flag)
          && (!Array.isArray(changed.risks) || !changed.risks.includes(flag)))) fail('SYSTEM_REVIEW_REQUIRED');
    } else {
      if (typeof args.toTaskId !== 'string' || !['related', 'blocks', 'blocked_by'].includes(String(args.relation))) fail('TOOL_ARGUMENTS_INVALID');
      const other = await store.get(project.id, args.toTaskId);
      if (!other || other.kind !== 'task') fail('TASK_NOT_FOUND');
      if(target.data.schemaVersion==='m2_task_profile_v1'||other.data.schemaVersion==='m2_task_profile_v1'
        ||(typeof store.compatibility==='function'&&(await store.compatibility()).schemaVersion===2)){
        const snapshot=await taskManagerSnapshot(store,project.id);
        let sourceId=target.id,targetId=other.id;if(args.relation==='blocked_by')[sourceId,targetId]=[targetId,sourceId];
        const relation=args.relation==='related'?'relates_to' as const:'blocks' as const;
        const pin=relation==='blocks'?pinBlockingRun(await store.projectEntities(project.id),targetId):undefined;
        const link={id:`agent-link-${entityId}`,sourceId,targetId,relation,actorId,createdAt:new Date().toISOString(),reason:'Agent task link',source:`agent:${run.id}`,
          state:pin?'pending' as const:'active' as const,...(pin?{blockedRun:pin,requiredAction:'stop_and_reconcile_then_activate' as const}:{})};
        const receipt=await commit([{expectedRevision:target.revision,entity:{id:target.id,kind:'task',data:target.data}},
          {expectedRevision:snapshot.settingsRevisions.links,entity:{id:'m2-links',kind:'settings',data:{items:[...snapshot.links,link]}}}],false,link.id);
        if(pin&&onPendingLink){try{await onPendingLink({projectId:project.id,linkId:link.id});}catch{/* A committed pending edge still fences new work and remains available for explicit Stop retry. */}}
        return receipt;
      }
      changed = { links: [...(target.data.links as unknown[]), { relation: args.relation, taskId: other.id, projectId: project.id }] };
    }
    const task = decodeM1TaskProfile({ ...target.data, ...changed });
    return commit([{ expectedRevision: target.revision, entity: { id: target.id, kind: 'task', data: task } }],task.schemaVersion==='m2_task_profile_v1'&&task.status!==target.status);
  } };
}
