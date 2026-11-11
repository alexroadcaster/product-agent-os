import type { Connection, ConnectionRoute, M1Api } from "../api/client.ts";
export function hasActiveConnection(connection: Connection | null): boolean {
  return (
    connection?.verified === true ||
    ["waiting_for_worker", "connecting", "connected"].includes(
      connection?.state ?? "",
    )
  );
}
export function initialConnectionRoute(
  connection: Connection | null,
): ConnectionRoute {
  return hasActiveConnection(connection)
    ? (connection?.route ?? "local_api_byok")
    : "codex_app_agent";
}
export function connectionRequest(
  route: ConnectionRoute,
  input: { connectionId?: unknown; apiKey?: unknown; remember?: boolean } = {},
): Parameters<M1Api["connect"]>[0] {
  if (route === "codex_app_agent") return { route, connectionId: "codex-app" };
  if (route !== "local_api_byok")
    throw new Error("UNSUPPORTED_CONNECTION_ROUTE");
  if (typeof input.connectionId !== "string" || !input.connectionId.trim())
    throw new Error("CONNECTION_ALIAS_REQUIRED");
  if (typeof input.apiKey !== "string" || !input.apiKey.trim())
    throw new Error("API_KEY_REQUIRED");
  return {
    route,
    connectionId: input.connectionId,
    apiKey: input.apiKey,
    remember: input.remember === true,
  };
}
