# Synthetic Data Migration Fixture

Source status: Synthetic Batch 39 M17 fixture. This is not production database evidence.

## Rules

- Do not connect to a live database.
- Do not run migrations against any environment.
- Do not access production data, backups, dumps, credentials or connection strings.
- Treat all database/data signals as `present_unverified` until dry-run, backup/restore, integrity, owner review and approval evidence exists.

