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
- Runtime methodology packet:
- `methodology_packet`:
- `finish_options`:
- Owner questions:
- Safe next action:
- Evidence gaps:
- Approval boundary:
- Detection-only warning:
- Methodology detection is not completion evidence:
- No staged artifact from recommendation-only packet:
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
- Delivery, Release & Operations methodology:
- `delivery_release_operations`:
- `delivery_release_operations_contract_present`:
- `delivery_release_operations_readiness_when_release_or_operations_changes`:
- Delivery eval fields: `release_scope_contract_present`, `version_impact_contract_present`, `release_evidence_contract_present`, `release_evidence_before_completion_contract_present`, `artifact_manifest_contract_present`, `rollout_strategy_contract_present`, `rollback_recovery_contract_present`, `ci_cd_governance_contract_present`, `operations_runbook_contract_present`, `incident_response_contract_present`, `post_release_measurement_contract_present`, `automation_manual_stability_contract_present`, `unsupported_delivery_claims_rejected_contract_present`
- Delivery artifacts: `release-readiness.md`, `versioning-policy.md`, `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `environment-matrix.md`, `deployment-plan.md`, `ci-cd-workflow-inventory.md`, `observability-map.md`, `slo-spec.md`, `operations-runbook.md`, `incident-record.md`, `postmortem.md`, `automation-candidate.md`, `post-release-review.md`
- Planning-first delivery classification:
- Required evidence: release scope, version impact, release evidence before completion, artifact manifest, rollout, rollback/recovery, environment approval boundary, CI/CD governance, operations runbook, incident path, post-release learning, DORA/post-release measurement and approval boundary:
- External release approval:
- Observability release evidence:
- SLO or operational gap:
- Automation manual stability: manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence, rollback/disable path, automation candidate-only, active schedules remain out of scope:
- Statuses: `not_applicable | applicable_missing | present_unverified | present_verified | proposal_staged | explicit_gap_accepted | approval_required`
- Forbidden shortcuts: release-ready without current evidence, feature flags remove release risk, GitOps is automatically safe, automation is safer because it is repeatable.
- Forbidden external actions: publish without approval, tag without approval, deployment without approval, active automation without manual stability.
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
- Cross-domain semantic evidence sufficiency:
- `semantic_evidence_sufficiency`:
- `owner_reviewed_evidence_sufficient_for_real_project_risk`:
- Applies when: high-risk, production, release, security-sensitive, AI or public-contract work is in scope:
- Accepted gap fields: `owner`, `reason`, `review_date`, `downstream_risk`, `follow_up_condition`
- Statuses: `present_unverified | explicit_gap_accepted | approval_required`
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
- Backend methodology (`backend`):
- Backend artifacts: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, `backend-operational-runbook.md`
- Backend gates: `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_dependency_failure_matrix_present`, `backend_observability_contract_present`, `backend_slo_or_gap_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_strategy_present`, `backend_config_secrets_boundary_present`, `backend_security_reviewed`, `backend_rollback_plan_present`
- Backend eval fields: `backend_service_boundary_contract_present`, `backend_runtime_behavior_contract_present`, `backend_dependency_failure_matrix_contract_present`, `backend_observability_contract_present`, `backend_slo_or_gap_contract_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_contract_present`, `backend_config_secrets_boundary_contract_present`, `backend_security_review_contract_present`, `backend_rollback_plan_contract_present`, `unsupported_backend_claims_rejected_contract_present`
- Runtime/failure evidence:
- Owner reviewed evidence sufficiency:
- Owner reviewed test/eval/runtime evidence sufficiency:
- Real project risk:
- Accepted gap owner:
- Accepted gap reason:
- Review date:
- Downstream risk:
- Follow-up:
- T9-S shared semantic sufficiency backlog:
- Explicit accepted gap:
- Approval required:
- Forbidden shortcuts: package docs do not prove backend runtime safety, logs-only observability, health-endpoint-only readiness, retries prove reliability, microservices by default.
- API & Integrations methodology (`api_integrations`):
- API artifacts: `api-inventory.md`, `api-contract-review.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, `external-integration-approval.md`, `api-style-guide.md`
- API eval fields: `api_integrations_contract_present`, `api_contract_source_present`, `api_consumer_map_present`, `api_breaking_change_reviewed`, `api_security_reviewed`, `api_error_contract_present`, `api_contract_test_matrix_present`, `event_delivery_contract_present`, `generated_client_manifest_present`, `external_write_approval_present`, `api_observability_contract_present`, `api_style_choice_recorded`, `api_unsupported_claims_rejected`
- Contract source, consumer, compatibility, security, error, event, SDK and external-write evidence:
- Forbidden shortcuts: Swagger UI is not source of truth, schema validation alone is not contract testing, OAuth alone is not complete security evidence, GraphQL/gRPC/events are not universal defaults.
- External writes are `approval_required`; generated client publication, provider mutation and webhook registration need approval before external action.
- LLM / AI / RAG methodology (`llm_ai_rag`):
- LLM / AI / RAG eval fields: `llm_ai_rag_contract_present`, `llm_ai_rag_readiness_when_ai_behavior_changes`, `ai_behavior_promise_present`, `ai_baseline_eval_present`, `ai_eval_rerun_evidence_present`, `ai_dataset_governance_present`, `ai_prompt_contract_present`, `ai_model_decision_record_present`, `ai_structured_output_contract_present`, `ai_tool_contract_present`, `rag_source_inventory_present`, `rag_retrieval_config_present`, `rag_eval_report_present`, `agent_workflow_trace_present`, `ai_safety_review_present`, `ai_cost_latency_budget_present`, `ai_agent_handoff_contract_compatibility_present`, `ai_eval_tooling_selector_contract_present`, `ai_model_migration_policy_contract_present`, `rag_corpus_lifecycle_privacy_contract_present`, `ai_behavior_diff_signal_policy_contract_present`, `ai_incident_workflow_contract_present`
- AI behavior promise:
- Baseline eval:
- Eval rerun:
- Eval rerun evidence:
- App-backed path:
- App-backed eval path:
- Dataset governance:
- Prompt/context inventory:
- AI/RAG artifacts: `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, agent task packet, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, `ai-cost-latency-budget.md`
- AI/RAG final-depth eval: handoff compatibility, conditional eval tooling, model migration thresholds, RAG deletion/privacy lifecycle, workspace/intent-only diff-signal policy, AI incident workflow and report evidence/approval/gap/risk rendering:
- Retrieval metrics, grounding, context precision, context recall, failed cases and current-run evidence:
- Structured output, tool approval boundary, agent trace, safety evidence and cost evidence:
- Accepted-gap handling:
- Forbidden shortcuts: prompt inspection is enough, ai quality claim without current eval evidence, citations alone prove grounding, model upgrade automatically improves quality.
- Database & Data methodology (`database_data`):
- Database eval fields: `database_data_contract_present`, `database_inventory_contract_present`, `database_dictionary_contract_present`, `database_schema_source_contract_present`, `database_migration_plan_contract_present`, `database_backup_restore_contract_present`, `database_constraints_integrity_contract_present`, `database_production_access_approval_contract_present`, and `unsupported_database_claims_rejected_contract_present`
- Database eval rejects schema-only artifact is not safety proof, production access without approval_required, destructive migration without rollback/backup evidence, and runtime pipeline/RAG ingestion claims that are not `present_unverified` or verified by current evidence.
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
