import { useEffect, useState, useRef, useLayoutEffect } from "react";
import type { FormEvent } from "react";
import { createHttpApi, HttpApiError } from "../api/client.ts";
import type {
  Connection,
  EntityKind,
  Project,
  StoredEntity,
  RuntimeState,
} from "../api/client.ts";
import { newTask, plannedFiles } from "../api/task.ts";
import {
  canSend,
  canAccept,
  runBlocksScopeChange,
  canStopRun,
  canAnswerApproval,
} from "../api/policy.ts";
import {
  startSessionPolling,
  startConnectionPolling,
} from "../api/session-poll.ts";
import {
  isExecutionTarget,
  attachTaskToSession,
  loadSavedSessionTarget,
} from "../api/session-target.ts";
import type { RunState } from "../api/policy.ts";
import { createLatestRequest } from "../api/latest-request.ts";
import { visibleAssistantDrafts } from "../api/visible-drafts.ts";
import { ConnectionControls } from "./ConnectionControls.tsx";
import { TaskRelations } from "./TaskRelations.tsx";
import {GraphExplorer} from '../features/graph/GraphExplorer.tsx';
import {SkillGenerator} from '../features/skills/SkillGenerator.tsx';
import {ArtifactExplorer} from '../features/artifacts/ArtifactExplorer.tsx';
import {WorkflowManager} from '../features/workflows/WorkflowManager.tsx';
import {SessionsCatalog} from '../features/sessions/SessionsCatalog.tsx';
import {TeamManager} from '../features/team/TeamManager.tsx';
import type {WorkflowRegistry} from '../../../../packages/contracts/workflows/workflow.ts';
import {TaskManager} from '../features/tasks/TaskManager.tsx';
import {
  SessionContext,
  RuntimeSummary,
  RuntimeDiff,
  RuntimeChecks,
} from "./SessionContext.tsx";
import {
  createDraftRegistry,
  sendWithDraftAck,
  type DraftLease,
} from "../api/draft-registry.ts";
import { mergeJournalMessages } from "../api/message-history.ts";
import {
  applyUiPreferences,
  loadUiPreferences,
  saveUiPreferences,
} from "../design/preferences.ts";
import type { UiPreferences } from "../design/preferences.ts";
import { uiLabel } from "../locales/messages.ts";
import { appLabel } from "../locales/app.ts";
import type { AppLabel } from "../locales/app.ts";
import {
  Backup,
  ImportTasks,
  Sources,
  TaskHistory,
  Catalog,
} from "./Operations.tsx";

const api = createHttpApi();
const draftRegistry = createDraftRegistry();
const sections = [
  "overview",
  "tasks",
  "sessions",
  "agents",
  "skills",
  "projectMap",
  "documents",
  "checks",
  "search",
  "import",
  "backup",
  "settings",
] as const;
type Section = (typeof sections)[number];
const statuses = [
  "backlog",
  "ready",
  "in_progress",
  "review",
  "verification",
  "awaiting_acceptance",
  "done",
  "cancelled",
];
type Text = (key: AppLabel) => string;

