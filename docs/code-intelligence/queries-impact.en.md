# Queries, freshness and impact

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: graph-cockpit-engineer + docs-maintainer. Scope: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when scanner, API, adapters, query contracts, tests or PoC status change. Graph outputs are derived orientation evidence, not substitutes for source reading and checks.

## Web graph

[service.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/service.mts) requires `revision` for graph/node/impact/source; missing or mismatched revision yields `GRAPH_REVISION_REQUIRED` / `GRAPH_REVISION_STALE`. Status separately returns fresh/stale/unavailable and coverage. Revision digests the file, parser and config manifest; the snapshot is in memory.

Graph query filters names/paths, edge types and neighbors to depth 3. Default page size is 50, maximum 100 nodes; incident edges are bounded at 100 and off-page endpoints return as contextNodes. `partial` indicates the result is not complete. An HMAC cursor binds project, revision and filters to an instance-random secret; persistence across restart is not promised.

Node impact returns directly incident edges and related tasks with `bounded_first_1000`, not a complete transitive blast radius. A source excerpt requires a fresh snapshot and checked file hash; default length is up to 2000, maximum 8000 characters with redaction. A stale source raises `GRAPH_SOURCE_STALE` instead.

## Python graph-only packets

[project_graph_queries.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_queries.py) reads graph JSON/JSONL without rereading source bodies. It supports `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `read_order`, `hotspots`, `node`, `status`, `search`, `changed_since`, `why_changed`, `agent_reading_packet`. Defaults are 25 results and 4000 tokens; maxima are 250 results, 20,000 tokens and depth 25; hub suppression and filters bound traversal. Check available CLI flags in the [scanner CLI](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/scan_project_code_graph.py).

Do not equate Python path/trace with Web immediate impact. Both surfaces have static coverage and stale-evidence limits; no result does not prove a call is absent. On drift inspect current source and select an authorized refresh; a query does not authorize target writes or provider calls.

Related tests: [Web code index](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [Python graph queries](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_queries.py), [Python overlays](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_overlays.py). These are verification routes, not claims of a new run.
