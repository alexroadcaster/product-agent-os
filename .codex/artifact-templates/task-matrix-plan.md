# Task Matrix Plan

Source status: staged artifact template

## Scope

- Schema version: task_matrix_plan_v1
- Generated at: {generated_at}
- Project: {project_name}
- Workspace: {workspace_path}
- Profile: {profile_name}
- Detected stack: {detected_stack_text}
- Timezone: Europe/Moscow

This template creates a planning artifact for methodology-heavy or evidence-heavy work. It is a staged proposal until the project owner chooses a concrete plan-file location. Generated task matrices are not source of truth by themselves; implementation evidence remains in the files, tests, reports and source-backed records that each task names.

## Trigger Policy

Use a task matrix when the work involves multi-slice delivery, cross-agent ownership, methodology standards, specs, ADRs, verification gates, release or approval boundaries, factual completion reports or user-visible sequencing. Lightweight exceptions are allowed only when the task records explicit exception evidence.

Lightweight exception fields:

- `reason`
- `reduced_evidence_path`
- `residual_risk`

## Status Policy

Allowed task statuses:

- `planned`
- `in_progress`
- `implemented`
- `blocked`
- `accepted_gap`

`planned` tasks must use `pending_execution_timestamp` for date and time of task implementation. `implemented` tasks must include an actual date and time in `DD-MM-YYYY HH:mm` format, the timezone `Europe/Moscow`, files touched / work locations, and current verification evidence from this run.

Validator target: detailed task blocks with one explicit field per line. Summary tables are planning indexes only and cannot replace the detailed task blocks.

Completion-skeptic evidence: when a task claims completion, readiness, release, fixed, verified, or implemented status, the completion report should link a `doubt_verification_packet` or explicitly record why the packet is not required. The report must name supported claims, unsupported claims, accepted gaps, current verification evidence, no-unapproved-actions proof, residual risks, and next action. Generated dashboards, generated sites, reports, and project graphs are orientation evidence only and cannot replace current command/source evidence or accepted gaps.

## Compatibility Policy

- Old matrices remain historical evidence.
- task_matrix_plan_v1 applies to new concrete task-plan files and optional backfilled rows only.
- Validator should not retroactively fail historical summary tables unless explicitly targeted.
- Summary tables remain planning indexes; detailed task blocks remain the validator target for new concrete task-plan files.

## Plan Lifecycle Policy

- Active concrete task files remain active while they drive current execution, unresolved acceptance criteria, open verification gates or owner handoff decisions.
- Evidence moves to RUNLOG.md when a current slice records command output, failed checks, handoff status, residual risk or completion evidence.
- History moves to docs/sources/*backlog*.md when a cycle closes and the detail is no longer needed in the active concrete task file.
- Source-backed claims enter docs/sources/registry*.md when documentation adds or changes source-backed factual claims.
- No secrets, raw chat, customer data, credentials, tokens or private keys belong in task plans, evidence packets or examples.
- Avoid root PLAN.md bloat, but never skip required PLAN/TEST/EVALS/RUNLOG updates because of size. When root files approach budget, move detailed history to the owning evidence artifact first, then keep root control-plane files compact and current.
- No automatic deletion of task files, evidence rows or historical records.
- No destructive cleanup without explicit owner approval and rollback notes.

## Detailed Task Block Template

### Task `<task_id>`

- Task:
- Status:
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger:
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on:
- Blocks:
- Source:
- Short description:
- Technical value:
- Product value:
- Scope:
- Non-goals:
- Expected result:
- Acceptance criteria:
- Verification gates:
- Risks / approval gates:
- Complexity:
- Estimated execution time:
- Agents:
- Skills:
- Output artifacts:
- Next step:

#### Completion Report

- status:
- what was done:
- files touched / work locations:
- technical value delivered:
- product value delivered:
- actual implementation date and time:
- verification evidence:
- residual risks:
- follow-up:

## Optional Summary Table

Summary tables are planning indexes only. Keep them compact and derive them from the detailed task blocks.

| Task | Status | Depends on | Blocks | Owner / skills | Expected result | Verification | Completion report |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<task_id>` | `planned` |  |  |  |  |  | pending |

## Safety And Evidence Boundaries

- No secrets, credentials, tokens, private keys, customer data or private chat logs.
- This template is not source of truth for implementation success.
- Keep generated artifacts staged unless the owner approves a target-workspace write.
- Perform no live automation from this template.
- Perform no provider/live external model/API calls from this template.
- Perform no git stage/commit/push/PR from this template.
- Preserve existing user-authored files outside managed sections.
- Record accepted gaps with `reason`, `reduced_evidence_path` and `residual_risk`.
