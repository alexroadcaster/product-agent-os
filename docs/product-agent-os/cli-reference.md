# Product-Agent OS CLI reference

Source status: `official + experiment`

Эта страница фиксирует локальные Product-Agent OS CLI surfaces, которые уже есть в `plugins/product-agent-os/scripts/`. Она описывает команды как stage/read-only tooling: они не публикуют plugin, не запускают внешние системы и не выполняют live provider/model/API calls без отдельного explicit approval.

## Назначение

CLI слой нужен для повторяемого локального evidence loop:

- read-only audit или dry-run packet перед изменениями;
- stage-only generation в явный output directory;
- approval-bound merge или rollback только через отдельный approval record;
- deterministic runtime contract для Codex App, CLI или IDE extension;
- project graph generation, queries, generated cockpit, local indexes и provider/mutation governance packets;
- docs/closure verification через отдельные docs-maintainer и tester slices.

Сгенерированные выходы не являются источником истины. Источником истины остаются checked-in source files, project docs, source registry, control-plane artifacts, текущий command evidence и owner-approved records.

## Core Commands

| Command | Purpose | Обязательные входы | Output / boundary |
| --- | --- | --- | --- |
| `python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --dry-run` | Print infrastructure render plan. | Target workspace path. | Read-only JSON/text plan; нет staged files. |
| `python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --stage <stage-dir>` | Stage generated control-plane/templates. | Workspace и explicit stage directory. | Writes только в рамках `<stage-dir>`; direct target merge остается separate. |
| `python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --plan` | Build read-only merge plan. | Workspace и stage directory. | Нет пишет к target workspace. |
| `python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --apply --approval-file <approval.json>` | Применить approved merge decisions. | Approval file matching plan. | Approved target пишет only; rollback manifest может быть produced через merge tooling. |
| `python plugins\product-agent-os\scripts\merge_infrastructure.py <workspace> <stage-dir> --rollback <rollback.json>` | Roll back prior approved merge. | Rollback manifest. | Restores scoped files из recorded rollback data. |
| `python plugins\product-agent-os\scripts\run_codex_runtime_runner.py <workspace> --contract` | Produce deterministic Codex runtime route packet. | Workspace. | Offline contract; нет external model call. |
| `python plugins\product-agent-os\scripts\run_codex_runtime_runner.py <workspace> --contract --allow-subagents` | Allow route recommendations который mention subagents. | Workspace и explicit subagent permission в текущий workflow. | Recommendation only; не create agents через itself. |
| `python plugins\product-agent-os\scripts\render_status_dashboard.py <workspace> --dry-run` | Print status dashboard plan. | Workspace. | Нет write. |
| `python plugins\product-agent-os\scripts\render_status_dashboard.py <workspace> --stage <stage-dir>` | Stage generated status dashboard HTML/JSON. | Workspace и explicit stage directory. | Generated view only, не является каноническим источником. |
| `python plugins\product-agent-os\scripts\render_agent_skill_metrics_report.py <workspace> --dry-run` | Print metrics report plan. | Workspace. | Нет write. |
| `python plugins\product-agent-os\scripts\render_agent_skill_metrics_report.py <workspace> --stage <stage-dir>` | Stage agent/skill metrics report. | Workspace и explicit stage directory. | Candidate-only report; нет modernization является applied. |

Runtime runner optional inputs включают `--approval-status`, `--intent-hint` и `--output`. Они change emitted route packet или save JSON; they не bypass политика источников, sandbox, approvals или external-action boundaries.

## First-run Analysis CLI

| Команда | Назначение | Входы | Вывод / граница |
| --- | --- | --- | --- |
| `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --dry-run` | Печатает first-run packet без записи файлов. | Путь target workspace. | Read-only preview; generated files не создаются. |
| `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --write` | Записывает локальный пакет первого анализа. | Путь target workspace. | Запись только в `.codex/product-agent-os/analysis/`, включая `.codex/product-agent-os/analysis/first-run-analysis-packet.json`; generated views остаются `orientation_only_not_proof`. |

`run_first_project_analysis.py` выбирает ровно один режим: `--dry-run` или `--write`. Команда не выдает approval на live servers, browser automation, provider/API calls, target source mutation, git actions, release или promotion.

```text
does not accept `--stage`
```

## Project Graph CLI

`scan_project_code_graph.py` имеет exactly-one-mode semantics. Choose один mode per invocation.

