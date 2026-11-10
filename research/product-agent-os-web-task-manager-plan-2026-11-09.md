# Product-Agent OS Web — план полноценного Task Manager

Source status: project-authored / proposed / requirements-backed. Дата: 2026-11-09.

Статус: **draft_for_review**. Это очередь будущей реализации, не разрешение начать разработку. Все 56 задач имеют статус planned; фактическое время отсутствует. Пользовательский scope расширен относительно read-only M1. Исходные M1–M3 сохраняются как история; при расхождении приоритет имеют PRD §17, architecture §21 и актуальная очередь v0.7 этого плана.

Связи: [PRD](product-agent-os-web-prd-2026-11-05.md), [архитектура](product-agent-os-web-architecture-2026-11-05.md), [экраны](product-agent-os-web-task-manager-screens-2026-11-09.md), [машинные группы](product-agent-os-web-task-manager-task-group-2026-11-09.json).




## Актуальная очередь v0.7: M1 после аудита

Source status: project-authored plan, 2026-11-10; 56 planned tasks / 12 groups; implementation_not_started. Нормативный scope — PRD §17, архитектура §21, wireframes v0.7. Очереди v0.1–v0.6 и прежние receipts ниже — история; при расхождении применяется этот раздел и обновлённые карточки/JSON.

| Этап | Задачи и gate | Ownership / результат |
| --- | --- | --- |
| M1a contracts | 0001 → 0054; 0002/0003 → 0048 после 0054; 0004; 0039/0040 → 0041 после 0054 | Architect фиксирует manifest/schema/policies; storage owner — driver/FTS5/transactions; runtime owner — bootstrap/credentials |
| M1b single window | 0048+0054 → 0055; 0041+0048+0055 → 0042 → 0043 → 0044 | Commands, scopes и writers до execution; минимальный Task CRUD/доска/catalog read-only принадлежат 0043 |
| M1c data | От 0048 независимо 0049 search, 0050 preview, 0051 backup; 0050+0051+0055+0044 → 0056 cutover | Backup и restore доказаны до смены authority; source digests проверяются после freeze |
| M1 acceptance | 0044+0049+0051+0056 → 0045 | Вся матрица ниже, включая UI, data и negative cases |
| M2 | Прежние full Task Manager/каталоги/граф, 0035/0038/0027 | Расширения M1 schema; полный ST-03/ST-09, без второй БД |
| M3 | G07, 0036/0037 | Workflow execution/agent autonomy поверх M1 coordinator |
| M4 | G08/0046; optional 0047 отдельно | Local/commercial qualification, AUTH-G1–G6 |
| T1 | 0052 после 0030 и storage foundations; 0053 после 0052/0056 | Separate hosting/auth/RBAC/runtime design; local M4 не зависит от team |

Новые задачи: 0054 compatibility manifest (12 h), 0055 agent commands/writers (16 h), 0056 cutover (12 h). 0050 сокращена до preview/staging (12 h вместо 20), 0051 больше не зависит от 0050. Полное транзитивное замыкание M1 до 0045 — **18 задач, 234 engineering hours**, rough estimate, не календарное обязательство. Реальные start/end/duration у всех 56 задач null. Оценки требуют уточнения после 0054; будущие M2–T1 не включены.

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

