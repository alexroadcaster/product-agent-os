# LLM/runtime route selection

Source status: repository_source / current_source_inspection; DG05, 2026-11-15.

Owner: runtime/LLM owner + docs-maintainer. Scope: PAOS implementation at `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update with route, prompt/output, credential, budget or telemetry contracts. Test links identify verification routes, not a new runtime run.

## Selector and ownership

[createRuntimeRouteSelector](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/route-selector.ts) serializes connect/disconnect/dispatch. Explicit `route` wins; otherwise presence of `apiKey` selects `local_api_byok`, and absence selects `codex_app_agent`. The App route rejects `apiKey`/`remember`. Changing an engaged route requires disconnect (`ROUTE_DISCONNECT_REQUIRED`); profile and foreign unresolved runs are checked before admission. Failure does not select another gateway.

| Route | Actual path | Evidence boundary |
| --- | --- | --- |
| `codex_app_agent` | [App gateway](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-gateway.mts) → attached consumer/lease → claim/report and domain operations | Selection and host lease do not supply model authentication; `modelAccess` remains `unverified`, and this gateway does not constrain all App host tools |
| `local_api_byok` | [Live gateway](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/live-gateway.mts) → qualified RPC → initialize → broker API-key login → coordinator | Successful auth does not establish model access; manifest/profile/policy gates may reject before dispatch |

## Credentials and failures

[Connection broker](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/connections/broker.ts) calls `account/login/start` with `type: apiKey`, then checks `account/read`. `remember` requires a secure store; the [Windows credential store](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/connections/windows-credential-store.ts) uses a bounded PAOS/profile/connection target and sends the secret through bridge stdin. No key examples or user credential reads are included here. The broker privately retains prior secrets to redact late frames; this is neither a DTO nor telemetry.

On failed connect the broker attempts logout and returns a safe code; no inherited-auth fallback occurs. Ordinary gateway disconnect calls broker.disconnect without `forget`: disconnect must not be documented as deleting stored credentials. RPC closure resets connection state; an uncertain dispatch requires recovery/reconcile rather than automatic replay. [Recovery](../../backend/recovery.md).

## Model/effort and upstream contract

[Team pins](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/team/service.mts) distinguish `requestedModel`/`requestedEffort` from `observedModel`/`observedEffort`, which are null here. The [coordinator](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/codex/coordinator.ts) sets a fixed recipe and `allowProviderModelFallback:false` at thread/start; the inspected turn/start sends no separate model/effort overrides. A pinned asset does not establish the effective model.

Official [Authentication](https://developers.openai.com/codex/auth) and [App Server](https://developers.openai.com/codex/app-server) were checked on 2026-11-15: they describe ChatGPT/API-key authentication and API-key RPC login; the protocol includes model/reasoning capabilities. This upstream contract does not prove PAOS supports every option. The installed adapter and qualification remain local compatibility authorities.

Checks: [route selector](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/runtime-route-selector.test.mts), [connections](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/connections.test.mts), [auth route](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/auth-route.test.mts). DG05 performed source review, not auth/model calls.
