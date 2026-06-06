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

Generated graph artifacts не являются источником истины. Это orientation evidence и cache-bound generated views.

source of truth остается в исходных файлах проекта, checked-in документации, schema/contracts, tests, approval packets, RUNLOG/TEST/EVALS evidence и явно принятых owner decisions. Graph, cockpit HTML/JSON, search/backend/semantic indexes, LLM proposal packets и extension closure reports не должны использоваться как самостоятельное доказательство architecture, runtime behavior, coverage, security posture или release readiness.

Без отдельного explicit approval запрещены live server, browser automation, provider/API calls, canonical graph mutation, git stage/commit/push/PR и любые external writes. Query и stage modes должны оставаться локальными, deterministic и generated-artifact-only.

## Входы

Основной вход:

- `<workspace>` для `scan_project_code_graph.py`;
- optional previous manifest/graph для freshness, provenance и temporal edge invalidation/supersession;
- existing `project-code-graph.json` или `project-code-graph.jsonl` для query mode;
- approval packets только для approval-bound extension modes: backend, semantic index, LLM proposals и extension closure evidence.

Scanner читает локальные файлы проекта, но graph/query packets по умолчанию исключают raw source bodies и редактируют absolute paths или secret-like values. Stage output должен быть явной директорией, предпочтительно вне target workspace.

## Выходы и артефакты

Базовые artifacts:

- `.codex/product-agent-os/project-code-graph.json` - основной graph JSON с `write_policy: read_only`, metadata, nodes, edges и observations.
- `.codex/product-agent-os/project-code-graph.jsonl` - bounded JSONL serialization для agent consumption.
- `.codex/product-agent-os/project-cockpit.html` - offline generated cockpit, review-only.
- `.codex/product-agent-os/project-cockpit.json` - structured cockpit model и projection.
- Graph analysis report из `project_graph_analysis.py` - source-free orientation report, не доказательство completeness.
- Status/runtime summaries из query packets и cockpit model - compact health/orientation summaries.

Extension artifacts:

- `.codex/product-agent-os/project-code-graph-search-index.json` - offline static search index с stale-index blocking и rollback path.
- `.codex/product-agent-os/project-code-graph-backend.json` - disabled-by-default local query backend store; нет active server через default.
- `.codex/product-agent-os/project-code-graph-semantic-index.json` - local deterministic semantic retrieval cache; external embedding/cross-encoder providers остаются approval-bound.
- `.codex/product-agent-os/project-code-graph-llm-proposals.json` - staged local deterministic semantic extraction proposals с provenance, uncertainty и unsupported-claim labels.
- `.codex/product-agent-os/project-code-graph-extension-closure.json` - extension verification, rollback/data deletion proof и graph-only fallback report.

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

Supported query kinds включают `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `changed_since`, `why_changed`, `read_order`, `hotspots`, `node`, `status` и `search`. Query packets являются bounded через `--max-results`, `--max-depth`, `--max-tokens`, filters и hub suppression.

Extension modes:

```powershell
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --build-index --stage C:\tmp\product-agent-os-graph-stage --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --build-backend --stage C:\tmp\product-agent-os-graph-stage --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --backend-approval approval.json
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --build-semantic-index --stage C:\tmp\product-agent-os-graph-stage --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --semantic-approval approval.json
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --build-llm-proposals --stage C:\tmp\product-agent-os-graph-stage --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --llm-approval approval.json
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --verify-extensions --stage C:\tmp\product-agent-os-graph-stage --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --verification-evidence evidence.json
```

Disable modes remove generated extension artifacts в рамках stage root: `--disable-backend`, `--disable-semantic-index`, `--disable-llm-proposals` и `--disable-extensions`.

## Проверка

Минимальная verification evidence для изменения этого слоя:

- graph schema validation через `project_graph_ontology.py`;
- redaction checks: нет raw source bodies, нет absolute local paths, нет secret-like values в returned packets;
- query packet checks для supported query kinds и bounded payloads;
- cockpit validation: eight-page structure, generated-view wording, нет external assets, static fallback path;
- search-quality evals: symbol recall, top-k/MRR, trace labels, affected-test precision, edge density и thresholds;
- extension validation: stale index blocking, disabled backend lifecycle, local deterministic semantic retrieval, proposal labels, rollback/data deletion proof и graph-only fallback.

Prior closure evidence recorded focused/full checks для graph/cockpit/search/status/runtime, fixture/lifecycle/docs suites, full unittest, fixture eval, transcript eval, Codex compatibility, strict MkDocs и diff hygiene. Для new changes, rerun только smallest relevant checks пока ownership expands.

## Риски And Failure Modes

- Dynamic dispatch, framework wiring, runtime routes и actual execution behavior являются не fully proven через static graph edges.
- Semantic hits и LLM proposals являются orientation evidence; unsupported или uncertain claims должен stay labeled и reviewable.
- Stale graph/index artifacts может mislead readers если source files changed после generation.
- Local backend store является generated file-store и остается disabled через default; это является не production server.
- Cockpit является static generated output; visual completeness не prove source correctness.
- Stage directories inside target workspace может blur source/generated boundaries пока explicitly approved.
- Future provider-backed retrieval, live runtime, canonical mutation и release actions требуют separate approval packets и rollback plans.

## Связанные страницы и следующий шаг

- `docs/product-agent-os/technical.md` - текущий technical summary для Product-Agent OS implementation status.
- `docs/product-agent-os/live-runtime-governance.md` - live/runtime/provider governance boundary.
- `docs/product-agent-os/artifact-contracts.md` - expected artifact schema reference когда available.
- `docs/product-agent-os/cli-reference.md` - script/mode reference когда available.

Следующий action для maintainer: использовать эта page как reader-facing Project Code Graph guide, затем link это из MkDocs navigation и source registry когда public docs map changes.
