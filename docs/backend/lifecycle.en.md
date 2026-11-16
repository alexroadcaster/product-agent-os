# Backend: local-service lifecycle

Source status: repository_source / static_source_review + bounded_native_synthetic_verified; 2026-11-15.; FUNC-G04: locally_verified_with_measured_limits, 16.11.2026.

Owner: backend/local-service and runtime owner. Scope/version: DG03, `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Update when startup, session admission, route selection or shutdown changes.

## Startup and admission

1. [main.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/main.mts) exports `startLocalService`: importing it creates no server, database, GUI or runtime child. The executable entrypoint requires launcher IPC and profile/instance ID. The profile must be an absolute local path; identity is bound before opening `state.sqlite`.
2. Store, runtime gateways, selector, recipes and scheduler are created; the HTTP listener binds an ephemeral `127.0.0.1` port. Code checks Host, origin and target and bounds request sizes. Health reports `alive` and separately `runtimeCapable`; the former does not prove the latter.
3. [session-gate.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/session-gate.mts) keeps sessions in memory: restart and re-pair invalidate prior cookies. Mutation requires origin and CSRF; exact origin/host are checked for reads too. Direct-navigation bootstrap and pairing are distinct entry paths to the shared session contract.
4. [route-selector.ts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/route-selector.ts) serializes connect/disconnect/runtime actions; default is `codex_app_agent` when neither route nor API key is supplied, while an `apiKey` without route selects `local_api_byok`. Switching an engaged route requires disconnect; no implicit fallback occurs. An App route does not prove an attached consumer.

## Native runtime qualification — FUNC-01

The current checkout is checked against the exact tuple in `packages/contracts/runtime/qualified-manifest.json`: Codex binary, Node binary/version, Windows release/arch, SQLite, adapter sources and Web lockfile. A UI dependency change can alter the lockfile and stop the broker with `package_lock_mismatch` even if the adapter is unchanged. Updating a pin requires new qualification.

On 2026-11-15 the initial mismatch was reproduced. Explicit `sandbox-broker-acceptance.mts --run-once --candidate-inspection --binary <verified-local-binary>` checked the candidate in disposable roots before manifest promotion; the subsequent run without candidate mode passed through the production loader. Execution writes inside the permitted root; outside/private temp writes receive `EPERM`. Discussion and Planning cannot write. Binary, lockfile and adapter drift is rejected before spawn. The initial executor rejection (`native MXC unavailable`) is retained separately from successful native execution.

This is bounded native offline evidence without provider/model calls or human acceptance. Any pinned-source change requires a new candidate receipt and production-admission rerun. [PAOS-FUNC-01](../planning/functional-remediation-2026-11-15.en.md#task-paos-func-01) owns current receipts; Requalification after F08 passed on the combined final sources; the card records the final receipts.

## Shutdown

On `quit()`, the service first rejects new requests and revokes sessions, cancels its own desktop dialog and begins HTTP server closure. Scheduler and recipes close, the selector drains, gateways/channel close. HTTP requests drain before store closure, preserving in-flight import/restore handlers. Repeated `quit` calls share one pending promise; errors permit a subsequent retry and do not prove complete shutdown.

[supervisor/lifecycle.ts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/supervisor/lifecycle.ts) is a separate supervisor contract: unknown drain requires a durable recovery receipt before child shutdown; failure returns `stop_blocked`, acknowledged drain gives `stopped`, and unknown after recording gives `stopped_recovery_required`. Do not treat the contract as proof of execution in a particular host session.

## Checks and limits

[runtime-route-selector.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-route-selector.test.mts), [runtime-adapter-shutdown.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-adapter-shutdown.test.mts), [runtime-sqlite.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-sqlite.test.mts) are related tests; links are not current test runs. Proving activation of a particular route requires authorized runtime evidence. This page does not establish isolation of arbitrary native clients or provider access.

## FUNC-G03 / F27 — durable background scans

`apps/local-service/src/project-scans/service.mts` separates project registration from the full traversal. `createProjectScans` exposes `initialized`, `status`, `start`, `cancel`, `retry` and `close`. After registry/root validation and CAS persistence, `start` returns `queued`; inventory and analyzers run in the background. HTTP/onboarding wiring and activation proof belong to the [FUNC-G03 owner](../planning/functional-remediation-2026-11-15.en.md#func-g03-results); service tests alone do not prove browser Add behavior.

Profile-owned `store_meta` namespace `project_scan_v1` stores `paos_project_scan_record_v1`: latest attempt, separate last successful/partial coverage and up to32 request digests. It is not a task/document entity or a new SQL migration. View `paos_project_scan_view_v1` carries a monotonic CAS version; `paos_project_scan_v1` binds projectId, scanId, attempt, rootIdentity, policyVersion and inventoryRevision. Replayed request IDs do not rerun work; equivalent active requests coalesce, while scope/revision conflicts are explicit. Restart changes queued/running to `interrupted`; continuation requires explicit `retry`. Unknown or malformed records never become completed and return project-specific `PROJECT_SCAN_STATE_UNAVAILABLE`.

Default stages are inventory/documents/code/analysis. The versioned contract permits schema/code_database only with explicitly supplied adapters; absent capabilities remain false. There is no automatic installation, provider/model call or fallback scanner. An analyzer failure retains other stage results and yields partial coverage. `lastSuccessful` may itself be partial and does not mean complete project analysis.

Cancel validates project/scan ownership before aborting its own controller and persisting a terminal state. An analyzer receives signal, `publicationGuard` and synchronous `canPublish`; it must check them before its own publication or external effects. The orchestrator rechecks scanId, root/policy and current inventory revision before saving stage/last results. Old, cancelled or superseded attempts cannot overwrite lastSuccessful later. Root integrates these fences into the code-index worker; an outer timeout Promise without the analyzer fence is insufficient.

Default budgets: one active scan, up to20 queued/active intents per instance,60s per job,30s per stage,256KiB per sanitized stage result; storage limits the persistent record to1MiB. These bounds do not isolate arbitrary JavaScript callback RSS: each adapter owns child/worker termination and memory limits. Shutdown interrupts only this instance's scan IDs, records interrupted and never replays work. Target sources stay read-only; bookkeeping remains outside the target.

Focused verification: `node --test tests/web/project-scans.test.mts` —12/12,0skip; `.tmp/func-g03/f27-final-focused.log`. Cases cover queued-before-completion, failed/unsupported stages, late cancellation, foreign-project cancel denial, coalescing/replay/restart/retry, source/root/policy drift, stale requested revision, external CAS supersession, timeout/result budgets, optional schema contract and a malformed current-version record. Fixtures separate the target workspace from the profile DB. A focused strict TypeScript check of service/contract passed (`.tmp/func-g03/f27-typecheck-green.log`); this is not a full Web/build/browser run. Real RED receipts remain; two initial timing oracles were corrected to observe persisted adapter progress rather than a not-yet-invoked callback.

Context7: [Node26 AbortSignal](https://github.com/nodejs/node/blob/v26.0.0/doc/api/globals.md) and [timer cancellation](https://github.com/nodejs/node/blob/v26.0.0/doc/api/timers.md). Abort listeners/timers are removed on settlement, and pre-aborted promises retain rejection handlers. Root separately owns runtime activation, current native tuple qualification, UI and human acceptance.

### F27 — persisted scan status UI

`ProjectScanStatus` consumes the authenticated scan API for the selected project. It shows latest/last successful coverage, stage progress/reasons, independent unknown counters, root/policy/revision provenance and start/cancel/retry/refresh controls. A single-flight2s poll runs only while enabled and mounted; cleanup aborts requests and clears timers. Monotonic record/attempt and project/scope guards reject late responses and prevent a terminal attempt reopening. Pure merge regressions3/3 and scoped React TypeScript passed; root owns actual mounted placement, browser proof and final source/build bindings.

## FUNC-G03 — current integration evidence

Production App/API integration is now verified: persisted asynchronous Add → Files before graph readiness → scan status → inert source preview and line deep link → structured document backlink → task. Browser foundation15/15, RU/EN × light/dark at1440/390px, Back focus, clipboard fallback, cross-project delayed response rejection, no external requests/page errors, unchanged target hashes. Clipboard and delayed delivery are explicitly synthetic boundaries. Source/build hashes and screenshots: `.tmp/func-g03/browser-foundation/evidence-q8ECT0/result.json`. Service/API integration13/13 (`.tmp/func-g03/f26-f27-api-integration.log`), backend typecheck and production frontend build passed. F18 common freshness and final group/native qualification follow; human acceptance remains separate.

## FUNC-G03 — final verification

Current integrated source, not the initial lower-module handoff: browser19/19; full Web594/594,0skip; backend TypeScript and production build passed. Source/build hashes and screenshots: `.tmp/func-g03/browser-final/evidence-IfLiEa/result.json`. Review policy-race findings are fixed and independently rechecked5/5. Native candidate and production-default receipts: `.tmp/func-g03/native-candidate-reviewed.log`, `native-default-reviewed.log`. Earlier pending/wiring statements describe their dated intermediate slice; final task reports own closure. Checkout core is available; packaged core remains explicitly unavailable. Human/provider acceptance and F14/F33/F34 are separate.

## FUNC-G04 — independent stages and read snapshots

F27 persists each scan's selected stages. Inventory is mandatory; schema/code_database can run independently of code/analysis. Coalescing binds stages and retry preserves them; recovery never auto-replays work. SQLite metadata jobs retain the native read lease until extractor completion/termination; helper loss/cancel forbids publication. Target code, migrations and SQL are not executed.

Graph status compares F28 metadata revision/root/policy without rereading every source body. Excerpts retain raw SHA256 verification. Build retains two checked raw passes,8 parallel handles and an8MiB reserved aggregate payload. The8-entry cache uses LRU and a new generation invalidates old cursors. Task/startup reads select kinds before the64MiB safety budget. History uses bounded disk-backed frozen TEMP snapshots without persistent schema migration; expiry/eviction/restart requires a new cursor. The230MiB payload and256MiB TEMP mainfile caps do not claim to bound all transient disk usage or process RSS.
