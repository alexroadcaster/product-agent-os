# Product-Agent OS — архитектура документации и backlog

Source status: repository_source / current_source_inspection / owner_requested_planning; subsystem documentation implementation planned; DG01 repair docs_static_verified.
Дата: 15.11.2026. Schema version: task_matrix_plan_v1. Timezone: Europe/Moscow.

## Результат анализа

В baseline `docs` 316 Markdown файлов (включая RU/EN и архив): структура преимущественно описывает Codex, методологии и Python plugin. Это полезная база знаний, но не полная документация текущего Web/desktop приложения. `docs/planning` был пуст. Найдены 42 самостоятельных plans/backlogs/task-state файлов вне него; они перенесены с обновлением ссылок. Полная [карта переноса](relocation-2026-11-15.json) сохраняет from/to и before/after hashes.

Проверены 57 верхнеуровневых research MD/JSON, legacy plans и task-state/specs, design implementation plans; source references искались в 2297 текстовых файлах. `research` с fixtures и reports не считается очередью только из-за упоминания task ID. Корневые AGENTS/PLAN/TEST/EVALS/RUNLOG остаются control-plane owners; packaged templates и synthetic target fixtures не являются планом этого проекта. Чужие session markers и private historical reviews не изменяются: их старые ссылки разрешаются по migration map, исторические receipts не выданы за заново выполненные.

### Подтверждённые наблюдения

| Область | Что найдено в реализации/документации | Пробел |
| --- | --- | --- |
| Backend | [apps/local-service/src/http/application.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/application.mts) связывает task manager, artifacts, team, code index, scheduler, recipes и decisions; отдельные storage/runtime modules | Нет единого module/lifecycle/API guide для PAOS Web; methodologies/backend — метод, а не фактическая архитектура |
| Frontend | [apps/web/src/ui/App.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/ui/App.tsx), features, API client, V3 design и [apps/web/README.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/README.md) | Нет связной карты screens/state/dataflow/design-to-code; README смешивает текущие инструкции и историю |
| DB | [apps/local-service/src/storage/migrations/schema.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/migrations/schema.mts) задаёт 16 CREATE TABLE/VIRTUAL TABLE statements, включая entities/events/outbox/FTS; SQLite worker/restore/search | Нужны ERD, таблицы/инварианты/authority и migration/backup contract; schema target-проекта F33 не равна SQLite PAOS |
| AI/LLM Web | [apps/local-service/src/runtime/route-selector.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/route-selector.ts) содержит codex_app_agent/local_api_byok и запрещает implicit fallback | Runtime маршруты/подключение/credentials/limits разбросаны по research и receipts |
| Retrieval/RAG | Web [apps/local-service/src/storage/search-queries.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/search-queries.mts) использует SQLite FTS5; [plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py) — отдельный deterministic semantic cache | Нельзя называть Web search полноценным production RAG; явная интеграция этих двух путей не установлена этим аудитом |
| Providers/proposals | [plugins/product-agent-os/scripts/product_agent_os/project_graph_embedding_provider.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_embedding_provider.py) и [plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py) определяют gates; default не вызывает live providers | Нужна capability matrix deterministic/staged/live-approved; наличие модуля не доказывает активацию |
| Guides | docs/product-agent-os уже содержит graph/governance/formation/CLI/privacy/evals; docs/agent-systems и methodologies — общие знания | Переиспользовать и связать владельцев; не копировать все страницы в новые пустые каталоги |

Это статический source/docs аудит, не runtime acceptance; provider/network calls не выполнялись. Наличие названий RAG/LLM среди task components не доказывает наличие RAG runtime.

## Предлагаемая структура docs

Имена каталогов — lowercase, как в существующем репозитории. AI объединяет вложенные agents/llm/rag, а не четыре независимых корневых раздела. Папки создаются вместе с содержательными страницами в задачах ниже; первоначальный аудит выполнил перенос planning и запись backlog, последующий DG01 завершил repair.

```text
docs/
  planning/                 # реальные планы, backlogs, task-state и migration map
  product/                  # актуальный продукт, домены, capabilities, user journeys
  architecture/decisions/   # структура системы и ADR
  backend/                  # local service и server modules
  api/                      # HTTP/events/shared contracts
  frontend/                 # UI/UX, navigation, state и design-to-code
  db/                       # SQLite PAOS, schema/ERD, migration, backup
  ai/
    agents/                 # orchestration, tools, sessions, approvals
    llm/                    # routes, prompts, models/providers, budgets
    rag/                    # lexical/semantic retrieval и реальные ограничения
  code-intelligence/        # discovery, inventory, graph, impact, adapters
  security/                 # product trust boundaries и data protection
  testing/                  # tests/evals и evidence map
  operations/               # запуск, profiles, update/rollback, troubleshooting
  product-agent-os/          # существующие plugin/operator guides
  diagrams/                 # единый существующий atlas
  codex/ methodologies/     # общая база знаний, отдельно от реализации
  agent-systems/ prompting/ # общие подходы, не evidence реализации PAOS
  sources/ insights/        # источники и research notes
  web/                      # existing user-facing guides, ссылки из frontend/operations
  superpowers/specs/        # исторические design/evidence, не live task backlog
```

## Что уже перенесено и что остаётся

| Класс | Действие |
| --- | --- |
| 6 файлов research: FUNC MD/JSON, Web MD/JSON, audit remediation и ordinary-route plan | Перенесены в docs/planning, статусы/карточки сохраняются |
| 20 legacy Markdown plans, включая EN | Перенесены из docs/superpowers/plans в docs/planning |
| 6 Track 8/9/10 backlog RU/EN | Перенесены из docs/sources в docs/planning; архивные пометки сохранены |
| 5 task-group/next-task JSON и 2 task-plan TXT | Перенесены из docs/superpowers/specs в docs/planning; evidence packets остаются в specs |
| 3 design implementation-plan | Перенесены в docs/planning с датой/версией в имени; изображения, design и receipts остаются рядом с design |
| PRD, architecture, auth/storage research | Пока остаются в research; DOCS-02/03/07/09/12 выделяют актуальные главы, переносят их в соответствующие канонические разделы и сохраняют исторические основания |
| Methodologies/backend/frontend/database/LLM-AI-RAG | Остаются методологиями; новые implementation guides ссылаются на них, но описывают реальный код |
| Plugin guides, diagram atlas, security/evals pages | Переиспользуются с явным ownership; DOCS-03/08/10/11/12/13/15 добавляют недостающие implementation-specific сведения |
| Execution reports/results, audit findings, requirement history | Остаются research/evidence, связаны с актуальными guides; отчёт со списком выполненных задач не переименовывается в новый план |

## Последовательность и связь с FUNC

Актуальный порядок исполнения задан семью группами ниже: сначала DG01, затем зависимости конкретных задач. Связь с функциональным планом сохранена: G01→backend/frontend/API; G02→code-intelligence/AI; G03→backend/API/frontend; G04→DB/code-intelligence/retrieval; G05→AI/security; G06→operations/testing; G07→product/testing/navigation. Функциональные группы и статусы не меняются.

## Группы реализации документации — 15.11.2026

Текущий статус: DG01 — **completed / docs_static_verified**; DOCS-13 и DOCS-16 — **in_progress**; остальные группы и 14 задач — **planned**. Группировка определила последовательность без реализации. Последующий запрос DG01 разрешает исправления ссылок, локализации и проверок; написание документации остальных подсистем не начато. IDs, исходные Depends on / Blocks, scope и AC карточек сохраняются.

### Правила этапов и зависимостей

DOCS-13 и DOCS-16 имеют по два этапа внутри существующей карточки: **13/A, 16/A** — устранение текущих проблем после переноса; **13/B, 16/B** — основная работа и полное закрытие. Обозначения этапов не создают новых task IDs или второй источник статуса. Всего 16 задач, 18 исполняемых этапов: 14 обычных задач и четыре этапа двух задач. Владелец полного закрытия DOCS-13 — DG06, DOCS-16 — DG07.

