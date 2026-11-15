# Backend: local-service lifecycle

Source status: repository_source / static_source_review + bounded_native_synthetic_verified; 2026-11-15.

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
