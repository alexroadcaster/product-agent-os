# Build Slice

Source status: project-local system workflow.

## Purpose

Implement the smallest useful change in the existing project without rewriting unrelated systems.

## Inputs

- Slice:
- Acceptance behavior:
- Existing pattern:
- Owned files:
- Forbidden files:
- Test or eval path:
- Rollback:
- Approval boundaries:

## Process

1. Read adjacent code, tests, scripts, and docs that directly constrain the slice.
2. Add or update the smallest focused test/eval/check when useful and feasible.
3. Patch only owned files.
4. Run the relevant local verification command when allowed.
5. Record evidence, residual risk, and the next handoff.

## Outputs

- Changed files:
- Commands run:
- Exit codes:
- Evidence:
- Rollback notes:
- Residual risks:
- Next agent:

## Stop Conditions

- Owned files are unclear.
- The change expands into an unrelated rewrite.
- Required verification cannot run and no accepted gap exists.
- Approval-bound action is required.

## Handoff

Return changed files, evidence, open risks, rollback notes, and recommended Tester or Reviewer route.
