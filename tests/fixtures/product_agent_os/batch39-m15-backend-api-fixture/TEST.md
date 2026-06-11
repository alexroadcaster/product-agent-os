# Test

Local checks:

- `python scripts/fixture_smoke.py`
- `python -m py_compile src/service.py scripts/fixture_smoke.py`

Unsupported checks:

- No live HTTP server check.
- No production dependency failure drill.
- No external integration call.
- No database migration.

