import { test } from "node:test";
import assert from "node:assert/strict";
import {
  connectionRequest,
  initialConnectionRoute,
  hasActiveConnection,
  appHostTransportLabel,
} from "../../apps/web/src/ui/connection-controls-model.ts";
test('App transport metadata never turns endpoint presence into a verified App connection',()=>{
 assert.equal(appHostTransportLabel({verified:false,route:'codex_app_agent',hostTransport:{status:'unavailable',reason:'app_host_endpoint_missing',transport:'websocket_over_stdio_proxy'}}),'appHostEndpointMissing');
 assert.equal(appHostTransportLabel({verified:false,route:'codex_app_agent',hostTransport:{status:'unverified',reason:'app_host_endpoint_unverified',transport:'websocket_over_stdio_proxy'}}),'appHostEndpointUnverified');
 assert.equal(appHostTransportLabel({verified:true,route:'codex_app_agent'}),null);
 assert.equal(appHostTransportLabel({verified:false,route:'local_api_byok'}),null);
});
test("App-agent is the default with an exact keyless body and no inherited API fields", () => {
  assert.equal(initialConnectionRoute(null), "codex_app_agent");
  assert.equal(
    initialConnectionRoute({
      verified: false,
      route: "local_api_byok",
      state: "unverified",
    }),
    "codex_app_agent",
  );
  assert.deepEqual(
    connectionRequest("codex_app_agent", {
      apiKey: "synthetic-leftover",
      connectionId: "previous",
      remember: true,
    }),
    { route: "codex_app_agent", connectionId: "codex-app" },
  );
});
test("BYOK is explicit, validates credentials without fallback, and keeps legacy connected fixtures recognizable", () => {
  assert.equal(initialConnectionRoute({ verified: true }), "local_api_byok");
  assert.deepEqual(
    connectionRequest("local_api_byok", {
      connectionId: "synthetic-account",
      apiKey: "synthetic-not-a-key",
      remember: true,
    }),
    {
      route: "local_api_byok",
      connectionId: "synthetic-account",
      apiKey: "synthetic-not-a-key",
      remember: true,
    },
  );
  assert.throws(() => connectionRequest("local_api_byok", {}), /REQUIRED/);
  assert.throws(() => connectionRequest("unknown" as any), /UNSUPPORTED/);
});
test("waiting App-agent is disconnectable without claiming a verified worker", () => {
  const waiting = {
    route: "codex_app_agent" as const,
    state: "waiting_for_worker",
    verified: false,
    nativeSandbox: false,
    cooperativeCancel: true,
  };
  assert.equal(hasActiveConnection(waiting), true);
  assert.equal(initialConnectionRoute(waiting), "codex_app_agent");
  assert.equal(
    initialConnectionRoute({ ...waiting, verified: true, state: "connected" }),
    "codex_app_agent",
  );
  assert.equal(waiting.verified, false);
  assert.equal(
    hasActiveConnection({ verified: false, state: "disconnected" }),
    false,
  );
});
