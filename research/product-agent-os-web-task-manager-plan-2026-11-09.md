# Product-Agent OS Web — план полноценного Task Manager

Текущий M2,12-11-2026: **26/26 implemented в local App-active technical scope**. Последние PAOS-0019/0020/0021/0022/0027: skills по требованиям/описанию, scoped code index/graph/impact, документы/checks/search. Web398/398, browser37, actual App29/2jobs, independent7findings fixed. [Текущие проверки и пределы](product-agent-os-web-m2c-execution-2026-11-12.md), [results](product-agent-os-web-m2c-results-2026-11-12.json). Все56 карточек/12групп/estimates сохранены; M3/T1, human/commercial/release отдельно. Ниже dated receipts — исторические срезы, не текущая очередь.


Текущий M2, 11-11-2026: **10/26 implemented** — PAOS-0031/0032/0033/0005/0006/0007/0008/0034/0038/0035, только выбранная владельцем очередь. Остальные16, включая PAOS-0036, planned. Web345/345, browser88, actual App/native27 и independent closed_allowed; [проверки и пределы](product-agent-os-web-m2-execution-2026-11-11.md), [results](product-agent-os-web-m2-results-2026-11-11.json). Полные56 cards/12groups/estimates сохранены. Ниже M1 receipts и старые срезы сохраняют исходный provenance; commercial/human/release отдельно.

Актуализация 11-11-2026: owner-default runtime теперь Codex App agents без API key. Нормативное уточнение App-dependent acceptance — в addendum в конце этого файла; последовательность 56 задач, 12 групп и оценки сохранены.

