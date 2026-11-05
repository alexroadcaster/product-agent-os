---
title: "Archive - Frontend Methodology Research"
---

# Archive - Frontend Methodology Research {#frontend-methodology-research}

> Historical source record. Dates and verdicts below describe that run; use current guides for present behavior.

Source status: `official + verified methodology + tool-assisted`

Research date: `2026-05-24`

Target methodology page: [../../methodologies/frontend.md](../../methodologies/frontend.md)

Target Product-Agent OS behavior: detect frontend work, require user-flow and component-state clarity, route UI changes through accessibility, responsive, visual, performance and API-contract gates, and require browser/runtime evidence before completion claims.

## Scope

This dossier covers frontend applications, UI routes/screens, reusable components, design systems, Storybook documentation, accessibility, responsive behavior, browser automation, visual regression, Core Web Vitals and UI-facing API dependencies.

It does not mandate React, Next.js, Storybook, Feature-Sliced Design or Playwright for every project. These are conditional practices selected by product scale, team workflow, risk, runtime and existing stack.

## Supported facts

- Feature-Sliced Design defines frontend architecture through layers, slices and segments. Its layer import rule allows a module in a slice to import other slices only from strictly lower layers, while the public API rule keeps external imports from depending on internal slice structure.
- Storybook Autodocs generates component documentation from stories tagged with `autodocs` and can be extended with MDX and Doc Blocks.
- Storybook interaction tests use stories and `play` functions to simulate user behavior such as clicks, typing and form submission, then assert the resulting UI behavior.
- Storybook visual tests turn stories into visual regression checks by comparing current snapshots with known good baselines.
- Playwright Test can generate and compare screenshots with `toHaveScreenshot()`, but screenshot baselines are sensitive to OS, browser, hardware and rendering environment.
- Playwright Trace Viewer is a GUI for inspecting recorded traces after test runs; traces help debug CI failures and can include actions, DOM snapshots, screenshots, network activity and console evidence.
- WCAG 2.2 is a W3C Recommendation. It provides testable accessibility success criteria organized around perceivable, operable, understandable and robust principles.
- WAI-ARIA Authoring Practices Guide documents accessible design patterns, ARIA roles/states/properties, keyboard support, accessible names and landmark usage.
- MDN guidance emphasizes semantic HTML, native controls, labels, source order and keyboard accessibility as the default foundation for accessible UI.
- MDN media query documentation supports responsive behavior through device/media characteristics such as viewport width, orientation, input capability and user preferences.
- Testing Library's guiding principle is to test software in a way that resembles how users use it; this supports accessibility-oriented queries and behavior-focused UI tests.
- web.dev lists current Core Web Vitals as LCP, INP and CLS, covering loading, interactivity and visual stability. INP is now the stable responsiveness metric replacing the older FID model.

## Methodologies

| Methodology | When to apply | Project-level behavior |
| --- | --- | --- |
| User-flow-first UI development | Any user-visible UI change | Start from route/screen, user goal, acceptance scenario, empty/loading/error/success path and expected evidence. |
| Component-driven development | Reusable components, design systems or repeated UI patterns | Stories capture component states, props, events, accessibility notes and visual examples. |
| Design-system-driven development | Product has tokens, shared components or brand rules | Use existing tokens/components first; document new variants, icons, spacing and typography decisions. |
| Conditional Feature-Sliced Design | Growing frontend with feature/business boundaries | Use layers/slices/public API/import rules when they reduce navigation and coupling cost. |
| Accessibility-first / inclusive design | Interactive, public, regulated, high-use or form-heavy UI | Keyboard, focus, labels, names, errors, contrast, semantics and assistive technology patterns are acceptance criteria. |
| Responsive/adaptive design | UI must work across viewport/input contexts | Define viewport matrix, content behavior, touch/mouse/keyboard assumptions and reduced-motion/preference handling. |
| Interaction-first testing | UI behavior depends on user actions | Test through user-observable behavior, not component internals. |
| Visual regression testing | Layout, styling or component states can regress silently | Capture screenshot/story baselines and compare stable viewport states. |
| Performance-by-design | Routes are user-facing, high-traffic or interaction-heavy | Define LCP/INP/CLS budget or explicit gap, then collect lab/field evidence as available. |
| API-contract-aware frontend development | UI depends on backend, API, feature flags or async data | Map UI states to contract examples, error shapes, pagination, permissions and stale/loading behavior. |
| State ownership design | Cross-component, cache or form state is non-trivial | Name local, route, server-cache, global and persistent state boundaries. |
| Content and i18n-ready UI | Long text, localization or user-generated content can break layout | Check truncation, wrapping, pluralization, empty copy, RTL/locales where applicable and non-overlap. |
| Evidence-before-completion | Any UI work claimed complete | Provide browser/runtime evidence, console status, screenshots or explicit verification gap. |

