import { useState } from "react";
import type { Connection, M1Api } from "../api/client.ts";
import type { AppLabel } from "../locales/app.ts";
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
  return (
    <section className="panel">
      <h2>{t("connection")}</h2>
      <p>
        {connection?.verified ? t("verified") : t("unverified")} ·{" "}
        {t("modelAccess")}: {t("unverified")}
      </p>
      <p className="quiet">{t("credentialHint")}</p>
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          const form = e.currentTarget,
            data = new FormData(form),
            secret = form.elements.namedItem("apiKey") as HTMLInputElement;
          setBusy(true);
          setError("");
          try {
            onConnection(
              await api.connect({
                connectionId: String(data.get("connectionId")),
                apiKey: String(data.get("apiKey")),
                remember: data.get("remember") === "on",
              }),
            );
          } catch (cause) {
            setError(String(cause));
          } finally {
            secret.value = "";
            setBusy(false);
          }
        }}
      >
        <label>
          {t("connectionAlias")}
          <input
            name="connectionId"
            required
            autoComplete="off"
            disabled={busy || connection?.verified}
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
            disabled={busy || connection?.verified}
          />
        </label>
        <label className="checkbox">
          <input
            name="remember"
            type="checkbox"
            disabled={busy || connection?.verified}
          />
          {t("rememberCredential")}
        </label>
        <button disabled={busy || connection?.verified}>{t("login")}</button>
        <button
          type="button"
          disabled={busy || !connection?.verified}
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
