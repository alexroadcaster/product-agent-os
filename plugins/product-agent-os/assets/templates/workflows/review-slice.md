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

- Use findings-first review ordered by severity.
- Check behavior against acceptance criteria.
- Check source constraints and public contract before judging implementation quality.
- Check file ownership and unrelated churn.
- Identify missing tests, regressions, and security risk.
- Check `.codex/workflows/control-plane-sync.md`: identify missing updates or missing `not_applicable` / `handoff_required` decisions for control-plane files.
- Record a verdict: approve, request changes, or block.

## Outputs

- Findings with file and line references:
- Spec compliance verdict:
- Quality/risk verdict:
- Missing tests:
- Regression risk:
- Security risk:
- Missing evidence:
- Control-plane sync gaps:
- Verdict:

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
- Review finds missing required control-plane sync evidence.
- Security or data handling issue blocks release.
