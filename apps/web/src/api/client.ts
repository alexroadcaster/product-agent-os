import type {
  UiPreferences,
  UiPreferencesStore,
} from "../design/preferences.ts";

export type EntityKind =
  | "task"
  | "session"
  | "message"
  | "comment"
  | "settings"
  | "draft"
  | "evidence"
  | "run"
  | "approval"
  | "document";
export type StoredEntity = {
  journalOrder?: number;
  id: string;
  projectId: string;
  kind: EntityKind;
  parentId?: string;
  title?: string;
  body?: string;
  status?: string;
  publicKey?: string;
  coverage?: unknown;
  data?: Record<string, unknown>;
  revision: number;
};
export type Project = {
  id: string;
  name: string;
  keyPrefix: string;
  authorityMode: "legacy_files" | "sql";
  authorityEpoch: number;
  streamGeneration: string;
};
export type Page = { items: StoredEntity[]; hasMore: boolean };
export type Connection = {
  verified: boolean;
  reason?: string;
  state?: string;
  payer?: "user_api_account";
  providerAuthority?: boolean;
};
export type Change = {
  expectedRevision: number;
  entity: StoredEntity;
  delete?: boolean;
};
export type RuntimeState = {
  visibleDrafts?: readonly {
    runId: string;
    sourceItemId: string;
    role: "assistant";
    text: string;
    revision: number;
    status: "streaming" | "completed" | "interrupted" | "recovery_required";
    phase?: "commentary" | "partial_answer" | "final_answer" | "unknown";
  }[];
  canSend: boolean;
  reason: string | null;
  bindingId?: string;
  runId?: string;
  generation?: string;
  state?: string;
  pendingApprovals?: {
    requestId: string | number;
    description?: string;
    kind?: string;
    runId?: string;
    generation?: string;
    bindingId?: string;
    expiresAt?: number;
    reviewable?: boolean;
    state?: string;
    details?: { command?: string; reason?: string; changes?: unknown };
  }[];
  fileChanges?: readonly {
    kind: "actual" | "proposed" | "external";
    path: string;
    previousPath?: string;
    diff?: string;
    operation?: string;
    coverage: "partial" | "unavailable";
    reason: string;
  }[];
  profile?: {
    id: string;
    version: string | null;
    role: string | null;
    assignment: string | null;
    coverage: "pinned" | "unavailable";
  };
  questions?: { status: "unsupported"; reason: string };
  streaming?: {
    policy: "final_answer_only";
    phaseStatus: "not_observed" | "phase_unavailable" | "final_answer_observed";
  };
  checks?: readonly {
    id: string;
    runId?: string;
    taskId?: string | null;
    itemType: string;
    status: string;
    outcome?: string;
    coverage: string;
    reason?: string;
  }[];
  diff?: string;
  modelAccess?: string;
  mode?: string;
};
export type SourceCoverage = {
  projectId: string;
  sources: {
    id: string;
    relativePath?: string;
    status: string;
    reason?: string;
  }[];
};
export type HistoryEvent = {
  seq: number;
  entityId?: string;
  kind?: string;
  type?: string;
  payload?: Record<string, unknown>;
  [key: string]: unknown;
};
export type ImportSource = {
  role: "records" | "projection";
  sourceName: string;
  content: string;
  sourceRelativePath: string;
};
export type ImportPreview = {
  mode?: "legacy_import" | "normalized_proposal";
  proposal?: Record<string, unknown>;
  sources?: readonly {
    role: string;
    sourceName: string;
    sourceRelativePath: string;
    sourceDigest: string;
  }[];
  stageId: string;
  parserVersion: string;
  sourceDigest: string;
  sourceName: string;
  items: { sourceId: string; task: Record<string, unknown> }[];
  blocked: { sourceId: string; reasons: string[] }[];
};
export interface M1Api {
  pair(code?: string): Promise<void>;
  quit(): Promise<{ status: "quit_requested" }>;
  projects(): Promise<Project[]>;
  createProject(name: string, workspaceRoot: string): Promise<unknown>;
  entities(
    projectId: string,
    kind: EntityKind,
    parentId?: string,
    offset?: number,
    signal?: AbortSignal,
  ): Promise<Page>;
  entity(projectId: string, id: string): Promise<StoredEntity>;
  messages(
    projectId: string,
    sessionId: string,
    offset?: number,
    signal?: AbortSignal,
  ): Promise<Page>;
  command(
    projectId: string,
    changes: Change[],
    idempotencyKey?: string,
  ): Promise<unknown>;
  manualCheck(
    projectId: string,
    taskId: string,
    revision: number,
    outcome: "passed" | "failed",
    note: string,
  ): Promise<{ checkId: string }>;
  accept(
    projectId: string,
    taskId: string,
    revision: number,
    checkId: string,
    accepted: boolean,
    note: string,
  ): Promise<unknown>;
  connection(): Promise<Connection>;
  connect(input: {
    connectionId: string;
    apiKey?: string;
    remember: boolean;
  }): Promise<Connection>;
  disconnect(): Promise<Connection>;
  runtime(
    action: "bindings" | "send" | "interrupt" | "approve" | "reconcile",
    body: Record<string, unknown>,
  ): Promise<unknown>;
  runtimeState(
    projectId: string,
    sessionId: string,
    signal?: AbortSignal,
  ): Promise<RuntimeState>;
  search(
    projectId: string,
    query: string,
    offset?: number,
    signal?: AbortSignal,
  ): Promise<Page & { coverage?: string; generation?: number }>;
  preferences: UiPreferencesStore;
  sources(projectId: string): Promise<SourceCoverage>;
  catalogs(projectId: string): Promise<{
    agents: {
      id: string;
      label: string;
      description: string;
      coverage: string;
    }[];
    skills: {
      id: string;
      label: string;
      description: string;
      coverage: string;
    }[];
    graph: { status: string; reason: string };
    coverage?: "complete" | "partial";
  }>;
  events(
    projectId: string,
    cursor?: string,
  ): Promise<{ items: HistoryEvent[]; nextCursor: string }>;
  previewImport(
    projectId: string,
    sourceName: string,
    content: string,
    sourceRelativePath?: string,
  ): Promise<ImportPreview>;
  previewImportBundle(
    projectId: string,
    sources: readonly ImportSource[],
  ): Promise<ImportPreview>;
  sourceStatus(projectId: string): Promise<{
    authorityMode: string;
    items: {
      sourceName: string;
      sourceRelativePath: string;
      status: string;
      sourceDigest: string;
      observedDigest?: string;
    }[];
  }>;
  sourceContent(
    projectId: string,
    name: string,
    signal?: AbortSignal,
  ): Promise<{
    relativePath: string;
    content: string;
    sha256: string;
    coverage: "complete" | "partial";
    redacted: boolean;
  }>;
  rebuildSearch(
    projectId: string,
    signal?: AbortSignal,
  ): Promise<Record<string, unknown>>;
  backup(projectId: string): Promise<{
    backupId: string;
    manifest: unknown;
    rotatedBackupIds?: string[];
    rotationCandidateIds?: string[];
    retention?: "complete" | "pending";
  }>;
  rotateBackups(
    projectId: string,
    candidateIds: string[],
  ): Promise<{ rotatedBackupIds: string[]; retention: "complete" }>;
  commitImport(
    projectId: string,
    input: {
      stageId: string;
      currentSource?: string;
      currentSources?: readonly ImportSource[];
      sourceDigest: string;
      idempotencyKey: string;
    },
  ): Promise<{ mappingCount: number; backupId: string; receipt: unknown }>;
  exportTasks(projectId: string): Promise<unknown>;
  restore(
    projectId: string,
    backupId: string,
  ): Promise<{
    restoreId: string;
    requiresRestart: boolean;
    activeProfileChanged: boolean;
  }>;
}