export function App() {
  const [preferences, setPreferences] = useState<UiPreferences>({
    locale: "ru",
    theme: "system",
  });
  const [projects, setProjects] = useState<Project[]>([]);
  const [projectId, setProjectId] = useState("");
  const [section, setSection] = useState<Section>("overview");
  const [linkedSession,setLinkedSession]=useState<{projectId:string;sessionId:string;messageId?:string}|null>(null);
  const [linkedTask,setLinkedTask]=useState<{projectId:string;id:string;tab?:"summary"|"files"}|null>(null);
  const [linkedAsset,setLinkedAsset]=useState<{projectId:string;id:string;kind:"agent"|"skill"}|null>(null);
  const [linkedGraph,setLinkedGraph]=useState<{projectId:string;id:string}|null>(null);
  const [ready, setReady] = useState(false);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");
  const [code, setCode] = useState("");
  const [connection, setConnection] = useState<Connection | null>(null);
  const connectionEpoch = useRef(0);
  const appliedAnchor=useRef('');
  function connectionChanged(current: Connection) {
    connectionEpoch.current++;
    setConnection(current);
  }
  const [mobileNav, setMobileNav] = useState(false);
  const t: Text = (key) => appLabel(preferences.locale, key);
  const label = (key: Section) =>
    ["search", "import", "backup"].includes(key)
      ? t(key as AppLabel)
      : uiLabel(
          preferences.locale,
          `nav.${key}` as Parameters<typeof uiLabel>[1],
        );
  async function initialise(pairCode?: string) {
    setBusy(true);
    setNotice("");
    try {
      await api.pair(pairCode);
      const [list, appearance, runtime] = await Promise.all([
        api.projects(),
        loadUiPreferences(api.preferences),
        api.connection(),
      ]);
      setProjects(list);
      setProjectId((current) =>
        list.some((p) => p.id === current) ? current : (list[0]?.id ?? ""),
      );
      setPreferences(appearance);
      connectionChanged(runtime);
      setReady(true);
      setCode("");
    } catch (error) {
      if (error instanceof HttpApiError && error.status === 401) {
        setReady(false);
        setProjects([]);
        setProjectId("");
        connectionEpoch.current++;
        setConnection(null);
        // A fresh profile has no local session yet. Guide pairing instead of reporting a failed operation.
        setNotice(
          error.code === "SESSION_REQUIRED" && !pairCode
            ? ""
            : error.code === "PAIRING_INVALID"
              ? t("pairingInvalid")
              : `${t("error")}: ${String(error)}`,
        );
      } else setNotice(`${t("error")}: ${String(error)}`);
    } finally {
      setBusy(false);
    }
  }
  useEffect(() => {
    void initialise();
  }, []);
  useEffect(()=>{
    if(!ready)return;
    const openAnchor=()=>{if(appliedAnchor.current===location.hash)return;const q=new URLSearchParams(location.hash.slice(1)),p=q.get('project'),session=q.get('session'),message=q.get('message');
      if(!p||!session||!message||!projects.some(project=>project.id===p)||[session,message].some(id=>id.length>200||/[\\\0\r\n]/.test(id)))return;
      appliedAnchor.current=location.hash;setProjectId(p);setLinkedSession({projectId:p,sessionId:session,messageId:message});setSection('sessions');
    };openAnchor();window.addEventListener('hashchange',openAnchor);return()=>window.removeEventListener('hashchange',openAnchor);
  },[ready,projects]);
  useEffect(() => {
    if (!ready) return;
    return startConnectionPolling({
      read: () => api.connection(),
      version: () => connectionEpoch.current,
      publish: setConnection,
      error: () =>
        setConnection({
          verified: false,
          reason: "connection_status_unavailable",
        }),
    });
  }, [ready]);
  useEffect(() => {
    const media = matchMedia("(prefers-color-scheme: dark)");
    const apply = () =>
      applyUiPreferences(
        document.documentElement,
        preferences,
        media.matches ? "dark" : "light",
      );
    apply();
    media.addEventListener("change", apply);
    return () => media.removeEventListener("change", apply);
  }, [preferences]);
  return (
    <div className="app">
      <a className="skip" href="#main">
        {uiLabel(preferences.locale, "action.skipToContent")}
      </a>
      <aside
        className={`navigation ${mobileNav ? "open" : ""}`}
        aria-label={t("menu")}
      >
        <div className="brand">
          Product-Agent OS<span>{t("local")}</span>
        </div>
        <label>
          {t("project")}
          <select
            value={projectId}
            onChange={(e) => setProjectId(e.target.value)}
            disabled={!ready}
          >
            <option value="">—</option>
            {projects.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>
        </label>
        <nav>
          {sections.map((key) => (
            <button
              key={key}
              disabled={!ready}
              aria-current={section === key ? "page" : undefined}
              onClick={() => {
                setSection(key);
                setMobileNav(false);
              }}
            >
              {label(key)}
            </button>
          ))}
        </nav>
        <div className="connection">
          <span className="eyebrow">{t("connection")}</span>
          <strong>
            {connection?.verified ? t("verified") : t("unverified")}
          </strong>
          <small>{connection?.reason}</small>
        </div>
      </aside>
      <div className="workspace">
        <header>
          <button
            className="mobile-menu"
            onClick={() => setMobileNav(!mobileNav)}
            aria-expanded={mobileNav}
          >
            {t("menu")}
          </button>
          <div
            className="breadcrumb"
            title={`${projects.find((p) => p.id === projectId)?.name ?? "Product-Agent OS"} / ${label(section)}`}
          >
            {projects.find((p) => p.id === projectId)?.name ??
              "Product-Agent OS"}
            <span>/</span>
            {label(section)}
          </div>
          <button onClick={() => void initialise()} disabled={busy}>
            {t("reload")}
          </button>
        </header>
        <main id="main" tabIndex={-1}>
          <div className="page-heading">
            <div>
              <p className="eyebrow">Product-Agent OS · M2</p>
              <h1>{label(section)}</h1>
            </div>
            <span className="quiet">
              {ready ? t("local") : t("unverified")}
            </span>
          </div>
          {notice && (
            <p role="alert" className="notice">
              {notice}
            </p>
          )}
          {!ready ? (
            <section className="panel narrow">
              <h2>{t("connect")}</h2>
              <p role="status">{t("pairingHint")}</p>
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  void initialise(code);
                }}
              >
                <label>
                  {t("code")}
                  <input
                    autoComplete="off"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    required
                  />
                </label>
                <button className="primary" disabled={busy}>
                  {busy ? t("loading") : t("connect")}
                </button>
              </form>
            </section>
          ) : section === "settings" ? (
            <><Settings
              preferences={preferences}
              onPreferences={setPreferences}
              connection={connection}
              onConnection={connectionChanged}
              t={t}
              onProject={async (name, root) => {
                await api.createProject(name, root);
                await initialise();
              }}
            />{projectId&&<WorkflowManager key={projectId} api={api} projectId={projectId} locale={preferences.locale}/>}</>
          ) : !projectId ? (
            <Empty text={t("empty")} />
          ) : section === "tasks" ? (
            <TaskManager key={projectId} api={api} projectId={projectId} locale={preferences.locale} initialTaskId={linkedTask?.projectId===projectId?linkedTask.id:undefined} initialTab={linkedTask?.projectId===projectId?linkedTask.tab:undefined} onOpenSession={sessionId=>{setLinkedSession({projectId,sessionId});setSection('sessions');}} />
          ) : section === "sessions" ? (
            <SessionsCatalog key={projectId} api={api} projectId={projectId} locale={preferences.locale}
              initialSessionId={linkedSession?.projectId===projectId?linkedSession.sessionId:undefined}
              initialMessageId={linkedSession?.projectId===projectId?linkedSession.messageId:undefined}
              renderSession={entity=><Session key={entity.id} entity={entity} connection={connection} t={t} locale={preferences.locale}/>}
              onOpenTask={(id,tab)=>{setLinkedTask({projectId,id,tab});setSection('tasks');}}
              onOpenAgent={id=>{setLinkedAsset({projectId,id,kind:'agent'});setSection('agents');}}/>
          ) : section === "search" ? (
            <ArtifactExplorer key={`${projectId}:all`} api={api} projectId={projectId} locale={preferences.locale} mode="all" onOpenTask={id=>{setLinkedTask({projectId,id});setSection('tasks');}} onOpenSession={sessionId=>{setLinkedSession({projectId,sessionId});setSection('sessions');}} onOpenGraph={id=>{setLinkedGraph({projectId,id});setSection('projectMap');}}/>
          ) : section === "checks" ? (
            <ArtifactExplorer key={`${projectId}:checks`} api={api} projectId={projectId} locale={preferences.locale} mode="checks" onOpenTask={id=>{setLinkedTask({projectId,id});setSection('tasks');}} onOpenSession={sessionId=>{setLinkedSession({projectId,sessionId});setSection('sessions');}} onOpenGraph={id=>{setLinkedGraph({projectId,id});setSection('projectMap');}}/>
          ) : section === "import" ? (
            <ImportTasks
              key={projectId}
              api={api}
              projectId={projectId}
              t={t}
            />
          ) : section === "backup" ? (
            <Backup key={projectId} api={api} projectId={projectId} t={t} />
          ) : section === "documents" ? (
            <ArtifactExplorer key={`${projectId}:documents`} api={api} projectId={projectId} locale={preferences.locale} mode="documents" onOpenTask={id=>{setLinkedTask({projectId,id});setSection('tasks');}} onOpenSession={sessionId=>{setLinkedSession({projectId,sessionId});setSection('sessions');}} onOpenGraph={id=>{setLinkedGraph({projectId,id});setSection('projectMap');}}/>
          ) : section === "agents" || section === "skills" ? (
            <><TeamManager key={`${projectId}:${section}`} api={api} projectId={projectId} kind={section==='agents'?'agent':'skill'} locale={preferences.locale}
              initialAssetId={linkedAsset?.projectId===projectId&&linkedAsset.kind===(section==='agents'?'agent':'skill')?linkedAsset.id:undefined}
              onOpenAsset={(kind,id)=>{setLinkedAsset({projectId,id,kind});setSection(kind==='agent'?'agents':'skills');}}
              onOpenSession={sessionId=>{setLinkedSession({projectId,sessionId});setSection('sessions');}}
              onOpenTask={id=>{setLinkedTask({projectId,id});setSection('tasks');}}/>{section==='skills'&&<SkillGenerator key={projectId} api={api} projectId={projectId} locale={preferences.locale} onOpenAsset={(kind,id)=>{setLinkedAsset({projectId,id,kind});setSection(kind==='skill'?'skills':'agents');}} onOpenSession={sessionId=>{setLinkedSession({projectId,sessionId});setSection('sessions');}}/>}</>
          ) : section === "projectMap" ? (
            <GraphExplorer key={projectId} api={api} projectId={projectId} locale={preferences.locale} initialNodeId={linkedGraph?.projectId===projectId?linkedGraph.id:undefined} onOpenTask={id=>{setLinkedTask({projectId,id});setSection('tasks');}}/>
          ) : section === "overview" ? (
            <Overview
              projectId={projectId}
              t={t}
              onTasks={() => setSection("tasks")}
            />
          ) : (
            <Empty text={t("unavailable")} />
          )}
        </main>
      </div>
    </div>
  );
}

