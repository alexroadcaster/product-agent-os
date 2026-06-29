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
3. For non-mechanical code work, run `.codex/workflows/coding-standards.md` and record `.codex/artifact-templates/coding-standard-checklist.md` or `not_applicable` reason before implementation claims.
4. Patch only owned files.
5. Run the relevant local verification command when allowed.
6. Run `.codex/workflows/control-plane-sync.md` before closing: update owned control-plane files or record `not_applicable` / `handoff_required`.
7. Record evidence, residual risk, control-plane sync decision, and the next handoff.

## Outputs

- Changed files:
- Commands run:
- Exit codes:
- Evidence:
- Control-plane sync decision:
- Rollback notes:
- Residual risks:
- Next agent:

## Stop Conditions

- Owned files are unclear.
- The change expands into an unrelated rewrite.
- Required verification cannot run and no accepted gap exists.
- Non-mechanical code work lacks coding-standard checklist status or `not_applicable` reason.
- Required control-plane sync is missing.
- Approval-bound action is required.

## Handoff

Return changed files, evidence, control-plane sync decision, open risks, rollback notes, and recommended Tester or Reviewer route.
