import { useEffect, useState } from "react";
import type {
  M1Api,
  ImportPreview,
  SourceCoverage,
  HistoryEvent,
} from "../api/client.ts";
import type { AppLabel } from "../locales/app.ts";
import { eventReferencesEntity } from "../api/policy.ts";
import { createLatestRequest } from "../api/latest-request.ts";
import { useRef } from "react";
import {
  prepareImportSources,
  canCommitImport,
} from "../api/import-sources.ts";
type Props = { api: M1Api; projectId: string; t: (key: AppLabel) => string };
export function Catalog({
  api,
  projectId,
  t,
  kind,
}: { kind: "agents" | "skills" | "graph" } & Props) {
  const [catalog, setCatalog] = useState<Awaited<
      ReturnType<M1Api["catalogs"]>
    > | null>(null),
    [error, setError] = useState("");
  useEffect(() => {
    let active = true;
    api
      .catalogs(projectId)
      .then((result) => {
        if (active) setCatalog(result);
      })
      .catch((cause) => {
        if (active) setError(String(cause));
      });
    return () => {
      active = false;
    };
  }, [api, projectId]);
  return (
    <section className="panel">
      {catalog?.coverage === "partial" && <p role="status">{t("partial")}</p>}
      {error ? (
        <p role="alert">{error}</p>
      ) : !catalog ? (
        <p role="status">{t("loading")}</p>
      ) : kind === "graph" ? (
        <>
          <p>{t("unavailable")}</p>
          <p className="mono">{catalog.graph.reason}</p>
        </>
      ) : (
        <ul className="records">
          {catalog[kind].map((item) => (
            <li key={item.id} className="source-row">
              <strong>{item.label}</strong>
              <p>{item.description}</p>
              <span className="badge">{item.coverage}</span>
            </li>
          ))}
          {!catalog[kind].length && <li>{t("empty")}</li>}
        </ul>
      )}
    </section>
  );
}

