# PAOS-AUD-G9 — реализация и сравнение

Source status: project-local execution evidence; implemented locally; owner acceptance pending. G8-T14 и закрытие G8 явно приняты владельцем; приёмка G9 и fresh-session activation отдельны.

## Scope и решение

Владелец разрешил полную локальную реализацию G9-T01–T10. Формирование выбирает документы и управляющие предложения; это не генерация приложения и не host activation. Код/тесты plugin, CLI, workflows и owning docs входят в scope; real targets/providers/Git/publication исключены.

Существующие возможности: discovery, scoped selection, document readiness, stage manifest, approval-bound merge/rollback, navigation, compaction/authority. Выбран небольшой orchestration module `project_formation.py` поверх renderer и merge; второй writer/реестр не создаётся. Legacy full catalog требует явного opt-in. Scoped G8 APIs сохраняются как совместимый режим, новый formation CLI использует один planner.

Owned runtime files: `plugins/product-agent-os/scripts/product_agent_os/project_formation.py`, `infrastructure.py`, `merge_infrastructure.py`, `stage_manifest.py` по доказанной необходимости; `scripts/render_infrastructure.py`; focused `tests/product_agent_os/test_project_formation.py` и затронутые compatibility tests/callers. Workflow owner: packaged project-formation и canonical implementation-planner; отдельного active project-formation workflow нет, действующий control-plane-sync переиспользован; public technical RU/EN и registry RU/EN. Root control-plane — краткие pointers, матрица — статусы.

Code-change contract: no_new_dependency; stdlib и existing renderer/merge вместо нового writer. Инварианты: нет неявного full catalog/activation; неизвестное не выдумывается; пользовательские bytes сохраняются; digest связывает preview/stage/current facts; freeze/SQL authority запрещает конфликтующую запись. Комментарии нужны для trust/path/receipt границ. Performance: bounded discovery/read budget; без quota на LOC/tests. Baseline сохранён до edits в ignored `.codex-tmp/g9-tests/baseline`, revision рядом; comparison одинаковых входов не доказывает model/cost superiority.

## Acceptance и сценарии

Требования и критерии — G9 в audit matrix. Primary владеет evidence. Given пустой/существующий/monorepo проект, when единый formation route получает одинаковый task packet, then объяснимый состав, существующие owners, ссылки и проверяемый stage. Given missing/ambiguous facts, then gaps без полного каталога. Given изменённый источник, freeze или conflict, then apply запрещён до записи. Given повторное применение/пользовательские данные, then без дубликатов и потери bytes. Given interrupted merge, then journal/rollback проверены существующим контрактом. Business rule — сохранить пользовательские решения и authority; non-goal — provider/host activation. Дополнительные DDD/frontend/CI/cloud документы not_applicable: локальный tooling slice, без app/UI/CI rollout. ADR/границы решения записаны здесь, отдельные дублирующие artifacts не нужны.

## Проверки

Локальные runtime gates и финальная docs/matrix/link сверка завершены; current receipts ниже. G8 evidence историческое и не является результатом G9.


## Итог реализации и traceability — 10-11-2026 20:11 Europe/Moscow

G8-T14/G8 owner accepted. G9 T01–T09 implemented_locally_verified; T10 technical work complete, needs_user_acceptance. Карточки и критерии сохранены в owning matrix; ниже evidence mapping. Свободные роли в карточках не означают dispatch: primary выполнил работу и self-review, независимых агентов в этом slice не запускал.

