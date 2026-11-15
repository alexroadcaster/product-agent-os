# Prepare, start and stop

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: runtime/operations owner + docs-maintainer. Scope: local desktop package at `259977f3b257ba7fc0e932396f8963262bd327ad`; update when launcher, CLI, snapshot or release gates change. Test links identify verification routes, not a new run. Real profiles, credentials and providers were not examined.

The commands below document [desktop CLI](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/main.mts); they are not a run receipt. Paths must be absolute local paths without linked ancestors; do not place package or install under node_modules. Match host/runtime prerequisites against the manifest; do not automatically install missing components.

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
