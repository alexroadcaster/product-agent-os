# Frontend State Matrix

Source status: `template`

Owner: UI owner

## Scope

Use this artifact for `frontend_component_state_matrix_present`, component/page states, Storybook state coverage and state ownership boundaries.

Alias mapping: `component-state-matrix.md` maps to `frontend-state-matrix.md`; Storybook story map fields can be recorded here for compact Product-Agent OS output.

## Visible States

| Component or route | Default | Loading | Skeleton | Empty | Error | Validation error | Success | Disabled | Focus | Permission denied | Offline/stale | Long content | Responsive | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## State Ownership

- Local state:
- Route state:
- Server-cache:
- Global state:
- Persisted state:
- Source of truth:
- Cache/stale behavior:
- Persistence risk:
- Accepted gap:

## Storybook

- Story file:
- Autodocs/MDX:
- Happy path:
- Loading/empty/error/disabled/focus/long-content stories:
- Interaction play function:
- Visual/accessibility state coverage:

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

Record Storybook, component test, interaction test, manual QA, browser/runtime evidence, console status and Playwright trace evidence.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, scope, downstream risk, review date and follow-up condition.

## Residual Risk

Missing state ownership can hide stale data, disabled/focus regressions and global state coupling.

## Approval Boundary

`approval_required` before external visual service, production data screenshot, remote browser run or publication.

## Verification

Record user-observable checks by role/name, keyboard input, click/tap, form submit and async state assertions.

## Rollback

Record rollback/no-rollback rationale for state behavior, component API or Storybook baseline changes.

## No Secrets

No Secrets, credentials, tokens, raw private chats, production payloads or private customer data in examples, fixtures, screenshots, stories or mocks.
