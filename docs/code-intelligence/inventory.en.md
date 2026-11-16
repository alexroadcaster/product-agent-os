# Inventory and scan boundaries

Source status: repository_source / focused_synthetic_verification; 2026-11-15.

Owner: graph-cockpit-engineer + docs-maintainer. Scope: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when scanner, API, adapters, query contracts, tests or PoC status change. Graph outputs are derived orientation evidence, not substitutes for source reading and checks.

## Shared Web inventory — FUNC-28

The lower module `apps/local-service/src/project-inventory/service.mts` and `packages/contracts/project-inventory.ts` separate metadata, read eligibility and indexing eligibility. `createProjectInventory({policy, limits})` exposes `assertProject`, `inspect`, `listDirectory`, `snapshot` and `read`. Directory listing does not depend on graph state or read every source byte: nested/empty directories, configuration, binary and unknown files remain metadata within the root policy. `inspect(project, path)` checks a specific path without enumerating the full directory.

Each entry includes normalized `relativePath`, name, kind, byte size, modifiedAt, revision and `access` eligibility/reason. Entry `access.readable` and `indexable` authorize an attempt; they do not prove a completed read or analyzer. `counts.discovered`, `files`, `directories`, `readEligible`, `indexEligible`, `unsupported`, `excluded` and `error` describe different, sometimes overlapping stages. `counts.readable` and `counts.indexed` remain `null` until a consumer actually performs that work; they must not be added as independent file populations. A completed empty selection differs from partial/error and from an unknown analyzer stage.

### Policy, ignore and revisions

Precedence: hard sensitive/link/root denial → project `exclude` → project `include` → `.gitignore` and default generated/vendor exclusions. Include cannot authorize `.env`, credential/key/cloud files, `.npmrc`/`.pypirc`/`.netrc`, `auth.json` or database contents. A DB/schema metadata candidate grants no connection or migration authority. Heavy directory entries remain visible, but children are not recursively enumerated by default. Explicitly including a descendant allows metadata traversal toward it without granting other descendants read access.

Supported ignore grammar includes nested `.gitignore`, comments, escaped `#`/`!` and spaces, basename/anchored/directory patterns, `*`, `?`, ranges, globstar and negation. Child negation cannot re-include an excluded parent within ignore rules; project include is a separate higher policy layer. Git global excludes, `.git/info/exclude` and tracked state are not loaded: this is a read/index policy rather than an exact `git status` clone. POSIX named classes are explicitly unsupported; policy becomes partial and content is denied in the affected scope. An unreadable or unsafe ignore handle does not count as successfully applied policy.

`policyVersion` is stable for the algorithm/configured policy. Separate `ignoreRevision` fingerprints applied ignore data; entry revision binds root identity, metadata and ancestor ignore context. `inspect`, directory and `read(path, revision)` therefore share one pin, while file/policy/ignore changes invalidate prior pins. Snapshot revision binds the observed bounded manifest. Metadata and ignore pins are rechecked before publication; source/root/policy drift rejects the result. This is not a global filesystem lock or a live-watcher promise.

### Reads and safety

`read` separately validates ancestors, canonical containment, registered root identity, no symlink/junction/multiple hard links, the opened handle and before/after metadata. Traversal, absolute paths, ADS and Windows device/trailing-dot aliases never acquire relative authority. Display paths preserve names; pin/rule comparisons respect Windows case semantics. Binary, invalid UTF-8, oversized or unavailable files have explicit errors while other entries and valid consumer results remain usable.

Default reads reject recognized sensitive content so it cannot enter the code index. A document/control-plane display consumer may explicitly select `redactSensitive:true`: ordinary credential assignments use existing `safePersistedText`, the response marks `redacted:true`, and hash/byteSize still identify original bytes. Private-key BEGIN markers, including a truncated block without END, hard sensitive filenames, links and binary remain denied in this mode. Known-form filtering does not prove detection of every possible secret. Returned HTML is text for safe rendering, never permission to execute scripts.

### Budgets and verification

Default page100, maximum200; up to2000 direct-directory entries,10000 recursive metadata entries/1000 files, depth32 and30 seconds. Source reads are bounded to512KiB, responses1MiB, ignore data64KiB per file and4096 rules across the traversal scope. Lower limits are allowed; response budget is at least8192bytes to leave room for the envelope. Directory/manifest/response limits produce explicit partial reasons, and a cancelled snapshot never publishes success. Signed cursors bind project/root/policy/revision/path/query/filter/page size; search explicitly covers the current directory.

