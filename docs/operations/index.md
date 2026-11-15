# Локальная эксплуатация

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: runtime/operations owner + docs-maintainer. Область: local desktop package на `259977f3b257ba7fc0e932396f8963262bd327ad`; обновлять при изменении launcher, CLI, snapshot или release gates. Ссылки на тесты — маршруты проверки, не новый прогон. Реальные профили, credentials и provider не исследовались.

Начните с [подготовки и запуска](install-start-stop.md), затем изучите [профили](profiles.md), [обновление и rollback](upgrade-rollback.md), [диагностику](troubleshooting.md) и [границы выпуска](release-boundaries.md). [CLI](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/main.mts) и [distribution](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/distribution.mts) владеют исполняемым контрактом, [desktop-local tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/desktop-local.test.mts) — маршрутом проверок.

Сборка UI, упаковка, qualification, установка, обновление и выпуск — разные действия. Текущий раздел описывает их условия, не выполняет их и не выдаёт право на распространение. Старый пилот относится к конкретному окружению, а не к любому новому запуску. [Web pilot](../web/pilot.md), [безопасность](../security/index.md), [карта проверок](../testing/test-map.md).