function Empty({ text }: { text: string }) {
  return (
    <div className="empty">
      <div className="empty-rule" />
      <p>{text}</p>
    </div>
  );
}
function useEntities(projectId: string, kind: EntityKind, parentId?: string) {
  const [items, setItems] = useState<StoredEntity[]>([]),
    [loading, setLoading] = useState(true),
    [error, setError] = useState(""),
    [hasMore, setHasMore] = useState(false);
  async function load(append = false) {
    setLoading(true);
    setError("");
    try {
      const result = await api.entities(
        projectId,
        kind,
        parentId,
        append ? items.length : 0,
      );
      setItems((previous) =>
        append ? [...previous, ...result.items] : result.items,
      );
      setHasMore(result.hasMore);
    } catch (cause) {
      setError(String(cause));
    } finally {
      setLoading(false);
    }
  }
  useEffect(() => {
    setItems([]);
    void load();
  }, [projectId, kind, parentId]);
  return { items, loading, error, hasMore, load };
}
function Overview({
  projectId,
  t,
  onTasks,
}: {
  projectId: string;
  t: Text;
  onTasks: () => void;
}) {
  const tasks = useEntities(projectId, "task");
  return (
    <section className="panel">
      <h2>{t("source")}</h2>
      {tasks.loading ? (
        <p role="status">{t("loading")}</p>
      ) : tasks.error ? (
        <p role="alert">{tasks.error}</p>
      ) : (
        <>
          <p>
            {t("taskCount")}: {tasks.items.length}
            {tasks.hasMore ? "+" : ""}
          </p>
          <button onClick={onTasks}>{t("details")}</button>
        </>
      )}
      <Sources api={api} projectId={projectId} t={t} />
    </section>
  );
}
function Settings({
  preferences,
  onPreferences,
  t,
  onProject,
  connection,
  onConnection,
}: {
  preferences: UiPreferences;
  onPreferences: (p: UiPreferences) => void;
  t: Text;
  onProject: (name: string, root: string) => Promise<void>;
  connection: Connection | null;
  onConnection: (connection: Connection) => void;
}) {
  const [draft, setDraft] = useState(preferences),
    [status, setStatus] = useState(""),
    [busy, setBusy] = useState(false);
  async function save(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    try {
      onPreferences(await saveUiPreferences(api.preferences, draft));
      setStatus(t("saved"));
    } catch (error) {
      setStatus(`${t("error")}: ${error}`);
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="settings-grid">
      <section className="panel">
        <h2>{uiLabel(preferences.locale, "nav.settings")}</h2>
        <form onSubmit={save}>
          <label>
            {uiLabel(preferences.locale, "preferences.language")}
            <select
              aria-label={uiLabel(preferences.locale, "preferences.language")}
              value={draft.locale}
              onChange={(e) =>
                setDraft({
                  ...draft,
                  locale: e.target.value as UiPreferences["locale"],
                })
              }
            >
              <option value="ru">Русский</option>
              <option value="en">English</option>
            </select>
          </label>
          <label>
            {uiLabel(preferences.locale, "preferences.theme")}
            <select
              aria-label={uiLabel(preferences.locale, "preferences.theme")}
              value={draft.theme}
              onChange={(e) =>
                setDraft({
                  ...draft,
                  theme: e.target.value as UiPreferences["theme"],
                })
              }
            >
              {(["light", "dark", "system"] as const).map((theme) => (
                <option key={theme} value={theme}>
                  {uiLabel(preferences.locale, `theme.${theme}`)}
                </option>
              ))}
            </select>
          </label>
          <button disabled={busy} className="primary">
            {uiLabel(preferences.locale, "preferences.save")}
          </button>
          <p role="status">{status}</p>
        </form>
      </section>
      <section className="panel">
        <h2>{t("addProject")}</h2>
        <form
          onSubmit={async (e) => {
            e.preventDefault();
            const form = e.currentTarget;
            const data = new FormData(form);
            setBusy(true);
            try {
              await onProject(
                String(data.get("name")),
                String(data.get("root")),
              );
              form.reset();
            } catch (error) {
              setStatus(`${t("error")}: ${error}`);
            } finally {
              setBusy(false);
            }
          }}
        >
          <label>
            {t("name")}
            <input name="name" required />
          </label>
          <label>
            {t("root")}
            <input name="root" required autoComplete="off" />
          </label>
          <button disabled={busy}>{t("addProject")}</button>
        </form>
      </section>
      <ConnectionControls
        api={api}
        connection={connection}
        onConnection={onConnection}
        t={t}
      />
      <QuitService t={t} />
    </div>
  );
}
function QuitService({ t }: { t: Text }) {
  const [confirmed, setConfirmed] = useState(false),
    [busy, setBusy] = useState(false),
    [requested, setRequested] = useState(false),
    [error, setError] = useState("");
  return (
    <section className="panel">
      <h2>{t("quit")}</h2>
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          if (!confirmed) return;
          setBusy(true);
          setError("");
          try {
            const result = await api.quit();
            if (result.status !== "quit_requested")
              throw new Error("QUIT_RESPONSE_UNVERIFIED");
            setRequested(true);
          } catch (cause) {
            setError(String(cause));
          } finally {
            setBusy(false);
          }
        }}
      >
        <label className="checkbox">
          <input
            type="checkbox"
            checked={confirmed}
            disabled={busy || requested}
            onChange={(e) => setConfirmed(e.target.checked)}
          />
          {t("quitConfirm")}
        </label>
        <button disabled={!confirmed || busy || requested} className="danger">
          {t("quit")}
        </button>
        <p role="alert">{error}</p>
        {requested && <p role="status">{t("quitRequested")}</p>}
      </form>
    </section>
  );
}

