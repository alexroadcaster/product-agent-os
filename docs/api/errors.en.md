# Access, validation and errors

Source status: repository_source / static_contract_inventory; 2026-11-15.

Owner: local-service/API; scope/version: DG03, commit `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Update when session gate, bootstrap, body parser or error mapping changes. [API](index.md) · [routes](endpoints.md).

## Access boundaries

[session-gate](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/session-gate.mts) accepts an `http://127.0.0.1:{port}` origin with an exact Host; forwarded host and cross-site are rejected. Mutations require the exact `Origin` and `x-paos-csrf`. Session cookies are `HttpOnly`, `SameSite=Strict`, `Path=/`; idle timeout is 30 minutes, absolute timeout 8 hours, maximum 64 active sessions. Restart/re-pair invalidates them. These checks do not isolate native OS HTTP clients.

[Browser launch](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/browser-launch.mts) requires direct navigation with Fetch Metadata, a one-time proof and cookie; `/bootstrap/exchange` uses a one-time pairing code (60 seconds, at most five attempts). `/health` needs no session. `/agent/v1` is a separate internal capability channel: Bearer token from the profile descriptor, exact origin, POST and JSON up to 65536 bytes. Browser cookies do not confer this authority. [Agent channel source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-channel.mts).

## JSON and common errors

[Handler](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts) requires a JSON object; default body limit is 1 MiB, upload 70 MiB, task-manager commands 16 MiB, team proposal preview/apply 8 MiB, imports preview 3 MiB; desktop picker 8192 bytes, app handoff 4096 and launch proof 1024. Domain validators can be stricter.

| HTTP status | Condition / code |
| --- | --- |
| 400 | `INVALID_REQUEST` and codes not matching the categories below |
| 401 | `SESSION_REQUIRED`, `PAIRING_INVALID` |
| 403 | `ORIGIN_REJECTED`, `CSRF_INVALID`, `LAUNCH_REJECTED` |
| 404 | code contains `NOT_FOUND` |
| 409 | code contains `CONFLICT`, `REQUIRED`, `UNAVAILABLE`, `AUTHORITY`, `FORBIDDEN`, `BLOCKED`, `UNVERIFIED`, `UNQUALIFIED`, `DRIFT`, `BUSY`, `STALE` or `PRIVATE` |
| 413 / 415 | `REQUEST_TOO_LARGE` / `JSON_REQUIRED` |

Error response: `{ "error": { "code": "REVISION_CONFLICT" } }`. A safe `cyclePath` may add bounded `details`. This is a synthetic shape; clients should use the code rather than expose exception contents. The private agent channel has its own 401/403/404/405/409/413/415 mapping. See [service-api tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/service-api.test.mts) and [client](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/web/src/api/client.ts). Their presence is not a claim of a new test run.
