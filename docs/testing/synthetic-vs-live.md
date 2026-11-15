# Synthetic, runtime и человеческая приёмка

Source status: repository_source / static_contract_review; DG06, 2026-11-15.

Владелец: verification owner + owner изменённого surface. Scope/version: repository `259977f3b257ba7fc0e932396f8963262bd327ad`; обновлять вместе с изменением маршрута evidence. Источники: [TEST.md](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/TEST.md), [EVALS.md](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/EVALS.md), [behavioral evals](../product-agent-os/behavioral-evals.md), [frontend accessibility](../frontend/accessibility.md). Ссылки на тесты не означают нового запуска.

| Evidence | Поддерживаемый вывод | Ограничение и следующий шаг |
| --- | --- | --- |
| Source/static inspection | Что объявляют проверенные код и конфигурация на указанной ревизии | Сам по себе не подтверждает выполнение, загрузку host, настройки текущего пользователя или результат модели. |
| Unit/fixture/transcript | Assertions для конкретных входов, synthetic workspace и harness | Не доказывает качество реального проекта, model access, production readiness или корректность всего маршрута. |
| Synthetic browser/native или локальный сервис | Измеренное взаимодействие в описанном fixture окружении | Указать launcher, браузер, профиль, сценарии и ограничения; не заявлять реальную учётную запись или человеческую приёмку. |
| Actual runtime/provider | Наблюдаемый маршрут и результат в указанном окружении и разрешённом scope | Требует evidence selector, intended/prior path и fallback при релевантной смене маршрута; не распространяется на другие окружения или будущие runs. |
| Human acceptance | Что проверил конкретный владелец/пользователь и какой результат принял | Не заменяет технические негативные проверки, security review или release qualification. |

Для каждого результата сохраняйте дату, revision и изменённые входы, command/scenario, environment, test data class, outcome, failures и ограничения. Привязывайте результат к неизменным inputs; когда код, config, fixtures, dependencies, данные или среда влияют на результат, выбирайте повторную проверку по TEST. `not_run`, `blocked`, `failed` и `not_available` — разные состояния. Невыполненные случаи и неизвестные метрики не становятся нулём или success.

## Исторические и нестабильные результаты

[DG01](../planning/documentation-architecture-2026-11-15.md#dg01-results) сохранила дату и первоначальные миграционные failures: archive assertions для отсутствовавших EN siblings и исторического PostToolUse; site checks для EN/search parity и strict build имели исходные ошибки. Позже DG01 исправила источники и тестовые ожидания с обоснованием и записала повторный результат. Нельзя выдавать ранний failure за текущий или исторический ретест за новый прогон DG06. Изменение hook trust не было способом закрытия.

[DG02](../planning/documentation-architecture-2026-11-15.md#dg02-results) зафиксировала аварии начальных Chrome/Edge попыток render в sandbox и последующий ограниченный успешный render в другом запуске. Это не подтверждает детерминизм всех браузеров. Сохраняйте оба receipts и условия; при повторяемом или подозреваемом flaky результате укажите частоту/условия, owner и следующий воспроизводимый шаг. Не переименовывайте неизвестную причину в flaky и не удаляйте failure ради зелёного итога. Если путь недоступен или разрешение отсутствует, фиксируйте blocked и влияние на итоговую приёмку.

Сценарии ручного screen-reader и полной WCAG-оценки не подтверждены в [frontend guide](../frontend/accessibility.md); визуальное V3 evidence имеет `needs_user_acceptance`. Такие пробелы не закрываются passing synthetic browser tests. Утверждения о выпуске и production требуют отдельной квалификации и решений владельца.
