# Database Migration Plan Template

Project: {project_name}

## Scope

- Schema source:
- Migration tool:
- Liquibase notes:
- Flyway notes:
- Alembic notes:
- Prisma notes:
- Rails/Django notes:
- No universal default rationale:
- Schema-diff tooling deferred owner/reason:

## Change Classification

- Expand-contract:
- Transaction boundary:
- Destructive change:
- DROP/rename/truncate/cleanup/purge:
- Backfill:
- Retention/deletion:
- Production data impact:

## Plan

| Step | Direction | Preconditions | Databasechangelog/schema history | Versioned/repeatable | Rollback or compensation | Owner |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Approval Boundary

- Do not run migration without approval.
- Do not access production data without approval.
- Destructive migration approval_required:
- Backup/restore approval_required:

## Verification

- Dry run command:
- Row count/checksum:
- Constraints/index checks:
- Owner review:
- Accepted gap:
