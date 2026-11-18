# Local Web package and pilot

Settings, 2026-11-13: Choose project folder opens the native Windows Explorer folder dialog, including New folder. Add project registers the selected root and reports bounded JS/TS/source scanning; partial coverage stays visible. Cancel adds nothing. Connect Codex App opens a prepared draft: explicitly send it in Codex App, then return; only an attached worker changes connection status. Opening a window does not prove model access. Quit the previous service before rebuilding/restarting with the same profile. [Contract and current evidence](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-m1-execution-2026-11-11.md).


Source status: project-authored / PAOS-0030 local delivery contract; technical receipts belong to the owning execution report.; FUNC-G06 current contract, locally_verified_with_explicit_limits, 16.11.2026.

This package supports local engineering on the pinned Windows/x64 host tuple. It contains the launcher, service, contracts, built Web UI and bounded runtime parser. Node/Codex binaries, profiles, credentials and workspaces remain external. PAOS licensing, admission and commercial terms remain separate gates; a local build grants no external release approval.

## FUNC-G07 / F23 — product acceptance protocol, revision 1 {#func-g07-pilot-protocol}

Source status: project-authored protocol proposal, 2026-11-16; participants_not_defined; consent_not_observed; human_pilot_not_started. The owner reported that participants have not been identified. F23 is `awaiting_user_decision` (Awaiting user decision); F19/F24 technical checks do not substitute for this gate. [Tasks and current status](../planning/functional-remediation-2026-11-15.en.md#func-g07-results).

This is a concrete proposal for agreement before observation. The owner selects five participants, an observer and a data owner. P01–P05 are prospective pseudonymous slots, not completed sessions. Voluntary opt-in, scenarios, a baseline and retention must be agreed first. Owner-only exploratory feedback cannot rescale the PRD targets of4/5 and3/5. Without participants, neither a started pilot nor product acceptance is claimed.

Owner decision 2026-11-16: the user will check the result personally and provide feedback. Next action is the user’s feedback and decision. The original AC and protocol below remain a proposal for a later owner decision; this handoff does not record acceptance or completion.

### Scope and data

Proposed scope: local UI with pinned build/fixture revisions and synthetic projects, without credentials, production data or provider/model calls. Agree accessibility needs, language and device before the pilot. Record local service preparation/startup separately from task-solving time. Keep only participant IDs, timings, outcomes, assistance, errors and de-identified receipt references. Do not collect names, contacts, private task text, code, personal absolute paths, chat logs, pairing/session secrets, audio or video.

Proposed retention: manually delete detailed local records30days after the owner decision; retain only agreed de-identified aggregates. No automation/TTL is active. Specify the data owner, actual deletion date, withdrawal procedure and consent scope before collection. Do not create a human-receipt directory before opt-in. On withdrawal stop collection and perform the agreed deletion; a missing observation stays missing. Publication or transfer to an external service needs a separate decision.

### Baseline and neutral scenarios

The PRD requires the baseline **before UI**. Proposed `md_readonly` baseline: the participant’s ordinary editor/search with equivalent synthetic MD/source data, without PAOS UI. This is not an actual chat/model baseline. An interactive chat baseline needs a separately agreed route and authority. Prepare equally difficult A/B tasks to reduce memorization: P01/P03/P05 use MD-A → UI-B; P02/P04 use MD-B → UI-A. Baseline→UI order, prior familiarity and task differences remain confounders. Do not presume product advantage. Keep observer answer keys separate and avoid UI-label hints.

| Scenario | Neutral participant task | Observation |
| --- | --- | --- |
| First opening / return | “You returned after a break. Identify the current work, blocker, evidence and next action” | Correct task, blocker/next action and evidence level; unassisted time |
| Ordinary file | “Add the selected folder and find the file that needs changing” | Folder selection/cancel, tree outside Control-plane; visibility ≠ indexing ≠ execution |
| Map and data | “Find the change location for a stored field and explain your source choice” | Map → schema/table/ERD → usages → source line; confirmed/inferred/unresolved and unsupported semantics |
| Limited coverage | “Is this evidence sufficient for the next action? Explain” | Empty, excluded, unsupported and partial; no false complete-analysis conclusion |
| Conflict / stale source | “The source changed. Continue while preserving your work” | Stale revision, draft preservation and appropriate refresh/retry |
| Stop / return | “Interrupt the action and return after restarting” | Cancel/retry/restart; unknown outcome never means completed |
| Acceptance | “What can you accept from this evidence, and why?” | Check/run evidence distinct from owner acceptance; scope-aware verified interpretation |

After the timed attempt, ask about **specific past behavior**: how they previously found this information, where help was needed and which source informed the decision. Avoid product-praise questions. Do not explain the correct answer before recording an error. Keep errors after debrief; retries are new diagnostic attempts.

### Metrics and decision rules

Primary hypothesis: at least4of5 participants correctly identify the task, blocker/next action and evidence level within180seconds on their first unassisted attempt. Errors, timeouts, assistance and missing observations stay in the denominator; a retry never replaces the first attempt. Report service startup separately. Compare baseline/UI success and time on comparable scenarios; technical benchmarks are not human measurements.

Reuse hypothesis: at least3of5 **distinct** participants use the product for **another real task** within their individual `first_use_at + 14 days` window. Scheduled technical clicks or repeated fixtures do not count. Do not mark unelapsed windows complete. A de-identified receipt records distinct real work without private content; absent confirmation remains unobserved. No such observation exists currently.

Guardrails: zero false interpretations of `verified` and zero data loss. Record errors, rejections and protocol deviations alongside successes. A changed UI/build requires a new revision while preserving previous outcomes. Do not overwrite failed attempts. Changes to cohort size, scenarios or duration require a separate owner decision while preserving the original AC; they do not automatically close mandatory F23.

### Future receipt and owner decision form

Receipt fields are **unfilled**: `protocol_revision`, `build_or_release_id`, `fixture_revision`, `participant_id`, `prior_familiarity`, `consent_scope`, `consent_observed_at`, `observer_id`, `data_owner`, `baseline_mode`, `baseline_variant`, `ui_variant`, `scenario_id`, `started_at`, `elapsed_seconds`, `current_task_correct`, `blocker_next_action_correct`, `evidence_level_correct`, `assistance`, `outcome`, `misinterpretation`, `data_loss_observed`, `protocol_deviation`, `first_use_at`, `reuse_window_end`, `distinct_real_task_reuse_observed_at`, `reuse_evidence_ref`, `retention_delete_at`. `null` means unobserved, never zero, consent or success.

After consent, detailed local receipts may live in ignored `.docs-tools/reports/func-g07/human-pilot/`; canonical docs receive only agreed aggregates and the decision. Owner form: revision/build/fixture, actual cohort and consent, baseline comparison, numerator/denominator and missing data, errors/loss, actual reuse windows/evidence, `accept` / `reject` / `further_evidence_required`, owner/date. Current decision=`not_observed`, cohort=`not_defined`. Next: await the user’s own checks, feedback and decision; the original protocol is retained for that decision. This document starts no outreach, schedule or provider call.

## FUNC-G06 / F17 — managed local delivery

The current addition is a private_local_pilot managed installer using setup/update/rollback and one managed-home. The CLI derives version/profile/backup paths, validates expected release/selection identities and preserves old versions and original profile bytes. Maintenance spans the transfer; managed-start shares the home→selection lock order, so an unresolved home operation fences launch. See [installation commands](../operations/install-start-stop.en.md) and [G06 decisions/evidence](../planning/functional-remediation-2026-11-15.en.md#func-g06-results).

Qualification launches actual relocated A/B/A installations with production NativeLauncher IPC and local-service in a fresh disposable user-space environment. The window host is an injected browser callback, not an actual native-window/SmartScreen test. Real HTTP task/comment/attachment/preferences readback, installed HTML markers, distinct profile identities and an explicitly fresh rollback snapshot establish data/path activation; no checkout fallback or provider call is used. SQL session-message preservation is separately qualified by F22.

Original files retain their hashes; newly created empty WAL/derived SHM are recorded separately under the [SQLite backup contract](../db/backup-restore.en.md). This is not a new OS account/SID or commercial/public release. The original 2026-11-12 pilot below remains historical evidence, not a new run.

## Build and install

1. Run `npm run build:web` in the source workspace with already approved dependencies and Node.
2. Run `node apps/desktop-local/main.mts pack --source <absolute-source> --output <new-absolute-package>`. The new directory contains `distribution.json` with releaseId, file hashes, runtime dependencies and exact Node/OS/SQLite prerequisites. Pack does not change source, PATH or registry and does not start a server.
3. Review the build receipt and releaseId independently. Self-hashes do not establish publisher identity. Run `verify --package <package> --expected-id <reviewed-release-id>` with the same CLI. Do not treat a digest read from an untrusted package as independent approval.
4. Run `install --package <package> --destination <new-install-directory> --expected-id <reviewed-release-id>`. The destination must be new. The CLI copies the manifest inventory and verifies hashes without overwriting an existing version.
5. Create a separate empty profile. Run `select --state <control-directory> --install <install-directory> --expected-id <reviewed-release-id> --profile <profile-directory> --expected-selection none` for the first selection. Install, profile and control directories must not overlap.
6. `status --state <control-directory>` returns selection and digest. `start --state <control-directory>` validates files/prerequisites and invokes the existing native launcher. Mismatch never installs prerequisites or selects a fallback. Do not place the package below node_modules: Node refuses TypeScript source entrypoints there.

All filesystem paths are absolute and local. The installed CLI lives at `apps/desktop-local/main.mts`; the original checkout is unnecessary. The launcher opens `/launch` in the system browser immediately, without dialogs or a manual code. A one-use HttpOnly challenge and same-origin POST establish the session; URLs/stdout contain no secrets. Admission requires direct-user-navigation Fetch Metadata and does not isolate native HTTP clients. An old service reports `service_restart_required`: Quit the old instance, then launch with the same profile. Closing the tab leaves the backend running; use Quit in the app. The default browser may use an existing profile; automated checks use disposable profiles. [Contract and evidence](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-m1-execution-2026-11-11.md).

Graph support includes pinned Rolldown1.2.18, Win32/x64 binding1.2.18, pluginutils1.1.0 and oxc types0.156.0. Versions match package-lock; files/notices match the manifest. The full node_modules and build toolchain are excluded. React/React DOM/Scheduler notices live in `apps/desktop-local/THIRD_PARTY_NOTICES.txt`; parser licenses remain with its packages. Complete transitive native license review remains a release gate.

## Backup, restore and rollback

| Operation | Contract |
| --- | --- |
| backup | `backup --install <install> --expected-id <id> --profile <stopped-profile> --output <existing-backup-directory>` creates a validated SQL/referenced-blob snapshot, excluding workspace files, credentials, runtime auth/threads and profile identity |
| restore | `restore --install <target-install> --expected-id <target-id> --backup <snapshot-directory> --profile <new-profile>` checks schema, hashes, blobs and integrity/FK without replacing a profile |
| upgrade | Stop owned service → backup → restore with the new version into a fresh profile → select using current `--expected-selection <digest>` → start |
| rollback | Choose a compatible snapshot → restore with the earlier version into another fresh profile → select using current digest → start; existing versions/profiles remain |

The chosen snapshot defines the data cutoff. To retain post-upgrade changes, take a newer snapshot and verify compatibility with the earlier application. Never open the current DB with old code in place or edit schema metadata to bypass rejection.

Select/backup/restore share the launcher's atomic `profile/service-instance` reservation, including starts through another control directory. Reconcile ownership before removing reservations or operation.lock. Ambiguous shutdown needs manual inspection. Source backups and previous profiles remain; no automatic version deletion or retention occurs.

Restore changes stream generation, marks approvals stale and unfinished runs/outbox recovery_required. A new physical profile identity does not inherit credential namespaces. Only internal `_paos_profile` metadata follows the new profile directory so appearance preferences work; real workspace bindings stay unchanged. Pair again after restore. A nonempty failed restore remains for diagnosis and does not replace active selection.

## Agreed pilot and evidence limits

The owner separately selected a codex_docs copy, keeping the original read-only during the pilot. A bounded snapshot contains14real files from control-plane, UI/task/workflow/graph source and the accessibility guide. The copy receives a pilot task, comments and synthetic attachment. Checks cover PLAN reading, lexical graph, appearance preferences and data preservation through two content revisions and rollback. Original hashes are compared before/after; later authorized task control-plane updates are recorded separately.

Technical observations demonstrate those actions and checked data. They do not establish broad usability, all-project usefulness, model quality, human product acceptance or production readiness. Those remain hypotheses pending owner evaluation. This pilot needs no provider call or real secret. AUTH-G1–G6 are rechecked, with unresolved commercial/license/account/privacy/support gates continuing to block the corresponding release.

Repository-root evidence: `research/product-agent-os-web-m4-0030-execution-2026-11-12.md`, companion results JSON and `docs/release/web-m4-local-release.json`. Preserve failure code, releaseId and a redacted receipt when reporting incidents; omit pairing codes and credentials. The workspace maintainer owns local incident handling; no commercial SLA/support commitment is made. See [Web accessibility](accessibility.md) and [runtime boundaries](../diagrams/runtime-decision-map.md).
