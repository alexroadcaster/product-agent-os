# Database Synthetic Fixtures Policy

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

## Policy

- Fixtures must not contain credentials, connection strings, production dumps, raw customer records or unredacted PII.
- Fixture identifiers use `synthetic_` prefixes.
- Smoke checks validate static files only.

