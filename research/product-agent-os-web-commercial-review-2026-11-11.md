# PAOS-0046 — коммерческий review перед M2

Source status: official sources retrieved 2026-11-11 / repository source inspection / project-authored release decisions. Ранний review, без регистрации, provider/API key, реальных credentials и коммерческого выпуска. Даты источников и границы выводов приведены ниже.

## Решение

**Результат раннего review: можно продолжать локальную инженерную разработку M2; коммерческий выпуск PAOS пока заблокирован.** Это решение о порядке разработки, а не юридическое разрешение использовать любую подписку, распространять продукт или обрабатывать клиентские данные.

Текущий `codex_app_agent` сохраняется как owner-default без отдельного API key. Модель работает в активном Codex App worker; PAOS обменивается scoped jobs/results через свой capability channel, а команды выполняет отдельный offline native broker. Успешная техническая M1 не доказывает commercial admission этого точного способа интеграции. Вывод review: `commercial_qualification_unresolved`, а не «разрешён» или «запрещён любой продукт с Codex».

PAOS-0046 закрывается как выполненное исследование, распределение ответственности и фиксация запретов выпуска. AUTH-G1–G6 остаются выпускными gates с приведёнными ниже частичными доказательствами и пробелами. Повторная проверка обязательна в PAOS-0030 перед выпуском и при изменении auth surface, contracts, account class, рынков или состава поставки.

Артефакт внутреннего review размещён в `research/`, а [машинный release-пакет](../docs/release/web-commercial-review.json) — в `docs/release/`. Это evidence задачи, не новая страница публичного MkDocs-сайта.

## Что проверено

- Канонические контракты: `research/product-agent-os-web-auth-commercial-2026-11-09.md`, PRD §17.7, architecture §21.10, карточка PAOS-0046 и source-owned JSON-матрица.
- Реальный текущий путь: `packages/contracts/auth/m1-route.ts`, App gateway/channel/client, offline sandbox broker, launcher/runtime manifest, SQLite Worker и backup implementation. Код не изменялся.
- M1 evidence используется с прежними датами: actual App/native105, task39, data25, headless33, unit306 и native qualification. Это технические receipts предыдущей задачи, не новые прогоны PAOS-0046 и не commercial entitlement.
- Локальные manifests/lock и LICENSE установленных Web dependencies, содержимое текущего Web `dist`, наличие distribution/license/notice артефактов. Не проверялись чужие auth caches, реальные аккаунты, пользовательские БД или персональные данные.
- Два независимых read-only направления: official commercial/auth sources и privacy/licensing/distribution. Финальный review документа и проверки проекта фиксируются в конце страницы.

## Источники и применимость

Все ссылки прочитаны 2026-11-11. Отсутствие даты публикации явно отличается от даты retrieval; права конкретного аккаунта не проверялись.

