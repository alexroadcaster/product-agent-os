# Review Slice

Project: {project_name}
Profile: {profile_name}

## Inputs

- Reviewed slice:
- Changed files:
- Acceptance criteria:
- Source constraints:
- Public contract:
- Migration context:
- Security-sensitive context:
- Data migration context:
- Release packaging context:
- Parallel work context:
- Coding-standard checklist:
- Existing-capability scan:
- Selected leverage path:
- Dependency decision:
- Verification evidence:
- Threat or data handling context:
- Missing evidence:

## Generalized Two-Stage Review

- Use generalized two-stage review for PR review, public contract changes, migration, security-sensitive work, data migration, release packaging, parallel work, external-system changes, or any slice with missing evidence.
- Stage 1: spec compliance:
  - Check acceptance criteria, source constraints, public contract, scope, compatibility, ownership, rollback, approvals, and required artifacts.
  - Record spec compliance verdict: `blocked | changes_requested | ready`.
  - Missing evidence blocks the stage.
- Stage 2: quality/risk:
  - Run only after Stage 1 is explicit.
  - Check tests, eval evidence, implementation quality, security, privacy, data handling, docs, release impact, maintainability, and unsupported claims.
  - Record quality/risk verdict: `blocked | changes_requested | ready`.
- Do not collapse the stages into generic review only.
- Do not run quality/risk before spec compliance.
- Do not return a ready verdict with missing evidence.

## Process

Execution budget: one reviewer window per slice and at most two repair cycles. A third review cycle stops the slice for replan. The same verification command must not run again unless a named code, config, fixture, input or environment change can affect its result.

- Use findings-first review ordered by severity.
- Check behavior against acceptance criteria.
- Check source constraints and public contract before judging implementation quality.
- Check file ownership and unrelated churn.
- Identify missing tests, regressions, and security risk.
- Check professional code authoring risk: unnecessary custom code, missing `one_line_candidate`, weak existing-capability scan, dependency debt, shallow wrappers, brittle refactors, low-signal comments, and unsupported code-quality claims.
- Treat maintainability findings as blockers only when they affect correctness, risk, evidence, ownership, dependency debt, legacy safety, or future change cost.
- Check `.codex/workflows/control-plane-sync.md`: identify missing updates or missing `not_applicable` / `handoff_required` decisions for control-plane files.
- Record a verdict: approve, request changes, or block.
- Count the review cycle and name the changed input that permits any repeated command.

## Evidence-Based Findings

Apply spec compliance before quality/risk review for risky changes. Ordinary work uses the eight-field compact code-change contract; the full coding-standard checklist is reference detail only when its extra risk questions apply.

Tie each finding to the checked revision and source, reachable scenario (or explicitly unverified hypothesis), consequence, proposed action and confidence. Empty findings are valid. Style/LOC preferences alone are advisory; correctness, security and data loss outrank brevity.

Record confirmed/fixed, rejected/false_positive, deferred or unresolved in the existing review artifact. Rejection needs evidence; deferred needs owner and revisit trigger. Suppression is not a fix. Read callers, exports, dynamic/config references before proposing deletion. A deliberate limitation is a defect only when its accepted boundary is crossed.

Repeat review for changed inputs, new risk, verification of a fix or a demonstrated reviewer gap. Unchanged reruns do not replace fixes; unrelated backlog does not block independent work. Reuse evidence with its original provenance and invalidate stale revisions.

## Outputs

- Findings with file and line references:
- Spec compliance verdict:
- Quality/risk verdict:
- Missing tests:
- Regression risk:
- Security risk:
- Unnecessary custom-code risk:
- Dependency debt risk:
- Legacy/refactor risk:
- Low-signal comment risk:
- Unsupported code-quality claims:
- Missing evidence:
- Control-plane sync gaps:
- Verdict:
- Review cycle: `1/2` or `2/2`:
- Changed input before repeated command:

## Verification

- Review cites current files and evidence.
- No success claim is made without a current check.
- Residual risk is explicit.

## Stop Conditions

- Diff or reviewed files are unavailable.
- Verification evidence is missing for risky behavior.
- Review uses generic review only for risky behavior.
- Review attempts quality/risk before spec compliance.
- Review attempts one-stage review for risky work.
- Review attempts a ready verdict with missing evidence.
- Review ignores missing applicable compact contract evidence; full checklist detail is required only for the additional risks it addresses.
- Review accepts new custom code without existing-capability scan, selected leverage path, rejected alternatives, or current evidence.
- Review accepts new dependencies without dependency risk, rollback/removal path, and approval status.
- Review finds missing required control-plane sync evidence.
- Security or data handling issue blocks release.
- Two repair cycles were consumed without acceptance.
- A command would be repeated with unchanged relevant inputs.
