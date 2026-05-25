# RUNLOG.md

<!-- product-agent-os:start runlog -->
Project: {project_name}
Workspace: {workspace_path}
Profile: {profile_name}
Detected stack: {detected_stack_text}
Generated at: {generated_at}

## Current State

- Task:
- Lifecycle state:
- Usage mode:
- Scenario status: `done | partial | pending | not_applicable`
- Files in scope:
- Files out of scope:

## Route Decision

- Primary route:
- Secondary routes:
- Confidence:
- Reasons:
- Minimum artifacts:
- Missing evidence, workflow, or template gap:
- Approval boundary:

## Decisions

- Decision:
- Rationale:
- Source or owner:

## Methodology Trace

- Product hypothesis:
- Metric hardening gate (`metric_hardening_when_product_behavior_changes`):
- North Star or primary value metric:
- Input metric:
- Counter-metric:
- Proxy metric risk:
- Guardrail:
- Qualitative review:
- Privacy classification:
- Retention period:
- Data minimization:
- Owner signoff:
- Post-release review evidence:
- Architecture boundary:
- FSD structure applicability (`fsd_structure`):
- Feature-Sliced Design layer/slice/segment:
- Public API:
- Import rule:
- FSD accepted gap or not applicable reason:
- Domain model applicability (`domain_model_when_complex_domain`):
- Bounded context architecture trace (`bounded_context_architecture_boundary_trace`):
- Bounded context -> architecture boundary:
- Ubiquitous language traceability (`ubiquitous_language_traceability`):
- Term-to-requirement:
- API/event/contract:
- UI label:
- Code module or owner:
- Domain expert review:
- Accepted gap:
- Requirements scope (`requirements_scope_present`):
- Requirements owner (`requirements_owner_present`):
- Requirement quality (`requirement_quality_present`):
- Requirement IDs (`requirement_ids_present`):
- Requirement registry: `requirement-registry.md`
- Stakeholder owner map: `stakeholder-owner-map.md`
- Story slice map: `story-slice-map.md`
- Requirements traceability (`requirements_traceability_present`): `requirements-traceability-matrix.md`
- Business rules (`business_rules_present`): `business-rules.md`
- Non-goals and constraints (`non_goals_constraints_present`):
- Constraints traceability (`constraints_traceability_present`):
- Open questions (`open_questions_recorded`):
- Declarative acceptance scenarios (`declarative_acceptance_scenarios_present`):
- Domain event contracts (`domain_event_contracts_present`):
- API/UI/data traceability (`api_ui_data_traceability_present`):
- Requirement change impact review (`requirement_change_impact_review_present`): `requirement-change-impact.md`
- Domain expert review (`domain_expert_review_present`): `domain-review-record.md`
- Accepted gap recorded (`accepted_gap_recorded`):
- Requirements evidence before implementation (`requirements_evidence_before_implementation`):
- Unsupported requirements claims rejected:
- Test-first or eval-first evidence:
- Quality methodology (`quality_testing_evals`):
- Quality strategy: `quality-strategy.md`
- Test/eval matrix: `test-eval-matrix.md`
- CI evidence record: `ci-evidence-record.md`
- Flaky test policy: `flaky-test-policy.md`
- Manual QA evidence: `manual-qa-evidence.md`
- Quality strategy gate (`quality_strategy_present`):
- Risk based scope gate (`risk_based_scope_present`):
- Test-first or gap gate (`test_first_or_gap_present`):
- Acceptance traceability gate (`acceptance_traceability_present`):
- Contract check gate (`contract_check_present`):
- Runtime evidence gate (`runtime_evidence_present`):
- Manual QA evidence gate (`manual_qa_evidence_present`):
- Visual/a11y evidence gate (`visual_a11y_evidence_present`):
- Eval spec gate (`eval_spec_present`):
- Eval rerun evidence gate (`eval_rerun_evidence_present`):
- Current evidence before completion (`current_evidence_before_completion`):
- CI quality gate (`ci_quality_gate_present`):
- Flaky test policy gate (`flaky_test_policy_present`):
- Coverage policy gate (`coverage_policy_present`):
- Test data privacy gate (`test_data_privacy_present`):
- Bug reproduction evidence gate (`bug_reproduction_evidence_present`):
- Regression impact gate (`regression_impact_present`):
- Coverage is a signal, not proof:
- Quality status: `present_unverified | explicit_gap_accepted | approval_required`
- Conditional readiness gates:
- Readiness statuses (`readiness_statuses`): `not_applicable | applicable_missing | present_unverified | present_verified | proposal_staged | explicit_gap_accepted | approval_required`
- Gate id:
- Applies when:
- Applicability reason:
- Required evidence:
- Status:
- Owner:
- Accepted gap status:
- Residual risk:
- Detection alone only supported `present_unverified`:
- Documentation impact:
- Docs tooling selector (`docs_tooling_selector`):
- Docs tooling decision artifact: `docs-tooling-decision.md`
- Docs-as-code impact (`docs_as_code_impact`):
- Docs-as-code status: `not_applicable | present_unverified | present_verified | proposal_staged | explicit_gap_accepted | approval_required`
- Selected tools:
- Rejected tools:
- Evidence owner:
- Maintenance owner:
- No forced install:
- No CI activation without approval:
- Hosted docs approval:
- DB introspection approval:
- Docs-light or internal-only reason:
- Standards trigger policy (`standards_trigger_policy`):
- ADR trigger policy:
- C4/arc42 applicability:
- OpenAPI source of truth:
- AsyncAPI contract:
- SemVer impact:
- Keep a Changelog categories:
- Governance proposal: `governance-proposal.md`
- CODEOWNERS status:
- GitHub Actions least privilege:
- No forced external activation:
- Review outcome:
- Post-release measurement plan:

