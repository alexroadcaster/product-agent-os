import { useState } from "react";
import type { Connection, M1Api, ConnectionRoute } from "../api/client.ts";
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
  connection,
  onConnection,
  t,
}: {
  api: M1Api;
  connection: Connection | null;
  onConnection: (connection: Connection) => void;
  t: (key: AppLabel) => string;
}) {
  const [busy, setBusy] = useState(false),
    [error, setError] = useState("");
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
      {hostLabel && <p className="quiet">{t(hostLabel)}</p>}
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
        · {t("modelAccess")}: {t("unverified")}
      </p>
      {isApp ? (
        <>
          <p className="quiet">{t("appAgentHint")}</p>
          <p className="quiet">{t(connection?.capabilities?.executionConfigured?'appBrokerBoundary':"appAgentBoundary")}</p>
          <p className="quiet">{t("appAgentNoFallback")}</p>
        </>
      ) : (
        <p className="quiet">{t("credentialHint")}</p>
      )}
      {connection?.reason && <p className="quiet">{connection.reason}</p>}
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
            setError(String(cause));
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
        <button disabled={busy || active}>
          {t(isApp ? "openAppAgentChannel" : "login")}
        </button>
        <button
          type="button"
          disabled={busy || !active}
          onClick={async () => {
            setBusy(true);
            setError("");
            try {
              onConnection(await api.disconnect());
            } catch (cause) {
              setError(String(cause));
            } finally {
              setBusy(false);
            }
          }}
        >
          {t("disconnect")}
        </button>
        <p role="alert">{error}</p>
      </form>
    </section>
  );
}
