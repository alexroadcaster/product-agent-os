# Adapters and future integrations

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: graph-cockpit-engineer + docs-maintainer. Scope: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when scanner, API, adapters, query contracts, tests or PoC status change. Graph outputs are derived orientation evidence, not substitutes for source reading and checks.

## Implemented local adapters

[project_graph_adapters.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_adapters.py) contains `python_ast`, `typescript_javascript_stdlib` and `unsupported_file`. Python AST builds package/symbol/import/call/test overlays; the limited JS/TS adapter recognizes selected export and import source patterns. Language overlays skip generated files and files larger than 1,000,000 bytes. `unresolved` preserves uncertainty, not a confirmed dependency.

Web uses a separate [parser worker](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/parser-worker.mts) and [lexical builder](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/lexical.mts); it does not invoke the Python adapter. The Python scanner has staged generated artifacts, optional local indexes and separate approval-bound extension gates. These are different contracts, stores and evidence limits.

## Planned solutions

| Initiative | Status and expected work |
| --- | --- |
| F26–F29: Files / scan / inventory / discovery | planned: independent directory, managed scan and UI/UX |
| F30 dependency-cruiser | planned JS/TS dependency-analysis PoC |
| F31 codebase-memory-mcp | planned graph/agent-navigation PoC |
| F32 tbls | planned target database-schema documentation PoC |
| F33/F34 | planned target DB map and code-to-table links, with display and evidence |

Exact acceptance, licensing and integration gates belong to the [functional plan](../planning/functional-remediation-2026-11-15.md). A project mention here does not mean installation, PoC execution, Web integration or permission to connect to a real database. After a FUNC task is performed its owner updates these pages and the source registry.

Existing AI adapter and query-quality boundaries are in [retrieval](../ai/rag/index.md). Related tests: [Web code index](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [Python graph queries](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_queries.py), [Python overlays](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_overlays.py). These are verification routes, not claims of a new run.
