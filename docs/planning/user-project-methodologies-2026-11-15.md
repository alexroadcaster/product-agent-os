# Product-Agent OS — направление B: методологии для проектов пользователей

Source status: repository_source / owner_requested_plan / B1_B2_B3_locally_verified; release_hold; remaining_slices_planned.
Дата создания: 15.11.2026. Редакция: 19.11.2026. Schema version: task_matrix_plan_v1. Timezone: Europe/Moscow.

## Назначение и два независимых направления

**A — качество самого Product-Agent OS:** [внутренний план](methodology-improvement-2026-11-15.md), [JSON](methodology-improvement-2026-11-15.json): 17 исполняемых задач, прежние ID сохранены; METH-16 сохранена отдельно как reference-only запись.

**B — этот продуктовый план:** 26 задач PAOS-PMETH-01–26, которые развивают выбор, применение и проверку Spec-Driven Development (Spec-DD), Design-Driven Development (Design-DD), Test-Driven Development (TDD), Agentic-Driven Development (ADD) и Feature-Sliced Design (FSD) в проектах пользователей. [JSON](user-project-methodologies-2026-11-15.json) владеет status/priority/dependencies; полный английский перевод карточек доступен через переключатель языка.

Направление B не зависит от внутренней FSD-миграции dashboard/tasks/workflows в A, от METH-18 go или от завершения всех FUNC-групп. Общие файлы требуют согласованного ownership/последовательной записи, а не выдуманных функциональных зависимостей. Владелец разрешил реализацию B1 в исходниках и синтетическую проверку. Для последующих групп действуют их условия входа.

## Что уже существует и что ещё предстоит доказать

Source snapshot: git HEAD `5a9c87bea374accc953a8401fa1ac32678ff6e6e`; 15 source-owner hashes в JSON. Выполнено source inspection, не новый runtime/model/browser acceptance. На начальном snapshot FUNC-владелец содержал 10 implemented / 24 planned после G01/G02. Во время планирования отдельно начат FUNC-G03: его live task-state и последующие source edits принадлежат тому workstream и не замораживаются этой матрицей. Это не новые runtime receipts текущего планирования; перед будущим slice требуется свежий source read.

Срез исследования от 18.11.2026 по текущему FUNC-владельцу — 33 implemented и F23 awaiting_user_decision. Повторно используются F02 (task/artifact links), F13 (document apply), F14 (code index) и F27–29 (project analysis и связи источников). Статусы описывают матрицу FUNC; новый runtime-прогон этим исследованием не выполнялся. Первичные источники и Context7 проверены 18.11.2026, результаты и ограничения приведены в исследовании.

| Область | Наблюдение в исходниках | Роль новых задач |
| --- | --- | --- |
| Discovery/intake | discovery.py вызывает build_methodology_audit; task_routing.py имеет explicit task context и file-free intake | PMETH-01/02 проверяют фактическую цепочку и сохраняют intent/provenance без второго scanner |
| Catalog/audit/synthesis | 12 methodology domains, recommendations, readiness statuses и grouped safe next action уже реализованы | PMETH-03/04 уточняют решения по пяти подходам, compatibility и соразмерность |
| Runner/skills | routes.py строит methodology_packet; contracts/guards и lifecycle/requirements/test-eval skills уже существуют | PMETH-05–17 связывают selected methods с артефактами, выполнением и evidence; не создают эти роли с нуля |
| CLI entrypoints | run_methodology_audit.py принимает workspace + JSON/report; другие entrypoints имеют task intake | PMETH-01/02 определяют canonical entrypoint/adapter; наличие empty intent default не означает, что весь engine теряет intent |
| Infrastructure | dry-run/stage/manifest/approval-aware merge и rollback уже существуют | PMETH-12/16 используют и проверяют этот pipeline, а не второй writer |
| Web/local service | Project Analysis включает guarded HTTP route, Node service, Python bridge и project scan records. Проекция сейчас ориентирована на проект, task-scoped advice остаётся пробелом | PMETH-19/20 расширяют существующий read-only путь; PMETH-18/21 добавляют сохраняемое решение и recovery при необходимости |
| Evidence | Есть Python fixtures/evals, runner guards и текущие Web checks | PMETH-22/23 проверяют сквозную связность; static/source evidence не объявляется activation или пользой модели |

Основные источники: `plugins/product-agent-os/scripts/product_agent_os/{discovery,methodology_audit,methodology_catalog,methodology_synthesis,task_routing,infrastructure,merge_infrastructure}.py`, `plugins/product-agent-os/scripts/codex_runtime_runner/{routes,contracts}.py`, canonical lifecycle/requirements/test-eval SKILL.md. [Текущее описание methodology intelligence](../product-agent-os/methodology-intelligence.md) используется вместе с кодом; неоднозначные смешанные RU/EN формулировки не являются самостоятельным доказательством.

Методологические первоисточники проверены в предшествующем анализе 15.11.2026 и перечислены в [направлении A](methodology-improvement-2026-11-15.md). Это project-authored proposal развития продукта, не новая проверенная capability и не единая отраслевая стандартизация терминов Design-DD/ADD.

## Ожидаемый продуктовый путь

| Шаг | Что получает пользователь | Проверяемый результат |
| --- | --- | --- |
| Контекст | Минимальный профиль проекта/задачи, ограничения, missing context | Source-bound facts отделены от предположений |
| Выбор | Какие методы нужны, зачем и с какой глубиной | Reasons, applicability, owner, override/disposition и next action |
| Планирование | Один согласованный план, требования/дизайн/границы/проверки по необходимости | AC и dependency DAG без лишней церемонии |
| Подготовка | Reviewable artifacts/proposals и точный diff | User-authored файлы сохраняются; target ещё не изменён |
| Выполнение | Один разрешённый slice, подходящий skill/agent и проверки | Authority, ownership, RED/GREEN где применимо, stop/recovery |
| Приёмка | Evidence по критериям и честные gaps | Technical/model/human/release conclusions не смешиваются |

Рекомендация метода не равна разрешению действий; выбор пользователем профиля не запускает apply. Настройка/документы, обнаруженная структура, текущая доступность, реальный запуск и принятый результат имеют отдельное evidence.

## Поведение по пяти методологиям

| Метод | Предлагаемая функция Product-Agent OS | Что доказывает применение |
| --- | --- | --- |
| Spec-DD | Concise/full requirements, AC/scenarios, canonical owners, traceability и drift handling | Связь intent → criterion → scenario/check → receipt, revision и owner |
| Design-DD | Journey/state matrix, reuse design system, prototypes/accepted differences, visual/interaction plan | Проверенный изменённый journey на current build; макет не равен human acceptance |
| TDD | Risk/behavior-based strategy и observable RED → GREEN → REFACTOR | Intended failure до changed implementation; setup failure и test count не доказательство |
| ADD | Bounded context, ownership, skills/tools, budgets, stop/handoff/recovery | Наблюдаемое разрешённое выполнение и current receipts; качество модели оценивается отдельно |
| FSD | Conditional suitability, source/import checks, ADR/public APIs, staged gradual migration | Проверенные границы/coverage и принятые checkpoints; folder names не означают соответствие |

## Разные проекты требуют разной глубины

| Сценарий | Соразмерный путь | Чего не навязывать |
| --- | --- | --- |
| Небольшой backend bug | Concise scope/AC, reproduction/TDD, bounded ADD и regression | Полный PRD, visual redesign и FSD |
| Greenfield frontend | Первый vertical slice, spec + journey/states, minimal architecture choice | Пустые FSD layers, многокомандную структуру и scaffold до решения/authority |
| Coupled legacy frontend | Read-only map, characterization, FSD alternatives, один pilot с bridges | Массовое перемещение и overwrite существующих правил |
| Уже модульный frontend | Проверить имеющиеся boundaries и сохранить достаточную архитектуру | Переименование каталогов ради FSD label |
| Native/mobile | Platform/journey checks где применимы, specs/TDD/ADD | Frontend FSD по одному package.json |
| AI/RAG | Behavior spec, baseline evals; TDD для deterministic tools/logic | Unit pass как доказательство качества LLM и скрытые provider calls |
| Docs-only/read-only | Релевантное чтение, concise result и source/static checks по изменению | Build gate, marker write или внедрение control plane в target без полномочий |

## Этапы и приоритеты

P1 — обязательные основы и защита корректности/полномочий перед включением соответствующего пути. P2 — пользовательская интеграция, расширенные предложения, оценка пользы и поставка. Приоритет не означает production incident или автоматическую авторизацию. P2, указанный в depends_on, обязателен для зависимого пути.

### Группы задач

Группы объединяют задачи по результату. Каждую задачу можно начинать после выполнения её `depends_on` и применимых условий выбора.

| Группа | Задачи | Условие старта и результат |
| --- | --- | --- |
| **B1. Выбор методологии и первый совет в CLI** | 01, 02, 22, 03, 04, 05, 07 | В цепочке 01 → 02 → 22 → 03 → 04 → 05 → 07 ожидаемые результаты фиксируются до изменения правил. В одном проекте CLI объясняет, как воспроизвести backend-ошибку и какой тест запустить, а для правки документа предлагает проверить источник. |
| **B2. Совет в Web, проверка пользы и решение о поставке** | 19, 20, 26, 23, 24, 25 | После 07 задачи 19 → 20 → 26 выводят совет в существующем интерфейсе задачи и закрепляют примеры в RU/EN. Затем 23 → 24 → 25 проверяют заявленный профиль, оценивают пользу и определяют объём поставки. При расширении профиля повторяют 23. |
| **B3. Методологии для интерфейса и frontend-архитектуры** | 08, 09, 10, 11, 12 | После 05 ветка 08 → 09 описывает и проверяет состояния интерфейса. После 04 ветка 10 → 11 → 12 определяет применимость FSD, проверяет импорты и готовит предложение по миграции. Ветки выбираются независимо. Для подготовки предложения достаточно чтения. |
| **B4. Исполнение, доказательства и восстановление** | 06, 13, 14, 15, 16, 17, 18, 21 | 06 отслеживает изменения спецификации. 13–15 определяют ответственность, skills и план исполнения. 16 отвечает за предпросмотр и запись, 17 — за доказательства по критериям, 18 — за сохранение решения, 21 — за остановку и восстановление. Каждая возможность подключается по зависимостям своей карточки. |

**Статус B1.** Выполнены и локально проверены 7 из 7 задач. CLI предлагает именованный тест для backend-ошибки и проверку источника для документации в одном синтетическом проекте. Следующая задача по зависимости — PMETH-19. [Проверки и передача](../superpowers/specs/paos-pmeth-b1-evidence.md).

**Статус B2.** Выполнены 6 из 6 задач. Read-only CLI/Web профиль локально проверен, пилот из четырёх прогонов дал недостаточно данных для вывода о пользе, владелец утвердил `hold` для поставки. [Проверки и решение](../superpowers/specs/paos-pmeth-b2-evidence.md).

**Статус B3.** Выполнены 5 из 5 задач. Дизайн-сценарии и выводы F14 проверены локально. При неполном анализе предложение о переносе не выдаётся. По зависимостям доступны входы B4 PAOS-PMETH-06 и PAOS-PMETH-13. [Доказательства B3](../superpowers/specs/paos-pmeth-b3-evidence.md).

**Первый принимаемый результат — read-only CLI+Web.** Жёсткие зависимости: PMETH 01 → 02 → 22 → 03 → 04 → 05 → 07 → 19 → 20 → 26. В одном disposable проекте backend bug и docs-only дают одинаковые выводы CLI/Web при равных данных и покрытии, с основанием и следующим проверяемым шагом. PMETH-26 закрепляет проверенные RU/EN примеры. Для приёмки нужны наблюдаемые CLI/HTTP/browser проверки и отрицательные случаи, результат проверки понимания или явный gap. PMETH-06, PMETH-08–18 и PMETH-21/23–25 за пределами prerequisites этапа.

