# Corpus and indexing

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: retrieval/graph owner + docs-maintainer. Scope: DG05, revision `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when index, filters, budgets, provenance or eval contract changes. Test links do not claim a new run.

## Web SQLite

[SQLite worker](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/storage/sqlite-worker.mts) indexes eligible project entity kinds; text larger than 1 MiB is excluded. FTS5 stores title/body, unicode61 and prefix 2/3; [search SQL](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/storage/search-queries.mts) filters project, deleted and current revision through its join. Exact ID/public key and exact relative document path precede FTS. See [DB guide](../../db/search-index.md). This is not a complete file tree or live target DB introspection.

## Python graph

[chunking](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_chunking.py) builds structural overlay nodes from the manifest: Markdown headings/diagrams, PlantUML, OpenAPI/AsyncAPI, SQL/DBML and top-level JSON/YAML keys. Candidates over 1,000,000 bytes and unreadable files are skipped; up to 100 nodes per file, with truncation/omitted count recorded. These are anchors/spans with fingerprints, not full semantic text chunking.

[semantic](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py) derives records per graph node from redacted labels, IDs, paths, static terms and observation IDs; raw source bodies and generated HTML are excluded. Terms are limited to 80, record text approximately to approved max_corpus_record_tokens (default 120); vectors use local SHA-256 token hashing, default dimension 64. The index requires a valid approval packet; this documentation does not imply execution. [semantic tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_semantic.py), [quality tests](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_search_quality.py).
