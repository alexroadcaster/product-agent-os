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

Execution budget: one reviewer window per slice and at most two repair cycles. A third review cycle stops the slice for replan. The same verification command must not run again unless a named code, config, fixture, input or environment change can affect its result.

1. Read the changed files and nearby source needed to understand behavior.
2. Prioritize bugs, regressions, missing tests, security/privacy risks, source-policy issues, and unsupported readiness claims.
3. Do not reward template presence without current behavior or command evidence.
4. Check applicable compact contract evidence and use `.codex/artifact-templates/coding-standard-checklist.md` only for relevant extra risks: missing `existing_capability_scan`, unnecessary dependency, shallow wrapper, comment noise, broad rewrite, or unsupported claim.
5. Check `.codex/workflows/control-plane-sync.md`: identify missing updates or missing `not_applicable` / `handoff_required` decisions for control-plane files.
6. Keep findings actionable and scoped.
7. Count the review cycle and name the changed input that permits any repeated command.

## Evidence-Based Findings

Apply spec compliance before quality/risk review for risky changes. Ordinary work uses the eight-field compact code-change contract; the full coding-standard checklist is reference detail only when its extra risk questions apply.

Tie each finding to the checked revision and source, reachable scenario (or explicitly unverified hypothesis), consequence, proposed action and confidence. Empty findings are valid. Style/LOC preferences alone are advisory; correctness, security and data loss outrank brevity.

Record confirmed/fixed, rejected/false_positive, deferred or unresolved in the existing review artifact. Rejection needs evidence; deferred needs owner and revisit trigger. Suppression is not a fix. Read callers, exports, dynamic/config references before proposing deletion. A deliberate limitation is a defect only when its accepted boundary is crossed.

Repeat review for changed inputs, new risk, verification of a fix or a demonstrated reviewer gap. Unchanged reruns do not replace fixes; unrelated backlog does not block independent work. Reuse evidence with its original provenance and invalidate stale revisions.

## Outputs

- Findings:
- Severity:
- File/line references:
- Missing evidence:
- Control-plane sync gaps:
- Residual risks:
- Required fixes or accepted gaps:
- Review cycle: `1/2` or `2/2`:
- Changed input before repeated command:
- Next agent:

## Stop Conditions

- Diff context is incomplete.
- Verification evidence is unavailable for the requested claim.
- Non-mechanical code work lacks applicable compact contract evidence or a justified reduced path.
- Control-plane sync evidence is missing for changed scope, plan, tests, evals, runlog, or an owned source evidence ledger.
- Review requires file mutation or external access without approval.
- Two repair cycles were consumed without acceptance.
- A command would be repeated with unchanged relevant inputs.

## Handoff

Return findings first, then evidence gaps, control-plane sync gaps, recommended fixes, and next role.
