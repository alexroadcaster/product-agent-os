# Tools, approvals and Stop

Source status: repository_source / static_source_review; 2026-11-15.

Owner: runtime/agent owner + docs-maintainer. Scope: PAOS implementation at `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when the selector, gateway, contracts, execution boundaries or related tests change. Linked tests are verification routes, not new runs; activation and human acceptance need separate evidence.

## Browser and private channel

[application.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/http/application.mts) handles browser API with session/origin/CSRF. [app-agent-channel.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-channel.mts) separately accepts POST on the loopback origin using an instance capability and host/origin, content-type and size checks. A browser cookie does not authorize attach/claim/report; capability and lease tokens must not be put into URLs, docs or reports. This boundary reduces authority mixing but does not prove isolation of arbitrary native clients.

## Mediated command

In [app-agent-gateway.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-gateway.mts), a worker in an execution job proposes an operation with ID, digest, generation, expiry and awaiting_approval state. Approve checks run/binding/generation, lifetime, state, ownership and task/autonomy boundaries. Repeating the same decision returns the existing state; a conflicting decision is rejected. On accept the lease is rechecked before dispatch through [sandbox-broker.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/sandbox-broker.mts); decline/cancel do not launch the command. See [API endpoints](../../api/endpoints.md) for action-level contracts.

The broker scope is PAOS-mediated commands; the App host's own tools are not automatically constrained by this broker. hostIdentity is attested, not cryptographic. Broker execution/output and file observations have their own coverage; proposal, approval and completion are distinct. [policy.ts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/web/src/api/policy.ts) is UI preflight; service validation remains authoritative.

## Stop and uncertainty

Stop may mark a queued job interrupted; an active job becomes cancel_requested and cooperative interruption is requested. Completion requires a corresponding observation. In recovery_required an unknown native operation is not replayed; `cancel_undispatched` is available only when absence of dispatch and current worker/generation ownership are established. [app-agent-gateway.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/app-agent-gateway.test.mts), [app-agent-channel.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/app-agent-channel.test.mts), [recipe-recovery.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/recipe-recovery.test.mts) are test routes, not a new execution. See [backend recovery](../../backend/recovery.md).
