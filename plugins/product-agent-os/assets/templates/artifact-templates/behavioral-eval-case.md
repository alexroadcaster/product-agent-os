# Behavioral Eval Case

## Identity

- Case name:
- Usage mode:
- Lifecycle state:
- Codex surface:

## Input

- Prompt:
- Workspace fixture:
- Control-plane state:
- Approval state:

## Expected Usage Mode

- Primary:
- Secondary:
- Confidence:
- Reasons:
- Fallback:

## Expected Route

- Skill:
- Subagent role:
- Write policy:
- Minimum artifacts:
- Stop condition:

## Forbidden Actions

- Forbidden actions:
- External systems:
- Hook or automation activation:
- Workspace writes:

## Evidence

- Commands:
- Files inspected:
- Reports:
- Residual risk:

## Professional Code Authoring Shortcut Guard

Use when the case tests AI-agent coding behavior.

- Gate: `professional_code_authoring_evidence_present`
- Required workflow: `.codex/workflows/coding-standards.md`
- Required checklist: `.codex/artifact-templates/coding-standard-checklist.md`
- Existing-capability scan:
- One-line candidate:
- Selected leverage path:
- Rejected alternatives:
- Dependency decision:
- Comment/noise decision:
- Abstraction/rewrite justification:
- Forbidden shortcut: `50-line custom code | unnecessary dependency | missing existing-capability scan | comment noise | shallow wrapper | unsupported legacy rewrite`
- Required evidence: current command/eval/review evidence or `explicit_gap_accepted`
- Activation boundary: generated eval case is contract evidence only, not hook/runtime activation.
