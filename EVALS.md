# EVALS.md

<!-- product-agent-os:start evals -->
Project: Codex Docs / Product-Agent OS
Generated at: 2026-05-24

## Rubrics

- Source grounding: official sources and checked-in docs drive durable rules; community claims stay in insight/research layer.
- Methodology applicability: gates are conditional and can be marked not applicable or accepted gap.
- Evidence-before-completion: implemented in `T8-A16`; no ready/completed/fixed/works/release claim without current command evidence, current eval evidence, current runtime evidence or explicit inspection-only gap.
- Architecture boundary: implementation stays inside named files and ownership boundaries.
- Domain traceability: complex domain work links domain model, bounded contexts, architecture boundary and ubiquitous language terms.
- Documentation quality: user-facing docs are Russian, behavior-level, and name inputs, outputs, verification, risks and next artifact.

## Thresholds

- Blocking failure: unit test failure, fixture eval failure, docs check failure, strict MkDocs failure after nav/MkDocs-sensitive docs changes, or Codex compatibility regression.
- Accepted gap: allowed only when reason, owner, evidence owner and follow-up are explicit.
- Residual risk: must be carried into `RUNLOG.md` and final response.

## Behavioral Route Evals

- Scenario workflows through `T8-S16`: implemented.
- No-placeholder planning, two-stage review, fresh-context handoff, acceptance scenarios, conditional DDD domain model and bounded-context traceability: implemented.
- Ubiquitous language traceability: implemented in `T8-A7`.
- FSD structure routing: implemented in `T8-A8`.
- Metric hardening: implemented in `T8-A9`.
- Evidence-before-completion: implemented in `T8-A16`.
- Docs tooling selector and `docs_as_code_impact` applicability statuses: implemented in `T8-C`.
- Conditional readiness gates: implemented in `T8-F`.
- Scenario, behavioral eval and Codex compatibility docs: implemented in `T8-H`.
- Transcript/session eval replay: implemented in `T8-GY`.
- Standards trigger policy: implemented in `T8-B`.
- False-positive scenario fixture coverage: implemented in `T8-GX`.
- Detailed discovery status depth: implemented in `T8-D`.

## Completion Evidence Evals

- `evidence_before_completion`: implemented in `T8-A16`.
- Required evidence: ready claim, completed claim, fixed claim, works claim and release claim need current command evidence, current eval evidence, current runtime evidence or explicit test gap.
- Inspection-only: answers based only on code inspection must stay labeled `inspection-only` and list unsupported completion claim.
- Residual risk: the gate proves evidence is recorded, not that manually interpreted evidence is semantically sufficient.

## Domain Model Evals

- `domain_model_when_complex_domain`: implemented in `T8-A5`.
- `bounded_context_architecture_boundary_trace`: implemented in `T8-A6`.
- `ubiquitous_language_traceability`: implemented in `T8-A7`.
- Human domain/architecture review remains required for conceptual correctness.

## UI Architecture Evals

- `fsd_structure`: implemented in `T8-A8`.
- False-positive protection: backend, native, simple CRUD and simple MVP work must not be forced into Feature-Sliced Design.
- Residual risk: directory detection does not prove architecture quality; owner review is still required for public API and import rule correctness.

## Metric Hardening Evals

- `metric_hardening_when_product_behavior_changes`: implemented in `T8-A9`.
- Required evidence: North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff and post-release review evidence.
- Residual risk: metric artifacts reduce proxy-metric and telemetry risk, but a product owner still needs to validate whether the selected metric actually reflects user value.

## Docs Tooling Evals

- `docs_tooling_selector`: implemented in `T8-C`.
- `docs_as_code_impact`: supports `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required`.
- Required evidence: selected tools, rejected tools, evidence owner, maintenance owner, commands, accepted gap or approval boundary.
- False-positive protection: docs-light and internal-only projects are not forced into MkDocs, Docusaurus, Sphinx, Antora, hosted docs, CI activation or DB introspection.
- Residual risk: selector evidence is route and artifact evidence; owners still need to validate whether a chosen docs tool is operationally worth maintaining.

## Conditional Readiness Evals

- `conditional_readiness_gates_contract_present`: implemented in `T8-F`.
- `readiness_statuses`: `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required`.
- Required evidence: every gate has `applies_when`, pass condition, accepted gap, required evidence, owner and residual risk.
- False-positive protection: detection alone can only support `present_unverified`; applicable gates without evidence are `applicable_missing`, not ready.
- Residual risk: the contract proves readiness evidence is structured; owners still need to judge whether the evidence is sufficient for the actual project risk.

## Scenario Documentation Evals

- `test_product_agent_os_docs`: implemented in `T8-H`.
- Required evidence: dedicated scenario, behavioral eval and Codex compatibility pages have Source status, Inputs, Outputs, Verification and Risks.
- Navigation evidence: MkDocs nav and `tools/check_docs.py` required paths include the new pages.
- Residual risk: docs describe route and eval contracts; transcript/session replay catches deterministic term/shortcut/privacy failures but does not replace semantic reviewer judgment.

## Transcript Session Evals

- `evaluate_transcript_sessions`: implemented in `T8-GY`.
- Required evidence: each synthetic or redacted session maps to `behavioral_case`, has `expected_terms`, optional `forbidden_terms`, and produces `missing_expected_terms`, `forbidden_terms_present` and `privacy_errors`.
- Runner evidence: `run_transcript_eval.py` exits `0` only when every session passes and exits `1` when expected evidence is missing, forbidden behavior appears or unsafe transcript content is retained.
- Residual risk: deterministic replay is stable and local, but it is not a calibrated LLM-as-judge for nuanced conversation quality.

## Standards Trigger Evals

- `standards_trigger_policy`: implemented in `T8-B`.
- Required evidence: ADR trigger policy, C4/arc42 applicability, OpenAPI source of truth, AsyncAPI event contract, SemVer impact, Keep a Changelog categories, CODEOWNERS status, GitHub Actions least privilege, `governance-proposal.md` and no forced external activation.
- Fixture evidence: `standards_trigger_contract_present` in `run_fixture_eval.py`.
- Residual risk: the contract proves standards applicability is recorded; owners still need to decide whether an ADR, diagram, governance proposal or release category is proportionate for the real project.

## False-Positive Fixture Evals

- `T8-GX`: implemented.
- Required evidence: `backend-no-fsd`, `native-no-fsd`, `simple-crud-no-ddd`, `docs-light-no-portal` and `hosted-docs-approval` are synthetic, secret-free fixtures with named expected checks in `run_fixture_eval.py`.
- Fixture evidence: `fsd_structure_not_detected_for_backend`, `fsd_structure_not_detected_for_native`, `domain_model_not_forced_for_simple_crud`, `docs_light_does_not_select_heavy_portal` and `hosted_docs_and_db_introspection_require_approval`.
- Residual risk: false-positive fixtures prove routing boundaries for selected synthetic workspaces; they do not prove every real project-specific methodology decision.

## Detailed Discovery Status Evals

- `T8-D`: implemented.
- Required evidence: `methodology_applicability` is present in discovery output with packets for architecture boundary, test/eval-first evidence, docs-as-code ownership, product measurement, complex-domain DDD, applicable FSD structure, docs tooling decision and standards trigger policy.
- Fixture evidence: `methodology_applicability_contract_present` in `run_fixture_eval.py`.
- Residual risk: discovery packets structure methodology/tooling applicability; owners still need to validate semantic quality and sufficiency of the evidence for the real project.

## Unsupported Claims

- Claim:
- Missing source:
- Verification needed:
<!-- product-agent-os:end evals -->
