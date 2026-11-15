# Corpus и индексация

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: retrieval/graph owner + docs-maintainer. Scope: DG05, revision `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении индекса, фильтров, бюджетов, provenance или eval contract. Ссылки на тесты не означают нового прогона.

## Web SQLite

[SQLite worker](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/storage/sqlite-worker.mts) индексирует допустимые типы сущностей проекта; текст более 1 MiB исключается. FTS5 хранит title/body, unicode61 и prefix 2/3; [search SQL](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/storage/search-queries.mts) фильтрует project, deleted и актуальную revision через join. Exact ID/public key и точный relative document path предшествуют FTS. Подробности — [DB guide](../../db/search-index.md). Это не полное файловое дерево или live target DB introspection.

## Python graph

[chunking](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_chunking.py) строит структурные overlay-узлы из manifest: Markdown headings/diagrams, PlantUML, OpenAPI/AsyncAPI, SQL/DBML, top-level JSON/YAML keys. Кандидаты свыше 1 000 000 bytes и нечитаемые файлы пропускаются; до 100 узлов на файл, truncation/omitted count фиксируются. Это anchors/spans с fingerprint, не полная semantic-нарезка.

[semantic](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py) формирует по graph node записи из редактированных labels, IDs, paths, static terms и observation IDs; raw source bodies и generated HTML исключены. Terms ограничены 80, текст записи приблизительно ограничен одобренным max_corpus_record_tokens (default 120); vector — локальное SHA-256 token hashing, default dimension 64. Индекс требует валидного approval packet; эта документация не подразумевает его выполнение. [semantic tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_semantic.py), [quality tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_search_quality.py).
