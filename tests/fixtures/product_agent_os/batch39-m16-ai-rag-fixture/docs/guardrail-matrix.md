# Guardrail Matrix

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

| Risk | Fixture guardrail | Evidence status |
| --- | --- | --- |
| Prompt injection | `guardrails/prompt-injection-cases.jsonl` | `present_unverified` |
| Data leakage | synthetic-only corpus | `present_unverified` |
| Tool misuse | local read-only retrieval tool | `present_unverified` |
| Hallucination | grounding rubric | `present_unverified` |

Unsupported claims:

- Guardrail presence does not prove safety or red-team success.