`node --test tests/web/project-inventory.test.mts` — **15/15 passed, 0 skipped** in the current focused run: unknown/binary metadata and empty folders, ignore/precedence, sensitive denial, inspect/read pins, Unicode/inert HTML, file/policy changes, binary/encoding/size failures, cursor isolation, limits/cancellation, actual hardlink/junction and root replacement, document-only redaction, source preservation and Windows case/device boundaries. The initial metadata RED observed missing entries; another regression corrected linked-source admission ordering before ignore reads. Existing-consumer/HTTP/UI integration is verified separately by the [FUNC-G03 owner](../planning/functional-remediation-2026-11-15.md); these15 tests do not constitute browser/native release qualification.

Context7 covered [Node26 fs](https://github.com/nodejs/node/blob/v26.0.0/doc/api/fs.md), [Node path.matchesGlob](https://github.com/nodejs/node/blob/v26.0.0/doc/api/path.md) and [official gitignore semantics](https://git-scm.com/docs/gitignore). `path.matchesGlob('*')` excludes dotfiles, so it cannot substitute for gitignore: a small position-set matcher implements the required wildcard grammar without regex backtracking or a new dependency. Rules/configs are data only; project commands are not executed and source files are unchanged.

Final lower receipt after the private-key fence: `.tmp/func-g03/f28-lower-native-key-fence-final.log`,15/15,0skip. A separate default-executor repeat had14pass/1setup EPERM creating a junction; that setup failure is neither behavioral RED nor a green suite. Its summary is preserved in `.tmp/func-g03/f28-lower-evidence.json`; the exact lower native retest exercised real link boundaries. Other group integration/browser/native gates remain root-owned.

## Historical Web source inventory

[sources.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/sources.mts) verifies registered root identity and ancestors; excludes sensitive directories/paths, symlinks and multiply hard-linked files, and checks UTF-8, drift and root containment. Traversal is bounded to depth 32, 10,000 directory entries and 1,000 eligible files. This is a bounded source inventory, not a visible tree of all files or a universal ignore-file implementation.

The graph [service.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/service.mts) limits total size to 8 MiB, one file to 512 KiB, 25,000 nodes, 50,000 edges and parser worker time to 10 seconds; up to eight snapshots. Other languages eligible for inventory receive `unsupported` coverage; linked sources can be `excluded`. A hard limit raises an error rather than guaranteeing a safe complete truncation.

## Python manifest

[project_graph_manifest.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_manifest.py) builds normalized file records, sizes, fingerprints, languages and generated flags; [project_code_graph.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_code_graph.py) uses them for the graph. Read the scanner for actual exclusion policies: Web and Python do not promise identical inventories. Generated paths may appear in the manifest without semantic overlays.

Compare revision/manifest, coverage and errors before using an index. Limits, encoding, omitted paths and drift must remain visible; results are not an audit of every project file. The pinned historical Web sources above describe the prior contract; shared-layer and dependent F26–F29 implementation belongs to FUNC-G03.

Checks: [Web source tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [manifest tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_manifest.py). This text does not claim a new runtime run.

## F28 — shared consumer integration

Graph, artifact catalog and fixed control-plane sources now reuse the lower inventory. The graph manifest includes metadata inventory/policy revision; file-size/encoding failures become explicit per-file exclusions. Artifact cursors bind root/policy/inventory revision, and stale policy cannot keep an old readable document. Profile-owned include/exclude/respectGitignore settings persist through CAS without changing immutable SQL migrations or creating task/document entities. Display-only document readers retain redacted before-images; analyzer reads cannot opt into that disclosure.

Current combined regression:57/57,0skip (`.tmp/func-g03/f28-verified-final.log`), TypeScript passed. G02 finite corpus projection was checked as a stricter subset of F28 read authority, with sensitive denial and no config execution; historical engine benchmarks were not rerun or rewritten. Prior sandbox EPERM and real RED receipts are retained.

Current addition: virtual `access(project,path)` validates policy and existing ancestors for missing create targets. A shared final registry fence invalidates captured authority after asynchronous work; metadata pins never replace raw content hashes. Full current Web594/594,0skip; independent policy-race regressions5/5.
