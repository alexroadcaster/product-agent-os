# Developing Product-Agent OS

Source status: repository_source / current_source_inspection / documentation_implementation; DG02/DG03/DG04/DG05, 2026-11-15.

Owner: docs-maintainer; domain owners below. Scope: documentation routing for Web/desktop, local service and Python plugin at `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Review this map when a section, contract, task owner or capability changes.

## Three entry points

- Develop PAOS: this map → [product overview](overview.md) → [architecture](../architecture/system-context.md) → the owning source/test/task.
- Use PAOS: [plugin/operator guides](../product-agent-os/index.md), [Web pilot](../web/pilot.md), [accessibility](../web/accessibility.md).
- Learn Codex and methods: [Codex](../codex/overview.md), [methods](../methodologies/index.md), [agent systems](../agent-systems/overview.md). General methods are not evidence of PAOS runtime capabilities.

## Find a subsystem

Existing source-backed entry points are available now. Backend, API and DB guides are provided by DG03, frontend by DG04; AI, LLM, retrieval and code-intelligence guides are provided by DG05. All task IDs below resolve through the [documentation plan](../planning/documentation-architecture-2026-11-15.md) or [functional plan](../planning/functional-remediation-2026-11-15.md).
| Area | Current guide | Source entry | Detailed guide owner / queue |
| --- | --- | --- | --- |
| Backend / API | [Local service](../backend/index.md), [API reference](../api/index.md) | [HTTP application](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts) | DOCS-04/05, DG03 |
| Frontend / UI | [Frontend map](../frontend/index.md), [navigation](../frontend/navigation.md) | [App.tsx](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/web/src/ui/App.tsx) | DOCS-06, DG04 |
| DB / SQLite | [SQLite schema](../db/schema.md), [data lifecycle](../db/index.md) | [Schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts) | DOCS-07, DG03 |
| AI / agents / LLM | [AI/agents](../ai/index.md), [LLM routes](../ai/llm/routes.md) | [Route selector](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/route-selector.ts) | DOCS-08/09, DG05 |
| RAG / retrieval / code intelligence | [Retrieval](../ai/rag/index.md), [code intelligence](../code-intelligence/index.md) | [FTS search](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/search-queries.mts) | DOCS-10/11, DG05; FUNC-14/26–34 separate |

## Documentation ownership and updates

| Sections | Purpose | Responsible role | Authoritative source / entry | Update trigger |
| --- | --- | --- | --- | --- |
| `product/` | Current PAOS model, capabilities and journeys | product-manager | Contracts and code; [capabilities](capabilities.md), [tasks](../planning/index.md) | Behavior or capability-status change |
| `architecture/`, `architecture/decisions/` | Component boundaries and decision rationale | architect | Source, accepted decisions and their evidence; [architecture](../architecture/system-context.md) | Process, authority, storage or route change |
| `backend/`, `api/`, `db/` | Service lifecycle, HTTP contracts, SQLite schema and recovery | backend/storage owner + docs-maintainer | [Backend](../backend/index.md), [API](../api/index.md), [DB](../db/index.md); linked source and tests | Module, endpoint, schema, transaction or recovery contract changes |
| `frontend/` | Screens, components, state and design consumption | frontend owner + docs-maintainer | [Frontend](../frontend/index.md), DESIGN, source and related tests | Screen, state, design or accessibility behavior changes |
| `ai/`, `code-intelligence/` | Agent execution, LLM contracts, retrieval and graph boundaries | runtime/graph owner + docs-maintainer | [AI](../ai/index.md), [code intelligence](../code-intelligence/index.md), linked code/tests | Route, prompt/output, indexing, query, provider gate or evidence change |
| `diagrams/` | Single atlas of execution paths and boundaries | architect + subsystem owner | Linked source-backed guide; [atlas](../diagrams/index.md) | Flow change; check diagram and RU/EN together |
| `product-agent-os/`, `web/` | Plugin usage, Web accessibility and local pilot | docs-maintainer + implementation owner | [Plugin guides](../product-agent-os/index.md), [pilot](../web/pilot.md), current code and dated receipts | Command, UI, installation or limit change |
| `product-agent/`, `playbooks/` | Working methods and repeatable user routes | lifecycle-orchestrator | Workflow/skill source; [lifecycle](../product-agent/lifecycle.md) | Route or responsibility change |
| `codex/`, `runtime/`, `agent-systems/`, `prompting/` | Knowledge base for Codex and agent design | research-source-analyst + docs-maintainer | Official sources in the [registry](../sources/registry.md); project inferences labeled separately | External contract change; verify source and date |
| `methodologies/`, `artifact-templates/`, `templates/` | Methods and reusable examples | method owner + docs-maintainer | [Methods](../methodologies/index.md), canonical template source | Applicability or contract change; an example is not implementation |
| `planning/` | Queues, cards, dependencies and statuses | product-manager + task owner | Owning MD/JSON in the [catalog](../planning/index.md); root PLAN only routes | Scope, dependency, status or evidence change |
| `sources/`, `evidence/`, `release/`, `superpowers/` | Sources, dated checks and design decisions | check/decision owner + release-operator | Primary receipt/manifest/spec; [registry](../sources/registry.md) | New results add provenance; never relabel old evidence as fresh |
| `insights/` | Unverified community/experiment observations | research-source-analyst | [Insights](../insights/index.md) with trust_level/verification_status | New verification or source change |
| `assets/` | Site presentation and local assets | docs-maintainer | mkdocs.yml, asset source and licenses | Presentation change; build and relevant render checks |

Roles assign responsibility for this repository; they do not prove an agent is running. Each substantive page states its source status, scope/date, source/test links and limitations. Runtime behavior belongs to code plus applicable observed checks; task status belongs to its owning plan/JSON, and acceptance belongs to the owner decision.

## How to update documentation

1. Inspect the changed contract, current code, callers and relevant tests. Locate its canonical page in the table.
2. Update that page and its full RU/EN counterpart; add a status-qualified cross-link instead of a second independent requirement.
3. Update navigation and registry when routes or source-backed claims change. Preserve dated research, previous decisions and receipts; extract current guidance with provenance rather than deleting history.
4. Run the affected source/link/matrix checks. Navigation or rendered-content changes require an isolated strict build, language-link postprocess and site checks. Diagram changes additionally require the relevant parser/render check.
5. Record evidence in the owning task; close only its completed scope. Follow [the documentation queue](../planning/documentation-architecture-2026-11-15.md).

## Evidence and limits

DG02 maps existing implementation and writes documentation; it does not run live providers, prove all journeys, promote commercial release or implement FUNC/M5. New domains get a directory when substantive documents exist, not empty placeholders. Historical research/PRD remains available through the overview and ADR provenance. [Source registry](../sources/registry.md) and [diagram atlas](../diagrams/index.md) retain their authority.

Related checks: `tools/check_docs.py`, `tests/product_agent_os/test_product_agent_os_docs.py`, `tests/product_agent_os/site_checks.py`; documentation task matrices and HTML links are verified in the DG02 result section of the owning plan.
