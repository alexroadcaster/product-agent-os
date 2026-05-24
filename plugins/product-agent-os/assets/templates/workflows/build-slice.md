# Build Slice

Project: {project_name}
Profile: {profile_name}

## Inputs

- One approved slice:
- Plan quality gate:
- No-placeholder status:
- Owner:
- Acceptance criteria:
- Product hypothesis and metric:
- Architecture boundary:
- Exact files:
- Owned files:
- Forbidden files:
- Test-first or eval-first path:
- Documentation impact:
- Exact commands:
- Expected outputs:
- Evidence owner:
- Mechanical_change reason:

## Process

1. Confirm requirements, owned files, forbidden files, and the no-placeholder plan quality gate.
2. Read adjacent implementation patterns.
3. For a non-trivial slice, stop before build unless exact files, exact commands, expected outputs, rollback, evidence owner, and placeholder scan are present.
4. If `mechanical_change` is used, confirm its reason and the reduced exact files, evidence owner, rollback, and command or no-command gap.
5. Create or update the smallest useful test, contract check, fixture, or eval before behavior changes.
6. Make the minimal edit inside the approved architecture boundary.
7. Update source-of-truth docs affected by the slice.
8. Run the relevant check.
9. Record result, evidence, rollback, and risks.

## Outputs

- Changed files:
- Command evidence:
- Expected outputs:
- Runtime or visual evidence:
- Rollback notes:
- RUNLOG.md entry:

## Verification

- Commands:
- Exit codes:
- Evidence:
- Missing coverage:
- Placeholder scan:

## Stop Conditions

- Slice is not approved.
- File ownership is unclear.
- Architecture boundary is unclear.
- Plan quality gate is blocked or missing.
- No-placeholder status is missing.
- Exact files, owned files, forbidden files, exact commands, expected outputs, rollback, or evidence owner are missing for a non-trivial slice.
- Placeholder scan finds unresolved names, vague validation, repeated-by-reference steps, or commands without expected outputs.
- Plan repair is required before implementation.
- Stop before build when `mechanical_change` lacks a reason.
- No test-first, eval-first, or explicitly accepted gap exists.
- Required check cannot run and no explicit gap is recorded.