Текущее техническое состояние M1: **18/18 implemented**, включая PAOS-0042, PAOS-0043, PAOS-0044 и PAOS-0045. Применяется App-active контракт PRD §17.7 / architecture §21.10: actual App/native105, task39, data25, headless33, Web306 и independent closed_allowed. [Приёмка и предел утверждений](product-agent-os-web-m1-execution-2026-11-11.md#app-mediated-native-broker--техническая-приёмка-m1). Более ранние 14/3/1 и blocked statements ниже — исторические срезы, не текущая очередь. PAOS-0046 ранний review выполнен; следующая реализация — локальная M2 в авторизованном чате. Human/commercial/release acceptance отдельно.

Source status: project-authored / proposed / requirements-backed. Дата: 2026-11-09.

Статус очереди: **order_approved / implementation_started / acceptance_partial**. Native MXC write/deny 11 ноября снял прежний Windows blocker PAOS-0054; local engineering route PAOS-0039 отделён от commercial gates. Реализуются все локальные поверхности M1 и исполняемый пакет PAOS-0045. [Текущий execution report](product-agent-os-web-m1-execution-2026-11-11.md) отделяет native/headless/SQLite evidence от фактических browser/App-agent проверок и оставшихся runtime/provider gates. Статусы и фактическое время хранятся в карточках и JSON. При расхождении приоритет имеют PRD §17, architecture §21 и актуальная очередь v0.8.

Связи: [PRD](product-agent-os-web-prd-2026-11-05.md), [архитектура](product-agent-os-web-architecture-2026-11-05.md), [экраны](product-agent-os-web-task-manager-screens-2026-11-09.md), [машинные группы](product-agent-os-web-task-manager-task-group-2026-11-09.json).




## Актуальная очередь v0.8: утверждённая последовательность

Source status: project-authored plan, 2026-11-10; 56 tasks / 12 groups; implementation_started. Нормативный scope — PRD §17, архитектура §21, wireframes v0.7. Очереди v0.1–v0.7 и прежние receipts ниже — история; при расхождении применяется этот раздел и обновлённые карточки/JSON.

| Этап | Задачи и gate | Ownership / результат |
| --- | --- | --- |
| M1a contracts | 0001 → 0054; 0002/0003 → 0048 после 0054; 0004; 0039/0040 → 0041 после 0054 | Architect фиксирует manifest/schema/policies; storage owner — driver/FTS5/transactions; runtime owner — bootstrap/credentials |
| M1b single window | 0048+0054 → 0055; 0041+0048+0055 → 0042 → 0043 → 0044 | Commands, scopes и writers до execution; минимальный Task CRUD/доска/catalog read-only принадлежат 0043 |
| M1c data | От 0048 независимо 0049 search, 0050 preview, 0051 backup; 0050+0051+0055+0044 → 0056 cutover | Backup и restore доказаны до смены authority; source digests проверяются после freeze |
| M1 acceptance | 0044+0049+0051+0056 → 0045 | Вся матрица ниже, включая UI, data и negative cases |
| После M1 | **0046**, сразу после 0045 и до M2 | Ранний commercial review; повторная актуализация перед выпуском в 0030 |
| M2 | Full Task Manager/каталоги/граф, **0035/0036/0038**, 0027 | Расширения M1 schema; полный ST-03/ST-09, без второй БД |
| M3 | G07, **0037** | Workflow execution/agent autonomy поверх M1 coordinator |
| M4 | 0028/0029/0030; optional 0047 отдельно | Local acceptance/pilot; повторная проверка AUTH-G1–G6 и gaps раннего 0046 |
| T1 | 0052 после 0030 и storage foundations; 0053 после 0052/0056 | Separate hosting/auth/RBAC/runtime design; local M4 не зависит от team |

Новые задачи: 0054 compatibility manifest (12 h), 0055 agent commands/writers (16 h), 0056 cutover (12 h). 0050 сокращена до preview/staging (12 h вместо 20), 0051 больше не зависит от 0050. Полное транзитивное замыкание M1 до 0045 — **18 задач, 234 engineering hours**, rough estimate. Оценки требуют уточнения после 0054; будущие M2–T1 не включены.

### Зафиксированная матрица очереди v0.8

Решение пользователя 2026-11-10: порядок ниже сохранён в execution_plan.stages и tasks[].execution_order/delivery_stage JSON. Приоритет раздела над прежними stage labels. Группы G01–G12 сохраняют владение модулями; номер группы не означает порядок исполнения. Детальные карточки ниже остаются отсортированы по ID.

Порядок — последовательная плановая baseline; технические depends_on не дополнены искусственными зависимостями между соседними строками. Независимая параллельная работа требует соблюдения dependencies и отдельных владельцев файлов. OPTIONAL можно пропустить; T1 не зависит от 0047 и требует отдельного team design/start. Никаких автоматических запусков эта metadata не создаёт.

| Этап | Задач | Оценка |
| --- | ---: | ---: |
| M1 — Единое рабочее окно | 18 | 234 ч |
| POST_M1 — Ранний коммерческий review | 1 | 8 ч |
| M2 — Полный Task Manager | 26 | 338 ч |
| M3 — Управляемая автономность | 5 | 84 ч |
| M4 — Приёмка и локальный пилот | 3 | 52 ч |
| OPTIONAL — Sign in with ChatGPT | 1 | 20 ч |
| T1 — Командная версия после отдельного design/start | 2 | 40 ч |
| Всего | 56 | 776 ч |

Local до пилота — 708 ч без OPTIONAL/T1; M1 — 234 ч. Rough estimates без резерва и календарного обещания.

| № | Этап | Группа | ID | Задача | Оценка |
| ---: | --- | --- | --- | --- | ---: |
| 1 | M1 | G01 | PAOS-0001 | Контракты и адаптеры проекта | 8 ч |
| 2 | M1 | G11 | PAOS-0054 | Контракт совместимости M1 и runtime manifest | 12 ч |
| 3 | M1 | G11 | PAOS-0039 | Допустимые auth routes и коммерческие границы | 6 ч |
| 4 | M1 | G01 | PAOS-0002 | Модель задачи и идентификаторы | 12 ч |
| 5 | M1 | G01 | PAOS-0003 | Время и журнал событий | 12 ч |
| 6 | M1 | G01 | PAOS-0004 | Темы и локализация | 8 ч |
| 7 | M1 | G11 | PAOS-0040 | Launcher и жизненный цикл локального приложения | 12 ч |
| 8 | M1 | G11 | PAOS-0041 | Локальное API-подключение и credential isolation | 16 ч |
| 9 | M1 | G12 | PAOS-0048 | SQLite: схема и транзакционные команды | 16 ч |
| 10 | M1 | G12 | PAOS-0055 | Команды агентов и совместимость legacy writers | 16 ч |
| 11 | M1 | G11 | PAOS-0042 | Codex App Server adapter и ограниченное выполнение | 20 ч |
| 12 | M1 | G11 | PAOS-0043 | Активная сессия и минимальная карточка задачи | 20 ч |
| 13 | M1 | G11 | PAOS-0044 | Recovery, повторное подключение и сохранённые сессии | 16 ч |
| 14 | M1 | G12 | PAOS-0049 | Локальный полнотекстовый поиск FTS5 | 12 ч |
| 15 | M1 | G12 | PAOS-0051 | Резервное копирование и восстановление local data | 12 ч |
| 16 | M1 | G12 | PAOS-0050 | Предварительный импорт MD/JSON в staging | 12 ч |
| 17 | M1 | G12 | PAOS-0056 | Переключение источника задач и проверка миграции | 12 ч |
| 18 | M1 | G11 | PAOS-0045 | Приёмка сквозного M1 в одном окне | 12 ч |
| 19 | POST_M1 | G11 | PAOS-0046 | Коммерческий review API-варианта и выпускные gates | 8 ч |
| 20 | M2 | G09 | PAOS-0031 | Иерархия Epic / Task / Bug / UserStory / Sub-Task | 14 ч |
| 21 | M2 | G09 | PAOS-0032 | Поля, авторство, приоритеты, компоненты и даты | 12 ч |
| 22 | M2 | G09 | PAOS-0033 | Версии продукта и release policy | 12 ч |
| 23 | M2 | G02 | PAOS-0005 | Список и доска задач | 14 ч |
| 24 | M2 | G02 | PAOS-0006 | Карточка и редактор задачи | 16 ч |
| 25 | M2 | G02 | PAOS-0007 | Файлы, артефакты и исполнители | 8 ч |
| 26 | M2 | G02 | PAOS-0008 | Приёмка и жизненный цикл | 14 ч |
| 27 | M2 | G09 | PAOS-0034 | Attachments, комментарии и история изменений | 20 ч |
| 28 | M2 | G10 | PAOS-0038 | Linked Issues и блокирующие зависимости | 14 ч |
| 29 | M2 | G10 | PAOS-0035 | Kanban и ручной жизненный цикл задачи | 16 ч |
| 30 | M2 | G10 | PAOS-0036 | Редактор, версии и миграции workflow | 20 ч |
| 31 | M2 | G03 | PAOS-0009 | Каталог всех доступных сессий | 12 ч |
| 32 | M2 | G03 | PAOS-0010 | Сообщения и переходы по контексту | 12 ч |
| 33 | M2 | G03 | PAOS-0011 | Поиск, приватность и хранение сессий | 10 ч |
| 34 | M2 | G04 | PAOS-0012 | Каталог и профиль агента | 8 ч |
| 35 | M2 | G04 | PAOS-0013 | Создание, изменение и удаление агента | 12 ч |
| 36 | M2 | G04 | PAOS-0014 | Управление агентом по описанию | 10 ч |
| 37 | M2 | G04 | PAOS-0015 | Назначения и статистика агентов | 12 ч |
| 38 | M2 | G05 | PAOS-0016 | Каталог и профиль скилла | 8 ч |
| 39 | M2 | G05 | PAOS-0017 | Редактор и версии скиллов | 12 ч |
| 40 | M2 | G05 | PAOS-0018 | Добавление по пути и find-skills | 12 ч |
| 41 | M2 | G05 | PAOS-0019 | Генерация по требованиям и описанию | 12 ч |
| 42 | M2 | G06 | PAOS-0020 | Индекс файлов и символов | 16 ч |
| 43 | M2 | G06 | PAOS-0021 | Граф и навигация к исходникам | 14 ч |
| 44 | M2 | G06 | PAOS-0022 | Влияние переменной и изменения | 14 ч |
| 45 | M2 | G08 | PAOS-0027 | Документы, проверки и общий поиск | 14 ч |
| 46 | M3 | G07 | PAOS-0023 | Политика автономности и лимиты | 12 ч |
| 47 | M3 | G10 | PAOS-0037 | Цепочки агентов и привязка к workflow | 20 ч |
| 48 | M3 | G07 | PAOS-0024 | Очередь, назначения и владение файлами | 16 ч |
| 49 | M3 | G07 | PAOS-0025 | Исполнение, восстановление и отмена | 24 ч |
| 50 | M3 | G07 | PAOS-0026 | Решения и наблюдаемость автономности | 12 ч |
| 51 | M4 | G08 | PAOS-0028 | Интеграционная проверка пути | 24 ч |
| 52 | M4 | G08 | PAOS-0029 | Доступность, языки и темы | 12 ч |
| 53 | M4 | G08 | PAOS-0030 | Упаковка и пилот | 16 ч |
| 54 | OPTIONAL | G11 | PAOS-0047 | Опциональный Sign in with ChatGPT | 20 ч |
| 55 | T1 | G12 | PAOS-0052 | Командный профиль PostgreSQL и pgvector | 24 ч |
| 56 | T1 | G12 | PAOS-0053 | Перенос local проекта в team workspace | 16 ч |

PAOS-0002 проверяет domain contract только M1 profile (§17 PRD). Полный round-trip следующих типов/полей/вложений закреплён за M2 PAOS-0006/0031–0034/0038; 0050/0056 владеют фактическим переносом и cutover. PAOS-0036 завершается в M2, PAOS-0037 подключает цепочки агентов в M3. PAOS-0046 выполняется сразу после M1, а 0030 повторно проверяет коммерческие ограничения перед выпуском.

### Матрица M1 DoD и граница последующих этапов

| Acceptance | M1 coverage / обязательное доказательство | Owner tasks | Позднее |
| --- | --- | --- | --- |
| SW-AC-01/02/07/09/10 | Launch, pairing, account boundary, offline SQL, полный путь; real runtime + browser отдельно | 0040/0041/0044/0045 | SIWC 0047 |
| SW-AC-03/04/05/06/08 | Mode policy, approval answered_or_cleared, duplicate, Stop/crash, manual acceptance | 0042/0043/0044/0054/0055; verification 0045 | Custom recipes M3 |
| ST-AC-01/02 | SQLite/FTS5 restart/offline, atomic commands/conflicts | 0048/0049/0055; 0045 | Team T1 |
| ST-AC-03/04/05 | Профиль PRD §17.2, duplicate/source drift, staged export diff, crash cutover | 0050/0056; 0045 | Full hierarchy/attachments/import M2 |
| ST-AC-06/07 | Search purge/rebuild, consistent backup/restore, stale approvals/replay | 0049/0051/0056; 0045 | ST-AC-08 только T1 |
| UX-AC-01–05 | Shell/composer/links/history/scroll/draft; Task minimum | 0004/0041/0042/0043; 0045 | Full task editors не dependency |
| UX-AC-06/07/08/09 | Pinned role read-only, diff и checks, decision vs permission, pending/cleared/outcome | 0042/0043/0044; 0045 | Agent CRUD 0012+, workflow 0026+ |
| UX-AC-10–13 | Dedup/Stop/acceptance/project isolation | 0043/0044/0055; 0045 | Не зависит от 0008 |
| UX-AC-14 | Text/reference context; attachment upload unsupported объяснён до Send | 0043; 0045 | Actual uploads 0034/M2 |
| UX-AC-15 | RU/EN, обе темы, keyboard, 200% zoom, 320/1280/1440/1920 для M1 views | 0004/0043; 0045 | 0029 повторяет полный scope M4 |
| UX-AC-16 | Unknown/empty/partial, собственная сохранённая история и read-only catalogs; graph coverage | 0042/0043/0049; 0045 | Import всех сторонних chats/полная аналитика M2 |
| UX-AC-17/18 | API-key failure, preserved draft; одна active run, новый mode/profile только следующий binding | 0041/0042/0044; 0045 | SIWC/автономная очередь M3 |
| DATA-AC-01–03 | S29 preview/mapping/freeze/receipt; unsupported data и conflict не теряются | 0050/0056; 0045 | General merge editor M2 |
| DATA-AC-04/05 | S30 backup/restore/coverage; S31 FTS scopes/partial/purge | 0051/0049; 0045 | Semantic retrieval T1 |

Текущие receipts — раздел «Проверка очереди v0.8» ниже. [Аудит §9.2](product-agent-os-web-m1-final-audit-2026-11-10.md#92-текущие-проверки-согласования) сохраняет исторические проверки v0.7; это не evidence исполнения задач.

Группы/границы файлов — в карточках. Общими packages/contracts владеет 0054 owner до handoff; 0048 storage owner, 0055 domain bridge owner, 0042 runtime owner применяют только согласованный contract. Без перекрывающейся записи общих файлов. Документационная правка не запускает перечисленных агентов.

Re-entry gate: 0001 открыт для потребителей подтверждённого project binding. 2026-11-11 native MXC и именованный профиль подтвердили write/deny. По уточнению владельца локальная реализация storage/UI/domain продолжается с заблокированной активацией runtime до полного manifest. При отсутствии обязательной capability использовать design issue. [Наблюдения изолированных прогонов](product-agent-os-web-m1-initial-qualification-2026-11-10.md) отделены от runtime/browser/commercial приёмки.

### Проверка очереди v0.8

Source status: current-run local documentation checks, 2026-11-10. Task: PAOS-WEB-EXECUTION-ORDER-2026-11-10.

| Проверка | Наблюдаемый результат |
| --- | --- |
| python -m unittest tests.product_agent_os.test_product_agent_os_docs -v | Exit 0, 105 tests OK, 21.887 s; TEMP/TMP process-local .docs-tools/reports/web-task-manager/test-temp |
| python tools/check_docs.py | Exit 0, documentation structure checks passed |
| python plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-web-task-manager-plan-2026-11-09.md | Exit 0, ok=true, errors=[] |
| Inline Node consistency self-review | errors=[]; 56 unique tasks / 12 unchanged groups; order 1–56, stage arrays, MD table/cards and JSON agree; every dependency precedes dependent; technical DAG unchanged |
| Preservation and totals | Estimates, task statuses, actual timestamps/durations and affected_files unchanged; all planned/actual null. M1 18/234 h, post-M1 1/8 h, M2 26/338 h, M3 5/84 h, M4 3/52 h, optional 1/20 h, T1 2/40 h; total 56/776 h |
| Text/source checks | 60 local links resolve; UTF-8/fences valid; touched root files below 50 KiB; unrelated shared-file sections preserved |
| git diff --check | Exit 0; CRLF normalization warnings only |

Strict MkDocs not_applicable для этого slice: nav, Mermaid source, Markdown extensions, MkDocs config, search/sitemap и generated site evidence не менялись. Исторические site receipts не выдаются за текущую проверку. App/runtime/provider/browser проверки не выполнялись; schema_version JSON остаётся paos_web_task_groups_v1, execution_plan — additive planning metadata, не активированный scheduler.

Control-plane sync: PLAN/TEST/RUNLOG updated в собственных Web sections; registry RU/EN synchronized; PRD/architecture/auth stage pointers aligned. REQUIREMENTS not_applicable: действующий M1 profile не изменён, устранено расхождение карточки; EVALS/prod_test not_applicable: eval rubrics и production evidence не менялись. Overflow not_required. Чужие dirty changes сохранены, другие lifecycle markers не затрагивались.

Review: self_review; closure_level=docs_static_verified. Утверждён только порядок документационного плана. Никакие из 56 implementation tasks не запущены/не закрыты.

## Историческая очередь v0.6: storage и миграция

Source status: engines selected by user / schema and implementation plan proposed, 2026-11-09. Всего **53 planned tasks / 12 groups**. G12 добавляет PAOS-0048–0053. Старые численности и v0.4 receipts ниже — исторические; существующие PAOS-0001–0047 сохраняются, зависимости уточнены только у 0042/0043/0045. Выбор SQLite + FTS5 local и PostgreSQL + pgvector team принят; разработка не разрешена.

| Этап | Очередь и результат | Gate / ownership |
| --- | --- | --- |
| M1a storage foundation | 0001 → 0002 → 0003 → **0048**; UI 0004 и launcher/auth 0039–0041 параллельно только при независимой ownership | Architect/storage owner: logical schema, driver/FTS5 availability, transaction/outbox/revision, source adapters и authority gate |
| M1b single window | 0042 → 0043 → 0044 поверх 0048 | Runtime/frontend: session/task/run durable state; external ACK/recovery и secrets boundary прежние |
| M1c search and safe adoption | **0049**, **0050 → 0051**, затем **0045** с dependencies 0049/0050/0051 | Storage/tester: ST-AC-01–07, dry-run/cutover/restore, browser journey; no two masters. Минимальная новая session может проверяться до legacy import, но M1 acceptance ждёт migration gate |
| M2 full Task Manager | Прежние G02–G06/G09, 0035/0038, 0027 | Domain owners расширяют schema через migrations; не создают альтернативный task storage |
| M3 autonomy | Прежние G07, 0036/0037 | Pinned workflow/recipe/profile versions; один coordinator |
| M4 local acceptance/release | Прежние G08 и 0046, optional 0047 отдельно | Local backup/restore и commercial gates; T1 не является dependency |
| T1 team edition — future | **0052 → 0053** после отдельного team design/start scope | PostgreSQL/pgvector, hosting/auth/RBAC/runtime placement, explicit export/import handover; no offline bidirectional sync |

G12 ownership: 0048 владеет storage repository/migrations; 0049 — search; 0050/0053 — import/export (последовательно); 0051 — backup; 0052 — server profile. Новые proposed app paths не создаются этим документом. Общие schema/contracts записывает один назначенный owner; runtime/domain/UI consumers изменяют их через согласованный contract. Старые 0042/0043 больше не выбирают собственный persistence engine.

Дополнительные оценки: local G12 60 engineering hours (16+12+20+12), team 40 (24+16). Это rough estimates для планирования, не календарное обещание и не полная стоимость team edition: hosting/RBAC/remote runtime и production operations требуют уточнения до старта. Actual у всех 53 задач null. Этапы не суммируются механически при пересекающейся domain работе.

Трассировка: 0048 → ST-01–04/09; 0049 → ST-06/12; 0050 → ST-02/03/07; 0051 → ST-08/12; 0052 → ST-10; 0053 → ST-11. ST-05 закрывается 0042/0043/0044 и существующими session tasks с новым persistence. Schema/authority — [архитектура §20](product-agent-os-web-architecture-2026-11-05.md#20-хранение-схема-и-миграция--v06), product acceptance — [PRD §16](product-agent-os-web-prd-2026-11-05.md#16-хранение-и-перенос-данных--v06).

Rollback будущей реализации: backup до schema/cutover, no blind downgrade, post-cutover deltas reconcile; source/DB switch только по authority_epoch. Rollback текущего authoring — собственные изменения документов/planning metadata, без отмены чужих hunks. REQUIREMENTS/PLAN/TEST/RUNLOG и source registries получают compact pointers; EVALS и prod_test not_applicable: рубрики/исторические проверки не меняются.

### Проверка storage contract v0.6

Owning task: PAOS-WEB-STORAGE-CONTRACT-2026-11-09. Только documentation/planning metadata; engines selected, schema proposed; app/DB/runtime не реализованы.

| Проверка текущего запуска | Результат |
| --- | --- |
| `python plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-web-task-manager-plan-2026-11-09.md` | Exit 0, ok=true, errors=[] |
| `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | Exit 0, 105 tests OK, 14.313 s; TEMP/TMP process-local: .docs-tools/reports/web-task-manager/test-temp |
| `python tools/check_docs.py` | Exit 0; documentation structure checks passed |
| `git diff --check` | Exit 0; CRLF normalization warnings без whitespace errors |
| Inline Node consistency check | errors=[]; 53 unique tasks / 12 groups, dependency DAG и reverse Blocks согласованы; original 47 task payloads сохранены, кроме depends_on у 0042/0043/0045; все planned/actual=null; 56 local links существуют, 13 Mermaid sources в трёх основных документах, fences/UTF-8 checked |
| `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/web-storage-contract/site` | Exit 1: Aborted with 10 warnings in strict mode. G6/G7 research/JSON links в coding-standards, control-plane-current-state и registry RU/EN вне docs index; вне собственных storage additions. Общий worktree меняется параллельно, предыдущий receipt с 8 warnings не выдается за текущий |
| Explicit self-review | Уточнены original ADR-W03 и legacy authority §6/§17/§19; историческая v0.4 очередь помечена; source drift, rollback deltas, SQL/file/blob/runtime ownership, delayed search/delete и team isolation рассмотрены. Independent review не проводился |

Control-plane sync: REQUIREMENTS/PLAN/TEST/RUNLOG обновлены; старые собственные Web summary blocks REQUIREMENTS сжаты в v0.6 pointer, owning detail/history сохранены в PRD/UX/плане. Все root control-plane files <51200 bytes на проверенном snapshot (REQUIREMENTS 50503 bytes). EVALS not_applicable: rubric/threshold/accepted-gap policy не менялись; prod_test not_applicable: исторический Batch 39 не затрагивался. Registry RU/EN синхронизированы, research помечен subsequent selected decision. Handoff_required: владельцы G6/G7 source links для общего strict-build gate; это не accepted gap.

Source checks: official SQLite FK/FTS5, PostgreSQL RLS и pgvector перечитаны; WAL/backup evidence взято из предыдущего исследования с его provenance. Research Mermaid не рендерились в browser; Markdown схемы не доказывают работающую DB. Windows packaging, migration/restore, нагрузка, retrieval quality, team authorization и реальные runtime проверки pending. Начальный marker bootstrap исправлен по действующему own-session contract с scope_note_shown; hooks и чужие markers не менялись.

Closure: documentation_updated / partially_verified из-за общего strict site gate; engine_decision_selected, schema_proposed, implementation_not_started. Rollback только собственных docs/planning edits, без Git history операций.


## UX v0.5: детализация сессий — 2026-11-09

Source status: project-authored / proposed UX. [Wireframes WF-01–16](product-agent-os-web-m1-wireframes-2026-11-09.md) и [каталог S01–S28](product-agent-os-web-task-manager-screens-2026-11-09.md) — текущая структура интерфейса. UX-AC-01–18 в §13 wireframes расширяют acceptance существующих задач; tasks, estimates и dependencies JSON не изменяются.

| Работы | Существующие задачи | Результат будущего исполнения |
| --- | --- | --- |
| Shell, catalog, composer, task context, diff | PAOS-0004, PAOS-0010, PAOS-0043 | WF-01–07/12, сохранение draft/scroll/selection |
| Profile/skill provenance в сессии | PAOS-0012, PAOS-0015, PAOS-0042 | WF-06, различение профиля, assignment и run |
| Permissions, ACK, interruption, recovery | PAOS-0026, PAOS-0042–0044 | WF-08/09/11, один ответ и явный unknown outcome |
| Результат, checks, responsive/a11y | PAOS-0008, PAOS-0029, PAOS-0045 | WF-10/12, acceptance без ложного Done |
| Полные задачи, каталоги, карта, workflow | Существующие G02–G10 по очереди ниже | WF-13–16 и S25/S26; не задерживают минимальный M1 |

В M1 отдельный agent stop, fork, все типы attachments и импорт внешней истории не обещаются без capability. Исторический read-only M1 теперь архивное приложение wireframes. Все UX сценарии pending execution; документационные проверки и независимый Hallmark review записываются в §14 wireframes. Rollback текущего authoring — только собственные добавления/замены, сохраняя старые тексты и чужие hunks.

## Историческая очередь v0.4: единое окно

Source status: user-selected direction / proposed implementation, 2026-11-09. Этот раздел заменяет очередность TM0–TM4 v0.3; старые receipts и stage descriptions ниже исторические. Все 47 задач в 11 группах planned; разработка не начиналась. G11 добавляет PAOS-0039–0047. [PRD SW-01–12](product-agent-os-web-prd-2026-11-05.md#15-единое-окно-и-codex-app-server--v04) и [AUTH-G1–G6](product-agent-os-web-auth-commercial-2026-11-09.md) — owning acceptance.

| Этап | Задачи / результат | Gate и владелец |
| --- | --- | --- |
| M1a — контракты и launch | PAOS-0001–0004, PAOS-0039/0040: project/task/events, locale, route decision и launcher | Architect/product: source authority, runtime version, startup и auth route выбраны; runtime trial только при отдельном разрешении |
| M1b — рабочая сессия | PAOS-0041–0044: connection, Codex adapter, composer/minimal task, approvals и recovery | Runtime/frontend/tester: один полный путь без Codex App; нет secrets leakage, duplicate runs или неявного fallback |
| M1c — проверка | PAOS-0045: SW-AC-01–10, локальный режим, browser и реальный runtime | Tester/owner: fixture доказательства отдельно от actual run; no-go при потерянном outcome/authority |
| M2 — полный Task Manager | G02–G06, G09, PAOS-0035/0038 и PAOS-0027 с их dependencies | Tasks, полные сессии/поиск, agents/skills, graph, hierarchy, Kanban, attachments/links; прежний scope сохранён |
| M3 — автономность и workflows | PAOS-0036/0037, G07; зависимости catalogs/links из M2 | Coordinator M1 расширяется, не создаётся второй runner; budgets/ownership/recipe versioning |
| M4 — full acceptance / выпуск | PAOS-0028–0030 и PAOS-0046 | Полный UX, a11y, install/update/restore, pilot, коммерческие gates; публикация отдельно разрешается |
| Опциональный SIWC | PAOS-0047 после admission и зависимостей | Не блокирует API-M1/API-only выпуск; без admission planned/unavailable, а не implicitly accepted |

Критический путь M1: PAOS-0001 → PAOS-0039/0040 → PAOS-0041 → PAOS-0042 → PAOS-0043 → PAOS-0044 → PAOS-0045; PAOS-0002/0003/0004 — обязательные входы. Порядок nominal IDs не является execution order. PAOS-0043 владеет минимальной task/session UI; PAOS-0005–0011 расширяют её позднее. Поэтому первый chat не ждёт полного board, graph, workflow editor и agent/skill CRUD.

G11 ownership: runtime owner — adapters/coordinator/connection; frontend — session/settings/recovery; product/security — коммерческий route; tester — crash/auth/browser/live acceptance. Один writer на общие contracts. Предлагаемые paths проверяются при discovery; каталоги приложения сейчас не создаются.

Изменены зависимости PAOS-0010 → PAOS-0043, PAOS-0025 → PAOS-0044, PAOS-0028 → PAOS-0045, PAOS-0030 → PAOS-0046. Остальные 38 task IDs и scope сохранены; обратные Blocks вычислены из Depends on. PAOS-0025 расширяет recovery M1 до autonomous queue, а не заменяет его.

Оценки новых карточек — rough engineering hours без ожидания OpenAI admission, юридического review и пользователей; не обещание календарного срока. Actual всех карточек null. Оценки группы не суммируются в обещание срока релиза.

Rollback проектируемой реализации: прекратить новые dispatch, согласовать active runs, сохранить journal/profile/source revisions; откат build/schema только при совместимости. Для текущей документации — отменить лишь свои hunks/новый auth документ, сохранить прежние receipts/изображения и чужие изменения.

### Проверка текущей документационной задачи

PAOS-WEB-SINGLE-WINDOW-2026-11-09: scope — документация и planning metadata. Принято направление single-window, детали реализации и commercial eligibility не подтверждены. Результаты текущего запуска записаны ниже; runtime/provider/browser acceptance не выполняется в этом scope.

| Проверка в этом запуске | Результат |
| --- | --- |
| `python plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-web-task-manager-plan-2026-11-09.md` | Exit 0; ok=true, errors=[] |
| `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | Exit 0; 105 tests OK, 7.637 s; process-local TEMP/TMP указывали на workspace .docs-tools/reports/web-task-manager/test-temp |
| `python tools/check_docs.py` | Exit 0; documentation structure checks passed |
| Inline `python -` artifact check | Exit 0; 47 unique tasks / 11 groups, DAG и обратные Blocks; все actual null; исходные payloads 38 задач сохранены кроме явно изменённых dependencies; 69 local links, 10 Mermaid fences, SW/AC/auth parity и root files <50 KiB |
| `git diff --check` | Exit 0 на проверенном общем worktree; CRLF normalization warnings без whitespace errors |
| `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/web-task-manager/site-v04` | Exit 1; Aborted with 6 warnings in strict mode. Четыре G7 research links в coding-standards.en.md/registry.en.md вне docs_dir и две G6 JSON links в control-plane-current-state.en.md/registry.en.md не попали в documentation index. Все шесть относятся к ранее существовавшим разделам; новые Web registry entries используют source-path notation |
| Official source review | Девять WEB-AUTH источников прочитаны; API/identity/plan usage и commercial admission разделены. Никаких live credentials/inference checks |
| Self-review | Проверены новый M1 dependency path, preserved TM-01–24, single coordinator, project/account isolation, process-bound approvals, lost ACK, local/remote и auth/billing boundaries; independent review не проводился |

Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG обновлены компактными собственными pointers; registries RU/EN синхронизированы. prod_test not_applicable — исторический Batch 39 не затрагивался. Handoff_required: владельцы G6/G7 documentation исправляют шесть общих strict-build links; это не accepted gap и не основание заявлять общий docs-ready. Research diagrams проверены как source/fences, не rendered browser evidence.

Closure ceiling: documentation_updated / partially_verified. Запрошенное содержание сохранено; strict site gate остаётся failed вне Web hunks. Commercial AUTH-G1–G6 pending; PAOS-0047 требует admission. Runtime, UI, provider, OAuth registration, установка и Git/publication не выполнялись. Новые сквозные требования не означают доказанный продукт.

Собственный marker: SessionStart session_id проверен SHA256; после отказа auto-review повторное рассмотрение с доказательством принадлежности разрешило только переход к новой документационной задаче. Чужие markers и hooks не редактировались. Предыдущий closure сохранён. Это reporting metadata, не runtime/product evidence.


## Протокол документационной задачи PAOS-WEB-TASK-MANAGER-2026-11-09

Это evidence подготовки документов и изображений. Не является Completion Report ни одной будущей карточки PAOS-0001–0030. Все implementation statuses остаются planned.

| Проверка текущего запуска | Наблюдаемый результат |
| --- | --- |
| `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | Exit 0; 100 tests, OK |
| `python tools/check_docs.py` | Exit 0; documentation structure checks passed |
| `python plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-web-task-manager-plan-2026-11-09.md` | Exit 0; ok=true, errors=[] |
| `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/web-task-manager/site` | Exit 0 после исправления research pointers; Documentation built in 16.28 seconds. Research pages вне docs_dir не становятся опубликованными страницами; Mermaid source проверен чтением, browser rendering не проверен |
| `git diff --check` | Exit 0 после удаления добавленных пустых строк в конце трёх Web MD; CRLF warnings не являются whitespace errors |
| `python -`, bounded inline artifact checker | 30 уникальных IDs, 8 групп без пропусков, полный набор полей, все planned/actual=null, DAG без циклов, TM-01–14, 24 экрана, local links/UTF-8 и шесть PNG прошли |
| Hallmark finish review | separate_fresh_context, agent hallmark_review; verdict fix; один пакет исправлений пяти листов; последующий self-review корневого агента по returned images |
| Изображения | 6 PNG, 24 композиции, 1536×1024 каждый; final hashes в assets/task-manager-2026-11-09/manifest.json |

Первый запуск task-matrix validator отверг Markdown bold вокруг имён полей; приведено к каноническому формату. Первый strict MkDocs остановился на четырёх EN registry ссылках за docs_dir; заменены на source-path notation в обоих реестрах. Это исправления документации; validators/hooks не ослаблялись.

Review исправления: read-only discovery S02; единый основной пример PAOS-0001; agent IDs вместо придуманных людей; список/доска и вкладки task; честный coverage сессии; proposal vs apply; незаполненная policy не разрешает запуск; тёмная EN Settings соответствует выбранной теме. Адаптация Rim названа явно.

Остаточные visual gaps: image generation допускает неточные мелкие labels, gloss и отличия secondary fixtures между листами; в S18 рисунок не является нормативной схемой symbol identity (повторяющийся label status не задаёт два реальных символа). Использовать контракт graph из архитектуры и данные плана, а не считывать seed data из картинок. Mobile/keyboard/error/loading layouts описаны текстом, но отдельные изображения этих состояний не изготовлены. Все 24 основные экранные композиции присутствуют. pixel-perfect/contrast/a11y/render acceptance не заявляется.

Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG updated только собственными компактными pointers; source registry RU/EN updated. prod_test not_applicable (историческая серия не затронута). Другие PAOS-AUD изменения сохранены. Все пять root control-plane файлов остаются в пределах 50 KiB. Application source, runtime/host configuration, hooks, provider connections, Git history и публикация вне scope.

Итог подготовки: docs_static_verified; визуальный пакет draft_for_review / needs_user_acceptance; implementation not_started. Следующий шаг — выбрать/скорректировать визуальное направление и отдельно разрешить первую группу реализации. Архитектурные integration gaps относятся к PAOS-0001.

## Этапы и группы

## Проверка расширения v0.3 — PAOS-WEB-ISSUE-WORKFLOWS-2026-11-09

Source status: current-run local evidence. Это проверка документов, не реализация PAOS-0001–0038. Previous v0.2 receipts выше остаются историческими.

| Проверка | Наблюдаемый результат текущего запуска |
| --- | --- |
| `python plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-web-task-manager-plan-2026-11-09.md` | Exit 0; ok=true; errors=[] |
| `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | 105 tests, OK, exit 0 при process-local TEMP/TMP = workspace .docs-tools/reports/web-task-manager/test-temp |
| Первоначальный docs unittest | 105 tests, 5 errors: sandbox temporary directory PermissionError; после переноса TEMP/TMP в writable workspace повтор прошёл. Код/права ОС/тесты не менялись |
| `python tools/check_docs.py` | Exit 0; documentation structure checks passed |
| Bounded inline `python -` consistency check | 38 уникальных карточек, 10 групп, DAG, reverse Blocks, JSON/MD fields, TM-01–24, 11 components, 8 statuses, local links/UTF-8, root budget; все actual values null; PNG hashes прежние |
| `git diff --check` | Промежуточный exit 0 после исправления своего EOF; финальный общий запуск exit 2 на новом чужом EOF в research/product-agent-os-audit-remediation-task-plan-2026-11-09.md:2197. Scoped запуск с 12 собственными docs paths: exit 0; чужой план не исправлялся |
| `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/web-task-manager/site-v03` | **Exit 1**: два warnings в прежних G6 разделах docs/product-agent-os/control-plane-current-state.en.md и docs/sources/registry.en.md; ссылка ../superpowers/specs/paos-aud-g6-pilot-results.json не найдена среди documentation files. Сам файл существует; причина его отсутствия в build index в этом scope не исправлялась |
| Source review | 13 официальных Atlassian reference pages; facts отделены от PAOS proposals в PRD §14. Community/API assumptions не использованы |
| Self-review | Проверены hierarchy vs links, affects vs fix, status vs resolution, creator vs initiator, manual completion, cancellation receipt, workflow pinning/migration, dependency cycles, comments/history и attachment boundaries |

Изменённые owning artifacts: PRD §14, plan/JSON, architecture §18, UX v0.3 impact; компактные собственные sections REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG и registry RU/EN. Прежние 24 image concepts сохранены; S25/S26 описаны текстом, итог — 26 routes. Sources/metadata поддерживают proposed поведение; browser/runtime/provider evidence не выполнялись.

Control-plane sync: пять root files update_required и обновлены в своём scope; prod_test not_applicable; source registries RU/EN updated. Root files <50 KiB на момент проверки. Handoff_required: владелец PAOS-AUD-G6 должен устранить два существовавших G6 link warnings; наша задача не переписывает его разделы. Незакрытый strict-build gate не объявлен accepted gap и не скрыт.

Completion ceiling: **documentation_updated / partially_verified**. Requested content сохранён; документационные unit/structure/plan/consistency checks passed; общий strict build остаётся failed по указанным внешним для slice ссылкам. Реализация Web not_started; все 38 implementation tasks planned. Product/domain owner acceptance и runtime проверки будущие. Общий requirements_ready/plan_ready/release-ready не заявляется.


### Историческая очередь v0.3

Актуализация v0.3: 38 задач, 10 групп. Исходные PAOS-0001–0030 сохранены; PAOS-0031–0038 добавляют Jira-informed issue model. Предыдущий протокол выше относится к пакету v0.2 и не является проверкой этого расширения.

| Группа | Содержание | Задачи |
| --- | --- | --- |
| G01 | Основа и контракты | PAOS-0001, PAOS-0002, PAOS-0003, PAOS-0004 |
| G02 | Задачи | PAOS-0005, PAOS-0006, PAOS-0007, PAOS-0008 |
| G03 | Сессии | PAOS-0009, PAOS-0010, PAOS-0011 |
| G04 | Агенты | PAOS-0012, PAOS-0013, PAOS-0014, PAOS-0015 |
| G05 | Скиллы | PAOS-0016, PAOS-0017, PAOS-0018, PAOS-0019 |
| G06 | Карта проекта | PAOS-0020, PAOS-0021, PAOS-0022 |
| G07 | Автономная работа | PAOS-0023, PAOS-0024, PAOS-0025, PAOS-0026 |
| G08 | Общие поверхности и пилот | PAOS-0027, PAOS-0028, PAOS-0029, PAOS-0030 |
| G09 | Иерархия, поля и контекст | PAOS-0031, PAOS-0032, PAOS-0033, PAOS-0034 |
| G10 | Kanban, workflow и взаимозависимости | PAOS-0035, PAOS-0036, PAOS-0037, PAOS-0038 |

TM0: G01 и контракты PAOS-0031/0032. TM1: основной UI G02–G06, контекст/версии G09, Kanban PAOS-0035 и документы PAOS-0027. TM2: управляемые agent/skill changes, editor/versioning workflow PAOS-0036. TM3: execution recipes PAOS-0037, links PAOS-0038 и автономность G07. TM4: G08 проверяет весь путь и пилот. Это roadmap; индивидуальные Depends on имеют приоритет над порядком номеров и групп.

Shared contracts: один writer. Иерархия/поля G09 публикуют contract до потребляющего UI; recipes/links G10 до scheduler G07; G08 принимает итоговый контракт. Предлагаемые apps/web, apps/local-service, packages/contracts не означают существующие файлы. PAOS-0001 уточняет точки интеграции до кода.

Оценки — предварительные часы инженерной работы, не календарное обещание и не измеренная скорость AI. Обновлены оценки PAOS-0002/0005/0006/0008/0028 из-за нового scope; прежние версии сохраняются Git/source history. Actual timestamps/duration всех задач null. Development not_started. Ни одна карточка не разрешает внешние вызовы, установку или публикацию.

Изменение scope: PRD §14 — источник требований TM-15–TM-24; G01/G02/G07/G08 адаптированы, G09/G10 добавлены. Статусы карточек плана planned не мигрируют в пользовательский Kanban. В JSON issue_model_proposal — предложение будущей модели, не активная runtime schema. Неизвестные legacy creators/dates/versions не выдумываются.

Rollback будущих изменений: versioned proposal, revision check, migration preview и сохранение источника. Rollback текущих документов — только hunks этого scope, без потери предыдущих концептов и чужих изменений.

## Проверка плана и условия старта

Документы проверяются существующими docs gates и validate_task_matrix.py. Для будущей реализации каждая карточка требует source discovery, подтверждения файлов, executable acceptance tests и доступности зависимостей. Команды build/E2E фиксируются в PAOS-0001 после выбора scaffolding; сейчас plan_ready для разработки не заявляется. Rollback будущих записей: versioned proposal, source revision check, сохранение предыдущей версии; rollback документации — только изменения этого scope.


### Task `PAOS-0001`

- Task: Контракты и адаптеры проекта
- Status: implemented
- Delivery stage: M1
- Execution order: 1
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 23:01
- Depends on: none
- Blocks: PAOS-0002, PAOS-0004, PAOS-0009, PAOS-0016, PAOS-0020, PAOS-0039, PAOS-0040, PAOS-0048, PAOS-0054
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Установить доступность источников и API установленного host; определить project binding и coverage
- Technical value: Установить доступность источников и API установленного host; определить project binding и coverage
- Product value: Пользователь сразу видит, какие сведения проекта доступны, и не принимает неполную историю за полную.
- Scope: apps/local-service/src/adapters; packages/contracts
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Контракты и адаптеры проекта доступна в соответствующем этапе
- Acceptance criteria: Подключённый проект показывает доступные и отсутствующие источники; чужой проект исключён
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 08:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/adapters; packages/contracts
- Next step: Передать contract разрешённым потребителям M1; runtime transport и UI интегрируются задачами 0042/0043.
- Actual time: старт 10-11-2026 22:15 MSK, приёмка среза 10-11-2026 23:01 MSK. Активная длительность по отдельным прогонам не измерена.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: implemented
- What was done: Реализованы registry binding, инвентаризация и частичный coverage через scoped `thread/list`. Адаптер отклоняет чужие строки независимо от host-фильтра.
- Files touched / work locations: `packages/contracts/project.ts`, `apps/local-service/src/adapters/project-sources.ts`, `tests/web/project-sources.test.mts`.
- Technical value delivered: Сервис проверяет canonical root и identity каталога, затем возвращает относительный coverage.
- Product value delivered: Контракт различает отсутствующий источник, исключённую ссылку и неподключённую runtime history.
- Actual implementation date and time: 10-11-2026 23:01
- Verification evidence: 3/3 scoped adapter tests. App Server вернул 1/1/0/2 для Alpha/Beta/Empty/All по synthetic persisted CLI rollout; `thread/read` подтвердил persisted path и правильный cwd. [Детали](product-agent-os-web-m1-initial-qualification-2026-11-10.md).
- Residual risks: Только первая страница поддерживаемых persisted источников, статус partial. Свежая `vscode` сессия с пустым preview не отображается; UI и реальные профили отдельно.
- Follow-up: PAOS-0042 подключает transport, PAOS-0043/0045 проверяют UI и сквозной путь.

### Task `PAOS-0002`

- Task: Модель задачи и идентификаторы
- Status: implemented
- Delivery stage: M1
- Execution order: 4
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 23:06
- Depends on: PAOS-0001
- Blocks: PAOS-0003, PAOS-0005, PAOS-0006, PAOS-0031, PAOS-0042, PAOS-0045, PAOS-0048
- Source: PRD §17.1–17.2; M1 profile; execution plan v0.8
- Short description: Domain contract профиля M1: flat Task, поля PRD §17.1–17.2, стабильные ID и отдельные product/planning statuses
- Technical value: Типизированная модель M1 и проверяемый round-trip поддерживаемых полей без зависимости от полного Task Manager M2.
- Product value: Пользователь ставит полную задачу один раз и сохраняет устойчивую ссылку на неё при изменениях проекта.
- Scope: packages/contracts/tasks; apps/local-service/src/tasks
- Non-goals: Полная модель/round-trip M2, UI и фактический импорт; глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Модель задачи и идентификаторы доступна в соответствующем этапе
- Acceptance criteria: Round-trip domain contract покрывает только профиль M1 PRD §17.1–17.2: flat Task, исходные 12 полей, status/creator/priority/Start Date/Due Date и related/blocks references; UI и фактический импорт реализуются в owning tasks. UUID и project key стабильны; creator provenance, source IDs/status, planned/actual operations и null/unknown time сохраняются без выдумки; product workflow status не подменяет task_matrix_plan_v1 status. Contract fixtures отклоняют неподдерживаемые значимые поля/типы/связи без потери данных; импорт и authority switch отдельно проверяются в 0050/0056. Epic/Bug/UserStory/Sub-Task, components, versions и attachments не являются acceptance PAOS-0002; полный round-trip M2 принадлежит PAOS-0006/0031–0034/0038.
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: packages/contracts/tasks; apps/local-service/src/tasks
- Next step: Использовать M1 contract в учёте времени, затем в storage и импорте по зависимостям.
- Actual time: локальная проверка 10-11-2026 23:06 MSK; точное начало и активная длительность не измерены.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: implemented
- What was done: Реализован типизированный `m1_task_profile_v1` и его валидация и сериализация.
- Files touched / work locations: `packages/contracts/tasks/m1-task-profile.ts`, `apps/local-service/src/tasks/task-profile.ts`, `tests/web/task-profile.test.mts`.
- Technical value delivered: Round-trip сохраняет UUID, key, planning provenance, product status, дату, null actual time и поддерживаемые ссылки.
- Product value delivered: Экспорт сохраняет известные поля и явно отклоняет значимые данные вне M1 scope.
- Actual implementation date and time: 10-11-2026 23:06
- Verification evidence: `node --test tests/web/task-profile.test.mts` — exit 0, 3/3 после RED.
- Residual risks: Source mapping, выделение ID, проверка полного графа, SQL и UI принадлежат зависимым задачам.
- Follow-up: PAOS-0003 потребляет модель в собственном контракте времени; PAOS-0048/0050 подключают persistence и import.

### Task `PAOS-0003`

- Task: Время и журнал событий
- Status: implemented
- Delivery stage: M1
- Execution order: 5
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 10-11-2026 23:09
- Depends on: PAOS-0002
- Blocks: PAOS-0006, PAOS-0015, PAOS-0042, PAOS-0045, PAOS-0048
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Оценка до старта, идемпотентные интервалы и измерение факта
- Technical value: Оценка до старта, идемпотентные интервалы и измерение факта
- Product value: Пользователь сравнивает ожидаемое и затраченное время без двойного учёта параллельной работы.
- Scope: apps/local-service/src/events; packages/contracts/time
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Время и журнал событий доступна в соответствующем этапе
- Acceptance criteria: Повтор события не удваивает время; pause/retry/crash и параллельные агенты не искажают длительность
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/events; packages/contracts/time
- Next step: Подключить журнал к SQLite и runtime после соответствующих gates.
- Actual time: локальная проверка 10-11-2026 23:09 MSK; точное начало и активная длительность не измерены.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: implemented
- What was done: Реализованы scoped event receipts и детерминированная проекция времени с pause, retry, crash и reconciliation.
- Files touched / work locations: `packages/contracts/time/task-time.ts`, `apps/local-service/src/events/task-time.ts`, `tests/web/task-time.test.mts`.
- Technical value delivered: Повтор не удваивает интервалы; конфликт identity и чужая задача отклоняются. Неизвестное окончание после crash сохраняет `null`.
- Product value delivered: Длительность задачи считается по объединению подтверждённых интервалов; трудозатраты показываются отдельно по исполнителям.
- Actual implementation date and time: 10-11-2026 23:09
- Verification evidence: `node --test tests/web/task-profile.test.mts tests/web/task-time.test.mts` — exit 0, 6/6 после RED, из них 3 проекции времени.
- Residual risks: SQLite и фактический runtime ещё не подают события; проверка UI в следующих задачах.
- Follow-up: PAOS-0048/0042 подключают журнал и runtime; PAOS-0043/0045 проверяют представление.

### Task `PAOS-0004`

- Task: Темы и локализация
- Status: implemented
- Delivery stage: M1
- Execution order: 6
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 11:57
- Depends on: PAOS-0001
- Blocks: PAOS-0005, PAOS-0006, PAOS-0009, PAOS-0016, PAOS-0021, PAOS-0032, PAOS-0043
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Общие токены и RU/EN для всех экранов
- Technical value: Общие токены и RU/EN для всех экранов
- Product value: Пользователь работает на удобном языке и в выбранной теме без потери читаемости и действий.
- Scope: apps/web/src/design; apps/web/src/locales
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Темы и локализация доступна в соответствующем этапе
- Acceptance criteria: Переключатели сохраняют выбор; длинный EN/RU текст и обе темы не скрывают действия
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 08:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/web/src/design; apps/web/src/locales
- Next step: PAOS-0042/0043/0044 provider-backed gates, затем0045; повторный ручной launcher тест владельцем не требуется.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: implemented
- What was done: RU/EN, Light/Dark/System и persistence подтверждены browser667; исправлены mobile header overflow и accessible labels select.
- Files touched / work locations: apps/web/src/design/app.css; apps/web/src/ui/App.tsx; tests/web/single-window/browser-acceptance.mts
- Technical value delivered: Реальные browser geometry/hit/focus/contrast/native zoom checks подтверждают acceptance.
- Product value delivered: Длинный текст сохраняет доступность действий; выбор темы и языка переживает reload.
- Actual implementation date and time: 11-11-2026 11:57
- Verification evidence: Текущий follow-up: Web197/197 no skips; browser669; autonomous launcher56; strict/build35 exit0. Native BVldIt closed-App25 samples, source hashes совпадают; owner accepted=false сохранён. Это разные прогоны. [Execution report](product-agent-os-web-m1-execution-2026-11-11.md).
- Residual risks: Обязательных gaps PAOS-0004 не осталось; полный WCAG audit и provider/M1 acceptance не заявлены.
- Follow-up: PAOS-0040 technical implemented; далее0042/0043/0044 и0045.

### Task `PAOS-0005`

- Task: Список и доска задач
- Status: implemented
- Delivery stage: M2
- Execution order: 23
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 22:40
- Depends on: PAOS-0002, PAOS-0004, PAOS-0032
- Blocks: PAOS-0035
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Фильтры, группировка, сохранённый вид и доступная смена статуса
- Technical value: Фильтры, группировка, сохранённый вид и доступная смена статуса
- Product value: Пользователь быстро находит нужную работу и видит, на каком этапе находится каждая задача.
- Scope: apps/web/src/features/tasks/list; apps/web/src/features/tasks/board
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Список и доска задач доступна в соответствующем этапе
- Acceptance criteria: Список/Kanban согласованы; type/parent/creator/priority/components/versions/dates filters сохраняются; расширенные mappings и transitions проверяются в PAOS-0035
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 14:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/web/src/features/tasks/list; apps/web/src/features/tasks/board
- Next step: Следующий неисполненный M2 scope — PAOS-0036; он требует отдельной команды владельца.
- Actual time: общий cohort начат 11-11-2026 20:41 MSK; проверен 11-11-2026 22:40 MSK. Start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: apps/web/src/features/tasks/TaskManager.tsx; apps/web/src/features/tasks/model.ts; apps/web/src/design/app.css. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Default Tasks route содержит согласованные list/board, полный snapshot/count, filters/group/sort, сохранённый view, явную DOM pagination и keyboard controls.
- Files touched / work locations: apps/web/src/features/tasks/TaskManager.tsx; apps/web/src/features/tasks/model.ts; apps/web/src/design/app.css.
- Technical value delivered: Фильтры, группировка, сохранённый вид и доступная смена статуса; транзакционные guards и regression checks реализованы.
- Product value delivered: Пользователь быстро находит нужную работу и видит, на каком этапе находится каждая задача.
- Actual implementation date and time: 11-11-2026 22:40
- Verification evidence: full Web 345/345 skip0; browser 88; actual App/native 27; focused negative cases, build/typecheck и independent closed_allowed. [Run evidence](product-agent-os-web-m2-execution-2026-11-11.md), [source hashes/results](product-agent-os-web-m2-results-2026-11-11.json).
- Residual risks: local App-active technical scope; active consumer required, sandbox только PAOS-mediated commands. Human/commercial/release acceptance и AUTH-G1–G6 отдельно; narrow Markdown subset обозначен в UI.
- Follow-up: Остальные 16 M2 tasks, включая PAOS-0036, остаются planned; commercial repeat review PAOS-0030. Эта карточка не закрывает весь M2.

### Task `PAOS-0006`

- Task: Карточка и редактор задачи
- Status: implemented
- Delivery stage: M2
- Execution order: 24
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 22:40
- Depends on: PAOS-0002, PAOS-0003, PAOS-0004, PAOS-0032
- Blocks: PAOS-0007, PAOS-0008
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Полная постановка задачи и понятная техническая/продуктовая ценность
- Technical value: Полная постановка задачи и понятная техническая/продуктовая ценность
- Product value: Пользователь понимает пользу задачи, формулирует ожидаемый результат и управляет её выполнением.
- Scope: apps/web/src/features/tasks/detail; apps/web/src/features/tasks/editor
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Карточка и редактор задачи доступна в соответствующем этапе
- Acceptance criteria: Все поля §13–§14 доступны; пользователь создаёт draft сам; отдельные Comments/History/Attachments/Linked Issues подключаются через PAOS-0034/0038; Ready проверяет обязательные поля
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/web/src/features/tasks/detail; apps/web/src/features/tasks/editor
- Next step: Следующий неисполненный M2 scope — PAOS-0036; он требует отдельной команды владельца.
- Actual time: общий cohort начат 11-11-2026 20:41 MSK; проверен 11-11-2026 22:40 MSK. Start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: apps/web/src/features/tasks/Editor.tsx; apps/web/src/features/tasks/TaskManager.tsx; apps/web/src/api/client.ts. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Полный editor и отдельные tabs, самостоятельный draft, Ready validation, memory-only unsaved state, revision conflicts без потери ввода и reviewed structural preview.
- Files touched / work locations: apps/web/src/features/tasks/Editor.tsx; apps/web/src/features/tasks/TaskManager.tsx; apps/web/src/api/client.ts.
- Technical value delivered: Полная постановка задачи и понятная техническая/продуктовая ценность; транзакционные guards и regression checks реализованы.
- Product value delivered: Пользователь понимает пользу задачи, формулирует ожидаемый результат и управляет её выполнением.
- Actual implementation date and time: 11-11-2026 22:40
- Verification evidence: full Web 345/345 skip0; browser 88; actual App/native 27; focused negative cases, build/typecheck и independent closed_allowed. [Run evidence](product-agent-os-web-m2-execution-2026-11-11.md), [source hashes/results](product-agent-os-web-m2-results-2026-11-11.json).
- Residual risks: local App-active technical scope; active consumer required, sandbox только PAOS-mediated commands. Human/commercial/release acceptance и AUTH-G1–G6 отдельно; narrow Markdown subset обозначен в UI.
- Follow-up: Остальные 16 M2 tasks, включая PAOS-0036, остаются planned; commercial repeat review PAOS-0030. Эта карточка не закрывает весь M2.

### Task `PAOS-0007`

- Task: Файлы, артефакты и исполнители
- Status: implemented
- Delivery stage: M2
- Execution order: 25
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 22:40
- Depends on: PAOS-0006
- Blocks: PAOS-0008, PAOS-0010, PAOS-0012, PAOS-0022, PAOS-0027, PAOS-0034, PAOS-0038
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Связать планируемые/фактические изменения, агентские runs и доказательства
- Technical value: Связать планируемые/фактические изменения, агентские runs и доказательства
- Product value: Пользователь видит, кто и что изменит, и открывает подтверждающий документ из задачи.
- Scope: apps/local-service/src/task-links; apps/web/src/features/tasks/links
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Файлы, артефакты и исполнители доступна в соответствующем этапе
- Acceptance criteria: Создание/изменение/удаление различимы; ссылка открывает нужную версию и контекст
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 08:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/task-links; apps/web/src/features/tasks/links
- Next step: Следующий неисполненный M2 scope — PAOS-0036; он требует отдельной команды владельца.
- Actual time: общий cohort начат 11-11-2026 20:41 MSK; проверен 11-11-2026 22:40 MSK. Start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: apps/local-service/src/task-manager/service.mts; apps/web/src/features/tasks/Panels.tsx; apps/local-service/src/runtime/storage-ports.mts. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Planned/actual create/modify/delete/rename/read, pinned source hash/context, assignments/profile/run/session и artifacts/provenance; stale/unavailable не подменяется текущим source.
- Files touched / work locations: apps/local-service/src/task-manager/service.mts; apps/web/src/features/tasks/Panels.tsx; apps/local-service/src/runtime/storage-ports.mts.
- Technical value delivered: Связать планируемые/фактические изменения, агентские runs и доказательства; транзакционные guards и regression checks реализованы.
- Product value delivered: Пользователь видит, кто и что изменит, и открывает подтверждающий документ из задачи.
- Actual implementation date and time: 11-11-2026 22:40
- Verification evidence: full Web 345/345 skip0; browser 88; actual App/native 27; focused negative cases, build/typecheck и independent closed_allowed. [Run evidence](product-agent-os-web-m2-execution-2026-11-11.md), [source hashes/results](product-agent-os-web-m2-results-2026-11-11.json).
- Residual risks: local App-active technical scope; active consumer required, sandbox только PAOS-mediated commands. Human/commercial/release acceptance и AUTH-G1–G6 отдельно; narrow Markdown subset обозначен в UI.
- Follow-up: Остальные 16 M2 tasks, включая PAOS-0036, остаются planned; commercial repeat review PAOS-0030. Эта карточка не закрывает весь M2.

### Task `PAOS-0008`

- Task: Приёмка и жизненный цикл
- Status: implemented
- Delivery stage: M2
- Execution order: 26
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 22:40
- Depends on: PAOS-0006, PAOS-0007
- Blocks: PAOS-0023, PAOS-0027, PAOS-0035
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Проверки и решение пользователя определяют завершение
- Technical value: Проверки и решение пользователя определяют завершение
- Product value: Пользователь принимает результат по проверяемым условиям и видит незакрытые требования.
- Scope: apps/local-service/src/task-workflow; apps/web/src/features/tasks/acceptance
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Приёмка и жизненный цикл доступна в соответствующем этапе
- Acceptance criteria: Completion, cancellation и reopening различены; criteria/child/dependency gates и manual evidence определены; действия расширяются PAOS-0035
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 14:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/task-workflow; apps/web/src/features/tasks/acceptance
- Next step: Следующий неисполненный M2 scope — PAOS-0036; он требует отдельной команды владельца.
- Actual time: общий cohort начат 11-11-2026 20:41 MSK; проверен 11-11-2026 22:40 MSK. Start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: packages/contracts/issues/task-profile.ts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/tasks/Panels.tsx; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/runtime/live-gateway.mts. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Manual completion без agent run, evidence/children/dependencies/active-writer gates, cancellation/reopen и original actual start/history; model turn не выполняет automatic Done.
- Files touched / work locations: packages/contracts/issues/task-profile.ts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/tasks/Panels.tsx; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/runtime/live-gateway.mts.
- Technical value delivered: Проверки и решение пользователя определяют завершение; транзакционные guards и regression checks реализованы.
- Product value delivered: Пользователь принимает результат по проверяемым условиям и видит незакрытые требования.
- Actual implementation date and time: 11-11-2026 22:40
- Verification evidence: full Web 345/345 skip0; browser 88; actual App/native 27; focused negative cases, build/typecheck и independent closed_allowed. [Run evidence](product-agent-os-web-m2-execution-2026-11-11.md), [source hashes/results](product-agent-os-web-m2-results-2026-11-11.json).
- Residual risks: local App-active technical scope; active consumer required, sandbox только PAOS-mediated commands. Human/commercial/release acceptance и AUTH-G1–G6 отдельно; narrow Markdown subset обозначен в UI.
- Follow-up: Остальные 16 M2 tasks, включая PAOS-0036, остаются planned; commercial repeat review PAOS-0030. Эта карточка не закрывает весь M2.

### Task `PAOS-0009`

- Task: Каталог всех доступных сессий
- Status: implemented
- Delivery stage: M2
- Execution order: 31
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 09:53
- Depends on: PAOS-0001, PAOS-0004
- Blocks: PAOS-0010, PAOS-0012
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Постраничная история проекта с archived/fork/subagent связями
- Technical value: Постраничная история проекта с archived/fork/subagent связями
- Product value: Пользователь возвращается к любому доступному обсуждению проекта, включая архив и дочерние сессии.
- Scope: apps/local-service/src/sessions; apps/web/src/features/sessions/list
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Каталог всех доступных сессий доступна в соответствующем этапе
- Acceptance criteria: Нет потерь и дублей между страницами; coverage показан; недоступная история обозначена
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/sessions; apps/web/src/features/sessions/list
- Next step: Оставшиеся M2 PAOS-0019/0020/0021/0022/0027 требуют отдельного scope; весь M2 не закрыт.
- Actual time: Общий cohort baseline12-11-2026 08:29 MSK, проверен 12-11-2026 09:53 MSK; start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: apps/local-service/src/sessions/service.mts; packages/contracts/sessions/history.ts; apps/local-service/src/http/application.mts; apps/web/src/features/sessions/SessionsCatalog.tsx. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Project catalog with bounded frozen-snapshot cursors, filters/archive/source/coverage, concurrent insertion without loss/duplicates; unavailable host history explicit.
- Files touched / work locations: apps/local-service/src/sessions/service.mts; packages/contracts/sessions/history.ts; apps/local-service/src/http/application.mts; apps/web/src/features/sessions/SessionsCatalog.tsx.
- Technical value delivered: Постраничная история проекта с archived/fork/subagent связями; source contracts и guards проверены.
- Product value delivered: Пользователь возвращается к любому доступному обсуждению проекта, включая архив и дочерние сессии.
- Actual implementation date and time: 12-11-2026 09:53
- Verification evidence: Web375/375 skip0; browser51; actual App/native49; build/typecheck, negative-case regressions и independent source review + root closed_allowed. [Run evidence](product-agent-os-web-m2b-execution-2026-11-12.md), [results](product-agent-os-web-m2b-results-2026-11-12.json).
- Residual risks: Local App-active technical scope; consumer required. History partial for unavailable sources, cursor15min; native loadedVersion unknown, remote discovery unavailable; M3/human/commercial/release отдельно.
- Follow-up: M2 technical21/26; remaining PAOS-0019/0020/0021/0022/0027 planned. AUTH-G1–G6/PAOS-0030 и human/release не закрыты.

### Task `PAOS-0010`

- Task: Сообщения и переходы по контексту
- Status: implemented
- Delivery stage: M2
- Execution order: 32
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 09:53
- Depends on: PAOS-0007, PAOS-0009, PAOS-0043
- Blocks: PAOS-0011, PAOS-0015
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Полный доступный диалог с авторами, задачами и сообщениями агентов
- Technical value: Полный доступный диалог с авторами, задачами и сообщениями агентов
- Product value: Пользователь читает обсуждение целиком и переходит от сообщения к соответствующей задаче или файлу.
- Scope: apps/web/src/features/sessions/transcript; packages/contracts/messages
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Сообщения и переходы по контексту доступна в соответствующем этапе
- Acceptance criteria: Порядок событий стабилен; длинный диалог открывает выбранное сообщение; fork и агент различимы
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/web/src/features/sessions/transcript; packages/contracts/messages
- Next step: Оставшиеся M2 PAOS-0019/0020/0021/0022/0027 требуют отдельного scope; весь M2 не закрыт.
- Actual time: Общий cohort baseline12-11-2026 08:29 MSK, проверен 12-11-2026 09:53 MSK; start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: apps/local-service/src/sessions/service.mts; apps/web/src/features/sessions/SessionsCatalog.tsx; apps/web/src/ui/App.tsx; packages/contracts/sessions/history.ts. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Full available transcript with stable message IDs/order, anchor110 of120, permalink/reload and author/task/file/fork/agent context; existing composer preserved.
- Files touched / work locations: apps/local-service/src/sessions/service.mts; apps/web/src/features/sessions/SessionsCatalog.tsx; apps/web/src/ui/App.tsx; packages/contracts/sessions/history.ts.
- Technical value delivered: Полный доступный диалог с авторами, задачами и сообщениями агентов; source contracts и guards проверены.
- Product value delivered: Пользователь читает обсуждение целиком и переходит от сообщения к соответствующей задаче или файлу.
- Actual implementation date and time: 12-11-2026 09:53
- Verification evidence: Web375/375 skip0; browser51; actual App/native49; build/typecheck, negative-case regressions и independent source review + root closed_allowed. [Run evidence](product-agent-os-web-m2b-execution-2026-11-12.md), [results](product-agent-os-web-m2b-results-2026-11-12.json).
- Residual risks: Local App-active technical scope; consumer required. History partial for unavailable sources, cursor15min; native loadedVersion unknown, remote discovery unavailable; M3/human/commercial/release отдельно.
- Follow-up: M2 technical21/26; remaining PAOS-0019/0020/0021/0022/0027 planned. AUTH-G1–G6/PAOS-0030 и human/release не закрыты.

### Task `PAOS-0011`

- Task: Поиск, приватность и хранение сессий
- Status: implemented
- Delivery stage: M2
- Execution order: 33
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 09:53
- Depends on: PAOS-0010
- Blocks: PAOS-0025, PAOS-0027
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Искать историю без раскрытия секретов и чужих проектов
- Technical value: Искать историю без раскрытия секретов и чужих проектов
- Product value: Пользователь находит нужное сообщение без раскрытия чужих проектов и чувствительных данных.
- Scope: apps/local-service/src/session-search; apps/local-service/src/redaction
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Поиск, приватность и хранение сессий доступна в соответствующем этапе
- Acceptance criteria: Редакция секретов и project isolation подтверждены; пропуск/усечение и retention видимы
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 10:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/session-search; apps/local-service/src/redaction
- Next step: Оставшиеся M2 PAOS-0019/0020/0021/0022/0027 требуют отдельного scope; весь M2 не закрыт.
- Actual time: Общий cohort baseline12-11-2026 08:29 MSK, проверен 12-11-2026 09:53 MSK; start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: apps/local-service/src/redaction/persisted.mts; apps/local-service/src/sessions/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/web/src/features/sessions/SessionsCatalog.tsx. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Known secret-form redaction before storage/FTS/App claim and on legacy public reads; project isolation/hidden metadata guards, visible coverage/retention/truncation.
- Files touched / work locations: apps/local-service/src/redaction/persisted.mts; apps/local-service/src/sessions/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/web/src/features/sessions/SessionsCatalog.tsx.
- Technical value delivered: Искать историю без раскрытия секретов и чужих проектов; source contracts и guards проверены.
- Product value delivered: Пользователь находит нужное сообщение без раскрытия чужих проектов и чувствительных данных.
- Actual implementation date and time: 12-11-2026 09:53
- Verification evidence: Web375/375 skip0; browser51; actual App/native49; build/typecheck, negative-case regressions и independent source review + root closed_allowed. [Run evidence](product-agent-os-web-m2b-execution-2026-11-12.md), [results](product-agent-os-web-m2b-results-2026-11-12.json).
- Residual risks: Local App-active technical scope; consumer required. History partial for unavailable sources, cursor15min; native loadedVersion unknown, remote discovery unavailable; M3/human/commercial/release отдельно.
- Follow-up: M2 technical21/26; remaining PAOS-0019/0020/0021/0022/0027 planned. AUTH-G1–G6/PAOS-0030 и human/release не закрыты.

### Task `PAOS-0012`

- Task: Каталог и профиль агента
- Status: implemented
- Delivery stage: M2
- Execution order: 34
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 09:53
- Depends on: PAOS-0007, PAOS-0009
- Blocks: PAOS-0013, PAOS-0015, PAOS-0016
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Инструкции, источник, действующая версия и назначенные задачи
- Technical value: Инструкции, источник, действующая версия и назначенные задачи
- Product value: Пользователь понимает назначение каждого агента и инструкции, по которым он работает.
- Scope: apps/local-service/src/agents; apps/web/src/features/agents/catalog
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Каталог и профиль агента доступна в соответствующем этапе
- Acceptance criteria: Effective/proposed/loaded версии различимы; переход к task/run/session работает
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 08:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/agents; apps/web/src/features/agents/catalog
- Next step: Оставшиеся M2 PAOS-0019/0020/0021/0022/0027 требуют отдельного scope; весь M2 не закрыт.
- Actual time: Общий cohort baseline12-11-2026 08:29 MSK, проверен 12-11-2026 09:53 MSK; start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: packages/contracts/team/assets.ts; apps/local-service/src/team/service.mts; apps/local-service/src/http/application.mts; apps/web/src/features/team/TeamManager.tsx; apps/web/src/api/client.ts. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Metadata catalog and full scoped profile distinguish effective/proposed/native loaded/observed PAOS pins; specific run/task/session navigation works.
- Files touched / work locations: packages/contracts/team/assets.ts; apps/local-service/src/team/service.mts; apps/local-service/src/http/application.mts; apps/web/src/features/team/TeamManager.tsx; apps/web/src/api/client.ts.
- Technical value delivered: Инструкции, источник, действующая версия и назначенные задачи; source contracts и guards проверены.
- Product value delivered: Пользователь понимает назначение каждого агента и инструкции, по которым он работает.
- Actual implementation date and time: 12-11-2026 09:53
- Verification evidence: Web375/375 skip0; browser51; actual App/native49; build/typecheck, negative-case regressions и independent source review + root closed_allowed. [Run evidence](product-agent-os-web-m2b-execution-2026-11-12.md), [results](product-agent-os-web-m2b-results-2026-11-12.json).
- Residual risks: Local App-active technical scope; consumer required. History partial for unavailable sources, cursor15min; native loadedVersion unknown, remote discovery unavailable; M3/human/commercial/release отдельно.
- Follow-up: M2 technical21/26; remaining PAOS-0019/0020/0021/0022/0027 planned. AUTH-G1–G6/PAOS-0030 и human/release не закрыты.

### Task `PAOS-0013`

- Task: Создание, изменение и удаление агента
- Status: implemented
- Delivery stage: M2
- Execution order: 35
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 09:53
- Depends on: PAOS-0012
- Blocks: PAOS-0014, PAOS-0023
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Ручной CRUD с diff, проверкой, архивом и восстановлением
- Technical value: Ручной CRUD с diff, проверкой, архивом и восстановлением
- Product value: Пользователь меняет состав команды и инструкции с возможностью сравнения и восстановления.
- Scope: apps/local-service/src/agent-proposals; apps/web/src/features/agents/editor
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Создание, изменение и удаление агента доступна в соответствующем этапе
- Acceptance criteria: Конфликт версии отклоняется; активный run не меняется; удалённый агент остаётся в истории
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/agent-proposals; apps/web/src/features/agents/editor
- Next step: Оставшиеся M2 PAOS-0019/0020/0021/0022/0027 требуют отдельного scope; весь M2 не закрыт.
- Actual time: Общий cohort baseline12-11-2026 08:29 MSK, проверен 12-11-2026 09:53 MSK; start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: packages/contracts/team/assets.ts; apps/local-service/src/team/contract.mts; apps/local-service/src/team/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/team/TeamManager.tsx. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Managed create/update/archive/delete/restore proposals with semantic diff, CAS/idempotent Apply, immutable history/pins, dependency/cycle checks and exact retry after lostACK/auth recovery.
- Files touched / work locations: packages/contracts/team/assets.ts; apps/local-service/src/team/contract.mts; apps/local-service/src/team/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/team/TeamManager.tsx.
- Technical value delivered: Ручной CRUD с diff, проверкой, архивом и восстановлением; source contracts и guards проверены.
- Product value delivered: Пользователь меняет состав команды и инструкции с возможностью сравнения и восстановления.
- Actual implementation date and time: 12-11-2026 09:53
- Verification evidence: Web375/375 skip0; browser51; actual App/native49; build/typecheck, negative-case regressions и independent source review + root closed_allowed. [Run evidence](product-agent-os-web-m2b-execution-2026-11-12.md), [results](product-agent-os-web-m2b-results-2026-11-12.json).
- Residual risks: Local App-active technical scope; consumer required. History partial for unavailable sources, cursor15min; native loadedVersion unknown, remote discovery unavailable; M3/human/commercial/release отдельно.
- Follow-up: M2 technical21/26; remaining PAOS-0019/0020/0021/0022/0027 planned. AUTH-G1–G6/PAOS-0030 и human/release не закрыты.

### Task `PAOS-0014`

- Task: Управление агентом по описанию
- Status: implemented
- Delivery stage: M2
- Execution order: 36
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 09:53
- Depends on: PAOS-0013
- Blocks: none
- Source: PRD: дополнение Task Manager; screen specification
- Short description: По описанию создать, изменить или подготовить удаление агента через редактируемый proposal
- Technical value: Разобрать intent create/update/archive/delete, разрешить однозначный target и применить общий versioned proposal contract
- Product value: Пользователь описывает нужное изменение команды обычным языком и проверяет последствия до применения.
- Scope: apps/local-service/src/agent-generation; apps/web/src/features/agents/generator
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Генерация агента по описанию доступна в соответствующем этапе
- Acceptance criteria: Create/update/delete intent создаёт draft; target и diff видны; неоднозначное имя требует уточнения; active run и history не удаляются молча
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 10:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/agent-generation; apps/web/src/features/agents/generator
- Next step: Оставшиеся M2 PAOS-0019/0020/0021/0022/0027 требуют отдельного scope; весь M2 не закрыт.
- Actual time: Общий cohort baseline12-11-2026 08:29 MSK, проверен 12-11-2026 09:53 MSK; start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: apps/local-service/src/team/generation.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/web/src/features/team/TeamManager.tsx. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Actual App planning create/update/delete intent yields strict editable proposals and separate Apply; exact target/clarification, no silent history deletion/provider fallback.
- Files touched / work locations: apps/local-service/src/team/generation.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/web/src/features/team/TeamManager.tsx.
- Technical value delivered: Разобрать intent create/update/archive/delete, разрешить однозначный target и применить общий versioned proposal contract; source contracts и guards проверены.
- Product value delivered: Пользователь описывает нужное изменение команды обычным языком и проверяет последствия до применения.
- Actual implementation date and time: 12-11-2026 09:53
- Verification evidence: Web375/375 skip0; browser51; actual App/native49; build/typecheck, negative-case regressions и independent source review + root closed_allowed. [Run evidence](product-agent-os-web-m2b-execution-2026-11-12.md), [results](product-agent-os-web-m2b-results-2026-11-12.json).
- Residual risks: Local App-active technical scope; consumer required. History partial for unavailable sources, cursor15min; native loadedVersion unknown, remote discovery unavailable; M3/human/commercial/release отдельно.
- Follow-up: M2 technical21/26; remaining PAOS-0019/0020/0021/0022/0027 planned. AUTH-G1–G6/PAOS-0030 и human/release не закрыты.

### Task `PAOS-0015`

- Task: Назначения и статистика агентов
- Status: implemented
- Delivery stage: M2
- Execution order: 37
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 09:53
- Depends on: PAOS-0003, PAOS-0010, PAOS-0012
- Blocks: PAOS-0024
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Наблюдать частоту, исходы, активные и прошлые задачи
- Technical value: Наблюдать частоту, исходы, активные и прошлые задачи
- Product value: Пользователь видит, как часто агент применяется, над чем работает и чем закончились его задачи.
- Scope: apps/local-service/src/agent-metrics; apps/web/src/features/agents/activity
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Назначения и статистика агентов доступна в соответствующем этапе
- Acceptance criteria: Метрики имеют период, знаменатель и coverage; отсутствующие данные не превращаются в нули
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/agent-metrics; apps/web/src/features/agents/activity
- Next step: Оставшиеся M2 PAOS-0019/0020/0021/0022/0027 требуют отдельного scope; весь M2 не закрыт.
- Actual time: Общий cohort baseline12-11-2026 08:29 MSK, проверен 12-11-2026 09:53 MSK; start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: apps/local-service/src/team/service.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/web/src/features/team/TeamManager.tsx. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Unique observed starts and outcomes/accepted tasks have period, denominator, source and coverage; missing duration/token/cost remain null, custom workflow categories supported.
- Files touched / work locations: apps/local-service/src/team/service.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/web/src/features/team/TeamManager.tsx.
- Technical value delivered: Наблюдать частоту, исходы, активные и прошлые задачи; source contracts и guards проверены.
- Product value delivered: Пользователь видит, как часто агент применяется, над чем работает и чем закончились его задачи.
- Actual implementation date and time: 12-11-2026 09:53
- Verification evidence: Web375/375 skip0; browser51; actual App/native49; build/typecheck, negative-case regressions и independent source review + root closed_allowed. [Run evidence](product-agent-os-web-m2b-execution-2026-11-12.md), [results](product-agent-os-web-m2b-results-2026-11-12.json).
- Residual risks: Local App-active technical scope; consumer required. History partial for unavailable sources, cursor15min; native loadedVersion unknown, remote discovery unavailable; M3/human/commercial/release отдельно.
- Follow-up: M2 technical21/26; remaining PAOS-0019/0020/0021/0022/0027 planned. AUTH-G1–G6/PAOS-0030 и human/release не закрыты.

### Task `PAOS-0016`

- Task: Каталог и профиль скилла
- Status: implemented
- Delivery stage: M2
- Execution order: 38
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 09:53
- Depends on: PAOS-0001, PAOS-0004, PAOS-0012
- Blocks: PAOS-0017
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Показать назначение, источник, версию, зависимости и использование
- Technical value: Показать назначение, источник, версию, зависимости и использование
- Product value: Пользователь находит доступные навыки и понимает, какие агенты их используют.
- Scope: apps/local-service/src/skills; apps/web/src/features/skills/catalog
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Каталог и профиль скилла доступна в соответствующем этапе
- Acceptance criteria: Project/global/vendor scopes различимы; effective версия и связь с агентами доступны
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 08:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/skills; apps/web/src/features/skills/catalog
- Next step: Оставшиеся M2 PAOS-0019/0020/0021/0022/0027 требуют отдельного scope; весь M2 не закрыт.
- Actual time: Общий cohort baseline12-11-2026 08:29 MSK, проверен 12-11-2026 09:53 MSK; start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: apps/local-service/src/team/sources.mts; apps/local-service/src/team/service.mts; packages/contracts/team/assets.ts; apps/web/src/features/team/TeamManager.tsx. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Project/global/vendor sources and unavailable scopes distinguished; effective/source versions, resources, provenance and reverse-agent links available.
- Files touched / work locations: apps/local-service/src/team/sources.mts; apps/local-service/src/team/service.mts; packages/contracts/team/assets.ts; apps/web/src/features/team/TeamManager.tsx.
- Technical value delivered: Показать назначение, источник, версию, зависимости и использование; source contracts и guards проверены.
- Product value delivered: Пользователь находит доступные навыки и понимает, какие агенты их используют.
- Actual implementation date and time: 12-11-2026 09:53
- Verification evidence: Web375/375 skip0; browser51; actual App/native49; build/typecheck, negative-case regressions и independent source review + root closed_allowed. [Run evidence](product-agent-os-web-m2b-execution-2026-11-12.md), [results](product-agent-os-web-m2b-results-2026-11-12.json).
- Residual risks: Local App-active technical scope; consumer required. History partial for unavailable sources, cursor15min; native loadedVersion unknown, remote discovery unavailable; M3/human/commercial/release отдельно.
- Follow-up: M2 technical21/26; remaining PAOS-0019/0020/0021/0022/0027 planned. AUTH-G1–G6/PAOS-0030 и human/release не закрыты.

### Task `PAOS-0017`

- Task: Редактор и версии скиллов
- Status: implemented
- Delivery stage: M2
- Execution order: 39
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 09:53
- Depends on: PAOS-0016
- Blocks: PAOS-0018, PAOS-0019, PAOS-0023
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Создавать и менять project-owned skills с проверкой структуры
- Technical value: Создавать и менять project-owned skills с проверкой структуры
- Product value: Пользователь адаптирует навык проекта и возвращается к прежней версии при ошибке.
- Scope: apps/local-service/src/skill-proposals; apps/web/src/features/skills/editor
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Редактор и версии скиллов доступна в соответствующем этапе
- Acceptance criteria: Preview diff и rollback работают; vendor original не перезаписывается; зависимость удаления видна
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/skill-proposals; apps/web/src/features/skills/editor
- Next step: Оставшиеся M2 PAOS-0019/0020/0021/0022/0027 требуют отдельного scope; весь M2 не закрыт.
- Actual time: Общий cohort baseline12-11-2026 08:29 MSK, проверен 12-11-2026 09:53 MSK; start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: apps/local-service/src/team/contract.mts; apps/local-service/src/team/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/team/TeamManager.tsx. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Skill preview/diff/versioned edit/archive/restore with historical blobs and resource retention; source originals preserved and dependency deletion guarded.
- Files touched / work locations: apps/local-service/src/team/contract.mts; apps/local-service/src/team/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/team/TeamManager.tsx.
- Technical value delivered: Создавать и менять project-owned skills с проверкой структуры; source contracts и guards проверены.
- Product value delivered: Пользователь адаптирует навык проекта и возвращается к прежней версии при ошибке.
- Actual implementation date and time: 12-11-2026 09:53
- Verification evidence: Web375/375 skip0; browser51; actual App/native49; build/typecheck, negative-case regressions и independent source review + root closed_allowed. [Run evidence](product-agent-os-web-m2b-execution-2026-11-12.md), [results](product-agent-os-web-m2b-results-2026-11-12.json).
- Residual risks: Local App-active technical scope; consumer required. History partial for unavailable sources, cursor15min; native loadedVersion unknown, remote discovery unavailable; M3/human/commercial/release отдельно.
- Follow-up: M2 technical21/26; remaining PAOS-0019/0020/0021/0022/0027 planned. AUTH-G1–G6/PAOS-0030 и human/release не закрыты.

### Task `PAOS-0018`

- Task: Добавление по пути и find-skills
- Status: implemented
- Delivery stage: M2
- Execution order: 40
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 09:53
- Depends on: PAOS-0017
- Blocks: PAOS-0019
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Единый выбор локального источника или найденного скилла
- Technical value: Единый выбор локального источника или найденного скилла
- Product value: Пользователь добавляет навык из папки или поиска, понимая его происхождение до установки.
- Scope: apps/local-service/src/skill-discovery; apps/web/src/features/skills/import
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Добавление по пути и find-skills доступна в соответствующем этапе
- Acceptance criteria: Поиск не устанавливает; path containment проверен; origin/license показаны до применения
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/skill-discovery; apps/web/src/features/skills/import
- Next step: Оставшиеся M2 PAOS-0019/0020/0021/0022/0027 требуют отдельного scope; весь M2 не закрыт.
- Actual time: Общий cohort baseline12-11-2026 08:29 MSK, проверен 12-11-2026 09:53 MSK; start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: apps/local-service/src/team/sources.mts; apps/local-service/src/team/service.mts; apps/local-service/src/http/application.mts; apps/web/src/features/team/TeamManager.tsx. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Local discovery never installs; reviewed bounded full-tree copy checks root identity/containment/links/secrets/hash, shows origin/license before Apply and preserves binary resources.
- Files touched / work locations: apps/local-service/src/team/sources.mts; apps/local-service/src/team/service.mts; apps/local-service/src/http/application.mts; apps/web/src/features/team/TeamManager.tsx.
- Technical value delivered: Единый выбор локального источника или найденного скилла; source contracts и guards проверены.
- Product value delivered: Пользователь добавляет навык из папки или поиска, понимая его происхождение до установки.
- Actual implementation date and time: 12-11-2026 09:53
- Verification evidence: Web375/375 skip0; browser51; actual App/native49; build/typecheck, negative-case regressions и independent source review + root closed_allowed. [Run evidence](product-agent-os-web-m2b-execution-2026-11-12.md), [results](product-agent-os-web-m2b-results-2026-11-12.json).
- Residual risks: Local App-active technical scope; consumer required. History partial for unavailable sources, cursor15min; native loadedVersion unknown, remote discovery unavailable; M3/human/commercial/release отдельно.
- Follow-up: M2 technical21/26; remaining PAOS-0019/0020/0021/0022/0027 planned. AUTH-G1–G6/PAOS-0030 и human/release не закрыты.

### Task `PAOS-0019`

- Task: Генерация по требованиям и описанию
- Status: implemented
- Delivery stage: M2
- Execution order: 41
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 11:38
- Depends on: PAOS-0017, PAOS-0018
- Blocks: PAOS-0024
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Предложить недостающие навыки проекта и сгенерировать draft
- Technical value: Предложить недостающие навыки проекта и сгенерировать draft
- Product value: Пользователь получает недостающие навыки из требований проекта или собственного описания.
- Scope: apps/local-service/src/skill-generation; apps/web/src/features/skills/generator
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Генерация по требованиям и описанию доступна в соответствующем этапе
- Acceptance criteria: Рекомендация связана с requirement; повтор не создаёт дубликат; применение имеет preview
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/skill-generation; apps/web/src/features/skills/generator
- Next step: Выбранный scope завершён; M2 technical26/26. Следующая стадия M3 требует отдельного запроса.
- Actual time: Общий cohort baseline12-11-2026 10:35:51 MSK; проверен 12-11-2026 11:38 MSK. Start/duration по отдельным карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: apps/local-service/src/team/skill-generation.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/http/application.mts; apps/web/src/features/skills/SkillGenerator.tsx; apps/web/src/api/client.ts; apps/web/src/ui/App.tsx; tests/web/skill-generation-artifacts.test.mts; tests/web/single-window/m2c-app-acceptance.mts. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Requirement-pinned или description-based App planning даёт editable SKILL.md с host requirement links; preview/explicit Apply; stable request/job/asset reuse; stale/invalid/no-gap/unavailable состояния явные.
- Files touched / work locations: apps/local-service/src/team/skill-generation.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/http/application.mts; apps/web/src/features/skills/SkillGenerator.tsx; apps/web/src/api/client.ts; apps/web/src/ui/App.tsx; tests/web/skill-generation-artifacts.test.mts; tests/web/single-window/m2c-app-acceptance.mts.
- Technical value delivered: Предложить недостающие навыки проекта и сгенерировать draft; bounded source/authority/revision contracts проверены.
- Product value delivered: Пользователь получает недостающие навыки из требований проекта или собственного описания.
- Actual implementation date and time: 12-11-2026 11:38
- Verification evidence: Web398/398 skip0; focused generation/artifacts10 и graph13; browser37; actual App planning29/2jobs; native exact cached candidate/default3modes; build/typecheck, Python1450 skip1, fixtures91/transcripts26, independent7findings fixed + root verification. [Evidence](product-agent-os-web-m2c-execution-2026-11-12.md), [results](product-agent-os-web-m2c-results-2026-11-12.json).
- Residual risks: Lexical subset без полного type/runtime proof; bounded derived snapshots/rebuild; available source/history coverage. Managed skill не native installation, document proposal staged-only. Installed npm Codex runtime_mismatch остаётся fail-closed; exact cached tuple квалифицирован отдельно. Human/commercial/release отдельно.
- Follow-up: M2 technical26/26; M3/T1, AUTH-G1–G6/C46-01–08, PAOS-0030 и human/release acceptance не закрыты.

### Task `PAOS-0020`

- Task: Индекс файлов и символов
- Status: implemented
- Delivery stage: M2
- Execution order: 42
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 11:38
- Depends on: PAOS-0001
- Blocks: PAOS-0021, PAOS-0022
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Типизированные зависимости файлов и переменных с source anchors
- Technical value: Типизированные зависимости файлов и переменных с source anchors
- Product value: Пользователь получает понятную основу карты зависимостей с явными пробелами анализа.
- Scope: apps/local-service/src/code-index; packages/contracts/graph
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Индекс файлов и символов доступна в соответствующем этапе
- Acceptance criteria: Неподдержанный язык и dynamic reference обозначены; индекс привязан к revision
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: graph-cockpit-engineer, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/code-index; packages/contracts/graph
- Next step: Выбранный scope завершён; M2 technical26/26. Следующая стадия M3 требует отдельного запроса.
- Actual time: Общий cohort baseline12-11-2026 10:35:51 MSK; проверен 12-11-2026 11:38 MSK. Start/duration по отдельным карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: packages/contracts/graph/code-graph.ts; apps/local-service/src/code-index/sources.mts; apps/local-service/src/code-index/lexical.mts; apps/local-service/src/code-index/parser-worker.mts; apps/local-service/src/code-index/service.mts; apps/local-service/src/http/application.mts; tests/web/code-index.test.mts. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Read-only bounded JS/TS AST lexical index с file/symbol/scope/namespace/UTF-16 anchor/revision; imports/calls/references и unsupported/dynamic/unresolved/parse-error coverage; immutable snapshots и checked source boundaries.
- Files touched / work locations: packages/contracts/graph/code-graph.ts; apps/local-service/src/code-index/sources.mts; apps/local-service/src/code-index/lexical.mts; apps/local-service/src/code-index/parser-worker.mts; apps/local-service/src/code-index/service.mts; apps/local-service/src/http/application.mts; tests/web/code-index.test.mts.
- Technical value delivered: Типизированные зависимости файлов и переменных с source anchors; bounded source/authority/revision contracts проверены.
- Product value delivered: Пользователь получает понятную основу карты зависимостей с явными пробелами анализа.
- Actual implementation date and time: 12-11-2026 11:38
- Verification evidence: Web398/398 skip0; focused generation/artifacts10 и graph13; browser37; actual App planning29/2jobs; native exact cached candidate/default3modes; build/typecheck, Python1450 skip1, fixtures91/transcripts26, independent7findings fixed + root verification. [Evidence](product-agent-os-web-m2c-execution-2026-11-12.md), [results](product-agent-os-web-m2c-results-2026-11-12.json).
- Residual risks: Lexical subset без полного type/runtime proof; bounded derived snapshots/rebuild; available source/history coverage. Managed skill не native installation, document proposal staged-only. Installed npm Codex runtime_mismatch остаётся fail-closed; exact cached tuple квалифицирован отдельно. Human/commercial/release отдельно.
- Follow-up: M2 technical26/26; M3/T1, AUTH-G1–G6/C46-01–08, PAOS-0030 и human/release acceptance не закрыты.

### Task `PAOS-0021`

- Task: Граф и навигация к исходникам
- Status: implemented
- Delivery stage: M2
- Execution order: 43
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 11:38
- Depends on: PAOS-0004, PAOS-0020
- Blocks: PAOS-0022
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Фильтровать graph и раскрывать соседей выбранного узла
- Technical value: Фильтровать graph и раскрывать соседей выбранного узла
- Product value: Пользователь исследует структуру проекта и быстро находит связанные файлы без чтения всех папок.
- Scope: apps/web/src/features/graph
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Граф и навигация к исходникам доступна в соответствующем этапе
- Acceptance criteria: Есть search, depth, edge type, keyboard list alternative; большие графы не загружаются целиком
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 14:00:00 (предварительно)
- Agents: graph-cockpit-engineer, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/web/src/features/graph
- Next step: Выбранный scope завершён; M2 technical26/26. Следующая стадия M3 требует отдельного запроса.
- Actual time: Общий cohort baseline12-11-2026 10:35:51 MSK; проверен 12-11-2026 11:38 MSK. Start/duration по отдельным карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: packages/contracts/graph/code-graph.ts; apps/local-service/src/code-index/service.mts; apps/web/src/features/graph/GraphExplorer.tsx; apps/web/src/api/client.ts; apps/web/src/ui/App.tsx; apps/web/src/design/app.css; tests/web/code-index.test.mts; tests/web/single-window/m2c-browser-acceptance.mts. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Bounded SVG и keyboard list, query/edge types/depth/neighbors/pages, source/impact inspector; context endpoints сохраняют cross-page edges, stale и late responses не маскируются как fresh.
- Files touched / work locations: packages/contracts/graph/code-graph.ts; apps/local-service/src/code-index/service.mts; apps/web/src/features/graph/GraphExplorer.tsx; apps/web/src/api/client.ts; apps/web/src/ui/App.tsx; apps/web/src/design/app.css; tests/web/code-index.test.mts; tests/web/single-window/m2c-browser-acceptance.mts.
- Technical value delivered: Фильтровать graph и раскрывать соседей выбранного узла; bounded source/authority/revision contracts проверены.
- Product value delivered: Пользователь исследует структуру проекта и быстро находит связанные файлы без чтения всех папок.
- Actual implementation date and time: 12-11-2026 11:38
- Verification evidence: Web398/398 skip0; focused generation/artifacts10 и graph13; browser37; actual App planning29/2jobs; native exact cached candidate/default3modes; build/typecheck, Python1450 skip1, fixtures91/transcripts26, independent7findings fixed + root verification. [Evidence](product-agent-os-web-m2c-execution-2026-11-12.md), [results](product-agent-os-web-m2c-results-2026-11-12.json).
- Residual risks: Lexical subset без полного type/runtime proof; bounded derived snapshots/rebuild; available source/history coverage. Managed skill не native installation, document proposal staged-only. Installed npm Codex runtime_mismatch остаётся fail-closed; exact cached tuple квалифицирован отдельно. Human/commercial/release отдельно.
- Follow-up: M2 technical26/26; M3/T1, AUTH-G1–G6/C46-01–08, PAOS-0030 и human/release acceptance не закрыты.

### Task `PAOS-0022`

- Task: Влияние переменной и изменения
- Status: implemented
- Delivery stage: M2
- Execution order: 44
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 11:38
- Depends on: PAOS-0007, PAOS-0020, PAOS-0021
- Blocks: PAOS-0028
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Показать define/read/write/reference по scope и задачам
- Technical value: Показать define/read/write/reference по scope и задачам
- Product value: Пользователь видит, какие места могут быть затронуты изменением конкретной переменной.
- Scope: apps/local-service/src/impact; apps/web/src/features/graph/inspector
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Влияние переменной и изменения доступна в соответствующем этапе
- Acceptance criteria: Одноимённые переменные разных scope различены; stale и unresolved edges видимы
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 14:00:00 (предварительно)
- Agents: graph-cockpit-engineer, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/impact; apps/web/src/features/graph/inspector
- Next step: Выбранный scope завершён; M2 technical26/26. Следующая стадия M3 требует отдельного запроса.
- Actual time: Общий cohort baseline12-11-2026 10:35:51 MSK; проверен 12-11-2026 11:38 MSK. Start/duration по отдельным карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: apps/local-service/src/code-index/lexical.mts; apps/local-service/src/code-index/service.mts; apps/local-service/src/impact/service.mts; apps/web/src/features/graph/GraphExplorer.tsx; tests/web/code-index.test.mts. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Shadowed bindings не сливаются; define/read/write/reference/call occurrences и explicit task file references с matching/stale/unknown pins; paged impact и ограничения lexical subset показаны.
- Files touched / work locations: apps/local-service/src/code-index/lexical.mts; apps/local-service/src/code-index/service.mts; apps/local-service/src/impact/service.mts; apps/web/src/features/graph/GraphExplorer.tsx; tests/web/code-index.test.mts.
- Technical value delivered: Показать define/read/write/reference по scope и задачам; bounded source/authority/revision contracts проверены.
- Product value delivered: Пользователь видит, какие места могут быть затронуты изменением конкретной переменной.
- Actual implementation date and time: 12-11-2026 11:38
- Verification evidence: Web398/398 skip0; focused generation/artifacts10 и graph13; browser37; actual App planning29/2jobs; native exact cached candidate/default3modes; build/typecheck, Python1450 skip1, fixtures91/transcripts26, independent7findings fixed + root verification. [Evidence](product-agent-os-web-m2c-execution-2026-11-12.md), [results](product-agent-os-web-m2c-results-2026-11-12.json).
- Residual risks: Lexical subset без полного type/runtime proof; bounded derived snapshots/rebuild; available source/history coverage. Managed skill не native installation, document proposal staged-only. Installed npm Codex runtime_mismatch остаётся fail-closed; exact cached tuple квалифицирован отдельно. Human/commercial/release отдельно.
- Follow-up: M2 technical26/26; M3/T1, AUTH-G1–G6/C46-01–08, PAOS-0030 и human/release acceptance не закрыты.

### Task `PAOS-0023`

- Task: Политика автономности и лимиты
- Status: implemented
- Delivery stage: M3
- Execution order: 46
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 13:20
- Depends on: PAOS-0008, PAOS-0013, PAOS-0017
- Blocks: PAOS-0024, PAOS-0026, PAOS-0037
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Задать заранее разрешённые действия, бюджеты и stop conditions
- Technical value: Задать заранее разрешённые действия, бюджеты и stop conditions
- Product value: Пользователь задаёт границы самостоятельной работы один раз и сохраняет возможность остановки.
- Scope: packages/contracts/autonomy/policy.ts; apps/local-service/src/autonomy-policy; existing App gateway/HTTP integration; apps/web/src/features/autonomy
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Политика автономности и лимиты доступна в соответствующем этапе
- Acceptance criteria: Preview policy объясняет возможности; UI не расширяет host permissions; pause доступна
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Повтор действий, конкурирующие writers, выход за разрешённый scope; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; react-best-practices; frontend-testing-debugging
- Output artifacts: apps/local-service/src/autonomy-policy/service.mts; packages/contracts/autonomy/policy.ts; apps/local-service/src/http/application.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/runtime/live-gateway.mts; packages/contracts/runtime/qualified-manifest.json; apps/web/src/features/autonomy/AutonomyManager.tsx; apps/web/src/api/client.ts; apps/web/src/ui/App.tsx; apps/web/src/locales/messages.ts; tests/web/autonomy-policy.test.mts; tests/web/autonomy-runtime.test.mts; tests/web/single-window/m3-autonomy-acceptance.mts; apps/web/README.md; research/product-agent-os-web-m3-0023-execution-2026-11-12.md; research/product-agent-os-web-m3-0023-results-2026-11-12.json; REQUIREMENTS.md; PLAN.md; TEST.md; RUNLOG.md; docs/sources/registry.md; docs/sources/registry.en.md; research/product-agent-os-web-task-manager-plan-2026-11-09.md; research/product-agent-os-web-task-manager-task-group-2026-11-09.json
- Next step: Следующая PAOS-0037: Depends on PAOS-0036/0023 технически выполнены; начать отдельным scope, сохраняя budget/pause/approval guards.
- Actual time: Measured scope start 12-11-2026 12:37:57 MSK; end 12-11-2026 13:20 MSK; active duration not separately measured, duration=null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: Actual create/modify receipts: apps/local-service/src/autonomy-policy/service.mts (create); packages/contracts/autonomy/policy.ts (create); apps/local-service/src/http/application.mts (modify); apps/local-service/src/runtime/app-agent-gateway.mts (modify); apps/local-service/src/runtime/live-gateway.mts (modify); packages/contracts/runtime/qualified-manifest.json (modify); apps/web/src/features/autonomy/AutonomyManager.tsx (create); apps/web/src/api/client.ts (modify); apps/web/src/ui/App.tsx (modify); apps/web/src/locales/messages.ts (modify); tests/web/autonomy-policy.test.mts (create); tests/web/autonomy-runtime.test.mts (create); tests/web/single-window/m3-autonomy-acceptance.mts (create); apps/web/README.md (modify); research/product-agent-os-web-m3-0023-execution-2026-11-12.md (create); research/product-agent-os-web-m3-0023-results-2026-11-12.json (create); REQUIREMENTS.md (modify); PLAN.md (modify); TEST.md (modify); RUNLOG.md (modify); docs/sources/registry.md (modify); docs/sources/registry.en.md (modify); research/product-agent-os-web-task-manager-plan-2026-11-09.md (modify); research/product-agent-os-web-task-manager-task-group-2026-11-09.json (modify)

#### Completion Report

- Status: implemented
- What was done: Project policy preview/save/resume/pause, explicit App opt-in, durable run/command budgets/deadline, stop conditions и current pause fence реализованы; old Pause replay cohort исправлен.
- Files touched / work locations: apps/local-service/src/autonomy-policy/service.mts; packages/contracts/autonomy/policy.ts; apps/local-service/src/http/application.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/runtime/live-gateway.mts; packages/contracts/runtime/qualified-manifest.json; apps/web/src/features/autonomy/AutonomyManager.tsx; apps/web/src/api/client.ts; apps/web/src/ui/App.tsx; apps/web/src/locales/messages.ts; tests/web/autonomy-policy.test.mts; tests/web/autonomy-runtime.test.mts; tests/web/single-window/m3-autonomy-acceptance.mts; apps/web/README.md; research/product-agent-os-web-m3-0023-execution-2026-11-12.md; research/product-agent-os-web-m3-0023-results-2026-11-12.json; REQUIREMENTS.md; PLAN.md; TEST.md; RUNLOG.md; docs/sources/registry.md; docs/sources/registry.en.md; research/product-agent-os-web-task-manager-plan-2026-11-09.md; research/product-agent-os-web-task-manager-task-group-2026-11-09.json
- Technical value delivered: Один server-side policy owner использует существующие SQLite CAS/idempotency и App coordinator; unsupported paths/routes fail closed, approvals не расширяются.
- Product value delivered: Пользователь выбирает задачи и лимиты, видит preview, явно включает допуск и ставит работу на паузу; черновик не теряется при conflict.
- Actual implementation date and time: 12-11-2026 13:20
- Verification evidence: Web413/413 skip0; focused15; production browser/native47; exact candidate/default native3modes; full Python/fixture91/transcript26/compatibility и docs gates — research/product-agent-os-web-m3-0023-execution-2026-11-12.md, соседний results JSON.
- Residual risks: PAOS-mediated commands only; App/active consumer required. Narrow paths/API opt-in и token/cost metering unavailable. Installed npm Codex mismatch сохраняется; cached exact tuple проверен отдельно. Human/commercial/release acceptance отдельно.
- Follow-up: Следующая PAOS-0037: Depends on PAOS-0036/0023 технически выполнены; начать отдельным scope, сохраняя budget/pause/approval guards.

### Task `PAOS-0024`

- Task: Очередь, назначения и владение файлами
- Status: implemented
- Delivery stage: M3
- Execution order: 48
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 15:44
- Depends on: PAOS-0015, PAOS-0019, PAOS-0023, PAOS-0037, PAOS-0038
- Blocks: PAOS-0025
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Назначать агентов и skills в пределах scope без конфликтующих writers
- Technical value: Назначать агентов и skills в пределах scope без конфликтующих writers
- Product value: Пользователь запускает независимые задачи параллельно без незаметного перезаписывания одних файлов.
- Scope: packages/contracts/scheduler/queue.ts; apps/local-service/src/scheduler; private recipe/App/SQLite/workflow integration; apps/web/src/features/workflows/recipes
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Очередь, назначения и владение файлами доступна в соответствующем этапе
- Acceptance criteria: Очередь соблюдает pinned recipe, blocks links, hard WIP и ownership; независимые writers допускаются только при отсутствии пересечения
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Повтор действий, конкурирующие writers, выход за разрешённый scope; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; react-best-practices; frontend-testing-debugging
- Output artifacts: EVALS.md; PLAN.md; REQUIREMENTS.md; RUNLOG.md; TEST.md; apps/local-service/src/execution-recipes/contract.mts; apps/local-service/src/execution-recipes/service.mts; apps/local-service/src/http/application.mts; apps/local-service/src/main.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/workflows/guards.mts; apps/web/README.md; apps/web/src/api/client.ts; apps/web/src/design/app.css; apps/web/src/features/workflows/WorkflowManager.tsx; apps/web/src/features/workflows/recipes/RecipeRunner.tsx; docs/sources/registry.en.md; docs/sources/registry.md; packages/contracts/runtime/qualified-manifest.json; packages/contracts/storage/local-store.ts; research/product-agent-os-requirements-history-2026-11-10.md; tests/web/app-agent-gateway.test.mts; tests/web/recipe-runtime.test.mts; apps/local-service/src/scheduler/contract.mts; apps/local-service/src/scheduler/ownership.mts; apps/local-service/src/scheduler/service.mts; apps/local-service/src/scheduler/storage-guards.mts; apps/web/src/features/workflows/recipes/QueueManager.tsx; packages/contracts/scheduler/queue.ts; research/product-agent-os-web-m3-0024-execution-2026-11-12.md; tests/web/parallel-workspaces.test.mts; tests/web/recipe-fixture.mts; tests/web/scheduler-capacity.test.mts; tests/web/scheduler-runtime.test.mts; tests/web/scheduler.test.mts; tests/web/single-window/m3-queue-acceptance.mts; tests/web/single-window/m3-queue-parallel-acceptance.mts; research/product-agent-os-web-task-manager-plan-2026-11-09.md; research/product-agent-os-web-task-manager-task-group-2026-11-09.json; research/product-agent-os-web-m3-0024-results-2026-11-12.json
- Next step: Следующая PAOS-0025: исполнение, восстановление и отмена. Зависимости0011/0024/0044 выполнены; следующий slice требует отдельного scope. PAOS-0026/0028 остаются planned.
- Actual time: Measured scope start12-11-2026 14:42:57 MSK; end 12-11-2026 15:44 MSK. Wall interval available, active duration not separately instrumented; duration=null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: EVALS.md (modify); PLAN.md (modify); REQUIREMENTS.md (modify); RUNLOG.md (modify); TEST.md (modify); apps/local-service/src/execution-recipes/contract.mts (modify); apps/local-service/src/execution-recipes/service.mts (modify); apps/local-service/src/http/application.mts (modify); apps/local-service/src/main.mts (modify); apps/local-service/src/runtime/app-agent-gateway.mts (modify); apps/local-service/src/storage/sqlite-worker.mts (modify); apps/local-service/src/task-manager/service.mts (modify); apps/local-service/src/workflows/guards.mts (modify); apps/web/README.md (modify); apps/web/src/api/client.ts (modify); apps/web/src/design/app.css (modify); apps/web/src/features/workflows/WorkflowManager.tsx (modify); apps/web/src/features/workflows/recipes/RecipeRunner.tsx (modify); docs/sources/registry.en.md (modify); docs/sources/registry.md (modify); packages/contracts/runtime/qualified-manifest.json (modify); packages/contracts/storage/local-store.ts (modify); research/product-agent-os-requirements-history-2026-11-10.md (modify); tests/web/app-agent-gateway.test.mts (modify); tests/web/recipe-runtime.test.mts (modify); apps/local-service/src/scheduler/contract.mts (create); apps/local-service/src/scheduler/ownership.mts (create); apps/local-service/src/scheduler/service.mts (create); apps/local-service/src/scheduler/storage-guards.mts (create); apps/web/src/features/workflows/recipes/QueueManager.tsx (create); packages/contracts/scheduler/queue.ts (create); research/product-agent-os-web-m3-0024-execution-2026-11-12.md (create); tests/web/parallel-workspaces.test.mts (create); tests/web/recipe-fixture.mts (create); tests/web/scheduler-capacity.test.mts (create); tests/web/scheduler-runtime.test.mts (create); tests/web/scheduler.test.mts (create); tests/web/single-window/m3-queue-acceptance.mts (create); tests/web/single-window/m3-queue-parallel-acceptance.mts (create); research/product-agent-os-web-task-manager-plan-2026-11-09.md (modify); research/product-agent-os-web-task-manager-task-group-2026-11-09.json (modify); research/product-agent-os-web-m3-0024-results-2026-11-12.json (create)

#### Completion Report

- Status: implemented
- What was done: Durable queue, reviewed enqueue/reorder/pause/cancel, frozen recipe assignments, atomic blocks/hard WIP/ownership admission и bounded coordinator реализованы. До4 разных non-overlapping workspace roots исполняются параллельно при одном writer/project/workspace; capacity/root findings исправлены.
- Files touched / work locations: EVALS.md; PLAN.md; REQUIREMENTS.md; RUNLOG.md; TEST.md; apps/local-service/src/execution-recipes/contract.mts; apps/local-service/src/execution-recipes/service.mts; apps/local-service/src/http/application.mts; apps/local-service/src/main.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/workflows/guards.mts; apps/web/README.md; apps/web/src/api/client.ts; apps/web/src/design/app.css; apps/web/src/features/workflows/WorkflowManager.tsx; apps/web/src/features/workflows/recipes/RecipeRunner.tsx; docs/sources/registry.en.md; docs/sources/registry.md; packages/contracts/runtime/qualified-manifest.json; packages/contracts/storage/local-store.ts; research/product-agent-os-requirements-history-2026-11-10.md; tests/web/app-agent-gateway.test.mts; tests/web/recipe-runtime.test.mts; apps/local-service/src/scheduler/contract.mts; apps/local-service/src/scheduler/ownership.mts; apps/local-service/src/scheduler/service.mts; apps/local-service/src/scheduler/storage-guards.mts; apps/web/src/features/workflows/recipes/QueueManager.tsx; packages/contracts/scheduler/queue.ts; research/product-agent-os-web-m3-0024-execution-2026-11-12.md; tests/web/parallel-workspaces.test.mts; tests/web/recipe-fixture.mts; tests/web/scheduler-capacity.test.mts; tests/web/scheduler-runtime.test.mts; tests/web/scheduler.test.mts; tests/web/single-window/m3-queue-acceptance.mts; tests/web/single-window/m3-queue-parallel-acceptance.mts; research/product-agent-os-web-task-manager-plan-2026-11-09.md; research/product-agent-os-web-task-manager-task-group-2026-11-09.json; research/product-agent-os-web-m3-0024-results-2026-11-12.json
- Technical value delivered: Queue coordinator сохраняет CAS/idempotency и immutable pins; SQLite атомарно проверяет dependencies/WIP/task ownership/physical roots/cap4, gateway обслуживает независимые native jobs.
- Product value delivered: Пользователь ставит Task в очередь с закреплённым recipe и назначениями, видит порядок/ожидание/владение, управляет pause/cancel; независимые workspaces выполняются параллельно без конфликтующих writers.
- Actual implementation date and time: 12-11-2026 15:44
- Verification evidence: Web443/443 skip0; queue/parallel7; Python1450(skip1); fixtures91/transcripts26; browser88, parallel native49 и actual App46; exact native candidate/default; docs/compatibility gates — research/product-agent-os-web-m3-0024-execution-2026-11-12.md и results JSON.
- Residual risks: Active App consumer required; PAOS-mediated commands only, host tools не confined. Execution phase in_progress; interrupted/unknown work не replay. Token/cost/performance/model-quality и human/commercial/release acceptance отдельно.
- Follow-up: Следующая PAOS-0025: исполнение, восстановление и отмена. Зависимости0011/0024/0044 выполнены; следующий slice требует отдельного scope. PAOS-0026/0028 остаются planned.

### Task `PAOS-0025`

- Task: Исполнение, восстановление и отмена
- Status: planned
- Delivery stage: M3
- Execution order: 49
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0011, PAOS-0024, PAOS-0044
- Blocks: PAOS-0026
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Run adapter выполняет ограниченный план с восстановлением
- Technical value: Run adapter выполняет ограниченный план с восстановлением
- Product value: Пользователь может продолжить или отменить работу после сбоя, сохранив понятную историю.
- Scope: apps/local-service/src/runtime; apps/local-service/src/recovery
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Исполнение, восстановление и отмена доступна в соответствующем этапе
- Acceptance criteria: Повтор команды идемпотентен; timeout/cancel/crash дают определённое состояние и evidence
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Повтор действий, конкурирующие writers, выход за разрешённый scope; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 24:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/runtime; apps/local-service/src/recovery
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0026`

- Task: Решения и наблюдаемость автономности
- Status: planned
- Delivery stage: M3
- Execution order: 50
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0023, PAOS-0025
- Blocks: PAOS-0028
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Показать что выполняется, почему остановилось и какое решение требуется
- Technical value: Показать что выполняется, почему остановилось и какое решение требуется
- Product value: Пользователь вмешивается там, где действительно требуется решение, и видит его последствия.
- Scope: apps/web/src/features/decisions; apps/local-service/src/decisions
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Решения и наблюдаемость автономности доступна в соответствующем этапе
- Acceptance criteria: Из решения доступен diff/scope/evidence; истёкшее решение не применяется; история сохраняется
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Повтор действий, конкурирующие writers, выход за разрешённый scope; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/web/src/features/decisions; apps/local-service/src/decisions
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0027`

- Task: Документы, проверки и общий поиск
- Status: implemented
- Delivery stage: M2
- Execution order: 45
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 11:38
- Depends on: PAOS-0007, PAOS-0008, PAOS-0011
- Blocks: PAOS-0028
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Объединить артефакты и результаты с задачами и источниками
- Technical value: Объединить артефакты и результаты с задачами и источниками
- Product value: Пользователь находит планы и проверки прямо из задачи, не разбираясь в расположении Markdown.
- Scope: apps/web/src/features/documents; apps/web/src/features/checks; apps/web/src/features/search
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Документы, проверки и общий поиск доступна в соответствующем этапе
- Acceptance criteria: Source version и время видны; результат теста не выдаётся за пользовательскую приёмку
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 14:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/web/src/features/documents; apps/web/src/features/checks; apps/web/src/features/search
- Next step: Выбранный scope завершён; M2 technical26/26. Следующая стадия M3 требует отдельного запроса.
- Actual time: Общий cohort baseline12-11-2026 10:35:51 MSK; проверен 12-11-2026 11:38 MSK. Start/duration по отдельным карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: packages/contracts/artifacts/catalog.ts; apps/local-service/src/artifacts/service.mts; apps/local-service/src/http/application.mts; apps/web/src/features/artifacts/ArtifactExplorer.tsx; apps/web/src/api/client.ts; apps/web/src/ui/App.tsx; tests/web/skill-generation-artifacts.test.mts; tests/web/single-window/m2c-browser-acceptance.mts. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Version/time-pinned document/check/acceptance catalog и reader/outline/anchors; global search включает доступные sources/symbols; safe staged document proposals сохраняют оригинал; checks не заменяют owner acceptance.
- Files touched / work locations: packages/contracts/artifacts/catalog.ts; apps/local-service/src/artifacts/service.mts; apps/local-service/src/http/application.mts; apps/web/src/features/artifacts/ArtifactExplorer.tsx; apps/web/src/api/client.ts; apps/web/src/ui/App.tsx; tests/web/skill-generation-artifacts.test.mts; tests/web/single-window/m2c-browser-acceptance.mts.
- Technical value delivered: Объединить артефакты и результаты с задачами и источниками; bounded source/authority/revision contracts проверены.
- Product value delivered: Пользователь находит планы и проверки прямо из задачи, не разбираясь в расположении Markdown.
- Actual implementation date and time: 12-11-2026 11:38
- Verification evidence: Web398/398 skip0; focused generation/artifacts10 и graph13; browser37; actual App planning29/2jobs; native exact cached candidate/default3modes; build/typecheck, Python1450 skip1, fixtures91/transcripts26, independent7findings fixed + root verification. [Evidence](product-agent-os-web-m2c-execution-2026-11-12.md), [results](product-agent-os-web-m2c-results-2026-11-12.json).
- Residual risks: Lexical subset без полного type/runtime proof; bounded derived snapshots/rebuild; available source/history coverage. Managed skill не native installation, document proposal staged-only. Installed npm Codex runtime_mismatch остаётся fail-closed; exact cached tuple квалифицирован отдельно. Human/commercial/release отдельно.
- Follow-up: M2 technical26/26; M3/T1, AUTH-G1–G6/C46-01–08, PAOS-0030 и human/release acceptance не закрыты.

### Task `PAOS-0028`

- Task: Интеграционная проверка пути
- Status: planned
- Delivery stage: M4
- Execution order: 51
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0022, PAOS-0026, PAOS-0027, PAOS-0033, PAOS-0034, PAOS-0035, PAOS-0036, PAOS-0037, PAOS-0038, PAOS-0045
- Blocks: PAOS-0029
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Проверить создание задачи, план, запуск, сессию, изменения и приёмку
- Technical value: Проверить создание задачи, план, запуск, сессию, изменения и приёмку
- Product value: Пользователь проходит весь путь от постановки до приёмки без разрывов между разделами.
- Scope: tests/web; tests/local-service
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Интеграционная проверка пути доступна в соответствующем этапе
- Acceptance criteria: Все 10 acceptance scenarios PRD §14 и прежний основной путь проверены; user-only completion и active-run cancellation подтверждены; отрицательные сценарии migration/links/attachments не теряют данные
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 24:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: tests/web; tests/local-service
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0029`

- Task: Доступность, языки и темы
- Status: planned
- Delivery stage: M4
- Execution order: 52
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0028
- Blocks: PAOS-0030
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Проверить клавиатуру, контраст, responsive и все локализованные состояния
- Technical value: Проверить клавиатуру, контраст, responsive и все локализованные состояния
- Product value: Пользователь сохраняет доступ ко всем действиям с клавиатуры, на узком экране и в обеих локализациях.
- Scope: tests/web/accessibility; docs/web/accessibility
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Доступность, языки и темы доступна в соответствующем этапе
- Acceptance criteria: Все 26 описанных экранов и новые task tabs проверены в RU/EN × Light/Dark; keyboard Kanban/workflow и длинные значения не теряют действия
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: tests/web/accessibility; docs/web/accessibility
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0030`

- Task: Упаковка и пилот
- Status: planned
- Delivery stage: M4
- Execution order: 53
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0029, PAOS-0046
- Blocks: PAOS-0052
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Проверить install/start/backup/rollback и полезность на реальном проекте
- Technical value: Проверить install/start/backup/rollback и полезность на реальном проекте
- Product value: Пользователь устанавливает и восстанавливает локальный продукт по проверенному процессу.
- Scope: apps/desktop-local; docs/web/pilot
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Упаковка и пилот доступна в соответствующем этапе
- Acceptance criteria: Пилот согласован отдельно; restore проверен; наблюдения отделены от продуктовых гипотез Перед коммерческим выпуском повторно сверить актуальность AUTH-G1–G6 и закрытие применимых gaps раннего PAOS-0046; прежний review не является бессрочным допуском.
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/desktop-local; docs/web/pilot
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0031`

- Task: Иерархия Epic / Task / Bug / UserStory / Sub-Task
- Status: implemented
- Delivery stage: M2
- Execution order: 20
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 22:40
- Depends on: PAOS-0002
- Blocks: PAOS-0032, PAOS-0034, PAOS-0038
- Source: PRD §14; TM-15, TM-16
- Short description: Родительские связи, преобразование типов и roll-up без двойного счёта
- Technical value: Родительские связи, преобразование типов и roll-up без двойного счёта
- Product value: Пользователь разбивает инициативу на работы и подзадачи и видит общий прогресс
- Scope: packages/contracts/issues; apps/local-service/src/issue-hierarchy; apps/web/src/features/tasks/hierarchy
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Иерархия Epic / Task / Bug / UserStory / Sub-Task в будущем Web
- Acceptance criteria: Epic содержит standard types; Sub-Task имеет один standard parent; циклы и недопустимый reparent отклоняются; закрытие parent проверяет children
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 14:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: packages/contracts/issues; apps/local-service/src/issue-hierarchy; apps/web/src/features/tasks/hierarchy
- Next step: Следующий неисполненный M2 scope — PAOS-0036; он требует отдельной команды владельца.
- Actual time: общий cohort начат 11-11-2026 20:41 MSK; проверен 11-11-2026 22:40 MSK. Start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: packages/contracts/issues/task-profile.ts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/tasks/TaskManager.tsx; apps/web/src/features/tasks/model.ts. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Versioned M2 profile, Epic/standard/Sub-Task rules, conversion preview, cycle/children gates и roll-up без двойного счёта; явный legacy upgrade без потери identity.
- Files touched / work locations: packages/contracts/issues/task-profile.ts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/tasks/TaskManager.tsx; apps/web/src/features/tasks/model.ts.
- Technical value delivered: Родительские связи, преобразование типов и roll-up без двойного счёта; транзакционные guards и regression checks реализованы.
- Product value delivered: Пользователь разбивает инициативу на работы и подзадачи и видит общий прогресс.
- Actual implementation date and time: 11-11-2026 22:40
- Verification evidence: full Web 345/345 skip0; browser 88; actual App/native 27; focused negative cases, build/typecheck и independent closed_allowed. [Run evidence](product-agent-os-web-m2-execution-2026-11-11.md), [source hashes/results](product-agent-os-web-m2-results-2026-11-11.json).
- Residual risks: local App-active technical scope; active consumer required, sandbox только PAOS-mediated commands. Human/commercial/release acceptance и AUTH-G1–G6 отдельно; narrow Markdown subset обозначен в UI.
- Follow-up: Остальные 16 M2 tasks, включая PAOS-0036, остаются planned; commercial repeat review PAOS-0030. Эта карточка не закрывает весь M2.


### Task `PAOS-0032`

- Task: Поля, авторство, приоритеты, компоненты и даты
- Status: implemented
- Delivery stage: M2
- Execution order: 21
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 22:40
- Depends on: PAOS-0031, PAOS-0004
- Blocks: PAOS-0005, PAOS-0006, PAOS-0033, PAOS-0035
- Source: PRD §14; TM-16
- Short description: Неизменяемый creator, отдельный initiator, project components и календарные поля
- Technical value: Неизменяемый creator, отдельный initiator, project components и календарные поля
- Product value: Пользователь знает источник задачи, её важность, область и сроки
- Scope: packages/contracts/issue-fields; apps/local-service/src/components; apps/web/src/features/tasks/editor
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Поля, авторство, приоритеты, компоненты и даты в будущем Web
- Acceptance criteria: 11 исходных components доступны; multi-select; creator неизменяем; start/due validation и timezone проверены; unknown import не подменяется user
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: packages/contracts/issue-fields; apps/local-service/src/components; apps/web/src/features/tasks/editor
- Next step: Следующий неисполненный M2 scope — PAOS-0036; он требует отдельной команды владельца.
- Actual time: общий cohort начат 11-11-2026 20:41 MSK; проверен 11-11-2026 22:40 MSK. Start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: packages/contracts/issues/task-profile.ts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/tasks/Editor.tsx; apps/web/src/features/tasks/Settings.tsx. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Immutable creator/initiator/createdAt, unknown import provenance, 11 components и archive/multi-select, calendar/timezone и Due Date reason через публичные writes.
- Files touched / work locations: packages/contracts/issues/task-profile.ts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/tasks/Editor.tsx; apps/web/src/features/tasks/Settings.tsx.
- Technical value delivered: Неизменяемый creator, отдельный initiator, project components и календарные поля; транзакционные guards и regression checks реализованы.
- Product value delivered: Пользователь знает источник задачи, её важность, область и сроки.
- Actual implementation date and time: 11-11-2026 22:40
- Verification evidence: full Web 345/345 skip0; browser 88; actual App/native 27; focused negative cases, build/typecheck и independent closed_allowed. [Run evidence](product-agent-os-web-m2-execution-2026-11-11.md), [source hashes/results](product-agent-os-web-m2-results-2026-11-11.json).
- Residual risks: local App-active technical scope; active consumer required, sandbox только PAOS-mediated commands. Human/commercial/release acceptance и AUTH-G1–G6 отдельно; narrow Markdown subset обозначен в UI.
- Follow-up: Остальные 16 M2 tasks, включая PAOS-0036, остаются planned; commercial repeat review PAOS-0030. Эта карточка не закрывает весь M2.


### Task `PAOS-0033`

- Task: Версии продукта и release policy
- Status: implemented
- Delivery stage: M2
- Execution order: 22
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 22:40
- Depends on: PAOS-0032
- Blocks: PAOS-0028
- Source: PRD §14; TM-17
- Short description: Раздельные affects/fix version references и условия планирования релиза
- Technical value: Раздельные affects/fix version references и условия планирования релиза
- Product value: Пользователь различает затронутый продукт и выпуск, который получит исправление
- Scope: apps/local-service/src/versions; apps/web/src/features/releases; packages/contracts/versions
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Версии продукта и release policy в будущем Web
- Acceptance criteria: Bug affects v1.2/fix v1.3 фильтруется корректно; archive сохраняет ссылки; Done не выпускает релиз
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: apps/local-service/src/versions; apps/web/src/features/releases; packages/contracts/versions
- Next step: Следующий неисполненный M2 scope — PAOS-0036; он требует отдельной команды владельца.
- Actual time: общий cohort начат 11-11-2026 20:41 MSK; проверен 11-11-2026 22:40 MSK. Start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: packages/contracts/issues/manager.ts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/tasks/Settings.tsx. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Version registry с description/dates/state; Affects и Fix раздельны, архив сохраняет references; release policy/explicit hotfix, Done не выпускает версию.
- Files touched / work locations: packages/contracts/issues/manager.ts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/tasks/Settings.tsx.
- Technical value delivered: Раздельные affects/fix version references и условия планирования релиза; транзакционные guards и regression checks реализованы.
- Product value delivered: Пользователь различает затронутый продукт и выпуск, который получит исправление.
- Actual implementation date and time: 11-11-2026 22:40
- Verification evidence: full Web 345/345 skip0; browser 88; actual App/native 27; focused negative cases, build/typecheck и independent closed_allowed. [Run evidence](product-agent-os-web-m2-execution-2026-11-11.md), [source hashes/results](product-agent-os-web-m2-results-2026-11-11.json).
- Residual risks: local App-active technical scope; active consumer required, sandbox только PAOS-mediated commands. Human/commercial/release acceptance и AUTH-G1–G6 отдельно; narrow Markdown subset обозначен в UI.
- Follow-up: Остальные 16 M2 tasks, включая PAOS-0036, остаются planned; commercial repeat review PAOS-0030. Эта карточка не закрывает весь M2.


### Task `PAOS-0034`

- Task: Attachments, комментарии и история изменений
- Status: implemented
- Delivery stage: M2
- Execution order: 27
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 22:40
- Depends on: PAOS-0031, PAOS-0007
- Blocks: PAOS-0028
- Source: PRD §14; TM-18, TM-24
- Short description: Managed files, comment revisions и append-only audit событий пользователя/агентов
- Technical value: Managed files, comment revisions и append-only audit событий пользователя/агентов
- Product value: Пользователь добавляет контекст и видит, кто, что и когда изменил
- Scope: apps/local-service/src/attachments; apps/local-service/src/comments; apps/local-service/src/audit; apps/web/src/features/tasks/activity
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Attachments, комментарии и история изменений в будущем Web
- Acceptance criteria: Upload quota/MIME/path checks; source file не меняется; tabs разделены; edits/tombstones/actor attribution и redaction проверены
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 20:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: apps/local-service/src/attachments; apps/local-service/src/comments; apps/local-service/src/audit; apps/web/src/features/tasks/activity
- Next step: Следующий неисполненный M2 scope — PAOS-0036; он требует отдельной команды владельца.
- Actual time: общий cohort начат 11-11-2026 20:41 MSK; проверен 11-11-2026 22:40 MSK. Start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: apps/local-service/src/task-manager/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/local-service/src/storage/snapshot.mts; apps/local-service/src/main.mts; apps/local-service/src/http/application.mts; apps/web/src/features/tasks/Panels.tsx; apps/web/src/features/tasks/CommentMarkdown.tsx; apps/web/src/features/tasks/comment-markdown.ts; apps/web/src/features/tasks/Settings.tsx. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Managed attachment copies/quota/MIME/hash/download-only, retry lost ACK, safe cleanup, comments Markdown/replies/revisions/tombstones, redacted audit и полный local archive/inactive restore.
- Files touched / work locations: apps/local-service/src/task-manager/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/local-service/src/storage/snapshot.mts; apps/local-service/src/main.mts; apps/local-service/src/http/application.mts; apps/web/src/features/tasks/Panels.tsx; apps/web/src/features/tasks/CommentMarkdown.tsx; apps/web/src/features/tasks/comment-markdown.ts; apps/web/src/features/tasks/Settings.tsx.
- Technical value delivered: Managed files, comment revisions и append-only audit событий пользователя/агентов; транзакционные guards и regression checks реализованы.
- Product value delivered: Пользователь добавляет контекст и видит, кто, что и когда изменил.
- Actual implementation date and time: 11-11-2026 22:40
- Verification evidence: full Web 345/345 skip0; browser 88; actual App/native 27; focused negative cases, build/typecheck и independent closed_allowed. [Run evidence](product-agent-os-web-m2-execution-2026-11-11.md), [source hashes/results](product-agent-os-web-m2-results-2026-11-11.json).
- Residual risks: local App-active technical scope; active consumer required, sandbox только PAOS-mediated commands. Human/commercial/release acceptance и AUTH-G1–G6 отдельно; narrow Markdown subset обозначен в UI.
- Follow-up: Остальные 16 M2 tasks, включая PAOS-0036, остаются planned; commercial repeat review PAOS-0030. Эта карточка не закрывает весь M2.


### Task `PAOS-0035`

- Task: Kanban и ручной жизненный цикл задачи
- Status: implemented
- Delivery stage: M2
- Execution order: 29
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 22:40
- Depends on: PAOS-0005, PAOS-0008, PAOS-0032
- Blocks: PAOS-0028, PAOS-0036
- Source: PRD §14; TM-19, TM-20
- Short description: Восемь статусов, семь колонок, transitions/guards, WIP и resolution
- Technical value: Восемь статусов, семь колонок, transitions/guards, WIP и resolution
- Product value: Пользователь сам создаёт, ведёт, закрывает и переоткрывает задачи без обязательного agent run
- Scope: apps/web/src/features/tasks/board; apps/local-service/src/task-workflow
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Kanban и ручной жизненный цикл задачи в будущем Web
- Acceptance criteria: Drag/menu равнозначны; multi-status column требует выбора; manual Done проверяет criteria; Cancelled сохраняет reason; active run ждёт cancel receipt
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: apps/web/src/features/tasks/board; apps/local-service/src/task-workflow
- Next step: Следующий неисполненный M2 scope — PAOS-0036; он требует отдельной команды владельца.
- Actual time: общий cohort начат 11-11-2026 20:41 MSK; проверен 11-11-2026 22:40 MSK. Start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: packages/contracts/issues/task-profile.ts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/tasks/TaskManager.tsx; apps/web/src/features/tasks/Panels.tsx; apps/web/src/features/tasks/Settings.tsx. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: 8 statuses/7 columns, drag/menu через единый transition, явный multi-status outcome, soft/hard WIP с audit, ручные completion/cancel/reopen и безопасный active-run fence.
- Files touched / work locations: packages/contracts/issues/task-profile.ts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/tasks/TaskManager.tsx; apps/web/src/features/tasks/Panels.tsx; apps/web/src/features/tasks/Settings.tsx.
- Technical value delivered: Восемь статусов, семь колонок, transitions/guards, WIP и resolution; транзакционные guards и regression checks реализованы.
- Product value delivered: Пользователь сам создаёт, ведёт, закрывает и переоткрывает задачи без обязательного agent run.
- Actual implementation date and time: 11-11-2026 22:40
- Verification evidence: full Web 345/345 skip0; browser 88; actual App/native 27; focused negative cases, build/typecheck и independent closed_allowed. [Run evidence](product-agent-os-web-m2-execution-2026-11-11.md), [source hashes/results](product-agent-os-web-m2-results-2026-11-11.json).
- Residual risks: local App-active technical scope; active consumer required, sandbox только PAOS-mediated commands. Human/commercial/release acceptance и AUTH-G1–G6 отдельно; narrow Markdown subset обозначен в UI.
- Follow-up: Остальные 16 M2 tasks, включая PAOS-0036, остаются planned; commercial repeat review PAOS-0030. Эта карточка не закрывает весь M2.


### Task `PAOS-0036`

- Task: Редактор, версии и миграции workflow
- Status: implemented
- Delivery stage: M2
- Execution order: 30
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 09:53
- Depends on: PAOS-0035
- Blocks: PAOS-0028, PAOS-0037
- Source: PRD §14; TM-21
- Short description: M2: редактор workflow, type mapping, draft/publish, pinned versions и migration; execution chains отдельно в M3 PAOS-0037
- Technical value: Workflow definitions, type mapping, draft/publish и pinned versions
- Product value: Пользователь создаёт собственный процесс, не меняя незаметно уже идущую работу
- Scope: apps/local-service/src/workflows; apps/web/src/features/workflows; packages/contracts/workflows
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Редактор, версии и миграции workflow в будущем Web
- Acceptance criteria: S25/S26 доступны; invalid graph rejected; publish не меняет v1 runs; migration preview/status mapping/revision guards и rollback проверены
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 20:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: apps/local-service/src/workflows; apps/web/src/features/workflows; packages/contracts/workflows
- Next step: Оставшиеся M2 PAOS-0019/0020/0021/0022/0027 требуют отдельного scope; весь M2 не закрыт.
- Actual time: Общий cohort baseline12-11-2026 08:29 MSK, проверен 12-11-2026 09:53 MSK; start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: packages/contracts/workflows/workflow.ts; packages/contracts/workflows/helpers.ts; apps/local-service/src/workflows/registry.mts; apps/local-service/src/workflows/commands.mts; apps/local-service/src/workflows/guards.mts; apps/local-service/src/workflows/runtime.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/workflows/WorkflowManager.tsx; apps/web/src/features/tasks/TaskManager.tsx; apps/web/src/api/session-target.ts. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: S25/S26 workflow editor, validation/publish, immutable pinned versions, default/type/explicit selection, reviewed cohort migration/CAS and rollback; custom categories retain host guards, recipes remain M2 metadata.
- Files touched / work locations: packages/contracts/workflows/workflow.ts; packages/contracts/workflows/helpers.ts; apps/local-service/src/workflows/registry.mts; apps/local-service/src/workflows/commands.mts; apps/local-service/src/workflows/guards.mts; apps/local-service/src/workflows/runtime.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/features/workflows/WorkflowManager.tsx; apps/web/src/features/tasks/TaskManager.tsx; apps/web/src/api/session-target.ts.
- Technical value delivered: Workflow definitions, type mapping, draft/publish и pinned versions; source contracts и guards проверены.
- Product value delivered: Пользователь создаёт собственный процесс, не меняя незаметно уже идущую работу
- Actual implementation date and time: 12-11-2026 09:53
- Verification evidence: Web375/375 skip0; browser51; actual App/native49; build/typecheck, negative-case regressions и independent source review + root closed_allowed. [Run evidence](product-agent-os-web-m2b-execution-2026-11-12.md), [results](product-agent-os-web-m2b-results-2026-11-12.json).
- Residual risks: Local App-active technical scope; consumer required. History partial for unavailable sources, cursor15min; native loadedVersion unknown, remote discovery unavailable; M3/human/commercial/release отдельно.
- Follow-up: M2 technical21/26; remaining PAOS-0019/0020/0021/0022/0027 planned. AUTH-G1–G6/PAOS-0030 и human/release не закрыты.


### Task `PAOS-0037`

- Task: Цепочки агентов и привязка к workflow
- Status: implemented
- Delivery stage: M3
- Execution order: 47
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 12-11-2026 14:29
- Depends on: PAOS-0036, PAOS-0023
- Blocks: PAOS-0024, PAOS-0028
- Source: PRD §14; TM-22
- Short description: Recipes с branches/join, ownership, budgets и идемпотентным запуском
- Technical value: Recipes с branches/join, ownership, budgets и идемпотентным запуском
- Product value: Пользователь направляет агентов по разным цепочкам для features, bugs и non-code работы
- Scope: packages/contracts/execution-recipes/recipe.ts; apps/local-service/src/execution-recipes (scheduler owner); private App/SQLite/workflow integration; apps/web/src/features/workflows/recipes
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Цепочки агентов и привязка к workflow в будущем Web
- Acceptance criteria: Replay не дублирует run; bounded retry останавливается; parallel writers проверяются; policy нельзя расширить recipe; Manual не запускает agent
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 20:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; react-best-practices; frontend-testing-debugging
- Output artifacts: EVALS.md; PLAN.md; REQUIREMENTS.md; RUNLOG.md; TEST.md; apps/local-service/src/http/application.mts; apps/local-service/src/main.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/team/service.mts; apps/local-service/src/workflows/guards.mts; apps/local-service/src/workflows/registry.mts; apps/web/README.md; apps/web/src/api/client.ts; apps/web/src/design/app.css; apps/web/src/features/workflows/WorkflowManager.tsx; apps/web/src/ui/App.tsx; docs/sources/registry.en.md; docs/sources/registry.md; packages/contracts/runtime/qualified-manifest.json; packages/contracts/storage/local-store.ts; apps/local-service/src/execution-recipes/contract.mts; apps/local-service/src/execution-recipes/pins.mts; apps/local-service/src/execution-recipes/service.mts; apps/web/src/features/workflows/recipes/RecipeRunner.tsx; packages/contracts/execution-recipes/recipe.ts; research/product-agent-os-web-m3-0037-execution-2026-11-12.md; tests/web/execution-recipes.test.mts; tests/web/recipe-pins.test.mts; tests/web/recipe-runtime.test.mts; tests/web/single-window/m3-recipes-acceptance.mts; research/product-agent-os-web-task-manager-plan-2026-11-09.md; research/product-agent-os-web-task-manager-task-group-2026-11-09.json; research/product-agent-os-web-m3-0037-results-2026-11-12.json
- Next step: Следующая PAOS-0024: общая очередь и single coordinator. Реализация требует отдельного scope; PAOS-0025/0026/0028 остаются planned.
- Actual time: Measured scope start12-11-2026 13:28:07 MSK; end 12-11-2026 14:29 MSK. Wall interval available, active duration not separately instrumented; duration=null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: EVALS.md (modify); PLAN.md (modify); REQUIREMENTS.md (modify); RUNLOG.md (modify); TEST.md (modify); apps/local-service/src/http/application.mts (modify); apps/local-service/src/main.mts (modify); apps/local-service/src/runtime/app-agent-gateway.mts (modify); apps/local-service/src/storage/sqlite-worker.mts (modify); apps/local-service/src/task-manager/service.mts (modify); apps/local-service/src/team/service.mts (modify); apps/local-service/src/workflows/guards.mts (modify); apps/local-service/src/workflows/registry.mts (modify); apps/web/README.md (modify); apps/web/src/api/client.ts (modify); apps/web/src/design/app.css (modify); apps/web/src/features/workflows/WorkflowManager.tsx (modify); apps/web/src/ui/App.tsx (modify); docs/sources/registry.en.md (modify); docs/sources/registry.md (modify); packages/contracts/runtime/qualified-manifest.json (modify); packages/contracts/storage/local-store.ts (modify); apps/local-service/src/execution-recipes/contract.mts (create); apps/local-service/src/execution-recipes/pins.mts (create); apps/local-service/src/execution-recipes/service.mts (create); apps/web/src/features/workflows/recipes/RecipeRunner.tsx (create); packages/contracts/execution-recipes/recipe.ts (create); research/product-agent-os-web-m3-0037-execution-2026-11-12.md (create); tests/web/execution-recipes.test.mts (create); tests/web/recipe-pins.test.mts (create); tests/web/recipe-runtime.test.mts (create); tests/web/single-window/m3-recipes-acceptance.mts (create); research/product-agent-os-web-task-manager-plan-2026-11-09.md (modify); research/product-agent-os-web-task-manager-task-group-2026-11-09.json (modify); research/product-agent-os-web-m3-0037-results-2026-11-12.json (create)

#### Completion Report

- Status: implemented
- What was done: Pinned workflow recipes, exact asset versions, finite branch/join/retry scheduler, transactional task ownership, policy-bound private App attempts, Manual0 и reviewed UI transitions реализованы. Replay/recovery/timeout findings исправлены.
- Files touched / work locations: EVALS.md; PLAN.md; REQUIREMENTS.md; RUNLOG.md; TEST.md; apps/local-service/src/http/application.mts; apps/local-service/src/main.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/team/service.mts; apps/local-service/src/workflows/guards.mts; apps/local-service/src/workflows/registry.mts; apps/web/README.md; apps/web/src/api/client.ts; apps/web/src/design/app.css; apps/web/src/features/workflows/WorkflowManager.tsx; apps/web/src/ui/App.tsx; docs/sources/registry.en.md; docs/sources/registry.md; packages/contracts/runtime/qualified-manifest.json; packages/contracts/storage/local-store.ts; apps/local-service/src/execution-recipes/contract.mts; apps/local-service/src/execution-recipes/pins.mts; apps/local-service/src/execution-recipes/service.mts; apps/web/src/features/workflows/recipes/RecipeRunner.tsx; packages/contracts/execution-recipes/recipe.ts; research/product-agent-os-web-m3-0037-execution-2026-11-12.md; tests/web/execution-recipes.test.mts; tests/web/recipe-pins.test.mts; tests/web/recipe-runtime.test.mts; tests/web/single-window/m3-recipes-acceptance.mts; research/product-agent-os-web-task-manager-plan-2026-11-09.md; research/product-agent-os-web-task-manager-task-group-2026-11-09.json; research/product-agent-os-web-m3-0037-results-2026-11-12.json
- Technical value delivered: Durable pinned execution owner сохраняет CAS/idempotency, deep ownership/join и существующие policy/approval guards.
- Product value delivered: Пользователь связывает recipe с переходом, видит preview/versions/budgets и историю, ведёт задачу вручную либо через конечную проверяемую цепочку.
- Actual implementation date and time: 12-11-2026 14:29
- Verification evidence: Web433/433 skip0; recipe20; Python1450(skip1); fixtures91/transcripts26; browser/native57 и actual App46/two steps; exact native candidate/default; docs/compatibility gates — research/product-agent-os-web-m3-0037-execution-2026-11-12.md и results JSON.
- Residual risks: Active App consumer required; PAOS-mediated commands only, host tools не confined. Execution phase in_progress; interrupted/unknown work не replay. Token/cost/performance/model-quality и human/commercial/release acceptance отдельно.
- Follow-up: Следующая PAOS-0024: общая очередь и single coordinator. Реализация требует отдельного scope; PAOS-0025/0026/0028 остаются planned.


### Task `PAOS-0038`

- Task: Linked Issues и блокирующие зависимости
- Status: implemented
- Delivery stage: M2
- Execution order: 28
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 22:40
- Depends on: PAOS-0031, PAOS-0007
- Blocks: PAOS-0024, PAOS-0028
- Source: PRD §14; TM-23
- Short description: Canonical typed edges, inverse display, DAG blocking и авторство
- Technical value: Canonical typed edges, inverse display, DAG blocking и авторство
- Product value: Пользователь и агенты связывают работы и понимают, что мешает продолжению
- Scope: apps/local-service/src/issue-links; apps/web/src/features/tasks/links; packages/contracts/issue-links
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Linked Issues и блокирующие зависимости в будущем Web
- Acceptance criteria: Self/duplicate/cyclic blocks rejected; relates не блокирует; cancellation blocker требует решения; обе стороны и history согласованы
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 14:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: apps/local-service/src/issue-links; apps/web/src/features/tasks/links; packages/contracts/issue-links
- Next step: Следующий неисполненный M2 scope — PAOS-0036; он требует отдельной команды владельца.
- Actual time: общий cohort начат 11-11-2026 20:41 MSK; проверен 11-11-2026 22:40 MSK. Start/duration отдельно по карточкам не измерены, null сохранён.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: packages/contracts/issues/task-profile.ts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/local-service/src/commands/domain-tools.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/web/src/features/tasks/Panels.tsx. Actual operations — matching JSON task.

#### Completion Report

- Status: implemented
- What was done: Canonical typed/inverse links, DAG/cycle path/canonical duplicates, mixed legacy preservation, cancelled blocker остаётся blocking; pending Stop закреплён за original run до ACK.
- Files touched / work locations: packages/contracts/issues/task-profile.ts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/local-service/src/commands/domain-tools.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/web/src/features/tasks/Panels.tsx.
- Technical value delivered: Canonical typed edges, inverse display, DAG blocking и авторство; транзакционные guards и regression checks реализованы.
- Product value delivered: Пользователь и агенты связывают работы и понимают, что мешает продолжению.
- Actual implementation date and time: 11-11-2026 22:40
- Verification evidence: full Web 345/345 skip0; browser 88; actual App/native 27; focused negative cases, build/typecheck и independent closed_allowed. [Run evidence](product-agent-os-web-m2-execution-2026-11-11.md), [source hashes/results](product-agent-os-web-m2-results-2026-11-11.json).
- Residual risks: local App-active technical scope; active consumer required, sandbox только PAOS-mediated commands. Human/commercial/release acceptance и AUTH-G1–G6 отдельно; narrow Markdown subset обозначен в UI.
- Follow-up: Остальные 16 M2 tasks, включая PAOS-0036, остаются planned; commercial repeat review PAOS-0030. Эта карточка не закрывает весь M2.

### Task `PAOS-0039`

- Task: Допустимые auth routes и коммерческие границы
- Status: implemented
- Delivery stage: M1
- Execution order: 3
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 08:09
- Depends on: PAOS-0001
- Blocks: PAOS-0041, PAOS-0047
- Source: PRD §15 SW-01–12; auth/commercial AUTH-G1–G6
- Short description: Зафиксировать owner-default Codex App agents без API key, explicit BYOK compatibility и коммерческие границы
- Technical value: Зафиксировать owner-default Codex App agents без API key, explicit BYOK compatibility и коммерческие границы
- Product value: Пользователь знает доступный способ подключения и плательщика до начала работы.
- Scope: research/product-agent-os-web-auth-commercial-2026-11-09.md; packages/contracts/auth
- Non-goals: Не менять hooks/global permissions; не запускать внешний/provider/Git/release scope без отдельного разрешения
- Expected result: Для local engineering preview выбран codex_app_agent / owner_default без API key; API BYOK остаётся explicit_compatibility с user_api_account. Connection проверяет leased agent channel, не native sandbox/model entitlement; commercial/hosted distribution ожидает AUTH-G1–G6.
- Acceptance criteria: Local route decision соответствует PRD §17.6 и auth §8: codex_app_agent owner_default без API key; BYOK только explicit_compatibility, без fallback и inherited cache. SIWC требует admission; commercial/hosted distribution блокируется до AUTH-G1–G6 и PAOS-0046/0030.
- Verification gates: Focused contract/negative tests; authorized runtime/browser where needed; no fixture-only activation claim
- Risks / approval gates: Неоднозначные условия или отсутствие коммерческого допуска. Provider calls, registration and publication require separate authority.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 06:00:00 (предварительно)
- Agents: product-manager, architect, security-privacy-supply-chain-reviewer
- Skills: implementation-planner; task-matching skills selected at start
- Output artifacts: research/product-agent-os-web-auth-commercial-2026-11-09.md; packages/contracts/auth
- Next step: Продолжить PAOS-0042/0043/0044 и PAOS-0045 по App-dependent addendum; не выдавать reasoning relay за полную execution/owner acceptance.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-auth-commercial-2026-11-09.md
- Affected files: proposed paths above; actual create/modify/delete receipts only after execution.

#### Completion Report

- Status: implemented
- What was done: Исходный API contract 08:09 сохранён как explicit compatibility; по решению владельца текущий default — codex_app_agent без API key. Реальный App-worker reasoning/result 17:50–17:51 проверен 16/16; execution boundary не подтверждён.
- Files touched / work locations: packages/contracts/auth/m1-route.ts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/runtime/route-selector.ts; tests/web/auth-route.test.mts; tests/web/app-agent-gateway.test.mts; tests/web/runtime-route-selector.test.mts; research/product-agent-os-web-auth-commercial-2026-11-09.md.
- Technical value delivered: Сквозные local contracts и отрицательные сценарии проверены без обхода authority.
- Product value delivered: Данные/границы работы доступны в локальном приложении с явным unavailable/partial состоянием.
- Actual implementation date and time: 11-11-2026 08:09
- Verification evidence: Web 150/150; strict/build exit 0; headless 33; Python 1450 (skip 1), fixture 91/91, transcript 26/26, compatibility compatible. [Текущий отчёт](product-agent-os-web-m1-execution-2026-11-11.md). [Историческая квалификация](product-agent-os-web-m1-initial-qualification-2026-11-10.md). Follow-up 11-11-2026: actual App-agent receipt 9TDdwj 16/16, Web238/238, strict0/build36 Cfgug4Ze; старые receipts не переобозначены как новые.
- Residual risks: App host identity attested; automatic wakeup/native permission boundary не доказаны, Execution blocked. SIWC/inherited login недоступны; commercial review PAOS-0046/0030 не выполнен.
- Follow-up: Продолжить PAOS-0042/0043/0044 и PAOS-0045 по App-dependent addendum; не выдавать reasoning relay за полную execution/owner acceptance.

Историческая запись до нативной проверки 11 ноября (не текущий статус):

> - Status: blocked
> - What was done: Реализовано fail-closed решение маршрута локального engineering preview.
> - Files touched / work locations: `packages/contracts/auth/m1-route.ts`, `tests/web/auth-route.test.mts`, `research/product-agent-os-web-auth-commercial-2026-11-09.md`.
> - Technical value delivered: Local BYOK отделён от managed login, SIWC, commercial и hosted.
> - Product value delivered: Плательщик локального preview известен, entitlement остаётся `unverified`.
> - Actual implementation date and time: pending_execution_timestamp
> - Verification evidence: `node --test tests/web/auth-route.test.mts` — 2/2 после RED.
> - Residual risks: AUTH-G1 ждёт решения владельца по paid/OSS, entity и рынкам. Допуск и фактический auth отдельно.
> - Follow-up: Зафиксировать точный коммерческий канал и затем проверить условия выбранного route.

### Task `PAOS-0040`

- Task: Launcher и жизненный цикл локального приложения
- Status: implemented
- Delivery stage: M1
- Execution order: 7
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 16:09
- Depends on: PAOS-0001
- Blocks: PAOS-0041
- Source: PRD §15 SW-01–12; auth/commercial AUTH-G1–G6
- Short description: Запуск service и UI, version/health checks, single instance, explicit install и graceful Quit
- Technical value: Запуск service и UI, version/health checks, single instance, explicit install и graceful Quit
- Product value: Работу можно начать ярлыком и понять, что продолжает выполняться после закрытия окна.
- Scope: apps/launcher; apps/local-service/src/supervisor
- Non-goals: Не менять hooks/global permissions; не запускать внешний/provider/Git/release scope без отдельного разрешения
- Expected result: UI запускается без Codex App; missing runtime/offline/second instance/Quit показывают корректные состояния, не выполняют скрытых install или inference.
- Acceptance criteria: UI запускается без Codex App; missing runtime/offline/second instance/Quit показывают корректные состояния, не выполняют скрытых install или inference.
- Verification gates: Focused contract/negative tests; authorized runtime/browser where needed; no fixture-only activation claim
- Risks / approval gates: Orphan processes, зависший shutdown, несовместимый runtime. Provider calls, registration and publication require separate authority.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: builder, tester
- Skills: implementation-planner; task-matching skills selected at start
- Output artifacts: apps/launcher; apps/local-service/src/supervisor
- Next step: PAOS-0042/0043/0044 provider-backed gates, затем0045; повторный ручной launcher тест владельцем не требуется.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-auth-commercial-2026-11-09.md
- Affected files: proposed paths above; actual create/modify/delete receipts only after execution.

#### Completion Report

- Status: implemented
- What was done: Технический SW-02 launcher/local lifecycle подтверждён составными native closed-App и актуальным autonomous browser56 receipts; guided pairing UI исправлен, ручная работа владельцу не требуется.
- Files touched / work locations: tests/web/single-window/autonomous-launcher-acceptance.mts; tests/web/launcher-standalone.test.mts; apps/web/src/api/client.ts; apps/web/src/ui/App.tsx; apps/web/src/locales/app.ts.
- Technical value delivered: Production launcher/service, source hashes, single instance, local/offline gating, authenticated Quit и cleanup проверены.
- Product value delivered: Локальное приложение запускается самостоятельно; отсутствие сессии объясняется, разделы доступны после pairing.
- Actual implementation date and time: 11-11-2026 16:09
- Verification evidence: Текущий follow-up: Web197/197 no skips; browser669; autonomous launcher56; strict/build35 exit0. Native BVldIt closed-App25 samples, source hashes совпадают; owner accepted=false сохранён. Это разные прогоны. [Execution report](product-agent-os-web-m1-execution-2026-11-11.md).
- Residual risks: Обязательных technical gaps SW-02 нет. Human product acceptance/rejected historical manual journey и полный SW-AC-01/10/provider turn не объявлены passed; их owning gate0045.
- Follow-up: Продолжить0042/0043/0044 по отдельной provider authority;0045 остаётся blocked.

### Task `PAOS-0041`

- Task: Локальное API-подключение и credential isolation
- Status: implemented
- Delivery stage: M1
- Execution order: 8
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 08:46
- Depends on: PAOS-0039, PAOS-0040, PAOS-0054
- Blocks: PAOS-0042
- Source: PRD §17; architecture §21; plan v0.7; audit WA-01–13
- Short description: Connection broker, secure store, payer/capabilities, disconnect и API profile без inherited login
- Technical value: Connection broker, secure store, payer/capabilities, disconnect и API profile без inherited login
- Product value: Пользователь подключает свой API account и контролирует расходы и данные.
- Scope: apps/local-service/src/connections; apps/web/src/settings/connections; packages/contracts/auth
- Non-goals: Не менять hooks/global permissions; не запускать внешний/provider/Git/release scope без отдельного разрешения
- Expected result: Локальное API-подключение и credential isolation — реализовано и проверено в назначенном этапе
- Acceptance criteria: Login state отличается от model access; secrets не попадают в logs/SQLite/browser storage/tool environment; disconnect останавливает новые calls; no fallback доказан. Auth §7 pairing/cookie/CSRF, Credential Manager + ephemeral RPC auth, no implicit fallback.
- Verification gates: Focused contract/negative tests; authorized runtime/browser where needed; no fixture-only activation claim
- Risks / approval gates: Credential leakage, неверный payer или недоказанная isolation.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: builder, security-privacy-supply-chain-reviewer, tester
- Skills: implementation-planner; task-matching skills selected at start
- Output artifacts: apps/local-service/src/connections; apps/web/src/settings/connections; packages/contracts/auth
- Next step: Передать local auth consumers PAOS-0042; полная приёмка PAOS-0045 сохраняет запрещённые provider/browser gates.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-auth-commercial-2026-11-09.md
- Affected files: proposed paths above; actual create/modify/delete receipts only after execution.

#### Completion Report

- Status: implemented
- What was done: Local API broker, ephemeral RPC auth, no fallback и native Windows Credential Manager квалифицированы на synthetic data; typed account.type apiKey и modelAccess unverified подтверждены настоящим App Server без inference.
- Files touched / work locations: apps/local-service/src/connections; apps/local-service/src/runtime/native-rpc.mts; apps/web/src/ui.
- Technical value delivered: Сквозные local contracts и отрицательные сценарии проверены без обхода authority.
- Product value delivered: Данные/границы работы доступны в локальном приложении с явным unavailable/partial состоянием.
- Actual implementation date and time: 11-11-2026 08:46
- Verification evidence: Native vault write/read/delete и verified absence, exit 0; actual broker + isolated stdio login/read/logout, typed apiKey, zero turns, revoked authorization, no canary files, clean process/profile. Web 159/159, no skips. [Текущий отчёт](product-agent-os-web-m1-execution-2026-11-11.md). [Историческая квалификация](product-agent-os-web-m1-initial-qualification-2026-11-10.md).
- Residual risks: Local auth components qualified; custom offline provider does not prove production OpenAI selector activation or entitlement. Model access remains unverified by design; provider/browser acceptance belongs to PAOS-0042/0045. Network zero was not instrumented; discovery-off/loopback gates verified.
- Follow-up: PAOS-0042/0045 в разрешённом scope; реальный provider и browser не запускать без отдельной authority.

### Task `PAOS-0042`

- Task: Codex App Server adapter и ограниченное выполнение
- Status: implemented
- Delivery stage: M1
- Execution order: 11
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 19:53
- Depends on: PAOS-0041, PAOS-0002, PAOS-0003, PAOS-0048, PAOS-0055
- Blocks: PAOS-0043
- Source: PRD §17; architecture §21; plan v0.7; audit WA-01–13
- Short description: Pinned stdio protocol, project/task/run/thread/turn binding, allowlist и одна минимальная recipe
- Technical value: Pinned stdio protocol, project/task/run/thread/turn binding, allowlist и одна минимальная recipe
- Product value: Codex выполняет задачу непосредственно из PAOS в заданных границах.
- Scope: apps/local-service/src/runtime/codex; packages/contracts/runtime
- Non-goals: Не менять hooks/global permissions; не запускать внешний/provider/Git/release scope без отдельного разрешения
- Expected result: Codex App Server adapter и ограниченное выполнение — реализовано и проверено в назначенном этапе
- Acceptance criteria: Owner-selected App-active contract PRD §17.7 / architecture §21.10. Настоящий App worker и qualified offline native command broker: Discussion/Planning write deny, Execution inside write/outside+TEMP deny, PAOS domain approvals, idempotency, actual diffs/checks и native Stop. Ключ API/auth cache не используются. Техническая приёмка только App-active/PAOS-mediated commands; Desktop daemon, whole-App/read sandbox, automatic wakeup и реальный ChatGPT account-switch не заявляются. Human product acceptance и AUTH-G1–G6/0046/0030 отдельно.
- Verification gates: Focused contract/negative tests; authorized runtime/browser where needed; no fixture-only activation claim
- Risks / approval gates: Protocol drift, duplicate dispatch, превышение authority.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 20:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching skills selected at start
- Output artifacts: apps/local-service/src/runtime/codex; packages/contracts/runtime
- Next step: PAOS-0046 — отдельный commercial review; не выполнять publication или внешний release этим закрытием.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-auth-commercial-2026-11-09.md
- Affected files: proposed paths above; actual create/modify/delete receipts only after execution.

#### Completion Report

- Status: implemented
- What was done: Настоящий App worker и qualified offline native command broker: Discussion/Planning write deny, Execution inside write/outside+TEMP deny, PAOS domain approvals, idempotency, actual diffs/checks и native Stop. Ключ API/auth cache не используются.
- Files touched / work locations: apps/local-service/src/runtime; packages/contracts/runtime; tests/web/runtime*.test.mts.
- Technical value delivered: Сквозные local contracts и отрицательные сценарии проверены без обхода authority.
- Product value delivered: Данные/границы работы доступны в локальном приложении с явным unavailable/partial состоянием.
- Actual implementation date and time: 11-11-2026 19:53
- Verification evidence: Текущие команды, counts, source hashes, RED/GREEN, failed receipts и AC map: [App-mediated native broker](product-agent-os-web-m1-execution-2026-11-11.md#app-mediated-native-broker--техническая-приёмка-m1) и execution-results JSON; исходный closed-App full-turn не объявлен passed.
- Residual risks: Техническая приёмка только App-active/PAOS-mediated commands; Desktop daemon, whole-App/read sandbox, automatic wakeup и реальный ChatGPT account-switch не заявляются. Human product acceptance и AUTH-G1–G6/0046/0030 отдельно.
- Follow-up: PAOS-0046 — ранний commercial review перед M2; технические M1 gaps закрыты в выбранном маршруте.

### Task `PAOS-0043`

- Task: Активная сессия и минимальная карточка задачи
- Status: implemented
- Delivery stage: M1
- Execution order: 12
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 19:53
- Depends on: PAOS-0042, PAOS-0004, PAOS-0048
- Blocks: PAOS-0010, PAOS-0044
- Source: PRD §17; architecture §21; plan v0.7; audit WA-01–13
- Short description: Composer discussion/planning/execution, streaming, task draft и панель diff/checks/decisions без полного board
- Technical value: Composer discussion/planning/execution, streaming, task draft и панель diff/checks/decisions без полного board
- Product value: Пользователь проходит от запроса к результату в одном рабочем окне.
- Scope: apps/web/src/sessions; apps/web/src/tasks/minimal; apps/local-service/src/conversations
- Non-goals: Не менять hooks/global permissions; не запускать внешний/provider/Git/release scope без отдельного разрешения
- Expected result: Активная сессия и минимальная карточка задачи — реализовано и проверено в назначенном этапе
- Acceptance criteria: SW-AC-01/03/04/08: все действия в PAOS; discussion не пишет target; Send/Stop имеют ACK; linked task содержит scope/criteria/estimate, turn success не закрывает её автоматически. M1 Task CRUD/manual closure/Comments/History/links, read-only agent/skill catalogs, fixed Kanban, RU/EN/themes; UX owners по v0.7, без зависимости от M2 editors.
- Verification gates: Focused contract/negative tests; authorized runtime/browser where needed; no fixture-only activation claim
- Risks / approval gates: Смешение task/comment/session или ложное завершение.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 20:00:00 (предварительно)
- Agents: builder, tester
- Skills: implementation-planner; task-matching skills selected at start
- Output artifacts: apps/web/src/sessions; apps/web/src/tasks/minimal; apps/local-service/src/conversations
- Next step: PAOS-0046 — отдельный commercial review; не выполнять publication или внешний release этим закрытием.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-auth-commercial-2026-11-09.md
- Affected files: proposed paths above; actual create/modify/delete receipts only after execution.

#### Completion Report

- Status: implemented
- What was done: Связанный browser/App/native путь и Task lifecycle: CRUD/conflict, Comments, durable подробная History, links, draft/context/scroll, checks, ручное решение о Done и reopen. Завершение run не закрывает Task автоматически.
- Files touched / work locations: apps/web; apps/local-service/src/http; apps/local-service/src/tasks.
- Technical value delivered: Сквозные local contracts и отрицательные сценарии проверены без обхода authority.
- Product value delivered: Данные/границы работы доступны в локальном приложении с явным unavailable/partial состоянием.
- Actual implementation date and time: 11-11-2026 19:53
- Verification evidence: Текущие команды, counts, source hashes, RED/GREEN, failed receipts и AC map: [App-mediated native broker](product-agent-os-web-m1-execution-2026-11-11.md#app-mediated-native-broker--техническая-приёмка-m1) и execution-results JSON; исходный closed-App full-turn не объявлен passed.
- Residual risks: Техническая приёмка только App-active/PAOS-mediated commands; Desktop daemon, whole-App/read sandbox, automatic wakeup и реальный ChatGPT account-switch не заявляются. Human product acceptance и AUTH-G1–G6/0046/0030 отдельно.
- Follow-up: PAOS-0046 — ранний commercial review перед M2; технические M1 gaps закрыты в выбранном маршруте.

### Task `PAOS-0044`

- Task: Recovery, повторное подключение и сохранённые сессии
- Status: implemented
- Delivery stage: M1
- Execution order: 13
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 19:53
- Depends on: PAOS-0043
- Blocks: PAOS-0025, PAOS-0045, PAOS-0047, PAOS-0056
- Source: PRD §15 SW-01–12; auth/commercial AUTH-G1–G6
- Short description: Durable intents, lost ACK reconciliation, restart/resume, process-bound approvals и account isolation
- Technical value: Durable intents, lost ACK reconciliation, restart/resume, process-bound approvals и account isolation
- Product value: Пользователь продолжает работу после перерыва без потери контекста и повторных изменений.
- Scope: apps/local-service/src/runtime/recovery; apps/web/src/recovery
- Non-goals: Не менять hooks/global permissions; не запускать внешний/provider/Git/release scope без отдельного разрешения
- Expected result: SW-AC-05/06/07/09: crash до/после dispatch не повторяет side effects; pending approval stale после restart; stop timeout показан как unknown; чужой account не продолжает run.
- Acceptance criteria: SW-AC-05/06/07/09: crash до/после dispatch не повторяет side effects; pending approval stale после restart; stop timeout показан как unknown; чужой account не продолжает run.
- Verification gates: Focused contract/negative tests; authorized runtime/browser where needed; no fixture-only activation claim
- Risks / approval gates: Невосстановимый outcome и частично выполненные tools. Provider calls, registration and publication require separate authority.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: builder, tester
- Skills: implementation-planner; task-matching skills selected at start
- Output artifacts: apps/local-service/src/runtime/recovery; apps/web/src/recovery
- Next step: PAOS-0046 — отдельный commercial review; не выполнять publication или внешний release этим закрытием.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-auth-commercial-2026-11-09.md
- Affected files: proposed paths above; actual create/modify/delete receipts only after execution.

#### Completion Report

- Status: implemented
- What was done: Сохранённый выбранный binding, active scope priority после restart, stale approval/capability rejection, same-worker private-state migration, terminal reconcile, no replay и явный cancel только never-dispatched intent; неизвестный native outcome остаётся fenced.
- Files touched / work locations: apps/local-service/src/runtime; apps/web/src/api; tests/web/recovery.test.mts.
- Technical value delivered: Сквозные local contracts и отрицательные сценарии проверены без обхода authority.
- Product value delivered: Данные/границы работы доступны в локальном приложении с явным unavailable/partial состоянием.
- Actual implementation date and time: 11-11-2026 19:53
- Verification evidence: Текущие команды, counts, source hashes, RED/GREEN, failed receipts и AC map: [App-mediated native broker](product-agent-os-web-m1-execution-2026-11-11.md#app-mediated-native-broker--техническая-приёмка-m1) и execution-results JSON; исходный closed-App full-turn не объявлен passed.
- Residual risks: Техническая приёмка только App-active/PAOS-mediated commands; Desktop daemon, whole-App/read sandbox, automatic wakeup и реальный ChatGPT account-switch не заявляются. Human product acceptance и AUTH-G1–G6/0046/0030 отдельно.
- Follow-up: PAOS-0046 — ранний commercial review перед M2; технические M1 gaps закрыты в выбранном маршруте.

### Task `PAOS-0045`

- Task: Приёмка сквозного M1 в одном окне
- Status: implemented
- Delivery stage: M1
- Execution order: 18
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 19:53
- Depends on: PAOS-0044, PAOS-0002, PAOS-0003, PAOS-0049, PAOS-0051, PAOS-0056
- Blocks: PAOS-0028, PAOS-0046
- Source: PRD §17; architecture §21; plan v0.7; audit WA-01–13
- Short description: Проверить launch/connection/chat/task/approval/result/resume и негативные границы на разрешённом runtime
- Technical value: Проверить launch/connection/chat/task/approval/result/resume и негативные границы на разрешённом runtime
- Product value: Первый MVP доказывает самостоятельный пользовательский путь, а не набор статичных экранов.
- Scope: tests/web/single-window; docs/evidence/web-m1
- Non-goals: Не менять hooks/global permissions; не запускать внешний/provider/Git/release scope без отдельного разрешения
- Expected result: Приёмка сквозного M1 в одном окне — реализовано и проверено в назначенном этапе
- Acceptance criteria: Owner-selected App-active contract PRD §17.7 / architecture §21.10. Все применимые SW/ST/UX/DATA M1 gates сопоставлены с actual App/native/browser/storage/workload receipts. Повторные task/data journeys после исправления History и lost-ACK backupId пройдены автономно; technical acceptance отделена от human/commercial/release. Техническая приёмка только App-active/PAOS-mediated commands; Desktop daemon, whole-App/read sandbox, automatic wakeup и реальный ChatGPT account-switch не заявляются. Human product acceptance и AUTH-G1–G6/0046/0030 отдельно.
- Verification gates: Focused contract/negative tests; authorized runtime/browser where needed; no fixture-only activation claim
- Risks / approval gates: Synthetic evidence ошибочно принято за live product proof.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: tester, reviewer
- Skills: implementation-planner; task-matching skills selected at start
- Output artifacts: tests/web/single-window; docs/evidence/web-m1
- Next step: PAOS-0046 — отдельный commercial review; не выполнять publication или внешний release этим закрытием.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-auth-commercial-2026-11-09.md
- Affected files: proposed paths above; actual create/modify/delete receipts only after execution.

#### Completion Report

- Status: implemented
- What was done: Все применимые SW/ST/UX/DATA M1 gates сопоставлены с actual App/native/browser/storage/workload receipts. Повторные task/data journeys после исправления History и lost-ACK backupId пройдены автономно; technical acceptance отделена от human/commercial/release.
- Files touched / work locations: tests/web/single-window; research/product-agent-os-web-m1-execution-2026-11-11.md.
- Technical value delivered: Сквозные local contracts и отрицательные сценарии проверены без обхода authority.
- Product value delivered: Данные/границы работы доступны в локальном приложении с явным unavailable/partial состоянием.
- Actual implementation date and time: 11-11-2026 19:53
- Verification evidence: Текущие команды, counts, source hashes, RED/GREEN, failed receipts и AC map: [App-mediated native broker](product-agent-os-web-m1-execution-2026-11-11.md#app-mediated-native-broker--техническая-приёмка-m1) и execution-results JSON; исходный closed-App full-turn не объявлен passed.
- Residual risks: Техническая приёмка только App-active/PAOS-mediated commands; Desktop daemon, whole-App/read sandbox, automatic wakeup и реальный ChatGPT account-switch не заявляются. Human product acceptance и AUTH-G1–G6/0046/0030 отдельно.
- Follow-up: PAOS-0046 — ранний commercial review перед M2; технические M1 gaps закрыты в выбранном маршруте.

### Task `PAOS-0046`

- Task: Коммерческий review API-варианта и выпускные gates
- Status: implemented
- Delivery stage: POST_M1
- Execution order: 19
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 20:37
- Depends on: PAOS-0045
- Blocks: PAOS-0030, PAOS-0047
- Source: PRD §15 SW-01–12; auth/commercial AUTH-G1–G6
- Short description: Ранний commercial review текущего App-agent default, BYOK/SIWC compatibility, AUTH-G1–G6 и release obligations до M2
- Technical value: Проверить AUTH-G1–G6, выбранные рынки, privacy, distribution licenses, payer, support и owner decision
- Product value: Коммерческий пакет честно описывает подключение, затраты и ограничения.
- Scope: research/product-agent-os-web-auth-commercial-2026-11-09.md; docs/release/web-commercial-review
- Non-goals: Не менять hooks/global permissions; не запускать внешний/provider/Git/release scope без отдельного разрешения
- Expected result: Каждый применимый AUTH gate содержит evidence/owner; нет обещаний без approval. Для API-only SIWC помечен unavailable; task не выполняет publication.
- Acceptance criteria: Каждый применимый AUTH gate содержит evidence/owner; нет обещаний без approval. Для API-only SIWC помечен unavailable; task не выполняет publication. Позиция 19 после PAOS-0045 и до M2: ранний review различает подтверждённые условия, pending evidence/admission и incompatible route; каждый gap имеет owner и запрет соответствующего выпуска. Актуальность условий повторно проверяется в PAOS-0030, ранний review не заменяет release acceptance.
- Verification gates: Focused contract/negative tests; authorized runtime/browser where needed; no fixture-only activation claim
- Risks / approval gates: Нет admission, legal review или достаточных runtime/security evidence. Provider calls, registration and publication require separate authority.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 08:00:00 (предварительно)
- Agents: product-manager, release-operator, security-privacy-supply-chain-reviewer
- Skills: implementation-planner; task-matching skills selected at start
- Output artifacts: research/product-agent-os-web-auth-commercial-2026-11-09.md; docs/release/web-commercial-review
- Next step: В авторизованном PAOS-M2 чате начать PAOS-0031 и согласованную очередь по dependencies; commercial gates повторно закрываются в PAOS-0030, SIWC только после admission.
- Actual time: 00:28:12 elapsed от первого current clock sample; параллельное время агентов не суммируется.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-auth-commercial-2026-11-09.md
- Affected files: proposed paths above; actual create/modify/delete receipts only after execution.

#### Completion Report

- Status: implemented
- What was done: Проверены11 source groups и текущая реализация; составлены6 AUTH gate rows и8 release gaps с owners/blocks. App bridge commercial qualification unresolved; локальная инженерная M2 может продолжаться. No API key, runtime/policy/publication change.
- Files touched / work locations: research/product-agent-os-web-commercial-review-2026-11-11.md; docs/release/web-commercial-review.json; research/product-agent-os-web-auth-commercial-2026-11-09.md; source-owned card/JSON; paired registries; REQUIREMENTS/PLAN/TEST/RUNLOG.
- Technical value delivered: Подтверждённые факты, inferred applicability и pending admission разделены; отсутствует ложная эквивалентность App Server auth, API Customer Applications и собственного App bridge.
- Product value delivered: Перед M2 определены границы payer/data/license/distribution/support; закрытие исследования отделено от commercial approval.
- Actual implementation date and time: 11-11-2026 20:37
- Verification evidence: Official sources retrieved2026-11-11; independent bounded review closed_allowed; auth-route2/2 +4 negative assertions; docs105/105,8.865s/checker/matrix/diff0. [Review и точный provenance](product-agent-os-web-commercial-review-2026-11-11.md), machine release packet docs/release/web-commercial-review.json. M1 runtime receipts не запускались повторно.
- Residual risks: Commercial release blocked AUTH-G1–G6/C46-01–08: entity/markets/license/bridgequalification/notices/privacy/retention/hostusage/support. No full gate passed; это не blocker текущего local engineering M2.
- Follow-up: Owner-authorized command в PAOS-M2 только после текущих mandatory checks; PAOS-0030 rechecks all applicable release gaps, PAOS-0047 remains admission-gated.


### Task `PAOS-0047`

- Task: Опциональный Sign in with ChatGPT
- Status: planned
- Delivery stage: OPTIONAL
- Execution order: 54
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0039, PAOS-0044, PAOS-0046
- Blocks: none
- Source: PRD §15 SW-01–12; auth/commercial AUTH-G1–G6
- Short description: После допуска реализовать отдельный SIWC route, consent, PKCE/scopes, refresh/restart/resume и preview capability matrix
- Technical value: После допуска реализовать отдельный SIWC route, consent, PKCE/scopes, refresh/restart/resume и preview capability matrix
- Product value: Eligible пользователь может использовать разрешённый ChatGPT plan без второго рабочего приложения.
- Scope: apps/local-service/src/connections/siwc; apps/web/src/settings/connections
- Non-goals: Не менять hooks/global permissions; не запускать внешний/provider/Git/release scope без отдельного разрешения
- Expected result: Только после подтверждённого admission exact paid/local route: identity и plan scope проверены, refresh/resume не дублирует работу, unsupported tools скрыты с причиной; API route не зависит от этой задачи.
- Acceptance criteria: Только после подтверждённого admission exact paid/local route: identity и plan scope проверены, refresh/resume не дублирует работу, unsupported tools скрыты с причиной; API route не зависит от этой задачи.
- Verification gates: Focused contract/negative tests; authorized runtime/browser where needed; no fixture-only activation claim
- Risks / approval gates: Admission отсутствует; preview restrictions изменяются; refresh прерывает активный turn. Provider calls, registration and publication require separate authority.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 20:00:00 (предварительно)
- Agents: builder, security-privacy-supply-chain-reviewer, tester
- Skills: implementation-planner; task-matching skills selected at start
- Output artifacts: apps/local-service/src/connections/siwc; apps/web/src/settings/connections
- Next step: Подтвердить зависимости, доступность route и отдельный implementation scope
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-auth-commercial-2026-11-09.md
- Affected files: proposed paths above; actual create/modify/delete receipts only after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0048`

- Task: SQLite: схема и транзакционные команды
- Status: implemented
- Delivery stage: M1
- Execution order: 9
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected SQLite/FTS5 local and PostgreSQL/pgvector team, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 08:09
- Depends on: PAOS-0001, PAOS-0002, PAOS-0003, PAOS-0054
- Blocks: PAOS-0042, PAOS-0043, PAOS-0049, PAOS-0050, PAOS-0051, PAOS-0052, PAOS-0055
- Source: PRD §17; architecture §21; plan v0.7; audit WA-01–13
- Short description: Создать versioned operational schema и repository adapter; entity/audit/outbox commit, revision/idempotency, legacy authority gate
- Technical value: Создать versioned operational schema и repository adapter; entity/audit/outbox commit, revision/idempotency, legacy authority gate
- Product value: Задачи, сессии и работа агентов сохраняются согласованно после перезапуска.
- Scope: apps/local-service/src/storage/sqlite; packages/contracts/storage; apps/local-service/src/storage/migrations
- Non-goals: Не менять глобальные permissions/hooks; не делать local semantic store или bidirectional sync; внешние операции отдельно разрешаются
- Expected result: SQLite: схема и транзакционные команды — реализовано и проверено в назначенном этапе
- Acceptance criteria: ST-01–04/09: FK/project isolation, duplicate/conflicting command, concurrent writers и transaction crash; legacy tasks остаются file-owned до cutover; current consumers используют adapter
- Verification gates: Focused contract/failure-injection tests; migration/restore fixtures; relevant browser journey; real DB acceptance before closure
- Risks / approval gates: Потеря транзакционности; legacy consumers обходят authority; несовместимый SQLite build
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/storage/sqlite; packages/contracts/storage; apps/local-service/src/storage/migrations
- Next step: Передать локальный контракт потребителям; оставшиеся gates — PAOS-0045.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-storage-research-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: implemented
- What was done: Dedicated SQLite Worker, FK/project scope, revisions/authority epoch, key allocation, atomic entity/audit/outbox, idempotency и crash rollback реализованы.
- Files touched / work locations: apps/local-service/src/storage; packages/contracts/storage; tests/web/storage.test.mts.
- Technical value delivered: Сквозные local contracts и отрицательные сценарии проверены без обхода authority.
- Product value delivered: Данные/границы работы доступны в локальном приложении с явным unavailable/partial состоянием.
- Actual implementation date and time: 11-11-2026 08:09
- Verification evidence: Web 150/150; strict/build exit 0; headless 33; Python 1450 (skip 1), fixture 91/91, transcript 26/26, compatibility compatible. [Текущий отчёт](product-agent-os-web-m1-execution-2026-11-11.md). [Историческая квалификация](product-agent-os-web-m1-initial-qualification-2026-11-10.md).
- Residual risks: Local single-principal profile; team profile отдельно T1. Произвольные legacy writers не объявляются совместимыми.
- Follow-up: Передать локальный контракт потребителям; оставшиеся gates — PAOS-0045.

### Task `PAOS-0049`

- Task: Локальный полнотекстовый поиск FTS5
- Status: implemented
- Delivery stage: M1
- Execution order: 14
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected SQLite/FTS5 local and PostgreSQL/pgvector team, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 08:09
- Depends on: PAOS-0048
- Blocks: PAOS-0045, PAOS-0052
- Source: PRD §16 ST-01–12; architecture §20; storage decision v0.6
- Short description: Индексировать разрешённые entities и file/message projections; exact ID/path lookup, revision-aware jobs, delete/rebuild/coverage
- Technical value: Индексировать разрешённые entities и file/message projections; exact ID/path lookup, revision-aware jobs, delete/rebuild/coverage
- Product value: Пользователь находит задачи и доступный контекст без отправки данных внешней модели.
- Scope: apps/local-service/src/search; apps/web/src/search
- Non-goals: Не менять глобальные permissions/hooks; не делать local semantic store или bidirectional sync; внешние операции отдельно разрешаются
- Expected result: Локальный полнотекстовый поиск FTS5 реализовано и проверено в назначенном этапе
- Acceptance criteria: ST-06/12: RU/EN, exact ID, project filters, tombstone, stale job, failed rebuild; provider вызовов нет; snippets не раскрывают скрытые данные
- Verification gates: Focused contract/failure-injection tests; migration/restore fixtures; relevant browser journey; real DB acceptance before closure
- Risks / approval gates: Потеря индекса; утечка project content; неверные ожидания морфологии
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/search; apps/web/src/search
- Next step: Передать локальный контракт потребителям; оставшиеся gates — PAOS-0045.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-storage-research-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: implemented
- What was done: FTS5 RU/EN/exact ID, scope/revision filtering, tombstone/partial/rebuild и bounded search реализованы; финальный workload p95 108,02 ms.
- Files touched / work locations: apps/local-service/src/storage/search-queries.mts; apps/local-service/src/http/application.mts; tests/web/single-window/workload.mts.
- Technical value delivered: Сквозные local contracts и отрицательные сценарии проверены без обхода authority.
- Product value delivered: Данные/границы работы доступны в локальном приложении с явным unavailable/partial состоянием.
- Actual implementation date and time: 11-11-2026 08:09
- Verification evidence: Web 150/150; strict/build exit 0; headless 33; Python 1450 (skip 1), fixture 91/91, transcript 26/26, compatibility compatible. [Текущий отчёт](product-agent-os-web-m1-execution-2026-11-11.md). [Историческая квалификация](product-agent-os-web-m1-initial-qualification-2026-11-10.md).
- Residual risks: Workload выполнен на текущем 20-logical-CPU host; browser/event-to-visible и 4-core baseline не измерены.
- Follow-up: Передать локальный контракт потребителям; оставшиеся gates — PAOS-0045.

### Task `PAOS-0050`

- Task: Предварительный импорт MD/JSON в staging
- Status: implemented
- Delivery stage: M1
- Execution order: 16
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected SQLite/FTS5 local and PostgreSQL/pgvector team, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 08:09
- Depends on: PAOS-0048
- Blocks: PAOS-0056
- Source: PRD §17; architecture §21; plan v0.7; audit WA-01–13
- Short description: Inventory, profile M1 mapping, validation и non-mutating preview; переключение authority принадлежит 0056
- Technical value: Проверить переносимость профиля M1 до остановки writers и переключения authority.
- Product value: Пользователь переносит старые задачи без потери документов и понимает, где теперь редактировать данные.
- Scope: apps/local-service/src/import-export; apps/web/src/projects/migration; packages/contracts/migration
- Non-goals: Не менять глобальные permissions/hooks; не делать local semantic store или bidirectional sync; внешние операции отдельно разрешаются
- Expected result: Предварительный импорт MD/JSON в staging — реализовано и проверено в назначенном этапе
- Acceptance criteria: PRD §17.2: supported schemas/fields/status mapping; MD/JSON dedup; unsupported significant data блокирует cutover; source drift, stable IDs, exact counts и preview без target mutations; authority switch не входит.
- Verification gates: Focused contract/failure-injection tests; migration/restore fixtures; relevant browser journey; real DB acceptance before closure
- Risks / approval gates: Потеря неизвестных полей; concurrent MD edit; двойная запись; unsafe rollback
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/import-export; apps/web/src/projects/migration; packages/contracts/migration
- Next step: Передать локальный контракт потребителям; оставшиеся gates — PAOS-0045.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-storage-research-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: implemented
- What was done: Versioned single/bundle MD+JSON preview сохраняет snapshot/provenance, dedup и conflicts; normalized SQL export возвращается proposal с base revisions.
- Files touched / work locations: apps/local-service/src/import-export/preview.mts; tests/web/import-preview.test.mts.
- Technical value delivered: Сквозные local contracts и отрицательные сценарии проверены без обхода authority.
- Product value delivered: Данные/границы работы доступны в локальном приложении с явным unavailable/partial состоянием.
- Actual implementation date and time: 11-11-2026 08:09
- Verification evidence: Web 150/150; strict/build exit 0; headless 33; Python 1450 (skip 1), fixture 91/91, transcript 26/26, compatibility compatible. [Текущий отчёт](product-agent-os-web-m1-execution-2026-11-11.md). [Историческая квалификация](product-agent-os-web-m1-initial-qualification-2026-11-10.md).
- Residual risks: Непредставимые значимые поля блокируют целый cutover; текущий research source не мигрирован. General merge editor относится к M2.
- Follow-up: Передать локальный контракт потребителям; оставшиеся gates — PAOS-0045.

### Task `PAOS-0051`

- Task: Резервное копирование и восстановление local data
- Status: implemented
- Delivery stage: M1
- Execution order: 15
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected SQLite/FTS5 local and PostgreSQL/pgvector team, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 08:09
- Depends on: PAOS-0048
- Blocks: PAOS-0045, PAOS-0052, PAOS-0056
- Source: PRD §17; architecture §21; plan v0.7; audit WA-01–13
- Short description: Согласованный DB/blob manifest, schema compatibility, restore rehearsal и rollback после новых writes
- Technical value: Согласованный DB/blob manifest, schema compatibility, restore rehearsal и rollback после новых writes
- Product value: Пользователь восстанавливает данные без пропажи вложений и повторного выполнения старых команд.
- Scope: apps/local-service/src/storage/backup; apps/web/src/settings/data
- Non-goals: Не менять глобальные permissions/hooks; не делать local semantic store или bidirectional sync; внешние операции отдельно разрешаются
- Expected result: Резервное копирование и восстановление local data — реализовано и проверено в назначенном этапе
- Acceptance criteria: ST-08/12: missing blob/hash mismatch, disk full, incompatible schema; restore в отдельный каталог; approvals stale; no blind dispatch replay; reverse transfer сохраняет post-cutover deltas Architecture §21.6: visible-message retention/coverage; last 5 managed backups; restore rehearsal до 0056, secrets/runtime threads excluded.
- Verification gates: Focused contract/failure-injection tests; migration/restore fixtures; relevant browser journey; real DB acceptance before closure
- Risks / approval gates: Неполный snapshot; backup на отказавшем диске; восстановление активного разрешения
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/storage/backup; apps/web/src/settings/data
- Next step: Передать локальный контракт потребителям; оставшиеся gates — PAOS-0045.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-storage-research-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: implemented
- What was done: Immutable consistent backup/blob hashes, отдельный restore/recovery generation и preview/explicit managed rotation реализованы; ENOSPC cleanup проверен injection.
- Files touched / work locations: apps/local-service/src/storage/snapshot.mts; apps/local-service/src/storage/restore-worker.mts; tests/web/storage-backup.test.mts.
- Technical value delivered: Сквозные local contracts и отрицательные сценарии проверены без обхода authority.
- Product value delivered: Данные/границы работы доступны в локальном приложении с явным unavailable/partial состоянием.
- Actual implementation date and time: 11-11-2026 08:09
- Verification evidence: Web 150/150; strict/build exit 0; headless 33; Python 1450 (skip 1), fixture 91/91, transcript 26/26, compatibility compatible. [Текущий отчёт](product-agent-os-web-m1-execution-2026-11-11.md). [Историческая квалификация](product-agent-os-web-m1-initial-qualification-2026-11-10.md).
- Residual risks: Restore создаёт отдельный профиль, не переключает активный автоматически; backup private local content без обещания secure erase или encrypted export.
- Follow-up: Передать локальный контракт потребителям; оставшиеся gates — PAOS-0045.

### Task `PAOS-0052`

- Task: Командный профиль PostgreSQL и pgvector
- Status: planned
- Delivery stage: T1
- Execution order: 55
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected SQLite/FTS5 local and PostgreSQL/pgvector team, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0048, PAOS-0049, PAOS-0051, PAOS-0030
- Blocks: PAOS-0053
- Source: PRD §17; architecture §21; plan v0.7; audit WA-01–13
- Short description: После отдельного T1 решения реализовать server repository, dialect migrations, tenancy/RLS, lexical и versioned vector index; hosting/auth/runtime design gate до кода
- Technical value: После отдельного T1 решения реализовать server repository, dialect migrations, tenancy/RLS, lexical и versioned vector index; hosting/auth/runtime design gate до кода
- Product value: Команда работает с общим актуальным состоянием и поиском в пределах своих прав.
- Scope: apps/server/src/storage/postgres; apps/server/src/search; packages/contracts/tenancy
- Non-goals: Не менять глобальные permissions/hooks; не делать local semantic store или bidirectional sync; внешние операции отдельно разрешаются
- Expected result: Командный профиль PostgreSQL и pgvector — реализовано и проверено в назначенном этапе
- Acceptance criteria: ST-10: domain parity, negative tenant/pool tests, filtered search; embedding model/privacy approved; lexical fallback; hosting/auth/runtime placement согласованы; local M4 не зависит от T1
- Verification gates: Focused contract/failure-injection tests; migration/restore fixtures; relevant browser journey; real DB acceptance before closure
- Risks / approval gates: RLS bypass; provider data disclosure/cost; dialect mismatch; отсутствие team authorization design
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 24:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/server/src/storage/postgres; apps/server/src/search; packages/contracts/tenancy
- Next step: Завершить зависимости; подтвердить schema/ownership и проверки до реализации
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-storage-research-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0053`

- Task: Перенос local проекта в team workspace
- Status: planned
- Delivery stage: T1
- Execution order: 56
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected SQLite/FTS5 local and PostgreSQL/pgvector team, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0056, PAOS-0052
- Blocks: none
- Source: PRD §17; architecture §21; plan v0.7; audit WA-01–13
- Short description: Versioned logical export/import, actor/tenant mapping, blob checks, final delta и one-authority handover
- Technical value: Versioned logical export/import, actor/tenant mapping, blob checks, final delta и one-authority handover
- Product value: Пользователь переносит проект команде с прежними задачами и историей без конфликтующих writable копий.
- Scope: apps/server/src/import-export; apps/local-service/src/import-export/team; apps/web/src/projects/transfer
- Non-goals: Не менять глобальные permissions/hooks; не делать local semantic store или bidirectional sync; внешние операции отдельно разрешаются
- Expected result: Перенос local проекта в team workspace — реализовано и проверено в назначенном этапе
- Acceptance criteria: ST-11/ST-AC-08: UUID/key collisions, identity mapping, counts/hashes/FK, final delta, rollback; credentials/pending approvals/commands исключены; local read-only после switch; без bidirectional sync
- Verification gates: Focused contract/failure-injection tests; migration/restore fixtures; relevant browser journey; real DB acceptance before closure
- Risks / approval gates: Потеря последних изменений; привязка чужих credentials; split authority
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/server/src/import-export; apps/local-service/src/import-export/team; apps/web/src/projects/transfer
- Next step: Завершить зависимости; подтвердить schema/ownership и проверки до реализации
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-storage-research-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0054`

- Task: Контракт совместимости M1 и runtime manifest
- Status: implemented
- Delivery stage: M1
- Execution order: 2
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested M1 audit remediation, 2026-11-10
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 08:09
- Depends on: PAOS-0001
- Blocks: PAOS-0041, PAOS-0048, PAOS-0055
- Source: PRD §17; architecture §21; plan v0.7; audit WA-01–13
- Short description: Закрепить candidate tuple, schema/event mapping, mode policy, bootstrap и credential transport до зависимых consumers
- Technical value: Закрепить candidate tuple, schema/event mapping, mode policy, bootstrap и credential transport до зависимых consumers
- Product value: Согласованный M1 сохраняет данные и показывает достоверное состояние работы в одном окне.
- Scope: packages/contracts/runtime; docs/evidence/web-m1/compatibility
- Non-goals: Не менять глобальные permissions/hooks; не делать local semantic store или bidirectional sync; внешние операции отдельно разрешаются
- Expected result: Контракт совместимости M1 и runtime manifest — реализовано и проверено в назначенном этапе
- Acceptance criteria: Architecture §21.4–21.5 и auth §7: exact versions/hashes/schema/capabilities; negative policy/secret fixtures; no provider inference без отдельного разрешения; unsupported tuple блокирует зависимые задачи.
- Verification gates: Focused contract/failure-injection tests; migration/restore fixtures; relevant browser journey; real DB acceptance before closure
- Risks / approval gates: Неподдержанная runtime/schema capability; потеря данных или ложный success при неполном evidence.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: packages/contracts/runtime; docs/evidence/web-m1/compatibility
- Next step: Передать локальный контракт потребителям; оставшиеся gates — PAOS-0045.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-storage-research-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: implemented
- What was done: Exact native-offline manifest закрепляет OS/build/binaries/schema/SQLite/lock и executable host revision. Native MXC ready, inside written/outside denied; ephemeral synthetic login/logout/canary проверены.
- Files touched / work locations: packages/contracts/runtime; tests/web/runtime-compatibility.test.mts; tests/web/runtime-manifest.test.mts.
- Technical value delivered: Сквозные local contracts и отрицательные сценарии проверены без обхода authority.
- Product value delivered: Данные/границы работы доступны в локальном приложении с явным unavailable/partial состоянием.
- Actual implementation date and time: 11-11-2026 08:09
- Verification evidence: Web 150/150; strict/build exit 0; headless 33; Python 1450 (skip 1), fixture 91/91, transcript 26/26, compatibility compatible. [Текущий отчёт](product-agent-os-web-m1-execution-2026-11-11.md). [Историческая квалификация](product-agent-os-web-m1-initial-qualification-2026-11-10.md).
- Residual risks: Manifest квалифицирует native-offline tuple, не provider entitlement, commercial admission или browser acceptance; любое изменение tuple блокирует dispatch.
- Follow-up: Передать локальный контракт потребителям; оставшиеся gates — PAOS-0045.

Историческая запись до нативной проверки 11 ноября (не текущий статус):

> - Status: blocked
> - What was done: Проверены схема, семантика событий App Server, FTS5 и файловая SQLite-проба. Предыдущие изолированные stdio-прогоны подтвердили только metadata, без пары write/deny. Офлайн-оценка требует фактическую запись и отказ на синтетических контролях.
> - Files touched / work locations: `packages/contracts/runtime/`, `tests/web/runtime-compatibility.test.mts`, `research/product-agent-os-web-m1-initial-qualification-2026-11-10.md`.
> - Technical value delivered: Локальный probe выявляет отсутствие обязательной части schema и отделяет static check от qualification.
> - Product value delivered: Зависимая интеграция получает проверяемый кандидат runtime без заявления о готовности запуска.
> - Actual implementation date and time: pending_execution_timestamp
> - Verification evidence: Schema, event и SQLite tests прошли 12/12. SQLite проверил rollback, снимок WAL и FK. Независимая сверка MXC и наблюдение Windows token подтвердили запуск диагностики в AppContainer, конкретная стадия отказа PSEC неизвестна. Оценка прежних receipts сохраняет блокировку `scoped_execution_policy`. [Candidate tuple и команды](product-agent-os-web-m1-initial-qualification-2026-11-10.md).
> - Residual risks: Native sandbox и фактическое ограничение записи, изоляция после входа, app lockfile и adapter revision остаются открытыми.
> - Follow-up: В поддерживаемой Windows-среде подтвердить native readiness и scoped write/deny proof до handoff контрактов.

### Task `PAOS-0055`

- Task: Команды агентов и совместимость legacy writers
- Status: implemented
- Delivery stage: M1
- Execution order: 10
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested M1 audit remediation, 2026-11-10
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 08:09
- Depends on: PAOS-0048, PAOS-0054
- Blocks: PAOS-0042, PAOS-0056
- Source: PRD §17; architecture §21; plan v0.7; audit WA-01–13
- Short description: Dynamic tools adapter, attribution/idempotency и inventory read/write consumers для SQL authority
- Technical value: Dynamic tools adapter, attribution/idempotency и inventory read/write consumers для SQL authority
- Product value: Согласованный M1 сохраняет данные и показывает достоверное состояние работы в одном окне.
- Scope: apps/local-service/src/agent-commands; packages/contracts/domain-commands; plugins/product-agent-os/scripts/product_agent_os
- Non-goals: Не менять глобальные permissions/hooks; не делать local semantic store или bidirectional sync; внешние операции отдельно разрешаются
- Expected result: Команды агентов и совместимость legacy writers — реализовано и проверено в назначенном этапе
- Acceptance criteria: Architecture §21.3: no raw SQL/agent credentials; malformed/cross-project/stale/replay denied; legacy consumers mapped/unsupported; M1 tools не обходят manual acceptance.
- Verification gates: Focused contract/failure-injection tests; migration/restore fixtures; relevant browser journey; real DB acceptance before closure
- Risks / approval gates: Неподдержанная runtime/schema capability; потеря данных или ложный success при неполном evidence.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/agent-commands; packages/contracts/domain-commands; plugins/product-agent-os/scripts/product_agent_os
- Next step: Передать локальный контракт потребителям; оставшиеся gates — PAOS-0045.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-storage-research-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: implemented
- What was done: Scoped dynamic domain tools, canonical idempotency, immutable system review guards и conservative inventory legacy writers реализованы.
- Files touched / work locations: apps/local-service/src/commands; tests/web/domain-idempotency.test.mts; tests/web/domain-migration.test.mts.
- Technical value delivered: Сквозные local contracts и отрицательные сценарии проверены без обхода authority.
- Product value delivered: Данные/границы работы доступны в локальном приложении с явным unavailable/partial состоянием.
- Actual implementation date and time: 11-11-2026 08:09
- Verification evidence: Web 150/150; strict/build exit 0; headless 33; Python 1450 (skip 1), fixture 91/91, transcript 26/26, compatibility compatible. [Текущий отчёт](product-agent-os-web-m1-execution-2026-11-11.md). [Историческая квалификация](product-agent-os-web-m1-initial-qualification-2026-11-10.md).
- Residual risks: Неизвестные installed writers остаются unsupported; нет raw SQL, agent credentials или автоматической manual acceptance.
- Follow-up: Передать локальный контракт потребителям; оставшиеся gates — PAOS-0045.

### Task `PAOS-0056`

- Task: Переключение источника задач и проверка миграции
- Status: implemented
- Delivery stage: M1
- Execution order: 17
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested M1 audit remediation, 2026-11-10
- Validator target: detailed task blocks
- Date and time of task implementation: 11-11-2026 08:09
- Depends on: PAOS-0050, PAOS-0051, PAOS-0055, PAOS-0044
- Blocks: PAOS-0045, PAOS-0053
- Source: PRD §17; architecture §21; plan v0.7; audit WA-01–13
- Short description: Freeze, source recheck, verified backup/restore и atomic authority epoch после staging и writer compatibility
- Technical value: Freeze, source recheck, verified backup/restore и atomic authority epoch после staging и writer compatibility
- Product value: Согласованный M1 сохраняет данные и показывает достоверное состояние работы в одном окне.
- Scope: apps/local-service/src/import-export/cutover; apps/web/src/projects/migration
- Non-goals: Не менять глобальные permissions/hooks; не делать local semantic store или bidirectional sync; внешние операции отдельно разрешаются
- Expected result: Переключение источника задач и проверка миграции — реализовано и проверено в назначенном этапе
- Acceptance criteria: ST-AC-03–05/07 и DATA-AC-01–03: whole-project supported profile, no loss; crashes до/после commit; backup restore до switch; repeat cutover и source drift; reverse export post-cutover deltas.
- Verification gates: Focused contract/failure-injection tests; migration/restore fixtures; relevant browser journey; real DB acceptance before closure
- Risks / approval gates: Неподдержанная runtime/schema capability; потеря данных или ложный success при неполном evidence.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/import-export/cutover; apps/web/src/projects/migration
- Next step: Передать локальный контракт потребителям; оставшиеся gates — PAOS-0045.
- Actual time: локальная реализация и проверка 11-11-2026; отдельная active duration не измерялась, JSON duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-storage-research-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: implemented
- What was done: Оба source files удерживаются native sharing locks до atomic cutover; re-read/digest/root checks, restore rehearsal, same-transaction source bindings и repeat receipt проверены.
- Files touched / work locations: apps/local-service/src/import-export; apps/local-service/src/storage/sqlite-worker.mts; tests/web/domain-migration.test.mts.
- Technical value delivered: Сквозные local contracts и отрицательные сценарии проверены без обхода authority.
- Product value delivered: Данные/границы работы доступны в локальном приложении с явным unavailable/partial состоянием.
- Actual implementation date and time: 11-11-2026 08:09
- Verification evidence: Web 150/150; strict/build exit 0; headless 33; Python 1450 (skip 1), fixture 91/91, transcript 26/26, compatibility compatible. [Текущий отчёт](product-agent-os-web-m1-execution-2026-11-11.md). [Историческая квалификация](product-agent-os-web-m1-initial-qualification-2026-11-10.md).
- Residual risks: Только supported synthetic project; реальный target не мигрирован. Post-cutover legacy edits показываются changed, не импортируются автоматически.
- Follow-up: Передать локальный контракт потребителям; оставшиеся gates — PAOS-0045.

## App-agent route: решение владельца 2026-11-11

Решение владельца 11-11-2026: выбран `codex_app_agent` с `selection: owner_default`, без API key; `local_api_byok` сохранён только как явно выбираемый `explicit_compatibility` с отдельным API account. Это разные маршруты, автоматического fallback нет. Inherited auth cache не читается; SIWC остаётся отдельным admission-gated маршрутом. AUTH-G1–G6 и PAOS-0046/0030 не закрыты этим решением.

Фактическая проверка 11-11-2026, 17:50:23–17:51:35 MSK: production UI → durable job → реальный App collaboration worker → capability-authenticated claim/report → сохранённый финальный ответ → результат в browser, **16/16**, service/fixture cleanup true. Receipt: `.tmp/paos-m1/app-agent-evidence-9TDdwj/app-agent-result.json`; actualAppAgent=true, actualAppServer=false, externalProviderClient=false, apiKey=false, nativeSandbox=false. Synthetic correlation value в ответе не является credential и здесь не копируется. Это реальный App-hosted reasoning/result путь, а не fixture RPC или новый provider client.

Действующий App coordinator должен быть активен: consumer lease 30 s с heartbeat, host identity attested, не cryptographic. Нет доказанного automatic Desktop wakeup и фоновой работы после остановки чата/App. Pinned 0.167.0 предоставляет публичный proxy command, но фактические daemon-version/proxy проверки завершились WSA10050, включая разрешённый native повтор; transport к работающему Desktop не квалифицирован. Этот результат не подменяется чтением auth cache или private IPC. Execution заблокирован до подтверждения permission boundary; cooperative Stop требует ACK, при потере lease сохраняется recovery_required без replay. Нет native sandbox/полной tool-permission приёмки и нет обещания неограниченного usage.

PAOS-0039 остаётся implemented только в контракте выбора маршрута. PAOS-0042/0043/0044 остаются in_progress, PAOS-0045 — blocked; M1: 14 implemented / 3 in_progress / 1 blocked — компонентный счёт, не readiness. Исходный full-turn gate «Codex App закрыт» SW-AC-01/UX-AC-01 сохранён как историческое требование самостоятельного App Server маршрута, остаётся непроверенным и не объявляется пройденным. Для нового owner-selected App-agent маршрута App и активный consumer обязательны: новый 16/16 receipt подтверждает только этот путь. Standalone/offline launcher PAOS-0040 проверен отдельно. Полная execution/recovery и M1/human acceptance этим addendum не закрываются; прежний manual owner rejection сохраняется.

Локальные текущие проверки root: Web **238/238**, strict exit 0, build **36 modules / Cfgug4Ze**. Предыдущие active-runtime fixture **55/55** (`yjqhQa`), browser **669** (`22l7mM`) и headless **33** сохраняют отдельный provenance; они не называются actual App-agent или новым full M1 run. Текущая сводка и hashes принадлежат [execution report](product-agent-os-web-m1-execution-2026-11-11.md).