**Расширенный путь.** PMETH-15 связывает выбранные slices. PMETH-16 добавляет применение, PMETH-17 — technical evidence, PMETH-18/21 — сохранение решения и восстановление. PMETH-23 проверяет заявленные профили, PMETH-24 оценивает пользу, PMETH-25 принимает решение о расширении. Design/FSD gates относятся к соответствующим профилям. JSON содержит 31 активное ребро. `planning_revision` фиксирует исходный граф из 54 рёбер и перенос write/override/документации. Основание — `research/methodology-plan-review-2026-11-18.md`.

## Условные требования перед квалификацией профиля

| Заявленный путь | Обязательная карточка перед профильным PMETH-23 |
| --- | --- |
| Базовый read-only bug/docs | PAOS-PMETH-26 |
| Design journey | PAOS-PMETH-09 |
| Миграция FSD | PAOS-PMETH-12 |
| Маршрутизация skills/tools | PAOS-PMETH-14 |
| Запись в target | PAOS-PMETH-16 |
| Technical readiness по AC | PAOS-PMETH-17 |
| Durable override и recovery | PAOS-PMETH-21 |

Базовая PMETH-23 ждёт PMETH-26. Перед go по каждому дополнительному claim обязательны указанная карточка, её hard prerequisites и профильные E2E с evidence на выбранных scope/revision. Для широкого rollout квалифицируются все строки. PMETH-25 сверяет статусы и evidence по `profile_qualification`; непроверенный claim не включается, critical gap блокирует соответствующий профиль. Расширение требует повторного PMETH-23 по новой области и revision.

## Связи с A и действующими планами

- Сохранённая METH-16 — только reference, её implementation owner теперь этот B-plan. Legacy AC01 покрывается PMETH-10/22; AC02 — PMETH-03/07/11; AC03 — PMETH-16/17/23/26. Старые AC и ID сохранены. Прежние edges METH-05/18 → METH-16 исключены из активного DAG; они не gate B.
- В A остаются METH-01–15/17/18; его решение о масштабировании относится к внутренним METH-14/15. Нет cross-direction hard dependencies.
- FUNC-G01 и F08 contracts, существующие discovery/renderer/merge и runner — reuse boundaries. F30 import-only PoC не означает установленный полный graph engine; PMETH-11 использует только подтверждённые adapters.
- F02/F28/F25, F11/F12/F15/F16, F19/F21/F22/F23/F24 и UI-12 сохраняют свои scope/status. B не закрывает их автоматически и не ждёт все FUNC-группы. Реальное изменение общего контракта требует сверки owner, regression и docs.
- Новые Files/Database/usages, hosting/auth/team storage M5, telemetry billing, установка и commercial release не включаются в B без отдельного решения.
- external_refs в JSON — ownership/evidence references, не hard dependencies и не второй статус. Предпосылки существующей capability проверяются на текущем source до выбранного slice; если она реально отсутствует, dependency уточняется у canonical owner, не предполагается закрытой.

## Проверка будущих slices

Это proposed acceptance profiles. Текущий маршрут остаётся у TEST.md; текущий запрос его не меняет.

| Профиль | Минимальные проверки при будущем выполнении |
| --- | --- |
| PV-PLAN / PV-DOCS | Source/semantic/link/parity checks и affected docs route; task matrices/DAG; без runtime claim |
| PV-ENGINE | Focused methodology/catalog/synthesis/task-routing tests + выбранные PMETH-22 cases, baseline/candidate при behavior/prompt changes |
| PV-CONTRACT | Python/TS schema/adapter roundtrip, malformed/unknown/version/revision/project negatives и compatibility |
| PV-TDD | Intended RED, minimal GREEN, scoped refactor; assertion/unique-test preservation и explicit unavailable gaps |
| PV-DESIGN | Changed journey/state/visual/keyboard plan, current-build comparison когда разрешён; accepted design и human acceptance отдельно |
| PV-FSD | Supported JS/TS/TSX imports/aliases/public APIs/cycles cases, partial coverage, no mutation и reviewable findings |
| PV-ADD | Ownership/context/tool/permission/timeout/partial/fallback negatives на baseline/candidate; prompt/model quality отдельно |
| PV-STAGE | Existing renderer/merge tests; dry-run → outside-target stage → reviewed fixture apply → rollback, drift/symlink/dirty-user preservation |
| PV-EVIDENCE | Criterion/receipt/readiness mapping, stale/forged/failure negatives; source/runtime provenance по типу claim |
| PV-STORAGE | Synthetic SQLite compatibility/migration/CAS/isolation/backup/restore; реальная DB вне scope |
| PV-BRIDGE | Real adapters/API request path и selector, negative old/fallback proof, session/origin/CSRF/project guards; pinned runtime qualification при затронутых pins |
| PV-UI | Type-check/build и scoped current-build synthetic browser на двух themes, RU/EN, keyboard/focus/errors; без provider/real credentials |
| PV-RECOVERY | Matching checkpoint, Stop/unknown/restart/no-replay, drift/concurrency/audit redaction и data preservation |
| PV-EVAL | Expected scenario outcomes до candidate, actual baseline/failed receipts, positive/edge/adversarial/regression scope без fictitious passes |
| PV-E2E | Disposable target projects, real selected CLI/API/UI adapters, inside/outside authority, evidence/cleanup; модель и human отдельно |
| PV-ACTUAL | Сопоставимые actual-agent baseline/candidate только с нужной authority, outcome/effort/available cost metrics и limits |
| PV-DECISION | Owner-reviewed supported scope, gap dispositions, rollback/disable и отсутствие внешних действий из одного decision |

Точные команды брать из TEST и актуальных entrypoints; ожидаемые будущие команды не выдаются за выполненные сегодня. Полные suites только по affected contract/неизвестной области влияния/release qualification. Повтор после unchanged input не нужен. Недоступный model/host check остаётся gap, deterministic fixture не подменяет actual-agent quality.

## Полномочия, данные, stop и rollout

Работа с target по умолчанию read-only; существующий user grant применяется лишь в его точных границах. Stage/proposal/profile/graph не выдаёт approval. Target writes, installs, providers/cost, credentials, Git, deployment/publication, hooks/trust и внешние automation требуют своей authority; synthetic acceptance в будущем local slice не означает разрешения на реальные проекты/БД.

Не хранить secrets, raw private chats, credentials, pairing/session material и private project content без необходимости/authorization. В evidence достаточно relative paths, revisions, выбранных facts и redacted receipts. Workspace/doc/MCP/tool content — недоверенные данные. Выбор методологии не изменяет instruction precedence или sandbox.

Stop при неподтверждённом source/authority, stale approval, overlap, data loss/replay, permission violation, unknown parser coverage, недоступной существенной проверке. Доступен безопасный read-only/manual next action; обхода и скрытого fallback нет. Rollback — только own approved changes/managed sections/совместимая state recovery, без уничтожения user files или destructive Git. Неразрешённый critical gap блокирует соответствующую приёмку, а не все несвязанные проекты.

Критические критерии: zero unauthorized writes, zero потерянных user files/replayed unknown effects, zero false-ready из detection/missing/stale evidence. Полезность/latency/cost thresholds определить до actual candidate run в PMETH-22/24; недостаток измерений не равен нулю или улучшению. Возможен bounded_go для поддержанного CLI/профиля либо hold/no-go; broad production usefulness и autonomous delivery не выводятся из этого плана.

## Историческая проверка редакции от 15.11.2026

Проверена подготовка планов, не исполнение A/B. Review mode: self_review; independent/runtime/model/human acceptance не заявлены.

- Четыре RU/EN task matrices A/B проверены через `python -B plugins/product-agent-os/scripts/validate_task_matrix.py` с соответствующим планом: ok, errors=[].
- `python -B .docs-tools/reports/methodology-split-2026-11-15/verify_split.py verify` — ok: A17 + B26 executable tasks, один retained reference, 155 active AC + 3 legacy AC; A25/B54 reciprocal edges, acyclic independent DAG, RU/EN/JSON parity и baseline-before-policy.
- Проверка сохранности восстановила исходный текст A обратным применением только текущих planning hunks; все 18 прежних ID/названия/status и legacy AC сохранены. Уточнение двух критериев METH-05/18 имеет before-image в JSON history.
- Existing shared documents сохранены вне собственных METH sections; новый FUNC-G03 обнаружен как concurrent work, его sections и source edits не отменялись. Исходные source hashes — snapshot, не утверждение об отсутствии изменений в соседнем workstream.
- `python -B tools/check_docs.py --paths` с 11 изменёнными Markdown owners — OK; site/archive не проверялись. `git diff --check --` с 13 owning plan/JSON/pointer paths — exit 0.
- Ранний preflight остановился на concurrent root change; после чтения подтверждён независимый G03 scope и применены только exact METH hunks. Large inline shell verification не запустился из-за packaged shell; проверка выполнена local helper через системный PowerShell, без installation/изменения политики.
- Control-plane sync: updated METH sections REQUIREMENTS/PLAN/RUNLOG, catalog и registry; TEST/EVALS/prod_test no_change_needed. Application code, active skills/workflows/hooks, targets, browser/native/provider/model/install/Git/publication не менялись/не исполнялись этой задачей. Все implementation timestamps pending_execution_timestamp.

## Индекс задач направления B

| ID | Приоритет | Группа / методы | Задача | Depends on |
| --- | --- | --- | --- | --- |
| PAOS-PMETH-01 | P1 | B1; Spec-DD, ADD | Проверить существующий путь методологий и назначить владельцев | — |
| PAOS-PMETH-02 | P1 | B1; Spec-DD, ADD | Нормализовать профиль проекта и намерение пользователя | PAOS-PMETH-01 |
| PAOS-PMETH-03 | P1 | B1; Spec-DD, Design-DD, TDD, ADD, FSD | Выбирать методологии соразмерно задаче и объяснять выбор | PAOS-PMETH-22 |
| PAOS-PMETH-04 | P1 | B1; Spec-DD, ADD | Согласовать версионированный methodology contract | PAOS-PMETH-03 |
| PAOS-PMETH-05 | P1 | B1; Spec-DD | Встроить Spec-Driven маршрут от запроса к проверяемой спецификации | PAOS-PMETH-04 |
| PAOS-PMETH-06 | P1 | B4; Spec-DD, ADD | Отслеживать изменения спецификации и устаревший контекст | PAOS-PMETH-05 |
| PAOS-PMETH-07 | P1 | B1; TDD, Spec-DD | Встроить TDD и воспроизведение ошибок в выполнение slices | PAOS-PMETH-05 |
| PAOS-PMETH-08 | P1 | B3; Design-DD, Spec-DD | Встроить Design-Driven сценарии и матрицу состояний | PAOS-PMETH-05 |
| PAOS-PMETH-09 | P1 | B3; Design-DD, TDD | Проверять пользовательский интерфейс по принятому design-контракту | PAOS-PMETH-08 |
| PAOS-PMETH-10 | P1 | B3; FSD, Spec-DD | Определять применимость FSD и предлагать архитектурный выбор | PAOS-PMETH-04 |
| PAOS-PMETH-11 | P1 | B3; FSD, TDD | Проверять frontend-зависимости по исходникам | PAOS-PMETH-10 |
| PAOS-PMETH-12 | P2 | B3; FSD, Spec-DD | Создавать поэтапный FSD migration proposal для проекта пользователя | PAOS-PMETH-11 |
| PAOS-PMETH-13 | P1 | B4; ADD, Spec-DD | Встроить ADD-контракт исполнения и ownership | PAOS-PMETH-04 |
| PAOS-PMETH-14 | P2 | B4; ADD | Связать выбранные методологии с доступными skills и инструментами | PAOS-PMETH-13 |
| PAOS-PMETH-15 | P1 | B4; Spec-DD, Design-DD, TDD, ADD, FSD | Объединить методологии в один соразмерный delivery plan | PAOS-PMETH-07, PAOS-PMETH-13 |
| PAOS-PMETH-16 | P1 | B4; Spec-DD, ADD, FSD | Подключить безопасные staging, preview и разрешённое применение | PAOS-PMETH-06, PAOS-PMETH-15 |
| PAOS-PMETH-17 | P1 | B4; Spec-DD, TDD, Design-DD, ADD, FSD | Собирать evidence и вычислять готовность по критериям | PAOS-PMETH-06, PAOS-PMETH-15 |
| PAOS-PMETH-18 | P2 | B4; Spec-DD, ADD | Определить durable state методологий в Web/desktop | PAOS-PMETH-17, PAOS-PMETH-19 |
| PAOS-PMETH-19 | P2 | B2; ADD, Spec-DD | Связать Python methodology engine с API и runtime приложения | PAOS-PMETH-07 |
| PAOS-PMETH-20 | P2 | B2; Design-DD, Spec-DD | Показать пользователю выбор, план и доказательства в интерфейсе | PAOS-PMETH-19 |
| PAOS-PMETH-21 | P1 | B4; ADD, Spec-DD | Обрабатывать drift, остановку, возобновление и аудит | PAOS-PMETH-16, PAOS-PMETH-18, PAOS-PMETH-20 |
| PAOS-PMETH-22 | P1 | B1; Spec-DD, Design-DD, TDD, ADD, FSD | Подготовить baseline и acceptance eval matrix пользовательских проектов | PAOS-PMETH-02 |
| PAOS-PMETH-23 | P1 | B2; Spec-DD, Design-DD, TDD, ADD, FSD | Провести сквозную synthetic приёмку методологического пути | PAOS-PMETH-26 |
| PAOS-PMETH-24 | P2 | B2; ADD, Spec-DD | Оценить полезность маршрута на сопоставимых actual-agent пилотах | PAOS-PMETH-23 |
| PAOS-PMETH-25 | P2 | B2; ADD, Spec-DD | Принять ограниченное решение о поставке и rollout | PAOS-PMETH-24 |
| PAOS-PMETH-26 | P2 | B2; Spec-DD, Design-DD | Подготовить пользовательское объяснение и operator документацию | PAOS-PMETH-20 |

