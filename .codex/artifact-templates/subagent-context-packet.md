# Subagent Context Packet

Use this before launch for every Codex subagent, parallel worker, or read-only sidecar. This is the Agent Handoff / Context Packet that explains what context is being passed instead of relying on raw conversation history.

## Launch Identity

- Packet id:
- Parent task id:
- Parent Task Brief ref:
- Subagent nickname:
- Role:
- Agent type:
- Model / reasoning:
- `fork_turns`:
- Launch surface:

## Prompt And Context

- Prompt:
- Prompt source:
- Complete task context:
- Templates/workflows/evals included:
- Allowed files:
- Allowed sources:
- Forbidden files:
- Inputs used:
- Expected outputs:
- Handoff output schema:

## Boundaries

- Allowed actions:
- Approval requirements:
- External/provider/browser/git/cache/live-server actions:
- Raw conversation history included:
- Secrets / private data boundary:
- Stop conditions:
- Sequential fallback:

## Transparency Checklist

- Subagent Context Packet before launch:
- Agent Handoff / Context Packet fields present:
- role:
- `fork_turns`:
- prompt:
- allowed files:
- files actually read:
- outputs:
- Subagent Result Packet required after completion:

