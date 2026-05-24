# Database & Data

Source status: `official + expert reference + vendor documentation + local implementation evidence + tool-assisted`

Источники: [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html), [PostgreSQL Backup and Restore](https://www.postgresql.org/docs/current/backup.html), [PostgreSQL Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html), [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html), [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html), [Liquibase core concepts](https://www.liquibase.org/get-started/core-usage/liquibase-core-concepts-author-database-changes), [Liquibase rollback](https://docs.liquibase.com/commands/rollback/rollback.html), [Flyway migrations](https://documentation.red-gate.com/flyway/flyway-concepts/migrations), [dbt data tests](https://docs.getdbt.com/docs/build/data-tests), [dbt model contracts](https://docs.getdbt.com/docs/mesh/govern/model-contracts), [Great Expectations](https://docs.greatexpectations.io/docs/cloud/expectations/expectations_overview/), [OpenLineage](https://openlineage.io/docs/), [NIST Privacy Framework](https://www.nist.gov/privacy-framework/using-privacy-framework-11), [Evolutionary Database Design](https://martinfowler.com/articles/evodb.html), [Prisma expand/contract pattern](https://www.prisma.io/dataguide/types/relational/expand-and-contract-pattern), [Context7 research](../sources/context7-research.md), [research dossier](../sources/methodology-research/database-data.md).

## Deep research цель

Database & Data слой описывает schema ownership, migrations, constraints, indexes, transactions, backfills, data quality, privacy classification, retention, lineage, backup/restore and production data access.

Главный принцип: data change нельзя считать завершенным, если понятен SQL или ORM diff, но не понятны production impact, rollback/compensation, backup/restore path, data quality checks, privacy boundary and performance evidence.

## Поддержанные факты

- PostgreSQL transaction isolation documentation describes Read Committed, Repeatable Read and Serializable behavior, including serialization failure retry requirements for stronger isolation levels.
- PostgreSQL constraints documentation defines integrity mechanisms such as check, not-null, unique, primary key, foreign key and exclusion constraints.
- PostgreSQL indexes and `EXPLAIN` documentation support performance review through index design and query-plan evidence. `EXPLAIN ANALYZE` executes the statement, so write statements require transaction/rollback care.
- PostgreSQL backup and restore documentation separates SQL dump and file-system-level backup approaches; production database work needs restore evidence, not only "backups exist".
- Liquibase documents changelogs as ordered changesets tracked in `DATABASECHANGELOG`, and supports rollback definitions, preconditions, contexts and labels.
- Flyway documents version-controlled migrations, versioned and repeatable migration concepts, dry-run/deployment reports and schema history.
- dbt data tests are SQL assertions that return failing rows; zero failing rows means the assertion passes. dbt model contracts define and enforce model column names and data types.
- Great Expectations defines executable Expectations for completeness, schema, uniqueness, validity, volume and custom SQL checks.
- OpenLineage defines an open standard around dataset, job and run entities for data lineage.
- NIST Privacy Framework supports privacy requirements, profiles, SDLC alignment and data-processing ecosystem risk management.
- Evolutionary Database Design describes small version-controlled migration scripts, application changes in CI/deployment pipelines and transition phases for destructive changes.
- Expand/contract migration introduces new structures in parallel, updates writes, backfills, validates, switches reads/writes and removes old structures after compatibility.

## Assumptions

- Product-Agent OS should not mandate PostgreSQL, Liquibase, Flyway, dbt, Great Expectations or OpenLineage. These provide vocabulary and candidate artifacts; actual tools come from project inventory.
- Data work is risky when it touches production data, destructive changes, sensitive fields, external consumers, analytics, AI/RAG sources, public APIs or high-volume backfills.
- Migration rollback can be reversible, compensating or irreversible. It is unsafe to call a destructive migration rollback-safe without evidence.
- Manual SQL can be operational evidence, but it cannot be the only durable record for schema/data changes.
- Production data must not appear in docs, prompts, examples, fixtures or templates.
- Data quality checks must be repeatable. Ad hoc SQL in a chat thread is not enough for a long-lived project gate.

## Инструкции применения на проекте

1. Классифицируйте работу: schema change, data migration, backfill, retention/deletion, data quality, query/index performance, analytics model, lineage, backup/restore or production data access.
2. Назовите database engine, environment, owner, data domain and schema/migration source of truth.
3. Зафиксируйте, затрагивает ли change production data, PII/sensitive fields, external consumers, analytics, AI/RAG sources or public APIs.
4. Для любого schema/backfill/retention change создайте `database-migration-plan.md` before implementation.
5. Держите migrations small, ordered, version-controlled and repeatable; manual production SQL не должен быть единственным record.
6. Для live/shared systems применяйте expand/contract или другой compatibility-preserving rollout before destructive changes.
7. Для multi-step writes/backfills опишите transaction boundary, isolation assumptions, lock impact, retry behavior and idempotency.
8. Для constraints and indexes опишите invariant/query, deployment impact and verification evidence.
9. Для performance-sensitive changes приложите query plan evidence and expected runtime/lock budget.
10. Для backfills опишите batch size, resume key, throttling, validation counts, observability and abort behavior.
11. Классифицируйте rollback как reversible, compensating or irreversible. Irreversible change требует owner acceptance.
12. Для production data заранее подтвердите backup/restore path and restore evidence.
13. Классифицируйте PII/sensitive fields до docs, prompts, fixtures and examples. Production data cannot be copied into examples.
14. Добавьте executable data quality checks для primary keys, nullability, relationships, accepted values, counts and critical business assertions.
15. Для analytics or AI/RAG pipelines опишите data contracts and lineage или explicit gap.
16. Для production data access требуйте approval, least privilege, audit trail and no-secrets/no-customer-data evidence.

## Применяемые методологии разработки

| Методология | Когда применять | Как выглядит в проекте |
| --- | --- | --- |
| Evolutionary Database Design | Product schema evolves continuously | Small versioned migrations, application changes and tests move together through CI/CD. |
| Migration-first planning | Schema, backfill or retention change | `database-migration-plan.md` exists before execution. |
| Expand/contract migration | Live systems, shared DB, public consumers, destructive changes | Add new structure, dual-write/backfill, switch reads/writes, remove old structure after compatibility window. |
| Database DevOps / migrations-as-code | Team-owned DB changes | Migrations are versioned, reviewed, repeatable and automated. |
| Data integrity by constraint | Relational correctness matters | Constraints, keys and indexes are explicit design artifacts. |
| Transaction and concurrency design | Multi-step writes, financial/accounting/state workflows | Isolation level, locks, retries and idempotency are documented. |
| Data quality gates | Critical product, analytics or AI/RAG data | Executable assertions validate keys, nulls, relationships, counts, drift and business rules. |
| Data contracts | Data model has consumers | Columns, types, semantics, compatibility and owner are explicit. |
| Privacy-by-design | PII/sensitive/regulated data | Classification, minimization, retention, deletion and access boundary are captured early. |
| Backup/restore-first change management | Production or irreversible data work | Restore path and restore drill evidence exist before risky execution. |
| Lineage-aware data operations | Analytics, reporting, ML/RAG, cross-system movement | Dataset/job/run lineage is captured or marked as a gap. |
| Performance-by-design | Indexes, heavy queries, high-volume backfills | Query plan, lock/runtime budget and index impact are reviewed. |
| Production data access control | Agent/developer touches prod data | Approval, least privilege, audit trail and no-secrets/no-customer-data policy are enforced. |

## Инструменты, артефакты и стандарты документирования

| Артефакт | Зачем нужен | Практический формат |
| --- | --- | --- |
| `database-inventory.md` | Databases, owners, environments, engines, connection boundaries and data domains. | Product-Agent OS template. |
| `database-dictionary.md` | Tables/collections, fields, types, business meaning, owner, sensitivity and retention. | DBML, dbdocs, SchemaSpy, Markdown. |
| Schema source of truth | Machine-readable schema or migration history used for review. | Migrations, DBML, ORM schema, SQL DDL. |
| `database-migration-plan.md` | Change intent, ordered steps, dry-run, validation, rollout, rollback/compensation and approvals. | Migration plan. |
| `database-expand-contract-record.md` | Parallel structures, dual-write/read switch, cleanup and compatibility window. | ADR or migration record. |
| `database-backfill-runbook.md` | Batching, idempotency, resume, throttling, progress, validation and abort behavior. | Runbook. |
| `database-rollback-feasibility.md` | Reversible, compensating or irreversible classification with owner acceptance. | Rollback record. |
| `database-backup-restore-evidence.md` | Backup source, restore drill, restore target, RPO/RTO and verification result. | DB/platform docs and runbook. |
| `database-data-classification-matrix.md` | PII/sensitive fields, legal basis, access boundary, retention and deletion behavior. | NIST Privacy Framework profile. |
| `database-data-quality-checks.md` | Executable checks for keys, nulls, relationships, accepted values, counts and drift. | dbt tests, Great Expectations, SQL checks. |
| `database-data-contract.md` | Consumer-facing data model columns, types, meaning, compatibility and owner. | dbt model contracts or Markdown. |
| `database-lineage-map.md` | Datasets, jobs, runs, sources, sinks and owners. | OpenLineage or data catalog. |
| `database-query-performance-review.md` | Query plan, index choices, cardinality, lock impact and expected runtime. | PostgreSQL `EXPLAIN`, stack-native tooling. |
| `database-retention-deletion-policy.md` | What is retained, where, how long, deletion path and audit evidence. | Privacy profile / compliance policy. |
| `database-synthetic-fixtures-policy.md` | Safe fixture generation, anonymization limits and prohibition on production secrets/data. | Project security policy. |
| `database-production-access-approval.md` | Who can access prod data, why, duration, commands and audit evidence. | Approval record. |

## Product-Agent OS routing

- `data_migration` usage mode routes schema/data changes to migration planning before implementation.
- `workspace-discovery-auditor` detects migrations, ORM schemas, SQL, dbt/GX/OpenLineage signals and production-data risk.
- `requirements-author` records data ownership, consumer impact, privacy constraints and accepted gaps.
- `implementation-planner` blocks risky data work when migration plan, rollback classification, backup/restore or validation evidence is missing.
- `test-eval-designer` selects migration dry-run, integration tests, data quality checks, query-plan checks and fixture safety checks.
- `risk-reviewer` handles PII/sensitive fields, destructive migration, production access, irreversible change and performance risk.
- `pr-release-operator` includes migration notes, restore/rollback guidance, data quality evidence and operational runbook impact.

## Candidate readiness gates

- `database_schema_source_present`: schema/migration source of truth is named.
- `database_migration_plan_present`: ordered steps, validation, rollout and owner are documented.
- `database_expand_contract_reviewed`: live/shared/destructive change has compatibility plan and cleanup window.
- `database_transaction_boundary_present`: isolation, locks, retry and idempotency are documented for multi-step writes.
- `database_backup_restore_evidence_present`: production/high-risk change has backup/restore path and restore evidence.
- `database_rollback_feasibility_present`: reversible/compensating/irreversible classification exists.
- `database_data_classification_present`: PII/sensitive fields have classification, retention and access boundary.
- `database_data_quality_contract_present`: executable quality checks or explicit gap exists.
- `database_performance_review_present`: query/index/backfill changes include plan, lock and runtime evidence.
- `database_lineage_present`: analytics or AI/RAG data movement has sources, jobs, sinks and owners.
- `database_production_access_approval_present`: production data access is approval-bound and auditable.
- `database_synthetic_fixture_policy_present`: examples/fixtures are synthetic and secret-free.

## Candidate eval fields

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
| Stack-native migration signals | `alembic.ini`, `schema.prisma`, Rails/Django migrations | Discovery signals; tool choice follows project inventory. |
| Schema documentation | DBML, dbdocs, SchemaSpy | Useful for dictionaries and relationship maps; requires secret-safe generation. |
| Data tests/contracts | dbt | Strong fit for warehouse/analytics models, data tests and model contracts. |
| Data quality | Great Expectations | Executable Expectations for data quality and multi-source comparisons. |
| Data lineage | OpenLineage | Open standard model for dataset/job/run lineage. |
| Privacy governance | NIST Privacy Framework | Useful vocabulary for privacy profiles, SDLC alignment and data-processing ecosystem roles. |
| Query performance | `EXPLAIN`, DB-native tooling | Attach evidence; avoid side-effecting analysis without transaction safety. |

## Проверки

- Migration plan exists before schema/data execution.
- Dry-run or staging migration command is named with expected output.
- Validation checks include counts and semantic business assertions.
- Backfill has batching, idempotency, resume and progress evidence.
- Rollback feasibility is explicit; irreversible risk is accepted by owner.
- Backup/restore evidence exists for production data work.
- Sensitive fields are classified and examples are synthetic.
- Query/index changes have query-plan and lock/runtime review.
- Data quality checks are executable or tooling gap is recorded.
- Production data access has approval and audit evidence.

## Failure modes

- Manual production SQL is the only record of a change.
- ORM schema and real database constraints drift silently.
- Index is added without lock/write-impact and query-plan review.
- Column is dropped or renamed before consumers move.
- Migration is called rollback-safe despite data loss.
- Backfill has no batching, idempotency or resume key.
- Validation checks count rows but miss semantic equivalence.
- `EXPLAIN ANALYZE` is run on writes without transaction/rollback control.
- Production data leaks into fixtures, prompts, examples or docs.
- Backup exists but restore was never tested.
- Data quality checks are ad hoc queries, not repeatable gates.
- Analytics or AI/RAG lineage is unknown after an incident.
- Agent receives broad production database access instead of scoped approval.

## Unsupported claims not adopted

- "ORM schema is the database source of truth." It can be one source, but real constraints, migrations and database state must not drift silently.
- "Migration applied means migration safe." Safety requires dry-run/staging, validation, rollback/compensation and owner review.
- "Rollback is just down migration." Destructive data changes may require compensation or explicit irreversible acceptance.
- "Backups exist, so restore is safe." Restore path needs evidence, not assumption.
- "Data quality can be checked manually." Long-lived product data needs repeatable checks or explicit tooling gap.
- "Anonymized production data is safe by default." Synthetic fixtures are safer; anonymization needs privacy review.
- "Analytics/RAG data lineage can be reconstructed later." Lineage gaps become expensive during incidents and deletion requests.

## Open questions for future implementation

- Which migration tool defaults should Product-Agent OS recommend by stack: Alembic, Prisma Migrate, Rails migrations, Django migrations, Liquibase, Flyway or framework-neutral?
- Should database readiness gates live only under data methodology, or also gate backend/API/LLM workflows when data changes are detected?
- Which schema-diff tools are mature enough to recommend without encouraging unsafe auto-migration behavior?
- How should Product-Agent OS detect destructive migrations from SQL/ORM diffs?
- Should the plugin ship default data-quality templates for dbt/GX, or only generic SQL checks?
- How should RAG ingestion lineage and data retention connect to database methodology and LLM methodology?