## Documentation artifacts and standards

| Artifact | Purpose | Candidate source/tool |
| --- | --- | --- |
| UI flow spec | User goal, route/screen, acceptance scenario and state paths. | `ui-flow-spec.md`, `REQUIREMENTS.md` |
| Route/page inventory | Pages, route params, data dependencies, auth/permission assumptions and SEO/meta notes. | Router docs, C4/container map |
| Component card | Purpose, props, events, states, accessibility, linked API and owner. | `component-card.md` |
| Component state matrix | Default/loading/empty/error/success/disabled/focus/responsive/long-text states. | Storybook stories, markdown table |
| Storybook story map | Which stories cover which components, variants and states. | Storybook CSF, Autodocs, MDX |
| Design system inventory | Tokens, components, variants, icons, typography, spacing and theme constraints. | Design tokens, Storybook, Figma/Open Design |
| Frontend boundary map | Page/widget/feature/entity/shared boundaries and public imports. | FSD, ADR, Mermaid |
| API dependency map | Endpoint/query/mutation/event, contract examples, auth, errors and cache behavior. | OpenAPI/AsyncAPI/Pact, mocks |
| Responsive viewport matrix | Desktop/tablet/mobile, orientation, input modality and reduced-motion/preference checks. | MDN media queries, Playwright projects |
| Accessibility review | WCAG level target or gap, semantic HTML, keyboard, focus, labels, names, errors and contrast. | WCAG 2.2, WAI-ARIA APG, axe/Storybook addon |
| Keyboard and focus map | Tab order, focus trap/release, modal/menu/listbox/dialog behavior and visible focus states. | WAI-ARIA APG |
| Visual evidence packet | Screenshot paths, viewport list, baseline reference, browser/OS and console status. | Playwright, Storybook visual tests |
| Interaction test matrix | User actions, expected UI state, role/name queries and async behavior. | Storybook `play`, Testing Library, Playwright |
| Performance budget | LCP/INP/CLS target or explicit non-applicability, measurement method and risk. | web.dev Core Web Vitals |
| Browser support matrix | Supported browsers/devices, known gaps and feature fallback. | Browserslist, Playwright projects |
| Content/i18n record | Long strings, localization, empty copy, pluralization, RTL and truncation behavior. | Product copy/i18n docs |

## Project application instructions

1. Classify the work: route/page, component, design-system primitive, layout, interaction, state, data-fetching UI, performance fix or accessibility fix.
2. Start with the user flow. Record user goal, acceptance scenario, primary route/screen and visible state transitions.
3. Name all UI states before implementation: default, loading, skeleton, empty, error, validation error, success, disabled, permission denied, offline/stale, long content and responsive states.
4. If the UI consumes API/data, map each visible state to contract examples and error shapes instead of assuming ideal data.
5. Use the existing design system before adding a new primitive. If a new component or variant is introduced, document why existing primitives are insufficient.
6. Apply Feature-Sliced Design only when the frontend has enough size or business-domain complexity. Do not create empty layers for a small app.
7. When FSD applies, document the layer/slice, public API and allowed import direction.
8. Use Storybook when reusable components or design-system primitives exist. A useful story set includes not just happy path, but loading, empty, error, disabled, focus and long-content states.
9. Treat accessibility as product behavior. Keyboard path, focus visibility, accessible names, semantic controls, form labels and error announcements must be checked or marked as a gap.
10. Define a responsive matrix before claiming a page works. At minimum, include one narrow mobile viewport and one desktop viewport for user-visible layout changes.
11. For visual changes, capture evidence through Playwright screenshots, Storybook visual tests or manual screenshots with browser/viewport notes.
12. For interaction changes, prefer user-observable tests: role/name queries, keyboard input, click/tap, form submission and async state assertions.
13. For user-facing routes, define Core Web Vitals budget or explicit non-applicability. Interaction-heavy screens should consider INP risk.
14. Keep secrets, tokens, private customer data and real private payloads out of UI examples, fixtures, screenshots and stories.
15. Completion requires current runtime evidence or an explicit verification gap. Code inspection alone is not enough for UI completion.

