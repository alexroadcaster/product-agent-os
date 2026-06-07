# Технические особенности и установка

Source status: `official + experiment`  

## Quick start

Для оператора эта страница отвечает на вопрос "какие локальные surfaces есть у plugin и где искать команду". Если нужна полная карта flags и approval boundaries, используйте [CLI Reference](cli-reference.md); если нужно понять generated outputs, используйте [Artifact Contracts](artifact-contracts.md).

| Задача | Стартовая команда или страница | Boundary |
| --- | --- | --- |
| Проверить staged infrastructure без пишет | `render_infrastructure.py <workspace> --dry-run` | Read-only plan; target workspace не меняется. |
| Сгенерировать proposal outside target workspace | `render_infrastructure.py <workspace> --stage <stage-dir>` | Stage directory должен быть явным. |
| Построить static graph/cockpit | [Project Code Graph](project-code-graph.md) | Generated graph/cockpit являются orientation evidence only. |
| Проверить live/runtime/provider gates | [Live Runtime Governance](live-runtime-governance.md) | Нет live server, provider calls или canonical graph mutation. |
| Подготовить docs и packaging closure | [Packaging And Closure](packaging-and-closure.md) | Исходные docs -> registry -> docs tests -> `check_docs.py` -> strict MkDocs -> optional full closure. |

## Capability status

Product-Agent OS ships local, approval-bound capabilities для staged infrastructure, lifecycle routing, project code graph navigation, generated cockpit views, offline search, runtime governance, provider gates, review ledgers, mutation dry-runs, audit packets, real-testing readiness, runtime QA и packaging closure.

Default contract консервативен:

- generated outputs являются staged evidence только и не является каноническим источником;
- real project testing требует owner-approved target и data policy;
- Codex App, CLI и IDE extension smoke является recorded как planning или evidence, не live browser automation через itself;
- provider surfaces keep `provider_call_allowed: false` и `external_call_performed: false` пока separate approval packet enables specific call;
- canonical graph mutation требует accepted review evidence, dry-run plan, journal и rollback proof;
- live server launch, browser automation, provider/live external model/API calls, canonical graph mutation и git stage/commit/push/PR остаются explicit-only.

Implemented graph и runtime surfaces include:

- offline static search index at `.codex/product-agent-os/project-code-graph-search-index.json`;
- disabled-by-default local query backend store at `.codex/product-agent-os/project-code-graph-backend.json`;
- local deterministic semantic retrieval cache at `.codex/product-agent-os/project-code-graph-semantic-index.json`;
- deterministic LLM-style proposal packets at `.codex/product-agent-os/project-code-graph-llm-proposals.json`;
- extension verification и rollback/data deletion proof через `project_graph_extension_closure.py`;
- approval, data classification, redaction, credentials, cache и budget governance через `project_graph_live_governance.py`;
- local read-only runtime contract через `project_graph_live_runtime.py`;
- embedding, reranker и LLM proposal provider gates через their provider-specific scripts;
- human review ledger, proposal diff preview, mutation dry-run, mutation journal и rollback proof;
- redacted audit log, security/privacy packet, observability packet и agent/skill handoff routing;
- real-testing readiness, target consent, dry-run pilot harness, Codex surface smoke и use-case pilot matrix;
- runtime browser QA expectations, performance budget и stabilization ledger.

## Operator contract

Этот operator contract separates base workspace audit profile и methodology audit complexity. Первый слой читает stack, files, control-plane state и route inputs; второй слой классифицирует methodology risk, maturity, recommendations и owner questions. `--intent-hint` может помочь routing, но не переопределяет политика источников, approvals, sandbox, писать guards или external-action boundaries.

