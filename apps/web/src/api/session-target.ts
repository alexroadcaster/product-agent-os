import type { Change, StoredEntity } from "./client.ts";
/** Resolve the saved ID directly, independently of selector pagination; eligibility never hides existing context. */
export async function loadSavedSessionTarget(
  api: { entity(projectId: string, id: string): Promise<StoredEntity> },
  projectId: string,
  taskId: string,
): Promise<StoredEntity | undefined> {
  if (!taskId) return undefined;
  const task = await api.entity(projectId, taskId);
  if (
    task.id !== taskId ||
    task.projectId !== projectId ||
    task.kind !== "task" ||
    ("deleted" in task && task.deleted === true)
  )
    throw new Error("TASK_SCOPE_MISMATCH");
  return task;
}
/** UI preflight; the service computes the authoritative digest from the saved task revision. */
export function isExecutionTarget(task: StoredEntity | undefined): boolean {
  if (
    !task ||
    task.kind !== "task" ||
    task.revision < 1 ||
    task.status !== "ready" ||
    (Array.isArray(task.data?.risks) &&
      task.data.risks.includes("recovery_review")) ||
    task.data?.schemaVersion !== "m1_task_profile_v1"
  )
    return false;
  const criteria = task.data.acceptanceCriteria,
    files = task.data.files;
  return (
    Array.isArray(criteria) &&
    criteria.length > 0 &&
    criteria.every(
      (value) => typeof value === "string" && Boolean(value.trim()),
    ) &&
    Array.isArray(files) &&
    files.length > 0 &&
    files.every((value) => {
      if (!value || typeof value !== "object") return false;
      const { relativePath, plannedOperation } = value as Record<
        string,
        unknown
      >;
      return (
        typeof relativePath === "string" &&
        Boolean(relativePath.trim()) &&
        !/^(?:[A-Za-z]:|[/\\])/.test(relativePath) &&
        !relativePath
          .split(/[/\\]/)
          .some((part) => part === ".." || part === "." || part === "") &&
        !/[\0\r\n:]/.test(relativePath) &&
        [
          "create",
          "modify",
          "delete",
          "rename",
          "read",
          "create_or_modify_after_discovery",
        ].includes(String(plannedOperation))
      );
    })
  );
}
export function attachTaskToSession(
  session: StoredEntity,
  task: StoredEntity,
): Change[] {
  if (
    task.projectId !== session.projectId ||
    task.kind !== "task" ||
    session.kind !== "session"
  )
    throw new Error("Task/session scope mismatch");
  const sessionIds = Array.isArray(task.data?.sessionIds)
    ? task.data.sessionIds.filter((value) => typeof value === "string")
    : [];
  return [
    {
      expectedRevision: session.revision,
      entity: { ...session, data: { ...session.data, taskId: task.id } },
    },
    {
      expectedRevision: task.revision,
      entity: {
        ...task,
        data: {
          ...task.data,
          sessionIds: [...new Set([...sessionIds, session.id])],
        },
      },
    },
  ];
}