Для обычных задач Depends on остаётся условием входа. Для DOCS-13/16 это условие этапа B и полного закрытия; этап A проверяет существующую документацию и не ждёт будущих разделов. Это явное уточнение прежнего неоднозначного разрешения раннего repair, а не удаление зависимостей. Завершение A фиксируется evidence внутри родительской карточки; родитель остаётся in_progress до B и выполнения всех исходных AC. Этапы A завершены; этапы B остаются planned.

**DG01 — обязательный первый этап:** DG02–DG07 не начинают исполнение до его acceptance. Внутри последующих групп старт определяется зависимостями конкретной задачи: номер группы не создаёт лишнего ожидания полного завершения предыдущего номера.

| Группа | Задачи / этапы | Вход и внутренний порядок | Результат и выходной gate |
| --- | --- | --- | --- |
| **DG01 — исправления после переноса** | **DOCS-16/A**, **DOCS-13/A** | Первая группа, без ожидания новых domain docs. Два независимых потока с согласованным владельцем проверок | Восстановлены repository/site links и anchors, обработаны ссылки за пределами docs, исправлены language links; 8 EN gaps закрыты содержательными переводами. Исторические assertions согласованы с текущим контрактом без включения hooks или ослабления guards ради зелёных тестов. Изолированный strict build, source checks, site/archive checks проходят; оставшийся blocking failure не позволяет закрыть DG01 |
| **DG02 — структура, продукт и архитектура** | **DOCS-01**, **DOCS-02**, **DOCS-03** | После DG01: 01 → 02 → 03 | Назначены владельцы разделов, актуальная продуктовая/доменная модель, архитектурные границы и ADR; Web/desktop, Python plugin и planned возможности разделены. Все три карточки удовлетворяют исходным AC |
| **DG03 — backend, API и данные** | **DOCS-04**, **DOCS-05**, **DOCS-07** | После 03: 04 → 05 → 07; результат 05 сразу доступен DG05 | Документация local service, HTTP/events/errors и SQLite/ERD/migrations/backup сверена с кодом и тестами; SQLite PAOS отделена от целевой БД F33 |
| **DG04 — frontend и UI/UX** | **DOCS-06** | После 01/02/03; параллельно DG03 | Карта navigation/screens/state/components/design/a11y; фактические и будущие Files/Map/Database states отмечены раздельно. Общие API сведения имеют одного владельца DOCS-05, без второй конфликтующей спецификации |
| **DG05 — AI, LLM, retrieval и графы** | **DOCS-08**, **DOCS-09**, **DOCS-10**, **DOCS-11** | 08 после 03/05; 08 → 09; 10 после 07/08/09; 11 после 03/05/10 | Согласованы orchestration/routes/providers, поиск/retrieval/RAG и discovery/graph/impact; существующие и PoC/planned пути разделены. DOCS-08 может идти одновременно с DOCS-07, DG04 не prerequisite |
| **DG06 — безопасность и проверяемость** | **DOCS-12**, **DOCS-13/B** | 12 после 03/05/07/08; 13/B после 13/A и 04/05/06/07/08. Эти две задачи допускают независимую работу | Security/privacy/trust-boundary guide и карта тестов/evals/evidence согласованы с владельцами подсистем. DOCS-13 закрывается только после A+B и всех исходных AC; не требуется ждать весь DG05 |
| **DG07 — эксплуатация, plugin и итоговая интеграция** | **DOCS-14**, **DOCS-15**, **DOCS-16/B** | 14 после 04/07/12/13; 15 после 01/03/08/11/13. 14 и 15 независимы при готовых входах; 16/B после 16/A и полного закрытия 01–15 | Operations/rollback/troubleshooting и Python plugin guides связаны с архитектурой. Итоговая owner/update matrix, связи с FUNC G01–G07, RU/EN navigation и strict/site/source checks принимают весь комплект, включая отсутствие повторного появления ошибок DG01 |

### Что относится к первому и финальному этапам

- **DOCS-16/A:** исправление последствий переноса 42 файлов: ссылки внутри репозитория и в публикуемом дереве, anchors/redirect policy, EN sibling links, восемь отсутствующих переводов, search/sitemap parity и воспроизводимая изолированная сборка. Сохранить task-state, migration provenance и исторические receipts. Нельзя скрыть проблему отключением validation или фиктивным переводом.
- **DOCS-13/A:** сверить исторический PostToolUse assertion и остальные обнаруженные после переноса ошибки с действующим контрактом, исправить устаревшие тестовые ожидания только с доказанным основанием, сохранить необходимые проверки. Hooks/trust остаются вне этого repair; он не разрешает их активацию. Если ошибка требует такого изменения, группа остаётся открытой с явным blocker.
- **DOCS-13/B:** основная документация карты тестов/evals, synthetic/runtime/human evidence и verification routes; результаты A включаются как ранее выполненный repair с датой, не повторная выдуманная проверка.
- **DOCS-16/B:** интеграция всех новых разделов, document owners и feature delivery; повторная проверка полного актуального набора. Успех первой группы не доказывает готовность будущего сайта.

Критерии DG01 дополняют раннюю часть DOCS-13/16. Критерии DG02–DG07 не заменяют исходные карточки: закрытие требует всех AC входящих задач. Полное закрытие DG07 требует результатов DG01–DG06; readiness продукта или автоматическая публикация из этого не следуют.

### Параллельность и владение файлами

После DG02 есть две ветки: DG03 и DG04. После DOCS-05 можно начать DOCS-08/09 одновременно с DOCS-07; DOCS-10 ждёт обе ветки. После DOCS-08 и готовности DB/frontend можно начать DG06, пока DG05 заканчивает retrieval/graph docs. DOCS-14 может стартовать до DOCS-11/15, если его собственные prerequisites закрыты.

Владение: DG03 — backend/api/db; DG04 — frontend; DG05 — ai/code-intelligence; DG06 — security/testing; DG07 — operations/product-agent-os и финальная интеграция. Общие mkdocs.yml, indexes, registries, PLAN/RUNLOG, diagram atlas и связанные checks обновляются последовательно через одного интеграционного владельца. Это схема будущей реализации, не запуск команды. Ускорение основано на независимых ветках; числовая экономия времени не оценена.

### Проверка этой группировки

Владелец порядка — этот раздел. Таблица карточек ниже сохраняет исходные зависимости; поэтапные исключения для DOCS-13/16 заданы выше и в самих карточках. Проверить: все 16 IDs покрыты; нет новых/потерянных карточек; каждый этап назначен одной группе; граф 18 этапов без циклов; DG01 блокирует последующий старт; исходные AC/status/dependencies сохранены. Текущая группировка не меняет прежние неуспешные build/archive/site receipts.

Проверки группировки 15.11.2026: validate_task_matrix — passed; source-docs unittest — 3/3 passed (0.669s); check_docs и git diff --check — passed. Сравнение карточек до/после: 16/16 сохранены побайтно после удаления только добавленных Delivery group/Execution stages полей; все planned. Покрытие 7 групп / 18 уникальных этапов и DAG с обязательным DG01 gate — passed. Review: self_review. Control-plane sync: PLAN/RUNLOG updated; REQUIREMENTS/TEST/EVALS/registries no_change_needed — требования, source claims и verification routes не менялись. MkDocs/site/archive не перезапускались: их исправление входит в будущий DG01, результаты прежнего прохода не повышены.

## DG01 — результаты исправления {#dg01-results}

Статус: **completed / docs_static_verified**, 15.11.2026. **DOCS-13/A и DOCS-16/A завершены**; родительские DOCS-13/16 остаются in_progress до B. DG02–DG07 и остальные 14 задач остаются planned.

Выполнены восемь полных EN-переводов: UI V1/V2/V3, документационная архитектура, functional remediation, audit remediation, ordinary route, Web task manager. Сохранены карточки, статусы, зависимости, AC, даты, команды и исторические ограничения. Смысловая проверка и сверка технических литералов дополняют regression полноты карточек и критериев.

Repository-only file/directory links ведут на проверенные blob/tree targets коммита 33ed0350738e549f932a9fffdeeff9d4908ca94c. EN JSON targets используют тот же snapshot, внутренние страницы — относительные ссылки. Targets сверены с Git tree; snapshot доступен через GitHub connector, каждый внешний URL отдельно по сети не проверялся. Исправлены RU/EN project-formation anchors, language links, search/sitemap parity.

