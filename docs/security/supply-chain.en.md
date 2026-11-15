# Supply chain and release boundary

Source status: repository_source / static_source_review; 2026-11-15.

Owner: security/runtime owner + docs-maintainer. Scope: PAOS source at `259977f3b257ba7fc0e932396f8963262bd327ad`; update with guards, tests or policy changes. Linked tests are verification routes, not a new run. No real profiles, credentials or provider calls were examined.

## Sources, dependencies and authority

[Privacy/supply-chain/retention](../product-agent-os/privacy-supply-chain-retention.md) owns the scoped evidence boundary: versions, hashes and summaries may be retained within the task; vulnerability audit, complete SBOM, dependency remediation, external scanning and raw-finding retention have separate approval/retention boundaries. This page does not run an audit, install or remediate dependencies. For implementation checks use [desktop tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/desktop-local.test.mts), [connection tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/connections.test.mts) and the [test map](../testing/index.md); functional tests do not replace supply-chain review.

[plugin manifest](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/plugins/product-agent-os/.codex-plugin/plugin.json) declares `MIT` while stating that distribution readiness is not established. [commercial review history](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/research/product-agent-os-web-auth-commercial-2026-11-09.md) records historical commercial review and separate gates for ownership, route, privacy, notices/license, packaging and payer/support. Historical review does not prove those gates are closed today or establish rights to every component. Before release the owner must reconcile current sources, rights, notices and the distribution decision; do not infer commercial authority from the manifest or this page.

Related boundaries: [Codex security](../codex/security.md), [retention](data-retention.md), [security model](threat-model.md). This page grants no new external writes, provider calls or publication authority.