## Generalized Two-Stage Review

- Review artifact: `review-slice.md` or PR risk review packet
- Risk triggers: public contract, migration, security-sensitive, data migration, release packaging, parallel work
- Stage 1: spec compliance:
- Acceptance criteria:
- Source constraints:
- Public contract:
- Spec compliance verdict: `blocked | changes_requested | ready`
- Missing evidence:
- Stage 2: quality/risk:
- Quality/risk verdict: `blocked | changes_requested | ready`
- Quality/risk evidence:
- Do not collapse:
- Generic review only:
- Quality/risk before spec compliance:
- One-stage review for risky work:
- Ready verdict with missing evidence:
- Final review outcome:

## Commands

- Command:
- Exit code:
- Relevant output:

## Verification Evidence

- Check:
- Result:
- Artifact:
- Claims still `present_unverified`:
- Evidence-before-completion (`evidence_before_completion`):
- Ready claim:
- Completed claim:
- Fixed claim:
- Works claim:
- Release claim:
- Current command evidence:
- Current eval evidence:
- Current runtime evidence:
- Inspection-only:
- Explicit test gap:
- Unsupported completion claim:
- Completion claim without current evidence:

## Measurement Notes

- Product hypothesis (`product_hypothesis_present`):
- Value proposition evidence (`value_proposition_evidence_present`):
- Decision horizon (`decision_horizon_present`): `discovery | MVP | beta | production | scale`
- Business outcome:
- Product outcome:
- Feature traction metric:
- Outcome metric level separated (`outcome_metric_level_separated`):
- Metric scope (`metric_scope_classified`): `required | not_applicable | accepted_gap`
- Metric:
- Baseline:
- Current observation:
- Input metric:
- Counter-metric:
- Proxy metric risk:
- Guardrail:
- Qualitative review:
- Qualitative feedback loop (`qualitative_feedback_loop_present`):
- Optional HEART metrics: Happiness, Engagement, Adoption, Retention, Task success.
- Analytics tracking plan (`analytics_tracking_plan_present`):
- Privacy classification:
- Retention period:
- Data minimization:
- Owner signoff:
- Post-release review evidence:
- Release measurement evidence (`release_measurement_evidence_present`):
- No-production-telemetry fallback:
- Workflow promotion value evidence (`workflow_promotion_value_evidence_present`):
- Do not claim success from a proxy metric without counter-metric, guardrail, qualitative review, and post-release review evidence:
- Decision or next experiment:

## Failures

- Failure:
- Reproduction:
- Resolution or next action:

## Risks

{risk_text}

## Handoff Summary

- Sources used:
- Assumptions:
- Files touched:
- Files proposed:
- Verification evidence:
- Open risks:
- Recommended next role:
<!-- product-agent-os:end runlog -->
