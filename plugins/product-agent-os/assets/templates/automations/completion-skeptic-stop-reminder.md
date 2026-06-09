# Completion Skeptic Stop Reminder Candidate

Source status: generated automation candidate template; candidate-only and inactive.

Project: {{ project_name }}
Workspace: {{ workspace_path }}
Generated at: {{ generated_at }}

## Candidate Status

- status: candidate-only
- no active schedule
- no hook activation
- no automation activation
- no external writes
- no MCP activation
- no Agents SDK runner
- no provider/live external model/API calls
- no git stage/commit/push/PR

## Purpose

Remind the operator to run `completion-skeptic` before a final completion claim when a stop/final response contains high-risk readiness language, missing current evidence, stale evidence, approval-bound actions, or generated-view-only proof.

This file is a manual pilot artifact, not an active hook, schedule, recurring job, GitHub Action, Codex App automation, or external workflow.

## Manual Pilot Criteria

- At least two manual pilot runs.
- Evidence that the reminder reduced unsupported completion claims.
- False-positive review for docs-only, read-only, and lightweight tasks.
- Explicit owner approval before any activation.
- disable path and rollback owner documented before activation.

## Trigger Draft

Candidate trigger signals:

- final answer says done, ready, verified, implemented, complete, or nothing missed;
- runner status is `completed` but verification evidence is missing or stale;
- source policy is blocked or present_unverified;
- dashboard/report/site/project graph is used as proof;
- approval boundary is required or approval_blocked;
- task matrix row would move to `implemented`.

## Reminder Text Draft

Before final completion: run `completion-skeptic`, update or link `doubt-verification-packet.md`, separate supported claims from unsupported claims, and record accepted gaps. Generated dashboards are not completion proof.

## Activation Boundary

Activation requires explicit owner approval and a separate approved change. Until then:

- do not create active automation;
- do not activate schedules;
- do not install or enable hooks;
- do not create external workflows;
- do not mutate config;
- do not claim this reminder is enforcement.

## Disable Path

- owner:
- disable command or manual removal step:
- rollback evidence:
- incident contact:
