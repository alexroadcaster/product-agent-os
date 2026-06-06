# Database & Data Methodology Research

Source status: `official + expert reference + vendor documentation + tool-assisted`

Research date: `2026-05-24`

Target methodology page: [../../methodologies/database-data.md](../../methodologies/database-data.md)

Target Product-Agent OS behavior: detect database and data work early, require schema ownership, migration safety, privacy classification, backup/restore evidence, data quality gates, performance review and rollback/compensation evidence before production-impacting data changes.

## Scope

This dossier covers relational database schemas, migrations, constraints, indexes, query plans, backfills, data quality checks, analytical model contracts, privacy classification, retention, lineage, backup/restore and production data access.

It does not mandate PostgreSQL, Liquibase, Flyway, dbt, Great Expectations or OpenLineage for every project. These sources provide vocabulary and candidate artifacts; the actual stack must be selected from the project inventory.

## Supported facts

- PostgreSQL official documentation treats the current documentation as PostgreSQL 18 at the time of this research run. Its transaction isolation documentation describes Read Committed, Repeatable Read and Serializable behavior, and explicitly notes serialization failure retry requirements for stronger isolation levels.
- PostgreSQL constraints documentation defines integrity mechanisms such as check, not-null, unique, primary key, foreign key and exclusion constraints. Database integrity should not be documented only as application prose when database-level constraints are appropriate.
- PostgreSQL indexes documentation and `EXPLAIN` documentation support performance review through index design and query plan evidence. `EXPLAIN ANALYZE` executes the statement, so write statements require transaction/rollback care during analysis.
- PostgreSQL backup and restore documentation separates SQL dump and file-system-level backup approaches. Production database work needs backup/restore evidence rather than only a statement that backups exist.
- Liquibase documents a changelog as an ordered list of changesets and tracks executed changesets in the `DATABASECHANGELOG` table. It also supports rollback definitions, preconditions, contexts and labels.
- Flyway documents migrations as version-controlled SQL scripts for incremental schema/data changes, with versioned, repeatable, baseline and undo migration concepts. It also documents dry-run/deployment reports and schema history.
- dbt data tests are SQL assertions that return failing rows; zero failing rows means the assertion passes. dbt also documents model contracts as a way to define and enforce model column names and data types for supported materializations.
- Great Expectations defines Expectations as verifiable assertions about data, including completeness, schema, uniqueness, validity and volume checks, plus custom SQL expectations and multi-source comparisons.
- OpenLineage defines an open standard for lineage metadata around dataset, job and run entities. It is useful when data products, analytics or AI/RAG pipelines need traceability.
- NIST Privacy Framework 1.1 guidance supports privacy requirements, profiles, SDLC alignment and data-processing ecosystem risk management. Database methodology should treat sensitive data as a lifecycle and governance concern, not a late release checklist.
- Fowler and Sadalage's Evolutionary Database Design describes putting migration scripts and application changes in version control, running them through CI/deployment pipelines and making database changes small. It also highlights transition phases for destructive changes.
- The expand/contract pattern documents a multi-step migration approach: introduce new structures in parallel, update writes, backfill, validate, switch reads/writes, then remove old structures. This is vendor documentation from Prisma and should be treated as a practical pattern reference, not a universal standard.

## Methodologies

