# Agent context and pinning

Source status: repository_source / static_source_review; 2026-11-15.

Owner: runtime/agent owner + docs-maintainer. Scope: PAOS implementation at `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when the selector, gateway, contracts, execution boundaries or related tests change. Linked tests are verification routes, not new runs; activation and human acceptance need separate evidence.

## What the Web runtime passes

For task execution [app-agent-gateway.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-gateway.mts) loads the task profile, validates task/workflow scope and stores a job `taskContext`: task ID/revision/scopeDigest, root identity, key/title, files, acceptance criteria and risks. A job may also contain `workflowSnapshot`, `assetPins` and recipe metadata. The consumer sees this projection on claim, not unconditional access to all project data. Source files and task text remain data and must be treated as untrusted.

Preflight in [team/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/team/service.mts) resolves assigned assets/dependencies, detects cycles and missing or archived assets, and pins version/hash/content/resources. A source-managed asset is read again; total pins are limited to 8 MiB. [team assets contract](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/packages/contracts/team/assets.ts) owns types. A pin proves a saved selected snapshot, not that an agent read every resource.

## Configured, pinned, observed

| State | Evidence provided | Not established |
| --- | --- | --- |
| configured / requested | Model/effort extracted from the agent asset in team service | Actual model, effort or expenditure |
| pinned | Version/hash and resource content included in the frozen run context | Execution or outcome |
| observed | Separately recorded observation with stated coverage/source | Full host history or unsupported metrics |

The source sets `requestedModel`/`requestedEffort` where available and `observedModel`/`observedEffort` to null in pins. Team analytics marks partial coverage and unavailable duration/token/cost telemetry. Do not turn unknown into zero.

## Instruction/data boundary

For the separate coordinator route, [m1-recipe.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/m1-recipe.mts) quotes saved task context and user request as untrusted JSON, bounds saved context to 64 KiB and applies supplied redaction. This local source contract is not a guarantee against prompt injection. [persisted.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/redaction/persisted.mts) and [privacy guidance](../../product-agent-os/privacy-supply-chain-retention.md) describe persistence boundaries; examples contain no secrets. See [app-agent-gateway.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/app-agent-gateway.test.mts) and [sessions-team.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/sessions-team.test.mts); runtime/providers were not run here.
