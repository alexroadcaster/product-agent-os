# ADR — граница Dashboard и Tasks

Source status: repository_source / bounded_internal_architecture_decision; 18.11.2026.

## Решение

Владелец: frontend Product-Agent OS. Для [пилота Dashboard](../../planning/methodology-improvement-2026-11-15.md#a1-results) усиливаем границы в существующей структуре. Dashboard играет роль страницы, App владеет навигацией и композицией, Tasks владеет семантикой статусов и блокировок. Local service сохраняет право записи и владение снимками. Действующие входы App — `Dashboard.tsx` и `TaskManager.tsx`.

Dashboard и `TeamManager.tsx` используют `features/tasks/read.ts`. Вход явно экспортирует `semanticStatus`, `isBlocked`, `statusText`, `errorText`, `durationText`, `label` и тип `Locale`. Единственные реализации остаются в `model.ts` и `labels.ts` внутри Tasks. Граница отделяет чтение от редактора, команд и композиции экранов. [Верификация A2](../../planning/methodology-improvement-2026-11-15.md#a2-results) · [Верификация METH-11](../../planning/methodology-improvement-2026-11-15.md#a4-results)

Tasks, Artifacts и Sessions используют `ui/MarkdownBody.tsx`. Парсер и проверка URL находятся в том же слое. Граница сохраняет допустимый Markdown, разрешённые HTTP(S)-ссылки без встроенных учётных данных и вывод неподдерживаемой разметки текстом. [Верификация METH-10](../../planning/methodology-improvement-2026-11-15.md#meth-10-results)

Graph, Workflows и Database передают подготовленный текст в `ui/MermaidView.tsx`. Graph и Database передают узлы и связи в `ui/NetworkView.tsx`. Правило Graph → Mermaid принадлежит `features/graph/diagram-source.ts`. Workflows и Database сохраняют свои преобразования.

`features/usage/RunUsage.tsx` владеет чтением измерений, периодом UTC и отображением покрытия. Tasks передаёт `taskId`, Sessions — `sessionId`, обзор проекта — `projectId`, представление агента — `agentId` в рамках проекта. У панели есть собственное состояние и чтение `M1Api.teamMetrics`, поэтому она имеет отдельный feature-вход. App и страницы сохраняют навигацию. Сервис сохраняет контракт и хранение. [Проверки METH-13](../../planning/methodology-improvement-2026-11-15.md#meth-13-results)

## Альтернативы

Сохранить только текущие папки и проверки — дешевле, но новые импорты соседних внутренних модулей останутся незаметными. Ограниченный переход на pages-first FSD дал бы явное физическое разделение, однако один проверяемый шов пока не оправдывает перемещение экранов и обновление всех потребителей. Проверки границы в текущих модулях дают обратимый пилот. Решение о `pages`, `widgets`, `entities` и `shared` принимается по результатам A2 и подтверждённой потребности.

## Проверяемые правила

- Модули одного участка могут ссылаться друг на друга. App использует действующие входы экранов. Другие потребители обращаются к явно утверждённым публичным входам.
- Dashboard и Tasks используют API, локализацию, общие контракты и UI-примитивы `Icon`, `CapabilityNotice`, `Modal` и `ProjectFreshness`. Правило разрешает `tasks/read.ts` для Dashboard и ровно одного файла Team — `TeamManager.tsx`. Тест границ проверяет доступ других потребителей, прямые импорты внутренних модулей Tasks и импорты App или соседних экранов.
- Цикл с участием Dashboard или Tasks блокирует проверку, включая путь через промежуточные frontend-модули. Действующие запреты contracts → apps и local service → frontend продолжают проверяться.
- Тест отклоняет прямые импорты feature-модулей и App из файлов общего Markdown, парсера, валидатора URL, Mermaid и D3. Tasks может импортировать именованные входы `MarkdownBody` и `safeExternalUrl`.
- `RunUsage.tsx` — именованный вход Usage. Тест разрешает его Tasks и Dashboard и отклоняет импорты App или feature-модулей из Usage.
- Исходные исключения зафиксированы на ревизии `bd7d9135f994201170277171eb54e4040cef4fa8`. A2 сняла три связи Dashboard → Tasks, METH-11 две TeamManager → Tasks, METH-10 две Artifacts/Sessions → Tasks, METH-13 две Tasks/Sessions → Dashboard. В `tests/web/fixtures/dashboard-import-baseline.json` осталось 10 исходных исключений, включая девять на `hold` из группы METH-11. Тест требует удалять запись вместе со связью.
- `node --test tests/web/contracts-boundaries.test.mts` разбирает TS, TSX и MTS. Буквальные импорты разрешаются по исходникам и поддерживаемым `baseUrl`/`paths` из Web tsconfig. Неизвестный alias или вычисляемая цель выдаёт отдельную диагностику. Проверка распространяется на указанную frontend-границу, а общие контракты и backend имеют свои правила.

## Откат и критерий достаточности

Для отката METH-13 возвращаем панель и прежний вход `UsageDashboard` в Dashboard, исходные импорты потребителей, обработчики фокуса Tasks и прежнее форматирование ошибок. Восстанавливаем два исключения и правило проверки. Повторяем сценарии Tasks, Sessions и обзора проекта.

Для отката METH-10 возвращаем Markdown-рендерер, парсер и валидатор ссылок в Tasks, восстанавливаем импорты трёх потребителей и два исключения. Возвращаем Mermaid и D3 в `GraphViews.tsx`, исходные импорты и передачу узлов Graph. Восстанавливаем прежнее правило теста и повторяем сборку и целевые браузерные маршруты.

Для отката METH-11 возвращаем два прямых импорта Team, четыре исходных runtime-экспорта `tasks/read.ts`, прежнее правило теста для Dashboard и два исключения Team. При отдельном откате A2 сначала учитываем зависимость Team от общего входа. После отката METH-11 возвращаем три импорта Dashboard, удаляем `tasks/read.ts` и восстанавливаем три соответствующих исключения и A1-правило. Синхронизируем статусы, тест и отчёт соответствующего среза, затем повторяем проверку границ, сборку и браузерный сценарий. Переноса данных нет.

## Решение по расширению {#a2-rollout}

`METH-18` подтверждает пилот для Dashboard. Сравнение показало переход с двух внутренних путей Tasks на один публичный вход, исчезновение трёх прямых нарушений и сохранение всех 50 общих браузерных проверок. Для выбора расширения оцениваем тот же тип связанности в конкретном потребителе.

| Задача | Решение и основание |
| --- | --- |
| METH-10 | `bounded_go` для Markdown, Mermaid и D3. Владелец — frontend shared UI. Markdown используют Tasks, Artifacts и Sessions. Mermaid используют Graph, Workflows и Database, сетевое представление D3 — Graph и Database. Цель — убрать два импорта внутренних модулей Tasks и три импорта представлений Graph из Workflows/Database, сохранить рендер и разделить вывод и подготовку данных. |
| METH-11 | `bounded_go` для одного потребителя, `TeamManager.tsx`. Владельцы — frontend Tasks и Team. Вход Tasks может явно предоставить уже используемые `durationText`, `label`, `errorText` и тип `Locale`. Измеримый результат — два deep imports Team → Tasks исчезают, новые нарушения не появляются, существенные сценарии Team и Dashboard проходят. Откат возвращает два импорта, исключения Team и прежний список экспортов. |
| METH-13 | `bounded_go` для Tasks. Владелец панели измерений — frontend Usage. Tasks владеет входом из карточки и возвратом. Исходная проверка подтвердила фильтр задачи, сохранение карточки, вкладки и черновиков, а также выявила потерю фокуса при обоих переходах. Цель — восстановить фокус и убрать два импорта Tasks/Sessions из Dashboard. Workflows сохраняет `hold` до выбора своего среза с проверками черновиков, CAS, фокуса и очереди. |
| METH-14 | `hold`. `AgentDashboard` вызывается только из Team, но использует проекции назначений и представления метрик Dashboard. `SkillGenerator` уже имеет свой вход. Для выбора Team нужен самостоятельный шов для метрик с проверками команды и профиля, для Skills — подтверждённая проблема текущего входа. |
| METH-15 | `hold`. METH-13 переводит Sessions на общий вход Usage с сохранением `sessionId`. Для дальнейшего переноса Sessions, Artifacts, Graph или App нужен отдельный сценарий с измеримой пользой и проверкой маршрутизации и владения состоянием. |

Выбранные срезы METH-10, METH-11 и METH-13 выполнены. Для METH-10 проверены потребители и браузерные сценарии каждого рендерера. Продуктовое направление B имеет отдельный план. [Результаты A4](../../planning/methodology-improvement-2026-11-15.md#a4-results)

Правила импортов и публичных API сверены через Context7. [FSD layers](https://feature-sliced.design/docs/reference/layers) · [FSD public API](https://feature-sliced.design/docs/reference/public-api)

Mermaid сохраняет локальный ассет, ленивую загрузку, строгий режим и тему. Конфигурация сверена через Context7. [Mermaid securityLevel](https://mermaid.js.org/config/schema-docs/config-properties-securitylevel.html)
