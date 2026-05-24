# REQUIREMENTS.md

<!-- product-agent-os:start requirements -->
Project: {project_name}
Workspace: {workspace_path}
Profile: {profile_name}
Detected stack: {detected_stack_text}
Generated at: {generated_at}

## Goal

- Define the outcome this project or slice must produce.

## Usage Mode And Scenario

- Primary `usage_mode`:
- Secondary modes:
- Confidence:
- Route evidence:
- Minimum artifacts:
- Scenario status: `done | partial | pending | not_applicable`
- Evidence gaps:

## Product Hypothesis And Metrics

- Hypothesis:
- Metric hardening gate (`metric_hardening_when_product_behavior_changes`):
- North Star or primary value metric:
- Primary success metric:
- Input metric:
- Counter-metric:
- Proxy metric risk:
- Guardrail metrics:
- Baseline or current state:
- Qualitative review:
- Privacy classification:
- Retention period:
- Data minimization:
- Owner signoff:
- Post-release measurement:
- Post-release review evidence:

## Users

- Primary users:
- Secondary users:
- Operators or reviewers:

## Scope

- In scope:
- Files or systems in scope:
- Expected outputs:

## Source-Of-Truth Artifacts

- Architecture docs:
- API contracts:
- UI component docs:
- Database docs:
- User-facing docs:
- Release or changelog docs:

## Non-Goals

- Out of scope:
- Deferred work:
- Explicitly unsupported behavior:

## Constraints

- Sandbox and approvals:
- Source of truth:
- Data handling:
- Runtime or stack constraints: {detected_stack_text}

## Acceptance Criteria

- Inputs, outputs, constraints, and verification commands are explicit.
- Acceptance scenarios are explicit for behavior changes, or an explicit gap is recorded.
- ATDD and BDD scenario mapping uses `requirement -> scenario -> check -> evidence owner`.
- Given, When, Then or an equivalent behavior format captures the business rule, edge case, non-goal, and evidence owner.
- Scenario status is explicit: completed workflow, partial methodology gate, pending template, or not applicable.
- Safety boundaries cover sandbox, approvals, external systems, and data handling.
- Architecture boundary, documentation impact, and test or eval path are explicit.
- Data-informed success metric and post-release measurement are named when product behavior changes.
- Product behavior metrics include the North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence, or an explicit not-applicable reason.
- Do not claim success from a proxy metric without counter-metric, guardrail, qualitative review, and post-release review evidence.
- Open questions are tracked before broad implementation starts.

## Assumptions

- Existing control-plane files: {existing_control_plane}
- Missing control-plane files at generation time: {missing_control_plane}
- Existing Codex assets: {existing_codex_assets}
- Initial risk note: {risk_text}

## Open Questions

- Question:
- Owner:
- Decision needed by:
<!-- product-agent-os:end requirements -->
