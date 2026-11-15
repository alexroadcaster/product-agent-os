# System context

Source status: repository_source / static_architecture_map; 2026-11-15.

Owner: Product-Agent OS architecture; scope/version: DG02 v1. Update when the cited sources, data boundaries or decisions change; related tests are listed below. Source inspection does not prove runtime activation or release readiness.

The user works in the Web SPA through the local service; the launcher manages local startup and the profile. Implementation and package contents are described in the [desktop contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/desktop-local/README.md). Source and the binding of a specific installation matter more than the existence of a diagram.

| Actor / boundary | Responsibility | Source and limit |
| --- | --- | --- |
| User and browser | Projects, tasks, documents and requests | [React App](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/web/src/ui/App.tsx); the UI does not grant arbitrary write authority |
| Local service | HTTP, session, domain operations and routing | [application](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts), [startup](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/main.mts); authority is not automatically inherited from the UI |
| Profile and project workspace | Profile SQL state and separate source files | [source adapter](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/adapters/project-sources.ts); authority depends on project mode |
| Codex App and API BYOK | Distinct explicitly selected runtime routes | [selector](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/route-selector.ts); no automatic switch to the other route |
| Python plugin | Separate discovery, staged infrastructure and lifecycle package | [plugin README](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/plugins/product-agent-os/README.md); not every Web request is asserted to invoke Python |

The [atlas diagram](../diagrams/paos-application-architecture.md) maps connections. Runtime, permission and model availability depend on the environment; a local package does not prove hosted delivery or standalone operation with Codex App closed.

**Tests and source:** [route selector test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-route-selector.test.mts), [project sources test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/project-sources.test.mts), [historical architecture](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-architecture-2026-11-05.md). The history includes superseded choices; see the [decision index](decisions/index.md).
