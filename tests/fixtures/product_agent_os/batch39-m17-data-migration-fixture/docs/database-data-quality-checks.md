# Database Data Quality Checks

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

## Static Checks

- Synthetic seed rows have no raw names, emails, phone numbers or payment data.
- Row count expectations are documented in `data/quality-rules.json`.
- Runtime data quality scan is not run.

