# Frontend state, polling and drafts

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: frontend and docs-maintainer. Scope: Web UI at source revision `ad78d5d15aced23febae90d319f2aba00bd64d0b` (DG04). Review when state, lifecycle, polling, draft ACK or API contracts change. Sources: [App](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/App.tsx), [client](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/client.ts), [session polling](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/session-poll.ts), [draft registry](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/draft-registry.ts).

## State ownership

App React state contains `ready`, project list and selection, section, preferences, connection and temporary task/session/asset/graph links. Components own local form, filter, tab, busy and error states. Project data, revisions and authority belong to the local service; their UI presentation does not make the client cache authoritative. [API](../api/index.md) and [transactions](../db/transactions.md) describe the server side.

`createHttpApi` keeps CSRF and project authority epochs in memory and uses same-origin credentials; `SESSION_REQUIRED` clears them. Some commands require a loaded epoch, revision and idempotency key. Changing a local screen alone does not cancel an operation already accepted by the server. The UI does not promise atomicity across independent calls.

## Polling and stale responses

| Flow | Implementation and boundary |
| --- | --- |
| Connection | One request in flight; the next starts 750 ms after completion. A connection version prevents an older read overwriting a newer mutation; dispose suppresses late publication. |
| Open session | Runtime and transcript use independent single-flight lanes and a shared `AbortController`; runtime timer is 750 ms after response. Transcript reads at most 20 pages of 50, merges by ID/revision and reports `hasMore` and errors. If runtime is unavailable, the previous snapshot is constrained to `canSend:false` and `recovery_required`. |
| Catalogs and graph | [SessionsCatalog](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/sessions/SessionsCatalog.tsx), [ArtifactExplorer](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/artifacts/ArtifactExplorer.tsx) and [GraphExplorer](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/graph/GraphExplorer.tsx) use request counters to suppress stale responses; cursor and revision belong to their specific query. |
| Actions / project change | During project registration `navigationEpoch` prevents a late result forcing the selected screen/project after user navigation. `createLatestRequest` aborts superseded requests and suppresses publication after dispose. Not every request in the application uses this helper. |
| Other managers | Decisions and scheduler use separate periodic polling; recipes use their own loop. Read intervals and error handling in each component rather than assuming one global poller. |

HTTP events/history use JSON polling and cursors, not SSE; cursor details and expiry are in [API events](../api/events.md). Aborting fetch limits UI publication but does not itself prove cancellation of a server-side effect. `partial`, `stale`, loading or error must not be interpreted as complete absence of data.

## Message draft and ACK

The session component acquires a registry lease by `(projectId, sessionId)` and reads the saved draft and revision. [Draft autosave](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/draft-autosave.ts) delays a write by 500 ms, serializes optimistic writes and retains a failed intent's key for explicit retry. Conflicting restored contents yield `DRAFT_RECOVERY_CONFLICT` instead of silently adopting a newer revision. A successful write requires an acknowledged increased revision.

Before send, the registry creates a ticket with `clientMessageId`; only a recognized ACK initiates cleanup of the original draft. An uncertain outcome preserves the draft; cleanup failure is reported separately. An App-agent queue ACK does not prove agent work completed. `busy`, selected mode, connection, run state and a valid target constrain send/interrupt/approve availability. See [backend recovery](../backend/recovery.md) for route and recovery limits.

[UI policy](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/policy.ts) fences scope changes when the outcome is unknown; a retained ID of a terminal run alone is not an active fence. Approval responses check binding/run/generation, pending status and expiry; accept also needs reviewable and meaningful details. This is client preflight: the service retains authority and validates current evidence.

## Task form draft

[TaskEditor](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/tasks/Editor.tsx) keeps a structured draft in module memory keyed by project/task (`new` for a new task), displays unsaved status and does not replace a dirty draft with a refreshed server entity. Such a draft can survive navigation and closing details in the same loaded page; it is not persisted in the database or guaranteed after restart. Separate local raw inputs, reason and preview are not part of that record and are not guaranteed after unmount.

Preview passes the current revision and returns a digest; a subsequent edit invalidates it. Save sends the revision and optional digest; errors, including revision conflicts, appear in the form. The in-memory draft is removed only after successful save or explicit discard. Expanding/collapsing the detail overlay retains the same DOM, but changing tabs can unmount the editor: unsaved local-only fields are not guaranteed. [TaskManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/tasks/TaskManager.tsx) and [Modal](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/Modal.tsx) own these boundaries.

## Checks and limits

Related tests: [ui-session-poll.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-session-poll.test.mts), [ui-draft-autosave.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-draft-autosave.test.mts), [ui-draft-registry.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-draft-registry.test.mts), [ui-api.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-api.test.mts). These are coverage references, not a new run. The page describes source mechanisms; live runtime, browser concurrency and human acceptance were not proven by this documentation review.