/** Same-origin only; bearer credentials never enter URLs or browser persistence. */
export function createHttpApi(fetcher: typeof fetch = fetch): M1Api {
  let csrfToken: string | undefined;
  const epochs = new Map<string, number>();
  async function request<T>(
    path: string,
    body?: unknown,
    method = body === undefined ? "GET" : "POST",
    signal?: AbortSignal,
  ): Promise<T> {
    if (method !== "GET" && !csrfToken && path !== "/bootstrap/exchange")
      throw new Error("Paired session required");
    const response = await fetcher(`/api/v1${path}`, {
      method,
      credentials: "same-origin",
      signal,
      headers: {
        Accept: "application/json",
        ...(body === undefined ? {} : { "Content-Type": "application/json" }),
        ...(method === "GET" || !csrfToken ? {} : { "X-PAOS-CSRF": csrfToken }),
      },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
    if (!response.ok) {
      const error = (await response.json().catch(() => null)) as {
        error?: { code?: unknown };
      } | null;
      const code = error?.error?.code;
      throw new Error(
        `HTTP ${response.status}${typeof code === "string" && /^[A-Za-z_]{1,80}$/.test(code) ? `: ${code}` : ""}`,
      );
    }
    if (response.status === 204) return undefined as T;
    return response.json() as Promise<T>;
  }
  const projectPath = (id: string) => `/projects/${encodeURIComponent(id)}`;
  function authority(projectId: string, revision: number) {
    if (!epochs.has(projectId))
      throw new Error("Project authority is unverified");
    return {
      expectedRevision: revision,
      expectedAuthorityEpoch: epochs.get(projectId),
      idempotencyKey: crypto.randomUUID(),
    };
  }
  return {
    quit: () => request("/quit", {}),
    async pair(code) {
      const session = await request<{ csrfToken: string }>(
        code ? "/bootstrap/exchange" : "/session",
        code ? { code } : undefined,
      );
      csrfToken = session.csrfToken;
    },
    async projects() {
      const result = await request<{ items: Project[] }>("/projects");
      for (const project of result.items)
        epochs.set(project.id, project.authorityEpoch);
      return result.items;
    },
    createProject: (name, workspaceRoot) =>
      request("/projects", { name, workspaceRoot }),
    entities: (id, kind, parentId, offset = 0, signal) => {
      const q = new URLSearchParams({
        kind,
        limit: "50",
        offset: String(offset),
      });
      if (parentId) q.set("parentId", parentId);
      return request<Page>(
        `${projectPath(id)}/entities?${q}`,
        undefined,
        "GET",
        signal,
      );
    },
    entity: (projectId, id) =>
      request(`${projectPath(projectId)}/entities/${encodeURIComponent(id)}`),
    messages: (projectId, sessionId, offset = 0, signal) =>
      request(
        `${projectPath(projectId)}/entities?${new URLSearchParams({ kind: "message", parentId: sessionId, order: "newest", limit: "50", offset: String(offset) })}`,
        undefined,
        "GET",
        signal,
      ),
    command: (id, changes, idempotencyKey = crypto.randomUUID()) => {
      if (!epochs.has(id))
        return Promise.reject(new Error("Project authority is unverified"));
      return request(`${projectPath(id)}/commands`, {
        idempotencyKey,
        expectedAuthorityEpoch: epochs.get(id),
        changes,
      });
    },
    manualCheck: async (projectId, taskId, revision, outcome, note) =>
      request(
        `${projectPath(projectId)}/tasks/${encodeURIComponent(taskId)}/check`,
        { ...authority(projectId, revision), outcome, note },
      ),
    accept: async (projectId, taskId, revision, checkId, accepted, note) =>
      request(
        `${projectPath(projectId)}/tasks/${encodeURIComponent(taskId)}/accept`,
        { ...authority(projectId, revision), checkId, accepted, note },
      ),
    connection: () => request<Connection>("/connection"),
    connect: (input) => request("/connection", input),
    disconnect: () => request("/connection", undefined, "DELETE"),
    runtime: (action, body) => request(`/runtime/${action}`, body),
    runtimeState: (projectId, sessionId, signal) =>
      request(
        `/runtime/state?${new URLSearchParams({ projectId, sessionId })}`,
        undefined,
        "GET",
        signal,
      ),
    search: (id, query, offset = 0, signal) =>
      request(
        `${projectPath(id)}/search?${new URLSearchParams({ q: query, offset: String(offset) })}`,
        undefined,
        "GET",
        signal,
      ),
    preferences: {
      read: () => request<UiPreferences>("/preferences"),
      write: async (preferences) => {
        await request("/preferences", preferences, "PUT");
      },
    },
    sources: (id) => request(`${projectPath(id)}/sources`),
    catalogs: (id) => request(`${projectPath(id)}/catalogs`),
    events: (id, cursor) =>
      request(
        `${projectPath(id)}/events${cursor ? `?${new URLSearchParams({ cursor })}` : ""}`,
      ),
    previewImport: (id, sourceName, content, sourceRelativePath) =>
      request(`${projectPath(id)}/imports/preview`, {
        sourceName,
        content,
        sourceRelativePath,
      }),
    previewImportBundle: (id, sources) =>
      request(`${projectPath(id)}/imports/preview`, { sources }),
    sourceStatus: (id) => request(`${projectPath(id)}/imports/source-status`),
    sourceContent: (id, name, signal) =>
      request(
        `${projectPath(id)}/sources/${encodeURIComponent(name)}`,
        undefined,
        "GET",
        signal,
      ),
    rebuildSearch: (id, signal) =>
      request(`${projectPath(id)}/search/rebuild`, {}, "POST", signal),
    backup: (id) => request(`${projectPath(id)}/backups`, {}),
    rotateBackups: (id, candidateIds) =>
      request(`${projectPath(id)}/backups/rotation`, { candidateIds }),
    commitImport: async (id, input) => {
      if (!epochs.has(id)) throw new Error("Project authority is unverified");
      return request(`${projectPath(id)}/imports/commit`, {
        ...input,
        expectedAuthorityEpoch: epochs.get(id),
      });
    },
    exportTasks: (id) => request(`${projectPath(id)}/imports/export`),
    restore: (id, backupId) =>
      request(`${projectPath(id)}/restores`, { backupId }),
  };
}
