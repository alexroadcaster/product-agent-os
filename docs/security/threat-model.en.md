# Threat model and trust boundaries

Source status: repository_source / static_source_review; 2026-11-15.

Owner: security/runtime owner + docs-maintainer. Scope: PAOS source at `259977f3b257ba7fc0e932396f8963262bd327ad`; update with guards, tests or policy changes. Linked tests are verification routes, not a new run. No real profiles, credentials or provider calls were examined.

## Surfaces

| Boundary | Source-level protection | Residual risk |
| --- | --- | --- |
| Browser → local service | [application](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/http/application.mts) uses [session-gate](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/http/session-gate.mts): loopback origin, host, session and CSRF for mutations | Local access is not universal OS protection; effective behavior requires environment checks |
| App host → private channel | [App agent channel](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/runtime/app-agent-channel.mts) separates channel capability from browser cookie | Claimed host identity is not cryptographic attestation |
| Agent → command | [gateway](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/runtime/app-agent-gateway.mts) checks binding and approval; [sandbox broker](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/runtime/sandbox-broker.mts) executes mediated commands | Broker does not constrain every native tool of the App host |
| Project → source | [project-sources](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/adapters/project-sources.ts) checks canonical root and identity; [app-agent-files](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/runtime/app-agent-files.mts) bounds task-file reads | Each surface has its own checks; this is not a universal filesystem sandbox |

Project content, prompts and external results are data, not authority to change permissions. A command proposal, approval and completion are distinct events. Stop for an active operation can be cooperative and does not prove immediate termination. [gateway tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/app-agent-gateway.test.mts), [channel tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/app-agent-channel.test.mts), [project source tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/project-sources.test.mts), and [file tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/app-agent-files.test.mts) identify related tests; live enforcement needs observations of the selected configuration.

Related contracts: [tools/approvals](../ai/agents/tools-approvals.md), [Codex platform](../codex/security.md). This page does not claim protection against an arbitrary local administrator or production readiness.
