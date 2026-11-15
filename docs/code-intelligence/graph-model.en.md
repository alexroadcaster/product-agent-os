# Graph models and coverage

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: graph-cockpit-engineer + docs-maintainer. Scope: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when scanner, API, adapters, query contracts, tests or PoC status change. Graph outputs are derived orientation evidence, not substitutes for source reading and checks.

## Matrix

| Surface | Languages / nodes | Edges and limits |
| --- | --- | --- |
| Web local service | JS/JSX/TS/TSX, including mjs/cjs/mts/cts; file, symbol, unresolved | lexical `define`, `read`, `write`, `reference`, `call`, `import`; imports/aliases and dynamic/member calls are not resolved runtime dependencies |
| Python plugin | file-level graph; Python AST package/module/class/function/method; limited JS/TS stdlib adapter | Python import/call/test edges, JS/TS source-pattern overlay; dynamic calls and unrecognized links remain uncertain/unresolved |
| Python contract overlays | Markdown and supported documentation/API/schema/diagram formats | Contract references and observations do not prove the entire runtime schema or API |

Web [lexical.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/lexical.mts) performs two lexical-scope passes without type resolution or a module linker; [parser-worker.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/parser-worker.mts) owns parser behavior and statuses. Web marks other recognized extensions `unsupported`, not analyzed.

[project_graph_adapters.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_adapters.py) implements Python AST and a limited JS/TS adapter; [project_graph_ontology.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_ontology.py) owns types and confidence. Static edges are observations: wiring, dynamic dispatch, runtime aliases and actual function execution require separate checks.

See [Web API](../api/endpoints.md), [Python contract](../product-agent-os/graph-intelligence-contract.md) and [adapters](adapters.md).

Related tests: [Web code index](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [Python graph queries](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_queries.py), [Python overlays](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_overlays.py). These are verification routes, not claims of a new run.
