# AI Behavior Spec

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

Behavior promise:

- Answer only from retrieved local snippets.
- Cite local snippet identifiers.
- Return `insufficient_context` for unsupported questions.
- Return a structured object that matches `structured-output/answer-schema.json`.

Unsupported claims:

- The fixture does not prove answer quality, safety, grounding or production behavior.

