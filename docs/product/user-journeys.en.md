# User journeys

Source status: `repository_source / journey_map / static_review`, 2026-11-15.

**Owner:** product and Web/desktop owners. **Scope/version:** local journeys and future additions, DG02/2026-11-15. Update when project selection, task/workflow, decisions, evidence or visible errors change. Check contracts and owning tasks, not just UI labels.

These sequences describe intent and corresponding source contracts. They do not prove the entire journey was checked on the current device. Historical scenarios and limits remain in the [PRD](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-prd-2026-11-05.md); later statuses belong to the [Web plan](../planning/product-agent-os-web-task-manager-plan-2026-11-09.md) and [functional backlog](../planning/functional-remediation-2026-11-15.md).

## 1. Add a project and understand coverage

1. The user selects a local folder and confirms Add. Cancelling selection should not register a project; the local service checks root binding and identity.
2. In current source, a requested scan inventories fixed control-plane sources and rebuilds a bounded code index. A scan failure after committed registration returns partial with a reason instead of undoing successful Add. Individual files may be unavailable or excluded.
3. The user reads available sources and coverage without treating that list as a complete file directory. A file tree, managed background scan and shared inventory/discovery are future [F26–F29](../planning/functional-remediation-2026-11-15.md); the existing index does not implement them by itself.

Sources: [registration](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts), [fixed sources](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/adapters/project-sources.ts), [bounded scanner](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/code-index/sources.mts). Related tests: [project sources](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/project-sources.test.mts), [code index](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/code-index.test.mts).

## 2. Prepare and execute a task

The user creates or opens a task, clarifies value, scope, criteria, risks and dependencies, and selects an applicable workflow and runtime. The [task profile](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/issues/task-profile.ts) and [workflow](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/workflows/workflow.ts) define fields and checks; creating a card or preview is not execution. Decisions and permissions apply to a particular operation and its state. Choosing App or BYOK does not automatically switch to the other route; host and provider availability require their own checks. Related tests: [workflows](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/workflows.test.mts), [decisions](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/decisions.test.mts), [recipe runtime](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/recipe-runtime.test.mts).

## 3. Verify and accept a result

After execution, the user reviews observed files and artifacts, check status, source version and gaps. A manual check records an observation separately from owner acceptance. Stale data, partial coverage or an operation requiring recovery need the relevant action, not automatic success. The [acceptance command source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/tasks/user-commands.mts) checks revision, criteria, workflow state and the linked check; the conditions of the specific route own the result. Further end-to-end and human-usefulness checks belong to F19 and F23, while displayed freshness alignment belongs to F18.

## 4. Navigate from files to a map and DB — planned

The future Files → Map → Database → code usages → source journey is described in [F19 and F26–F34](../planning/functional-remediation-2026-11-15.md). Inventory/scan contracts and PoCs precede selected adapters, UI and evidence. FUNC-G02 research is closed: dependency-cruiser bounded_adopt for imports; codebase-memory-mcp reject for the current Windows profile; tbls reject for authoritative SQLite metadata, with an explicit Node metadata alternative. Isolated V3 navigation passed22 browser checks. These are measured PoC decisions; production integration remains F14/F33/F34. This journey does not establish that a target database is connected or its schema has been read.

Known limitations: historical receipts describe specific versions and environments; this map does not verify the current host, human acceptance, provider availability or commercial release. For a subsequent change use [capability traceability](capabilities.md) and the specific task card.
