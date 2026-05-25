# TEST.md

<!-- product-agent-os:start test-plan -->
Project: {project_name}
Workspace: {workspace_path}
Profile: {profile_name}
Detected stack: {detected_stack_text}
Generated at: {generated_at}

## Deterministic Checks

- Static analysis:
- Unit tests:
- Test-first cases:
- Fixture or contract tests:
- API, event, or schema checks:
- Build command:

## Scenario And Route Checks

- Usage mode expected:
- Usage mode observed:
- Scenario status: `done | partial | pending | not_applicable`
- Behavioral eval case:
- Minimum artifacts present:
- Partial or pending gap accepted:
- Forbidden behavior checked:

## Manual Checks

- Acceptance scenario:
- Acceptance scenarios:
- ATDD or BDD mapping:
- Requirement -> scenario -> check -> evidence owner:
- Given:
- When:
- Then:
- Equivalent behavior format:
- Business rule:
- Edge case:
- Non-goal:
- Behavior changes:
- Explicit gap:
- Evidence owner:
- Data handling review:
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
- Do not claim success from a proxy metric without counter-metric, guardrail, qualitative review, and post-release review evidence:
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
- Quality methodology (`quality_testing_evals`):
- Quality strategy artifact: `quality-strategy.md`
- Test/eval matrix artifact: `test-eval-matrix.md`
- CI evidence artifact: `ci-evidence-record.md`
- Flaky test policy artifact: `flaky-test-policy.md`
- Manual QA evidence artifact: `manual-qa-evidence.md`
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
- FSD structure applicability (`fsd_structure`):
- Feature-Sliced Design layer/slice/segment:
- Public API:
- Import rule:
- FSD accepted gap or not applicable reason:
- Domain model applicability (`domain_model_when_complex_domain`):
- Bounded context -> architecture boundary trace (`bounded_context_architecture_boundary_trace`):
- Ubiquitous language traceability (`ubiquitous_language_traceability`):
- Term-to-requirement:
- API/event/contract:
- UI label:
- Code module or owner:
- Domain expert review:
- Accepted gap:
- Requirements scope gate (`requirements_scope_present`):
- Requirements owner gate (`requirements_owner_present`):
- Requirement quality gate (`requirement_quality_present`):
- Requirement IDs gate (`requirement_ids_present`):
- Requirements traceability gate (`requirements_traceability_present`):
- Business rules gate (`business_rules_present`):
- Non-goals and constraints gate (`non_goals_constraints_present`):
- Constraints traceability gate (`constraints_traceability_present`):
- Open questions gate (`open_questions_recorded`):
- Declarative acceptance scenarios gate (`declarative_acceptance_scenarios_present`):
- Domain event contracts gate (`domain_event_contracts_present`):
- API/UI/data traceability gate (`api_ui_data_traceability_present`):
- Domain expert review gate (`domain_expert_review_present`):
- Requirement change impact review gate (`requirement_change_impact_review_present`):
- Accepted gap recorded (`accepted_gap_recorded`):
- Requirements evidence before implementation (`requirements_evidence_before_implementation`):
- Requirement registry: `requirement-registry.md`
- Stakeholder owner map: `stakeholder-owner-map.md`
- Story slice map: `story-slice-map.md`
- Requirements traceability matrix: `requirements-traceability-matrix.md`
- Business rules artifact: `business-rules.md`
- Example map: `example-map.md`
- Requirement change impact: `requirement-change-impact.md`
- Domain review record: `domain-review-record.md`
- Approval review:
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
- Detection alone remains `present_unverified`:

## Runtime Or Visual Checks

- Runtime command:
- Browser, app, or API behavior:
- Screenshot, log, or trace evidence:

## Documentation Checks

- Architecture docs:
- API contracts:
- UI component docs:
- Database docs:
- User-facing docs:
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
- AsyncAPI channel/message/payload schema:
- SemVer impact:
- Keep a Changelog categories:
- Governance proposal: `governance-proposal.md`
- CODEOWNERS status:
- GitHub Actions permissions/triggers/owners:
- No forced external activation:

## AI Or Subjective Quality Checks

- Eval command:
- Dataset or fixtures:
- Grounding or citation checks:
- Retrieval metrics:
- Latency or cost thresholds:

## Known Gaps

{risk_text}

## Evidence Format

- Command:
- Exit code:
- Relevant output:
- Files or artifacts inspected:
- Claims still `present_unverified`:
- Ready claim / completed claim / fixed claim / works claim / release claim evidence:
- Current command evidence:
- Current eval evidence:
- Current runtime evidence:
- Inspection-only label:
- Explicit test gap:
- Unsupported completion claim:
- Completion claim without current evidence:
- Residual risk:
<!-- product-agent-os:end test-plan -->