Текущие machine-readable surfaces: renderer JSON включает `renderer_file_count`, stage manifest и status fields; runtime JSON включает `codex_runner_result`, `methodology_packet`, `finish_options`, compact first-response fields и schema v1 additive compatibility; audit/report tooling включает `run_methodology_audit.py`; behavioral evidence включает `run_transcript_eval.py` и fixture eval checks. Docs следует describe implemented commands и fields, не planned features.
Additional sources: [Codex MCP](https://developers.openai.com/codex/mcp), [Context7 MCP clients](https://context7.com/docs/resources/all-clients).  
Источники: [Codex plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://developers.openai.com/codex/skills), [Subagents](https://developers.openai.com/codex/subagents), [Codex hooks](https://developers.openai.com/codex/hooks), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex automations](https://developers.openai.com/codex/app/automations), [Product-Agent OS plugin](index.md).

## Package layout

Реализация находится в `plugins/product-agent-os/`.

```text
plugins/product-agent-os/
  .codex-plugin/plugin.json
  skills/
  scripts/
  assets/
    templates/
    fixtures/
```

Официальный contract Codex plugin требует `.codex-plugin/plugin.json`; остальные bundled components лежат в plugin root. В текущем package manifest указывает на bundled `skills` и `.mcp.json`, а пользовательская логика lives в local scripts и templates.

## Bundled MCP

`.mcp.json` registers Context7 как bundled MCP server:

```json
{
  "context7": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp"],
    "startup_timeout_sec": 20
  }
}
```

Эта keeps plugin package free из API keys и follows Codex MCP Context7 example. Projects который нужны higher Context7 limits или private sources следует provide credentials через their own trusted Codex MCP configuration, не через эта repository.

## Packaged skills

| Skill | Назначение |
| --- | --- |
| `project-lifecycle-orchestrator` | Определяет lifecycle state и следующий bounded step |
| `workspace-discovery-auditor` | Делает read-only audit workspace |
| `requirements-author` | Готовит requirements packet |
| `implementation-planner` | Готовит executable plan |
| `agent-team-designer` | Проектирует project-scoped roles и handoffs |
| `test-eval-designer` | Определяет deterministic checks и quality gates |
| `risk-reviewer` | Проверяет diff, risks, source fidelity и missing tests |
| `pr-release-operator` | Готовит PR или release packet |
| `learning-loop-maintainer` | Переносит устойчивые lessons в durable artifacts |
| `automation-promoter` | Делает candidate-only automation readiness analysis |

Каждый skill задает trigger, inputs, outputs, failure modes и final response contract. Source-sensitive skills не должны превращать community claims в project rules без verification status.

## Generated infrastructure

Renderer может создать или предложить:

- `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- `.codex/config.toml`;
- `.codex/agents/*.toml`;
- `.codex/hooks/*`;
- `.codex/workflows/*.md`;
- `.codex/artifact-templates/*.md`;
- `.codex/evals/*.json`;
- `.codex/pr/*`;
- `.codex/automation-candidates/automation-candidate.md`;
- `.codex/workflows/system-file-hygiene-audit.md`;
- `.codex/artifact-templates/system-file-hygiene-report.md`;
- `.codex/automation-candidates/system-file-hygiene-audit.md`.

Workflow inventory включает two methodology packets:

- `.codex/workflows/development-standards.md` - product hypothesis, architecture boundary, test-first/eval-first path, bounded agentic implementation, review и measurement.
- `.codex/workflows/documentation-system.md` - docs-as-code routing для architecture docs, API contracts, UI component docs, database docs, code reference и release docs.

Concrete artifact templates keep methodology guidance actionable:

- `.codex/artifact-templates/adr.md`;
- `.codex/artifact-templates/architecture-overview.md`;
- `.codex/artifact-templates/domain-modeling.md`;
- `.codex/artifact-templates/metric-spec.md`;
- `.codex/artifact-templates/api-contract-review.md`;
- `.codex/artifact-templates/component-card.md`;
- `.codex/artifact-templates/database-dictionary.md`;
- `.codex/artifact-templates/docs-tooling-decision.md`.

Scenario routing adds workflow coverage:

| Status | Generated или routed surface |
| --- | --- |
| `done` | `.codex/workflows/first-run-intake.md`, `.codex/workflows/bug-rescue.md`, `.codex/workflows/greenfield-idea-to-plan.md`, `.codex/workflows/complex-system-acceleration.md`, `.codex/workflows/pr-review-readiness.md`, `.codex/workflows/legacy-onboarding.md`, `.codex/workflows/api-migration.md`, `.codex/workflows/ai-eval-regression.md`, `.codex/workflows/native-mobile-feature.md`, `.codex/workflows/desktop-local-first.md`, `.codex/workflows/data-migration.md`, `.codex/workflows/security-sensitive-change.md`, `.codex/workflows/ci-stabilization.md`, `.codex/workflows/release-packaging.md`. |
| `done` | `.codex/artifact-templates/bug-rescue-report.md`, `greenfield-idea-brief.md`, `integration-catalog.md`, `pr-risk-review.md`, `onboarding-map.md`, `migration-plan.md`, `ai-eval-spec.md`, `security-risk-review.md`, `ci-stabilization-report.md`, `release-readiness.md`. |
| `done methodology gate` | `acceptance-scenarios.md`, `domain-modeling.md`, `architecture-overview.md`, `component-card.md`, `metric-spec.md`, `release-packet.md`, `docs-tooling-decision.md`, `plan-quality-check.md`, `agent-task-packet.md`, `project-readiness.json` и `behavioral-workflows.json` cover ATDD/BDD traceability, conditional DDD domain modeling, bounded-context-to-architecture traceability, ubiquitous language traceability, optional `fsd_structure`, metric hardening, evidence-before-completion, docs tooling selection, conditional readiness statuses, no-placeholder planning, two-stage review и fresh-context handoff. |

First-run intake является visible в runtime route packet, lifecycle skills и behavioral evals для empty, broken, existing control-plane и complex system starts. Release packaging является visible в `usage_mode`, fixture evals, renderer output, lifecycle skills, и packaged `release-packaging.md` / `release-readiness.md` templates. Dedicated operator docs now live в [scenarios](scenarios.md), [behavioral evals](behavioral-evals.md) и [Codex compatibility](codex-compatibility.md).

Generation является staged-first. Existing user-authored files являются preserved outside managed sections:

```markdown
<!-- product-agent-os:start section-id -->
...
<!-- product-agent-os:end section-id -->
```

Если existing file не имеет managed markers, plugin stages companion proposal instead из overwriting it.

## Local commands

Read-only infrastructure plan:

```powershell
python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --dry-run
```

Stage generated artifacts outside target workspace:

```powershell
python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --stage <stage-dir>
```

Plan merge из staged artifacts:

```powershell
python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --plan
```

Применить требует approval record:

```powershell
python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --apply --approval-file <approval.json>
```

Запустите Codex-only runtime contract mode:

```powershell
python plugins\product-agent-os\scripts\run_codex_runtime_runner.py <workspace> --contract
```

Allow route recommendation к Codex subagent когда текущий Codex thread explicitly permits it:

```powershell
python plugins\product-agent-os\scripts\run_codex_runtime_runner.py <workspace> --contract --allow-subagents
```

Запустите plugin fixture evals:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Read-only audit системных файлов:

```powershell
python plugins\product-agent-os\scripts\validate_system_file_hygiene.py <workspace> --trigger soft_size_review
```

## Self-verification metrics loop

Product-Agent OS включает local, read-only `agent_skill_metrics_loop` contract для reviewing agents, skills, prompt/policy packs, router/tool policies и harness versions после real work leaves evidence. Цикл collects target registry, проверяет trace intake, checks dataset quality, records local grader summaries, blocks uncalibrated grader/judge calibration, builds cadence recommendation values `L0`, `L1`, `L2` и `L3`, и пишет staged scorecard ledger или report packets.

Main files и commands:

- `plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics.py` - source priority, target registry, trace intake, dataset quality, grader/judge calibration, metrics, scorecards, cadence recommendation и run-record contracts.
- `plugins/product-agent-os/scripts/product_agent_os/agent_skill_metrics_report.py` - redacted offline report rendering для `agent-skill-evaluation-report.html`.
- `plugins/product-agent-os/scripts/render_agent_skill_metrics_report.py` - dry-run или stage-only report CLI.
- `.codex/artifact-templates/agent-skill-scorecard-ledger.md`, `.codex/artifact-templates/agent-skill-metrics-daily.md`, `.codex/artifact-templates/agent-skill-metrics-weekly.md` и `.codex/artifact-templates/agent-skill-update-candidate.md` - generated review artifacts.

Политика канонического источника остается explicit: control-plane artifacts, `run records`, trace/eval packets и accepted gaps могут поддерживать metrics; generated dashboard/report HTML, memory, raw chat logs и unsupported community claims не могут. Report не является источником истины. Все metrics outputs являются только staged evidence, а не proof того, что real project является semantically ready.

Approval boundary: Product-Agent OS не выполняет live eval/model/API calls, не создает active schedules, не делает external writes, не applies modernization candidates и не allows self-applied updates. Modernization candidate требует owner review, rollback target и explicit approval state до изменений target workspace, skill, prompt/policy pack, router/tool policy или harness configuration.

## System file hygiene audit

Product-Agent OS включает read-only контракт `system_file_hygiene_audit`, чтобы системные файлы проекта оставались компактными и source-owned. Проверка использует hybrid triggers: weekly full review, monthly deep ownership review, on-change review после правок системных файлов, size-threshold review и release/automation approval review.

Поддерживаемые поверхности: root control-plane files, `README.md`, nested `AGENTS.md`, `.codex/config.toml`, MCP config, `.codex/agents`, `.codex/skills`, `.codex/workflows`, `.codex/artifact-templates`, `.codex/automation-candidates`, `.codex/hooks`, `.codex/evals`, `.codex/pr`, docs source-control files, `.github/workflows`, `CODEOWNERS`, `SECURITY.md` и checked-in plugin package control files. Audit reports покрывает size limits, duplicate headings, mojibake/BOM markers, secret-like literals, historical ledger leakage и active schedule markers внутри automation candidates.

Audit не сокращает файлы самостоятельно и не создает schedule. Результат: JSON плюс staged `system-file-hygiene-report.md`; любая правка, hook activation, GitHub workflow, Codex App automation, MCP change или external write остается отдельным owner-approved slice.

JSON пакет содержит `audit_trigger`, `finding_type`, `compaction_decision`, `approval_boundary`, `no_secrets_status` и `active_schedule_markers`. CLI `--trigger` записывает причину запуска, печатает JSON, возвращает `0` для `ok` или `review_required` и возвращает `1` только для `blocked`; workspace остается read-only.

Status dashboard projection показывает `file_statuses`, `mtime_utc`, `age_days`, `content_digest` и `top_finding` как generated review evidence. Даты берутся из filesystem metadata: это подсказки свежести для review, а не семантическое доказательство, что содержимое файла корректно или достаточно актуально для completion claim.

## Project code graph и cockpit

Local read-only graph foundation и generated cockpit поддерживают project navigation. Scanner inventories files, emits stable file-level graph nodes и `contains` edges, adds Python AST package/module/class/function/method overlays, adds conservative import/call/test edges, builds structured overlays для parseable Markdown, OpenAPI/Swagger, AsyncAPI, DBML, SQL, JSON, YAML, Mermaid и PlantUML inputs, проверяет controlled ontology, records manifest freshness/provenance, stores observation records с relative paths/spans/fingerprints и поддерживает temporal edge invalidation/supersession helpers. Query mode читает existing JSON/JSONL graph artifacts и produce bounded `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `changed_since`, `why_changed`, `read_order`, `hotspots`, `node`, `status` и `search` packets. Это исключает raw source bodies через default и redacts local absolute paths или secret-like values из returned packets.

Main files и commands:

- `plugins/product-agent-os/scripts/product_agent_os/project_code_graph.py` - graph JSON/JSONL packet builder.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_adapters.py` - Python AST scanner и unsupported-language adapter boundary.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_chunking.py` - structured docs/contracts/schema/diagram overlays, partitions, aliases и readiness summaries.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_manifest.py` - file fingerprints, freshness и provenance.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_observations.py` - observation records и edge delta lineage.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_ontology.py` - controlled ontology и graph schema validation.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_queries.py` - bounded graph-only query packets.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_analysis.py` - source-free graph analysis report.
- `plugins/product-agent-os/scripts/product_agent_os/project_cockpit_model.py` - eight-page cockpit information architecture и Code Flow section model.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_visual_model.py` - Graphology-compatible static projection, large-graph bounds, selected evidence и local Graphology/Sigma vendor boundary.
- `plugins/product-agent-os/scripts/product_agent_os/project_graph_renderer.py` - offline stage-only cockpit HTML/JSON renderer с нет external assets.
- `plugins/product-agent-os/scripts/scan_project_code_graph.py` - dry-run, stage-only scanner и graph query CLI.
- `plugins/product-agent-os/assets/templates/project-graph/` - local cockpit, graph, Code Flow и CSS templates.

```powershell
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --dry-run
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --stage C:\tmp\product-agent-os-graph-stage
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --query neighbors --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --node-id function:app.main.main
```

Stage mode должен использовать output directory outside target workspace. Query mode reads existing graph artifact и не scan source text. Existing graph artifacts в target workspace являются не modified. Этот graph остается conservative: dynamic dispatch, framework wiring, runtime routes и semantic/rationale extraction являются не verified dependency proof. Runtime/status summaries и graph analysis reports являются orientation evidence only.

Cockpit rendering использует `render_project_graph_cockpit_plan()` для dry-run plans и `stage_project_graph_cockpit()` для explicit stage directories outside target workspace. Это stages `.codex/product-agent-os/project-cockpit.html` и `.codex/product-agent-os/project-cockpit.json`. Этот staged HTML exposes exactly eight top-level pages, keeps Code Flow inside `Code Intelligence`, embeds safe JSON, использует static local CSS/JS, имеет filter/reset/copy/select commands, selected-node evidence, fallback static table, mobile layout и generated-view-only wording. Graphology и Sigma являются recorded как local Graphology/Sigma vendor-only capabilities; нет vendored assets являются currently bundled, so verified renderer использует static fallback path с Graphology-compatible static projection data.

Fixture structural fields, search-quality evals, local backend gates и semantic gates keep graph features bounded. Fixture eval records graph contract, нет external assets, redaction, scale bounds, generated-view-only, eight-page cockpit structure, section preservation, cockpit generated-view boundary, `project_graph_search_quality_present` и `project_graph_future_backend_semantic_gates_present`. Search-quality evals являются local и deterministic: they record symbol recall, top-k/MRR, trace success или failure labels, affected-test precision, edge density и explicit thresholds. Этот approved static index, local backend gate и local deterministic semantic retrieval gate являются implemented; live database/server, live external model/API embedding или cross-encoder providers, LLM semantic extraction и rationale/comment extraction stay outside approved surface пока explicit approval defines redaction, cache, token budget, eval threshold и rollback path.

Focused и full verification следует cover graph/cockpit/search, status/runtime и fixture/lifecycle/docs suites до claiming readiness. Этот explicit-only git boundary остается в force. Approved extensions являются limited к staged proposals, generated extension closure evidence, rollback/data deletion proof и graph-only fallback. Live production server, live external model/API extraction и canonical graph mutation still требуют separate explicit approval.

## Codex installation boundary

Для Codex installation plugin должен быть доступен через plugin marketplace или curated plugin list, а package root должен содержать `.codex-plugin/plugin.json`. В этом репозитории package уже подготовлен локально в рамках `plugins/product-agent-os/`; подключение к конкретной Codex App installation остается отдельным environment step и следует follow текущий official Codex plugin docs.

Этот project intentionally keeps runtime code Codex-only:

- нет separate OpenAI API key;
- нет standalone Agents SDK application;
- нет background MCP server started через plugin scripts; Context7 является declared как bundled Codex MCP server и начинается только когда Codex enables который MCP configuration;
- нет active automation created из templates;
- нет plugin-root hook activation без explicit approval.

## Guardrails

| Guardrail | Enforcement |
| --- | --- |
| Политика источников | `validate_source_policy.py` blocks unsupported OpenAI/Codex claims и secret-like content |
| Automation policy | `validate_automation_candidate.py` требует manual success evidence, owner, cadence, verification, rollback и approval |
| Staged manifest | stage paths должен stay inside stage root и target paths inside workspace |
| Approval record | approved пишет требуют explicit decisions и matching plan digest |
| Rollback | apply может produce rollback manifest для later rollback |
| Runtime runner | проверяет lifecycle route, approval boundary, политика источников, handoff shape и redaction |
| Transcript/session eval runner | `run_transcript_eval.py` replays synthetic или redacted sessions against `behavioral-workflows.json` без external model calls |
| Redaction | secret assignments, local absolute paths и private data markers являются redacted из runner result |
| Engineering standards | templates требуют product metrics, architecture boundary, test/eval gates, влияние на docs и measurement notes |
| Methodology discovery | workspace audit reports architecture docs, ADR, domain model, architecture context maps, optional `fsd_structure`, OpenAPI, AsyncAPI, Storybook, DB docs, CODEOWNERS, CI, evals и metrics signals |
| Scenario routing | `usage_mode` distinguishes completed workflows, partial methodology gates, и base modes; это returns minimum artifacts plus evidence gaps |

## Проверка commands для эта repo

After docs или nav changes:

```powershell
python tools\check_docs.py
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; python -m mkdocs build --strict
```

After plugin scripts, templates, fixtures или tests change:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
```
