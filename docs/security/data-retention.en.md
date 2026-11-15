# Data, redaction and retention

Source status: repository_source / static_source_review; 2026-11-15.

Owner: security/runtime owner + docs-maintainer. Scope: PAOS source at `259977f3b257ba7fc0e932396f8963262bd327ad`; update with guards, tests or policy changes. Linked tests are verification routes, not a new run. No real profiles, credentials or provider calls were examined.

## Data and evidence classes

[persisted redaction](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/redaction/persisted.mts) filters known credential forms and hidden messages in processed values. This is a limited filter, not a guarantee to detect every secret or PII; raw bytes may exist elsewhere. [project-sources](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/adapters/project-sources.ts) and [app-agent-files](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/runtime/app-agent-files.mts) have their own exclusion/redaction rules, while the broker keeps a private set of earlier secrets to handle late frames. Do not infer universal deletion or cleanup of all logs from a redacted DTO.

[snapshot](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/storage/snapshot.mts) creates a verifiable database and linked-blob backup but excludes credentials, repository files, runtime threads and runtime auth store. Rotation candidates do not mean deletion; restore and separate prune have their own conditions. See [backup/restore](../db/backup-restore.md); [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/storage-backup.test.mts) is a synthetic test route.

[Privacy/supply-chain/retention](../product-agent-os/privacy-supply-chain-retention.md) owns evidence rules: retain minimal information; raw scanner findings are not retained by default without a retention, redaction and cleanup decision. This evidence policy does not define automatic deletion periods for all user data. Backups, local DB, OS credentials and external providers have different boundaries; deletion and retention for a particular deployment require separate evidence and authority. No real profiles were inspected.