| Task | Результат / acceptance coverage | Owning implementation / evidence |
| --- | --- | --- |
| T01 | Контракт project_formation_v1: task, domains, canonical paths, facts, control proposals; единый результат с provenance, gaps и границами. | `project_formation.py; assets/templates/workflows/project-formation.md` |
| T02 | Bounded read-only inventory и existing discovery/routing: digest, состояния документов, detected stack, вопросы и неоднозначные owners. | `project_formation.py: source_inventory, formation_plan` |
| T03 | Переиспользованы selected_templates; явные control surfaces, условный EVALS, dependency closure и explicit legacy catalog. | `project_formation.py; infrastructure.py; compatibility callers/tests` |
| T04 | Канонические aliases, выбранные docs domains, navigation index, URL-encoded ссылки, case/path collision checks. | `project_formation.py: _owner_path, _document, formation_plan` |
| T05 | Переиспользованы G8 scoped_document/readiness; supplied facts остаются данными с source; новые proposals не получают acceptance. | `infrastructure.py; project_formation.py; existing control_plane_documents.py reused` |
| T06 | Единый CLI analyze/preview/stage/merge/rollback; formation и legacy/scoped режимы явно разделены; workflow указывает общий planner. | `scripts/render_infrastructure.py; assets/templates/workflows/project-formation.md; skills/implementation-planner/SKILL.md` |
| T07 | Source/stack/target binding, preview digest, preserve-existing merge; write-ahead journal, atomic create, bounded journal retry и crash recovery. | `project_formation.py; infrastructure.py; merge_infrastructure.py` |
| T08 | Previous-plan change impact, review-only removal и manual updates; G8 budgets/compaction/authority переиспользованы; freeze/SQL conflicts блокируют writer. | `project_formation.py; existing control_plane_compaction.py reused; public workflow/docs` |
| T09 | Три сквозных synthetic-пилота с frozen baseline; preview/stage/apply/repeat/next change/rollback, исходная и предложенная navigation. | `tests/product_agent_os/test_project_formation.py; tests/fixtures/product_agent_os/g9-project-formation/cases.json; docs/superpowers/specs/paos-aud-g9-project-formation-results.json` |
| T10 | RU/EN docs, registry, packaged workflow, canonical skill и control-plane синхронизированы; итоговый пакет передаётся владельцу. | `docs/product-agent-os/project-formation.md/.en.md; technical.md/.en.md; architecture.md/.en.md; cli-reference.md/.en.md; docs/runtime/worktrees-hooks-rules.md/.en.md; docs/sources/registry.md/.en.md; root control-plane; G9 report` |

Точные runtime пути начинаются с `plugins/product-agent-os/scripts/product_agent_os/`; CLI — `plugins/product-agent-os/scripts/render_infrastructure.py`. `control_plane_documents.py`, `control_plane_compaction.py`, `templates.py`, `stage_manifest.py` переиспользованы без новой реализации/нового state registry. Compatibility tests переведены на explicit `legacy_catalog=True`; runtime runner legacy fallback остаётся отдельным контрактом. В публичных docs есть компактный режим, расширенное дерево и условия выбора.

## Сравнение baseline / G9

Baseline revision: `6548ee12933091864b3876e8544985deaf376f4f`; копия plugin заморожена до runtime edits. В обоих маршрутах одинаковые workspace/task facts; `domains` — новая возможность, baseline её не поддерживает и не получает фиктивную реализацию. Среда: Windows, Python 3.13.5, без providers. Source/template/test/fixture hashes зафиксированы в [JSON результатов](../docs/superpowers/specs/paos-aud-g9-project-formation-results.json). Размеры — bytes предложенных текстов, не размер принятого проекта и не стоимость модели.

| Профиль | Baseline scoped: файлов / bytes | G9: файлов / bytes | Файлов docs/ | Существующих файлов для manual review | Результат |
| --- | --- | --- | --- | --- | --- |
| empty-project | 7 / 7964 | 14 / 28257 | 4 | 0 | passed |
| existing-project | 7 / 7964 | 14 / 28208 | 4 | 4 | passed |
| monorepo-ai | 8 / 8404 | 16 / 29045 | 5 | 0 | passed |

Старый no-context каталог предлагал 210 файлов во всех трёх профилях; новый default без input явно блокируется. Scoped baseline давал 0 project docs; G9 добавляет выбранные разделы, оглавление и требуемые dependencies. Увеличение 7 → 14 / 8 → 16 объясняется новым результатом и dependency closure, а не ухудшением или экономией по счётчику файлов.

Во всех трёх случаях: preview/stage не меняют target; merge выполняется только с synthetic approval в временном synthetic workspace; исходные bytes сохранены; текущая и предложенная navigation разрешимы; повторный stage не требует новых target writes; следующее изменение обнаруживается; rollback возвращает исходные bytes. Existing profile сохраняет AGENTS.md, TEST.md, docs/architecture.md и docs/index.md; их обновления требуют manual companion adoption. Проверка предложенного оглавления не означает его автоматическое применение.

