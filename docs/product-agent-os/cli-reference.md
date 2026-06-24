# Product-Agent OS CLI reference

Source status: `official + experiment`

Эта страница фиксирует локальные поверхности `CLI`, которые уже есть в `plugins/product-agent-os/scripts/`. Команды рассматриваются как `stage/read-only tooling`: они не публикуют plugin, не запускают внешние системы и не выполняют `live provider/model/API calls` без отдельного `explicit approval`.

## Назначение

Слой `CLI` нужен для повторяемого локального цикла доказательств:

- аудит только для чтения или пакет `dry-run` перед изменениями;
- генерация только в явный каталог вывода;
- слияние или откат только через отдельную запись approval;
- детерминированный runtime contract для Codex App, CLI или IDE extension;
- генерация graph, query-пакеты, cockpit, локальные индексы и governance-пакеты для provider/mutation;
- проверка документации и закрытия через отдельные роли `docs-maintainer` и `tester`.

Сгенерированные выходы не являются источником истины. Источником истины остаются исходные файлы, проектная документация, `source registry`, `control-plane artifacts`, текущие доказательства команд и `owner-approved records`.

## Основные команды

| Команда | Назначение | Обязательные входы | Вывод / граница |
| --- | --- | --- | --- |
| `python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --dry-run` | Печатает план генерации инфраструктуры. | Путь workspace. | JSON/text план только для чтения; staged files не создаются. |
| `python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --stage <stage-dir>` | Создает control-plane/templates в staging-каталоге. | Workspace и явный stage directory. | Запись только в рамках `<stage-dir>`; прямое слияние в target остается отдельным шагом. |
| `python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --plan` | Строит план слияния только для чтения. | Workspace и stage directory. | Не пишет в target workspace. |
| `python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --apply --approval-file <approval.json>` | Применяет решения merge с `approval`. | `Approval file`, соответствующий плану. | Пишет только разрешенный `target scope`; `rollback manifest` создается через `merge tooling`. |
| `python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --rollback <rollback.json>` | Откатывает предыдущее approved merge. | Rollback manifest. | Восстанавливает scoped files из recorded rollback data. |
| `python plugins\product-agent-os\scripts\run_codex_runtime_runner.py <workspace> --contract` | Создает детерминированный `Codex runtime route packet`. | Workspace. | `Offline contract`; нет `external model call`. |
| `python plugins\product-agent-os\scripts\run_codex_runtime_runner.py <workspace> --contract --allow-subagents` | Разрешает `route recommendations` с упоминанием subagents. | Workspace и explicit subagent permission в текущем workflow. | Только рекомендация; agents не создаются автоматически. |
| `python plugins\product-agent-os\scripts\render_status_dashboard.py <workspace> --dry-run` | Печатает план status dashboard. | Workspace. | Записи нет. |
| `python plugins\product-agent-os\scripts\render_status_dashboard.py <workspace> --stage <stage-dir>` | Создает status dashboard HTML/JSON в staging-каталоге. | Workspace и explicit stage directory. | `Generated view only`; не является каноническим источником. |
| `python plugins\product-agent-os\scripts\render_agent_skill_metrics_report.py <workspace> --dry-run` | Печатает план metrics report. | Workspace. | Записи нет. |
| `python plugins\product-agent-os\scripts\render_agent_skill_metrics_report.py <workspace> --stage <stage-dir>` | Создает agent/skill metrics report в staging-каталоге. | Workspace и explicit stage directory. | Candidate-only report; modernization не применяется. |

Optional inputs runtime runner включают `--approval-status`, `--intent-hint` и `--output`. Они меняют emitted route packet или сохраняют JSON, но не обходят политику источников, sandbox, approvals или external-action boundaries.

## First-run Analysis CLI

| Команда | Назначение | Входы | Вывод / граница |
| --- | --- | --- | --- |
| `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --full-dry-run` | Выполняет safe first-run orchestration без записи файлов. | Путь `target workspace`. | Preview только для чтения; `generated files` не создаются. |
| `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --dry-run` | Печатает first-run packet без записи файлов. | Путь `target workspace`. | Preview только для чтения; `generated files` не создаются. |
| `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --stage <dir>` | Создает `first-run generated artifacts` в explicit stage directory. | `Target workspace` и `stage directory`. | `Stage root` должен быть вне `target workspace`; `stage-inside-target is blocked`. |
| `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --write-analysis` | Записывает `generated first-run packet` и offline HTML в локальную analysis folder. | Путь `target workspace`. | Запись только в `.codex/product-agent-os/analysis/`; `generated views` остаются `orientation_only_not_proof`. |
| `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --write` | `Legacy write route` для локального пакета первого анализа. | Путь `target workspace`. | Запись `generated packet`, включая `.codex/product-agent-os/analysis/first-run-analysis-packet.json`; не является `target source mutation`. |

