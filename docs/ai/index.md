# AI и агенты Product-Agent OS

Source status: repository_source / static_source_review; 15.11.2026.

Владелец: runtime/agent owner + docs-maintainer. Область: реализация PAOS на `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении селектора, gateway, контрактов, границ исполнения или связанных тестов. Описанные тесты — маршруты проверки, не новый прогон; фактическая активация и human acceptance требуют отдельного evidence.

## Две разные поверхности

[main.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/main.mts) связывает Web local service с [route-selector.ts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/route-selector.ts), App gateway и отдельным локальным API gateway. Этот runtime работает с project/session/binding, выбранным route и явно подключённым consumer. Код и статус подключения не доказывают успешный запуск модели. [Оркестрация](agents/orchestration.md), [контекст](agents/context.md), [инструменты и approvals](agents/tools-approvals.md), [сессии](agents/sessions.md) описывают эту поверхность.

Packaged Python plugin содержит lifecycle skills и staged templates, например [workspace-discovery-auditor/SKILL.md](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md) и [staged agent templates](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/assets/templates/agents/architect.toml). Это локальные управляющие и предложенные target assets, а не Web worker и не доказательство установленного/запущенного subagent. [Архитектура plugin](../product-agent-os/architecture.md) и [общий справочник](../agent-systems/subagents-skills.md) сохраняют свои области. Общие советы не заменяют текущие runtime-контракты.

## Дальнейшие входы

[LLM routes и контракты](llm/index.md), [retrieval и RAG](rag/index.md), [code intelligence](../code-intelligence/index.md), [API](../api/index.md) и [backend recovery](../backend/recovery.md). F26–F34, live providers и автономная hosted delivery не следуют из наличия этих файлов. [runtime-route-selector.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/runtime-route-selector.test.mts) и [app-agent-gateway.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/app-agent-gateway.test.mts) описывают связанные проверки, но здесь не запускаются.
