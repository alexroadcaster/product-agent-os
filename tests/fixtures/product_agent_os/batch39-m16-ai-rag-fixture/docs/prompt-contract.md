# Prompt Contract

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

Prompt contract:

- Prompt source: `prompts/answer-policy.md`.
- Inputs: user question and retrieved snippets.
- Outputs: structured answer, citations, confidence and unsupported marker.
- The prompt must not rely on private memory, external data or hidden tools.

Unsupported claims:

- Prompt text presence does not prove reliable model behavior.

