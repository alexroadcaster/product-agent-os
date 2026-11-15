# Supply chain и граница выпуска

Source status: repository_source / static_source_review; 15.11.2026.

Владелец: security/runtime owner + docs-maintainer. Область: исходники PAOS на `259977f3b257ba7fc0e932396f8963262bd327ad`; обновлять при изменении guards, tests или policy. Ссылки на тесты обозначают маршруты проверки, а не новый прогон. Реальные профили, credentials и provider-вызовы не исследовались.

## Источники, зависимости и authority

[Privacy/supply-chain/retention](../product-agent-os/privacy-supply-chain-retention.md) владеет границей scoped evidence: версии, hashes и summary допустимы в рамках задания; vulnerability audit, полный SBOM, dependency remediation, внешнее сканирование и сохранение raw findings имеют отдельные approval/retention границы. Данный документ не запускает аудит, установку или исправление зависимостей. Для проверки реализации используйте [desktop tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/desktop-local.test.mts), [connection tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/connections.test.mts) и [карту тестов](../testing/index.md); прохождение функциональных тестов не заменяет supply-chain review.

[plugin manifest](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/plugins/product-agent-os/.codex-plugin/plugin.json) содержит декларацию `MIT`, одновременно отмечая отсутствие установленной готовности к распространению. [commercial review history](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/research/product-agent-os-web-auth-commercial-2026-11-09.md) фиксирует исторический commercial review и отдельные gates на ownership, route, privacy, notices/license, packaging и payer/support. Исторический review не доказывает закрытие gates сегодня и не устанавливает лицензионные права всех компонентов. Перед выпуском владелец должен сверить текущие источники, права, notices и решение по распространению; не выводите коммерческое разрешение из manifest или этой страницы.

Соседние границы: [Codex security](../codex/security.md), [retention](data-retention.md), [security model](threat-model.md). Никаких новых external writes, provider calls или publication authority здесь не предоставляется.
