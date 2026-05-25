# PLAN.md

<!-- product-agent-os:start plan -->
Project: {project_name}
Workspace: {workspace_path}
Profile: {profile_name}
Detected stack: {detected_stack_text}
Generated at: {generated_at}

## Lifecycle State

- Current phase:
- Entry criteria:
- Exit criteria:
- Stop condition:

## Usage Mode Overlay

- Primary `usage_mode`:
- Scenario status: `done | partial | pending | not_applicable`
- Minimum artifacts required before build:
- Packaged workflow available:
- Missing workflow or template gap:
- First response contract:
- Approval boundary:

## Implementation Slices

- Slice:
- User value:
- Product hypothesis or metric:
- Product hypothesis gate (`product_hypothesis_present`):
- Decision horizon (`decision_horizon_present`): `discovery | MVP | beta | production | scale`
- Business outcome:
- Product outcome:
- Feature traction metric:
- Outcome metric level separated (`outcome_metric_level_separated`):
- Metric scope (`metric_scope_classified`): `required | not_applicable | accepted_gap`
- Architecture boundary:
- Exact files:
- Owned files:
- Forbidden files:
- Test-first or eval-first path:
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
- Metric hardening applicability (`metric_hardening_when_product_behavior_changes`):
- North Star or primary value metric:
- Input metric:
- Counter-metric:
- Proxy metric risk:
- Value proposition evidence (`value_proposition_evidence_present`):
- Analytics tracking plan (`analytics_tracking_plan_present`):
- Qualitative feedback loop (`qualitative_feedback_loop_present`):
- Release measurement evidence (`release_measurement_evidence_present`):
- No-production-telemetry fallback:
- Guardrail:
- Qualitative review:
- Privacy classification:
- Retention period:
- Data minimization:
- Owner signoff:
- Post-release review evidence:
- FSD structure applicability (`fsd_structure`):
- Feature-Sliced Design layer/slice/segment:
- Public API:
- Import rule:
- FSD accepted gap or not applicable reason:
- Frontend methodology (`frontend`):
- Frontend flow artifact: `frontend-flow-spec.md` (`ui-flow-spec.md` alias)
- Frontend state artifact: `frontend-state-matrix.md` (`component-state-matrix.md` alias)
- Frontend visual QA artifact: `frontend-visual-qa.md`
- Frontend accessibility artifact: `frontend-accessibility-review.md` (`accessibility-review.md` alias)
- Frontend performance artifact: `frontend-performance-budget.md`
- Frontend gates: `frontend_user_flow_acceptance_present`, `frontend_component_docs_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_fsd_boundary_reviewed`, `frontend_api_contract_alignment_present`, `frontend_accessibility_review_present`, `frontend_keyboard_focus_contract_present`, `frontend_responsive_viewport_matrix_present`, `frontend_visual_evidence_present`, `frontend_runtime_console_evidence_present`, `frontend_performance_budget_present`, `frontend_browser_support_present`, `frontend_content_i18n_boundary_present`, `frontend_interaction_test_evidence_present`
- Route params, auth/permission, SEO/meta, token owner, variant policy, local state, server-cache and persisted state:
- Browser/runtime evidence, console status, Playwright trace, baseline owner, reduced motion, input modality, WCAG 2.2 AA and external visual service approval:
- Unsupported frontend claims: Storybook proves UI quality, desktop-only screenshot proves responsive UI, automated accessibility addon output is enough, lab Web Vitals always represent production UX, code inspection proves UI completion.
- Backend methodology (`backend`):
- Backend artifacts: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, `backend-operational-runbook.md`
- Backend gates: `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_dependency_failure_matrix_present`, `backend_observability_contract_present`, `backend_slo_or_gap_present`, `backend_health_probe_contract_present`, `backend_job_queue_contract_present`, `backend_data_consistency_strategy_present`, `backend_config_secrets_boundary_present`, `backend_security_reviewed`, `backend_rollback_plan_present`
- Runtime/failure evidence, dependency failure matrix, observability/SLO/health evidence, job/queue contract, data consistency strategy, security review and rollback/replay evidence:
- Unsupported backend shortcuts rejected: package docs do not prove backend runtime safety, logs-only observability, health-endpoint-only readiness, retries prove reliability, and microservices by default.
- Backend accepted gap: use `explicit_gap_accepted` only with owner, reason, review date, downstream risk and follow-up condition; use `approval_required` before production data, external writes, secrets, deploy actions or irreversible side effects.
- API & Integrations methodology (`api_integrations`):
- API artifacts: `api-inventory.md`, `api-contract-review.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, `external-integration-approval.md`, `api-style-guide.md`
- API gates: `api_contract_source_present`, `api_consumer_map_present`, `api_breaking_change_reviewed`, `api_security_reviewed`, `api_error_contract_present`, `api_contract_test_matrix_present`, `event_delivery_contract_present`, `generated_client_manifest_present`, `external_write_approval_present`, `api_observability_contract_present`, `api_style_choice_recorded`, `api_unsupported_claims_rejected`
- Contract source, consumers, compatibility, security schemes, error examples, event delivery, generated SDK manifest, request ID, correlation ID and external-write approval evidence:
- Unsupported API shortcuts rejected: Swagger UI is not source of truth, schema validation alone is not contract testing, OAuth alone is not complete security evidence, GraphQL/gRPC/events are not universal defaults.
- API accepted gap: use `explicit_gap_accepted` only with owner, reason, review date, downstream consumer risk and follow-up condition; external writes are `approval_required`.
- Ubiquitous language traceability (`ubiquitous_language_traceability`):
- Term-to-requirement trace:
- API/event/contract:
- UI label:
- Code module or owner:
- Domain expert review:
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
- Domain expert review (`domain_expert_review_present`): `domain-review-record.md`
- Requirement change impact review (`requirement_change_impact_review_present`): `requirement-change-impact.md`
- Accepted gap recorded (`accepted_gap_recorded`):
- Requirements evidence before implementation (`requirements_evidence_before_implementation`):
- Exact commands:
- Expected outputs:
- Evidence owner:
- Verification command:
- Conditional readiness gates:
- Readiness statuses (`readiness_statuses`): `not_applicable | applicable_missing | present_unverified | present_verified | proposal_staged | explicit_gap_accepted | approval_required`
- Gate id:
- Applies when:
- Applicability reason:
- Required evidence:
- Status:
- Owner:
- Accepted gap:
- Residual risk:
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

## Codex Agentic Workflow

- Methodology: `codex_agentic_workflow`
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

## Plan Quality Gate

- No-placeholder contract:
- Plan quality gate status: `pending | passed | blocked | mechanical_change`
- Non-trivial slice:
- Exact files:
- Owned files:
- Forbidden files:
- Exact commands:
- Expected outputs:
- Rollback:
- Evidence owner:
- Placeholder scan:
- Vague validation:
- Repeated-by-reference:
- Commands without expected outputs:
- Mechanical_change reason:
- Plan repair:
- Stop before build:

## Ownership

- Owner:
- Reviewer:
- File ownership boundaries:
- Parallel work conflicts:

## Dependencies

- Source context:
- Runtime or tooling:
- External approvals:
- Blockers:

## Methodology Gates

- Product/data gate: hypothesis, metric, and measurement plan are clear or marked not applicable.
- Business/Product gate: product_hypothesis_present, value_proposition_evidence_present, decision_horizon_present, outcome_metric_level_separated, metric_scope_classified, analytics_tracking_plan_present, qualitative_feedback_loop_present, and release_measurement_evidence_present are satisfied or explicitly gapped before behavior-changing implementation.
- Metric hardening gate: `metric_hardening_when_product_behavior_changes` requires a North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence for product behavior changes. Do not claim success from a proxy metric without the counter evidence.
- Architecture gate: slice boundary, dependency rule, public contract, and ownership are clear.
- Domain model gate: `domain_model_when_complex_domain` is satisfied or explicitly not applicable for simple CRUD/MVP work.
- Bounded context trace gate: `bounded_context_architecture_boundary_trace` maps every bounded context to an architecture boundary or accepted gap.
- Ubiquitous language trace gate: `ubiquitous_language_traceability` maps every domain term through term-to-requirement evidence and at least one API/event/contract, UI label, code module or owner, or accepted gap with domain expert review.
- Requirements & Domain gate: `requirements_scope_present`, `requirements_owner_present`, `requirement_quality_present`, `requirement_ids_present`, `requirements_traceability_present`, `business_rules_present`, `non_goals_constraints_present`, `constraints_traceability_present`, `open_questions_recorded`, `declarative_acceptance_scenarios_present`, `domain_event_contracts_present`, `api_ui_data_traceability_present`, `domain_expert_review_present`, `requirement_change_impact_review_present`, `accepted_gap_recorded`, and `requirements_evidence_before_implementation` are satisfied, explicitly not applicable, or accepted as gaps before implementation.
- Requirements artifacts gate: `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `domain-review-record.md`, and `requirement-change-impact.md` are staged when their gates apply.
- Declarative scenario gate: `declarative_acceptance_scenarios_present` rejects UI selectors, database internals, function names and test harness details in business-facing scenarios.
- Accepted gap gate: `accepted_gap_recorded` requires owner, reason, scope, review date, downstream risk and follow-up condition.
- Requirement change gate: `requirement_change_impact_review_present` reviews affected tests/evals, API, DB, UI, docs, rollout, rollback and approval boundary.
- FSD structure gate: `fsd_structure` applies only to web UI/component architecture with FSD-like layer directories or explicit owner decision; backend, native, simple CRUD, and simple MVP work record not applicable or accepted gap.
- Test gate: deterministic tests, contract checks, evals, or accepted gaps are named before implementation.
- Documentation gate: required docs-as-code artifacts and source-of-truth updates are named.
- Docs tooling gate: `docs_tooling_selector` records `docs_as_code_impact`, `docs-tooling-decision.md`, selected tools, rejected tools, `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, `approval_required`, evidence owner, maintenance owner, no forced install, no CI activation without approval, hosted docs approval, DB introspection approval, and any docs-light or internal-only reason.
- Standards trigger gate: `standards_trigger_policy` records ADR trigger policy, C4/arc42 applicability, OpenAPI source of truth, AsyncAPI contract, SemVer impact, Keep a Changelog categories, CODEOWNERS status, GitHub Actions least privilege, `governance-proposal.md`, no external activation without approval, and no forced external activation.
- Review gate: security, privacy, performance, migration, and rollback risks are reviewable.
- Scenario gate: current `usage_mode` has the required minimum artifacts, or a partial/pending evidence gap is explicit before implementation.
- Conditional readiness gates: every applicable gate records `applies_when`, required evidence, status, owner, accepted gap, and residual risk. Detection alone can only produce `present_unverified`; missing evidence is `applicable_missing`; verified command/owner evidence is required for `present_verified`; low-scope exclusions are `not_applicable` with an applicability reason; accepted gaps are `explicit_gap_accepted`; external or irreversible actions are `approval_required`.
- Evidence-before-completion gate: `evidence_before_completion` blocks a ready claim, completed claim, fixed claim, works claim, or release claim unless the plan names current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, record `inspection-only`, unsupported completion claim, and completion claim without current evidence as blocked.

## Risks

{risk_text}

## Rollback

- Revert only files owned by the current slice.
- Preserve verification evidence and failure notes in `RUNLOG.md`.

## Verification Gates

- Deterministic checks:
- Runtime or visual checks:
- Contract or schema checks:
- Documentation checks:
- Eval or LLM-as-judge checks:
- Manual acceptance:
- Evidence location:
- Current command evidence:
- Current eval evidence:
- Current runtime evidence:
- Inspection-only result and explicit test gap:

## Approval Needs

- Sandbox or filesystem approvals:
- Network or external system approvals:
- Release approvals:
<!-- product-agent-os:end plan -->