| Methodology | When to apply | Project-level behavior |
| --- | --- | --- |
| Evolutionary database design | Product evolves continuously | Schema/data changes are small, versioned, automated and tested with application changes. |
| Migration-first planning | Any schema, backfill or retention change | `database-migration-plan.md` exists before execution. |
| Expand/contract migration | Live systems, shared DB, public consumers | Add new structure in parallel, dual-write/backfill, switch reads/writes, then remove old structure. |
| Database DevOps / migrations-as-code | Team-owned database changes | Migrations live in version control and run through repeatable tooling and CI/CD gates. |
| Data integrity by constraint | Relational data needs correctness guarantees | Constraints and indexes are designed explicitly, not inferred only from ORM models. |
| Transaction and concurrency design | Multi-step writes, financial/accounting/state workflows | Isolation level, locks, retry behavior and idempotency are documented. |
| Data quality gates | Business-critical, analytical or AI/RAG source data | Executable tests/assertions validate uniqueness, nullability, accepted values, counts and drift. |
| Data contracts | Data models consumed by other teams/systems | Column names, data types, semantics, owner and compatibility rules are explicit. |
| Privacy-by-design | PII, sensitive data, regulated data, retention changes | Classification, minimization, retention, deletion and access controls are documented early. |
| Backup/restore-first change management | Production data, irreversible or high-risk migration | Restore path is known and periodically tested before risky execution. |
| Lineage-aware data operations | Analytics, reporting, ML/RAG, cross-system movement | Dataset/job/run lineage is captured or the gap is explicit. |
| Performance-by-design | New indexes, heavy queries, high-volume backfills | Query plans, index impact, lock impact and runtime budgets are reviewed. |
| Production data access control | Any agent or developer touches prod data | Approval, least privilege, audit trail and no-secrets/no-customer-data policy are enforced. |

## Documentation artifacts and standards

| Artifact | Purpose | Candidate source/tool |
| --- | --- | --- |
| Database inventory | Databases, owners, environments, engines, connection boundaries and data domains. | `database-inventory.md` |
| Database dictionary | Tables/collections, fields, types, business meaning, owner, sensitivity and retention. | DBML, dbdocs, SchemaSpy, Markdown |
| Schema source of truth | Machine-readable schema or migration history used for review. | Migrations, DBML, ORM schema, SQL DDL |
| Migration plan | Change intent, migration steps, backfill, validation, rollback/compensation and approvals. | `database-migration-plan.md` |
| Expand/contract record | Parallel structures, dual-write/read switch, cleanup and compatibility window. | ADR or migration record |
| Backfill runbook | Batching, idempotency, resume, throttling, progress, validation and abort behavior. | `database-backfill-runbook.md` |
| Rollback feasibility record | Reversible, compensating or irreversible classification with owner acceptance. | `database-rollback-feasibility.md` |
| Backup/restore evidence | Backup source, restore drill, restore target, RPO/RTO and verification result. | DB/platform docs and runbook |
| Data classification matrix | PII/sensitive fields, legal basis, access boundary, retention and deletion behavior. | NIST Privacy Framework profile |
| Data quality check suite | Executable checks for keys, nulls, relationships, accepted values, counts and drift. | dbt tests, Great Expectations, SQL checks |
| Data contract | Consumer-facing data model columns, types, meaning, compatibility and owner. | dbt model contracts or Markdown |
| Lineage map | Datasets, jobs, runs, sources, sinks and owners. | OpenLineage or data catalog |
| Query performance review | Query plan, index choices, cardinality, lock impact and expected runtime. | PostgreSQL `EXPLAIN`, stack-native tooling |
| Retention/deletion policy | What is retained, where, how long, deletion path and audit evidence. | Privacy profile / compliance policy |
| Synthetic fixtures policy | Safe fixture generation, anonymization limits and prohibition on production secrets/data. | Project security policy |
| Production data access approval | Who can access prod data, why, duration, commands and audit evidence. | Approval record |

## Project application instructions

1. Classify the work: schema change, data migration, backfill, retention/deletion, data quality, query/index performance, analytics model, lineage, backup/restore or production data access.
2. Identify the database engine, environment, owner, data domain and source of truth for schema/migrations.
3. Record whether the change affects production data, sensitive fields, external consumers, analytics, AI/RAG sources or public APIs.
4. Create a migration plan before implementation for any schema, backfill or retention change.
5. Prefer small, ordered, version-controlled migrations. Avoid hidden manual SQL as the only record of a change.
6. For live/shared systems, use expand/contract or another compatibility-preserving strategy before destructive changes.
7. Define transaction boundary, isolation assumptions, lock impact, retry policy and idempotency for multi-step writes or backfills.
8. For constraints and indexes, document why they are needed, which queries or invariants they protect and what deployment impact they may have.
9. For performance-sensitive changes, attach query-plan evidence and expected runtime/lock budget.
10. For backfills, document batch size, resume key, throttling, validation counts, observability and abort behavior.
11. Classify rollback as reversible, compensating or irreversible. Do not call a destructive migration rollback-safe without evidence.
12. For production data, document backup/restore path and restore evidence before execution.
13. Classify PII/sensitive fields before writing docs, fixtures, examples or prompts. Never copy production data into examples.
14. Add data quality checks for primary keys, nullability, relationships, accepted values, counts and business-critical assertions.
15. For analytical or AI/RAG pipelines, document data contracts and lineage or explicitly record the gap.
16. Require approval and audit evidence before an agent or developer performs production data access or external data writes.

