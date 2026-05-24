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
