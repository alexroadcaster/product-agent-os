# Adapters and future integrations

Source status: repository_source / bounded_f33_backend_native_verified + static_contract_review_and_synthetic_poc; 2026-11-15.; FUNC-G04: locally_verified_with_measured_limits, 16.11.2026.

Owner: graph-cockpit-engineer + docs-maintainer. Scope: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when scanner, API, adapters, query contracts, tests or PoC status change. Graph outputs are derived orientation evidence, not substitutes for source reading and checks.

## Implemented local adapters

[project_graph_adapters.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_adapters.py) contains `python_ast`, `typescript_javascript_stdlib` and `unsupported_file`. Python AST builds package/symbol/import/call/test overlays; the limited JS/TS adapter recognizes selected export and import source patterns. Language overlays skip generated files and files larger than 1,000,000 bytes. `unresolved` preserves uncertainty, not a confirmed dependency.

Web uses a separate [parser worker](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/parser-worker.mts) and [lexical builder](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/lexical.mts); it does not invoke the Python adapter. The Python scanner has staged generated artifacts, optional local indexes and separate approval-bound extension gates. These are different contracts, stores and evidence limits.

## PoC decisions and future integrations

| Initiative | Status and expected work |
| --- | --- |
| F26–F29: Files / scan / inventory / discovery | planned: independent directory, managed scan and UI/UX |
| F30 dependency-cruiser | implemented research: bounded_adopt, imports only; production F14 planned |
| F31 codebase-memory-mcp | implemented research: reject on current Windows profile; unavailable before index |
| F32 tbls | implemented research: reject authoritative SQLite metadata; explicit Node alternative selected for F33 |
| F33/F34 | planned target DB map and code-to-table links, with display and evidence |

Exact acceptance, licensing and integration gates belong to the [functional plan](../planning/functional-remediation-2026-11-15.md). A project mention here does not mean installation, PoC execution, Web integration or permission to connect to a real database. After a FUNC task is performed its owner updates these pages and the source registry.

Existing AI adapter and query-quality boundaries are in [retrieval](../ai/rag/index.md). Related tests: [Web code index](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [Python graph queries](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_queries.py), [Python overlays](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_overlays.py). These are verification routes, not claims of a new run.

## FUNC-30 — bounded import-only PoC, locally verified

The current checkout tests dependency-cruiser18.6.0 (commit59606f7133843b190aa328c95d5c676631ca45f1), MIT, on Node26.5.0/Windows10.0.26200x64. An isolated copy uses cached TypeScript5.9.2 (Apache-2.0); this cruiser version does not support application TypeScript7, which is unchanged. The44-package license roster contains MIT/ISC/Apache-2.0; version/lock/package/compiler hashes are retained in the tool audit.

Shared synthetic corpus:10/10 expected import edges, precision1/recall1; current lexical parser7/10, precision1/recall0.7 (alias/dynamic/CommonJS gaps). Incoming-lib/alias/cycle tasks:3/3 versus baseline2/3. Median of three cold-process runs:817.39ms versus218.27ms; RSS about140–143MiB versus104–105MiB. Additional200files:961.49ms,146.33MiB,142302bytes. This is a small synthetic benchmark, not measured human productivity or production-monorepo performance.

Final PoC decision: **bounded_adopt for file imports**, with no call/definition/multilanguage/index-daemon claim. The adapter retains root identity, source revision, path/line, import direction, unresolved and unknown type-only classification. An import is not a call. Source/config/secret exclusions use an allowlisted projection; explicit no-config and trusted tsconfig data, while the Node measurement process denies writes and network. Original hashes are preserved; rename/parse-error/timeout/retry cases are checked. The baseline uses the existing parser Worker separately from the new engine. Normalization regressions4/4;17engine scenarios executed.

Artifacts: `tests/web/poc/func-g02/f30-run.mts`, `f30-model.mts`, `tests/fixtures/func_g02/protocol.json`, `corpus.json`; results `.tmp/func-g02/f30/result.json`, `snapshot.json`, `tool-audit.json`. Context7 [CLI no-config](https://github.com/sverweij/dependency-cruiser/blob/v18.6.0/doc/cli.md) and [pre-compilation semantics](https://github.com/sverweij/dependency-cruiser/blob/v18.6.0/doc/options-reference.md) checked against installed source. Isolated V3 UI passed the shared22-browser matrix and source/build provenance check; production integration belongs to F14. Research task closure does not activate the adapter in PAOS. [FUNC-G02 closure](../planning/functional-remediation-2026-11-15.md#func-g02-results).

## F33: production backend for the selected SQLite metadata adapter

The current local implementation is in `apps/local-service/src/database-map/`; it transfers verified F32 `sqlite_metadata_v2_effective_nullable` semantics into a production module without importing the PoC runner. tbls remains rejected. The backend requires explicit registration of an offline SQLite file within the registry root; source candidates remain metadata and never open a database automatically. No external DB connections, ORM/migration execution or whole-DB copy were added.

The new F28 `admitDatabaseSource` capability independently applies policy/ignore/hard denial and checks only the100-byte SQLite header. Generic `database_content` denial is unchanged. A Windows native lease closes the path-open race: the selected file and root-to-file directories are held without write/delete sharing; final paths, volume/file IDs and Node root/policy/stat are rechecked before SQLite starts. Existing writers, sidecars or WAL header2 are rejected. Unsupported hosts/lease refusals report explicit unavailable, without automatic fallback. A trusted constructor path/identity guard excludes the PAOS profile DB.

An owned Node child uses fixed metadata SQL and the SQLite authorizer; user rows, ATTACH, DDL, target scripts and extensions are denied. Views/virtual tables report partial without expansion. Composite FK, implicit PK ordinal resolution, generated columns, effective nullable and index direction are retained; raw DDL/default literals are excluded. Child deadline5s/output512KiB, lease15s; source128MiB,200tables/4096columns/1024FK/4096index parts. JS heap/watchdog limits are not native RSS limits.

The F27 `schema` analyzer returns compact `snapshotRevision` and source provenance; two schema snapshots are stored through profile CAS. The public service offers status, explicit select/clear, snapshot/filter/page/scoped Mermaid and compatible changes. Stale metadata is available only within a compatible root/policy/source envelope and does not substitute fresh source bytes. Revoke/cancel/selection CAS fences late publication. Focused native evidence is in `.tmp/func-g04/f33/focused-native-final.log`; production UI/browser and F34 code-to-table acceptance remain separate stages. [ERD and limits](../db/erd.md).
