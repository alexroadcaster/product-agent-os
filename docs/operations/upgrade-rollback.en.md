# Backup, upgrade and rollback

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: runtime/operations owner + docs-maintainer. Scope: local desktop package at `259977f3b257ba7fc0e932396f8963262bd327ad`; update when launcher, CLI, snapshot or release gates change. Test links identify verification routes, not a new run. Real profiles, credentials and providers were not examined.

First stop the owned service normally and confirm the owned launcher outcome; CLI status reports selection and digest, not whether the service stopped. [CLI](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/main.mts) defines two separate operations:

- `node apps/desktop-local/main.mts backup --install <install> --expected-id <reviewed-id> --profile <stopped-profile> --output <existing-backup-directory>` creates a verifiable SQL and referenced-blob snapshot.
- `node apps/desktop-local/main.mts restore --install <target-install> --expected-id <target-id> --backup <snapshot> --profile <new-profile>` validates the snapshot and restores only to a new profile.

For upgrade: backup → verify target package → install it to a new target directory (or use an already verified target install) → restore with that target version into a new profile → select using the current `--expected-selection <digest>` → start. For rollback choose a compatible snapshot and restore with the earlier version into another new profile, then select using the current digest. Do not open the current database in-place with older code or bypass schema/hash failures. A snapshot represents its own point in time: later changes may be absent.

Backup excludes project files, credentials, runtime auth and threads; restore requires reconnection. Earlier versions, profiles and source backup are preserved; a nonempty failed new profile remains for reconciliation. There is no automatic retention/deletion. [Storage contract](../db/backup-restore.md), [distribution](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/distribution.mts), [tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/storage-backup.test.mts). Historical tests do not prove recovery of specific user data.