Исторический PostToolUse receipt сохраняет пять событий; текущий contract отдельно проверяет SessionStart/PreToolUse/PermissionRequest/Stop. Hooks/trust не изменены. Regression проверяет все карточки, plain/backtick dependency IDs и AC numbering; групповые заголовки отделены от карточек. Литеральные имена полей оформлены в RU тексте без отключения языкового gate.

| Проверка | Команда / результат |
| --- | --- |
| Матрицы | `python -B plugins/product-agent-os/scripts/validate_task_matrix.py <plan>` — 16 RU/EN matrices passed |
| Исходная документация | `python -B tools/check_docs.py`; `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q` — passed, 3/3 |
| Архив и переводы | `python -B -m unittest tests.product_agent_os.docs_archive_checks -q` — 99/99 passed |
| Hook regression | Historical receipt / current hook shape / optional advisory targeted checks — 3/3 passed |
| Strict build | `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/dg01/site` — exit 0 |
| Language links | `tools/fix_site_i18n_links.ps1 -SiteDir .docs-tools/reports/dg01/site` — passed |
| Сайт | `PAOS_DOCS_SITE_DIR=.docs-tools/reports/dg01/site`; `python -B -m unittest tests.product_agent_os.site_checks -q` — 7/7 passed |
| HTML links/anchors | `python -B .docs-tools/reports/dg01/check_links.py` — 30 затронутых RU/EN routes, missing targets/anchors: 0 |
| Diff | `git diff --check` — passed |

Сохранены причины RED: исходный PostToolUse assertion, отсутствующие/частичные переводы, 17 EN JSON warnings, граница group/card, литеральное имя поля, group Status и 7 directory/2 EN anchor targets. Соответствующие GREEN checks выполнены после исправлений; прежние migration receipts ниже остаются историческими.

Review: self_review и независимая проверка переводов/теста агентами с раздельным владением; замечания устранены. Control-plane sync: PLAN/RUNLOG, каталог, registry RU/EN updated; TEST содержит evidence pointer. REQUIREMENTS/EVALS/prod_test no_change_needed: scope, рубрики и production history не менялись. Feature JSON task-state/dependencies сохранены. Корневой site/, публикация, runtime/provider activation и будущие domain docs не входят в результат. Следующий плановый этап — DG02.

## Evidence миграции и проверки

Статус: перенос и backlog записаны; verification частичная, публикация сайта не готова. Продуктовые задачи не реализовывались.

- Preservation: 42/42 исходных файла совпадают с результатом только path/link relocation и добавления Source status там, где он отсутствовал. Literal template examples сохранены; 7 JSON owners сохраняют task IDs/status/dependencies/AC/receipts. Старые файлы отсутствуют; 42 новых владельца существуют.

- Task matrices: новый DOCS и текущие FUNC/Web/audit/ordinary-route проходят validate_task_matrix; DOCS DAG 16/16 без циклов.

- Source/docs и path-dependent tests: 120 tests passed (5.614s); check_docs exit0. Три изменённых fixture helpers: graph/backend gates, hygiene docs loading и doubt artifact path — passed.

- Архив: 98 tests, 6 failures. Пять assertions выявляют 8 отсутствующих EN sibling страниц после включения research/design планов и нового backlog в docs. Ещё один требует PostToolUse, отсутствующий уже в исходном hooks.json; этот hook здесь не менялся и не включается ради теста.

- Strict MkDocs baseline из HEAD: exit1, 42 WARNING lines (21 RU + 21 EN); текущий preview: exit1, 351 WARNING lines (330 RU + 21 EN). Финальная строка каждого запуска сообщает 21 warnings только последнего языкового прохода; первоначальная оценка по tail была неполной и исправлена после чтения всего журнала. Новые RU warnings вызваны ссылками переносимых research/design планов и нового backlog на код/evidence за пределами docs, а также прямыми EN sibling links в каталоге. Репозиторные ссылки существуют, но это не рабочие ссылки опубликованного сайта. Полная публикация требует DOCS-16; root site не заменялся.

- Site checks после штатного fix_site_i18n_links: 7 tests, 4 failures — отсутствующие EN страницы и search/source parity; отсутствие успешного strict build не маскируется.

- Исправленные промежуточные ошибки: неверное перебазирование template angle links, CRLF insertion boundary, дополнительные JSON backlinks, legacy DOCS-relative inventories и сортировка expected paths. Assertions не отключались; формальные EN заглушки не добавлялись.

