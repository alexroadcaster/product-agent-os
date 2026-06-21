# Project Code Graph

Source status: `official + experiment`

This page describes the local Project Code Graph layer in Product-Agent OS. It helps readers navigate a codebase through a generated graph, query packets, cockpit and local indexes, but it does not replace source files, checked-in documentation, tests, approval records or owner decisions.

## Purpose

Project Code Graph provides offline project navigation:

- scans the workspace and builds a file-level graph with file nodes, `contains` edges, fingerprints, spans and observation records;
- adds Python AST overlays for package/module/class/function/method, import/call/test edges and unresolved call summaries;
- adds docs/contracts/schema overlays for Markdown, OpenAPI/Swagger, AsyncAPI, DBML, SQL, JSON, YAML, Mermaid and PlantUML;
- emits bounded query packets for graph reading without rereading raw source bodies;
- renders a static cockpit as a generated view for overview navigation;
- adds extension surfaces for search index, backend gate, semantic retrieval, deterministic LLM proposals and closure evidence.

## Source-of-truth boundary

Generated graph artifacts are not source of truth. They are orientation evidence and cache-bound generated views.

Source of truth remains in project source files, checked-in documentation, schema/contracts, tests, approval packets, RUNLOG/TEST/EVALS evidence and explicit owner decisions. Graph, cockpit HTML/JSON, search/backend/semantic indexes, LLM proposal packets and extension closure reports must not be used as standalone proof of architecture, runtime behavior, coverage, security posture or release readiness.

Without separate explicit approval, live server, browser automation, provider/API calls, canonical graph mutation, git stage/commit/push/PR and external writes are forbidden. Query and stage modes must remain local, deterministic and generated-artifact-only.

## Inputs

Main inputs:

- `<workspace>` for `scan_project_code_graph.py`;
- optional previous manifest/graph for freshness, provenance and temporal edge invalidation/supersession;
- existing `project-code-graph.json` or `project-code-graph.jsonl` for query mode;
- approval packets only for approval-bound extension modes: backend, semantic index, LLM proposals and extension closure evidence.

The scanner reads local project files, but graph/query packets exclude raw source bodies by default and redact absolute paths or secret-like values. Stage output must be an explicit directory, preferably outside the target workspace.

## Outputs And Artifacts

Base artifacts:

- `.codex/product-agent-os/project-code-graph.json` - main graph JSON with `write_policy: read_only`, metadata, nodes, edges and observations.
- `.codex/product-agent-os/project-code-graph.jsonl` - bounded JSONL serialization for agent consumption.
- `.codex/product-agent-os/project-cockpit.html` - offline generated cockpit, review-only.
- `.codex/product-agent-os/project-cockpit.json` - structured cockpit model and projection.
- Graph analysis report from `project_graph_analysis.py` - source-free orientation report, not completeness proof.
- Status/runtime summaries from query packets and cockpit model - compact health/orientation summaries.

Extension artifacts:

- `.codex/product-agent-os/project-code-graph-search-index.json` - offline static search index with stale-index blocking and rollback path.
- `.codex/product-agent-os/project-code-graph-backend.json` - disabled-by-default local query backend store; no active server by default.
- `.codex/product-agent-os/project-code-graph-semantic-index.json` - local deterministic semantic retrieval cache; external embedding/cross-encoder providers remain approval-bound.
- `.codex/product-agent-os/project-code-graph-llm-proposals.json` - staged local deterministic semantic extraction proposals with provenance, uncertainty and unsupported-claim labels.
- `.codex/product-agent-os/project-code-graph-extension-closure.json` - extension verification, rollback/data deletion proof and graph-only fallback report.

## Cockpit Surfaces

The cockpit collects graph, file and code orientation surfaces into one offline generated view. It is useful for first project reading, but it remains a review surface:

- `Project Map` shows graph projection, filters, selected-node evidence and a fallback static table.
- `Code Intelligence` shows hotspots, `read_order`, trace/impact packets and `Code Flow`.
- `Contracts` shows API, schema, diagram and explicit contract overlays.
- `Quality & Metrics` shows tests, fixtures, affected-test packets and quality evidence pointers.
- `Operations & Risk` shows stale flags, ambiguous edges, scale budget and visual QA hints.
- `Proposal Ledger` shows proposal-only items, owner-review boundary and unsupported-claim labels.

Recommended reading order:

