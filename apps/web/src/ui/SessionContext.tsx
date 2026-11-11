import { useEffect, useState } from "react";
import type { M1Api, RuntimeState, StoredEntity } from "../api/client.ts";
import type { AppLabel } from "../locales/app.ts";
import { Sources } from "./Operations.tsx";
type Text = (key: AppLabel) => string;
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
}: {
  api: M1Api;
  entity: StoredEntity;
  state: RuntimeState | null;
  t: Text;
  onReference?: (reference: string) => void;
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
    <div>
      <RuntimeSummary state={state} t={t} />
      <p className="quiet">{t("referenceHint")}</p>
      <Sources
        api={api}
        projectId={entity.projectId}
        t={t}
        onReference={onReference}
      />
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
      <RuntimeChecks state={state} t={t} />
    </div>
  );
}
