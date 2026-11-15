# Подготовка, запуск и остановка

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: runtime/operations owner + docs-maintainer. Область: local desktop package на `259977f3b257ba7fc0e932396f8963262bd327ad`; обновлять при изменении launcher, CLI, snapshot или release gates. Ссылки на тесты — маршруты проверки, не новый прогон. Реальные профили, credentials и provider не исследовались.

Команды ниже — справочник [desktop CLI](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/main.mts), а не результаты их запуска. Все пути — абсолютные локальные, без linked ancestors; package и install не размещают в node_modules. Предварительные условия host/runtime сверяются с manifest; не устанавливайте отсутствующие компоненты автоматически.

| Действие | Команда из корня checkout/package, содержащего `apps/` |
| --- | --- |
| UI build | `npm run build:web` в checkout с согласованными зависимостями |
| Package | `node apps/desktop-local/main.mts pack --source <source> --output <new-package>` |
| Verify | `node apps/desktop-local/main.mts verify --package <package> --expected-id <reviewed-id>` |
| Install | `node apps/desktop-local/main.mts install --package <package> --destination <new-install> --expected-id <reviewed-id>` |
| Выбор | `node apps/desktop-local/main.mts select --state <control> --install <install> --expected-id <reviewed-id> --profile <profile> --expected-selection none` для первого выбора |
| Статус / старт | `node apps/desktop-local/main.mts status --state <control>`; `node apps/desktop-local/main.mts start --state <control>` |

Перед verify независимо проверьте releaseId: self-hash пакета не устанавливает издателя. Destination для pack/install должен быть новым; install/profile/control не пересекаются. Последующие select требуют текущий digest из status вместо `none`, иначе conflict. После переноса CLI доступен внутри установленного каталога. [Distribution](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/distribution.mts), [launcher](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/launcher/launcher.ts), [тесты](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/desktop-local.test.mts).

Native launcher открывает браузер и запускает локальный сервис в рамках выбранного профиля. Закрытие вкладки не останавливает backend: используйте штатный **Quit** в приложении, дождитесь завершения owned service. Pairing/session данные не помещайте в URL или отчёты. Отказ host qualification, устаревший сервис или невыполненный Stop требуют диагностики, а не обхода проверок. См. [диагностику](troubleshooting.md) и [исторический pilot](../web/pilot.md).
