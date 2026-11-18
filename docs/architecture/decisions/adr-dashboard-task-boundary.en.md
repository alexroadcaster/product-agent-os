# ADR — Dashboard and Tasks boundary

Source status: repository_source / bounded_internal_architecture_decision; 2026-11-18.

## Decision

Owner: Product-Agent OS frontend. For the [Dashboard pilot](../../planning/methodology-improvement-2026-11-15.en.md#a1-results), enforce boundaries in the existing structure. Dashboard acts as a page, App owns navigation and composition, and Tasks owns status and blocking semantics. The local service retains write authority and snapshot ownership. App's existing entry points are `Dashboard.tsx` and `TaskManager.tsx`.

In the A2 pilot, Dashboard uses `features/tasks/read.ts`. The entry explicitly exports `semanticStatus`, `isBlocked`, `statusText`, `errorText`, and the `Locale` type. The single implementations stay in Tasks' `model.ts` and `labels.ts`. The boundary separates reads from editing, commands, and screen composition. [A2 verification](../../planning/methodology-improvement-2026-11-15.en.md#a2-results)

## Alternatives

Keeping only the current folders and tests costs less but leaves new imports of sibling internals undetected. A pages-first FSD migration would provide physical separation, but one testable boundary does not justify moving full screens and updating all consumers. Checking the boundary in place gives a reversible pilot. Decisions about `pages`, `widgets`, `entities` and `shared` depend on A2 results and demonstrated need.

## Enforced rules

- Modules may import other modules in the same area. App uses the existing screen entry points. Other consumers use explicitly approved public entry points.
- Dashboard and Tasks may use their API client, localization, shared contracts, and the `Icon`, `CapabilityNotice`, `Modal`, and `ProjectFreshness` UI primitives. The pilot permits Dashboard to use `tasks/read.ts`. New consumers require their own validation. Tasks internals and imports of App or peer screens remain covered by the boundary check.
- A cycle involving Dashboard or Tasks fails the check, including a path through intermediate frontend modules. The existing contracts → apps and local service → frontend prohibitions still apply.
- The original exceptions were pinned at revision `bd7d9135f994201170277171eb54e4040cef4fa8`. The pilot removes three Dashboard → Tasks exceptions. `tests/web/fixtures/dashboard-import-baseline.json` retains 16 exceptions, with owners and removal tasks. The test requires removing entries when their edges are removed.
- `node --test tests/web/contracts-boundaries.test.mts` parses TS, TSX and MTS. Literal imports resolve against source files and supported `baseUrl`/`paths` in the Web tsconfig. Unknown aliases and computed targets have distinct diagnostics. The rule covers the specified frontend boundary. Shared contracts and the backend have their own rules.

## Rollback and stopping criterion

To roll Dashboard back, restore the three old imports, remove `tasks/read.ts`, and restore the corresponding exceptions and former check rule. If reverting the entire change, restore the API test, browser hash references, and A2 cards to the baseline as part of the same patch. Rerun the boundary check, build, and browser scenario on the restored revision. The pilot has no data migration.

## Expansion decision {#a2-rollout}

`METH-18` confirms the Dashboard pilot. The comparison shows two Tasks internal paths reduced to one public entry, three direct violations removed, and all 50 common browser checks preserved. Expansion considers the same kind of coupling in a specific consumer.

| Task | Decision and rationale |
| --- | --- |
| METH-10 | `hold`. The pilot tested Tasks reads. Extracting common Markdown or UI requires its own boundary evidence and rendering checks. |
| METH-11 | `bounded_go` for one consumer, `TeamManager.tsx`. Owners are Tasks and Team frontend. The Tasks entry can explicitly expose the already used `durationText`, `label`, `errorText`, and `Locale` type. Measurable outcome: remove two Team → Tasks deep imports, introduce zero violations, and pass relevant Team and Dashboard scenarios. Rollback restores the two imports, Team exceptions, and former export list. |
| METH-13 | `hold`. Moving Tasks or Workflows requires a separate user-journey result and verification of drafts, CAS, and focus. |
| METH-14 | `hold`. METH-11 covers only Team's imports of Tasks. Changes to Team and Skills boundaries require their own demonstrated problem. |
| METH-15 | `hold`. Sessions, Artifacts, Graph, and composition changes depend on their own criteria and demonstrated benefits. |

A3 proceeds on its own path from METH-05. The selected METH-11 scope applies to the next A4 implementation. Product direction B has its own plan.

Reviewed import and public API rules with Context7. [FSD layers](https://feature-sliced.design/docs/reference/layers) · [FSD public API](https://feature-sliced.design/docs/reference/public-api)
