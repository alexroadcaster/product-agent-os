import type { StoredEntity } from "./client.ts";
/** Editing a path list must not erase file-operation evidence already attached to unchanged paths. */
export function plannedFiles(
  paths: string,
  existing: unknown,
): Record<string, unknown>[] {
  const files = Array.isArray(existing)
    ? (existing.filter((value) => value && typeof value === "object") as Record<
        string,
        unknown
      >[])
    : [];
  return paths
    .split("\n")
    .map((path) => path.trim())
    .filter(Boolean)
    .map(
      (relativePath) =>
        files.find((file) => file.relativePath === relativePath) ?? {
          relativePath,
          plannedOperation: "create_or_modify_after_discovery",
          actualOperation: null,
        },
    );
}
/** The service assigns the public task key and replaces creator with the paired actor. */
export function newTask(
  projectId: string,
  title: string,
  body: string,
  criteria: string[],
  id = crypto.randomUUID(),
): StoredEntity {
  return {
    id,
    projectId,
    kind: "task",
    title,
    body,
    status: "backlog",
    revision: 0,
    data: {
      schemaVersion: "m1_task_profile_v1",
      type: "Task",
      id,
      projectId,
      key: "",
      legacyAlias: null,
      title,
      summary: body,
      technicalValue: "",
      productValue: "",
      files: [],
      agentAssignments: [],
      artifactReferences: [],
      acceptanceCriteria: criteria,
      estimateSeconds: null,
      actual: { startedAt: null, endedAt: null, durationSeconds: null },
      risks: [],
      status: "backlog",
      creator: { kind: "user", actorId: "local-user" },
      priority: null,
      startDate: null,
      dueDate: null,
      links: [],
      sessionIds: [],
      provenance: null,
    },
  };
}
