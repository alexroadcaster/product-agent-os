# Frontend Accessibility Review

Source status: `template`

Owner: accessibility owner

## Scope

Use this artifact for `frontend_accessibility_review_present`, `frontend_keyboard_focus_contract_present`, WCAG target, semantic controls, labels/names, focus and error behavior.

Alias mapping: `accessibility-review.md` maps to `frontend-accessibility-review.md`; `keyboard-focus-map.md` maps here for compact Product-Agent OS output.

## Accessibility Target

- Default target for public UI: WCAG 2.2 AA.
- Accepted exception:
- Product/legal risk level:
- Automated check limitations:

## Keyboard And Focus

| UI pattern | Tab order | Visible focus | Trap/release | Escape behavior | Accessible name | Error announcement | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | `present_unverified` |

## Semantic And Content Checks

- Native HTML first:
- ARIA only when needed:
- Labels/names:
- Semantic controls:
- Error announcements:
- Contrast:
- Motion concerns:

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

Record manual keyboard/focus review, automated check output, screen-reader relevant notes, browser/runtime evidence, console status and Playwright trace where available.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, scope, downstream risk, review date and follow-up condition.

## Residual Risk

Automated accessibility output alone can miss keyboard, focus, semantic and error-announcement failures.

## Approval Boundary

`approval_required` before external accessibility services, production-data screenshots, regulated/public-risk exceptions or publication.

## Verification

Record keyboard path, focus behavior, accessible names, semantic controls, labels, error announcements and contrast evidence or explicit gap.

## Rollback

Record rollback/no-rollback rationale for accessibility exceptions, component API changes or accepted gaps.

## No Secrets

No Secrets, credentials, tokens, raw private chats, production payloads or private customer data in examples, fixtures, screenshots, stories or mocks.
