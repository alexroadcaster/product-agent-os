# Пользовательские сценарии

Source status: `repository_source / journey_map / static_review`, 15.11.2026.

**Владелец:** product и владельцы Web/desktop. **Scope/version:** локальные сценарии и будущие дополнения, DG02/2026-11-15. Обновлять при изменении выбора проекта, task/workflow, решения, evidence или видимого состояния ошибки. Проверять контракты и owning tasks, а не только подписи UI.

Эти последовательности описывают намерение и соответствующие source contracts. Они не являются свидетельством, что весь путь проверен на текущем устройстве. Исторические сценарии и ограничения сохранены в [PRD](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-prd-2026-11-05.md), позднейшие статусы — в [Web-плане](../planning/product-agent-os-web-task-manager-plan-2026-11-09.md) и [функциональном backlog](../planning/functional-remediation-2026-11-15.md).

## 1. Добавить проект и понять покрытие

1. Пользователь выбирает локальную папку и подтверждает добавление. Отмена выбора не должна регистрировать проект; root binding и identity проверяет local service.
2. Запрошенный scan в текущем коде выполняет inventory фиксированных control-plane sources и перестраивает ограниченный code index. После сохранённой регистрации сбой scan возвращается как partial с причиной, а не отменяет успешное добавление. Отдельные файлы могут быть недоступны или исключены.
3. Пользователь читает доступные источники и coverage, не принимая их список за полную файловую директорию. Дерево файлов, управляемый background scan и общий inventory/discovery — будущие [F26–F29](../planning/functional-remediation-2026-11-15.md). Они не считаются реализованными из-за существующего индекса.

Источники: [registration](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts), [fixed sources](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/adapters/project-sources.ts), [bounded scanner](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/code-index/sources.mts). Related tests: [project sources](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/project-sources.test.mts), [code index](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/code-index.test.mts).

## 2. Подготовить и выполнить задачу

Пользователь создаёт или открывает задачу, уточняет ценность, scope, критерии, риски и зависимости, затем выбирает применимый workflow и runtime. Контракты [task profile](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/issues/task-profile.ts) и [workflow](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/workflows/workflow.ts) задают поля и проверки; создание карточки или preview не равны запуску. Решения и разрешения относятся к конкретной операции и её состоянию. Выбор App или BYOK не означает автоматического переключения на другой route; доступность host и provider требует собственной проверки. Related tests: [workflows](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/workflows.test.mts), [decisions](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/decisions.test.mts), [recipe runtime](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/recipe-runtime.test.mts).

## 3. Проверить и принять результат

После исполнения пользователь просматривает наблюдаемые файлы и артефакты, статус проверки, версию источника и gaps. Manual check фиксирует наблюдение отдельно от owner acceptance. Если данные устарели, покрытие неполно или операция требует восстановления, требуется соответствующее действие, а не автоматический success. В [коде команды приёмки](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/tasks/user-commands.mts) проверяются revision, критерии, состояние workflow и связанный check; условия конкретного маршрута остаются владельцем результата. Следующие проверки полноты маршрута и human usefulness принадлежат F19 и F23, а синхронизация отображаемой свежести — F18.

## 4. Перейти от файлов к карте и БД — planned

Будущий маршрут Files → Map → Database → code usages → source описан в [F19 и F26–F34](../planning/functional-remediation-2026-11-15.md). Сначала нужны inventory/scan contracts и PoC, затем выбранные adapters, UI и evidence. Исследования FUNC-G02 закрыты: dependency-cruiser bounded_adopt для imports; codebase-memory-mcp reject текущего Windows profile; tbls reject для authoritative SQLite metadata, с явной Node metadata alternative. Изолированная V3-навигация прошла22 browser checks. Это измеренные решения PoC; production integration остаётся F14/F33/F34. Никакая страница этого сценария не подтверждает, что target database подключена или её схема прочитана.

Known limitations: historical receipts отражают конкретные версии и окружения; current host, human acceptance, доступность provider и коммерческий выпуск не проверяются этой картой. Для следующего изменения используйте [capability traceability](capabilities.md) и конкретную task card.
