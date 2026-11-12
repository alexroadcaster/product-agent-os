import type {Execution} from '../execution-recipes/contract.mts';
import type {QueueState,OwnershipClaim} from '../../../../packages/contracts/scheduler/queue.ts';
/** Private frozen intent. Public queue views contain metadata, never instructions/resources. */
export type FrozenRecipePlan=Pick<Execution,'taskId'|'taskContext'|'scopeHash'|'workflowSnapshot'|'transition'|'recipe'|'pins'|'inputArtifacts'|'budgetId'|'policyHash'|'bindingId'|'sessionId'> & {taskRevision:number;authorityEpoch:number;workspaceRoot:string;rootIdentity:string;reason:string};
export type QueueEntry={category:'scheduler_entry';id:string;projectId:string;plan:FrozenRecipePlan;claims:OwnershipClaim[];state:QueueState;executionId:string|null;reason?:string;createdAt:number;updatedAt:number};
export type QueueRegistry={category:'scheduler_queue';paused:boolean;order:string[]};
export const queueRegistryId='scheduler-queue';
export const pendingQueue=(entry:QueueEntry)=>['queued','paused','needs_review'].includes(entry.state);
export const liveQueue=(entry:QueueEntry)=>['queued','paused','needs_review','running','recovery_required'].includes(entry.state);