1. Start with `Project Map` to identify large file/code clusters and selected-node evidence.
2. Open `Code Intelligence` and use `read_order` as a hint for which files to read first.
3. Check `Contracts` when a change touches APIs, schemas, diagrams, OpenAPI/Swagger, AsyncAPI, DBML, SQL, JSON or YAML overlays.
4. Check `Quality & Metrics` to understand which tests or fixture references might be affected.
5. Before claiming behavior, readiness or a fix, open source files and run the current verification gates; the cockpit does not prove those claims by itself.

The schema/contract surface shows where the scanner found parseable contracts and schema-like inputs. It does not replace contract tests, owner-approved API changes, source registry updates or runtime evidence.

## Static Visual Boundary

The current cockpit renders a local-only static fallback: SVG/table projection, selected-node panel, filters and safe embedded JSON. `project_graph_visual_model.py` marks Graphology/Sigma as `not_bundled_static_fallback`; the renderer does not fetch external assets.

Cosmos.gl/WebGL is not a confirmed runtime/browser capability of this layer. Until separate approved browser/runtime proof exists, docs must not claim interactive WebGL rendering, canvas performance, browser screenshots, WCAG visual proof or generated `site` freshness. If a future renderer adds Cosmos.gl, Graphology, Sigma or another browser layer, it must preserve static fallback, local/vendor boundary, source labels, visual QA evidence and a separate approval gate.

## Operating Modes And Commands

Base scanner and stage-only generation:

```powershell
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --dry-run
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --stage C:\tmp\product-agent-os-graph-stage
```

Graph-only queries read an existing JSON/JSONL artifact:

```powershell
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --query status --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --query neighbors --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --node-id function:app.main.main
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --query search --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --text "runtime"
```

Supported query kinds include `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `changed_since`, `why_changed`, `read_order`, `hotspots`, `node`, `status` and `search`. Query packets are bounded by `--max-results`, `--max-depth`, `--max-tokens`, filters and hub suppression.

Extension modes:

```powershell
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --build-index --stage C:\tmp\product-agent-os-graph-stage --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --build-backend --stage C:\tmp\product-agent-os-graph-stage --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --backend-approval approval.json
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --build-semantic-index --stage C:\tmp\product-agent-os-graph-stage --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --semantic-approval approval.json
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --build-llm-proposals --stage C:\tmp\product-agent-os-graph-stage --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --llm-approval approval.json
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --verify-extensions --stage C:\tmp\product-agent-os-graph-stage --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --verification-evidence evidence.json
```

Disable modes remove generated extension artifacts under the stage root: `--disable-backend`, `--disable-semantic-index`, `--disable-llm-proposals` and `--disable-extensions`.

## Verification

Minimum verification evidence for changes to this layer:

- graph schema validation through `project_graph_ontology.py`;
- redaction checks: no raw source bodies, no absolute local paths, no secret-like values in returned packets;
- query packet checks for supported query kinds and bounded payloads;
- cockpit validation: eight-page structure, generated-view wording, no external assets, static fallback path;
- search-quality evals: symbol recall, top-k/MRR, trace labels, affected-test precision, edge density and thresholds;
- extension validation: stale index blocking, disabled backend lifecycle, local deterministic semantic retrieval, proposal labels, rollback/data deletion proof and graph-only fallback.

Prior closure evidence recorded focused/full checks for graph/cockpit/search/status/runtime, fixture/lifecycle/docs suites, full unittest, fixture eval, transcript eval, Codex compatibility, strict MkDocs and diff hygiene. For new changes, rerun only the smallest relevant checks unless ownership expands.

## Risks And Failure Modes

- Dynamic dispatch, framework wiring, runtime routes and actual execution behavior are not fully proven by static graph edges.
- Semantic hits and LLM proposals are orientation evidence; unsupported or uncertain claims must stay labeled and reviewable.
- Stale graph/index artifacts can mislead readers if source files changed after generation.
- Local backend store is a generated file-store and remains disabled by default; it is not a production server.
- Cockpit is static generated output; visual completeness does not prove source correctness.
- Stage directories inside a target workspace can blur source/generated boundaries unless explicitly approved.
- Future provider-backed retrieval, live runtime, canonical mutation and release actions require separate approval packets and rollback plans.

## Related Pages And Next Action

- `docs/product-agent-os/technical.md` - current technical summary for Product-Agent OS implementation status.
- `docs/product-agent-os/live-runtime-governance.md` - live/runtime/provider governance boundary.
- `docs/product-agent-os/artifact-contracts.md` - expected artifact schema reference when available.
- `docs/product-agent-os/cli-reference.md` - script/mode reference when available.

Next action for a maintainer: use this page as the reader-facing Project Code Graph guide, then link it from MkDocs navigation and source registry when the public docs map changes.