`run_first_project_analysis.py` выбирает ровно один режим: `--full-dry-run`, `--dry-run`, `--stage <dir>`, `--write-analysis` или `--write`. Полная матрица команд принадлежит `DOC-M26`: см. [матрицу команд](operator-command-matrix.md). Redocly `not_applicable` до появления `OpenAPI source contract`. Эти команды не выдают `approval` на `live servers`, `browser automation`, `provider/API calls`, `target source mutation`, `git actions`, `release`, `promotion` или root `site` rebuild.

Безопасные operator examples:

```powershell
python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --full-dry-run
python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --dry-run
python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --stage C:\tmp\product-agent-os-first-run
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --dry-run
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --stage C:\tmp\product-agent-os-graph-stage
```

Эти examples не являются `broad command matrix`. Полная `command-policy` матрица, `docs tooling smokes`, `install/runtime variations` и `approval-state coverage` принадлежат `DOC-M26`. `CLI docs` дают только безопасные pointers и не расширяют разрешение на `live server`, `browser automation`, `provider/API calls`, `canonical mutation`, `git actions` или root `site` rebuild.

## Self-Learning Loop Due-Check CLI

| Команда | Назначение | Входы | Вывод / граница |
| --- | --- | --- | --- |
| `python plugins\product-agent-os\scripts\check_self_learning_due.py <workspace> --dry-run` | Проверяет, пора ли предложить ручной запуск Self-Learning Loop. | Product-Agent OS workspace с `.codex/product-agent-os/self-learning-state.json`. | Печатает `due`, `not_due`, `disabled` или `state_invalid`; не запускает анализ, не пишет state, не создает schedule и не включает auto-apply. |

`weekly` в этом контракте означает due-check basis, а не active schedule. Ручной запуск loop остается отдельной будущей поверхностью и требует своего approval/write boundary.

## Project Graph CLI

`scan_project_code_graph.py` использует exactly-one-mode semantics: выбирайте один mode за запуск.

| Mode | Назначение | Обязательные входы | Вывод / граница |
| --- | --- | --- | --- |
| `--dry-run` | Строит `graph packet` без записи файлов. | `<workspace>`. | Печатает graph JSON; записи нет. |
| `--stage <stage-dir>` | Создает graph и `cockpit artifacts`. | `<workspace>`, explicit stage directory. | Пишет `generated graph/cockpit files` в рамках `stage root`. |
| `--query <kind>` | Читает `bounded query packet` из `existing graph`. | `--graph <project-code-graph.json>` plus query args. | Читает `existing graph artifact`; source не сканируется заново. |
| `--build-index` | Строит offline static search index. | `--stage`, `--graph`. | `Generated index cache`; не является каноническим источником. |
| `--build-backend` | Создает disabled-by-default local query backend store. | `--stage`, `--graph`, `--backend-approval`. | `Generated file-store`; `active server` по умолчанию не запускается. |
| `--build-semantic-index` | Создает local deterministic semantic retrieval index. | `--stage`, `--graph`, `--semantic-approval`. | `Generated semantic cache`; `provider calls` остаются `blocked` до отдельного `approval`. |
| `--build-llm-proposals` | Создает local deterministic LLM-style proposal packets. | `--stage`, `--graph`, `--llm-approval`. | Только proposals, не canonical facts. |
| `--verify-extensions` | Создает extension verification и rollback closure. | `--stage`, `--graph`, `--verification-evidence`. | Closure packet и rollback/data deletion proof. |
| `--validate-live-governance` | Создает live governance packet. | `--stage`, `--live-approval`. | Нет `live calls`; проверяет `approval/data/redaction/cache/budget boundary`. |
| `--validate-live-runtime` | Создает local read-only runtime contract. | `--stage`, `--live-runtime-approval`, `--live-governance`. | `Disabled-by-default local runtime contract`; запуска нет. |
| `--validate-embedding-provider` | Создает embedding provider gate. | `--stage`, `--embedding-provider-approval`, graph/semantic inputs как required. | `Provider gate/eval packet`; `provider call` запрещен до `later execution approval`. |
| `--validate-reranker-provider` | Создает reranker provider gate. | `--stage`, `--reranker-provider-approval`. | `Provider gate packet`; `external call` по умолчанию нет. |
| `--build-hybrid-retrieval` | Создает hybrid retrieval pipeline. | `--stage`, graph/index/semantic/reranker inputs. | Generated explainable fusion packet; canonical mutation не выполняется. |
| `--validate-llm-proposal-provider` | Создает LLM proposal provider gate. | `--stage`, `--llm-proposal-provider-approval`, proposal/eval inputs. | `Provider gate` и safety eval; proposal-only. |
| `--build-review-ledger` | Создает human review ledger и proposal diff. | `--stage`, `--review-ledger-approval`, `--review-decisions`. | Owner decision ledger; остается non-mutating. |
| `--build-canonical-mutation` | Создает mutation dry-run, journal и rollback artifacts. | `--stage`, `--canonical-mutation-approval`, review ledger и proposal diff. | Только `staged mutated graph copy`; `canonical source graph` не меняется silently. |
| `--build-live-audit` | Создает audit/security/observability/handoff packets. | `--stage`, `--live-audit-approval`, live runtime/actions/security inputs. | Redacted audit и `operability evidence`. |
| `--build-real-testing-readiness` | Создает readiness, `target consent` и pilot artifacts. | `--stage`, `--real-testing-approval` и target/gate/pilot inputs. | Только `dry-run pilot/readiness evidence`. |
| `--build-runtime-qa` | Создает runtime QA, performance и `stabilization artifacts`. | `--stage`, `--runtime-qa-approval` и QA/performance/stabilization inputs. | `Staged QA evidence`; `live browser automation` в docs work нет. |

