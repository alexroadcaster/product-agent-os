# Search, retrieval and RAG boundaries

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: retrieval/graph owner + docs-maintainer. Scope: DG05, revision `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when index, filters, budgets, provenance or eval contract changes. Test links do not claim a new run.

## Three distinct paths

| Path | Source and purpose | Boundary |
| --- | --- | --- |
| Web SQLite | [SQLite worker](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/storage/sqlite-worker.mts), [search SQL](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/storage/search-queries.mts) — FTS5 search over PAOS entities | Not semantic project-tree retrieval; [DB search](../../db/search-index.md) owns details |
| Python graph | [semantic](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py), [hybrid](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_hybrid_retrieval.py) — generated graph/index packets and deterministic ranking | Orientation evidence, not source truth or production RAG |
| External providers | [embedding gate](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_embedding_provider.py), [reranker gate](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_reranker_provider.py) — approval-bound gates/evals | A gate makes no call itself; live invocation requires separate authorization |

[Corpus](corpus-and-indexing.md), [retrieval](retrieval.md), [freshness](freshness-and-provenance.md), [quality](evaluation.md), [code intelligence](../../code-intelligence/index.md). End-to-end Web RAG is not established; Python cache/gates do not connect to Web automatically. M5 PostgreSQL/pgvector and F30–F34 are planned in the [plan](../../planning/functional-remediation-2026-11-15.md). A partial/stale result cannot prove a file absent. [semantic tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_semantic.py), [provider tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_embedding_provider.py), [quality tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_search_quality.py) identify verification routes.
