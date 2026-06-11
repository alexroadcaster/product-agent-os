# Retrieval Tool Contract

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

Tool boundary:

- The retrieval tool reads only the local synthetic corpus.
- The tool has no write path.
- The tool has no network path.
- Human approval is required before connecting any live tool, provider, vector store or external corpus.

Unsupported claims:

- This document does not prove tool safety or runtime behavior.