Disable modes удаляют `generated artifacts` в рамках `stage root`: `--disable-backend`, `--disable-semantic-index`, `--disable-llm-proposals`, `--disable-extensions`, `--disable-live-governance`, `--disable-live-runtime`, `--disable-embedding-provider`, `--disable-reranker-provider`, `--disable-hybrid-retrieval`, `--disable-llm-proposal-provider`, `--disable-review-ledger`, `--disable-canonical-mutation`, `--disable-live-audit`, `--disable-real-testing-readiness` и `--disable-runtime-qa`.

## Входы query

Graph query mode accepts:

- `--graph` для `project-code-graph.json` или `project-code-graph.jsonl`;
- optional `--index`, `--backend`, `--semantic-index`, `--hybrid-retrieval` и `--reranker-provider`;
- `--node-id`, `--target-id` и `--text` для query-specific selectors;
- `--max-results`, `--max-depth`, `--max-tokens`, `--hub-threshold`, `--node-type`, `--edge-type`, `--confidence` и `--path-prefix` для bounded output.

Supported query kinds включают `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `changed_since`, `why_changed`, `read_order`, `hotspots`, `node`, `status` и `search`.

## Query-поверхность cockpit

Project graph CLI передает данные в cockpit, но не превращает cockpit в доказательство:

- `--stage <stage-dir>` пишет generated `project-code-graph.json`, `project-code-graph.jsonl`, `project-cockpit.html` и `project-cockpit.json` внутри stage root.
- `--query read_order --graph <project-code-graph.json>` возвращает `bounded guided read order`; используйте его как подсказку чтения, затем проверяйте `source files` перед правками или `impact claims`.
- `--query trace`, `--query impact` и `--query affected_tests` создают static query packets; они не доказывают runtime routes, dynamic dispatch или test results.
- `--query search` может использовать graph-only search, static index, semantic index или hybrid inputs, если они переданы; returned hits остаются orientation evidence.

Примеры команд для чтения cockpit:

```powershell
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --query read_order --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --max-results 12
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --query trace --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json --node-id function:app.main.main --max-depth 3
python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --query status --graph C:\tmp\product-agent-os-graph-stage\.codex\product-agent-os\project-code-graph.json
```

Static fallback является поддержанной `visual boundary` в этом docs slice. Cosmos.gl/WebGL, `browser screenshots`, `interactive canvas behavior`, `performance proof` и `accessibility visual proof` остаются unsupported до появления отдельного `approved runtime/browser evidence packet`.

## Проверка команд

Базовые локальные команды проверки:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
python -m mkdocs build --strict
git diff --check
```

Запустите минимальный релевантный набор для текущего slice. Закрывающий claim требует порядок: `source docs -> registry -> docs tests -> check_docs.py -> strict MkDocs -> optional full closure`.

## Риски и сбои

- Запуск `stage command` внутри `target workspace` может смешать generated и source-of-truth boundaries.
- Approval JSON недостаточен, если `owner`, `allowed surfaces`, `data policy`, rollback и `verification evidence` отсутствуют.
- Query packets могут устареть, если `graph fingerprints` больше не совпадают с текущим source.
- Provider gate commands не являются permission к `call providers`.
- Canonical mutation dry-run не является permission к `mutate checked-in source` или graph facts.
- Git commands остаются explicit-only и находятся вне этих CLI reference commands.

## Следующее действие

Используйте эту страницу как operator reference для local scripts. `Navigation`, `source registry entries`, `docs tests` и `generated site refresh` принадлежат своим `docs-maintainer` и `tester` slices.
