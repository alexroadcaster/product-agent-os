# PR Review Readiness

Project: {project_name}
Profile: {profile_name}

## Inputs

- Diff source:
- Changed files map:
- Base branch or comparison point:
- Requirements or acceptance criteria:
- Commands run and observed results:
- Review evidence already available:
- Known approval boundary:

## Process

1. Confirm the diff source and changed files map before judging behavior.
2. Run a two-stage review:
   - Spec compliance verdict: compare the change with requirements, acceptance criteria, source constraints, public contracts, and user-visible behavior.
   - Quality/risk verdict: review implementation quality, tests or evals, security, data handling, migrations, docs, release impact, and rollback.
3. Map impact by area:
   - Behavior impact:
   - API impact:
   - Database impact:
   - UI impact:
   - Security impact:
   - Docs impact:
   - Release impact:
4. Record missing checks with exact commands or manual checks that are still needed.
5. Keep review evidence separate from assumptions and unsupported claims.
6. Do not create a PR, do not push, do not publish, and do not perform external writes during review. Any external action requires explicit approval.

## Outputs

- Changed files map:
- Spec compliance verdict:
- Quality/risk verdict:
- Findings by severity:
- Missing checks:
- Reviewer questions:
- Review evidence:
- Approval requirements:
- Residual risk:

## Verification

- Every finding cites a file, changed area, command result, or explicit evidence gap.
- Spec compliance verdict appears before quality/risk verdict.
- Missing checks name the command or manual check needed.
- External writes, PR creation, push, publish, deployment, and release actions remain out of scope unless explicitly approved.

## Stop Conditions

- Diff source or changed files map is unavailable.
- Requirements or acceptance criteria are absent for behavior-changing work.
- Verification evidence is missing for risky API, database, security, UI, or release changes.
- The request asks for PR creation, push, publish, deployment, or external writes without explicit approval.
