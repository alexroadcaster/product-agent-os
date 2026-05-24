# Governance Proposal Template

Project: {project_name}

## Purpose

Use this artifact when `standards_trigger_policy` finds repository governance impact and the work needs a proposal before any external activation. This template is proposal-only.

## Applicability

- Trigger:
- Governance proposal status: `not_applicable | present_unverified | present_verified | proposal_staged | explicit_gap_accepted | approval_required`
- Applicability reason:
- Evidence owner:
- Maintenance owner:
- Residual risk:

## Standards Trigger Policy

- ADR trigger policy impact:
- C4 or arc42 architecture documentation impact:
- OpenAPI source of truth or AsyncAPI contract impact:
- SemVer impact or Keep a Changelog impact:
- CODEOWNERS status:
- GitHub Actions impact:

## CODEOWNERS Proposal

- CODEOWNERS status: `present_verified | proposal_staged | approval_required | not_applicable`
- Paths or ownership areas:
- Proposed owners:
- Reviewer groups:
- Approval requirement:
- Verification evidence:
- Residual risk:

## GitHub Actions Proposal

- GitHub Actions status: `present_verified | proposal_staged | approval_required | not_applicable`
- Workflow names:
- Commands:
- Permissions:
- Triggers:
- Owners:
- Least privilege:
- Secrets policy:
- External actions policy:
- Cache or artifact policy:
- Runner assumptions:
- Rollback:
- Verification evidence:

## Approval Boundary

- No external activation without approval.
- No forced external activation.
- Do not change repository settings, branch protection, CODEOWNERS, required checks, GitHub Actions, environments, secrets, releases, packages, or external systems from this proposal.
- Stage files or text only when requested; keep remote activation, settings changes, workflow enablement, and permission changes approval-bound.

## Verification

- Proposal matches current repository context.
- Permissions are least privilege.
- Workflow names, commands, triggers, owners, and rollback are explicit.
- CODEOWNERS status uses the approved vocabulary.
- Missing governance evidence is recorded as `present_unverified`, `proposal_staged`, `explicit_gap_accepted`, or `approval_required`, not as verified.
