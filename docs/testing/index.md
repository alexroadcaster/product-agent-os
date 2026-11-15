# Проверяемость Product-Agent OS

Source status: repository_source / static_contract_review; DG06, 2026-11-15.

Владелец: verification owner + docs-maintainer. Scope: Web, local service и packaged Python plugin на revision `259977f3b257ba7fc0e932396f8963262bd327ad`. Обновлять при изменении тестовых маршрутов или границы доказательств. Ссылки на проверки ниже показывают их владельцев и не означают новый запуск.

[TEST.md](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/TEST.md) владеет текущим выбором команд и условиями расширения. [EVALS.md](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/EVALS.md) владеет рубриками, thresholds и пределами выводов. Датированные результаты сохраняют исходный revision, environment и scope; при изменении значимых входов старый результат не становится текущим.

1. Выберите затронутый контракт и потребителей по [карте тестов](test-map.md), затем уточните текущий маршрут в TEST.
2. Определите, какие выводы допускают [synthetic, runtime и human evidence](synthetic-vs-live.md), и какие проверки остаются открытыми.
3. Для AI изменений задайте baseline, cases, thresholds и ограничения по [AI evals](ai-evals.md); для изменения документации — [проверки документации](documentation-checks.md).
4. Запишите реальные команды, результаты, revision, окружение, данные, сбои и residual risk в owning evidence artifact. Следуйте отдельным границам разрешений для выбранного действия.

При пропущенной проверке укажите `not_verified` или `blocked` с причиной и следующим действием. Passing test проверяет только свои assertions и setup; он не устанавливает автономную работу на чужом проекте или готовность к выпуску. Связанные источники: [behavioral evals](../product-agent-os/behavioral-evals.md), [retrieval evaluation](../ai/rag/evaluation.md), [frontend accessibility](../frontend/accessibility.md). Общие product claims требуют соответствующих фактических проверок, owner review и, где применимо, человеческой приёмки.
