const approvalMethods = {
  'item/commandExecution/requestApproval': 'command',
  'item/fileChange/requestApproval': 'file',
  'item/permissions/requestApproval': 'permissions',
} as const;

const itemTypes = [
  'userMessage', 'hookPrompt', 'agentMessage', 'functionCallOutput', 'plan', 'reasoning',
  'commandExecution', 'fileChange', 'mcpToolCall', 'dynamicToolCall', 'collabAgentToolCall',
  'subAgentActivity', 'webSearch', 'imageView', 'sleep', 'enteredReviewMode',
  'exitedReviewMode', 'contextCompaction',
] as const;

type RequestId = string | number;
type TurnIdentity = { threadId: string; turnId: string };
type TurnOutcome = 'completed' | 'failed' | 'interrupted';
type ItemStatus = 'completed' | 'failed' | 'declined' | 'interrupted';
type ItemType = typeof itemTypes[number];

const itemOutcomes: Partial<Record<ItemType, readonly ItemStatus[]>> = {
  commandExecution: ['completed', 'failed', 'declined'],
  fileChange: ['completed', 'failed', 'declined'],
  mcpToolCall: ['completed', 'failed'],
  dynamicToolCall: ['completed', 'failed'],
  collabAgentToolCall: ['completed', 'failed', 'interrupted'],
};

export type RuntimeEvent =
  | ({ kind: 'turn_accepted' } & TurnIdentity)
  | ({ kind: 'turn_started' } & TurnIdentity)
  | ({ kind: 'turn_ended'; outcome: TurnOutcome } & TurnIdentity)
  | ({ kind: 'approval_requested'; approval: typeof approvalMethods[keyof typeof approvalMethods]; requestId: RequestId; itemId: string } & TurnIdentity)
  | { kind: 'request_resolved'; threadId: string; requestId: RequestId }
  | ({ kind: 'item_ended'; itemId: string; itemType: ItemType; itemStatus: ItemStatus | null } & TurnIdentity)
  | { kind: 'non_lifecycle' }
  | { kind: 'recovery_required' };

const recovery = Object.freeze({ kind: 'recovery_required' } as const);

function record(value: unknown): Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
    ? value as Record<string, unknown>
    : {};
}

function nonempty(value: unknown): value is string {
  return typeof value === 'string' && value.trim().length > 0;
}

function requestId(value: unknown): value is RequestId {
  return nonempty(value) || (typeof value === 'number' && Number.isSafeInteger(value));
}

function terminal(value: unknown): value is TurnOutcome {
  return value === 'completed' || value === 'failed' || value === 'interrupted';
}

/** Use after RPC correlation. The result acknowledges dispatch and cannot end a turn. */
export function mapTurnAccepted(threadId: unknown, result: unknown): RuntimeEvent {
  const turn = record(record(result).turn);
  if (!nonempty(threadId) || !nonempty(turn.id) || (turn.status !== 'inProgress' && !terminal(turn.status))) {
    return recovery;
  }
  return { kind: 'turn_accepted', threadId, turnId: turn.id };
}

/** Project lifecycle state. The caller owns correlation and routes content frames to their own handlers. */
export function mapRuntimeEvent(message: unknown): RuntimeEvent {
  const { method, params: payload, id } = record(message);
  const params = record(payload);
  const { threadId, turnId, itemId } = params;
  if (!nonempty(threadId)) return recovery;

  if (typeof method === 'string' && Object.hasOwn(approvalMethods, method)) {
    if (!requestId(id) || !nonempty(turnId) || !nonempty(itemId)) return recovery;
    return { kind: 'approval_requested', approval: approvalMethods[method as keyof typeof approvalMethods],
      requestId: id, threadId, turnId, itemId };
  }
  if (id !== undefined) return recovery;

  switch (method) {
    case 'turn/started':
    case 'turn/completed': {
      const turn = record(params.turn);
      if (!nonempty(turn.id)) return recovery;
      if (method === 'turn/started' && turn.status === 'inProgress') {
        return { kind: 'turn_started', threadId, turnId: turn.id };
      }
      return method === 'turn/completed' && terminal(turn.status)
        ? { kind: 'turn_ended', threadId, turnId: turn.id, outcome: turn.status }
        : recovery;
    }
    case 'serverRequest/resolved':
      return requestId(params.requestId) ? { kind: 'request_resolved', threadId, requestId: params.requestId } : recovery;
    case 'item/started':
      return nonempty(turnId) && nonempty(record(params.item).id) ? { kind: 'non_lifecycle' } : recovery;
    case 'item/agentMessage/delta':
    case 'item/plan/delta':
      return nonempty(turnId) && nonempty(itemId) && typeof params.delta === 'string'
        ? { kind: 'non_lifecycle' }
        : recovery;
    case 'item/completed': {
      const item = record(params.item);
      const itemType = itemTypes.find((type) => type === item.type);
      if (!nonempty(turnId) || !nonempty(item.id) || !itemType) return recovery;
      // A status-bearing item must carry a valid terminal outcome of its own type.
      const outcomes = itemOutcomes[itemType];
      const itemStatus = outcomes?.find((outcome) => outcome === item.status);
      if (outcomes && itemStatus === undefined) return recovery;
      return { kind: 'item_ended', threadId, turnId, itemId: item.id, itemType, itemStatus: itemStatus ?? null };
    }
    default:
      return recovery;
  }
}
