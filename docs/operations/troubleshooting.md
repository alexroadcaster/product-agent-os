# Диагностика без потери данных

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: runtime/operations owner + docs-maintainer. Область: local desktop package на `259977f3b257ba7fc0e932396f8963262bd327ad`; обновлять при изменении launcher, CLI, snapshot или release gates. Ссылки на тесты — маршруты проверки, не новый прогон. Реальные профили, credentials и provider не исследовались.

Начните с redacted кода ошибки, releaseId, версии, времени и описания операции. Не включайте pairing codes, credentials, содержимое профиля или полный приватный лог. Определите владельца запущенного экземпляра и состояние операции, прежде чем менять файлы. [Launcher](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/launcher/launcher.ts), [distribution](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/distribution.mts) и [desktop tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/desktop-local.test.mts) — источники и связанные тесты, не доказательство текущего состояния.

| Симптом | Следующий шаг |
| --- | --- |
| `service_restart_required` | Штатно завершить прежний owned экземпляр через Quit, дождаться подтверждения и повторить старт с тем же профилем. Закрытие вкладки не заменяет Stop. |
| `PROFILE_RUNNING_OR_UNRESOLVED` / `SELECTION_BUSY` | Сверить владельца и завершение service/maintenance. Не удалять `service-instance` или `operation.lock` принудительно при неопределённом состоянии. |
| `SELECTION_CONFLICT` | Прочитать актуальный status и digest, проверить намеренный профиль и повторить выбор с этим digest только после сверки. |
| Ошибка integrity/hash/schema | Сохранить redacted код и исходный backup; проверить совместимость версии, releaseId и snapshot. Не изменять manifest или базу ради обхода отказа. |
| Нет подтверждения model access | Проверить выбранный route и состояние подключения по [LLM guide](../ai/llm/routes.md); открытие App или launcher не доказывает доступ к модели. |

Не удаляйте неизвестные файлы, профили или reservation как обычный шаг диагностики. Если Stop заблокирован или завершение неоднозначно, сохраните состояние и передайте расследование владельцу; не приписывайте успешное завершение. Для отдельного восстановления см. [backup и rollback](upgrade-rollback.md).
