import type {
  UiPreferences,
  UiPreferencesStore,
} from "../design/preferences.ts";
import type {ManagerSnapshot} from '../../../../packages/contracts/issues/manager.ts';

export type TaskReference = {availability:'available'|'unavailable'|'stale';relativePath:string;revision?:string;expectedRevision?:string;reason?:string;content?:string;redacted?:boolean};
export type FullProfileArchive = {format:string;backupId:string;manifest:unknown;restoreEndpoint:string};

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
  updatedAt?:string;
  blobIds?:readonly string[];
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
export type ConnectionRoute = "codex_app_agent" | "local_api_byok";
export type Connection = {
  verified: boolean;
  reason?: string;
  state?: string;
  payer?: "user_api_account";
  providerAuthority?: boolean;
  route?: ConnectionRoute;
  nativeSandbox?: boolean;
  cooperativeCancel?: boolean;
  modelAccess?: string;
  hostTransport?:{status:'unavailable'|'unverified';reason:string;transport:'websocket_over_stdio_proxy';checkedAt?:string};
  capabilities?:{executionConfigured?:boolean;nativeSandbox?:boolean;sandboxScope?:string;appHostSandboxVerified?:boolean};
};
export type Change = {
  expectedRevision: number;
  entity: StoredEntity;
  delete?: boolean;
};
export type RuntimeState = {
  recovery?:{canCancelUndispatched:boolean};
  capabilities?:{executionConfigured?:boolean;nativeSandbox?:boolean;sandboxScope?:string;appHostSandboxVerified?:boolean};
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
    decisionId?:string;
    description?: string;
    kind?: string;
    runId?: string;
    generation?: string;
    bindingId?: string;
    expiresAt?: number;
    reviewable?: boolean;
    source?:string;
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
  actorId?: string;
  occurredAt?: string;
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
  decisions(projectId:string,query?:Record<string,string|number>):Promise<import('../../../../packages/contracts/decisions/decision.ts').DecisionsPage>;
  decision(projectId:string,id:string):Promise<import('../../../../packages/contracts/decisions/decision.ts').DecisionView>;
  decisionCreate(projectId:string,input:Record<string,unknown>):Promise<import('../../../../packages/contracts/decisions/decision.ts').DecisionView>;
  decisionRespond(projectId:string,id:string,input:Record<string,unknown>):Promise<import('../../../../packages/contracts/decisions/decision.ts').DecisionResponse>;
  scheduler(projectId:string):Promise<import('../../../../packages/contracts/scheduler/queue.ts').QueueSnapshot>;
  schedulerPreview(projectId:string,input:Record<string,unknown>):Promise<import('../../../../packages/contracts/scheduler/queue.ts').QueuePreview>;
  schedulerAction(projectId:string,action:string,input:Record<string,unknown>):Promise<{entryId?:string;revision:number}>;
  recipes(projectId:string):Promise<{items:import('../../../../packages/contracts/execution-recipes/recipe.ts').RecipeExecutionView[]}>;
  recipePreview(projectId:string,input:Record<string,unknown>):Promise<import('../../../../packages/contracts/execution-recipes/recipe.ts').RecipePreview>;
  recipeStart(projectId:string,input:Record<string,unknown>):Promise<import('../../../../packages/contracts/execution-recipes/recipe.ts').RecipeExecutionView|{mode:'manual';agentRuns:number;taskId:string;target:string}>;
  recipeAction(projectId:string,id:string,action:'pause'|'resume'|'cancel'|'reconcile',input:Record<string,unknown>):Promise<import('../../../../packages/contracts/execution-recipes/recipe.ts').RecipeExecutionView>;
  project(projectId:string):Promise<Project>;
  autonomy(projectId:string):Promise<import('../../../../packages/contracts/autonomy/policy.ts').AutonomySnapshot>;
  autonomyPreview(projectId:string,input:Record<string,unknown>):Promise<import('../../../../packages/contracts/autonomy/policy.ts').AutonomyPreview>;
  autonomyAction(projectId:string,action:'save'|'pause'|'resume',input:Record<string,unknown>):Promise<import('../../../../packages/contracts/autonomy/policy.ts').AutonomySnapshot & {interrupts?:{runId:string;status:string;reason?:string}[]}>;
  graphStatus(projectId:string):Promise<import('../../../../packages/contracts/graph/code-graph.ts').GraphStatus>;
  rebuildGraph(projectId:string):Promise<import('../../../../packages/contracts/graph/code-graph.ts').GraphStatus>;
  graphPage(projectId:string,query:Record<string,string|number>):Promise<import('../../../../packages/contracts/graph/code-graph.ts').GraphPage>;
  graphNode(projectId:string,id:string,revision:string):Promise<import('../../../../packages/contracts/graph/code-graph.ts').GraphNodeDetail>;
  graphImpact(projectId:string,id:string,query:Record<string,string|number>):Promise<import('../../../../packages/contracts/graph/code-graph.ts').GraphImpact>;
  graphSource(projectId:string,query:Record<string,string|number>):Promise<import('../../../../packages/contracts/graph/code-graph.ts').GraphSourceExcerpt>;
  artifactCatalog(projectId:string,query:Record<string,string|number>):Promise<import('../../../../packages/contracts/artifacts/catalog.ts').ArtifactPage>;
  artifactDocument(projectId:string,id:string,version?:string):Promise<import('../../../../packages/contracts/artifacts/catalog.ts').ArtifactDocument>;
  previewDocumentProposal(projectId:string,input:Record<string,unknown>):Promise<any>;
  saveDocumentProposal(projectId:string,input:Record<string,unknown>,key?:string):Promise<any>;
  startSkillGeneration(projectId:string,input:Record<string,unknown>):Promise<any>;
  skillGeneration(projectId:string,id:string):Promise<any>;
  applySkillGeneration(projectId:string,id:string,input:Record<string,unknown>):Promise<any>;

  sessionCatalog(projectId:string,query:Record<string,string|number>):Promise<unknown>;
  sessionSearch(projectId:string,query:Record<string,string|number>):Promise<unknown>;
  sessionTranscript(projectId:string,sessionId:string,query:Record<string,string|number>):Promise<unknown>;
  teamRun(projectId:string,id:string):Promise<any>;
  teamCatalog(projectId:string):Promise<import('../../../../packages/contracts/team/assets.ts').TeamCatalog>;
  teamAsset(projectId:string,id:string):Promise<import('../../../../packages/contracts/team/assets.ts').AssetProfile>;
  teamPreview(projectId:string,input:Record<string,unknown>):Promise<import('../../../../packages/contracts/team/assets.ts').AssetPreview>;
  teamApply(projectId:string,input:Record<string,unknown>,idempotencyKey?:string):Promise<{assetId:string;version:number}>;
  assetCopyPreview(projectId:string,id:string):Promise<unknown>;
  assetResourceUrl(projectId:string,id:string,path:string):string;
  assetExportUrl(projectId:string,id:string):string;
  skillDiscovery(projectId:string,query:string):Promise<unknown>;
  skillSourcePreview(projectId:string,sourceRootId:string,relativePath:string):Promise<unknown>;
  teamMetrics(projectId:string,from:string,to:string):Promise<unknown>;
  startTeamGeneration(projectId:string,input:Record<string,unknown>):Promise<any>;
  teamGeneration(projectId:string,id:string):Promise<any>;

  taskManager(projectId:string,signal?:AbortSignal):Promise<ManagerSnapshot<StoredEntity>>;
  taskManagerCommand(projectId:string,input:Record<string,unknown>,idempotencyKey?:string):Promise<Record<string,unknown>>;
  stopPendingLink(projectId:string,linkId:string):Promise<{stopRequested:boolean}>;
  uploadAttachment(projectId:string,taskId:string,revision:number,file:{filename:string;mediaType:string;base64:string},idempotencyKey?:string):Promise<unknown>;
  attachmentUrl(projectId:string,taskId:string,attachmentId:string):string;
  taskReference(projectId:string,input:{taskId:string;relativePath:string;revision?:string|null}):Promise<TaskReference>;
  exportFullProfile(projectId:string):Promise<FullProfileArchive>;
  restoreFullProfile(projectId:string,backupId:string):Promise<{restoreId:string;requiresRestart:boolean;activeProfileChanged:boolean}>;
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
    route?: ConnectionRoute;
    connectionId: string;
    apiKey?: string;
    remember?: boolean;
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
  history(projectId:string,cursor?:string):Promise<{items:HistoryEvent[];nextCursor:string}>;
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

/** Bounded service metadata supports UI recovery without parsing human-readable text. */
export class HttpApiError extends Error {
  readonly status: number;
  readonly code?: string;
  readonly cyclePath?: readonly string[];
  constructor(status: number, code?: string, cyclePath?: readonly string[]) {
    super(`HTTP ${status}${code ? `: ${code}` : ""}`);
    this.name = "HttpApiError";
    this.status = status;
    this.code = code;
    this.cyclePath = cyclePath;
  }
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
        error?: { code?: unknown; details?: {cyclePath?:unknown} };
      } | null;
      const code = error?.error?.code;
      const safeCode =
        typeof code === "string" && /^[A-Za-z_]{1,80}$/.test(code)
          ? code
          : undefined;
      if (response.status === 401 && safeCode === "SESSION_REQUIRED") {
        csrfToken = undefined;
        epochs.clear();
      }
      const path=error?.error?.details?.cyclePath;
      const safePath=Array.isArray(path)&&path.length<=256&&path.every(id=>typeof id==='string'&&/^[A-Za-z0-9_-]{1,100}$/.test(id))?path as string[]:undefined;
      throw new HttpApiError(response.status, safeCode,safePath);
    }
    if (response.status === 204) return undefined as T;
    return response.json() as Promise<T>;
  }
  const params=(q:Record<string,string|number>)=>new URLSearchParams(Object.entries(q).map(([k,v])=>[k,String(v)]));
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
    decisions:(id,query={})=>request(projectPath(id)+'/decisions?'+new URLSearchParams(Object.entries(query).map(([k,v])=>[k,String(v)]))),
    decision:(id,decision)=>request(projectPath(id)+'/decisions/'+encodeURIComponent(decision)),
    decisionCreate:(id,input)=>request(projectPath(id)+'/decisions',input),
    decisionRespond:(id,decision,input)=>request(projectPath(id)+'/decisions/'+encodeURIComponent(decision)+'/respond',input),
    scheduler:id=>request(`${projectPath(id)}/scheduler`),
    schedulerPreview:(id,input)=>request(`${projectPath(id)}/scheduler/preview`,input),
    schedulerAction:(id,action,input)=>request(`${projectPath(id)}/scheduler/${encodeURIComponent(action)}`,input),
    recipes:id=>request(`${projectPath(id)}/execution-recipes`),
    recipePreview:(id,input)=>request(`${projectPath(id)}/execution-recipes/preview`,input),
    recipeStart:(id,input)=>request(`${projectPath(id)}/execution-recipes/start`,input),
    recipeAction:(id,execution,action,input)=>request(`${projectPath(id)}/execution-recipes/${encodeURIComponent(execution)}/${action}`,input),
    project:async id=>{const project=await request<Project>(projectPath(id));epochs.set(id,project.authorityEpoch);return project;},
    autonomy:id=>request(`${projectPath(id)}/autonomy`),
    autonomyPreview:(id,input)=>request(`${projectPath(id)}/autonomy/preview`,input),
    autonomyAction:(id,action,input)=>request(`${projectPath(id)}/autonomy/${action}`,input),
    sessionCatalog:(id,q)=>request(`${projectPath(id)}/sessions/catalog?${new URLSearchParams(Object.entries(q).map(([k,v])=>[k,String(v)]))}`),
    sessionSearch:(id,q)=>request(`${projectPath(id)}/sessions/search?${new URLSearchParams(Object.entries(q).map(([k,v])=>[k,String(v)]))}`),
    sessionTranscript:(id,session,q)=>request(`${projectPath(id)}/sessions/${encodeURIComponent(session)}/transcript?${new URLSearchParams(Object.entries(q).map(([k,v])=>[k,String(v)]))}`),
    teamRun:(id,run)=>request(`${projectPath(id)}/team/runs/${encodeURIComponent(run)}`),
    teamCatalog:id=>request(`${projectPath(id)}/team/catalog`),
    teamAsset:(id,asset)=>request(`${projectPath(id)}/team/assets/${encodeURIComponent(asset)}`),
    teamPreview:(id,input)=>request(`${projectPath(id)}/team/proposals/preview`,input),
    teamApply:(id,input,key=crypto.randomUUID())=>request(`${projectPath(id)}/team/proposals/apply`,{...input,...authority(id,Number(input.expectedRevision)),epoch:epochs.get(id),idempotencyKey:key}),
    assetCopyPreview:(id,asset)=>request(`${projectPath(id)}/team/assets/${encodeURIComponent(asset)}/copy-preview`,{}),
    assetResourceUrl:(id,asset,path)=>`/api/v1${projectPath(id)}/team/assets/${encodeURIComponent(asset)}/resources/${path.split('/').map(encodeURIComponent).join('/')}`,
    assetExportUrl:(id,asset)=>`/api/v1${projectPath(id)}/team/assets/${encodeURIComponent(asset)}/export`,
    skillDiscovery:(id,q)=>request(`${projectPath(id)}/team/skills/discovery?${new URLSearchParams({q})}`),
    skillSourcePreview:(id,sourceRootId,relativePath)=>request(`${projectPath(id)}/team/skills/source-preview`,{sourceRootId,relativePath}),
    teamMetrics:(id,from,to)=>request(`${projectPath(id)}/team/metrics?${new URLSearchParams({from,to})}`),
    startTeamGeneration:(id,input)=>request(`${projectPath(id)}/team/generation`,input),
    teamGeneration:(id,generation)=>request(`${projectPath(id)}/team/generation/${encodeURIComponent(generation)}`),
    graphStatus:id=>request(`${projectPath(id)}/graph/status`),
    rebuildGraph:id=>request(`${projectPath(id)}/graph/rebuild`,{}),
    graphPage:(id,q)=>request(`${projectPath(id)}/graph?${params(q)}`),
    graphNode:(id,node,revision)=>request(`${projectPath(id)}/graph/nodes/${encodeURIComponent(node)}?${params({revision})}`),
    graphImpact:(id,node,q)=>request(`${projectPath(id)}/graph/nodes/${encodeURIComponent(node)}/impact?${params(q)}`),
    graphSource:(id,q)=>request(`${projectPath(id)}/graph/source?${params(q)}`),
    artifactCatalog:(id,q)=>request(`${projectPath(id)}/artifacts?${params(q)}`),
    artifactDocument:(id,document,version)=>request(`${projectPath(id)}/artifacts/${encodeURIComponent(document)}${version?'?'+params({version}):''}`),
    previewDocumentProposal:(id,input)=>request(`${projectPath(id)}/artifacts/proposals/preview`,input),
    saveDocumentProposal:(id,input,key=crypto.randomUUID())=>request(`${projectPath(id)}/artifacts/proposals`,{...input,...authority(id,0),epoch:epochs.get(id),idempotencyKey:key}),
    startSkillGeneration:(id,input)=>request(`${projectPath(id)}/team/skills/generation`,input),
    skillGeneration:(id,job)=>request(`${projectPath(id)}/team/skills/generation/${encodeURIComponent(job)}`),
    applySkillGeneration:(id,job,input)=>request(`${projectPath(id)}/team/skills/generation/${encodeURIComponent(job)}/apply`,{...input,...authority(id,0),epoch:epochs.get(id)}),
    taskManager:(projectId,signal)=>request(`${projectPath(projectId)}/task-manager`,undefined,'GET',signal),
    stopPendingLink:(projectId,linkId)=>request(`${projectPath(projectId)}/task-manager/links/${encodeURIComponent(linkId)}/stop`,{}),
    taskManagerCommand:(projectId,input,idempotencyKey=crypto.randomUUID())=>{
      if(!epochs.has(projectId))return Promise.reject(new Error('Project authority is unverified'));
      return request(`${projectPath(projectId)}/task-manager/commands`,{...input,expectedAuthorityEpoch:epochs.get(projectId),idempotencyKey});
    },
    uploadAttachment:(projectId,taskId,revision,file,idempotencyKey=crypto.randomUUID())=>
      request(`${projectPath(projectId)}/tasks/${encodeURIComponent(taskId)}/attachments`,{...file,...authority(projectId,revision),idempotencyKey}),
    attachmentUrl:(projectId,taskId,attachmentId)=>`/api/v1${projectPath(projectId)}/tasks/${encodeURIComponent(taskId)}/attachments/${encodeURIComponent(attachmentId)}`,
    taskReference:(projectId,input)=>request(`${projectPath(projectId)}/task-manager/reference`,input),
    exportFullProfile:projectId=>request(`${projectPath(projectId)}/task-manager/export`,{}),
    restoreFullProfile:(projectId,backupId)=>request(`${projectPath(projectId)}/task-manager/import-backup`,{backupId}),
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
    history:(id,cursor)=>request(`${projectPath(id)}/history${cursor?`?${new URLSearchParams({cursor})}`:''}`),
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
