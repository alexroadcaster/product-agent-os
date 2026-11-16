import { useEffect, useState } from "react";
import type { M1Api, RuntimeState, StoredEntity } from "../api/client.ts";
import type { AppLabel } from "../locales/app.ts";
import { Sources } from "./Operations.tsx";
type Text = (key: AppLabel) => string;
/** Inventory visibility and execution budgets remain separate user decisions. */
export function FileExecutionPreflight({report,error,locale,onRefresh}:{report?:import('../../../../packages/contracts/runtime/file-preflight.ts').FilePreflight|null;error?:string;locale:'ru'|'en';onRefresh:()=>void}){
 const w=(ru:string,en:string)=>locale==='ru'?ru:en;
 return <section className="panel" data-testid="file-execution-preflight"><h3>{w('Файлы перед выполнением','Files before execution')}</h3><p>{w('Видимость и чтение в Files определяются inventory policy. Выполнение отдельно ограничено32 путями,64KiB на файл и512KiB суммарно; rename занимает два пути. Проверка повторяется сервером перед dispatch.','Files visibility and reading follow inventory policy. Execution separately allows32 paths,64KiB per file and512KiB total; rename uses two paths. The server repeats validation before dispatch.')}</p>
  {error&&<p role="alert">{error}</p>}{report?<><p role="status" data-testid="file-preflight-state" data-allowed={report.allowed}>{report.allowed?w('Scope разрешён текущей проверкой','Scope allowed at this observation'):w('Выполнение заблокировано','Execution blocked')} · {report.counts.paths}/{report.limits.files} · {report.counts.totalBytes}/{report.limits.totalBytes} B {report.counts.bytesComplete?'':w('(известная часть)','(known portion)')}</p><ul>{report.items.filter(item=>!item.allowed).map((item,i)=><li key={i}><code>{item.path}</code> · {item.reason}</li>)}</ul><p>{report.reasons.join(' · ')}</p><details><summary>{w('Версия проверки','Check provenance')}</summary><p>{report.observedAt}</p><code>{report.policyVersion}</code><p className="mono">{report.digest}</p></details></>:<p role="status">{w('Проверка ещё не получена; dispatch всё равно повторит её.','No preflight observation yet; dispatch still repeats it.')}</p>}<button type="button" data-testid="file-preflight-refresh" onClick={onRefresh}>{w('Обновить проверку файлов','Refresh file preflight')}</button></section>;
}
export function RuntimeSummary({
  state,
  t,
}: {
  state: RuntimeState | null;
  t: Text;
}) {
  return (
    <section>
      <h3>{t("runStatus")}</h3>
      <p className="mono">{state?.state ?? t("unverified")}</p>
      <p className="quiet">{state?.reason}</p>
      <h3>{t("pinnedProfile")}</h3>
      <dl className="task-metadata">
        {(["id", "version", "role", "assignment"] as const).map((key) => (
          <div key={key}>
            <dt>{key}</dt>
            <dd className="mono">{state?.profile?.[key] ?? t("unverified")}</dd>
          </div>
        ))}
      </dl>
      <span className="badge">{state?.profile?.coverage ?? "unavailable"}</span>
      {state?.streaming?.phaseStatus === "phase_unavailable" && (
        <p className="quiet">{t("streamUnavailable")}</p>
      )}
    </section>
  );
}
export function RuntimeDiff({
  state,
  t,
}: {
  state: RuntimeState | null;
  t: Text;
}) {
  return (
    <section>
      <h3>{t("changes")}</h3>
      {state?.fileChanges?.length ? (
        <ul>
          {state.fileChanges.map((file, index) => (
            <li
              key={`${file.kind}:${file.path}:${index}`}
              className="source-row"
            >
              <strong>
                {t(
                  file.kind === "actual"
                    ? "actualChanges"
                    : file.kind === "proposed"
                      ? "proposedChanges"
                      : "externalChanges",
                )}
              </strong>
              <p className="mono">
                {file.previousPath ? `${file.previousPath} → ` : ""}
                {file.path} · {file.operation}
              </p>
              <span className="badge">{file.coverage}</span>
              <p className="quiet">{file.reason}</p>
              {file.diff && file.kind !== "external" && (
                <pre className="diff">{file.diff}</pre>
              )}
            </li>
          ))}
        </ul>
      ) : (
        <p className="quiet">{t("noDiff")}</p>
      )}
    </section>
  );
}
export function RuntimeChecks({
  state,
  t,
}: {
  state: RuntimeState | null;
  t: Text;
}) {
  return (
    <section>
      <h3>{t("check")}</h3>
      <p className="quiet">{t("runtimeChecksHint")}</p>
      {state?.checks?.length ? (
        <ul>
          {state.checks.map((item) => (
            <li key={item.id}>
              <p className="mono">
                {item.itemType} · {item.status}
                {item.outcome ? ` · ${item.outcome}` : ""}
              </p>
              <small className="mono">
                {item.taskId ?? "—"} · {item.runId}
              </small>
              <span className="badge">{item.coverage}</span>
              {item.reason && <p>{item.reason}</p>}
            </li>
          ))}
        </ul>
      ) : (
        <p className="quiet">{t("empty")}</p>
      )}
    </section>
  );
}
export function SessionContext({
  api,
  entity,
  state,
  t,
  onReference,
  view = 'context',
}: {
  api: M1Api;
  entity: StoredEntity;
  state: RuntimeState | null;
  t: Text;
  onReference?: (reference: string) => void;
  view?: 'context' | 'question';
}) {
  const [decisions, setDecisions] = useState<StoredEntity[]>([]),
    [busy, setBusy] = useState(false),
    [error, setError] = useState("");
  async function load() {
    try {
      const page = await api.entities(entity.projectId, "comment", entity.id);
      setDecisions(
        page.items.filter((item) => item.data?.category === "product_decision"),
      );
    } catch (cause) {
      setError(String(cause));
    }
  }
  useEffect(() => {
    void load();
  }, [entity.id, entity.projectId]);
  return (
    <div className="session-context-view">
      <div hidden={view !== 'context'}>
      <RuntimeSummary state={state} t={t} />
      <p className="quiet">{t("referenceHint")}</p>
      <Sources
        api={api}
        projectId={entity.projectId}
        t={t}
        onReference={onReference}
      />
      </div>
      <section hidden={view !== 'question'}>
      <h3>{t("runtimeQuestion")}</h3>
      <p className="quiet">
        {t("questionUnsupported")}{" "}
        <span className="mono">
          {state?.questions?.reason ?? "request_user_input_unsupported"}
        </span>
      </p>
      <h3>{t("productDecision")}</h3>
      <p className="quiet">{t("decisionHint")}</p>
      <ul className="comments">
        {decisions.map((item) => (
          <li key={item.id}>{item.body}</li>
        ))}
      </ul>
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          const form = e.currentTarget,
            body = String(new FormData(form).get("decision"));
          setBusy(true);
          setError("");
          try {
            await api.command(entity.projectId, [
              {
                expectedRevision: 0,
                entity: {
                  id: crypto.randomUUID(),
                  projectId: entity.projectId,
                  parentId: entity.id,
                  kind: "comment",
                  title: "Product decision",
                  body,
                  data: { category: "product_decision" },
                  revision: 0,
                },
              },
            ]);
            form.reset();
            await load();
          } catch (cause) {
            setError(String(cause));
          } finally {
            setBusy(false);
          }
        }}
      >
        <label>
          {t("productDecision")}
          <textarea name="decision" required rows={3} />
        </label>
        <button disabled={busy}>{t("save")}</button>
        <p role="alert">{error}</p>
      </form>
      </section>
    </div>
  );
}
