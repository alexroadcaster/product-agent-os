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
- Product hypothesis gate (`product_hypothesis_present`):
- Target user segment:
- Explicitly excluded users:
- Problem or opportunity:
- Opportunity is not only a solution request (`opportunity_not_solution_present`):
- Decision horizon (`decision_horizon_present`): `discovery | MVP | beta | production | scale`
- Business outcome:
- Product outcome:
- Feature traction metric:
- Outcome metric level separated (`outcome_metric_level_separated`):
- Metric scope (`metric_scope_classified`): `required | not_applicable | accepted_gap`
- Value proposition evidence (`value_proposition_evidence_present`):
- Metric hardening gate (`metric_hardening_when_product_behavior_changes`):
- North Star or primary value metric:
- Primary success metric:
- Input metric:
- Counter-metric:
- Proxy metric risk:
- Guardrail metrics:
- Baseline or current state:
- Qualitative review:
- Qualitative feedback loop (`qualitative_feedback_loop_present`):
- Privacy classification:
- Privacy classification for metrics (`privacy_classification_for_metrics_present`):
- Retention period:
- Data minimization:
- Analytics tracking plan (`analytics_tracking_plan_present`):
- HEART metrics when applicable: Happiness, Engagement, Adoption, Retention, Task success.
- Owner signoff:
- Post-release measurement:
- Post-release measurement plan (`post_release_measurement_plan_present`):
- Post-release review evidence:
- Release measurement evidence (`release_measurement_evidence_present`):
- No-production-telemetry fallback:
- Workflow promotion value evidence (`workflow_promotion_value_evidence_present`):

## Users

- Primary users:
- Secondary users:
- Operators or reviewers:

## Scope

- In scope:
- Files or systems in scope:
- Expected outputs:

## Requirements And Domain

- Requirements scope gate (`requirements_scope_present`):
- Requirements owner gate (`requirements_owner_present`):
- Requirement quality gate (`requirement_quality_present`): atomicity, clarity, testability, feasibility, traceability, source, owner.
- Requirement IDs gate (`requirement_ids_present`):
- Requirement registry: `requirement-registry.md`
- Stakeholder owner map: `stakeholder-owner-map.md`
- Story slice map: `story-slice-map.md`
- Requirement taxonomy: `functional | non-functional | compliance | operational | AI behavior | data/privacy | release/rollback`
- Business rules gate (`business_rules_present`): `business-rules.md`
- Non-goals and constraints gate (`non_goals_constraints_present`):
- Constraints traceability gate (`constraints_traceability_present`):
- Open questions gate (`open_questions_recorded`):
- Requirements traceability gate (`requirements_traceability_present`): `requirements-traceability-matrix.md`
- API/UI/data traceability gate (`api_ui_data_traceability_present`):
- Domain event contract gate (`domain_event_contracts_present`):
- Invariants and failure modes gate (`invariants_and_failure_modes_present`):
- Domain expert review gate (`domain_expert_review_present`): `domain-review-record.md`
- Requirement change impact gate (`requirement_change_impact_review_present`): `requirement-change-impact.md`
- Accepted gap gate (`accepted_gap_recorded`): owner, reason, scope, review date, downstream risk, follow-up condition.
- Requirements evidence before implementation (`requirements_evidence_before_implementation`):
- Example Mapping gate (`example_mapping_when_unclear_story`): `example-map.md`
- Domain discovery gate (`domain_discovery_workshop_when_complex_process`):
- Declarative acceptance scenario gate (`declarative_acceptance_scenarios_present`):
- Unsupported claims rejected: BDD replaces testing, Gherkin is mandatory, user story template is complete requirements, glossary is ubiquitous language, OpenAPI is requirements source of truth.

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

## Backend Intake

- Backend methodology (`backend`) applicability:
- Service/user behavior:
- Non-goals:
- Runtime constraints:
- Affected backend unit:
- Backend dependencies:
- Backend data stores:
- Operational assumptions:
- Explicit gaps before implementation planning:
- Approval boundary:
- Evidence owner:

## Acceptance Criteria

- Inputs, outputs, constraints, and verification commands are explicit.
- Acceptance scenarios are explicit for behavior changes, or an explicit gap is recorded.
- Requirements evidence is explicit before implementation, or an accepted gap is recorded.
- ATDD and BDD scenario mapping uses `requirement -> scenario -> check -> evidence owner`.
- Given, When, Then or an equivalent behavior format captures the business rule, edge case, non-goal, and evidence owner.
- Acceptance scenarios are declarative: no UI selectors, database internals, function names, or test harness details.
- Requirement quality includes atomicity, clarity, testability, feasibility, traceability, source, and owner.
- Requirement IDs, business rules, constraints, traceability, owner review, accepted gaps, and change impact are explicit when relevant.
- Scenario status is explicit: completed workflow, partial methodology gate, pending template, or not applicable.
- Safety boundaries cover sandbox, approvals, external systems, and data handling.
- Architecture boundary, documentation impact, and test or eval path are explicit.
- Data-informed success metric and post-release measurement are named when product behavior changes.
- Product work classifies metric scope as required, not_applicable, or accepted_gap.
- Product work separates business outcome, product outcome, and feature traction metric.
- Product analytics claims include tracking-plan status, event taxonomy, property definitions, owner, validation evidence, and privacy classification.
- If production telemetry does not exist, manual, qualitative, support, customer-success, owner review, or accepted gap evidence is recorded.
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
