# Review Slice

Project: {project_name}
Profile: {profile_name}

## Inputs

- Reviewed slice:
- Changed files:
- Acceptance criteria:
- Verification evidence:
- Threat or data handling context:

## Process

- Use findings-first review ordered by severity.
- Check behavior against acceptance criteria.
- Check file ownership and unrelated churn.
- Identify missing tests, regressions, and security risk.
- Record a verdict: approve, request changes, or block.

## Outputs

- Findings with file and line references:
- Missing tests:
- Regression risk:
- Security risk:
- Verdict:

## Verification

- Review cites current files and evidence.
- No success claim is made without a current check.
- Residual risk is explicit.

## Stop Conditions

- Diff or reviewed files are unavailable.
- Verification evidence is missing for risky behavior.
- Security or data handling issue blocks release.