## Product-Agent OS candidate rules

### Discovery signals

- Directories: `app/`, `pages/`, `routes/`, `components/`, `widgets/`, `features/`, `entities/`, `shared/ui/`, `stories/`, `.storybook/`, `e2e/`, `tests/playwright/`
- Files: `*.stories.*`, `storybook/main.*`, `playwright.config.*`, `vite.config.*`, `next.config.*`, `tailwind.config.*`, `tokens.*`, `theme.*`, `components.json`
- Terms: component, route, page, widget, feature, Storybook, FSD, visual regression, screenshot, viewport, accessibility, WCAG, keyboard, focus, design system, responsive, Core Web Vitals, LCP, INP, CLS
- Dependency signals: React/Vue/Svelte/Angular/Solid, Next.js/Nuxt/SvelteKit/Astro, Storybook, Playwright, Testing Library, axe, Chromatic, design-token packages

### Readiness gates

| Gate | Trigger | Block condition |
| --- | --- | --- |
| `frontend_user_flow_acceptance_present` | User-visible UI work | User goal, route/screen or acceptance scenario is missing. |
| `frontend_component_state_matrix_present` | Component/page has multiple states | Loading, empty, error, disabled, focus, success or long-content states are unspecified. |
| `frontend_component_docs_present` | Reusable component/design-system change | No story, component card, Autodocs/MDX note or explicit docs gap. |
| `frontend_design_system_boundary_present` | New UI primitive, token or visual pattern | Existing design system usage/extension decision is not recorded. |
| `frontend_fsd_boundary_reviewed` | FSD project or growing feature structure | Layer/slice/public API/import direction is unclear. |
| `frontend_api_contract_alignment_present` | UI consumes or changes API/data contract | Contract examples, errors, auth/permission and cache behavior are missing. |
| `frontend_accessibility_review_present` | Interactive/form/public UI | Keyboard, focus, label/name, semantic control and error behavior are not checked. |
| `frontend_keyboard_focus_contract_present` | Dialog/menu/listbox/form/navigation interaction | Focus movement, trap/release, visible focus and escape behavior are unspecified. |
| `frontend_responsive_viewport_matrix_present` | Layout or visual change | Mobile and desktop viewport expectations are missing. |
| `frontend_visual_evidence_present` | Styling/layout/visual state change | No screenshot, Storybook visual baseline, Playwright evidence or explicit gap. |
| `frontend_runtime_console_evidence_present` | Browser-rendered app work | Browser console/runtime status is not checked where a dev server or preview is available. |
| `frontend_interaction_test_evidence_present` | User interaction behavior changes | No user-observable interaction test or manual interaction evidence. |
| `frontend_performance_budget_present` | User-facing route/performance-sensitive UI | LCP/INP/CLS budget or explicit non-applicability is absent. |
| `frontend_browser_support_present` | Public UI or browser-specific behavior | Supported browsers/devices or known gaps are not named. |
| `frontend_content_i18n_boundary_present` | Long text, localization or user-generated content | Wrapping/truncation/i18n/RTL assumptions are missing. |

### Candidate templates

- `ui-flow-spec.md`
- `route-page-inventory.md`
- `component-card.md`
- `component-state-matrix.md`
- `storybook-story-map.md`
- `design-system-inventory.md`
- `design-tokens-reference.md`
- `frontend-boundary-map.md`
- `fsd-boundary-record.md`
- `frontend-api-dependency-map.md`
- `responsive-viewport-matrix.md`
- `accessibility-review.md`
- `keyboard-focus-map.md`
- `visual-evidence-packet.md`
- `frontend-interaction-test-matrix.md`
- `frontend-performance-budget.md`
- `frontend-browser-support-matrix.md`
- `frontend-content-i18n-record.md`

### Candidate eval fields

