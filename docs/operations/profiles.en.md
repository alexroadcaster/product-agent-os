# Profiles and path ownership

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: runtime/operations owner + docs-maintainer. Scope: local desktop package at `259977f3b257ba7fc0e932396f8963262bd327ad`; update when launcher, CLI, snapshot or release gates change. Test links identify verification routes, not a new run. Real profiles, credentials and providers were not examined.

[Distribution](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/distribution.mts) separates install, profile and control state; absolute local paths are checked for links, overlap and physical identity. [Profile identity](../security/auth-credentials.md) separately defines the credential namespace: copying or restoring data does not transfer it automatically. A workspace is excluded from package and backup.

Selection stores releaseId, profile and digest. First selection requires `--expected-selection none`; subsequent selection uses the current status digest. CAS prevents an unnoticed selection change. `select`, backup and restore share the launcher's profile reservation, including competing starts with another control state. A busy or unresolved profile must not be assumed free.

Restore creates a new profile and retains the old one. Workspace bindings are not rewritten; credentials and runtime auth require reconnection, approvals become stale and unfinished runs/outbox become recovery_required. [Desktop-local](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/desktop-local.test.mts) and [backup](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/storage-backup.test.mts) checks use synthetic data; preservation of a particular profile needs separate evidence. Keep real paths and secrets out of diagnostic reports.