## Подробные карточки направления B

### Task `PAOS-PMETH-01`

- Task: PAOS-PMETH-01
- Task name: Проверить существующий путь методологий и назначить владельцев
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized bounded B1 implementation following the plan review.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 20:43
- Depends on: Нет.
- Blocks: PAOS-PMETH-02
- External references: PAOS-FUNC-25
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Проверить и развить уже существующие компоненты вместо нового параллельного methodology engine.
- Technical value: Карта существующих компонентов, gaps и canonical owners в evidence PMETH-01.
- Product value: Избежать повторной реализации уже работающих компонентов.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files. Модули и проверки для переиспользования: `apps/local-service/src/project-analysis/bridge.py`, `apps/local-service/src/http/application.mts`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Карта существующих компонентов, gaps и canonical owners в evidence PMETH-01.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-01-AC01**: Карта reuse/extend/missing прослеживает CLI intake → discovery/audit/synthesis/task routing и Project Analysis → Python bridge → Sources/Teams & Tasks; для записи отдельно G9/F13. У каждого звена указан фактический вход, владелец и существующие тесты.
  - **PAOS-PMETH-01-AC02**: Зафиксированы два существующих обхода discovery/audit, их фильтры и пример разного покрытия; используется существующая инвентаризация. Detection, observed projection, proposal и execution различаются.
  - **PAOS-PMETH-01-AC03**: Для каждого нового контракта выбран один owner и существующий entrypoint; дублирующий движок не создаётся.
  - **PAOS-PMETH-01-AC04**: Baseline fixtures, команды, revision и compatibility consumers перечислены; активные target assets не изменены аудитом.

- Verification gates: PV-PLAN; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: architect + explorer; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Карта существующих компонентов, gaps и canonical owners в evidence PMETH-01.
- Next step: Следующая зависимость PAOS-PMETH-02.

#### Completion Report

- status: implemented
- what was done: Карта владельцев связывает CLI, аудит, Project Analysis и отдельно запись. Проверены разные фильтры двух обходов.
- files touched / work locations: [B1 evidence and canonical owners](../superpowers/specs/paos-pmeth-b1-evidence.md).
- technical value delivered: Маршрут и его доказательства связаны в записи B1.
- product value delivered: Проверяемый совет в штатном CLI.
- actual implementation date and time: 18-11-2026 20:43
- verification evidence: [B1 verification](../superpowers/specs/paos-pmeth-b1-evidence.md).
- residual risks: Паритет Web и полезность для реальных агентов проверяются отдельно.
- follow-up: PAOS-PMETH-02.

### Task `PAOS-PMETH-02`

- Task: PAOS-PMETH-02
- Task name: Нормализовать профиль проекта и намерение пользователя
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized bounded B1 implementation following the plan review.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 20:43
- Depends on: PAOS-PMETH-01
- Blocks: PAOS-PMETH-22
- External references: PAOS-FUNC-28
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Дать системе минимальный достоверный контекст для выбора глубины процесса.
- Technical value: Нормализованный профиль и intent receipt с provenance и compatibility tests.
- Product value: Получать процесс, соответствующий задаче и доступной среде.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/product_agent_os/question_protocol.py`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files. Модули и проверки для переиспользования: `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`, `plugins/product-agent-os/scripts/run_methodology_audit.py`, `apps/local-service/src/project-analysis/bridge.py`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Нормализованный профиль и intent receipt с provenance и compatibility tests.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-02-AC01**: Профиль различает greenfield/legacy, тип поверхности, масштаб/связанность, риск, change mode, доступные проверки и ограничения среды; размер repo не равен риску.
  - **PAOS-PMETH-02-AC02**: Один нормализованный intent и применимые AC доходят до audit/route. Приоритет task_context и intent_hint явно определён; конфликтный, смешанный или ошибочный ввод отклоняется либо даёт явный gap. Проверены desktop/Python adapter input и CLI intake на эквивалентных bug/docs; parity результата в рабочем HTTP path проверяет PMETH-19, staging — PMETH-16. Repository-only audit сохранён.
  - **PAOS-PMETH-02-AC03**: Факты имеют provenance/revision, assumptions и missing context отдельны; один существенный blocking question не заменяет доступное чтение.
  - **PAOS-PMETH-02-AC04**: Docs-only, небольшой bugfix и backend-only не получают полную продуктовую церемонию или frontend gates.

- Verification gates: PV-ENGINE; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: product-manager + plugin-runtime-builder; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Нормализованный профиль и intent receipt с provenance и compatibility tests.
- Next step: Следующая зависимость PAOS-PMETH-22.

#### Completion Report

- status: implemented
- what was done: Нормализованы intent, AC и профиль. Проверены CLI/Python parity, конфликт, неполный и смешанный ввод, legacy audit.
- files touched / work locations: [B1 evidence and canonical owners](../superpowers/specs/paos-pmeth-b1-evidence.md).
- technical value delivered: Маршрут и его доказательства связаны в записи B1.
- product value delivered: Проверяемый совет в штатном CLI.
- actual implementation date and time: 18-11-2026 20:43
- verification evidence: [B1 verification](../superpowers/specs/paos-pmeth-b1-evidence.md).
- residual risks: Паритет Web и полезность для реальных агентов проверяются отдельно.
- follow-up: PAOS-PMETH-22.

### Task `PAOS-PMETH-03`

- Task: PAOS-PMETH-03
- Task name: Выбирать методологии соразмерно задаче и объяснять выбор
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized bounded B1 implementation following the plan review.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 20:43
- Depends on: PAOS-PMETH-22
- Blocks: PAOS-PMETH-04
- External references: Нет; internal A не является prerequisite.
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Выдавать объяснимое соразмерное решение по пяти методологиям.
- Technical value: Объяснимые решения по пяти методологиям и baseline/candidate routing evidence.
- Product value: Понимать причины выбора и не выполнять лишнюю методологическую работу.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_catalog.py`; `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Объяснимые решения по пяти методологиям и baseline/candidate routing evidence.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-03-AC01**: Для каждой из пяти методологий возвращаются applicability, reason, evidence refs, требуемая глубина, owner и smallest next action; существующие 12 domains не заменяются.
  - **PAOS-PMETH-03-AC02**: TDD включается для изменяемого тестируемого поведения; Design-DD для journey/UI; FSD условен по frontend coupling; Spec-DD имеет compact/full варианты.
  - **PAOS-PMETH-03-AC03**: Missing evidence даёт вопрос/gap/present_unverified. В read-only пути пользователь уточняет вход и пересчитывает совет без записи. Durable override с причиной и областью применения закреплён за PMETH-18/21 и сохраняет обязательные проверки.
  - **PAOS-PMETH-03-AC04**: Baseline/candidate cases PMETH-22 подтверждают отсутствие blanket FSD/DDD/TDD mandate, скрытых новых gates и ложной готовности.

- Verification gates: PV-ENGINE; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: architect + plugin-runtime-builder; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Объяснимые решения по пяти методологиям и baseline/candidate routing evidence.
- Next step: Следующая зависимость PAOS-PMETH-04.

#### Completion Report

- status: implemented
- what was done: Выбор объясняет применимость, глубину, владельца и следующий шаг для пяти методов. Backend/docs проверены без frontend-гейтов.
- files touched / work locations: [B1 evidence and canonical owners](../superpowers/specs/paos-pmeth-b1-evidence.md).
- technical value delivered: Маршрут и его доказательства связаны в записи B1.
- product value delivered: Проверяемый совет в штатном CLI.
- actual implementation date and time: 18-11-2026 20:43
- verification evidence: [B1 verification](../superpowers/specs/paos-pmeth-b1-evidence.md).
- residual risks: Паритет Web и полезность для реальных агентов проверяются отдельно.
- follow-up: PAOS-PMETH-04.

### Task `PAOS-PMETH-04`

- Task: PAOS-PMETH-04
- Task name: Согласовать версионированный methodology contract
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized bounded B1 implementation following the plan review.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 20:43
- Depends on: PAOS-PMETH-03
- Blocks: PAOS-PMETH-05, PAOS-PMETH-10, PAOS-PMETH-13
- External references: PAOS-FUNC-08
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Сохранить единый совместимый контракт между engine, runner и интерфейсом.
- Technical value: Canonical versioned contract, adapters и compatibility tests.
- Product value: Сохранять согласованность решений между CLI, runner и Web.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_catalog.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `packages/contracts/`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files. Модули и проверки для переиспользования: `packages/contracts/project-analysis.ts`, `packages/contracts/issues/task-profile.ts`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Canonical versioned contract, adapters и compatibility tests.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-04-AC01**: Выбран один schema owner и минимальные Python/TypeScript adapters к существующим контрактам. Project-only facts и task-scoped advice различаются; project/task identity, source/task revisions и evidence refs проверяются на границе.
  - **PAOS-PMETH-04-AC02**: Существующие readiness statuses, domain packets и legacy consumers поддержаны explicit compatibility mapping; unknown/newer versions не превращаются в default success.
  - **PAOS-PMETH-04-AC03**: Decision, plan, execution receipt и acceptance verdict различаются; contract не хранит raw private chat, secrets или полномочия, выведенные из рекомендации.
  - **PAOS-PMETH-04-AC04**: Contract tests покрывают roundtrip, malformed input, wrong project/task/revision и adapter parity; добавление schema не означает runtime activation.

- Verification gates: PV-CONTRACT; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: architect; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Canonical versioned contract, adapters и compatibility tests.
- Next step: Следующая зависимость PAOS-PMETH-05.

#### Completion Report

- status: implemented
- what was done: Python и TypeScript читают контракт v1. Проверены roundtrip, версия, чужой scope и ошибочные ссылки на источники.
- files touched / work locations: [B1 evidence and canonical owners](../superpowers/specs/paos-pmeth-b1-evidence.md).
- technical value delivered: Маршрут и его доказательства связаны в записи B1.
- product value delivered: Проверяемый совет в штатном CLI.
- actual implementation date and time: 18-11-2026 20:43
- verification evidence: [B1 verification](../superpowers/specs/paos-pmeth-b1-evidence.md).
- residual risks: Паритет Web и полезность для реальных агентов проверяются отдельно.
- follow-up: PAOS-PMETH-05.

### Task `PAOS-PMETH-05`

- Task: PAOS-PMETH-05
- Task name: Встроить Spec-Driven маршрут от запроса к проверяемой спецификации
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized bounded B1 implementation following the plan review.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 20:43
- Depends on: PAOS-PMETH-04
- Blocks: PAOS-PMETH-06, PAOS-PMETH-07, PAOS-PMETH-08
- External references: Нет; internal A не является prerequisite.
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Превратить пользовательский запрос в проверяемый контракт выбранного slice.
- Technical value: Concise/full requirements proposal с AC traceability и назначенным owner.
- Product value: Принимать результат по заранее понятным критериям.
- Scope: `plugins/product-agent-os/skills/requirements-author/SKILL.md`; `plugins/product-agent-os/skills/implementation-planner/SKILL.md`; `plugins/product-agent-os/assets/templates/artifact-templates/`; `plugins/product-agent-os/scripts/product_agent_os/templates.py`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files. Модули и проверки для переиспользования: `plugins/product-agent-os/scripts/product_agent_os/control_plane_documents.py`, `plugins/product-agent-os/scripts/product_agent_os/project_formation.py`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Concise/full requirements proposal с AC traceability и назначенным owner.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-05-AC01**: Небольшая задача получает concise scope/AC в существующей задаче или read-only проекции без генерации файла. Сложная получает требования/non-goals/invariants и сценарии через существующего владельца.
  - **PAOS-PMETH-05-AC02**: Каждый AC связан с observable scenario/check/evidence owner либо explicit gap; неоднозначность и предположения вынесены до build.
  - **PAOS-PMETH-05-AC03**: Существующие user-authored требования и их владелец сохраняются. Read-only путь показывает следующий шаг текстом/ссылкой. Staged proposal/diff и применение принадлежат PMETH-16.
  - **PAOS-PMETH-05-AC04**: Greenfield не scaffold-ится до выбранного первого vertical slice и соответствующей authority; изменение спецификации не доказывает работоспособность кода.

- Verification gates: PV-ENGINE; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: plugin-runtime-builder + product-manager; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Concise/full requirements proposal с AC traceability и назначенным owner.
- Next step: Следующая зависимость PAOS-PMETH-07.

#### Completion Report

- status: implemented
- what was done: Компактное или полное предложение связывает AC со сценарием, проверкой или пробелом и владельцем. Проверен greenfield без создания файлов.
- files touched / work locations: [B1 evidence and canonical owners](../superpowers/specs/paos-pmeth-b1-evidence.md).
- technical value delivered: Маршрут и его доказательства связаны в записи B1.
- product value delivered: Проверяемый совет в штатном CLI.
- actual implementation date and time: 18-11-2026 20:43
- verification evidence: [B1 verification](../superpowers/specs/paos-pmeth-b1-evidence.md).
- residual risks: Паритет Web и полезность для реальных агентов проверяются отдельно.
- follow-up: PAOS-PMETH-07.

### Task `PAOS-PMETH-06`

- Task: PAOS-PMETH-06
- Task name: Отслеживать изменения спецификации и устаревший контекст
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B4
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-05
- Blocks: PAOS-PMETH-16, PAOS-PMETH-17
- External references: PAOS-FUNC-02, PAOS-FUNC-25
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Не исполнять устаревший план и сохранять связность требований и evidence.
- Technical value: Revision/impact/disposition records и stale-context regression evidence.
- Product value: Не терять решения и не исполнять устаревшие указания.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/product_agent_os/control_plane_documents.py`; `plugins/product-agent-os/scripts/product_agent_os/documentation_sync.py`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files. Модули и проверки для переиспользования: `plugins/product-agent-os/scripts/product_agent_os/project_formation.py`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Revision/impact/disposition records и stale-context regression evidence.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-06-AC01**: Изменения AC/API/schema/source revision находят затронутые slices/checks и владельцев; текстовый diff не выдаётся за полную semantic impact proof.
  - **PAOS-PMETH-06-AC02**: Stale plan/proposal/receipt не повышает readiness; resume требует актуального context/authority, прежняя история сохранена.
  - **PAOS-PMETH-06-AC03**: Повторная оценка unchanged inputs не пишет документы повторно; conflicting owner edits дают review/handoff, не overwrite.
  - **PAOS-PMETH-06-AC04**: Synthetic concurrent edit, renamed artifact, missing owner и changed acceptance имеют явные outcomes и проверку сохранности.

