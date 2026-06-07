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
- Runtime methodology packet (`methodology_packet`):
- `finish_options`:
- Owner questions:
- Safe next action:
- Evidence gaps:
- Approval boundary:
- Detection-only warning:
- Methodology detection is not completion evidence:
- No staged artifact from recommendation-only packet:

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
- Delivery, Release & Operations methodology (`delivery_release_operations`):
- Delivery readiness gate: `delivery_release_operations_readiness_when_release_or_operations_changes`
- Delivery artifacts: `release-readiness.md`, `versioning-policy.md`, `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `environment-matrix.md`, `deployment-plan.md`, `ci-cd-workflow-inventory.md`, `observability-map.md`, `slo-spec.md`, `operations-runbook.md`, `incident-record.md`, `postmortem.md`, `automation-candidate.md`, `post-release-review.md`
- Delivery gates checked: `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, `automation_manual_stability_present`
- Planning-first delivery classification:
- Release scope, version impact, release evidence before completion, artifact manifest, rollout, rollback/recovery, environment approval boundary, CI/CD governance, operations runbook, incident path and post-release measurement:
- External release approval:
- Observability release evidence:
- SLO or operational gap:
- Current build/test/docs/eval/runtime/artifact evidence:
- Approval boundary:
- `approval_required` before publish, tag, release creation, artifact upload, deployment, PR creation, branch push, package registry, marketplace, store submission or external CI/CD mutation:
- Automation manual stability: manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence and rollback/disable path:
- Automation candidate-only behavior:
- Active schedules remain out of scope:
- Automation activation gate: `activation_gate`, two successful manual runs, deterministic command evidence, owner approval, accepted residual risks, rollback/disable plan, `future_activation_handoff_required`, `schedule_status: not_created`, and no GitHub Actions, Codex App automation, hook activation or external write:
- Accepted gap (`explicit_gap_accepted`):
- Residual risk:
- Unsupported release claims rejected: release-ready without current evidence, feature flags remove release risk, GitOps is automatically safe, automation is safer because it is repeatable.
- Forbidden external actions checked: publish without approval, tag without approval, deployment without approval, active automation without manual stability.
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
- Cross-domain semantic evidence sufficiency (`semantic_evidence_sufficiency`):
- Applies to high-risk, production, release, security-sensitive, AI and public-contract work:
- Owner-reviewed evidence sufficient for real project risk (`owner_reviewed_evidence_sufficient_for_real_project_risk`):
- Accepted gap fields checked: `owner`, `reason`, `review_date`, `downstream_risk`, `follow_up_condition`
- Status checked: `present_unverified | explicit_gap_accepted | approval_required`
- FSD structure applicability (`fsd_structure`):
- Feature-Sliced Design layer/slice/segment:
- Public API:
- Import rule:
- FSD accepted gap or not applicable reason:
- Frontend methodology (`frontend`):
- Frontend artifacts: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, `frontend-performance-budget.md`
- Source aliases: `ui-flow-spec.md`, `component-state-matrix.md`, `accessibility-review.md`
- Frontend gates: `frontend_user_flow_acceptance_present`, `frontend_component_docs_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_fsd_boundary_reviewed`, `frontend_api_contract_alignment_present`, `frontend_accessibility_review_present`, `frontend_keyboard_focus_contract_present`, `frontend_responsive_viewport_matrix_present`, `frontend_visual_evidence_present`, `frontend_runtime_console_evidence_present`, `frontend_performance_budget_present`, `frontend_browser_support_present`, `frontend_content_i18n_boundary_present`, `frontend_interaction_test_evidence_present`
- Route params/auth/permission/SEO/meta coverage:
- Token owner/variant policy/design-system review:
- Local state/server-cache/persisted state boundaries:
- Browser/runtime evidence, console status and Playwright trace:
- Baseline owner, reduced motion, input modality, WCAG 2.2 AA and external visual service approval:
- Unsupported frontend claims rejected: Storybook proves UI quality, desktop-only screenshot proves responsive UI, automated accessibility addon output is enough, lab Web Vitals always represent production UX, code inspection proves UI completion.
- Backend methodology (`backend`):
- Backend artifacts: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, `backend-operational-runbook.md`
- Backend gates: `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_dependency_failure_matrix_present`, `backend_observability_contract_present`, `backend_slo_or_gap_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_strategy_present`, `backend_config_secrets_boundary_present`, `backend_security_reviewed`, `backend_rollback_plan_present`
- Runtime/failure evidence:
- Dependency failure matrix:
- Observability/SLO/health evidence:
- Health checks are tested where the platform/runtime is available:
- Health-check platform-unavailable gap owner, reason and follow-up:
- Documentation alone is not sufficient for deployable service health readiness:
- Job/queue and data consistency checks:
- Security and rollback evidence:
- Unsupported backend claims rejected: package docs do not prove backend runtime safety, logs-only observability, health-endpoint-only readiness, retries prove reliability, microservices by default.
- Backend accepted gap or `approval_required` status:
- API & Integrations methodology (`api_integrations`):
- API artifacts: `api-inventory.md`, `api-contract-review.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, `external-integration-approval.md`, `api-style-guide.md`
- API gates: `api_contract_source_present`, `api_consumer_map_present`, `api_breaking_change_reviewed`, `api_security_reviewed`, `api_error_contract_present`, `api_contract_test_matrix_present`, `event_delivery_contract_present`, `generated_client_manifest_present`, `external_write_approval_present`, `api_observability_contract_present`, `api_style_choice_recorded`, `api_unsupported_claims_rejected`
- Contract source and consumer map:
- Compatibility and breaking-change review:
- Security schemes, scopes, token claims, object-level authorization and rate limits:
- Error model with Problem Details or explicit compatibility gap:
- Contract test matrix, event delivery, generated SDK manifest and observability evidence:
- Unsupported API claims rejected: Swagger UI is not source of truth, schema validation alone is not contract testing, OAuth alone is not complete security evidence, GraphQL/gRPC/events are not universal defaults.
- External writes are `approval_required`:
- LLM / AI / RAG methodology (`llm_ai_rag`):
- LLM / AI / RAG readiness gate (`llm_ai_rag_readiness_when_ai_behavior_changes`):
- AI behavior promise:
- Baseline eval:
- Eval rerun:
- Eval rerun evidence:
- App-backed path:
- App-backed eval path:
- Dataset governance:
- Prompt/context inventory:
- AI/RAG artifacts: `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, agent task packet, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, `ai-cost-latency-budget.md`
- AI/RAG final-depth checks: handoff compatibility, eval tooling selector, model migration threshold, RAG deletion/privacy lifecycle, diff-signal limits, AI incident workflow and methodology report evidence/approval/gap/risk rendering:
- Retrieval metrics, grounding, context precision, context recall, failed cases and current-run evidence:
- Structured output, tool approval boundary, agent trace, safety evidence and cost evidence:
- Accepted-gap handling:
- Unsupported AI/RAG shortcuts rejected: prompt inspection is enough, ai quality claim without current eval evidence, citations alone prove grounding, model upgrade automatically improves quality.
- Database & Data methodology (`database_data`):
- Database checks cover database inventory, database dictionary, schema source, data contract, constraints, indexes, foreign keys, unique, not null, transaction boundary, expand-contract, backfill, dry run, rollback feasibility, backup restore evidence, PII, retention, deletion, data quality, Great Expectations, dbt tests, lineage, OpenLineage, query performance, destructive migration, DROP/rename/truncate, production access approval_required, and no production data in fixtures.
- Runtime pipeline and RAG ingestion signals stay `present_unverified`; schema-only artifact is not safety proof; do not access production data and do not run migration during tests without explicit approval.
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
- Codex agentic workflow (`codex_agentic_workflow`):
- Runtime routes: Codex App, CLI, IDE extension, `codex exec`, GitHub Action, MCP, Agents SDK, automation
- Gate `agentic_scope_classified`:
- Gate `control_plane_present`:
- Gate `source_of_truth_present`:
- Gate `read_only_discovery_complete`:
- Gate `model_reasoning_policy_present`:
- Gate `fresh_context_handoff_present`:
- Gate `ownership_split_present`:
- Gate `subagent_parallelism_safe`:
- Gate `approval_boundary_present`:
- Gate `mcp_permission_review_present`:
- Gate `hook_activation_approval_present`:
- Gate `plugin_boundary_present`:
- Gate `skill_promotion_evidence_present`:
- Gate `automation_manual_stability_present`:
- Gate `agent_eval_workflow_present`:
- Gate `memory_policy_present`:
- Gate `agentic_evidence_before_completion`:
- Status: `present_unverified | explicit_gap_accepted | approval_required`
- No silent activation:
- Memory as recall only:

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
- Baseline eval:
- Eval rerun evidence:
- App-backed eval path:
- Dataset governance:
- Prompt/context inventory:
- Grounding or citation checks:
- Retrieval metrics:
- Latency or cost thresholds:
- Current-run evidence:
- Accepted-gap handling:

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