Empty/monorepo profiles сохраняют implementation gaps: отсутствуют подтверждённые проектные команды проверки/инструкции. Formation scaffolds не объявляются готовыми к реализации. Missing input, ambiguity, traversal, case/owner collisions, secret-like data, stale/new sources, malformed markers, profile removal и freeze/SQL conflicts проверены отдельно; общий successful pilot score их не подменяет.

## Выполненные проверки и provenance

Все команды запускались из repo root; TEMP/TMP = `.codex-tmp/g9-tests`; `python -B`, Python 3.13.5. Ниже current-run receipts, не заимствование из G8:

- `python -B -m unittest discover -s tests -p 'test_*.py' -q` — Ran 1435 tests in 803.716s, OK (skipped=1), exit 0; `.codex-tmp/g9-tests/all-gates-full.log`. Skip: existing non-Windows guard on Windows; no G9 scenario skipped.
- `python -B -m unittest tests.product_agent_os.test_project_formation tests.product_agent_os.test_merge_infrastructure -q` — 57 tests / 32.824s, OK, exit 0; после исправления transient journal lock, `.codex-tmp/g9-tests/receipt-lock-green.log`.
- Earlier affected suite: formation, renderer, CLI, merge, stage manifest, runtime CLI и docs — 254 tests / 108.119s, OK; до последнего bounded-retry изменения, не финальное доказательство этой правки.
- `python -B tests/product_agent_os/test_project_formation.py --report docs/superpowers/specs/paos-aud-g9-project-formation-results.json --baseline .codex-tmp/g9-tests/baseline` — 3/3 profiles, exit 0, hashes match final implementation/test/workflow sources.
- `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` — 91/91, exit 0; `.codex-tmp/g9-tests/fixtures-final.json`.
- `python -B plugins/product-agent-os/scripts/run_transcript_eval.py` — 26/26, ok=true, errors=[], exit 0; `.codex-tmp/g9-tests/transcripts.json`. Transcript assertions не являются новым live-model evaluation.
- `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py` — compatible, exit 0; `.codex-tmp/g9-tests/compatibility.json`; host statuses not_verified.
- `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .codex-tmp/g9-tests/site` — success, 24.06s, exit 0; `.codex-tmp/g9-tests/mkdocs-final.log`. Только isolated preview, исторический root `site/` не promoted. Новая RU/EN страница учтена в source page counts и pending-site list, существующие published-page assertions сохранены.

## Сбои, RED/GREEN и исправления

1. RED no-context generation: прежний default выбирал каталог. GREEN: явный blocked результат и explicit legacy mode; compatibility callers обновлены без ослабления assertions.
2. RED interruption after write/before receipt: отсутствовал восстанавливаемый факт записи. GREEN: write-ahead journal, атомарная запись, проверены исключение и реальное `os._exit(17)` в отдельном процессе; rollback сохраняет post-apply user edits через digest refusal.
3. RED conditional EVALS: generic reference втягивал EVALS в ordinary profile. GREEN: условный selection и адаптация необязательных references; AI scope сохраняет EVALS.
4. Initial integration выявлял CLI mock signature, incomplete dependency handling и preservation differences; исправлены, повторные focused/integration runs passed. Один диагностический запуск без workspace TEMP завершился sandbox setup error; он не использован как продуктовый результат.
5. Первый broad run: 1432 tests / 824.981s, failures=15, skipped=1. Причины: устаревшее legacy mode expectation; 13 docs source-count ожиданий; CLI digest comparison во время изменения исходников. Последующие source/site-count ожидания разделены: 161 source pages, 151 localized, 143 historical promoted; новая страница preview-only. Один affected запуск имел SyntaxError в test evidence source path; опечатка исправлена. Это не passed evidence.
6. Два Windows `WinError 5` наблюдались при atomic rollback-journal replacement (ранний recovery run и поздний formation run). Добавлен максимум 3 попытки той же atomic journal write с ожиданием 50/100ms; постоянный отказ останавливает операцию, предыдущий journal сохраняется, pending file другого writer не удаляется. RED targeted 1 error; GREEN 57 tests. Причина внешнего file lock не установлена; отсутствие будущих OS-level ошибок не заявляется.
7. Промежуточные full runs остановлены при уточнении docs expectations и после воспроизведённого journal failure; они не являются full pass. Финальный stable run выше относится к исправленному runtime. Неполные/ошибочные логи остаются под `.codex-tmp/g9-tests/`.

