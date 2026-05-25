# Component Card Template

Source status: `template`

Project: {project_name}

Owner: UI owner

## Operating Contract

- Evidence:
- Accepted Gap: use `explicit_gap_accepted` only with owner, reason, residual risk, review date and follow-up.
- Residual Risk:
- Approval Boundary: `approval_required` before external visual service approval, production-data screenshots, hosted browser runs or publication.
- Verification:
- Rollback or no-rollback rationale:
- No Secrets, credentials, tokens, raw private chats, production payloads or private customer data.

## Component

- Name:
- Layer or feature slice:
- Owner:
- Linked route, page, or flow:

## FSD Structure

- `fsd_structure` applicability: `required | not applicable | accepted gap`
- Feature-Sliced Design layer: `app | pages | widgets | features | entities | shared | not applicable`
- Slice:
- Segment:
- Public API:
- Import rule:
- Not applicable reason for backend, native, simple CRUD, or simple MVP work:

## Usage

- Purpose:
- Use when:
- Do not use when:
- Linked API contract:

## Interface

- Props or inputs:
- Events or outputs:
- Slots, children, or composition points:
- Public API:

## States

- Default:
- Loading:
- Empty:
- Error:
- Disabled:
- Success:
- Responsive:
- Keyboard and focus:

## Accessibility

- Native HTML first:
- ARIA only when needed:
- Focus behavior:
- Screen reader label:
- Contrast or motion concerns:

## Storybook

- Story file:
- Autodocs:
- MDX notes:
- Visual or accessibility check:

## Design System Governance

- Existing primitive reused:
- New primitive or variant:
- Token owner:
- Variant policy:
- Icon policy:
- Typography/spacing/theme rule:
- Breaking component API migration notes:

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
- Storybook proves UI quality is an unsupported claim
