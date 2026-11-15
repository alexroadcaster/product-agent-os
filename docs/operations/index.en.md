# Local operations

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: runtime/operations owner + docs-maintainer. Scope: local desktop package at `259977f3b257ba7fc0e932396f8963262bd327ad`; update when launcher, CLI, snapshot or release gates change. Test links identify verification routes, not a new run. Real profiles, credentials and providers were not examined.

Start with [preparation and launch](install-start-stop.md), then consult [profiles](profiles.md), [upgrade and rollback](upgrade-rollback.md), [troubleshooting](troubleshooting.md) and [release boundaries](release-boundaries.md). [CLI](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/main.mts) and [distribution](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/distribution.mts) own executable contracts; [desktop-local tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/desktop-local.test.mts) identify a verification route.

UI build, packaging, qualification, installation, upgrade and release are distinct operations. This guide describes conditions; it neither performs them nor grants distribution rights. A historical pilot applies to its stated environment, not every new run. See [Web pilot](../web/pilot.md), [security](../security/index.md), [test map](../testing/test-map.md).
