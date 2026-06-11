# RAG Retrieval Config

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

Retrieval settings:

- Chunking: one JSONL record per chunk.
- Ranking: deterministic keyword overlap.
- Top-k: 2.
- Embeddings: not run.
- Vector database: not used.

Unsupported claims:

- This configuration does not prove retrieval quality or production performance.

