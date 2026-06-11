# Source Context Pack

Source status: project-local system workflow.

## Purpose

Give the next agent enough fresh project context to act without rereading the whole repository or relying on raw conversation history.

## Inputs

- User task:
- Target subsystem:
- Allowed write scope:
- Approval-bound surfaces:
- Relevant current files:
- Relevant commands:
- Current evidence:

## Process

1. Read the nearest active instructions and only the source files needed for the task.
2. Identify the existing implementation pattern before recommending changes.
3. Separate verified facts, assumptions, unsupported claims, and stale or generated-view-only evidence.
4. Name the relevant Product-Agent OS domain: product, architecture, implementation, verification, review, docs, release, or system maintenance.
5. Stop when the next agent has enough context to act safely.

## Outputs

- Files read:
- Existing patterns:
- Current constraints:
- Allowed files:
- Forbidden files:
- Approval boundaries:
- Commands discovered:
- Evidence available:
- Unsupported claims:
- Recommended next agent:

## Stop Conditions

- Required source cannot be read.
- The task requires external access, provider calls, browser automation, git mutation, hook/automation activation, deployment, or permission changes without approval.
- Context collection is becoming broad inventory instead of task-specific evidence.

## Handoff

Keep the handoff concise enough for the next agent to work without raw chat history.
