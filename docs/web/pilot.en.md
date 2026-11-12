# Local Web package and pilot

Source status: project-authored / PAOS-0030 local delivery contract; technical receipts belong to the owning execution report.

This package supports local engineering on the pinned Windows/x64 host tuple. It contains the launcher, service, contracts, built Web UI and bounded runtime parser. Node/Codex binaries, profiles, credentials and workspaces remain external. PAOS licensing, admission and commercial terms remain separate gates; a local build grants no external release approval.

## Build and install

1. Run `npm run build:web` in the source workspace with already approved dependencies and Node.
2. Run `node apps/desktop-local/main.mts pack --source <absolute-source> --output <new-absolute-package>`. The new directory contains `distribution.json` with releaseId, file hashes, runtime dependencies and exact Node/OS/SQLite prerequisites. Pack does not change source, PATH or registry and does not start a server.
3. Review the build receipt and releaseId independently. Self-hashes do not establish publisher identity. Run `verify --package <package> --expected-id <reviewed-release-id>` with the same CLI. Do not treat a digest read from an untrusted package as independent approval.
4. Run `install --package <package> --destination <new-install-directory> --expected-id <reviewed-release-id>`. The destination must be new. The CLI copies the manifest inventory and verifies hashes without overwriting an existing version.
5. Create a separate empty profile. Run `select --state <control-directory> --install <install-directory> --expected-id <reviewed-release-id> --profile <profile-directory> --expected-selection none` for the first selection. Install, profile and control directories must not overlap.
6. `status --state <control-directory>` returns selection and digest. `start --state <control-directory>` validates files/prerequisites and invokes the existing native launcher. Mismatch never installs prerequisites or selects a fallback. Do not place the package below node_modules: Node refuses TypeScript source entrypoints there.

All filesystem paths are absolute and local. The installed CLI lives at `apps/desktop-local/main.mts`; the original checkout is unnecessary. Pairing reaches the native window through IPC/stdin, never URL/stdout. Cancel shuts down the owned service. Normal OK opens the local UI in the system browser and may use its existing profile; automated checks use disposable browser profiles.

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