- Verification gates: PV-ENGINE; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: plugin-runtime-builder + tester; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Revision/impact/disposition records и stale-context regression evidence.
- Next step: Проверить depends_on, source/permission freshness и выбрать отдельно разрешённый bounded slice этой задачи.

#### Completion Report

- status: planned
- what was done: Сформирована карточка; реализация не начата.
- files touched / work locations: Implementation files не менялись этой записью; будущие locations в Scope.
- technical value delivered: Не заявлена до исполнения AC.
- product value delivered: Не заявлена до исполнения AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Только static authoring/split checks; будущие AC не выполнены.
- residual risks: Baseline может измениться; applicability/authority/activation и model usefulness требуют evidence выбранного slice.
- follow-up: Следующий разрешённый slice по DAG, без автоматического запуска.

### Task `PAOS-PMETH-07`

- Task: PAOS-PMETH-07
- Task name: Встроить TDD и воспроизведение ошибок в выполнение slices
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: TDD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized bounded B1 implementation following the plan review.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 20:43
- Depends on: PAOS-PMETH-05
- Blocks: PAOS-PMETH-15, PAOS-PMETH-19
- External references: PAOS-FUNC-21, PAOS-FUNC-22
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Выполнять test-first там, где он проверяет поведение, и честно объяснять исключения.
- Technical value: Test/eval route, RED/GREEN receipts и обоснованные исключения.
- Product value: Получать воспроизводимые исправления и защиту от регрессий.
- Scope: `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`; `plugins/product-agent-os/scripts/product_agent_os/test_strategy_selector.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/assets/templates/workflows/`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files. Модули и проверки для переиспользования: `plugins/product-agent-os/scripts/product_agent_os/test_strategy_selector.py`, `tests/product_agent_os/test_codex_runtime_runner_cli.py`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Test/eval route, RED/GREEN receipts и обоснованные исключения.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-07-AC01**: Read-only маршрут показывает следующий тест для backend bug и source check для docs-only. Synthetic fixture подтверждает один regression check с observable intended RED, minimal GREEN и scoped refactor disposition. Команда, revision и expected/actual сохранены в имеющемся evidence без записи в целевой проект.
  - **PAOS-PMETH-07-AC02**: Setup/import/tool-missing failures не засчитываются как RED; исходный воспроизводимый failure сохраняется при последующем успехе.
  - **PAOS-PMETH-07-AC03**: Behavior-preserving refactor использует characterization/regression; docs/config/subjective LLM outputs получают подходящие static checks/evals без искусственного RED.
  - **PAOS-PMETH-07-AC04**: Недоступная проверка остаётся explicit gap; нельзя переписать/удалить assertion ради green или сделать test count доказательством correctness.

- Verification gates: PV-TDD; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: plugin-runtime-builder + tester; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Test/eval route, RED/GREEN receipts и обоснованные исключения.
- Next step: Следующая зависимость PAOS-PMETH-19.

#### Completion Report

- status: implemented
- what was done: CLI предлагает backend-тест и docs-only источник. Фактический RED, минимальный GREEN и ошибка импорта зафиксированы отдельно.
- files touched / work locations: [B1 evidence and canonical owners](../superpowers/specs/paos-pmeth-b1-evidence.md).
- technical value delivered: Маршрут и его доказательства связаны в записи B1.
- product value delivered: Проверяемый совет в штатном CLI.
- actual implementation date and time: 18-11-2026 20:43
- verification evidence: [B1 verification](../superpowers/specs/paos-pmeth-b1-evidence.md).
- residual risks: Паритет Web и полезность для реальных агентов проверяются отдельно.
- follow-up: PAOS-PMETH-19.

### Task `PAOS-PMETH-08`

- Task: PAOS-PMETH-08
- Task name: Встроить Design-Driven сценарии и матрицу состояний
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B3
- Methodologies: Design-DD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B3 local read-only implementation and synthetic verification.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:37
- Depends on: PAOS-PMETH-05
- Blocks: PAOS-PMETH-09
- External references: UI-12
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Проектировать пользовательский сценарий и состояния до реализации изменённого journey.
- Technical value: Journey/state matrix, design references и acceptance boundaries.
- Product value: Проверять удобство сценария до дорогой реализации.
- Scope: `tools/project-methodology.mts`; `tools/project-methodology/design.mts`; `tests/fixtures/product_agent_os/pmeth-b3-design.json`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Journey/state matrix, design references и acceptance boundaries.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-08-AC01**: Изменяемый journey определяет цель, шаги, данные, interaction/error/empty/loading/dirty states и accessibility. Для существенного или неясного journey фиксируются гипотеза о проблеме и наблюдение с представительным пользователем либо evidence gap. Backend-only получает not_applicable.
  - **PAOS-PMETH-08-AC02**: Существующий дизайн и design system переиспользованы, missing states предложены отдельно; новый макет не объявлен утверждённым пользователем.
  - **PAOS-PMETH-08-AC03**: Прототип различает synthetic/current/unavailable data и реальные API ограничения; невозможные состояния не обещаны как доступная функция.
  - **PAOS-PMETH-08-AC04**: Design artifacts, implementation и human acceptance имеют отдельные owners/evidence; небольшая UI правка не требует redesign всего проекта.

