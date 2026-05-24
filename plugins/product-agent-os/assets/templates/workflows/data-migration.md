# Data Migration

Project: {project_name}
Profile: {profile_name}

## Inputs

- User goal:
- Migration plan:
- Database dictionary:
- Schema change:
- Backfill:
- Data quality:
- PII:
- Sensitive fields:
- Retention:
- Validation:
- Dry run:
- Backup:
- Rollback:
- Production DB:
- Owner review:
- Approval boundary:

## Process

1. Keep the workflow read-only until migration plan, database dictionary, schema change, backfill scope, data quality checks, PII, sensitive fields, retention, rollback, dry run, backup, owner review, production DB boundary, and approval boundary are explicit.
2. Inventory schema sources, migrations, database dictionary, DBML, SQL files, ORM models, data quality reports, dry run reports, row counts, retention notes, sensitive field notes, backup notes, rollback notes, and owner review evidence.
3. Classify each data change as schema-only, backfill, cleanup, retention change, sensitive-field change, destructive migration, or production data operation.
4. Record schema change, backfill, data quality, PII, sensitive fields, retention, rollback, validation, dry run, backup, database dictionary, production DB access, and owner review as `present_unverified` until migration dry run, validation evidence, database owner review, or approved production evidence confirms the claim.
5. Define validation before implementation: pre-counts, post-counts, constraints, nullability checks, idempotency, duplicate handling, sampling, audit table, and rollback verification where applicable.
6. Select verification from detected project files only: migration tool dry run, SQL lint, ORM migration plan, DBML/dbdocs check, local database restore, row count comparison, backup restore check, or manual DBA review.
7. Do not access production data, do not access production DB, do not run migration, and do not run destructive cleanup without explicit approval.
8. Do not store PII, sensitive fields, raw customer data, credentials, connection strings, dumps, or secret-bearing configs in artifacts, prompts, fixtures, or logs.
9. Do not claim migration safety, data quality, retention compliance, rollback readiness, or production readiness from code inspection only.

## Outputs

- Data migration plan:
- Database dictionary:
- Schema change:
- Backfill:
- Data quality:
- PII:
- Sensitive fields:
- Retention:
- Validation:
- Dry run:
- Backup:
- Rollback:
- Production DB boundary:
- Owner review:
- Approval requirements:
- Residual risk:

## Verification

- Migration plan and database dictionary are present or marked `applicable_missing`.
- Schema change, backfill, data quality, PII, sensitive fields, retention, rollback, validation, dry run, backup, production DB boundary, and owner review are explicit.
- Dry run is named before implementation or marked unavailable with reason.
- Validation includes pre-counts, post-counts, constraints, idempotency, and rollback evidence where applicable.
- PII and sensitive fields are documented without storing raw private data or dumps.
- Production DB access, production data access, destructive migration, backup restore, and migration execution remain blocked until explicit approval.

## Stop Conditions

- Migration target or schema change is unknown.
- PII, sensitive fields, retention, or data ownership is unclear.
- Rollback or backup plan is missing for a destructive migration.
- Validation or dry run evidence is missing for a migration readiness claim.
- Owner review is missing for a production DB or sensitive-data migration.
- The request asks to access production data, access production DB, run migration, run destructive cleanup, restore backups, or change retention without explicit approval.
