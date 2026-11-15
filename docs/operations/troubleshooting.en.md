# Troubleshooting without data loss

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: runtime/operations owner + docs-maintainer. Scope: local desktop package at `259977f3b257ba7fc0e932396f8963262bd327ad`; update when launcher, CLI, snapshot or release gates change. Test links identify verification routes, not a new run. Real profiles, credentials and providers were not examined.

Start with the redacted error code, releaseId, version, time and operation description. Exclude pairing codes, credentials, profile contents and complete private logs. Identify the running instance owner and operation state before modifying files. [Launcher](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/launcher/launcher.ts), [distribution](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/distribution.mts) and [desktop tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/desktop-local.test.mts) are source and related test routes, not proof of current state.

| Symptom | Next step |
| --- | --- |
| `service_restart_required` | Normally quit the earlier owned instance, wait for confirmation and retry with the same profile. Closing the tab does not replace Stop. |
| `PROFILE_RUNNING_OR_UNRESOLVED` / `SELECTION_BUSY` | Reconcile the owner and completion of service/maintenance. Do not forcibly remove `service-instance` or `operation.lock` while state is unresolved. |
| `SELECTION_CONFLICT` | Read current status and digest, confirm intended profile, and retry selection with that digest only after reconciliation. |
| Integrity/hash/schema error | Preserve a redacted code and the original backup; inspect version, releaseId and snapshot compatibility. Do not alter manifest or database to bypass rejection. |
| Model access unconfirmed | Inspect selected route and connection state in the [LLM guide](../ai/llm/routes.md); opening App or launcher does not prove model access. |

Do not delete unknown files, profiles or reservations as routine troubleshooting. If Stop is blocked or completion ambiguous, preserve state and escalate to the owner; do not claim successful termination. For separate recovery see [backup and rollback](upgrade-rollback.md).