function Tasks({ projectId, t }: { projectId: string; t: Text }) {
  const list = useEntities(projectId, "task");
  const [selected, setSelected] = useState<string | null>(null),
    [creating, setCreating] = useState(false),
    [error, setError] = useState("");
  const task = list.items.find((item) => item.id === selected);
  const [view, setView] = useState<"list" | "board">("list");
  async function save(entity: StoredEntity, remove = false) {
    await api.command(projectId, [
      {
        expectedRevision: entity.revision,
        entity,
        ...(remove ? { delete: true } : {}),
      },
    ]);
    await list.load();
    if (remove) setSelected(null);
  }
  return (
    <div className="task-layout">
      <section className="panel task-list">
        <div className="tabs">
          <button
            aria-pressed={view === "list"}
            onClick={() => setView("list")}
          >
            {t("list")}
          </button>
          <button
            aria-pressed={view === "board"}
            onClick={() => setView("board")}
          >
            {t("board")}
          </button>
        </div>
        <div className="section-heading">
          <h2>
            {t("taskCount")}: {list.items.length}
            {list.hasMore ? "+" : ""}
          </h2>
          <button className="primary" onClick={() => setCreating(!creating)}>
            {t("create")}
          </button>
        </div>
        {creating && (
          <TaskForm
            t={t}
            onSave={async (title, body, criteria, extra) => {
              try {
                const task = newTask(projectId, title, body, criteria);
                await save({ ...task, data: { ...task.data, ...extra } });
                setCreating(false);
              } catch (cause) {
                setError(String(cause));
              }
            }}
          />
        )}
        {(list.error || error) && <p role="alert">{list.error || error}</p>}
        {list.loading && <p role="status">{t("loading")}</p>}
        {!list.loading && !list.items.length && <Empty text={t("empty")} />}
        {view === "board" ? (
          <div className="kanban">
            {[
              "backlog",
              "ready",
              "in_progress",
              "review",
              "verification",
              "awaiting_acceptance",
              "closed",
            ].map((column) => (
              <section key={column} className="kanban-column">
                <h3>{column === "closed" ? t("closed") : column}</h3>
                <ul className="records">
                  {list.items
                    .filter((item) =>
                      column === "closed"
                        ? ["done", "cancelled"].includes(item.status ?? "")
                        : item.status === column,
                    )
                    .map((item) => (
                      <li key={item.id}>
                        <button onClick={() => setSelected(item.id)}>
                          <span className="mono">{item.publicKey}</span>
                          <strong>{item.title}</strong>
                          <span className="badge">{item.status}</span>
                        </button>
                      </li>
                    ))}
                </ul>
              </section>
            ))}
          </div>
        ) : (
          <ul className="records">
            {list.items.map((item) => (
              <li key={item.id}>
                <button
                  aria-current={selected === item.id ? "true" : undefined}
                  onClick={() => setSelected(item.id)}
                >
                  <span className="mono quiet">
                    {item.publicKey ??
                      String(item.data?.key ?? item.id.slice(0, 8))}
                  </span>
                  <strong>
                    {item.title ?? String(item.data?.title ?? "")}
                  </strong>
                  <span className="badge">{item.status}</span>
                </button>
              </li>
            ))}
          </ul>
        )}
        {list.hasMore && (
          <button onClick={() => void list.load(true)} disabled={list.loading}>
            {t("more")}
          </button>
        )}
      </section>
      {task && (
        <TaskDetail
          key={`${task.id}:${task.revision}`}
          entity={task}
          t={t}
          onSave={save}
          onRefresh={() => list.load()}
          onClose={() => setSelected(null)}
        />
      )}
    </div>
  );
}
function TaskForm({
  t,
  entity,
  onSave,
}: {
  t: Text;
  entity?: StoredEntity;
  onSave: (
    title: string,
    body: string,
    criteria: string[],
    extra: Record<string, unknown>,
  ) => Promise<void>;
}) {
  const [busy, setBusy] = useState(false);
  return (
    <form
      onSubmit={async (e) => {
        e.preventDefault();
        const data = new FormData(e.currentTarget);
        setBusy(true);
        try {
          await onSave(
            String(data.get("title")),
            String(data.get("body")),
            String(data.get("criteria"))
              .split("\n")
              .map((s) => s.trim())
              .filter(Boolean),
            {
              technicalValue: String(data.get("technicalValue")),
              productValue: String(data.get("productValue")),
              priority: String(data.get("priority")) || null,
              estimateSeconds: data.get("estimate")
                ? Number(data.get("estimate"))
                : null,
              startDate: String(data.get("startDate")) || null,
              dueDate: String(data.get("dueDate")) || null,
              risks: String(data.get("risks")).split("\n").filter(Boolean),
              agentAssignments: String(data.get("agents"))
                .split("\n")
                .filter(Boolean),
              artifactReferences: String(data.get("artifacts"))
                .split("\n")
                .filter(Boolean),
              files: plannedFiles(
                String(data.get("files")),
                entity?.data?.files,
              ),
            },
          );
        } finally {
          setBusy(false);
        }
      }}
    >
      <label>
        {t("title")}
        <input name="title" defaultValue={entity?.title} required />
      </label>
      <details>
        <summary>{t("details")}</summary>
        <div className="advanced-fields">
          {(["technicalValue", "productValue"] as const).map((key) => (
            <label key={key}>
              {t(key)}
              <textarea
                name={key}
                defaultValue={String(entity?.data?.[key] ?? "")}
                rows={2}
              />
            </label>
          ))}
          <label>
            {t("priority")}
            <select
              name="priority"
              defaultValue={String(entity?.data?.priority ?? "")}
            >
              <option value="">—</option>
              {["highest", "high", "medium", "low", "lowest"].map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>
          </label>
          <label>
            {t("estimate")}
            <input
              name="estimate"
              type="number"
              min="0"
              step="1"
              defaultValue={
                entity?.data?.estimateSeconds == null
                  ? ""
                  : Number(entity.data.estimateSeconds)
              }
            />
          </label>
          {(["startDate", "dueDate"] as const).map((key) => (
            <label key={key}>
              {t(key)}
              <input
                name={key}
                type="date"
                defaultValue={String(entity?.data?.[key] ?? "")}
              />
            </label>
          ))}
          {(["risks", "agents", "artifacts", "files"] as const).map((key) => {
            const source =
              entity?.data?.[
                key === "agents"
                  ? "agentAssignments"
                  : key === "artifacts"
                    ? "artifactReferences"
                    : key
              ];
            return (
              <label key={key}>
                {t(key)}
                <textarea
                  name={key}
                  rows={3}
                  defaultValue={
                    Array.isArray(source)
                      ? source
                          .map((value) =>
                            key === "files"
                              ? String(
                                  (value as { relativePath: string })
                                    .relativePath,
                                )
                              : String(value),
                          )
                          .join("\n")
                      : ""
                  }
                />
              </label>
            );
          })}
        </div>
      </details>
      <label>
        {t("description")}
        <textarea name="body" defaultValue={String(entity?.data?.summary??entity?.body??'')} rows={4} />
      </label>
      <label>
        {t("criteria")}
        <textarea
          name="criteria"
          rows={3}
          defaultValue={
            Array.isArray(entity?.data?.acceptanceCriteria)
              ? entity.data.acceptanceCriteria.join("\n")
              : ""
          }
        />
      </label>
      <button disabled={busy} className="primary">
        {t("save")}
      </button>
    </form>
  );
}
function TaskDetail({
  entity,
  t,
  onSave,
  onRefresh,
  onClose,
}: {
  entity: StoredEntity;
  t: Text;
  onSave: (entity: StoredEntity, remove?: boolean) => Promise<void>;
  onRefresh: () => Promise<void>;
  onClose: () => void;
}) {
  const [tab, setTab] = useState("details"),
    [notice, setNotice] = useState(""),
    [deleting, setDeleting] = useState(false),
    [pending, setPending] = useState(false);
  const criteria = Array.isArray(entity.data?.acceptanceCriteria)
    ? entity.data.acceptanceCriteria.map(String)
    : [];
  async function mutate(next: StoredEntity, remove = false) {
    setPending(true);
    try {
      await onSave(next, remove);
      setNotice(t("saved"));
    } catch (error) {
      setNotice(`${t("error")}: ${error}`);
    } finally {
      setPending(false);
    }
  }
  return (
    <aside className="panel task-detail" aria-label={t("details")}>
      <div className="section-heading">
        <h2>{entity.publicKey ?? t("details")}</h2>
        <button onClick={onClose}>{t("close")}</button>
      </div>
      <div className="tabs">
        {(["details", "comments", "history"] as const).map((key) => (
          <button
            key={key}
            aria-pressed={tab === key}
            onClick={() => setTab(key)}
          >
            {t(key)}
          </button>
        ))}
      </div>
      <p role="status">{notice}</p>
      {tab === "details" ? (
        <>
          <TaskForm
            t={t}
            entity={entity}
            onSave={async (title, body, acceptanceCriteria, extra) =>
              mutate({
                ...entity,
                title,
                body,
                data: {
                  ...entity.data,
                  title,
                  summary: body,
                  acceptanceCriteria,
                  ...extra,
                },
              })
            }
          />
          <label>
            Status
            <select
              value={entity.status}
              disabled={pending}
              onChange={(e) =>
                void mutate({
                  ...entity,
                  status: e.target.value,
                  data: { ...entity.data, status: e.target.value },
                })
              }
            >
              {statuses.map((status) => (
                <option
                  key={status}
                  value={status}
                  disabled={status === "done"}
                >
                  {status}
                </option>
              ))}
            </select>
          </label>
          <ManualAcceptance
            entity={entity}
            t={t}
            onAccepted={async () => {
              await onRefresh();
              onClose();
            }}
          />
          <TaskRelations
            api={api}
            entity={entity}
            t={t}
            onSave={(next) => mutate(next)}
          />
          <dl className="task-metadata">
            <dt>{t("actual")}</dt>
            <dd className="mono">
              {JSON.stringify(entity.data?.actual ?? null)}
            </dd>
            <dt>{t("creator")}</dt>
            <dd className="mono">
              {JSON.stringify(entity.data?.creator ?? null)}
            </dd>
            <dt>{t("relations")}</dt>
            <dd className="mono">{JSON.stringify(entity.data?.links ?? [])}</dd>
          </dl>
          <button className="danger" onClick={() => setDeleting(!deleting)}>
            {t("remove")}
          </button>
          {deleting && (
            <div className="confirm">
              <p>{t("confirmDelete")}</p>
              <button
                disabled={pending}
                onClick={() => void mutate(entity, true)}
              >
                {t("confirmDelete")}
              </button>
              <button onClick={() => setDeleting(false)}>{t("cancel")}</button>
            </div>
          )}
        </>
      ) : tab === "comments" ? (
        <Comments entity={entity} t={t} />
      ) : (
        <History entity={entity} t={t} />
      )}
    </aside>
  );
}
function Comments({ entity, t }: { entity: StoredEntity; t: Text }) {
  const list = useEntities(entity.projectId, "comment", entity.id),
    [error, setError] = useState(""),
    [pending, setPending] = useState(false);
  return (
    <>
      <ul className="comments">
        {list.items.map((comment) => (
          <li key={comment.id}>
            <small>
              {comment.data?.category === "manual_check"
                ? t("check")
                : comment.data?.category === "owner_acceptance"
                  ? t("acceptance")
                  : t("comments")}
              {comment.data?.outcome
                ? ` · ${String(comment.data.outcome)}`
                : ""}
              {typeof comment.data?.accepted === "boolean"
                ? ` · ${comment.data.accepted ? t("accept") : t("deny")}`
                : ""}
            </small>
            <p>{comment.body}</p>
            <small className="mono">r{comment.revision}</small>
          </li>
        ))}
      </ul>
      <p role="alert">{error || list.error}</p>
      {list.hasMore && (
        <>
          <p role="status">{t("partial")}</p>
          <button
            type="button"
            disabled={list.loading || pending}
            onClick={() => void list.load(true)}
          >
            {t("more")}
          </button>
        </>
      )}
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          const form = e.currentTarget,
            data = new FormData(form);
          setPending(true);
          try {
            await api.command(entity.projectId, [
              {
                expectedRevision: 0,
                entity: {
                  id: crypto.randomUUID(),
                  projectId: entity.projectId,
                  parentId: entity.id,
                  kind: "comment",
                  body: String(data.get("comment")),
                  revision: 0,
                },
              },
            ]);
            form.reset();
            await list.load();
          } catch (cause) {
            setError(String(cause));
          } finally {
            setPending(false);
          }
        }}
      >
        <label>
          {t("comment")}
          <textarea name="comment" required rows={3} />
        </label>
        <button disabled={pending}>{t("comment")}</button>
      </form>
    </>
  );
}
/** Manual evidence and explicit owner acceptance use distinct audited service commands. */
function ManualAcceptance({
  entity,
  t,
  onAccepted,
}: {
  entity: StoredEntity;
  t: Text;
  onAccepted: () => Promise<void>;
}) {
  const criteria = Array.isArray(entity.data?.acceptanceCriteria)
    ? entity.data.acceptanceCriteria.map(String)
    : [];
  const [receipt, setReceipt] = useState<{
    checkId: string;
    revision: number;
    passed: boolean;
  } | null>(null);
  const [note, setNote] = useState(""),
    [status, setStatus] = useState(""),
    [busy, setBusy] = useState(false);
  async function accept(accepted: boolean) {
    if (!receipt) return;
    setBusy(true);
    try {
      await api.accept(
        entity.projectId,
        entity.id,
        entity.revision,
        receipt.checkId,
        accepted,
        note,
      );
      setStatus(t("saved"));
      await onAccepted();
    } catch (error) {
      setStatus(`${t("error")}: ${error}`);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="acceptance">
      <h3>{t("check")}</h3>
      <p className="quiet">{t("acceptanceHint")}</p>
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          const data = new FormData(e.currentTarget);
          const passed =
            criteria.length > 0 &&
            criteria.every((_, index) => data.get(`check-${index}`) === "on");
          setBusy(true);
          try {
            const result = await api.manualCheck(
              entity.projectId,
              entity.id,
              entity.revision,
              passed ? "passed" : "failed",
              String(data.get("evidence")),
            );
            setReceipt({
              checkId: result.checkId,
              revision: entity.revision,
              passed,
            });
            setStatus(t("saved"));
          } catch (error) {
            setStatus(`${t("error")}: ${error}`);
          } finally {
            setBusy(false);
          }
        }}
      >
        {criteria.map((criterion, index) => (
          <label className="checkbox" key={index}>
            <input type="checkbox" name={`check-${index}`} />
            {criterion}
          </label>
        ))}
        <label>
          {t("evidence")}
          <input name="evidence" required />
        </label>
        <button disabled={busy || !criteria.length}>{t("check")}</button>
      </form>
      <h3>{t("acceptance")}</h3>
      <label>
        {t("comment")}
        <textarea value={note} onChange={(e) => setNote(e.target.value)} />
      </label>
      <div className="actions">
        <button
          disabled={
            busy ||
            !canAccept(
              entity.status ?? "",
              entity.data?.runState === "running"
                ? "running"
                : entity.data?.runState === "uncertain"
                  ? "uncertain"
                  : "idle",
              criteria,
              criteria.map(() => receipt?.passed === true),
            ) ||
            receipt?.revision !== entity.revision
          }
          onClick={() => void accept(true)}
        >
          {t("accept")}
        </button>
        <button
          disabled={busy || !receipt || entity.status !== "awaiting_acceptance"}
          onClick={() => void accept(false)}
        >
          {t("deny")}
        </button>
      </div>
      <p role="status">{status}</p>
    </section>
  );
}
function History({ entity, t }: { entity: StoredEntity; t: Text }) {
  return (
    <>
      <p className="mono">revision {entity.revision}</p>
      <TaskHistory
        api={api}
        projectId={entity.projectId}
        taskId={entity.id}
        t={t}
      />
    </>
  );
}

