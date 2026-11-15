# Project discovery and graphs

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: graph-cockpit-engineer + docs-maintainer. Scope: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when scanner, API, adapters, query contracts, tests or PoC status change. Graph outputs are derived orientation evidence, not substitutes for source reading and checks.

## Choose the path

| Question | Current owner and output |
| --- | --- |
| What did first-run analysis find? | [Discovery](discovery.md): Python analysis and evidence |
| Which files are included and why is coverage incomplete? | [Inventory](inventory.md): separate Web and Python rules |
| Which nodes and edges exist? | [Graph model](graph-model.md): Web lexical and Python overlays |
| How can I find a path and possible impact? | [Queries and impact](queries-impact.md): cursor/revision and bounded packets |
| Which adapters and future PoCs exist? | [Adapters](adapters.md): current implementation and F26–F34 queue |

## Two separate paths

The Web local service calls its own JS/TS code index; HTTP and UI are owned by [API](../api/endpoints.md) and [frontend](../frontend/navigation.md). The Python plugin constructs a separate file graph and overlays through CLI, stage and query packets. Current source does not establish automatic transfer or merging of Web snapshots and the Python graph.

[Project Code Graph](../product-agent-os/project-code-graph.md) and [Graph intelligence contract](../product-agent-os/graph-intelligence-contract.md) retain ownership of the Python graph and evidence boundary. [Retrieval](../ai/rag/index.md) separately covers search and semantic cache. A `partial`, `stale`, `unresolved` or `unsupported` graph does not establish absence of a dependency.

## Next action

Use the graph as a pointer, then inspect current source and related tests; affected tests are candidates, not proof of sufficient coverage. A full file tree, managed scan, target DB map and code-to-table links, and PoC engines remain in the [functional plan](../planning/functional-remediation-2026-11-15.md), F26–F34.

Related tests: [Web code index](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [Python graph queries](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_queries.py), [Python overlays](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_overlays.py). These are verification routes, not claims of a new run.