Текущие documentation receipts и strict-site gap — [аудит §9.2](product-agent-os-web-m1-final-audit-2026-11-10.md#92-текущие-проверки-согласования). Это не evidence исполнения задач.

Группы/границы файлов — в карточках. Общими packages/contracts владеет 0054 owner до handoff; 0048 storage owner, 0055 domain bridge owner, 0042 runtime owner применяют только согласованный contract. Без перекрывающейся записи общих файлов. Документационная правка не запускает перечисленных агентов.

Re-entry gate: после отдельного разрешения начать с 0001/0054 и зависимостей; если capability отсутствует, вернуть design issue до зависящего кода. Эту спецификацию нельзя объявить verified runtime или commercial-ready. Плановые criterion IDs не являются уже выполненными проверками.

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
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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
- Next step: Проверить источники и контракт адаптеров
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

### Task `PAOS-0002`

- Task: Модель задачи и идентификаторы
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0001
- Blocks: PAOS-0003, PAOS-0005, PAOS-0006, PAOS-0031, PAOS-0042, PAOS-0045, PAOS-0048
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Контракт прежних 12 и дополнительных полей §14 PRD; отдельные product status и planning status
- Technical value: Единый контракт всех полей задачи, стабильные ID и миграция старых записей
- Product value: Пользователь ставит полную задачу один раз и сохраняет устойчивую ссылку на неё при изменениях проекта.
- Scope: packages/contracts/tasks; apps/local-service/src/tasks
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Модель задачи и идентификаторы доступна в соответствующем этапе
- Acceptance criteria: Все поля §13–§14 проходят round-trip; стабильные ID; creator provenance; product workflow status не подменяет task_matrix_plan_v1 status
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: packages/contracts/tasks; apps/local-service/src/tasks
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

### Task `PAOS-0003`

- Task: Время и журнал событий
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0004`

- Task: Темы и локализация
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0005`

- Task: Список и доска задач
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0006`

- Task: Карточка и редактор задачи
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0007`

- Task: Файлы, артефакты и исполнители
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0008`

- Task: Приёмка и жизненный цикл
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0009`

- Task: Каталог всех доступных сессий
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0010`

- Task: Сообщения и переходы по контексту
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0011`

- Task: Поиск, приватность и хранение сессий
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0012`

- Task: Каталог и профиль агента
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0013`

- Task: Создание, изменение и удаление агента
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0014`

- Task: Управление агентом по описанию
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0015`

- Task: Назначения и статистика агентов
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0016`

- Task: Каталог и профиль скилла
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0017`

- Task: Редактор и версии скиллов
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0018`

- Task: Добавление по пути и find-skills
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0019`

- Task: Генерация по требованиям и описанию
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0020`

- Task: Индекс файлов и символов
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0021`

- Task: Граф и навигация к исходникам
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0022`

- Task: Влияние переменной и изменения
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0023`

- Task: Политика автономности и лимиты
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0008, PAOS-0013, PAOS-0017
- Blocks: PAOS-0024, PAOS-0026, PAOS-0037
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Задать заранее разрешённые действия, бюджеты и stop conditions
- Technical value: Задать заранее разрешённые действия, бюджеты и stop conditions
- Product value: Пользователь задаёт границы самостоятельной работы один раз и сохраняет возможность остановки.
- Scope: apps/local-service/src/autonomy-policy; apps/web/src/features/autonomy
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Политика автономности и лимиты доступна в соответствующем этапе
- Acceptance criteria: Preview policy объясняет возможности; UI не расширяет host permissions; pause доступна
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Повтор действий, конкурирующие writers, выход за разрешённый scope; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/autonomy-policy; apps/web/src/features/autonomy
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

### Task `PAOS-0024`

- Task: Очередь, назначения и владение файлами
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0015, PAOS-0019, PAOS-0023, PAOS-0037, PAOS-0038
- Blocks: PAOS-0025
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Назначать агентов и skills в пределах scope без конфликтующих writers
- Technical value: Назначать агентов и skills в пределах scope без конфликтующих writers
- Product value: Пользователь запускает независимые задачи параллельно без незаметного перезаписывания одних файлов.
- Scope: apps/local-service/src/scheduler
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Очередь, назначения и владение файлами доступна в соответствующем этапе
- Acceptance criteria: Очередь соблюдает pinned recipe, blocks links, hard WIP и ownership; независимые writers допускаются только при отсутствии пересечения
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Повтор действий, конкурирующие writers, выход за разрешённый scope; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/scheduler
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

### Task `PAOS-0025`

- Task: Исполнение, восстановление и отмена
- Status: planned
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
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0028`

- Task: Интеграционная проверка пути
- Status: planned
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
- Acceptance criteria: Пилот согласован отдельно; restore проверен; наблюдения отделены от продуктовых гипотез
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
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

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


### Task `PAOS-0032`

- Task: Поля, авторство, приоритеты, компоненты и даты
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

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


### Task `PAOS-0033`

- Task: Версии продукта и release policy
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

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


### Task `PAOS-0034`

- Task: Attachments, комментарии и история изменений
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

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


### Task `PAOS-0035`

- Task: Kanban и ручной жизненный цикл задачи
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

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


### Task `PAOS-0036`

- Task: Редактор, версии и миграции workflow
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0035
- Blocks: PAOS-0028, PAOS-0037
- Source: PRD §14; TM-21
- Short description: Workflow definitions, type mapping, draft/publish и pinned versions
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
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

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


### Task `PAOS-0037`

- Task: Цепочки агентов и привязка к workflow
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0036, PAOS-0023
- Blocks: PAOS-0024, PAOS-0028
- Source: PRD §14; TM-22
- Short description: Recipes с branches/join, ownership, budgets и идемпотентным запуском
- Technical value: Recipes с branches/join, ownership, budgets и идемпотентным запуском
- Product value: Пользователь направляет агентов по разным цепочкам для features, bugs и non-code работы
- Scope: apps/local-service/src/execution-recipes; apps/local-service/src/scheduler; apps/web/src/features/workflows/recipes
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Цепочки агентов и привязка к workflow в будущем Web
- Acceptance criteria: Replay не дублирует run; bounded retry останавливается; parallel writers проверяются; policy нельзя расширить recipe; Manual не запускает agent
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 20:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: apps/local-service/src/execution-recipes; apps/local-service/src/scheduler; apps/web/src/features/workflows/recipes
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

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


### Task `PAOS-0038`

- Task: Linked Issues и блокирующие зависимости
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

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

### Task `PAOS-0039`

- Task: Допустимые auth routes и коммерческие границы
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0001
- Blocks: PAOS-0041, PAOS-0047
- Source: PRD §15 SW-01–12; auth/commercial AUTH-G1–G6
- Short description: Зафиксировать API BYOK baseline, ограничения managed login и admission SIWC; выбрать deployment/channel без внешней регистрации
- Technical value: Зафиксировать API BYOK baseline, ограничения managed login и admission SIWC; выбрать deployment/channel без внешней регистрации
- Product value: Пользователь знает доступный способ подключения и плательщика до начала работы.
- Scope: research/product-agent-os-web-auth-commercial-2026-11-09.md; packages/contracts/auth
- Non-goals: Не менять hooks/global permissions; не запускать внешний/provider/Git/release scope без отдельного разрешения
- Expected result: AUTH-G1 имеет решение владельца по exact route; отсутствующий SIWC admission явно блокирует этот путь, но не подменяется managed login.
- Acceptance criteria: AUTH-G1 имеет решение владельца по exact route; отсутствующий SIWC admission явно блокирует этот путь, но не подменяется managed login.
- Verification gates: Focused contract/negative tests; authorized runtime/browser where needed; no fixture-only activation claim
- Risks / approval gates: Неоднозначные условия или отсутствие коммерческого допуска. Provider calls, registration and publication require separate authority.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 06:00:00 (предварительно)
- Agents: product-manager, architect, security-privacy-supply-chain-reviewer
- Skills: implementation-planner; task-matching skills selected at start
- Output artifacts: research/product-agent-os-web-auth-commercial-2026-11-09.md; packages/contracts/auth
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


### Task `PAOS-0040`

- Task: Launcher и жизненный цикл локального приложения
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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


### Task `PAOS-0041`

- Task: Локальное API-подключение и credential isolation
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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


### Task `PAOS-0042`

- Task: Codex App Server adapter и ограниченное выполнение
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0041, PAOS-0002, PAOS-0003, PAOS-0048, PAOS-0055
- Blocks: PAOS-0043
- Source: PRD §17; architecture §21; plan v0.7; audit WA-01–13
- Short description: Pinned stdio protocol, project/task/run/thread/turn binding, allowlist и одна минимальная recipe
- Technical value: Pinned stdio protocol, project/task/run/thread/turn binding, allowlist и одна минимальная recipe
- Product value: Codex выполняет задачу непосредственно из PAOS в заданных границах.
- Scope: apps/local-service/src/runtime/codex; packages/contracts/runtime
- Non-goals: Не менять hooks/global permissions; не запускать внешний/provider/Git/release scope без отдельного разрешения
- Expected result: Codex App Server adapter и ограниченное выполнение — реализовано и проверено в назначенном этапе
- Acceptance criteria: Initialize/start/events/approvals/interrupt работают на выбранном build; один writer на canonical workspace; Codex App и чужой auth profile не используются. Architecture §21: project cursors, root fencing/global concurrency=1, mode binding boundary, answered_or_cleared отдельно от item outcome.
- Verification gates: Focused contract/negative tests; authorized runtime/browser where needed; no fixture-only activation claim
- Risks / approval gates: Protocol drift, duplicate dispatch, превышение authority.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 20:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching skills selected at start
- Output artifacts: apps/local-service/src/runtime/codex; packages/contracts/runtime
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


### Task `PAOS-0043`

- Task: Активная сессия и минимальная карточка задачи
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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


### Task `PAOS-0044`

- Task: Recovery, повторное подключение и сохранённые сессии
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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


### Task `PAOS-0045`

- Task: Приёмка сквозного M1 в одном окне
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0044, PAOS-0002, PAOS-0003, PAOS-0049, PAOS-0051, PAOS-0056
- Blocks: PAOS-0028, PAOS-0046
- Source: PRD §17; architecture §21; plan v0.7; audit WA-01–13
- Short description: Проверить launch/connection/chat/task/approval/result/resume и негативные границы на разрешённом runtime
- Technical value: Проверить launch/connection/chat/task/approval/result/resume и негативные границы на разрешённом runtime
- Product value: Первый MVP доказывает самостоятельный пользовательский путь, а не набор статичных экранов.
- Scope: tests/web/single-window; docs/evidence/web-m1
- Non-goals: Не менять hooks/global permissions; не запускать внешний/provider/Git/release scope без отдельного разрешения
- Expected result: Приёмка сквозного M1 в одном окне — реализовано и проверено в назначенном этапе
- Acceptance criteria: SW-AC-01–10, ST-AC-01–07 (M1 profile), UX-AC-01–18 (M1 slice), DATA-AC-01–05 имеют receipts по матрице v0.7; runtime/browser/workload proof отдельно от fixtures; Codex App закрыт; неразрешённые external gates pending.
- Verification gates: Focused contract/negative tests; authorized runtime/browser where needed; no fixture-only activation claim
- Risks / approval gates: Synthetic evidence ошибочно принято за live product proof.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: tester, reviewer
- Skills: implementation-planner; task-matching skills selected at start
- Output artifacts: tests/web/single-window; docs/evidence/web-m1
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


### Task `PAOS-0046`

- Task: Коммерческий review API-варианта и выпускные gates
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected single-window Codex App Server, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0045
- Blocks: PAOS-0030, PAOS-0047
- Source: PRD §15 SW-01–12; auth/commercial AUTH-G1–G6
- Short description: Проверить AUTH-G1–G6, выбранные рынки, privacy, distribution licenses, payer, support и owner decision
- Technical value: Проверить AUTH-G1–G6, выбранные рынки, privacy, distribution licenses, payer, support и owner decision
- Product value: Коммерческий пакет честно описывает подключение, затраты и ограничения.
- Scope: research/product-agent-os-web-auth-commercial-2026-11-09.md; docs/release/web-commercial-review
- Non-goals: Не менять hooks/global permissions; не запускать внешний/provider/Git/release scope без отдельного разрешения
- Expected result: Каждый применимый AUTH gate содержит evidence/owner; нет обещаний без approval. Для API-only SIWC помечен unavailable; task не выполняет publication.
- Acceptance criteria: Каждый применимый AUTH gate содержит evidence/owner; нет обещаний без approval. Для API-only SIWC помечен unavailable; task не выполняет publication.
- Verification gates: Focused contract/negative tests; authorized runtime/browser where needed; no fixture-only activation claim
- Risks / approval gates: Нет admission, legal review или достаточных runtime/security evidence. Provider calls, registration and publication require separate authority.
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 08:00:00 (предварительно)
- Agents: product-manager, release-operator, security-privacy-supply-chain-reviewer
- Skills: implementation-planner; task-matching skills selected at start
- Output artifacts: research/product-agent-os-web-auth-commercial-2026-11-09.md; docs/release/web-commercial-review
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


### Task `PAOS-0047`

- Task: Опциональный Sign in with ChatGPT
- Status: planned
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
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected SQLite/FTS5 local and PostgreSQL/pgvector team, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0049`

- Task: Локальный полнотекстовый поиск FTS5
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected SQLite/FTS5 local and PostgreSQL/pgvector team, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0050`

- Task: Предварительный импорт MD/JSON в staging
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected SQLite/FTS5 local and PostgreSQL/pgvector team, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0051`

- Task: Резервное копирование и восстановление local data
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-selected SQLite/FTS5 local and PostgreSQL/pgvector team, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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

### Task `PAOS-0052`

- Task: Командный профиль PostgreSQL и pgvector
- Status: planned
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
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested M1 audit remediation, 2026-11-10
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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


### Task `PAOS-0055`

- Task: Команды агентов и совместимость legacy writers
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested M1 audit remediation, 2026-11-10
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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


### Task `PAOS-0056`

- Task: Переключение источника задач и проверка миграции
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested M1 audit remediation, 2026-11-10
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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
