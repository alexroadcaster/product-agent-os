# Backend: жизненный цикл local service

Source status: repository_source / static_source_review + bounded_native_synthetic_verified; 15.11.2026.

Владелец: backend/local-service и runtime owner. Scope/version: DG03, `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Обновлять при изменении startup, session admission, route selection или shutdown.

## Запуск и admission

1. [main.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/main.mts) экспортирует `startLocalService`: импорт не создаёт server, базу, GUI или runtime child. Исполняемый entrypoint требует launcher IPC и профиль/instance ID. Профиль должен быть абсолютным локальным путём, identity привязывается до открытия `state.sqlite`.
2. Создаются store, runtime gateways, selector, recipes и scheduler; HTTP listener привязывается к случайному порту `127.0.0.1`. Код проверяет Host, origin, target и ограничивает размеры запросов. Health сообщает `alive` и отдельно `runtimeCapable`; первое не доказывает второе.
3. [session-gate.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/session-gate.mts) хранит sessions в памяти: restart и повторный pairing инвалидируют прежние cookies. Mutation требует origin и CSRF; exact origin/host проверяется и на read. Direct navigation bootstrap и pairing — разные пути входа в общий session contract.
4. [route-selector.ts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/route-selector.ts) сериализует connect/disconnect/runtime actions; default — `codex_app_agent` при отсутствии явного route и API key, наличие `apiKey` при отсутствии route выбирает `local_api_byok`. Переключение занятого route требует disconnect; implicit fallback отсутствует. Наличие App route не означает, что consumer подключён.

## Квалификация native runtime — FUNC-01

Текущий checkout проверяется по exact tuple в `packages/contracts/runtime/qualified-manifest.json`: Codex binary, Node binary/version, Windows release/arch, SQLite, adapter sources и Web lockfile. Изменение UI dependencies может изменить lockfile и остановить native broker с `package_lock_mismatch` даже при неизменном adapter. Обновлять pin без новой квалификации нельзя.

15.11.2026 исходный mismatch воспроизведён. Явный `sandbox-broker-acceptance.mts --run-once --candidate-inspection --binary <verified-local-binary>` проверил candidate на disposable roots, после чего manifest обновлён; повтор без candidate mode прошёл через production loader. Execution записывает внутри разрешённого root, outside/private temp получают `EPERM`; Discussion и Planning не записывают. Подмена binary, lockfile или adapter отклоняется до spawn. Первый отказ executor (`native MXC unavailable`) сохранён отдельно от успешного native прогона.

Это bounded native offline evidence без provider/model calls и human acceptance. После любого изменения pinned source нужен новый candidate receipt и повтор production admission. Карточка [PAOS-FUNC-01](../planning/functional-remediation-2026-11-15.md#task-paos-func-01) владеет актуальными receipts; Повторная квалификация после F08 выполнена на итоговых исходниках; final receipts указаны в карточке.

## Завершение

При `quit()` сервис сначала отклоняет новые запросы и отзывает sessions, отменяет собственный desktop dialog и начинает закрытие HTTP server. Затем закрываются scheduler и recipes, дренируется selector, закрываются gateways/channel. HTTP requests дренируются до закрытия store — это защищает незавершённые import/restore handlers. Повтор `quit` использует одну pending promise; ошибки сохраняют возможность повторной попытки, а не доказывают полный останов.

[supervisor/lifecycle.ts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/supervisor/lifecycle.ts) — отдельный supervisor contract: при неизвестном drain требуется durable recovery receipt до stop children; failure возвращает `stop_blocked`, подтверждённый drain — `stopped`, неизвестный после записи — `stopped_recovery_required`. Не смешивайте этот контракт с доказательством его исполнения в конкретном host-сеансе.

## Проверки и ограничения

[runtime-route-selector.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-route-selector.test.mts), [runtime-adapter-shutdown.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-adapter-shutdown.test.mts), [runtime-sqlite.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-sqlite.test.mts) — связанные тесты; их ссылки не являются текущим прогоном. Проверить фактическую активацию конкретного маршрута можно только с авторизованным runtime evidence. Эта страница не подтверждает сетевую изоляцию произвольных native clients или доступ к provider.
