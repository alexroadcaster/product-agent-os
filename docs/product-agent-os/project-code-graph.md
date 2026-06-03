# Project Code Graph

Source status: `official + experiment`

Эта страница описывает локальный слой Project Code Graph в Product-Agent OS. Он помогает ориентироваться в кодовой базе через сгенерированный graph, query packets, cockpit и локальные indexes, но не заменяет исходные файлы, checked-in документацию, tests, approval records или решения owner.

## Назначение

Project Code Graph отвечает за offline-навигацию по проекту:

- сканирует workspace и строит file-level graph с nodes файлов, `contains` edges, fingerprints, spans и observation records;
- добавляет Python AST overlays для package/module/class/function/method, import/call/test edges и unresolved call summaries;
- добавляет docs/contracts/schema overlays для Markdown, OpenAPI/Swagger, AsyncAPI, DBML, SQL, JSON, YAML, Mermaid и PlantUML;
- выдает bounded query packets для чтения graph без повторного чтения raw source bodies;
- рендерит static cockpit как generated view для обзорной навигации;
- добавляет extension surface для search index, backend gate, semantic retrieval, deterministic LLM proposals и closure evidence.

## Source-of-truth boundary

Generated graph artifacts are not source of truth. Они являются orientation evidence и cache-bound generated views.

Source of truth остается в исходных файлах проекта, checked-in документации, schema/contracts, tests, approval packets, RUNLOG/TEST/EVALS evidence и явно принятых owner decisions. Graph, cockpit HTML/JSON, search/backend/semantic indexes, LLM proposal packets и extension closure reports не должны использоваться как самостоятельное доказательство architecture, runtime behavior, coverage, security posture или release readiness.

Без отдельного explicit approval запрещены live server, browser automation, provider/API calls, canonical graph mutation, git stage/commit/push/PR и любые external writes. Query и stage modes должны оставаться локальными, deterministic и generated-artifact-only.

## Inputs

Основной вход:

- `<workspace>` для `scan_project_code_graph.py`;
- optional previous manifest/graph для freshness, provenance и temporal edge invalidation/supersession;
- existing `project-code-graph.json` или `project-code-graph.jsonl` для query mode;
- approval packets только для approval-bound extension modes: backend, semantic index, LLM proposals и extension closure evidence.

Scanner читает локальные файлы проекта, но graph/query packets по умолчанию исключают raw source bodies и редактируют absolute paths или secret-like values. Stage output должен быть явной директорией, предпочтительно вне target workspace.

## Outputs And Artifacts

Базовые artifacts:

- `.codex/product-agent-os/project-code-graph.json` - основной graph JSON с `write_policy: read_only`, metadata, nodes, edges и observations.
- `.codex/product-agent-os/project-code-graph.jsonl` - bounded JSONL serialization для agent consumption.
- `.codex/product-agent-os/project-cockpit.html` - offline generated cockpit, review-only.
- `.codex/product-agent-os/project-cockpit.json` - structured cockpit model and projection.
- Graph analysis report из `project_graph_analysis.py` - source-free orientation report, не доказательство completeness.
- Status/runtime summaries из query packets и cockpit model - compact health/orientation summaries.

Extension artifacts:

- `.codex/product-agent-os/project-code-graph-search-index.json` - offline static search index with stale-index blocking and rollback path.
- `.codex/product-agent-os/project-code-graph-backend.json` - disabled-by-default local query backend store; no active server by default.
- `.codex/product-agent-os/project-code-graph-semantic-index.json` - local deterministic semantic retrieval cache; external embedding/cross-encoder providers remain approval-bound.
- `.codex/product-agent-os/project-code-graph-llm-proposals.json` - staged local deterministic semantic extraction proposals with provenance, uncertainty and unsupported-claim labels.
- `.codex/product-agent-os/project-code-graph-extension-closure.json` - extension verification, rollback/data deletion proof and graph-only fallback report.

## Operating Modes And Commands

Базовый scanner и stage-only generation:

```powershell
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --dry-run
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --stage C:\tmp\product-agent-os-graph-stage
```

Graph-only queries читают существующий JSON/JSONL artifact:

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

Минимальная verification evidence для изменения этого слоя:

- graph schema validation через `project_graph_ontology.py`;
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
