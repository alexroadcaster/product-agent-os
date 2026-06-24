# Control-Plane Sync

Source status: project-local system workflow.

## Purpose

Use this workflow before closing any non-mechanical Product-Agent OS task to decide whether root control-plane files need updates.

This is not an active hook or automation. It is a mandatory agent checklist that runs inside the parent task before the Completion Brief.

## Control-Plane Files

- `REQUIREMENTS.md`: current scope, users, constraints, acceptance criteria, assumptions, and non-goals.
- `PLAN.md`: current sequencing, queue, dependencies, rollback, and planning pointers.
- `TEST.md`: current verification commands, escalation rules, and latest maintenance evidence.
- `EVALS.md`: current eval rubrics, thresholds, subjective gates, unsupported-claim policy, and accepted-gap policy.
- `RUNLOG.md`: current-cycle decisions, latest completed slice, evidence summary, residual risks, and handoff state.
- `prod_test.md`: Batch 39 attempt, failure, fix, retest, and overlay ledger.

## Process

1. Run this check after implementation and verification, before the Completion Brief.
2. For each control-plane file, decide `update_required`, `not_applicable`, or `handoff_required`.
3. Update the file directly when the current task changed its owned information class and the file is in the task write scope.
4. Use `handoff_required` when the file is relevant but belongs to another owner or would bloat the compact root layer.
5. Preserve compactness: record current state and routing only; move detailed history to source-owned docs, generated artifacts, or `prod_test.md`.
6. Enforce the `RUNLOG.md` size budget as `50 KB` (`50 * 1024` UTF-8 bytes). If the file exceeds that budget, do not delete or compress first. First redistribute current information to the owning system files or source-owned artifacts, then shorten `RUNLOG.md` to pointers.
7. Before shortening `RUNLOG.md`, route scope and constraints to `REQUIREMENTS.md`, sequencing and next actions to `PLAN.md`, verification commands and ownership to `TEST.md`, eval thresholds and claim ceilings to `EVALS.md`, detailed evidence to source-owned plans/specs/backlogs or `prod_test.md`, and only current handoff/residual risk pointers to `RUNLOG.md`.
8. Never treat generated dashboards, stale logs, or previous runs as current evidence.
9. Do not activate hooks, automations, external writes, git actions, provider calls, browser automation, live servers, cache mutation, or target workspace mutation through this workflow.

## Update Triggers

- `REQUIREMENTS.md`: user goal, scope, acceptance criteria, assumptions, constraints, or non-goals changed.
- `PLAN.md`: task order, active batch status, dependency, rollback route, or next planned action changed.
- `TEST.md`: verification command, required check, escalation rule, or test ownership changed.
- `EVALS.md`: eval rubric, threshold, failure class, accepted-gap policy, or evidence standard changed.
- `RUNLOG.md`: current-cycle handoff, latest completed slice, residual risk, or next route changed.
- `prod_test.md`: any Batch 39 test attempt, failure, fix, retest, overlay, counter, mutation proof, or no-unapproved-actions evidence changed.

## Outputs

- Control-plane sync decision:
- `RUNLOG.md` overflow decision:
- Files updated:
- Files marked `not_applicable`:
- Handoffs required:
- Evidence refs:
- Residual risks:

## Stop Conditions

- A required control-plane update is missing.
- The task would close with only code/artifact changes while scope, plan, tests, evals, runlog, or `prod_test.md` changed.
- The needed update would bloat a compact root file instead of routing detailed history to an owned artifact.
- `RUNLOG.md` exceeds `50 KB` and no redistribution decision names the owning files or source artifacts that received the detailed information.
- Ownership is unclear and no handoff is recorded.
- Verification evidence is missing for a completion, fixed, verified, ready, or release-ready claim.
