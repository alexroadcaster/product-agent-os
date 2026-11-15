# Данные, redaction и retention

Source status: repository_source / static_source_review; 15.11.2026.

Владелец: security/runtime owner + docs-maintainer. Область: исходники PAOS на `259977f3b257ba7fc0e932396f8963262bd327ad`; обновлять при изменении guards, tests или policy. Ссылки на тесты обозначают маршруты проверки, а не новый прогон. Реальные профили, credentials и provider-вызовы не исследовались.

## Классы данных и доказательств

[persisted redaction](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/redaction/persisted.mts) фильтрует известные формы credentials и скрытые сообщения в обрабатываемых значениях. Это ограниченный фильтр, не гарантия обнаружения всех secrets или PII; исходные байты могут существовать в других местах. [project-sources](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/adapters/project-sources.ts) и [app-agent-files](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/runtime/app-agent-files.mts) имеют собственные правила исключения/redaction, а broker хранит приватный набор ранее использованных secrets для обработки поздних кадров. Не выводите из redacted DTO обещание универсального удаления или очистки всех логов.

[snapshot](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/storage/snapshot.mts) создаёт проверяемый backup БД и связанных blobs, но исключает credentials, repository files, runtime threads и runtime auth store. Rotation candidates не означают удаление; restore и отдельное prune имеют самостоятельные условия. Подробнее [backup/restore](../db/backup-restore.md); [backup tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/storage-backup.test.mts) — synthetic тестовый маршрут.

[Privacy/supply-chain/retention](../product-agent-os/privacy-supply-chain-retention.md) — владелец правил evidence: только минимальные сведения; raw scanner findings по умолчанию не сохраняются без решения о сроке, redaction и cleanup. Эта политика evidence не определяет автоматический срок удаления всех пользовательских данных. Резервные копии, local DB, OS credentials и внешние провайдеры имеют разные границы; для удаления и retention конкретного deployment нужны отдельные evidence и authority. Реальные профили не исследовались.