## Self-review, ограничения и решение для владельца

context_mode=self_review; tester_verdict=partial_only для закрытия группы до owner decision. Review: single planner/reused writer; source and manifest target binding; no implicit catalog; non-AI EVALS conditional; existing canonical paths preserved; stage validation before writes; current/companion navigation checked; freeze and rollback authority; actual crash recovery; no dependencies/install/provider/cache/Git changes. Comment advisory рассмотрен по затронутым trust/recovery границам; unmodified helpers не переписаны ради quota.

Ограничения: bounded file/manifest analysis, не полное понимание бизнес-логики; existing content и структура требуют semantic owner review; supplied facts остаются untrusted data; типовые secret-like patterns не гарантируют обнаружение всех секретов. Нет cross-file ACID или concurrent-writer guarantee; writers должны быть изолированы. При постоянном I/O отказе выполнение останавливается с recovery evidence. M1 authority проверена synthetic-контрактом, SQL adapter и cutover принадлежат M1. Не проводились host/fresh-session activation, real-project adoption, live model A/B, production или cost/token measurement. Broad release readiness и превосходство модели не заявляются.

40 000 UTF-8 bytes / warning 32 000 сохраняются для применимых документов; G8 lossless compaction и recovery переиспользованы, history не сокращается этим planner. Подробные матрицы docs/planning/ исключены из default size trigger; research matrix остаётся одним файлом по решению владельца. Перенос/сокращение не выполнялись.

Предлагаемая приёмка: принять локальную реализацию T01–T09 и технический результат T10 с описанными границами; существующие target документы обновлять только после review конкретных companion proposals. До явного решения владельца G9 не закрыта. Fresh-session activation остаётся отдельной открытой задачей, T34 no-go и G6 acceptance не изменены.

Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG update_required и обновлены; AGENTS/prod_test not_applicable (durable rules/Batch39 evidence не менялись); handoff_required — owner decision G9 и отдельная activation. Новая страница описывает существующую staging/merge boundary, отдельная диаграмма не нужна. Подробные receipts находятся здесь, root files содержат краткие pointers.

## Финальная сверка после control-plane sync

- `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_status_snapshot -q` — 130 tests / 12.727s, OK, exit 0; `.codex-tmp/g9-tests/closure-docs.log`.
- `python -B tools/check_docs.py` — documentation structure checks passed.
- `python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-audit-remediation-task-plan-2026-11-09.md` — ok=true, errors=[], exit 0. T10 uses schema status `in_progress`; semantic gate `needs_user_acceptance` recorded in its report. Initial status mismatch corrected without changing validator.
- `python -B .codex-tmp/g9-tests/check_final.py` — 58 cards, all acceptance criteria preserved against HEAD; G9 nine implemented + T10 in_progress/needs_user_acceptance; 75 projection rows, issues=[]; root files below 40 000 bytes; local links errors=[]; current comparison hashes match; docs/planning matrices unchanged. REQUIREMENTS remains in the 32 000-byte warning band (35 089 bytes), below hard limit; no automatic compaction.
- `git diff --check` — exit 0, final whitespace check; an extra blank line at matrix EOF was removed, PLAN revision repinned.
- Final strict MkDocs: `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .codex-tmp/g9-tests/site` — successful, 24.39s, exit 0; `.codex-tmp/g9-tests/mkdocs-closure.log`. No publication or root site promotion.
- Supplementary CLI/runtime links: plain-GFM navigation checker reports two existing MkDocs `{#ordinary-route-contract}` attribute-list anchors as unresolved; both IDs are confirmed in RU/EN rendered HTML. This is a checker syntax limitation, not a missing rendered anchor; no link or validator weakened.

