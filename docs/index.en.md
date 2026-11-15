# Product-Agent OS

[Project plans and tasks](planning/index.md): current queues, historical plans and the subsystem documentation backlog.

Source status: repository_source (DG02 routing, 2026-11-15) + official/experiment (dated knowledge guides).

## Documentation entry points

| Goal | Route | Result |
| --- | --- | --- |
| Develop PAOS | [Development map and section owners](product/index.md) → [product model](product/overview.md) → [architecture](architecture/system-context.md) | Current contracts, code/test links and owning tasks |
| Use PAOS | [Plugin guides](product-agent-os/index.md) and [local Web/desktop pilot](web/pilot.md) | Supported actions and explicit limits |
| Learn Codex and methods | [Codex](codex/overview.md), [methods](methodologies/index.md), [agent systems](agent-systems/overview.md) | General guidance with its own sources |

Find backend/frontend/DB/AI through the [subsystem map](product/index.md); find current work in [plans](planning/index.md), without reading historical RUNLOG entries. Owner: docs-maintainer; routing reviewed 2026-11-15 for DG02. Update both languages and navigation when a section or implemented capability changes. Related checks: source documentation, strict MkDocs, site language/search and HTML links.

The platform-learning routes below retain their dated source verification; DG02 does not reverify every external platform claim.


Use these guides to complete a task with Codex, onboard an existing project, or design an agent application. User workflows checked against official documentation: **2026-11-05**. Availability depends on client, account, authentication and managed policy.

## Start with your task

| Goal | Start here | Result |
| --- | --- | --- |
| Complete or fix one task | [Surfaces](codex/surfaces.md) → [Workflows](codex/workflows.md) | Bounded scope, change, verification and result |
| Onboard a project | [Product-Agent OS](product-agent-os/index.md) → [workspace audit](playbooks/workspace-readiness-audit.md) | Read-only discovery and a reviewable staged proposal |
| Build an agent application | [Runtime choice](agent-systems/sdk-patterns.md) → [evals](agent-systems/evals-observability.md) | Explicit state/tool ownership and quality criteria |

An ordinary change does not require a new document set or a team. For complex work use the [Diagram atlas](diagrams/index.md), [lifecycle](product-agent/lifecycle.md) and [model migration](playbooks/model-migration.md). Model and reasoning selection: [current matrix](codex/models-and-reasoning.md).

## Implementation and evidence boundary

The repository implements Web/desktop, a local service with SQLite storage and explicit runtime routes, and a separate Python plugin with lifecycle skills, staged infrastructure, validators, graph/cockpit and eval fixtures. [Capabilities and evidence boundaries](product/capabilities.md) separate source implementation, dated verification and planned work. These surfaces do not establish hosted delivery, success on every project or production readiness.

Markdown sources, current source/configuration, command/runtime evidence and owner decisions establish facts. Generated `site/`, dashboards, graphs, cockpit and reports help navigation but do not replace that evidence.

## Sources and history

Official OpenAI material supports platform claims; project decisions are labeled separately. Community/experiment material does not become official guidance without verification. [Registry](sources/registry.md) · [insights](insights/index.md) · [current state and dated history](product-agent-os/control-plane-current-state.md).

Historical plans and source receipts retain their dates and do not replace current guides. Public guides explain goals, inputs, actions, expected results and limits.

External writes, Git publication, deployment, provider calls and hook/schedule activation require applicable authority. Documentation does not activate those capabilities.

## Public/Internal Documentation Boundary

Internal evidence pages preserve the source registry, packets, backlogs and verification records. Source of truth remains in Markdown source files, current code/configuration, observed checks and owner decisions. Historical records do not replace current guides.
