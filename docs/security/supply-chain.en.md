# Supply chain and release boundary

Source status: repository_source / static_source_review; 2026-11-15.; FUNC-G05 locally_verified_with_explicit_limits, 16.11.2026.

Owner: security/runtime owner + docs-maintainer. Scope: PAOS source at `259977f3b257ba7fc0e932396f8963262bd327ad`; update with guards, tests or policy changes. Linked tests are verification routes, not a new run. No real profiles, credentials or provider calls were examined.

## Sources, dependencies and authority

[Privacy/supply-chain/retention](../product-agent-os/privacy-supply-chain-retention.md) owns the scoped evidence boundary: versions, hashes and summaries may be retained within the task; vulnerability audit, complete SBOM, dependency remediation, external scanning and raw-finding retention have separate approval/retention boundaries. This page does not run an audit, install or remediate dependencies. For implementation checks use [desktop tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/desktop-local.test.mts), [connection tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/connections.test.mts) and the [test map](../testing/index.md); functional tests do not replace supply-chain review.

[plugin manifest](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/plugins/product-agent-os/.codex-plugin/plugin.json) declares `MIT` while stating that distribution readiness is not established. [commercial review history](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/research/product-agent-os-web-auth-commercial-2026-11-09.md) records historical commercial review and separate gates for ownership, route, privacy, notices/license, packaging and payer/support. Historical review does not prove those gates are closed today or establish rights to every component. Before release the owner must reconcile current sources, rights, notices and the distribution decision; do not infer commercial authority from the manifest or this page.

Related boundaries: [Codex security](../codex/security.md), [retention](data-retention.md), [security model](threat-model.md). This page grants no new external writes, provider calls or publication authority.

## FUNC-G05 — implemented contracts

F12 external search requires explicit opt-in. The only current adapter is openai/plugins, package superpowers, pinned commit d420d13051bffe4543ed39e30fa46b87148e47dd. The deprecated openai/skills repository is not used. Fixed anonymous GET requests use credentials=omit without query/project text, redirects/auth fallback/install/hooks; failures preserve the local catalog. Git blob SHA1, raw SHA256, actual MIT LICENSE, manifest, truncated trees, mode/path and byte/count/deadline budgets are checked. Import includes the selected SKILL.md, allowed local text companions and exact agents/openai.yaml as opaque UTF-8 metadata; executable/binary/out-of-scope dependencies are rejected. Provenance, revision, hashes and LICENSE.source.txt accompany the project managed copy. Preview followed by explicit Apply does not activate native assets or raise instruction trust. [Checked upstream](https://github.com/openai/plugins/tree/d420d13051bffe4543ed39e30fa46b87148e47dd/plugins/superpowers).

Current focused evidence and remaining qualification: [FUNC-G05](../planning/functional-remediation-2026-11-15.en.md#func-g05-results).
