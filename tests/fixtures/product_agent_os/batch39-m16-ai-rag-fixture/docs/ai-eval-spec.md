# AI Eval Spec

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

Eval scope:

- Baseline cases: `evals/rag-eval-cases.jsonl`.
- Static report: `evals/eval-run-report.json`.
- Rubric: `docs/grounding-rubric.md`.
- Threshold: no production threshold is accepted in this fixture.
- Failure cases: prompt injection and unsupported-context examples are synthetic only.

Unsupported claims:

- This spec does not prove eval quality, model improvement, grounding, safety or release readiness.

