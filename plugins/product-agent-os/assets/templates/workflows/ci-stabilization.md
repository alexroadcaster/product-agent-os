# CI Stabilization Workflow

Source status: `codex-plugin-template`

Use this workflow when a project has failing or flaky CI, pipeline, GitHub Actions, hosted runner, or local test evidence that needs diagnosis before implementation, remote CI changes, or readiness claims.

## Inputs

- User goal and accepted scope.
- CI workflow files, failing job, failing command, logs, environment, runner, and test result evidence.
- Deterministic or flaky classification evidence, including rerun evidence when available.
- Local reproduction command, isolation plan, known dependency or cache changes, and residual risk.
- Remote CI, GitHub Actions, branch protection, secrets, runner, permission, or schedule approval boundary.

## Process

1. Keep the workflow read-only until failure evidence, failing job, command, logs, environment, deterministic/flaky classification, isolation plan, local reproduction, rerun evidence, approval boundary, and residual risk are explicit.
2. Inventory workflow files, failure logs, failing job clues, command clues, environment clues, test results, flaky history, local reproduction notes, rerun notes, and approval notes as `present_unverified`.
3. Separate deterministic failure from flaky behavior. If evidence is insufficient, mark classification as unknown and stop at the smallest evidence-gathering step.
4. Identify the failing job, command, logs, environment, runner image, dependency/cache surface, test result path, and recent change boundary.
5. Prefer local reproduction before implementation: run or propose the smallest local command that matches the CI command and environment.
6. Build an isolation plan before broad fixes: single failing test, dependency boundary, cache boundary, environment mismatch, timing/concurrency, network dependency, or fixture/data issue.
7. Require rerun evidence before any CI health claim. Rerun evidence can be local rerun, approved remote CI rerun, or owner-provided CI result.
8. Keep no remote mutation as a hard boundary: do not change CI settings, secrets, branch protections, GitHub Actions permissions, hosted runner config, schedules, concurrency, cache keys, or workflow activation without explicit approval.
9. Do not rerun remote CI without approval when the action consumes hosted resources, writes status, changes external state, or requires connector access.
10. Do not claim CI health, flake resolution, pipeline stability, or release readiness from code inspection only.
11. Keep the Scenario Handoff concise.

## Outputs

- Staged CI stabilization report with:
  - failing job;
  - command;
  - logs;
  - environment;
  - deterministic/flaky classification;
  - failure evidence;
  - test result evidence;
  - local reproduction;
  - isolation plan;
  - rerun evidence;
  - remote CI and GitHub Actions boundary;
  - approval needs;
  - residual risk.
- Scenario Handoff:
  - sources/context used;
  - assumptions;
  - files touched;
  - files proposed;
  - verification evidence;
  - open risks;
  - recommended next role;
  - stop reason.

## Verification

- Failing job, command, logs, environment, deterministic/flaky classification, failure evidence, isolation plan, local reproduction, rerun evidence, approval, and residual risk are explicit.
- CI health claims cite current local reproduction, approved remote CI rerun evidence, or owner-provided CI evidence.
- Remote CI, GitHub Actions, branch protection, hosted runner, workflow permissions, workflow activation, and CI settings changes remain approval-bound.
- No remote mutation occurred unless approval evidence is recorded.

## Stop Conditions

- Failing job, command, logs, or environment are unknown.
- Deterministic/flaky classification lacks evidence.
- Local reproduction or explicit unavailable reason is missing.
- Rerun evidence is missing for a CI health or flake-resolution claim.
- The task requires remote CI rerun, CI settings change, workflow permission change, branch protection change, hosted runner mutation, or GitHub Actions activation without approval.
