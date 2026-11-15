# Prompt и output contracts

Source status: repository_source / current_source_inspection; DG05, 2026-11-15.

Владелец: runtime/LLM owner + docs-maintainer. Область: реализация PAOS на `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении route, prompt/output, credentials, budget или telemetry контрактов. Ссылки на тесты — маршруты проверки, не новый runtime-прогон.

## Инвентарь владельцев

| Surface / owner | Вход и instructions | Выход и gate |
| --- | --- | --- |
| [M1 recipe](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/m1-recipe.mts) + [coordinator](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/codex/coordinator.ts) | Fixed `m1_fixed_v1`, analyst/planner/builder по discussion/planning/execution; developerInstructions отдельно от JSON-quoted task/user data | Thread/turn correlated events, сообщения и evidence; завершение turn не означает owner acceptance |
| [App gateway team proposal](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-gateway.mts) | `team_proposal_generation_v1`, catalog/target/request как недоверенные данные, planning-only policy | Один JSON proposal или clarification; kind/action/target/content/dependencies/reason, отдельный preview/apply |
| [Skill generation](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/team/skill-generation.mts) | REQUIREMENTS revision/строки либо описание, existing skill metadata, stable generationKey | SKILL.md create с YAML name/description и requirementIds; либо noGap/reason, clarification; stale/invalid/duplicate_candidate не применяются молча |
| [Recipe step input](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-gateway.mts) | `bounded_recipe_step`, frozen step/task/pins, iteration/attempt и predecessorArtifacts | Correlated run/report; текст об успехе не является доказательством checks/Done |
| [Python extraction](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py) | Redacted graph + semantic index, approved `local_deterministic`, external calls false | Semantic node/edge/rationale proposals, review_required и fingerprints; не live generation |
| [Python provider gate](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_proposal_provider.py) | Approved redacted prompt schema/evidence IDs, governance и budget/eval policies | Structured JSON proposal contract/safety eval; canonical mutation forbidden, external call не выполняется этим builder |

## Context и валидация

`quotedTaskInput` редактирует и JSON-кодирует task context, ограничивает saved context 64 KiB и отделяет пользовательский текст от fixed instructions. Instructions не являются механизмом sandbox: фактические boundaries принадлежат runtime guards и host. [Контекст агентов](../agents/context.md), [tools/approvals](../agents/tools-approvals.md).

Skill generation сверяет current requirement digest до результата, проверяет schema/frontmatter и provenance, показывает preview, затем отдельный Apply проверяет digest и использует стабильный ключ. Автоматическая установка или применение model prose не следуют из completed run. App-side consumer требуется для этого пути.

Python extraction проверяет approval, graph/semantic fingerprints и генерирует proposals локально. Provider gate сохраняет `provider_enabled:false`, `accepted_for_canonical_graph:false`, запрещает raw source/secrets/absolute paths. `ready` означает готовность контракта, не сетевой вызов. [Retrieval boundaries](../rag/index.md).

Packaged [prompt-contract template](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/assets/templates/artifact-templates/prompt-contract.md) — шаблон целевого проекта, а не активный Web prompt. Fixture prompts также не доказывают production model call. Не копируйте полные инструкции в документацию как второго владельца; меняйте source и связанные evals в отдельном согласованном срезе.

Проверки: [M1 recipe](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/runtime-adapter-gateway.test.mts), [skill generation](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/skill-generation-artifacts.test.mts), [local extraction](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_llm_extraction.py), [provider gate](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_llm_proposal_provider.py). Ссылки — verification map; новые model/eval вызовы не выполнялись.
