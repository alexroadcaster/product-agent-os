import {CapabilityNotice} from './CapabilityNotice.tsx';
import {runtimeConnectionState} from './capability.ts';
import { useRef,useState } from "react";
import {HttpApiError,type Connection,type M1Api,type ConnectionRoute} from '../api/client.ts';
import type { AppLabel } from "../locales/app.ts";
import {
  initialConnectionRoute,
  hasActiveConnection,
  connectionRequest,
  appHostTransportLabel,
} from "./connection-controls-model.ts";
/** Secret input lives only in the native control and is cleared after each submission. */
export function ConnectionControls({
  api,
  locale,
  connection,
  onConnection,
  t,
}: {
  api: M1Api;
  locale: "ru" | "en";
  connection: Connection | null;
  onConnection: (connection: Connection) => void;
  t: (key: AppLabel) => string;
}) {
  const w=(ru:string,en:string)=>locale==='ru'?ru:en;
  const connectionState=runtimeConnectionState(connection);
  const [busy, setBusy] = useState(false),
    [error, setError] = useState("");
  const [handoff,setHandoff]=useState(false);
  const pendingHandoff=useRef<string|undefined>(undefined);
  const [chosenRoute, setChosenRoute] = useState<ConnectionRoute>(() =>
    initialConnectionRoute(connection),
  );
  const active = hasActiveConnection(connection),
    route = active ? initialConnectionRoute(connection) : chosenRoute,
    isApp = route === "codex_app_agent";
  const appAttached =
    connection?.route === "codex_app_agent" &&
    connection.state === "connected" &&
    connection.verified;
  const waiting =
    connection?.route === "codex_app_agent" &&
    connection.state === "waiting_for_worker";
  const hostLabel=appHostTransportLabel(connection);
  return (
    <section className="panel">
      <h2>{t("connection")}</h2>
      <label>
        {t("connectionRoute")}
        <select
          aria-label={t("connectionRoute")}
          value={route}
          disabled={busy || active}
          onChange={(e) => {
            setChosenRoute(e.target.value as ConnectionRoute);
            setError("");
          }}
        >
          <option value="codex_app_agent">{t("appAgentRoute")}</option>
          <option value="local_api_byok">{t("byokRoute")}</option>
        </select>
      </label>
      <p role="status">
        {isApp
          ? appAttached
            ? t("appWorkerConnected")
            : waiting
              ? t("appWorkerWaiting")
              : t("unverified")
          : connection?.verified
            ? t("verified")
            : t("unverified")}{" "}
        {!isApp&&<> · {t("modelAccess")}: {t("unverified")}</>}
      </p>
      {isApp&&<CapabilityNotice testId="capability-runtime" locale={locale} state={connectionState}
        scope={w('Подключение канала PAOS; готовность выполнения проверяется для выбранной сессии','PAOS channel connection; execution readiness is checked for the selected session')}
        reason={connectionState==='connected'?w('Worker подключён. Это не свидетельство квалификации broker, model access или sandbox собственных tools Codex App.','The worker is attached. This does not attest broker qualification, model access or a sandbox for Codex App host tools.'):w('Канал Codex App worker не подключён. Endpoint и открытое окно не подтверждают attached worker.','The Codex App worker channel is not connected. An endpoint or an open window does not attest an attached worker.')}
        next={connectionState==='connected'?w('Выберите задачу и execution-сессию: её preflight и runtime snapshot показывают scope broker. Используйте действующий approval без нового запроса.','Select a task and execution session: its preflight and runtime snapshot show broker scope. Use existing approval without a new request.'):isApp?t(handoff?'appHandoffOpened':waiting?'appWaitingInstruction':'appConnectInstruction'):t('credentialHint')}/>}
      {isApp ? (
        <>
          {!appAttached&&<p className="notice" role="status" data-testid="app-connection-next-step">{t(handoff?'appHandoffOpened':waiting?'appWaitingInstruction':'appConnectInstruction')}</p>}
        </>
      ) : (
        <p className="quiet">{t("credentialHint")}</p>
      )}
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          const form = e.currentTarget,
            secret = form.elements.namedItem(
              "apiKey",
            ) as HTMLInputElement | null;
          setBusy(true);
          setError("");
          try {
            if(isApp){
              pendingHandoff.current??=crypto.randomUUID();
              const result=await api.openAppAgent(pendingHandoff.current);pendingHandoff.current=undefined;
              setHandoff(result.opened);onConnection(await api.connection());return;
            }
            const data = isApp ? undefined : new FormData(form);
            const input = connectionRequest(
              route,
              data
                ? {
                    connectionId: data.get("connectionId"),
                    apiKey: data.get("apiKey"),
                    remember: data.get("remember") === "on",
                  }
                : {},
            );
            onConnection(await api.connect(input));
          } catch (cause) {
            if(isApp&&cause instanceof HttpApiError){
              pendingHandoff.current=undefined;
              setError(t(cause.code==='ROUTE_NOT_FOUND'||cause.code==='APP_HANDOFF_UNAVAILABLE'?'desktopUnavailable':'appOpenFailed'));
            }else setError(String(cause));
          } finally {
            if (secret) secret.value = "";
            setBusy(false);
          }
        }}
      >
        {!isApp && (
          <>
            <label>
              {t("connectionAlias")}
              <input
                name="connectionId"
                required
                autoComplete="off"
                disabled={busy || active}
              />
            </label>
            <label>
              API key
              <input
                name="apiKey"
                type="password"
                required
                autoComplete="off"
                spellCheck={false}
                disabled={busy || active}
              />
            </label>
            <label className="checkbox">
              <input
                name="remember"
                type="checkbox"
                disabled={busy || active}
              />
              {t("rememberCredential")}
            </label>
          </>
        )}
        <button disabled={busy || (isApp?appAttached:active)}>
          {t(isApp ? appAttached?'appWorkerConnected':waiting?'appReopen':'appConnect' : "login")}
        </button>
        <button
          type="button"
          disabled={busy || !active}
          onClick={async () => {
            setBusy(true);
            setError("");
            try {
              onConnection(await api.disconnect());
              setHandoff(false);pendingHandoff.current=undefined;
            } catch (cause) {
              setError(String(cause));
            } finally {
              setBusy(false);
            }
          }}
        >
          {t(isApp?'appDisconnect':"disconnect")}
        </button>
        <p role="alert">{error}</p>
      </form>
      {isApp&&<ol className="connection-steps"><li>{t('appConnect')}</li><li>{t('appAgentBoundary')}</li><li>{t('appWorkerConnected')}</li></ol>}{isApp&&<details><summary>{t('appConnectionDetails')}</summary>
        {hostLabel&&<p className="quiet">{t(hostLabel)}</p>}
        <p className="quiet">{t(connection?.capabilities?.executionConfigured?'appBrokerBoundary':'appAgentBoundary')}</p>
        <p className="quiet">{t('appAgentNoFallback')}</p><p>{t('modelAccess')}: {t('unverified')}</p>
        {connection?.reason&&<p className="quiet">{connection.reason}</p>}
      </details>}
    </section>
  );
}