## Product-Agent OS candidate rules

### Discovery signals

- Directories: `db/`, `database/`, `migrations/`, `schema/`, `sql/`, `seeds/`, `fixtures/`, `analytics/`, `models/`, `warehouse/`, `etl/`, `elt/`, `pipelines/`
- Files: `schema.sql`, `structure.sql`, `*.dbml`, `schema.prisma`, `alembic.ini`, `liquibase.*`, `flyway.conf`, `dbt_project.yml`, `profiles.yml`, `great_expectations.yml`
- Terms: migration, schema, backfill, retention, delete data, PII, sensitive field, index, constraint, transaction, isolation, rollback, backup, restore, lineage, data quality, data contract, production data
- Runtime signals: database clients, ORM models, migration tools, data warehouse jobs, scheduled data pipelines, RAG ingestion, reporting tables

### Readiness gates

| Gate | Trigger | Block condition |
| --- | --- | --- |
| `database_schema_source_present` | Any schema/data change | No named schema or migration source of truth. |
| `database_migration_plan_present` | Schema, backfill, retention or destructive change | No steps, validation, owner, environment or rollout plan. |
| `database_expand_contract_reviewed` | Live/shared/destructive schema change | No compatibility plan or cleanup window. |
| `database_transaction_boundary_present` | Multi-step write, backfill, financial/state workflow | Isolation, retry, lock or idempotency behavior is missing. |
| `database_backup_restore_evidence_present` | Production/high-risk/irreversible data change | No backup/restore path or restore drill evidence. |
| `database_rollback_feasibility_present` | Any migration plan | Reversible/compensating/irreversible classification is missing. |
| `database_data_classification_present` | PII/sensitive/regulated data | Classification, retention, deletion or access boundary is missing. |
| `database_data_quality_contract_present` | Critical data, analytics, AI/RAG source | No executable quality checks or explicit gap. |
| `database_performance_review_present` | Index, heavy query, high-volume backfill | No query-plan, runtime or lock-impact evidence. |
| `database_lineage_present` | Analytics, ML/RAG, cross-system data movement | Sources, jobs, sinks or owners are unknown. |
| `database_production_access_approval_present` | Agent/developer prod data access | No approval, least-privilege scope or audit evidence. |
| `database_synthetic_fixture_policy_present` | Fixtures/examples/docs use realistic data | No proof that data is synthetic or safely anonymized. |

### Candidate templates

- `database-inventory.md`
- `database-dictionary.md`
- `database-migration-plan.md`
- `database-expand-contract-record.md`
- `database-backfill-runbook.md`
- `database-rollback-feasibility.md`
- `database-backup-restore-evidence.md`
- `database-data-classification-matrix.md`
- `database-data-quality-checks.md`
- `database-data-contract.md`
- `database-lineage-map.md`
- `database-query-performance-review.md`
- `database-retention-deletion-policy.md`
- `database-synthetic-fixtures-policy.md`
- `database-production-access-approval.md`

### Candidate eval fields

