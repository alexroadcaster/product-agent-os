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
