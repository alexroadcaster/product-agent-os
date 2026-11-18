# ADR — Dashboard and Tasks boundary

Source status: repository_source / bounded_internal_architecture_decision; 2026-11-18.

## Decision

Owner: Product-Agent OS frontend. For the [Dashboard pilot](../../planning/methodology-improvement-2026-11-15.en.md#a1-results), enforce boundaries in the existing structure. Dashboard acts as a page, App owns navigation and composition, and Tasks owns status and blocking semantics. The local service retains write authority and snapshot ownership. App's existing entry points are `Dashboard.tsx` and `TaskManager.tsx`.

In A2, test a narrow, explicit Tasks read API for `semanticStatus` and `isBlocked`. Tasks retains the implementation. Move or expose presentation dependencies such as `statusText` and `errorText` through an explicit interface when a consumer and verification justify it. If a compatibility export is needed, the old path forwards to the new owner. Avoid reverse dependencies and duplicate implementations.

## Alternatives

Keeping only the current folders and tests costs less but leaves new imports of sibling internals undetected. A pages-first FSD migration would provide physical separation, but one testable boundary does not justify moving full screens and updating all consumers. Checking the boundary in place gives a reversible pilot. Decisions about `pages`, `widgets`, `entities` and `shared` depend on A2 results and demonstrated need.

## Enforced rules

- Modules may import other modules in the same area. App uses the existing screen entry points. Other consumers use explicitly approved public entry points.
- Dashboard and Tasks may use their API client, localization, shared contracts, and the `Icon`, `CapabilityNotice`, `Modal`, and `ProjectFreshness` UI primitives. Both modules forbid new direct imports of App and peer screens. Dashboard also forbids new imports of Tasks internals.
- A cycle involving Dashboard or Tasks fails the check, including a path through intermediate frontend modules. The existing contracts → apps and local service → frontend prohibitions still apply.
- The test pins existing edges in `tests/web/fixtures/dashboard-import-baseline.json` at revision `bd7d9135f994201170277171eb54e4040cef4fa8`. Each group has an owner and a removal task. Removing an edge requires removing its entry. METH-12 reviews Dashboard imports of Tasks. METH-18 selects appropriate A4 work for the other consumers.
- `node --test tests/web/contracts-boundaries.test.mts` parses TS, TSX and MTS. Literal imports resolve against source files and supported `baseUrl`/`paths` in the Web tsconfig. Unknown aliases and computed targets have distinct diagnostics. The rule covers the specified frontend boundary. Shared contracts and the backend have their own rules.

## Rollback and stopping criterion

In A2, rerun the same Dashboard browser scenario and compare boundary edges and change effort. The pilot may stop at Dashboard if the read API reduces coupling and preserves covered behavior. If it fails, revert only A2 changes and restore entries for restored edges. The A1 check continues to protect the original boundary.

Reviewed import and public API rules with Context7. [FSD layers](https://feature-sliced.design/docs/reference/layers) · [FSD public API](https://feature-sliced.design/docs/reference/public-api)