- Database engine, owner and environment are named.
- Schema/migration source of truth is linked.
- Migration plan has ordered steps, dry-run and validation commands.
- Backfill plan includes batching, idempotency, resume and progress evidence.
- Rollback feasibility is classified as reversible, compensating or irreversible.
- Backup/restore evidence exists for production or high-risk changes.
- PII/sensitive fields are classified and examples are synthetic.
- Data quality checks are executable or the tooling gap is explicit.
- Query/index changes include plan evidence and lock/runtime notes.
- Data lineage is documented for analytics or AI/RAG data movement.
- Production data access is approval-bound and auditable.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| Relational source reference | PostgreSQL docs | Useful for transaction, constraint, index, query-plan and backup vocabulary. |
| Migration management | Liquibase | Changelog/changeset model, rollback, preconditions, contexts and labels. |
| Migration management | Flyway | Versioned/repeatable migrations, schema history, dry-run reports and validation. |
| Schema documentation | DBML, dbdocs, SchemaSpy | Useful for dictionaries and relationship maps; requires secret-safe generation. |
| Data tests/contracts | dbt | Strong fit for warehouse/analytics models, data tests and model contracts. |
| Data quality | Great Expectations | Executable Expectations for data quality and multi-source comparisons. |
| Data lineage | OpenLineage | Open standard model for dataset/job/run lineage. |
| Privacy governance | NIST Privacy Framework | Useful vocabulary for privacy profiles, SDLC alignment and data processing ecosystem roles. |
| Query performance | `EXPLAIN`, DB-native tooling | Attach evidence; avoid running side-effecting analysis without transaction safety. |

## Типовые сбои

- Running a migration manually in production with no committed migration artifact.
- Treating ORM model changes as sufficient schema documentation while DB constraints differ.
- Adding an index without lock/write-impact and query-plan review.
- Dropping/renaming a column before consumers have moved.
- Calling a migration reversible when data loss makes rollback impossible.
- Backfill has no batching, idempotency, resume key or progress evidence.
- Validation checks only row count and misses semantic equivalence.
- `EXPLAIN ANALYZE` is run on writes without transaction/rollback control.
- Production data appears in fixtures, prompts, examples or documentation.
- Backup exists but restore has never been tested.
- Data quality checks are informal queries, not repeatable gates.
- Lineage for analytics or AI/RAG data is reconstructed manually after incidents.
- Agent receives broad production database access instead of scoped approval.

## Open questions for deeper research

- Which migration tool defaults should Product-Agent OS recommend by stack: Alembic, Prisma Migrate, Rails migrations, Django migrations, Liquibase, Flyway or framework-neutral?
- Should database readiness gates live under data methodology only, or also gate backend/API/LLM workflows when data changes are detected?
- Which schema-diff tools are mature enough to recommend without creating unsafe auto-migration behavior?
- How should Product-Agent OS detect destructive migrations from SQL/ORM diffs?
- Should the plugin ship default data-quality templates for dbt/GX, or only generic SQL checks?
- How should RAG ingestion lineage and data retention be connected to database methodology and LLM methodology?

## Sources

- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL Backup and Restore](https://www.postgresql.org/docs/current/backup.html)
- [PostgreSQL Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)
- [Liquibase core concepts](https://www.liquibase.org/get-started/core-usage/liquibase-core-concepts-author-database-changes)
- [Liquibase rollback](https://docs.liquibase.com/commands/rollback/rollback.html)
- [Flyway migrations](https://documentation.red-gate.com/flyway/flyway-concepts/migrations)
- [dbt data tests](https://docs.getdbt.com/docs/build/data-tests)
- [dbt model contracts](https://docs.getdbt.com/docs/mesh/govern/model-contracts)
- [Great Expectations Expectations overview](https://docs.greatexpectations.io/docs/cloud/expectations/expectations_overview/)
- [OpenLineage documentation](https://openlineage.io/docs/)
- [NIST Privacy Framework 1.1 usage guidance](https://www.nist.gov/privacy-framework/using-privacy-framework-11)
- [Martin Fowler: Evolutionary Database Design](https://martinfowler.com/articles/evodb.html)
- [Prisma Data Guide: expand and contract pattern](https://www.prisma.io/dataguide/types/relational/expand-and-contract-pattern)
- [Context7 research](../context7-research.md)
