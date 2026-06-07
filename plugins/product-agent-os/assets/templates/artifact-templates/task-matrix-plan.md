# Task Matrix Plan

Source status: staged artifact template

## Scope

- Template batch marker: B37-S2
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
