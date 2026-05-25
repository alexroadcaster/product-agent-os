# Frontend Performance Budget

Source status: `template`

Owner: performance owner

## Scope

Use this artifact for `frontend_performance_budget_present`, route budgets, LCP/INP/CLS target, lab vs field/RUM status and performance risk.

## Budget

| Route or screen | User journey | LCP target | INP target | CLS target | Measurement path | Lab vs field/RUM status | Risk | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | Lighthouse, Playwright trace, WebPageTest or RUM | TBD | TBD | TBD |

## Measurement

- Current command or report:
- Browser/OS:
- Viewport:
- Network/profile assumptions:
- Playwright trace:
- Field/RUM evidence:
- Explicit non-applicability:

## Frontend Shared Contract Terms

- `frontend_user_flow_acceptance_present`
- `frontend_component_docs_present`
- `frontend_component_state_matrix_present`
- `frontend_design_system_boundary_present`
- `frontend_fsd_boundary_reviewed`
- `frontend_api_contract_alignment_present`
- `frontend_accessibility_review_present`
- `frontend_keyboard_focus_contract_present`
- `frontend_responsive_viewport_matrix_present`
- `frontend_visual_evidence_present`
- `frontend_runtime_console_evidence_present`
- `frontend_performance_budget_present`
- `frontend_browser_support_present`
- `frontend_content_i18n_boundary_present`
- `frontend_interaction_test_evidence_present`
- `frontend-flow-spec.md`
- `frontend-state-matrix.md`
- `frontend-visual-qa.md`
- `frontend-accessibility-review.md`
- `frontend-performance-budget.md`
- `ui-flow-spec.md`
- `component-state-matrix.md`
- `accessibility-review.md`
- route params
- auth/permission
- SEO/meta
- token owner
- variant policy
- local state
- server-cache
- persisted state
- browser/runtime evidence
- console status
- Playwright trace
- baseline owner
- reduced motion
- input modality
- WCAG 2.2 AA
- external visual service approval
- Storybook proves UI quality is an unsupported claim

## Evidence

Record LCP, INP and CLS budget or explicit non-applicability, browser/runtime evidence, console status and Playwright trace or field/RUM evidence.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, scope, downstream risk, review date and follow-up condition.

## Residual Risk

Lab Web Vitals can diverge from production UX; missing budget can push performance review after release.

## Approval Boundary

`approval_required` before external monitoring setup, production telemetry, hosted performance service or external publication.

## Verification

Record measurement path, expected target, actual result, freshness, environment and owner review before release or performance claim.

## Rollback

Record rollback/no-rollback rationale for budget misses, feature flags, asset changes or performance accepted gaps.

## No Secrets

No Secrets, credentials, tokens, raw private chats, production payloads or private customer data in examples, fixtures, screenshots, stories or mocks.
