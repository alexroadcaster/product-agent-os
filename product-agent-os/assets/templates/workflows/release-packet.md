# Release Packet

Project: {project_name}
Profile: {profile_name}

## Inputs

- Completed slice:
- Review verdict:
- Verification evidence:
- Release target:
- Approval requirements:

## Process

- Assemble a staged release draft.
- Summarize the pull request scope and user impact.
- Include checks, rollback, residual risks, and approval requirements.
- Keep external actions pending until explicitly approved.

## Outputs

- PR summary:
- Changed files:
- Checks:
- User impact:
- Rollback:
- Residual risks:
- Approval requirements:

## Verification

- Release packet matches current diff.
- Failed or skipped checks are named.
- Rollback is practical and scoped.

## Stop Conditions

- Required approval is missing.
- Blocking check failed.
- Residual risk is unacceptable for the release target.