Команды: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_methodology_synthesis tests.product_agent_os.test_self_learning_state tests.product_agent_os.test_coding_standards_artifacts tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_validators tests.product_agent_os.test_doubt_verification -q`; `python -B tools/check_docs.py`; `python -B plugins/product-agent-os/scripts/validate_task_matrix.py` с каждым из пяти названных plans; `python -B -m unittest tests.product_agent_os.docs_archive_checks -q`; `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/planning-relocation-2026-11-15/site`; `tools/fix_site_i18n_links.ps1 -SiteDir .docs-tools/reports/planning-relocation-2026-11-15/site`; `python -B -m unittest tests.product_agent_os.site_checks -q` с PAOS_DOCS_SITE_DIR на этот preview; `git diff --check`. Локальные raw logs: `.docs-tools/reports/planning-relocation-2026-11-15/` (не опубликованы).

DOCS-16/A и DOCS-13/A включены в обязательную первую группу DG01; финальные этапы DOCS-16/B и DOCS-13/B сохраняют исходные зависимости полного закрытия. Историческая проверка PostToolUse сверяется с текущим контрактом без изменения trust ради зелёного теста. EVALS/prod_test: только механические ссылки, рубрики и исторические verdicts не меняются; TEST route сохранён.

Отсутствующие EN страницы: `2026-11-13-ui-implementation-plan.md`, `2026-11-13-v2-ui-implementation-plan.md`, `2026-11-13-v3-ui-implementation-plan.md`, `documentation-architecture-2026-11-15.md`, `functional-remediation-2026-11-15.md`, `product-agent-os-audit-remediation-task-plan-2026-11-09.md`, `product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`, `product-agent-os-web-task-manager-plan-2026-11-09.md` — все в docs/planning. Это реальный переводческий долг, не подтверждение полной RU/EN parity.

## Отдельный список задач

Всего 16 задач PAOS-DOCS-01–16: DOCS-13/16 — in_progress для DG01, остальные 14 — planned. Они не добавляются к 34 FUNC задачам и не меняют их статусы. Начальный запрос покрывал перенос и backlog; последующий запрос DG01 разрешает repair, но не написание всех новых разделов или реализацию фич.

| ID | Задача / каталог | Что сделать | Зависимости |
| --- | --- | --- | --- |
| PAOS-DOCS-01 | Разделить документацию реализации, руководства и базу знаний — `docs/index.md + docs/product/index.md` | Карта разделов с тремя входами: разработка PAOS, использование PAOS, знания о Codex/методологиях. | Нет |
| PAOS-DOCS-02 | Собрать актуальную продуктовую спецификацию и доменную модель — `docs/product/` | overview.md, domain-model.md, capabilities.md, user-journeys.md. | PAOS-DOCS-01 |
| PAOS-DOCS-03 | Консолидировать архитектуру и журнал решений — `docs/architecture/ и docs/architecture/decisions/` | system-context.md, containers.md, data-flow.md, decisions/index.md. | PAOS-DOCS-01, PAOS-DOCS-02 |
| PAOS-DOCS-04 | Описать backend и жизненный цикл локального сервиса — `docs/backend/` | index.md, modules.md, lifecycle.md, commands-events.md, recovery.md. | PAOS-DOCS-03 |
| PAOS-DOCS-05 | Составить справочник HTTP API, событий и общих контрактов — `docs/api/` | index.md, endpoints.md, events.md, errors.md; OpenAPI только после решения о поддерживаемом генераторе. | PAOS-DOCS-03, PAOS-DOCS-04 |
| PAOS-DOCS-06 | Описать frontend, UI/UX и навигационные состояния — `docs/frontend/` | index.md, navigation.md, state-management.md, components.md, design-system.md, accessibility.md. | PAOS-DOCS-01, PAOS-DOCS-02, PAOS-DOCS-03 |
| PAOS-DOCS-07 | Документировать фактическую SQLite-схему и жизненный цикл данных — `docs/db/` | index.md, schema.md, erd.md, migrations.md, transactions.md, backup-restore.md, search-index.md. | PAOS-DOCS-03, PAOS-DOCS-05 |
| PAOS-DOCS-08 | Описать AI-оркестрацию и работу агентов PAOS — `docs/ai/ и docs/ai/agents/` | index.md, agents/orchestration.md, agents/context.md, agents/tools-approvals.md, agents/sessions.md. | PAOS-DOCS-03, PAOS-DOCS-05 |
| PAOS-DOCS-09 | Описать LLM routes, prompts и model/provider boundaries — `docs/ai/llm/` | index.md, routes.md, prompts-and-outputs.md, budgets-and-observability.md. | PAOS-DOCS-08 |
| PAOS-DOCS-10 | Документировать поиск, retrieval и границы RAG — `docs/ai/rag/` | index.md, corpus-and-indexing.md, retrieval.md, freshness-and-provenance.md, evaluation.md. | PAOS-DOCS-07, PAOS-DOCS-08, PAOS-DOCS-09 |
| PAOS-DOCS-11 | Согласовать документацию discovery и графов проекта — `docs/code-intelligence/` | index.md, discovery.md, inventory.md, graph-model.md, queries-impact.md, adapters.md. | PAOS-DOCS-03, PAOS-DOCS-05, PAOS-DOCS-10 |
| PAOS-DOCS-12 | Собрать security/privacy и trust-boundary документацию продукта — `docs/security/` | index.md, threat-model.md, filesystem.md, auth-credentials.md, data-retention.md, supply-chain.md. | PAOS-DOCS-03, PAOS-DOCS-05, PAOS-DOCS-07, PAOS-DOCS-08 |
| PAOS-DOCS-13 | Создать карту тестов, evals и границ доказательств — `docs/testing/` | index.md, test-map.md, synthetic-vs-live.md, ai-evals.md, documentation-checks.md. | PAOS-DOCS-04, PAOS-DOCS-05, PAOS-DOCS-06, PAOS-DOCS-07, PAOS-DOCS-08 |
| PAOS-DOCS-14 | Описать локальную эксплуатацию, упаковку и восстановление — `docs/operations/` | index.md, install-start-stop.md, profiles.md, upgrade-rollback.md, troubleshooting.md, release-boundaries.md. | PAOS-DOCS-04, PAOS-DOCS-07, PAOS-DOCS-12, PAOS-DOCS-13 |
| PAOS-DOCS-15 | Упорядочить документацию Python plugin, skills и learning loop — `docs/product-agent-os/ (существующий раздел)` | Текущий index, module map, CLI/contracts cross-links и разделение staged/manual_only/active. | PAOS-DOCS-01, PAOS-DOCS-03, PAOS-DOCS-08, PAOS-DOCS-11, PAOS-DOCS-13 |
| PAOS-DOCS-16 | Связать документационные задачи с feature delivery и проверить навигацию — `docs/planning/ + mkdocs.yml + docs/sources/` | Owner/update matrix, RU/EN navigation, redirect/link map, maintained current-state indexes. | PAOS-DOCS-01, PAOS-DOCS-02, PAOS-DOCS-03, PAOS-DOCS-04, PAOS-DOCS-05, PAOS-DOCS-06, PAOS-DOCS-07, PAOS-DOCS-08, PAOS-DOCS-09, PAOS-DOCS-10, PAOS-DOCS-11, PAOS-DOCS-12, PAOS-DOCS-13, PAOS-DOCS-14, PAOS-DOCS-15 |

### Task `PAOS-DOCS-01`

- Task: PAOS-DOCS-01 — Разделить документацию реализации, руководства и базу знаний
- Status: planned
- Delivery group: DG02
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Depends on: нет
- Blocks: `PAOS-DOCS-02`, `PAOS-DOCS-03`, `PAOS-DOCS-06`, `PAOS-DOCS-15`, `PAOS-DOCS-16`
- Source: [docs/index.md](../index.md), [docs/product-agent-os/index.md](../product-agent-os/index.md), [docs/agent-systems/overview.md](../agent-systems/overview.md), [docs/methodologies/index.md](../methodologies/index.md)
- Short description: Разделить документацию реализации, руководства и базу знаний
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/index.md + docs/product/index.md; restructure; Карта разделов с тремя входами: разработка PAOS, использование PAOS, знания о Codex/методологиях.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: Карта разделов с тремя входами: разработка PAOS, использование PAOS, знания о Codex/методологиях.
- Acceptance criteria: AC1: Каждый раздел имеет назначение, владельца, source-of-truth и правила актуализации; не создаются пустые категории ради названий. AC2: RU/EN navigation позволяет найти backend/frontend/DB/AI и текущие планы без чтения исторического RUNLOG. AC3: Текущий Web/desktop, Python plugin и будущие функции обозначены раздельно; полнота реализации не выводится из имени папки. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: Карта разделов с тремя входами: разработка PAOS, использование PAOS, знания о Codex/методологиях. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: planned
- what was done: сформулирован scope и acceptance; документация подсистемы ещё не написана.
- files touched / work locations: будущий каталог указан в Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: статическое сопоставление источников; будущие проверки не выполнены.
- residual risks: source drift, смешение historical/planned/current и UI/plugin/runtime surfaces.
- follow-up: выбрать bounded slice по dependencies.
- Documentation impact: будущий source-owned раздел, registry/nav и только затронутые control-plane owners.

### Task `PAOS-DOCS-02`

- Task: PAOS-DOCS-02 — Собрать актуальную продуктовую спецификацию и доменную модель
- Status: planned
- Delivery group: DG02
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-01`
- Blocks: `PAOS-DOCS-03`, `PAOS-DOCS-06`, `PAOS-DOCS-16`
- Source: [research/product-agent-os-web-prd-2026-11-05.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-prd-2026-11-05.md), [docs/planning/product-agent-os-web-task-manager-plan-2026-11-09.md](product-agent-os-web-task-manager-plan-2026-11-09.md), [REQUIREMENTS.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/REQUIREMENTS.md), [packages/contracts/issues/task-profile.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/packages/contracts/issues/task-profile.ts)
- Short description: Собрать актуальную продуктовую спецификацию и доменную модель
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/product/; extract_and_move; overview.md, domain-model.md, capabilities.md, user-journeys.md.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: overview.md, domain-model.md, capabilities.md, user-journeys.md.
- Acceptance criteria: AC1: Из PRD выделены актуальные project/task/workflow/run/approval/evidence сущности, инварианты и пользовательские сценарии; старые версии сохраняются с provenance. AC2: Current/implemented-not-verified/planned и F01–F34/M5 связаны с владельцами задач; README и source-backed claims не противоречат им. AC3: Есть трассировка requirement → code/contract → test/evidence → owning task; требования не дублируются независимыми копиями. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: overview.md, domain-model.md, capabilities.md, user-journeys.md. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: planned
- what was done: сформулирован scope и acceptance; документация подсистемы ещё не написана.
- files touched / work locations: будущий каталог указан в Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: статическое сопоставление источников; будущие проверки не выполнены.
- residual risks: source drift, смешение historical/planned/current и UI/plugin/runtime surfaces.
- follow-up: выбрать bounded slice по dependencies.
- Documentation impact: будущий source-owned раздел, registry/nav и только затронутые control-plane owners.

### Task `PAOS-DOCS-03`