Дополнительный final docs gate после записи текущего handoff: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` — 105 tests / 13.062s, OK, exit 0; `.codex-tmp/g9-tests/docs-terminal.log`. Последующие изменения — только фиксация этого receipt; финальный docs checker, links/projection и diff hygiene повторены.

Review disposition: local implementation and required gates passed; owner decision remains pending. Historical planning and failed attempts are retained. Full run time measured at 803.716s; total interactive execution duration/tool/token counters unavailable as a single complete trace after context compaction. No subagent dispatch or provider calls.

## Исторический handoff планирования до авторизации реализации

Сохранён текст прежнего planning handoff; относительные ссылки rebased для расположения отчёта в research/.

### REQUIREMENTS.md

## PAOS-AUD-G9 — планирование, без реализации

Разрешено только планирование: [группа G9](product-agent-os-audit-remediation-task-plan-2026-11-09.md#paos-aud-g9), T01–T10 planned. Цель будущей реализации — анализ → выбор файлов → согласованная структура docs/ и .codex/ → preview/staging → разрешённое применение и сопровождение. Переиспользовать G8, сохранить пользовательские данные и source ownership M1. G8-T14, fresh-session activation и внешние действия не закрываются этой правкой.

### PLAN.md

## PAOS-AUD-G9 — планирование, без реализации

[группа G9](product-agent-os-audit-remediation-task-plan-2026-11-09.md#paos-aud-g9) содержит десять planned-карточек; реализация не начата. Порядок T01 → T02 → T03 → T04 → T05 → T06 → T07 → T08 → T09 → T10; точные dependencies и owners — в матрице. Приёмка G8-T14 отдельна; завершение M1 целиком и HOST activation не являются prerequisite локальной реализации G9. Shared writers подчиняются M1 freeze/authority. Следующий шаг — отдельный запрос владельца на реализацию.

### TEST.md

## PAOS-AUD-G9 — планирование, без реализации

Для текущего authoring [группа G9](product-agent-os-audit-remediation-task-plan-2026-11-09.md#paos-aud-g9): docs unittest, tools/check_docs.py, validate_task_matrix.py, current-state revision/projection и git diff --check. Новые G9 runtime tests и пилоты не выполняются: реализация отсутствует. Будущие focused/integration/fixture/compatibility gates задаются карточками и общим TEST.md; strict MkDocs — при изменении навигации/config/site evidence.

### EVALS.md

## PAOS-AUD-G9 — планирование, без реализации

Будущий comparison contract [группа G9](product-agent-os-audit-remediation-task-plan-2026-11-09.md#paos-aud-g9), T09: одинаковые входы и зафиксированный baseline; пустой/существующий/сложный проект, ordinary/AI, missing context, conflict и повторное формирование. Метрики: достаточность, лишние файлы, зависимости/ссылки, сохранность и следующее изменение. Отдельный mandatory failure не скрывать score; уменьшение файлов не доказывает качество или экономию. Сейчас eval results отсутствуют.

### RUNLOG.md

## PAOS-AUD-G9 — планирование, без реализации

Добавлены десять planned-карточек [группа G9](product-agent-os-audit-remediation-task-plan-2026-11-09.md#paos-aud-g9) со всеми полями, dependencies и acceptance. Обновлены summary группы и revision-pinned PLAN selector; исторические карточки G1–G8 сохранены. Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG updated; AGENTS и prod_test not_applicable — durable rules и Batch39 не менялись. Public implementation docs/source registries не менялись: новых реализованных возможностей и внешних source claims нет. G9 implementation_not_started; G8-T14 needs_user_acceptance; fresh-session activation отдельно. Текущие проверки: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_status_snapshot -q` — 130 tests / 12.689s, OK, exit 0; `python -B tools/check_docs.py` — OK; `python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-audit-remediation-task-plan-2026-11-09.md` — ok=true, errors=[]; `git diff --check` — exit 0. Прямые read-only assertions: 48 прежних карточек сохранены текстуально; всего 58 карточек, G9 10/10 planned; dependency refs ведут к предыдущим задачам; revision-pinned projection 75 rows, issues=[]; local links errors=[]; все root control-plane files менее 40 000 bytes. Начальные замечания валидатора (обязательные Completion Report placeholders и HTML anchor, распознанный как placeholder) исправлены без изменения validator. Первый link probe отклонён из-за Windows separators; POSIX-relative retest passed. Strict MkDocs not_applicable: nav/config/public site docs не менялись. Финальный повтор `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q` после записи handoff: 105 tests / 11.313s, OK, exit 0. Полный runtime suite и G9 pilots не запускались — planning-only; их прежние результаты не выданы за evidence G9.

