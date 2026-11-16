# Filesystem and root identity

Source status: repository_source / static_source_review + FUNC-10_inspector_focused_verified; API_gateway_UI_locally_verified; 2026-11-15.

Owner: security/runtime owner + docs-maintainer. Scope: PAOS source at `259977f3b257ba7fc0e932396f8963262bd327ad`; update with guards, tests or policy changes. Linked tests are verification routes, not a new run. No real profiles, credentials or provider calls were examined.

## Registration and reads

[project-sources](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/adapters/project-sources.ts) accepts a local absolute path and binds the canonical root to directory identity (device/inode); before reading fixed control-plane files it rechecks the binding, regular file, absence of symbolic and hard links, 1 MiB limit, open handle identity, and changes during the read. The digest represents raw bytes while displayed text can be redacted. This is a bounded reader, not a complete project explorer.

[app-agent-files](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/runtime/app-agent-files.mts) observes pinned task files only: at most 32 files, 64 KiB each and 512 KiB total. It excludes private paths, links and binary/private-key content, checks path and handle and rebinds the root; the diff is bounded and redacted. Failure or excluded means no permitted observation, not proof that nothing changed.

[profile identity](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/connections/profile-identity.mts) separately checks profile directory identity and credential-store namespace. Admission checking is not an atomic filesystem lock. Changes require [project source tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/project-sources.test.mts), [file tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/app-agent-files.test.mts), [profile tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/profile-identity.test.mts), and the relevant user-surface check; these links do not mean those tests ran now. No real project was scanned here; the full file directory and future integrations are planned, not established by this reader.

## FUNC-G03 / F28 — shared inventory boundary

Current F28 implementation replaces the separate listing/read/index source policy with a common checked inventory. Metadata visibility grants no content, indexing or execution permission. Hard sensitive names, linked paths, canonical aliases, root drift and private-key BEGIN markers remain denied; configured include cannot reopen them. Ordinary document credential assignments may be displayed only through explicit redaction, retaining the raw-byte hash; code analyzers reject those contents. Fixed control-plane display reads now share the bounded512KiB read policy.

Root/policy/ignore/file revisions bind pages and reads; changing policy invalidates graph and artifact cursors. Durable policy CAS stays in the PAOS profile, with no target writes or schema-migration change. At F28 closure, synthetic source/consumer checks57/57 included actual Windows hardlink/junction cases; this is not human acceptance, a real-project audit or complete secret detection. [Inventory contract](../code-intelligence/inventory.en.md).

## FUNC-10 — shared execution file preflight

Current `preflightTaskFiles(project, files)` in `apps/local-service/src/runtime/app-agent-files.mts` reuses the F28 root/policy/read boundary. Public `paos_file_preflight_v1` returns metadata only: allowed, limits/counts, per-path operation/state/reason, observed raw SHA256 and metadata pins, rootIdentity/policyVersion, digest and selected-scope revision. Neither source text nor diffs enter the report. Binary/encoding/hash validation internally reads only bounded selected-file bytes; this does not send the project to a model.

Execution limits are unchanged: **32 paths,65536 raw bytes per file,524288 raw bytes total**. UTF-8 character counts do not replace byte counts. Rename includes source/destination and consumes two slots. Count overflow prevents content checks; `not_checked` is absence of observation rather than a successful read. `counts.totalBytes` sums known raw sizes, and `bytesComplete=false` marks incomplete knowledge; an excluded path's unknown size is not a proven zero.

| Planned operation | Admission condition |
| --- | --- |
| `create` | Destination is absent, virtual path is policy-allowed and existing ancestors checked. An existing target is a conflict. |
| `read`, `modify`, `delete` | Require an existing regular readable source within limits. Missing source blocks dispatch. |
| `rename` | Old source exists/is permitted; new destination is absent/is permitted. Both paths are checked. |
| `create_or_modify_after_discovery` | Explicitly permits existing or missing targets under the same policy/root/budget checks. |
| `null` / omitted | Compatible read/observe meaning; it does not implicitly authorize creating a missing file. |

New metadata-only lower seam `inventory.access(project,path)` applies ancestor ignore/project policy to a missing create target without opening that missing file or creating parents. Existing ancestors/root and applied ignore pins are revalidated; a previously missing parent appearing during inspection causes drift. Sensitive paths, symlink/junction/hardlink, binary/private-key contents, invalid UTF-8 and unreliable revisions block admission with distinct reasons. Include cannot override hard denial; an ignored missing `*.log` is not permitted merely because it does not exist yet.

Optional file `revision` compares raw-byte SHA256, and `fileRevision` separately compares metadata/policy pins. The scope digest excludes observation time and is stable for unchanged inputs; `inventoryRevision` covers selected task paths rather than a full project scan. Task expectedRevision/CAS, actual gateway/native dispatch and rechecking immediately before the side effect remain root integration work. A positive report does not itself start a run, grant sandbox approval or eliminate TOCTOU through an atomic filesystem lock.

`captureTaskFiles` retains observational before/after semantics through the same checked inspector. A target created by planned create may be present afterward; planned operations and old source pins do not forbid observing the actual after-state. Rename appears as an observed delete of the old path and add of the new path. Excluded sources produce no fake diffs and do not prove that nothing changed; compact diffs stay bounded/redacted, with raw-byte hashes. Ordinary credential assignments are redacted for diff display; private-key BEGIN remains denied without END. Native broker ownership must cover both rename paths independently of UI visibility.

Current focused evidence: `node --test tests/web/file-preflight.test.mts tests/web/app-agent-files.test.mts` — **13/13 native,0skip**, `.tmp/func-g03/f10-inspector-final-native.log`; targeted inspector/transitive-lower TypeScript — exit0. Cases cover32/33,65536/65537,524288/524289, create/missing/rename, stale pins, source preservation, no-content reports and real link/root boundaries. The new lower-access test has observed RED/GREEN. A separate combined29-case default run had26pass/3junction setupEPERM, retained as `.tmp/func-g03/f10-focused-sandbox.log`; exactly3 boundary cases were rerun native,3/3,0skip in `f10-link-boundary-native-retest.log`. This is not claimed as one green sandbox run. Gateway/API/browser and current native-runtime qualification remain root [FUNC-G03](../planning/functional-remediation-2026-11-15.md) work. Node26 fs/checked-handle semantics were previously checked through Context7; this focused slice added no dependencies or actual project execution.

## FUNC-G03 — final registry authority

A captured project/policy is not assumed current after asynchronous I/O. Task preflight atomically rereads task and registry at completion; native dispatch compares scope after dependency/autonomy waits. Task references, Files, artifact body/cursor previews, direct graph rebuild/source, control-plane HTTP and requirement grounding use a shared final registry fence. Policy revocation during a read cannot return plaintext or replace the prior graph. Independent review reproduced the race as RED; cycle2 verified5/5 fixed regressions, closed_allowed.

API/gateway/production UI integration is complete: blocked preflight preserves the draft and never calls runtime Send. Final browser19/19 (`.tmp/func-g03/browser-final/evidence-IfLiEa/result.json`); full Web594/594,0skip. Native tuple64cd3b58… passed candidate and production-default offline write/deny/drift/interrupt checks; executable source pins now include the Python bridge. This does not establish provider or human acceptance.