- Task: PAOS-DOCS-03 — Консолидировать архитектуру и журнал решений
- Status: planned
- Delivery group: DG02
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Depends on: `PAOS-DOCS-01`, `PAOS-DOCS-02`
- Blocks: `PAOS-DOCS-04`, `PAOS-DOCS-05`, `PAOS-DOCS-06`, `PAOS-DOCS-07`, `PAOS-DOCS-08`, `PAOS-DOCS-11`, `PAOS-DOCS-12`, `PAOS-DOCS-15`, `PAOS-DOCS-16`
- Source: [research/product-agent-os-web-architecture-2026-11-05.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-architecture-2026-11-05.md), [research/batch45-professional-code-authoring-architecture-v2.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/batch45-professional-code-authoring-architecture-v2.md), [research/batch45-professional-code-authoring-solution-map.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/batch45-professional-code-authoring-solution-map.md), [docs/product-agent-os/architecture.md](../product-agent-os/architecture.md), [docs/diagrams/index.md](../diagrams/index.md)
- Short description: Консолидировать архитектуру и журнал решений
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/architecture/ и docs/architecture/decisions/; extract_and_move; system-context.md, containers.md, data-flow.md, decisions/index.md.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: system-context.md, containers.md, data-flow.md, decisions/index.md.
- Acceptance criteria: AC1: Архитектура сопоставляет Web SPA, local service, SQLite worker, launcher/desktop, Codex App/API routes и Python plugin с реальными исходниками. AC2: Исторические предложения извлечены без повышения статуса; ADR содержат status, rationale, alternatives и consequences. AC3: Диаграммы остаются в существующем atlas и связаны с архитектурой; нет второй конфликтующей схемы. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: system-context.md, containers.md, data-flow.md, decisions/index.md. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: planned
- what was done: сформулирован scope и acceptance; документация подсистемы ещё не написана.
- files touched / work locations: будущий каталог указан в Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: статическое сопоставление источников; будущие проверки не выполнены.
- residual risks: source drift, смешение historical/planned/current и UI/plugin/runtime surfaces.
- follow-up: выбрать bounded slice по dependencies.
- Documentation impact: будущий source-owned раздел, registry/nav и только затронутые control-plane owners.

### Task `PAOS-DOCS-04`

- Task: PAOS-DOCS-04 — Описать backend и жизненный цикл локального сервиса
- Status: planned
- Delivery group: DG03
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Depends on: `PAOS-DOCS-03`
- Blocks: `PAOS-DOCS-05`, `PAOS-DOCS-13`, `PAOS-DOCS-14`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/http/application.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/application.mts), [apps/local-service/src/scheduler/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/scheduler/service.mts), [apps/local-service/src/execution-recipes/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/execution-recipes/service.mts), [apps/local-service/src/supervisor](https://github.com/alexroadcaster/product-agent-os/tree/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/supervisor), [research/product-agent-os-web-m2c-execution-2026-11-12.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-m2c-execution-2026-11-12.md)
- Short description: Описать backend и жизненный цикл локального сервиса
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/backend/; write_from_source; index.md, modules.md, lifecycle.md, commands-events.md, recovery.md.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: index.md, modules.md, lifecycle.md, commands-events.md, recovery.md.
- Acceptance criteria: AC1: Документированы модули и ownership, command/event/outbox flow, concurrency, idempotency, errors, cancellation и shutdown/recovery. AC2: Приведены реальные entrypoints/contracts и тесты, а не описание абстрактного backend из methodologies/backend.md. AC3: Разделяются Web runtime и Python plugin; текущие cross-layer зависимости описаны честно с ссылкой на F08, не объявлены уже исправленными. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: index.md, modules.md, lifecycle.md, commands-events.md, recovery.md. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: planned
- what was done: сформулирован scope и acceptance; документация подсистемы ещё не написана.
- files touched / work locations: будущий каталог указан в Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: статическое сопоставление источников; будущие проверки не выполнены.
- residual risks: source drift, смешение historical/planned/current и UI/plugin/runtime surfaces.
- follow-up: выбрать bounded slice по dependencies.
- Documentation impact: будущий source-owned раздел, registry/nav и только затронутые control-plane owners.

### Task `PAOS-DOCS-05`

- Task: PAOS-DOCS-05 — Составить справочник HTTP API, событий и общих контрактов
- Status: planned
- Delivery group: DG03
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Depends on: `PAOS-DOCS-03`, `PAOS-DOCS-04`
- Blocks: `PAOS-DOCS-07`, `PAOS-DOCS-08`, `PAOS-DOCS-11`, `PAOS-DOCS-12`, `PAOS-DOCS-13`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/http/application.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/application.mts), [apps/local-service/src/http/session-gate.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/session-gate.mts), [apps/web/src/api/client.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/api/client.ts), [packages/contracts](https://github.com/alexroadcaster/product-agent-os/tree/33ed0350738e549f932a9fffdeeff9d4908ca94c/packages/contracts)
- Short description: Составить справочник HTTP API, событий и общих контрактов
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/api/; write_from_source; index.md, endpoints.md, events.md, errors.md; OpenAPI только после решения о поддерживаемом генераторе.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: index.md, endpoints.md, events.md, errors.md; OpenAPI только после решения о поддерживаемом генераторе.
- Acceptance criteria: AC1: Для актуальных маршрутов перечислены request/response, auth/CSRF, errors, pagination, revision/cursor, idempotency и side effects. AC2: Fixtures/examples синтетические; endpoint inventory сверяется с handler/client/tests, unsupported capabilities явно обозначены. AC3: Контракт не обещает отсутствующие Files/scan/DB endpoints F26–F34; schema generation не запускает target scripts. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: index.md, endpoints.md, events.md, errors.md; OpenAPI только после решения о поддерживаемом генераторе. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: planned
- what was done: сформулирован scope и acceptance; документация подсистемы ещё не написана.
- files touched / work locations: будущий каталог указан в Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: статическое сопоставление источников; будущие проверки не выполнены.
- residual risks: source drift, смешение historical/planned/current и UI/plugin/runtime surfaces.
- follow-up: выбрать bounded slice по dependencies.
- Documentation impact: будущий source-owned раздел, registry/nav и только затронутые control-plane owners.

### Task `PAOS-DOCS-06`

- Task: PAOS-DOCS-06 — Описать frontend, UI/UX и навигационные состояния
- Status: planned
- Delivery group: DG04
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Depends on: `PAOS-DOCS-01`, `PAOS-DOCS-02`, `PAOS-DOCS-03`
- Blocks: `PAOS-DOCS-13`, `PAOS-DOCS-16`
- Source: [DESIGN.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/DESIGN.md), [design/2026-11-13-v3/README.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/README.md), [design/2026-11-13-v3/task-field-map.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/task-field-map.md), [apps/web/README.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/README.md), [apps/web/src/ui/App.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/ui/App.tsx), [apps/web/src/features](https://github.com/alexroadcaster/product-agent-os/tree/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features), [docs/web/accessibility.md](../web/accessibility.md)
- Short description: Описать frontend, UI/UX и навигационные состояния
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/frontend/; extract_and_write; index.md, navigation.md, state-management.md, components.md, design-system.md, accessibility.md.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: index.md, navigation.md, state-management.md, components.md, design-system.md, accessibility.md.
- Acceptance criteria: AC1: Существующие screens/routes/components, API state, drafts, polling/late responses, themes и RU/EN описаны с code references. AC2: DESIGN и visual assets остаются владельцами дизайна; docs/frontend даёт карту использования, а не вторую копию tokens/screenshots. AC3: Будущие Files/Map/Database/usages из F26–F34 помечены planned; текущие accessibility evidence и human/WCAG gaps разделены. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: index.md, navigation.md, state-management.md, components.md, design-system.md, accessibility.md. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: planned
- what was done: сформулирован scope и acceptance; документация подсистемы ещё не написана.
- files touched / work locations: будущий каталог указан в Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: статическое сопоставление источников; будущие проверки не выполнены.
- residual risks: source drift, смешение historical/planned/current и UI/plugin/runtime surfaces.
- follow-up: выбрать bounded slice по dependencies.
- Documentation impact: будущий source-owned раздел, registry/nav и только затронутые control-plane owners.

### Task `PAOS-DOCS-07`

- Task: PAOS-DOCS-07 — Документировать фактическую SQLite-схему и жизненный цикл данных
- Status: planned
- Delivery group: DG03
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Depends on: `PAOS-DOCS-03`, `PAOS-DOCS-05`
- Blocks: `PAOS-DOCS-10`, `PAOS-DOCS-12`, `PAOS-DOCS-13`, `PAOS-DOCS-14`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/storage/migrations/schema.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/migrations/schema.mts), [apps/local-service/src/storage/sqlite-worker.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/sqlite-worker.mts), [apps/local-service/src/storage/local-store.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/local-store.mts), [apps/local-service/src/storage/restore-worker.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/restore-worker.mts), [research/product-agent-os-web-storage-research-2026-11-09.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-storage-research-2026-11-09.md)
- Short description: Документировать фактическую SQLite-схему и жизненный цикл данных
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/db/; extract_and_write; index.md, schema.md, erd.md, migrations.md, transactions.md, backup-restore.md, search-index.md.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: index.md, schema.md, erd.md, migrations.md, transactions.md, backup-restore.md, search-index.md.
- Acceptance criteria: AC1: Таблицы/колонки/PK/FK/indexes/FTS, JSON payloads и schema/checksum/version fences сверены с source; есть editable Mermaid ERD и объяснение authority. AC2: WAL/worker ownership, transactions/idempotency, snapshot/backup/restore/import и отказные случаи связаны с тестами; реальные БД пользователя не открываются. AC3: SQLite PAOS отличается от целевой БД проекта F33; PostgreSQL/pgvector M5 помечены planned, а не текущим хранилищем. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: index.md, schema.md, erd.md, migrations.md, transactions.md, backup-restore.md, search-index.md. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: planned
- what was done: сформулирован scope и acceptance; документация подсистемы ещё не написана.
- files touched / work locations: будущий каталог указан в Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: статическое сопоставление источников; будущие проверки не выполнены.
- residual risks: source drift, смешение historical/planned/current и UI/plugin/runtime surfaces.
- follow-up: выбрать bounded slice по dependencies.
- Documentation impact: будущий source-owned раздел, registry/nav и только затронутые control-plane owners.

### Task `PAOS-DOCS-08`

- Task: PAOS-DOCS-08 — Описать AI-оркестрацию и работу агентов PAOS
- Status: planned
- Delivery group: DG05
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Depends on: `PAOS-DOCS-03`, `PAOS-DOCS-05`
- Blocks: `PAOS-DOCS-09`, `PAOS-DOCS-10`, `PAOS-DOCS-12`, `PAOS-DOCS-13`, `PAOS-DOCS-15`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/runtime/route-selector.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/route-selector.ts), [apps/local-service/src/runtime/app-agent-gateway.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/app-agent-gateway.mts), [apps/local-service/src/runtime/codex/coordinator.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/codex/coordinator.ts), [apps/local-service/src/team/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/team/service.mts), [docs/product-agent-os/live-runtime-governance.md](../product-agent-os/live-runtime-governance.md), [docs/agent-systems/subagents-skills.md](../agent-systems/subagents-skills.md)
- Short description: Описать AI-оркестрацию и работу агентов PAOS
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/ai/ и docs/ai/agents/; extract_and_write; index.md, agents/orchestration.md, agents/context.md, agents/tools-approvals.md, agents/sessions.md.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: index.md, agents/orchestration.md, agents/context.md, agents/tools-approvals.md, agents/sessions.md.
- Acceptance criteria: AC1: Описан фактический dispatch/attach/session/approval/Stop flow и границы ответственности Codex и PAOS; status configured/pinned/observed не смешивается. AC2: Web execution и packaged lifecycle agents/skills показаны как разные surfaces с реальными selectors/callers. AC3: Общие советы agent-systems остаются справочником; каждое описание реализации ссылается на код и evidence, без обещаний autonomous hosted delivery. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: index.md, agents/orchestration.md, agents/context.md, agents/tools-approvals.md, agents/sessions.md. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: planned
- what was done: сформулирован scope и acceptance; документация подсистемы ещё не написана.
- files touched / work locations: будущий каталог указан в Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: статическое сопоставление источников; будущие проверки не выполнены.
- residual risks: source drift, смешение historical/planned/current и UI/plugin/runtime surfaces.
- follow-up: выбрать bounded slice по dependencies.
- Documentation impact: будущий source-owned раздел, registry/nav и только затронутые control-plane owners.

