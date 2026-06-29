# Legacy Onboarding

Project: {project_name}
Profile: {profile_name}

## Inputs

- Workspace inventory:
- User goal:
- Known entry points:
- Known run commands:
- Existing README/docs:
- Existing architecture notes:
- Verification evidence:
- Approval boundary:

## Process

1. Keep this workflow read-only until the owner approves a write.
2. Build a source map from observed files, not guesses.
3. Identify entry points, run commands, package scripts, tests, build steps, and local service boundaries.
4. Mark every discovered command, entry point, docs page, and architecture clue as `present_unverified` until commands run or owner evidence confirms it.
5. Record architecture/doc gaps and a docs debt map before proposing any cleanup.
6. Treat stale docs as historical context, not source of truth. Do not infer behavior from stale docs without command or owner evidence.
7. For legacy refactor requests, record `legacy_seam_check`, characterization evidence, suspected seams, no-big-rewrite boundary, and rollback or accepted gap before proposing code changes.
8. Propose the first safe documentation slice: a small onboarding note, runbook, source map, architecture gap note, or characterization-test plan.
9. Do not refactor, rename, move files, rewrite stale docs as truth, or broaden scope before orientation and legacy seam evidence are complete.

## Outputs

- Source map:
- Entry points:
- Run commands:
- Architecture/doc gaps:
- Docs debt map:
- Verification status:
- `present_unverified` items:
- First safe documentation slice:
- Legacy seam check:
- Characterization evidence:
- No-big-rewrite boundary:
- Assumptions:
- Open risks:
- Approval requirements:

## Verification

- Every source map item cites an observed file.
- Every run command is marked `present_unverified` until it has current command evidence.
- Documentation and architecture claims are `present_unverified`, `applicable_missing`, or evidence-backed.
- First safe documentation slice is explicitly without refactor.
- No runtime, build, test, or architecture claim is treated as verified from inspection alone.
- Legacy refactor work records characterization evidence, seam strategy, no-big-rewrite boundary, and rollback or accepted gap before implementation proposals.

## Stop Conditions

- Read scope is unclear.
- The user asks for broad refactor before source map and run commands are recorded.
- The user asks for legacy rewrite before `legacy_seam_check`, characterization evidence, seam strategy, rollback, and owner acceptance exist.
- The user asks to rewrite docs as truth before stale docs are checked.
- A command, dependency install, external system, or write is needed without explicit approval.
