# Frontend: design, themes and localization

Source status: repository_source / static_source_review; 2026-11-15.

Owner: frontend owner and design owner. Scope: V3 application in Web UI at revision `ad78d5d15aced23febae90d319f2aba00bd64d0b`. Update when approved design, preference contracts, CSS or implementation verification changes.

## Design authority

[DESIGN.md](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/DESIGN.md) and [V3 design assets](https://github.com/alexroadcaster/product-agent-os/tree/ad78d5d15aced23febae90d319f2aba00bd64d0b/design/2026-11-13-v3) own the direction, visual material and field map. This page routes to implementation rather than copying tokens or screenshots. [Implementation evidence](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/design/2026-11-13-v3/implementation-evidence.md) is dated 2026-11-13 and reports local checks and `needs_user_acceptance`; it is not a new DG04 acceptance.

## Application

[main.tsx](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/main.tsx) imports `theme.css`, `app.css`, `workspace.css`, `parity.css`. [theme.css](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/design/theme.css) defines semantic CSS variables for Porcelain/Obsidian and focus; the other stylesheets and feature CSS apply them to specific surfaces. When changing a component, inspect existing tokens/styles, the visual reference, loading/empty/error/disabled states and both themes; edit the owning source rather than a documentation copy.

[preferences.ts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/design/preferences.ts) supports `ru`/`en` and `light`/`dark`/`system`; invalid or missing persisted values independently fall back to `ru` and `system`. Applying sets root `lang` and resolved `data-theme`; System follows the current OS color scheme. [preference-controls.ts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/design/preference-controls.ts) separates draft from applied preferences: applied values change after a successful local-service write; an error does not claim a successful save.

[messages.ts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/locales/messages.ts), [app.ts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/locales/app.ts) and localized component strings hold UI labels. User names, text, paths and technical identifiers are not automatically translated. When adding UI text, check both locales and accessible names, preserving schema keys and error codes.

## Motion and graphics

[Sidebar](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/Sidebar.tsx) uses local `requestAnimationFrame` motion and snaps without animation for `prefers-reduced-motion`; `App` uses GSAP for entry when motion is allowed. [GraphViews](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/graph/GraphViews.tsx) contains D3 and lazy-loads local Mermaid, which receives the active theme. Installed libraries do not prove rendering on a particular device.

Related checks: [theme-locale.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/theme-locale.test.mts), [ui-v3-diagram.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-v3-diagram.test.mts); references do not assert a new run. [Accessibility](accessibility.md) covers historical scope, human checks and limits. Planned Files/Map/Database/usages F26–F34 are not implemented merely because of a design.
