# Модель угроз и границы доверия

Source status: repository_source / static_source_review; 15.11.2026.

Владелец: security/runtime owner + docs-maintainer. Область: исходники PAOS на `259977f3b257ba7fc0e932396f8963262bd327ad`; обновлять при изменении guards, tests или policy. Ссылки на тесты обозначают маршруты проверки, а не новый прогон. Реальные профили, credentials и provider-вызовы не исследовались.

## Поверхности

| Граница | Защита в исходниках | Остаточный риск |
| --- | --- | --- |
| Browser → local service | [application](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/http/application.mts) использует [session-gate](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/http/session-gate.mts): loopback origin, host, session и CSRF для мутаций | Локальный доступ не равен универсальной защите ОС; фактическое поведение требует проверок среды |
| App host → private channel | [App agent channel](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/runtime/app-agent-channel.mts) отделяет channel capability от browser cookie | Заявленный host identity не является криптографической аттестацией |
| Agent → команда | [gateway](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/runtime/app-agent-gateway.mts) проверяет привязку и approval; [sandbox broker](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/runtime/sandbox-broker.mts) исполняет mediated commands | Broker не ограничивает все собственные инструменты App host |
| Project → source | [project-sources](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/adapters/project-sources.ts) проверяет canonical root и identity; [app-agent-files](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/runtime/app-agent-files.mts) ограничивает чтение файлов задачи | Каждая поверхность имеет собственную область checks; это не универсальный filesystem sandbox |

Содержимое проекта, prompt и внешние результаты рассматриваются как данные, а не право менять permissions. Предложение команды, approval и её завершение — разные события. Stop активной операции может быть cooperative и не доказывает немедленную остановку. [gateway tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/app-agent-gateway.test.mts), [channel tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/app-agent-channel.test.mts), [project source tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/project-sources.test.mts), [file tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/app-agent-files.test.mts) — связанные тесты; для live enforcement нужны наблюдения выбранной конфигурации.

Смежные контракты: [tools/approvals](../ai/agents/tools-approvals.md), [Codex platform](../codex/security.md). Здесь не утверждается защита от произвольного локального администратора или production readiness.
