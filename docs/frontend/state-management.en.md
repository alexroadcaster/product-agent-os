# Frontend state, polling and drafts

Source status: repository_source / static_contract_review / local_synthetic_browser_acceptance; 2026-11-15.

Owner: frontend and docs-maintainer. Scope: Web UI at source revision `ad78d5d15aced23febae90d319f2aba00bd64d0b` (DG04). Review when state, lifecycle, polling, draft ACK or API contracts change. Sources: [App](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/App.tsx), [client](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/client.ts), [session polling](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/session-poll.ts), [draft registry](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/draft-registry.ts).

The `PAOS-FUNC-03` and `PAOS-FUNC-04` changes below describe the current working tree after DG04; the [FUNC matrix](../planning/functional-remediation-2026-11-15.en.md) owns their acceptance and statuses. DG04 links retain their original provenance and do not present the old revision as fixed.

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

`PAOS-FUNC-03`: **Discard draft** resets the structured model, raw inputs, estimate, reason, error, preview and dirty state together. A new task returns to an empty form; discarded criteria, risks and references do not reappear on the next save. An existing task adopts the current server entity and its revision from the snapshot. Refresh preserves a dirty draft: a save conflict stays visible and retains input; explicit discard adopts server changes, and the next save uses the new revision.

## Workflow assignment draft

`PAOS-FUNC-04`: `WorkflowManager` keeps definition and type assignment drafts in a project memory-only cache. Each has an independent dirty flag and original CAS revision; a mapping-only draft does not dirty the definition. Returning to Settings restores `typeMapping`, `mappingDirty` and its revision, with a visible unsaved warning. App mounts the manager with `key={projectId}`; the initial request ignores a response arriving after unmount. Drafts do not cross projects or survive page reload.

**Save assignments** sends the original revision and clears dirty only after a successful write. Refresh preserves the dirty mapping revision, so another writer produces a conflict without losing input. **Discard assignments** adopts the current server snapshot's mapping and revision and clears mapping dirty/error; the definition draft remains independent. Default workflow changes are separate writes: the pending mapping draft's CAS base advances only to the exact `m2-workflows` revision in its successful ACK, retaining its input. A newer revision from another writer in the following refresh is not automatically adopted; an unconfirmed revision leaves an error and the draft.

## Checks and limits

Related tests: [ui-session-poll.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-session-poll.test.mts), [ui-draft-autosave.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-draft-autosave.test.mts), [ui-draft-registry.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-draft-registry.test.mts), [ui-api.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-api.test.mts). These are coverage references, not a new run. The page describes source mechanisms; live runtime, browser concurrency and human acceptance were not proven by this documentation review.

For F03/F04, `tests/web/single-window/func-g01-drafts-acceptance.mts --synthetic-browser --playwright-core <installed-path> --chromium <installed-path>` ran on 2026-11-15: 54 checks passed against a production build, local HTTP/SQLite and disposable projects. It covered reset, subsequent save, concurrent task updates, navigation/project isolation, stale mapping conflict, discard, another writer between the default-workflow ACK and refresh, and a late response from the previous project; desktop 1440×1000 and mobile 390×844 screenshots are in the local receipt. Mobile coverage checks horizontal overflow rather than full UX/accessibility. The initial RED exposed stale raw fields/error/reason and mapping loss on navigation; an additional RED confirmed possible mapping overwrite between ACK and refresh. The sandbox startup failure and corrected assertions made before ACK/refresh completion are retained separately from behavioral RED. This suite does not establish runtime/model/provider or human acceptance.

## FUNC-18 — snapshot freshness and editor preservation

`GET /projects/:id/freshness` returns a cheap profile stamp: project/root identity, stream generation/throughSeq, scan CAS version and inventory-policy CAS version. It does not traverse the filesystem. HTTP task-manager rows and their stamp come from one SQLite read transaction, avoiding a first-poll baseline captured after an older load. Task Manager and Dashboard poll the stamp single-flight2s after completion, expose stale/unavailable and offer explicit refresh. Cleanup aborts requests/timers; the hidden overview Dashboard unmounts. Full task snapshots are not reloaded every2s.

The expanded task overlay contains its own accessible freshness notice and refresh. Refresh preserves the dirty editor and original optimistic revision; external changes display a conflict notice. Save with the old revision receives409 without clearing the draft. Previous-project requests cannot publish into the newly selected scope.

Filesystem freshness uses bounded explicit rescan/refresh, without a watcher. Directory refresh reloads the current branch; Check file freshness validates the old metadata pin and hides content for stale/missing/forbidden states. Graph/artifact/analysis revisions bind root/policy/inventory; create/modify/rename/delete and policy/root changes invalidate old observations on the next refresh. Analysis GET also checks adapter/core revision. Shared `SourceProvenance` and `sameSourceRevision` support future schema/code-table consumers; F14/F33/F34 own their UI implementation.

Checks: project-freshness API/poll5/5; final browser19/19 (`.tmp/func-g03/browser-final/evidence-IfLiEa/result.json`) covers second-channel change, accessible stale refresh, dirty/CAS409, polling disposal, file modify/rename and stale analysis. Full Web594/594,0skip. Context7: [React effect cleanup](https://react.dev/learn/synchronizing-with-effects).
## Dashboard — A1 pilot states {#dashboard-a1-states}

The contract covers project Overview and All projects in light and dark themes. Dashboard owns its composition, App selects the project and route, and the local service owns the data. The [V3 design](../planning/2026-11-13-v3-ui-implementation-plan.md) supplies the approved composition.

| State | Observable behavior |
| --- | --- |
| Loaded | Totals and progress use available Tasks snapshots. Cancelled tasks are excluded from the progress denominator. The queue uses scheduler positions and recent tasks are sorted by `updatedAt`. |
| Loading | The loading state and expected project count are visible. Refresh stays disabled until reads settle. |
| Empty | A successful empty snapshot shows “No tasks yet.” A successful empty scheduler response shows “Queue is empty.” |
| Error and partial data | Unavailable values are shown as dashes. Coverage appears beside the totals. The source section shows errors and the refresh control retries the reads. |
| Stale | A changed stamp displays a warning and preserves the visible snapshot until explicit refresh. |
| Keyboard and focus | Tab moves from Refresh dashboard to Current data · sources and coverage. Focus is visible and Enter opens the sources. |

Units are tasks, observed runs, and queue positions. Assignments and observed runs over seven days use different sources. Tokens, cost, and `tool_use` stay unavailable when measurements are missing. Synthetic test data is isolated from user application data. Editing, validation, and confirmation do not apply to this read-only Dashboard. F03/F04 and F18 own draft scenarios. [A1 checks](../testing/test-map.en.md#dashboard-a1-criteria)
