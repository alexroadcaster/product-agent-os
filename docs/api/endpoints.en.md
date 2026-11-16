# Endpoint inventory

Source status: repository_source / current_source_contract_review; 2026-11-15.; FUNC-G04: locally_verified_with_measured_limits, 16.11.2026.; FUNC-G05 locally_verified_with_explicit_limits, 16.11.2026.

Owner: local-service/API maintainers; scope/version: DG03, commit `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Update when handler, client, delegate service or tests change. [Backend](../backend/index.md); [authentication/errors](errors.md); [events](events.md).

Every browser `/api/v1` route below requires the loopback session and same-origin validation; non-GET/HEAD additionally require `Origin` and `x-paos-csrf`. Exceptions `/health`, `/launch`, bootstrap and `/agent/v1` are listed explicitly. A dash means no application body/query, not no HTTP headers. Non-GET routes with listed JSON require `application/json`; per-row parameters are handler-level summary; field-level constraints and return types are owned by linked implementation/contracts below. Client `Record<string, unknown>` is not a published exhaustive schema. Default success JSON is 200 unless stated; binary downloads and HTML bootstrap are exceptions. Errors are mapped in [errors](errors.md).

Each row applies only its explicitly listed pagination, revision or idempotency rules; otherwise none are imposed by the HTTP handler. Domain services may impose additional revision, cursor and idempotency checks: their contract links below are authoritative, and claiming that an unspecified field is optional would be unsafe. A mutation may be rejected by `MIGRATION_BUSY` even if syntactically valid. These tables document source behavior, not fresh live verification.

| Method and path | Request / query | Response | Side effect / fence |
| --- | --- | --- | --- |
| `GET /health` | — | instanceId, build, alive, sourceReaderReady, runtimeCapable, browserLaunchVersion | health only |
| `GET /launch` | direct navigation Fetch Metadata | HTML bootstrap or 303 | session bootstrap; see launch |
| `POST /bootstrap/launch` | JSON proof and launch cookie | csrfToken, instanceId, actorId + session cookie | consumes one-time proof |
| `POST /bootstrap/exchange; POST /api/v1/bootstrap/exchange` | JSON code | csrfToken, instanceId, actorId + session cookie | consumes pairing code |
| `POST /agent/v1/{attach,heartbeat,claim,report,command,operation,progress,reconcile,task-create}` | private capability JSON; Bearer token | action result or agent error | private channel; no browser-cookie authority |
| `GET /api/v1/session` | — | actorId, csrfToken, instanceId | session principal |
| `POST /api/v1/quit` | — | 202 status=quit_requested | request owner shutdown |
| `POST /api/v1/logout` | — | revoked | revoke sessions / launch proofs |
| `GET /api/v1/preferences` | — | locale, theme | read profile settings |
| `PUT /api/v1/preferences` | locale, theme | saved preferences | write settings |
| `POST /api/v1/desktop/project-folder` | requestId, optional initialDirectory | cancelled or workspaceRoot | native picker; requestId replay requires identical payload |
| `POST /api/v1/connection/app-handoff` | requestId | opened, requiresSend, verified, state | opens draft; does not send; requestId replay requires identical payload |
| `GET /api/v1/connection` | — | connection state | inspect status |
| `POST /api/v1/connection` | route?, connectionId, apiKey?, remember? | connection state | connect selected route; credentials sensitive |
| `DELETE /api/v1/connection` | — | connection state | disconnect |
| `GET /api/v1/runtime/state` | projectId?, sessionId? | runtime snapshot, pending approvals | may synchronize observed decisions |
| `POST /api/v1/runtime/{bindings,send,interrupt,approve,reconcile}` | action-specific JSON | runtime/decision result | dispatch / interrupt / approval; no implicit fallback |
| `GET /api/v1/projects` | — | items of id, name, keyPrefix, authorityMode, authorityEpoch, streamGeneration | list registered projects |
| `POST /api/v1/projects` | name, workspaceRoot, keyPrefix?, legacySource?, requestId?, scan? | 201 id/name/keyPrefix/authorityMode/authorityEpoch, optional scan | register; scan may be partial; requestId replay optional |
| `GET /api/v1/projects/{projectId}` | projectId | id/name/keyPrefix/authorityMode/authorityEpoch/streamGeneration | read project |
| `GET /api/v1/projects/{projectId}/sources` | projectId | bounded source coverage | inspect allowlisted project sources |
| `GET /api/v1/projects/{projectId}/sources/{name}` | name | relativePath/content/sha256/coverage/redacted | read bounded source, not arbitrary directory |
| `GET /api/v1/projects/{projectId}/catalogs` | projectId | agents, skills, graph, coverage | bounded read-only catalog |
| `GET /api/v1/projects/{projectId}/entities` | kind?, parentId?, limit?, offset?, order? | items, hasMore | limit 1–100 default50; private kinds hidden |
| `GET /api/v1/projects/{projectId}/entities/{id}` | entity id | stored entity | settings/run/approval denied |
| `POST /api/v1/projects/{projectId}/commands` | idempotencyKey, expectedAuthorityEpoch, changes[] | write result | revision/authority checked; write |
| `POST /api/v1/projects/{projectId}/tasks/{taskId}/check` | expectedRevision, expectedAuthorityEpoch, idempotencyKey, outcome, note? | check receipt | record manual check |
| `POST /api/v1/projects/{projectId}/tasks/{taskId}/accept` | expectedRevision, expectedAuthorityEpoch, idempotencyKey, checkId, accepted, note? | acceptance result | owner acceptance separate from check |
| `GET /api/v1/projects/{projectId}/search` | q, offset? | items, coverage, generation, hasMore | FTS; limit50, private kinds filtered |
| `POST /api/v1/projects/{projectId}/search/rebuild` | JSON object | status, coverage | rebuild local search; abort signal |
| `GET /api/v1/projects/{projectId}/{events,history}` | cursor? | items, generation, nextCursor | signed cursor; replay and immutable audit differ |
| `POST /api/v1/projects/{projectId}/imports/preview` | sources[] or sourceName + content; sourceRelativePath? | stageId, parserVersion, sourceDigest, proposal, sources, items, blocked | writes staging document; not pure read |
| `GET /api/v1/projects/{projectId}/imports/source-status` | — | authorityMode, items | read source status |
| `POST /api/v1/projects/{projectId}/imports/commit` | stageId, sourceDigest, expectedAuthorityEpoch, idempotencyKey, currentSource? | receipt, sourceDigest, backupId, mappingCount | cutover; fenced by authority |
| `GET /api/v1/projects/{projectId}/imports/export` | — | reverse-transfer document | read export |
| `POST /api/v1/projects/{projectId}/{backups,task-manager/export}` | — | format, scope, restoreEndpoint, backupId, manifest, rotationCandidateIds, retention | writes full local profile backup |
| `POST /api/v1/projects/{projectId}/backups/rotation` | candidateIds[] | rotatedBackupIds, retention | deletes selected managed backups |
| `POST /api/v1/projects/{projectId}/{restores,task-manager/import-backup}` | backupId | restoreId, requiresRestart, activeProfileChanged=false | writes staged restore; active profile unchanged |
| `GET /api/v1/projects/{projectId}/decisions` | kind?, state?, sessionId?, offset?, limit? | DecisionsPage | sync observed decisions |
| `POST /api/v1/projects/{projectId}/decisions` | decision input | DecisionView | create decision; migration freeze |
| `GET /api/v1/projects/{projectId}/decisions/{id}` | decision id | DecisionView | read |
| `POST /api/v1/projects/{projectId}/decisions/{id}/respond` | response input | DecisionResponse | respond; migration freeze |
| `GET /api/v1/projects/{projectId}/graph/status` | — | GraphStatus | read index state |
| `POST /api/v1/projects/{projectId}/graph/rebuild` | JSON object | GraphStatus | rebuild local index |
| `GET /api/v1/projects/{projectId}/graph` | revision, query?, depth?, nodeId?, edgeTypes?, limit?, cursor? | GraphPage | bounded graph, partial coverage |
| `GET /api/v1/projects/{projectId}/graph/source` | revision, fileId, start?, end? | GraphSourceExcerpt | read bounded source excerpt |
| `GET /api/v1/projects/{projectId}/graph/nodes/{id}` | revision query | GraphNodeDetail | read node at revision |
| `GET /api/v1/projects/{projectId}/graph/nodes/{id}/impact` | revision/query as code-index service | GraphImpact | read bounded impact |
| `GET /api/v1/projects/{projectId}/scheduler` | — | QueueSnapshot | read scheduler |
| `POST /api/v1/projects/{projectId}/scheduler/{preview,enqueue,pause,resume,reorder,cancel,pause-entry,resume-entry}` | action-specific scheduler JSON | QueuePreview or entryId?/revision | preview or queue mutation; migration freeze |
| `GET /api/v1/projects/{projectId}/execution-recipes` | — | items: RecipeExecutionView[] | list executions |
| `POST /api/v1/projects/{projectId}/execution-recipes/{preview,start}` | recipe input | RecipePreview or RecipeExecutionView / manual target | preview/start; migration freeze |
| `GET /api/v1/projects/{projectId}/execution-recipes/{id}` | execution id | RecipeExecutionView | read execution |
| `POST /api/v1/projects/{projectId}/execution-recipes/{id}/{pause,resume,cancel,reconcile}` | action-specific JSON | RecipeExecutionView | execution transition; migration freeze |
| `GET /api/v1/projects/{projectId}/autonomy` | — | AutonomySnapshot | read policy |
| `POST /api/v1/projects/{projectId}/autonomy/preview` | policy, expectedRevision | AutonomyPreview | validate preview |
| `POST /api/v1/projects/{projectId}/autonomy/{save,resume,pause}` | policy/command input | AutonomySnapshot; pause may include interrupts | save or transition; migration freeze |
| `GET /api/v1/projects/{projectId}/task-manager` | — | ManagerSnapshot | read task projections |
| `POST /api/v1/projects/{projectId}/task-manager/commands` | action, idempotencyKey, expectedAuthorityEpoch, action fields / expectedRevision | result; may include pendingStop | writes tasks/links/workflows; freeze and revisions |
| `POST /api/v1/projects/{projectId}/task-manager/links/{id}/stop` | JSON object | pending stop status | request runtime stop |
| `POST /api/v1/projects/{projectId}/task-manager/reference` | taskId, relativePath, revision? | availability, relativePath, revision?, expectedRevision?, reason?, content?, redacted? | bounded source reference |
| `POST /api/v1/projects/{projectId}/tasks/{taskId}/attachments` | filename, mediaType, base64, expectedRevision, expectedAuthorityEpoch, idempotencyKey | upload result | managed blob write |
| `GET /api/v1/projects/{projectId}/tasks/{taskId}/attachments/{id}` | taskId, attachmentId | binary download | read managed attachment |
| `GET /api/v1/projects/{projectId}/team/runs/{id}` | run id | id, sessionId, taskId, status, mode, route, timestamps, assetPins, workflow, coverage, source | redacted persisted run |
| `GET /api/v1/projects/{projectId}/team/catalog` | — | TeamCatalog | read team assets |
| `POST /api/v1/projects/{projectId}/team/generation` | generation input | generation result | start generation; runtime dependent |
| `GET /api/v1/projects/{projectId}/team/generation/{id}` | generation id | generation result | read generation |
| `GET /api/v1/projects/{projectId}/team/skills/discovery` | q? | discovery result | read skill catalog |
| `POST /api/v1/projects/{projectId}/team/skills/source-preview` | sourceRootId, relativePath | source preview | bounded read |
| `POST /api/v1/projects/{projectId}/team/skills/generation` | generation input | generation result | start skill generation |
| `GET /api/v1/projects/{projectId}/team/skills/generation/{id}` | generation id | generation result | read |
| `POST /api/v1/projects/{projectId}/team/skills/generation/{id}/apply` | proposal input | apply result | write; migration freeze |
| `POST /api/v1/projects/{projectId}/team/proposals/preview` | proposal JSON | AssetPreview | preview |
| `POST /api/v1/projects/{projectId}/team/proposals/apply` | proposal JSON, idempotencyKey as contract | assetId, version | apply; migration freeze |
| `GET /api/v1/projects/{projectId}/team/metrics` | from, to | metrics result | read |
| `POST /api/v1/projects/{projectId}/team/assets/{id}/copy-preview` | JSON object | copy preview | preview |
| `GET /api/v1/projects/{projectId}/team/assets/{id}` | asset id | AssetProfile | read |
| `GET /api/v1/projects/{projectId}/team/assets/{id}/history` | asset id | assetId, versions | read history |
| `GET /api/v1/projects/{projectId}/team/assets/{id}/export` | asset id | export object | read export |
| `GET /api/v1/projects/{projectId}/team/assets/{id}/resources/{path}` | version? | binary download | read asset resource |
| `GET /api/v1/projects/{projectId}/sessions/catalog` | q?, archived?, status?, taskId?, agentId?, source?, limit?, cursor?, anchor? | catalog result | read |
| `GET /api/v1/projects/{projectId}/sessions/search` | q, limit?, cursor?, anchor? | search result | read |
| `GET /api/v1/projects/{projectId}/sessions/{id}/transcript` | limit?, cursor?, anchor? | transcript result | read session |
| `GET /api/v1/projects/{projectId}/artifacts` | q?, kind?, taskId?, limit?, cursor? | ArtifactPage | bounded snapshot |
| `GET /api/v1/projects/{projectId}/artifacts/{id}` | version? | ArtifactDocument | read document |
| `POST /api/v1/projects/{projectId}/artifacts/proposals/preview` | proposal input | preview result | preview |
| `POST /api/v1/projects/{projectId}/artifacts/proposals` | proposal input | proposal result | persist proposal; migration freeze |


## FUNC-G03: current local contract

This 2026-11-15 addition describes current `http/application.mts`, `project-files/service.mts`, `project-scans/service.mts` and `runtime/task-file-preflight.mts`; the pinned DG03 links below retain their historical version.

| Method and path under `/api/v1` | Input | Result and boundary |
| --- | --- | --- |
| `GET /projects/{id}/files` | `path`, `cursor?`, `limit?`, `filter?`, `query?` | Lazy single-directory page; `filter=all/control_plane`, current-directory search, default100/max200; coverage/reasons and access metadata |
| `GET /projects/{id}/files/read` | `path`, `revision?`, `line?` | `available/stale/forbidden/binary/too_large/unsupported/unavailable`; content only for `available`, plain text with display redaction |
| `GET /projects/{id}/files/policy` | — | `version`, `policy`, `policyVersion` |
| `POST /projects/{id}/files/policy` | `policy`, `expectedVersion` | Profile-owned CAS; include/exclude/respectGitignore cannot override hard deny |
| `GET /projects/{id}/scans` | — | Persisted latest/lastSuccessful and stage outcomes |
| `POST /projects/{id}/scans` | `requestId?`, `revision?` | 202; bounded background scan, request replay/coalescing and scope fences |
| `POST /projects/{id}/scans/{scanId}/cancel` | empty JSON object | Cancel the project's owned scan |
| `POST /projects/{id}/scans/{scanId}/retry` | empty JSON object | 202; new attempt using an idempotent retry key |
| `GET /projects/{id}/analysis` | — | Persisted core analysis checked against current source/adapter revisions; explicit unavailable/stale |
| `POST /projects/{id}/runtime/file-preflight` | `taskId`, required integer `expectedRevision` | Metadata-only `allowed`, limits/counts/items/reasons, digest/taskRevision and source pins; no content/diff |
| `GET /projects/{id}/freshness` | — | Cheap profile stamp without filesystem traversal |

`POST /projects` persists registration first. `scan:true` requests a background scan; the response may include `scan` or `scanError`, and scan failure preserves registration. Replaying `requestId` requires the same registration payload. `GET task-manager` returns entities and freshness from one SQLite read transaction.

The registry owns root and policy; the browser cannot supply an arbitrary root. `fileRevision` is a metadata/policy pin; `hash` and reference `revisionKind=sha256` pin raw-byte content. They are not interchangeable. Freshness `policyVersion` is an integer CAS version; source `policyVersion` is a string identity. Preflight reads saved task scope and rejects stale task revision; the optional execution client guard `{digest,taskRevision}` does not authorize execution. The gateway checks preflight at admission and rechecks access during capture before a native command; approvals and broker restrictions remain applicable.

The parent agent's current bounded integration receipts are F29 API 6/6, file-preflight API 1/1, gateway policy 28/28 and F18 5/5. These are handed-off local results; this page does not claim a new final browser/native run or human acceptance. The next artifact is the concrete API/scan result with provenance, followed by its applicable user check.

## Action-level fields and fences

The following minimum fields and result shapes apply to the App-agent route and listed service implementations. API BYOK has a separate [live gateway](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/live-gateway.mts); do not assume that its input or available actions are identical. Question marks mark conditionally optional values. The private agent channel uses the common workerId/generation/leaseToken except attach; it is not a browser API.

| Action | Required / conditional input | Result / fence | Source |
| --- | --- | --- | --- |
| `runtime/bindings` | projectId, sessionId, mode (discussion/planning/execution) | bindingId, projectId, sessionId, mode, route | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L256-L282) |
| `runtime/send` | projectId, sessionId, bindingId, clientMessageId, input; taskId required in execution; autonomy?, taskCreationApproved?; approval only in execution without autonomy; handler injects actorId as taskCreationInitiator and rejects caller-supplied field | public job {id,bindingId,projectId,sessionId,state,mode,route}; same messageId/digest replay | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L283-L325) |
| `runtime/interrupt` | projectId, sessionId, bindingId, runId | public job; queued → interrupted, running → cancel_requested | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L340-L344) |
| `runtime/approve` | projectId, sessionId, bindingId, runId, generation, requestId, decision=accept/decline/cancel | operation view; scoped approval decision | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L326-L339) |
| `runtime/reconcile` | projectId, sessionId, bindingId; optional runId/resolution=cancel_undispatched | public job or null; only undispatched cancellation | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L345-L354) |
| `agent/attach` | hostIdentity=codex_app, workerId, generation | workerId, generation, leaseToken, expiresAt | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L357-L362) |
| `agent/heartbeat` | workerId, generation, leaseToken | expiresAt, job, jobs | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L363-L364) |
| `agent/claim` | workerId, generation, leaseToken, runId? | job or null; claim transitions queued → running | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L365-L374) |
| `agent/report` | workerId, generation, leaseToken, runId, seq, idempotencyKey, status; text required if completed | runId, seq, state, route; replay only for identical key/digest | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L413-L428) |
| `agent/command` | workerId, generation, leaseToken, runId, operationId, argv[], timeoutMs? | operation view awaiting approval; timeout 1–30000ms | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L399-L411) |
| `agent/operation` | workerId, generation, leaseToken, runId, operationId | operation view | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L375-L380) |
| `agent/progress` | workerId, generation, leaseToken, runId, seq, text, phase | runId, seq; monotonic sequence | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L396-L398) |
| `agent/reconcile` | workerId, generation, leaseToken, runId | last report receipt or public job | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L375-L379) |
| `agent/task-create` | workerId, generation, leaseToken, runId, operationId, title, summary, acceptanceCriteria[] | taskId, runId, sessionId; owner-opted-in execution only | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L382-L395) |
| `scheduler/preview` | taskId, transitionId, mode=recipe, sessionId, roleBindings, expectedTaskRevision, reason | QueuePreview including previewDigest and queueRevision | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts#L46-L47) |
| `scheduler/enqueue` | preview input + previewDigest, expectedRevision, expectedAuthorityEpoch, idempotencyKey | entryId, revision; receipt binds action+payload | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts#L67-L73) |
| `scheduler/pause, resume` | expectedRevision, expectedAuthorityEpoch, idempotencyKey | revision | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts#L74-L75) |
| `scheduler/reorder` | expectedRevision, expectedAuthorityEpoch, idempotencyKey, order[] | revision; order must be complete permutation | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts#L74-L76) |
| `scheduler/cancel, pause-entry, resume-entry` | expectedRevision, expectedAuthorityEpoch, idempotencyKey, entryId | revision; entry state constraints | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts#L74-L80) |
| `execution-recipes/preview` | taskId, transitionId, mode, expectedTaskRevision, reason; sessionId and roleBindings for recipe mode | RecipePreview and previewDigest | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/execution-recipes/service.mts#L33-L52) |
| `execution-recipes/start` | preview input + previewDigest, expectedAuthorityEpoch, idempotencyKey | RecipeExecutionView or manual result | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/execution-recipes/service.mts#L143-L149) |
| `execution-recipes/{id}/pause,resume,cancel,reconcile` | expectedRevision, expectedAuthorityEpoch, idempotencyKey; reason? | RecipeExecutionView; action-specific recovery checks | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/execution-recipes/service.mts#L151-L180) |
| `autonomy/preview` | policy, expectedRevision | AutonomyPreview incl previewDigest | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/autonomy-policy/service.mts) |
| `autonomy/save` | policy, previewDigest, expectedRevision, expectedAuthorityEpoch, idempotencyKey | AutonomySnapshot | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/autonomy-policy/service.mts#L42-L52) |
| `autonomy/pause, resume` | expectedRevision, expectedAuthorityEpoch, idempotencyKey | AutonomySnapshot; pause may include interrupts | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/autonomy-policy/service.mts#L42-L61) |
| `decisions POST` | kind=clarification/product, title, body, expiresInSeconds, expectedAuthorityEpoch, idempotencyKey; taskId?, sessionId?, proposedDiff?, evidenceIds? | DecisionView; 60–604800s expiry | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/decisions/service.mts#L112-L116) |
| `decisions/{id}/respond` | expectedRevision, expectedAuthorityEpoch, idempotencyKey, response; answer?, reason? | DecisionResponse; review/authority checks | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/decisions/service.mts#L79-L109) |


### Team and artifact proposals

| Action | Input | Result / fence | Source |
| --- | --- | --- | --- |
| `team/proposals/preview` | proposal, expectedRevision; proposal.kind/action/name/description/content/reason/dependencies; assetId for non-create | AssetPreview {proposal,baseRevision,diff,dependencyImpact,warnings,previewDigest} | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/team/contract.mts#L8-L43) |
| `team/proposals/apply` | proposal, expectedRevision, epoch, idempotencyKey, previewDigest | assetId, version; verifies exact preview and transaction fences | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/team/service.mts#L28-L37) |
| `team/generation` | description, sessionId, bindingId; targetAssetId?, idempotencyKey? | id, sessionId, runId, purpose, state | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/team/generation.mts#L5-L11) |
| `team/skills/generation` | mode=requirements/description, sessionId, bindingId, description?; requirements mode requires expectedRevision, startLine?, endLine? | id, runId, sessionId, state, generationKey, requirements, applyKey | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/team/skill-generation.mts#L21-L33) |
| `team/skills/generation/{id}/apply` | proposal, previewDigest, epoch; expectedRevision=0 and applyKey assigned by service | assetId, version; validates proposal/requirement revision | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/team/skill-generation.mts#L68-L75) |
| `artifacts/proposals/preview` | documentId, sourceVersion, body | documentId, sourceVersion, before, after, previewDigest, applied=false, policy=staged_only | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/artifacts/service.mts#L57) |
| `artifacts/proposals` | documentId, sourceVersion, body, previewDigest, epoch, idempotencyKey | id, staged=true, replayed; staged only, no target apply | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/artifacts/service.mts#L59) |

## Detailed service contracts and tests

These links provide complete current validation for the inputs summarized above; generated OpenAPI is not available. No repository or target scripts are run for this inventory.

| Family | Implementation | Contract / tests |
| --- | --- | --- |
| HTTP / auth | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/session-gate.mts) |
| UI client | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/web/src/api/client.ts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/service-api.test.mts) |
| Task manager | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/task-manager/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/issues/manager.ts) |
| Runtime / channel | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/route-selector.ts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-channel.mts) |
| Graph | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/code-index/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/graph/code-graph.ts) |
| Decisions | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/decisions/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/decisions/decision.ts) |
| Scheduler | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/scheduler/queue.ts) |
| Recipes | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/execution-recipes/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/execution-recipes/recipe.ts) |
| Autonomy | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/autonomy-policy/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/autonomy/policy.ts) |
| Team / assets | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/team/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/team/assets.ts) |
| Sessions | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/sessions/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/sessions/history.ts) |
| Artifacts | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/artifacts/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/artifacts/catalog.ts) |
| Storage / import | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/local-store.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/import-export/migration.mts) |

Graph queries require an existing matching `revision`; pagination cursor is scoped to revision and filters. `graph/source` additionally needs `fileId`, optional bounded `start`/`end`, and a fresh index. Decisions use `offset`/`limit` (default 50, 1–100), not the graph cursor. Session history uses a frozen 15-minute snapshot cursor, `limit` 1–100; artifact snapshots also use scoped cursors. See [events](events.md).

`scan=true` on project creation performs bounded existing source inspection and graph rebuild, reporting partial failures after committed registration. It is not a full directory browser or the planned managed background scan F26–F29. PoC and target database/schema/code-table endpoints F30–F34 are not represented by this API. [Functional backlog](../planning/functional-remediation-2026-11-15.md) owns those future capabilities.

Limits: only source and listed tests were inspected; no provider, real profile/database, network server or application runtime was exercised. [Source registry](../sources/registry.md); [Web task plan](../planning/product-agent-os-web-task-manager-plan-2026-11-09.md).

## FUNC-G04 / F09 — bounded history and artifact summaries

Session catalog selects sessions and related task/run attribution in SQLite. Transcript filters kind, parent and hidden/analysis/reasoning before materialization; search preserves Unicode case folding. The Worker freezes membership and values in connection-private SQLite TEMP tables: edits, inserts, deletions or archival after page one do not alter later pages. `journalOrder` retains the insertion ordinal. Only the current page enters JavaScript and uses the existing redaction mapper; whole history bodies are not transferred to the LocalStore caller.

Cursors last up to 15 minutes and may be evicted by LRU storage pressure. Scope includes project/root identity, authority epoch, inventory policy and query/filters; mismatch, expiry, eviction or restart returns `CURSOR_STALE`. `limit` is 1–100; the byte cap may return fewer items, and `nextCursor` continues without skipping values. Response budget is 1 MiB with metadata headroom. An oversized item returns `HISTORY_ITEM_TOO_LARGE`; over 200,000 rows or payload budget returns `HISTORY_SNAPSHOT_BUSY`. SQL size preflight precedes freezing, eviction precedes insert, and rollback retains existing cursors. Aggregate payload is bounded at 230 MiB, leaving room for indexes/page metadata; `temp.max_page_count` also caps the main TEMP database file at 256 MiB. This does not cap RSS or all disk I/O: transient SQLite sorting/journal overhead is separate. No persistent schema or migration changes.

Artifact catalog receives SQL `substr(body,1,280)` and selected kinds while retaining frozen summaries/cursors and root/policy checks. For longer persisted bodies, reason `persisted_body_preview_only_search` means title/preview-only search; absence in the rest of the body is not established. Projection over 6 MiB reports partial reason `artifact_projection_byte_limit`; existing catalog snapshot budgets remain active. Raw persisted document reads check SQL byte lengths before loading: body up to 512 KiB, metadata up to 256 KiB, otherwise `DOCUMENT_TOO_LARGE`. Workspace document reads retain existing checked-source guards.

Current synthetic regression route: `node --test tests/web/snapshot-history-scale.test.mts` — 9/9: 100,000 messages around 100 MiB, 1000 documents of 107,315 bytes, page-only mapping, immutable edit/archive values, LRU/expiry/scope drift, rollback, byte caps, Unicode and oversized-read rejection. Existing session/source-policy/code-index integration was checked separately; native-junction skips remain gaps. These checks do not replace F20 after/final p95/soak or human acceptance. Node `DatabaseSync.function` was verified through Context7 `/nodejs/node/v26.0.0` against [official documentation](https://github.com/nodejs/node/blob/v26.0.0/doc/api/sqlite.md); installed Node is v26.5.0.

## FUNC-G04 — code graph, schema and static queries

GET graph accepts mode=all|dependencies|symbols, direction=both|incoming|outgoing and nodeId/pathTo for bounded static paths (8 hops/1000 visited nodes). Search, filters and cursors bind revision and cache generation; restart/eviction requires rebuild. These are imports/lexical occurrences, not runtime calls.

GET /projects/:id/database returns registration/status/candidates only. POST database/source selects relativePath+expectedFileRevision+expectedVersion or clears selection without opening SQLite. POST database/scan runs F27 inventory+schema; standard cancel/retry routes preserve selected stages. GET database/schema returns a bounded page, escaped Mermaid and diagramEntities from one snapshot. GET database/changes compares two compatible metadata snapshots; current/stale/incompatible and missing baseline remain distinct. Source admission does not permit generic Files DB reads. The adapter is Windows/offline SQLite; no PostgreSQL, credentials, row reads or project SQL.

GET /projects/:id/code-database and GET code-database/links return status and static source evidence; POST code-database/scan runs inventory+code_database. Links require codeRevision and schemaRevision, support table/path/operation/confidence/limit/cursor, and are bounded to32KiB. Confirmed requires source binding; inferred/unresolved do not become runtime facts. SQL values and rows are not returned.

POST /agent/v1/project-query is a private App-agent action requiring channel capability, worker lease, runId, kind=status|links and the same query fields. Project scope comes from the claimed run; payload projectId is rejected. Lease/run/scope are checked before and after the async read; response≤32KiB. Browser cookies do not grant this capability. Claimed jobs advertise the query port. Verification uses a synthetic worker without a model/provider call.

## FUNC-G05 — current contracts

F11 GET /team/metrics requires ISO from/to with a timezone and from<to, accepts taskId/sessionId/agentId and selects runs started in [from,to). More than1000runs or a1MiB response raises METRICS_PERIOD_TOO_BROAD without silent truncation. F12 GET /team/skills/discovery?external=1 enables the fixed-source external reader; POST /team/skills/remote-preview accepts only candidateId/revision. F13 POST /artifacts/proposals/{apply-preview,apply,recover,rollback-preview,rollback} uses strict DTOs, paired session/CSRF and authority checks. Preview/recovery are not acceptance. F16 GET /sessions/{catalog,search} and transcript add source capabilities; /team/assets/:id adds executionEvidence and /team/runs/:id separates requested/observed values. F15 policy remains autonomy_policy_v1 with optional maxCommandsTotal; exhaustion returns AUTONOMY_TOTAL_COMMAND_BUDGET_EXHAUSTED/409. Unsupported budget fields are rejected.
