# Plan B3 — UI journeys and FSD boundary verification

Source status: local implementation and bounded synthetic verification.

## PMETH-08 and PMETH-09 {#design-verification}

`tools/project-methodology.mts design` emits a revision-bound JSON plan with the journey goal, steps, available data, loading/empty/error/dirty states, focus and keyboard behavior. Existing design assets are identified by path. Proposed states and evidence gaps remain visible. Substantial journeys support a problem hypothesis and a representative user observation. The Web profile marks backend and native work `not_applicable`.

The input distinguishes `synthetic`, `current` and `unavailable`. The proposal, supplied observation and human acceptance have separate evidence and owners. If the browser is unavailable, the plan shows a gap and a feasible component or source check. The browser scenario uses the existing task summary and local API with disposable data. [CLI usage](../../product-agent-os/methodology-intelligence.en.md#frontend-methodology)

The browser runner passed **48/48** checks. It observed user actions, geometry and region order in both themes and languages, a 400 px viewport, a long revision, loading, absent evidence, errors, dirty input, keyboard navigation and zero external requests. The same DOM failed an intentionally incorrect order. The old CSS left a 33 px recommendation at a 400 px viewport. `apps/web/src/design/parity.css` now stacks task context beneath the recommendation at narrow widths, where the rerun measured 303 px. Wide layouts keep the context to the right. RED receipt `pmeth-b3-c3YdHv/result.json` has SHA-256 `55a9c0c3c4e6684ace520c72d836b4b9be99c9b0299e8b50f2f42cdfd9f9c43d`. `tests/fixtures/product_agent_os/pmeth-b3-composition.json` records the expected order and review policy. Browser receipt `pmeth-b3-xzvNdb/result.json` contains source, bundle and harness digests and the Chromium version. Its SHA-256 is `bd8e9904768b094fb489c34eaf14edf303ddfc4c2aedb6704802a2ff8ea40c80`. Fixture cleanup and matching target bytes were verified. Human acceptance and accessibility certification were outside this check.

## PMETH-10 and PMETH-11 {#architecture-evidence}

The `architecture` command invokes the existing F14 index using a disposable profile. The report binds observations to the graph and inventory and gives the import path, line, rule, owner, admitted `@x` API and scoped legacy exception with its reason.

| Input | Result |
| --- | --- |
| Static page with a misleading `features` directory | Retain the architecture. Folder names alone have no effect. |
| Modular legacy with public boundaries and an admitted `@x` API | Retain the boundaries. An undeclared cross-slice entry yields a finding. |
| Growing frontend with violations reachable from a frequently changed page and moderate effort | Recommend gradual FSD. High effort or a selected page with no path to the findings yields a recommendation to strengthen boundaries. |
| Backend or native | Return the applicable architecture policy and current source signals. |
| Missing adapter, malformed config, unknown import, linked path or unsupported source | Report `partial` with reasons and withhold a migration proposal. |

The tests ran the previous B1 route before the B3 candidate on the same three frontend fixtures. B1 treated the modular and coupled page paths alike. F14 distinguished them using observed imports. The initial F14 check missed the first-line `TSImportType` edge. The corrected check covers import types, re-exports, literal dynamic imports and local JSON `extends`, including aliases relative to their defining config. Package or cyclic extensions, unknown aliases, external paths and unsupported syntax do not increase reported coverage. F30 remains the comparison corpus for import behavior. [Official FSD public API reference](https://feature-sliced.design/docs/reference/public-api) · [TypeScript module resolution reference](https://www.typescriptlang.org/docs/handbook/modules/reference.html)

## PMETH-12 {#migration-proposal}

For an eligible page the proposal gives baseline imports, reachable findings, ownership, a compatibility re-export, an import ratchet and rollback. The first checkpoint is limited to one page and its used APIs. Lower-layer extraction needs observed reuse and an owner. The ratchet compares counts using stable source and target paths and the rule, so line movement alone leaves the result unchanged. The plan can stop after the pilot, with separate conditions for PMETH-16 and profile-specific PMETH-23.

The report uses stdout and working memory. Target file SHA-256 digests matched before and after each synthetic CLI run. Staging, applying or activating rules requires separate authority for the selected scope.

## Technical verification {#local-verification}

Focused F14, CLI and contract checks passed **26/26**, the full Windows Web suite passed **724/724** before the final CSS and pilot-selection edits, and Python CLI compatibility passed **40/40**. The final edits were covered by the repeated focused F14/CLI checks and **37/37** packaging, Task Manager and contract checks. Web and tool type checks and the Web build passed. Candidate and default native qualification passed for runtime revision `c4c90577acecd765aaf85d60acae9f2a1de37efdcb7865aaba96fcc88005cf9f`. The candidate SHA-256 is `99908f16a5489206fc0d5764e8751c04c6ac4c7e86746d55f96a28cb1403a7dd`, and the default receipt SHA-256 is `21b98fda84ec32d1cb7bd3590aae337f2397420b77a8dcb86ca9537b1722a794`. The previous B2 release hold still applies.
