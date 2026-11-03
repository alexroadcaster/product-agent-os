# Control-Plane Sync

Source status: project-local system workflow.

## Purpose

Use this workflow before closing any non-mechanical Product-Agent OS task to decide whether root control-plane files need updates.

This is not an active hook or automation. It is a mandatory agent checklist that runs inside the parent task before the Completion Ledger.

## Control-Plane Files

- `REQUIREMENTS.md`: current scope, users, constraints, acceptance criteria, assumptions, and non-goals.
- `PLAN.md`: current sequencing, queue, dependencies, rollback, and planning pointers.
- `TEST.md`: current verification commands, escalation rules, and latest maintenance evidence.
- `EVALS.md`: current eval rubrics, thresholds, subjective gates, unsupported-claim policy, and accepted-gap policy.
- `RUNLOG.md`: current-cycle decisions, latest completed slice, evidence summary, residual risks, and handoff state.
- `prod_test.md`: historical Batch 39 production-test ledger; update it only when the current task explicitly changes that evidence family.

## Process

1. Run this check after implementation and verification, before the Completion Ledger.
2. For each control-plane file, decide `update_required`, `not_applicable`, `handoff_required`, or `overflow_refactor_required`.
3. Update the file directly when the current task changed its owned information class and the file is in the task write scope.
4. Use `handoff_required` only when the file is relevant but belongs to another owner or is outside the current write scope. Do not use `handoff_required` merely because the file is near a size limit.
5. Use `overflow_refactor_required` when a required update would bloat a compact root file. First move cold history, detailed evidence, row banks, long matrices, or old cycle decisions to the owning source artifact, then shorten the root file to current pointers and apply the required update in the same slice when the file is in scope.
6. Preserve compactness: root files record current state, routing, gates, and pointers only; detailed history belongs in source-owned docs, specs, backlogs, product docs, generated artifacts, or `prod_test.md`.
7. Treat `50 KB` (`50 * 1024` UTF-8 bytes) as the default compactness budget for root control-plane files unless a project-specific test defines a different budget. A budget crossing is a compaction trigger, not permission to skip the control-plane update.
8. Before shortening `RUNLOG.md` or any root control-plane file, route scope and constraints to `REQUIREMENTS.md`, sequencing and next actions to `PLAN.md`, verification commands and ownership to `TEST.md`, eval thresholds and claim ceilings to `EVALS.md`, detailed evidence to source-owned plans/specs/backlogs or `prod_test.md`, and only current handoff/residual risk pointers to `RUNLOG.md`.
9. Never treat generated dashboards, stale logs, or previous runs as current evidence.
10. Do not activate hooks, automations, external writes, git actions, provider calls, browser automation, live servers, cache mutation, or target workspace mutation through this workflow.

## Update Triggers

- `REQUIREMENTS.md`: user goal, scope, acceptance criteria, assumptions, constraints, or non-goals changed.
- `PLAN.md`: task order, active batch status, dependency, rollback route, or next planned action changed.
- `TEST.md`: verification command, required check, escalation rule, or test ownership changed.
- `EVALS.md`: eval rubric, threshold, failure class, accepted-gap policy, or evidence standard changed.
- `RUNLOG.md`: current-cycle handoff, latest completed slice, residual risk, or next route changed.
- `prod_test.md`: the current task explicitly changed Batch 39 attempt, failure, fix, retest, overlay, counter, mutation-proof, or no-unapproved-actions evidence.

## Outputs

- Control-plane sync decision:
- Overflow/refactor decision:
- Files updated:
- Files marked `not_applicable`:
- Handoffs required:
- Evidence refs:
- Residual risks:

## Stop Conditions

- A required control-plane update is missing.
- The task would close with only code/artifact changes while scope, plan, tests, evals, runlog, or an owned source evidence ledger changed.
- A needed update is skipped because a root control-plane file is near or over budget.
- `overflow_refactor_required` is needed but no redistribution decision names the owning files or source artifacts that received the detailed information.
- Ownership is unclear and no handoff is recorded.
- Verification evidence is missing for a completion, fixed, verified, ready, or release-ready claim.
