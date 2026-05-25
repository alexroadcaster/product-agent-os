# EVALS.md

<!-- product-agent-os:start evals -->
Project: {project_name}
Workspace: {workspace_path}
Profile: {profile_name}
Detected stack: {detected_stack_text}
Generated at: {generated_at}

## Rubrics

- Correctness:
- Completeness:
- Safety:
- Source grounding:
- Route selection:
- Shortcut resistance:
- Evidence-before-completion:
- `evidence_before_completion`:
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
- Architecture boundary:
- FSD structure routing:
- Bounded context traceability:
- Ubiquitous language traceability:
- Metric hardening:
- Conditional readiness gates:
- `readiness_statuses`:
- `not_applicable`:
- `applicable_missing`:
- `present_unverified`:
- `present_verified`:
- `proposal_staged`:
- `explicit_gap_accepted`:
- `approval_required`:
- Detection alone:
- Applicability reason:
- Owner:
- Residual risk:
- Documentation quality:
- Docs tooling selector:
- `docs_tooling_selector`:
- `docs-tooling-decision.md`:
- `docs_as_code_impact`:
- Docs-as-code statuses: `not_applicable | present_unverified | present_verified | proposal_staged | explicit_gap_accepted | approval_required`
- Selected tools:
- Rejected tools:
- Evidence owner:
- Maintenance owner:
- No forced install:
- No CI activation without approval:
- Hosted docs approval:
- DB introspection approval:
- Docs-light:
- Internal-only:
- Standards trigger policy:
- `standards_trigger_policy`:
- ADR trigger policy:
- C4:
- arc42:
- OpenAPI source of truth:
- AsyncAPI:
- SemVer impact:
- Keep a Changelog:
- Governance proposal: `governance-proposal.md`
- CODEOWNERS status:
- GitHub Actions:
- Least privilege:
- No forced external activation:
- Quality methodology:
- `quality_testing_evals`:
- `quality_strategy_present`:
- `risk_based_scope_present`:
- `test_first_or_gap_present`:
- `acceptance_traceability_present`:
- `contract_check_present`:
- `runtime_evidence_present`:
- `manual_qa_evidence_present`:
- `visual_a11y_evidence_present`:
- `eval_spec_present`:
- `eval_rerun_evidence_present`:
- `current_evidence_before_completion`:
- `ci_quality_gate_present`:
- `flaky_test_policy_present`:
- `coverage_policy_present`:
- `test_data_privacy_present`:
- `bug_reproduction_evidence_present`:
- `regression_impact_present`:
- Quality artifacts: `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, `manual-qa-evidence.md`
- Coverage is a signal, not proof:
- Quality status: `present_unverified | explicit_gap_accepted | approval_required`
- Frontend methodology:
- `frontend`:
- Artifacts: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, `frontend-performance-budget.md`
- Aliases: `ui-flow-spec.md`, `component-state-matrix.md`, `accessibility-review.md`
- Gates: `frontend_user_flow_acceptance_present`, `frontend_component_docs_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_fsd_boundary_reviewed`, `frontend_api_contract_alignment_present`, `frontend_accessibility_review_present`, `frontend_keyboard_focus_contract_present`, `frontend_responsive_viewport_matrix_present`, `frontend_visual_evidence_present`, `frontend_runtime_console_evidence_present`, `frontend_performance_budget_present`, `frontend_browser_support_present`, `frontend_content_i18n_boundary_present`, `frontend_interaction_test_evidence_present`
- Route params, auth/permission, SEO/meta:
- Token owner, variant policy:
- Local state, server-cache, persisted state:
- Browser/runtime evidence, console status, Playwright trace:
- Baseline owner, reduced motion, input modality, WCAG 2.2 AA, external visual service approval:
- Unsupported claims rejected: Storybook proves UI quality, desktop-only screenshot proves responsive UI, automated accessibility addon output is enough, lab Web Vitals always represent production UX, code inspection proves UI completion.
- Codex agentic workflow:
- `codex_agentic_workflow`:
- Runtime routes: Codex App, CLI, IDE extension, `codex exec`, GitHub Action, MCP, Agents SDK, automation
- `agentic_scope_classified`:
- `control_plane_present`:
- `source_of_truth_present`:
- `read_only_discovery_complete`:
- `model_reasoning_policy_present`:
- `fresh_context_handoff_present`:
- `ownership_split_present`:
- `subagent_parallelism_safe`:
- `approval_boundary_present`:
- `mcp_permission_review_present`:
- `hook_activation_approval_present`:
- `plugin_boundary_present`:
- `skill_promotion_evidence_present`:
- `automation_manual_stability_present`:
- `agent_eval_workflow_present`:
- `memory_policy_present`:
- `agentic_evidence_before_completion`:
- No silent activation:
- Memory as recall only:
- AI answer quality:
- Retrieval quality:
- Handoff quality:

## Thresholds

- Minimum passing score:
- Blocking failure:
- Regression tolerance:
- Latency threshold:
- Cost threshold:
- Grounding threshold:

## Artifacts

- Baseline:
- Current run:
- Diff or report:
- Reviewer notes:

## Behavioral Route Evals

- Prompt or scenario:
- Workspace fixture:
- Expected `usage_mode`:
- Expected minimum artifacts:
- Forbidden actions:
- Scenario status: `done | partial | pending | not_applicable`
- Residual risk:

## Acceptance Scenario Evals

- Acceptance scenarios:
- ATDD or BDD mapping:
- Requirement -> scenario -> check -> evidence owner:
- `requirements_scope_contract_present`:
- `requirements_owner_contract_present`:
- `requirement_quality_contract_present`:
- `requirement_ids_contract_present`:
- `acceptance_scenarios_contract_present`:
- `declarative_scenario_quality_contract_present`:
- `requirements_traceability_contract_present`:
- `business_rules_contract_present`:
- `non_goals_constraints_contract_present`:
- `constraints_traceability_contract_present`:
- `open_questions_contract_present`:
- `stakeholder_owner_map_contract_present`:
- `story_slice_map_contract_present`:
- `example_mapping_contract_present`:
- `domain_discovery_contract_present`:
- `domain_model_contract_present`:
- `bounded_context_trace_contract_present`:
- `ubiquitous_language_traceability_contract_present`:
- `invariants_failure_modes_contract_present`:
- `domain_event_contracts_present`:
- `api_ui_data_traceability_contract_present`:
- `domain_expert_review_contract_present`:
- `requirement_change_impact_contract_present`:
- `accepted_gap_contract_present`:
- `requirements_evidence_before_implementation_contract_present`:
- `unsupported_claims_rejected_contract_present`:
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
- Declarative acceptance scenarios (`declarative_acceptance_scenarios_present`): no UI selectors, database internals, function names, or test harness details.
- Requirements traceability (`requirements_traceability_present`): requirement -> scenario -> implementation -> check/eval -> evidence owner.
- Business rules (`business_rules_present`): source, owner, enforcement layer, exceptions, failure mode and tests/evals.
- Accepted gap (`accepted_gap_recorded`): owner, reason, scope, review date, downstream risk and follow-up condition.

## Domain Model Evals

- `domain_model_when_complex_domain`:
- `bounded_context_architecture_boundary_trace`:
- `ubiquitous_language_traceability`:
- Bounded context -> architecture boundary:
- Term-to-requirement:
- API/event/contract:
- UI label:
- Code module or owner:
- Accepted gap:
- Domain expert review:
- Domain expert or architecture owner:

## UI Architecture Evals

- `fsd_structure`:
- Feature-Sliced Design layer:
- Slice:
- Segment:
- Public API:
- Import rule:
- Backend/native/simple CRUD/simple MVP not applicable reason:
- UI owner review:

## Metric Hardening Evals

- `metric_hardening_when_product_behavior_changes`:
- Product hypothesis (`product_hypothesis_present`):
- Decision horizon (`decision_horizon_present`):
- Business outcome:
- Product outcome:
- Feature traction metric:
- Outcome metric level separated (`outcome_metric_level_separated`):
- Metric scope (`metric_scope_classified`):
- North Star or primary value metric:
- Input metric:
- Counter-metric:
- Proxy metric risk:
- Guardrail:
- Qualitative review:
- Qualitative feedback loop (`qualitative_feedback_loop_present`):
- Optional HEART metrics: Happiness, Engagement, Adoption, Retention, Task success.
- Analytics tracking plan (`analytics_tracking_plan_present`):
- Privacy classification:
- Privacy classification for metrics (`privacy_classification_for_metrics_present`):
- Retention period:
- Data minimization:
- Owner signoff:
- Post-release review evidence:
- Release measurement evidence (`release_measurement_evidence_present`):
- AI product eval gate (`ai_product_eval_when_ai_behavior_changes`):
- Value proposition evidence (`value_proposition_evidence_present`):
- Do not claim success from a proxy metric without counter-metric, guardrail, qualitative review, and post-release review evidence:

## Regression Notes

- Known regressions:
- Reproduction command:
- Owner:
- Next action:

## Unsupported Claims

- Claim:
- Missing source:
- Verification needed:
- Unsupported completion claim:
- Completion claim without current evidence:
<!-- product-agent-os:end evals -->