| ID | Первичный источник | Установленный факт / предел |
| --- | --- | --- |
| C46-S01 | [App Server — Auth endpoints](https://learn.chatgpt.com/docs/app-server#auth-endpoints), publication date не указана | Документ разрешает продолжение local/open-source authentication и прямо исключает commercial/hosted services. Правило расположено перед auth modes. Оно не классифицирует собственный PAOS App-agent bridge, который не вызывает account/login; из этого не следует ни exemption, ни blanket ban именно bridge. |
| C46-S02 | [SIWC — Request a client ID](https://developers.openai.com/siwc/request-client-id), publication date не указана | Commercial доступ предоставляется выбранным партнёрам; waitlist не равен admission, client registration или entitlement PAOS. Формы не отправлялись. |
| C46-S03 | [SIWC — ChatGPT plan usage](https://developers.openai.com/siwc/token-sharing-open-source), publication date не указана | Plan usage — дополнительное разрешение к identity для eligible requests; OSS/local guide не означает допуска paid/remote приложения и не предоставляет ChatGPT conversation context. |
| C46-S04 | [OpenAI Services Agreement](https://openai.com/policies/services-agreement/), updated 2025-12-01, effective 2026-01-01, §§2.2,3.1–3.3 | API Customer Applications — предусмотренный договором класс. Это не blanket approval PAOS/App Server. Sharing/resale account access, передача API keys и обход Usage Limits ограничены; локальное использование собственного ключа не тождественно продаже ключа. |
| C46-S05 | [Terms of Use](https://openai.com/policies/terms-of-use/), published/effective 2026-01-01, Registration/Using/Content | Consumer terms ограничивают доступ других лиц к аккаунту, распространение Services и programmatic extraction. Ownership Output отдельно от способа доступа. Применимость к supported agent-authored tool report, account class и региональному договору PAOS не установлена; нельзя объявлять exemption по отсутствию token copying. |
| C46-S06 | [Service Terms](https://openai.com/policies/service-terms/), updated 2026-11-10, introduction/§§1,2,4 | Имеют приоритет при договорном конфликте; API используется по документации; beta и сторонние лицензии code output учитываются отдельно. Прямого разрешения коммерческого PAOS bridge в прочитанном тексте не найдено. |
| C46-S07 | [Codex pricing](https://learn.chatgpt.com/docs/pricing), publication date не указана | Использование host связано с условиями и allowance его плана/workspace; API billing — отдельный канал. Не устанавливает цену, остаток квоты или доступ конкретного пользователя PAOS. Нет обещания unlimited/free usage. |
| C46-S08 | [Codex 0.167.0 LICENSE](https://github.com/openai/codex/blob/rust-v0.167.0/LICENSE), [NOTICE](https://github.com/openai/codex/blob/rust-v0.167.0/NOTICE) | Apache-2.0 и отдельные attribution exact source tag. Лицензия кода не предоставляет модельный доступ или общее право на бренд; фактическая binary поставка требует своего inventory. |
| C46-S09 | [Node 26.5.0 LICENSE](https://github.com/nodejs/node/blob/v26.5.0/LICENSE) | Содержит условия Node и bundled third-party components. Утверждение «весь Node MIT» неверно; состав распространяемого binary ещё должен быть закреплён. |
| C46-S10 | [OpenAI brand guidelines](https://openai.com/brand/) | Нельзя создавать ложное впечатление sponsorship/endorsement; branding rights не выводятся из лицензии исходного кода. Review не разрешает использовать чужие логотипы как бренд PAOS. |
| C46-S11 | `apps/web/package-lock.json` и установленные `react/LICENSE`, `react-dom/LICENSE`, `scheduler/LICENSE` | Локальное evidence exact versions: React/React DOM19.3.1, Scheduler0.28.0 — MIT и обязательные notices. Lock metadata отдельно различает production и dev dependencies; оно не заменяет shipping SBOM. |

## Варианты использования

| Вариант | Плательщик и фактический механизм | Решение review |
| --- | --- | --- |
| Текущий local engineering App-active | Собственный host account/workspace; App worker reasoning → PAOS claim/report, broker без model turns/auth | Продолжать инженерный M2 в принятом техническом scope. Активный App consumer обязателен. Это не новый commercial grant. |
| Платный local App-agent продукт | Тот же bridge либо другой выбранный supported surface; модель у конечного пользователя | `commercial_qualification_unresolved`; не продавать доступ/подписку и не рекламировать route как commercial-approved до C46-01/02/05–08. |
| Hosted/shared-account App-agent сервис | Remotely доступный PAOS, чужой/shared host account либо новая tenant boundary | Не поддержан M1; блокирован commercial/security/hosting gates. Нельзя превращать личный App account в общий backend. |
| `local_api_byok` compatibility | Собственный API account пользователя; текущая реализация вызывает App Server `account/login/start apiKey` | Отдельный explicit route. Наличие API key не снимает широкого ограничения C46-S01. Нет commercial approval; в этой задаче ключ не запрашивается и маршрут не переключается. |
| Обычный API Customer Application | Самостоятельная интеграция с API в рамках C46-S04, отдельный payer/contract | Возможный класс будущей архитектуры; это не существующая сертифицированная альтернатива PAOS. Потребовал бы отдельного решения и реализации; автоматического fallback нет. |
| SIWC | Собственный approved OAuth client и разрешённые scopes/plan usage | `unavailable_admission_pending`, optional PAOS-0047. Не требуется для локального M2 и не включается без допуска. |
| OSS/source distribution | Требуются собственная лицензия PAOS и выполнение dependencies terms | `license_undecided`; `private:true` и размещение исходников не создают OSS grant. Платный local продукт нельзя объявить eligible только по слову local. |

## AUTH-G1–G6: доказательства и release gates

| Gate | Статус раннего review | Evidence сейчас | Ответственный и условие снятия запрета |
| --- | --- | --- | --- |
| AUTH-G1 | `pending_route_qualification` | Точный App/BYOK/SIWC механизм описан; C46-S01–06 проверены. Entity, paid/OSS, рынки, account class и применимый договор не определены. Bridge applicability остаётся неизвестной. | Product owner + commercial/legal reviewer: закрепить модель поставки, supported integration и применимый договор; при отсутствии ясного официального ответа получить письменное уточнение конкретной схемы. До этого коммерческий auth/продажа не заявляются. |
| AUTH-G2 | `partially_verified` | M1 exact Codex0.167.0/native tuple и actual App roundtrip/recovery сохранены; без inherited-login fallback. Конкретные host model ID/account entitlement не аттестованы; идентичность worker только attested. | Runtime owner + tester: до pilot с реальными клиентами закрепить release tuple/model/account-policy и заново проверить выбранный route. Успешный synthetic turn не закрывает release entitlement. |
| AUTH-G3 | `partially_verified` | M1 Origin/CSRF/capability/profile/generation/replay/redaction и synthetic broker boundaries проверены. Default route не обрабатывает OpenAI credentials. Same-user process attack, все PII/secret patterns, реальное переключение host account не доказаны. OAuth cases пока неприменимы к default, обязательны при включении SIWC. | Security/tester: проверить выбранную release threat model и допустимые данные; до этого нет pilot с secrets/customer data или broad confidentiality claims. |
| AUTH-G4 | `blocked_release` | Локальные зависимости/лицензии и dataflow изучены. Собственная лицензия/правообладатель PAOS не выбраны; shipping manifest/notices/Terms/Privacy/retention ещё не готовы. | Product/privacy owner + Release Operator: закрыть C46-01/05/06 и проверить точный release archive. Нет платной/OSS/hosted поставки на основании текущего build. |
| AUTH-G5 | `partially_verified_host_usage_unknown` | Route payer labels и no-fallback сохранены; offline broker не делает model turns. Host quota/стоимость/entitlement неизвестны; discovery не означает разрешение inference. | Product/tester: перед customer pilot утвердить disclosure payer/data/usage/limits и проверить реальные limit/error paths выбранного account. Никаких auto purchases, писем администраторам или скрытого payer switch. |
| AUTH-G6 | `pending_release_operations` | M1 native Stop, restart, stale approval/capability, reattach/reconcile без replay и отдельное task acceptance подтверждены. Не доказаны remote logout/revocation, upgrade подписанного дистрибутива, support commitments и human acceptance. | Runtime/Release Operator + product owner: C46-08, version/rollback/support пакет и актуальная приёмка в PAOS-0030. Disconnect PAOS не означает отмену host подписки или удаление remote history. |

Ни один полный release gate этим review не объявлен `passed`. `partially_verified` означает известное техническое evidence плюс конкретный недостающий release scope, а не условный допуск.

## Открытые решения и запреты выпуска

| ID | Пробел | Владелец | Точный запрет / повторная проверка |
| --- | --- | --- | --- |
| C46-01 | Entity, target markets/cohort, paid/OSS и local/hosted distribution не выбраны | Product owner | Нет договорных обещаний, customer pilot и distribution до выбора и проверки применимых условий. Язык/часовой пояс не определяют страну владельца или клиентов; PAOS-0030 повторно проверяет рынки и доступность. |
| C46-02 | Commercial applicability конкретного App-agent claim/report surface не установлена | Product owner + commercial/legal reviewer | Нет продажи «доступа к Codex через PAOS». Требуется exact integration qualification с учётом extraction/account-access terms; не выводить разрешение или запрет по аналогии с другим auth flow. |
| C46-03 | BYOK через App Server auth не квалифицирован коммерчески | Architect + Product owner | Не выпускать этот compatibility route как commercial-approved. Либо ясное разрешение для точной схемы, либо отдельный approved architecture change. API key в текущей задаче не нужен. |
| C46-04 | SIWC admission/client registration отсутствуют | Product owner + auth owner | SIWC unavailable; PAOS-0047 и PAOS-0030 проверяют admission/scopes/callbacks. Waitlist — не approval; заявку этот review не отправляет. |
| C46-05 | Собственная лицензия, notices, package composition и updates не определены | Product owner + Release Operator | Нет готового коммерческого/OSS release package. При внешних prerequisites и при bundling разные obligations; exact archive/SBOM/notices проверяются в PAOS-0030. |
| C46-06 | Terms/Privacy, data permissions и retention/delete по всем слоям не определены | Product/privacy owner + security/tester | Не обещать local-only/no-training/hard-delete и не допускать реальные customer secrets. До pilot согласовать и проверить DB/audit/WAL/blobs/backups/exports/App/provider handling. |
| C46-07 | Host account class, limits, tariff и customer consent/disclosure неизвестны | Product owner + tester | Не обещать free/unlimited, нулевые расходы или оплату обычного API из ChatGPT plan. Release проверяет выбранный payer и отсутствие скрытых затрат. |
| C46-08 | Support, release upgrade/rollback, incident ownership и human acceptance | Runtime owner + Release Operator + Product owner | Нет GA/SLA/production-ready claim. Проверить реальные supported versions, release rollback и ответственность за host failures перед PAOS-0030. |

Это backlog выпускных решений, а не новые незакрытые задачи технической M1. Он не блокирует локальную инженерную разработку M2 с разрешёнными проверками, пока M2 не включает real-customer pilot, новый auth route, shared account, hosting или distribution. Такое расширение scope требует отдельного решения до соответствующей реализации.

## Dataflow и retention

Browser/local service/SQLite и pairing остаются локальными. App worker получает input и task context, включая filenames, title, criteria, risks и сведения о workspace; дальнейшая передача модели зависит от host/account. Поэтому утверждение «данные никогда не покидают компьютер» не подтверждено. Provider/account training, residency и remote retention не наследуются из loopback topology и offline broker.

Commands stdout/stderr и наблюдаемые diffs сохраняются в run data. Known-secret redaction, исключение credential files и bounded snapshots уменьшают определённые риски, но не являются DLP или гарантией отсутствия всех PII. Пользователь должен иметь права на передаваемые Input; ownership Output отдельно от прав стороннего code/output и способа доступа [C46-S04–06].

Удаление entity устанавливает tombstone и не доказывает физическое стирание DB/audit. SQLite backup сохраняет содержимое БД; история может оставаться в snapshots/exports и у App/provider. Managed backup rotation до пяти копий не задаёт retention TTL всем данным. Публичное скрытие текста удалённого комментария подтверждено M1, но не означает уничтожения всех private originals и backups. Реальные user DB/credentials при review не читались.

## Состав поставки и лицензии

В просмотренной поставке `apps/web/dist` находятся HTML/CSS/JS; отдельные LICENSE/NOTICE не обнаружены. Проверка JS на стандартные MIT/copyright/React notice markers дала отрицательные результаты. Это отсутствие доказанной доставки notices в текущем артефакте, не утверждение о совершённом нарушении уже опубликованным продуктом. MIT notices production React/React DOM/Scheduler должны входить в точный распространяемый пакет.

В production dependency graph Web — React, React DOM и Scheduler с указанными выше версиями. Dev graph также включает Apache-2.0 (TypeScript7.0.2/detect-libc), MPL-2.0 (Lightning CSS1.33.0/platform packages), ISC (picocolors) и BSD-3-Clause (source-map-js). Нельзя считать все зависимости MIT или автоматически переносить dev-tool license на emitted CSS без анализа скопированного кода. Source/toolchain distribution проверяется отдельно.

Корневой LICENSE/выбор условий PAOS в просмотренных manifests не обнаружен; `private:true` не является лицензией. Текущий launcher выбирает внешний Codex `binaryPath` и текущий Node `process.execPath`, сверяет fingerprints. Упаковка этих binaries в PAOS не установлена; installer/distribution manifest ещё не задан. При будущем bundling понадобятся exact binary provenance и весь набор notices Codex/Node/dependencies [C46-S08–09]. Старый G7/tooling SBOM не является Web shipping SBOM.

## Контроль ошибочных выводов

1. Успешный M1 turn при pending C46-02 не разрешает коммерческий запуск.
2. Отсутствие переноса credentials не устанавливает exemption из Service/Use terms.
3. API Customer Application rights не разрешают автоматически App Server auth или перепродажу App account.
4. Закрытие PAOS-0046 не переключает `commercial_review_required` в runtime и не активирует SIWC.
5. Apache-2.0/MIT code license не предоставляет модельный entitlement, право на бренд или поддержку.
6. Удаление из UI и очистка публичного audit не означают hard delete snapshots/remote history.
7. Разрешение инженерного M2 не превращается в разрешение выпуска или в изменение системных политик.

## Передача M2

После проверенного закрытия PAOS-0046 владелец разрешил отправить команду в существующий чат PAOS-M2. Целевой thread: `01a1cb91-c2df-7d13-97fe-64e981d02d42`; в нём уже указана первая очередь: **PAOS-0031 → 0032 → 0033 → 0005 → 0006 → 0007 → 0008 → 0034 → 0038 → 0035**. Выполнение по зависимостям и локальным acceptance, без расширения до остальных M2/M3 задач этим сообщением.

Передаваемые условия: no API key, no system-policy changes, no manual tests; основной `codex_app_agent` и запрет fallback сохраняются; external commercial gates C46-01–08 не повышаются. Агент M2 перечитывает актуальные AGENTS/PRD/plan и координирует shared control-plane ownership. Реализация M2 начинается в том чате после команды; текущая PAOS-0046 сама код M2 не меняет.

## Проверка и закрытие review

<!-- PAOS-0046 verification:start -->
**PAOS-0046 implemented / closure_level = docs_static_verified_early_commercial_review.** Independent reviewer `/root/commercial_sources`, context_mode=separate_reused_context, tester_verdict=closed_allowed для раннего review с незакрытыми release gates. Второй независимый privacy/license audit включён в gap register; новых источников runtime entitlement он не создаёт.

Наблюдаемые проверки текущей задачи:

- `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q`: **105/105**,8.865s,exit0.
- `python -B tools/check_docs.py`: exit0; detailed task matrix validator: errors=[],exit0; `git diff --check`: exit0, только line-ending normalization warnings.
- `node --test tests/web/auth-route.test.mts`: **2/2**,117.8079ms,exit0; четыре дополнительных pure contract assertions App/BYOK × commercial_local/hosted сохраняют blocked/commercial_review_required, без provider/API key.
- Bounded artifact validation:6 уникальных AUTH gates,8 release gaps,11 source groups;55 прочих JSON task objects и Markdown task blocks, все estimates сохранены. Runtime, tests, policies и navigation не менялись.

Первый docs run105/6.836s имел13 failures: ошибочно созданная публичная Markdown-страница добавила страницу в фиксированный RU/EN/site inventory. Отчёт перенесён без потери содержания в research, release-пакет сохранён как JSON; тесты, counts, guards и исторический site не менялись. Первый собственный control-plane CAS штатно restored по after-images; окончательный reviewed CAS digest `0a73c07e47c0ff3abf7dbbda1927ff45178838d45f4cbdd9bf7823ebaa7155f6` применён к REQUIREMENTS/PLAN/TEST/RUNLOG. Journal и before-images сохранены. Новая публикация/страница сайта не создавалась; strict MkDocs not_applicable без nav/config/diagram/site изменения или freshness claim.

AGENTS/EVALS/prod_test: no_change_needed — durable authority, rubric/thresholds и Batch39 не менялись. Обязательных gaps для самого раннего review нет; commercial release по AUTH/C46 всё ещё blocked. Передача M2 разрешена владельцем после closure; receipt доставки относится к текущему чату и его lifecycle-marker, а не к разрешению выпуска.
<!-- PAOS-0046 verification:end -->

Связанные артефакты: [auth/commercial contract](product-agent-os-web-auth-commercial-2026-11-09.md), [план и карточка PAOS-0046](product-agent-os-web-task-manager-plan-2026-11-09.md), [M1 evidence](product-agent-os-web-m1-execution-2026-11-11.md).
