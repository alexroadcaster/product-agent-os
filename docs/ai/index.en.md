# AI and agents in Product-Agent OS

Source status: repository_source / static_source_review; 2026-11-15.

Owner: runtime/agent owner + docs-maintainer. Scope: PAOS implementation at `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when the selector, gateway, contracts, execution boundaries or related tests change. Linked tests are verification routes, not new runs; activation and human acceptance need separate evidence.

## Two distinct surfaces

[main.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/main.mts) wires the Web local service to [route-selector.ts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/route-selector.ts), the App gateway and a separate local API gateway. This runtime uses project/session/binding, a selected route and an explicitly attached consumer. Code or connection status alone does not establish a successful model run. See [orchestration](agents/orchestration.md), [context](agents/context.md), [tools and approvals](agents/tools-approvals.md), [sessions](agents/sessions.md).

The packaged Python plugin contains lifecycle skills and staged templates, including [workspace-discovery-auditor/SKILL.md](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md) and [staged agent templates](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/assets/templates/agents/architect.toml). These are local operating and proposed target assets, not the Web worker or proof that a subagent is installed or running. [Plugin architecture](../product-agent-os/architecture.md) and the [general guide](../agent-systems/subagents-skills.md) retain their own scope. General guidance is not the current runtime contract.

## Next entry points

[LLM routes and contracts](llm/index.md), [retrieval and RAG](rag/index.md), [code intelligence](../code-intelligence/index.md), [API](../api/index.md) and [backend recovery](../backend/recovery.md). F26–F34, live providers and autonomous hosted delivery do not follow from these files. [runtime-route-selector.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/runtime-route-selector.test.mts) and [app-agent-gateway.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/app-agent-gateway.test.mts) identify related checks, not a new run.
