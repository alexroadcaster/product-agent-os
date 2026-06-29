# Subagent Result Packet

Use this after completion, timeout, cancellation, or close for every Codex subagent, parallel worker, or read-only sidecar. This packet records what the subagent actually did and what context it actually used.

## Result Identity

- Packet id:
- Parent task id:
- Context packet ref:
- Subagent Context Packet created before launch:
- Subagent nickname:
- Role:
- Agent type:
- Agent id:
- Status:
- Completion surface:

## Actual Context Used

- Prompt received:
- `fork_context`:
- Allowed files:
- Files actually read:
- Commands run:
- Tools used:
- Templates/workflows/evals used:
- Coding-standard workflow/checklist used:
- Outputs:

## Result

- Summary:
- Findings:
- Files touched:
- Files proposed:
- Existing-capability scan:
- Selected leverage path:
- Dependency decision:
- Code-quality evidence:
- Verification evidence:
- Unsupported claims:
- Unsupported code-quality claims:
- Residual risks:
- Stop reason:
- Recommended next role:

## Boundary Evidence

- External/provider/browser/git/cache/live-server actions:
- Approval boundary status:
- Raw conversation history dependency:
- Secrets / private data exposure:
- Subagent Result Packet after completion:
- Agent Handoff / Context Packet linked:
