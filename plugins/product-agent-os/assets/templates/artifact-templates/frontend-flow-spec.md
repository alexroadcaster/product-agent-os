# Frontend Flow Spec

Source status: `template`

Owner: UI owner

## Scope

Use this artifact for `frontend_user_flow_acceptance_present`, route/page flow, route params, auth/permission, data dependency, SEO/meta and content/i18n boundaries before UI implementation or completion claims.

Alias mapping: `ui-flow-spec.md` maps to `frontend-flow-spec.md`; `route-page-inventory.md` maps here for compact Product-Agent OS output.

## Flow

| User goal | Route or screen | Route params | Acceptance scenario | Visible state path | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | default/loading/error/success | TBD | `present_unverified` |

## Route And Data Inventory

- Route params:
- Data dependencies:
- Linked API contract:
- Auth/permission:
- SEO/meta:
- Feature flags:
- Cache/stale/pagination:

## Content And I18n

- Long text:
- User-generated content:
- Wrapping/truncation:
- Localization:
- Pluralization:
- RTL/locales:
- Non-overlap assumptions:

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

Record linked acceptance scenario, screenshots, browser/runtime evidence, console status, Playwright trace, current command evidence or explicit gap.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, scope, downstream risk, review date and follow-up condition.

## Residual Risk

Missing route/page and content evidence can make a component appear complete while the actual user flow breaks.

## Approval Boundary

`approval_required` before external browser services, production-data screenshots, analytics writes, hosted visual uploads or external publication.

## Verification

Record current browser/dev-server or preview URL/context, viewport, browser/OS, console status and linked test or manual evidence.

## Rollback

Record rollback or no-rollback rationale for UI routing, copy, SEO/meta or auth/permission behavior.

## No Secrets

No Secrets, credentials, tokens, raw private chats, production payloads or private customer data in examples, fixtures, screenshots, stories or mocks.
