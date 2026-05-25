# External Integration Approval

Source status: `template`

Project: {project_name}

## External System

- External system:
- Owner:
- Environment:
- Read capability:
- Write capability:
- Sandbox credentials status:
- Data exchanged:
- PII or sensitive fields:

## Approval

- Staged draft:
- Requested action:
- Approval status: `approval_required`
- Approver:
- Approval evidence:
- Rollback:
- Disable path:
- Residual risk:

## Safety

- Do not call external systems without explicit approval.
- No secrets in staged artifacts.
- Do not store secrets, tokens, credentials or private customer data.
- External writes, provider mutations and generated client publication remain blocked until approval.
