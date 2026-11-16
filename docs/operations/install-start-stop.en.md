# Prepare, start and stop

Source status: repository_source / static_contract_review; 2026-11-15.; FUNC-G06 managed delivery locally_verified_with_explicit_limits, 16.11.2026.

Owner: runtime/operations owner + docs-maintainer. Scope: local desktop package at `259977f3b257ba7fc0e932396f8963262bd327ad`; update when launcher, CLI, snapshot or release gates change. Test links identify verification routes, not a new run. Real profiles, credentials and providers were not examined.

The commands below document [desktop CLI](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/main.mts); they are not a run receipt. Paths must be absolute local paths without linked ancestors; do not place package or install under node_modules. Match host/runtime prerequisites against the manifest; do not automatically install missing components.

## FUNC-G06 / F17 — one managed-home

The new private local-pilot user-space installer reuses the portable package without a system installer or automatic runtime installation. From the package run `node apps/desktop-local/main.mts setup --home <home> --package <package> --expected-id <reviewed-id> --expected-selection none`. `managed-status --home <home>` returns selection/digest and operation phase. Update uses `update --home <home> --package <new-package> --expected-id <reviewed-id> --expected-selection <digest>`; rollback uses `rollback --home <home> --expected-id <previous-id> --expected-selection <digest> --backup <compatible-snapshot-under-home-backups>`. `managed-start --home <home>` launches the selected installation. Paths for versions/profiles/backups are derived from home.

Quit the owned service before switching. Current-profile maintenance spans snapshot, restore and selection; each target uses a new profile. Old profiles/versions/backups remain. An explicitly selected rollback snapshot defines the data cutoff: take a fresh compatible backup to retain post-update work. Mismatched host tuple/schema, stale digest, live/residual reservations and tampered artifacts reject rather than falling back. After commit, missing acknowledgement is diagnosed as selection_committed_receipt_pending. Unresolved locks need explicit inspection, not automatic deletion/replay. Low-level commands remain below.

| Action | Command from the checkout/package root containing `apps/` |
| --- | --- |
| UI build | `npm run build:web` in a checkout with agreed dependencies |
| Package | `node apps/desktop-local/main.mts pack --source <source> --output <new-package>` |
| Verify | `node apps/desktop-local/main.mts verify --package <package> --expected-id <reviewed-id>` |
| Install | `node apps/desktop-local/main.mts install --package <package> --destination <new-install> --expected-id <reviewed-id>` |
| Select | `node apps/desktop-local/main.mts select --state <control> --install <install> --expected-id <reviewed-id> --profile <profile> --expected-selection none` on first selection |
| Status / start | `node apps/desktop-local/main.mts status --state <control>`; `node apps/desktop-local/main.mts start --state <control>` |

Independently review releaseId before verify: a package self-hash does not identify its publisher. Pack/install destinations must be new; install/profile/control must not overlap. Later selections use the current digest from status instead of `none`, otherwise they conflict. After relocation the CLI is inside the installed directory. [Distribution](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/distribution.mts), [launcher](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/launcher/launcher.ts), [tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/desktop-local.test.mts).

The native launcher opens the browser and starts the local service under the selected profile. Closing the tab does not stop the backend: use **Quit** in the application and wait for the owned service to stop. Keep pairing/session material out of URLs and reports. A failed host qualification, stale service or incomplete Stop requires diagnosis, not bypassing checks. See [troubleshooting](troubleshooting.md) and the [historical pilot](../web/pilot.md).

Profile preservation means original database/blob/settings/credential-file bytes remain unchanged. Snapshot reads may create explicitly recorded empty WAL/derived SHM bookkeeping; full directory inventory identity is not claimed. Maintenance reservations coordinate managed launchers and are not an OS sandbox against arbitrary SQLite writers. [Backup contract](../db/backup-restore.en.md).
