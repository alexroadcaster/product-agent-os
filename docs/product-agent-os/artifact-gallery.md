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

## Как читать результаты

1. Сначала выберите группу результата и проверьте, какой пользовательский вопрос она закрывает.
2. Затем откройте owning source: исходный файл, control-plane artifact, command evidence, eval report или решение владельца.
3. После этого проверьте boundary: что этот результат доказывает, а что только помогает увидеть.
4. В конце берите ближайшее безопасное действие, а не всю карту проекта сразу.

## Связанные страницы

- [Artifact Contracts](artifact-contracts.md) описывает форматы JSON, HTML и ledger-пакетов.
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
