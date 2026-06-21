# Витрина результатов Product-Agent OS

Source status: `official + experiment`

Эта страница показывает, какие проверяемые материалы пользователь обычно получает от Product-Agent OS и зачем они нужны. Она не является журналом исполнения или доказательством готовности. Источником истины остаются исходные файлы проекта, актуальные артефакты управления, реестр источников, свежие результаты команд, `evals`, `runtime`-проверки, решения владельца и явно принятые gaps.

## Быстрый обзор

| Группа | Примеры | Польза для пользователя | Граница доверия |
| --- | --- | --- | --- |
| Контур управления | `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` | Проект получает устойчивые правила, scope, план, проверки, quality gates и текущий handoff. | Авторитетны только когда актуальны, проверены владельцем и не противоречат исходному коду. |
| Первый запуск | состояние lifecycle, карта рисков, `usage_mode`, gaps, `safe_next_action` | Понятно, с чего начать без широкого переписывания проекта. | Диагностика не равна проверке; следующий шаг должен быть подтвержден evidence. |
| Методологический пакет | рекомендации, вопросы владельцу, связь методологий с файлами проекта | Включаются только нужные gates: DDD, TDD, ADD, FSD, eval-driven и другие практики. | `present_unverified` не становится `present_verified` без артефакта или решения владельца. |
| Статусная панель | `status.html`, `status.json`, route snapshot | Быстро видно состояние маршрута, gaps и ближайшее действие. | Это обзорная поверхность; она не доказывает completion или readiness. |
| Граф и cockpit | `project-code-graph.json`, `project-cockpit.html`, query packets | Упрощают чтение большого проекта, поиск hotspots и выбор affected tests. | Сгенерированные виды помогают навигации, но canonical files остаются главными. |
| Реальные проверки | runtime, browser, provider, mutation и git evidence packets | Каждое действие с внешним или изменяющим эффектом видно отдельно. | Одно approval не разрешает другое действие; каждый запуск имеет свой boundary. |
| Scorecards | metrics report, scorecard ledger, modernization candidate | Agents и skills можно улучшать по фактам, а не по впечатлению. | Candidate-only: предложения не применяются сами. |
| Release и closure | readiness packet, artifact manifest, rollback, handoff | Решение о PR, package или release имеет scope, проверки и остаточные риски. | Нет publish, git stage, commit, push или PR без отдельного explicit approval. |

## First-run Packet And Cockpit

First-run outputs помогают понять проект до изменения файлов. Они не являются source truth и не подтверждают готовность сами по себе.

| Артефакт | Где искать | Что показывает | Producer / consumer | Что доказывает | Что не доказывает |
| --- | --- | --- | --- | --- | --- |
| First-run packet | `.codex/product-agent-os/analysis/first-run-analysis-packet.json` | Inventory, route, source-policy state, gaps, safe next action и unsupported claims. | `run_first_project_analysis.py --write`, `first_run_analysis.py` -> `analysis_artifact_renderer.py`. | Что локальный diagnostic packet был собран для чтения оператором. | Не доказывает source truth, readiness, completion, release, runtime/browser/provider proof или target mutation safety. |
| Render manifest | `.codex/product-agent-os/analysis/analysis-manifest.json` | Список страниц, page/source digests, `manifest_digest`, `redaction_report`, `source_policy_gate`, baseline comparison и cleanup guidance. | `analysis_artifact_renderer.py` -> docs maintainer, reviewer, cleanup handoff. | Что renderer зафиксировал generated files и свои guardrails. | Не доказывает generated-site freshness, semantic review источников или public readiness. |
| Primary HTML cockpit | `.codex/product-agent-os/analysis/index.html` | Self-contained architecture cockpit: overview, project map, code intelligence, contracts, methodology, quality, risk и recommendations. | `analysis_artifact_renderer.py` -> human reader. | Что generated view доступен как orientation surface. | Не доказывает WebGL/Cosmos.gl runtime execution, browser screenshots, WCAG certification или release readiness. |
| Diagnostic HTML pages | `.codex/product-agent-os/analysis/*.html` | Legacy/detail pages: inventory, architecture, methodology, runtime route, control plane, graph, code flow, quality/evals, risks и recommendations. | `analysis_artifact_renderer.py` -> maintainer diagnostics. | Что разделы можно читать отдельно при разборе. | Не заменяет primary cockpit и не является evidence сильнее source files. |
| Answer ledger | `answer-ledger-template.json` рядом со staged first-run outputs | Вопросы владельцу, статус ответа, `target_artifact`, redaction metadata и validation errors. | Guided question protocol -> owner handoff. | Что вопросы подготовлены и private-data boundary размечен. | Не является owner decision, accepted gap или artifact update до фактического ответа и review. |
| Comparison packet | `batch41-s9-m57-neural-flow-comparison.json` или аналогичный target comparison | Digest/key/HTML marker deltas между staged runs, unsupported claims preserved и no-unapproved-actions surface. | Maintainer comparison script/result -> reviewer. | Что конкретный read-only rerun сравнил staged outputs и зафиксировал mutation/runtime/browser/provider/git boundaries. | Не переносится автоматически на другой target и не доказывает freshness после нового rerun. |