### Task `PAOS-DOCS-09`

- Task: PAOS-DOCS-09 — Описать LLM routes, prompts и model/provider boundaries
- Status: planned
- Delivery group: DG05
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-08`
- Blocks: `PAOS-DOCS-10`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/runtime/route-selector.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/route-selector.ts), [apps/local-service/src/connections](https://github.com/alexroadcaster/product-agent-os/tree/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/connections), [research/product-agent-os-web-auth-commercial-2026-11-09.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-auth-commercial-2026-11-09.md), [plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py), [plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_proposal_provider.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_proposal_provider.py)
- Short description: Описать LLM routes, prompts и model/provider boundaries
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/ai/llm/; extract_and_write; index.md, routes.md, prompts-and-outputs.md, budgets-and-observability.md.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: index.md, routes.md, prompts-and-outputs.md, budgets-and-observability.md.
- Acceptance criteria: AC1: codex_app_agent и local_api_byok, explicit route choice/no silent fallback, credentials и failure recovery описаны по source; внешние OpenAI claims перепроверяются по официальным источникам при написании. AC2: Инвентаризированы prompt/output contracts и owners; deterministic proposal gate не называется live LLM generation. AC3: Tokens/cost/latency ограничены наблюдаемыми источниками; F11/F15 и отсутствующие capabilities помечены planned/unknown, secrets не попадают в примеры. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: index.md, routes.md, prompts-and-outputs.md, budgets-and-observability.md. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: planned
- what was done: сформулирован scope и acceptance; документация подсистемы ещё не написана.
- files touched / work locations: будущий каталог указан в Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: статическое сопоставление источников; будущие проверки не выполнены.
- residual risks: source drift, смешение historical/planned/current и UI/plugin/runtime surfaces.
- follow-up: выбрать bounded slice по dependencies.
- Documentation impact: будущий source-owned раздел, registry/nav и только затронутые control-plane owners.

### Task `PAOS-DOCS-10`

- Task: PAOS-DOCS-10 — Документировать поиск, retrieval и границы RAG
- Status: planned
- Delivery group: DG05
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-07`, `PAOS-DOCS-08`, `PAOS-DOCS-09`
- Blocks: `PAOS-DOCS-11`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/storage/search-queries.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/search-queries.mts), [plugins/product-agent-os/scripts/product_agent_os/project_graph_chunking.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_chunking.py), [plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py), [plugins/product-agent-os/scripts/product_agent_os/project_graph_embedding_provider.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_embedding_provider.py), [plugins/product-agent-os/scripts/product_agent_os/project_graph_hybrid_retrieval.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_hybrid_retrieval.py), [docs/product-agent-os/project-code-graph.md](../product-agent-os/project-code-graph.md)
- Short description: Документировать поиск, retrieval и границы RAG
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/ai/rag/; extract_and_write; index.md, corpus-and-indexing.md, retrieval.md, freshness-and-provenance.md, evaluation.md.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: index.md, corpus-and-indexing.md, retrieval.md, freshness-and-provenance.md, evaluation.md.
- Acceptance criteria: AC1: Раздельно описаны Web SQLite FTS5, Python graph retrieval/semantic cache и approval-bound provider adapters; отсутствие подтверждённого end-to-end Web RAG обозначено явно. AC2: Для существующих веток зафиксированы corpus/filters/chunking/revision/freshness, query budget и failure/rollback; live embeddings не подразумеваются. AC3: Retrieval quality отделена от answer quality; current deterministic checks, future provider evals и M5 pgvector имеют разные статусы. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: index.md, corpus-and-indexing.md, retrieval.md, freshness-and-provenance.md, evaluation.md. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: planned
- what was done: сформулирован scope и acceptance; документация подсистемы ещё не написана.
- files touched / work locations: будущий каталог указан в Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: статическое сопоставление источников; будущие проверки не выполнены.
- residual risks: source drift, смешение historical/planned/current и UI/plugin/runtime surfaces.
- follow-up: выбрать bounded slice по dependencies.
- Documentation impact: будущий source-owned раздел, registry/nav и только затронутые control-plane owners.

