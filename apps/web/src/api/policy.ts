import type { Connection, RuntimeState } from "./client.ts";
/** A retained historical run ID is not an active execution fence. Unknown outcomes remain fenced. */
export function runBlocksScopeChange(snapshot: RuntimeState | null): boolean {
  if (!snapshot) return true;
  if (["completed", "failed", "interrupted"].includes(snapshot.state ?? ""))
    return false;
  if (snapshot.runId) return true;
  return !["idle", "connected", "disconnected", "unverified", "error"].includes(
    snapshot.state ?? "",
  );
}
export function canStopRun(snapshot: RuntimeState | null): boolean {
  return Boolean(
    snapshot?.bindingId &&
    snapshot.runId &&
    ["running", "awaiting_approval", "interrupt_requested"].includes(
      snapshot.state ?? "",
    ),
  );
}
export type RunState = "idle" | "running" | "uncertain" | "approval_required";
export function canAnswerApproval(
  snapshot: RuntimeState | null,
  request: NonNullable<RuntimeState["pendingApprovals"]>[number],
  decision: "accept" | "decline",
  now = Date.now(),
): boolean {
  const current = Boolean(
    snapshot?.bindingId &&
    snapshot.runId &&
    snapshot.generation &&
    request.bindingId === snapshot.bindingId &&
    request.runId === snapshot.runId &&
    request.generation === snapshot.generation &&
    request.state === "pending" &&
    typeof request.expiresAt === "number" &&
    Number.isFinite(request.expiresAt) &&
    request.expiresAt > now,
  );
  const details =
    request.kind === "command"
      ? typeof request.details?.command === "string" &&
        Boolean(request.details.command.trim())
      : request.kind === "file" &&
        Array.isArray(request.details?.changes) &&
        request.details.changes.length > 0;
  return (
    current &&
    (decision === "decline" || (request.reviewable === true && details))
  );
}
/** Source text mentioning a key is not evidence that an event belongs to that task. */
export function eventReferencesEntity(
  payload: unknown,
  entityId: string,
  depth = 0,
): boolean {
  if (depth > 12 || !payload || typeof payload !== "object") return false;
  if (Array.isArray(payload))
    return payload.some((value) =>
      eventReferencesEntity(value, entityId, depth + 1),
    );
  return Object.entries(payload).some(
    ([key, value]) =>
      (["id", "entityId", "parentId", "taskId"].includes(key) &&
        value === entityId) ||
      (typeof value === "object" &&
        eventReferencesEntity(value, entityId, depth + 1)),
  );
}
export function canSend(
  connection: Connection | null,
  state: RunState,
  draft: string,
): boolean {
  return (
    connection?.verified === true && state === "idle" && Boolean(draft.trim())
  );
}
/** UI preflight only. The service must enforce current evidence and owner authority. */
export function canAccept(
  status: string,
  state: RunState,
  criteria: readonly string[],
  checked: readonly boolean[],
): boolean {
  return (
    status === "awaiting_acceptance" &&
    state === "idle" &&
    criteria.length > 0 &&
    criteria.length === checked.length &&
    checked.every((value) => value === true)
  );
}
