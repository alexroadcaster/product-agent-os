export const M1_TASK_PROFILE = 'm1_task_profile_v1';
export const M1_TASK_STATUSES = [
  'backlog', 'ready', 'in_progress', 'review', 'verification', 'awaiting_acceptance', 'done', 'cancelled',
] as const;
export const M1_TASK_PRIORITIES = ['highest', 'high', 'medium', 'low', 'lowest'] as const;
export const M1_TASK_RELATIONS = ['related', 'blocks', 'blocked_by'] as const;
export const M1_ACTUAL_FILE_OPERATIONS = ['create', 'modify', 'delete', 'rename', 'read'] as const;
export const M1_PLANNED_FILE_OPERATIONS = [...M1_ACTUAL_FILE_OPERATIONS, 'create_or_modify_after_discovery'] as const;
export const M1_TASK_SOURCE_SCHEMAS = ['task_matrix_plan_v1', 'paos_web_task_groups_v1'] as const;

export type M1TaskStatus = typeof M1_TASK_STATUSES[number];
export type M1TaskCreator = { readonly kind: 'user'; readonly actorId: string }
  | { readonly kind: 'imported_unknown'; readonly actorId: null };

/** Normalized task interchange. External source parsing and ID allocation belong to import/storage. */
export type M1TaskProfile = Readonly<{
  schemaVersion: typeof M1_TASK_PROFILE;
  type: 'Task';
  id: string;
  projectId: string;
  key: string;
  legacyAlias: string | null;
  title: string;
  summary: string;
  technicalValue: string;
  productValue: string;
  files: readonly Readonly<{
    relativePath: string;
    previousRelativePath?: string;
    plannedOperation: typeof M1_PLANNED_FILE_OPERATIONS[number] | null;
    actualOperation: typeof M1_ACTUAL_FILE_OPERATIONS[number] | null;
  }>[];
  agentAssignments: readonly string[];
  artifactReferences: readonly string[];
  acceptanceCriteria: readonly string[];
  estimateSeconds: number | null;
  actual: Readonly<{ startedAt: string | null; endedAt: string | null; durationSeconds: number | null }>;
  risks: readonly string[];
  status: M1TaskStatus;
  creator: M1TaskCreator;
  priority: typeof M1_TASK_PRIORITIES[number] | null;
  startDate: string | null;
  dueDate: string | null;
  links: readonly Readonly<{ relation: typeof M1_TASK_RELATIONS[number]; taskId: string; projectId: string }>[];
  sessionIds: readonly string[];
  provenance: Readonly<{
    sourceSchema: typeof M1_TASK_SOURCE_SCHEMAS[number];
    adapterVersion: string;
    sourceId: string;
    sourceGroup: string | null;
    sourceStatus: string;
    sourceDigest: string;
    sourceDocument: string;
    mappingReceipt: string;
  }> | null;
}>;