export function Sources({
  api,
  projectId,
  t,
  onReference,
}: Props & { onReference?: (reference: string) => void }) {
  const [source, setSource] = useState<SourceCoverage | null>(null),
    [error, setError] = useState("");
  const [content, setContent] = useState<Awaited<
      ReturnType<M1Api["sourceContent"]>
    > | null>(null),
    [reading, setReading] = useState(false);
  const latest = useRef(createLatestRequest());
  useEffect(() => {
    let active = true;
    setSource(null);
    setContent(null);
    setError("");
    api
      .sources(projectId)
      .then((value) => {
        if (active) setSource(value);
      })
      .catch((cause) => {
        if (active) setError(String(cause));
      });
    return () => {
      active = false;
      latest.current.dispose();
    };
  }, [api, projectId]);
  return (
    <section className="panel">
      <h2>{t("source")}</h2>
      {error ? (
        <p role="alert">{error}</p>
      ) : !source ? (
        <p role="status">{t("loading")}</p>
      ) : (
        <ul className="records">
          {source.sources.map((item) => (
            <li key={item.id} className="source-row">
              <strong>{item.relativePath ?? item.id}</strong>
              <span className="badge">{item.status}</span>
              {item.reason && <p className="quiet">{item.reason}</p>}
              {item.relativePath && (
                <button
                  disabled={reading || item.status !== "available"}
                  onClick={() => {
                    setReading(true);
                    setError("");
                    void latest.current.run(
                      (signal) => api.sourceContent(projectId, item.id, signal),
                      (value) => {
                        setContent(value);
                        setReading(false);
                      },
                      (cause) => {
                        setError(String(cause));
                        setReading(false);
                      },
                    );
                  }}
                >
                  {t("readSource")}
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
      {content && (
        <section>
          <h3>{content.relativePath}</h3>
          <p className="mono">SHA-256 {content.sha256}</p>
          <span className="badge">{content.coverage}</span>
          {content.redacted && <p className="quiet">{t("redactedSource")}</p>}
          <pre className="diff">{content.content}</pre>
          {onReference && (
            <button
              onClick={() =>
                onReference(
                  `[source path=${JSON.stringify(content.relativePath)} sha256=${content.sha256} coverage=${content.coverage}]`,
                )
              }
            >
              {t("addReference")}
            </button>
          )}
        </section>
      )}
    </section>
  );
}
export function ImportTasks({ api, projectId, t }: Props) {
  const [preview, setPreview] = useState<ImportPreview | null>(null),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  const [sourceFile, setSourceFile] = useState<File | null>(null),
    [confirmed, setConfirmed] = useState(false),
    [commitKey, setCommitKey] = useState(""),
    [committed, setCommitted] = useState<{
      mappingCount: number;
      backupId: string;
    } | null>(null),
    [exported, setExported] = useState<unknown>(null);
  const [sourcePath, setSourcePath] = useState(""),
    [projectionFile, setProjectionFile] = useState<File | null>(null),
    [projectionPath, setProjectionPath] = useState(""),
    [sourceStatus, setSourceStatus] = useState<Awaited<
      ReturnType<M1Api["sourceStatus"]>
    > | null>(null);
  return (
    <section className="panel">
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          const file = new FormData(e.currentTarget).get("file");
          if (!(file instanceof File)) return;
          setBusy(true);
          setError("");
          setPreview(null);
          setConfirmed(false);
          setCommitted(null);
          setSourceFile(null);
          try {
            const files = await prepareImportSources(
              file,
              sourcePath,
              projectionFile,
              projectionPath,
            );
            setPreview(
              files.length === 2
                ? await api.previewImportBundle(projectId, files)
                : await api.previewImport(
                    projectId,
                    file.name,
                    files[0].content,
                    sourcePath,
                  ),
            );
            setSourceFile(file);
            setCommitKey(crypto.randomUUID());
          } catch (cause) {
            setError(String(cause));
          } finally {
            setBusy(false);
          }
        }}
      >
        <label>
          {t("sourceFile")}
          <input
            type="file"
            name="file"
            accept=".json,.md"
            required
            disabled={busy}
            onChange={(event) => {
              setSourcePath(event.target.files?.[0]?.name ?? "");
              setPreview(null);
              setSourceFile(null);
              setConfirmed(false);
              setCommitted(null);
            }}
          />
        </label>
        <label>
          {t("sourcePath")}
          <input
            required
            value={sourcePath}
            disabled={busy}
            onChange={(e) => {
              setSourcePath(e.target.value);
              setPreview(null);
              setConfirmed(false);
            }}
          />
        </label>
        <label>
          {t("projectionFile")}
          <input
            type="file"
            accept=".md"
            disabled={busy}
            onChange={(e) => {
              const file = e.target.files?.[0] ?? null;
              setProjectionFile(file);
              setProjectionPath(file?.name ?? "");
              setPreview(null);
              setConfirmed(false);
            }}
          />
        </label>
        {projectionFile && (
          <label>
            {t("sourcePath")}
            <input
              required
              value={projectionPath}
              disabled={busy}
              onChange={(e) => {
                setProjectionPath(e.target.value);
                setPreview(null);
                setConfirmed(false);
              }}
            />
          </label>
        )}
        <p className="quiet">{t("sourceBindingHint")}</p>
        <button disabled={busy}>{busy ? t("loading") : t("preview")}</button>
      </form>
      <p role="alert">{error}</p>
      {error.includes("WRITER_INVENTORY_INCOMPLETE") && (
        <p role="status">{t("writerInventory")}</p>
      )}
      {preview && (
        <div className="import-preview">
          <p className="mono">
            {preview.sourceName}
            <br />
            {preview.parserVersion}
            <br />
            {preview.sourceDigest}
          </p>
          <h3>
            {t("candidates")}: {preview.items.length}
          </h3>
          <ul className="records">
            {preview.items.map((item) => (
              <li key={item.sourceId}>
                <strong>
                  {item.sourceId}: {String(item.task.title)}
                </strong>
                <p>{String(item.task.status)}</p>
              </li>
            ))}
          </ul>
          <h3>
            {t("blocked")}: {preview.blocked.length}
          </h3>
          <ul>
            {preview.blocked.map((item) => (
              <li key={item.sourceId}>
                {item.sourceId}: {item.reasons.join(", ")}
              </li>
            ))}
          </ul>
          <p className="quiet">{t("importSafety")}</p>
          <label className="checkbox">
            <input
              type="checkbox"
              checked={confirmed}
              disabled={
                busy ||
                Boolean(committed) ||
                preview.mode === "normalized_proposal"
              }
              onChange={(e) => setConfirmed(e.target.checked)}
            />
            {t("confirmScope")}
          </label>
          <button
            disabled={
              busy ||
              !confirmed ||
              !sourceFile ||
              preview.blocked.length > 0 ||
              Boolean(committed) ||
              !canCommitImport(preview)
            }
            onClick={async () => {
              if (!sourceFile) return;
              setBusy(true);
              setError("");
              try {
                const files = await prepareImportSources(
                  sourceFile,
                  sourcePath,
                  projectionFile,
                  projectionPath,
                );
                const receipt = await api.commitImport(projectId, {
                  stageId: preview.stageId,
                  ...(files.length === 2
                    ? { currentSources: files }
                    : { currentSource: files[0].content }),
                  sourceDigest: preview.sourceDigest,
                  idempotencyKey: commitKey,
                });
                setCommitted(receipt);
                await api.projects();
                setSourceStatus(await api.sourceStatus(projectId));
              } catch (cause) {
                setError(String(cause));
              } finally {
                setBusy(false);
              }
            }}
          >
            {busy ? t("loading") : t("confirmImport")}
          </button>
          {preview.mode === "normalized_proposal" && (
            <>
              <p role="status">{t("proposalHint")}</p>
              <pre className="diff">
                {JSON.stringify(preview.proposal, null, 2)}
              </pre>
            </>
          )}
          {committed && (
            <p role="status">
              {t("saved")} · {t("candidates")}: {committed.mappingCount} ·{" "}
              {t("backupId")}:{" "}
              <span className="mono">{committed.backupId??t('unavailable')}</span>
            </p>
          )}
        </div>
      )}
      <section>
        <h3>{t("sourceStatus")}</h3>
        <button
          disabled={busy}
          onClick={async () => {
            setBusy(true);
            try {
              setSourceStatus(await api.sourceStatus(projectId));
            } catch (cause) {
              setError(String(cause));
            } finally {
              setBusy(false);
            }
          }}
        >
          {t("reload")}
        </button>
        {sourceStatus && (
          <>
            <p className="mono">{sourceStatus.authorityMode}</p>
            <ul className="records">
              {sourceStatus.items.map((item) => (
                <li key={item.sourceRelativePath} className="source-row">
                  <strong>{item.sourceRelativePath}</strong>
                  <span className="badge">{item.status}</span>
                  <p className="mono">
                    {item.sourceDigest}
                    {item.observedDigest ? ` → ${item.observedDigest}` : ""}
                  </p>
                </li>
              ))}
            </ul>
          </>
        )}
      </section>
      <section className="reverse-export">
        <h3>{t("reverseExport")}</h3>
        <button
          disabled={busy}
          onClick={async () => {
            setBusy(true);
            setError("");
            try {
              setExported(await api.exportTasks(projectId));
            } catch (cause) {
              setError(String(cause));
            } finally {
              setBusy(false);
            }
          }}
        >
          {t("reverseExport")}
        </button>
        {exported !== null && (
          <>
            <pre className="diff">{JSON.stringify(exported, null, 2)}</pre>
            <button
              onClick={() => {
                const url = URL.createObjectURL(
                  new Blob([JSON.stringify(exported, null, 2)], {
                    type: "application/json",
                  }),
                );
                const link = document.createElement("a");
                link.href = url;
                link.download = "paos-tasks-export.json";
                link.click();
                setTimeout(() => URL.revokeObjectURL(url), 1000);
              }}
            >
              {t("downloadExport")}
            </button>
          </>
        )}
      </section>
    </section>
  );
}
export function Backup({ api, projectId, t }: Props) {
  const [receipt, setReceipt] = useState<{
      backupId: string;
      manifest: unknown;
      rotatedBackupIds?: string[];
      rotationCandidateIds?: string[];
      retention?: "complete" | "pending";
    } | null>(null),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  const [rotationConfirmed, setRotationConfirmed] = useState(false);
  const [backupId, setBackupId] = useState(""),
    [restoreConfirmed, setRestoreConfirmed] = useState(false),
    [restored, setRestored] = useState<{
      restoreId: string;
      requiresRestart: boolean;
      activeProfileChanged: boolean;
    } | null>(null);
  return (
    <section className="panel">
      <h2>{t("backup")}</h2>
      <button
        className="primary"
        disabled={busy}
        onClick={async () => {
          setBusy(true);
          setError("");
          try {
            const created = await api.backup(projectId);
            setReceipt(created);
            setRotationConfirmed(false);
            setBackupId(created.backupId);
            setRestored(null);
            setRestoreConfirmed(false);
          } catch (cause) {
            setError(String(cause));
          } finally {
            setBusy(false);
          }
        }}
      >
        {busy ? t("loading") : t("createBackup")}
      </button>
      <p role="alert">{error}</p>
      {receipt && (
        <>
          <p role="status">
            {t("backupCreated")}:{" "}
            <span className="mono">{receipt.backupId}</span>
          </p>
          <pre className="diff">
            {JSON.stringify(receipt.manifest, null, 2)}
          </pre>
          <p>
            {t("backupRetention")}:{" "}
            <span className="badge">
              {receipt.retention ?? t("unverified")}
            </span>
          </p>
          {receipt.retention === "pending" && (
            <section>
              <p role="status">{t("rotationPending")}</p>
              <ul className="mono">
                {receipt.rotationCandidateIds?.map((id) => (
                  <li key={id}>{id}</li>
                ))}
              </ul>
              <label className="checkbox">
                <input
                  type="checkbox"
                  checked={rotationConfirmed}
                  disabled={busy}
                  onChange={(e) => setRotationConfirmed(e.target.checked)}
                />
                {t("confirmRotation")}
              </label>
              <button
                disabled={
                  busy ||
                  !rotationConfirmed ||
                  !receipt.rotationCandidateIds?.length
                }
                onClick={async () => {
                  setBusy(true);
                  setError("");
                  try {
                    const result = await api.rotateBackups(
                      projectId,
                      receipt.rotationCandidateIds!,
                    );
                    setReceipt((previous) =>
                      previous
                        ? { ...previous, ...result, rotationCandidateIds: [] }
                        : null,
                    );
                    setRotationConfirmed(false);
                  } catch (cause) {
                    setError(String(cause));
                  } finally {
                    setBusy(false);
                  }
                }}
              >
                {t("applyRotation")}
              </button>
            </section>
          )}
          {receipt.rotatedBackupIds && (
            <p>
              {t("rotatedBackups")}:{" "}
              <span className="mono">
                {receipt.rotatedBackupIds.length
                  ? receipt.rotatedBackupIds.join(", ")
                  : "—"}
              </span>
            </p>
          )}
        </>
      )}
      <section className="restore">
        <h3>{t("restore")}</h3>
        <p className="quiet">{t("restoreHint")}</p>
        <form
          onSubmit={async (e) => {
            e.preventDefault();
            if (!restoreConfirmed) return;
            setBusy(true);
            setError("");
            try {
              const result = await api.restore(projectId, backupId);
              if (
                result.requiresRestart !== true ||
                result.activeProfileChanged !== false
              )
                throw new Error("RESTORE_RESPONSE_UNVERIFIED");
              setRestored(result);
            } catch (cause) {
              setError(String(cause));
            } finally {
              setBusy(false);
            }
          }}
        >
          <label>
            {t("backupId")}
            <input
              required
              pattern="[a-zA-Z0-9_-]{1,100}"
              value={backupId}
              onChange={(e) => {
                setBackupId(e.target.value);
                setRestored(null);
                setRestoreConfirmed(false);
              }}
            />
          </label>
          <label className="checkbox">
            <input
              type="checkbox"
              checked={restoreConfirmed}
              onChange={(e) => setRestoreConfirmed(e.target.checked)}
            />
            {t("confirmRestore")}
          </label>
          <button disabled={busy || !restoreConfirmed || Boolean(restored)}>
            {busy ? t("loading") : t("restore")}
          </button>
        </form>
        {restored && (
          <p role="status">
            {t("restartPending")}{" "}
            <span className="mono">{restored.restoreId}</span>
          </p>
        )}
      </section>
    </section>
  );
}
/** History is read from the service event stream; manual checks and acceptance keep their recorded identity. */
export function TaskHistory({
  api,
  projectId,
  t,
  taskId,
}: { taskId: string } & Props) {
  const [items, setItems] = useState<HistoryEvent[]>([]),
    [cursor, setCursor] = useState<string>(),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  async function load(append = false) {
    setBusy(true);
    try {
      const page = await api.history(projectId, append ? cursor : undefined);
      setItems((previous) =>
        append ? [...previous, ...page.items] : page.items,
      );
      setCursor(page.nextCursor);
    } catch (cause) {
      setError(String(cause));
    } finally {
      setBusy(false);
    }
  }
  useEffect(() => {
    void load();
  }, [projectId, taskId]);
  const scoped = items.filter(
    (item) =>
      item.entityId === taskId || eventReferencesEntity(item.payload, taskId),
  );
  return (
    <div>
      <p role="alert">{error}</p>
      <ul className="records">
        {scoped.map((item) => {
          const changes=Array.isArray(item.payload?.taskChanges)?item.payload.taskChanges.filter((change:any)=>change&&change.id===taskId):[];
          const display=(value:unknown)=>value===null||value===undefined?t('historyNotRecorded'):typeof value==='string'?value:JSON.stringify(value);
          return (
          <li key={item.seq}>
            <p className="mono">
              {item.seq} · {item.type ?? item.kind ?? "event"}
            </p>
            <dl className="task-metadata">
              <dt>{t('historyActor')}</dt><dd>{item.actorId??t('historyNotRecorded')}</dd>
              <dt>{t('historyTime')}</dt><dd><time dateTime={item.occurredAt}>{item.occurredAt&&Number.isFinite(Date.parse(item.occurredAt))?new Date(item.occurredAt).toLocaleString():t('historyNotRecorded')}</time></dd>
              <dt>{t('historyRevision')}</dt><dd className="mono">{item.seq} · {display(item.payload?.commandId)}</dd>
            </dl>
            {changes.length?changes.map((change:any,index:number)=><section key={index} className="task-history-change">
              <p>{t('historyRevision')}: {display(change.previousRevision)} → {display(change.currentRevision)} · {change.operation}</p>
              <p>{t('historySource')}: {display(change.source)}</p><p>{t('historyReason')}: {display(change.reason)}</p>
              {change.coverage==='partial'&&<p>{t('partial')}</p>}
              {Array.isArray(change.fields)&&change.fields.map((field:any,fieldIndex:number)=><section key={fieldIndex} className="task-history-field">
                <h4>{t('historyField')}: {String(field.field)}</h4>
                <dl><dt>{t('historyBefore')}</dt><dd><pre className="diff">{display(field.previous)}</pre></dd><dt>{t('historyAfter')}</dt><dd><pre className="diff">{display(field.current)}</pre></dd></dl>
                {field.redacted&&<span className="badge">{t('redactedSource')}</span>}{field.coverage==='partial'&&<span className="badge">{t('partial')}</span>}
              </section>)}
            </section>):Array.isArray(item.payload?.commentChanges)&&item.payload.commentChanges.some((change:any)=>change?.contentExcluded===true)?<p className="quiet">{t('redactedSource')}</p>:<p className="quiet">{t('historyBefore')} / {t('historyAfter')}: {t('historyNotRecorded')}</p>}
            <details><summary>{t('historyRevision')}</summary><pre className="diff">{JSON.stringify(item.payload??item,null,2)}</pre></details>
          </li>
        );})}
      </ul>
      {!scoped.length && !busy && <p className="quiet">{t("empty")}</p>}
      <button disabled={busy} onClick={() => void load(true)}>
        {busy ? t("loading") : t("more")}
      </button>
    </div>
  );
}