### Task `PAOS-DOCS-11`

- Task: PAOS-DOCS-11 — Согласовать документацию discovery и графов проекта
- Status: planned
- Delivery group: DG05
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-03`, `PAOS-DOCS-05`, `PAOS-DOCS-10`
- Blocks: `PAOS-DOCS-15`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/code-index/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/service.mts), [apps/local-service/src/code-index/lexical.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/lexical.mts), [plugins/product-agent-os/scripts/product_agent_os/discovery.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/discovery.py), [plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py), [docs/product-agent-os/project-code-graph.md](../product-agent-os/project-code-graph.md), [docs/product-agent-os/graph-intelligence-contract.md](../product-agent-os/graph-intelligence-contract.md)
- Short description: Согласовать документацию discovery и графов проекта
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/code-intelligence/; reuse_and_write; index.md, discovery.md, inventory.md, graph-model.md, queries-impact.md, adapters.md.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: index.md, discovery.md, inventory.md, graph-model.md, queries-impact.md, adapters.md.
- Acceptance criteria: AC1: Python core discovery/graph и Web lexical graph описаны отдельно, с матрицей языков/связей/source/limits и реальным integration status. AC2: Источники existing graph contract сохраняют владельца; navigation links объясняют какой путь использует Web и какой CLI. AC3: F26–F34 и PoC engines отмечены planned до runtime evidence; docs обновляются владельцем feature при выполнении соответствующей FUNC задачи. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: index.md, discovery.md, inventory.md, graph-model.md, queries-impact.md, adapters.md. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: planned
- what was done: сформулирован scope и acceptance; документация подсистемы ещё не написана.
- files touched / work locations: будущий каталог указан в Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: статическое сопоставление источников; будущие проверки не выполнены.
- residual risks: source drift, смешение historical/planned/current и UI/plugin/runtime surfaces.
- follow-up: выбрать bounded slice по dependencies.
- Documentation impact: будущий source-owned раздел, registry/nav и только затронутые control-plane owners.

### Task `PAOS-DOCS-12`

- Task: PAOS-DOCS-12 — Собрать security/privacy и trust-boundary документацию продукта
- Status: planned
- Delivery group: DG06
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Depends on: `PAOS-DOCS-03`, `PAOS-DOCS-05`, `PAOS-DOCS-07`, `PAOS-DOCS-08`
- Blocks: `PAOS-DOCS-14`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/http/session-gate.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/session-gate.mts), [apps/local-service/src/runtime/app-agent-files.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/app-agent-files.mts), [apps/local-service/src/redaction](https://github.com/alexroadcaster/product-agent-os/tree/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/redaction), [docs/product-agent-os/privacy-supply-chain-retention.md](../product-agent-os/privacy-supply-chain-retention.md), [research/product-agent-os-web-auth-commercial-2026-11-09.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-auth-commercial-2026-11-09.md)
- Short description: Собрать security/privacy и trust-boundary документацию продукта
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/security/; extract_and_write; index.md, threat-model.md, filesystem.md, auth-credentials.md, data-retention.md, supply-chain.md.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: index.md, threat-model.md, filesystem.md, auth-credentials.md, data-retention.md, supply-chain.md.
- Acceptance criteria: AC1: Local HTTP/session/CSRF/origin, filesystem root, approvals, credentials, redaction и profile isolation привязаны к guards/tests. AC2: Platform guidance codex/security.md и фактические ограничения приложения различаются; configured policy не называется доказанным enforcement. AC3: Нет secrets/PII/real profile dump; commercial/license gaps и внешние authority gates сохранены. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: index.md, threat-model.md, filesystem.md, auth-credentials.md, data-retention.md, supply-chain.md. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: planned
- what was done: сформулирован scope и acceptance; документация подсистемы ещё не написана.
- files touched / work locations: будущий каталог указан в Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: статическое сопоставление источников; будущие проверки не выполнены.
- residual risks: source drift, смешение historical/planned/current и UI/plugin/runtime surfaces.
- follow-up: выбрать bounded slice по dependencies.
- Documentation impact: будущий source-owned раздел, registry/nav и только затронутые control-plane owners.

### Task `PAOS-DOCS-13`

- Task: PAOS-DOCS-13 — Создать карту тестов, evals и границ доказательств
- Status: in_progress
- Delivery group: DG01 (A), DG06 (B; полное закрытие)
- Execution stages: A — DG01, без будущих domain prerequisites; B — после A и всех исходных Depends on. Выполнение A не закрывает задачу; полный scope/AC сохранён. Этап A completed; B planned.
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-04`, `PAOS-DOCS-05`, `PAOS-DOCS-06`, `PAOS-DOCS-07`, `PAOS-DOCS-08`
- Blocks: `PAOS-DOCS-14`, `PAOS-DOCS-15`, `PAOS-DOCS-16`
- Source: [TEST.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/TEST.md), [EVALS.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/EVALS.md), [tests/web](https://github.com/alexroadcaster/product-agent-os/tree/33ed0350738e549f932a9fffdeeff9d4908ca94c/tests/web), [tests/product_agent_os](https://github.com/alexroadcaster/product-agent-os/tree/33ed0350738e549f932a9fffdeeff9d4908ca94c/tests/product_agent_os), [docs/product-agent-os/behavioral-evals.md](../product-agent-os/behavioral-evals.md), [docs/web/accessibility.md](../web/accessibility.md)
- Short description: Создать карту тестов, evals и границ доказательств
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/testing/; extract_and_write; index.md, test-map.md, synthetic-vs-live.md, ai-evals.md, documentation-checks.md.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: index.md, test-map.md, synthetic-vs-live.md, ai-evals.md, documentation-checks.md.
- Acceptance criteria: AC1: Каждая подсистема связана с targeted test/eval/browser/native checks и условиями расширения; TEST/EVALS остаются оперативными владельцами команд/порогов. AC2: Исторические receipts, текущие проверки, human acceptance и production claims не смешаны; flaky/blocked сценарии видимы. AC3: Установлен проверяемый маршрут source links → strict preview → RU/EN/search/site parity; failures текущей миграции и baseline различаются, проверки не ослабляются. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: index.md, test-map.md, synthetic-vs-live.md, ai-evals.md, documentation-checks.md. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: in_progress
- what was done: Этап A завершён в DG01; этап B и полная приёмка родительской задачи остаются открытыми.
- files touched / work locations: docs/planning/, затронутые guides/registries и docs_archive_checks.py; изолированный .docs-tools/reports/dg01/site.
- technical value delivered: Этап A docs_static_verified; B not_implemented.
- product value delivered: Рабочая RU/EN навигация и сохранённые planning contracts; будущие subsystem guides остаются planned.
- actual implementation date and time: Этап A 15-11-2026; полная задача pending_execution_timestamp.
- verification evidence: [Результаты DG01](#dg01-results); archive 99/99, source 3/3, site 7/7; matrices, strict build и HTML links passed.
- residual risks: Зависимости B и исходные AC полной задачи остаются обязательными.
- follow-up: DG06 / DOCS-13/B после исходных dependencies; следующая общая группа DG02.
- Documentation impact: Этап A синхронизирован с owning plan, каталогом, registries и control plane; domain documentation остаётся planned.

### Task `PAOS-DOCS-14`

- Task: PAOS-DOCS-14 — Описать локальную эксплуатацию, упаковку и восстановление
- Status: planned
- Delivery group: DG07
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-04`, `PAOS-DOCS-07`, `PAOS-DOCS-12`, `PAOS-DOCS-13`
- Blocks: `PAOS-DOCS-16`
- Source: [apps/desktop-local/README.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/desktop-local/README.md), [apps/desktop-local/distribution.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/desktop-local/distribution.mts), [apps/launcher/launcher.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/launcher/launcher.ts), [docs/web/pilot.md](../web/pilot.md), [docs/release/web-m4-local-release.json](../release/web-m4-local-release.json), [research/product-agent-os-web-m4-0030-execution-2026-11-12.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-m4-0030-execution-2026-11-12.md)
- Short description: Описать локальную эксплуатацию, упаковку и восстановление
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/operations/; extract_and_write; index.md, install-start-stop.md, profiles.md, upgrade-rollback.md, troubleshooting.md, release-boundaries.md.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: index.md, install-start-stop.md, profiles.md, upgrade-rollback.md, troubleshooting.md, release-boundaries.md.
- Acceptance criteria: AC1: Команды и параметры сверены с CLI/launcher, paths/profile ownership и штатный Stop понятны; опасные действия не выдаются за default troubleshooting. AC2: Build/package/qualification/install/upgrade/rollback разделены; unsigned/local/human/commercial gaps не исчезают при переносе receipts. AC3: F17 остаётся отдельной реализационной задачей; документация не публикует и не устанавливает приложение. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: index.md, install-start-stop.md, profiles.md, upgrade-rollback.md, troubleshooting.md, release-boundaries.md. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: planned
- what was done: сформулирован scope и acceptance; документация подсистемы ещё не написана.
- files touched / work locations: будущий каталог указан в Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: статическое сопоставление источников; будущие проверки не выполнены.
- residual risks: source drift, смешение historical/planned/current и UI/plugin/runtime surfaces.
- follow-up: выбрать bounded slice по dependencies.
- Documentation impact: будущий source-owned раздел, registry/nav и только затронутые control-plane owners.

### Task `PAOS-DOCS-15`

- Task: PAOS-DOCS-15 — Упорядочить документацию Python plugin, skills и learning loop
- Status: planned
- Delivery group: DG07
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-01`, `PAOS-DOCS-03`, `PAOS-DOCS-08`, `PAOS-DOCS-11`, `PAOS-DOCS-13`
- Blocks: `PAOS-DOCS-16`
- Source: [plugins/product-agent-os/README.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/README.md), [docs/product-agent-os/cli-reference.md](../product-agent-os/cli-reference.md), [docs/product-agent-os/project-formation.md](../product-agent-os/project-formation.md), [docs/product-agent-os/self-learning-loop.md](../product-agent-os/self-learning-loop.md), [plugins/product-agent-os/scripts/product_agent_os/self_learning_state.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/self_learning_state.py)
- Short description: Упорядочить документацию Python plugin, skills и learning loop
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/product-agent-os/ (существующий раздел); reuse_and_reorganize; Текущий index, module map, CLI/contracts cross-links и разделение staged/manual_only/active.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: Текущий index, module map, CLI/contracts cross-links и разделение staged/manual_only/active.
- Acceptance criteria: AC1: Существующие полноценные plugin guides переиспользованы, отсутствующие module/consumer links добавлены; новый дублирующий каталог plugin не создаётся. AC2: Agents/skills/hooks/templates/validators/learning candidates имеют актуальных owners и правила обновления; activation не выводится из наличия файла. AC3: Manual-only/candidate-only и target-preservation contracts сохранены; task history отделена от руководства. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: Текущий index, module map, CLI/contracts cross-links и разделение staged/manual_only/active. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: planned
- what was done: сформулирован scope и acceptance; документация подсистемы ещё не написана.
- files touched / work locations: будущий каталог указан в Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: статическое сопоставление источников; будущие проверки не выполнены.
- residual risks: source drift, смешение historical/planned/current и UI/plugin/runtime surfaces.
- follow-up: выбрать bounded slice по dependencies.
- Documentation impact: будущий source-owned раздел, registry/nav и только затронутые control-plane owners.

### Task `PAOS-DOCS-16`

- Task: PAOS-DOCS-16 — Связать документационные задачи с feature delivery и проверить навигацию
- Status: in_progress
- Delivery group: DG01 (A), DG07 (B; полное закрытие)
- Execution stages: A — DG01, без будущих domain prerequisites; B — после A и всех исходных Depends on. Выполнение A не закрывает задачу; полный scope/AC сохранён. Этап A completed; B planned.
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-01`, `PAOS-DOCS-02`, `PAOS-DOCS-03`, `PAOS-DOCS-04`, `PAOS-DOCS-05`, `PAOS-DOCS-06`, `PAOS-DOCS-07`, `PAOS-DOCS-08`, `PAOS-DOCS-09`, `PAOS-DOCS-10`, `PAOS-DOCS-11`, `PAOS-DOCS-12`, `PAOS-DOCS-13`, `PAOS-DOCS-14`, `PAOS-DOCS-15`
- Blocks: нет
- Source: [docs/planning/functional-remediation-2026-11-15.json](functional-remediation-2026-11-15.json), [docs/planning/functional-remediation-2026-11-15.md](functional-remediation-2026-11-15.md), [mkdocs.yml](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/mkdocs.yml), [docs/sources/registry.md](../sources/registry.md), [docs/sources/registry.en.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/sources/registry.en.md)
- Short description: Связать документационные задачи с feature delivery и проверить навигацию
- Technical value: Canonical ownership, source-to-contract traceability и меньшая вероятность неверного изменения кода агентом.
- Product value: Разработчик и пользователь понимают текущее поведение, ограничения и следующий шаг.
- Scope: docs/planning/ + mkdocs.yml + docs/sources/; integrate_and_verify; Owner/update matrix, RU/EN navigation, redirect/link map, maintained current-state indexes.
- Non-goals: Новая функциональность, silent provider/runtime activation, переписывание evidence или дублирование методологий.
- Expected result: Owner/update matrix, RU/EN navigation, redirect/link map, maintained current-state indexes.
- Acceptance criteria: AC1: Каждый FUNC delivery group имеет documentation owner и список затрагиваемых разделов; feature closure требует актуализации именно своих фактов, а не всей базы. AC2: Ссылки/anchors, локализация и search/sitemap проверены на изолированном strict build; старые адреса маршрутизированы или явно описана миграция, historical receipts сохранены. AC3: Все 16 documentation tasks имеют source/acceptance/status; запуск CI/automation/publication не производится этой задачей планирования. AC5: Восемь EN gaps из evidence устранены содержательными переводами, strict build и site checks проходят; новые warnings после migration отсутствуют. AC4: Есть Source status, владелец, scope/version, source links, related tests и known limitations; связанные RU/EN/nav/registry обновлены без ложного implemented/live claim.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs и affected site checks для nav/render; exact commands/results записать при исполнении.
- Risks / approval gates: Не выдавать план за реализацию. Live/provider/user profile/installation/publication не разрешены; stale источники перепроверить до записи.
- Complexity: medium; broad source reconciliation, точный объём после current-source review
- Estimated execution time: Не оценено: сначала ограничить source/module slice; срок не является обязательством.
- Agents: docs-maintainer с source owner; роли предложены, команда сейчас не запускается
- Skills: documentation-and-adrs; implementation-specific skills только при необходимости
- Output artifacts: Owner/update matrix, RU/EN navigation, redirect/link map, maintained current-state indexes. Статус и receipts — эта карточка; краткий handoff — RUNLOG.
- Rollback: Только собственные изменения с сохранением source history, backlink map и предыдущих документов.
- Next step: Проверить dependencies и выбрать один документационный slice; не запускать весь backlog автоматически.

#### Completion Report

- status: in_progress
- what was done: Этап A завершён в DG01; этап B и полная приёмка родительской задачи остаются открытыми.
- files touched / work locations: docs/planning/, затронутые guides/registries и docs_archive_checks.py; изолированный .docs-tools/reports/dg01/site.
- technical value delivered: Этап A docs_static_verified; B not_implemented.
- product value delivered: Рабочая RU/EN навигация и сохранённые planning contracts; будущие subsystem guides остаются planned.
- actual implementation date and time: Этап A 15-11-2026; полная задача pending_execution_timestamp.
- verification evidence: [Результаты DG01](#dg01-results); archive 99/99, source 3/3, site 7/7; matrices, strict build и HTML links passed.
- residual risks: Зависимости B и исходные AC полной задачи остаются обязательными.
- follow-up: DG07 / DOCS-16/B после исходных dependencies; следующая общая группа DG02.
- Documentation impact: Этап A синхронизирован с owning plan, каталогом, registries и control plane; domain documentation остаётся planned.
