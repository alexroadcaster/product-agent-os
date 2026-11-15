# Product-Agent OS product

Source status: `repository_source / product_contract / static_review`, 2026-11-15.

**Owner:** product and the Web/desktop and plugin owners. **Scope/version:** local product and its boundaries, DG02/2026-11-15. Update when the user problem, supported route, authority or delivery status changes; do not copy source requirements and cards into an independent queue.

Product-Agent OS helps manage development with Codex: identify project state, define work, prepare a bounded route, retain decisions and relate results to checks. Web/desktop offers projects, tasks, sessions, decisions and results; the Python plugin supplies separate local discovery, lifecycle, staging and verification tooling. The presence of both packages does not prove automatic delivery for every project or production readiness.

## Users and problem

The historical [PRD](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-prd-2026-11-05.md) describes a technically independent user or lead engineer returning to a project, defining AI work and needing to understand known facts, required decisions and trustworthy evidence. Its team scenario is a future-use hypothesis, not proof of shared access. This document does not measure the expected reduction in orientation time.

| Surface | Purpose | Current status owner |
| --- | --- | --- |
| Web/desktop + local service | Local project management, task manager, sessions, decisions and results | [Web plan and cards](../planning/product-agent-os-web-task-manager-plan-2026-11-09.md); [functional backlog](../planning/functional-remediation-2026-11-15.md) |
| Python plugin | Discovery, workflow, staged infrastructure and engineering evidence | [Plugin and boundaries](../product-agent-os/index.md), [plugin architecture](../product-agent-os/architecture.md) |
| Planned extensions | Address known gaps, Files/scan, graph and DB PoCs; separate M5 | [F01–F34](../planning/functional-remediation-2026-11-15.md), [M5](../planning/product-agent-os-web-task-manager-plan-2026-11-09.md#paos-m5) |

The Web plan retains historical local implementation and acceptance receipts. Check current source and the specific receipt before applying an old acceptance to a changed version or environment. The functional backlog records F01–F34 as `planned` on 2026-11-15; PAOS-0047/0052/0053 belong to the separate M5 plan. Plans own status and dependencies; this page does not maintain a competing copy.

## Model and routes

- [Domain model](domain-model.md): project, task, workflow, run, approval and evidence and their trust boundaries.
- [Capability map and traceability](capabilities.md): requirement → source contract → test/evidence → owning task.
- [User journeys](user-journeys.md): connect a project, prepare work, execute and accept it.
- [System architecture](../architecture/system-context.md) and [diagram atlas](../diagrams/index.md): component and source boundaries.

## Checks and limitations

Related tests: [project-sources.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/project-sources.test.mts), [task-profile.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/task-profile.test.mts), [workflows.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/workflows.test.mts). These are routes to verify contracts, not claims that tests ran when this page was written. Host/provider activation, AI quality, commercial readiness and human acceptance need separate current evidence.
