# ADR Template

Source status: `local methodology artifact`

Project: {project_name}

Use this artifact for `adr_for_architecture_decision`, `tradeoff_record_for_high_impact_decision`, `migration_rollback_path_present`, and `accepted_gap_recorded`.

## Title

ADR-0000: Decision title

## Status

Proposed | Accepted | Superseded | Rejected | `not_applicable` | `explicit_gap_accepted`

## Standards Trigger Policy

- Gate: `standards_trigger_policy`.
- ADR trigger policy: create or propose an ADR/MADR for architecture boundary, API contract, storage, auth/security, irreversible migration, automation activation, public contract, runtime topology, or high-cost technology decisions.
- Not applicable status: use `not_applicable` only when the slice has no significant decision and record the reason.
- Accepted gap: use `explicit_gap_accepted` only with owner, reason, residual risk, and follow-up condition.

## Context

- What problem or constraint forced a decision?
- Which stakeholders, quality attributes, risks, and source facts matter?
- Which alternatives were considered?
- Architecture boundary affected:
- Public contract affected:
- Data ownership or trust boundary affected:

## Options And Tradeoff

| Option | Benefit | Cost/risk | Security/privacy impact | Runtime/operations impact | Decision |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Decision

- Chosen option:
- Public contract or architecture boundary affected:
- Files, services, data stores, APIs, or workflows affected:
- Owner:
- Review owner:

## Consequences

- Positive consequences:
- Negative consequences:
- Operational, security, privacy, performance, cost, reliability or migration risks:
- Documentation and test impact:
- Residual risk:

## Verification

- Commands or checks:
- Evidence location:
- Owner review:
- Current command evidence:
- Current eval evidence:
- Current runtime evidence:

## Rollback

- Reversal path:
- Data or migration rollback:
- Dependent artifacts to update:
- No-rollback rationale:

## Accepted Gap

- Gap:
- Owner:
- Reason:
- Scope:
- Review date:
- Downstream risk:
- Follow-up condition:

## Safety

- No secrets, credentials, private customer data, raw private chat logs, connection strings or unpublished roadmap details stored in this artifact:
