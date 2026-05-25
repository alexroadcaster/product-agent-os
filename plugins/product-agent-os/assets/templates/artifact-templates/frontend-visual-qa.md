# Frontend Visual QA

Source status: `template`

Owner: tester or UI owner

## Scope

Use this artifact for `frontend_visual_evidence_present`, `frontend_runtime_console_evidence_present`, responsive evidence, browser support and visual baseline stability.

## Runtime Evidence

| Context | URL or command | Browser/OS | Viewport | Console status | Network/runtime errors | Screenshot or trace | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dev-server or preview | TBD | TBD | TBD | TBD | TBD | Playwright trace or screenshot | TBD | `present_unverified` |

## Responsive Matrix

- Mobile viewport:
- Desktop viewport:
- Tablet by risk:
- Orientation:
- Input modality:
- Reduced motion/preferences:
- Theme/dark mode:
- Long text/user-generated content:
- Non-overlap assumptions:

## Visual Baseline Stability

- Baseline owner:
- OS/browser/hardware/rendering environment:
- Viewport list:
- Known noisy diffs:
- Baseline update rule:
- External visual service approval:
- Privacy-safe screenshot/story/mock constraints:

## Browser Support

- Supported browsers:
- Supported devices/webviews:
- Playwright projects:
- Known gaps:
- Fallback:

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

Record privacy-safe screenshots, Storybook visual baseline, Playwright screenshot comparison, browser/runtime evidence, console status and Playwright trace.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, scope, downstream risk, review date and follow-up condition.

## Residual Risk

Desktop-only or unstable visual evidence can miss responsive, theme, preference and runtime regressions.

## Approval Boundary

`approval_required` before external visual service, hosted screenshot upload, browser farm, production-data screenshot or external publication.

## Verification

Record current command, browser/OS, viewport, trace path, console status and result before any UI completion claim.

## Rollback

Record rollback/no-rollback rationale for baseline update, visual diff acceptance or browser support gap.

## No Secrets

No Secrets, credentials, tokens, raw private chats, production payloads or private customer data in examples, fixtures, screenshots, stories or mocks.
