# Supply chain и граница выпуска

Source status: repository_source / static_source_review; 15.11.2026.; FUNC-G05 locally_verified_with_explicit_limits, 16.11.2026.

Владелец: security/runtime owner + docs-maintainer. Область: исходники PAOS на `259977f3b257ba7fc0e932396f8963262bd327ad`; обновлять при изменении guards, tests или policy. Ссылки на тесты обозначают маршруты проверки, а не новый прогон. Реальные профили, credentials и provider-вызовы не исследовались.

## Источники, зависимости и authority

[Privacy/supply-chain/retention](../product-agent-os/privacy-supply-chain-retention.md) владеет границей scoped evidence: версии, hashes и summary допустимы в рамках задания; vulnerability audit, полный SBOM, dependency remediation, внешнее сканирование и сохранение raw findings имеют отдельные approval/retention границы. Данный документ не запускает аудит, установку или исправление зависимостей. Для проверки реализации используйте [desktop tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/desktop-local.test.mts), [connection tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/connections.test.mts) и [карту тестов](../testing/index.md); прохождение функциональных тестов не заменяет supply-chain review.

[plugin manifest](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/plugins/product-agent-os/.codex-plugin/plugin.json) содержит декларацию `MIT`, одновременно отмечая отсутствие установленной готовности к распространению. [commercial review history](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/research/product-agent-os-web-auth-commercial-2026-11-09.md) фиксирует исторический commercial review и отдельные gates на ownership, route, privacy, notices/license, packaging и payer/support. Исторический review не доказывает закрытие gates сегодня и не устанавливает лицензионные права всех компонентов. Перед выпуском владелец должен сверить текущие источники, права, notices и решение по распространению; не выводите коммерческое разрешение из manifest или этой страницы.

Соседние границы: [Codex security](../codex/security.md), [retention](data-retention.md), [security model](threat-model.md). Никаких новых external writes, provider calls или publication authority здесь не предоставляется.

## FUNC-G05 — реализованные контракты

F12 внешний поиск включается явно. Единственный текущий адаптер — openai/plugins, пакет superpowers, pinned commit d420d13051bffe4543ed39e30fa46b87148e47dd. Старый openai/skills deprecated и не используется. Фиксированные anonymous GET с credentials=omit, без query/project text, redirects/auth fallback/install/hooks; локальный каталог сохраняется при отказе. Проверяются Git blob SHA1, raw SHA256, фактический MIT LICENSE, manifest, truncated tree, mode/path, byte/count/deadline budgets. Импортирует выбранный SKILL.md, допустимые локальные text companions и точный agents/openai.yaml как opaque UTF-8 metadata; executable/binary/out-of-scope dependencies отклоняются. Provenance, revision, hashes и LICENSE.source.txt входят в проектную managed copy. Preview→явное Apply не означает native activation и не повышает доверие инструкций. [Проверенный upstream](https://github.com/openai/plugins/tree/d420d13051bffe4543ed39e30fa46b87148e47dd/plugins/superpowers).

Текущие focused evidence и оставшаяся квалификация: [FUNC-G05](../planning/functional-remediation-2026-11-15.md#func-g05-results).