## Manifest Fields To Check

При чтении manifest сначала проверьте эти поля:

- `schema_version`: версия generated manifest, а не обещание полной JSON Schema.
- `pages` и `page_digests`: какие HTML outputs были записаны и как они связаны с digest evidence.
- `source_digests`: какие source artifacts попали в digest boundary; это не равно semantic source review.
- `primary_cockpit` и `cockpit_contract`: primary view model и contract map для `index.html`.
- `redaction_report`: `passed_redacted` должен быть текущим для generated payload; это не DLP или security certification.
- `source_policy_gate`: `diagnostic_artifact_allowed` может быть true, пока `apply_allowed` и `promotion_allowed` остаются false.
- `baseline_comparison`: показывает добавленные/измененные pages/sources при наличии baseline.
- `cleanup_guidance`: preview-only список generated files; удаление требует explicit approval.

## Generated-view Policy

Generated dashboard, graph, cockpit, scorecard, report или comparison packet имеют статус orientation evidence. Они помогают выбрать следующий шаг, но не заменяют:

- source files и checked-in contracts;
- `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- source registry entries с актуальным verification status;
- current command/eval/runtime evidence;
- owner decisions и accepted gaps с residual risk.

Если first-run artifact выглядит убедительно, следующий шаг все равно должен быть source-backed: прочитать owning source, проверить текущую команду или записать явный accepted gap. Generated `site/` freshness остается финальным `DOC-M25` gate после G2-G5 и не следует из этой галереи.

## Cleanup Guidance

`first_run_artifact_cleanup_guidance_v1` в manifest является подсказкой, а не разрешением удалить файлы. Без отдельного approval запрещено:

- удалять user-authored files, source docs, project config или `.git`;
- чистить target workspace шире generated analysis directory;
- считать cleanup выполненным, если `deletion_performed` остается `false`;
- использовать cleanup как rollback proof для release, mutation или external-write действий.

Безопасная трактовка: список `generated_files` помогает reviewer понять, что было создано renderer, а `rollback_policy` обычно означает повторный first-run analysis для восстановления generated orientation artifacts.

## Как читать результаты

1. Сначала выберите группу результата и проверьте, какой пользовательский вопрос она закрывает.
2. Затем откройте owning source: исходный файл, control-plane artifact, command evidence, eval report или решение владельца.
3. После этого проверьте boundary: что этот результат доказывает, а что только помогает увидеть.
4. В конце берите ближайшее безопасное действие, а не всю карту проекта сразу.

## Completion-skeptic examples

Эти completion-skeptic examples синтетические и source-safe. Они показывают, как `doubt_verification_packet` меняет final answer style без заявления, что pilot value уже доказан.

| Example id | Artifact type | Trigger | Packet excerpt | Verdict |
| --- | --- | --- | --- | --- |
| `docs_research_example` | Ответ docs/research | "Check sources" | evidence из source registry, community `intake_only`, `needs_fresh_check` для текущих фактов | `revise`, если есть unsupported claims |
| `code_check_example` | Claim по code/change | "Done?" | command evidence, missing lint/test checks, approval boundary | `blocked_by_approval` или `accepted_risk`, если checks нельзя запустить |
| `architecture_review_example` | Architecture/spec | "Did we miss anything?" | requirement ledger, non-goals, dependencies, rollback gaps | `revise` only confirmed architecture gaps |
| `product_planning_example` | Product plan | "Check the matrix" | acceptance criteria, user value, stop conditions и dependencies | `revise` для missing tasks или `accepted_risk` для scoped cuts |
| `security_release_example` | Security/release | "Can we ship?" | source status, rollback, no-unapproved-actions proof, owner approval | `blocked_by_approval` until release evidence exists |
| `ai_eval_example` | AI/eval work | "Check quality" | baseline/current eval, scorecard thresholds, false pass/rewrite signals | manual-only until scorecard and owner review |

## Связанные страницы

- [Artifact Contracts](artifact-contracts.md) описывает форматы JSON, HTML и ledger-пакетов.
- [Doubt verification loop](../playbooks/doubt-verification-loop.md) показывает manual workflow behind these examples.
- [Project Code Graph](project-code-graph.md) объясняет generated graph, cockpit и query packets.
- [Methodology Intelligence](methodology-intelligence.md) показывает, как подбираются DDD, TDD, ADD, FSD и другие методологии.
- [Approval-Bound Real Testing](approval-bound-real-testing.md) фиксирует границы runtime, browser, provider, mutation и git actions.
- [Packaging And Closure](packaging-and-closure.md) связывает финальные проверки, release packet, rollback и handoff.

## Проверка

Для документационного изменения эта страница должна оставаться в `mkdocs.yml`, `tools/check_docs.py`, парной `.en.md` странице и focused docs contract. Если nav или rendered `site/` меняется, нужен strict MkDocs build.

## Риски

- Витрина может быть ошибочно прочитана как доказательство готовности.
- Generated dashboard, graph, cockpit, scorecard или report могут устареть быстрее, чем source files.
- Исторический evidence и public product copy нельзя смешивать: история объясняет происхождение, а public docs должны вести пользователя к следующему действию.
