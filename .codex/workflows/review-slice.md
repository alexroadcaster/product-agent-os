# Review Slice

Source status: project-local system workflow.

## Purpose

Review a focused change for correctness, risk, evidence gaps, and fit with the existing Product-Agent OS project.

## Inputs

- Diff or changed files:
- Intended behavior:
- Verification evidence:
- Approval boundaries:
- Release or docs impact:

## Process

1. Read the changed files and nearby source needed to understand behavior.
2. Prioritize bugs, regressions, missing tests, security/privacy risks, source-policy issues, and unsupported readiness claims.
3. Do not reward template presence without current behavior or command evidence.
4. Check professional code authoring risk: missing `.codex/artifact-templates/coding-standard-checklist.md`, missing `existing_capability_scan`, unnecessary dependency, custom-code bloat, shallow wrapper, comment noise, broad rewrite, or unsupported code-quality claim.
5. Check `.codex/workflows/control-plane-sync.md`: identify missing updates or missing `not_applicable` / `handoff_required` decisions for control-plane files.
6. Keep findings actionable and scoped.

## Outputs

- Findings:
- Severity:
- File/line references:
- Missing evidence:
- Control-plane sync gaps:
- Residual risks:
- Required fixes or accepted gaps:
- Next agent:

## Stop Conditions

- Diff context is incomplete.
- Verification evidence is unavailable for the requested claim.
- Non-mechanical code work lacks coding-standard checklist status or `not_applicable` reason.
- Control-plane sync evidence is missing for changed scope, plan, tests, evals, runlog, or an owned source evidence ledger.
- Review requires file mutation or external access without approval.

## Handoff

Return findings first, then evidence gaps, control-plane sync gaps, recommended fixes, and next role.
