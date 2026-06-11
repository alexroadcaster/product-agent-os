# Task Plan Lifecycle

Source status: `codex-plugin-template`

Project: {project_name}
Profile: {profile_name}

## Purpose

Use this workflow before and after execution when Product-Agent OS work needs a concrete task-plan file instead of a loose chat plan.

This workflow also defines the user-visible contract:

- Show the Task Brief in chat before execution starts.
- Show the Completion Brief in chat after execution or handoff.
- Do not hide the brief only in a file, `prod_test.md` row, runlog, or generated artifact.

## Before Execution

0. Show the Task Brief to the user before editing or running non-read-only execution commands.
1. Create a detailed task block with `task_matrix_plan_v1`.
2. Keep status `planned`.
3. Use `pending_execution_timestamp` for date and time of task implementation.
4. Name product value, technical value, scope, non-goals, expected result, acceptance criteria, verification gates, risks, agents, skills, output artifacts, complexity, estimated execution time, and next step.
5. Validate the plan file before execution:

```powershell
python plugins\product-agent-os\scripts\validate_task_matrix.py <plan-file>
```

Optional generator:

```powershell
python plugins\product-agent-os\scripts\create_task_plan.py new --output <plan-file> --task-id <id> --task <id> --plan-trigger <trigger> --source <source> --short-description <text> --technical-value <text> --product-value <text> --scope <text> --non-goals <text> --expected-result <text> --acceptance-criteria <text> --verification-gates <command-or-gap> --risks-approval-gates <text> --complexity <low-medium-high> --estimated-execution-time <time> --agents <roles> --skills <skills> --output-artifacts <paths> --next-step <text>
```

## After Execution

0. Show the Completion Brief to the user after execution, verification, or a blocked handoff.
1. Update the same task block, not only a summary table.
2. Change status to `implemented` only when current evidence exists or an accepted gap is recorded.
3. Replace `pending_execution_timestamp` with actual `DD-MM-YYYY HH:mm` time in `Europe/Moscow`.
4. Fill the Completion Report: what was done, files touched / work locations, technical value delivered, product value delivered, verification evidence, residual risks, and follow-up.
5. Validate the plan file again.

Optional generator:

```powershell
python plugins\product-agent-os\scripts\create_task_plan.py complete --path <plan-file> --task-id <id> --timestamp <DD-MM-YYYY HH:mm> --what-was-done <text> --files-touched <paths> --technical-value-delivered <text> --product-value-delivered <text> --verification-evidence <command-evidence> --residual-risks <text> --follow-up <text>
```

## Outputs

- User-visible Task Brief:
- Pre-execution detailed task block:
- User-visible Completion Brief:
- Post-execution Completion Report:
- Validation command:
- Evidence ref:
- Handoff target:

## Task Brief Fields

- Task ID:
- Product value:
- Technical value:
- Source / trigger:
- Scope:
- Non-goals:
- Agents and skills:
- Files / artifacts expected:
- Verification gate:
- Approval boundary / risks:
- Complexity:
- Estimated execution time:
- Next action:

## Completion Brief Fields

- Task ID:
- Result status:
- What was done:
- Files / artifacts changed:
- Verification evidence:
- Residual risks / accepted gaps:
- Follow-up:

## Stop Conditions

- The work is small and mechanical and a lightweight exception is explicitly recorded.
- A required Task Brief or Completion Brief would be missing from the user-visible conversation.
- Exact files, verification gates, evidence owner, or approval boundaries are unknown.
- Current evidence is missing for an `implemented`, `fixed`, `verified`, `ready`, or `release-ready` claim.
- The task would require external writes, provider calls, browser automation, git mutation, deployment, hooks, automation, or permission changes without approval.
