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
- Coding-standard workflow:
- Compact code-change contract:
- Existing-capability scan:
- Selected leverage path:
- Dependency decision:
- Documentation impact:
- Exact commands:
- Expected outputs:
- Evidence owner:
- Mechanical_change reason:

## Process

1. Confirm requirements, owned files, forbidden files, and the no-placeholder plan quality gate.
2. Read adjacent implementation patterns.
3. For non-mechanical code work, apply `.codex/workflows/coding-standards.md` before editing: record existing-capability scan, `one_line_candidate`, selected leverage path, rejected alternatives, dependency decision, and `not_applicable` only when justified.
4. For a non-trivial slice, stop before build unless exact files, relevant commands, expected outputs, rollback, evidence owner, placeholder scan, and compact code-change contract evidence are present. Use the full coding-standard checklist only as reviewer/reference detail for applicable extra risks.
5. If `mechanical_change` is used, confirm its reason and the reduced exact files, evidence owner, rollback, command or no-command gap, and coding-standard `not_applicable` reason.
6. Create or update the smallest useful test, contract check, fixture, or eval before behavior changes.
7. Make the minimal edit inside the approved architecture boundary.
8. Update source-of-truth docs affected by the slice.
9. Select the smallest reliable checks for the changed contract through `TEST.md`; add affected integration checks when wiring changes. Plan/report/control-plane text edits alone do not trigger product-wide checks.
10. Run `.codex/workflows/control-plane-sync.md` before closing: update owned control-plane files or record `not_applicable` / `handoff_required`.
11. Record result, evidence, rollback, control-plane sync decision, and risks.

## Outputs

- Changed files:
- Command evidence:
- Expected outputs:
- Runtime or visual evidence:
- Compact code-change contract evidence:
- Selected leverage path:
- Dependency decision:
- Unsupported code-quality claims:
- Control-plane sync decision:
- Rollback notes:
- RUNLOG.md entry:

## Verification

- Commands:
- Exit codes:
- Evidence:
- Missing coverage:
- Placeholder scan:
- Existing-capability scan:
- Rejected alternatives:
- Code-quality evidence:

## Stop Conditions

- Slice is not approved.
- File ownership is unclear.
- Architecture boundary is unclear.
- Plan quality gate is blocked or missing.
- No-placeholder status is missing.
- Exact files, owned files, forbidden files, exact commands, expected outputs, rollback, or evidence owner are missing for a non-trivial slice.
- Non-mechanical code work lacks compact contract evidence or a justified `not_applicable` reason.
- New custom code lacks existing-capability scan, selected leverage path, rejected alternatives, or test/eval evidence.
- New dependency lacks `negative_dependency_rule`, owner, risk note, rollback/removal path, or approval status.
- Placeholder scan finds unresolved names, vague validation, repeated-by-reference steps, or commands without expected outputs.
- Plan repair is required before implementation.
- Stop before build when `mechanical_change` lacks a reason.
- No test-first, eval-first, or explicitly accepted gap exists.
- Required check cannot run and no explicit gap is recorded.
- Required control-plane sync is missing before completion.
