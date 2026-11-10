# Product-Agent OS Web — авторизация и коммерческое использование

Source status: official documentation checked 2026-11-09 / project-authored design. Версия: 0.7; auth mechanism: §7. Документация, не реализация и не разрешение на коммерческий запуск.

Owning requirement: [PRD §15](product-agent-os-web-prd-2026-11-05.md#15-единое-окно-и-codex-app-server--v04); architecture contracts: [архитектура §19](product-agent-os-web-architecture-2026-11-05.md#19-единое-окно-runtime-и-авторизация--v04); tasks: [G11](product-agent-os-web-task-manager-plan-2026-11-09.md). Источники WEB-AUTH-01–09 перечислены ниже и в RU/EN registry.

## 1. Решение и граница уверенности

Выбранный пользователем runtime — Codex App Server внутри собственного клиента Product-Agent OS. Codex App не обязателен. Для планирования первого коммерческого local-first варианта базовый кандидат — API-доступ пользователя (BYOK) из его локального окружения; Product-Agent OS не получает ключ на свои серверы и не продаёт доступ к чужой подписке. Это архитектурный выбор, а не подтверждение допуска конкретного продукта или аккаунта. Перед платным выпуском обязательна проверка условий выбранного канала AUTH-G1–G6.

Sign in with ChatGPT (SIWC) — отдельный дополнительный путь. Для платного или remotely hosted приложения он не считается доступным по умолчанию: требуется соответствующий допуск OpenAI. Если допуска нет, этот пункт остаётся недоступным с объяснением; API-путь не переключается на него автоматически. Внутренний личный prototype не служит доказательством права на коммерческое распространение.

## 2. Что подтверждено источниками

| ID | Источник, прочитан 2026-11-09 | Подтверждённый факт и предел |
| --- | --- | --- |
| WEB-AUTH-01 | [App Server: auth](https://learn.chatgpt.com/docs/app-server#auth-endpoints) | Документированы API key, managed ChatGPT и experimental external tokens. Страница прямо ограничивает App Server authentication для commercial/hosted services; прежний локальный/OSS случай нельзя автоматически переносить на платный продукт. Наличие метода не означает допустимость любого способа применения. |
| WEB-AUTH-02 | [SIWC: client ID](https://developers.openai.com/siwc/request-client-id) | Commercial SIWC предоставляется выбранным партнёрам; есть waitlist. Подтверждения допуска Product-Agent OS нет. |
| WEB-AUTH-03 | [ChatGPT plan usage](https://developers.openai.com/siwc/token-sharing-open-source) | Использование плана — дополнительная capability к identity. Документы адресованы OSS/local apps; paid/remote apps направляются в interest form. Не даёт доступ к ChatGPT conversations/account context. |
| WEB-AUTH-04 | [SIWC с App Server](https://developers.openai.com/siwc/token-sharing-open-source/codex-app-server) | Документирован Responses provider с OAuth access token в окружении child process; refresh принадлежит клиенту, после замены token требуется restart и thread/resume. model/list не доказывает entitlement. |
| WEB-AUTH-05 | [Preview limitations](https://developers.openai.com/siwc/token-sharing-open-source/preview-limitations) | Ограничения относятся именно к SIWC plan usage. Local thread resume сохраняется; hosted tools и некоторые виды input/API недоступны. Не переносить ограничения механически на обычный API-канал. |
| WEB-AUTH-06 | [Website identity flow](https://developers.openai.com/siwc/website) | Authorization Code + PKCE/OIDC, backend validation и собственная app session. Identity scopes отдельно от plan usage. Конкретная регистрация desktop/local клиента требует проверки, website recipe не равен готовому desktop контракту. |
| WEB-AUTH-07 | [OpenAI Services Agreement](https://openai.com/policies/services-agreement/) | §2.2 предусматривает интеграцию API в Customer Applications для End Users; §3.3 запрещает передачу/продажу ключей и обход ограничений. Это основание рассматривать обычный API-путь, не blanket approval нашей реализации. |
| WEB-AUTH-08 | [ChatGPT/API billing](https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform) | Учёт расходов API и ChatGPT разделён. Подписка не является общим API-балансом; специальные eligible benefits не отменяют разделения. |
| WEB-AUTH-09 | [Codex LICENSE](https://github.com/openai/codex/blob/main/LICENSE) | Репозиторий Codex публикует Apache-2.0. При упаковке проверяются LICENSE/NOTICE и зависимости точного распространяемого build; лицензия кода не предоставляет модельный доступ или права на бренд. |

Материальная неоднозначность: формулировка ограничения WEB-AUTH-01 широкая и расположена перед списком auth modes. Поэтому её нельзя объявить юридически разрешённой для нашего BYOK-варианта только по наличию apiKey RPC. Проектное решение — обычный API-provider с локально принадлежащим пользователю credential, отдельный от наследования ChatGPT/Codex login; соответствие точного коммерческого deployment подтверждается AUTH-G1, при неоднозначности — уточнением у OpenAI до продажи. Нельзя обещать, что "любой local app разрешён", если он платный.

## 3. Матрица вариантов

| Вариант | Кто оплачивает inference | Хранение / граница | Решение PAOS |
| --- | --- | --- | --- |
| Local API BYOK | Пользователь/его API organization | Credential остаётся у пользователя; local credential broker → runtime → OpenAI API | Базовый кандидат M1; коммерческий gate отдельно; никакой пересылки ключа разработчику PAOS |
| SIWC с plan usage | Условия eligible плана/разрешения OpenAI | Собственный OAuth client/consent; защищённый local store; токен только нужному child process | Опциональный путь после admission и технической проверки; не launch dependency API-варианта |
| Managed ChatGPT login, унаследованный из Codex App | Подписка пользователя | Чужой auth cache и отдельный lifecycle | Не использовать как коммерческий default или скрытый fallback; не читать cookies/auth-файлы другого приложения |
| API за счёт PAOS через backend | Product-Agent OS, далее собственная коммерческая модель | Ключ сервиса только на сервере; tenants, billing, abuse control, privacy | Отложено; нельзя встроить общий secret в distributed launcher или browser |
| Локальный/OSS исследовательский вариант | Зависит от выбранного auth route | Условия конкретного local/OSS flow | Отдельная квалификация; успех prototype не разрешает paid/hosted rollout |

Платный local продукт и hosted SaaS — разные способы размещения, но оба требуют проверки коммерческих условий. BYOK не снимает обязанности по политике данных, лицензиям и защите local API. Выбор юридического лица, стран распространения и paid/OSS лицензирования PAOS остаётся за владельцем; эти сведения пока отсутствуют.

## 4. Четыре независимых разрешения

1. **Local UI session:** доступ браузера к локальному сервису PAOS. Не требует обязательного облачного аккаунта PAOS в M1.
2. **Provider connection:** право выбранного аккаунта и приложения отправлять inference requests и оплачивать их.
3. **Workspace authority:** какие каталоги, команды, network/actions и budgets разрешены конкретному run.
4. **Product entitlement:** право использовать платную редакцию PAOS, если владелец введёт такую модель. Не заменяет provider entitlement; billing/licensing backend вне M1.

Login success не разрешает запись в проект, task acceptance не разрешает deployment, OAuth identity не разрешает расходование ChatGPT plan. UI показывает эти состояния отдельно.

## 5. Пользовательский flow

Первый запуск: локальная session → выбор API connection или доступного SIWC → объяснение плательщика/передаваемых данных → подтверждение connection → выбор проекта → read-only discovery → обсуждение/план/выполнение. Просмотр локальных задач и документов доступен без provider. Открытие папки не выполняет inference.

Connection states: disconnected, authorizing, connected_unverified, ready, expired, revoked, quota_exceeded, unsupported, error. Успешный login даёт connected_unverified. Только отдельно разрешённый минимальный inference через выбранный канал и модель даёт receipt access_verified_at с scope этого запроса; это не бессрочная гарантия доступа ко всем моделям. Во время нынешней документационной задачи такой запрос не выполняется.

Settings показывает account/workspace label (минимум PII), тип connection, выбранную модель, payer, доступные capabilities, последнюю проверку и действия Reconnect/Disconnect. Неизвестный лимит или стоимость — unknown, не 0. Стоимость PAOS и расходы inference показываются отдельно. Смена account/channel требует явного выбора; не использовать личный account при недоступности корпоративного.

При исчерпании квоты новые dispatch останавливаются; уже выполняемая операция reconciled по реальному outcome. Нет автоматической покупки credits, писем администратору, смены ключа или перехода на платный fallback.

## 6. Предлагаемый credential contract

- Credential broker — local-service компонент, не UI, не агент и не task document. Windows native credential storage предпочтителен; конкретный механизм и Codex persistence проверяются на pinned build. Нельзя обещать keychain-only, если runtime создаёт plaintext-копию.
- В SQLite сохраняются connection ID, account binding, auth mode, expiry metadata и ссылка на secure storage. Ключи/refresh/access tokens не попадают в MD/JSON, transcripts, SSE, analytics, crash dumps, browser localStorage, URL или command arguments. Секретное поле ввода не сохраняется в frontend state дольше отправки; чтение сохранённого секрета через Web API отсутствует.
- Isolated PAOS runtime profile не наследует silently global login/config. Итоговые sandbox/approvals и project instructions проверяются явно; изоляция config не отменяет обязательную policy окружения. Проект не может подменить credential source или provider endpoint.
- Передача runtime — только проверенным механизмом pinned build. Env-based injection допускается лишь после проверки, что shell/child tools не получают credential из окружения. Если runtime не даёт такой гарантии, маршрут не проходит security gate; redaction одного лога недостаточна.
- Для разрешённого SIWC клиента нужны PKCE S256, fresh state/nonce, одноразовая expiring transaction, точный callback, проверка signature/issuer/audience/expiry/nonce и granted scopes. Данные identity минимальны; email match не используется как доказательство владения аккаунтом. Confidential client secret нельзя поставлять в desktop package.
- Token refresh сериализован на connection. Для документированного env_key SIWC пути: stop new dispatch → bounded завершение/interrupt активного turn → refresh → restart process → initialize → thread/resume → reconciliation. Не повторять side effects автоматически. Это отдельный путь, не подмена экспериментального chatgptAuthTokens API.
- Disconnect отзывает локальную возможность запуска, останавливает связанные процессы по явной политике и удаляет локальные secrets. Remote token revocation выполняется только поддерживаемым механизмом; отсутствие такого подтверждения показано. Logout не означает удаления истории задач/сессий; retention/delete — отдельное действие.

## 7. Ограничения SIWC preview и UX

Применяются только к каналу WEB-AUTH-05, сверяются перед implementation и каждым выпуском:

- Inference streaming, без server-side response storage; долговременная история принадлежит локальному runtime. Не обещать импорт ChatGPT conversations.
- Hosted image generation, file search, Code Interpreter, native computer use, hosted MCP/connectors и Responses tool_search не входят в этот flow. Local shell/MCP и child agents — другая категория; их capabilities надо проверить.
- Audio/video и Files upload API не поддержаны этим flow. Text/images/files зависят от модели и RPC input; task attachment не означает, что его можно отправить модели. UI объясняет unsupported type и предлагает локальный просмотр.
- Выбор модели из каталога не подтверждает доступ. Disabled action содержит причину; переключение auth route не делает неиспытанный tool поддержанным.

Capability matrix хранит runtime build, connection route, account/workspace policy, model и observed checks. Не обещать паритет с Codex App по plugins/connectors/computer use только из-за общего движка.

## 8. Commercial launch gates

| Gate | Обязательное evidence | Владелец / стоп |
| --- | --- | --- |
| AUTH-G1 | Определены paid/OSS, local/remote, плательщик, entity и целевые рынки; проверены актуальные условия exact API/auth route. Для SIWC — реальный admission/client registration, не waitlist | Product owner; до решения нельзя обещать коммерческий auth |
| AUTH-G2 | Pinned Codex build/protocol, модель и account entitlement; реальный turn через выбранный путь и доказательство отсутствия inherited-login fallback | Runtime owner; без live proof статус not_verified |
| AUTH-G3 | Secret-store и process/environment leakage checks; OAuth negative cases; cross-project/account, origin/CSRF/replay tests | Security/tester; отсутствие evidence блокирует pilot с secrets |
| AUTH-G4 | Notices/лицензии выбранного дистрибутива и dependencies; Terms/Privacy, disclosure передаваемых project данных, retention/delete | Release/product owner; legal review по выбранной модели, не по догадке |
| AUTH-G5 | Понятный payer/usage, limit/errors и consent; нет расхода при discovery, скрытых purchases или переключения канала | Product/tester; pricing не фиксируется без актуальных данных |
| AUTH-G6 | Disconnect/revocation/expired token, crash/restart/resume, upgrade/rollback и поддержка; acceptance пользователя | Runtime/release owner; успешный login не закрывает весь gate |

Статусы всех AUTH-G1–G6 сейчас pending. Право коммерческого использования не заявляется как установленное; прямой запрос пользователем этого документа не авторизует регистрацию приложения, отправку interest form, покупки или provider calls.

## 9. Связь с планом и открытые вопросы

PAOS-0039 фиксирует допустимые routes, admission и ownership; PAOS-0041 — local API credential connection; PAOS-0042–0045 — runtime, UX, recovery и M1 evidence; PAOS-0046 — ранний коммерческий review сразу после M1 (до M2), с повторной актуализацией применимых gates в PAOS-0030 перед выпуском; PAOS-0047 — SIWC только при подтверждённой eligibility. Запуск API-M1 не зависит от завершения опциональной PAOS-0047.

Открыто: paid local или OSS-first distribution; entity/рынки; точный runtime build и безопасный credential transport; SIWC admission; retention defaults; модель/бюджет пилота. Решение владельца по интерфейсу принято; эти вопросы не подменяются предположением о коммерческом допуске.

## 7. Конкретный local M1 auth contract — v0.7

Source status: project-authored design, 2026-11-10; qualification pending. Этот раздел закрывает выбор механизма, не подтверждает его реализацию и не отменяет AUTH-G1–G6.

Первый запуск: launcher связывается только с 127.0.0.1 на выбранном порту, показывает в собственном локальном окне одноразовый pairing code (128 случайных бит, TTL 60 s, максимум 5 попыток). Пользователь вводит code в PAOS; POST /bootstrap/exchange принимает только exact Host/Origin и application/json. Ни URL/query/fragment, ни localStorage, telemetry или логи не содержат code/token. Launcher выводит только UI, не stdout. Истёкший code перевыпускается локально. Это startup pairing, Codex App/второй рабочий интерфейс не нужен.

После exchange: random server-side session, HttpOnly; SameSite=Strict; Path=/; host-only cookie, без Domain. Loopback HTTP в M1: Secure flag не заявляется, HTTPS/LAN/remote не поддерживаются; CSRF header привязан к session, exact Host/Origin проверяются на всех mutating routes, CORS default deny, WS upgrade отсутствует. Session idle timeout 30 min, absolute 8 h; restart/logout/re-pair revoke. Отдельные UA/port instances не должны разделять cookie namespace; cookie name содержит instance ID, server проверяет принадлежность session. Не считать cookie port-isolated: local processes с правами пользователя остаются вне threat model. Pairing/rate-limit/DNS-rebinding/cross-origin checks — 0041/0054.

BYOK: пользователь вводит ключ в connection form после pairing, только memory field → local POST → Windows Credential Manager credential текущего OS user, namespaced PAOS/profile/connection. UI немедленно очищает поле; SQL хранит opaque ref, display fingerprint нельзя выводить из полного ключа в логах. Никаких env/CLI args/browser storage/exports. Service получает ключ из secure store и передаёт в account/login/start apiKey через закрытый stdio child. Отдельный PAOS-owned runtime profile; cli_auth_credentials_store=ephemeral, запрет наследования чужого auth.json/ChatGPT login. Runtime получает секрет для inference, но не передаёт его shell tools. Если exact build не обеспечивает ephemeral auth либо managed policy конфликтует, Send blocked; fallback в file/auto/env запрещён. Глобальный Codex config не изменяется.

Проверки 0054/0041: disposable canary credential без inference, проверка redacted logs/files/tool environment, profile isolation, logout/restart, managed-policy denial; затем только отдельно разрешённая 0045 реальная проверка provider. OS same-user arbitrary process isolation не обещается. Отсутствие secure store оставляет local CRUD, подключение недоступно.

M1 — локальный engineering preview через свой API account. Для платного продукта BYOK остаётся candidate: широкое ограничение App Server auth не трактуется как автоматически снятое API-ключом. AUTH-G1–G6 проверяются до M4 commercial distribution; если admission/условия несовместимы, запуск продажи блокируется, требуется новый runtime ADR. SIWC — optional 0047, не fallback. Наличие schema/login не подтверждает право коммерческого использования.

Источники: [App Server auth](https://learn.chatgpt.com/docs/app-server#auth-endpoints), [Codex credential store](https://learn.chatgpt.com/docs/config-file/config-reference) перепроверены 2026-11-10. Cookie/pairing/TTL — проектные решения.
