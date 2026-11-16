# Graph models and coverage

Source status: repository_source / focused_f14_parser_verified + static_contract_review; 2026-11-15.; FUNC-G04: locally_verified_with_measured_limits, 16.11.2026.

Owner: graph-cockpit-engineer + docs-maintainer. Scope: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when scanner, API, adapters, query contracts, tests or PoC status change. Graph outputs are derived orientation evidence, not substitutes for source reading and checks.

## Matrix

| Surface | Languages / nodes | Edges and limits |
| --- | --- | --- |
| Web local service | JS/JSX/TS/TSX, including mjs/cjs/mts/cts; file, symbol, unresolved | lexical `define`, `read`, `write`, `reference`, `call`, `import`; imports/aliases and dynamic/member calls are not resolved runtime dependencies |
| Python plugin | file-level graph; Python AST package/module/class/function/method; limited JS/TS stdlib adapter | Python import/call/test edges, JS/TS source-pattern overlay; dynamic calls and unrecognized links remain uncertain/unresolved |
| Python contract overlays | Markdown and supported documentation/API/schema/diagram formats | Contract references and observations do not prove the entire runtime schema or API |

Web [lexical.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/lexical.mts) performs two lexical-scope passes without type resolution or a module linker; [parser-worker.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/parser-worker.mts) owns parser behavior and statuses. Web marks other recognized extensions `unsupported`, not analyzed.

[project_graph_adapters.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_adapters.py) implements Python AST and a limited JS/TS adapter; [project_graph_ontology.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_ontology.py) owns types and confidence. Static edges are observations: wiring, dynamic dispatch, runtime aliases and actual function execution require separate checks.

See [Web API](../api/endpoints.md), [Python contract](../product-agent-os/graph-intelligence-contract.md) and [adapters](adapters.md).

Related tests: [Web code index](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [Python graph queries](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_queries.py), [Python overlays](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_overlays.py). These are verification routes, not claims of a new run.

## F14: verifiable file imports and a bounded resolver

The current 2026-11-15 slice extends production `code-index/lexical.mts`, `parser-worker.mts` and new `module-resolver.mts`. Historical DG05 links above describe the earlier version; F30/F31 PoCs do not become runtime dependencies. It uses the already installed public `rolldown/utils` parser in an owned Node child; Worker remains a focused test seam. Context7 `/rolldown/rolldown` confirmed `parseSync`/program/errors and TS AST options; compatibility was checked against the installed parser without TS Compiler API, installation or temporary PoC engine imports.

File-level import edges come from AST `ImportDeclaration`, source-bearing reexports, `import('literal')` and unshadowed `require('literal')`. Relative workspace paths, cycles, type-only imports and Unicode/spaces are retained. Require uses existing lexical function/import/parameter/catch/block/hoisted-var bindings, including TypeScript constructor parameter properties. Shadowed require remains an ordinary local call. Dynamic inputs/template imports and member calls do not become guessed imports. File dependencies do not become cross-file symbol/call edges: imported symbol aliases still do not prove runtime callees.

The resolver is a pure function over an allowlist of already admitted/indexed source paths; it performs no filesystem/package discovery. It supports bounded root-relative `baseUrl` and literal `paths`, up to64aliases,8targets/alias,256chars/value and one wildcard. Root wiring reads only permitted root `tsconfig.json` as bounded JSON, binds config/source hashes and passes `resolverConfig`/`configReasons` to the parser child. Extends, references, absolute/traversal paths, executable configs and unsupported structures do not widen the root; relative imports remain available with an explicit config diagnostic. Package exports/conditions, TS project references and a full TypeScript/Node module linker are not claimed.

Exact aliases precede wildcards; wildcard matching chooses the longest prefix. Multiple permitted targets, including extension/directory ambiguity, report `ambiguous_module` rather than choosing arbitrarily. Missing/unknown/bare external dependencies remain unresolved; the resolver never reads parent package.json, runs scripts or returns a file outside the allowlist. Root config changes participate in source/revision freshness; the shared publication contract fences late/foreign results.

Focused Worker ground truth `tests/fixtures/func_g02/corpus.json`: before the change7/10 imports resolved, afterward10/10, precision1/recall1 on this fixed corpus. The check also passes through production `createCodeIndex`: root alias wiring, config drift and a hostile executable-config canary without execution. Separate fixtures cover ambiguity, unsupported config/accessors, dynamic inputs and shadowing; a false import involving a TS parameter property was fixed through RED/GREEN. This measures a synthetic import subset, not all-language coverage or a runtime call graph.

Reproduce with `node --test tests/web/graph-imports.test.mts`; affected existing regressions are in `tests/web/code-index.test.mts`. Receipts: `.tmp/func-g04/f14/`; root owns shared API/UI integration, native regression handoff and browser acceptance. The next artifact is a graph snapshot with compatible revision, unresolved reasons and a checked source anchor. [Queries/impact](queries-impact.md), [adapters](adapters.md).

## G04 integration and native failure containment

Production parsing runs in an owned Node child with a minimal environment, empty temporary cwd,128MiB JS heap, independent ready-handshake watchdog,10s parent deadline and bounded stdin/stdout. Native stack failures remain inside the child; cancellation waits for close before cleanup. JS heap limits are not native RSS limits; child self peak RSS is reported separately from the service process. Focused Worker corpus tests remain distinct from production-child tests.

Graph status performs one F28 metadata walk and no unconditional source-body reread; excerpts still verify raw SHA256 and final registry authority. A policy-revocation race preserves PROJECT_SCOPE_STALE. LRU8 and per-build cursor generation permit a ninth project without restart. API/UI dependency/symbol modes, incoming/outgoing,8-hop/1000-node paths and graph/list/Mermaid share a revision. Source-backed DB usage is a separate bounded code→table network with confidence/evidence, not an inferred architecture or runtime call graph.
