# Model Decision Record

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

Decision boundary:

- The fixture uses a `local_stub_model` label only.
- No provider, hosted model or live model endpoint is invoked.
- Any model migration, model alias, snapshot change, latency target or cost estimate requires owner approval and eval evidence.

Unsupported claims:

- This file does not prove model quality, provider suitability, latency, cost or release readiness.

