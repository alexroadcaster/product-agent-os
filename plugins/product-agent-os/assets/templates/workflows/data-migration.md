# Data Migration

Project: {project_name}
Profile: {profile_name}

## Inputs

- User goal:
- Migration plan:
- Database inventory:
- Database dictionary:
- Database data contract:
- Schema change:
- Backfill:
- Data quality:
- Constraints and indexes:
- Lineage:
- Query performance:
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

1. Keep the workflow read-only until migration plan, database inventory, database dictionary, database data contract, schema change, backfill scope, data quality checks, constraints and indexes, lineage, PII, sensitive fields, retention, rollback, dry run, backup, owner review, production DB boundary, and approval boundary are explicit.
2. Inventory schema sources, migrations, database dictionary, DBML, SQL files, ORM models, Liquibase, Flyway, Alembic, Prisma, Rails/Django migrations, data quality reports, lineage, runtime pipeline, RAG ingestion, query plans, dry run reports, row counts, retention notes, sensitive field notes, backup notes, rollback notes, and owner review evidence.
3. Classify each data change as schema-only, backfill, cleanup, retention change, sensitive-field change, destructive migration, production data operation, runtime pipeline impact, RAG ingestion impact, data contract change, constraint/index change, or query performance risk.
4. Record schema change, backfill, data quality, constraints, indexes, lineage, PII, sensitive fields, retention, rollback, validation, dry run, backup, database dictionary, data contract, production DB access, and owner review as `present_unverified` until migration dry run, validation evidence, database owner review, backup/restore evidence, query-plan evidence, lineage evidence or approved production evidence confirms the claim.
5. Define validation before implementation: pre-counts, post-counts, constraints, foreign keys, unique, not null, indexes, nullability checks, idempotency, duplicate handling, sampling, audit table, data drift, and rollback verification where applicable.
6. Select verification from detected project files only: migration tool dry run, SQL lint, ORM migration plan, DBML/dbdocs check, local database restore, row count comparison, backup restore check, data quality check, lineage review, query performance review, or manual DBA review.
7. Do not access production data, do not access production DB, do not run migration, and do not run destructive cleanup without explicit approval.
8. Do not store PII, sensitive fields, raw customer data, credentials, connection strings, dumps, or secret-bearing configs in artifacts, prompts, fixtures, or logs.
9. Do not claim migration safety, data quality, retention compliance, rollback readiness, database contract safety, lineage correctness, query performance, or production readiness from code inspection only.
10. No universal database tooling default: Liquibase, Flyway, Alembic, Prisma, Rails/Django, dbt, Great Expectations, OpenLineage, DBML, dbdocs, SchemaSpy and schema-diff tooling are selected only when project evidence supports them; schema-diff tooling deferred needs owner/reason.

## Outputs

- Data migration plan:
- Database inventory:
- Database dictionary:
- Database data contract:
- Schema change:
- Backfill:
- Data quality:
- Constraints and indexes:
- Lineage:
- Query performance:
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
- Schema change, backfill, data quality, constraints, indexes, lineage, data contract, PII, sensitive fields, retention, rollback, validation, dry run, backup, production DB boundary, and owner review are explicit.
- Dry run is named before implementation or marked unavailable with reason.
- Validation includes pre-counts, post-counts, constraints, foreign keys, unique, not null, indexes, idempotency, data drift, and rollback evidence where applicable.
- PII and sensitive fields are documented without storing raw private data or dumps.
- Production DB access, production data access, destructive migration, backup restore, and migration execution remain blocked until explicit approval.

## Stop Conditions

- Migration target or schema change is unknown.
- PII, sensitive fields, retention, or data ownership is unclear.
- Rollback or backup plan is missing for a destructive migration.
- Database data contract, constraints/index review, lineage review, or query performance review is missing for an affected database/data surface.
- Validation or dry run evidence is missing for a migration readiness claim.
- Owner review is missing for a production DB or sensitive-data migration.
- The request asks to access production data, access production DB, run migration, run destructive cleanup, restore backups, or change retention without explicit approval.
