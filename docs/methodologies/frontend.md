# Frontend

Source status: `official + verified methodology + tool-assisted + experiment`

Источники: [Feature-Sliced Design](https://fsd.how/docs/reference/layers/), [FSD Public API](https://fsd.how/docs/reference/public-api/), [Storybook Autodocs](https://storybook.js.org/docs/writing-docs/autodocs), [Storybook interaction tests](https://storybook.js.org/docs/writing-tests/interaction-testing), [Storybook visual tests](https://storybook.js.org/docs/writing-tests/visual-testing), [Storybook accessibility testing](https://storybook.js.org/docs/writing-tests/accessibility-testing), [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots), [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer), [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/), [Testing Library guiding principles](https://testing-library.com/docs/guiding-principles/), [MDN accessible HTML](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML), [MDN media queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Media_queries/Using), [web.dev Web Vitals](https://web.dev/articles/vitals), [web.dev INP](https://web.dev/articles/inp), [Context7 research](../sources/context7-research.md), [research dossier](../sources/methodology-research/frontend.md).

## Deep research цель

Frontend слой фиксирует, как строить UI behavior, route/page flows, component boundaries, design-system usage, accessibility, responsive states, visual verification, browser/runtime evidence и performance так, чтобы UI changes были понятны людям и проверяемы агентами.

Главный принцип: frontend-изменение нельзя считать завершенным после code inspection. Для UI нужны user-flow acceptance, documented states, responsive/accessibility coverage и текущие browser/runtime evidence или явно записанный verification gap.

## Поддержанные факты

- Feature-Sliced Design defines layers and public API boundaries for frontend structure when feature/business slicing reduces coupling.
- Storybook Autodocs, interaction tests, visual tests and accessibility testing can serve as component documentation and verification surfaces.
- Playwright supports screenshots, visual comparisons and Trace Viewer for browser runtime evidence.
- WCAG 2.2, WAI-ARIA APG, semantic HTML guidance and Testing Library principles support user-observable accessibility and interaction checks.
- Web Vitals and Interaction to Next Paint (INP) give frontend performance vocabulary for user-facing and interaction-heavy routes.
- Frontend evidence must include visible states, responsive states, keyboard/focus behavior, console/runtime status and privacy-safe screenshots where applicable.

## Assumptions

- Product-Agent OS will not require one frontend framework. React/Next.js, Vue/Nuxt, Svelte/SvelteKit, Angular and framework-neutral HTML/CSS/JS need the same behavior-level contract with stack-specific commands.
- Storybook is a strong component documentation and verification surface, but it should be conditional: required for design systems and reusable components, optional for small one-off UI.
- Feature-Sliced Design is useful when layer/slice boundaries reduce coupling; it is not a default folder template for every MVP.
- Automated accessibility checks are necessary but incomplete. Keyboard flow, focus behavior, accessible names, semantic controls and error announcements still need user-observable evidence.
- Visual evidence must be privacy-safe. Screenshots, stories and mock data must not include secrets, private customer data or raw private payloads.

## Инструкции применения на проекте

1. Классифицировать работу: route/page, component, design-system primitive, layout, interaction, state, data-fetching UI, accessibility fix или performance fix.
2. Начинать с user flow: цель пользователя, экран/route, acceptance scenario и видимые state transitions.
3. До реализации назвать UI states: default, loading, skeleton, empty, error, validation error, success, disabled, permission denied, offline/stale, long content и responsive states.
4. Если UI зависит от API/data, связать каждый видимый state с contract examples, auth/permission, error shape, pagination/cache/stale behavior.
5. Сначала использовать существующий design system. Новый primitive, token или variant требует объяснения, почему текущих элементов недостаточно.
6. Feature-Sliced Design применять условно: когда UI растет по features/business entities и слои реально снижают coupling. Не создавать пустые слои для маленького MVP.
7. Если FSD применяется, фиксировать layer/slice, public API и допустимое направление imports.
8. Storybook использовать как docs and verification surface для reusable components и design system: stories должны покрывать не только happy path, но loading, empty, error, disabled, focus и long-content states.
9. Accessibility считать поведением продукта: keyboard path, focus visibility, accessible names, semantic controls, labels, error announcements и contrast проверяются или явно помечаются как gap.
10. Для layout/visual work заранее задать responsive matrix: минимум узкий mobile viewport и desktop viewport; по риску добавить tablet, orientation, reduced motion, dark/theme variants.
11. Для visual changes сохранять evidence через Playwright screenshots, Storybook visual tests или manual screenshots с browser/viewport notes.
12. Для interaction changes предпочитать user-observable tests: role/name queries, keyboard input, click/tap, form submit, async state assertions.
13. Для user-facing routes задавать Core Web Vitals budget или explicit non-applicability. Interaction-heavy screens отдельно проверять INP risk.
14. Не помещать secrets, tokens, private customer data и реальные private payloads в UI examples, stories, screenshots, fixtures или mocks.
15. Completion требует current runtime evidence: browser/dev-server check, console status, screenshots, Storybook build/test, Playwright trace или explicit verification gap.

## Применяемые методологии разработки

| Методология | Когда применять | Как выглядит в проекте |
| --- | --- | --- |
| User-flow-first UI development | Любое user-visible UI изменение | Экран, user goal, acceptance scenario и state paths заданы до component work. |
| Component-driven development | Reusable components, design system, repeated UI patterns | Stories фиксируют props, variants, states, events, accessibility и examples. |
| Design-system-driven development | Есть tokens, shared components или brand rules | Новая UI работа использует существующие primitives; extensions документируются. |
| Conditional Feature-Sliced Design | Frontend растет по features/business entities | Layers/slices/public API/import rules применяются там, где уменьшают coupling. |
| Accessibility-first / inclusive design | Interactive, public, regulated, form-heavy или high-use UI | WCAG/APG-oriented checks, keyboard/focus/labels/errors как acceptance criteria. |
| Responsive/adaptive design | UI работает в разных viewport/input contexts | Viewport matrix, wrapping/truncation, touch/mouse/keyboard assumptions. |
| Interaction-first testing | Поведение зависит от user actions | Тестируется observable behavior, а не component internals. |
| Visual regression testing | Layout/style может сломаться без unit failure | Playwright/Storybook screenshots и stable baselines. |
| Performance-by-design | User-facing, high-traffic или interaction-heavy routes | LCP/INP/CLS budget или явный gap; evidence собирается до release. |
| API-contract-aware frontend development | UI зависит от backend/API/feature flags/async data | UI states привязаны к OpenAPI/AsyncAPI/Pact/examples/errors/cache behavior. |
| State ownership design | Form, cache, global или persistent state становится нетривиальным | Local, route, server-cache, global и persisted state boundaries названы. |
| Content and i18n-ready UI | Long text, localization, user-generated content | Проверены wrapping, truncation, pluralization, empty copy, RTL/locales where applicable. |
| Evidence-before-completion | Любая заявка “UI готов” | Есть current browser/runtime/visual evidence или explicit verification gap. |

## Инструменты, артефакты и стандарты документирования

- `ui-flow-spec.md`: user goal, route/screen, acceptance scenario, state paths.
- `route-page-inventory.md`: routes, params, data dependencies, auth/permission, SEO/meta notes.
- `component-card.md`: purpose, props, events, states, accessibility, linked API, owner.
- `component-state-matrix.md`: default/loading/empty/error/success/disabled/focus/responsive/long-text states.
- `storybook-story-map.md`: stories, variants, state coverage, Autodocs/MDX links.
- `design-system-inventory.md`: tokens, components, variants, icons, typography, spacing, themes.
- `frontend-boundary-map.md` / `fsd-boundary-record.md`: page/widget/feature/entity/shared boundary, public API, import constraints.
- `frontend-api-dependency-map.md`: endpoint/query/mutation/event, contract examples, auth, errors, cache behavior.
- `responsive-viewport-matrix.md`: desktop/tablet/mobile, orientation, input modality, reduced motion, theme.
- `accessibility-review.md`: WCAG target or gap, semantic HTML, keyboard, focus, labels, names, errors, contrast.
- `keyboard-focus-map.md`: tab order, trap/release, modal/menu/listbox/dialog behavior, visible focus.
- `visual-evidence-packet.md`: screenshots, viewport list, browser/OS, console status, baseline reference.
- `frontend-interaction-test-matrix.md`: user actions, expected state, accessible queries, async behavior.
- `frontend-performance-budget.md`: LCP/INP/CLS target or non-applicability, measurement path, risk.
- `frontend-browser-support-matrix.md`: supported browsers/devices, Playwright projects, known gaps.
- `frontend-content-i18n-record.md`: long strings, localization, empty copy, pluralization, RTL, truncation.

## Что еще включить в deep research

- Stack-specific templates: React/Next.js, Vue/Nuxt, Svelte/SvelteKit, Angular, framework-neutral HTML/CSS/JS.
- Design system governance: token owner, variant policy, icon policy, breaking component API changes.
- Storybook adoption policy: when required, when optional, when too heavy for a small project.
- Visual QA thresholds: what evidence is enough for tiny UI change, page redesign, design-system primitive and public route.
- Accessibility risk levels: default WCAG 2.2 AA target vs product/legal risk-based level.
- FSD auto-detection: imports, aliases, public API violations, cross-slice references.
- Core Web Vitals measurement selector: Lighthouse, WebPageTest, Playwright trace, field RUM.
- Browser/device support policy: desktop web, mobile web, embedded webview, Electron/desktop shell.
- Data privacy for UI artifacts: screenshots, stories, mocks, generated fixtures and demo accounts.

## Product-Agent OS routing

- `workspace-discovery-auditor` detects frontend stack, routes, Storybook, Playwright, design system, FSD-like structure, test commands and browser/runtime constraints.
- `requirements-author` captures user flow, acceptance scenario, accessibility expectations, supported viewports and content/i18n constraints.
- `implementation-planner` blocks risky UI work when component states, design-system boundary, API contract or verification path is missing.
- `test-eval-designer` selects Storybook, unit/component, Playwright, visual, accessibility, performance and manual browser checks.
- `risk-reviewer` reviews public component APIs, accessibility gaps, design-system drift, screenshot privacy and performance risk.
- `docs-maintainer` updates component cards, Storybook docs, visual evidence packet and methodology/source references.

## Candidate readiness gates

- `frontend_user_flow_acceptance_present`: user goal, route/screen and acceptance scenario are present.
- `frontend_component_state_matrix_present`: loading, empty, error, disabled, focus, success, long-content and responsive states are documented where applicable.
- `frontend_component_docs_present`: reusable component/design-system change has story, component card, Autodocs/MDX note or explicit docs gap.
- `frontend_design_system_boundary_present`: design-system reuse or extension decision is recorded.
- `frontend_fsd_boundary_reviewed`: FSD layer/slice/public API/import direction is clear when FSD applies.
- `frontend_api_contract_alignment_present`: UI data dependency is tied to contract examples, auth, permission, errors and cache behavior.
- `frontend_accessibility_review_present`: keyboard, focus, labels/names, semantic controls, errors and contrast are checked or marked as gap.
- `frontend_keyboard_focus_contract_present`: dialog/menu/listbox/form/navigation focus behavior is specified.
- `frontend_responsive_viewport_matrix_present`: mobile and desktop expectations are documented for layout/visual work.
- `frontend_visual_evidence_present`: screenshot, Storybook visual baseline, Playwright evidence or explicit gap exists.
- `frontend_runtime_console_evidence_present`: browser console/runtime status is checked where preview/dev server is available.
- `frontend_interaction_test_evidence_present`: interaction change has user-observable test or manual evidence.
- `frontend_performance_budget_present`: LCP/INP/CLS budget or explicit non-applicability is recorded.
- `frontend_browser_support_present`: supported browsers/devices or known gaps are named.
- `frontend_content_i18n_boundary_present`: long text, localization, user-generated content and truncation assumptions are documented.

## Candidate eval fields

- User flow, route/screen and acceptance scenario are present.
- Component state matrix covers loading, empty, error, disabled, focus, success, long content and responsive states where applicable.
- Reusable component has story, component card, Autodocs/MDX note or explicit docs gap.
- Design-system reuse or extension decision is recorded.
- FSD layer/slice/public API/import direction is clear when FSD applies.
- UI data dependency links to contract examples, auth, permission, error and cache behavior.
- Keyboard, focus, labels/names, semantic controls, errors and contrast are checked or marked as gap.
- Visual/runtime evidence includes browser, viewport, console status and screenshot/trace where relevant.
- Performance budget covers LCP/INP/CLS or explains non-applicability.
- UI artifacts contain no secrets or private customer data.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| Frontend structure | Feature-Sliced Design | Use only when layers/slices reduce real coupling; record public API rules. |
| Component docs | Storybook Autodocs / MDX | Useful for reusable components and design-system primitives; `autodocs` signals generated component docs. |
| Component interaction checks | Storybook interaction tests | Good for component states and user events; `play` functions are a Storybook interaction-test signal. |
| Visual/runtime checks | Playwright screenshots, Trace Viewer | Browser evidence for layout, state, trace and console issues. |
| Accessibility | WCAG 2.2, WAI-ARIA APG, Testing Library, MDN | Use semantic queries and user-observable behavior. |
| Performance | Web Vitals, INP, Lighthouse/RUM where available | Choose field or lab measurement by release risk. |
| Design-system docs | `design-tokens-reference.md`, `components.json` | Token and component registry when project uses generated UI metadata. |
| Story coverage | `storybook-story-map.md`, Autodocs | Tracks story/state coverage and docs gaps. |

## Проверки

- UI behavior maps to user flow and acceptance scenario.
- Component state matrix is current or gap is explicit.
- Storybook docs or component card exist for reusable components.
- FSD public API/import rule is respected when FSD applies.
- API/data contract examples cover loading, empty, error and permission states.
- Keyboard/focus behavior is tested manually or automatically for interactive UI.
- Responsive matrix covers at least one mobile and one desktop viewport for visual/layout work.
- Visual/runtime check is current: Playwright, Storybook visual, browser screenshots or explicit gap.
- Browser console has no relevant runtime errors where preview/dev server is available.
- Performance budget covers LCP/INP/CLS for user-facing routes or explains non-applicability.

## Failure modes

- UI work starts from component hierarchy while user flow and acceptance scenario are vague.
- Folder structure imitates FSD but imports violate layer or public API rules.
- Storybook exists but only documents happy path.
- Component docs list props but omit loading, empty, error, disabled, focus, long text and responsive states.
- Accessibility is reduced to addon output; keyboard, focus, labels and semantic controls are not checked.
- UI completion is claimed after code inspection only.
- Screenshots cover desktop only and miss mobile, loading/error/empty, long text or theme variants.
- Visual baselines are generated in unstable environments and create noisy diffs.
- API data shape is assumed without contract examples, error shapes or permission states.
- Design-system changes add new tokens/variants without owner review or migration notes.

## Unsupported claims not adopted

- "FSD should be mandatory for every frontend project." Not adopted; it is conditional on project size, coupling and ownership boundaries.
- "Storybook proves UI quality by itself." Not adopted; stories need interaction, accessibility, visual/runtime evidence and state coverage.
- "Automated a11y addon output is enough." Not adopted; keyboard, focus, semantic and error-announcement behavior remain acceptance concerns.
- "A desktop screenshot proves responsive UI." Not adopted; mobile/desktop viewport matrix and relevant state coverage are required for layout work.
- "Lab Web Vitals always represent production UX." Not adopted; lab checks are useful, but field/RUM evidence is preferred when release risk justifies it.

## Open questions for future implementation

- Which stack-specific templates should Product-Agent OS generate first: React/Next.js, Vue/Nuxt, Svelte/SvelteKit, Angular or framework-neutral HTML/CSS/JS?
- When should Storybook be required, optional or too heavy for a small project?
- What visual evidence is enough for a tiny UI change versus a page redesign or design-system primitive?
- Should WCAG 2.2 AA be the default target for all public UI, with explicit exceptions?
- How should FSD auto-detection flag import/public API violations?
- Which Web Vitals measurement path should be recommended by default: Lighthouse, Playwright trace, WebPageTest or field RUM?
