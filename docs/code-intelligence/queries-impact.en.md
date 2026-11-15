# Queries, freshness and impact

Source status: repository_source / static_contract_review + FUNC-31_native_admission_PoC; 2026-11-15.

Owner: graph-cockpit-engineer + docs-maintainer. Scope: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when scanner, API, adapters, query contracts, tests or PoC status change. Graph outputs are derived orientation evidence, not substitutes for source reading and checks.

## Web graph

[service.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/service.mts) requires `revision` for graph/node/impact/source; missing or mismatched revision yields `GRAPH_REVISION_REQUIRED` / `GRAPH_REVISION_STALE`. Status separately returns fresh/stale/unavailable and coverage. Revision digests the file, parser and config manifest; the snapshot is in memory.

Graph query filters names/paths, edge types and neighbors to depth 3. Default page size is 50, maximum 100 nodes; incident edges are bounded at 100 and off-page endpoints return as contextNodes. `partial` indicates the result is not complete. An HMAC cursor binds project, revision and filters to an instance-random secret; persistence across restart is not promised.

Node impact returns directly incident edges and related tasks with `bounded_first_1000`, not a complete transitive blast radius. A source excerpt requires a fresh snapshot and checked file hash; default length is up to 2000, maximum 8000 characters with redaction. A stale source raises `GRAPH_SOURCE_STALE` instead.

## Python graph-only packets

[project_graph_queries.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_queries.py) reads graph JSON/JSONL without rereading source bodies. It supports `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `read_order`, `hotspots`, `node`, `status`, `search`, `changed_since`, `why_changed`, `agent_reading_packet`. Defaults are 25 results and 4000 tokens; maxima are 250 results, 20,000 tokens and depth 25; hub suppression and filters bound traversal. Check available CLI flags in the [scanner CLI](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/scan_project_code_graph.py).

Do not equate Python path/trace with Web immediate impact. Both surfaces have static coverage and stale-evidence limits; no result does not prove a call is absent. On drift inspect current source and select an authorized refresh; a query does not authorize target writes or provider calls.

Related tests: [Web code index](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [Python graph queries](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_queries.py), [Python overlays](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_overlays.py). These are verification routes, not claims of a new run.

## FUNC-31: codebase-memory-mcp — PoC decision

Decision on 2026-11-15: **reject for the current Windows workspace profile**. This rejects integration of the checked build in this environment; other host profiles were not assessed. [F31 and current statuses](../planning/functional-remediation-2026-11-15.en.md#task-paos-func-31) own the group result and separate UI-prototype acceptance.

Version **0.12.1**, commit `a7158ac2f48ca646b4527341b76f930f2aeff87e`. Official Windows archive SHA-256 `4e4e0f16b45233af5c757a1fcbe3c3b16e9056375b1fbe2ce020b6de75dedcc0` matched release checksums; extracted binary SHA-256 `39f6a789cd858d7428561ac5afaefb9a47b018dcba0ad6fa41ae71a45e0ed656`. Core license is MIT; supplied binary notices also list BSD and Apache-2.0. Checksum verification is not independent build attestation or redistribution approval. No installer, global MCP/skills/hooks/PATH changes, models or credentials.

### Observed admission gate

`--version`, `cli --help` and `index_repository` help completed. The first daemon-backed `cli --quiet list_projects --format json` returned exit1 and `could not load saved runtime settings`, separately in the sandbox and on an authorized executor. An additional `index_repository --repo-path` invocation with a fresh home/cache created by the engine itself returned the same rejection before indexing. No cache/runtime files appeared; hashes of synthetic originals and the allowlisted projection were preserved. Excluded `.env` and executable configuration were not passed to the engine.

Tag-pinned [runtime settings source](https://github.com/DeusData/codebase-memory-mcp/blob/v0.12.1/src/cli/runtime_settings.c) validates private cache ancestry before dispatch; [Windows IPC source](https://github.com/DeusData/codebase-memory-mcp/blob/v0.12.1/src/daemon/ipc.c) rejects mutation-granting ACLs for untrusted principals on existing ancestors. Read-only ACL observation found such grants on Desktop/workspace ancestors. Source and observations therefore point to incompatible ancestry of the current workspace: this is **source/ACL inference**, not an internal engine diagnostic trace. ACLs, sandbox and system policy were unchanged; other out-of-workspace cache roots were not tested.

[Configuration](https://github.com/DeusData/codebase-memory-mcp/blob/v0.12.1/docs/CONFIGURATION.md) distinguishes `CBM_CACHE_DIR` and `CBM_RUNTIME_DIR`; both targeted the owned disposable profile. [Bootstrap source](https://github.com/DeusData/codebase-memory-mcp/blob/v0.12.1/src/daemon/bootstrap.c) applies the runtime override to every endpoint; the Windows named-pipe namespace includes the runtime-parent hash. No default rendezvous, `daemon stop`, installer/update or user daemon was used. Source analysis preceded native commands; Context7 informed documentation, while version-sensitive conclusions were checked against tag0.12.1.

### Checked and unavailable evidence

`tests/web/poc/func-g02/codebase-memory.mts` reproduces credential-free preflight and the fresh-cache admission probe. `node --test tests/web/poc/func-g02/codebase-memory.test.mts` — **3/3**: scoped environment, native rejection versus executor failure, source-preservation hashes. `.tmp/func-g02/f31/result.json` contains12 positive integrity/rejection/preservation checks; raw receipts are `preflight-sandbox.json`, `preflight-elevated.json`, `admission-rejection.json`, `acl-observation.json`.

Index/query accuracy, precision/recall, cold/incremental scan, rename/delete/branch-like changes, cancel/retry/restart, two projects, RSS and query latency are **`not_executed_after_failed_admission`**. Their values are unknown; they are not passed or zero. The engine cache SQLite was not used as a writable PAOS API.

The versioned `paos_engine_poc_snapshot_v1` snapshot carries `coverage=unavailable`, the native-refusal reason and disabled search/definitions/references/calls/impact capabilities. Empty nodes/edges mean no measured result, not absence of files or relationships. Proposed-contract fixtures in the isolated UI must be labeled separately from actual engine output.

F14 alternative: use the qualified F30 file-dependency subset and retain existing bounded lexical JS/TS queries. Multilanguage semantic/call-path support remains an explicit design gap. Revisiting F31 requires a separately qualified host/adapter satisfying privacy, lifecycle and benchmark gates; the current reject does not authorize weaker checks.

Isolated UI acceptance: F31 unavailable controls and disabled query/export capabilities passed; a separately labelled symbol/call contract fixture exercises navigation without claiming measured CBM output. Shared browser22/22, model8/8; [FUNC-G02 closure](../planning/functional-remediation-2026-11-15.md#func-g02-results).