| Mode | Purpose | Обязательные входы | Output / boundary |
| --- | --- | --- | --- |
| `--dry-run` | Build graph packet без writing files. | `<workspace>`. | Prints graph JSON; нет write. |
| `--stage <stage-dir>` | Stage graph и cockpit artifacts. | `<workspace>`, explicit stage directory. | Writes generated graph/cockpit files в рамках stage root. |
| `--query <kind>` | Read bounded query packet из existing graph. | `--graph <project-code-graph.json>` plus query args. | Reads existing graph artifact; не rescan source. |
| `--build-index` | Build offline static search index. | `--stage`, `--graph`. | Generated index cache; не является каноническим источником. |
| `--build-backend` | Stage disabled-by-default local query backend store. | `--stage`, `--graph`, `--backend-approval`. | Generated file-store; нет active server через default. |
| `--build-semantic-index` | Stage local deterministic semantic retrieval index. | `--stage`, `--graph`, `--semantic-approval`. | Generated semantic cache; provider calls остаются blocked пока separately approved. |
| `--build-llm-proposals` | Stage local deterministic LLM-style proposal packets. | `--stage`, `--graph`, `--llm-approval`. | Proposals only, never canonical facts. |
| `--verify-extensions` | Stage extension verification и rollback closure. | `--stage`, `--graph`, `--verification-evidence`. | Closure packet и rollback/data deletion proof. |
| `--validate-live-governance` | Stage live governance packet. | `--stage`, `--live-approval`. | Нет live calls; проверяет approval/data/redaction/cache/budget boundary. |
| `--validate-live-runtime` | Stage local read-only runtime contract. | `--stage`, `--live-runtime-approval`, `--live-governance`. | Disabled-by-default local runtime contract; нет launch. |
| `--validate-embedding-provider` | Stage embedding provider gate. | `--stage`, `--embedding-provider-approval`, graph/semantic inputs как required. | Provider gate/eval packet; нет provider call пока approved в later execution. |
| `--validate-reranker-provider` | Stage reranker provider gate. | `--stage`, `--reranker-provider-approval`. | Provider gate packet; нет external call через default. |
| `--build-hybrid-retrieval` | Stage hybrid retrieval pipeline. | `--stage`, graph/index/semantic/reranker inputs. | Generated explainable fusion packet; нет canonical mutation. |
| `--validate-llm-proposal-provider` | Stage LLM proposal provider gate. | `--stage`, `--llm-proposal-provider-approval`, proposal/eval inputs. | Provider gate и safety eval; proposal-only. |
| `--build-review-ledger` | Stage human review ledger и proposal diff. | `--stage`, `--review-ledger-approval`, `--review-decisions`. | Owner decision ledger; still non-mutating. |
| `--build-canonical-mutation` | Stage mutation dry-run, journal и rollback artifacts. | `--stage`, `--canonical-mutation-approval`, review ledger и proposal diff. | Staged mutated graph copy only; canonical source graph является не silently changed. |
| `--build-live-audit` | Stage audit/security/observability/handoff packets. | `--stage`, `--live-audit-approval`, live runtime/actions/security inputs. | Redacted audit и operability evidence. |
| `--build-real-testing-readiness` | Stage readiness, target consent и pilot artifacts. | `--stage`, `--real-testing-approval` и target/gate/pilot inputs. | Dry-run pilot/readiness evidence only. |
| `--build-runtime-qa` | Stage runtime QA, performance и stabilization artifacts. | `--stage`, `--runtime-qa-approval` и QA/performance/stabilization inputs. | Staged QA evidence; нет live browser automation в docs work. |

Disable modes delete generated artifacts в рамках stage root: `--disable-backend`, `--disable-semantic-index`, `--disable-llm-proposals`, `--disable-extensions`, `--disable-live-governance`, `--disable-live-runtime`, `--disable-embedding-provider`, `--disable-reranker-provider`, `--disable-hybrid-retrieval`, `--disable-llm-proposal-provider`, `--disable-review-ledger`, `--disable-canonical-mutation`, `--disable-live-audit`, `--disable-real-testing-readiness` и `--disable-runtime-qa`.

## Входы query

Graph query mode accepts:

- `--graph` для `project-code-graph.json` или `project-code-graph.jsonl`;
- optional `--index`, `--backend`, `--semantic-index`, `--hybrid-retrieval` и `--reranker-provider`;
- `--node-id`, `--target-id` и `--text` для query-specific selectors;
- `--max-results`, `--max-depth`, `--max-tokens`, `--hub-threshold`, `--node-type`, `--edge-type`, `--confidence` и `--path-prefix` для bounded output.

Supported query kinds включают `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `changed_since`, `why_changed`, `read_order`, `hotspots`, `node`, `status` и `search`.

## Проверка Commands

Common local verification commands:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
python -m mkdocs build --strict
git diff --check
```

Запустите smallest relevant set для текущий slice. A closure claim требует full source docs -> registry -> docs tests -> `check_docs.py` -> strict MkDocs -> optional full closure order.

## Риски And Failure Modes

- Running stage command inside target workspace может blur generated и source-of-truth boundaries.
- Supplying approval JSON является не enough если owner, allowed surfaces, data policy, rollback и verification evidence являются missing.
- Query packets может быть stale если graph fingerprints нет longer match текущий source.
- Provider gate commands являются не permission к call providers.
- Canonical mutation dry-run является не permission к mutate checked-in source или graph facts.
- Git commands остаются explicit-only и являются outside these CLI reference commands.

## Next Action

Используйте эта page как operator reference для local scripts. Navigation, source registry entries, docs tests и generated `site/` refresh belong к their owning docs-maintainer и tester slices.
