# PR Risk Review

Project: {project_name}
Profile: {profile_name}

Use this packet for PR review and as the risk review packet for generalized two-stage review when a slice changes a public contract, migration, security-sensitive path, data migration, release packaging boundary, parallel work boundary, or external-system behavior.

## Inputs

- Diff source:
- Changed files:
- Requirements or acceptance criteria:
- Source constraints:
- Public contract:
- Migration context:
- Security-sensitive context:
- Data migration context:
- Release packaging context:
- Parallel work context:
- Missing evidence:
- Commands run:
- Observed results:
- Approvals already granted:

## Changed Files

- Changed files:
- Files reviewed:
- Files intentionally not reviewed:

## Generalized Two-Stage Review

- Stage 1: spec compliance:
  - Check acceptance criteria, source constraints, public contract, migration scope, security-sensitive boundary, data migration expectations, release packaging boundary, parallel work ownership, approvals, rollback, and compatibility.
  - Spec compliance verdict: `blocked | changes_requested | ready`
  - Spec compliance evidence:
- Stage 2: quality/risk:
  - Run only after Stage 1 is explicit.
  - Check tests, eval evidence, implementation quality, regressions, security, privacy, docs, release impact, maintainability, and unsupported claims.
  - Quality/risk verdict: `blocked | changes_requested | ready`
  - Quality/risk evidence:
- Do not collapse the stages into generic review only.
- Do not run quality/risk before spec compliance.
- Do not allow one-stage review for risky work.
- Do not return a ready verdict with missing evidence.

## Two-Stage Verdict

- Spec compliance verdict: `blocked | changes_requested | ready`
- Spec compliance evidence:
- Quality/risk verdict: `blocked | changes_requested | ready`
- Quality/risk evidence:

## Impact Map

- Behavior impact:
- API impact:
- Database impact:
- UI impact:
- Security impact:
- Docs impact:
- Release impact:

## Findings

| Severity | File or area | Evidence | Required action |
| --- | --- | --- | --- |
|  |  |  |  |

## Missing Checks

- Missing checks:
- Commands run:
- Commands still needed:
- Manual checks still needed:

## Questions And Risks

- Reviewer questions:
- Unsupported claims:
- Missing evidence:
- Approval gaps:
- External writes requested:
- PR creation requested:
- Publish actions requested:
- Residual risk:

## Boundaries

- Do not perform external writes from this review packet.
- Do not perform PR creation, push, publish, deployment, tag, package release, or production action without explicit approval.
- Do not claim readiness without current review evidence and listed command results.
- Treat generic review only, quality/risk before spec compliance, one-stage review for risky work, and ready verdict with missing evidence as blockers.