function Sessions({
  projectId,
  connection,
  t,
  locale,
  initialSessionId,
}: {
  projectId: string;
  connection: Connection | null;
  t: Text;
  locale: UiPreferences["locale"];
  initialSessionId?:string;
}) {
  const sessions = useEntities(projectId, "session");
  const [selected, setSelected] = useState(initialSessionId??""),
    [notice, setNotice] = useState("");
  const [linked,setLinked]=useState<StoredEntity>();
  // A task's pinned session may be outside the first history page; resolve its ID directly.
  useEffect(()=>{let ignore=false;if(initialSessionId)void api.entity(projectId,initialSessionId).then(entity=>{
    if(entity.kind!=='session'||entity.projectId!==projectId)throw new Error('SESSION_SCOPE_MISMATCH');
    if(!ignore)setLinked(entity);
  }).catch(error=>{if(!ignore)setNotice(String(error));});return()=>{ignore=true;};},[projectId,initialSessionId]);
  const current = sessions.items.find((item) => item.id === selected)??(linked?.id===selected?linked:undefined);
  return (
    <div className="session-layout">
      <aside className="session-list">
        <button
          className="primary"
          onClick={async () => {
            try {
              const id = crypto.randomUUID();
              await api.command(projectId, [
                {
                  expectedRevision: 0,
                  entity: {
                    id,
                    projectId,
                    kind: "session",
                    title: t("discussion"),
                    status: "idle",
                    data: { mode: "discussion" },
                    revision: 0,
                  },
                },
              ]);
              await sessions.load();
              setSelected(id);
            } catch (error) {
              setNotice(`${t("error")}: ${error}`);
            }
          }}
        >
          {uiLabel(locale, "action.newSession")}
        </button>
        <ul className="records">
          {sessions.items.map((session) => (
            <li key={session.id}>
              <button
                aria-current={selected === session.id ? "true" : undefined}
                onClick={() => setSelected(session.id)}
              >
                {session.title ?? session.id}
                <small>{session.status}</small>
              </button>
            </li>
          ))}
        </ul>
        <p role="alert">{sessions.error || notice}</p>
        {sessions.hasMore && (
          <>
            <p role="status">{t("partial")}</p>
            <button
              disabled={sessions.loading}
              onClick={() => void sessions.load(true)}
            >
              {t("more")}
            </button>
          </>
        )}
      </aside>
      {current ? (
        <Session
          key={current.id}
          entity={current}
          connection={connection}
          t={t}
          locale={locale}
        />
      ) : (
        <Empty text={t("empty")} />
      )}
    </div>
  );
}
function Session({
  entity,
  connection,
  t,
  locale,
}: {
  entity: StoredEntity;
  connection: Connection | null;
  t: Text;
  locale: UiPreferences["locale"];
}) {
  const [messages, setMessages] = useState<{
    items: StoredEntity[];
    loading: boolean;
    error: string;
    hasMore: boolean;
  }>({ items: [], loading: true, error: "", hasMore: false });
  const tailMessages = useRef<{
      items: StoredEntity[];
      hasMore: boolean;
      historyOffset: number;
    }>({ items: [], hasMore: false, historyOffset: 0 }),
    olderWindow = useRef<{
      items: StoredEntity[];
      offset: number;
      hasMore: boolean;
    } | null>(null),
    olderRequest = useRef(createLatestRequest());
  const [historyBusy, setHistoryBusy] = useState(false);
  const tasks = useEntities(entity.projectId, "task");
  const [workflowRegistry,setWorkflowRegistry]=useState<WorkflowRegistry>();
  useEffect(()=>{let ignore=false;void api.taskManager(entity.projectId).then(value=>{if(!ignore)setWorkflowRegistry(value.workflows);}).catch(()=>{});return()=>{ignore=true;};},[entity.projectId]);
  const [targetId, setTargetId] = useState(String(entity.data?.taskId ?? "")),
    [linkedTaskId, setLinkedTaskId] = useState(
      String(entity.data?.taskId ?? ""),
    ),
    [actionBusy, setActionBusy] = useState(false);
  const [linkedTarget, setLinkedTarget] = useState<StoredEntity | undefined>();
  const targetMap = new Map(tasks.items.map((task) => [task.id, task]));
  if (
    linkedTarget &&
    (!targetMap.has(linkedTarget.id) ||
      linkedTarget.revision >= targetMap.get(linkedTarget.id)!.revision)
  )
    targetMap.set(linkedTarget.id, linkedTarget);
  const targetChoices = [...targetMap.values()];
  const target = targetChoices.find((task) => task.id === targetId);
  const modeHydrated = useRef(false);
  const autosave = useRef<DraftLease | null>(null),
    draftText = useRef(""),
    scrollTop = useRef(0),
    atBottom = useRef(true),
    transcript = useRef<HTMLDivElement | null>(null);
  const [draftSaving, setDraftSaving] = useState(false);
  const [draftAvailable, setDraftAvailable] = useState(false);
  const mounted = useRef(false);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);
  const [boundMode, setBoundMode] = useState<string | null>(null);
  const [draft, setDraft] = useState(""),
    [mode, setMode] = useState("discussion"),
    [notice, setNotice] = useState(""),
    [snapshot, setSnapshot] = useState<RuntimeState | null>(null),
    [pane, setPane] = useState("chat");
  const runState: RunState =
    draftAvailable &&
    !actionBusy &&
    snapshot?.canSend === true &&
    mode === boundMode &&
    (mode !== "execution" ||
      (targetId === linkedTaskId && isExecutionTarget(target,workflowRegistry)))
      ? "idle"
      : snapshot?.state === "running"
        ? "running"
        : "uncertain";
  useEffect(() => {
    if (["completed", "failed", "interrupted"].includes(snapshot?.state ?? ""))
      void tasks.load();
  }, [snapshot?.runId, snapshot?.state]);
  useEffect(() => {
    let active = true;
    if (!linkedTaskId) {
      setLinkedTarget(undefined);
      return;
    }
    void loadSavedSessionTarget(api, entity.projectId, linkedTaskId)
      .then((task) => {
        if (active) setLinkedTarget(task);
      })
      .catch((error) => {
        if (active) {
          setLinkedTarget(undefined);
          setNotice(String(error));
        }
      });
    return () => {
      active = false;
    };
  }, [entity.projectId, linkedTaskId, snapshot?.runId, snapshot?.state]);
  useLayoutEffect(() => {
    const element = transcript.current;
    if (element) {
      element.scrollTop = atBottom.current
        ? element.scrollHeight
        : scrollTop.current;
    }
  }, [messages.items, snapshot?.visibleDrafts, pane]);
  useEffect(() => {
    let template: StoredEntity | undefined;
    let saver: DraftLease;
    try {
      saver = draftRegistry.acquire([entity.projectId, entity.id], {
        read: async () => {
          const page = await api.entities(entity.projectId, "draft", entity.id);
          template = page.items[0];
          return {
            id: template?.id ?? `draft:${entity.id}`,
            body: template?.body ?? "",
            revision: template?.revision ?? 0,
          };
        },
        write: async (record, body, key) => {
          const next: StoredEntity = {
            ...template,
            id: record.id,
            projectId: entity.projectId,
            parentId: entity.id,
            kind: "draft",
            body,
            revision: record.revision,
          };
          const receipt = (await api.command(
            entity.projectId,
            [{ expectedRevision: record.revision, entity: next }],
            key,
          )) as { revisions?: { id: string; revision: number }[] };
          const revision = receipt.revisions?.find(
            (row) => row.id === record.id,
          )?.revision;
          if (!Number.isSafeInteger(revision) || revision! <= record.revision)
            throw new Error("DRAFT_ACK_UNVERIFIED");
          return { id: record.id, body, revision: revision! };
        },
      });
    } catch (error) {
      setDraftAvailable(false);
      setNotice(
        error instanceof Error && error.message === "DRAFT_SCOPE_CAPACITY"
          ? t("draftScopeUnavailable")
          : String(error),
      );
      return;
    }
    autosave.current = saver;
    setDraftAvailable(true);
    const unsubscribe = saver.subscribe((state) => {
      draftText.current = state.body;
      setDraft(state.body);
      setDraftSaving(state.saving);
      if (state.error) setNotice(state.error);
    });
    return () => {
      unsubscribe();
      saver.release();
      if (autosave.current === saver) autosave.current = null;
    };
  }, [entity.id, entity.projectId]);
  useEffect(() => {
    const dispose = startSessionPolling({
      state: (signal) => api.runtimeState(entity.projectId, entity.id, signal),
      messages: (offset, signal) =>
        api.messages(entity.projectId, entity.id, offset, signal),
      publish: (update) => {
        setSnapshot(update.state);
        setBoundMode(update.state.mode ?? null);
        if (!modeHydrated.current) {
          modeHydrated.current = true;
          if (
            ["discussion", "planning", "execution"].includes(
              update.state.mode ?? "",
            )
          )
            setMode(update.state.mode!);
        }
        tailMessages.current = {
          items: update.messages,
          hasMore: update.hasMore,
          historyOffset: update.historyOffset,
        };
        setMessages({
          items: mergeJournalMessages(
            olderWindow.current?.items ?? [],
            update.messages,
          ),
          hasMore: update.hasMore,
          loading: update.messagesLoading ?? false,
          error: update.messagesError ?? "",
        });
      },
      error: (error) => {
        setMessages((previous) => ({
          ...previous,
          loading: false,
          error: String(error),
        }));
        setSnapshot((previous) =>
          previous ? { ...previous, canSend: false } : null,
        );
      },
    });
    return () => {
      dispose();
      olderRequest.current.dispose();
    };
  }, [entity.id, entity.projectId]);
  async function loadHistory(direction: "older" | "newer") {
    const tail = tailMessages.current,
      current = olderWindow.current;
    const offset =
      direction === "older"
        ? current
          ? current.offset + 50
          : tail.historyOffset
        : current
          ? current.offset - 50
          : 0;
    if (direction === "newer" && offset < tail.historyOffset) {
      olderWindow.current = null;
      setMessages((previous) => ({
        ...previous,
        items: tail.items,
        hasMore: tail.hasMore,
      }));
      atBottom.current = true;
      return;
    }
    setHistoryBusy(true);
    atBottom.current = false;
    scrollTop.current = 0;
    await olderRequest.current.run(
      (signal) => api.messages(entity.projectId, entity.id, offset, signal),
      (page) => {
        olderWindow.current = {
          items: page.items,
          offset,
          hasMore: page.hasMore,
        };
        setMessages((previous) => ({
          ...previous,
          items: mergeJournalMessages(page.items, tailMessages.current.items),
          hasMore: tailMessages.current.hasMore,
        }));
        setHistoryBusy(false);
      },
      (error) => {
        setMessages((previous) => ({ ...previous, error: String(error) }));
        setHistoryBusy(false);
      },
    );
  }
  async function persistDraft(body: string) {
    const saved = await autosave.current?.flush(body);
    if (saved && mounted.current) setNotice(t("saved"));
    return saved;
  }
  async function runtime(
    action: "bindings" | "send" | "interrupt" | "reconcile" | "approve",
    extra: Record<string, unknown> = {},
  ) {
    const binding = {
      bindingId: snapshot?.bindingId,
      runId: snapshot?.runId,
      generation: snapshot?.generation,
    };
    setSnapshot((previous) =>
      previous ? { ...previous, canSend: false } : null,
    );
    setActionBusy(true);
    let acknowledgement =
      action === "interrupt"
        ? uiLabel(locale, "state.stopRequested")
        : t("saved");
    try {
      if (action === "send") {
        const lease = autosave.current;
        if (!lease || typeof extra.input !== "string")
          throw new Error(t("draftScopeUnavailable"));
        const result = await sendWithDraftAck(
          lease,
          extra.input,
          (clientMessageId) =>
            api.runtime(action, {
              projectId: entity.projectId,
              sessionId: entity.id,
              ...binding,
              ...extra,
              clientMessageId,
            }),
        );
        if (!result.acknowledged)
          acknowledgement = uiLabel(locale, "state.checkingSend");
        else if (!result.cleanupSaved)
          acknowledgement += ` · ${t("draftCleanupPending")}`;
      } else {
        await api.runtime(action, {
          projectId: entity.projectId,
          sessionId: entity.id,
          ...binding,
          ...extra,
        });
      }
      if (!mounted.current) return;
      setNotice(acknowledgement);
      if (action === "bindings") setBoundMode(mode);
      // Refresh failure cannot undo the already consumed command ACK or its durable draft cleanup.
      try {
        const current = await api.runtimeState(entity.projectId, entity.id);
        if (mounted.current) setSnapshot(current);
      } catch (error) {
        if (mounted.current)
          setNotice(`${acknowledgement} · ${t("partial")}: ${error}`);
      }
    } catch (error) {
      if (mounted.current) setNotice(`${t("error")}: ${error}`);
    } finally {
      if (mounted.current) setActionBusy(false);
    }
  }
  return (
    <>
      <section className="chat-panel">
        <div className="tabs">
          {(["chat", "context", "changes"] as const).map((tab) => (
            <button
              key={tab}
              aria-pressed={pane === tab}
              onClick={() => setPane(tab)}
            >
              {t(tab)}
            </button>
          ))}
        </div>
        {pane === "chat" ? (
          <>
            {messages.hasMore && (
              <div className="history-paging">
                <p role="status">{t("historyWindowHint")}</p>
                <button
                  type="button"
                  disabled={
                    historyBusy ||
                    !(olderWindow.current?.hasMore ?? messages.hasMore)
                  }
                  onClick={() => void loadHistory("older")}
                >
                  {t("olderMessages")}
                </button>
                {olderWindow.current && (
                  <button
                    type="button"
                    disabled={historyBusy}
                    onClick={() => void loadHistory("newer")}
                  >
                    {t("newerMessages")}
                  </button>
                )}
              </div>
            )}
            {messages.items.some(
              (item) => !Number.isSafeInteger(item.journalOrder),
            ) && (
              <p role="status" className="quiet">
                {t("historyOrderUnknown")}
              </p>
            )}
            <div
              className="transcript"
              role="log"
              aria-live="polite"
              ref={transcript}
              onScroll={(e) => {
                scrollTop.current = e.currentTarget.scrollTop;
                atBottom.current =
                  e.currentTarget.scrollHeight -
                    e.currentTarget.clientHeight -
                    e.currentTarget.scrollTop <
                  40;
              }}
            >
              {messages.items.map((message) => (
                <article key={message.id}>
                  <small>{String(message.data?.role ?? message.kind)}</small>
                  <p>{message.body}</p>
                </article>
              ))}
              {visibleAssistantDrafts(snapshot, messages.items).map(
                (message) => (
                  <article
                    key={`stream:${message.runId}:${message.sourceItemId}`}
                  >
                    <small>{t("streaming")}</small>
                    <p>{message.text}</p>
                  </article>
                ),
              )}
              {!messages.items.length && (
                <Empty text={messages.loading ? t("loading") : t("empty")} />
              )}
            </div>
            <form
              className="composer"
              onSubmit={(e) => {
                e.preventDefault();
                if (!draftSaving && canSend(connection, runState, draft))
                  void runtime("send", {
                    input: draft,
                    ...(linkedTaskId ? { taskId: linkedTaskId } : {}),
                  });
              }}
            >
              <label>
                {t("mode")}
                <select
                  value={mode}
                  disabled={actionBusy || runBlocksScopeChange(snapshot)}
                  onChange={(e) => setMode(e.target.value)}
                >
                  {(["discussion", "planning", "execution"] as const).map(
                    (value) => (
                      <option key={value} value={value} disabled={value === 'execution' && connection?.route === 'codex_app_agent' && !connection.capabilities?.executionConfigured}>
                        {t(value)}
                      </option>
                    ),
                  )}
                </select>
              </label>
              <label>
                {t("executionTarget")}
                <select
                  value={targetId}
                  disabled={actionBusy || runBlocksScopeChange(snapshot)}
                  onChange={(e) => setTargetId(e.target.value)}
                >
                  <option value="">—</option>
                  {targetChoices.map((task) => (
                    <option key={task.id} value={task.id}>
                      {task.publicKey ?? task.id}: {task.title}
                    </option>
                  ))}
                </select>
              </label>
              <button
                type="button"
                disabled={
                  actionBusy ||
                  runBlocksScopeChange(snapshot) ||
                  !target ||
                  targetId === linkedTaskId
                }
                onClick={async () => {
                  if (!target) return;
                  setActionBusy(true);
                  try {
                    const [currentSession, currentTask] = await Promise.all([
                      api.entity(entity.projectId, entity.id),
                      api.entity(entity.projectId, target.id),
                    ]);
                    await api.command(
                      entity.projectId,
                      attachTaskToSession(currentSession, currentTask),
                    );
                    setLinkedTaskId(target.id);
                    await tasks.load();
                  } catch (error) {
                    setNotice(`${t("error")}: ${error}`);
                  } finally {
                    setActionBusy(false);
                  }
                }}
              >
                {t("attachTask")}
              </button>
              {mode === "execution" &&
                (!isExecutionTarget(target,workflowRegistry) || targetId !== linkedTaskId) && (
                  <p className="quiet">{t("executionScopeHint")}</p>
                )}
              {tasks.hasMore && (
                <button
                  type="button"
                  disabled={tasks.loading}
                  onClick={() => void tasks.load(true)}
                >
                  {t("more")}
                </button>
              )}
              {messages.hasMore && <p role="status">{t("partial")}</p>}
              <label>
                {t("draft")}
                <textarea
                  value={draft}
                  disabled={!draftAvailable}
                  onChange={(e) => {
                    autosave.current?.edit(e.target.value);
                  }}
                  rows={4}
                />
              </label>
              <p className="quiet" id="send-hint">
                {t("sendHint")}
              </p>
              <div className="actions">
                <button
                  className="primary"
                  disabled={
                    draftSaving || !canSend(connection, runState, draft)
                  }
                  aria-describedby="send-hint"
                >
                  {uiLabel(locale, "action.send")}
                </button>
                <button
                  type="button"
                  disabled={draftSaving}
                  onClick={() => void persistDraft(draft)}
                >
                  {t("save")}
                </button>
                <button
                  type="button"
                  disabled={
                    !connection?.verified || runBlocksScopeChange(snapshot)
                  }
                  onClick={() => void runtime("bindings", { mode })}
                >
                  {t("connect")}
                </button>
                <button
                  type="button"
                  disabled={actionBusy || !canStopRun(snapshot)}
                  onClick={() => void runtime("interrupt")}
                >
                  {uiLabel(locale, "action.stopRun")}
                </button>
                <button type="button" onClick={() => void runtime("reconcile", snapshot?.recovery?.canCancelUndispatched?{resolution:'cancel_undispatched'}:{})}>
                  {t(snapshot?.recovery?.canCancelUndispatched?'cancelUndispatched':"recover")}
                </button>
              </div>
              <p role="status">{notice || messages.error}</p>
            </form>
          </>
        ) : (
          <>
            {pane === "changes" ? (
              <RuntimeDiff state={snapshot} t={t} />
            ) : (
              <SessionContext
                api={api}
                entity={entity}
                state={snapshot}
                t={t}
                onReference={(reference) => {
                  const next = `${draftText.current}${draftText.current ? "\n" : ""}${reference}`;
                  if (!autosave.current) {
                    setNotice(t("draftScopeUnavailable"));
                    return;
                  }
                  autosave.current?.edit(next);
                }}
              />
            )}
          </>
        )}
      </section>
      <aside className="inspector">
        <RuntimeSummary state={snapshot} t={t} />
        <h2>{t("context")}</h2>
        <p className="mono">{entity.id}</p>
        <p>
          {t("connection")}:{" "}
          {connection?.verified ? t("verified") : t("unverified")}
        </p>
        <h3>{t("approval")}</h3>
        <p className="quiet">
          {t("modelAccess")}: {snapshot?.modelAccess ?? t("unverified")}
        </p>
        <p className="quiet">{snapshot?.reason}</p>
        {snapshot?.pendingApprovals?.length ? (
          snapshot.pendingApprovals.map((request) => (
            <div key={request.requestId}>
              {request.source==='paos_domain'&&<p className="quiet">{t('appDomainApproval')}</p>}
              <p>{request.description ?? request.requestId}</p>
              <span className="badge">{request.state ?? t("unverified")}</span>
              <p className="quiet">
                {request.kind} · {request.details?.reason}
              </p>
              {request.details?.command && (
                <pre className="diff">{request.details.command}</pre>
              )}
              {request.details?.changes != null && (
                <pre className="diff">
                  {JSON.stringify(request.details.changes, null, 2)}
                </pre>
              )}
              {!request.reviewable && <p>{t("approvalDetailsMissing")}</p>}
              <button
                disabled={
                  actionBusy || !canAnswerApproval(snapshot, request, "accept")
                }
                onClick={() =>
                  void runtime("approve", {
                    requestId: request.requestId,
                    decision: "accept",
                  })
                }
              >
                {t("approve")}
              </button>
              <button
                disabled={
                  actionBusy || !canAnswerApproval(snapshot, request, "decline")
                }
                onClick={() =>
                  void runtime("approve", {
                    requestId: request.requestId,
                    decision: "decline",
                  })
                }
              >
                {t("deny")}
              </button>
            </div>
          ))
        ) : (
          <p className="quiet">{t("noApproval")}</p>
        )}
        <RuntimeChecks state={snapshot} t={t} />
        <p className="quiet">
          {t("changes")}: {snapshot?.fileChanges?.length ?? 0}
        </p>
      </aside>
    </>
  );
}
function Checks({ projectId, t }: { projectId: string; t: Text }) {
  const evidence = useEntities(projectId, "evidence");
  return (
    <section className="panel">
      <h2>{t("check")}</h2>
      {evidence.loading && <p role="status">{t("loading")}</p>}
      {evidence.error && <p role="alert">{evidence.error}</p>}
      <ul className="records">
        {evidence.items.map((item) => (
          <li key={item.id}>
            <h3>{item.title}</h3>
            <p>{item.body}</p>
            <span className="badge">
              {item.coverage === "complete" ? item.status : t("partial")}
            </span>
          </li>
        ))}
      </ul>
      {!evidence.loading && !evidence.items.length && (
        <Empty text={t("empty")} />
      )}
      {evidence.hasMore && (
        <button
          disabled={evidence.loading}
          onClick={() => void evidence.load(true)}
        >
          {t("more")}
        </button>
      )}
    </section>
  );
}
function Search({ projectId, t }: { projectId: string; t: Text }) {
  const [items, setItems] = useState<StoredEntity[]>([]),
    [status, setStatus] = useState(""),
    [query, setQuery] = useState(""),
    [executedQuery, setExecutedQuery] = useState(""),
    [hasMore, setHasMore] = useState(false),
    [busy, setBusy] = useState(false);
  const latest = useRef(createLatestRequest());
  useEffect(() => () => latest.current.dispose(), [projectId]);
  async function search(nextQuery: string, append = false) {
    setBusy(true);
    setStatus(t("loading"));
    if (!append) {
      setItems([]);
      setHasMore(false);
      setExecutedQuery(nextQuery);
    }
    await latest.current.run(
      (signal) =>
        api.search(projectId, nextQuery, append ? items.length : 0, signal),
      (page) => {
        setItems((previous) =>
          append ? [...previous, ...page.items] : page.items,
        );
        setHasMore(page.hasMore);
        setStatus(
          page.coverage === "partial"
            ? t("partial")
            : !page.items.length && !append
              ? t("empty")
              : "",
        );
        setBusy(false);
      },
      (error) => {
        setStatus(`${t("error")}: ${error}`);
        setBusy(false);
      },
    );
  }
  return (
    <section className="panel">
      <form
        onSubmit={(e) => {
          e.preventDefault();
          void search(query);
        }}
      >
        <label>
          {t("query")}
          <input
            name="q"
            type="search"
            required
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </label>
        <button disabled={busy}>{t("search")}</button>
      </form>
      <button
        disabled={busy}
        onClick={() => {
          setBusy(true);
          setStatus(t("loading"));
          void latest.current.run(
            (signal) => api.rebuildSearch(projectId, signal),
            (receipt) => {
              setStatus(
                String(receipt.status ?? "") +
                  " · " +
                  String(receipt.coverage ?? t("unverified")),
              );
              setBusy(false);
            },
            (error) => {
              setStatus(String(error));
              setBusy(false);
            },
          );
        }}
      >
        {t("rebuildSearch")}
      </button>
      <p role="status">{status}</p>
      <ul className="records">
        {items.map((item) => (
          <li key={item.id}>
            <strong>{item.title}</strong>
            <p>{item.body}</p>
            <span className="mono">{item.publicKey ?? item.id}</span>
          </li>
        ))}
      </ul>
      {hasMore && (
        <button
          disabled={busy}
          onClick={() => void search(executedQuery, true)}
        >
          {t("more")}
        </button>
      )}
    </section>
  );
}