- Verification gates: PV-ENGINE. [Выполненные проверки](../superpowers/specs/paos-pmeth-b3-evidence.md#design-verification).
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: product-manager + plugin-runtime-builder; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Journey/state matrix, design references и acceptance boundaries.
- Next step: 09 проверяет связанный UI-сценарий.

#### Completion Report

- status: implemented
- what was done: Цель, шаги, данные, матрица состояний и доступность привязаны к ревизии.
- files touched / work locations: [Пути реализации и фикстуры](../superpowers/specs/paos-pmeth-b3-evidence.md#design-verification).
- technical value delivered: Результат привязан к ревизии и имеет явные доказательства.
- product value delivered: Видны существующие активы, предложенные состояния и пробелы.
- actual implementation date and time: 19-11-2026 11:37
- verification evidence: [Фактические проверки](../superpowers/specs/paos-pmeth-b3-evidence.md#design-verification).
- residual risks: Наблюдение с представительным пользователем требуется для выбранного реального сценария.
- follow-up: 09 проверяет связанный UI-сценарий.

### Task `PAOS-PMETH-09`

- Task: PAOS-PMETH-09
- Task name: Проверять пользовательский интерфейс по принятому design-контракту
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B3
- Methodologies: Design-DD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B3 local read-only implementation and synthetic verification.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:37
- Depends on: PAOS-PMETH-08
- Blocks: Нет.
- External references: PAOS-FUNC-19, UI-12
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Сопоставлять работающий интерфейс с принятым design-контрактом.
- Technical value: Current-build visual/interaction evidence либо явный unavailable gap.
- Product value: Видеть расхождения между дизайном и работающим интерфейсом.
- Scope: `tools/project-methodology/design.mts`; `apps/web/src/design/parity.css`; `tests/web/single-window/methodology-advice-browser-acceptance.mts`; `tests/fixtures/product_agent_os/pmeth-b3-composition.json`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Current-build visual/interaction evidence либо явный unavailable gap.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-09-AC01**: План проверки выбирает доступные component/browser/visual/keyboard checks изменённого journey, viewport/theme/long-content состояния и source/build/harness provenance.
  - **PAOS-PMETH-09-AC02**: Композиция и действия проверяются помимо overflow/contrast; intentional fixture mismatch выявляется, baseline updates явно reviewable.
  - **PAOS-PMETH-09-AC03**: Screenshot/prototype pass не объявляется human usability acceptance, WCAG certification или доказательством API side effect.
  - **PAOS-PMETH-09-AC04**: Если runtime/browser не разрешён или недоступен, возвращается gap с безопасным next action без обхода ограничений и подмены старым screenshot.

- Verification gates: PV-DESIGN. [Выполненные проверки](../superpowers/specs/paos-pmeth-b3-evidence.md#design-verification).
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: tester + plugin-runtime-builder; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Current-build visual/interaction evidence либо явный unavailable gap.
- Next step: При расширении профиля повторить PMETH-23.

#### Completion Report

- status: implemented
- what was done: Состояния, доступность и композиция сопоставлены с версией design-контракта.
- files touched / work locations: [Пути реализации и фикстуры](../superpowers/specs/paos-pmeth-b3-evidence.md#design-verification).
- technical value delivered: Результат привязан к ревизии и имеет явные доказательства.
- product value delivered: Две локализации проверены в браузере. При недоступности браузера виден пробел.
- actual implementation date and time: 19-11-2026 11:37
- verification evidence: [Фактические проверки](../superpowers/specs/paos-pmeth-b3-evidence.md#design-verification).
- residual risks: Технические проверки ограничены синтетическим сценарием.
- follow-up: При расширении профиля повторить PMETH-23.

### Task `PAOS-PMETH-10`

- Task: PAOS-PMETH-10
- Task name: Определять применимость FSD и предлагать архитектурный выбор
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B3
- Methodologies: FSD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B3 local read-only implementation and synthetic verification.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:37
- Depends on: PAOS-PMETH-04
- Blocks: PAOS-PMETH-11
- External references: PAOS-FUNC-30
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Предлагать FSD только при доказанной полезности для frontend проекта пользователя.
- Technical value: FSD applicability decision и architecture proposal с альтернативами.
- Product value: Выбирать архитектуру по пользе, а не моде или названию папок.
- Scope: `tools/project-methodology.mts`; `tools/project-methodology/architecture.mts`; `tests/web/project-methodology-b3.test.mts`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: FSD applicability decision и architecture proposal с альтернативами.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-10-AC01**: Small/static frontend, backend/native-only, растущий frontend и уже модульный legacy получают разные рекомендации с подтверждёнными signals.
  - **PAOS-PMETH-10-AC02**: Сравниваются сохранить архитектуру, усилить boundaries и gradual FSD; выбор учитывает coupling, change frequency, ownership и migration cost.
  - **PAOS-PMETH-10-AC03**: Предложение начинается со страниц и подтверждённого coupling. Public APIs и нижние layers/slices появляются при подтверждённой потребности. Backend/Python и native получают применимую архитектурную политику.
  - **PAOS-PMETH-10-AC04**: Архитектурный proposal требует соответствующего решения владельца перед migration; отсутствие FSD не является дефектом само по себе.

- Verification gates: PV-ENGINE. [Выполненные проверки](../superpowers/specs/paos-pmeth-b3-evidence.md#architecture-evidence).
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: architect + plugin-runtime-builder; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: FSD applicability decision и architecture proposal с альтернативами.
- Next step: 11 проверяет публичные границы и владельцев.

#### Completion Report

- status: implemented
- what was done: Оценка применимости основана на наблюдаемых импортах и стеке.
- files touched / work locations: [Пути реализации и фикстуры](../superpowers/specs/paos-pmeth-b3-evidence.md#architecture-evidence).
- technical value delivered: Результат привязан к ревизии и имеет явные доказательства.
- product value delivered: Решения различают статический, модульный, связанный frontend и другие стеки.
- actual implementation date and time: 19-11-2026 11:37
- verification evidence: [Фактические проверки](../superpowers/specs/paos-pmeth-b3-evidence.md#architecture-evidence).
- residual risks: Неполное покрытие обозначено как partial с причиной.
- follow-up: 11 проверяет публичные границы и владельцев.

### Task `PAOS-PMETH-11`

- Task: PAOS-PMETH-11
- Task name: Проверять frontend-зависимости по исходникам
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B3
- Methodologies: FSD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B3 local read-only implementation and synthetic verification.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:37
- Depends on: PAOS-PMETH-10
- Blocks: PAOS-PMETH-12
- External references: PAOS-FUNC-14, PAOS-FUNC-30
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Различать folder signals и проверенные границы кода на поддерживаемом языке.
- Technical value: Source-bound findings, coverage/unknown report и boundary regression cases.
- Product value: Получать проверяемые архитектурные findings вместо догадок.
- Scope: `apps/local-service/src/code-index/lexical.mts`; `apps/local-service/src/code-index/resolver-config.mts`; `apps/local-service/src/code-index/service.mts`; `tools/project-methodology/architecture.mts`; `tests/web/graph-imports.test.mts`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Source-bound findings, coverage/unknown report и boundary regression cases.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-11-AC01**: FSD rules используют наблюдаемые рёбра F14 для JS/TS/TSX и привязаны к source revision. Покрытие TSImportType, reexports, tsconfig aliases/extends и literal dynamic imports проверяется явно.
  - **PAOS-PMETH-11-AC02**: Unsupported syntax/alias/symlink/out-of-scope source и CLI без доступного адаптера дают partial/unknown с coverage и объяснением. Частичный graph и folder signals не дают present_verified.
  - **PAOS-PMETH-11-AC03**: Нарушения имеют путь/строку/rule/owner и отделены от допустимого entity public API и legacy exceptions.
  - **PAOS-PMETH-11-AC04**: Переиспользованы F14 code-index, parser/resolver и fixtures. F30 остаётся import-only reference. Проверены meaningful parser cases, циклы и no-source-mutation hashes без обязательной установки.

- Verification gates: PV-FSD. [Выполненные проверки](../superpowers/specs/paos-pmeth-b3-evidence.md#architecture-evidence).
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: plugin-runtime-builder + tester; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Source-bound findings, coverage/unknown report и boundary regression cases.
- Next step: 12 использует наблюдаемые находки в предложении.

#### Completion Report

- status: implemented
- what was done: Проверены слои, публичные API, циклы, @x и точные legacy-исключения.
- files touched / work locations: [Пути реализации и фикстуры](../superpowers/specs/paos-pmeth-b3-evidence.md#architecture-evidence).
- technical value delivered: Результат привязан к ревизии и имеет явные доказательства.
- product value delivered: Отчёт показывает импорт, якорь, правило и владельца.
- actual implementation date and time: 19-11-2026 11:37
- verification evidence: [Фактические проверки](../superpowers/specs/paos-pmeth-b3-evidence.md#architecture-evidence).
- residual risks: Неподдерживаемые импорты явно ограничивают покрытие.
- follow-up: 12 использует наблюдаемые находки в предложении.

### Task `PAOS-PMETH-12`

- Task: PAOS-PMETH-12
- Task name: Создавать поэтапный FSD migration proposal для проекта пользователя
- Status: implemented
- Priority: P2
- Direction: B — user projects
- Delivery group: B3
- Methodologies: FSD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B3 local read-only implementation and synthetic verification.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:37
- Depends on: PAOS-PMETH-11
- Blocks: Нет.
- External references: Нет; internal A не является prerequisite.
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Планировать минимальную обратимую migration по принятым boundaries.
- Technical value: Поэтапный migration plan с pilot/public APIs/rollback и staged diff.
- Product value: Улучшать frontend постепенно с сохранением рабочего поведения.
- Scope: `tools/project-methodology/architecture.mts`; `tests/web/project-methodology-b3.test.mts`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Read-only migration proposal с reversible page pilot, public APIs, import ratchet и критериями следующего checkpoint.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-12-AC01**: Proposal содержит baseline imports, минимальный pilot, AC, owners, dependencies, compatibility bridges и rollback; нет mandatory full rewrite.
  - **PAOS-PMETH-12-AC02**: Сначала граница и один page pilot с public API/import ratchet. Вынос в shared/entities оправдан подтверждённым повторным использованием. Следующие checkpoints зависят от принятия предыдущих; возможна остановка на пилоте.
  - **PAOS-PMETH-12-AC03**: Proposal описывает ожидаемое сохранение user files, dirty changes и business/API semantics и показывает, как проверить границы legacy imports. На этой стадии исходники сохраняются; фактический перенос проверяется в PMETH-23, если вошёл в scope пилота.
  - **PAOS-PMETH-12-AC04**: Готовый read-only proposal доступен в памяти. Staged diff и apply по отдельно выбранному FSD пути используют PMETH-16 writer и проверяются в PMETH-23. Target write и hook activation требуют отдельной authority.

- Verification gates: PV-STAGE. [Выполненные проверки](../superpowers/specs/paos-pmeth-b3-evidence.md#migration-proposal).
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: architect + plugin-runtime-builder; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Read-only migration proposal с reversible page pilot, public APIs, import ratchet и критериями следующего checkpoint.
- Next step: Запись требует отдельно разрешённой области.

#### Completion Report

- status: implemented
- what was done: Подготовлено предложение для одной страницы с baseline, re-export, import ratchet и откатом.
- files touched / work locations: [Пути реализации и фикстуры](../superpowers/specs/paos-pmeth-b3-evidence.md#migration-proposal).
- technical value delivered: Результат привязан к ревизии и имеет явные доказательства.
- product value delivered: После первой страницы можно остановиться и проверить зафиксированные импорты.
- actual implementation date and time: 19-11-2026 11:37
- verification evidence: [Фактические проверки](../superpowers/specs/paos-pmeth-b3-evidence.md#migration-proposal).
- residual risks: Перенос зависит от PMETH-16 и приёмки выбранного профиля PMETH-23.
- follow-up: Запись требует отдельно разрешённой области.

### Task `PAOS-PMETH-13`

- Task: PAOS-PMETH-13
- Task name: Встроить ADD-контракт исполнения и ownership
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B4
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-04
- Blocks: PAOS-PMETH-14, PAOS-PMETH-15
- External references: PAOS-FUNC-15, PAOS-FUNC-16
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Поручать агентам ограниченную проверяемую работу без расширения полномочий.
- Technical value: Bounded agent context, ownership/budget/stop records и guard tests.
- Product value: Доверять агенту ограниченную задачу с понятной остановкой.
- Scope: `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`; `plugins/product-agent-os/skills/agent-team-designer/SKILL.md`; `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/guards.py`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Bounded agent context, ownership/budget/stop records и guard tests.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-13-AC01**: Slice передаёт goal/AC/source revision, allowed/forbidden paths, checks, stop/handoff; обычная задача использует concise route.
  - **PAOS-PMETH-13-AC02**: Один агент — default; parallel work только при независимом ownership и разрешённом host capability; overlapping files сериализуются.
  - **PAOS-PMETH-13-AC03**: Model/reasoning/tool budgets следуют действующей конфигурации; profile не предоставляет отдельный sandbox, escalation/provider selection не выводятся из роли.
  - **PAOS-PMETH-13-AC04**: Unknown capability, timeout, partial child и stale handoff не становятся success; no silent fallback и bounded retry имеют явные receipts.

- Verification gates: PV-ADD; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: lifecycle-orchestrator + plugin-runtime-builder; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Bounded agent context, ownership/budget/stop records и guard tests.
- Next step: Проверить depends_on, source/permission freshness и выбрать отдельно разрешённый bounded slice этой задачи.

#### Completion Report

- status: planned
- what was done: Сформирована карточка; реализация не начата.
- files touched / work locations: Implementation files не менялись этой записью; будущие locations в Scope.
- technical value delivered: Не заявлена до исполнения AC.
- product value delivered: Не заявлена до исполнения AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Только static authoring/split checks; будущие AC не выполнены.
- residual risks: Baseline может измениться; applicability/authority/activation и model usefulness требуют evidence выбранного slice.
- follow-up: Следующий разрешённый slice по DAG, без автоматического запуска.

### Task `PAOS-PMETH-14`

- Task: PAOS-PMETH-14
- Task name: Связать выбранные методологии с доступными skills и инструментами
- Status: planned
- Priority: P2
- Direction: B — user projects
- Delivery group: B4
- Methodologies: ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-13
- Blocks: Нет.
- External references: PAOS-FUNC-12
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Связать решение с реально доступным исполнителем без скрытой установки.
- Technical value: Skill/tool route с provenance, capabilities и безопасным fallback disposition.
- Product value: Использовать доступные возможности без скрытой настройки окружения.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/skills/references/`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files. Модули и проверки для переиспользования: `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Skill/tool route с provenance, capabilities и безопасным fallback disposition.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-14-AC01**: Для каждого метода выбраны существующий canonical skill/workflow и task-relevant inputs; нет загрузки всех skills или выдуманного доступного tool.
  - **PAOS-PMETH-14-AC02**: Installed/staged/exposed/invoked различаются; missing skill/tool даёт safe manual/staged next action и gap.
  - **PAOS-PMETH-14-AC03**: Skills/MCP/docs содержимое не повышает полномочия; embedded instructions, malicious commands и external writes не исполняются как рекомендации.
  - **PAOS-PMETH-14-AC04**: Новые install/connect/activation остаются отдельными разрешёнными действиями; модельный prompt не копирует секреты и raw private chats.

- Verification gates: PV-ADD; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: plugin-runtime-builder; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Skill/tool route с provenance, capabilities и безопасным fallback disposition.
- Next step: Проверить depends_on, source/permission freshness и выбрать отдельно разрешённый bounded slice этой задачи.

#### Completion Report

- status: planned
- what was done: Сформирована карточка; реализация не начата.
- files touched / work locations: Implementation files не менялись этой записью; будущие locations в Scope.
- technical value delivered: Не заявлена до исполнения AC.
- product value delivered: Не заявлена до исполнения AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Только static authoring/split checks; будущие AC не выполнены.
- residual risks: Baseline может измениться; applicability/authority/activation и model usefulness требуют evidence выбранного slice.
- follow-up: Следующий разрешённый slice по DAG, без автоматического запуска.

### Task `PAOS-PMETH-15`

- Task: PAOS-PMETH-15
- Task name: Объединить методологии в один соразмерный delivery plan
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B4
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-07, PAOS-PMETH-13
- Blocks: PAOS-PMETH-16, PAOS-PMETH-17
- External references: Нет; internal A не является prerequisite.
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Получить один рабочий delivery DAG с минимально необходимыми gates.
- Technical value: Единый delivery DAG и связи методов с каждым slice.
- Product value: Работать по одному согласованному плану вместо нескольких очередей.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`; `plugins/product-agent-os/skills/implementation-planner/SKILL.md`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files. Модули и проверки для переиспользования: `plugins/product-agent-os/scripts/product_agent_os/project_formation.py`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Единый delivery DAG и связи методов с каждым slice.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-15-AC01**: Один DAG использует methodology_synthesis и formation_plan. Canonical name и alias одного существующего файла дают один артефакт и одного владельца с обоими основаниями.
  - **PAOS-PMETH-15-AC02**: Dependencies отражают фактические prerequisites. PMETH-08/09 и PMETH-10–12 входят только в Design/FSD ветки, PMETH-14 добавляет skills по потребности. Компактная bug/docs рекомендация доступна через PMETH-19/20 без delivery DAG.
  - **PAOS-PMETH-15-AC03**: Каждый slice имеет input/output/owner/AC/checks/stop; backend/API/AI paths получают только релевантные gates, subjective AI quality использует evals.
  - **PAOS-PMETH-15-AC04**: Cycle/conflict/accepted-gap cases дают объяснимый next action; methodology advice не расширяет авторизацию и не запускает plan автоматически.

- Verification gates: PV-ENGINE; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: architect + plugin-runtime-builder; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Единый delivery DAG и связи методов с каждым slice.
- Next step: Проверить depends_on, source/permission freshness и выбрать отдельно разрешённый bounded slice этой задачи.

#### Completion Report

- status: planned
- what was done: Сформирована карточка; реализация не начата.
- files touched / work locations: Implementation files не менялись этой записью; будущие locations в Scope.
- technical value delivered: Не заявлена до исполнения AC.
- product value delivered: Не заявлена до исполнения AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Только static authoring/split checks; будущие AC не выполнены.
- residual risks: Baseline может измениться; applicability/authority/activation и model usefulness требуют evidence выбранного slice.
- follow-up: Следующий разрешённый slice по DAG, без автоматического запуска.

### Task `PAOS-PMETH-16`

- Task: PAOS-PMETH-16
- Task name: Подключить безопасные staging, preview и разрешённое применение
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B4
- Methodologies: Spec-DD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-06, PAOS-PMETH-15
- Blocks: PAOS-PMETH-21
- External references: PAOS-FUNC-13
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Использовать существующий approval-aware pipeline без потери user-authored файлов.
- Technical value: Stage/preview/approval/apply/rollback receipts на fixture targets.
- Product value: Сохранять собственные файлы и контролировать применение предложений.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`; `plugins/product-agent-os/scripts/product_agent_os/stage_manifest.py`; `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`; `plugins/product-agent-os/scripts/merge_infrastructure.py`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files. Модули и проверки для переиспользования: `plugins/product-agent-os/scripts/product_agent_os/project_formation.py`, `packages/contracts/artifacts/document-apply.ts`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Stage/preview/approval/apply/rollback receipts на fixture targets.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-16-AC01**: Infrastructure bundle использует G9 formation/dry-run/stage/manifest/merge, допустимый single-document proposal использует F13 document apply. Вид операции выбирает одного writer; stage вне target, запись требует точную authority.
  - **PAOS-PMETH-16-AC02**: Существующий preview показывает owned paths, user-file handling, method/AC links, side effects и writer. Unmarked AGENTS/config/hooks сохраняются; apply доступен только у своего маршрута.
  - **PAOS-PMETH-16-AC03**: Preview/apply связаны точным digest, project/task, revision и operation ID. Drift, wrong root/project, traversal/symlink и stale approval отклоняются; recovery сохраняет edits и не повторяет эффект с unknown outcome.
  - **PAOS-PMETH-16-AC04**: Synthetic apply/rollback проверяет только fixture target и byte preservation; создание proposal не включает hooks/automation/install/provider.

- Verification gates: PV-STAGE; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: L
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: plugin-runtime-builder + tester; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Stage/preview/approval/apply/rollback receipts на fixture targets.
- Next step: Проверить depends_on, source/permission freshness и выбрать отдельно разрешённый bounded slice этой задачи.

#### Completion Report

- status: planned
- what was done: Сформирована карточка; реализация не начата.
- files touched / work locations: Implementation files не менялись этой записью; будущие locations в Scope.
- technical value delivered: Не заявлена до исполнения AC.
- product value delivered: Не заявлена до исполнения AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Только static authoring/split checks; будущие AC не выполнены.
- residual risks: Baseline может измениться; applicability/authority/activation и model usefulness требуют evidence выбранного slice.
- follow-up: Следующий разрешённый slice по DAG, без автоматического запуска.

### Task `PAOS-PMETH-17`

- Task: PAOS-PMETH-17
- Task name: Собирать evidence и вычислять готовность по критериям
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B4
- Methodologies: Spec-DD, TDD, Design-DD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-06, PAOS-PMETH-15
- Blocks: PAOS-PMETH-18
- External references: PAOS-FUNC-02
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Обосновывать готовность каждой применимой проверки актуальным evidence.
- Technical value: Criterion/evidence/readiness ledger с различением technical/human/release.
- Product value: Отличать подтверждённый результат от плана и предположения.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`; `plugins/product-agent-os/skills/completion-skeptic/SKILL.md`; `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files. Модули и проверки для переиспользования: `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`, `apps/local-service/src/tasks/user-commands.mts`, `apps/local-service/src/workflows/guards.mts`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Criterion/evidence/readiness ledger с различением technical/human/release.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-17-AC01**: Requirement → stable AC ID → scenario/check → receipt → verdict имеет owner, revision/environment и применимость. В synthetic задаче manual acceptance сохраняется для двух AC, technical evidence засчитывается только у AC с привязанным receipt нужной revision. Accepted gap остаётся отдельным.
  - **PAOS-PMETH-17-AC02**: Переиспользованы task_routing input_digest/check_observations и существующие receipts/acceptTask. Caller-reported results, detection, generated files и test count не дают technical passed; missing/stale/failed/partial видны.
  - **PAOS-PMETH-17-AC03**: Expected implementation/provider path проверяется runtime evidence только когда claim это требует и действие разрешено; unit smoke не объявляет activation.
  - **PAOS-PMETH-17-AC04**: CLI pilot связывает применимые методы с checks на одном fixture revision. Technical, manual/human и release acceptance различаются. Visual/FSD/target-apply evidence требуется для соответствующих claims PMETH-23.

- Verification gates: PV-EVIDENCE; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: tester + plugin-runtime-builder; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Criterion/evidence/readiness ledger с различением technical/human/release.
- Next step: Проверить depends_on, source/permission freshness и выбрать отдельно разрешённый bounded slice этой задачи.

#### Completion Report

- status: planned
- what was done: Сформирована карточка; реализация не начата.
- files touched / work locations: Implementation files не менялись этой записью; будущие locations в Scope.
- technical value delivered: Не заявлена до исполнения AC.
- product value delivered: Не заявлена до исполнения AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Только static authoring/split checks; будущие AC не выполнены.
- residual risks: Baseline может измениться; applicability/authority/activation и model usefulness требуют evidence выбранного slice.
- follow-up: Следующий разрешённый slice по DAG, без автоматического запуска.

### Task `PAOS-PMETH-18`

- Task: PAOS-PMETH-18
- Task name: Определить durable state методологий в Web/desktop
- Status: planned
- Priority: P2
- Direction: B — user projects
- Delivery group: B4
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-17, PAOS-PMETH-19
- Blocks: PAOS-PMETH-21
- External references: PAOS-FUNC-02, PAOS-FUNC-08, PAOS-FUNC-22, PAOS-FUNC-28, PAOS-FUNC-29
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Хранить согласованное состояние проекта и задачи без второго владельца статуса.
- Technical value: Durable profile/decision/evidence model и synthetic migration/recovery checks.
- Product value: Продолжать работу без расхождений project/task state.
- Scope: `packages/contracts/`; `apps/local-service/src/storage/`; `apps/local-service/src/task-manager/service.mts`; `apps/local-service/src/artifacts/service.mts`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files. Модули и проверки для переиспользования: `apps/local-service/src/project-scans/service.mts`, `packages/contracts/issues/task-profile.ts`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Durable profile/decision/evidence model и synthetic migration/recovery checks.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-18-AC01**: Project facts, task advice, persisted decision и criterion evidence имеют canonical owners в scans, задачах/ссылках и evidence. Новый durable record оправдан только подтверждённым пробелом, чтение PMETH-19 не требует миграции.
  - **PAOS-PMETH-18-AC02**: Version/revision/CAS, history, project isolation и explicit unknown поддержаны. Override хранит причину, область, автора и revisions, сохраняя обязательные проверки. Older clients/newer schema не теряют данные.
  - **PAOS-PMETH-18-AC03**: Если нужна migration, она additive/recoverable на synthetic backup/restore с compatibility checks; не читать/мигрировать реальную user DB этим slice.
  - **PAOS-PMETH-18-AC04**: Schema не хранит secrets/raw private chat; отсутствие token/cost telemetry остаётся null/unavailable, не создаёт F11 scope.

- Verification gates: PV-STORAGE; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: L
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: architect + builder — storage/contracts; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Durable profile/decision/evidence model и synthetic migration/recovery checks.
- Next step: Проверить depends_on, source/permission freshness и выбрать отдельно разрешённый bounded slice этой задачи.

#### Completion Report

- status: planned
- what was done: Сформирована карточка; реализация не начата.
- files touched / work locations: Implementation files не менялись этой записью; будущие locations в Scope.
- technical value delivered: Не заявлена до исполнения AC.
- product value delivered: Не заявлена до исполнения AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Только static authoring/split checks; будущие AC не выполнены.
- residual risks: Baseline может измениться; applicability/authority/activation и model usefulness требуют evidence выбранного slice.
- follow-up: Следующий разрешённый slice по DAG, без автоматического запуска.

### Task `PAOS-PMETH-19`

- Task: PAOS-PMETH-19
- Task name: Связать Python methodology engine с API и runtime приложения
- Status: implemented
- Priority: P2
- Direction: B — user projects
- Delivery group: B2
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B2 local implementation, synthetic acceptance and rollout disposition.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:10
- Depends on: PAOS-PMETH-07
- Blocks: PAOS-PMETH-18, PAOS-PMETH-20
- External references: PAOS-FUNC-01, PAOS-FUNC-08, PAOS-FUNC-27
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Довести существующий methodology engine до наблюдаемого application path.
- Technical value: Versioned bridge/API и current-path activation/negative receipts.
- Product value: Использовать методологический путь через приложение с наблюдаемым результатом.
- Scope: `apps/local-service/src/http/application.mts`; `apps/local-service/src/runtime/`; `packages/contracts/`; `plugins/product-agent-os/scripts/product_agent_os/`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files. Модули и проверки для переиспользования: `apps/local-service/src/project-analysis/bridge.py`, `apps/local-service/src/project-analysis/service.mts`, `apps/local-service/src/project-scans/service.mts`, `packages/contracts/project-analysis.ts`, `tests/web/project-analysis-api.test.mts`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Read-only task advice через существующий Project Analysis API, CLI parity, partial/last relevant stage и negative receipts.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-19-AC01**: Guarded Project Analysis HTTP → Python bridge возвращает task-scoped advice отдельно от project facts. Эквивалентные bug/docs запросы при одинаковых данных и coverage дают те же решения и причины в CLI. Если Web видит только metadata, а CLI прочитал исходники, различие объясняется coverage и partial/unknown. Ответ другого project/task/revision или неподдержанной версии отклоняется.
  - **PAOS-PMETH-19-AC02**: Read-only запрос проверяет session/origin/project scope, input bounds и cancellation. CSRF применяется по HTTP-методу и действующему контракту. Target write и новый durable store не требуются. PMETH-16/21 владеют mutating route и проверками его полномочий.
  - **PAOS-PMETH-19-AC03**: Receipt показывает intended path/selector, partial/ready/warnings и причину. После analysis → schema/code_database открытие advice сохраняет последнюю релевантную стадию analysis нужной revision либо объясняет следующий шаг. Bridge failure виден без маскировки fallback.
  - **PAOS-PMETH-19-AC04**: Bridge не вызывает model/provider, не запускает произвольный repo command и не использует реальные credentials; pinned-source изменения следуют TEST qualification route.

- Verification gates: PV-BRIDGE; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: L
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: builder — local-service + plugin-runtime-builder; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Read-only task advice через существующий Project Analysis API, CLI parity, partial/last relevant stage и negative receipts.
- Next step: PAOS-PMETH-20

#### Completion Report

- status: implemented
- what was done: Подключён guarded HTTP endpoint и изолированный Python bridge. Паритет CLI/Web, scope, ошибки и отмена проверены.
- files touched / work locations: [B2 evidence and canonical route](../superpowers/specs/paos-pmeth-b2-evidence.md).
- technical value delivered: Подтверждено в разрешённом объёме B2.
- product value delivered: Проверяемый совет по сохранённой задаче.
- actual implementation date and time: 19-11-2026 11:10
- verification evidence: [B2 verification](../superpowers/specs/paos-pmeth-b2-evidence.md).
- residual risks: Поставка на hold. Для новых профилей и понимания человеком нужны отдельные доказательства.
- follow-up: PAOS-PMETH-20.

### Task `PAOS-PMETH-20`

- Task: PAOS-PMETH-20
- Task name: Показать пользователю выбор, план и доказательства в интерфейсе
- Status: implemented
- Priority: P2
- Direction: B — user projects
- Delivery group: B2
- Methodologies: Design-DD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B2 local implementation, synthetic acceptance and rollout disposition.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:10
- Depends on: PAOS-PMETH-19
- Blocks: PAOS-PMETH-21, PAOS-PMETH-26
- External references: PAOS-FUNC-23, PAOS-FUNC-24, PAOS-FUNC-27, UI-12
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Помочь пользователю понять выбор, ограничения и следующий шаг.
- Technical value: Утверждённый UI flow, реализация выбранного scope и browser evidence.
- Product value: Понимать следующий шаг, ограничения и причины остановки.
- Scope: `apps/web/src/ui/App.tsx`; `apps/web/src/features/tasks/`; `apps/web/src/features/projects/`; `apps/web/src/locales/`; `docs/frontend/`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files. Модули и проверки для переиспользования: `apps/web/src/features/projects/project-analysis.css`, `tests/web/project-analysis-api.test.mts`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Read-only bug/docs flow в Sources и Teams & Tasks, synthetic browser и результат проверки понимания либо явный gap.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-20-AC01**: Project facts видны в Sources, task advice и следующий проверяемый шаг — в существующем Teams & Tasks flow. Согласованы минимальные placement/states. Видны причина, глубина и required/optional/not_applicable.
  - **PAOS-PMETH-20-AC02**: Показаны source/coverage/unknown, scope, permissions и причины остановки. Сценарий понимания проверяет, может ли человек без подсказки объяснить совет, назвать следующий шаг и отличить просмотр от применения. Результат или evidence gap записан по PMETH-22.
  - **PAOS-PMETH-20-AC03**: Проверены loading/empty/error/stale/partial и applicable permission-required, RU/EN, themes и keyboard/focus. Partial показывает доступные факты и предупреждения, недоступный backend не подменяется fixture success. PMETH-21/23 проверяют конфликт и apply для записи.
  - **PAOS-PMETH-20-AC04**: Synthetic browser проходит PMETH-19 API для backend bug и docs-only, включая wrong project/task, partial и смену latest scan stage. Target и durable methodology state не меняются. Persisted override/audit принадлежат PMETH-18/21.

- Verification gates: PV-UI; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: L
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: product-manager + builder — web; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Read-only bug/docs flow в Sources и Teams & Tasks, synthetic browser и результат проверки понимания либо явный gap.
- Next step: PAOS-PMETH-26

#### Completion Report

- status: implemented
- what was done: В существующей сводке задачи появился совет. Проверены RU/EN, обе темы, клавиатура и состояния результата. Проверка понимания человеком остаётся пробелом.
- files touched / work locations: [B2 evidence and canonical route](../superpowers/specs/paos-pmeth-b2-evidence.md).
- technical value delivered: Подтверждено в разрешённом объёме B2.
- product value delivered: Проверяемый совет по сохранённой задаче.
- actual implementation date and time: 19-11-2026 11:10
- verification evidence: [B2 verification](../superpowers/specs/paos-pmeth-b2-evidence.md).
- residual risks: Поставка на hold. Для новых профилей и понимания человеком нужны отдельные доказательства.
- follow-up: PAOS-PMETH-26.

### Task `PAOS-PMETH-21`

- Task: PAOS-PMETH-21
- Task name: Обрабатывать drift, остановку, возобновление и аудит
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B4
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-16, PAOS-PMETH-18, PAOS-PMETH-20
- Blocks: Нет.
- External references: PAOS-FUNC-21
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Безопасно продолжать работу после изменения контекста или остановки.
- Technical value: Drift/stop/resume/audit records и replay/data-preservation checks.
- Product value: Восстанавливаться после остановки без повторного побочного эффекта.
- Scope: `apps/local-service/src/runtime/`; `apps/local-service/src/sessions/`; `apps/local-service/src/storage/`; `plugins/product-agent-os/scripts/codex_runtime_runner/`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Drift/stop/resume/audit records и replay/data-preservation checks.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-21-AC01**: Изменение task/source/profile/permission revision инвалидирует зависимую authority/readiness; replan объясняет затронутый scope без автозаписи в target.
  - **PAOS-PMETH-21-AC02**: Stop/cancel и unknown outcome не replay-ят эффект; resume требует matching project/task/checkpoint и текущие permissions.
  - **PAOS-PMETH-21-AC03**: Audit сохраняет минимальные records с redaction, owner и временем. Manual override/disposition видимы в существующей задаче, partial/failed attempts сохранены. Preview/apply показывают digest/revision, diff, conflict и authority state.
  - **PAOS-PMETH-21-AC04**: Restart/bridge failure/concurrent edit/budget exhaustion имеют synthetic tests и visible next action; unattended automation и closed-App operation не заявлены.

- Verification gates: PV-RECOVERY; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: L
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: builder — runtime + tester; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Drift/stop/resume/audit records и replay/data-preservation checks.
- Next step: Проверить depends_on, source/permission freshness и выбрать отдельно разрешённый bounded slice этой задачи.

#### Completion Report

- status: planned
- what was done: Сформирована карточка; реализация не начата.
- files touched / work locations: Implementation files не менялись этой записью; будущие locations в Scope.
- technical value delivered: Не заявлена до исполнения AC.
- product value delivered: Не заявлена до исполнения AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Только static authoring/split checks; будущие AC не выполнены.
- residual risks: Baseline может измениться; applicability/authority/activation и model usefulness требуют evidence выбранного slice.
- follow-up: Следующий разрешённый slice по DAG, без автоматического запуска.

### Task `PAOS-PMETH-22`

- Task: PAOS-PMETH-22
- Task name: Подготовить baseline и acceptance eval matrix пользовательских проектов
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized bounded B1 implementation following the plan review.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 20:43
- Depends on: PAOS-PMETH-02
- Blocks: PAOS-PMETH-03
- External references: PAOS-FUNC-23
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Определить ожидаемое поведение и baseline до изменения маршрутов.
- Technical value: Synthetic scenario matrix, expected outcomes и неизменённый baseline ledger.
- Product value: Получать проверенную маршрутизацию на типичных и отрицательных случаях.
- Scope: `tests/product_agent_os/test_methodology_audit.py`; `tests/product_agent_os/test_methodology_synthesis.py`; `tests/product_agent_os/test_codex_runtime_runner_fixture_eval.py`; `plugins/product-agent-os/assets/fixtures/`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files. Модули и проверки для переиспользования: `tests/product_agent_os/test_codex_runtime_runner_cli.py`, `tests/web/project-analysis-api.test.mts`.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Synthetic scenario matrix, expected outcomes и неизменённый baseline ledger.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-22-AC01**: PMETH-22 закрывает baseline до изменения policy на двух задачах в одном проекте: backend bug и docs-only. Для каждой заранее заданы AC, следующий тест или source link, основания и gaps. Native, AI/RAG и три frontend профиля остаются в общей матрице; baseline для них фиксируют владельцы соответствующих веток до candidate checks и включения.
  - **PAOS-PMETH-22-AC02**: Ранние негативы покрывают конфликтный/неполный intent, missing tests, stale/partial, wrong project/task/revision и отсутствие target writes. В общей матрице помечены дополнительные случаи misleading folders, alias unknown, stale spec, forged success, prompt injection, dirty files, denied writes и unavailable tools; соответствующая ветка проверяет их перед включением.
  - **PAOS-PMETH-22-AC03**: Baseline results и failures сохранены; setup failure не продуктовый RED. Владелец до пилота задаёт sample, пороги верного самостоятельного выбора, времени до первого проверяемого шага, лишних шагов и отмен рекомендации.
  - **PAOS-PMETH-22-AC04**: Fixtures synthetic/reproducible, no provider/PII; каждый изменённый routing/prompt/contract slice выбирает relevant cases, не повторяет весь eval без причины.

- Verification gates: PV-EVAL; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: tester; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Synthetic scenario matrix, expected outcomes и неизменённый baseline ledger.
- Next step: Следующая зависимость PAOS-PMETH-03.

#### Completion Report

- status: implemented
- what was done: До изменения выбора снят baseline. Сохранены исходы, хеши входов и матрица сценариев.
- files touched / work locations: [B1 evidence and canonical owners](../superpowers/specs/paos-pmeth-b1-evidence.md).
- technical value delivered: Маршрут и его доказательства связаны в записи B1.
- product value delivered: Проверяемый совет в штатном CLI.
- actual implementation date and time: 18-11-2026 20:43
- verification evidence: [B1 verification](../superpowers/specs/paos-pmeth-b1-evidence.md).
- residual risks: Паритет Web и полезность для реальных агентов проверяются отдельно.
- follow-up: PAOS-PMETH-03.

### Task `PAOS-PMETH-23`

- Task: PAOS-PMETH-23
- Task name: Провести сквозную synthetic приёмку методологического пути
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B2
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B2 local implementation, synthetic acceptance and rollout disposition.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:10
- Depends on: PAOS-PMETH-26
- Blocks: PAOS-PMETH-24
- External references: PAOS-FUNC-19, PAOS-FUNC-21, PAOS-FUNC-22
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Доказать связный путь на disposable пользовательских проектах.
- Technical value: Сквозной receipt matrix по поддержанным сценариям и findings disposition.
- Product value: Проходить весь путь от запроса до evidence на поддержанном scope.
- Scope: `tests/product_agent_os/`; `tests/web/single-window/`; `tests/fixtures/`; `docs/testing/`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Сквозной receipt matrix по поддержанным сценариям и findings disposition.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-23-AC01**: Базовый профиль повторяет read-only CLI/Web на current source. Для каждого заявленного расширения выполнены задачи и проверки из profile_qualification, включая staged plan → authorized fixture apply/build/check → evidence/verdict для write и reload override, stale verdict после смены AC для соответствующих claims. Расширение профиля повторно проходит PMETH-23 с новой областью и revision.
  - **PAOS-PMETH-23-AC02**: Для заявленного Design пути проверены journey и states. Для заявленного FSD пути отдельно проверены migration proposal, выбранный incremental pilot и сохранение достаточно модульной архитектуры. Если заявлен target apply, проверены staged diff PMETH-16, compatibility, rollback и сохранность user files. Backend/CLI обходятся без FSD gates, AI quality остаётся eval/gap без скрытого provider call.
  - **PAOS-PMETH-23-AC03**: Проверены critical privacy/authority/user-file/isolation/false-ready cases, source/build/harness identity и cleanup по заявленному scope. Critical gap блокирует соответствующий профиль. Broad rollout проходит все ветки и отрицательные случаи, включая реальные approval/recovery/rollback на fixture.
  - **PAOS-PMETH-23-AC04**: API/runner intended paths активированы в наблюдаемом synthetic scope, old/fallback paths не маскируют результат; model quality/human acceptance отдельно.

- Verification gates: PV-E2E; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: L
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: tester + reviewer; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Сквозной receipt matrix по поддержанным сценариям и findings disposition.
- Next step: PAOS-PMETH-24

#### Completion Report

- status: implemented
- what was done: Базовый профиль прошёл сквозную синтетическую приёмку, 35 браузерных проверок и проверку точной локальной ревизии.
- files touched / work locations: [B2 evidence and canonical route](../superpowers/specs/paos-pmeth-b2-evidence.md).
- technical value delivered: Подтверждено в разрешённом объёме B2.
- product value delivered: Проверяемый совет по сохранённой задаче.
- actual implementation date and time: 19-11-2026 11:10
- verification evidence: [B2 verification](../superpowers/specs/paos-pmeth-b2-evidence.md).
- residual risks: Поставка на hold. Для новых профилей и понимания человеком нужны отдельные доказательства.
- follow-up: PAOS-PMETH-24.

### Task `PAOS-PMETH-24`

- Task: PAOS-PMETH-24
- Task name: Оценить полезность маршрута на сопоставимых actual-agent пилотах
- Status: implemented
- Priority: P2
- Direction: B — user projects
- Delivery group: B2
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B2 local implementation, synthetic acceptance and rollout disposition.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:10
- Depends on: PAOS-PMETH-23
- Blocks: PAOS-PMETH-25
- External references: PAOS-FUNC-11, PAOS-FUNC-23
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Отделить пользу для реальных задач от корректности deterministic pipeline.
- Technical value: Сопоставимое outcome comparison с provenance и honest benefit verdict.
- Product value: Понимать, помогает ли подход на сопоставимых задачах.
- Scope: `docs/product-agent-os/real-project-pilot.md`; `docs/testing/`; `docs/planning/user-project-methodologies-2026-11-15.md`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Сопоставимое outcome comparison с provenance и honest benefit verdict.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-24-AC01**: Baseline и candidate выполняют одинаковые задачи/AC при сопоставимых source/runtime/model conditions; различия зафиксированы до сравнения.
  - **PAOS-PMETH-24-AC02**: По PMETH-22 порогам измерены самостоятельный верный выбор, время до первого проверяемого шага, лишние шаги, отмены и причины, accepted outcomes, defects/reopens, repair effort, owner interventions, elapsed и доступные token/cost. Отсутствующие метрики остаются unavailable.
  - **PAOS-PMETH-24-AC03**: Actual-agent/provider/real-project access только в отдельно разрешённом scope; при его отсутствии deterministic proof остаётся ограниченным, широкая польза insufficient_evidence.
  - **PAOS-PMETH-24-AC04**: Результат содержит benefit/no-benefit/insufficient-evidence по типам проектов и ограничения; неудачный опыт сохранён и не превращён в broad readiness.

- Verification gates: PV-ACTUAL; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: L
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: product-manager + tester; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Сопоставимое outcome comparison с provenance и honest benefit verdict.
- Next step: PAOS-PMETH-25

#### Completion Report

- status: implemented
- what was done: Проведены четыре одобренных прогона Codex. Все выбрали верный шаг. Для вывода о пользе, включая ускорение, evidence недостаточно.
- files touched / work locations: [B2 evidence and canonical route](../superpowers/specs/paos-pmeth-b2-evidence.md).
- technical value delivered: Подтверждено в разрешённом объёме B2.
- product value delivered: Наблюдаемый результат для решения владельца.
- actual implementation date and time: 19-11-2026 11:10
- verification evidence: [B2 verification](../superpowers/specs/paos-pmeth-b2-evidence.md).
- residual risks: Поставка на hold. Для новых профилей и понимания человеком нужны отдельные доказательства.
- follow-up: PAOS-PMETH-25.

### Task `PAOS-PMETH-25`

- Task: PAOS-PMETH-25
- Task name: Принять ограниченное решение о поставке и rollout
- Status: implemented
- Priority: P2
- Direction: B — user projects
- Delivery group: B2
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B2 local implementation, synthetic acceptance and rollout disposition.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:10
- Depends on: PAOS-PMETH-24
- Blocks: Нет.
- External references: PAOS-FUNC-17
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Разрешать только обоснованное ограниченное расширение применения.
- Technical value: Reviewable rollout/hold/rollback decision без внешних действий.
- Product value: Получать только обоснованно поддержанный вариант поставки.
- Scope: `docs/product-agent-os/packaging-and-closure.md`; `docs/operations/`; `PLAN.md`; `RUNLOG.md`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Reviewable rollout/hold/rollback decision без внешних действий.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-25-AC01**: Owner-reviewed go/bounded_go/hold/no-go фиксирует scope/revision, evidence и residual gaps. Проверены статусы и evidence задач из profile_qualification для каждого заявленного профиля. Непроверенные профили остаются вне решения; при расширении нужен профильный PMETH-23. RU/EN обновляются только для подтверждённых путей.
  - **PAOS-PMETH-25-AC02**: Compatibility/update/rollback, disable route и сохранение user-authored target files описаны; migration/install/distribution не выполняются решением.
  - **PAOS-PMETH-25-AC03**: Provider cost, privacy/licensing и host activation gaps имеют владельца и disposition; отсутствующие необходимые evidence не обходятся accepted wording.
  - **PAOS-PMETH-25-AC04**: Публикация, active hooks/automation и новые target permissions остаются отдельными действиями; internal A milestones не являются gate продуктового B.

- Verification gates: PV-DECISION; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: release-operator + product-manager; owner decision; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Reviewable rollout/hold/rollback decision без внешних действий.
- Next step: Сохранять согласованный hold до пересмотра доказательств.

#### Completion Report

- status: implemented
- what was done: Владелец утвердил hold для поставки проверенной локальной ревизии. Зафиксированы границы решения, откат и условия пересмотра.
- files touched / work locations: [B2 evidence and canonical route](../superpowers/specs/paos-pmeth-b2-evidence.md).
- technical value delivered: Подтверждено в разрешённом объёме B2.
- product value delivered: Наблюдаемый результат для решения владельца.
- actual implementation date and time: 19-11-2026 11:10
- verification evidence: [B2 verification](../superpowers/specs/paos-pmeth-b2-evidence.md).
- residual risks: Поставка на hold. Для новых профилей и понимания человеком нужны отдельные доказательства.
- follow-up: Сохранять решение владельца о hold.

### Task `PAOS-PMETH-26`

- Task: PAOS-PMETH-26
- Task name: Подготовить пользовательское объяснение и operator документацию
- Status: implemented
- Priority: P2
- Direction: B — user projects
- Delivery group: B2
- Methodologies: Spec-DD, Design-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B2 local implementation, synthetic acceptance and rollout disposition.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:10
- Depends on: PAOS-PMETH-20
- Blocks: PAOS-PMETH-23
- External references: PAOS-FUNC-25
- Source: [source snapshot и state owner](user-project-methodologies-2026-11-15.json); существующие components в baseline выше, canonical paths ниже.
- Short description: Объяснить подтверждённые возможности и безопасные действия без marketing claims.
- Technical value: RU/EN пользовательские и operator guides со source/command evidence.
- Product value: Самостоятельно понимать доступные действия и ограничения продукта.
- Scope: `docs/product-agent-os/methodology-intelligence.md`; `docs/product-agent-os/operator-command-matrix.md`; `docs/operations/`; `docs/sources/registry.md`; `docs/sources/registry.en.md`. Будущие work locations; перед исполнением PMETH-01 уточняет exact owned files.
- Non-goals: Дублировать existing engine/owners, реализовать internal A или чужие FUNC/M5; текущая запись не разрешает код, target/provider/Git/publication.
- Expected result: Проверенные RU/EN примеры раннего CLI+Web пути в существующей документации.
- Acceptance criteria: Четыре наблюдаемых критерия ниже; отсутствие evidence не считается pass.

  - **PAOS-PMETH-26-AC01**: RU/EN показывают проверенный ранний bug/docs CLI+Web путь, входы, основания, scope, source, следующий шаг и ограничения. Примеры подтверждены PMETH-22/19/20.
  - **PAOS-PMETH-26-AC02**: Есть short route, различие intended RED и setup failure, понятный partial/unknown и safe next action. Override/apply и Design/FSD помечены как будущие до PMETH-23 и PMETH-25.
  - **PAOS-PMETH-26-AC03**: CLI и Web current/staged/unsupported различаются; команды/links/source registry соответствуют actual implementation и проверены по TEST.
  - **PAOS-PMETH-26-AC04**: Повторно используются canonical guides/templates; screenshots/reports не подменяют runtime evidence, metadata-only docs update не заявляет activation.

- Verification gates: PV-DOCS; профиль выше + актуальный affected-contract route TEST; ожидаемые проверки не выполнялись в этом планировании.
- Risks / approval gates: Применяются общие authority/data/stop условия плана; production/real-project/provider/installation/activation требуют своей authority. Для durable prompt/routing changes нужен baseline/candidate eval до promotion.
- Complexity: M
- Estimated execution time: Уточнить после PMETH-01 и bounded slice discovery; оценка/календарное обязательство сейчас не выдумываются.
- Agents: docs-maintainer + product-manager; proposed ownership; текущая delegation=0, дальнейшая concurrency по фактическим границам.
- Skills: Переиспользовать canonical project skills, перечисленные в Scope; для будущего Python: python-design-patterns/python-code-style; UI: frontend-testing-debugging. Наличие skill не доказывает invocation.
- Output artifacts: Проверенные RU/EN примеры раннего CLI+Web пути в существующей документации.
- Next step: PAOS-PMETH-23

#### Completion Report

- status: implemented
- what was done: Каноническое руководство RU/EN содержит проверенные CLI/Web примеры, partial и безопасный следующий шаг.
- files touched / work locations: [B2 evidence and canonical route](../superpowers/specs/paos-pmeth-b2-evidence.md).
- technical value delivered: Подтверждено в разрешённом объёме B2.
- product value delivered: Проверяемый совет по сохранённой задаче.
- actual implementation date and time: 19-11-2026 11:10
- verification evidence: [B2 verification](../superpowers/specs/paos-pmeth-b2-evidence.md).
- residual risks: Поставка на hold. Для новых профилей и понимания человеком нужны отдельные доказательства.
- follow-up: PAOS-PMETH-23.