- User flow, route/screen and acceptance scenario are present.
- Component states include loading, empty, error, disabled, focus, long-content and responsive states where applicable.
- Reusable component changes include Storybook story, component card or explicit docs gap.
- Design-system reuse or extension decision is recorded.
- FSD boundaries are documented when the project uses FSD-like structure.
- API/data dependency is tied to contract examples and error states.
- Accessibility review includes keyboard, focus, names/labels, semantic controls and errors.
- Responsive matrix includes mobile and desktop viewports.
- Visual evidence includes screenshot/story baseline path, browser/viewport and console status.
- Interaction tests use user-observable behavior rather than implementation internals.
- Performance budget covers LCP, INP and CLS or explains why not applicable.
- Completion evidence is current for the active slice.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| Frontend architecture | Feature-Sliced Design | Useful when business-feature boundaries are stable enough to justify layers/slices. |
| Component documentation | Storybook Autodocs, MDX, Doc Blocks | Good for reusable components and design-system documentation. |
| Component states | Storybook CSF stories | Stories should include failure and edge states, not just happy path. |
| Interaction checks | Storybook `play`, Testing Library, Playwright | Prefer user-observable behavior and accessible queries. |
| Browser E2E | Playwright | Use for route behavior, screenshots, traces, console/network evidence and cross-browser projects. |
| Visual regression | Playwright screenshots, Storybook visual tests, Chromatic | Baselines must be stable and environment-aware. |
| Accessibility | WCAG 2.2, WAI-ARIA APG, axe, Storybook a11y addon | Automated checks are useful but do not replace keyboard/focus/manual review. |
| Responsive behavior | MDN media queries, Playwright viewport projects | Include viewport and input modality assumptions. |
| Performance | web.dev Core Web Vitals, Lighthouse, WebPageTest, RUM | Use LCP/INP/CLS budget or explicit gap for user-facing routes. |
| Design tokens | Style Dictionary, platform-native token pipeline, CSS variables | Select by existing design system, not by default novelty. |

## Failure modes

- UI work starts from component hierarchy while user flow and acceptance scenario remain vague.
- Storybook exists but only documents the happy path.
- Component docs list props but omit loading, empty, error, disabled, focus, long-text and responsive states.
- Folder structure imitates Feature-Sliced Design while imports violate layer or public API rules.
- Accessibility is reduced to a scanner result and ignores keyboard, focus, semantic controls and error announcements.
- A UI is claimed complete after code inspection without browser/runtime evidence.
- Screenshots cover desktop only and miss mobile, long text, empty/error/loading states or dark/theme variants.
- Visual regression baselines are generated in an unstable environment and create noisy diffs.
- API data shape is assumed in UI without contract examples, permission states or error handling.
- Core Web Vitals are checked only after release, not used as a design constraint for route work.
- Design-system changes create new tokens/variants without owner review or migration notes.
- UI examples, fixtures or screenshots leak real customer data or secrets.

## Open questions for deeper research

- Which frontend stack-specific templates should come first: React/Next.js, Vue/Nuxt, Svelte/SvelteKit, Angular or framework-neutral?
- Should Product-Agent OS enforce Storybook only when reusable components exist, or offer it as an optional docs tool for all frontend projects?
- What is the minimum visual evidence packet for small UI changes versus design-system changes?
- Should accessibility gates target WCAG 2.2 AA by default, or choose level by product risk and legal context?
- How should the plugin detect FSD boundary violations automatically across TypeScript path aliases?
- Which Core Web Vitals measurement path should be the default: Lighthouse lab evidence, Playwright trace, WebPageTest, or RUM?
- Should design token documentation live under frontend, design system or product-brand governance?

## Sources

- [Feature-Sliced Design layers](https://fsd.how/docs/reference/layers/)
- [Feature-Sliced Design public API](https://fsd.how/docs/reference/public-api/)
- [Storybook Autodocs](https://storybook.js.org/docs/writing-docs/autodocs)
- [Storybook interaction tests](https://storybook.js.org/docs/writing-tests/interaction-testing)
- [Storybook visual tests](https://storybook.js.org/docs/writing-tests/visual-testing)
- [Storybook accessibility tests](https://storybook.js.org/docs/writing-tests/accessibility-testing)
- [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots)
- [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer)
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [Testing Library guiding principles](https://testing-library.com/docs/guiding-principles/)
- [MDN: HTML as a good basis for accessibility](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML)
- [MDN: Using media queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Media_queries/Using)
- [web.dev: Web Vitals](https://web.dev/articles/vitals)
- [web.dev: Interaction to Next Paint](https://web.dev/articles/inp)
- [Context7 research](../context7-research.md)
