# API Contract Test Matrix

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

| Check | Command | Evidence status |
| --- | --- | --- |
| OpenAPI path presence | `python scripts/fixture_smoke.py` | local static check |
| Python syntax | `python -m py_compile src/service.py scripts/fixture_smoke.py` | local static check |
| Live request behavior | none | `not_run` |

Unsupported claims:

- Static contract checks do not prove runtime request handling.

