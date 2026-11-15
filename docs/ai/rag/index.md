# Поиск, retrieval и границы RAG

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: retrieval/graph owner + docs-maintainer. Scope: DG05, revision `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении индекса, фильтров, бюджетов, provenance или eval contract. Ссылки на тесты не означают нового прогона.

## Три отдельные ветки

| Ветка | Источник и назначение | Граница |
| --- | --- | --- |
| Web SQLite | [SQLite worker](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/storage/sqlite-worker.mts), [search SQL](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/storage/search-queries.mts) — FTS5 поиск сущностей PAOS | Не semantic retrieval по дереву; детали принадлежат [DB search](../../db/search-index.md) |
| Python graph | [semantic](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py), [hybrid](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_hybrid_retrieval.py) — generated graph/index packets и deterministic ranking | Ориентир, не source truth и не production RAG |
| External providers | [embedding gate](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_embedding_provider.py), [reranker gate](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_reranker_provider.py) — approval-bound gates/evals | Gate сам не делает вызов; live invocation требует отдельной авторизации |

[Corpus](corpus-and-indexing.md), [retrieval](retrieval.md), [freshness](freshness-and-provenance.md), [quality](evaluation.md), [code intelligence](../../code-intelligence/index.md). Подтверждённого end-to-end Web RAG нет; Python cache/gates не подключаются к Web автоматически. M5 PostgreSQL/pgvector и F30–F34 — planned в [плане](../../planning/functional-remediation-2026-11-15.md). Partial/stale результат не доказывает отсутствие файла. [semantic tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_semantic.py), [provider tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_embedding_provider.py), [quality tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_search_quality.py) — маршруты проверок.
